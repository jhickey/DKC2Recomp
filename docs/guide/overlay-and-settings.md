# Pause menu and settings

## The overlay

Press **Escape** during gameplay (or the controller **Guide** button, or
**Start+Back**) to pause and open the overlay. It offers Resume, Settings,
Controls, Characters, Assist Tools / Cheats, Credits and Quit. Gameplay input
and audio pause while it is open. Drag its title bar to move it.

In a fullscreen SDL or Mac window, the first Escape returns to windowed mode
without opening the overlay.

The overlay works with every renderer, including the GDI compatibility
renderer on Windows.

## Settings

The Settings page holds the same display, audio, filtering, screen-model,
aspect-ratio and skip-launcher choices as the launcher. See [Video](video.md)
for the display options and [MSU-1 music](msu1-music.md) for the audio
replacement options.

- Apply immediately: volume, aspect ratio, texture filtering, screen model,
  Player 1/2 source and deadzone, and the Assist Tools switch.
- Apply on next launch: window scale, fullscreen mode, renderer, audio
  enable and skip-launcher.

The sample-rate choice is saved, but the game currently always outputs the
SNES-native 32,040 Hz.

### Restore Defaults

**Restore Defaults** (after a confirmation) resets the whole launcher
configuration: window and display choices, audio, controller sources,
deadzones and bindings, Assist bindings and the skip-launcher preference. It
does **not** touch your selected ROM, cartridge saves, save states or rewind
history. The restored choices are saved when you press Play.

## Assist Tools

Rewind, fast-forward, the five save-state slots and all Assist shortcuts are
off until you enable **Enable Assist Tools / Cheats**. While enabled, the game
window title shows `(Assist Tools: On)`. The setting is saved as
`AssistTools` in `launcher.cfg`.

The top-level **Assist Tools** page (launcher) and the Controls page's
**Assist** tab (overlay) edit the Rewind, Fast-forward, Save State and Load
State bindings.

### Save states

The overlay shows five save-state slots, stored as `saves/dkc2s0.sav` through
`saves/dkc2s4.sav`. Slot 1 can also load the older `saves/dkc20.sav` name.
Save states are separate from the game's own cartridge save.

On the Mac app, **Game > Quick Save State / Quick Load State** always use
Slot 1, even with Assist Tools disabled.

## Credits

The launcher and overlay both have a **Credits** page listing the projects
and people this port builds on.
