---
name: ultimate-u1-maintenance
description: Maintain zhavir/ultimate-u1-slicer, investigate upstream alerts, integrate U1/MCP/profile changes, and build or publish experimental Windows portable artifacts. Use for this slicer's ongoing development and release maintenance.
---

# Ultimate U1 maintenance

Read root `AGENTS.md`, then the references for the current task. The authoritative public destination is `zhavir/ultimate-u1-slicer`, default branch `main`. The owner currently permits tested changes pushed directly to main and experimental artifact publication there. Do not push to third-party upstream repositories or force-push. No printer action is authorized by repository/release work.

## Source and architecture

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

Push reviewed commits to main, then use `gh workflow run u1-windows-portable.yml --repo zhavir/ultimate-u1-slicer --ref main -f publish=true` when an experimental prerelease is intended. Track the exact source SHA with `gh run list/view`; inspect failed logs, fix concrete failures and rerun only affected work. Do not assume a dispatched run succeeded. The verification job launches the actual Windows executable, checks bearer authentication and confirms the roaming profile and automatic URL registration stay untouched after GUI readiness. The prerelease job requires both portable verification and the full native Windows unit-test job to pass. A successful compiler exit alone is insufficient. Keep Windows launcher diagnostics on stderr so packaged MCP stdio remains valid JSON, retain legacy Orca configuration protection, and test plugin imports from UTF-8 paths (including non-ASCII Windows usernames). Only verified archives reach the prerelease job. Download/check the SHA-256 and report the run/release links. Native launch verification does not prove slicing or physical printing.

The other application platforms use `u1-platform-builds.yml`; component CI uses `u1-component-tests.yml`. Inherited workflows remain enabled: automatic approval review rejected broad workflow disabling. This project uses dedicated U1 entrypoints; do not assume inherited administrative or duplicate build automation has been disabled. Keep source-integration and notification behavior separate when syncing workflows. Read `docs/building-ultimate-u1.md` for local builds.

## Current release gates

Read `docs/roadmap.md` before release claims. Linux compilation, native MCP inspection/STL slicing and synthetic mixed-nozzle paths have passed. Original Snapmaker v2.4.1 3MF imports reject automatic support expansion `-1`; do not silently clamp its different support semantics. Full FOrca per-feature schema/Color Patch migration, current Snapmaker gateway/feeding parity, full inherited regression coverage, native platform packaging and physical printing remain separate gates. No stable/production U1 release is established by an experimental portable ZIP.

Keep MCP loopback/bearer auth, default-off scripts, authorized file roots and the restricted tool catalog. Printer-control approval adapters remain missing. Never print, heat, home, execute macros, flash firmware, invent RFID identifiers or expose credentials as part of maintenance.
