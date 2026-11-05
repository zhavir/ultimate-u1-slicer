#!/usr/bin/env python3
"""Offline source inventory for the U1 parity review; source presence is not verification."""
from __future__ import annotations

import argparse
import bisect
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
SOURCE_REFS = {
    'snapmaker-v241': 'bac6fd5c1e1c23ddf057cf6471ba4ed7ed621c4c',
    'snapmaker-main': 'f5fd7289ea067997181ee6c2cf15a98f58faba43',
    'orca-mcp-base': '17a745e30c248cf3acb4c429b650b22d106fd19a',
    'forca': '0b1f80cd22793785d8ae5c4296d2fe4a9248bd21',
}


def config_definitions(root):
    path = root / 'src/libslic3r/PrintConfig.cpp'
    if not path.is_file():
        return {}
    text = path.read_text(encoding='utf-8', errors='replace')
    starts = [m for m in re.finditer(r'\badd\("([^\"]+)"', text)]
    newlines = [i for i, ch in enumerate(text) if ch == '\n']
    owners = [(m.start(), m.group(1)) for m in re.finditer(r'^(?:\w+\s+)?(PrintConfigDef::\w+)\s*\(', text, re.MULTILINE)]
    owner_offsets = [pos for pos, _ in owners]
    result = {}
    for i, match in enumerate(starts):
        block = text[match.start():starts[i+1].start() if i+1 < len(starts) else len(text)]
        result[match.group(1)] = {
            'path': 'src/libslic3r/PrintConfig.cpp',
            'line': bisect.bisect_right(newlines, match.start()) + 1,
            'symbol': owners[bisect.bisect_right(owner_offsets, match.start()) - 1][1] if owners else 'unresolved',
            'type_expression': (re.findall(r'add\(\"[^\"]+\",\s*(\w+)', block) or [None])[0],
            'min_expression': (re.findall(r'def->min\s*=\s*([^;]+)', block) or [None])[0],
            'default_expression': (re.findall(r'def->set_default_value\(([^;]+)', block) or [None])[0],
        }
    return result


def source_index(root):
    result = {}
    for directory in ('src', 'plugins/u1_integrations', 'tools/u1/windows'):
        base = root / directory
        if not base.is_dir():
            continue
        for path in base.rglob('*'):
            if path.suffix not in ('.cpp', '.hpp', '.h', '.py', '.ps1') or not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            text = path.read_text(encoding='utf-8', errors='replace')
            result[relative] = text
    return result


def source_hits(index, fragments, keys):
    hits = []
    for path, text in index.items():
        if not any(fragment in path for fragment in fragments):
            continue
        if path.endswith(('PrintConfig.cpp', 'PrintConfig.hpp')):
            continue  # definitions are recorded separately; do not pretend they are consumers
        tokens = [key for key in keys if re.search(r'\b' + re.escape(key) + r'\b', text)]
        symbols = []
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith('//'):
                continue
            match = re.match(r'\s*(?:[\w:<>,*&]+\s+)+((?:\w+::)+~?\w+)\s*\(', line)
            if not match:
                match = re.match(r'\s*def\s+(\w+)\s*\(', line)
            if match:
                symbols.append({'symbol': match.group(1), 'line': line_number})
        hits.append({'path': path, 'sha256': hashlib.sha256(text.encode()).hexdigest(),
                     'referenced_configuration_keys': tokens, 'declared_symbols': symbols[:24]})
    return hits


def plugin_suitability(feature):
    if feature['category'] == 'Plugins':
        return 'Implemented by the named optional plugin/host integration, within its documented tested scope.'
    if feature['category'] in ('Prime tower', 'Supports', 'Full Spectrum', 'FOrca'):
        return 'The bundled plugins do not implement this slicing-kernel behavior. Prefer native upstream code and reviewed schema adapters.'
    if feature['category'] in ('Connectivity', 'Firmware'):
        return 'Studio may evaluate supplied facts; neither bundled plugin supplies validated Snapmaker gateway, RFID, camera or feeder control.'
    if feature['category'] == 'MCP':
        return 'Retain/extend the native MCP implementation. Generic plugin/UI bridges must not bypass authorization gates.'
    return 'No bundled plugin substitutes for this native compatibility/release gate.'


