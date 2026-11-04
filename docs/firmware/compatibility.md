# Firmware compatibility

No printer was queried or controlled. Official U1 and Extended Firmware support are targets, not physically verified claims. The inspected Extended Firmware develop pin is in sources.lock.json. Its release sample contains stable v2.0.0-paxx12-24 and rolling 2.1.0 development assets. “Target 2.1.0” does not mean every user has a stable 2.1.0 release or identical installed services.

## Ownership and capability detection

Keep stock Snapmaker gateway/pairing and generic Moonraker adapters separate. Official Orca's SnapmakerPrinterAgent reads print_task_config and optional filament_detect data via Moonraker-style object queries. Network status/upload comes from MoonrakerPrinterAgent. Snapmaker's newer GatewayAccount/Device/Protocol/Service stack also carries vendor behavior that is not ported yet. Automatic feeding and pairing parity must pass vendor-specific tests before release.

A future read-only handshake must obtain server info, available objects and reported configuration. Detect `print_stats`, temperature objects, `print_task_config`, `filament_detect`, per-extruder objects and explicitly known macros individually. Distinguish unavailable, unauthorized, offline, unconfigured and unsupported. Neither firmware string matching nor “Moonraker exists” authorizes a macro or proves four-tool semantics. Unknown services remain unavailable; do not SSH into a printer to discover them.

## Optional components

Extended Firmware includes source/docs for multiACE, Fluidd/Mainsail-related components, HelixScreen and OpenRFID. These are installation-dependent. HelixScreen and browser UIs are presentation clients, not replacement printer APIs. MultiACE topology/capacity requires an explicit reported or operator-declared capability. The imported planner accepts declared ACE flags but does not detect hardware or send commands.

RFID overlays include NTAG215/NDEF support, card-type/UID metadata and filament-detect endpoint changes. `docs/design/rfid.md` and the actual parser/patches are source evidence. No tag writes, identifier fabrication or authentication bypass is implemented. A safe future metadata adapter must use documented public metadata, preserve provenance, validate types/units and require explicit authorization for writes. Protocol compatibility and installed service capabilities remain unverified.

Missing release tests: captured stock/Extended response fixtures, optional-object absence, authentication errors, malformed arrays, tool-index conventions, disconnect/reconnect, filament sync, safe upload without start, and operator-approved physical prints. No firmware upgrade or hardware test runs automatically.
