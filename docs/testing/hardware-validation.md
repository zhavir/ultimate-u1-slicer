# U1 hardware validation checklist

All entries pending. No physical compatibility claim is justified by source inspection or generated G-code alone. Use a supervised printer with an accessible emergency stop and an operator who approves every physical action. Record firmware build, installed extensions, nozzle diameters, loaded materials, profiles, source commit and G-code SHA-256.

1. Confirm stock firmware detection, printer identity and authentication without movement or heating. Repeat independently for an Extended Firmware installation; record actual capabilities.
2. Verify four toolhead identities, independent nozzle sizes and loaded filament mapping against the physical machine. Check nozzle and temperature/material limits; refuse an inconsistent configuration.
3. Compare single-material and four-tool G-code with the vendor slicer, inspecting startup, tool-change/park/dock, heating, purge/prime tower and end sequences before submission.
4. Obtain operator authorization for uploading the exact hash; uploading alone must not start a job. Obtain separate explicit authorization to start.
5. Supervise a small single-material print, then a four-color print. Record collisions, ooze, adhesion, tower stability, feeding and status/progress correctness.
6. After mixed-nozzle integration passes offline tests, supervise a representative mixed-nozzle print with measured widths/heights and inspect tool-specific speeds, extrusion and offsets.
7. After Color Patch integration passes slicing tests, supervise a shell/core sample using a deliberately chosen compatible material pair; document bond quality and geometry.
8. Exercise reconnect, cancellation and safe recovery manually, using vendor-approved procedures. Never script emergency-stop release, unsafe motion, homing with obstructions or arbitrary macros.
9. Test optional MultiACE/NFC metadata synchronization only with documented compatible hardware and explicit operator approval. Do not write tag identifiers or bypass authentication.
10. Repeat approved release samples on the final packaged build, including import of real existing U1 3MF projects. Record results and attach photographs/measurements where useful.

Failures block production release. Untested firmware/service combinations stay provisional. No CI workflow is allowed to execute these hardware steps.
