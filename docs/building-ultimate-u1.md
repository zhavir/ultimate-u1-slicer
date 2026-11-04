# Build and validation

This is an experimental integration checkout at `ultimate-u1/integration`. It retains official Orca's CMake/dependency system and native MCP implementation. A full Linux Release binary has been linked and executed here. No macOS ARM64 artifact has been produced.

The source worktree is `/home/aaramini/snapmaker3d-projects/ultimate-u1-slicer`; its Git object store is in the neighboring `ultimate-u1-audit/orca/.git`. Keep that audit checkout while using this linked worktree. A standalone clone can be made from the committed integration branch before moving either directory; do not delete the backing object store. Public source baselines are in tools/u1/sources.lock.json.

## Fast native component checks

Use a C++17 compiler, CMake and Ninja. The current local tooling environment pins CMake 3.31.10 and Ninja 1.13.0.

```sh
cmake -S tools/u1/native-tests -B build/u1-native -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build/u1-native --parallel 4
ctest --test-dir build/u1-native --output-on-failure
python3 -m unittest discover -s tools/u1/tests -v
```

These targets compile actual production MCP protocol and planner code plus the file-policy header using the existing bundled Catch2. They do not replace the full application tests or validate the GUI adapter. Use `PATH="$PWD/.venv-build/bin:$PATH"` locally if relying on the isolated build tools.

## Full application

Follow the inherited build prerequisites and scripts; never point a build, run or profile import at an installed slicer. Use Release. On native macOS ARM64, after installing the prerequisites documented by the upstream build:

```sh
./build_release_macos.sh -dx -a arm64
./build_release_macos.sh -sxT -a arm64
```

The first command builds dependencies, the second builds the application/tests using the same script. `-T` is the upstream test flag, not a timing flag. macOS x86_64 uses `-a x86_64` if supported by the available Xcode SDK. No cross-compilation from this Linux host is claimed.

On Linux, use `build_linux.sh` after provisioning its documented system libraries. `./build_linux.sh -d` builds dependencies and `./build_linux.sh -sti` builds the app, tests and AppImage. The `-u` flag installs system packages and is not required for component tests. On Windows, use the existing `build_win.bat -ds --run-tests` in a configured native developer environment. Consult each script's help for generator/compiler options.

The direct full configure here stopped at missing Boost 1.83. The dependency project configured successfully, but GTK3/autoconf/automake/libtool are also absent on this host. Boost 1.84 was subsequently built locally with the inherited dep_Boost target, enabling the original HTTP tests. A separate Ubuntu build image has been built using the inherited -g recipe; the application build outcome is recorded in local-validation.md. See [local validation](testing/local-validation.md) for actual outcomes; do not infer a successful app build from a successful dependency configure.

## Isolation and packaging

The successful Linux run created the inherited image with `ORCA_DOCKER_CMAKE_VERSION=3.31.10 ./build_linux.sh -g -r -j4`, then ran `CI=true GITHUB_ACTIONS=true GITHUB_WORKSPACE="$PWD" ./build_linux.sh -dstrlL -j2` inside it as the unprivileged ubuntu account. Mount this checkout and its linked Git object store at their original absolute paths, the latter read-only. Four CPUs/eight GiB bounded the dependency/application run. The app, profile validator and cache generator linked; the later broad test build was interrupted to prioritize focused regressions. Dependency caches remain under deps/build. This establishes a local Linux build, not bit-identical reproducibility or native macOS packaging.

User data uses `UltimateU1Slicer`, the viewer uses `UltimateU1SlicerGcodeViewer`, and portable data uses `ultimate_u1_data_dir`. The fork does not auto-migrate another slicer's Flatpak data. It retains the inherited `OrcaSlicer` translation catalog name, independent of its data key. Bundle and Linux IPC identities are fork-specific. Packaging currently retains upstream binary/bundle filenames to match existing build scripts; distribution under a distinct final bundle/installer name, URL associations, updater behavior, cache generators and every resource path still require a native packaging audit before release.

No workflow publishes a stable Ultimate U1 release automatically. The added release-preparation job hashes available artifacts and records source/version metadata; building, signing, notarizing, installing and physically validating those artifacts remain separate gates.

Optional HTTP tests use the locally built Boost prefix: add `-DU1_ENABLE_HTTP_TESTS=ON -DCMAKE_PREFIX_PATH=/absolute/project/deps/build/u1/destdir/usr/local` to the component configure. `-DU1_ENABLE_SANITIZERS=ON` instruments the component protocol/planner tests. Socket tests require permission to bind loopback; no printer is involved.

## Focused production-engine regression

After the inherited full dependency/configure steps, enable `cmake -S . -B build -DU1_BUILD_FOCUSED_REGRESSIONS=ON` and build `cmake --build build --config Release --target u1_fff_tests --parallel 2`. Run `build/tests/fff_print/Release/u1_fff_tests "[U1ToolGcode]"` on Linux. This uses the existing FFF helpers and actual libslic3r engine; the same fixture remains in the broad fff_print_tests target. It verifies one/four-tool selection and mixed-nozzle path widths, not firmware macros or hardware. The broad test suite has not completed locally.

## GitHub Windows x64 portable

The authorized project is https://github.com/zhavir/ultimate-u1-slicer, branch main. `u1-windows-portable.yml` reuses the inherited build/dependency scripts with portable-only enabled, skips NSIS, and packages `Ultimate-U1-Slicer-Windows-x64-portable.zip`. Extract into a writable folder, keep `ultimate_u1_data_dir` beside `orca-slicer.exe`, and launch that executable; no installer is needed. Do not rename the data folder to upstream `data_dir`.

The verification job extracts a private copy on a clean native Windows runner, checks executable help, starts only the local MCP endpoint, confirms a bearer token is required and initialization identifies Ultimate U1, and proves discovery/settings are created beside the executable without a roaming UltimateU1Slicer directory. After native GUI readiness it also checks that portable startup did not register the Ultimate U1 URL handler. Automatic file/URL associations are skipped for portable startup; explicit Preferences actions remain user-controlled. It does not contact a printer. The tested extraction and generated credentials are removed; the published archive remains the clean build payload plus a portable marker. SHA256SUMS and verification.json accompany the verified artifact.

Pushes build artifacts. For an experimental prerelease, explicitly dispatch `gh workflow run u1-windows-portable.yml --repo zhavir/ultimate-u1-slicer --ref main -f publish=true`; publication depends on successful native verification. Check the exact run/commit with gh and link its artifacts/release. No stable release claim follows from portable startup verification. Native slicing, project migration and hardware remain their own gates.
