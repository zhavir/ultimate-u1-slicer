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
    snapmaker_a = capabilities.get("snapmaker_a_parameter", False)
    if not isinstance(snapmaker_a, bool):
        raise ValueError("snapmaker_a_parameter must be a boolean")
    mapping = capabilities.get("logical_to_physical", list(range(4)))
    if not isinstance(mapping, list) or len(mapping) < 4 or len(mapping) > 1024:
        raise ValueError("logical_to_physical must explicitly map at least four logical slots")
    if any(isinstance(value, bool) or not isinstance(value, int) or not -1 <= value < 4 for value in mapping):
        raise ValueError("logical_to_physical entries must be -1 (unmapped) or a physical head 0..3")
    if snapmaker_a and "logical_to_physical" not in capabilities:
        raise ValueError("Snapmaker A semantics require the actual job's logical_to_physical map")
    if not snapmaker_a and "logical_to_physical" in capabilities:
        raise ValueError("a logical map requires explicitly declared Snapmaker A semantics")

    def physical(index, mapped):
        if isinstance(index, float) and (not math.isfinite(index) or not index.is_integer()):
            return None
        if index < 0:
            return None
        index = int(index)
        if mapped:
            return mapping[index] if index < len(mapping) and mapping[index] >= 0 else None
        return index if index < 4 else None

    errors, warnings, selected, physical_selected, temperatures = [], [], [], [], [None] * 4
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
            params = line.split()[1:]
            if params and (not snapmaker_a or len(params) != 1 or params[0].upper() not in {"A0", "A1"}):
                errors.append({"line": number, "message": "unsupported tool-selection arguments"})
                continue
            if command not in {"T0", "T1", "T2", "T3"}:
                errors.append({"line": number, "message": "tool selection outside T0..T3"})
            else:
                tool = int(command[1:])
                mapped = snapmaker_a and (not params or params[0].upper() != "A0")
                current = physical(tool, mapped)
                if current is None:
                    errors.append({"line": number, "message": "tool selection has no declared physical head mapping"})
                else:
                    selected.append(tool)
                    physical_selected.append(current)
            continue
        if command not in allowed:
            errors.append({"line": number, "message": f"command not declared by capability fixture: {command}"})
            continue
        if command in {"SAVE_CONFIG", "FIRMWARE_RESTART", "RESTART", "M500", "M502", "SET_PRINT_EXTRUDER_MAP"}:
            errors.append({"line": number, "message": "configuration/restart command in print G-code"})
            continue
        if command == "SWITCH_OF_EXTENDED_EXTRUDER":
            # Verified stock source: toolhead.py translates INDEX >= 4 through print_task_config,
            # then selects the physical extruder with mapping bypassed. Never execute it here.
            match = re.fullmatch(r"SWITCH_OF_EXTENDED_EXTRUDER\s+INDEX=(\d+)", line, re.IGNORECASE)
            if not snapmaker_a or not match or len(match[1]) > 10 or int(match[1]) < 4:
                errors.append({"line": number, "message": "extended selection requires declared Snapmaker semantics and INDEX >= 4"})
                continue
            logical = int(match[1])
            current = physical(logical, True)
            if current is None:
                errors.append({"line": number, "message": "extended tool has no declared physical head mapping"})
            else:
                selected.append(logical)
                physical_selected.append(current)
            continue
        if command in {"M104", "M109"}:
            params = {}
            for token in line.split()[1:]:
                match = re.fullmatch(r"([A-Za-z])([-+]?(?:\d+(?:\.\d*)?|\.\d+))", token)
                if not match or match[1].upper() in params:
                    errors.append({"line": number, "message": "invalid or repeated temperature parameter"})
                    continue
                params[match[1].upper()] = float(match[2])
            permitted = {"T", "S"} if snapmaker_a or command == "M104" else {"T", "S", "R"}
            if snapmaker_a:
                permitted.add("A")
            if set(params) - permitted or ("S" in params and "R" in params):
                errors.append({"line": number, "message": "ambiguous or unsupported temperature parameters"})
                continue
            if "A" in params and params["A"] not in {0, 1}:
                errors.append({"line": number, "message": "unsupported A mapping flag"})
                continue
            target = physical(params["T"], snapmaker_a and params.get("A", 1) != 0) if "T" in params else current
            if target is None:
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
            "physical_tools_selected": sorted(set(physical_selected)),
            "indexing": "declared Snapmaker A/map semantics" if snapmaker_a else "direct four-tool fixture",
            "scope": "declared tool mapping, nozzle fixture bounds, temperature commands, declared command names",
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
