#!/usr/bin/env python3
"""Build deterministic, installable wheels; never fetch code or modify installed plugins."""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
VERSION = "0.1.0"
PACKAGES = {
    "u1_studio_plugin": ("studio", "Snapmaker Studio inspection"),
    "u1_bambu_converter_plugin": ("converter", "Bambu-to-U1 converter connector"),
}


def verify_snapshot():
    root = ROOT / "third_party/snapmaker-studio"
    source = json.loads((root / "SOURCE.json").read_text(encoding="utf-8"))
    actual = {str(p.relative_to(root)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(root.rglob("*")) if p.is_file() and p.name != "SOURCE.json"}
    if source["files"] != actual:
        raise ValueError("Studio snapshot differs from its audited source manifest")
    return root, source


def build(output):
    vendor, source = verify_snapshot()
    own = ROOT / "plugins/u1_integrations"
    output.mkdir(parents=True, exist_ok=True)
    built = []
    for package, (mode, title) in PACKAGES.items():
        files = {}
        for filename in ("common.py", mode + ".py"):
            files[f"{package}/{filename}"] = (own / filename).read_bytes()
        for src, dest in (("entry.py.in", "__init__.py"), ("ui.html", "ui.html")):
            text = (own / src).read_text(encoding="utf-8").replace("__MODE__", mode).replace("__TITLE__", title)
            files[f"{package}/{dest}"] = text.encode()
        if mode == "studio":
            for p in sorted((vendor / "snapstudio_core").rglob("*")):
                if p.is_file():
                    files[f"snapstudio_core/{p.relative_to(vendor / 'snapstudio_core').as_posix()}"] = p.read_bytes()
            for filename in ("LICENSE", "THIRD_PARTY_NOTICES.md", "SOURCE.json"):
                files[f"{package}/upstream/{filename}"] = (vendor / filename).read_bytes()
        dist = f"{package}-{VERSION}.dist-info"
        dependency = "Requires-Dist: lxml==6.1.3\n" if mode == "studio" else ""
        files[f"{dist}/METADATA"] = (f"Metadata-Version: 2.5\nName: {package}\nVersion: {VERSION}\n"
            f"Summary: {title}\nAuthor: Ultimate U1 contributors\nRequires-Python: >=3.13\n"
            f"Import-Name: {package}\nLicense: AGPL-3.0\n{dependency}\n"
            "Optional user-enabled integration. No printer controls. See bundled notices.\n").encode()
        files[f"{dist}/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: ultimate-u1\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
        files[f"{dist}/top_level.txt"] = (package + "\n").encode()
        files[f"{dist}/licenses/Ultimate-U1-LICENSE"] = (ROOT / "LICENSE.txt").read_text(encoding="utf-8").encode("utf-8")
        record = io.StringIO(newline="")
        writer = csv.writer(record, lineterminator="\n")
        for name, content in sorted(files.items()):
            digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).rstrip(b"=").decode()
            writer.writerow((name, "sha256=" + digest, len(content)))
        writer.writerow((f"{dist}/RECORD", "", ""))
        files[f"{dist}/RECORD"] = record.getvalue().encode()
        path = output / f"{package}-{VERSION}-py3-none-any.whl"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in sorted(files.items()):
                info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content)
        built.append({"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "mode": mode, "bundled_upstream_sha": source["sha"] if mode == "studio" else None})
    (output / "plugins.json").write_text(json.dumps({"schema": 1, "plugins": built}, indent=2) + "\n")
    return built


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "resources/u1_plugins")
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2))


if __name__ == "__main__":
    main()
