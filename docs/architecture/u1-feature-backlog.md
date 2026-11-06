# Current parity implementation backlog

2026-11-06 user priority: U1 is the only target printer. Finish complete Snapmaker stock behavior and its native device/UI/companion integration before optional Orca/FOrca/MCP additions. Hardware availability is not a blocker to available source porting. The software gate requires connected consumers, migration, runtime dependencies, packaging and passing offline tests; then hand over the separate hardware checklist. Current source-only or partially connected ports remain Partial.

Current checkpoint: original Snapmaker single/four-tool 3MF fixtures slice with the preserved machine macros; support migration and core configuration regressions pass. The imported gateway foundation passes 38 offline cases but is not connected to the device UI/isolated companion startup. Continue from that dependency boundary rather than treating gateway source import as finished camera/pairing/RFID/feeder integration.

Use [functional-parity-audit.md](functional-parity-audit.md) and its exact-source JSON as the detailed feature inventory. The original narrower checkpoint follows below for history; it is not a claim of full parity.

## Priority and dependencies

| Priority | Implementation package | Dependencies | Acceptance |
|---|---|---|---|
| P0 | Finish bundled plugin discovery, explicit disabled installation and native UI catalog verification | Existing plugin host; deterministic wheels | Both packages visible, no auto-load, user content preserved; native Windows check |
| P0 | Original Snapmaker 3MF and automatic support geometry | Exact v2.4.1 support implementation; schema migration | Load/save/slice original single/four-tool projects; automatic/explicit support footprint comparisons |
| P0 | Unified stock/Extended capability model and recorded fixtures | Documented per-service APIs | Unknown remains unknown; API/service differences and installed nozzle state preserved |
| P0 | Snapmaker gateway, pairing and native device model | Capability model; companion/runtime/license audit | Offline protocol tests, then separately authorized read-only live verification |
| P0 | Camera, RFID, filament inventory, automatic feeder and cover status | Validated gateway/firmware interfaces; exact cover variant | Native UI state/transport tests; no generic Bambu or Moonraker substitution claims |
| P0 | High-flow schema, SSWCP mapping and nozzle/profile selection | Device model; migration | Per-head flow variants, compatible materials and round-trip projects; no invented calibration |
| P0 | Complete typed MCP project/file controls and operator-bound approval adapters | Migration; native lifecycle; authorized roots | No generic script/UI bypass, no token exposure, new-file safety and reviewed destructive confirmation |
| P0 | FOrca schema/mapping and native role assignment adapters | Project migration; head/flow model | All widths/speeds/assignments preserved; unsupported keys never silently discarded |
| P0 | Signed Windows release and native macOS ARM64 bundle | Real signing identity; all applicable tests | Trusted timestamped signatures and full native build results |
| P1 | Complete prime-tower and support-transition parity | Material groups, thermal state, support schema | Semantic path/temperature/interface/consumption comparisons against reference slicers |
| P1 | Full Spectrum recipe/mode/decomposition/subdivision migration | Mixed-filament serialization; geometry tests | Ratio/Cycle/Match/Gradient and advanced modes verified individually |
| P1 | FOrca Color Patch and per-nozzle engine consumers | FOrca schema, nozzle mapping and role assignment | Shell/core geometry, tool-specific paths and material checks; ordinary painting is not equivalence |
| P1 | Material/profile synchronization and override import | Schema validation; attribution/licensing | Preserve user overrides/inheritance and flag uncalibrated imports |
| Gate | Supervised hardware validation | Every software gate above | No unattended heating, homing, printing, macros or firmware changes |

Coupled generator/schema/protocol ports must stay reviewable. Do not add inert settings, clamp incompatible values or mark a plugin substitute as a kernel implementation. No production or physical compatibility claim is possible from offline tests alone.

---

# Whole-application U1 feature integration

The scope is the complete slicer. Preserve and integrate every compatible Orca/FOrca capability that benefits U1: slicing algorithms, process controls, modeling/painting, calibration, project formats, UI, diagnostics, connectivity and native AI automation. Profiles are one subsystem. Reuse the full official implementation already in this application; do not rewrite a feature merely because a fork uses different names.

