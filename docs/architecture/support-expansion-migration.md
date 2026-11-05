# Snapmaker first-layer support expansion migration

Status: source investigation only; no compatibility adapter implemented or tested. This remains an existing-project release gate.

The audited Snapmaker revision `f5fd7289ea067997181ee6c2cf15a98f58faba43` defines `raft_first_layer_expansion` with minimum/default `-1`; the selected official engine requires a nonnegative value and defaults to `2`. Original Snapmaker projects therefore fail validation before slicing. Merely accepting the number or replacing it with zero/two would change geometry.

| Path | Audited Snapmaker behavior | Current official implementation |
| --- | --- | --- |
| Normal support/raft | `Support/SupportCommon.cpp:403` resolves negative expansion to 2 mm before first-layer inflation. | `Support/SupportCommon.cpp` scales the configured nonnegative value directly. |
| Tree raft | `Support/TreeSupport.cpp:1612` expands the base footprint by a fixed 3 mm before generating the base raft layers, then applies the raw configured expansion on the first layer. Auto `-1` consequently insets that layer by 1 mm relative to the expanded base. | The raft footprint and first layer both depend on the configured expansion; this is a different construction. |
| Tree support without raft | `Support/TreeSupport.cpp:2386` combines the configured width with an automatic polygon-moment expansion derived from support speed and branch height, followed by collision-aware offsetting. | Separate `tree_support_brim_width` and `tree_support_auto_brim` settings select a branch-radius/height approximation before object avoidance. |

Snapmaker's additional `ExPolygon::map_moment_to_expansion` in `ExPolygon.cpp:603` uses polygon second moments, footprint extents, support height and speed. Positive-input results are bounded to 1–10 mm. This method is absent from the selected official engine. The helper's geometry dependencies and degenerate-footprint handling require review before import.

A reviewed migration must preserve both engines' existing positive-value behavior, retain source attribution, distinguish the source project semantics, and cover normal support, tree support, hybrid support and multi-layer raft footprints. Preserve the automatic value in saved projects instead of silently flattening it into a constant. Versioned compatibility settings or a narrowly scoped adapter require a separate implementation decision; no such setting currently exists.

Validation should load the original single/four-material Snapmaker reference projects unchanged, slice representative supported overhangs with automatic/zero/explicit expansion, inspect first/all-raft-layer footprints and collision clearance, and compare geometric invariants with the isolated reference application. Byte-for-byte output identity is not required. New geometry must not silently affect non-U1 projects or official-only support options. Hardware adhesion remains a separate supervised test.
