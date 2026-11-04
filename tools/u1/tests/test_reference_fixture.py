import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parents[1]))
from reference_fixture import build_fixture


class ReferenceFixtureTests(unittest.TestCase):
    def test_resolves_profiles_with_legacy_cli_context_without_modifying_sources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profiles = root / "profiles"
            profiles.mkdir()
            index = {"version": "01.00.00.00"}
            values = {
                "machine": [{"name": "Machine", "nozzle_diameter": ["0.4"]}],
                "process": [{"name": "Base", "layer_height": "0.2"},
                            {"name": "Process", "inherits": "Base", "post_process": ["unsafe-command"]}],
                "filament": [{"name": "PLA", "nozzle_temperature": ["220"]}],
            }
            for kind, presets in values.items():
                folder = profiles / "Snapmaker" / kind
                folder.mkdir(parents=True)
                index[kind + "_list"] = []
                for value in presets:
                    relative = kind + "/" + value["name"] + ".json"
                    (profiles / "Snapmaker" / relative).write_text(json.dumps(value))
                    index[kind + "_list"].append({"name": value["name"], "sub_path": relative})
            (profiles / "Snapmaker.json").write_text(json.dumps(index))
            (profiles / "OrcaFilamentLibrary.json").write_text(json.dumps({"version": "01.00.00.00"}))
            before = {path: path.read_bytes() for path in profiles.rglob("*.json")}
            destination = root / "fixture"
            manifest = build_fixture(profiles, destination, "Machine", "Process", "PLA")
            process = json.loads((destination / "process.json").read_text())
            self.assertEqual(process["layer_height"], "0.2")
            self.assertEqual(process["nozzle_diameter"], ["0.4"])
            self.assertEqual(process["post_process"], [])
            self.assertEqual(process["from"], "system")
            self.assertNotIn("inherits", process)
            self.assertFalse(manifest["calibration_verified"])
            self.assertEqual({path: path.read_bytes() for path in before}, before)
            four = root / "four"
            mapped = build_fixture(profiles, four, "Machine", "Process", "PLA", tools=4)
            self.assertEqual(mapped["object_filament_ids"], [1, 2, 3, 4])
            self.assertEqual(len({json.loads((four / f"filament{i}.json").read_text())["name"]
                                  for i in range(1, 5)}), 4)
            self.assertTrue((four / "cube4.stl").is_file())
            with self.assertRaisesRegex(ValueError, "empty"):
                build_fixture(profiles, destination, "Machine", "Process", "PLA")
            with self.assertRaisesRegex(ValueError, "outside"):
                build_fixture(profiles, profiles / "fixture", "Machine", "Process", "PLA")


if __name__ == "__main__":
    unittest.main()
