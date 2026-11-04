# Imported-source attribution

`src/libslic3r/FosFilamentArrangement.{hpp,cpp}` are imported unchanged from jiyang1018/FOrcaSlicer at 0b1f80cd22793785d8ae5c4296d2fe4a9248bd21 (AGPL-3.0 root LICENSE.txt). Their comments attribute the swap model to multiACE optimizers. The U1 adapter bounds and validates inputs before invoking this pure calculation. Physical head binding, background unloads, material compatibility and extrusion-time estimates are not implemented by that adapter.

The complete official native MCP implementation comes from OrcaSlicer feature/mcp at 17a745e30c248cf3acb4c429b650b22d106fd19a, under the inherited AGPL-3.0 license and history. Local changes add protocol validation fixes, the U1 slicer-only allowlist, file-root policy and the advisory planner registration. Do not claim this is a newly written MCP implementation.

Profile review snapshots are generated locally and ignored by Git. Separate Snapmaker profile redistribution is blocked because the pinned source lacks a license file. No firmware, SSH credentials, proprietary plugin binary or RFID identifier is imported.
