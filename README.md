# Ultimate U1 Slicer

Experimental, U1-first integration of the OrcaSlicer ecosystem. **This is not a stable release.** No macOS ARM64 application build or physical U1 print has been verified yet.

The source starts from official OrcaSlicer's native MCP development branch, with an explicit Snapmaker compatibility patch queue. SnOrca is Snapmaker Orca's nickname, not a fourth independent upstream. All source pins and the base decision are documented in the [repository audit](docs/architecture/repository-audit.md) and [ADR](docs/architecture/architecture-decision.md).

This is the full Orca application, not a profile collection. The integration scope includes every U1-beneficial compatible engine, calibration, model/painting, project, UI, connectivity and automation feature. [FOrcaSlicer](https://github.com/jiyang1018/FOrcaSlicer) is also a tracked Git upstream with release/tag/branch alerts. Retained implementations and remaining fork migrations are listed in the [whole-application feature backlog](docs/architecture/u1-feature-backlog.md); existing source does not by itself establish U1 verification.

Current additions include a bounded advisory FOrca filament-partition planner in the native MCP server, protocol input-validation fixes, a restricted slicer-only MCP tool catalog, operator-owned file roots, independent application-data identity, and immutable attributed profile review catalogs. Imported profiles remain unvalidated for U1; no user presets or installed slicers are modified. The complete official MCP implementation remains in source, but file/project mutation, generic UI/script bridges and printer-control tools are gated pending authorization review.

The Linux application builds and slices a cube with retained official U1 profiles. Native GUI MCP inspection/planning and synthetic one/four-tool engine regressions pass. Original Snapmaker 3MF compatibility is still blocked by configuration differences.

Use the [build instructions](docs/building-ultimate-u1.md), [feature matrix](docs/architecture/feature-matrix.md), [actual validation results](docs/testing/local-validation.md) and [roadmap](docs/roadmap.md). Snapmaker gateway/feeding parity, full FOrca per-nozzle/Color Patch integration, configuration migrations, live GUI/client slicing regressions and native platform packaging remain release gates.

Fast checks use the existing CMake/Catch2 stack and Python standard library:

```sh
cmake -S tools/u1/native-tests -B build/u1-native -DCMAKE_BUILD_TYPE=Release
cmake --build build/u1-native --parallel 4
ctest --test-dir build/u1-native --output-on-failure
python3 -m unittest discover -s tools/u1/tests -v
```

The optional unchanged upstream HTTP test suite requires Boost and loopback socket access. Passing component tests does not establish a working GUI, valid representative U1 G-code or physical printer compatibility. Hardware tests are manual and separately authorized.

[Profile synchronization](docs/profiles/synchronization.md), [MCP integration](docs/mcp/integration.md), [firmware boundaries](docs/firmware/compatibility.md) and [upstream review](docs/architecture/upstream-strategy.md) describe the current limits. The GitHub project is [zhavir/ultimate-u1-slicer](https://github.com/zhavir/ultimate-u1-slicer). Windows portable builds use u1-windows-portable.yml and include a dedicated portable data directory. Six-hour upstream checks create assigned issues for branch/release/tag changes. The project maintenance skill is [.claude/skills/ultimate-u1-maintenance/SKILL.md](.claude/skills/ultimate-u1-maintenance/SKILL.md). The Actions workflows build experimental candidates and notifications; they never merge source updates or publish a stable Ultimate U1 release automatically.

Licensed under the inherited AGPL-3.0 terms; retain corresponding source and attribution. See [LICENSE.txt](LICENSE.txt), [import attribution](docs/architecture/imports.md) and the [original upstream README](docs/architecture/upstream-readme.md). Separate Snapmaker profile redistribution remains blocked pending license clarification.
