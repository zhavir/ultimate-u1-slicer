#!/usr/bin/env python3
"""Hash candidate artifacts without publishing or labeling them a stable release."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def create_manifest(artifacts: Path, output: Path):
    artifacts, output = artifacts.resolve(), output.resolve()
    if output.is_relative_to(artifacts) or artifacts.is_relative_to(output):
        raise ValueError("artifact and metadata directories must be separate")
    files = []
    for path in sorted(artifacts.rglob("*")):
        if path.is_symlink():
            raise ValueError("artifact directory contains a symlink")
        if path.is_file():
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            files.append({"path": path.relative_to(artifacts).as_posix(), "size": path.stat().st_size,
                          "sha256": digest.hexdigest()})
    if not files:
        raise ValueError("no artifacts to hash")
    root = Path(__file__).resolve().parents[2]
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    # This tool cannot certify that an arbitrary downloaded file was built from HEAD.
    metadata = {"project": "Ultimate U1 Slicer", "source_commit": sha, "status": "experimental-candidate",
                "artifact_provenance_verified": False, "hardware_verified": False,
                "release_gates": "See docs/roadmap.md; this manifest is not release approval", "files": files}
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (output / "SHA256SUMS").write_text("".join(f"{f['sha256']}  {f['path']}\n" for f in files))
    (output / "release-notes.md").write_text(
        f"# Ultimate U1 experimental candidate\n\nSource commit: {sha}\n\n"
        "Includes the official native MCP baseline and initial U1 integration patches. "
        "This candidate is not a stable release. Review docs/roadmap.md and the workflow test evidence. "
        "Snapmaker gateway parity, full FOrca feature integration, application/client regressions "
        "and supervised hardware validation remain release gates.\n")
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = create_manifest(args.artifacts, args.output)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(f"Hashed {len(result['files'])} candidate artifacts; no release was published")


if __name__ == "__main__":
    main()
