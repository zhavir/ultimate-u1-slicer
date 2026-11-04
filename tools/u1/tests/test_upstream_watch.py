import copy
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("upstream_watch", Path(__file__).parents[1] / "upstream_watch.py")
watch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(watch)


class UpstreamWatchTests(unittest.TestCase):
    def setUp(self):
        source = {"url": "https://github.com/example/slicer.git", "sha": "a" * 40, "default_branch": "main"}
        self.lock = {"sources": {"main": source, "mcp": {**source, "branch": "feature/mcp"}}}
        self.calls = []

        def api(endpoint, payload=None):
            self.calls.append((endpoint, payload))
            if "/releases?" in endpoint:
                return [{"id": 10, "tag_name": "v1", "updated_at": "2026-01-01", "html_url": "https://github.com/example/slicer/releases/tag/v1",
                         "prerelease": False, "draft": False}]
            if "/tags?" in endpoint:
                return [{"name": "v1", "commit": {"sha": "a" * 40}}]
            if "/commits/" in endpoint:
                return {"sha": "a" * 40}
            raise AssertionError(endpoint)
        self.api = api
        self.baseline = watch.snapshot(self.lock, self.api)

    def test_unchanged_sources_are_quiet_and_repository_metadata_is_fetched_once(self):
        self.assertEqual(watch.changes(self.lock, self.baseline, self.baseline), [])
        self.assertEqual(sum("/releases?" in endpoint for endpoint, _ in self.calls), 1)
        self.assertTrue(any("feature%2Fmcp" in endpoint for endpoint, _ in self.calls))

    def test_branch_release_edit_and_retag_are_detected_without_duplicate_alias_notifications(self):
        current = copy.deepcopy(self.baseline)
        for value in current["sources"].values():
            value["releases"]["10"]["updated_at"] = "2026-02-01"
            value["tags"]["v0"] = "b" * 40
        current["sources"]["mcp"]["head"] = "c" * 40
        events = watch.changes(self.lock, self.baseline, current)
        self.assertCountEqual([item["kind"] for item in events], ["branch", "release", "tag"])
        self.assertEqual(len({item["fingerprint"] for item in events}), 3)
        current["sources"]["main"]["tags"]["v1"] = "d" * 40
        # The edited release already covers its tag; it does not send a second same-run alert.
        self.assertEqual(len(watch.changes(self.lock, self.baseline, current)), 3)

    def test_closed_issues_deduplicate_events_and_new_issues_notify_only_the_configured_maintainer(self):
        change = watch.event("main", "branch", "main", "b" * 40, "a" * 40, "https://example.invalid/compare")
        another = watch.event("mcp", "branch", "feature/mcp", "c" * 40, "a" * 40, "https://example.invalid/compare")
        mutations = []

        def api(endpoint, payload=None):
            if payload is None:
                self.assertIn("state=all", endpoint)
                return [{"state": "closed", "body": f"<!-- u1-upstream-event:{change['fingerprint']} -->"}]
            mutations.append(payload)
            return {"html_url": "https://example.invalid/issues/1"}
        report = watch.notify("example/ultimate-u1", [change, another], "owner", api)
        self.assertEqual(report["deduplicated"], 1)
        self.assertEqual(len(mutations), 1)
        self.assertEqual(mutations[0]["assignees"], ["owner"])
        self.assertEqual(mutations[0]["labels"], ["upstream-update"])

    def test_notification_limit_does_not_drop_pending_work(self):
        events = [watch.event("main", "branch", str(i), "b", "a", "https://example.invalid") for i in range(3)]

        def api(endpoint, payload=None):
            return {"html_url": "https://example.invalid/1"} if payload else []
        result = watch.notify("example/ultimate-u1", events, api=api, limit=1)
        self.assertEqual(len(result["created"]), 1)
        self.assertEqual(result["deferred"], 2)

    def test_api_failure_is_an_explicit_monitor_error_without_hiding_other_sources(self):
        def api(endpoint, payload=None):
            if "feature%2Fmcp" in endpoint:
                raise RuntimeError("HTTP 404 branch no longer exists")
            return self.api(endpoint, payload)
        current = watch.snapshot(self.lock, api)
        events = watch.changes(self.lock, self.baseline, current)
        self.assertEqual([item["kind"] for item in events], ["monitor-error"])
        self.assertEqual(current["sources"]["main"]["head"], "a" * 40)

    def test_missing_baseline_and_non_github_sources_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing baseline"):
            watch.changes(self.lock, {"sources": {}}, self.baseline)
        with self.assertRaisesRegex(ValueError, "GitHub HTTPS"):
            watch.repository({"url": "https://token@example.invalid/project.git"})


if __name__ == "__main__":
    unittest.main()
