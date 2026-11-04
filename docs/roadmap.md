# Ultimate U1 Slicer roadmap

Current milestone: experimental source integration and component validation. No stable or production release exists.

## Completed investigation and initial implementation

- Cloned and inspected three distinct slicer sources, verified SnOrca alias, recorded full pins/branches/release and issue samples, computed common ancestry and source diffs.
- Selected official MCP development as an integration baseline, retained original server/lifecycle/tests and recorded U1 parity gaps in ADR-001.
- Created isolated application data identity, a native advisory FOrca partition-planner import, MCP protocol validation fixes, file-root policy and a tested slicer-only tool gate.
- Implemented immutable, attributed cross-source profile review catalog generation. It detects inheritance errors, repeated identities, collisions and source/snapshot tampering without touching user presets.
- Added native component tests using production C++ and existing Catch2. Full application configure reached missing Boost; macOS build/hardware remain unavailable.

## Next executable work and release gates

1. Restore a complete upstream dependency build and get a clean full Release build on macOS ARM64. Prove bundle/executable/resource/localization/data-path isolation and disable inappropriate upstream installer/update paths before distribution. Linux component tests are insufficient.
2. Execute the upstream native MCP transport/core suites and live client replay tests; add operator-bound authorization for project/file operations, sensitive config, destructive actions and printer control. Expand the explicit allowlist only after each handler is reviewed and tested.
3. Validate selected profile catalogs against actual ConfigDef and compiled preset loader. Resolve the separate Snapmaker profiles license. Promote compatible presets with versioned bundle changes; implement read-only user preset import and explicit overrides.
4. Port FOrca per-nozzle schema, feature assignment, import/remapping, safety preflight, material rules and Color Patch together as reviewed patches. The advisory optimizer is not a substitute. Add project migration fixtures and golden semantic G-code comparisons.
5. Port or adapt current Snapmaker gateway/pairing/feeding behavior; exercise stock and optional Extended Firmware fixtures through read-only capability detection. Keep generic Moonraker behavior separately reported.
6. Run real single-material, four-tool, mixed-nozzle and Color Patch slicing tests, existing U1 3MF import/export, unsafe configuration rejection and MCP-driven slicing. No representative outputs have been generated yet.
7. Run macOS ARM64, macOS x86_64 if supported, Windows x64 and Linux x64 application CI, package under a unique application identity, generate SHA-256/version/release notes, preserve a tested stable release and exercise update-review automation.
8. Complete the separate supervised hardware checklist before a production release. Initial stable software release may keep physical compatibility provisional only when all offline definition-of-done gates pass.

## Known external blockers

This host is Linux x86_64 with no native macOS/Windows toolchains or U1 hardware. No GitHub destination/runner credentials were supplied, so workflows are authored but not dispatched or remotely verified. Missing application dependencies may be built locally; the current dependency-build outcome is recorded in local-validation.md. Unknown profile redistribution rights block shipping those profiles even though local review is possible.

The architecture audit is substantial but not exhaustive: third-party license/SBOM review, all issue/PR history, project migrations and every slicing path still need work. Do not call Phase 1 complete in the sense of a full release audit. Continue through feasible implementation work; each release gate requires its own evidence.
