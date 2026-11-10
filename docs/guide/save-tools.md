# Save tools

## Unlocking every level in a save

`scripts/dkc2_unlock_levels.py` (from the source repository; needs Python 3)
marks every real level of a save file as cleared. That opens every path on
the world maps and every world whose boss it clears. It can also open the
Lost World and set coin counts.

**Quit the game before running it.** The game writes its own copy of the save
back when it exits. Afterwards, start from the file-select screen.

Example on macOS (adjust the paths for Windows, where saves live beside the
executable):

```bash
python3 scripts/dkc2_unlock_levels.py \
  --save "$HOME/Library/Application Support/Flat2VR/DKC2Recomp/saves/save.srm" \
  --rom /private/path/dkc2.sfc \
  --file all --lost-world --kremkoins 75 --banana-coins 99 \
  --snapshot "$HOME/Library/Application Support/Flat2VR/DKC2Recomp/saves/dkc2s0.sav"
```

The script backs up each file it changes beside the original first
(`.before-unlock`, numbered if a backup already exists).

| Option | Effect |
| --- | --- |
| `--save PATH` | The `save.srm` to change (required). |
| `--rom PATH` | Your DKC2 ROM, read only (required). |
| `--file 0\|1\|2\|all` | Which in-game save file to change (default `0`). |
| `--lost-world` | Marks every Klubba kiosk as paid, so Klubba lets the Kongs through without a toll, and records the five Lost World levels as beaten, which opens Krocodile Kore. |
| `--kremkoins N` | Sets the Kremkoin count (0-99). The kiosks charge 15 each, 75 in total. |
| `--banana-coins N` | Banana Coins are not stored in the save file (the game zeroes them whenever it loads one), so this sets them only in the save state named by `--snapshot`. |
| `--snapshot PATH` | The save state (for example `dkc2s0.sav`) that `--banana-coins` changes. |
| `--no-levels` | Leaves the level-cleared flags alone. |
| `--repair` | Recomputes the header of a save the game shows as empty because its checksums disagree, while its data is intact. |
| `--output PATH` | Writes the changed save here instead of changing it in place. |
| `--dry-run` | Reports what would change without writing anything. |

The completion percentage is recounted by the game the next time it saves.
