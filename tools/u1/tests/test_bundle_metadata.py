from pathlib import Path
import plistlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]


class BundleMetadataTests(unittest.TestCase):
    def test_macos_template_is_a_valid_plist_with_fork_specific_identity(self):
        value = plistlib.loads((ROOT / "src/dev-utils/platform/osx/Info.plist.in").read_bytes())
        self.assertEqual(value["CFBundleExecutable"], "OrcaSlicer")
        self.assertNotEqual(value["CFBundleIdentifier"], "com.orcaslicer.OrcaSlicer")
        self.assertIsInstance(value["CFBundleURLTypes"], list)
        schemes = value["CFBundleURLTypes"][0]["CFBundleURLSchemes"]
        self.assertNotIn("orcaslicer", schemes)
        self.assertNotIn("orcasliceropen", schemes)
        self.assertEqual(value["ATSApplicationFontsPath"], "fonts/")

    def test_application_data_key_does_not_reuse_an_existing_slicer_namespace(self):
        version = (ROOT / "version.inc").read_text()
        key = re.search(r'set\(SLIC3R_APP_KEY "([^"]+)"\)', version)[1]
        self.assertNotIn(key, {"OrcaSlicer", "Snapmaker_Orca", "FOrcaSlicer"})


if __name__ == "__main__":
    unittest.main()
