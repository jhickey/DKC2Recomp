# Simultaneous co-op: behavior and verification

This page collects the detailed co-op behavior, coverage and private
verification notes that used to live in the README. For players, see the
[co-op guide](../guide/co-op.md). For the design, see
[Simultaneous co-op boundary](../ARCHITECTURE.md#simultaneous-co-op-boundary).
For tuning and private CTest snapshot variables, see
[BUILDING.md](../../BUILDING.md#compiled-configuration).

Each paragraph records a supported interaction and how it is verified. Most
private checks replay an owner-supplied save state, which stays outside Git,
against the user's own ROM.

## Core behavior

Selecting "2 PLAYER TEAM" in the game's own menu used to alternate control:
one Kong was player-controlled while the other followed by AI, and control
passed only when a Kong was hit or swapped. The port now makes TEAM mode
simultaneous by default: controller 1 always drives the first Kong slot and
controller 2 always drives the second, so both players play at the same time,
each with their own Kong. The second Kong stands by (and auto-catches-up when
separated) until player 2 first touches their controller, then stays fully
playable, including after landing. Both players use normal bright colors and
can attack enemies; Player 2's roll, stomp and bounce are covered by a private
first-level replay, along with contact damage and a Player 1 attack regression.
Roll/stomp recovery restores walking and jumping. Held barrels follow and
launch from their owner, including throws across different platform heights.
An empty-handed partner's run/pick and jump inputs do not release the owner's
item. Ground and airborne item ownership also survive save/load; the private
`supplied_rom_coop_item_input` replay covers both player slots.
Either player can finish the level by landing on the goal. The Kong that
hits it runs the native ending sequence, with fixed controller assignments
preserved. With `DKC2_ROM` and an external `DKC2_COOP_GOAL_STATE` configured,
`supplied_rom_coop_goal` replays the reported goal regression for both players.
Hold **Select** (keyboard **Right Shift** by default) for the configured hold (**two seconds** by default) to
bring your Kong beside your teammate in simultaneous TEAM mode. Release it
before using it again. If both players hold it, the camera follower joins the
leader once. Select is reserved for this catch-up action in that
mode; classic TEAM and single-player retain the normal tag action. Rescue
requires two living players and a grounded or swimming destination. It can pull
the requesting Kong off a rope, including an offscreen rope or rope junction,
and works into, out of and within water. Swimmers turn to face their movement.
An on-foot partner can also recover beside a grounded Rambi rider, including
a live Kong stuck waiting below the level. The rider and Rambi stay in place.
Riders themselves, other mounts, barrels and scripted actions remain excluded; pause/loading resets
the hold. Existing saves with a stale lost flag on a confirmed live Kong recover
automatically. To replay the reported rope rescue, run
`python scripts/check_coop_rescue.py --runner <headless-runner> --rom <external-ROM> --state <external-save>`.
Use `--water-state <external-save>` for the reported swimming regression.
Use `--mount-state <external-save>` for the reported Rambi/waiting regression.
Either player can walk up to their partner and press **SNES A** (keyboard
**X** by default) to carry them. Pickup requires both Kongs on foot and within
24 game pixels horizontally and 16 vertically. Press A again to put them down,
or Y to throw them. The carrier keeps their own controls; both players regain
independent movement after release. Diddy/Dixie and Donkey/Kiddy checks cover
near/far pickup, carrying, drop/throw and save/load.
Each player can grab and climb ropes independently, with climbing animations
in both directions. Single/double-rope junctions complete normally, including
when loading a save already stuck at the end of a transition. The Topsail Trouble
regression covers Player 2 attaching, both players climbing in opposite
directions, save/load and jumping to the neighboring rope. To repeat it with
the private reported snapshot, configure `DKC2_COOP_ROPE_STATE` with its
external path and run the `supplied_rom_coop_ropes` CTest check. Adding
`DKC2_COOP_ROPE_JUNCTION_STATE` enables the second reported checkpoint's
double-rope animations, side exits and transition save/load checks.
It also checks crossing the entire net and reversing direction to reach both
outer ropes without repeating the turning animation in place.
A hurt Kong completes its departure and waits for a DK barrel; pressing its
controls or loading a save cannot revive it. The survivor continues without
the original TEAM turn-taking prompt. A DK barrel restores independent control.
If either player falls into a pit, a live teammate keeps playing with their
own controller. Level loss occurs when the last surviving player falls.
Private checks cover both Kong roles after a leader swap and save/load across
loss, revival and a second loss.
Either player can mount Rambi; the rider becomes the camera leader and keeps
their own controller. The other Kong retains on-foot movement. Private checks
cover riding, jumping, dismount/remount, passing Rambi from P1 to P2 and loading
while mounted. Death handoff keeps the survivor in place and resumes enemies.
Both players can collect banana trails while the other rides Rambi; overlapping
hitboxes and revisiting collected bananas after save/load award each only once.
Both Kongs can move into the visible side areas in 16:10 and 16:9, with the
level walls retained. In simultaneous TEAM, the camera targets the midpoint
of both playable Kongs, with native scrolling limits and framing retained.
Transport-cannon entry and firing carry both living players together when
either player enters, including the current follower. Manual rotating barrels
also take both players inside; either player can press jump to fire both.
After the native launch lock ends, either player can steer left/right in
the air independently. Both use native barrel-shot physics for equal upward
force and return to normal walking animation after landing. Steering and normal
movement retain separate controller
ownership. Bonus-room
entrance restores both live players on the arrival platform without holding
Select. A fixed tail-hook attaches the Kong that touched it; both players
can share the hook and jump off independently, including the last occupant's
first jump after the other player leaves. Kleever's dropping hooks also support
both players in either grab order, with separate single-press departures.
Throwing a carried Kong into the
reported elevated Gangplank barrel completes entry for both players and
restores control on the upper platform.
The on-foot player can also use hangers while the teammate rides Rattly.
Rattly's superjump can leave the partner below the camera without losing them;
hold that partner's Select for the configured duration to teleport beside the rider,
including while the snake is airborne. Actual pit deaths still require rescue
from a DK barrel. A Rattly rider falling into a pit releases the mount and
restores its palette ownership, leaving the survivor on foot.
Both living players hang from Squawks together. If the controlling Kong is
hit, flight passes to the surviving player's controller, including after save/load.
Scripted boss intros keep the partner in native wait/follow handling until
normal play resumes; the Kleever intro no longer lets the partner sink into lava.
Full-game death/respawn, other animal variants and special throwables remain unverified.
The "2P Team mode" choice in the overlay's Settings
page (or
`CoopMode` in `launcher.cfg`, or `DKC2_COOP=simultaneous|classic`) restores
the classic alternating behavior; 1 PLAYER and "2 PLAYER CONTEST" are never
affected.

## Interaction notes

Shared manual barrel aiming (2026-10-21): when both players are inside, either
controller can rotate and fire the barrel. Opposite directions cancel per axis;
matching directions retain the native rotation speed. After firing, air controls
remain separate. The reported level-$28 barrel passes both entry orders and
save/reload checks. Optional private CMake test: DKC2_ROM plus
DKC2_COOP_BARREL_ROTATION_STATE (external snapshot).

When a real enemy stomp is accepted, a nearby living teammate who is also
airborne and descending above that enemy gets the same bounce impulse. This
distance window forgives slightly staggered landings. Each player retains
their own position and horizontal movement. Grounded, rising, distant,
lost, mounted and scripted players keep normal behavior. Shared bouncing does
not grant invincibility or teleport either player. The reported level-$28
checkpoint passes both first-stomper orders, separate steering, mid-bounce
reload and both players reaching the next platform. Private checks assume the
default tuning; configure DKC2_ROM and DKC2_COOP_SHARED_STOMP_STATE externally.

### Independent enemy pushes and actor poles

Enemy knockback now keeps a controlled partner independent instead of running
the original AI follower's automatic regroup/pickup. Intentional team pickup
still works from either controller. The reported pole supports both players
in either grab order, separate up/down movement, native height limits and
single-press jump-off without immediately regrabbing. Mid-push and mid-jump
save/load retain those behaviors. This actor-pole policy currently covers
regular type $2D8 states $05/$06; other pole families and physical controller acceptance remain
unverified. Optional private CMake snapshots: DKC2_COOP_ENEMY_PUSH_STATE and
DKC2_COOP_POLE_STATE, together with external DKC2_ROM.

Pole climbing also advances each player's native up/down animation and returns
to the native idle pose when stopped, including the inactive Kong.

The two-player midpoint camera also includes actor-pole climbers, with either
one or both players on a pole. Native level camera limits still apply.

Enemy bounce state $16 contributes to the two-player midpoint camera too,
whether a stomp launches one player or both.

A living player hanging on an actor pole now survives their teammate's pit
death, keeps their own controls, and can continue after saving/loading.

A DK-barrel return finishes at the living teammate's current position with
entrance momentum cleared, preventing an idle player from sliding into a pit.

Shared barrel launches also copy native gravity and terminal fall speed into
each player's physics work. Old grounded saves restore the player's own normal
fall-speed limit rather than retaining the follower's floating descent.

Mounted bonus returns preserve the native animal/barrel arrival until the
rider lands; the dormant partner then regains independent control on safe
ground beside the rider. Verified with the reported Rambi bonus timeout.

Animal-transformation sections keep the inactive Kong hidden. Each accepted
surviving hit switches the animal to the other controller while native health,
DK-barrel healing and final loss remain intact. Ordinary mounts still support
the independently controlled on-foot partner.

A teammate entering water no longer drops the other player's held beetle or
other grabbable. The carrier's own water-entry drop remains native.

Thorn contact in simultaneous co-op keeps the cartridge's hurt animation,
death arc and survivor handoff for the player who touched the hazard. Instant
pit removal still preserves an eligible teammate. Copied-save acceptance:
`scripts/check_coop_thorns.py --runner <headless> --rom <external-rom> --state <external-save>`.

Shared enemy stomps also accept descending barrel-flight players, keeping the
compiled proximity thresholds and excluding rising or grounded teammates.
Private copied-save check: `scripts/check_coop_barrel_stomp.py` with external
`--runner`, `--rom` and `--state` paths.

Kudgel's ground shake checks both co-op players independently. Grounded
players receive the native stun and recover normally; jumping players avoid
it. Private copied-save acceptance: `scripts/check_coop_ground_shake.py`
with external `--runner`, `--rom` and `--state` paths.

Honey-floor sticking belongs to the player who touches it. Either Kong can
jump free independently, including when both stand on honey; the dry teammate
retains normal movement. Private acceptance: `scripts/check_coop_honey.py`
with external `--runner`, `--rom` and `--state` paths.

Sticky-wall contact also belongs to the touching player. Both Kongs can
attach to the same wall and jump away independently. Private acceptance:
`scripts/check_coop_honey_wall.py` with external `--runner`, `--rom` and
`--state` paths.

The co-op midpoint camera includes honey-wall attachment, wall jumps and
sliding, plus sticky-floor movement/carry states. Live players continue to
contribute their positions while using honey terrain.

Team throws into hangers now release the thrower's movement once the passenger
is attached. The thrower can walk or fall normally while the other player
continues hanging; saved throw waits recover on load.

Select rescue also works while attached to sticky walls or stuck on honey.
Teleporting to a teammate on a sticky wall shares that wall attachment;
teleporting from the wall to the floor restores normal movement.

A living teammate on a sticky wall or honey floor now prevents a pit fall
from ending the level. Either fallen player is marked lost consistently;
revival uses a DK barrel rather than Select teleport.

A Squitter rider's pit death now releases the spider mount before control
passes to the survivor, preserving character palettes and normal movement.
The fallen rider needs a DK barrel to revive.

With both players alive, the co-op camera centers its view between them,
including animal riders and hanging players. Native level boundaries and
scroll smoothing still apply. Scripted/death sequences keep native framing.

Pole jump-off suppression now expires once the player leaves contact, so a
later grab or a pole reusing the same sprite slot remains available. A revived
active player also clears a stale lost flag after a new life; dead waiting
teammates still require a DK barrel.

Coaster enemy stomps bounce the rider upward, including a nearby descending
teammate within the configured shared-stomp threshold. Leaving an old cart
preserves forward momentum and each player's own movement context. A missed
track gap loses the fallen rider; a safe teammate continues to the next cart.

A lone coaster survivor can board the next cart through the native descending
foot contact. Accepted contact finishes seating immediately; the lost teammate
stays lost and native airborne steering remains available.

Paired coaster jumps allow a descending partner within 32 horizontal pixels
of the empty seat and from 32 pixels above to 24 below to join a teammate who
has landed. Own-seat jumps stay independent; distant fallers stay lost.

Shared stomp bounce also applies after coaster riders detach from a cart.
Nearby descending riders retain native coaster bounce and can land on the
next cart; compiled stomp distance settings still control eligibility.

An accepted cannon entry releases the departed coaster so an early jump
cannot be pulled back into its pit. Native cannon shooting and destination
cart landing remain available; genuinely missed jumps still lose a life.

Coaster riders remain attached during the scripted track exit, allowing the
normal transition to the goal area and completion back to the map.

Ceiling-thorn damage follows the player who touches it, including an inactive
co-op player. Native hurt/death and survivor handoff remain intact.

Shared mode-02 karts keep both Kongs seated and jump as one vehicle. The first
player to board controls Jump; the passenger cannot jump out or trigger it.
Ordinary mode-01 coasters retain separate rider jumps.

Hook contacts accept horizontal team throws as well as upward throws in
simultaneous co-op. Hooks with camera-framing parameters support sharing
while retaining their native framing. Each occupant jumps off independently.

Hook grabs also restore interaction eligibility after a team throw, including
older hanging saves. A player hanging on another hook cannot block new grabs.

Cat O' Nine Tails grabs only the player that touches it in simultaneous
co-op. The other player stays independent while the captured player spins
and launches; the camera continues to include both live players.

## Validation evidence

The [2026-10-29 evidence manifest](../evidence/coop-validation-2026-10-29.md)
records the external checkpoint inventory, reproducible replay commands and
original results: 56/58 CTest checks and 44/45 targeted private checks passed.
The packaging and blank-SRAM item-pickup setup failures were fixed in the
follow-ups below. Save files remain private and outside Git.

Packaging follow-up: both module-resolution failures are fixed; the complete
public suite now passes **58/58**. See [follow-up evidence](../evidence/packaging-validation-2026-10-29.md).
The earlier evidence retains its original results.

Item-input follow-up: the blank-SRAM setup is repaired and both players pass
ownership checks. See [the new evidence](../evidence/item-input-validation-2026-10-29.md).
This reruns the previously failing case; the other 44 private successes remain
recorded in the original validation. No gameplay code changed.
