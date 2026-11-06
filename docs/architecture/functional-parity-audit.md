# Functional parity audit — 2026-11-05

Bounded source-backed feature inventory, not certification. Read code/test evidence and dependencies; key overlap does not prove semantic parity.

Exact reference source revisions: `snapmaker-v241` `bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`, `snapmaker-main` `f5fd7289ea067997181ee6c2cf15a98f58faba43`, `orca-mcp-base` `17a745e30c248cf3acb4c429b650b22d106fd19a`, `forca` `0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`, `orca-main-tip` `f96bbe8db13f603c767f0a21fce80da85c6a09f4`, `orca-mcp-tip` `56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`, `snapmaker-tip` `b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`.

**There is no 100% U1 compatibility or stable-release claim.** The exact v2.4.1 release and post-release Snapmaker main are separate evidence columns.

## Summary

| Status | Features |
|---|---:|
| Verified | 6 |
| Implemented but untested | 11 |
| Partial | 39 |
| Missing | 11 |
| Incompatible | 0 |
| Unknown | 5 |

## Feature matrix

| ID | Feature | Status | Priority | Depends on |
|---|---|---|---|---|
| [tower-grouping](#tower-grouping) | Material compatibility grouping | Partial | P0 | — |
| [tower-preextrusion](#tower-preextrusion) | Interface pre-extrusion distance and length | Implemented but untested | P0 | tower-grouping |
| [tower-temperature](#tower-temperature) | Interface temperature and tool-change thermal waits | Partial | P0 | tower-grouping |
| [tower-cooling](#tower-cooling) | Cooling before tower and during interfaces | Implemented but untested | P0 | tower-temperature |
| [tower-ribs](#tower-ribs) | Tower ribs, wall gap, brim and chamfer | Partial | P1 | tower-grouping |
| [tower-toolpaths](#tower-toolpaths) | Special U1 tool-change and docking paths | Partial | P0 | tower-temperature, profile-macros |
| [tower-accounting](#tower-accounting) | Non-Bambu Type 1 tower material accounting | Verified | P1 | — |
| [support-transitions](#support-transitions) | Transition layers, speed, flow and perimeters | Missing | P0 | project-migration |
| [support-contact](#support-contact) | Minimum support-interface contact-area threshold | Missing | P0 | support-transitions |
| [support-adaptive](#support-adaptive) | Snapmaker adaptive tree support layers | Missing | P1 | support-transitions |
| [painting-depth](#painting-depth) | Top and bottom painting penetration controls | Implemented but untested | P1 | project-migration |
| [support-auto](#support-auto) | Automatic negative raft/support expansion | Partial | P0 | — |
| [spectrum-ratio](#spectrum-ratio) | Ratio mixing | Partial | P1 | project-migration |
| [spectrum-cycle](#spectrum-cycle) | Cycle and interleaved-layer mixing | Partial | P1 | spectrum-ratio |
| [spectrum-match](#spectrum-match) | Color Match and matching algorithms | Partial | P1 | spectrum-ratio |
| [spectrum-gradient](#spectrum-gradient) | Gradient curves and ranges | Partial | P1 | spectrum-ratio |
| [spectrum-decompose](#spectrum-decompose) | Color decomposition and component selection | Implemented but untested | P1 | spectrum-match |
| [spectrum-subdivision](#spectrum-subdivision) | Geometry subdivision and textured segmentation | Implemented but untested | P1 | spectrum-decompose |
| [spectrum-advanced](#spectrum-advanced) | Advanced dithering, pointillism and local-Z modes | Partial | P1 | spectrum-cycle, spectrum-subdivision |
| [fos-color-patch](#fos-color-patch) | Color Patch shell/core geometry and loops | Missing | P1 | fos-nozzles, fos-widths, project-fos |
| [fos-nozzles](#fos-nozzles) | Independent mixed nozzle configuration and mapping | Partial | P0 | project-fos |
| [fos-widths](#fos-widths) | Per-nozzle wall, infill, support and tower widths | Partial | P1 | fos-nozzles |
| [fos-speeds](#fos-speeds) | Per-nozzle feature speeds and thermal constraints | Missing | P1 | fos-nozzles |
| [fos-roles](#fos-roles) | Outer/inner wall and sparse/solid infill tool assignments | Partial | P0 | project-fos |
| [fos-support-tower](#fos-support-tower) | Support/interface/prime-tower filament selection | Implemented but untested | P1 | fos-roles |
| [fos-object-overrides](#fos-object-overrides) | Per-object and per-filament overrides | Partial | P1 | project-fos |
| [fos-nozzle-safety](#fos-nozzle-safety) | Nozzle verification and incompatibility checks | Partial | P0 | high-flow, fos-nozzles |
| [filament-planner](#filament-planner) | Advisory filament/nozzle partition planner | Verified | P1 | — |
| [u1-lan](#u1-lan) | U1 LAN discovery and network submission | Partial | P0 | firmware-capabilities |
| [u1-gateway](#u1-gateway) | Snapmaker gateway transport and device protocol | Partial | P0 | — |
| [u1-cloud](#u1-cloud) | Snapmaker cloud account, pairing and authorization | Missing | P0 | u1-gateway |
| [u1-status](#u1-status) | Device status, job, progress and temperatures | Partial | P0 | u1-lan |
| [u1-camera](#u1-camera) | U1 camera, authentication and streaming | Missing | P0 | u1-gateway, firmware-capabilities |
| [u1-rfid](#u1-rfid) | U1 RFID/NFC filament metadata and refresh | Partial | P0 | u1-gateway, firmware-capabilities |
| [u1-filaments](#u1-filaments) | Filament inventory, assignments and synchronization | Partial | P0 | u1-rfid, high-flow |
| [u1-feeder](#u1-feeder) | Automatic feeding and unloading | Unknown | P0 | u1-gateway, firmware-capabilities |
| [u1-multiace](#u1-multiace) | MultiACE device integration | Missing | P1 | u1-feeder, fos-nozzles |
| [u1-cover](#u1-cover) | Top cover/door/enclosure capability and status | Unknown | P0 | firmware-capabilities |
| [high-flow](#high-flow) | High-flow hotend detection and compatibility | Partial | P0 | u1-gateway, project-migration |
| [nozzle-02](#nozzle-02) | Uniform 0.2 mm U1 profile | Implemented but untested | P1 | profile-visibility |
| [nozzle-04](#nozzle-04) | Uniform 0.4 mm U1 profile | Verified | P0 | profile-visibility |
| [nozzle-06](#nozzle-06) | Uniform 0.6 mm U1 profile | Implemented but untested | P1 | profile-visibility |
| [nozzle-08](#nozzle-08) | Uniform 0.8 mm U1 profile | Implemented but untested | P1 | profile-visibility |
| [nozzle-mixed](#nozzle-mixed) | Mixed 0.4+0.6 U1 profile and arbitrary head combinations | Partial | P0 | fos-nozzles |
| [profile-visibility](#profile-visibility) | Printer wizard and selected-preset visibility | Partial | P0 | — |
| [profile-macros](#profile-macros) | U1 machine start/end/tool-change macro preservation | Partial | P0 | project-migration |
| [profile-sync](#profile-sync) | Attribution, inheritance, collisions and user overrides | Partial | P1 | — |
| [project-migration](#project-migration) | Original Snapmaker 3MF import and configuration migration | Partial | P0 | support-auto |
| [project-export](#project-export) | 3MF save/export and metadata fidelity | Partial | P0 | project-migration |
| [project-fos](#project-fos) | FOrca schema and object/filament metadata migration | Missing | P0 | — |
| [mcp-core](#mcp-core) | Native protocol, authentication and stdio | Verified | P0 | — |
| [mcp-transform](#mcp-transform) | Move, rotate, scale, arrange and inspect | Partial | P1 | mcp-core |
| [mcp-slicing](#mcp-slicing) | Slicing, estimates, consumption, warnings and export | Partial | P0 | mcp-core, project-migration |
| [mcp-project-files](#mcp-project-files) | Open/import/create/save/export projects and files | Partial | P0 | mcp-core, project-migration |
| [mcp-settings](#mcp-settings) | Object/material/support/profile authoring | Partial | P1 | mcp-core, project-fos |
| [mcp-destruction](#mcp-destruction) | Duplicate/delete and destructive operation approval | Partial | P0 | mcp-core |
| [mcp-printer](#mcp-printer) | Authorized printer state, submission and controls | Missing | P0 | u1-gateway, firmware-capabilities |
| [firmware-stock](#firmware-stock) | Stock U1 firmware API and G-code behavior | Partial | P0 | u1-gateway, profile-macros |
| [firmware-extended](#firmware-extended) | Extended Firmware 2.1 and optional services | Partial | P0 | firmware-capabilities |
| [firmware-capabilities](#firmware-capabilities) | Dynamic capability detection and explicit unknowns | Partial | P0 | — |
| [plugins-discovery](#plugins-discovery) | Bundled plugin discovery, consent and installation | Partial | P0 | — |
| [plugin-studio](#plugin-studio) | Studio read-only project inspection and preflight | Verified | P1 | plugins-discovery |
| [plugin-converter](#plugin-converter) | External converter connector and project-copy workflow | Verified | P1 | plugins-discovery |
| [windows-signing](#windows-signing) | Windows-trusted Authenticode signatures | Partial | P0 | — |
| [macos-build](#macos-build) | Native macOS ARM64 application and packaging | Unknown | P0 | — |
| [hardware-print](#hardware-print) | Physical single/four-tool/mixed-nozzle validation | Unknown | P0 | project-migration, u1-gateway, fos-nozzles, profile-macros |
| [orca-engine](#orca-engine) | Retained walls, infill, cooling, seams and G-code engine | Partial | P1 | — |
| [orca-geometry](#orca-geometry) | STL/STEP/3MF, modeling, painting and CAD | Implemented but untested | P1 | — |
| [orca-calibration](#orca-calibration) | Calibration and process workflows | Implemented but untested | P1 | profile-macros |
| [orca-gates](#orca-gates) | Integration changes, disabled features and default policies | Partial | P0 | — |
| [high-flow-detection](#high-flow-detection) | Detect and reconcile reported U1 high-flow hotends | Missing | P0 | u1-gateway, high-flow |
| [snapmaker-tip-cooling-motion](#snapmaker-tip-cooling-motion) | Snapmaker development cooling, infill margin and short-travel changes | Unknown | P1 | project-migration |

The detailed JSON contains exact source file hashes, configuration definitions, line numbers, symbols, schema differences and the complete integration source-path diff. Source hits are evidence for inspection, not an automatic equivalence verdict.

<a id="tower-grouping"></a>
## Material compatibility grouping

**Partial; P0.** Dependencies: none.

Generic grouping and an advisory FOrca planner exist; neither proves Snapmaker material-grouping parity.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerHelper.cpp`, `src/libslic3r/GCode/WipeTowerHelper.hpp`. Keys: `filament_grouping_mode`, `filament_is_high_temperature`, `filament_type`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerHelper.cpp`, `src/libslic3r/GCode/WipeTowerHelper.hpp`. Keys: `filament_grouping_mode`, `filament_is_high_temperature`, `filament_type`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerEstimate.cpp`, `src/libslic3r/GCode/WipeTowerEstimate.hpp`. Keys: `filament_type`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/FosFilamentArrangement.cpp`, `src/libslic3r/FosFilamentArrangement.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `filament_is_high_temperature`, `filament_type`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/FosFilamentArrangement.cpp`, `src/libslic3r/FosFilamentArrangement.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `filament_is_high_temperature`, `filament_type`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerEstimate.cpp`, `src/libslic3r/GCode/WipeTowerEstimate.hpp`. Keys: `filament_type`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerEstimate.cpp`, `src/libslic3r/GCode/WipeTowerEstimate.hpp`. Keys: `filament_type`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerHelper.cpp`, `src/libslic3r/GCode/WipeTowerHelper.hpp`. Keys: `filament_grouping_mode`, `filament_is_high_temperature`, `filament_type`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="tower-preextrusion"></a>
## Interface pre-extrusion distance and length

**Implemented but untested; P0.** Dependencies: tower-grouping.

Compare actual four-tool paths and interface extrusion using stock U1 macros.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `filament_tower_interface_pre_extrusion_dist`, `filament_tower_interface_pre_extrusion_length`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `filament_tower_interface_pre_extrusion_dist`, `filament_tower_interface_pre_extrusion_length`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_pre_extrusion_dist`, `filament_tower_interface_pre_extrusion_length`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_pre_extrusion_dist`, `filament_tower_interface_pre_extrusion_length`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_pre_extrusion_dist`, `filament_tower_interface_pre_extrusion_length`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_pre_extrusion_dist`, `filament_tower_interface_pre_extrusion_length`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `filament_tower_interface_pre_extrusion_dist`, `filament_tower_interface_pre_extrusion_length`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="tower-temperature"></a>
## Interface temperature and tool-change thermal waits

**Partial; P0.** Dependencies: tower-grouping.

A matching temperature key does not prove matching waits, standby or reheating behavior.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `delta_temperature`, `filament_tower_interface_print_temp`, `tool_change_temprature_wait`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `delta_temperature`, `filament_tower_interface_print_temp`, `tool_change_temprature_wait`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_print_temp`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `delta_temperature`, `tool_change_temprature_wait`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_print_temp`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_print_temp`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `filament_tower_interface_print_temp`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `delta_temperature`, `filament_tower_interface_print_temp`, `tool_change_temprature_wait`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="tower-cooling"></a>
## Cooling before tower and during interfaces

**Implemented but untested; P0.** Dependencies: tower-temperature.

Validate cooling commands and ordering in generated U1 G-code; no heater/fan hardware tests.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: `enable_tower_interface_cooldown_during_tower`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: `enable_tower_interface_cooldown_during_tower`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `enable_tower_interface_cooldown_during_tower`, `filament_cooling_before_tower`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `enable_tower_interface_cooldown_during_tower`, `filament_cooling_before_tower`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `enable_tower_interface_cooldown_during_tower`, `filament_cooling_before_tower`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `enable_tower_interface_cooldown_during_tower`, `filament_cooling_before_tower`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: `enable_tower_interface_cooldown_during_tower`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="tower-ribs"></a>
## Tower ribs, wall gap, brim and chamfer

**Partial; P1.** Dependencies: tower-grouping.

Some options are shared; fork-only geometry keys need coupled geometry tests, not inert schema entries.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerHelper.cpp`, `src/libslic3r/GCode/WipeTowerHelper.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_width`, `wipe_tower_rib_width`, `wipe_tower_wall_gap`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerHelper.cpp`, `src/libslic3r/GCode/WipeTowerHelper.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_width`, `wipe_tower_rib_width`, `wipe_tower_wall_gap`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerEstimate.cpp`, `src/libslic3r/GCode/WipeTowerEstimate.hpp`. Keys: `prime_tower_width`, `wipe_tower_rib_width`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/slic3r/GUI/WipeTowerDialog.cpp`, `src/slic3r/GUI/WipeTowerDialog.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_width`, `wipe_tower_rib_width`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerEstimate.cpp`, `src/libslic3r/GCode/WipeTowerEstimate.hpp`. Keys: `prime_tower_width`, `wipe_tower_rib_width`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerEstimate.cpp`, `src/libslic3r/GCode/WipeTowerEstimate.hpp`. Keys: `prime_tower_width`, `wipe_tower_rib_width`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerEstimate.cpp`, `src/libslic3r/GCode/WipeTowerEstimate.hpp`. Keys: `prime_tower_width`, `wipe_tower_rib_width`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`, `src/libslic3r/GCode/WipeTowerHelper.cpp`, `src/libslic3r/GCode/WipeTowerHelper.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_width`, `wipe_tower_rib_width`, `wipe_tower_wall_gap`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="tower-toolpaths"></a>
## Special U1 tool-change and docking paths

**Partial; P0.** Dependencies: tower-temperature, profile-macros.

Retained machine macros are not proof of optimized Snapmaker tower/tool-change path equivalence.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: `change_filament_gcode`, `enable_change_pressure_when_wiping`, `ramming_line_width_ratio`, `ramming_pressure_advance_value`, `z_hop_when_prime`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: `change_filament_gcode`, `enable_change_pressure_when_wiping`, `ramming_line_width_ratio`, `ramming_pressure_advance_value`, `z_hop_when_prime`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `change_filament_gcode`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: `change_filament_gcode`, `enable_change_pressure_when_wiping`, `ramming_line_width_ratio`, `ramming_pressure_advance_value`, `z_hop_when_prime`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `change_filament_gcode`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `change_filament_gcode`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`. Keys: `change_filament_gcode`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`. Keys: `change_filament_gcode`, `enable_change_pressure_when_wiping`, `ramming_line_width_ratio`, `ramming_pressure_advance_value`, `z_hop_when_prime`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="tower-accounting"></a>
## Non-Bambu Type 1 tower material accounting

**Verified; P1.** Dependencies: none.

Verified only for the adopted upstream engine regression and full FFF suite, not physical U1 material usage.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_brim_width`, `prime_tower_enable_framework`, `prime_tower_width`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_brim_width`, `prime_tower_enable_framework`, `prime_tower_width`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `prime_tower_brim_width`, `prime_tower_enable_framework`, `prime_tower_flat_ironing`, `prime_tower_infill_gap`, `prime_tower_skip_points`, `prime_tower_width`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_brim_width`, `prime_tower_width`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `prime_tower_brim_width`, `prime_tower_enable_framework`, `prime_tower_flat_ironing`, `prime_tower_infill_gap`, `prime_tower_skip_points`, `prime_tower_width`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `prime_tower_brim_width`, `prime_tower_enable_framework`, `prime_tower_flat_ironing`, `prime_tower_infill_gap`, `prime_tower_skip_points`, `prime_tower_width`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`. Keys: `prime_tower_brim_width`, `prime_tower_enable_framework`, `prime_tower_flat_ironing`, `prime_tower_infill_gap`, `prime_tower_skip_points`, `prime_tower_width`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/WipeTower.cpp`, `src/libslic3r/GCode/WipeTower.hpp`, `src/libslic3r/GCode/WipeTower2.cpp`, `src/libslic3r/GCode/WipeTower2.hpp`. Keys: `prime_tower_brim_chamfer`, `prime_tower_brim_chamfer_max_width`, `prime_tower_brim_width`, `prime_tower_enable_framework`, `prime_tower_width`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="support-transitions"></a>
## Transition layers, speed, flow and perimeters

**Missing; P0.** Dependencies: project-migration.

Snapmaker transition schema/consumer path is absent; import its coupled generator and tests.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/SupportTransitionLayer.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`. Keys: `support_transition_flow_ratio`, `support_transition_perimeter`, `support_transition_speed`, `tree_support_transition_layers`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/SupportTransitionLayer.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`. Keys: `support_transition_flow_ratio`, `support_transition_perimeter`, `support_transition_speed`, `tree_support_transition_layers`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/SupportTransitionLayer.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`. Keys: `support_transition_flow_ratio`, `support_transition_perimeter`, `support_transition_speed`, `tree_support_transition_layers`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="support-contact"></a>
## Minimum support-interface contact-area threshold

**Missing; P0.** Dependencies: support-transitions.

Do not substitute ordinary interface spacing or generic support style for this threshold.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: `support_interface_min_area`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: `support_interface_min_area`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/SupportMaterial.cpp`, `src/libslic3r/Support/SupportMaterial.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`. Keys: `support_interface_min_area`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="support-adaptive"></a>
## Snapmaker adaptive tree support layers

**Missing; P1.** Dependencies: support-transitions.

Ordinary adaptive model layers do not establish this support-specific algorithm.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `tree_support_adaptive_layer_height`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `tree_support_adaptive_layer_height`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `tree_support_adaptive_layer_height`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `tree_support_adaptive_layer_height`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="painting-depth"></a>
## Top and bottom painting penetration controls

**Implemented but untested; P1.** Dependencies: project-migration.

Compare segmented geometry and boundaries; source presence is not U1 painting parity.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: `bottom_color_penetration_layers`, `top_color_penetration_layers`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: `bottom_color_penetration_layers`, `top_color_penetration_layers`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: `bottom_color_penetration_layers`, `top_color_penetration_layers`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: `bottom_color_penetration_layers`, `top_color_penetration_layers`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: `bottom_color_penetration_layers`, `top_color_penetration_layers`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: `bottom_color_penetration_layers`, `top_color_penetration_layers`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/PrintObject.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoMmuSegmentation.hpp`. Keys: `bottom_color_penetration_layers`, `top_color_penetration_layers`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="support-auto"></a>
## Automatic negative raft/support expansion

**Partial; P0.** Dependencies: none.

Path-specific Snapmaker automatic expansion and an explicit persisted compatibility marker are implemented. Focused normal/tree/raft geometry and original single/four-tool project tests pass; broader support-transition/contact/adaptive parity and physical behavior remain open.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Support/SupportCommon.cpp`, `src/libslic3r/Support/SupportCommon.hpp`, `src/libslic3r/Support/TreeSupport.cpp`, `src/libslic3r/Support/TreeSupport.hpp`, `src/libslic3r/Support/TreeSupport3D.cpp`, `src/libslic3r/Support/TreeSupport3D.hpp`. Keys: `raft_first_layer_expansion`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/u1-compatibility-2026-11-06.json`; `tests/fff_print/test_u1_support_compatibility.cpp`; `tests/libslic3r/test_3mf.cpp`; `docs/architecture/support-expansion-migration.md`.

<a id="spectrum-ratio"></a>
## Ratio mixing

**Partial; P1.** Dependencies: project-migration.

Official and Snapmaker mixed-filament metadata differ; compare recipes and resulting extrusion.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `mixed_filament_definitions`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `mixed_filament_definitions`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/FilamentMixer.cpp`, `src/libslic3r/FilamentMixer.hpp`, `src/libslic3r/FilamentMixerModel.hpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `filament_mixed_components`, `filament_mixed_sublayer_ratios`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/FilamentMixer.cpp`, `src/libslic3r/FilamentMixer.hpp`, `src/libslic3r/FilamentMixerModel.hpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `filament_mixed_components`, `filament_mixed_sublayer_ratios`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/FilamentMixer.cpp`, `src/libslic3r/FilamentMixer.hpp`, `src/libslic3r/FilamentMixerModel.hpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `filament_mixed_components`, `filament_mixed_sublayer_ratios`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/FilamentMixer.cpp`, `src/libslic3r/FilamentMixer.hpp`, `src/libslic3r/FilamentMixerModel.hpp`, `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `filament_mixed_components`, `filament_mixed_sublayer_ratios`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `mixed_filament_definitions`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="spectrum-cycle"></a>
## Cycle and interleaved-layer mixing

**Partial; P1.** Dependencies: spectrum-ratio.

Do not label ordinary multi-material painting as cycle mixing.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`. Keys: `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_color_layer_height_a`, `mixed_color_layer_height_b`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`. Keys: `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_color_layer_height_a`, `mixed_color_layer_height_b`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_mixed_sublayer_ratios`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_mixed_sublayer_ratios`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_mixed_sublayer_ratios`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_mixed_sublayer_ratios`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`. Keys: `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_color_layer_height_a`, `mixed_color_layer_height_b`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="spectrum-match"></a>
## Color Match and matching algorithms

**Partial; P1.** Dependencies: spectrum-ratio.

Identify algorithm/color-space and recipe constraints, then compare known target colors.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_component_bias_enabled`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_component_bias_enabled`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_component_bias_enabled`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="spectrum-gradient"></a>
## Gradient curves and ranges

**Partial; P1.** Dependencies: spectrum-ratio.

Similar controls use different serialization; verify curve/range round trips and generated layers.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_gradient_mode`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_gradient_mode`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/GradientCurveEditor.cpp`, `src/slic3r/GUI/GradientCurveEditor.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/GradientCurveEditor.cpp`, `src/slic3r/GUI/GradientCurveEditor.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/GUI/GradientCurveEditor.cpp`, `src/slic3r/GUI/GradientCurveEditor.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/GradientCurveEditor.cpp`, `src/slic3r/GUI/GradientCurveEditor.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`, `src/slic3r/GUI/MixedFilamentDialog.hpp`. Keys: `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_gradient_mode`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="spectrum-decompose"></a>
## Color decomposition and component selection

**Implemented but untested; P1.** Dependencies: spectrum-match.

Native decomposition implementation retained; U1 material/recipe/color reproduction remains unverified.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_component_bias_enabled`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_component_bias_enabled`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: `filament_mixed_components`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: `filament_mixed_components`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: `filament_mixed_components`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/ColorDecomposeRecipe.cpp`, `src/libslic3r/ColorDecomposeRecipe.hpp`, `src/slic3r/GUI/ColorDecomposeDialog.cpp`, `src/slic3r/GUI/ColorDecomposeDialog.hpp`, `src/slic3r/GUI/ColorDecomposeSupport.cpp`, `src/slic3r/GUI/ColorDecomposeSupport.hpp`. Keys: `filament_mixed_components`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/slic3r/GUI/MixedFilamentBadge.cpp`, `src/slic3r/GUI/MixedFilamentBadge.hpp`, `src/slic3r/GUI/MixedFilamentBatchDialog.cpp`. Keys: `mixed_filament_component_bias_enabled`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="spectrum-subdivision"></a>
## Geometry subdivision and textured segmentation

**Implemented but untested; P1.** Dependencies: spectrum-decompose.

Retained subdivision must be checked for mesh validity, paint fidelity and slicing effects.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`. Keys: `dithering_local_z_direct_multicolor`, `dithering_local_z_infill`, `dithering_local_z_mode`, `dithering_local_z_whole_objects`, `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_color_layer_height_a`, `mixed_color_layer_height_b`, `mixed_filament_advanced_dithering`, `mixed_filament_component_bias_enabled`, `mixed_filament_definitions`, `mixed_filament_gradient_mode`, `mixed_filament_height_lower_bound`, `mixed_filament_height_upper_bound`, `mixed_filament_pointillism_line_gap`, `mixed_filament_pointillism_pixel_size`, `mixed_filament_region_collapse`, `mixed_filament_surface_indentation`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`. Keys: `dithering_local_z_direct_multicolor`, `dithering_local_z_infill`, `dithering_local_z_mode`, `dithering_local_z_whole_objects`, `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_color_layer_height_a`, `mixed_color_layer_height_b`, `mixed_filament_advanced_dithering`, `mixed_filament_component_bias_enabled`, `mixed_filament_definitions`, `mixed_filament_gradient_mode`, `mixed_filament_height_lower_bound`, `mixed_filament_height_upper_bound`, `mixed_filament_pointillism_line_gap`, `mixed_filament_pointillism_pixel_size`, `mixed_filament_region_collapse`, `mixed_filament_surface_indentation`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.cpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.hpp`, `src/libslic3r/TextureDisplacement.cpp`, `src/libslic3r/TextureDisplacement.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_is_mixed`, `filament_mixed_components`, `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`, `filament_mixed_sublayer_ratios`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`. Keys: `has_mixed_nozzle_sizes`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.cpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.hpp`, `src/libslic3r/TextureDisplacement.cpp`, `src/libslic3r/TextureDisplacement.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_is_mixed`, `filament_mixed_components`, `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`, `filament_mixed_sublayer_ratios`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.cpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.hpp`, `src/libslic3r/TextureDisplacement.cpp`, `src/libslic3r/TextureDisplacement.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_is_mixed`, `filament_mixed_components`, `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`, `filament_mixed_sublayer_ratios`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.cpp`, `src/libslic3r/TextureBake/TextureBakeSubdivide.hpp`, `src/libslic3r/TextureDisplacement.cpp`, `src/libslic3r/TextureDisplacement.hpp`. Keys: `enable_mixed_color_sublayer`, `filament_is_mixed`, `filament_mixed_components`, `filament_mixed_gradient`, `filament_mixed_gradient_curve`, `filament_mixed_gradient_per_part`, `filament_mixed_gradient_range`, `filament_mixed_sublayer_ratios`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`. Keys: `dithering_local_z_direct_multicolor`, `dithering_local_z_infill`, `dithering_local_z_mode`, `dithering_local_z_whole_objects`, `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_color_layer_height_a`, `mixed_color_layer_height_b`, `mixed_filament_advanced_dithering`, `mixed_filament_component_bias_enabled`, `mixed_filament_definitions`, `mixed_filament_gradient_mode`, `mixed_filament_height_lower_bound`, `mixed_filament_height_upper_bound`, `mixed_filament_pointillism_line_gap`, `mixed_filament_pointillism_pixel_size`, `mixed_filament_region_collapse`, `mixed_filament_surface_indentation`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="spectrum-advanced"></a>
## Advanced dithering, pointillism and local-Z modes

**Partial; P1.** Dependencies: spectrum-cycle, spectrum-subdivision.

Multiple Snapmaker-specific keys are absent; do not equate generic mixed layers with the advanced modes.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`. Keys: `dithering_local_z_direct_multicolor`, `dithering_local_z_infill`, `dithering_local_z_mode`, `dithering_local_z_whole_objects`, `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_filament_advanced_dithering`, `mixed_filament_pointillism_line_gap`, `mixed_filament_pointillism_pixel_size`, `mixed_filament_region_collapse`, `mixed_filament_surface_indentation`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`. Keys: `dithering_local_z_direct_multicolor`, `dithering_local_z_infill`, `dithering_local_z_mode`, `dithering_local_z_whole_objects`, `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_filament_advanced_dithering`, `mixed_filament_pointillism_line_gap`, `mixed_filament_pointillism_pixel_size`, `mixed_filament_region_collapse`, `mixed_filament_surface_indentation`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`, `src/libslic3r/MultiMaterialSegmentation.hpp`, `src/slic3r/GUI/MixedFilamentDialog.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/MixedFilament.cpp`, `src/libslic3r/MixedFilament.hpp`, `src/libslic3r/MixedFilamentConfigRemap.hpp`, `src/libslic3r/MultiMaterialSegmentation.cpp`. Keys: `dithering_local_z_direct_multicolor`, `dithering_local_z_infill`, `dithering_local_z_mode`, `dithering_local_z_whole_objects`, `dithering_step_painted_zones_only`, `dithering_z_step_size`, `mixed_filament_advanced_dithering`, `mixed_filament_pointillism_line_gap`, `mixed_filament_pointillism_pixel_size`, `mixed_filament_region_collapse`, `mixed_filament_surface_indentation`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="fos-color-patch"></a>
## Color Patch shell/core geometry and loops

**Missing; P1.** Dependencies: fos-nozzles, fos-widths, project-fos.

Distinct FOrca feature; ordinary painting and Full Spectrum are not equivalents.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `color_patch_enabled`, `color_patch_loops`, `filament_color_depth`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/PerimeterGenerator.cpp`, `src/libslic3r/PerimeterGenerator.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="fos-nozzles"></a>
## Independent mixed nozzle configuration and mapping

**Partial; P0.** Dependencies: project-fos.

Generic mixed 0.4/0.6 paths were tested; complete FOrca mapping and imported projects are not verified.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `fos_filament_nozzle`, `has_mixed_nozzle_sizes`, `nozzle_diameter`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/PrintObject.cpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="fos-widths"></a>
## Per-nozzle wall, infill, support and tower widths

**Partial; P1.** Dependencies: fos-nozzles.

Generic percentage widths are not the complete FOrca per-nozzle arrays and precedence.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: `tower_line_width`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="fos-speeds"></a>
## Per-nozzle feature speeds and thermal constraints

**Missing; P1.** Dependencies: fos-nozzles.

Port definitions and every consumer together with migration and safety tests.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: `fos_nozzle_desync`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintObject.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="fos-roles"></a>
## Outer/inner wall and sparse/solid infill tool assignments

**Partial; P0.** Dependencies: project-fos.

Native role assignments exist. FOrca names, array semantics and imported project equivalence need adapters.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `solid_infill_filament`, `sparse_infill_filament`, `wall_filament`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `solid_infill_filament`, `sparse_infill_filament`, `wall_filament`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `bottom_surface_filament_id`, `inner_wall_filament_id`, `internal_solid_filament_id`, `outer_wall_filament_id`, `sparse_infill_filament_id`, `top_surface_filament_id`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `fos_filament_mms_slot`, `fos_filament_nozzle`, `fos_filament_translucency`, `fos_filament_transparent`, `solid_infill_filament`, `sparse_infill_filament`, `wall_filament`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `bottom_surface_filament_id`, `inner_wall_filament_id`, `internal_solid_filament_id`, `outer_wall_filament_id`, `sparse_infill_filament_id`, `top_surface_filament_id`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `bottom_surface_filament_id`, `inner_wall_filament_id`, `internal_solid_filament_id`, `outer_wall_filament_id`, `sparse_infill_filament_id`, `top_surface_filament_id`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `bottom_surface_filament_id`, `inner_wall_filament_id`, `internal_solid_filament_id`, `outer_wall_filament_id`, `sparse_infill_filament_id`, `top_surface_filament_id`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/PrintRegion.cpp`, `src/slic3r/GUI/Plater.cpp`. Keys: `solid_infill_filament`, `sparse_infill_filament`, `wall_filament`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="fos-support-tower"></a>
## Support/interface/prime-tower filament selection

**Implemented but untested; P1.** Dependencies: fos-roles.

Retained generic selectors require FOrca/U1-specific generated path validation.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/SLAPrint.cpp`, `src/slic3r/Utils/CrealityPrint.cpp`, `src/slic3r/Utils/OctoPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/SLAPrint.cpp`, `src/slic3r/Utils/CrealityPrint.cpp`, `src/slic3r/Utils/OctoPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/SLAPrint.cpp`, `src/libvgcode/src/ColorPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/SLAPrint.cpp`, `src/slic3r/Utils/CrealityPrint.cpp`, `src/slic3r/Utils/OctoPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/SLAPrint.cpp`, `src/libvgcode/src/ColorPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/SLAPrint.cpp`, `src/libvgcode/src/ColorPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/SLAPrint.cpp`, `src/libvgcode/src/ColorPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/GCode/ToolOrdering.cpp`, `src/libslic3r/GCode/ToolOrdering.hpp`, `src/libslic3r/Print.cpp`, `src/libslic3r/SLAPrint.cpp`, `src/slic3r/Utils/CrealityPrint.cpp`, `src/slic3r/Utils/OctoPrint.cpp`. Keys: `support_filament`, `support_interface_filament`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="fos-object-overrides"></a>
## Per-object and per-filament overrides

**Partial; P1.** Dependencies: project-fos.

Generic overrides remain; fork-specific schema and precedence are not losslessly migrated.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: `filament_settings_id`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: `filament_settings_id`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`. Keys: `filament_settings_id`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: `filament_settings_id`, `fos_filament_mms_slot`, `fos_filament_nozzle`, `fos_filament_translucency`, `fos_filament_transparent`, `fos_mms_head_ace`, `fos_mms_topology`, `fos_mms_unit_count`, `fos_nozzle_desync`, `fos_physical_nozzle_diameter`, `fos_slot_config_serial`, `fos_support_interface_nozzle_pool`, `fos_support_nozzle_pool`, `fos_wipe_tower_nozzle_pool`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`. Keys: `filament_settings_id`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`. Keys: `filament_settings_id`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`. Keys: `filament_settings_id`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: `filament_settings_id`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="fos-nozzle-safety"></a>
## Nozzle verification and incompatibility checks

**Partial; P0.** Dependencies: high-flow, fos-nozzles.

Do not substitute planner success for nozzle/material safety.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/FilamentHotBedNozzleRules.cpp`, `src/libslic3r/FilamentHotBedNozzleRules.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_volume_type`, `nozzle_type`, `nozzle_volume_type`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/FilamentHotBedNozzleRules.cpp`, `src/libslic3r/FilamentHotBedNozzleRules.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_volume_type`, `nozzle_type`, `nozzle_volume_type`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/MultiNozzleUtils.cpp`, `src/libslic3r/MultiNozzleUtils.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.cpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.h`, `src/slic3r/GUI/DeviceCore/DevNozzleRack.cpp`. Keys: `nozzle_type`, `nozzle_volume_type`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/FilamentHotBedNozzleRules.cpp`, `src/libslic3r/FilamentHotBedNozzleRules.hpp`, `src/libslic3r/NozzleLayerPlanner.cpp`, `src/libslic3r/NozzleLayerPlanner.hpp`, `src/slic3r/GUI/FilamentNozzleMapDialog.cpp`, `src/slic3r/GUI/FilamentNozzleMapDialog.hpp`. Keys: `fos_nozzle_desync`, `nozzle_type`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/MultiNozzleUtils.cpp`, `src/libslic3r/MultiNozzleUtils.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.cpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.h`, `src/slic3r/GUI/DeviceCore/DevNozzleRack.cpp`. Keys: `nozzle_type`, `nozzle_volume_type`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/MultiNozzleUtils.cpp`, `src/libslic3r/MultiNozzleUtils.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.cpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.h`, `src/slic3r/GUI/DeviceCore/DevNozzleRack.cpp`. Keys: `nozzle_type`, `nozzle_volume_type`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/MultiNozzleUtils.cpp`, `src/libslic3r/MultiNozzleUtils.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.cpp`, `src/slic3r/GUI/DeviceCore/DevMappingNozzle.h`, `src/slic3r/GUI/DeviceCore/DevNozzleRack.cpp`. Keys: `nozzle_type`, `nozzle_volume_type`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/FilamentHotBedNozzleRules.cpp`, `src/libslic3r/FilamentHotBedNozzleRules.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_volume_type`, `nozzle_type`, `nozzle_volume_type`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/fff_print/test_wipe_tower.cpp`; `tests/fff_print/test_multifilament.cpp`; `tests/fff_print/test_u1_four_tool_gcode.cpp`.

<a id="filament-planner"></a>
## Advisory filament/nozzle partition planner

**Verified; P1.** Dependencies: none.

Verified native planner/protocol tests; advisory only and does not check physical material compatibility.

Plugin/agent assessment: The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): No matching component in the inspected source scope. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/FosFilamentArrangement.cpp`, `src/libslic3r/FosFilamentArrangement.hpp`. Keys: `fos_filament_nozzle`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/FosFilamentArrangement.cpp`, `src/libslic3r/FosFilamentArrangement.hpp`, `src/libslic3r/U1FilamentPlan.cpp`, `src/libslic3r/U1FilamentPlan.hpp`, `src/slic3r/GUI/Mcp/McpToolsU1.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="u1-lan"></a>
## U1 LAN discovery and network submission

**Partial; P0.** Dependencies: firmware-capabilities.

Generic Moonraker/Snapmaker agent source is retained, but full stock/gateway parity is not verified.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: `host_type`, `print_host`, `printhost_apikey`, `printhost_authorization_type`, `printhost_cafile`, `printhost_password`, `printhost_port`, `printhost_ssl_ignore_revoke`, `printhost_user`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="u1-gateway"></a>
## Snapmaker gateway transport and device protocol

**Partial; P0.** Dependencies: none.

Snapmaker account/protocol, process lifecycle and HTTP/WebSocket service are ported, compiled and pass 38 offline gateway cases. Foreign companion takeover is opt-in. Device/native UI integration, isolated companion startup and packaging are unfinished; no printer connection is verified.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/ConnectionProcessManager.cpp`, `src/slic3r/Utils/ConnectionProcessManager.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/ConnectionProcessManager.cpp`, `src/slic3r/Utils/ConnectionProcessManager.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): No matching component in the inspected source scope. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/ConnectionProcessManager.cpp`, `src/slic3r/Utils/ConnectionProcessManager.hpp`, `src/slic3r/Utils/GatewayProtocol.cpp`, `src/slic3r/Utils/GatewayProtocol.hpp`, `src/slic3r/Utils/GatewayService.cpp`, `src/slic3r/Utils/GatewayService.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/ConnectionProcessManager.cpp`, `src/slic3r/Utils/ConnectionProcessManager.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/u1-compatibility-2026-11-06.json`; `docs/architecture/evidence/snapmaker-gateway-port.json`; `tests/slic3rutils/GatewayService_test.cpp`.

<a id="u1-cloud"></a>
## Snapmaker cloud account, pairing and authorization

**Missing; P0.** Dependencies: u1-gateway.

Orca cloud or Bambu login is not Snapmaker pairing. Credentials/services required for live verification.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayAccount.cpp`, `src/slic3r/Utils/GatewayAccount.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayAccount.cpp`, `src/slic3r/Utils/GatewayAccount.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): No matching component in the inspected source scope. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/GatewayAccount.cpp`, `src/slic3r/Utils/GatewayAccount.hpp`, `src/slic3r/Utils/GatewayProtocol.cpp`, `src/slic3r/Utils/GatewayProtocol.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayAccount.cpp`, `src/slic3r/Utils/GatewayAccount.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `No feature-specific U1 runtime/hardware verification recorded; generic suite success is not parity.`.

<a id="u1-status"></a>
## Device status, job, progress and temperatures

**Partial; P0.** Dependencies: u1-lan.

Source paths exist; use recorded stock/Extended fixtures before live read-only confirmation.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="u1-camera"></a>
## U1 camera, authentication and streaming

**Missing; P0.** Dependencies: u1-gateway, firmware-capabilities.

Generic printer-video infrastructure exists, but no validated U1-specific camera transport/authentication integration is present. GUI/Camera.cpp is the 3D viewport camera and is not evidence of printer streaming. Snapmaker routes camera start/timelapse through SSWCP and its MoonRaker host/Flutter device bridge; these are not present as an equivalent U1 integration.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`, `src/slic3r/GUI/WebRtcMediaController.cpp`, `src/slic3r/GUI/WebRtcMediaController.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`, `src/slic3r/GUI/WebRtcMediaController.cpp`, `src/slic3r/GUI/WebRtcMediaController.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`, `src/slic3r/GUI/WebRtcMediaController.cpp`, `src/slic3r/GUI/WebRtcMediaController.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`, `src/slic3r/GUI/WebRtcMediaController.cpp`, `src/slic3r/GUI/WebRtcMediaController.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/CameraPopup.cpp`, `src/slic3r/GUI/CameraPopup.hpp`, `src/slic3r/GUI/MediaPlayCtrl.cpp`, `src/slic3r/GUI/MediaPlayCtrl.h`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `No feature-specific U1 runtime/hardware verification recorded; generic suite success is not parity.`.

<a id="u1-rfid"></a>
## U1 RFID/NFC filament metadata and refresh

**Partial; P0.** Dependencies: u1-gateway, firmware-capabilities.

The production Snapmaker filament metadata reader validates four physical slots separately from the logical job mapping, unknown material/color values and optional NFC temperatures; offline parser tests pass. Native refresh/sync, tag/protocol variants and hardware behavior remain unfinished or unverified.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/GUI/filamentsync/FilamentSyncAlgorithm.cpp`, `src/slic3r/GUI/filamentsync/FilamentSyncAlgorithm.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/GUI/filamentsync/FilamentSyncAlgorithm.cpp`, `src/slic3r/GUI/filamentsync/FilamentSyncAlgorithm.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/GUI/filamentsync/FilamentSyncAlgorithm.cpp`, `src/slic3r/GUI/filamentsync/FilamentSyncAlgorithm.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/u1-compatibility-2026-11-06.json`; `tests/slic3rutils/test_snapmaker_filament_state.cpp`.

<a id="u1-filaments"></a>
## Filament inventory, assignments and synchronization

**Partial; P0.** Dependencies: u1-rfid, high-flow.

Local assignment exists; current Snapmaker inventory/mapping synchronization remains incomplete.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/GUI/filamentsync/FilamentColorMapBox.cpp`, `src/slic3r/GUI/filamentsync/FilamentColorMapBox.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/GUI/filamentsync/FilamentColorMapBox.cpp`, `src/slic3r/GUI/filamentsync/FilamentColorMapBox.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/GUI/filamentsync/FilamentColorMapBox.cpp`, `src/slic3r/GUI/filamentsync/FilamentColorMapBox.hpp`. Keys: `filament_colour`, `filament_settings_id`, `filament_type`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="u1-feeder"></a>
## Automatic feeding and unloading

**Unknown; P0.** Dependencies: u1-gateway, firmware-capabilities.

Need exact stock feeder API/state machine and offline fixtures. Do not execute hardware commands during this work.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `No feature-specific U1 runtime/hardware verification recorded; generic suite success is not parity.`.

<a id="u1-multiace"></a>
## MultiACE device integration

**Missing; P1.** Dependencies: u1-feeder, fos-nozzles.

Firmware-/device-dependent FOrca integration is not imported or hardware-verified.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): No matching component in the inspected source scope. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/FosFilamentArrangement.cpp`, `src/libslic3r/FosFilamentArrangement.hpp`, `src/slic3r/GUI/FosColourDialog.cpp`, `src/slic3r/GUI/FosColourDialog.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`. Keys: `fos_filament_mms_slot`, `fos_filament_nozzle`, `fos_filament_translucency`, `fos_filament_transparent`, `fos_mms_head_ace`, `fos_mms_topology`, `fos_mms_unit_count`, `fos_nozzle_desync`, `fos_physical_nozzle_diameter`, `fos_slot_config_serial`, `fos_support_interface_nozzle_pool`, `fos_support_nozzle_pool`, `fos_wipe_tower_nozzle_pool`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/FosFilamentArrangement.cpp`, `src/libslic3r/FosFilamentArrangement.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="u1-cover"></a>
## Top cover/door/enclosure capability and status

**Unknown; P0.** Dependencies: firmware-capabilities.

Exact stock sensor/API and third-party cover variant must be identified. A printer cover thumbnail or chamber setting is not sensor integration.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`. Keys: `chamber_temperature`, `support_chamber_temp_control`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`. Keys: `chamber_temperature`, `support_chamber_temp_control`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `chamber_minimal_temperature`, `chamber_temperature`, `support_chamber_temp_control`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: `chamber_temperature`, `support_chamber_temp_control`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `chamber_minimal_temperature`, `chamber_temperature`, `support_chamber_temp_control`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `chamber_minimal_temperature`, `chamber_temperature`, `support_chamber_temp_control`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: `chamber_minimal_temperature`, `chamber_temperature`, `support_chamber_temp_control`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/DeviceManager.cpp`, `src/slic3r/GUI/DeviceManager.hpp`, `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`. Keys: `chamber_temperature`, `support_chamber_temp_control`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `No feature-specific U1 runtime/hardware verification recorded; generic suite success is not parity.`.

<a id="high-flow"></a>
## High-flow hotend detection and compatibility

**Partial; P0.** Dependencies: u1-gateway, project-migration.

Snapmaker flow-variant schema, SSWCP payload and profile selection are coupled and not fully ported.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/FlowTypeHelper.cpp`, `src/slic3r/GUI/FlowTypeHelper.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_flow_support`, `filament_volume_type`, `nozzle_volume_type`, `printer_flow_support`, `process_flow_support`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/FlowTypeHelper.cpp`, `src/slic3r/GUI/FlowTypeHelper.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_flow_support`, `filament_volume_type`, `nozzle_volume_type`, `printer_flow_support`, `process_flow_support`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/SSWCP.cpp`, `src/slic3r/GUI/SSWCP.hpp`, `src/slic3r/Utils/MoonRaker.cpp`, `src/slic3r/Utils/MoonRaker.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/FlowTypeHelper.cpp`, `src/slic3r/GUI/FlowTypeHelper.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_flow_support`, `filament_volume_type`, `nozzle_volume_type`, `printer_flow_support`, `process_flow_support`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `No feature-specific U1 runtime/hardware verification recorded; generic suite success is not parity.`.

<a id="nozzle-02"></a>
## Uniform 0.2 mm U1 profile

**Implemented but untested; P1.** Dependencies: profile-visibility.

Preset is present; no claim of physical calibration or supported material combinations.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="nozzle-04"></a>
## Uniform 0.4 mm U1 profile

**Verified; P0.** Dependencies: profile-visibility.

A retained-profile cube sliced/exported in Linux; physical printing and every process/material remain unverified.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="nozzle-06"></a>
## Uniform 0.6 mm U1 profile

**Implemented but untested; P1.** Dependencies: profile-visibility.

Preset is present; complete material/process and physical validation is missing.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="nozzle-08"></a>
## Uniform 0.8 mm U1 profile

**Implemented but untested; P1.** Dependencies: profile-visibility.

Preset is present; complete material/process and physical validation is missing.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_diameter`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: `nozzle_diameter`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="nozzle-mixed"></a>
## Mixed 0.4+0.6 U1 profile and arbitrary head combinations

**Partial; P0.** Dependencies: fos-nozzles.

0.4/0.6 synthetic engine paths verified. One visible preset is not a FOrca-only hardware limit.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/PrintRegion.cpp`. Keys: `nozzle_diameter`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="profile-visibility"></a>
## Printer wizard and selected-preset visibility

**Partial; P0.** Dependencies: none.

All five diameter variants exist in the system catalog; inspect selection visibility without changing existing user configurations.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`, `src/slic3r/GUI/PresetComboBoxes.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`, `src/slic3r/GUI/PresetComboBoxes.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizardTypes.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`, `src/slic3r/GUI/PresetComboBoxes.cpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizardTypes.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizardTypes.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizardTypes.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ConfigWizard.cpp`, `src/slic3r/GUI/ConfigWizard.hpp`, `src/slic3r/GUI/ConfigWizard_private.hpp`, `src/slic3r/GUI/PresetComboBoxes.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="profile-macros"></a>
## U1 machine start/end/tool-change macro preservation

**Partial; P0.** Dependencies: project-migration.

Do not replace stock docking/feeding/temperature macros with generic commands; generated outputs require semantic comparison.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/PrintConfigConstants.hpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `change_filament_gcode`, `machine_end_gcode`, `machine_start_gcode`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="profile-sync"></a>
## Attribution, inheritance, collisions and user overrides

**Partial; P1.** Dependencies: none.

Immutable review catalogs are tested; unvalidated/calibration and separate-profile redistribution gates remain.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `compatible_printers`, `inherits`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `compatible_printers`, `inherits`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`, `src/slic3r/GUI/ExportPresetBundleDialog.hpp`, `src/slic3r/GUI/PresetBundleDialog.cpp`. Keys: `compatible_printers`, `inherits`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `compatible_printers`, `inherits`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`, `src/slic3r/GUI/ExportPresetBundleDialog.hpp`, `src/slic3r/GUI/PresetBundleDialog.cpp`. Keys: `compatible_printers`, `inherits`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`, `src/slic3r/GUI/ExportPresetBundleDialog.hpp`, `src/slic3r/GUI/PresetBundleDialog.cpp`. Keys: `compatible_printers`, `inherits`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`, `src/slic3r/GUI/ExportPresetBundleDialog.hpp`, `src/slic3r/GUI/PresetBundleDialog.cpp`. Keys: `compatible_printers`, `inherits`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Preset.cpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `compatible_printers`, `inherits`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="project-migration"></a>
## Original Snapmaker 3MF import and configuration migration

**Partial; P0.** Dependencies: support-auto.

Original Snapmaker v2.4.1 single/four-tool fixtures now import, restore embedded G-code and slice with original machine macros; compatibility marker and explicit opt-out round-trip. Complete vendor settings/metadata fidelity and all-project coverage remain open.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `mixed_filament_definitions`, `printer_flow_support`, `raft_first_layer_expansion`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `mixed_filament_definitions`, `printer_flow_support`, `raft_first_layer_expansion`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`. Keys: `raft_first_layer_expansion`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `raft_first_layer_expansion`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`. Keys: `raft_first_layer_expansion`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`. Keys: `raft_first_layer_expansion`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/slic3r/GUI/ExportPresetBundleDialog.cpp`. Keys: `raft_first_layer_expansion`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/PresetBundle.hpp`. Keys: `mixed_filament_definitions`, `printer_flow_support`, `raft_first_layer_expansion`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/u1-compatibility-2026-11-06.json`; `tests/fff_print/test_u1_support_compatibility.cpp`; `tests/libslic3r/test_3mf.cpp`; `docs/architecture/support-expansion-migration.md`.

<a id="project-export"></a>
## 3MF save/export and metadata fidelity

**Partial; P0.** Dependencies: project-migration.

Own-project export passed. Vendor round-trip preservation and fork-specific metadata are not proven.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/Model.cpp`, `src/slic3r/GUI/AuxiliaryDataViewModel.cpp`, `src/slic3r/GUI/GLModel.cpp`, `src/slic3r/GUI/MultiSendMachineModel.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="project-fos"></a>
## FOrca schema and object/filament metadata migration

**Missing; P0.** Dependencies: none.

A known set of FOrca keys has no native equivalent/schema consumer. Never drop them silently.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: `color_patch_enabled`, `color_patch_loops`, `fos_filament_mms_slot`, `fos_filament_nozzle`, `fos_filament_translucency`, `fos_filament_transparent`, `fos_mms_head_ace`, `fos_mms_topology`, `fos_mms_unit_count`, `fos_nozzle_desync`, `fos_physical_nozzle_diameter`, `fos_slot_config_serial`, `fos_support_interface_nozzle_pool`, `fos_support_nozzle_pool`, `fos_wipe_tower_nozzle_pool`, `has_mixed_nozzle_sizes`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintConfigConstants.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/libslic3r/PrintRegion.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="mcp-core"></a>
## Native protocol, authentication and stdio

**Verified; P0.** Dependencies: none.

Native component/transport and real GUI HTTP/stdio smoke passed; this is not full client or printer verification.

Plugin/agent assessment: Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/Mcp/McpHttpServer.cpp`, `src/slic3r/GUI/Mcp/McpHttpServer.hpp`, `src/slic3r/GUI/Mcp/McpProtocol.cpp`, `src/slic3r/GUI/Mcp/McpProtocol.hpp`, `src/slic3r/GUI/Mcp/McpStdioBridge.cpp`, `src/slic3r/GUI/Mcp/McpStdioBridge.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Mcp/McpHttpServer.cpp`, `src/slic3r/GUI/Mcp/McpHttpServer.hpp`, `src/slic3r/GUI/Mcp/McpProtocol.cpp`, `src/slic3r/GUI/Mcp/McpProtocol.hpp`, `src/slic3r/GUI/Mcp/McpStdioBridge.cpp`, `src/slic3r/GUI/Mcp/McpStdioBridge.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/Mcp/McpHttpServer.cpp`, `src/slic3r/GUI/Mcp/McpHttpServer.hpp`, `src/slic3r/GUI/Mcp/McpProtocol.cpp`, `src/slic3r/GUI/Mcp/McpProtocol.hpp`, `src/slic3r/GUI/Mcp/McpStdioBridge.cpp`, `src/slic3r/GUI/Mcp/McpStdioBridge.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="mcp-transform"></a>
## Move, rotate, scale, arrange and inspect

**Partial; P1.** Dependencies: mcp-core.

Typed handlers are retained; allowed subset and actual runtime tests differ by operation.

Plugin/agent assessment: Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/Mcp/McpToolsScene.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Mcp/McpToolsScene.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/Mcp/McpToolsScene.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="mcp-slicing"></a>
## Slicing, estimates, consumption, warnings and export

**Partial; P0.** Dependencies: mcp-core, project-migration.

Native STL/cube slicing passed; project/file export handlers remain gated pending review.

Plugin/agent assessment: Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/Mcp/McpToolsProject.cpp`, `src/slic3r/GUI/Mcp/McpToolsView.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Mcp/McpToolsProject.cpp`, `src/slic3r/GUI/Mcp/McpToolsView.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/Mcp/McpToolsProject.cpp`, `src/slic3r/GUI/Mcp/McpToolsView.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="mcp-project-files"></a>
## Open/import/create/save/export projects and files

**Partial; P0.** Dependencies: mcp-core, project-migration.

Upstream handlers exist but U1 policy denies them. Authorized roots do not by themselves authorize destructive overwrite.

Plugin/agent assessment: Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/Mcp/McpPaths.cpp`, `src/slic3r/GUI/Mcp/McpPaths.hpp`, `src/slic3r/GUI/Mcp/McpToolsProject.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Mcp/McpPaths.cpp`, `src/slic3r/GUI/Mcp/McpPaths.hpp`, `src/slic3r/GUI/Mcp/McpToolsProject.cpp`, `src/slic3r/GUI/Mcp/McpU1Policy.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/Mcp/McpPaths.cpp`, `src/slic3r/GUI/Mcp/McpPaths.hpp`, `src/slic3r/GUI/Mcp/McpToolsProject.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="mcp-settings"></a>
## Object/material/support/profile authoring

**Partial; P1.** Dependencies: mcp-core, project-fos.

Most configuration mutation is intentionally gated until argument/credential/approval review.

Plugin/agent assessment: Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/Mcp/McpToolsConfig.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Mcp/McpToolsConfig.cpp`, `src/slic3r/GUI/Mcp/McpU1Policy.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/Mcp/McpToolsConfig.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="mcp-destruction"></a>
## Duplicate/delete and destructive operation approval

**Partial; P0.** Dependencies: mcp-core.

Source is not equivalent to exposed tools; destructive operations need operator-bound confirmation.

Plugin/agent assessment: Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/Mcp/McpToolsScene.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Mcp/McpToolsScene.cpp`, `src/slic3r/GUI/Mcp/McpU1Policy.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/Mcp/McpToolsScene.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="mcp-printer"></a>
## Authorized printer state, submission and controls

**Missing; P0.** Dependencies: u1-gateway, firmware-capabilities.

No reviewed operator-bound printer-control adapter. Generic UI/script/plugin bridges remain blocked.

Plugin/agent assessment: Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/BBLPrinterAgent.cpp`, `src/slic3r/Utils/BBLPrinterAgent.hpp`, `src/slic3r/Utils/IPrinterAgent.hpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/OrcaPrinterAgent.cpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Mcp/McpToolsU1.cpp`, `src/slic3r/GUI/Mcp/McpU1Policy.hpp`, `src/slic3r/Utils/BBLPrinterAgent.cpp`, `src/slic3r/Utils/BBLPrinterAgent.hpp`, `src/slic3r/Utils/IPrinterAgent.hpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/BBLPrinterAgent.cpp`, `src/slic3r/Utils/BBLPrinterAgent.hpp`, `src/slic3r/Utils/IPrinterAgent.hpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/OrcaPrinterAgent.cpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/BBLPrinterAgent.cpp`, `src/slic3r/Utils/BBLPrinterAgent.hpp`, `src/slic3r/Utils/IPrinterAgent.hpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/OrcaPrinterAgent.cpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `docs/testing/evidence/components.junit.xml`; `docs/testing/evidence/mcp-live-smoke.json`; `docs/testing/evidence/mcp-slice-smoke.json`.

<a id="firmware-stock"></a>
## Stock U1 firmware API and G-code behavior

**Partial; P0.** Dependencies: u1-gateway, profile-macros.

Must compare actual stock API fixtures, command vocabulary and tool mapping; hardware remains untested.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `gcode_flavor`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `gcode_flavor`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`. Keys: `gcode_flavor`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `gcode_flavor`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`. Keys: `gcode_flavor`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`. Keys: `gcode_flavor`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`. Keys: `gcode_flavor`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/GCode.cpp`. Keys: `gcode_flavor`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="firmware-extended"></a>
## Extended Firmware 2.1 and optional services

**Partial; P0.** Dependencies: firmware-capabilities.

Do not infer all installations expose identical Moonraker, camera, NFC or macro services.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="firmware-capabilities"></a>
## Dynamic capability detection and explicit unknowns

**Partial; P0.** Dependencies: none.

Need unified per-service/version capability negotiation and recorded fixtures, not hardcoded version assumptions.

Plugin/agent assessment: Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/Utils/MoonrakerPrinterAgent.cpp`, `src/slic3r/Utils/MoonrakerPrinterAgent.hpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.cpp`, `src/slic3r/Utils/SnapmakerPrinterAgent.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/slic3r/Utils/GatewayDevice.cpp`, `src/slic3r/Utils/GatewayDevice.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="plugins-discovery"></a>
## Bundled plugin discovery, consent and installation

**Partial; P0.** Dependencies: none.

Native installation/load and disabled staging tests pass; Windows GUI catalog verification belongs to the next candidate build.

Plugin/agent assessment: Implemented by the named optional plugin/host integration, within its documented tested scope.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/slic3rutils/test_u1_plugin_packages.cpp`; `tools/u1/tests/test_plugin_integrations.py`.

<a id="plugin-studio"></a>
## Studio read-only project inspection and preflight

**Verified; P1.** Dependencies: plugins-discovery.

Actual pinned core inspection and no-mutation checks passed. Conversion/clamping/printer controls are not exposed.

Plugin/agent assessment: Implemented by the named optional plugin/host integration, within its documented tested scope.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/slic3rutils/test_u1_plugin_packages.cpp`; `tools/u1/tests/test_plugin_integrations.py`.

<a id="plugin-converter"></a>
## External converter connector and project-copy workflow

**Verified; P1.** Dependencies: plugins-discovery.

Actual loopback service round trip passed and preserved input hash. Noncommercial implementation is not distributed.

Plugin/agent assessment: Implemented by the named optional plugin/host integration, within its documented tested scope.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/plugin/PluginLoader.cpp`, `src/slic3r/plugin/PluginLoader.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `tests/slic3rutils/test_u1_plugin_packages.cpp`; `tools/u1/tests/test_plugin_integrations.py`.

<a id="windows-signing"></a>
## Windows-trusted Authenticode signatures

**Partial; P0.** Dependencies: none.

Signing/verification pipeline prepared; no signing identity is configured. Self-signing is not Windows-trusted signing.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): No matching component in the inspected source scope. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `tools/u1/windows/sign-portable.ps1`, `tools/u1/windows/verify-portable.ps1`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="macos-build"></a>
## Native macOS ARM64 application and packaging

**Unknown; P0.** Dependencies: none.

Component checks are not a full macOS application build; stable release gate remains.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): No matching component in the inspected source scope. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="hardware-print"></a>
## Physical single/four-tool/mixed-nozzle validation

**Unknown; P0.** Dependencies: project-migration, u1-gateway, fos-nozzles, profile-macros.

No physical U1 prints are authorized or performed. 100% physical compatibility cannot be certified offline.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): No matching component in the inspected source scope. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): No matching component in the inspected source scope. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): No matching component in the inspected source scope. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): No matching component in the inspected source scope. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`; `No feature-specific U1 runtime/hardware verification recorded; generic suite success is not parity.`.

<a id="orca-engine"></a>
## Retained walls, infill, cooling, seams and G-code engine

**Partial; P1.** Dependencies: none.

Full FFF suite passed for its scope; it does not prove every retained feature with every U1 profile.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`, `src/libslic3r/Fill/FillAdaptive.cpp`, `src/libslic3r/Fill/FillAdaptive.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`, `ironing_pattern`, `ironing_spacing`, `ironing_speed`, `ironing_type`, `seam_gap`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`, `src/libslic3r/Fill/FillAdaptive.cpp`, `src/libslic3r/Fill/FillAdaptive.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`, `ironing_pattern`, `ironing_spacing`, `ironing_speed`, `ironing_type`, `seam_gap`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/Fill/AdaptiveInfillField.cpp`, `src/libslic3r/Fill/AdaptiveInfillField.hpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_layers_between_ripple_offset`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_ripple_offset`, `fuzzy_skin_ripples_per_layer`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_angle_fixed`, `ironing_expansion`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`, `src/libslic3r/Fill/FillAdaptive.cpp`, `src/libslic3r/Fill/FillAdaptive.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`, `ironing_pattern`, `ironing_spacing`, `ironing_speed`, `ironing_type`, `seam_gap`.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/Fill/AdaptiveInfillField.cpp`, `src/libslic3r/Fill/AdaptiveInfillField.hpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_layers_between_ripple_offset`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_ripple_offset`, `fuzzy_skin_ripples_per_layer`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_angle_fixed`, `ironing_expansion`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/Fill/AdaptiveInfillField.cpp`, `src/libslic3r/Fill/AdaptiveInfillField.hpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_layers_between_ripple_offset`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_ripple_offset`, `fuzzy_skin_ripples_per_layer`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_angle_fixed`, `ironing_expansion`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/Fill/AdaptiveInfillField.cpp`, `src/libslic3r/Fill/AdaptiveInfillField.hpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_layers_between_ripple_offset`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_ripple_offset`, `fuzzy_skin_ripples_per_layer`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_angle_fixed`, `ironing_expansion`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/Fill/Fill.hpp`, `src/libslic3r/Fill/Fill3DHoneycomb.cpp`, `src/libslic3r/Fill/Fill3DHoneycomb.hpp`, `src/libslic3r/Fill/FillAdaptive.cpp`, `src/libslic3r/Fill/FillAdaptive.hpp`. Keys: `fuzzy_skin`, `fuzzy_skin_first_layer`, `fuzzy_skin_mode`, `fuzzy_skin_noise_type`, `fuzzy_skin_octaves`, `fuzzy_skin_persistence`, `fuzzy_skin_point_distance`, `fuzzy_skin_scale`, `fuzzy_skin_thickness`, `ironing_angle`, `ironing_fan_speed`, `ironing_flow`, `ironing_inset`, `ironing_pattern`, `ironing_spacing`, `ironing_speed`, `ironing_type`, `seam_gap`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="orca-geometry"></a>
## STL/STEP/3MF, modeling, painting and CAD

**Implemented but untested; P1.** Dependencies: none.

Native implementations retained. Complete U1 workflows and full source-to-reference comparison are not executed.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/Format/STEP.cpp`, `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAssembly.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/Format/STEP.cpp`, `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAssembly.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/CAD/CadDocument.cpp`, `src/libslic3r/CAD/CadDocument.hpp`, `src/libslic3r/CAD/GeometryEngine.cpp`, `src/libslic3r/CAD/GeometryEngine.hpp`, `src/libslic3r/CAD/SketchConstraints.cpp`, `src/libslic3r/CAD/SketchConstraints.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/Format/STEP.cpp`, `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAssembly.cpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/CAD/CadDocument.cpp`, `src/libslic3r/CAD/CadDocument.hpp`, `src/libslic3r/CAD/GeometryEngine.cpp`, `src/libslic3r/CAD/GeometryEngine.hpp`, `src/libslic3r/CAD/SketchConstraints.cpp`, `src/libslic3r/CAD/SketchConstraints.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/CAD/CadDocument.cpp`, `src/libslic3r/CAD/CadDocument.hpp`, `src/libslic3r/CAD/GeometryEngine.cpp`, `src/libslic3r/CAD/GeometryEngine.hpp`, `src/libslic3r/CAD/SketchConstraints.cpp`, `src/libslic3r/CAD/SketchConstraints.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/CAD/CadDocument.cpp`, `src/libslic3r/CAD/CadDocument.hpp`, `src/libslic3r/CAD/GeometryEngine.cpp`, `src/libslic3r/CAD/GeometryEngine.hpp`, `src/libslic3r/CAD/SketchConstraints.cpp`, `src/libslic3r/CAD/SketchConstraints.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/Format/STEP.cpp`, `src/libslic3r/Format/bbs_3mf.cpp`, `src/libslic3r/Format/bbs_3mf.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp`, `src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp`, `src/slic3r/GUI/Gizmos/GLGizmoAssembly.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="orca-calibration"></a>
## Calibration and process workflows

**Implemented but untested; P1.** Dependencies: profile-macros.

Audit printer-specific calibration commands before claiming U1 safety; no hardware tests run.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/slic3r/GUI/Calibration.cpp`, `src/slic3r/GUI/Calibration.hpp`, `src/slic3r/GUI/CalibrationPanel.cpp`, `src/slic3r/GUI/CalibrationPanel.hpp`, `src/slic3r/GUI/CalibrationWizard.cpp`, `src/slic3r/GUI/CalibrationWizard.hpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="orca-gates"></a>
## Integration changes, disabled features and default policies

**Partial; P0.** Dependencies: none.

Whole-source diff against MCP base is recorded. MCP restrictions and isolated identity are intentional changes, not full exposed upstream parity.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/slic3r/GUI/GUI_App.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/slic3r/GUI/GUI_App.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/slic3r/GUI/GUI_App.cpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/slic3r/GUI/GUI_App.cpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/slic3r/GUI/GUI_App.cpp`, `src/slic3r/GUI/Mcp/McpU1Policy.hpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/slic3r/GUI/GUI_App.cpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/slic3r/GUI/GUI_App.cpp`, `src/slic3r/plugin/PluginManager.cpp`, `src/slic3r/plugin/PluginManager.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/slic3r/GUI/GUI_App.cpp`. Keys: none for this bounded component.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="high-flow-detection"></a>
## Detect and reconcile reported U1 high-flow hotends

**Missing; P0.** Dependencies: u1-gateway, high-flow.

A generic nozzle-volume setting does not detect installed U1 high-flow hardware. Port reported per-head flow state and conflict checks using documented firmware/gateway fixtures.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/FlowTypeHelper.cpp`, `src/slic3r/GUI/FlowTypeHelper.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_flow_support`, `filament_volume_type`, `nozzle_volume_type`, `printer_flow_support`, `process_flow_support`.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/FlowTypeHelper.cpp`, `src/slic3r/GUI/FlowTypeHelper.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_flow_support`, `filament_volume_type`, `nozzle_volume_type`, `printer_flow_support`, `process_flow_support`.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): No matching component in the inspected source scope. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/PrintConfigConstants.hpp`. Keys: `nozzle_volume_type`.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/SSWCPProtocol.cpp`, `src/libslic3r/SSWCPProtocol.hpp`, `src/slic3r/GUI/FlowTypeHelper.cpp`, `src/slic3r/GUI/FlowTypeHelper.hpp`, `src/slic3r/GUI/HighFlowCompat.cpp`, `src/slic3r/GUI/HighFlowCompat.hpp`. Keys: `filament_flow_support`, `filament_volume_type`, `nozzle_volume_type`, `printer_flow_support`, `process_flow_support`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.

<a id="snapmaker-tip-cooling-motion"></a>
## Snapmaker development cooling, infill margin and short-travel changes

**Unknown; P1.** Dependencies: project-migration.

Six additional schema names at Snapmaker b070bcf, beyond exact v2.4.1, are absent here. Inspect consumers and possible renamed equivalents before deciding whether to port cooling transitions/slowdown, external infill margin and short-travel acceleration. Add source-attributed behavior and G-code comparisons; no inert settings or automatic profile substitution.

Plugin/agent assessment: No bundled plugin substitutes for this native compatibility/release gate.

Reference implementation evidence:
- snapmaker-v241 (`bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/LayerRegion.cpp`. Keys: none for this bounded component.
- snapmaker-main (`f5fd7289ea067997181ee6c2cf15a98f58faba43`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/LayerRegion.cpp`. Keys: none for this bounded component.
- orca-mcp-base (`17a745e30c248cf3acb4c429b650b22d106fd19a`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`. Keys: none for this bounded component.
- forca (`0b1f80cd22793785d8ae5c4296d2fe4a9248bd21`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/LayerRegion.cpp`. Keys: none for this bounded component.
- ultimate (`working tree; see candidate_base and diff digest`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`. Keys: none for this bounded component.
- orca-main-tip (`f96bbe8db13f603c767f0a21fce80da85c6a09f4`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`. Keys: none for this bounded component.
- orca-mcp-tip (`56b03d7bdfd9fc98ebe39e416a8d4324d18a1ec7`): `src/libslic3r/BeltGCode.cpp`, `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`. Keys: none for this bounded component.
- snapmaker-tip (`b070bcfaffcf93aaa04dff8fe97da3ee8dbd68bb`): `src/libslic3r/CustomGCode.cpp`, `src/libslic3r/Fill/Fill.cpp`, `src/libslic3r/GCode.cpp`, `src/libslic3r/GCode/CoolingBuffer.cpp`, `src/libslic3r/GCode/CoolingBuffer.hpp`, `src/libslic3r/LayerRegion.cpp`. Keys: `cooling_perimeter_transition_distance`, `cooling_slowdown_logic`, `external_infill_margin`, `overhang_threshold_participating_cooling`, `overhang_totally_speed`, `travel_short_distance_acceleration`.

Tests/evidence: `docs/testing/local-validation.md`; `docs/testing/evidence/plugin-integration-offline.json`.
