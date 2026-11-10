# Installing and running

## Supported ROM

DKC2Recomp accepts exactly one ROM: the North American v1.0 release of
*Donkey Kong Country 2*. The launcher verifies it after removing an optional
512-byte copier header.

| Property | Expected value |
| --- | --- |
| Size | 4,194,304 bytes (headerless body) |
| CRC32 | `006364DB` |
| SHA-256 | `35421a9af9dd011b40b91f792192af9f99c93201d8d394026bdfb42cbf2d8633` |
| Internal name | `DIDDY'S KONG QUEST` |
| Region/version | North America v1.0 |

You must supply your own lawfully obtained dump. ROMs, extracted graphics,
music, level data and save files are never distributed with the project. The
ROM always stays at the path you choose and is never copied into the
application.

## Windows

1. Download the latest `DKC2Recomp-vX.Y.Z-Windows-x64.zip` from the project's
   Releases page and extract the **complete** archive.
2. Run `DKC2Recomp.exe`.
3. In the launcher, select your ROM and choose **Play**.

`DKC2RecompSDL.exe` is an alternate host built on SDL. Keep the bundled DLLs
and the `assets` folder beside both executables. The archive also contains
this guide, including the [character](characters.md) and
[MSU-1](msu1-music.md) setup pages; those packs are supplied separately.

Both Windows hosts have a **Game / View / Input** menu bar:

- **Game**: pause/resume and Quick Save/Load.
- **View**: aspect ratio, scaling, level edges, screen filters and fullscreen.
- **Input**: each player's Keyboard/Gamepad source and the TEAM co-op mode.

Changes apply while playing. **Alt+Enter** toggles fullscreen. **Escape**
leaves fullscreen when the overlay is closed and otherwise pauses or resumes.

## macOS (Apple silicon)

1. Download `DKC2Recomp-vX.Y.Z-macOS-arm64.zip` from Releases and extract it.
2. Open `DKC2Recomp.app` and select your ROM.

The Mac app is ad-hoc signed but not notarized. If Gatekeeper blocks it,
Control-click the app in Finder, choose **Open** and confirm once.

> Mac releases can lag behind Windows. Check the release notes for which
> features a given Mac build includes, or build the current source yourself
> (see `BUILDING.md` in the source repository).

The Mac app has an AppKit menu bar. Its Game menu's **Quick Save State** and
**Quick Load State** always use save-state Slot 1.

## Linux

There is no Linux release yet. The portable SDL host builds from source; see
`BUILDING.md` in the source repository.

## Where files are kept

| File | Contents |
| --- | --- |
| `rom.cfg` | Path to your selected ROM |
| `launcher.cfg` | Display, audio, controls, Assist Tools and co-op settings |
| `kongs.cfg` | Character choices and the character pack path |
| `msu1.cfg` | MSU-1 enablement, volume and folder |
| `saves/save.srm` | In-game cartridge save; the previous clean save is kept as `save.srm.bak` |
| `saves/dkc2s0.sav` ... `dkc2s4.sav` | Save-state Slots 1-5 |
| `diagnostics/` | Last-run report and support bundles |

On Windows these live beside the executable. On macOS they live in
`~/Library/Application Support/Flat2VR/DKC2Recomp`. In-game cartridge saves and
save states are separate: a save state never overwrites `save.srm`.
