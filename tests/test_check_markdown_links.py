import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_markdown_links.py"
SPEC = importlib.util.spec_from_file_location("check_markdown_links", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SlugTests(unittest.TestCase):
    def test_github_heading_rules(self):
        slug = MODULE.github_slug
        self.assertEqual(slug("Aspect ratio (widescreen)"), "aspect-ratio-widescreen")
        self.assertEqual(slug("Simultaneous co-op boundary"), "simultaneous-co-op-boundary")
        self.assertEqual(slug("`DKC2_ROM` and *tests*"), "dkc2_rom-and-tests")
        self.assertEqual(slug("2026-10-25 — F8 boss"), "2026-10-25--f8-boss")
        self.assertEqual(slug("See [the guide](guide.md)"), "see-the-guide")


class CheckerTests(unittest.TestCase):
    def run_checker(self, root: Path, *paths: str) -> tuple[int, str]:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
            code = MODULE.main(["--root", str(root), *paths])
        return code, stderr.getvalue()

    def write(self, root: Path, relative: str, text: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_valid_links_and_anchors_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write(root, "docs/guide.md",
                       "# Guide\n\n## Video settings\n\n## Video settings\n")
            self.write(root, "README.md", "\n".join([
                "# Title",
                "[guide](docs/guide.md) [section](docs/guide.md#video-settings)",
                "[duplicate](docs/guide.md#video-settings-1) [self](#title)",
                "[dir](docs/) [web](https://example.com/x.md) [route](../../releases)",
                "![image](docs/guide.md \"title\")",
                "",
            ]))
            self.assertEqual(self.run_checker(root), (0, ""))

    def test_missing_file_and_anchor_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write(root, "docs/guide.md", "# Guide\n")
            self.write(root, "README.md",
                       "[a](docs/missing.md)\n[b](docs/guide.md#nowhere)\n[c](#nope)\n")
            code, errors = self.run_checker(root)
            self.assertEqual(code, 1)
            self.assertIn("README.md:1: missing link target docs/missing.md", errors)
            self.assertIn("README.md:2: missing anchor #nowhere in docs/guide.md", errors)
            self.assertIn("README.md:3: missing anchor #nope in README.md", errors)

    def test_code_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write(root, "README.md",
                       "`[x](missing.md)`\n\n```md\n[y](missing.md)\n# Heading\n```\n")
            self.assertEqual(self.run_checker(root), (0, ""))

    def test_invalid_utf8_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "CHANGELOG.md").write_bytes(b"# Log\n\n## 2026 \x97 entry\n")
            code, errors = self.run_checker(root)
            self.assertEqual(code, 1)
            self.assertIn("CHANGELOG.md: not valid UTF-8", errors)

    def test_links_into_unchecked_out_submodules_are_skipped(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write(root, ".gitmodules",
                       '[submodule "lib"]\n\tpath = vendor/lib\n\turl = https://example.com/lib.git\n')
            self.write(root, "README.md",
                       "[a](vendor/lib/README.md) [b](vendor/libother.md)\n")
            code, errors = self.run_checker(root)
            self.assertEqual(code, 1)
            self.assertNotIn("vendor/lib/README.md", errors)
            self.assertIn("missing link target vendor/libother.md", errors)

    def test_excluded_directories_are_skipped(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write(root, "snesrecomp/README.md", "[x](missing.md)\n")
            self.write(root, "build-release/notes.md", "[x](missing.md)\n")
            self.write(root, "README.md", "# Ok\n")
            self.assertEqual(self.run_checker(root), (0, ""))


if __name__ == "__main__":
    unittest.main()
