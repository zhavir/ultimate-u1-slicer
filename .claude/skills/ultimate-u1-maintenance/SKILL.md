---
name: ultimate-u1-maintenance
description: Maintain zhavir/ultimate-u1-slicer, investigate upstream alerts, integrate U1/MCP/profile changes, and build or publish experimental Windows portable artifacts. Use for this slicer's ongoing development and release maintenance.
---

# Ultimate U1 maintenance

Read root `AGENTS.md`, then the references for the current task. The authoritative public destination is `zhavir/ultimate-u1-slicer`, default branch `main`. The owner currently permits tested changes pushed directly to main and experimental artifact publication there. Do not push to third-party upstream repositories or force-push. No printer action is authorized by repository/release work.

## Source and architecture

The product is U1-only. As of 2026-11-06 the user prioritizes complete Snapmaker-fork source integration ahead of MCP, official Orca additions and FOrca extras. Treat Snapmaker as the stock-device behavioral authority. Preserve the existing implementation while reassessing ADR-001 if the official-base patch queue cannot preserve complete U1 behavior. Source-only import is not integration: connect consumers, UI, companion/runtime dependencies, isolated storage, packaging and configuration migration, then run offline tests. Hardware availability blocks end-to-end verification, not feasible software implementation. Track that verification separately; do not operate hardware until explicitly authorized.

The default scope is every compatible U1-beneficial feature in the complete Orca and FOrca applications, not profile synchronization alone. Read `docs/architecture/u1-feature-backlog.md` for retained implementations, source-backed evidence and the remaining migration order. Audited source pins do not imply every feature at that revision has been ported or tested.

`tools/u1/sources.lock.json` owns reviewed source revisions. The experimental base is official Orca's native MCP branch, with a small U1 patch queue; retain its server, GUI and existing CMake/dependency scripts. SnOrca is the verified nickname for Snapmaker Orca, not a separate source. Read `docs/architecture/architecture-decision.md`, `repository-audit.md` and `feature-matrix.md` before changing the base or claiming parity. Inspect implementation and tests, not just READMEs or version numbers.

The original local checkout is a linked worktree backed by neighboring `ultimate-u1-audit/orca/.git`; do not delete that store. GitHub checkouts are standalone. `origin` is this project's writable remote; `orca-upstream`, `snapmaker`, `forca` and the firmware/profile remotes are source references. Preserve AGPL notices and attribution. The separate Snapmaker profile repository has unresolved redistribution licensing: local review does not authorize shipping it.

## Handle an upstream issue

1. Read the issue's source/ref/event and exact compare/release URL. An alert is not verified functionality. Releases/tags are watched once per repository; official main and feature/mcp have separate branch heads. A monitor-error means observation failed, not that a feature is absent.
2. Read `docs/architecture/upstream-strategy.md`; use `python3 tools/u1/upstream_review.py --fetch --probe-merges` for source classifications/overlaps. A clean merge-tree probe does not establish API or G-code compatibility. Fetch source only; do not execute unreviewed upstream workflows/scripts.
3. Integrate selected fixes on a local integration branch or patch queue, retaining U1 features. Review schema/project migration, native MCP lifecycle, printer protocol and profile inheritance together where coupled. Avoid full merges merely to reach the latest version.
4. Run affected tests below, update the feature evidence/roadmap and only then advance reviewed pins. Close the notification with the integration commit or explicit deferral. Never auto-merge an alert into main.

`tools/u1/upstream_watch.py` observes API metadata and creates fingerprinted `upstream-update` issues assigned to the configured maintainer. Closed issues remain part of deduplication. `.github/u1-maintenance.json` owns destination/assignee; `.github/u1-upstream-baseline.json` owns initial release/tag observations, not integrated code. Capture a replacement baseline only after reviewing what it acknowledges. It checks the configured branch heads and 30 recent releases/tags, including prereleases, release edits and tag retargets; it does not crawl every upstream issue or branch. The six-hour workflow has read-only source access and issue-write access, with no merge/push permissions.

## Validate a change

- Fast C++: configure/build/ctest `tools/u1/native-tests` (production protocol/planner/file policy). Optional original HTTP tests need Boost and loopback sockets.
- Tooling: `python3 -m unittest discover -s tools/u1/tests -v` and `ruff check tools/u1`. Run meaningful affected tests; do not manufacture tests that merely match wording.
- Slicing: build `u1_fff_tests` with `-DU1_BUILD_FOCUSED_REGRESSIONS=ON`, then run `[U1ToolGcode]`. It checks real engine paths for one/four tools and mixed 0.4/0.6 mm nozzles. Also run relevant full suites for behavioral changes. Read `tests/AGENTS.md`.
- Live MCP: `tools/u1/mcp_smoke.py` uses an already-running task-isolated native GUI. Its optional slice mode requires a trusted offline fixture loaded by the operator. Never bypass modal safety warnings or re-enable generic UI/script bridges to make a test pass.
- Profiles: `profile_sync.py` builds immutable attributed review catalogs, never installed presets. Run the actual profile/schema validators before promotion, preserve overrides/inheritance and mark uncalibrated imports. Read `docs/profiles/synchronization.md` and `.claude/skills/orca-profiles/SKILL.md` when changing shipped profiles.

