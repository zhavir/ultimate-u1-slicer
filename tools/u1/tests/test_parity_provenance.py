"""Audit pins must describe the inspected bytes, not just a declared SHA."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from parity_audit import validate_source_snapshot


class SourceProvenanceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'src').mkdir()
        self.source = self.root / 'src/example.cpp'
        self.source.write_bytes(b'int example() { return 1; }\n')
        self.git('init', '-q')
        self.git('config', 'core.autocrlf', 'false')
        self.git('add', 'src')
        self.git('-c', 'user.name=Audit fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'Pinned source')
        self.ref = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True)

    def test_exact_snapshot_is_accepted(self):
        validate_source_snapshot(self.root, self.ref, self.root)

    def test_same_inventory_with_changed_bytes_is_rejected(self):
        self.source.write_bytes(b'int example() { return 2; }\n')
        with self.assertRaisesRegex(ValueError, 'Source bytes differ'):
            validate_source_snapshot(self.root, self.ref, self.root)

    def test_incomplete_export_is_rejected(self):
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, 'inventory differs'):
            validate_source_snapshot(self.root, self.ref, self.root)

    def test_unattributed_extra_source_is_rejected(self):
        (self.root / 'src/extra.hpp').write_bytes(b'void unreviewed();\n')
        with self.assertRaisesRegex(ValueError, 'inventory differs'):
            validate_source_snapshot(self.root, self.ref, self.root)
