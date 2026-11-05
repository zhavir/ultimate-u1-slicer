import base64
import csv
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import types
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_plugins


def project_bytes():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as archive:
        archive.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        archive.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        archive.writestr('3D/3dmodel.model', '<model xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" unit="millimeter"><resources><object id="1" type="model"><mesh><vertices><vertex x="0" y="0" z="0"/><vertex x="10" y="0" z="0"/><vertex x="0" y="10" z="1"/></vertices><triangles><triangle v1="0" v2="1" v3="2"/></triangles></mesh></object></resources><build><item objectid="1"/></build></model>')
        archive.writestr('Metadata/project_settings.config', json.dumps({'printer_model': 'Snapmaker U1', 'raft_first_layer_expansion': '-1', 'filament_colour': ['#FFFFFF'], 'nozzle_diameter': ['0.4']}))
    return buffer.getvalue()


class Integrations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packages = tempfile.TemporaryDirectory()
        cls.wheels = build_plugins.build(Path(cls.packages.name) / 'wheels')
        cls.import_root = Path(cls.packages.name) / 'import'
        for wheel in cls.wheels:
            with zipfile.ZipFile(Path(cls.packages.name) / 'wheels' / wheel['file']) as archive:
                archive.extractall(cls.import_root)
        # Only the Python entry decorator is stubbed here. Native load/install is covered
        # separately by the C++ runtime test; Studio functions below run their real code.
        cls.orca = types.ModuleType('orca')
        cls.orca.script = types.SimpleNamespace(ScriptPluginCapabilityBase=object)
        cls.orca.base = object
        cls.orca.plugin = lambda c: c
        cls.previous_orca = sys.modules.get('orca')
        sys.modules['orca'] = cls.orca
        sys.path.insert(0, str(cls.import_root))
        cls.studio = importlib.import_module('u1_studio_plugin.studio')
        cls.converter = importlib.import_module('u1_bambu_converter_plugin.converter')
        cls.common = importlib.import_module('u1_bambu_converter_plugin.common')

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(str(cls.import_root))
        if cls.previous_orca is None:
            sys.modules.pop('orca', None)
        else:
            sys.modules['orca'] = cls.previous_orca
        cls.packages.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.environment = patch.dict(os.environ, {'U1_MCP_ALLOWED_ROOTS': json.dumps([str(self.root)])})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.source = self.root / 'input.3mf'
        self.source.write_bytes(project_bytes())

    def test_deterministic_wheels_have_valid_record_hashes(self):
        rebuilt = build_plugins.build(self.root / 'wheels')
        self.assertEqual(rebuilt, self.wheels)
        for wheel in rebuilt:
            with zipfile.ZipFile(self.root / 'wheels' / wheel['file']) as archive:
                record = next(n for n in archive.namelist() if n.endswith('.dist-info/RECORD'))
                for name, checksum, size in csv.reader(io.StringIO(archive.read(record).decode())):
                    if not checksum:
                        continue
                    data = archive.read(name)
                    self.assertEqual(int(size), len(data))
                    expected = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode()
                    self.assertEqual(checksum, 'sha256=' + expected)

    def test_real_studio_inspects_without_mutating_auto_expansion(self):
        before = self.source.read_bytes()
        result = self.studio.inspect_project({'path': str(self.source)})
        self.assertFalse(result['project_modified'])
        self.assertFalse(result['printer_contacted'])
        self.assertFalse(result['hardware_verified'])
        self.assertEqual(self.source.read_bytes(), before)
        self.assertIn('checks', result['preflight'])
        self.assertIn('format', result['traits'])
        with zipfile.ZipFile(self.source) as archive:
            self.assertEqual(json.loads(archive.read('Metadata/project_settings.config'))['raft_first_layer_expansion'], '-1')

    def test_unknown_printer_is_not_reported_as_verified(self):
        result = self.studio.inspect_project({'path': str(self.source)})
        self.assertIn('unknown', json.dumps(result['preflight']).lower())
        self.assertFalse(result['hardware_verified'])

    def test_paths_deny_by_default_traversal_and_existing_outputs(self):
        with patch.dict(os.environ, {'U1_MCP_ALLOWED_ROOTS': '[]'}):
            with self.assertRaises(ValueError):
                self.common.AuthorizedFiles().path(str(self.source))
        policy = self.common.AuthorizedFiles()
        with self.assertRaises(ValueError):
            policy.path(str(self.root / 'sub' / '..' / 'input.3mf'))
        with self.assertRaises(ValueError):
            policy.path(str(self.source), output=True)
        with self.assertRaises(ValueError):
            policy.path('input.3mf')

    def test_output_creation_never_overwrites(self):
        self.source.write_bytes(b'original')
        with self.assertRaises(FileExistsError):
            self.common.write_new(self.source, b'replacement')
        self.assertEqual(self.source.read_bytes(), b'original')

    def test_loopback_only_and_no_credentials_or_redirect_urls(self):
        for endpoint in ('http://example.com:8080', 'http://localhost:8080', 'http://127.0.0.1:0',
                         'http://user:secret@127.0.0.1:8080', 'http://127.0.0.1:8080/api',
                         'https://127.0.0.1:8080', 'file:///etc/passwd'):
            with self.subTest(endpoint=endpoint), self.assertRaises(ValueError):
                self.converter.LocalConverter(endpoint)

    def test_license_acknowledgment_is_required_before_contact(self):
        with self.assertRaisesRegex(ValueError, 'license'):
            self.converter.convert_project({'endpoint': 'http://127.0.0.1:1', 'path': str(self.source),
                'output': str(self.root / 'output.3mf'), 'reference_profile': 'standard', 'license_acknowledged': False})

    def test_unsafe_download_archive_is_rejected(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('../escape', 'unsafe')
        with self.assertRaises(ValueError):
            self.common.check_3mf(buffer.getvalue())
        with self.assertRaises(ValueError):
            self.common.check_3mf(b'not a zip')

    def test_converter_contract_round_trip_uses_new_output_and_disables_pauses(self):
        captured = []
        project = project_bytes()

        class Service(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                if self.path == '/api/profiles':
                    body = b'[{"id":"standard"}]'
                elif self.path == '/api/download/test-job':
                    body = project
                else:
                    self.send_error(404)
                    return
                self.send_response(200)
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                captured.append((self.path, self.rfile.read(int(self.headers['Content-Length']))))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"job_id":"test-job","diff":{"counts":{}}}')

        server = ThreadingHTTPServer(('127.0.0.1', 0), Service)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            endpoint = f'http://127.0.0.1:{server.server_port}'
            self.assertEqual(self.converter.list_profiles({'endpoint': endpoint}), [{'id': 'standard'}])
            output = self.root / 'output.3mf'
            result = self.converter.convert_project({'endpoint': endpoint, 'path': str(self.source),
                'output': str(output), 'reference_profile': 'standard', 'license_acknowledged': True})
            self.assertEqual(output.read_bytes(), project)
            self.assertTrue(result['requires_reslicing'])
            self.assertFalse(result['printer_contacted'])
            self.assertEqual(captured[0][0], '/api/convert')
            self.assertIn(b'name="insert_swap_pauses"\r\n\r\nfalse', captured[0][1])
            self.assertNotIn(b'M600', captured[0][1])
            self.assertEqual(self.source.read_bytes(), project)
        finally:
            server.shutdown()
            worker.join(timeout=5)
            server.server_close()


if __name__ == '__main__':
    unittest.main()
