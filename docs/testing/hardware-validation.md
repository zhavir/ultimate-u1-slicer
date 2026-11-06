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


## Software completion before hardware handoff (2026-11-06)

The product targets Snapmaker U1 only. The user will provide the printer after the complete in-scope software implementation is connected and passes offline checks. Hardware availability is not a prerequisite for porting available Snapmaker source. This plan does not authorize any printer operation.

Before requesting that handoff, reconcile all 72 audit groups against source, native UI, protocol/runtime dependencies, packaging and migration. No Missing, Incompatible, or Unknown implementation may be presented as code-complete. For each remaining Partial group, identify whether software is genuinely unfinished or only named hardware behavior is unverified; copied files or generic Moonraker substitutes do not satisfy this gate. Optional upstream additions must not postpone stock Snapmaker U1 compatibility.

Prepare a per-feature execution sheet for the following hardware checks. Every row needs the exact application/firmware revision, installed services, profiles/nozzles/materials, authorized action, expected observations, actual result and evidence. Keep credentials out of the sheet.

| Feature | Hardware verification after software completion |
|---|---|
| Gateway and account | Launch/shutdown/reconnect isolation; discovery, login/logout and pairing; no interference with another installed slicer |
| Device connection | Stock and Extended Firmware identity, capabilities, temperature/job/progress status and reconnect behavior |
| Camera | Authenticated live stream start/stop/reconnect, privacy behavior and supported timelapse retrieval |
| RFID and inventory | Real tag metadata, refresh, empty/unknown spool behavior, four physical slots and logical job mapping |
| Feeders | Operator-authorized feed/unload, runout and interrupted operation; optional MultiACE only when installed and advertised |
| Cover and sensors | Confirm the exact installed sensor/cover variant, reported state and firmware protection behavior without bypassing safeguards |
| Hotends and nozzles | Per-head installed diameter/high-flow detection, mismatch warnings and applicable profile selection |
| Project and slicing | Original Snapmaker projects preserve assignments/settings; inspect generated commands before submitting |
| Single/four-tool printing | Separately approved small prints, docking, purge/prime tower, temperatures, feeder state and material consumption |
| Advanced slicing | Mixed nozzles, support transitions, Full Spectrum and Color Patch only after their offline implementation checks pass |
| Failures and cancellation | Authorized upload/start/cancel boundaries; disconnect/reconnect and safe error reporting without suppressing printer protections |

A passed offline suite marks only its named software behavior Verified. Physical behavior remains unverified until the corresponding supervised check passes; production release still requires the complete hardware record.
