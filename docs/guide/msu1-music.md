# MSU-1 music

DKC2Recomp can replace the game's music with an MSU-1 soundtrack pack while
keeping the original sound effects. No patched ROM is needed.

## Setting it up

1. Download and extract an MSU-1 pack for DKC2. Extract the archive yourself;
   DKC2Recomp reads the extracted `.pcm` files directly.
2. Open **Escape > Settings > Audio** and choose the folder that contains the
   `dkc2_msu1-N.pcm` files.
3. Enable **Replacement music (MSU-1)** and set **Music volume** (0-200%).
   **Master volume** still controls music and sound effects together.

Track files named `dkc2_msu1-N.pcm`, `dkc2_msu-N.pcm` or `track-N.pcm` are
recognized. The folder must contain a valid track 1. BPS patches and `.msu`
marker files are not used. The folder, volume and on/off choice are saved in
`msu1.cfg`.

## What to expect

- Tracks missing from the pack fall back to the original SNES music.
- Fanfares, deaths, victories and similar jingles play once; level music
  loops as the pack defines.
- Loading a save state or rewinding restarts the current song from its
  beginning.
- Turning the replacement off mid-song resumes the original music where it
  paused.

Only the supported ROM (see [Installing](installing.md#supported-rom))
receives the music replacement. The ROM file itself is never modified.

To change the folder or volume for a single run, see
[Environment variables](advanced.md#audio).
