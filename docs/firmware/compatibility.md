# Firmware compatibility

No printer was queried or controlled. Official U1 and Extended Firmware support are targets, not physically verified claims. The inspected Extended Firmware develop pin is in sources.lock.json. Its release sample contains stable v2.0.0-paxx12-24 and rolling 2.1.0 development assets. “Target 2.1.0” does not mean every user has a stable 2.1.0 release or identical installed services.

## Ownership and capability detection

Keep stock Snapmaker gateway/pairing and generic Moonraker adapters separate. Official Orca's SnapmakerPrinterAgent reads print_task_config and optional filament_detect data via Moonraker-style object queries. Network status/upload comes from MoonrakerPrinterAgent. Snapmaker's newer GatewayAccount/Device/Protocol/Service stack also carries vendor behavior that is not ported yet. Automatic feeding and pairing parity must pass vendor-specific tests before release.

A future read-only handshake must obtain server info, available objects and reported configuration. Detect `print_stats`, temperature objects, `print_task_config`, `filament_detect`, per-extruder objects and explicitly known macros individually. Distinguish unavailable, unauthorized, offline, unconfigured and unsupported. Neither firmware string matching nor “Moonraker exists” authorizes a macro or proves four-tool semantics. Unknown services remain unavailable; do not SSH into a printer to discover them.

## Optional components

Extended Firmware includes source/docs for multiACE, Fluidd/Mainsail-related components, HelixScreen and OpenRFID. These are installation-dependent. HelixScreen and browser UIs are presentation clients, not replacement printer APIs. MultiACE topology/capacity requires an explicit reported or operator-declared capability. The imported planner accepts declared ACE flags but does not detect hardware or send commands.

RFID overlays include NTAG215/NDEF support, card-type/UID metadata and filament-detect endpoint changes. `docs/design/rfid.md` and the actual parser/patches are source evidence. No tag writes, identifier fabrication or authentication bypass is implemented. A safe future metadata adapter must use documented public metadata, preserve provenance, validate types/units and require explicit authorization for writes. Protocol compatibility and installed service capabilities remain unverified.

Missing release tests: captured stock/Extended response fixtures, optional-object absence, authentication errors, malformed arrays, tool-index conventions, disconnect/reconnect, filament sync, safe upload without start, and operator-approved physical prints. No firmware upgrade or hardware test runs automatically.

## Stock source contracts verified during this checkpoint

Additional shallow source clones were inspected at Snapmaker/u1-klipper 7ac453b50fe6779b2ec0b759038a17da5e6d671d, u1-moonraker ed7b3752a9a938c87ee086f3b7b21a9352a2a0c9 and u1-fluidd 727005d55885dedddb67e69cb7881b0a8dfd0544 (all declare GPL-3.0). They are research inputs, not firmware flashed or code linked into the slicer.

In stock Klipper, extras/print_task_config.py distinguishes four physical extruders and 32 logical slots. Its extruder_map_table and material arrays must not be treated as interchangeable head lists. kinematics/extruder.py maps T/M104/M109 indices through print_task_config by default, with A0 bypassing that mapping. toolhead.py provides SWITCH_OF_EXTENDED_EXTRUDER INDEX for logical indices beyond the physical selectors. These are source-observed contracts, not evidence that every installed firmware version behaves identically.

The offline gcode_check.py accepts these semantics only when a capability fixture explicitly supplies snapmaker_a_parameter and the actual job's logical_to_physical table. It checks physical heater bounds after mapping and recognizes extended selection only when that command is declared. It never invents a map from a version string, executes a macro or approves a physical print. Generic direct-four-tool fixtures remain a separate mode.

Stock filament_detect.py exposes read-only status info/state/config, while Extended Firmware's RFID patch adds a separate filament_detect/set endpoint. Stock print_task_config registers set_print_preferences and prevents map changes while printing/paused. Moonraker's components/klippy_connection.py forwards non-reserved Klipper endpoints, but that still requires the module to exist and authorization/services to be available on the actual installation. No endpoint writes or live capability probes were performed.

Extended Firmware's own multiACE documentation calls its integration experimental and rolling-only; HelixScreen is an optional on-demand UI replacement. Treat both as opt-in installed components, not guaranteed capabilities of every Extended Firmware printer.
