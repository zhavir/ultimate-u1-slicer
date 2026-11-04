#!/usr/bin/env python3
"""Create temporary, attributed CLI fixtures from indexed presets; do not install profiles."""
import argparse
import hashlib
import json
from pathlib import Path

from profile_sync import inventory, read_json, safe_file


def build_fixture(profiles, destination, machine, process, filament, tools=1):
    if tools not in (1, 4):
        raise ValueError("fixture tools must be 1 or 4")
    if destination.resolve().is_relative_to(profiles.resolve()):
        raise ValueError("fixture destination must be outside the source profiles")
    records, _ = inventory(profiles, ["Snapmaker", "OrcaFilamentLibrary"])
    by_key = {tuple(record["identity"]): record for record in records}

    def resolve(kind, name, vendor="Snapmaker"):
        key = (vendor, kind, name)
        if key not in by_key and kind == "filament":
            key = ("OrcaFilamentLibrary", kind, name)
        if key not in by_key:
            raise ValueError(f"indexed profile not found: {key}")
        record = by_key[key]
        value = read_json(safe_file(profiles, record["path"]))
        result = {}
        if record["inherits"]:
            result.update(resolve(kind, record["inherits"], key[0]))
        includes = record["include"]
        if isinstance(includes, str):
            includes = [includes]
        for parent in includes:
            result.update(resolve(kind, parent, key[0]))
        result.update(value)
        result.pop("inherits", None)
        result.pop("include", None)
        # Preserve system identity for the legacy CLI's compatibility check. "User"
        # without an inherits field produces an empty printer system name there.
        result.update({"type": kind, "from": "system"})
        return result

    presets = {"machine": resolve("machine", machine), "process": resolve("process", process),
               "filament": resolve("filament", filament)}
    # Legacy fork CLIs normalize each partial preset before merging it. In both audited forks,
    # wipe_tower_filament normalization dereferences nozzle_diameter even for a process preset.
    # Carry the selected machine's context into temporary inputs, without changing source presets.
    for kind in ("process", "filament"):
        presets[kind].setdefault("nozzle_diameter", presets["machine"]["nozzle_diameter"])
    # This is a controlled offline fixture, not promotion or calibration of the source preset.
    presets["process"]["post_process"] = []
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("fixture destination must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for kind, value in presets.items():
        data = (json.dumps(value, indent=2) + "\n").encode()
        path = destination / (kind + ".json")
        path.write_bytes(data)
        hashes[path.name] = hashlib.sha256(data).hexdigest()
    # A closed 5 mm cube, in positive bed coordinates. No network or printer operation.
    vertices = [(x, y, z) for z in (0, 5) for y in (10, 15) for x in (10, 15)]
    faces = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    lines = ["solid u1_reference_cube"]
    for a, b, c, d in faces:
        for triangle in [(a, b, c), (a, c, d)]:
            lines += ["facet normal 0 0 0", "outer loop"]
            lines += ["vertex " + " ".join(map(str, vertices[index])) for index in triangle]
            lines += ["endloop", "endfacet"]
    lines.append("endsolid u1_reference_cube")
    geometry = ("\n".join(lines) + "\n").encode()
    (destination / "cube.stl").write_bytes(geometry)
    hashes["cube.stl"] = hashlib.sha256(geometry).hexdigest()
    if tools == 4:
        for index, color in enumerate(("#FF0000", "#00FF00", "#0000FF", "#FFFFFF"), 1):
            value = dict(presets["filament"])
            value.update({"name": f"Offline reference material {index}", "default_filament_colour": [color]})
            data = (json.dumps(value, indent=2) + "\n").encode()
            for name, content in ((f"filament{index}.json", data), (f"cube{index}.stl", geometry)):
                (destination / name).write_bytes(content)
                hashes[name] = hashlib.sha256(content).hexdigest()
    manifest = {"source_profile_root": str(profiles), "source_presets": {"machine": machine, "process": process,
                "filament": filament}, "fixture_hashes": hashes, "profile_installation": False,
                "calibration_verified": False, "purpose": "offline reference slicing only",
                "tools": tools, "object_filament_ids": list(range(1, tools + 1))}
    manifest["cli_compatibility_adapter"] = (
        "flattened system identity retained; machine nozzle context supplied to legacy per-preset normalize_fdm"
    )
    (destination / "fixture-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--machine", required=True)
    parser.add_argument("--process", required=True)
    parser.add_argument("--filament", required=True)
    parser.add_argument("--tools", type=int, choices=(1, 4), default=1)
    args = parser.parse_args()
    try:
        build_fixture(args.profiles, args.destination, args.machine, args.process, args.filament, args.tools)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print("Created an offline CLI fixture; no profiles were installed or calibrated")


if __name__ == "__main__":
    main()
