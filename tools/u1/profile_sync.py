#!/usr/bin/env python3
"""Build an attributed, immutable review catalog; never install or rewrite presets."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile

LISTS = {"machine_model_list": "machine_model", "machine_list": "machine",
         "filament_list": "filament", "process_list": "process"}


def read_json(path: Path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def safe_file(root: Path, relative: str) -> Path:
    root = root.resolve()
    p = PurePosixPath(relative)
    if p.is_absolute() or ".." in p.parts or "\\" in relative or not p.parts:
        raise ValueError(f"unsafe profile path: {relative!r}")
    candidate = root / relative
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"profile escapes source tree: {relative!r}")
    if any(parent.is_symlink() for parent in [candidate, *candidate.parents]
           if parent.is_relative_to(root)):
        raise ValueError(f"symlink in profile source: {relative!r}")
    if not candidate.is_file():
        raise ValueError(f"missing profile file: {candidate}")
    return candidate


def inventory(profiles: Path, vendors: list[str]) -> tuple[list[dict], dict[str, bytes]]:
    """Validate indexed identities and scoped inheritance without changing source bytes."""
    records, files = [], {}
    for vendor in sorted(set(vendors)):
        if not vendor or not vendor.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"invalid vendor id {vendor!r}")
        index_path = safe_file(profiles, vendor + ".json")
        index = read_json(index_path)
        if not isinstance(index, dict) or not isinstance(index.get("version"), str):
            raise ValueError(f"invalid bundle index: {index_path}")
        files[vendor + ".json"] = index_path.read_bytes()
        for list_name, kind in LISTS.items():
            entries = index.get(list_name, [])
            if not isinstance(entries, list):
                raise ValueError(f"{vendor}: {list_name} must be an array")
            for entry in entries:
                if not isinstance(entry, dict) or not isinstance(entry.get("sub_path"), str):
                    raise ValueError(f"{vendor}: invalid index entry")
                relative = vendor + "/" + entry["sub_path"]
                path = safe_file(profiles, relative)
                preset = read_json(path)
                if not isinstance(preset, dict) or preset.get("name") != entry.get("name"):
                    raise ValueError(f"{relative}: indexed and embedded names differ")
                # Some inherited system bases omit type; their index provides the kind.
                if "type" in preset and preset["type"] != kind:
                    raise ValueError(f"{relative}: expected type {kind}")
                data = path.read_bytes()
                key = (vendor, kind, preset["name"])
                previous = next((r for r in records if r["identity"] == list(key)), None)
                if previous:
                    if previous["path"] != relative or previous["sha256"] != hashlib.sha256(data).hexdigest():
                        raise ValueError(f"conflicting duplicate preset identity: {key}")
                    previous["index_occurrences"] += 1
                    continue
                files[relative] = data
                records.append({"identity": list(key), "path": relative,
                                "sha256": hashlib.sha256(data).hexdigest(),
                                "index_occurrences": 1,
                                "inherits": preset.get("inherits", ""),
                                "include": preset.get("include", []),
                                "u1_validation": "unvalidated",
                                "schema_validation": "structure-and-inheritance-only"})
        # Preserve textures, models and auxiliary JSON too. Indexed profiles retain original names.
        for path in sorted((profiles / vendor).rglob("*")):
            if path.is_symlink():
                raise ValueError(f"symlink in vendor tree: {path}")
            if path.is_file():
                rel = path.relative_to(profiles).as_posix()
                files[rel] = safe_file(profiles, rel).read_bytes()
    by_key = {tuple(r["identity"]): r for r in records}
    visiting, visited = set(), set()

    def visit(key):
        if key in visiting:
            raise ValueError(f"inheritance/include cycle at {key}")
        if key in visited:
            return
        visiting.add(key)
        record = by_key[key]
        includes = record["include"]
        if isinstance(includes, str):
            includes = [includes]
        if not isinstance(includes, list) or any(not isinstance(v, str) for v in includes):
            raise ValueError(f"invalid include list: {key}")
        parents = ([record["inherits"]] if record["inherits"] else []) + includes
        for name in parents:
            if not isinstance(name, str):
                raise ValueError(f"invalid parent name: {key}")
            parent = (key[0], key[1], name)
            if parent not in by_key and key[1] == "filament":
                parent = ("OrcaFilamentLibrary", "filament", name)
            if parent not in by_key:
                raise ValueError(f"unresolved parent/include {name!r} for {key}")
            visit(parent)
        visiting.remove(key)
        visited.add(key)

    for key in by_key:
        visit(key)
    return records, files


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def synchronize(checkouts: dict[str, Path], destination: Path, lock: dict,
                vendors: list[str]) -> dict:
    destination = destination.absolute()
    # The caller explicitly names a new managed catalog, not a slicer preset directory.
    if destination.is_symlink():
        raise ValueError("catalog must not be a symlink")
    destination = destination.resolve()
    for source in checkouts.values():
        if destination.is_relative_to(source.resolve()) or source.resolve().is_relative_to(destination):
            raise ValueError("catalog and source checkouts must be separate")
    marker = destination / ".ultimate-u1-catalog"
    if marker.is_symlink():
        raise ValueError("catalog marker must not be a symlink")
    if destination.exists() and not marker.is_file() and any(destination.iterdir()):
        raise ValueError("refusing a non-empty directory that is not an Ultimate U1 catalog")
    staged = []
    # Validate every input before any catalog writes.
    for alias, repo in sorted(checkouts.items()):
        expected = lock["sources"].get(alias)
        if expected is None:
            raise ValueError(f"unknown source {alias}")
        sha = git(repo, "rev-parse", "HEAD")
        if sha != expected["sha"]:
            raise ValueError(f"{alias}: checkout SHA differs from sources.lock.json")
        if git(repo, "status", "--porcelain", "--untracked-files=all", "--", "resources/profiles"):
            raise ValueError(f"{alias}: profile tree contains local changes")
        profiles_relative = expected.get("profiles_path", "resources/profiles")
        profiles = repo / profiles_relative
        if not profiles.resolve().is_relative_to(repo.resolve()):
            raise ValueError("profile root escapes checkout")
        if git(repo, "status", "--porcelain", "--untracked-files=all", "--", profiles_relative):
            raise ValueError(f"{alias}: profile tree contains local changes")
        selected = [v for v in vendors if (profiles / (v + ".json")).is_file()]
        if not selected:
            raise ValueError(f"{alias}: none of the requested vendors exist")
        records, files = inventory(profiles, selected)
        staged.append((alias, sha, expected, records, files))
    destination.mkdir(parents=True, exist_ok=True)
    marker.touch(exist_ok=True)
    snapshots = destination / "sources"
    snapshots.mkdir(exist_ok=True)
    if snapshots.is_symlink():
        raise ValueError("catalog sources directory is a symlink")
    current = {"format": 1, "sources": {}, "collisions": [], "duplicates": [],
               "installed": False, "u1_validation": "unvalidated"}
    identities, digests = {}, {}
    for alias, sha, expected, records, files in staged:
        snapshot_name = alias + "-" + sha
        target = snapshots / snapshot_name
        manifest = {"source": alias, "url": expected["url"], "sha": sha,
                    "license": expected["license"], "profiles": records,
                    "files": {p: hashlib.sha256(b).hexdigest() for p, b in sorted(files.items())}}
        if target.exists() or target.is_symlink():
            if target.is_symlink() or read_json(target / "manifest.json") != manifest:
                raise ValueError(f"existing immutable snapshot differs: {target}")
            for rel, digest in manifest["files"].items():
                if hashlib.sha256(safe_file(target / "profiles", rel).read_bytes()).hexdigest() != digest:
                    raise ValueError(f"immutable snapshot was modified: {target / rel}")
        else:
            with tempfile.TemporaryDirectory(prefix=".stage-", dir=snapshots) as temporary:
                temp = Path(temporary)
                for rel, data in files.items():
                    path = temp / "profiles" / rel
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
                (temp / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
                os.replace(temp, target)
        current["sources"][alias] = {"snapshot": "sources/" + snapshot_name, "sha": sha,
                                      "profile_count": len(records)}
        for record in records:
            name = tuple(record["identity"])
            qualified = alias + "/" + "/".join(name)
            if name in identities:
                current["collisions"].append([identities[name], qualified])
            else:
                identities[name] = qualified
            digest = record["sha256"]
            if digest in digests:
                current["duplicates"].append([digests[digest], qualified])
            else:
                digests[digest] = qualified
    # Overrides are intentionally never read, copied or written by this tool.
    handle, name = tempfile.mkstemp(prefix=".current-", dir=destination)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as output:
            json.dump(current, output, indent=2)
            output.write("\n")
        os.replace(name, destination / "current.json")
    finally:
        Path(name).unlink(missing_ok=True)
    return current


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, metavar="NAME=CHECKOUT")
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--lock", type=Path, default=Path(__file__).with_name("sources.lock.json"))
    parser.add_argument("--vendor", action="append", help="default: Snapmaker and OrcaFilamentLibrary")
    args = parser.parse_args()
    sources = {}
    for item in args.source:
        alias, separator, path = item.partition("=")
        if not separator or alias in sources:
            parser.error("each source must be a unique NAME=CHECKOUT")
        sources[alias] = Path(path).resolve()
    try:
        result = synchronize(sources, args.destination, read_json(args.lock),
                             args.vendor or ["Snapmaker", "OrcaFilamentLibrary"])
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps({"sources": result["sources"], "collisions": len(result["collisions"]),
                      "duplicates": len(result["duplicates"]), "installed": False}, indent=2))


if __name__ == "__main__":
    main()
