# Documentation index

- **Players:** start with the [user guide](guide/index.md). The same pages
  are published as the project's documentation site.
- **Building and testing:** see [BUILDING.md](../BUILDING.md).
- **Contributors:** read [AGENTS.md](../AGENTS.md) for the content boundary
  and the required workflow.

The rest of this folder is developer documentation. It stays in the
repository and is not published to the site.

## Project records

| Document | Contents |
| --- | --- |
| [IMPLEMENTATION_JOURNAL.md](IMPLEMENTATION_JOURNAL.md) | Plain-language record of what was done, why, and how it was checked. |
| [ROADMAP.md](ROADMAP.md) | Milestones and open work. |
| [CHANGELOG.md](../CHANGELOG.md) | User-visible changes by release. |
| [releases/](releases/) | Release notes for each published version, plus unreleased changes. |
| [evidence/](evidence/) | Validation evidence manifests for specific commits. |
| [RECONCILIATION.md](RECONCILIATION.md) | Provenance and disposition of the pre-upstream working tree. |
| [history/](history/) | Archived status files kept for provenance. |

## Architecture and hardware

| Document | Contents |
| --- | --- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design: analysis, execution, rendering, widescreen, co-op and host boundaries. |
| [HARDWARE_NOTES.md](HARDWARE_NOTES.md) | DKC2 cartridge map and SNES hardware behavior relied on by the port. |
| [CPU_CONFORMANCE.md](CPU_CONFORMANCE.md) | W65C816 instruction conformance references and tests. |
| [TIMING_AND_INTERRUPTS.md](TIMING_AND_INTERRUPTS.md) | Master-cycle timing, interrupts, HDMA and controllers. |
| [PPU_RENDERING.md](PPU_RENDERING.md) | Headless PPU renderer and reference-image comparison. |
| [SNESRECOMP_INTEGRATION.md](SNESRECOMP_INTEGRATION.md) | How the `snesrecomp` submodule is consumed. |
| [UPSTREAM_PR_PLAN.md](UPSTREAM_PR_PLAN.md) | Proposed upstream `snesrecomp` changes. |
| [dev/recompilation-status.md](dev/recompilation-status.md) | Static recompilation coverage and runtime-selected entries. |

## Features

| Document | Contents |
| --- | --- |
| [dev/presentation.md](dev/presentation.md) | Renderers, screen-color model, scaling, CRT, frame pacing and controller notes. |
| [dev/widescreen.md](dev/widescreen.md) | Widescreen margin reconstruction and per-stage status. |
| [WIDESCREEN_DIAGNOSTICS.md](WIDESCREEN_DIAGNOSTICS.md) | Deterministic widescreen evidence capture and route auditing. |
| [CRT_DISPLAY_PLAN.md](CRT_DISPLAY_PLAN.md) | Design of the CRT television display. |
| [dev/coop-internals.md](dev/coop-internals.md) | Simultaneous co-op behavior, coverage and private checks. |
| [dev/project-kongs.md](dev/project-kongs.md) | Donkey/Kiddy character-pack verification. |
| [dev/msu1.md](dev/msu1.md) | MSU-1 scheduler policy, track mapping and verification. |
| [DKC3_FEATURE_PARITY.md](DKC3_FEATURE_PARITY.md) | Desktop feature parity with DKC3Recomp. |

## Testing and tooling

| Document | Contents |
| --- | --- |
| [BUILD_HYGIENE.md](BUILD_HYGIENE.md) | Canonical build directories, outputs and test-version policy. |
| [CROSS_PLATFORM.md](CROSS_PLATFORM.md) | SDL host builds and native acceptance gates. |
| [DESKTOP_TESTING.md](DESKTOP_TESTING.md) | Interactive desktop test builds, crash drills and release packaging. |
| [FIRST_LEVEL_ROUTE_TESTING.md](FIRST_LEVEL_ROUTE_TESTING.md) | Recording and replaying deterministic gameplay routes. |
| [REFERENCE_WORKFLOW.md](REFERENCE_WORKFLOW.md) | Private reference-validation workflow. |
| [SYMBOL_DATABASE.md](SYMBOL_DATABASE.md) | Generated index of reviewed DKC2 symbols. |

## Policy and research

| Document | Contents |
| --- | --- |
| [LEGAL_AND_CONTENT.md](LEGAL_AND_CONTENT.md) | Legal and content boundary for contributors. |
| [RESEARCH_NOTES.md](RESEARCH_NOTES.md) | External research sources and reuse decisions. |
