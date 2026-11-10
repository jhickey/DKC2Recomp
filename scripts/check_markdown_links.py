#!/usr/bin/env python3
"""Check relative links and heading anchors in the repository's Markdown.

Every inline link or image whose target is a relative path must name an
existing file or directory. A ``#fragment`` on a Markdown target (or on the
current file) must match one of that file's headings, using GitHub's
heading-anchor rules. External URLs are not fetched. A relative target that
resolves outside the repository root (for example ``../../releases`` from the
README, which GitHub serves as a web route) is ignored, as is any target
inside a submodule listed in ``.gitmodules``, which may not be checked out.

Usage:
    check_markdown_links.py [--root DIR] [FILE_OR_DIR ...]

With no paths, every ``*.md`` file under the root is checked, except
submodules, build output and ignored private folders.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

EXCLUDED_DIRS = {
    ".git", ".cache", ".idea", ".vs", ".vscode", "build", "cmake-build-debug",
    "generated", "private", "recordings", "release-stage", "site", "versions",
    "diagnostics", "snesrecomp", "recomp-ui", "node_modules", "__pycache__",
}

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
# [text](target "title") and ![alt](target); target may be wrapped in <>.
LINK_RE = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*(<[^>]*>|[^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
HTML_ANCHOR_RE = re.compile(r"<a\s+(?:name|id)=\"([^\"]+)\"", re.IGNORECASE)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def github_slug(text: str) -> str:
    """Return the anchor GitHub generates for a heading's text."""
    text = INLINE_CODE_RE.sub(lambda m: m.group(2), text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> text
    text = re.sub(r"<[^>]+>", "", text)  # inline HTML
    text = text.strip().lower()
    out = []
    for ch in text:
        if ch in " -":
            out.append("-" if ch == " " else ch)
        elif ch == "_" or ch.isalnum():
            out.append(ch)
        elif unicodedata.category(ch).startswith(("L", "N", "M")):
            out.append(ch)
    return "".join(out)


def iter_content_lines(text: str):
    """Yield (line_number, line) outside fenced code blocks."""
    fence = None
    for number, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker[0] * 3
                continue
            if marker.startswith(fence):
                fence = None
                continue
        if fence is None:
            yield number, line


def anchors_for(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        anchors: set[str] = set()
        counts: dict[str, int] = {}
        text = path.read_text(encoding="utf-8", errors="replace")
        for _, line in iter_content_lines(text):
            for name in HTML_ANCHOR_RE.findall(line):
                anchors.add(name)
            match = HEADING_RE.match(line)
            if not match:
                continue
            slug = github_slug(match.group(2))
            seen = counts.get(slug, 0)
            counts[slug] = seen + 1
            anchors.add(slug if seen == 0 else f"{slug}-{seen}")
        cache[path] = anchors
    return cache[path]


def submodule_paths(root: Path) -> list[Path]:
    """Return the resolved paths of submodules declared in .gitmodules."""
    gitmodules = root / ".gitmodules"
    if not gitmodules.is_file():
        return []
    text = gitmodules.read_text(encoding="utf-8", errors="replace")
    return [(root / match.strip()).resolve()
            for match in re.findall(r"^\s*path\s*=\s*(.+)$", text, re.MULTILINE)]


def check_file(path: Path, root: Path, cache: dict[Path, set[str]],
               submodules: list[Path] | None = None) -> list[str]:
    errors = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return [f"{path.relative_to(root)}: not valid UTF-8 at byte {error.start}"]
    for number, line in iter_content_lines(text):
        scrubbed = INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)
        for match in LINK_RE.finditer(scrubbed):
            target = match.group(1).strip("<>")
            if not target or SCHEME_RE.match(target) or target.startswith("//"):
                continue
            location, _, fragment = target.partition("#")
            location = unquote(location.split("?", 1)[0])
            where = f"{path.relative_to(root)}:{number}"
            if location:
                resolved = (path.parent / location).resolve()
                try:
                    resolved.relative_to(root)
                except ValueError:
                    continue  # outside the repository: a hosting web route
                if any(resolved == sub or sub in resolved.parents
                       for sub in submodules or []):
                    continue  # submodule content may not be checked out
                if not resolved.exists():
                    errors.append(f"{where}: missing link target {target}")
                    continue
            else:
                resolved = path
            if fragment and resolved.is_file() and resolved.suffix.lower() == ".md":
                if unquote(fragment).lower() not in {a.lower() for a in anchors_for(resolved, cache)}:
                    errors.append(f"{where}: missing anchor #{fragment} in "
                                  f"{resolved.relative_to(root)}")
    return errors


def collect(paths: list[Path], root: Path) -> list[Path]:
    files: list[Path] = []
    for base in paths:
        if base.is_file():
            files.append(base.resolve())
            continue
        for candidate in sorted(base.rglob("*.md")):
            relative = candidate.resolve().relative_to(root)
            if any(part in EXCLUDED_DIRS or part.startswith("build-")
                   or part.startswith("_") for part in relative.parts[:-1]):
                continue
            files.append(candidate.resolve())
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root (default: this script's parent checkout)")
    parser.add_argument("paths", nargs="*", type=Path,
                        help="Markdown files or directories (default: the whole root)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    files = collect([p if p.is_absolute() else root / p for p in args.paths] or [root], root)
    cache: dict[Path, set[str]] = {}
    submodules = submodule_paths(root)
    errors = [error for path in files
              for error in check_file(path, root, cache, submodules)]
    for error in errors:
        print(error, file=sys.stderr)
    print(f"checked {len(files)} Markdown files: "
          f"{'no broken links' if not errors else f'{len(errors)} broken link(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