Sources: [official Orca](https://github.com/OrcaSlicer/OrcaSlicer), [Snapmaker Orca / SnOrca](https://github.com/Snapmaker/OrcaSlicer), and [FOrcaSlicer](https://github.com/jiyang1018/FOrcaSlicer). FOrca is the `forca` remote and a watched `main` branch in `tools/u1/sources.lock.json`. Its unchanged branch does not imply its fork-specific features have all been integrated. Pins record audited source snapshots, not blanket feature-parity claims.

## Source-backed inventory

These implementation locations were inspected in the selected full Orca base. “Implemented but untested” here means source exists; it does not imply all U1 presets, GUI paths or physical behavior have passed. Use the narrower executed evidence in feature-matrix.md and docs/testing/.

| Capability | Implementation retained in this application | Current U1 evidence or gap |
|---|---|---|
| Four-tool and mixed-nozzle slicing | `src/libslic3r/Print.cpp`, `PrintConfig.cpp`, `PrintRegion.cpp`, `GCode.cpp` | Synthetic one/four-tool and 0.4/0.6 mm path widths verified; vendor project migration remains incompatible |
| Independent wall/infill/surface tool assignments | `PrintConfig.cpp` defines outer_wall_filament_id, inner_wall_filament_id, sparse_infill_filament_id, internal_solid_filament_id, top_surface_filament_id and bottom_surface_filament_id; `PrintRegion.cpp` resolves roles; `GUI/Plater.cpp` registers role selectors and `GUI/ConfigManipulation.cpp` controls their availability | Implemented but untested as a complete U1 role-assignment workflow; inherited `test_multifilament.cpp` covers these behaviors |
| Per-object/part overrides and multimaterial painting | `Model.cpp`, `MultiMaterialSegmentation.cpp`, `GUI/Gizmos/GLGizmoPainterBase.cpp` | Implemented but untested across imported U1 projects and FOrca metadata |
| Arachne walls and thin-feature generation | `src/libslic3r/Arachne/WallToolPaths.cpp` | Implemented but untested for complete U1-specific nozzle/material combinations; inherited perimeter tests retained |
| Precise seams/scarf seams | `GCode/SeamPlacer.cpp`, `GCode/PreciseSeam.cpp`, `PrintConfig.cpp` and scarf emission in `GCode.cpp` | Implemented but untested for U1 output parity; preserve seam/perimeter regression coverage |
| Adaptive layers and advanced infill | `SlicingAdaptive.cpp`, `Fill/FillAdaptive.cpp`, `Fill/FillGyroid.cpp`, `Fill/FillLightning.cpp` | Implemented but untested as a complete U1 workflow; slicing/flow tests retained |
| Normal/tree supports and support painting | `Support/TreeSupport.cpp`, `Support/SupportCommon.cpp`, `GUI/Gizmos/GLGizmoFdmSupports.cpp` | Implemented but untested; Snapmaker automatic expansion -1 has different semantics and is a known import blocker |
| Ironing, fuzzy skin and surface processing | `PrintConfig.cpp`, `Feature/FuzzySkin/FuzzySkin.cpp`, `GUI/Gizmos/GLGizmoFuzzySkin.cpp` | Implemented but untested for U1 calibration; not profile-only features |
| Bridges, overhangs, cooling and pressure advance | `BridgeDetector.cpp`, G-code cooling/FanMover/pressure-advance paths and their inherited tests | Implemented but untested against actual U1 firmware commands and tool-specific thermal behavior |
| Calibration workflows | `GUI/Calibration.cpp`, `CalibrationPanel.cpp`, `ExtrusionCalibration.cpp` | Implemented but untested for U1-safe emitted G-code; retain generic calibration, adapt printer-specific commands before promotion |
| Arrangement, plates, STL/STEP/3MF workflows | `Arrange.cpp`, `ModelArrange.cpp`, `GUI/Jobs/ArrangeJob.cpp`, `Format/STEP.cpp`, `Format/bbs_3mf.cpp` | Implemented but untested comprehensively; own-profile cube export passes, original Snapmaker 3MF validation fails |
| Native MCP and extensible UI/CAD workflows | `GUI/Mcp/`, `GUI/CAD/` | Native inspection/planning/STL slicing verified in isolated Linux GUI; file/settings/printer authorization adapters remain incomplete |
| Mixed-filament/full-spectrum processing | Existing mixed-filament config, tool-ordering and slicing implementations; `test_mixed_filament.cpp` | Implemented but untested as a U1 workflow; distinct from FOrca Color Patch shell/core semantics |
| FOrca per-nozzle width/speed arrays | Audited FOrca `PrintConfig.cpp` fos_nozzle_* definitions and downstream PrintObject/GCode consumers | Partially implemented: generic percentage widths are verified; FOrca arrays, full migration and assignment UI not ported |
| FOrca Color Patch, mapping and MultiACE integration | Audited FOrca color_patch_enabled/color_patch_loops definitions, slicing and connectivity paths | Missing full integration; inspect implementation and material/firmware prerequisites; do not equate this with ordinary painting or mixed-layer color |

## Integration order and acceptance

1. Preserve reliable U1 project loading and four-head G-code. Port Snapmaker's automatic support semantics with reference geometry and configuration migration; never silently clamp -1. Preserve current connectivity while implementing current gateway/pairing/feeding parity.
2. Exercise retained upstream role assignment, supports, modifiers, seams, infill, calibration and multimaterial regressions through the actual engine and U1 fixtures. Add new tests only for untested U1 invariants, rather than copying tests already upstream. The full inherited FFF suite is being built/executed in addition to the focused U1 fixture.
3. Map FOrca feature settings to native equivalents where semantics match. Port coupled schema/geometry/G-code/UI changes where they do not. Preserve per-head widths, speeds, material assignments, nozzle verification and project round trips together. Keep original attribution and reference-output comparisons.
4. Integrate Color Patch and MultiACE only with explicit geometry/material/firmware capability contracts, offline regressions and supervised hardware gates. Keep generic Moonraker separate from Snapmaker APIs.
5. Expand native MCP to the retained application features using typed handlers, authorized file roots and operator-bound approvals. Do not bypass the restricted catalog through generic UI clicks, scripts or macros.
6. For every upstream release/feature/fix, classify the whole repository diff and record Adopt / Already present / Needs adapter / Deferred / Incompatible / Unknown with source/test evidence. Unknown is not Missing. Preserve useful unrelated-printer functionality when it does not compromise U1.

The scheduled watcher reports branch/release/tag changes for all sources, with full-slicer subsystem summaries for unseen branch events. It does not automatically integrate code. A source-present feature becomes “verified” only for the actual tests that pass; hardware compatibility remains provisional until physical printing tests.

## Development-tip follow-up

The refreshed audit also inspects byte-validated exports of official main f96bbe8db13f603c767f0a21fce80da85c6a09f4, MCP tip 56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7 and Snapmaker tip b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb. These are comparison references, not fully integrated baselines. After project migration, review the P1 `snapmaker-tip-cooling-motion` group: six new cooling/infill/travel schema names require consumer/alias and emitted-behavior comparisons before adoption. The original exact-v2.4.1 findings remain separate.

Live notification run [42095557022](https://github.com/zhavir/ultimate-u1-slicer/actions/runs/42095557022) passed all 49 tooling tests and observed all 11 sources without observation errors. New review items since the audited tips: Snapmaker `6dd88c98f9` fixes gateway WebSocket shutdown (port together with the missing gateway stack and lifecycle tests); Orca `a620d804ef` changes by-layer copy ordering (candidate for a focused order regression); `637d7a9ce6` changes automatic vendor update defaults (review against managed-catalog/override boundaries before adopting); `73766ddd42` changes the PR template. None is claimed integrated. Full observation/notification evidence is under `evidence/upstream-notifications-2026-11-05.json`; alerts are assigned to zhavir.
