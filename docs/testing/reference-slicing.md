# Offline reference slicing

The 2026-11-04 Linux runs used publisher-digest-verified AppImages, extracted into task-only folders. They were not installed. Containers had no network, a read-only root filesystem, an unprivileged user and separate temporary HOME/datadir paths. G-code was never executed. Release and output hashes are in [reference evidence](evidence/reference-releases.json).

Snapmaker Orca v2.4.1 successfully sliced and exported a single-cube U1 project and a four-cube/four-material U1 project. Their emitted tool selections were respectively T0 and T0/T1/T2/T3. These are reference outputs, not proof that Ultimate U1 can yet load or slice them, nor that physical tool changes are safe.

FOrca v2.3.2-fos.8.6.8 generated single-cube G-code but exited with SIGSEGV during 3MF export, both with and without a virtual display. No successful FOrca project export is claimed. Its generated G-code is available only as a provisional diagnostic reference.

## Reproduce test inputs

Run `tools/u1/reference_fixture.py` against the extracted AppImage's `resources/profiles`, choosing the exact indexed machine, process and filament names. For Snapmaker v2.4.1:

```sh
python3 tools/u1/reference_fixture.py \
  --profiles /task/extracted/resources/profiles --destination /task/fixture \
  --machine 'Snapmaker U1 (0.4 nozzle)' \
  --process '0.20mm Standard @Snapmaker U1 (0.4 nozzle)' \
  --filament 'Snapmaker PLA SnapSpeed @U1' --tools 4
```

FOrca's corresponding process name is `0.20 Standard @Snapmaker U1 (0.4 nozzle)`. The tool resolves indexed inheritance into temporary inputs, preserves system identity, supplies machine nozzle context to partial presets and clears post-processing commands. Original presets remain unchanged. Four-tool mode creates distinct material display names/colors and four cube files; it retains source material identifiers and does not fabricate NFC/RFID data. The fixture manifest records hashes and unvalidated calibration status.

Invoke the extracted CLI using its own AppRun environment wrapper in an isolated container with Xvfb. For one tool, load `machine.json;process.json`, `filament.json` and `cube.stl`. For four tools, load `filament1.json;...;filament4.json`, pass `--filament-colour "#FF0000;#00FF00;#0000FF;#FFFFFF"`, `--load-filament-ids '1,2,3,4' --arrange 1`, and load the four cube files. Use `--slice 0 --outputdir /task/output --export-3mf reference.3mf`. The export name must be relative: the legacy CLI prepends outputdir itself.

## Diagnosed input failures

Both audited legacy forks normalize each partial preset separately. Their `DynamicPrintConfig::normalize_fdm` dereferences `nozzle_diameter` when processing `wipe_tower_filament`, causing SIGSEGV for a flattened process preset without machine context. A GDB backtrace confirmed this path. Supplying the selected machine's nozzle array avoids that failure. Changing flattened inputs to `from: User` without `inherits` also makes the legacy CLI compare compatibility against an empty system printer name; preserving `from: system` retains the selected machine identity. These adapters are confined to test inputs and do not constitute production profile migration.

No mixed-nozzle, Color Patch, material-adhesion, printer-connectivity or physical-print validation is implied.

The initial four-material export without explicit CLI filament colors retained a single color entry. A corrected run with the above four colors exported all four entries and T0/T1/T2/T3 selections. Ultimate U1 rejects both the single and corrected four-color vendor projects on raft_first_layer_expansion=-1, not on that corrected color metadata. This is an executed compatibility failure.
