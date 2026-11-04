# Repository audit — 2026-11-04

This is a source audit and initial integration checkpoint, not certification of a working slicer. No GUI build, U1 slicing run or physical print has passed yet. Read [feature matrix](feature-matrix.md), [decision](architecture-decision.md), and [roadmap](../roadmap.md) together.

## Verified sources and pins

| Source | Default | Audited commit | Release sample |
|---|---|---|---|
| [Snapmaker Orca / SnOrca](https://github.com/Snapmaker/OrcaSlicer) | main | f5fd7289ea067997181ee6c2cf15a98f58faba43 | v2.4.1, 2026-10-28 |
| [FOrcaSlicer](https://github.com/jiyang1018/FOrcaSlicer) | main | 0b1f80cd22793785d8ae5c4296d2fe4a9248bd21 | v2.3.2-fos.8.6.8, 2026-10-16 |
| [Official OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) | main | 9281032fdc3925474e2afb0af8ba4cca79fc626f | v2.4.2 stable; v2.5.0-rc 2026-11-01 |
| Official native MCP development | feature/mcp | 17a745e30c248cf3acb4c429b650b22d106fd19a | development branch; no release claim |
| [Extended Firmware](https://github.com/paxx12-snapmaker-u1/SnapmakerU1-Extended-Firmware) | develop | e086afa5068e3f724aa6ff9ca193dc742213c3c3 | v2.0.0-paxx12-24; rolling includes 2.1.0 development assets |
| [Snapmaker profiles](https://github.com/Snapmaker/snapmaker-profiles) | main | 1e201f6aa8920b4878daa02a21d43073ba92c06c | exact gitlink in audited Snapmaker source |

All three distinct slicer repositories were cloned with complete commit history and partial blob retrieval, then checked out for inspection. A separate clone of firmware develop is shallow. The profiles source was discovered in Snapmaker `.gitmodules` and `cmake/SyncSnapmakerProfiles.cmake`; Snapmaker main does **not** ship its active U1 JSON presets in resources/profiles until CMake copies the pinned submodule. Importing just that directory would omit the U1 presets.

**SnOrca is not an additional independent fork.** Snapmaker's [own retrospective](https://www.snapmaker.com/blog/snapmaker-2025-recap) calls Snapmaker Orca “Snorca”; its official repository README points to the same Snapmaker/OrcaSlicer releases. Community repositories using SnOrca in their name are not presumed canonical. No duplicate clone or double-counted feature source is needed.

The complete discovered branch lists and five-release samples are in [evidence](evidence/). They are snapshots, not exhaustive release histories. Open-issue samples contain up to 15 entries per repository and include PRs; they are not an exhaustive issue triage. Pins live in `tools/u1/sources.lock.json`.

## Git ancestry and divergence

`git merge-base` and `git rev-list --left-right --count` were run on fetched commit graphs.

| Comparison | Common ancestor | Snapmaker-only | Other-only | Changed paths |
|---|---|---:|---:|---:|
| Snapmaker vs official main | 737948be1f5b108b191420d4c670b511f8118604 | 674 | 7452 | 24299 |
| Snapmaker vs FOrca main | 99f25f4eed115d9285ec3abf49edd56c2b172760 | 195 | 203 | 1551 |

These are graph counts, not counts of useful independent patches. Changed paths include packaging, assets and localization. Rename detection reached Git's limit, so `.numstat` files must not be interpreted as exact semantic churn. Raw output is preserved in `evidence/ancestry.json` and `snapmaker-vs-*.numstat`.

The MCP branch is based on current official development. Its merge-base diff against audited main spans 325 paths, 71,978 insertions and 2,652 deletions. It touches CAD, UI action registration, modal/worker lifecycle, plugin APIs, tests and packaging. A small detached “MCP server file” port would not preserve its behavior.

## Implementations inspected

| Subsystem | Evidence and implication |
|---|---|
| Core engine and schema | `src/libslic3r/{Print,PrintObject,PrintConfig,GCode}.cpp` and `PrintConfig.hpp` in each tree. Shared ancestry does not make option arrays or project serialization interchangeable. FOrca adds `fos_filament_nozzle`, `fos_nozzle_*`, `color_patch_*`, `has_mixed_nozzle_sizes`. Current official code has a different generic multi-extruder/variant schema. |
| Snapmaker networking | Snapmaker `src/slic3r/Utils/Gateway{Account,Device,Protocol,Service}.*`, gateway regression tests, Flutter device resources, `GUI/filamentsync/`. These are substantial fork-specific integrations, not generic Moonraker behavior. |
| Official U1 networking | Official `Utils/SnapmakerPrinterAgent.cpp` subclasses `MoonrakerPrinterAgent`; `fetch_filament_info` queries `print_task_config` and `filament_detect`, maps vendors/materials/colors and optional NFC metadata. Generic base provides job submission/status. This does not prove parity with Snapmaker cloud pairing, gateway settings or feeding. |
| FOrca nozzle mapping | `PrintConfig.cpp` option definitions, `Print.cpp` preflight and remapping, `GCode.cpp` effective-nozzle selection, GUI per-nozzle settings. Per-object/foreign extruder import work appears in commit 012a2fb1f. |
| FOrca Color Patch | `PerimeterGenerator.cpp` checks actual Color Patch region identity and adjusts loops/flows; not just a checkbox. Full behavior still needs slicing and prints. |
| FOrca supply system | `Utils/MultiACE.*`, `libslic3r/FosFilamentArrangement.*` with bounded combinatorial search; topology and cross-diameter partitions are separate from final physical head binding. |
| Native MCP | Official feature/mcp `GUI/Mcp/{McpProtocol,McpHttpServer,McpCore,McpService,McpTools*}.*`; startup flags in `src/OrcaSlicer.cpp`; GUI settings and stdio bridge; existing Catch2 and replay tests. Official main's CAD `McpControl.*` alone is not the native network server. |
| Firmware/NFC | Extended Firmware `docs/design/rfid.md`, `docs/multiace.md`, `docs/helixscreen.md`, `overlays/.../13-patch-rfid/`, `64-app-openrfid/`, and Moonraker overlays. Optional components must be detected, never inferred from version. |

A focused graphify AST graph was generated locally for the 77 native MCP code files (2,893 nodes, 7,784 edges). It aids navigation; extracted relationships are not runtime evidence. Generated graphs are ignored by Git.

## Issues and limitations

FOrca's sampled open issues include [Color Patch incorrect #15](https://github.com/jiyang1018/FOrcaSlicer/issues/15), [login window closes #14](https://github.com/jiyang1018/FOrcaSlicer/issues/14), and [upgrade for high-flow configuration #13](https://github.com/jiyang1018/FOrcaSlicer/issues/13). These are reported issues, not locally reproduced defects. FOrca's README explicitly identifies a research preview without independent bed testing. Snapmaker and official issue/PR samples are stored alongside the source evidence; further triage is required before release.

Relevant official branches include feature/mcp, feat/printer-agent-filament-mapping, feat/generic-extruders-and-ams, feature/update_wipetower, FullSpectrum_integration, release/v2.4 and release/v2.5.0. Snapmaker has release_2.4.1, port/main-20261026, feature_multi_extruders_dev and active gateway fix branches. FOrca has fos-8.6-dev, older fos-* series and clean-main. Branch names do not establish correctness; only the pinned code was inspected in depth.

Other projects discovered, not imported or certified: Snapmaker/u1-klipper, Snapmaker/u1-moonraker, Snapmaker/u1-fluidd (linked by the official U1 FAQ); HelixScreen U1 support; openspool-snOrca; u1hub; FullSpectrum forks. Their independent licenses, APIs and maintenance health still need scoped audits before code reuse.

## Licensing and dependencies

The slicer roots declare AGPL-3.0; preserve their notices and disclose modifications with corresponding source when distributing. The imported FOrca optimizer has the same root license; attribution and hashes are recorded in `docs/architecture/imports.md`. Extended Firmware declares GPL-3.0 and is inspected, not linked into the slicer. No license file was found in the pinned separate Snapmaker profiles tree: redistribution of those snapshots is blocked pending license clarification; local review catalog generation is not a distribution approval.

Established CMake/deps systems remain intact. Dependencies include Boost, TBB, wxWidgets/OpenGL, OCCT, image codecs, bundled Python/uv and platform libraries. Source recipes and license notices need a complete distribution/SBOM review; an AGPL root is not proof that every dependency or asset can be redistributed unchanged. No proprietary network binary has been imported.

## Build evidence and boundaries

All slicers use C++17/CMake and platform build scripts. FOrca has macOS ARM64/x86 and Linux workflows; official Orca includes mature platform build, profile and test workflows. Existing workflows are source evidence only; none was dispatched here. Native Windows and macOS compilers are unavailable on this Linux x86_64 host.

A project-local environment pins CMake 3.31.10 and Ninja 1.13.0. Full Release configuration initially failed while downloading pinned uv in the network sandbox; the authorized retry downloaded it, then failed at missing Boost >=1.83. No full app build is claimed. A small CMake component target reuses actual production protocol/planner/policy sources and bundled Catch2; its results are recorded in `docs/testing/local-validation.md`. Passing it does not prove wxWidgets linkage, project compatibility, slicing or hardware behavior.
