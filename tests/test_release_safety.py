"""Synthetic, offline regressions for release safety and evidence review."""
import contextlib
import copy
from datetime import datetime, timezone
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


scanner = load("release_scanner", "skills/github-safe-publisher/scripts/scan_public_safety.py")
installer = load("safe_installer", "tools/install_skills.py")
backup = load("backup_auditor", "skills/backup-readiness-auditor/scripts/audit_backup.py")


class ScannerTests(unittest.TestCase):
    def test_baseline_file_content_is_scanned(self):
        marker = "gh" + "p_" + "C" * 30
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / scanner.BASELINE_FILENAME).write_text(json.dumps({"findings": [], "extra": marker}), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                status = scanner.main([str(root), "--no-baseline", "--json"])
            self.assertEqual(status, 1)
            self.assertTrue(any(f["severity"] == "block" for f in json.loads(out.getvalue())))
            self.assertNotIn(marker, out.getvalue())

    def test_text_json_and_baseline_never_repeat_match(self):
        marker = "gh" + "p_" + "A" * 30
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "example.txt").write_text("token = " + marker, encoding="utf-8")
            original = (root / "example.txt").read_bytes()
            for extra in ([], ["--json"], ["--write-baseline"]):
                out = io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                    try:
                        status = scanner.main([str(root), "--no-baseline", *extra])
                    except SystemExit as exc:
                        status = exc.code
                self.assertNotEqual(status, 0)
                self.assertNotIn(marker, out.getvalue())
                self.assertNotIn(str(root), out.getvalue())
            self.assertEqual(original, (root / "example.txt").read_bytes())
            self.assertFalse((root / scanner.BASELINE_FILENAME).exists())

    def test_legacy_review_fingerprint_and_block_cannot_be_suppressed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            line = "token is an intentional example"
            (root / "a.md").write_text(line, encoding="utf-8")
            found = scanner.scan(root)[0]
            legacy = scanner.Finding("review", "a.md", 1, "credential keyword", line)
            self.assertEqual(scanner.finding_fingerprint(found), scanner.finding_fingerprint(legacy))
            self.assertEqual(scanner.apply_baseline([found], {scanner.finding_fingerprint(legacy)}), ([], 1))
            blocked = scanner.Finding("block", "a.md", 1, "test", "withheld")
            self.assertEqual(scanner.apply_baseline([blocked], {scanner.finding_fingerprint(blocked)}), ([blocked], 0))

    def test_invalid_baseline_does_not_echo_content_or_path(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "baseline.json"
            path.write_text("{sensitive-example", encoding="utf-8")
            with self.assertRaises(SystemExit) as caught:
                scanner.load_baseline(path)
            self.assertNotIn(str(path), str(caught.exception))
            self.assertNotIn("sensitive-example", str(caught.exception))

    def test_binary_oversized_and_directory_baselines_are_redacted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "baseline.json"
            for raw in (b"\xff", b"x" * 2097153):
                path.write_bytes(raw)
                with self.assertRaises(SystemExit) as caught:
                    scanner.load_baseline(path)
                self.assertNotIn(str(path), str(caught.exception))
            with self.assertRaises(SystemExit):
                scanner.load_baseline(Path(temp))

    def test_ci_wrapper_redacts_blocking_filenames(self):
        check = load("release_ci_check", "tools/check_public_safety.py")
        marker = "gh" + "p_" + "D" * 30
        found = scanner.Finding("block", marker + ".md", 1, "test", "Matched content withheld.")
        out = io.StringIO()
        with patch.object(check, "load_scanner", return_value=scanner), patch.object(scanner, "scan", return_value=[found]):
            with contextlib.redirect_stdout(out):
                self.assertEqual(check.main(), 1)
        self.assertNotIn(marker, out.getvalue())

    def test_read_error_is_blocking_and_redacted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "a.md"
            path.write_text("hello", encoding="utf-8")
            with patch.object(Path, "read_text", side_effect=PermissionError("sensitive-detail")):
                found = scanner.scan_file(path, path.parent)
            self.assertEqual(found[0].severity, "block")
            self.assertNotIn("sensitive-detail", found[0].detail)

    def test_link_is_not_read(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "a.md"
            path.write_text("hello", encoding="utf-8")
            with patch.object(scanner, "is_link", return_value=True), patch.object(Path, "read_text", side_effect=AssertionError("read")):
                self.assertEqual(scanner.scan(path)[0].kind, "linked input")

    def test_filename_and_single_file_locations_are_redacted(self):
        marker = "gh" + "p_" + "B" * 30
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / (marker + ".md")
            path.write_text("token example", encoding="utf-8")
            text = json.dumps([scanner.public_finding(f) for f in scanner.scan(root)])
            self.assertNotIn(marker, text)
            self.assertEqual(scanner.scan(path)[0].path, "<input>")


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.source = self.root / "skills" / "sample-skill"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text("Fictional first version", encoding="utf-8")
        self.target = self.base / "installed"

    def run_install(self, **kwargs):
        return installer.install(self.root, self.target, ["sample-skill"], **kwargs)

    def test_dry_run_writes_nothing(self):
        result = self.run_install(dry_run=True)
        self.assertEqual(result[0]["action"], "install")
        self.assertFalse(self.target.exists())

    def test_unreadable_directory_fails_closed(self):
        def denied_walk(_root, **kwargs):
            kwargs["onerror"](PermissionError("private directory detail"))
            return iter(())
        with patch.object(installer.os, "walk", denied_walk), self.assertRaises(ValueError) as caught:
            self.run_install()
        self.assertNotIn("private directory detail", str(caught.exception))
        self.assertFalse(self.target.exists())

    def test_fresh_install_and_idempotence(self):
        self.run_install()
        before = installer.inventory(self.target / "sample-skill", True)
        self.assertEqual(self.run_install()[0]["action"], "unchanged")
        self.assertEqual(before, installer.inventory(self.target / "sample-skill", True))

    def test_unmanaged_and_locally_modified_are_preserved(self):
        self.run_install()
        destination = self.target / "sample-skill"
        (destination / "SKILL.md").write_text("Private variation", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.run_install(replace=True)
        self.assertEqual((destination / "SKILL.md").read_text(), "Private variation")
        (destination / installer.RECEIPT).unlink()
        with self.assertRaises(ValueError):
            self.run_install(replace=True)

    def test_replace_requires_opt_in_and_keeps_backup(self):
        self.run_install()
        (self.source / "SKILL.md").write_text("Fictional second version", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.run_install()
        self.run_install(replace=True)
        copies = list(self.target.glob(".sample-skill.backup-*"))
        self.assertEqual(len(copies), 1)
        self.assertEqual((copies[0] / "SKILL.md").read_text(), "Fictional first version")
        self.assertEqual((self.target / "sample-skill" / "SKILL.md").read_text(), "Fictional second version")

    def test_all_selection_preflight_prevents_partial_install(self):
        other = self.root / "skills" / "second-skill"
        other.mkdir()
        (other / "SKILL.md").write_text("Second", encoding="utf-8")
        conflict = self.target / "second-skill"
        conflict.mkdir(parents=True)
        with self.assertRaises(ValueError):
            installer.install(self.root, self.target, ["sample-skill", "second-skill"])
        self.assertFalse((self.target / "sample-skill").exists())

    def test_traversal_overlap_and_reserved_receipt(self):
        with self.assertRaises(ValueError):
            installer.install(self.root, self.target, ["../outside"])
        with self.assertRaises(ValueError):
            installer.install(self.root, self.root / "skills", ["sample-skill"])
        (self.source / installer.RECEIPT).write_text("{}", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.run_install()

    def test_copy_failure_does_not_touch_existing_copy(self):
        self.run_install()
        (self.source / "SKILL.md").write_text("Changed", encoding="utf-8")
        original = Path.read_bytes
        calls = 0
        def unstable(path):
            nonlocal calls
            if path == self.source / "SKILL.md":
                calls += 1
                if calls > 1:
                    raise OSError("synthetic copy failure")
            return original(path)
        with patch.object(Path, "read_bytes", unstable), self.assertRaises(OSError):
            self.run_install(replace=True)
        self.assertEqual((self.target / "sample-skill" / "SKILL.md").read_text(), "Fictional first version")

    def test_linked_target_and_dangling_link_are_refused(self):
        other = self.base / "other"
        other.mkdir()
        self.target.mkdir()
        link = self.target / "sample-skill"
        try:
            link.symlink_to(other, target_is_directory=True)
        except OSError:
            self.skipTest("Native symlink creation unavailable")
        try:
            with self.assertRaises(ValueError):
                self.run_install(replace=True)
            other.rmdir()
            with self.assertRaises(ValueError):
                self.run_install()
        finally:
            link.unlink()

    @unittest.skipUnless(os.name == "nt", "Windows junction integration")
    def test_windows_junction_is_preserved(self):
        shell = shutil.which("pwsh")
        if not shell:
            self.fail("PowerShell is required for Windows junction coverage")
        other = self.base / "other"
        other.mkdir()
        (other / "sentinel.txt").write_text("keep", encoding="utf-8")
        self.target.mkdir()
        link = self.target / "sample-skill"
        subprocess.run([shell, "-NoProfile", "-Command",
                        "New-Item -ItemType Junction -Path '" + str(link) + "' -Target '" + str(other) + "' | Out-Null"],
                       check=True, capture_output=True)
        try:
            with self.assertRaises(ValueError):
                self.run_install(replace=True)
            self.assertEqual((other / "sentinel.txt").read_text(), "keep")
            self.assertEqual(scanner.scan(link)[0].kind, "linked input")
            with patch.object(scanner, "load_baseline", wraps=scanner.load_baseline) as reader:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(scanner.main([str(link), "--json"]), 1)
                self.assertIsNone(reader.call_args.args[0])
            with self.assertRaises(OSError):
                scanner.load_baseline(link / scanner.BASELINE_FILENAME)
            with self.assertRaises(ValueError):
                backup.load_pack(link / "sentinel.txt")
        finally:
            os.rmdir(link)

    def test_failed_swap_restores_original(self):
        self.run_install()
        (self.source / "SKILL.md").write_text("Changed", encoding="utf-8")
        original = Path.rename
        def fail_swap(path, target):
            if path.name.startswith(".jqai-stage-"):
                raise OSError("synthetic rename failure")
            return original(path, target)
        with patch.object(Path, "rename", fail_swap), self.assertRaises(OSError):
            self.run_install(replace=True)
        self.assertEqual((self.target / "sample-skill" / "SKILL.md").read_text(), "Fictional first version")

    def test_shell_entrypoints(self):
        commands = []
        if shutil.which("pwsh"):
            commands.append([shutil.which("pwsh"), "-NoProfile", "-File", str(ROOT / "install.ps1"),
                             "backup-readiness-auditor", "-Target"])
        bash = shutil.which("bash")
        if not bash and os.name == "nt" and shutil.which("git"):
            candidate = Path(shutil.which("git")).parent.parent / "bin/bash.exe"
            if candidate.exists():
                bash = str(candidate)
        if bash:
            commands.append([bash, str(ROOT / "install.sh"), "backup-readiness-auditor", "--target"])
        self.assertTrue(commands, "At least one shell wrapper must be tested")
        for index, command in enumerate(commands):
            target = self.base / ("wrapper-" + str(index))
            result = subprocess.run([*command, str(target)], capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "backup-readiness-auditor" / "SKILL.md").is_file())
            result = subprocess.run([*command, str(target)], capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("unchanged", result.stdout)

    def test_complete_library_install_in_disposable_target(self):
        names = sorted(p.name for p in (ROOT / "skills").iterdir()
                       if installer.NAME.fullmatch(p.name) and (p / "SKILL.md").is_file())
        self.assertGreaterEqual(len(names), 47)
        plans = installer.install(ROOT, self.target, names, dry_run=True)
        self.assertEqual(len(plans), len(names))
        self.assertFalse(self.target.exists())
        installer.install(ROOT, self.target, names)
        self.assertTrue(all(item["action"] == "unchanged"
                            for item in installer.install(ROOT, self.target, names)))
        for name in names:
            self.assertEqual(installer.inventory(ROOT / "skills" / name),
                             installer.managed_files(self.target / name, name))


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.pack = json.loads((ROOT / "skills/backup-readiness-auditor/assets/example-evidence.json").read_text())
        self.now = datetime(2026, 10, 14, 12, tzinfo=timezone.utc)

    def test_complete_pack_is_not_independent_or_destructive_authority(self):
        before = copy.deepcopy(self.pack)
        result = backup.audit(self.pack, self.now)
        self.assertEqual(result["verdict"], "EVIDENCE_COMPLETE")
        self.assertFalse(result["independently_verified"])
        self.assertFalse(result["destructive_action_authorized"])
        self.assertEqual(before, self.pack)

    def test_known_failures_block(self):
        for key in ("hash_mismatches", "read_errors", "cloud_only_files", "unresolved_links"):
            with self.subTest(key=key):
                data = copy.deepcopy(self.pack)
                data["records"][0][key] = 1
                self.assertEqual(backup.audit(data, self.now)["verdict"], "BLOCKED")
        self.pack["records"][0]["verified_files"] = 11
        self.assertEqual(backup.audit(self.pack, self.now)["verdict"], "BLOCKED")

    def test_missing_required_capacity_and_independence(self):
        for mutate in (lambda p: p["required_ids"].append("missing"),
                       lambda p: p["destination"].update(free_bytes=0),
                       lambda p: p["destination"].update(independent=False),
                       lambda p: p["records"][0].update(restore_test="failed", snapshot_consistent=False)):
            data = copy.deepcopy(self.pack)
            mutate(data)
            self.assertEqual(backup.audit(data, self.now)["verdict"], "BLOCKED")

    def test_unknown_stale_future_and_unrestored_require_review(self):
        for mutate in (lambda p: p.update(scope_complete=False),
                       lambda p: p["destination"].update(independent=None),
                       lambda p: p["records"][0].update(snapshot_consistent=None),
                       lambda p: p["records"][0].update(restore_test="not_run"),
                       lambda p: p["records"][0].update(captured_at="2026-01-01T00:00:00Z"),
                       lambda p: p["records"][0].update(captured_at="2027-01-01T00:00:00Z")):
            data = copy.deepcopy(self.pack)
            mutate(data)
            self.assertEqual(backup.audit(data, self.now)["verdict"], "REVIEW")

    def test_invalid_types_extra_fields_duplicates_and_impossible_counts(self):
        for mutate in (lambda p: p.update(version=True),
                       lambda p: p.update(extra="private information"),
                       lambda p: p["records"].append(copy.deepcopy(p["records"][0])),
                       lambda p: p["records"][0].update(verified_files=13),
                       lambda p: p["records"][0].update(read_errors=True),
                       lambda p: p["records"][0].update(id="../outside")):
            data = copy.deepcopy(self.pack)
            mutate(data)
            with self.assertRaises(ValueError):
                backup.audit(data, self.now)

    def test_freshness_and_capacity_boundaries(self):
        self.pack["destination"]["free_bytes"] = 2000
        self.assertEqual(backup.audit(self.pack, self.now, 1)["verdict"], "EVIDENCE_COMPLETE")
        self.assertEqual(backup.audit(self.pack, self.now, 0)["verdict"], "REVIEW")

    def test_cli_and_input_byte_preservation(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "evidence.json"
            path.write_text(json.dumps(self.pack), encoding="utf-8")
            before = path.read_bytes()
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                result = backup.main(["--input", str(path), "--as-of", self.now.isoformat(), "--json"])
            self.assertEqual(result, 0)
            self.assertEqual(json.loads(out.getvalue())["verdict"], "EVIDENCE_COMPLETE")
            self.assertEqual(before, path.read_bytes())
            self.assertNotIn(str(path), out.getvalue())

    def test_malformed_input_is_not_echoed(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            for raw in ('{"version":1,"version":1}', '{"private-example":', 'x' * 1048577):
                path.write_text(raw, encoding="utf-8")
                out = io.StringIO()
                with contextlib.redirect_stderr(out):
                    status = backup.main(["--input", str(path), "--as-of", self.now.isoformat(), "--json"])
                self.assertEqual(status, 2)
                self.assertNotIn(str(path), out.getvalue())
                self.assertNotIn("private-example", out.getvalue())


if __name__ == "__main__":
    unittest.main()
