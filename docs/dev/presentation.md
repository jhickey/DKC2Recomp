# Presentation, pacing and input notes

Implementation details of the video presentation path, frame pacing and
controller handling that used to live in the README. Player-facing
descriptions are in the [Video](../guide/video.md) and
[Controls](../guide/controls.md) guide pages. See also
[CRT_DISPLAY_PLAN.md](../CRT_DISPLAY_PLAN.md) and the
[Reconstruct upscaler](../ARCHITECTURE.md#reconstruct-upscaler-experiment)
and [CRT television display](../ARCHITECTURE.md#crt-television-display)
architecture sections.

## Screen-color model

The launcher defaults to the OpenGL presenter with nearest-neighbor sampling
and the **Raw** screen model. Raw is a byte-exact presentation bypass. The
opt-in **CRT**, **Composite**, and **Trinitron** choices apply the present-time
screen-color lookup table used by PSXRecomp: CRT models a consumer SMPTE-C-like
phosphor gamut, display gamma, luminance, and black floor; the other two retain
the corresponding upstream variants. This model changes color response only;
it does not add scanlines, curvature, a bezel, or persistence blur.

## Renderers, scaling, CRT, pacing and save states

The **GDI compatibility** renderer remains selectable and is also used
automatically if OpenGL initialization fails. Screen-color selection is
renderer-independent, so CRT produces the same transformed source pixels on
both presentation paths. **Nearest/Bilinear** controls only how that completed
frame is scaled. Settings persist in `launcher.cfg`; Raw remains the default
unless the user opts in. For repeatable diagnostics, `DKC2_SCREEN=raw`, `crt`,
`composite`, or `trinitron` overrides the saved screen model for one process.

Both desktop hosts offer experimental **Reconstruct** scaling. In the regular
`DKC2Recomp.exe`, select OpenGL and restart if currently using GDI; all five
reconstruction levels and the edge strength, softness, and smooth shading
sliders then apply live. `DKC2RecompSDL.exe` supports the same shader. The
shader source is shared, and all four screen-color presets compose with it.
The shader keeps pixel edges sharp at any
fractional scale, decodes the checkerboard and line dithers SNES artists
used for mid-tones, and rebuilds diagonal edges of the pre-rendered art
with an xBR-style corner test evaluated per output pixel, then softens
the result: wider transition bands and gradient shading where neighboring
colors are close. Its mode combo adds the stages one at a time and sliders
scale the edge blend, the softness, and the shading;
`DKC2_UPSCALER=nearest|bilinear|reconstruct` overrides the saved choice in SDL.

The Settings page's **Display** combo switches the Mac app from the flat
panel presentation to an optional **CRT television** simulation
([CRT_DISPLAY_PLAN.md](../CRT_DISPLAY_PLAN.md) is its design). It is not a scanline overlay:
every source line becomes an electron-beam profile whose width grows with
its brightness, so bright lines widen and merge while dark lines stay thin,
and the beam is normalised so the picture keeps its brightness. A fine
aperture-grille phosphor mask (three panel pixels per triad, below the eye's
resolving limit at arm's length), a soft glow and halation from blurred
copies, a gently curved tube face with rounded corners, and a dither finish
the look. "Living room" is the default preset; "Studio monitor" is sharper
and flat, "Soft" is wider and glowier, and the sliders (scanlines,
sharpness, mask, glow, halation, curvature) make a custom tube. The
upscaler is bypassed while the tube is on, and the tube fades to the flat
image in small windows where its lines cannot be drawn.
`DKC2_DISPLAY=flat|crt`, `DKC2_CRT_PRESET=living-room|studio|soft`, and
the `DKC2_CRT_*` sliders override the saved choice. The frame after the
phosphor-color model is the tube's input, so those models still apply; the
native frame, its hashes, and save states are untouched.

Visible OpenGL gameplay windows on Windows request a one-buffer swap interval
to reduce tearing. The accepted status is written with the presentation
backend in `diagnostics/last_run_report.json`; `on` means the graphics driver
accepted the request, while `request-failed` or `unsupported` means it did
not. Hidden automation disables the request so driver pacing cannot block
unattended tests, and GDI synchronization remains managed by the Windows
compositor. The Mac app instead paces each frame on the display's own refresh
tick and keeps the audio in step with dynamic rate control, so every frame is
shown for exactly one refresh on a 60-Hz or ProMotion display;
`DKC2_DISPLAY_LOCK=0` returns to the host clock and `DKC2_PACING_LOG=<file>`
records the cadence for `scripts/analyze_pacing_log.py`. Neither changes the
emulated 60.098811862 Hz clock.

Save states are named `saves/dkc2s0.sav` through `saves/dkc2s4.sav`; the
overlay presents these as Slots 1–5 and the native Mac Game menu uses Slot 1.
On macOS this relative directory lives under
`~/Library/Application Support/Flat2VR/DKC2Recomp`; portable builds keep it
beside the executable. The first slot still loads the former
`saves/dkc20.sav` name as a compatibility fallback, but all new writes use the
unambiguous names. States are separate from the cartridge SRAM files used for
normal in-game saves.

The launcher and game window use the development title
`DKC2 Recomp Alpha Pre-Release`; the game window appends the measured
presentation rate once per second.
Press `F` to write per-phase main-thread timings to `performance.log` beside
the executable; press it again to stop. The log identifies the active OpenGL
or GDI backend and selected screen model. It measures CPU time spent submitting
presentation work, but neither path currently collects GPU timestamp queries,
so GPU time remains explicitly unavailable instead of being reported as zero.

## Controllers

The launcher exposes independent Player 1 and Player 2 source selectors. By
default the keyboard controls Player 1 and the first connected gamepad controls
Player 2. The Windows host now uses SDL GameController for USB and Bluetooth
controllers. Select the actual controller for each player in the launcher's
controller list; device choices, sources, deadzones and bindings persist in
`launcher.cfg`. Both controllers can drive the two SNES ports independently.
Controllers connected after game launch are detected automatically; an
explicitly selected missing controller stays neutral until reconnected.
The bundled mapping also recognizes the 8BitDo SN30 Pro in Bluetooth DInput
mode, which the older SDL database omitted. Keyboard-mapping software is
unnecessary for the detected Xbox One S and SN30 Pro devices. In the pause
menu, each player's Controls tab shows its device and captures that player's
controller bindings. Physical button/rumble testing remains owner acceptance.

## DKC3 display and feedback parity

Display and controller parity with DKC3 is recorded in
[DKC3_FEATURE_PARITY.md](../DKC3_FEATURE_PARITY.md). Both hosts now expose
21:9 (446x224) alongside 4:3, 16:10, and 16:9. Stomp rumble and separate P1/P2
test pulses are in Escape > Settings, with controller routing matching input
assignment (keyboard P1 plus gamepad P2 uses that gamepad for P2 feedback).
Physical rumble sensation and full-game ultrawide coverage require further play.
