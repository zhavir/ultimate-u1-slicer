# Current validation checkpoint — 2026-11-05

The [experimental Windows portable build](windows-portable.md) compiled and passed native verification plus all 3,462 configured Windows unit tests. Source `b3fcd387d8610da34b39357afc4df5e71e42dcdb`; [CI run](https://github.com/zhavir/ultimate-u1-slicer/actions/runs/41964174657). Independent archive integrity/checksum checks passed. No stable/hardware compatibility is claimed.

The complete Linux FFF suite passed with zero errors/failures and two inherited skips, and all five affected recording/plugin cases passed with 69 assertions in isolated processes. The full Linux GUI test binary builds, but only the named affected GUI cases were rerun. The failed native Windows attempts and successful final report remain in evidence. The following dated checkpoints describe earlier results, not current authorization or the final Windows outcome.

## 2026-11-05 regression update

The full inherited FFF suite passed after restoring Orca-family G-code header compatibility: 1,230 generated cases, 607,110 assertion records, zero errors/failures and two inherited skips (419.422 seconds). The preceding full run exposed seven branding-related errors; that failure is preserved alongside the successful rerun in [structured evidence](evidence/fff-gcode-compatibility.json). The added cross-brand regression passed 27 assertions across five producer scenarios. Maintenance tooling passed all 36 tests.

The native Windows application compiled in [run 41923614157](https://github.com/zhavir/ultimate-u1-slicer/actions/runs/41923614157), but verification and nine regression cases failed. Follow-up commits fix launcher diagnostics on protocol stdout, G-code branding compatibility, legacy configuration protection, Windows Unicode plugin paths and explicit recording-fixture authorization. Windows revalidation remains required; no verified portable release is claimed. Local GUI/plugin tests are rebuilding separately. Native Windows interoperability from WSL failed with `UtilBindVsockAnyPort`, so Windows validation uses GitHub native runners.

User authorization now includes direct main pushes and experimental publication at `zhavir/ultimate-u1-slicer`. Earlier local-only statements below describe the earlier checkpoint, not current authorization.

# Local validation checkpoint

Host: Linux x86_64, 2026-11-04. The user requested local-only work. No remote workflow, publication or physical printer test was performed. Installed slicers and user preset directories were not used.

## Application and native MCP

The inherited Ubuntu 24.04 container recipe built the dependencies and linked the full Release application, profile validator and system-cache generator. The executable is `build/src/Release/orca-slicer`; its help identifies UltimateU1Slicer 2.5.0-dev. The broad test build was interrupted to prioritize focused U1 regressions; the entire inherited suite is not claimed to pass. Packaging/signing and native macOS/Windows builds remain unverified.

The actual native Linux GUI server passed bearer authentication, legacy 2025-11-25 initialization, current 2026-07-28 discovery, get_state, list_objects and advisory planning. A second live run loaded an STL via the application command line, selected shipped Snapmaker U1 presets in a private configuration, rejected a wrapping object index and sliced through MCP. It returned a successful plate, 25 layers, and estimated time/material metrics. This is a custom smoke client, not Codex/Claude client validation. See evidence/mcp-live-smoke.json and evidence/mcp-slice-smoke.json. No printer was contacted.

The diagnostic image needed a valid CA bundle and generated en_US.UTF-8 locale. Early GUI calls were correctly refused as not-ready. A flattened CLI-exported project triggered the existing Customized Preset safety dialog; the MCP mutation guard refused slicing. That warning was retained. The successful fixture used an STL and shipped presets. Readiness is awaited through the native wait tool. File/project/settings/UI/script/printer MCP tools remain gated pending authorization adapters.

## Tests and tooling

- Production protocol/planner/file policy: **12 cases / 68 assertions pass**, with undefined-behavior and float-cast-overflow instrumentation. Coverage includes bounded searches, malformed fields, negotiation, policy and Unicode/traversal/symlink paths.
- Unchanged upstream HTTP tests: **8 cases / 43 assertions pass** using loopback-only servers. The restricted shell initially denied sockets; the authorized local run passed.
- Production FFF engine: **1 case / 3 generated scenarios / 36 assertions pass**: one material, four uniform nozzles, and four mixed 0.4/0.6 mm nozzles. It verifies extruding tool assignments and actual generated outer-wall path widths at 105% of the assigned nozzle. The synthetic fixture warns about absent optional filament retraction overrides; it does not establish vendor calibration.
- Python tooling: **28 tests pass**, covering immutable catalogs, inheritance/cycles, pins/dirty trees, safe destinations, offline G-code checks, upstream review, checksums and reference adapters.
- Ruff 0.14.3, new-file clang-format 19.1.7 checks and git diff --check pass. Workflow YAML parses locally; remote runner execution remains unverified.
- macOS plist structure passed regression tests after repairing inherited key/value ordering. This is not a macOS build.

JUnit evidence: evidence/components.junit.xml, evidence/mcp-http.junit.xml and evidence/u1-fff.junit.xml. Catch2 XML tests counters count assertions; console summaries distinguish cases and generated variants.

## Actual projects and G-code

The compiled app slices a 5 mm cube using temporary flattened copies of retained official U1 machine/process/PLA presets, exports G-code/3MF and exits 0 without slicing warnings. These profiles are not newly calibrated. Tool/motion/docking safety and material adhesion are not physically verified.

Publisher-digest-verified Snapmaker v2.4.1 produced single/four-material reference G-code and 3MF successfully. Explicit color metadata was needed for the complete four-color reference. Both vendor projects fail this app's validation on `raft_first_layer_expansion = -1`: automatic in Snapmaker's newer support implementation, but below this official engine's minimum zero. It was not silently clamped. Existing Snapmaker project compatibility remains a release blocker. See [reference procedure](reference-slicing.md) and evidence/reference-releases.json.

FOrca generated single-material G-code but crashed during 3MF export in the isolated environment. No successful FOrca project export or equivalent-output claim is made. Synthetic four-head tests do not validate vendor docking macros, purge towers, full FOrca feature assignment or Color Patch.

## Profiles, upstreams and remaining gates

The immutable review catalog contains 3125 presets and 821 cross-source collisions kept separate. Repeated sync verifies hashes and preserves overrides. Shipped Snapmaker/OrcaFilamentLibrary validation passes; imported FOrca/separate Snapmaker catalogs fail the official validator and remain quarantined. Real exits/examples are in evidence/profile-validation.json. Separate Snapmaker profile redistribution rights remain unknown.

The upstream audit found one official commit and five profile commits beyond pins. Git merge-tree reports a clean textual merge for the official candidate despite a shared touched path. No source updates were integrated or semantically verified. See ../architecture/evidence/upstream-review-initial.json.

No macOS ARM64/x86_64 or Windows build, Codex/Claude replay, complete inherited suite, full FOrca migration, stock/Extended Firmware connection or physical print has passed here. There is no stable release or macOS artifact. See [roadmap](../roadmap.md).
