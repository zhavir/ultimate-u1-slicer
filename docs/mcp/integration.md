# Native MCP integration

The application uses the official native server in `src/slic3r/GUI/Mcp/`, not an external competing bridge. Its CMake source list, startup lifecycle, GUI preferences, stdio bridge and original tests remain together. The app identifies itself as `ultimate-u1-slicer` and uses an independent `UltimateU1Slicer` configuration key. The native Linux GUI server has passed an isolated live smoke test; no printer was contacted.

## Transport and clients

The official HTTP server binds 127.0.0.1, checks Host/Origin, accepts JSON POST /mcp and checks a bearer token. Default port is 13619. Its stdio bridge is a local client of the same server, not another slicer implementation. Prefer the existing Preferences > AI features > MCP connection setup when a full build is available. Do not copy a bearer token into source, test logs or documentation. Native client configuration generation still needs live testing with Codex and Claude Code; do not present a placeholder config as proven.

The protocol source supports 2026-07-28 stateless requests and legacy 2025-11-25 / 2025-06-18 initialization. The [current specification](https://modelcontextprotocol.io/specification/2026-07-28) was checked on 2026-11-04. Modern requests require matching `MCP-Protocol-Version`, `Mcp-Method` and, where relevant, `Mcp-Name` headers. Component tests verify current ping, legacy negotiation, malformed fields, extreme integer inputs and the default policy. The unchanged upstream HTTP suite also passed locally: 8 cases and 43 assertions, using only loopback test servers. The restricted shell could not bind sockets; the authorized local retry passed. A running Linux GUI additionally passed authentication, current discovery, legacy handshake, get_state, list_objects and the advisory planner. See ../testing/evidence/mcp-live-smoke.json. A subsequent STL fixture with shipped U1 presets passed MCP-driven slicing and returned estimates, and the live selection handler rejected an overflowing index. See ../testing/evidence/mcp-slice-smoke.json. Real Codex/Claude connections and stdio launch remain untested.

## Current U1 policy and gaps

The native application enables `ServerInfo::slicer_only`. Only reviewed typed slicer tools appear in tools/list: get_state, list_objects, select, transform, arrange, slice, cancel, get_preview, list_plates, wait, list_presets, u1_plan_filament_partition. Direct calls of excluded names and generic api_call/action/UI/Python/plugin escape hatches are refused by protocol policy. A plugin's read-only annotation does not grant access.

Open/create/save/export, settings mutation, screenshots, scripts, CAD and all printer actions are present in upstream source but deliberately unavailable over U1 MCP until their file, sensitive-setting, unsaved-project and operator-approval adapters are reviewed. This is a documented incomplete capability set, not full MCP parity. The normal GUI continues to provide its existing operations. Never work around the gate with synthetic clicks or macros.

Printing, heating, homing, arbitrary macros and printer-control actions are not exposed by the U1 protocol. Their future adapter must obtain explicit operator authorization bound to printer identity, project/G-code hash and action; a client-supplied `confirmed:true` is not sufficient. Credentials stay in the existing printer connection subsystem. Generic Moonraker does not stand in for Snapmaker pairing, feeder or NFC APIs.

## File authorization

MCP path helpers now use `FileAccessPolicy`. Default authorized output is the application's own MCP output directory. Additional roots must be supplied by the operator before startup via `U1_MCP_ALLOWED_ROOTS`, a JSON array of absolute directory paths. For example on POSIX: `U1_MCP_ALLOWED_ROOTS='["/absolute/project/folder"]'`. No tool may change this setting. Invalid configuration fails closed. Paths must be absolute; parent traversal, sibling-prefix matches and symlink escapes are denied.

This is a path authorization check, not an OS sandbox. It does not defeat a malicious local process replacing files between check and use. Filesystem MCP tools remain gated while that surface is reviewed. Optional Python stays disabled by upstream defaults and is not exposed by the U1 policy.

## FOrca advisory tool

`u1_plan_filament_partition` invokes imported `FosFilamentArrangement` through `U1FilamentPlan`. It accepts four nozzle diameters, zero-based filament-to-nozzle entries, bounded tool-change events and optional operator-declared per-head ACE flags. It rejects invalid indices, dimensions, non-finite diameters, unknown arguments and oversized searches. At most eight distinct filaments and 4096 events are accepted, with an additional combined placement/event work budget to keep requests bounded.

The result is a proposal requiring reslicing, not a command or physical head binding. The current adapter models only FOrca's inline swap stall cost; it does not pass extrusion volumes/speeds into the optimizer and must not be marketed as a total print-time estimator. Material compatibility is explicitly `not_checked`. GUI registration compiled and the tool passed in the actual Linux GUI MCP smoke test. This verifies the advisory operation, not physical hardware or FOrca feature parity.

## Reproduce a native smoke check

Launch the app in a dedicated datadir, then run `python3 tools/u1/mcp_smoke.py --discovery /task/datadir/mcp/server.json --output /task/report.json`. It accepts only an explicit loopback endpoint, disables proxy/redirect forwarding, reads the private discovery token without putting it into the report, waits for readiness and checks inspection/planning. The optional `--slice-current-project` also tests rejection of an overflowing selection and slices a trusted fixture already loaded by the operator. It never uploads G-code or starts printing. A modal safety dialog causes refusal; do not bypass it.
