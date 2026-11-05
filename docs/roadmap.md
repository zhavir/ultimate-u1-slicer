# Ultimate U1 Slicer roadmap

Current milestone: experimental source integration and component validation. No stable or production release exists.

Feature scope is the whole application: every U1-compatible beneficial Orca/FOrca feature is in scope, including engine, modeling/painting, calibration, project workflows, UI, diagnostics, connectivity and native MCP. See architecture/u1-feature-backlog.md. FOrca is already a tracked upstream; unchanged branch metadata is not a full-integration claim.

## Completed investigation and initial implementation

- Cloned and inspected three distinct slicer sources, verified SnOrca alias, recorded full pins/branches/release and issue samples, computed common ancestry and source diffs.
- Selected official MCP development as an integration baseline, retained original server/lifecycle/tests and recorded U1 parity gaps in ADR-001.
- Created isolated application data identity, a native advisory FOrca partition-planner import, MCP protocol validation fixes, file-root policy and a tested slicer-only tool gate.
- Implemented immutable, attributed cross-source profile review catalog generation. It detects inheritance errors, repeated identities, collisions and source/snapshot tampering without touching user presets.
- Added native component tests using production C++ and existing Catch2. The full Linux application and inherited dependencies now build. Native MCP HTTP/component tests, live GUI MCP inspection and STL slicing plus synthetic one/four/mixed-nozzle engine slicing pass; macOS build/hardware remain unavailable.

## Next executable work and release gates

1. Restore a complete upstream dependency build and get a clean full Release build on macOS ARM64. Prove bundle/executable/resource/localization/data-path isolation and disable inappropriate upstream installer/update paths before distribution. Linux component tests are insufficient.
2. Execute the upstream native MCP transport/core suites and live client replay tests; add operator-bound authorization for project/file operations, sensitive config, destructive actions and printer control. Expand the explicit allowlist only after each handler is reviewed and tested.
3. Validate selected profile catalogs against actual ConfigDef and compiled preset loader. Resolve the separate Snapmaker profiles license. Promote compatible presets with versioned bundle changes; implement read-only user preset import and explicit overrides.
4. Port FOrca per-nozzle schema, feature assignment, import/remapping, safety preflight, material rules and Color Patch together as reviewed patches. The advisory optimizer is not a substitute. Add project migration fixtures and golden semantic G-code comparisons.
5. Port or adapt current Snapmaker gateway/pairing/feeding behavior; exercise stock and optional Extended Firmware fixtures through read-only capability detection. Keep generic Moonraker behavior separately reported.
6. Run real single-material, four-tool, mixed-nozzle and Color Patch slicing tests, existing U1 3MF import/export, unsafe configuration rejection and MCP-driven slicing. Reference Snapmaker single/four-material outputs were generated. The local shipped-profile single cube slices/exports successfully, but original Snapmaker project import fails validation and remains a release blocker.
7. Run macOS ARM64, macOS x86_64 if supported, Windows x64 and Linux x64 application CI, package under a unique application identity, generate SHA-256/version/release notes, preserve a tested stable release and exercise update-review automation.
8. Complete the separate supervised hardware checklist before a production release. Initial stable software release may keep physical compatibility provisional only when all offline definition-of-done gates pass.

## Known external blockers

This host is Linux x86_64 with no native macOS/Windows toolchains or U1 hardware. The user subsequently authorized git@github.com:zhavir/ultimate-u1-slicer.git as the writable project, direct pushes to main, GitHub configuration, Actions builds and experimental publication. Windows x64 portable is the current artifact priority. GitHub run results are recorded separately; workflow source alone is not success. Six-hour upstream checks create assigned, deduplicated issues and never merge source automatically. A local container build is being used to supply the absent host development libraries; the current application/test-build outcome is recorded in local-validation.md. Unknown profile redistribution rights block shipping those profiles even though local review is possible.

The architecture audit is substantial but not exhaustive: third-party license/SBOM review, all issue/PR history, project migrations and every slicing path still need work. Do not call Phase 1 complete in the sense of a full release audit. Continue through feasible implementation work; each release gate requires its own evidence.

## Current compatibility findings

Snapmaker v2.4.1 uses raft_first_layer_expansion=-1 with automatic semantics different from the selected official engine. Do not clamp it silently: port and test those semantics before claiming existing-project compatibility. An initial four-material reference export retained one filament color and was rejected by the stricter current CLI. Regenerating it with explicit four-color metadata removed that fixture defect; the corrected project reaches the same -1 schema rejection. FOrca reference G-code generation succeeded, but its 3MF export crashed in the isolated environment.

## 2026-11-05 regression checkpoint

Full Linux FFF tests now pass (1,230 generated cases, zero errors/failures, two inherited skips). Windows compilation succeeded, but portable verification and unit failures prevented publication; targeted fixes are committed and require native Windows rerun. The GUI/plugin suite is rebuilding locally. See testing/evidence/fff-gcode-compatibility.json. This does not resolve the existing Snapmaker 3MF auto-expansion migration or establish complete FOrca parity.

The source-level migration investigation is recorded in [support expansion migration](architecture/support-expansion-migration.md). Normal support, tree raft and tree support without a raft have different Snapmaker semantics; accepting or clamping `-1` alone is insufficient.

## Windows portable checkpoint — 2026-11-05

The experimental portable artifact is compiled and verified: all 3,462 configured Windows unit tests pass, alongside GUI/MCP HTTP/stdio and storage/registry-isolation checks. See [download and evidence](testing/windows-portable.md). Linux full FFF tests and five targeted GUI cases also pass. This completes the current Windows portable packaging milestone, not the stable release definition. Next remain original Snapmaker project/support semantics, reviewed native MCP file/project adapters, full FOrca advanced-nozzle migration, current Snapmaker connectivity parity and native macOS ARM64 application validation.

## Expanded functional-parity gate

The 71-group source-backed audit separates exact Snapmaker v2.4.1, later Snapmaker main, official MCP base and FOrca. See architecture/functional-parity-audit.md and the dependency-aware implementation backlog. Missing names include aliases and actual missing consumers; counts are not a hardware certification. The next portable candidate includes opt-in plugin discovery and signing gates, with signed publication blocked until a real identity is configured.
