# Building DKC2Recomp

This page covers building from source, running the tests and packaging test
builds. Players who just want to play should download a release instead; see
the [user guide](docs/guide/index.md).

Building requires your own ROM: the game's C code is generated from it on
your machine and is never committed. See [Supported ROM](docs/guide/installing.md#supported-rom)
for the exact dump the build accepts.

## Prerequisites

| Platform | Requirements |
| --- | --- |
| Windows | CMake and Ninja; MSVC or MinGW-w64 (MSYS2); Python 3.9+; Rust/Cargo. An installed SDL2 package is optional. |
| macOS (Apple silicon) | Xcode Command Line Tools, CMake, Ninja, Python 3, Rust/Cargo and SDL2. |
| Linux | CMake, Ninja, a C/C++ toolchain, Python 3.9+, Rust/Cargo and SDL2. |

Rust/Cargo builds the native whole-program analyzer. If no SDL2 package is
found, the build fetches the pinned SDL 2.30.9 source, so `SDL2_DIR` is
optional.

Clone with submodules:

```sh
git clone --recurse-submodules https://github.com/elliotttate/DKC2Recomp
cd DKC2Recomp
```

The `snesrecomp` and `recomp-ui` submodule URLs are pinned in `.gitmodules`.

## Windows

```powershell
.\scripts\generate_snesrecomp.ps1 -Rom "C:\private\dkc2.sfc"

$env:Path = "C:\msys64\mingw64\bin;$env:Path"
cmake -S . -B build-snesrecomp -G Ninja `
  -DCMAKE_BUILD_TYPE=Release `
  -DDKC2_BUILD_SNESRECOMP=ON `
  -DSDL2_DIR=C:\msys64\mingw64\lib\cmake\SDL2
cmake --build build-snesrecomp --target dkc2_snesrecomp_desktop
```

This builds `DKC2Recomp.exe`. Target `dkc2_snesrecomp_sdl` builds the portable
host, `DKC2RecompSDL.exe`. Use `build-snesrecomp/` as the single routine
Windows build directory; [Build hygiene](docs/BUILD_HYGIENE.md) explains the
older `build*` folders.

To embed a private Windows `.ico` without adding it to Git, configure with
`-DDKC2_DESKTOP_ICON="C:\private\dkc2.ico"`.

Windows toolchain notes:

- Use a native Windows Python. The MSYS2/devkitPro `python` on `PATH` mangles
  Windows path arguments.
- MinGW gcc needs Windows-style `TMP`/`TEMP`; otherwise it falls back to
  `C:\Windows` and fails with permission errors.

## macOS app bundle

```sh
./build_macos.sh "/private/path/to/DKC2-USA-v1.0.sfc"
open build/macos/DKC2Recomp.app
```

The result, `build/macos/DKC2Recomp.app`, bundles its SDL2 library, carries
the project icon and is ad-hoc signed. It stores settings, saves and
diagnostics under `~/Library/Application Support/Flat2VR/DKC2Recomp`. The ROM
stays at its original path.

## Linux and other SDL builds

```sh
python3 scripts/generate_snesrecomp.py --rom /private/path/dkc2.sfc
cmake -S . -B build-release -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DDKC2_BUILD_SNESRECOMP=ON
cmake --build build-release --target dkc2_snesrecomp_sdl
./build-release/DKC2Recomp /private/path/dkc2.sfc
```

The SDL host is runtime-tested on Windows, and the macOS app bundle above is
built on it. Linux is not a supported release until its native acceptance
matrix passes; see
[Cross-platform desktop foundation](docs/CROSS_PLATFORM.md).

## Regenerating after source changes

Generated banks use `file(GLOB CONFIGURE_DEPENDS)`. After a regeneration adds
or removes `bank*_v2.c` files, reconfigure (`cmake -S . -B <build-dir>`) so the
new files are picked up; otherwise the link fails with missing-bank errors.

Release builds compile project-owned desktop and headless code for speed
(`-O3` with GCC/Clang, `/O2` with MSVC).

## Running the tests

Public tests use synthetic fixtures only:

```sh
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

or, for the core library without CMake:

```sh
make test
```

Private integration tests need your ROM and are enabled by passing its path
at configure time:

```sh
cmake -S . -B build -DDKC2_ROM=/private/path/dkc2.sfc
make verify-rom ROM=/private/path/dkc2.sfc
make boot-rom ROM=/private/path/dkc2.sfc
```

Further private regressions replay owner-supplied save states and input
recordings. Each is enabled by its own CMake cache variable pointing at an
external file, for example `DKC2_COOP_ROPE_STATE`, `DKC2_COOP_GOAL_STATE`,
`DKC2_PIRATE_PANIC_INPUT` / `DKC2_PIRATE_PANIC_SRAM` or `DKC2_STATE_CORPUS`.
List them all with their descriptions:

```sh
cmake -LH build | grep -B1 -E '^DKC2_(COOP|PIRATE|BRAMBLE|STATE)'
```

These files stay outside Git. Packaging tests (`make_release`,
`create_windows_version`) run on Windows only.

## Compiled configuration

Two configuration files are compiled into the executable. Rebuild after
editing them; restarting alone does not apply changes.

### Co-op tuning

[`config/coop_tuning.cfg`](config/coop_tuning.cfg) holds the simultaneous
co-op thresholds. The compiler rejects values outside the documented ranges.

| Setting | Default | Meaning |
| --- | --- | --- |
| DKC2_COOP_SELECT_HOLD_MS | 2000 | Select hold in milliseconds before teleport; rounded up to console frames |
| DKC2_COOP_STOMP_HORIZONTAL_PX | 32 | Maximum horizontal separation between simultaneous stompers |
| DKC2_COOP_STOMP_VERTICAL_PX | 32 | Maximum vertical separation between simultaneous stompers |

Private co-op checks assume the default tuning.

### Developer shortcuts

`config/developer.cfg` is compiled into the game. `DKC2_DEVELOPER_ENABLED=1`
enables developer tools; set it to `0` and rebuild to disable them. With the
default `DKC2_DEVELOPER_BEAT_LEVEL_KEY=8`, press **F8** during gameplay
to complete the current level, boss fight or bonus room. Normal levels and
bosses return to the world map; bonuses credit their reward and return to
the parent level, preserving the animal form. Use `0` to disable this shortcut,
or `1..12` to choose another function key, then rebuild. Menus, maps, death sequences
and an already-running exit reject the command. Rewards are credited once.
Special final-boss ending cinematics have not been verified. Windows and SDL hosts use
the same compiled policy; holding the key does not repeatedly trigger it.

## Symbols

Reverse-engineering knowledge is kept outside the generated C.
`recomp/symbols.toml` assigns reviewed names, aliases, confidence, provenance,
tags, and notes to stable USA v1.0 CFG addresses. `recomp/layouts.toml` records
confirmed WRAM objects and fields. `docs/SYMBOL_DATABASE.md` is the generated
readable index.

After editing either TOML file, validate and regenerate with Python 3.11+ (or
Python 3.9/3.10 with `tomli`):

```powershell
python scripts\build_dkc2_symbol_database.py --apply-cfg
python scripts\build_dkc2_symbol_database.py --check
python scripts\lookup_dkc2_symbol.py banana
```

The build tool imports all 3,314 structural CFG entries into an ignored JSON
index at `.cache/dkc2-symbols.json`, updates only exact-address CFG names, and
generates the constants consumed by widescreen diagnostics. Generated game C
remains ignored and must still be rebuilt from the user's verified ROM.

### Promoting names from a private symbol overlay

The checked-in `recomp/bank*.cfg` files already contain the active,
revision-validated disassembly names used in generated C and trace logs. A
private WLA symbol overlay can conservatively expand remaining `CODE_...`
names without copying the overlay into the repository:

```powershell
python .\scripts\promote_snesrecomp_symbols.py `
  --cfg-dir .\recomp `
  --symbols .\private\dkc2-yoshifanatic-v1.sym

# Review the dry run, then apply the same validated set.
python .\scripts\promote_snesrecomp_symbols.py `
  --cfg-dir .\recomp `
  --symbols .\private\dkc2-yoshifanatic-v1.sym `
  --apply
```

The tool only accepts an unambiguous `context_CODE_BBXXXX` alias that retains
the original generic identity. It rejects bank mismatches, collisions, and
ambiguous aliases; raw same-address matching is intentionally unsupported
because revision-dependent layout changes can shift dense dispatch tables.
Regenerate after applying so `recomp/funcs.h` and private generated C receive
the new names.

## Packaging test builds

Create the next source-clean, user-testable Windows snapshot with:

```powershell
.\scripts\create_windows_version.ps1
```

The first run creates `versions\Version 01`, the next creates
`versions\Version 02`, and so on. Existing numbered folders are never deleted
or overwritten. Each folder contains both playable Windows hosts, the required
launcher assets, documentation, and a `VERSION.txt` provenance/hash manifest.
Normal packaging refuses uncommitted source; `-AllowDirty` is available only
for an explicitly marked development snapshot.
The packager allowlists the documented launcher cover and refuses ROM, save,
generated, diagnostic, configuration, screenshot, and audio artifacts. The
compiler continues to reuse its normal build tree; only testable handoffs are
duplicated, avoiding multi-gigabyte source/build copies.

For private play testing, create a second copy outside the repository after
the normal version has been packaged:

```powershell
.\scripts\create_personal_test_version.ps1 `
  -PublicVersionDirectory "versions\Version 05" `
  -RomPath "C:\private\dkc2.smc" `
  -SavesDirectory "build-snesrecomp\Release\saves" `
  -LauncherConfigPath "build-snesrecomp\Release\launcher.cfg"
```

The helper verifies the exact supported ROM hash and, by default, creates
`..\DKC2 Personal Test Builds\Version NN` with a relative `rom.cfg`, the ROM,
the selected saves, and optional launcher settings. It refuses destinations
inside this repository and refuses to overwrite an existing private version.
These personal folders must never be committed, uploaded, or attached to a
release.

For the current widescreen investigation, a private diagnostic version can be
created directly without making a redundant public package:

```powershell
.\scripts\create_private_diagnostic_version.ps1 `
  -RomPath "C:\private\dkc2.smc" `
  -Sequence 10
```

It assembles the normal and trace executables, verified ROM, saves, existing
private recordings, launcher settings, control bindings, and capture helpers
outside Git. Its bundled `Record-Pirate-Panic.ps1` preserves starting SRAM,
refuses reused evidence names, and requires fresh performance, tier-2, and
last-run reports; `Diagnose-Frame.ps1` then creates an isolated same-frame
layer/object report. The focused Swanky validator is packaged under `tools/`.
See
[Build hygiene](docs/BUILD_HYGIENE.md) and the package's
`TESTING_README.md`.

Use `build-snesrecomp/` as the single routine Windows compiler workspace and
launch manual-test builds only from `versions/Version NN/`. The older
`build*` folders are explained and classified in
[Build hygiene](docs/BUILD_HYGIENE.md); they are not additional source
versions.

Public releases are packaged by `scripts/make_release.ps1`; release notes for
each version live in [`docs/releases/`](docs/releases/).

## Documentation site

The user guide in `docs/guide/` is published as a static site built with
[Zensical](https://zensical.org/) from `mkdocs.yml`. To preview it locally:

```sh
python3 -m pip install -r docs/requirements.txt
zensical serve          # http://localhost:8000
zensical build --strict # writes the ignored site/ folder; fails on broken links
```

CTest's `markdown_links_current` check (and the `docs` GitHub Actions
workflow) also verifies every relative link and heading anchor in the
repository's Markdown, and fails on files that are not valid UTF-8.

## Contributing

Read [AGENTS.md](AGENTS.md) before contributing. It sets out the content
boundary (no ROMs, extracted assets or save files in Git) and the required
test and documentation workflow. Developer documentation is indexed in
[docs/README.md](docs/README.md).
