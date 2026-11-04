# Feature matrix

Statuses: **Implemented and verified** means the named local test passed for that scope; **Implemented but untested** means source exists without corresponding execution here; **Partially implemented** means a known subset exists; **Missing** is used only for an inspected, bounded absence; **Incompatible** means an identified schema/API conflict; **Unknown** means evidence is insufficient. Source inspection alone never qualifies as runtime verification. SnOrca is the Snapmaker column, not a separate fork.

| Capability | Snapmaker/SnOrca | FOrca | Official main / MCP branch | Ultimate U1 integration |
|---|---|---|---|---|
| Four independent U1 tools, filament assignment, tool-change G-code | Implemented but untested | Implemented but untested | Implemented but untested | Implemented but untested |
| U1 stock profiles | Implemented but untested (pinned submodule) | Implemented but untested | Implemented but untested | Implemented but untested (official profiles retained) |
| Mixed nozzle engine/schema | Partially implemented (no FOS per-feature model) | Implemented but untested | Implemented but untested (different generic schema) | Partially implemented; FOS project migration missing |
| Per-nozzle wall/infill/support/tower widths and speeds | Unknown parity | Implemented but untested (`fos_nozzle_*`, Print/GCode paths) | Unknown parity | Partially implemented; full FOS behavior not ported |
| Outer/inner wall and solid/sparse tool assignment | Partially implemented | Implemented but untested | Partially implemented | Partially implemented |
| Color Patch shell/core slicing | Unknown | Implemented but untested; issue #15 | Unknown parity with FullSpectrum/chromastack | Missing FOS Color Patch integration |
| Filament/nozzle partition planning | Unknown | Implemented but untested | Unknown | Implemented and verified (component tests); advisory MCP registration untested in GUI |
| Prime/purge tower | Implemented but untested | Implemented but untested | Implemented but untested | Implemented but untested; compare output required |
| Material compatibility and nozzle safety | Implemented but untested | Implemented but untested | Partially implemented | Unknown U1 parity; planner explicitly does not check materials |
| Automatic feeding / MultiACE hardware | Unknown complete behavior | Implemented but untested adapter | Unknown | Unknown; no hardware control imported |
| Snapmaker cloud pairing / gateway | Implemented but untested | Implemented but untested older implementation | Incompatible with current gateway architecture | Missing gateway parity adapter; release blocker |
| U1 LAN filament sync / NFC reads | Implemented but untested | Implemented but untested | Implemented but untested (`SnapmakerPrinterAgent`) | Implemented but untested |
| Network upload, status, temperatures, current job | Implemented but untested | Implemented but untested | Implemented but untested agent paths | Implemented but untested in GUI; blocked over MCP |
| Native MCP server | Missing in audited main | Missing in audited main | Missing in main; implemented but untested in feature/mcp | Partially implemented and restricted; whole official source present |
| MCP JSON-RPC validation / version negotiation | Missing server | Missing server | Implemented but untested | Implemented and verified in native component tests |
| MCP project open/save/export | Missing server | Missing server | Implemented but untested on branch | Partially implemented; upstream handlers present but denied by U1 allowlist pending authorization adapters |
| MCP model transform/arrange/slice/inspect | Missing server | Missing server | Implemented but untested on branch | Implemented but untested in running GUI |
| MCP settings/support/material authoring | Missing server | Missing server | Implemented but untested on branch | Partially implemented; restricted until review |
| MCP loopback/bearer/DNS rebinding defenses | Missing server | Missing server | Implemented but untested (`McpHttpServer`) | Implemented but untested at live transport level |
| MCP authorized file roots | Missing server | Missing server | Partially implemented (absolute paths/overwrite checks) | Implemented and verified policy; GUI path wiring untested; no filesystem tools exposed yet |
| MCP printer actions and macro authorization | Missing server | Missing server | Unknown broad UI/plugin reach | Partially implemented: denied by tested default policy; explicit approval adapter missing |
| Profile immutable sync, duplicates, inheritance | Unknown | Unknown | Existing profile tooling, not this cross-source catalog | Implemented and verified for local catalog scope; no automatic installation |
| Imported profile calibration / full ConfigDef schema validation | Unknown | Unknown | Existing validation tools | Unknown calibration; partial structural validation only |
| FOS configuration migration into official schema | Not applicable | Own schema | Incompatible without explicit adapter | Missing; release blocker |
| Official / Extended 2.1.0 capability negotiation | Unknown exact installation | Unknown exact installation | Generic agent support | Partially designed; live detection and firmware fixtures missing |
| RFID writing / identifier fabrication / auth bypass | Unknown | Unknown | Unknown | Unsupported and not implemented |
| macOS ARM64 application build | Workflows/source only | Workflows/source only | Workflows/source only | Unverified; no macOS runner here |
| Single/four-tool/mixed-nozzle/Color Patch output regressions | Not run | Not run | Not run | Missing executed integration results |
| Physical printing | Not tested here | Not tested here | Not tested here | Unknown, explicitly provisional |

Detailed source locations, known reports and pins: [repository audit](repository-audit.md). Actual executed checks and failures: [local validation](../testing/local-validation.md). A stable release requires all relevant definition-of-done gates in [roadmap](../roadmap.md), not just green component tests.
