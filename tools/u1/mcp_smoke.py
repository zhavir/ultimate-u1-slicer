#!/usr/bin/env python3
"""Inspect a task-isolated native MCP endpoint; optionally slice its operator-loaded test project."""
import argparse
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def smoke(discovery, slice_project=False):
    endpoint = discovery["url"]
    url = urlsplit(endpoint)
    if (url.scheme != "http" or url.hostname != "127.0.0.1" or not url.port or url.path != "/mcp"
            or url.username or url.password or url.query or url.fragment):
        raise ValueError("smoke test requires an explicit 127.0.0.1 HTTP /mcp endpoint")
    token = discovery["token"]
    if not isinstance(token, str) or not token or "\n" in token or "\r" in token:
        raise ValueError("invalid discovery token")
    opener = build_opener(ProxyHandler({}), NoRedirect())
    sequence = 0

    def call(method, params, authenticated=True, modern=True):
        nonlocal sequence
        sequence += 1
        params = dict(params)
        if modern:
            params["_meta"] = {"io.modelcontextprotocol/protocolVersion": "2026-07-28"}
        body = json.dumps({"jsonrpc": "2.0", "id": sequence, "method": method, "params": params}).encode()
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                   "MCP-Protocol-Version": "2026-07-28" if modern else "2025-11-25",
                   "Mcp-Method": method}
        if method == "tools/call":
            headers["Mcp-Name"] = params["name"]
        if authenticated:
            headers["Authorization"] = "Bearer " + token
        with opener.open(Request(endpoint, body, headers), timeout=55) as response:
            result = json.load(response)
        if "error" in result:
            raise ValueError("MCP returned a protocol error")
        return result["result"]

    try:
        call("ping", {}, authenticated=False)
    except HTTPError as error:
        if error.code != 401:
            raise ValueError("unexpected unauthenticated response") from None
    else:
        raise ValueError("endpoint accepted an unauthenticated request")
    initialized = call("initialize", {"protocolVersion": "2025-11-25", "capabilities": {},
                                     "clientInfo": {"name": "ultimate-u1-local-smoke", "version": "1"}}, modern=False)
    if initialized["serverInfo"]["name"] != "ultimate-u1-slicer":
        raise ValueError("endpoint is not Ultimate U1 Slicer")
    discovered = call("server/discover", {})
    if "2026-07-28" not in discovered["supportedVersions"]:
        raise ValueError("current MCP revision not supported")
    names = {tool["name"] for tool in call("tools/list", {})["tools"]}
    required = {"get_state", "list_objects", "u1_plan_filament_partition"}
    allowed = required | {"select", "transform", "arrange", "slice", "cancel", "get_preview", "list_plates",
                          "wait", "list_presets"}
    if not required.issubset(names) or names - allowed:
        raise ValueError("unexpected U1 tool catalog")
    call("tools/call", {"name": "wait", "arguments": {"for": "ready", "timeout_s": 45}})
    for name, arguments in [("get_state", {}), ("list_objects", {}),
                            ("u1_plan_filament_partition", {"events": [0, 1, 0, 1],
                             "nozzle_diameters": [0.4] * 4, "filament_nozzle": [0, 1]})]:
        result = call("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError", False):
            raise ValueError("read-only MCP tool failed: " + name + ": " +
                             "; ".join(item.get("text", "") for item in result.get("content", [])))
    slicing = None
    if slice_project:
        rejected = call("tools/call", {"name": "select", "arguments": {"objects": [4294967296]}})
        message = "; ".join(item.get("text", "") for item in rejected.get("content", []))
        if not rejected.get("isError", False) or "outside the supported integer range" not in message:
            raise ValueError("overflowing object index was not rejected before selection")
        def tool_data(result):
            if result.get("isError", False):
                raise ValueError("MCP-driven fixture slicing failed: " +
                                 "; ".join(item.get("text", "") for item in result.get("content", [])))
            return json.loads(result["content"][0]["text"])

        slicing = tool_data(call("tools/call", {"name": "slice", "arguments": {"plates": "current", "timeout_s": 45}}))
        for _ in range(3):
            if "job" not in slicing or slicing.get("status") != "running":
                break
            slicing = tool_data(call("tools/call", {"name": "wait", "arguments": {
                "for": "job", "job": slicing["job"], "timeout_s": 45}}))
        if slicing.get("status") != "done" or not slicing.get("plates") or any(
                plate.get("outcome") != "ok" for plate in slicing["plates"]):
            raise ValueError("MCP slicing did not finish with nonempty successful plates")
    return {"authentication_required": True, "protocol": "2026-07-28",
            "legacy_handshake": initialized["protocolVersion"],
            "server": initialized["serverInfo"]["name"], "tools": sorted(names),
            "read_only_calls_passed": ["get_state", "list_objects", "u1_plan_filament_partition"],
            "project_mutated": slice_project, "slicing": slicing, "printer_contacted": False,
            "overflowing_selection_rejected": slice_project,
            "codex_or_claude_client_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discovery", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--slice-current-project", action="store_true",
                        help="slice an already-loaded trusted offline fixture; never submit it to a printer")
    args = parser.parse_args()
    result = smoke(json.loads(args.discovery.read_text()), args.slice_current_project)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print("Native MCP smoke test passed; credentials omitted from report")


if __name__ == "__main__":
    main()
