import importlib.util
import hashlib
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("release_manifest", Path(__file__).parents[1] / "release_manifest.py")
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseManifestTests(unittest.TestCase):
    def test_hashes_bytes_without_claiming_release_or_hardware_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            data = b"synthetic artifact, not a slicer binary"
            (artifacts / "fixture.bin").write_bytes(data)
            result = release.create_manifest(artifacts, root / "metadata")
            self.assertEqual(result["files"][0]["sha256"], hashlib.sha256(data).hexdigest())
            self.assertFalse(result["hardware_verified"])
            self.assertFalse(result["artifact_provenance_verified"])
            self.assertEqual(result["status"], "experimental-candidate")
            self.assertEqual(release.create_manifest(artifacts, root / "metadata"), result)

    def test_refuses_empty_or_overlapping_artifact_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            with self.assertRaisesRegex(ValueError, "no artifacts"):
                release.create_manifest(artifacts, root / "metadata")
            with self.assertRaisesRegex(ValueError, "separate"):
                release.create_manifest(artifacts, artifacts / "metadata")


if __name__ == "__main__":
    unittest.main()
