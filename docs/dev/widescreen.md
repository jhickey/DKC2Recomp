# Widescreen implementation status

This page collects the detailed widescreen status that used to live in the
README. For players, the [Video guide](../guide/video.md#aspect-ratio-widescreen)
describes the options. For the design, see
[Experimental widescreen boundary](../ARCHITECTURE.md#experimental-widescreen-boundary)
in the architecture notes. For the debugging workflow, see
[Widescreen diagnosis workflow](../WIDESCREEN_DIAGNOSTICS.md).

Widescreen remains experimental. The sections below record what has been
reconstructed, how, and which stages still need route or owner acceptance.
Keep this page current when a stage's status changes.

## Margin reconstruction and stage status

The experimental aspect selector is available in the pre-boot Settings page,
the in-game Settings tab, and the native Mac **View > Aspect Ratio** menu.
Authentic 4:3 remains 256x224, Mac-oriented 16:10 uses 308x224 (26 added source
pixels per side), and 16:9 uses 342x224 (43 per side). Both wide choices
preserve the original center. Pirate Panic's collision-bearing foreground margins use
DKC2's live decompressed WRAM level map to reconstruct exact 8x8 tiles, with
world-keyed history retaining game-authored updates. The adapter accounts for
the game's 256-pixel map/camera origin difference, its rotated column buffer,
and the one-frame WRAM/PPU latch difference that can occur while the camera
crosses an 8-pixel row. Terrain shadow Y unwraps the PPU's tile-aligned
origin before restoring the fine phase, and the world-keyed store retains
1,024 tile rows so tall vertical rooms such as Topsail Trouble keep their
second epoch.

Every other margin decision is a property of the live PPU geometry, not a
level list. Each enabled bounded background (a 32-column tilemap, or a
64-column allocation whose extension page is another enabled layer's map),
whether enabled for the whole frame or only inside an HDMA band, repeats
its rendered native scanline, which is exactly what a wider PPU
would draw from a map that wraps at 256 pixels. A bounded backdrop kept in a
64-column allocation continues each line at the period its own rendered
pixels prove, so a 96-pixel cabin wall does not restart every 256 pixels,
and rebuilds its stale endpoint pixels from that period; 32-column maps keep
their exact hardware wrap. A 64-column BG3 with pages of its own
renders its authentic adjacent columns; the ship-deck rigging, which the
cartridge streams into that ring with no lead, is instead decoded from its
ROM map into a third world-keyed store after the decode has reproduced every
fully uploaded native column of the current frame. The lava geyser steam of
Red-Hot Ride, a bounded 32-column BG3 the cartridge draws only for geysers
inside its own view, is decoded from the stage's ROM geyser list and
animation tables into the same store, so a geyser beside the view keeps its
column and the map's 256-pixel wrap no longer puts steam over solid rock.
A static 64-column plane that the cartridge never streams (the lava
stages' foreground rocks and far spikes) continues into the margins as its
own hardware wrap once its content proves it is authored to wrap.
Rolling BG1/BG2 terrain layers are classified per HDMA scanline band, read
from the cartridge's own HDMA tables before drawing: a band at the terrain
phase is served from the one world-keyed terrain store (the second physical
layer reads it through an alias view), and any other band repeats its
rendered line, so the lava stages' BG1/BG2 exchanges need no special case.
At a hard level wall the 4:3 edge stays pinned at the wall, so nothing past
the level is ever shown, and the inward view is released gradually over eight
margins of camera travel (edge policy `glide`, the default). Three
alternatives are selectable from the pause menu's Settings page ("Level
edge"), the `WidescreenEdge` key in `launcher.cfg`, or the
`DKC2_WIDESCREEN_EDGE` environment variable: `reflect` keeps the view locked
to the game's camera and mirrors the nearest authored columns into the
unauthored strip; `bars` keeps the view locked and leaves that strip black;
`shift` is the earlier inward clamp, whose view stands still for the first
43 pixels of camera motion away from a wall while the HUD slides with it. The presented native viewport is exact under
every policy.
Unknown layouts remain transparent rather than guessing.
The original 4:3 mode is the default.

The widescreen adapter reads DKC2's live gameplay sub-mode before choosing a
terrain-map policy. Proven horizontal stages decode the game's column-major
map, and proven vertical stages decode its row-major map. Bramble Scramble's
sub-mode `$10` uses a distinct 48-metatile/`$60`-byte square layout confirmed
against 954/957 visible BG1 cells. Ordinary wasp-hive sub-mode `$03` calls the
same cartridge square scroller and now exposes that terrain path
experimentally; Parrot Chute Panic retains its separate narrow-row layout.
Ship-hold sub-mode `$02` also uses the rolling row/column DMA path, but its
source map is 80 metatiles wide; Lockjaw's Locker's exact state matched all
957 sampled visible BG1 cells under that decoder. Treating the room's
64-column VRAM ring as a complete static map was the cause of the missing and
unrelated edge strips during movement.
Hornet Hole, Rambi Rumble, and King Zing still need route and per-layer visual
acceptance. Other square rooms and special handlers remain centered until they
have reference-backed reconstruction and route coverage; a 64-column PPU
tilemap alone is not sufficient evidence that a screen is safe to widen.

All three neutral-input attract demos now retain true 16:9 gameplay. Mainbrace
Mayhem uses its existing vertical BG1 terrain reconstruction and repeats the
authentic BG3 cloud/lighting scanline, removing the former 4:3 brightness
seams. Rickety Race uses the established horizontal policy. Parrot Chute Panic
uses the disassembly-confirmed alternate wasp-hive handler: its BG2 terrain is
decoded as a 512-pixel-wide row-major map with 16 metatiles (`$20` bytes) per
row, while its cyclic BG1/BG3 hive artwork repeats after normal PPU rendering.
Representative early/middle/late captures are full width, and a 12,000-frame
run completes two ordered attract cycles with zero sequence errors. Final
normal-speed owner validation remains required.

The common DKC2 object activation/despawn and sprite-render boundaries have
been widened, and Pirate Panic has deterministic composite, per-layer, and OAM
margin evidence. Those widened object bounds activate only after the terrain
source for the frame has been verified. This is not yet a whole-game
widescreen certification:
vertical stages, bosses, bonuses, maps, Mode-7 screens, and special effects
still require explicit route testing. The complete recorded Pirate Panic route
and two late BG1 margin regressions pass deterministically. The newer regression
clears source-map cells proven transparent on every frame while preserving
current dynamic game writes, removing stale deck fragments without flattening
ship details. Horizontal source-page calibration improves the sampled frames
at 12,000 and 12,300, which the owner accepted, but frames 12,900, 13,800, and
15,900 remain open visual defects. Physical 64-column BG3 ship rigging can now
render in the margins after the same exact terrain-readiness gate; synthetic
coverage includes Pirate Panic's and Rattle Battle's shared ship-deck PPU
signature, while normal-speed route acceptance remains separate.
Topsail Trouble's supplied exact state is separately accepted at 308x224: its
isolated BG3 rain now reaches both 26-pixel margins, and the original 256-pixel
center is pixel-identical to the pre-fix render. Its later lower-camera Quick
Save is also accepted: exact BG1 terrain now fills both margins through tile
row 540, and the native center is pixel-identical to the 4:3 oracle. A
fresh-entry moving route is still required before treating the complete stage
as closed.
The private Rambi route additionally retains an 8-pixel horizontal guard and
the tile-aligned vertical epoch correction. Exact frames 6,509, 6,511, and
6,512 no longer produce the previous 1,120-sample blank-margin bursts; final
normal-speed owner validation is still required.
Use
`DKC2_WIDESCREEN=1` for a
one-process developer override without changing `launcher.cfg`.

The private 3,134-frame `bramble-01` route now exercises Bramble Scramble's
entrance, horizontal movement, vertical climb, and late-stage area. Its BG1
terrain reconstructs into both margins, bounded BG2 uses the existing
rendered-scanline repeat, and BG3 remains clamped because the audited composite
does not expose a gap. The route records sprite output in both margins and
finishes with zero sequence/runtime errors, but it ends before the level goal;
entrance-to-goal acceptance and normal-speed owner testing remain open.

Collectible bananas are a separate cartridge subsystem, not ordinary entries
in the common game-sprite table. Their list traversal and clip span receive the
same fail-closed widening, while a banana-only coordinate adapter supplies
OAM's ninth X bit for positions `$0100-$012A`. Without that adapter, a banana
at widescreen X=291 was submitted as X=35 and appeared on the wrong side of
the screen. The private `bg-02` frame-2,582 replay now places both banana tiles
at X=291 in the right margin. A separate native negative-X tile cutoff has
also been extended through the left margin: the full marsh replay now records
banana tiles at X=-43..-1 rather than only X=-14..-1. Both adaptations remain
off in 4:3; other dedicated object/effect renderers still need route-by-route
audit.

The private `bg-01` route confirms why policies must remain screen-specific:
a later forest screen streams its collision terrain to BG2 `$7800`, not BG1
`$7000`. Widescreen reconstruction now matches live `$17B6` to the enabled
BG tilemap base and prefills the selected layer. Deterministic frames 4,500 and
4,800 now contain the missing BG2 terrain without the prior colored BG1 margin
cells. The automated classifier still flags a sparse secondary BG1 margin, so
owner motion testing and screen-specific foreground auditing remain required.
Mudhole Marsh additionally opts its cyclic BG3 `$6C00` forest backdrop into
scanline repetition. This fills the formerly flat-colored margins without
reading unseen BG3 tilemap columns. Other BG3 uses remain conservatively
clamped until audited.

The subsequent `bg-02` vertical-motion recording exposed a separate
engine-level row-association error. DKC2 stages the rolling terrain tilemap one
256-pixel page above camera Y. The active BG1/BG2 terrain shadow now keys live
viewport captures, VRAM uploads, and exact prefill in the same rendered PPU
source-row domain. This follows the live terrain destination and is therefore
not hardcoded to Mudhole Marsh, but screens that do not use the standard
rolling terrain streamer remain intentionally excluded.

## Route auditing

The experimental 16:9 path includes an automatic deterministic route auditor,
not only single-frame screenshots. `scripts/audit_widescreen_route.py` replays
composite/BG/OBJ layers and correlates them with camera state, exact
world-keyed terrain entries, margin-source provenance, and placed-object
lifetimes. Its HTML/JSON report flags raw rolling-VRAM fallback, missing
terrain replaced by transparent tiles, terrain identity changes, old-edge
seams, object spawn/despawn near the former 4:3 boundary, and active margin
objects with no OBJ pixels.

The trace also proves, for each sampled frame, how many expanded-margin cells
were requested, present, and equal to the static level source. A newer
cartridge tilemap write is treated as authoritative rather than compared with
a later animation phase. Verified transparent fallback is retained in a
separate safe-observation section; it is not counted as an actionable defect.
Object lifetime conclusions require `--step 1`.

Start with a coarse `--step 4` route, then rerun a short suspicious interval at
`--step 1`. All generated evidence belongs under ignored `.cache/` or an
external private test directory. See
[`WIDESCREEN_DIAGNOSTICS.md`](../WIDESCREEN_DIAGNOSTICS.md) for commands,
confidence meanings, storage costs, and limitations.
