# Two-player co-op

In the original game, **2 PLAYER TEAM** takes turns: one Kong is controlled
while the other follows by computer, and control passes only when a Kong is
hit or the players tag. DKC2Recomp makes TEAM mode **simultaneous** by
default. Controller 1 always drives the first Kong and controller 2 always
drives the second, so both players play at the same time.

1 PLAYER and **2 PLAYER CONTEST** are never changed.

## Getting started

1. Assign a source to each player (see [Controls](controls.md#players-and-controllers)).
2. Start a game and choose **2 PLAYER TEAM** in the game's own menu.
3. Player 2's Kong stands by, catching up automatically if left behind,
   until Player 2 first touches their controller. From then on it is fully
   independent.

The camera centers between both living Kongs, within the level's normal
scrolling limits. Both Kongs can move into the extra side areas in
[widescreen](video.md#aspect-ratio-widescreen).

## Co-op actions

| Action | How |
| --- | --- |
| **Catch up** | Hold **Select** (keyboard **Right Shift**) for two seconds to jump beside your teammate. Release before using it again. |
| **Carry your partner** | Walk up to your partner and press **SNES A** (keyboard **X**). Press A again to put them down, or **Y** to throw them. |
| **Revive** | A Kong that is hit or falls waits for a DK barrel. The other player keeps playing; the level is lost only when the last surviving Kong falls. |

Catch-up needs both players alive and a solid or swimming spot beside the
teammate. It also gets you off ropes, out of water, unstuck from sticky walls
or honey, and back beside a teammate riding Rambi or Rattly. It does not
revive a Kong that has fallen into a pit; that still needs a DK barrel.

Carrying works when both Kongs are on foot and standing close together.

## What works together

Most of DKC2 supports both players at once, including:

- ropes, rope nets, hooks, poles and hangers, each grabbed independently;
- barrel cannons, rotating barrels and bonus-room entrances, which take both
  players together; either player can fire a shared barrel;
- held barrels and items, which stay with whoever picked them up;
- animal buddies: either player can ride Rambi, Rattly or Squitter while the
  other stays on foot; both hang from Squawks together; animal
  transformations pass to the other player on a hit;
- enemy stomps: a nearby teammate who is also falling onto the enemy gets the
  same bounce;
- hazards such as thorns, honey, ground shakes and Cat O' Nine Tails affect
  only the player who touches them;
- roller-coaster and kart stages, including shared karts where the first
  player to board controls jumping;
- either player finishing the level at the goal.

Save states and rewind keep each player's state.

## Known limitations

- Full-game death/respawn, some animal variants and special throwable items
  have not been fully verified yet.
- Scripted sequences, such as boss introductions, keep the partner under the
  game's own wait/follow control until normal play resumes.

Please report anything that misbehaves in co-op, with a save state if you can.

## Switching back to classic TEAM

To restore the original alternating behavior, change **2P Team mode** in the
overlay's Settings page, or the Windows **Input** menu, to classic. In classic
TEAM and single-player, **Select** keeps its normal tag action.
