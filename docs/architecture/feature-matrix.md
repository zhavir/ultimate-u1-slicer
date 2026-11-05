# Feature matrix

Authoritative detailed audit: [functional parity](functional-parity-audit.md); machine-readable exact source/configuration evidence: [JSON](functional-parity.json).

Statuses are **Verified**, **Implemented but untested**, **Partial**, **Missing**, **Incompatible**, or **Unknown**. Verification is limited to the named executed test scope; it never implies physical U1 validation. Source presence or matching option names alone is insufficient.

| Feature | Status | Priority |
|---|---|---|
| [Material compatibility grouping](functional-parity-audit.md#tower-grouping) | Partial | P0 |
| [Interface pre-extrusion distance and length](functional-parity-audit.md#tower-preextrusion) | Implemented but untested | P0 |
| [Interface temperature and tool-change thermal waits](functional-parity-audit.md#tower-temperature) | Partial | P0 |
| [Cooling before tower and during interfaces](functional-parity-audit.md#tower-cooling) | Implemented but untested | P0 |
| [Tower ribs, wall gap, brim and chamfer](functional-parity-audit.md#tower-ribs) | Partial | P1 |
| [Special U1 tool-change and docking paths](functional-parity-audit.md#tower-toolpaths) | Partial | P0 |
| [Non-Bambu Type 1 tower material accounting](functional-parity-audit.md#tower-accounting) | Verified | P1 |
| [Transition layers, speed, flow and perimeters](functional-parity-audit.md#support-transitions) | Missing | P0 |
| [Minimum support-interface contact-area threshold](functional-parity-audit.md#support-contact) | Missing | P0 |
| [Snapmaker adaptive tree support layers](functional-parity-audit.md#support-adaptive) | Missing | P1 |
| [Top and bottom painting penetration controls](functional-parity-audit.md#painting-depth) | Implemented but untested | P1 |
| [Automatic negative raft/support expansion](functional-parity-audit.md#support-auto) | Incompatible | P0 |
| [Ratio mixing](functional-parity-audit.md#spectrum-ratio) | Partial | P1 |
| [Cycle and interleaved-layer mixing](functional-parity-audit.md#spectrum-cycle) | Partial | P1 |
| [Color Match and matching algorithms](functional-parity-audit.md#spectrum-match) | Partial | P1 |
| [Gradient curves and ranges](functional-parity-audit.md#spectrum-gradient) | Partial | P1 |
| [Color decomposition and component selection](functional-parity-audit.md#spectrum-decompose) | Implemented but untested | P1 |
| [Geometry subdivision and textured segmentation](functional-parity-audit.md#spectrum-subdivision) | Implemented but untested | P1 |
| [Advanced dithering, pointillism and local-Z modes](functional-parity-audit.md#spectrum-advanced) | Partial | P1 |
| [Color Patch shell/core geometry and loops](functional-parity-audit.md#fos-color-patch) | Missing | P1 |
| [Independent mixed nozzle configuration and mapping](functional-parity-audit.md#fos-nozzles) | Partial | P0 |
| [Per-nozzle wall, infill, support and tower widths](functional-parity-audit.md#fos-widths) | Partial | P1 |
| [Per-nozzle feature speeds and thermal constraints](functional-parity-audit.md#fos-speeds) | Missing | P1 |
| [Outer/inner wall and sparse/solid infill tool assignments](functional-parity-audit.md#fos-roles) | Partial | P0 |
| [Support/interface/prime-tower filament selection](functional-parity-audit.md#fos-support-tower) | Implemented but untested | P1 |
| [Per-object and per-filament overrides](functional-parity-audit.md#fos-object-overrides) | Partial | P1 |
| [Nozzle verification and incompatibility checks](functional-parity-audit.md#fos-nozzle-safety) | Partial | P0 |
| [Advisory filament/nozzle partition planner](functional-parity-audit.md#filament-planner) | Verified | P1 |
| [U1 LAN discovery and network submission](functional-parity-audit.md#u1-lan) | Partial | P0 |
| [Snapmaker gateway transport and device protocol](functional-parity-audit.md#u1-gateway) | Missing | P0 |
| [Snapmaker cloud account, pairing and authorization](functional-parity-audit.md#u1-cloud) | Missing | P0 |
| [Device status, job, progress and temperatures](functional-parity-audit.md#u1-status) | Partial | P0 |
| [U1 camera, authentication and streaming](functional-parity-audit.md#u1-camera) | Missing | P0 |
| [U1 RFID/NFC filament metadata and refresh](functional-parity-audit.md#u1-rfid) | Partial | P0 |
| [Filament inventory, assignments and synchronization](functional-parity-audit.md#u1-filaments) | Partial | P0 |
| [Automatic feeding and unloading](functional-parity-audit.md#u1-feeder) | Unknown | P0 |
| [MultiACE device integration](functional-parity-audit.md#u1-multiace) | Missing | P1 |
| [Top cover/door/enclosure capability and status](functional-parity-audit.md#u1-cover) | Unknown | P0 |
| [High-flow hotend detection and compatibility](functional-parity-audit.md#high-flow) | Partial | P0 |
| [Uniform 0.2 mm U1 profile](functional-parity-audit.md#nozzle-02) | Implemented but untested | P1 |
| [Uniform 0.4 mm U1 profile](functional-parity-audit.md#nozzle-04) | Verified | P0 |
| [Uniform 0.6 mm U1 profile](functional-parity-audit.md#nozzle-06) | Implemented but untested | P1 |
| [Uniform 0.8 mm U1 profile](functional-parity-audit.md#nozzle-08) | Implemented but untested | P1 |
| [Mixed 0.4+0.6 U1 profile and arbitrary head combinations](functional-parity-audit.md#nozzle-mixed) | Partial | P0 |
| [Printer wizard and selected-preset visibility](functional-parity-audit.md#profile-visibility) | Partial | P0 |
| [U1 machine start/end/tool-change macro preservation](functional-parity-audit.md#profile-macros) | Partial | P0 |
| [Attribution, inheritance, collisions and user overrides](functional-parity-audit.md#profile-sync) | Partial | P1 |
| [Original Snapmaker 3MF import and configuration migration](functional-parity-audit.md#project-migration) | Incompatible | P0 |
| [3MF save/export and metadata fidelity](functional-parity-audit.md#project-export) | Partial | P0 |
| [FOrca schema and object/filament metadata migration](functional-parity-audit.md#project-fos) | Missing | P0 |
| [Native protocol, authentication and stdio](functional-parity-audit.md#mcp-core) | Verified | P0 |
| [Move, rotate, scale, arrange and inspect](functional-parity-audit.md#mcp-transform) | Partial | P1 |
| [Slicing, estimates, consumption, warnings and export](functional-parity-audit.md#mcp-slicing) | Partial | P0 |
| [Open/import/create/save/export projects and files](functional-parity-audit.md#mcp-project-files) | Partial | P0 |
| [Object/material/support/profile authoring](functional-parity-audit.md#mcp-settings) | Partial | P1 |
| [Duplicate/delete and destructive operation approval](functional-parity-audit.md#mcp-destruction) | Partial | P0 |
| [Authorized printer state, submission and controls](functional-parity-audit.md#mcp-printer) | Missing | P0 |
| [Stock U1 firmware API and G-code behavior](functional-parity-audit.md#firmware-stock) | Partial | P0 |
| [Extended Firmware 2.1 and optional services](functional-parity-audit.md#firmware-extended) | Partial | P0 |
| [Dynamic capability detection and explicit unknowns](functional-parity-audit.md#firmware-capabilities) | Partial | P0 |
| [Bundled plugin discovery, consent and installation](functional-parity-audit.md#plugins-discovery) | Partial | P0 |
| [Studio read-only project inspection and preflight](functional-parity-audit.md#plugin-studio) | Verified | P1 |
| [External converter connector and project-copy workflow](functional-parity-audit.md#plugin-converter) | Verified | P1 |
| [Windows-trusted Authenticode signatures](functional-parity-audit.md#windows-signing) | Partial | P0 |
| [Native macOS ARM64 application and packaging](functional-parity-audit.md#macos-build) | Unknown | P0 |
| [Physical single/four-tool/mixed-nozzle validation](functional-parity-audit.md#hardware-print) | Unknown | P0 |
| [Retained walls, infill, cooling, seams and G-code engine](functional-parity-audit.md#orca-engine) | Partial | P1 |
| [STL/STEP/3MF, modeling, painting and CAD](functional-parity-audit.md#orca-geometry) | Implemented but untested | P1 |
| [Calibration and process workflows](functional-parity-audit.md#orca-calibration) | Implemented but untested | P1 |
| [Integration changes, disabled features and default policies](functional-parity-audit.md#orca-gates) | Partial | P0 |
| [Detect and reconcile reported U1 high-flow hotends](functional-parity-audit.md#high-flow-detection) | Missing | P0 |

| [Snapmaker development cooling, infill margin and short-travel changes](functional-parity-audit.md#snapmaker-tip-cooling-motion) | Unknown | P1 |

The U1 catalog already contains uniform 0.2/0.4/0.6/0.8 mm and mixed 0.4+0.6 mm profiles. Installed/selected printer variants determine dropdown visibility; these entries are not all physically calibrated here. A 0.4+0.6-only selection is not evidence of a FOrca hardware limit.

No stable or 100% U1-compatible release is certified. Camera/gateway/pairing/feeding, complete FOrca/Full Spectrum migrations, original-project support semantics, native macOS packaging and physical tests remain separate gates. Windows-trusted signing additionally needs a real signing identity.