def generate(roots):
    catalog = json.loads((ROOT / 'tools/u1/feature_catalog.json').read_text())
    known = {f['id'] for f in catalog['features']}
    for feature in catalog['features']:
        if feature['status'] not in catalog['statuses'] or not set(feature['dependencies']) <= known:
            raise ValueError('Invalid feature status or dependency')
    visited, active = set(), set()

    def visit(key):
        if key in active:
            raise ValueError('Cyclic feature dependencies')
        if key in visited:
            return
        active.add(key)
        for child in next(f for f in catalog['features'] if f['id'] == key)['dependencies']:
            visit(child)
        active.remove(key)
        visited.add(key)
    for key in known:
        visit(key)
    definitions = {name: config_definitions(path) for name, path in roots.items()}
    indexes = {name: source_index(path) for name, path in roots.items()}
    features = []
    for item in catalog['features']:
        feature = dict(item)
        feature['plugin_or_agent_equivalence'] = plugin_suitability(item)
        feature['source_evidence'] = {}
        for name in roots:
            keys = sorted(key for key in definitions[name] if item['configuration_pattern'] and
                          re.fullmatch(item['configuration_pattern'], key))
            feature['source_evidence'][name] = {
                'commit': SOURCE_REFS.get(name, 'working tree; see candidate_base and diff digest'),
                'configuration': {key: definitions[name][key] for key in keys},
                'implementation_files': source_hits(indexes[name], item['source_file_fragments'], keys),
            }
        feature['automated_evidence'] = evidence_for(item['id'])
        feature['recommended_strategy'] = item['migration_boundary']
        features.append(feature)
    own = definitions['ultimate']
    delta = {name: {'absent_configuration_keys': sorted(set(values)-set(own)),
                    'shared_keys_with_changed_range_or_default': sorted(key for key in set(values)&set(own)
                        if any(values[key][field] != own[key][field] for field in ('type_expression','min_expression','default_expression')))}
             for name, values in definitions.items() if name != 'ultimate'}
    base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    diff = subprocess.check_output(['git', 'diff', SOURCE_REFS['orca-mcp-base'], '--', 'src'], cwd=ROOT)
    changed = subprocess.check_output(['git', 'diff', '--name-status', SOURCE_REFS['orca-mcp-base'], '--', 'src'], cwd=ROOT, text=True).splitlines()
    profiles = []
    for path in sorted((ROOT/'resources/profiles/Snapmaker/machine').glob('*.json')):
        data = json.loads(path.read_text())
        if data.get('printer_model') == 'Snapmaker U1':
            profiles.append({'path': path.relative_to(ROOT).as_posix(), 'name': data.get('name'),
                             'variant': data.get('printer_variant'), 'nozzle_diameter': data.get('nozzle_diameter'),
                             'calibrated_hardware_here': False})
    return {'schema': 1, 'audit_date': '2026-11-05', 'candidate_base': base,
            'scope': 'Bounded source-backed feature inventory, not certification. Read code/test evidence and dependencies; key overlap does not prove semantic parity.',
            'mcp_allowed_tool_names': re.findall(r'\"([a-z_]+)\"', (ROOT/'src/slic3r/GUI/Mcp/McpU1Policy.hpp').read_text()),
            'source_refs': SOURCE_REFS, 'counts': dict(Counter(f['status'] for f in features)),
            'features': features, 'schema_deltas': delta, 'u1_nozzle_profiles': profiles,
            'official_integration_source_diff': {'base':SOURCE_REFS['orca-mcp-base'], 'sha256':hashlib.sha256(diff).hexdigest(), 'changed_paths':changed},
            'global_limits':['No physical printer operated.','No public-trusted signing identity configured.','Full current-upstream merge/parity is not claimed.','Some source hits are generic implementations, not U1-specific protocol support.']}


