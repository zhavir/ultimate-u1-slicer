import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("gcode_check", Path(__file__).parents[1] / "gcode_check.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class GcodeCheckTests(unittest.TestCase):
    def setUp(self):
        # Synthetic bounds, not measured U1 material/nozzle calibration.
        self.capabilities = {"tools": [{"nozzle_diameter": d, "minimum_print_temperature": 180,
                                          "maximum_temperature": 260} for d in [0.2, 0.4, 0.6, 0.8]],
                             "allowed_commands": ["M104", "M109", "G0", "G1", "G90", "SAVE_CONFIG"]}

    def check_gcode(self, text):
        return checker.validate(text, self.capabilities)

    def test_accepts_four_tool_temperature_commands_and_heater_off(self):
        result = self.check_gcode("T0\nM109 S210\nT1\nM104 S220 T1\nT2\nT3\nM104 S0 T0\nG1 X10 Y10")
        self.assertTrue(result["passed_subset"])
        self.assertEqual(result["tools_selected"], [0, 1, 2, 3])
        self.assertFalse(result["physical_compatibility_verified"])

    def test_rejects_invalid_tool_and_temperature(self):
        for text in ["T4", "T-1", "M104 S210", "T0\nM104 S300", "M109 T-1 S200", "M104 T0 S-1"]:
            with self.subTest(text=text):
                self.assertFalse(self.check_gcode(text)["passed_subset"])

    def test_rejects_undeclared_macros_and_restart_even_if_declared(self):
        for text in ["ARBITRARY_MACRO", "SAVE_CONFIG", "T[next_extruder]"]:
            self.assertFalse(self.check_gcode(text)["passed_subset"])

    def test_reports_low_standby_temperature_without_claiming_full_validation(self):
        result = self.check_gcode("T0\nM104 S150")
        self.assertTrue(result["passed_subset"])
        self.assertEqual(len(result["warnings"]), 1)
        self.assertIn("motion collisions", result["not_checked"])

    def test_refuses_ambiguous_temperature_arguments_and_malformed_capability_fixtures(self):
        for line in ["M104 T0 S210 S300", "M109 T0 S210 R300", "M104 T0 S210 X99"]:
            self.assertFalse(self.check_gcode(line)["passed_subset"])
        for fixture in [None, [], {"tools": [1, 2, 3, 4]}]:
            with self.assertRaises(ValueError):
                checker.validate("T0", fixture)


if __name__ == "__main__":
    unittest.main()
