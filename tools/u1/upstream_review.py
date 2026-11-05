#!/usr/bin/env python3
"""Produce a source-change review; do not merge, cherry-pick, push or contact a printer."""
import argparse
import json
from pathlib import Path
import re
import subprocess


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE).strip()


def subsystem(path):
    for prefix, category in [("backend/snapstudio_core/", "project-preflight-conversion"),
                             ("backend/snapstudio_api/", "companion-api"),
                             ("backend/", "project-conversion"),
                             ("plugins/", "plugin-integrations"),
                             ("src/slic3r/plugin/", "plugin-runtime"),
                             ("src/slic3r/GUI/Mcp/", "mcp"),
                             ("src/slic3r/GUI/Calibration", "calibration"),
                             ("src/slic3r/GUI/ExtrusionCalibration", "calibration"),
                             ("src/slic3r/GUI/Gizmos/", "model-painting-supports"),
                             ("src/slic3r/GUI/CAD/", "cad-modeling"),
                             ("src/libslic3r/Format/", "project-import-export"),
                             ("src/libslic3r/Arrange", "arrangement"),
                             ("src/libslic3r/ModelArrange", "arrangement"),
                             ("src/libslic3r/", "engine-schema-gcode"),
                             ("src/slic3r/Utils/", "connectivity"),
                             ("src/slic3r/GUI/", "ui-workflows"),
                             ("tests/", "regression-tests"),
                             ("resources/profiles", "profiles"), ("submodules/Profiles", "profiles"),
                             ("deps", "dependencies"), (".github/", "ci-release")]:
        if path.startswith(prefix):
            return category
    return "ui-build-other"


def review(root, lock, fetch=False, probe_merges=False):
    baseline = lock["sources"]["orca-mcp"]["sha"]
    own = set(git(root, "diff", "--name-only", baseline, "HEAD").splitlines())
    results = {}
    for alias, source in lock["sources"].items():
        if not re.fullmatch(r"[a-z0-9-]+", alias):
            raise ValueError("invalid source alias")
        url = source["url"]
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git", url):
            raise ValueError("source URL must be a public GitHub HTTPS Git URL without credentials")
        branch = source.get("branch", source.get("default_branch", "main"))
        ref = "refs/remotes/u1-" + alias + "/" + branch
        if fetch:
            subprocess.run(["git", "-C", str(root), "fetch", "--filter=blob:none", "--no-tags", url,
                            "+refs/heads/" + branch + ":" + ref], check=True)
            if subprocess.run(["git", "-C", str(root), "cat-file", "-e", source["sha"] + "^{commit}"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
                subprocess.run(["git", "-C", str(root), "fetch", "--filter=blob:none", "--no-tags", url,
                                source["sha"]], check=True)
        try:
            tip = git(root, "rev-parse", "--verify", ref)
            paths = git(root, "diff", "--name-only", "--no-renames", source["sha"], tip).splitlines()
            counts = {}
            for path in paths:
                key = subsystem(path)
                counts[key] = counts.get(key, 0) + 1
            commits = git(root, "log", "--format=%H %s", source["sha"] + ".." + tip).splitlines()
            results[alias] = {"baseline": source["sha"], "tip": tip, "subsystems": counts,
                              "potential_conflict_paths": sorted(own.intersection(paths)),
                              "commits": commits, "changed_paths": paths,
                              "source_integrated": False, "compatibility": "unverified"}
            if probe_merges and commits and alias in {"orca", "orca-mcp"}:
                # Git's merge-tree writes objects only. It does not change HEAD, the index,
                # source files or the running build. A clean textual merge is not API parity.
                probe = subprocess.run(["git", "-C", str(root), "merge-tree", "--write-tree", "--messages",
                                        "HEAD", tip], capture_output=True, text=True)
                results[alias]["textual_merge_probe"] = {
                    "status": "clean" if probe.returncode == 0 else "conflicts" if probe.returncode == 1 else "failed",
                    "exit_code": probe.returncode,
                    "output_excerpt": (probe.stdout + probe.stderr)[:8192],
                    "semantic_compatibility_verified": False,
                }
        except subprocess.CalledProcessError:
            if fetch:
                raise
            results[alias] = {"status": "unavailable locally; rerun with --fetch"}
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="fetch public sources before review")
    parser.add_argument("--probe-merges", action="store_true", help="probe official upstream textual merges without changing the worktree")
    parser.add_argument("--output", type=Path, default=Path("docs/architecture/upstream-review.json"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    lock = json.loads(Path(__file__).with_name("sources.lock.json").read_text())
    result = {"source_integration_performed": False, "application_tests_run": False,
              "sources": review(root, lock, args.fetch, args.probe_merges)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {args.output}; source integration and compatibility testing remain required")


if __name__ == "__main__":
    main()
