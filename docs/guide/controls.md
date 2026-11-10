# Controls

## Default layout

| Action | Keyboard | Controller |
| --- | --- | --- |
| D-Pad | Arrow keys | D-Pad |
| A / B | X / Z | B / A |
| X / Y | S / A | Y / X |
| L / R | Q / W | Left / right shoulder |
| Start / Select | Enter / Right Shift | Start / Back |
| Rewind | Hold 1 | Left trigger |
| Fast-forward | Hold 2 | Right trigger |
| Save state (selected slot) | F5 | Unbound |
| Load state (selected slot) | F9 | Unbound |
| Toggle performance log | F | - |
| Open/close pause overlay | Escape | Guide, or Start+Back |

In DKC2 terms: **Z** (SNES B) jumps and **A** (SNES Y) runs, rolls and picks
up. Rewind, fast-forward and save states only work while
[Assist Tools](overlay-and-settings.md#assist-tools) are enabled.

**Start+Back** opens or closes the overlay without sending that chord to the
game.

## Rebinding

Bindings can be edited in two places:

- the launcher, from each player's **Configure** page and the top-level
  **Assist Tools** page;
- the in-game overlay's **Controls** page, which has Player 1, Player 2,
  Assist and Fixed Shortcuts tabs.

Select a binding, then press the replacement key, controller button or axis.
Controller capture waits for every button to be released first, so the button
that opened the editor is not recorded. **Escape** cancels a capture. The
overlay and performance-log shortcuts are fixed so they can never be made
unreachable. Per-player and Assist reset buttons restore only their own
defaults. Bindings, deadzones and device choices are saved in `launcher.cfg`.

## Players and controllers

Player 1 defaults to the keyboard and Player 2 to the first connected
gamepad. To use two gamepads, select **Gamepad** for both players and choose
each player's controller in the launcher's controller list.

- USB and Bluetooth controllers are supported through SDL GameController,
  including on the native Windows host.
- Controllers connected after launch are detected automatically. A specific
  controller that you selected but is disconnected stays neutral until it
  reconnects.
- The bundled mapping recognizes the 8BitDo SN30 Pro in Bluetooth DInput mode.
  Xbox One S and SN30 Pro controllers need no keyboard-mapping software.
- Each player's Controls tab shows which device it is using.

Rumble for stomps can be enabled in **Settings**, with separate test pulses
for Player 1 and Player 2. Rumble goes to the controller assigned to that
player.

For two-player play, see [Two-player co-op](co-op.md).
