"""Shared opt-in plugin boundary; no printer-control or shell-execution APIs."""
from __future__ import annotations

import json
import os
from pathlib import Path
import queue
import zipfile

MAX_INPUT = 128 * 1024 * 1024
MAX_OUTPUT = 256 * 1024 * 1024


class BoundaryError(ValueError):
    pass


class AuthorizedFiles:
    """Roots come from the operator's launch environment, never plugin arguments."""

    def __init__(self):
        try:
            roots = json.loads(os.environ.get("U1_MCP_ALLOWED_ROOTS", "[]"))
        except (ValueError, TypeError) as exc:
            raise BoundaryError("U1_MCP_ALLOWED_ROOTS must be a JSON array of directories") from exc
        if not isinstance(roots, list) or any(not isinstance(p, str) for p in roots):
            raise BoundaryError("U1_MCP_ALLOWED_ROOTS must be a JSON array of directories")
        self.roots = []
        for raw in roots:
            p = Path(raw)
            if not p.is_absolute() or not p.is_dir():
                raise BoundaryError("Every authorized root must be an existing absolute directory")
            self.roots.append(p.resolve(strict=True))

    def path(self, raw, *, output=False):
        if not isinstance(raw, str) or not raw or len(raw) > 32768:
            raise BoundaryError("An absolute file path is required")
        p = Path(raw)
        if not p.is_absolute() or ".." in p.parts:
            raise BoundaryError("Paths must be absolute and contain no parent traversal")
        resolved = p.resolve(strict=not output)
        if not any(resolved.is_relative_to(root) for root in self.roots):
            raise BoundaryError("Directory not authorized: set U1_MCP_ALLOWED_ROOTS before launching the slicer")
        if output:
            if p.is_symlink() or p.exists() or not p.parent.is_dir():
                raise BoundaryError("Choose a new file in an existing authorized directory; overwriting is disabled")
        elif not p.is_file() or p.stat().st_size > MAX_INPUT:
            raise BoundaryError("Input must be a file no larger than 128 MiB")
        return resolved


def object_args(args, allowed, required=()):
    if not isinstance(args, dict) or set(args) - set(allowed) or any(k not in args for k in required):
        raise BoundaryError("Invalid plugin arguments")
    return args


def check_3mf(data):
    """Check a returned container without extracting or executing its contents."""
    import io
    from pathlib import PurePosixPath, PureWindowsPath

    if not data or len(data) > MAX_OUTPUT:
        raise BoundaryError("Converted project exceeds the download limit")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            if len(entries) > 10000 or sum(e.file_size for e in entries) > 1024**3:
                raise BoundaryError("Converted archive exceeds its expanded size/member budget")
            names = set()
            for entry in entries:
                name = entry.filename
                posix, windows = PurePosixPath(name), PureWindowsPath(name)
                if (name in names or posix.is_absolute() or windows.drive or windows.root
                        or ".." in posix.parts or ".." in windows.parts or entry.flag_bits & 1):
                    raise BoundaryError("Unsafe converted archive entry")
                names.add(name)
            if "[Content_Types].xml" not in names or "Metadata/project_settings.config" not in names:
                raise BoundaryError("Service did not return an Orca-family project")
            if archive.testzip() is not None:
                raise BoundaryError("Converted archive failed its CRC check")
    except zipfile.BadZipFile as exc:
        raise BoundaryError("Service did not return a valid 3MF archive") from exc


def write_new(path, data):
    """Exclusive creation preserves an existing project even if it appears mid-request."""
    import os

    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def launch_window(title, html, dispatch):
    """Native Script capability worker does I/O; WebView callbacks only enqueue."""
    import orca

    pending = queue.Queue(maxsize=1)

    def receive(payload):
        try:
            pending.put_nowait(payload)
        except queue.Full:
            pass

    window = orca.host.ui.create_window(html, title=title, width=880, height=720, on_message=receive)
    while window.is_open():
        try:
            payload = pending.get(timeout=0.2)
        except queue.Empty:
            continue
        try:
            result = dispatch(payload)
            message = {"ok": True, "result": result}
        except Exception as exc:
            message = {"ok": False, "error": str(exc)}
        if window.is_open():
            window.post(message)
    return orca.ExecutionResult.success()
