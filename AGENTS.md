# Ultimate U1 Slicer contributor instructions

This is an integration branch, not a stable U1 release. Preserve inherited AGPL notices and source attribution. The baseline is official OrcaSlicer feature/mcp at the SHA in tools/u1/sources.lock.json.

Use C++17, existing CMake targets, wxWidgets conventions, RAII and established upstream APIs. Read tests/AGENTS.md before adding tests, and the relevant .claude/skills/ entry before modifying system profiles or wxWidgets UI. Run clang-format on changed C++ when available. Keep vendored dependencies pinned; do not edit them without source/version attribution.

Never modify installed slicers or user preset directories. Ultimate U1 uses its own application key. Profile imports go into a separate managed catalog, never directly into resources/profiles or existing user directories. Imported presets are unvalidated for U1 until calibrated.

Keep slicer operations separate from printer operations. No autonomous printing, heating, homing, macro execution, firmware flashing or destructive hardware testing. Credentials never belong in tracked files or logs. Bind MCP to loopback, retain bearer authentication and default-off Python execution, and restrict file operations to operator-authorized roots. Do not call generic Moonraker a replacement for Snapmaker pairing or gateway APIs.

Record source evidence and exact test commands. A source implementation is not runtime or hardware verification. Unknown functionality stays Unknown. Missing full application builds, project/slicing regressions and physical tests block stable releases. Update docs/roadmap.md with remaining gates.

Use small commits. Inspect git status, diff and staged paths before each commit. Never include unrelated files. Do not automatically merge upstream updates. Generate a compatibility report and run relevant tests before proposing an integration. Preserve pinned source baselines.

Build the full app using the inherited build scripts. Fast component tests: cmake -S tools/u1/native-tests -B build/u1-native; cmake --build build/u1-native; ctest --test-dir build/u1-native --output-on-failure. Python tooling tests: python3 -m unittest discover -s tools/u1/tests -v. These checks do not prove a working GUI or a safe print.
