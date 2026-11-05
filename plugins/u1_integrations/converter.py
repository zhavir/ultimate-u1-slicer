"""Independent AGPL connector to a separately installed noncommercial converter.

No thadius83 converter code, rule files, profiles or service binaries are bundled.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
import uuid

from .common import AuthorizedFiles, BoundaryError, MAX_INPUT, MAX_OUTPUT, check_3mf, object_args, write_new

CONVERTER_SHA = "630bc8a92eb128464be14cc5a94838e4e2d2a101"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise BoundaryError("Converter redirects are not allowed")


class LocalConverter:
    def __init__(self, endpoint):
        if not isinstance(endpoint, str):
            raise BoundaryError("A loopback HTTP service URL is required")
        try:
            parsed = urllib.parse.urlsplit(endpoint)
            port = parsed.port
        except ValueError as exc:
            raise BoundaryError("Invalid converter URL") from exc
        if (parsed.scheme != "http" or parsed.hostname not in ("127.0.0.1", "::1")
                or parsed.username or parsed.password or parsed.query or parsed.fragment
                or parsed.path not in ("", "/") or not port):
            raise BoundaryError("Use http://127.0.0.1:PORT or http://[::1]:PORT; remote hosts and URL credentials are disabled")
        self.url = endpoint.rstrip("/")
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def request(self, path, *, data=None, content_type=None, limit=1024 * 1024):
        headers = {"Accept": "application/json"}
        if content_type:
            headers["Content-Type"] = content_type
        req = urllib.request.Request(self.url + path, data=data, headers=headers)
        try:
            with self.opener.open(req, timeout=120) as response:
                payload = response.read(limit + 1)
                if len(payload) > limit:
                    raise BoundaryError("Converter response exceeds the size limit")
                return payload
        except urllib.error.URLError as exc:
            raise BoundaryError("Local converter service unavailable or request refused") from exc

    def profiles(self):
        profiles = json.loads(self.request("/api/profiles"))
        if not isinstance(profiles, list):
            raise BoundaryError("Unexpected converter profile response")
        return profiles


def list_profiles(args):
    object_args(args, ("endpoint",), ("endpoint",))
    return LocalConverter(args["endpoint"]).profiles()


def convert_project(args):
    object_args(args, ("endpoint", "path", "output", "reference_profile", "license_acknowledged"),
                ("endpoint", "path", "output", "reference_profile", "license_acknowledged"))
    if args["license_acknowledged"] is not True:
        raise BoundaryError("Confirm that your use of the separately installed service is permitted by its license")
    profile = args["reference_profile"]
    if not isinstance(profile, str) or not re.fullmatch(r"[\w .-]{1,160}", profile):
        raise BoundaryError("Invalid reference profile identifier")
    files = AuthorizedFiles()
    source, destination = files.path(args["path"]), files.path(args["output"], output=True)
    if source.suffix.lower() != ".3mf" or destination.suffix.lower() != ".3mf":
        raise BoundaryError("Conversion input and new output must use .3mf")
    service = LocalConverter(args["endpoint"])
    # Fixed fields match the audited service contract. No macros or arbitrary overrides.
    boundary = "u1" + uuid.uuid4().hex
    parts = []
    for name, value in {"reference_profile": profile, "apply_rules": "false", "clamp_speeds": "false",
                        "preserve_color_painting": "true", "insert_swap_pauses": "false"}.items():
        parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n').encode())
    with source.open("rb") as stream:
        source_bytes = stream.read(MAX_INPUT + 1)
    if len(source_bytes) > MAX_INPUT:
        raise BoundaryError("Input exceeds the upload limit")
    parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="input.3mf"\r\n'
                  'Content-Type: application/octet-stream\r\n\r\n').encode() + source_bytes + b"\r\n")
    body = b"".join(parts) + f"--{boundary}--\r\n".encode()
    job = json.loads(service.request("/api/convert", data=body, content_type=f"multipart/form-data; boundary={boundary}"))
    job_id = job.get("job_id") if isinstance(job, dict) else None
    if not isinstance(job_id, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,128}", job_id):
        raise BoundaryError("Invalid converter job identifier")
    converted = service.request("/api/download/" + job_id, limit=MAX_OUTPUT)
    check_3mf(converted)
    # Recheck authorization after the network request, and never replace an existing file.
    destination = AuthorizedFiles().path(str(destination), output=True)
    write_new(destination, converted)
    return {"output": str(destination), "diff": job.get("diff"), "requires_reslicing": True,
            "printer_contacted": False, "hardware_verified": False,
            "service_contract_sha": CONVERTER_SHA,
            "warning": "External service output is not certified U1-compatible. Review its diff, inspect tool/material assignments and slice afresh before printing."}
