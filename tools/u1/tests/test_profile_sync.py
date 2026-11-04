import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("profile_sync", Path(__file__).parents[1] / "profile_sync.py")
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class ProfileSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "source"
        self.profiles = self.repo / "resources/profiles"
        self.profiles.mkdir(parents=True)
        self.child = {"type": "filament", "name": "Child", "inherits": "Base"}
        self.base = {"name": "Base", "instantiation": "false", "nozzle_temperature": ["220"]}
        self.write_bundle()
        self.run_git("init", "-q")
        self.commit()
        self.destination = self.root / "catalog"

    def run_git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def commit(self):
        self.run_git("add", "resources")
        self.run_git("-c", "user.name=U1 Test", "-c", "user.email=u1-test@example.invalid",
                     "commit", "-qm", "Synthetic profile fixture")
        self.lock = {"sources": {"fixture": {"sha": self.run_git("rev-parse", "HEAD"),
                     "url": "https://example.invalid/fixture", "license": "test-fixture"}}}

    def write_bundle(self, duplicate=False):
        folder = self.profiles / "Test/filament"
        folder.mkdir(parents=True, exist_ok=True)
        for value in [self.base, self.child]:
            (folder / (value["name"] + ".json")).write_text(json.dumps(value))
        entries = [{"name": p["name"], "sub_path": "filament/" + p["name"] + ".json"}
                   for p in [self.base, self.child]]
        if duplicate:
            entries.append(entries[-1])
        (self.profiles / "Test.json").write_text(json.dumps({"name": "Test", "version": "01.00.00.01",
                                                             "filament_list": entries}))

    def synchronize(self):
        return sync.synchronize({"fixture": self.repo}, self.destination, self.lock, ["Test"])

    def test_preserves_inheritance_source_bytes_and_user_overrides(self):
        original = (self.profiles / "Test/filament/Child.json").read_bytes()
        result = self.synchronize()
        snapshot = self.destination / result["sources"]["fixture"]["snapshot"]
        self.assertEqual((snapshot / "profiles/Test/filament/Child.json").read_bytes(), original)
        overrides = self.destination / "overrides"
        overrides.mkdir()
        user = overrides / "custom.json"
        user.write_text('{"user_setting":true}')
        self.assertEqual(self.synchronize(), result)
        self.assertEqual(user.read_text(), '{"user_setting":true}')
        self.assertFalse(result["installed"])
        self.assertEqual(self.run_git("status", "--porcelain"), "")

    def test_pin_and_dirty_source_rejected_before_catalog_creation(self):
        self.lock["sources"]["fixture"]["sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "SHA differs"):
            self.synchronize()
        self.assertFalse(self.destination.exists())
        self.lock["sources"]["fixture"]["sha"] = self.run_git("rev-parse", "HEAD")
        (self.profiles / "Test/filament/Child.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "local changes"):
            self.synchronize()

    def test_snapshot_tampering_is_refused(self):
        result = self.synchronize()
        snapshot = self.destination / result["sources"]["fixture"]["snapshot"]
        (snapshot / "profiles/Test/filament/Child.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "modified"):
            self.synchronize()

    def test_cross_source_collisions_keep_both_namespaces(self):
        self.lock["sources"]["second"] = self.lock["sources"]["fixture"].copy()
        result = sync.synchronize({"fixture": self.repo, "second": self.repo},
                                  self.destination, self.lock, ["Test"])
        self.assertEqual(len(result["collisions"]), 2)
        self.assertEqual(len(result["duplicates"]), 2)
        self.assertEqual(len(result["sources"]), 2)

    def test_missing_requested_vendors_are_reported(self):
        result = sync.synchronize({"fixture": self.repo}, self.destination, self.lock, ["Test", "Missing"])
        self.assertEqual(result["sources"]["fixture"]["missing_vendors"], ["Missing"])

    def test_nested_profile_revision_is_checked_separately_from_parent(self):
        self.lock["sources"]["fixture"]["profiles_sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "pinned profiles submodule"):
            self.synchronize()
        self.assertFalse(self.destination.exists())

    def test_cycles_and_missing_parents_are_refused(self):
        self.base["inherits"] = "Child"
        self.write_bundle()
        with self.assertRaisesRegex(ValueError, "cycle"):
            sync.inventory(self.profiles, ["Test"])
        self.base.pop("inherits")
        self.child["inherits"] = "Absent"
        self.write_bundle()
        with self.assertRaisesRegex(ValueError, "unresolved"):
            sync.inventory(self.profiles, ["Test"])

    def test_duplicate_json_keys_are_refused(self):
        path = self.root / "bad.json"
        path.write_text('{"name":"first","name":"second"}')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            sync.read_json(path)

    def test_repeated_index_entry_is_counted_without_renaming(self):
        self.write_bundle(duplicate=True)
        records, _ = sync.inventory(self.profiles, ["Test"])
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1]["index_occurrences"], 2)

    def test_unmanaged_destination_is_not_overwritten(self):
        self.destination.mkdir()
        original = self.destination / "user.conf"
        original.write_text("preserve")
        with self.assertRaisesRegex(ValueError, "non-empty"):
            self.synchronize()
        self.assertEqual(original.read_text(), "preserve")

    def test_symlink_and_traversal_sources_are_refused(self):
        outside = self.root / "secret.json"
        outside.write_text("{}")
        link = self.profiles / "Test/filament/link.json"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("symlink creation unavailable")
        with self.assertRaisesRegex(ValueError, "escapes|symlink"):
            sync.safe_file(self.profiles, "Test/filament/link.json")
        with self.assertRaisesRegex(ValueError, "unsafe"):
            sync.safe_file(self.profiles, "../secret.json")


if __name__ == "__main__":
    unittest.main()
