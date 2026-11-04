#!/usr/bin/env python3
"""Offline U1 tool/temperature/command checks against an explicit capability fixture."""
import argparse
import json
import math
from pathlib import Path
import re


def validate(text, capabilities):
    if not isinstance(capabilities, dict):
        raise ValueError("capability fixture must be an object")
    tools = capabilities.get("tools", [])
    if not isinstance(tools, list) or len(tools) != 4 or any(not isinstance(tool, dict) for tool in tools):
        raise ValueError("a U1 capability fixture must describe exactly four tools")
    for tool in tools:
        values = [tool.get(k) for k in ("nozzle_diameter", "minimum_print_temperature", "maximum_temperature")]
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
            raise ValueError("nozzle and temperature bounds must be finite numbers")
        if values[0] <= 0 or not 0 <= values[1] <= values[2] <= 500:
            raise ValueError("invalid nozzle or temperature bounds")
    commands = capabilities.get("allowed_commands", [])
    if not isinstance(commands, list) or not commands or any(not isinstance(command, str) for command in commands):
        raise ValueError("allowed_commands must explicitly name supported G-code commands and macros")
    allowed = set(commands)
    errors, warnings, selected, temperatures = [], [], [], [None] * 4
    current = None
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.partition(";")[0].strip()
        if not line:
            continue
        command = line.split()[0].upper()
        if any(c in line for c in "{}[]"):
            errors.append({"line": number, "message": "unexpanded template or unsupported expression"})
            continue
        if re.fullmatch(r"T[-+]?\d+", command):
            tool = int(command[1:])
            if not 0 <= tool < 4:
                errors.append({"line": number, "message": "tool selection outside T0..T3"})
            else:
                current = tool
                selected.append(tool)
            continue
        if command not in allowed:
            errors.append({"line": number, "message": f"command not declared by capability fixture: {command}"})
            continue
        if command in {"SAVE_CONFIG", "FIRMWARE_RESTART", "RESTART", "M500", "M502"}:
            errors.append({"line": number, "message": "configuration/restart command in print G-code"})
            continue
        if command in {"M104", "M109"}:
            params = {}
            for token in line.split()[1:]:
                match = re.fullmatch(r"([A-Za-z])([-+]?(?:\d+(?:\.\d*)?|\.\d+))", token)
                if not match or match[1].upper() in params:
                    errors.append({"line": number, "message": "invalid or repeated temperature parameter"})
                    continue
                params[match[1].upper()] = float(match[2])
            target = params.get("T", current)
            if set(params) - {"T", "S", "R"} or ("S" in params and "R" in params):
                errors.append({"line": number, "message": "ambiguous or unsupported temperature parameters"})
                continue
            if target is None or not float(target).is_integer() or not 0 <= target < 4:
                errors.append({"line": number, "message": "temperature command has no valid tool target"})
                continue
            target = int(target)
            temperature = params.get("S", params.get("R"))
            if temperature is None or not math.isfinite(temperature) or temperature < 0 or temperature > tools[target]["maximum_temperature"]:
                errors.append({"line": number, "message": "missing, negative or excessive nozzle temperature"})
                continue
            if temperature and temperature < tools[target]["minimum_print_temperature"]:
                warnings.append({"line": number, "message": "temperature below printing range; may be intentional standby"})
            temperatures[target] = temperature
    return {"passed_subset": not errors, "errors": errors, "warnings": warnings,
            "tools_selected": sorted(set(selected)), "last_commanded_temperatures": temperatures,
            "scope": "tool indices, nozzle fixture bounds, temperature commands, declared command names",
            "physical_compatibility_verified": False,
            "not_checked": ["motion collisions", "extrusion volume", "tool docking sequences",
                            "macro implementation safety", "prime tower geometry", "material adhesion"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gcode", type=Path)
    parser.add_argument("--capabilities", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = validate(args.gcode.read_text(), json.loads(args.capabilities.read_text()))
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["passed_subset"] else 1)


if __name__ == "__main__":
    main()
