"""Offline synthetic coverage for safe publishing handoffs."""
from __future__ import annotations

import builtins
from copy import deepcopy
from datetime import datetime, timezone
from io import BytesIO
import importlib.util
import json
import os
import shutil
from pathlib import Path
import socket
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from unittest.mock import patch

from PIL import Image, PngImagePlugin

ROOT = Path(os.environ.get("SKILL_TEST_ROOT", Path(__file__).resolve().parents[1]))
SKILLS = ROOT / "skills"


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, SKILLS / relative)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


handoff = module("handoff_test", "static-site-handoff/scripts/static_handoff.py")
campaign = module("campaign_test", "social-campaign-proof-tracker/scripts/audit_campaign_package.py")
verifier = module("verifier_test", "remove-ai-image-metadata/scripts/verify_image_cleanup.py")
cleaner = verifier.cleaner_module()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def tree_bytes(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.build = self.root / "build"
        self.build.mkdir()
        (self.build / "index.html").write_text("Example Studio", encoding="utf-8")
        (self.build / "assets").mkdir()
        (self.build / "assets/app.js").write_text("sample()", encoding="utf-8")
        self.state = self.root / "state"

    def prepare(self, name="package"):
        return handoff.prepare(self.build, self.root / name, self.state)

    def confirm(self, result, name="package"):
        return handoff.confirm(self.root / name, self.state, result["package_id"], True)

    def test_first_full_package_and_input_preservation(self):
        before = tree_bytes(self.build)
        result = self.prepare()
        self.assertEqual(result["snapshot"], result["upload"])
        self.assertEqual(tree_bytes(self.root / "package/upload"), before)
        self.assertEqual(tree_bytes(self.build), before)
        self.assertIsNone(handoff.read_state(self.state)["baseline"])
        self.assertEqual(handoff.verify(self.root / "package"), result)

    def test_hashes_ignore_timestamps_and_unconfirmed_changes_survive(self):
        first = self.prepare()
        self.confirm(first)
        os.utime(self.build / "index.html", (10, 10))
        unchanged = self.prepare("no-change")
        self.assertEqual(unchanged["upload"], {})
        (self.build / "index.html").write_text("Revised", encoding="utf-8")
        second = self.prepare("second")
        third = self.prepare("third")
        self.assertEqual(second["upload"], third["upload"])
        self.assertEqual(set(third["upload"]), {"index.html"})
        with self.assertRaises(handoff.HandoffError):
            self.confirm(second, "second")
        self.confirm(third, "third")

    def test_removed_paths_are_reports_and_reintroduced_files_are_copied(self):
        first = self.prepare()
        self.confirm(first)
        original = (self.build / "assets/app.js").read_bytes()
        (self.build / "assets/app.js").unlink()
        second = self.prepare("second")
        self.assertEqual(second["removed"], ["assets/app.js"])
        self.confirm(second, "second")
        self.assertTrue((self.root / "package/upload/assets/app.js").exists())
        (self.build / "assets/app.js").write_bytes(original)
        third = self.prepare("third")
        self.assertIn("assets/app.js", third["upload"])

    def test_tampering_missing_added_edited_and_manifest(self):
        for variant in ("missing", "added", "edited", "manifest"):
            with self.subTest(variant=variant):
                self.prepare(variant)
                package = self.root / variant
                if variant == "missing":
                    (package / "upload/index.html").unlink()
                elif variant == "added":
                    (package / "upload/extra.html").write_text("extra")
                elif variant == "edited":
                    (package / "upload/index.html").write_text("changed")
                else:
                    data = json.loads((package / "manifest.json").read_text())
                    data["created_at"] = "changed"
                    write(package / "manifest.json", data)
                with self.assertRaises(handoff.HandoffError):
                    handoff.verify(package)

    def test_failure_preserves_existing_state_and_package(self):
        first = self.prepare()
        self.confirm(first)
        before_state, before_package = tree_bytes(self.state), tree_bytes(self.root / "package")
        with patch.object(handoff.shutil, "copyfile", side_effect=OSError("synthetic")):
            (self.build / "index.html").write_text("changed")
            with self.assertRaises(OSError):
                self.prepare("failed")
        self.assertEqual(tree_bytes(self.state), before_state)
        self.assertEqual(tree_bytes(self.root / "package"), before_package)
        self.assertFalse((self.root / "failed").exists())

    def test_state_write_failure_leaves_unconfirmable_orphan(self):
        first = self.prepare()
        before = tree_bytes(self.state)
        save = handoff.save_json
        def fail_state(path, value):
            if path.name == "state.json":
                raise OSError("synthetic")
            save(path, value)
        with patch.object(handoff, "save_json", side_effect=fail_state):
            with self.assertRaises(OSError):
                self.prepare("orphan")
        self.assertEqual(tree_bytes(self.state), before)
        orphan = handoff.verify(self.root / "orphan")
        with self.assertRaises(handoff.HandoffError):
            self.confirm(orphan, "orphan")
        self.assertEqual(handoff.read_state(self.state)["pending"]["id"], first["package_id"])

    def test_empty_export_and_input_changed_mid_copy(self):
        for file in self.build.rglob("*"):
            if file.is_file():
                file.unlink()
        with self.assertRaises(handoff.HandoffError):
            self.prepare()
        (self.build / "index.html").write_text("first")
        copy = handoff.shutil.copyfile
        def changing(source, target):
            result = copy(source, target)
            (self.build / "index.html").write_text("second")
            return result
        with patch.object(handoff.shutil, "copyfile", side_effect=changing):
            with self.assertRaises(handoff.HandoffError):
                self.prepare("changed")
        self.assertFalse((self.root / "changed").exists())

    def test_existing_overlap_network_and_sensitive_files(self):
        self.prepare()
        with self.assertRaises(handoff.HandoffError):
            self.prepare()
        with self.assertRaises(handoff.HandoffError):
            handoff.prepare(self.build, self.build / "nested", self.state)
        with self.assertRaises(handoff.HandoffError):
            handoff.local_path("https://example.com/build")
        for name in (".env", "config.json", "private.pem", "source.js.map"):
            (self.build / name).write_text("synthetic")
            with self.assertRaises(handoff.HandoffError):
                self.prepare("refused")
            (self.build / name).unlink()

    def test_lock_and_acknowledgement(self):
        result = self.prepare()
        with self.assertRaises(handoff.HandoffError):
            handoff.confirm(self.root / "package", self.state, result["package_id"])
        (self.state / ".handoff.lock").mkdir()
        with self.assertRaises(handoff.HandoffError):
            self.confirm(result)
        (self.state / ".handoff.lock").rmdir()
        self.confirm(result)
        with self.assertRaises(handoff.HandoffError):
            self.confirm(result)
        history = handoff.read_state(self.state)["history"]
        self.assertEqual(len(history), 1)
        self.assertIn("not_live", history[0]["evidence"])

    def test_paths_and_reparse_detection(self):
        for value in ("../outside", "/outside", "a/../b", "a\\b", "a:b", "NUL.txt", "trailing."):
            with self.subTest(value=value), self.assertRaises(handoff.HandoffError):
                handoff.relative_name(value)
        real = Path.lstat
        target = self.build / "index.html"
        def changed(path):
            info = real(path)
            if path == target:
                class Reparse:
                    st_mode = info.st_mode
                    st_file_attributes = 0x400
                return Reparse()
            return info
        with patch.object(Path, "lstat", changed), self.assertRaises(handoff.HandoffError):
            handoff.snapshot(self.build)

    def test_symlink_is_refused(self):
        link = self.build / "linked.html"
        try:
            link.symlink_to(self.build / "index.html")
        except OSError:
            self.skipTest("Native link creation unavailable; reparse rejection covered separately.")
        with self.assertRaises(handoff.HandoffError):
            self.prepare()

    def test_unicode_and_cli_json(self):
        (self.build / "café.html").write_text("Example", encoding="utf-8")
        script = SKILLS / "static-site-handoff/scripts/static_handoff.py"
        result = subprocess.run([sys.executable, "-B", str(script), "prepare", "--build-dir", str(self.build),
                                 "--package-dir", str(self.root / "cli"), "--state-dir", str(self.state), "--json"],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["live_deployment"], "unverified")

    @unittest.skipUnless(os.name == "nt", "Windows directory junction coverage")
    def test_real_directory_junction_is_refused(self):
        destination = self.root / "external"
        destination.mkdir()
        (destination / "keep.html").write_text("preserve")
        link = self.build / "junction"
        command = "New-Item -ItemType Junction -Path '" + str(link).replace("'", "''") + "' -Target '" + str(destination).replace("'", "''") + "' | Out-Null"
        result = subprocess.run([shutil.which("pwsh") or "powershell.exe", "-NoProfile", "-Command", command],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, "Temporary junction creation failed")
        with self.assertRaises(handoff.HandoffError):
            self.prepare()
        self.assertEqual((destination / "keep.html").read_text(), "preserve")

    def test_no_network_calls(self):
        with patch.object(socket.socket, "connect", side_effect=AssertionError("network")):
            result = self.prepare()
            self.confirm(result)


class CampaignTests(unittest.TestCase):
    now = datetime(2026, 10, 28, 12, tzinfo=timezone.utc)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "package.json"
        self.approval = self.root / "approval.json"
        self.receipts = self.root / "receipts.json"
        (self.root / "cover.png").write_bytes(b"synthetic-media-bytes")
        self.data = {"schema_version": 1, "provider": "example-provider", "destination": "example-studio",
                     "scheduled_at": None, "posts": [{"copy": "Build with evidence.", "title": "Example",
                     "media": [{"path": "cover.png", "role": "cover", "alt_text": "Example artwork"}]}]}
        write(self.package, self.data)

    def audit(self, approved=False, receipts=False):
        return campaign.audit(self.package, self.approval if approved else None,
                              self.receipts if receipts else None, self.now)

    def approve(self):
        fp = self.audit()["fingerprint"]
        write(self.approval, {"schema_version": 1, "fingerprint": fp, "decision": "approved",
                              "approved_at": "2026-10-28T10:00:00Z"})
        return fp

    def receipt(self, state="published", **changes):
        return {"provider": self.data["provider"], "destination": self.data["destination"],
                "fingerprint": self.audit()["fingerprint"], "state": state,
                "observed_at": "2026-10-28T11:00:00Z", "receipt_id": "example-delivery", **changes}

    def receipts_pack(self, *records):
        write(self.receipts, {"schema_version": 1, "records": records})

    def test_missing_and_matching_approval_never_authorize_action(self):
        self.assertEqual(self.audit()["state"], "prepared")
        self.approve()
        result = self.audit(True)
        self.assertEqual(result["state"], "approved")
        self.assertTrue(result["approval_record_matches"])
        self.assertFalse(result["human_consent_authenticated"])
        self.assertFalse(result["external_action_authorized"])

    def test_every_material_field_changes_fingerprint(self):
        self.approve()
        for field in ("copy", "title", "alt_text", "role", "provider", "destination", "scheduled_at"):
            with self.subTest(field=field):
                changed = deepcopy(self.data)
                if field in {"copy", "title"}:
                    changed["posts"][0][field] += "!"
                elif field in {"alt_text", "role"}:
                    changed["posts"][0]["media"][0][field] += "!"
                elif field == "scheduled_at":
                    changed[field] = "2027-01-01T00:00:00Z"
                else:
                    changed[field] += "!"
                write(self.package, changed)
                self.assertFalse(self.audit(True)["approval_record_matches"])
        write(self.package, self.data)

    def test_media_bytes_path_order_and_post_order(self):
        fp = self.approve()
        (self.root / "cover.png").write_bytes(b"new")
        self.assertNotEqual(fp, self.audit()["fingerprint"])
        (self.root / "cover.png").write_bytes(b"synthetic-media-bytes")
        (self.root / "second.png").write_bytes(b"synthetic-media-bytes")
        changed = deepcopy(self.data)
        changed["posts"][0]["media"][0]["path"] = "second.png"
        write(self.package, changed)
        self.assertNotEqual(fp, self.audit()["fingerprint"])
        changed["posts"][0]["media"].append(self.data["posts"][0]["media"][0])
        write(self.package, changed)
        first = self.audit()["fingerprint"]
        changed["posts"][0]["media"].reverse()
        write(self.package, changed)
        self.assertNotEqual(first, self.audit()["fingerprint"])
        changed["posts"].append({"copy": "Second item", "title": "", "media": []})
        write(self.package, changed)
        first = self.audit()["fingerprint"]
        changed["posts"].reverse()
        write(self.package, changed)
        self.assertNotEqual(first, self.audit()["fingerprint"])

    def test_receipt_progression_and_supplied_verification(self):
        self.approve()
        self.receipts_pack(self.receipt("scheduled", observed_at="2026-10-28T09:00:00Z"),
                           self.receipt("published", observed_at="2026-10-28T10:00:00Z"),
                           self.receipt("verified"))
        result = self.audit(True, True)
        self.assertEqual(result["state"], "verified")
        self.assertFalse(result["live_state_verified"])
        self.assertEqual(result["receipt_count"], 3)

    def test_conflicts_are_not_collapsed(self):
        cases = [
            [self.receipt(), self.receipt("failed")],
            [self.receipt(), self.receipt(provider="other-provider")],
            [self.receipt(), self.receipt(destination="another-studio")],
            [self.receipt(), self.receipt(fingerprint="0" * 64)],
            [self.receipt(), self.receipt(receipt_id="second-delivery")],
            [self.receipt(), self.receipt()],
            [self.receipt("uncertain")],
            [self.receipt(observed_at="2027-01-01T00:00:00Z")],
            [self.receipt("verified", observed_at="2026-10-28T09:00:00Z"), self.receipt("scheduled")],
        ]
        for records in cases:
            with self.subTest(records=records):
                self.receipts_pack(*records)
                result = self.audit(receipts=True)
                self.assertEqual(result["state"], "uncertain")
                self.assertEqual(result["receipt_count"], len(records))
                self.assertEqual(result["retry"], "reconcile_before_any_retry")

    def test_empty_receipts_past_schedule_and_failed_receipt(self):
        self.data["scheduled_at"] = "2026-10-28T01:00:00+01:00"
        write(self.package, self.data)
        self.approve()
        self.receipts_pack()
        result = self.audit(True, True)
        self.assertIn("empty_receipts_are_not_cancellation_evidence", result["findings"])
        self.assertIn("past_schedule_requires_review_not_post_now", result["findings"])
        self.receipts_pack(self.receipt("failed"))
        self.assertEqual(self.audit(True, True)["state"], "failed")
        self.assertFalse(self.audit(True, True)["external_action_authorized"])

    def test_rejected_future_approval_and_missing_offset(self):
        self.approve()
        data = json.loads(self.approval.read_text())
        data["decision"] = "rejected"
        write(self.approval, data)
        self.assertFalse(self.audit(True)["approval_record_matches"])
        data["decision"] = "approved"
        data["approved_at"] = "2027-01-01T00:00:00Z"
        write(self.approval, data)
        self.assertFalse(self.audit(True)["approval_record_matches"])
        self.data["scheduled_at"] = "2027-01-01T00:00:00"
        write(self.package, self.data)
        with self.assertRaises(campaign.AuditError):
            self.audit()

    def test_strict_schema_paths_and_no_network_or_writes(self):
        before = tree_bytes(self.root)
        with patch.object(socket.socket, "connect", side_effect=AssertionError("network")):
            self.audit()
        self.assertEqual(tree_bytes(self.root), before)
        for path in ("../outside.png", "https://example.com/a.png", ".env", "a/../cover.png"):
            self.data["posts"][0]["media"][0]["path"] = path
            write(self.package, self.data)
            with self.assertRaises(campaign.AuditError):
                self.audit()
        self.package.write_text('{"schema_version":1,"schema_version":1}')
        with self.assertRaises(campaign.AuditError):
            self.audit()

    def test_json_output_is_redacted(self):
        self.package.write_text("PRIVATE_SYNTHETIC_BAD_JSON")
        result = subprocess.run([sys.executable, "-B", str(SKILLS / "social-campaign-proof-tracker/scripts/audit_campaign_package.py"),
                                 "--package", str(self.package), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("PRIVATE_SYNTHETIC", result.stdout + result.stderr)
        self.assertNotIn(str(self.root), result.stdout + result.stderr)
        json.loads(result.stdout)


class ImageVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def pair(self, kind="PNG", **options):
        source, output = self.root / "before", self.root / "after"
        frame = Image.new("RGBA" if kind != "JPEG" else "RGB", (24, 16), (20, 100, 150))
        if kind == "PNG":
            info = PngImagePlugin.PngInfo()
            info.add_text("Software", "OpenAI synthetic generator")
            info.add_text("Copyright", "Example Studio")
            options.setdefault("pnginfo", info)
        frame.save(source, format=kind, **options)
        result = cleaner.clean_bytes(source.read_bytes(), Path("image"), False)
        output.write_bytes(result.cleaned)
        return source, output

    def test_static_formats_and_read_only(self):
        for kind in ("PNG", "JPEG", "WEBP", "GIF"):
            with self.subTest(kind=kind):
                source, output = self.pair(kind)
                before = tree_bytes(self.root)
                result = verifier.verify(source, output)
                self.assertEqual(result["status"], "pass", result)
                self.assertEqual(tree_bytes(self.root), before)

    def test_residual_metadata_and_unrelated_rights_change(self):
        source, output = self.pair()
        output.write_bytes(source.read_bytes())
        self.assertEqual(verifier.verify(source, output)["checks"]["supported_metadata_absent"]["status"], "fail")
        source, output = self.pair()
        image = Image.open(output)
        info = PngImagePlugin.PngInfo()
        info.add_text("Copyright", "Different attribution")
        image.save(output, format="PNG", pnginfo=info)
        self.assertEqual(verifier.verify(source, output)["checks"]["selective_changes_only"]["status"], "fail")

    def test_pixel_dimension_and_transparency_changes(self):
        source, output = self.pair()
        Image.new("RGBA", (25, 16), (20, 100, 150, 80)).save(output, format="PNG")
        result = verifier.verify(source, output)
        self.assertEqual(result["status"], "fail")
        for name in ("dimensions", "decoded_frames", "transparency", "encoded_payload"):
            self.assertEqual(result["checks"][name]["status"], "fail")

    def test_exif_orientation_and_icc(self):
        exif = Image.Exif()
        exif[274] = 6
        source, output = self.pair("JPEG", exif=exif, icc_profile=b"synthetic-colour-profile")
        self.assertEqual(verifier.verify(source, output)["status"], "pass")
        changed = Image.open(output)
        exif[274] = 1
        changed.save(output, format="JPEG", exif=exif, icc_profile=b"other-profile")
        result = verifier.verify(source, output)
        self.assertEqual(result["checks"]["orientation"]["status"], "fail")
        self.assertEqual(result["checks"]["colour_information"]["status"], "fail")

    def test_animated_png_webp_gif_and_timing_loop(self):
        for kind in ("PNG", "WEBP", "GIF"):
            with self.subTest(kind=kind):
                source, output = self.root / "before", self.root / "after"
                first = Image.new("RGBA", (12, 12), (255, 0, 0, 255))
                second = Image.new("RGBA", (12, 12), (0, 0, 255, 100))
                first.save(source, format=kind, save_all=True, append_images=[second],
                           duration=[100, 200], loop=2)
                output.write_bytes(cleaner.clean_bytes(source.read_bytes(), Path("image"), False).cleaned)
                self.assertEqual(verifier.verify(source, output)["status"], "pass")
                first.save(output, format=kind, save_all=True, append_images=[second],
                           duration=[100, 300], loop=3)
                result = verifier.verify(source, output)
                self.assertEqual(result["checks"]["frame_timing"]["status"], "fail")
                self.assertEqual(result["checks"]["loop_behaviour"]["status"], "fail")

    def test_missing_pillow_is_unverified(self):
        source, output = self.pair()
        original_import = builtins.__import__
        def missing(name, *args, **kwargs):
            if name == "PIL":
                raise ImportError("synthetic")
            return original_import(name, *args, **kwargs)
        with patch.object(builtins, "__import__", side_effect=missing):
            result = verifier.verify(source, output)
        self.assertEqual(result["status"], "unverified")
        self.assertEqual(result["checks"]["decoded_frames"]["reason"], "pillow_unavailable")

    def test_corrupt_unsupported_and_limits_cannot_pass(self):
        source, output = self.root / "before", self.root / "after"
        source.write_bytes(b"not an image")
        output.write_bytes(source.read_bytes())
        self.assertNotEqual(verifier.verify(source, output)["status"], "pass")
        Image.new("RGB", (10, 10)).save(source, format="TIFF")
        output.write_bytes(source.read_bytes())
        self.assertEqual(verifier.verify(source, output)["status"], "unverified")
        source, output = self.pair()
        with patch.object(verifier, "MAX_DECODED_PIXELS", 1):
            self.assertEqual(verifier.verify(source, output)["status"], "unverified")
        with patch.object(verifier, "MAX_FILE_BYTES", 1):
            self.assertEqual(verifier.verify(source, output)["status"], "unverified")

    def test_unsupported_jumbf_is_not_silently_removed(self):
        source, output = self.pair("JPEG")
        blob = source.read_bytes()
        source.write_bytes(blob[:2] + cleaner.jpeg_segment(0xEB, b"JPsynthetic") + blob[2:])
        output.write_bytes(source.read_bytes())
        result = verifier.verify(source, output)
        self.assertNotEqual(result["status"], "pass")
        self.assertEqual(result["checks"]["supported_metadata_absent"]["status"], "unverified")

    def test_malformed_valid_crc_png_is_unverified_without_traceback(self):
        def chunk(kind, payload):
            return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
        source = self.root / "malformed.png"
        source.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", b"bad") + chunk(b"IDAT", b"x") + chunk(b"IEND", b""))
        result = verifier.verify(source, source)
        self.assertEqual(result["status"], "unverified")
        script = SKILLS / "remove-ai-image-metadata/scripts/verify_image_cleanup.py"
        command = subprocess.run([sys.executable, "-B", str(script), str(source), str(source), "--json"], capture_output=True, text=True)
        self.assertEqual(command.returncode, 2)
        self.assertEqual(command.stderr, "")
        self.assertNotIn(str(self.root), command.stdout)

    def test_json_cli_and_no_raw_metadata(self):
        source, output = self.pair()
        script = SKILLS / "remove-ai-image-metadata/scripts/verify_image_cleanup.py"
        result = subprocess.run([sys.executable, "-B", str(script), str(source), str(output), "--json"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "pass")
        self.assertNotIn("Example Studio", result.stdout)
        self.assertNotIn(str(self.root), result.stdout)


if __name__ == "__main__":
    unittest.main()

