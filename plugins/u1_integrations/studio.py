"""Reviewed read-only adapter for the pinned MIT Snapmaker Studio core."""
from __future__ import annotations

import json
from .common import AuthorizedFiles, BoundaryError, object_args

STUDIO_SHA = "6d2e7f0485bfb7fa24caa9a58a4bd5fd37431222"


def inspect_project(args):
    object_args(args, ("path", "printer_snapshot"), ("path",))
    path = AuthorizedFiles().path(args["path"])
    if path.suffix.lower() not in (".3mf", ".stl"):
        raise BoundaryError("Studio inspection supports 3MF and STL")
    snapshot = args.get("printer_snapshot", {})
    if not isinstance(snapshot, dict) or len(json.dumps(snapshot)) > 1024 * 1024:
        raise BoundaryError("printer_snapshot must be an object no larger than 1 MiB")
    from pathlib import Path
    import snapstudio_core
    expected = Path(__file__).resolve().parent.parent / "snapstudio_core"
    if Path(snapstudio_core.__file__).resolve().parent != expected:
        raise BoundaryError("Another plugin loaded a different Studio core; unload it and restart before using this pinned integration")
    from snapstudio_core import preflight, project_traits

    traits = project_traits.extract(str(path))
    return {
        "source": {"project": "DVOpenLabs/snapmaker-studio", "sha": STUDIO_SHA},
        "traits": traits,
        "preflight": preflight.evaluate(traits, snapshot),
        "printer_contacted": False,
        "project_modified": False,
        "hardware_verified": False,
        "limitations": [
            "Printer facts are supplied snapshots, not a fresh hardware measurement.",
            "No automatic conversion rules, raft expansion clamp, or printer controls are exposed.",
            "Generic/reference profiles are not U1 calibrations.",
        ],
    }
