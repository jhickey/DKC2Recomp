# DKC2Recomp user guide

DKC2Recomp runs *Donkey Kong Country 2: Diddy's Kong Quest* (SNES) as a native
desktop application. The game program is statically recompiled to C; the SNES
hardware around it is modeled by the shared
[snesrecomp](https://github.com/mstan/snesrecomp) runtime. It is a community
project, not an official port, and you must supply your own legally obtained
North American v1.0 ROM.

## Start here

- [Installing and running](installing.md): download a release, select your
  ROM and find where settings and saves are kept.
- [Controls](controls.md): default keyboard and controller layout, rebinding,
  and two-controller setup.
- [Pause menu and settings](overlay-and-settings.md): the in-game overlay,
  Assist Tools (rewind, fast-forward, save states) and Restore Defaults.

## Features

- [Video](video.md): widescreen aspect ratios, screen-color models,
  Reconstruct scaling and the CRT television display.
- [Two-player co-op](co-op.md): simultaneous TEAM mode, where both players
  control their own Kong at the same time.
- [Donkey and Kiddy characters](characters.md): optional replacement
  characters imported from your own Project Kongs checkout.
- [MSU-1 music](msu1-music.md): replacement soundtrack packs.
- [Save tools](save-tools.md): unlock every level in a save file.

## Help

- [Troubleshooting and crash reports](troubleshooting.md)
- [Environment variables](advanced.md) for one-off overrides and diagnostics

Report reproducible gameplay, video or audio regressions on the project's
issue tracker. Attach a [support bundle](troubleshooting.md#support-bundles)
when you can, after checking what it contains.
