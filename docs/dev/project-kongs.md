# Donkey and Kiddy characters: verification

Player-facing setup lives in the [characters guide](../guide/characters.md).
This page covers the private comparison tooling and co-op checks.
Provenance is recorded in [third_party/project_kongs](../../third_party/project_kongs/README.md).

## Importer and runtime checks

Synthetic importer/runtime tests are included in CTest. Private comparisons:

```sh
python3 scripts/check_project_kongs.py \
  --runner build/macos/dkc2_snesrecomp_headless \
  --rom /private/path/dkc2.sfc \
  --pack /private/path/project-kongs.dkc2kongs \
  --states /private/path/saved-states \
  --output /private/path/kongs-check --frames 120
```

Optional `--input /private/path/recording.input`, `--aspect 4:3` (also 16:10
or 16:9), and `--choices 2,1` exercise motion, aspect and the reversed pair.
The checker compares WRAM, VRAM, CGRAM, OAM and audio fingerprints, rejects
unmatched visible compound layouts, and writes private images and logs.
Version 3 intentionally changes machine state during carry/throw and ground
attacks; v5 also changes team-throw release timing/origin. Disabling inherited
flight also changes active glide states. Use
recordings without those actions for the preservation check.
Those checks establish game-state preservation and sprite ownership, not
visual animation correctness. Inspect mounted idle, motion, jumps, landings
and both facing directions in the resulting images and the rebuilt app.
`DKC2_KONGS_PACK`, `DKC2_KONGS=1,2` (0 original, 1 Donkey, 2 Kiddy), and
`DKC2_KONGS_TRACE=1` support individual deterministic headless/desktop runs.

## Combined Windows co-op checks

Per-slot move state prevents the partner update from canceling a throw or
attack. Replacement callback ownership follows the existing simultaneous
co-op helpers. To replay both barrel kinds with Donkey/Kiddy enabled:

```
python scripts/check_coop_barrels.py --runner EXE --rom ROM --kongs-pack PACK
```

This checks P2 attachment, both throw directions, origin and recovery. It is
limited first-level coverage, not complete replacement-character acceptance.