Read `docs/testing/local-validation.md` for actual scope and `docs/testing/reference-slicing.md` for isolated reference fixtures. Preserve failures as evidence. Local component tests do not establish Windows/macOS, live client or hardware success.

## Windows portable build and publication

Use `.github/workflows/u1-windows-portable.yml`: it reuses the established dependency/application builds with `portable-only: true`. The ZIP contains the inherited `orca-slicer.exe`, resources/DLLs and `ultimate_u1_data_dir/portable-mode.txt`. The directory must be beside the executable to select portable storage; do not rename it to upstream `data_dir` or package generated user settings/tokens. No installer or changes to existing installations are required.

Push reviewed commits to main, then use `gh workflow run u1-windows-portable.yml --repo zhavir/ultimate-u1-slicer --ref main -f publish=true` when an experimental prerelease is intended. Track the exact source SHA with `gh run list/view`; inspect failed logs, fix concrete failures and rerun only affected work. Do not assume a dispatched run succeeded. The verification job launches the actual Windows executable, checks bearer authentication and confirms the roaming profile and automatic URL registration stay untouched after GUI readiness. The prerelease job requires both portable verification and the full native Windows unit-test job to pass. A successful compiler exit alone is insufficient. Read operator-owned UTF-8 environment values through Boost nowide consistently with the existing environment helpers; on Windows, Win32 environment updates and CRT getenv can expose different views. Keep Windows launcher diagnostics on stderr so packaged MCP stdio remains valid JSON, retain legacy Orca configuration protection, and test plugin imports from UTF-8 paths (including non-ASCII Windows usernames). Only verified archives reach the prerelease job. Download/check the SHA-256 and report the run/release links. Native launch verification does not prove slicing or physical printing.

The other application platforms use `u1-platform-builds.yml`; component CI uses `u1-component-tests.yml`. Inherited workflows remain enabled: automatic approval review rejected broad workflow disabling. This project uses dedicated U1 entrypoints; do not assume inherited administrative or duplicate build automation has been disabled. Keep source-integration and notification behavior separate when syncing workflows. Read `docs/building-ultimate-u1.md` for local builds.

## Current release gates

Read `docs/roadmap.md` before release claims. Linux compilation, native MCP inspection/STL slicing and synthetic mixed-nozzle paths have passed. Original Snapmaker v2.4.1 single/four-tool fixtures now import and slice offline with path-specific automatic support expansion and a persisted compatibility marker; complete project/engine fidelity remains Partial. Never silently clamp vendor support semantics. Full FOrca per-feature schema/Color Patch migration, current Snapmaker gateway/feeding parity, full inherited regression coverage, native macOS/Linux packaging and physical printing remain separate gates. Windows portable launch/MCP/isolation and all configured Windows unit tests have passed; read `docs/testing/windows-portable.md` for the exact artifact/source and evidence. No stable/production U1 release is established by an experimental portable ZIP.

Keep MCP loopback/bearer auth, default-off scripts, authorized file roots and the restricted tool catalog. Printer-control approval adapters remain missing. Never print, heat, home, execute macros, flash firmware, invent RFID identifiers or expose credentials as part of maintenance.

## Full parity and bundled integrations

Read docs/architecture/functional-parity-audit.md, functional-parity.json and the updated dependency backlog before claiming U1 functionality. Exact Snapmaker v2.4.1 is bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c; later main is a distinct reference. Use the explicit statuses Verified / Implemented but untested / Partial / Missing / Incompatible / Unknown. A viewport camera is not a printer stream; generic Moonraker/Bambu RFID is not U1 parity. All nozzle variants already in the catalog must remain available without inventing calibration.

Build optional wheels with tools/u1/build_plugins.py. Preserve the pinned MIT Studio snapshot and original notices. The noncommercial converter remains a connector to a separately installed service: never vendor its code/profiles/rules. Bundled packages must be discoverable but atomically installed disabled; the ordinary installer defaults to enabled, so staging must explicitly opt out. Never overwrite user packages while discovering bundles. Run native [U1Plugins] tests and the real Python inspection/HTTP-contract tests.

Windows signing uses tools/u1/windows/sign-portable.ps1 and independent Authenticode verification. No identity is currently configured. Do not substitute a self-signed certificate, leak PFX material, claim SmartScreen reputation, or call an unsigned candidate signed. Manual publication defaults to requiring a trusted timestamped signature. See docs/releasing/windows-signing.md.