def evidence_for(key):
    base = ['docs/testing/local-validation.md', 'docs/testing/evidence/plugin-integration-offline.json']
    if key in ('support-auto','project-migration'):
        return base + ['docs/testing/reference-slicing.md','docs/architecture/support-expansion-migration.md']
    if key.startswith('mcp-') or key == 'filament-planner':
        return base + ['docs/testing/evidence/components.junit.xml','docs/testing/evidence/mcp-live-smoke.json','docs/testing/evidence/mcp-slice-smoke.json']
    if key in ('plugins-discovery','plugin-studio','plugin-converter'):
        return base + ['tests/slic3rutils/test_u1_plugin_packages.cpp','tools/u1/tests/test_plugin_integrations.py']
    if key.startswith('tower-') or key.startswith('fos-'):
        return base + ['tests/fff_print/test_wipe_tower.cpp','tests/fff_print/test_multifilament.cpp','tests/fff_print/test_u1_four_tool_gcode.cpp']
    if key in ('high-flow','u1-camera','u1-cover','u1-rfid','u1-feeder','u1-cloud','u1-gateway','hardware-print'):
        return base + ['No feature-specific U1 runtime/hardware verification recorded; generic suite success is not parity.']
    return base


def write_report(result, destination):
    destination.mkdir(parents=True, exist_ok=True)
    (destination/'functional-parity.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    lines=['# Functional parity audit — 2026-11-05','',result['scope'],'',
           'Exact reference source revisions: '+', '.join(f'`{name}` `{sha}`' for name,sha in SOURCE_REFS.items())+'.','',
           '**There is no 100% U1 compatibility or stable-release claim.** The exact v2.4.1 release and post-release Snapmaker main are separate evidence columns.','',
           '## Summary','', '| Status | Features |','|---|---:|']
    lines += [f'| {name} | {result["counts"].get(name,0)} |' for name in ('Verified','Implemented but untested','Partial','Missing','Incompatible','Unknown')]
    lines += ['', '## Feature matrix','', '| ID | Feature | Status | Priority | Depends on |','|---|---|---|---|---|']
    lines += [f'| [{f["id"]}](#{f["id"]}) | {f["title"]} | {f["status"]} | {f["priority"]} | '+(', '.join(f['dependencies']) or '—')+' |' for f in result['features']]
    lines += ['', 'The detailed JSON contains exact source file hashes, configuration definitions, line numbers, symbols, schema differences and the complete integration source-path diff. Source hits are evidence for inspection, not an automatic equivalence verdict.','']
    for f in result['features']:
        lines += [f'<a id="{f["id"]}"></a>', f'## {f["title"]}', '', f'**{f["status"]}; {f["priority"]}.** Dependencies: '+(', '.join(f['dependencies']) or 'none')+'.','', f['migration_boundary'],'',f'Plugin/agent assessment: {f["plugin_or_agent_equivalence"]}','', 'Reference implementation evidence:']
        for name, evidence in f['source_evidence'].items():
            paths = sorted({x['path'] for x in evidence['implementation_files']})
            keys = list(evidence['configuration'])
            lines += ['- '+name+' (`'+evidence['commit']+'`): '+(', '.join('`'+p+'`' for p in paths[:6]) or 'No matching component in the inspected source scope')+'. Keys: '+(', '.join('`'+k+'`' for k in keys[:18]) or 'none for this bounded component')+'.']
        lines += ['', 'Tests/evidence: '+ '; '.join('`'+p+'`' for p in f['automated_evidence'])+'.','']
    (destination/'functional-parity-audit.md').write_text('\n'.join(lines).rstrip()+'\n', encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapmaker-v241',type=Path,default=Path('/tmp/u1-snapmaker-v241'))
    parser.add_argument('--snapmaker-main',type=Path,default=ROOT.parent/'ultimate-u1-audit/snapmaker')
    parser.add_argument('--forca',type=Path,default=ROOT.parent/'ultimate-u1-audit/forca')
    parser.add_argument('--orca-mcp-base',type=Path,default=Path('/tmp/u1-orca-mcp-base'))
    args=parser.parse_args()
    roots={'snapmaker-v241':args.snapmaker_v241,'snapmaker-main':args.snapmaker_main,
           'orca-mcp-base':args.orca_mcp_base,'forca':args.forca,'ultimate':ROOT}
    if any(not (path/'src/libslic3r/PrintConfig.cpp').is_file() for path in roots.values()):
        raise SystemExit('All exact reference source trees must be available; see reference commits in this script.')
    result=generate(roots)
    write_report(result,ROOT/'docs/architecture')
    print(json.dumps({'features':len(result['features']),'counts':result['counts'],
                      'schema_absences':{k:len(v['absent_configuration_keys']) for k,v in result['schema_deltas'].items()}},indent=2))


if __name__=='__main__':
    main()
