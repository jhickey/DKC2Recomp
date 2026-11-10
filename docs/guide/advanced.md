# Environment variables

Environment variables override a saved setting for one run without changing
`launcher.cfg`. They are mainly useful for testing and bug reports. Set them
before launching, for example:

```sh
DKC2_ASPECT=16:9 /Applications/DKC2Recomp.app/Contents/MacOS/DKC2Recomp   # macOS
```

`open` does not pass environment variables to an app, so run the executable
inside the bundle directly, as above.

```powershell
$env:DKC2_SCREEN = "crt"; .\DKC2Recomp.exe            # Windows PowerShell
```

## Video

| Variable | Values | Effect |
| --- | --- | --- |
| `DKC2_ASPECT` | `4:3`, `16:10`, `16:9`, `21:9` | Aspect ratio. |
| `DKC2_WIDESCREEN` | `0`, `1` | Older switch: `1` selects 16:9. Ignored when `DKC2_ASPECT` is set. |
| `DKC2_WIDESCREEN_EDGE` | `glide`, `reflect`, `bars`, `shift` | [Level-edge policy](video.md#level-edge). |
| `DKC2_SCREEN` | `raw`, `crt`, `composite`, `trinitron` | [Screen color model](video.md#screen-color-model). |
| `DKC2_UPSCALER` | `nearest`, `bilinear`, `reconstruct` | Scaling (SDL host). |
| `DKC2_DISPLAY` | `flat`, `crt` | Flat panel or [CRT television](video.md#crt-television). |
| `DKC2_CRT_PRESET` | `living-room`, `studio`, `soft` | CRT preset. |
| `DKC2_CRT_SCANLINES`, `DKC2_CRT_SHARPNESS`, `DKC2_CRT_MASK_STRENGTH`, `DKC2_CRT_GLOW`, `DKC2_CRT_HALATION`, `DKC2_CRT_CURVATURE` | `0`-`100` | Individual CRT sliders; setting any of them selects the Custom preset. |
| `DKC2_CRT_MASK` | `none`, `grille`, `grille-coarse`, `slot` | Phosphor mask type; selects the Custom preset. |
| `DKC2_DISPLAY_LOCK` | `0` | macOS: use the host clock instead of display-locked pacing. |
| `DKC2_PACING_LOG` | file path | macOS: record frame cadence for `scripts/analyze_pacing_log.py`. |

## Audio

| Variable | Values | Effect |
| --- | --- | --- |
| `DKC2_MSU1_PATH` | folder path, or empty | [MSU-1](msu1-music.md) folder; an empty value turns replacement music off. |
| `DKC2_MSU1_VOLUME` | `0`-`200` | MSU-1 music volume. |
| `DKC2_MSU1_TRACE` | `1` | Log MSU-1 track selection. |

## Gameplay

| Variable | Values | Effect |
| --- | --- | --- |
| `DKC2_COOP` | `simultaneous`, `classic` | [TEAM co-op](co-op.md) behavior. |
| `DKC2_KONGS_PACK` | file path | [Character pack](characters.md) to load. |
| `DKC2_KONGS` | e.g. `1,2` | Character per slot: `0` original, `1` Donkey, `2` Kiddy. |
| `DKC2_KONGS_TRACE` | `1` | Log character-pack activity. |

## Files and diagnostics

| Variable | Values | Effect |
| --- | --- | --- |
| `DKC2_USER_DIR` | folder path | macOS: store settings and saves in this folder. |
| `DKC2_PORTABLE` | `1` | macOS: store settings and saves beside the app instead of in Application Support. |
| `DKC2_DIAGNOSTIC_BUNDLE` | `1` | Write a [support bundle](troubleshooting.md#support-bundles) even after a clean exit. |
| `SNESRECOMP_INPUT_REC` | file path | Record per-frame controller input. |
| `SNESRECOMP_INPUT_PLAY` | file path | Replay a recording (headless host). |

Developer-only test variables are described in the developer documentation
in the source repository.
