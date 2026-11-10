# Recompilation status

This page records static recompilation coverage and the gameplay
route-testing gate. For the analysis pipeline itself, see
[ARCHITECTURE.md](../ARCHITECTURE.md#native-snesrecomp-execution-path) and
[SNESRECOMP_INTEGRATION.md](../SNESRECOMP_INTEGRATION.md).

## Static recompilation coverage

The current analysis profile has 3,325 roots across 13 banks. It emits 3,475
exact CPU-mode variants as static C and retains two deliberate original-game
fault variants on LLE. This is compile-time structural closure, not a
percentage of dynamically executed CPU instructions and not a claim that the
shared interpreter can be removed.

The interpreter remains the safe runtime default for an unavailable exact
entry state. Two dormant bugs in the original game also deliberately preserve
their real JSR stack frames and hand control to the interpreter if reached:
both calls enter bytes documented as data/garbage and crash on original
hardware. They are explicit exceptional LLE edges from compiled callers, not
normal game logic and not guessed native implementations.

The generated C remains ignored because it is derived from the user's ROM.
Only source-owned configuration and structural metadata are committed.

## Runtime-selected entry coverage

The structural-closure figures above cover every entry state demanded by the
static graph; they do not prove that every address selected later from mutable
game data was already named as a root. An owner-recorded Version 11 session
exposed that distinction in Swanky's Bonus Bonanza. The process exited cleanly,
but runtime state `$B4:A4CB` reached the interpreter's 2,000,000-instruction
safety cap and appeared interactively as 1-3 FPS.

The source configuration now declares Swanky's states `$B4:A3E0`, `$B4:A475`,
`$B4:A4CB`, `$B4:A5D9`, and `$B4:A665`, plus helper `$B4:A7CA`, as explicit
AOT roots. The shared call bridge also preserves the handler's intentional
non-local return: in 16-bit accumulator mode, `PLA` consumes the paired JSR
frame and the following `RTL` consumes an outer JSL frame. That return must
unwind the compiled caller rather than resume code the game deliberately
skipped. The shared-bridge regression passes 62/62 checks. DKC2 regeneration
and both optimized Release and trace builds now succeed, and the generated
dispatch table contains all six exact entries.

Rolling diagnostic reports now preserve the last 1,024 runtime indirect
dispatch events. `scripts/validate_swanky_run.py` requires a native M0X0
dispatch from the Swanky dispatcher to `$B4:A4CB`, rejects interpreter caps,
missing Swanky AOT entries, the original corrupt sequence, and execution in
SNES MMIO addresses. Its synthetic regression passes and it correctly fails
the original Version 11 artifact. The complete available suite is 52/53; the
only failure is the unchanged supplied-ROM frame-3,309 sprite-reference
mismatch. The owner's fresh normal-speed game-show check remains pending.

## First-level route testing

Pirate Panic is the next gameplay correctness target. The desktop host can
record per-frame input with `SNESRECOMP_INPUT_REC`, and the headless host can
replay it with `SNESRECOMP_INPUT_PLAY`. The new private route gate checks that
the replay enters Pirate Panic, stays active, changes the completion flags,
triggers a level-exit transition, and keeps audio unclipped.

Recordings should live in ignored private storage such as `recordings/` or
`private/`. See
[`FIRST_LEVEL_ROUTE_TESTING.md`](../FIRST_LEVEL_ROUTE_TESTING.md) for
the exact recording and replay commands. The first captured route reaches the
goal, but the native replay currently exposes an unresolved dispatch at
`$BA:B33F`; Roadmap #2 remains open until that path replays without an
interpreter-cap or unresolved-dispatch diagnostic.

Input files record the resolved controller word for each forward emulated
frame. They do not encode host rewind or save-state save/load actions. Fast
forward remains recordable because every forward emulated frame is sampled,
but a route that rewinds or loads a state cannot be reproduced from its
`.input` and starting SRAM alone. Capture focused regression routes without
those actions until the recording format gains an explicit host-action stream.
