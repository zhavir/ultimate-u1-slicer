# U1 nozzle preset coverage

The audited catalog indexes five selectable U1 printer presets: 0.2, 0.4,
0.4+0.6, 0.6 and 0.8 mm. This is not a FOrca limitation to 0.4/0.6 mm.
`resources/profiles/Snapmaker.json` registers each machine file;
`resources/profiles/Snapmaker/machine/Snapmaker U1.json` advertises all five
variants. The mixed preset is a separate printer preset, not the complete nozzle
catalog. Each selectable machine declares its matching `printer_variant`.

Seeing only the mixed preset does not establish that the others are missing.
Reopen the application's printer setup, select Snapmaker U1 and the desired
nozzle variants where offered, then finish and inspect the printer preset list.
Use this application's own portable directory. Do not copy settings into an
installed Snapmaker/Orca configuration or edit the installation's configuration
by hand. If the desired presets still do not appear, retain the diagnostic log
and report the exact portable version and selected printer setup; that runtime
case is not yet reproduced.

Source boundaries: the native `PrinterPicker` in `ConfigWizard.cpp` reads
`AppConfig::get_variant`; the current WebView setup uses `WebGuideDialog.cpp`
`nozzle_diameter` and `nozzle_selected` plus `resources/web/guide/21/common.js`.
These are separate setup implementations. Their source presence is not evidence
of a successful interaction in the user's Windows session.

Validation on 2026-11-05: `python3 scripts/orca_profile_tool.py check --vendor
Snapmaker --vendor OrcaFilamentLibrary` checked both bundles with zero errors
and zero warnings. It validates the catalog, not UI visibility, printer firmware,
high-flow hotend detection, material calibration or safe physical printing.
No user configuration was read or modified for this check. Extra nozzle sizes
must remain provisional until their tool-specific slicing and hardware checks
pass; do not infer calibration from a generic inherited filament preset.
