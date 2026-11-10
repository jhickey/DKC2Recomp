# Video

All of these options are in the launcher's Settings page and the overlay's
**Settings** page. Most are also in the Windows **View** menu and the Mac
**View** menu. Choices are saved in `launcher.cfg`. To override one for a
single run, see [Environment variables](advanced.md).

## Renderer

| Renderer | Notes |
| --- | --- |
| OpenGL (default) | Supports every option on this page. |
| GDI compatibility (Windows) | Used automatically if OpenGL fails to start. Supports the overlay and Nearest/Bilinear scaling, but not Reconstruct or the CRT television. |
| SDL host (`DKC2RecompSDL.exe`, Mac, Linux) | Supports every option on this page. |

Changing the renderer takes effect on the next launch.

On Windows, OpenGL windows request vsync to reduce tearing. The Mac app paces
each frame to the display's own refresh, including ProMotion displays, so
every frame is shown for exactly one refresh.

## Aspect ratio (widescreen)

| Choice | Game resolution | Notes |
| --- | --- | --- |
| 4:3 (default) | 256x224 | The original picture. |
| 16:10 | 308x224 | 26 extra pixels each side; suits Mac displays. |
| 16:9 | 342x224 | 43 extra pixels each side. |
| 21:9 | 446x224 | Ultrawide. |

Widescreen is **experimental**. The original 4:3 picture stays exactly in the
center and the game draws the extra side areas from its own level data.
Coverage varies by stage:

- Many horizontal and vertical stages, including all three attract-mode
  demos, fill the full width.
- Some special rooms, bosses, bonus rooms, world maps and Mode 7 screens stay
  centered until each one has been verified.
- Where the port cannot prove what belongs in the margin, it leaves the
  margin empty rather than guess.

Please report stages where the side areas show wrong or missing scenery.

### Level edge

When the camera reaches a hard level wall, there is nothing authored past it.
**Level edge** chooses what to show:

| Policy | Behavior |
| --- | --- |
| `glide` (default) | The 4:3 edge stays at the wall, and the extra width eases in over a short distance as the camera moves away. Nothing beyond the level is ever shown. |
| `reflect` | The view stays locked to the game's camera; the empty strip mirrors the nearest level columns. |
| `bars` | The view stays locked; the empty strip is black. |
| `shift` | The earlier behavior: the view stands still for the first 43 pixels of camera movement away from a wall, while the HUD slides. |

## Screen color model

| Choice | Effect |
| --- | --- |
| Raw (default) | The exact pixels the game produced. |
| CRT | Models a consumer CRT's phosphor colors, gamma, brightness and black level. |
| Composite | A composite-video color variant. |
| Trinitron | A Trinitron color variant. |

These change color only. They add no scanlines or curvature (use the
[CRT television](#crt-television) display for that), and they behave the same
on every renderer.

## Scaling

- **Nearest** (default): sharp, blocky pixels.
- **Bilinear**: smooth, slightly blurred.
- **Reconstruct** (experimental, OpenGL and SDL only): keeps pixel edges sharp
  at any window size, smooths the checkerboard and line dithering SNES artists
  used for in-between shades, rebuilds diagonal edges, and adds gentle
  shading. It has five levels plus sliders for edge strength, softness and
  smooth shading. All screen color models work with it. On Windows, select
  OpenGL and restart if you are using GDI.

## CRT television

**Settings > Display > CRT television** replaces the flat panel with a
simulated tube. It is more than a scanline overlay: each line is drawn as an
electron-beam profile that widens with brightness, through a fine phosphor
mask, with glow, halation and a gently curved screen.

| Preset | Look |
| --- | --- |
| Living room (default) | Balanced consumer TV |
| Studio monitor | Sharper and flat |
| Soft | Wider, glowier lines |
| Custom | Your own Scanlines, Sharpness, Phosphor mask, Mask strength, Glow, Halation and Curvature |

The screen color model still applies underneath the tube. Reconstruct
scaling is bypassed while the tube is on, and in very small windows, where
lines cannot be drawn, the tube fades to the flat image. The CRT television
is available on OpenGL and SDL; GDI uses the flat display.
