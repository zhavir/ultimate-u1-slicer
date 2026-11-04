# ADR-001: Official Orca integration baseline with an explicit U1 patch queue

Status: accepted for an experimental integration branch; stable-release acceptance remains blocked by U1 regression gates.

Executed checkpoint: the Linux application links, shipped-profile cube slicing and native GUI MCP slicing pass, and synthetic mixed 0.4/0.6 mm paths preserve per-head widths. Original Snapmaker v2.4.1 projects are rejected on automatic raft/support expansion -1. That semantic migration is a release blocker, not a reason to clamp the value. These results support retaining the experimental baseline while measuring the remaining support/gateway/FOrca port burden; they do not establish U1 parity or make this a stable architecture acceptance.

## Decision

Use official OrcaSlicer `feature/mcp` at 17a745e30c248cf3acb4c429b650b22d106fd19a, based on the audited official main, as the starting integration source. Keep upstream's native server, GUI lifecycle, tests, transport and dependency management together. Track official main and Snapmaker independently. Import isolated, attributed FOrca code where compatible; do not merge whole forks to resolve a feature request.

## Alternatives

| Architecture | Implementation effort | U1 strength now | MCP effort | Divergence / profile risk | Regression risk | Maintenance / builds |
|---|---|---|---|---|---|---|
| A. Snapmaker main | Low initial U1 setup; high ongoing upstream port effort | Strongest current gateway, feeding and paired-device workflows | High: current native MCP spans 325 files and modern UI/plugin dependencies | 674/7452 divergent commits; pinned separate profiles | Lower initial stock U1 risk; large MCP port risk | Must maintain both deep GUI and engine forks; Linux/macOS/Windows scripts present |
| B. FOrca main | Lowest cost for Color Patch and mixed-nozzle authoring | Existing advanced U1 paths, but a research preview; behind current Snapmaker gateway/high-flow work | Highest: forward-port modern UI lifecycle and MCP across older engine/schema | 203 commits unique relative to Snapmaker, 1551 changed paths; FOS-specific options | Color Patch and login issue reports; no independent hardware validation | Must carry advanced engine changes plus Snapmaker and official ports; platform workflows present |
| C. Official main plus MCP branch and U1 adapters | High initial U1 parity work | Existing U1 agent/profiles; gateway/feeding parity incomplete | Lowest: use whole official implementation | Thin own patch queue; incompatible FOS schema needs explicit migration | U1 release blocked until adapters and project/G-code tests pass | Lowest expected long-term MCP/engine maintenance; established platform CI |
| D. Separate slicing engines behind a new GUI/server | Very high | Potentially retains outputs but projects/settings drift between engines | New abstraction and duplicate lifecycle | Multiple schemas and duplicate security surfaces | Highest integration uncertainty | Highest build/dependency/testing burden; rejected |

No numeric cost score is invented. The recommendation is based on the inspected source boundaries and graph counts. It is not a claim that the chosen baseline already has the strongest U1 feature parity. C requires the largest **explicit initial compatibility gate**, but avoids permanently maintaining a large backport of a rapidly developing official automation stack. B is retained as the behavioral reference for advanced slicing, A for stock U1 connectivity.

## Consequences and release rule

The current source is experimental. Snapmaker pairing/gateway/feeding, FOrca Color Patch, full per-nozzle feature authoring, configuration migration, and physical printing are **not** marked complete. None may be silently replaced by generic Moonraker behavior. These gaps must close before a stable U1 release. If parity cannot be achieved without a larger and less maintainable patch set than A, revisit this ADR before release.

The first isolated FOrca import is its pure filament-partition optimizer, exposed as an advisory native MCP tool. It neither ports Color Patch nor applies a tool mapping. Keep source-specific profiles in read-only-source review catalogs with attribution, never flatten their inheritance into the official bundle. Do not ship presets whose redistribution license is unresolved.

The initial MCP exposure is a reviewed slicer-only allowlist. Unreviewed UI/action/script/plugin bridges, filesystem import/export and printer-control tools remain unavailable through the protocol until their authorization adapters are implemented. The underlying upstream implementation remains in source and the normal GUI remains available. This intentional restriction is documented, tested and a blocker for the requested complete MCP feature set.

The pins in sources.lock.json and local u1-baseline tag preserve comparison states, not a newly verified “known-good U1 release.” Snapmaker's published v2.4.1 remains the external stable reference; no Ultimate U1 stable branch or release exists yet.
