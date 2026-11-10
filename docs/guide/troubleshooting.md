# Troubleshooting and crash reports

## The launcher rejects my ROM

Only the North American v1.0 ROM is supported. Compare your file with the
table in [Installing](installing.md#supported-rom). A 512-byte copier header
is fine; other regions and revisions are not.

## The Mac app will not open

The app is ad-hoc signed but not notarized. Control-click it in Finder,
choose **Open** and confirm once.

## OpenGL fails on Windows

The Windows host falls back to the GDI compatibility renderer automatically.
GDI supports the overlay and Nearest/Bilinear scaling, but not Reconstruct or
the CRT television. Updating your graphics driver may restore OpenGL.

## Last-run report

Every run writes `diagnostics/last_run_report.json`. It records the
presentation backend and whether vsync was accepted: `on` means the graphics
driver accepted the request, while `request-failed` or `unsupported` means it
did not.

## Support bundles

A runtime failure, or a native Windows exception, creates a timestamped
`diagnostics/diagnostic_bundle_*` folder. Windows exception bundles include a
minidump. To request a bundle after a normal exit, set
`DKC2_DIAGNOSTIC_BUNDLE=1` before launching (see
[Environment variables](advanced.md#files-and-diagnostics)).

A bundle contains only:

- the JSON run report and instructions;
- your `launcher.cfg`, if present;
- `performance.log`, if present;
- a Windows minidump, if one was written.

It never contains `rom.cfg`, ROM bytes or paths, generated game code, saves,
save states, screenshots or audio captures. It **does** include loaded
program-module paths and basic operating-system and hardware information, so
look through the folder before sharing it.

## Performance log

Press **F** during play to start writing per-phase main-thread timings to
`performance.log`, and press it again to stop. The log names the active
renderer and screen model. It measures CPU time only; GPU time is reported as
unavailable rather than zero.

The game window title shows the measured presentation rate once per second.
