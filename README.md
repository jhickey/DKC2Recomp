# DKC2Recomp

> This recompilation is a byproduct of developing
> [snesrecomp](https://github.com/mstan/snesrecomp): the games are the proving
> ground, while the reusable framework is the larger goal. This is a community
> recompilation, not an official port. Please report any reproducible gameplay,
> video, or audio regressions.

A static recompilation of *Donkey Kong Country 2: Diddy's Kong Quest* (SNES)
into native desktop applications. The 65816 game program is translated to C
wherever analysis can prove an exact entry state, with the shared 65816
interpreter kept as a correctness and exceptional-path fallback. The rest of
the SNES (PPU, SPC700/S-DSP audio, DMA/HDMA, controllers and cartridge
mapping) is modeled by the shared `snesrecomp` runtime.

You must supply your own legally obtained ROM. No game content is included.

## Platforms

| Platform | Status |
| --- | --- |
| Windows x64 | Release builds: `DKC2Recomp.exe` (native host) and `DKC2RecompSDL.exe` (SDL host). |
| macOS (Apple silicon) | Release builds as an ad-hoc-signed `.app` (not notarized); may lag behind Windows features. |
| Linux | Builds from source with the SDL host; not yet a supported release. |

## Features

- **[Widescreen](docs/guide/video.md#aspect-ratio-widescreen)** (experimental):
  16:10, 16:9 and 21:9, drawn from the game's own level data, with the
  original 4:3 picture unchanged in the center.
- **[Display options](docs/guide/video.md)**: screen-color models,
  Reconstruct pixel-art scaling and a simulated CRT television.
- **[Simultaneous two-player co-op](docs/guide/co-op.md)**: TEAM mode where both
  players control their own Kong at the same time.
- **[Donkey and Kiddy Kong](docs/guide/characters.md)** as optional playable
  characters, from a pack you build from your own Project Kongs checkout.
- **[MSU-1 replacement music](docs/guide/msu1-music.md)** without patching the ROM.
- **[Assist Tools](docs/guide/overlay-and-settings.md#assist-tools)**: rewind,
  fast-forward and five save-state slots (off by default).
- Rebindable keyboard and controller input for two players, and
  [crash reports](docs/guide/troubleshooting.md) that leave out private data.

## Quick start

1. Download the latest Windows or macOS archive from
   [Releases](../../releases) and extract the complete archive.
2. Run `DKC2Recomp.exe` (Windows) or `DKC2Recomp.app` (macOS).
3. Select your North American v1.0 ROM in the launcher and choose **Play**.
   Press **Escape** in game for the pause menu and settings.

See [Installing and running](docs/guide/installing.md) for details, including
where settings and saves are stored.

## Supported ROM

| Property | Expected value |
| --- | --- |
| Region/version | North America v1.0 (`DIDDY'S KONG QUEST`) |
| Size | 4,194,304 bytes, headerless (a 512-byte copier header is accepted) |
| SHA-256 | `35421a9af9dd011b40b91f792192af9f99c93201d8d394026bdfb42cbf2d8633` |

ROMs, extracted graphics, music, level data, save files and generated
ROM-derived C are never distributed in this repository or its release
archives. The launcher includes the North American retail cover art solely
to identify the supported game; its source and copyright notice are in
[`recomp/launcher/README.md`](recomp/launcher/README.md).

## Documentation

| | |
| --- | --- |
| [User guide](docs/guide/index.md) | Installing, controls, settings, video, co-op, characters, music and troubleshooting. |
| [BUILDING.md](BUILDING.md) | Building from source, running tests and packaging. |
| [Developer docs](docs/README.md) | Architecture, hardware notes, implementation journal, roadmap and feature internals. |
| [CHANGELOG.md](CHANGELOG.md) | Changes by release; release notes are in [docs/releases](docs/releases/). |
| [AGENTS.md](AGENTS.md) | Contribution rules: content boundary, tests and documentation workflow. |

## Repository layout

- `runner/` - DKC2 host adapters: input, presentation, rewind, co-op and ROM checks.
- `src/`, `include/`, `app/` - the original bring-up core (ROM verification,
  65816 decoder/interpreter, HiROM bus, headless PPU, APU) and its
  `dkc2_verify` / `dkc2_analyze` / `dkc2_boot` tools.
- `recomp/` - source-owned CFG, symbol database and structural metadata.
- `snesrecomp/` - pinned shared recompiler and SNES runtime (submodule). It
  currently points at the `jhickey/snesrecomp` fork while a fix is upstreamed;
  `mstan/snesrecomp` is the authoritative upstream.
- `recomp-ui/` - pinned shared Dear ImGui launcher (submodule, `mstan/recomp-ui`).
- `config/` - compiled co-op tuning and developer-shortcut settings.
- `scripts/` - regeneration, testing, packaging and save tools.
- `tests/` - synthetic unit tests and private-ROM integration checks.
- `docs/` - user guide (`docs/guide/`) and developer documentation.
- `third_party/` - vendored components with their provenance and licenses.
- `generated/`, `private/` and build directories - ignored local artifacts.

## Acknowledgements

- [H4v0c21's DKC2 disassembly](https://github.com/H4v0c21/DKC2-disassembly)
  provides the independently verified symbols and structural boundaries used
  during analysis. No disassembly or ROM-derived assets are redistributed.
- [snesrecomp](https://github.com/mstan/snesrecomp) provides the static
  recompiler, interpreter fallback, and shared SNES runtime.
- [recomp-ui](https://github.com/mstan/recomp-ui) provides the shared Dear
  ImGui launcher.
- The optional screen-color LUT is adapted from
  [PSXRecomp](https://github.com/mstan/psxrecomp) at the pinned revision and
  implemented by the shared SNESRecomp color-LUT module. It retains its
  upstream license and JRickey/gba-recomp attribution under
  `third_party/psxrecomp_color_lut/` and in the submodule's matching
  `third_party/` notice directory.
- The SNES hardware implementation derives from LakeSnes, with additional
  algorithms credited to Snes9x in the relevant source files.
- The optional Donkey/Kiddy characters build on
  [DKC 2 Project Kongs](https://github.com/H4v0c21/DKC-2-Project-Kongs); see
  the [characters guide](docs/guide/characters.md#credits) for full credits.

## License

Project-owned source is available under the [MIT License](LICENSE). Vendored
dependencies and submodules retain their own licenses; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). In particular, the
PSXRecomp-derived screen-color component is PolyForm Noncommercial 1.0.0 with
an MIT/Apache-2.0 color-science lineage; the complete notices are in
`third_party/psxrecomp_color_lut/` and it is not relicensed by the root MIT
license. Nintendo and Rare own their respective game content and trademarks;
no license in this repository grants rights to that content.
