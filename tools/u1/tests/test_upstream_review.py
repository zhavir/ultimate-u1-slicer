import importlib.util
from pathlib import Path
import unittest
import subprocess
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("upstream_review", Path(__file__).parents[1] / "upstream_review.py")
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


class UpstreamReviewTests(unittest.TestCase):
    def test_classifies_engine_mcp_profiles_and_connectivity(self):
        for path, expected in [("src/libslic3r/PrintConfig.cpp", "engine-schema-gcode"),
                               ("src/slic3r/GUI/Mcp/McpCore.cpp", "mcp"),
                               ("submodules/Profiles", "profiles"),
                               ("src/slic3r/Utils/GatewayDevice.cpp", "connectivity")]:
            self.assertEqual(review.subsystem(path), expected)

    def test_report_marks_overlaps_without_claiming_integration(self):
        lock = {"sources": {"orca-mcp": {"sha": "a" * 40,
                 "url": "https://github.com/OrcaSlicer/OrcaSlicer.git", "branch": "feature/mcp"}}}
        with patch.object(review, "git", side_effect=["src/libslic3r/Print.cpp", "b" * 40,
                                                      "src/libslic3r/Print.cpp", "b candidate"]):
            result = review.review(Path("."), lock)["orca-mcp"]
        self.assertFalse(result["source_integrated"])
        self.assertEqual(result["compatibility"], "unverified")
        self.assertEqual(result["potential_conflict_paths"], ["src/libslic3r/Print.cpp"])

    def test_refuses_credential_bearing_source_urls(self):
        lock = {"sources": {"orca-mcp": {"sha": "a" * 40,
                 "url": "https://token@github.com/org/repo.git"}}}
        with patch.object(review, "git", return_value=""):
            with self.assertRaisesRegex(ValueError, "without credentials"):
                review.review(Path("."), lock)

    def test_textual_merge_probe_never_claims_semantic_compatibility_or_changes_head(self):
        lock = {"sources": {"orca-mcp": {"sha": "a" * 40,
                 "url": "https://github.com/OrcaSlicer/OrcaSlicer.git", "branch": "feature/mcp"}}}
        with patch.object(review, "git", side_effect=["src/libslic3r/Print.cpp", "b" * 40,
                                                      "src/libslic3r/Print.cpp", "b candidate"]):
            with patch.object(review.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "c" * 40, "")) as run:
                result = review.review(Path("."), lock, probe_merges=True)["orca-mcp"]
        self.assertEqual(result["textual_merge_probe"]["status"], "clean")
        self.assertFalse(result["textual_merge_probe"]["semantic_compatibility_verified"])
        self.assertFalse(result["source_integrated"])
        self.assertIn("merge-tree", run.call_args.args[0])
        self.assertNotIn("merge", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
