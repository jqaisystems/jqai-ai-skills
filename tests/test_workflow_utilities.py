"""Synthetic regression tests. No real inventory or live automation access."""
import contextlib
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import socket
import stat
import struct
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import xml.etree.ElementTree as ET

from PIL import Image
from PIL.PngImagePlugin import PngInfo

ROOT = Path(__file__).resolve().parents[1]


def load(name, skill, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "skills" / skill / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


media = load("media_check", "media-spec-checker", "check_media.py")
recon = load("reconcile", "automation-state-reconciler", "reconcile_snapshots.py")
windows = load("reinstall", "windows-reinstall-planner", "build_reinstall_plan.py")
metadata = load("metadata_clean", "remove-ai-image-metadata", "clean_image_metadata.py")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_cli(module, args):
    return subprocess.run([sys.executable, "-X", "utf8", "-B", module.__file__, *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8", timeout=30)


class MediaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.photo = self.root / "sample.png"
        Image.new("RGB", (80, 40), "blue").save(self.photo)

    def test_inclusive_bounds_and_unchanged_input(self):
        before = digest(self.photo)
        rules = {"image": {"formats": ["png"], "width": {"min": 80, "max": 80},
                           "aspect_ratio": {"min": 2, "max": 2}, "max_bytes": self.photo.stat().st_size}}
        result = media.inspect_file(self.photo, self.root, rules, 5)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(before, digest(self.photo))
        rules["image"]["width"]["max"] = 79
        self.assertEqual(media.inspect_file(self.photo, self.root, rules, 5)["status"], "fail")

    def test_orientation_and_animation(self):
        exif = Image.Exif()
        exif[274] = 6
        rotated = self.root / "rotated.jpg"
        Image.new("RGB", (80, 40)).save(rotated, exif=exif)
        measured = media.image_info(rotated)
        self.assertEqual((measured["width"], measured["height"]), (40, 80))
        animated = self.root / "sample.gif"
        Image.new("RGB", (10, 10), "red").save(animated, save_all=True,
            append_images=[Image.new("RGB", (10, 10), "blue")], duration=[100, 200], loop=0)
        measured = media.image_info(animated)
        self.assertTrue(measured["animated"])
        self.assertAlmostEqual(measured["duration"], .3)

    def test_corrupt_unknown_missing_and_static_duration(self):
        bad = self.root / "bad.jpg"
        bad.write_bytes(b"not a media file")
        rules = {"image": {"width": {"min": 1}, "duration": {"min": 0}}}
        self.assertEqual(media.inspect_file(bad, self.root, rules, 5)["status"], "unverified")
        self.assertEqual(media.inspect_file(self.photo, self.root, rules, 5)["status"], "unverified")
        unknown = self.root / "sample.txt"
        unknown.write_text("fictional")
        self.assertEqual(media.inspect_file(unknown, self.root, rules, 5)["status"], "unverified")
        with patch.dict(sys.modules, {"PIL": None}):
            with self.assertRaises(ValueError):
                media.image_info(self.photo)

    def test_video_missing_timeout_and_rotation(self):
        path = self.root / "sample.mp4"
        path.write_bytes(b"synthetic placeholder")
        with patch.object(media.shutil, "which", return_value=None):
            with self.assertRaisesRegex(ValueError, "unavailable"):
                media.video_info(path, 1)
        with patch.object(media.shutil, "which", return_value="ffprobe"), patch.object(
                media.subprocess, "run", side_effect=subprocess.TimeoutExpired("ffprobe", 1)):
            with self.assertRaisesRegex(ValueError, "timed out"):
                media.video_info(path, 1)
        data = {"format": {"format_name": "mov,mp4", "duration": "2"},
                "streams": [{"codec_type": "video", "codec_name": "h264", "width": 80, "height": 40,
                             "sample_aspect_ratio": "2:1", "side_data_list": [{"rotation": 90}]}]}
        completed = subprocess.CompletedProcess([], 0, json.dumps(data), "")
        with patch.object(media.shutil, "which", return_value="ffprobe"), patch.object(
                media.subprocess, "run", return_value=completed) as runner:
            result = media.video_info(path, 3)
        self.assertEqual(result["width"], 40)
        self.assertEqual(result["aspect_ratio"], .25)
        command = runner.call_args.args[0]
        self.assertEqual(command[command.index("-protocol_whitelist") + 1], "file")
        self.assertFalse(runner.call_args.kwargs.get("shell", False))

    def test_json_cli_and_rules_rejection(self):
        rules = self.root / "rules.json"
        rules.write_text(json.dumps({"schema_version": 1, "image": {"width": {"min": 80}}}))
        result = run_cli(media, [self.photo, "--rules", rules, "--json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["files"][0]["file"], self.photo.name)
        self.assertNotIn(str(self.root), result.stdout)
        with self.assertRaises(ValueError):
            media.validate_rules({"schema_version": 1, "image": {"unknown": True}})
        with self.assertRaises(ValueError):
            media.validate_rules({"schema_version": 1, "image": {"width": {"min": 10, "max": 5}}})
        with self.assertRaises(ValueError):
            media.local_path("https://example.com/sample.mp4")

    def test_missing_video_aspect_is_not_assumed(self):
        data = {"format": {"format_name": "mp4"}, "streams": [
            {"codec_type": "video", "width": 80, "height": 40, "sample_aspect_ratio": "N/A"}]}
        completed = subprocess.CompletedProcess([], 0, json.dumps(data), "")
        with patch.object(media.shutil, "which", return_value="ffprobe"), patch.object(
                media.subprocess, "run", return_value=completed):
            result = media.video_info(self.root / "sample.mp4", 2)
        self.assertIsNone(result["aspect_ratio"])
        self.assertEqual(media.evaluate(result, {"aspect_ratio": {"min": 1}}, "sample.mp4")[0]["status"], "unverified")

    def test_decoder_diagnostics_are_not_exported(self):
        with patch.object(media, "image_info", side_effect=ValueError("Example private tag content")):
            result = media.inspect_file(self.photo, self.root, {"image": {"width": {"min": 1}}}, 3)
        self.assertEqual(result["status"], "unverified")
        self.assertNotIn("private tag", json.dumps(result))

    def test_link_not_followed(self):
        target = self.root / "linked.png"
        try:
            target.symlink_to(self.photo)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation not available")
        self.assertNotIn(target, media.collect(self.root, True))
        with self.assertRaises(ValueError):
            media.local_path(target)

    def test_reparse_attribute_detection_without_symlink_support(self):
        flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        with patch.object(Path, "is_symlink", return_value=False):
            for attributes, expected in ((flag, True), (flag | 0x20, True), (0x20, False)):
                with self.subTest(attributes=attributes), patch.object(
                        Path, "lstat", return_value=SimpleNamespace(st_file_attributes=attributes)):
                    self.assertEqual(media.linked(self.photo), expected)
            with patch.object(Path, "lstat", return_value=SimpleNamespace()):
                self.assertFalse(media.linked(self.photo))

    def test_reparse_file_and_ancestor_are_rejected(self):
        for blocked in (self.photo, self.root):
            with self.subTest(blocked=blocked.name), patch.object(
                    media, "linked", side_effect=lambda path: path == blocked):
                with self.assertRaisesRegex(ValueError, "Linked paths"):
                    media.local_path(self.photo)

    @unittest.skipUnless(sys.platform == "win32", "Windows junction integration test")
    def test_directory_junction_not_followed(self):
        shell = shutil.which("pwsh")
        self.assertIsNotNone(shell, "PowerShell 7 is required for the Windows junction test")
        target = self.root / "target"
        target.mkdir()
        nested = target / "nested.png"
        shutil.copyfile(self.photo, nested)
        before = digest(nested)
        junction = self.root / "linked-directory"
        # Both paths are generated inside this test's disposable directory.
        self.assertEqual(junction.parent, self.root)
        self.assertEqual(target.parent, self.root)
        try:
            subprocess.run([shell, "-NoProfile", "-Command",
                "New-Item -ItemType Junction -Path $env:SKILL_TEST_LINK "
                "-Target $env:SKILL_TEST_TARGET -ErrorAction Stop | Out-Null"],
                env={**os.environ, "SKILL_TEST_LINK": str(junction), "SKILL_TEST_TARGET": str(target)},
                check=True, capture_output=True, text=True, timeout=20)
            self.assertTrue(media.linked(junction))
            self.assertEqual(media.collect(self.root, True), sorted([self.photo, nested]))
            for path in (junction, junction / nested.name):
                with self.subTest(path=path.name), self.assertRaisesRegex(ValueError, "Linked paths"):
                    media.local_path(path)
            self.assertEqual(digest(nested), before)
        finally:
            # Remove only the junction itself, never recursively remove its target.
            if os.path.lexists(junction):
                junction.rmdir()
        self.assertTrue(nested.is_file())
        self.assertEqual(digest(nested), before)

    def test_failure_and_unknown_are_both_visible(self):
        rules = self.root / "rules.json"
        rules.write_text(json.dumps({"schema_version": 1, "image": {"width": {"min": 100}, "duration": {"min": 1}}}))
        result = run_cli(media, [self.photo, "--rules", rules, "--json"])
        self.assertEqual(result.returncode, 2)
        report = json.loads(result.stdout)
        self.assertEqual(report["counts"]["fail"], 1)
        self.assertEqual(report["check_counts"]["unverified"], 1)
        self.assertTrue(report["has_unverified"])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg and ffprobe required")
    def test_real_synthetic_video(self):
        video = self.root / "sample.mp4"
        subprocess.run([shutil.which("ffmpeg"), "-v", "error", "-f", "lavfi", "-i",
                        "color=c=blue:s=80x40:d=1", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(video)],
                       check=True, capture_output=True, timeout=20)
        before = digest(video)
        result = media.inspect_file(video, self.root, {"video": {"codecs": ["h264"],
                                    "duration": {"min": .9, "max": 1.1}}}, 10)
        self.assertEqual(result["status"], "pass", result)
        self.assertEqual(digest(video), before)


NOW = datetime(2026, 1, 2, 12, tzinfo=timezone.utc)


def snapshot(rows, **overrides):
    result = {"schema_version": 1, "captured_at": NOW.isoformat(), "complete": True,
              "max_age_hours": 24, "compare_fields": ["status", "title"], "records": rows}
    result.update(overrides)
    return result


def record(identifier, title="Example item", status="ready", **extra):
    return {"id": identifier, "values": {"status": status, "title": title}, **extra}


class ReconciliationTests(unittest.TestCase):

    def test_network_input_rejected_before_read(self):
        with patch.object(Path, "read_text", side_effect=AssertionError("Must not read")):
            with self.assertRaises(ValueError):
                recon.read_json(Path(r"\\example.invalid\share\source.json"))
        with self.assertRaises(ValueError):
            recon.receipt_index({"schema_version": True, "records": []}, NOW)
    def test_classifications_and_no_network_or_input_mutation(self):
        source = snapshot([record("same"), record("new"), record("edit", "Updated"),
                           record("dup-a", content_hash="fictional-shared")])
        local = snapshot([record("same"), record("missing"), record("edit", "Original"),
                          record("dup-b", content_hash="fictional-shared")])
        before = json.dumps([source, local], sort_keys=True)
        with patch.object(socket, "socket", side_effect=AssertionError("No network")):
            result = recon.reconcile(source, local, now=NOW)
        actual = {r["id"]: r["classification"] for r in result["records"]}
        self.assertEqual(actual, {"same": "unchanged", "new": "new", "edit": "changed",
                                 "missing": "missing-from-source", "dup-a": "duplicate", "dup-b": "duplicate"})
        self.assertEqual(before, json.dumps([source, local], sort_keys=True))
        self.assertFalse(result["mutations_performed"])

    def test_incomplete_absence_and_empty_stale_snapshots(self):
        result = recon.reconcile(snapshot([], complete=False), snapshot([record("item")]), now=NOW)
        self.assertEqual(result["records"][0]["classification"], "ambiguous")
        old = snapshot([], captured_at=(NOW - timedelta(days=3)).isoformat())
        self.assertTrue(recon.reconcile(old, snapshot([]), now=NOW)["review_required"])
        future = snapshot([record("item")], captured_at=(NOW + timedelta(hours=1)).isoformat())
        self.assertEqual(recon.reconcile(future, snapshot([]), now=NOW)["records"][0]["classification"], "ambiguous")

    def test_duplicate_id_missing_field_and_type_changes(self):
        result = recon.reconcile(snapshot([record("item"), record("item")]), snapshot([]), now=NOW)
        self.assertEqual(result["records"][0]["classification"], "ambiguous")
        row = record("item")
        del row["values"]["title"]
        self.assertEqual(recon.reconcile(snapshot([row]), snapshot([record("item")]), now=NOW)["records"][0]["classification"], "ambiguous")
        a, b = record("item", title=True), record("item", title=1)
        self.assertEqual(recon.reconcile(snapshot([a]), snapshot([b]), now=NOW)["records"][0]["classification"], "changed")

    def test_absence_and_receipt_ambiguity_precede_duplicates(self):
        source = snapshot([record("new", content_hash="same")])
        local = snapshot([record("existing", content_hash="same")], complete=False)
        result = recon.reconcile(source, local, now=NOW)
        self.assertEqual(next(r for r in result["records"] if r["id"] == "new")["classification"], "ambiguous")
        local["complete"] = True
        receipts = {"schema_version": 1, "records": [{"id": "new", "status": "published", "observed_at": NOW.isoformat()}]}
        result = recon.reconcile(source, local, receipts, NOW)
        row = next(r for r in result["records"] if r["id"] == "new")
        self.assertEqual(row["classification"], "ambiguous")
        self.assertTrue(any("recover history" in reason for reason in row["reasons"]))

    def test_receipt_conflict_and_protection(self):
        receipts = {"schema_version": 1, "records": [
            {"id": "item", "status": "published", "observed_at": NOW.isoformat()},
            {"id": "item", "status": "failed", "observed_at": NOW.isoformat()}]}
        result = recon.reconcile(snapshot([record("item")]), snapshot([record("item")]), receipts, NOW)
        row = result["records"][0]
        self.assertEqual(row["classification"], "ambiguous")
        self.assertTrue(row["history_protected"])
        receipts["records"] = receipts["records"][:1]
        self.assertEqual(recon.reconcile(snapshot([]), snapshot([]), receipts, NOW)["records"][0]["classification"], "ambiguous")

    def test_validation_and_cli(self):
        with self.assertRaises(ValueError):
            recon.reconcile(snapshot([]), snapshot([], compare_fields=["title"]), now=NOW)
        with self.assertRaises(ValueError):
            recon.reconcile(snapshot([], captured_at="2026-01-02"), snapshot([]), now=NOW)
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "source.json", Path(tmp) / "local.json"
            fresh = snapshot([], captured_at=datetime.now(timezone.utc).isoformat())
            a.write_text(json.dumps(fresh)); b.write_text(json.dumps(fresh))
            before = digest(a), digest(b)
            result = run_cli(recon, ["--source", a, "--local", b, "--json"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)["review_required"])
            self.assertEqual(before, (digest(a), digest(b)))


def software(identifier, name="Example Editor", source="registry-user", **extra):
    result = {"record_id": identifier, "source": source, "name": name, "version": "",
              "publisher": "Example Studio", "package_id": "",
              "evidence": "shortcut-only" if source == "start-menu" else "registered"}
    result.update(extra)
    return result


def inventory(rows):
    return {"schema_version": 1, "captured_at": NOW.isoformat(), "records": rows,
            "coverage": [
                {"source": "Registry", "status": "complete", "count": sum(r["source"].startswith("registry-") for r in rows)},
                {"source": "Store", "status": "complete", "count": sum(r["source"] == "store-current-user" for r in rows)},
                {"source": "StartMenu", "status": "complete", "count": sum(r["source"] == "start-menu" for r in rows)}]}


class ReinstallTests(unittest.TestCase):
    def test_malformed_coverage_and_network_input(self):
        data = inventory([software("a")])
        data["coverage"][0]["status"] = []
        with self.assertRaises(ValueError):
            windows.validate(data)
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli(windows, ["--input", r"\\example.invalid\share\inventory.json", "--output-dir", Path(tmp) / "reports"])
            self.assertEqual(result.returncode, 2)
            self.assertIn("local file", result.stderr)
    def test_groups_preserve_evidence_and_versions(self):
        rows = [software("a", version="1.01"), software("b", version="2.00"),
                software("c", publisher="Other Studio"), software("d", source="start-menu", publisher="")]
        self.assertEqual(len(windows.groups(rows)), 3)
        outputs = windows.render(inventory(rows))
        self.assertIn("1.01, 2.00", outputs["reinstall-checklist.md"])
        self.assertIn("Version unknown", outputs["reinstall-checklist.md"])
        self.assertIn("Shortcut only", outputs["reinstall-checklist.md"])
        self.assertEqual(outputs["software-inventory.csv"].count("Undecided"), 4)

    def test_partial_coverage_and_formula_safety(self):
        data = inventory([software("a", "=SUM(1,2)"), software("b", "Cr\u00e8me Editor")])
        data["coverage"][1]["status"] = "unavailable"
        outputs = windows.render(data)
        self.assertIn("Store: unavailable", outputs["coverage-report.md"])
        self.assertIn("'=SUM", outputs["software-inventory.csv"])
        self.assertIn("Cr\u00e8me", outputs["reinstall-checklist.md"])
        for value in ["=1", "+1", "-1", "@value", "\tname", "  =1"]:
            self.assertTrue(windows.cell(value).startswith("'"))
        data["coverage"][0]["count"] = 9
        with self.assertRaises(ValueError):
            windows.validate(data)

    def test_missing_publishers_do_not_establish_identity(self):
        rows = [software("a", publisher=""), software("b", publisher="", source="start-menu")]
        self.assertEqual(len(windows.groups(rows)), 2)

    def test_unique_ids_and_no_overwrite(self):
        with self.assertRaises(ValueError):
            windows.validate(inventory([software("same"), software("same")]))
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "reports"
            result = windows.write_reports(inventory([software("a")]), output)
            self.assertEqual(len(result), 3)
            before = {p.name: digest(p) for p in output.iterdir()}
            with self.assertRaises(ValueError):
                windows.write_reports(inventory([software("b")]), output)
            self.assertEqual(before, {p.name: digest(p) for p in output.iterdir()})

    def test_cli_does_not_change_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "inventory.json"
            source.write_text(json.dumps(inventory([software("a")])))
            before = digest(source)
            result = run_cli(windows, ["--input", source, "--output-dir", Path(tmp) / "reports"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)["software_changed"])
            self.assertEqual(before, digest(source))


XMP = b'''<x:xmpmeta xmlns:x="adobe:ns:meta/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
 xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:tiff="http://ns.adobe.com/tiff/1.0/"><rdf:RDF>
 <rdf:Description xmp:CreatorTool="OpenAI" dc:rights="Example Studio" tiff:Orientation="6">
 <dc:creator><rdf:Seq><rdf:li>Example Builder</rdf:li></rdf:Seq></dc:creator>
 <dc:title><rdf:Alt><rdf:li>ChatGPT Image sample</rdf:li><rdf:li>Keep this title</rdf:li></rdf:Alt></dc:title>
 </rdf:Description></rdf:RDF></x:xmpmeta>'''


def encoded_image(fmt, **kwargs):
    buffer = io.BytesIO()
    Image.new("RGB", (16, 12), "green").save(buffer, format=fmt, **kwargs)
    return buffer.getvalue()


def photoshop_resource(identifier, data):
    return b"8BIM" + struct.pack(">H", identifier) + b"\0\0" + struct.pack(">I", len(data)) + data + (b"\0" if len(data) & 1 else b"")


class MetadataTests(unittest.TestCase):
    def verify_pixels(self, before, after):
        with Image.open(io.BytesIO(before)) as a, Image.open(io.BytesIO(after)) as b:
            self.assertEqual(a.size, b.size)
            self.assertEqual(a.convert("RGB").tobytes(), b.convert("RGB").tobytes())

    def test_jpeg_selective_attributes_and_records(self):
        jpeg = encoded_image("JPEG")
        before = jpeg[:2] + metadata.jpeg_segment(0xE1, metadata.XMP_HEADER + XMP) + jpeg[2:]
        result = metadata.clean_bytes(before, Path("sample.jpg"), False)
        self.assertTrue(result.removals)
        self.assertNotIn(b"OpenAI", result.cleaned)
        self.assertNotIn(b"ChatGPT", result.cleaned)
        for text in (b"Example Studio", b"Example Builder", b"Keep this title", b'Orientation="6"'):
            self.assertIn(text, result.cleaned)
        self.assertEqual(result.encoded_hash, metadata.encoded_hash_for(result.cleaned, Path("sample.jpg")))
        self.assertEqual(result.cleaned, metadata.clean_bytes(result.cleaned, Path("sample.jpg"), False).cleaned)
        self.verify_pixels(before, result.cleaned)

    def test_protected_xmp_and_no_match_are_unchanged(self):
        original = XMP.replace(b"OpenAI", b"Example Editor").replace(b"ChatGPT", b"Example")
        result, edits = metadata.selective_xmp(metadata.XMP_HEADER + original, Path("sample.jpg"))
        self.assertEqual(edits, 0)
        self.assertEqual(result, metadata.XMP_HEADER + original)
        protected = original.replace(b"Example Studio", b"OpenAI copyright holder")
        self.assertEqual(metadata.selective_xmp(metadata.XMP_HEADER + protected, Path("sample.jpg"))[1], 0)

    def test_xmp_malformed_and_extended_stop(self):
        for packet in (b"<broken>", b"<!DOCTYPE x [<!ENTITY a 'x'>]><x/>", b"<unrecognized/>"):
            with self.assertRaises(metadata.ImageMetadataError):
                metadata.selective_xmp(metadata.XMP_HEADER + packet, Path("sample.jpg"))
        jpeg = encoded_image("JPEG")
        before = jpeg[:2] + metadata.jpeg_segment(0xE1, metadata.XMP_EXTENDED + b"demo") + jpeg[2:]
        with self.assertRaises(metadata.ImageMetadataError):
            metadata.clean_bytes(before, Path("sample.jpg"), False)

    def test_photoshop_lengths_unicode_and_other_resources(self):
        name = "OpenAI ChatGPT DALL-E"
        text = struct.pack(">I4II", 6, 0, 0, 12, 16, len(name)) + name.encode("utf-16-be") + struct.pack(">I", 0)
        other = photoshop_resource(0x040F, b"OpenAI ICC rendering")
        payload = metadata.PHOTOSHOP_HEADER + photoshop_resource(0x041A, text) + other
        cleaned, edits = metadata.selective_photoshop(payload, Path("sample.jpg"))
        self.assertGreater(edits, 0)
        self.assertEqual(len(cleaned), len(payload))
        self.assertTrue(cleaned.endswith(other))
        with self.assertRaises(metadata.ImageMetadataError):
            metadata.selective_photoshop(payload[:-1], Path("sample.jpg"))
        for text in (struct.pack(">I", 999) + b"OpenAI", b"OpenAI", text + b"OpenAI descriptor"):
            with self.assertRaises(metadata.ImageMetadataError):
                metadata.selective_photoshop(metadata.PHOTOSHOP_HEADER + photoshop_resource(0x041A, text), Path("sample.jpg"))

    def test_truncated_and_progressive_jpeg(self):
        for progressive in (False, True):
            before = encoded_image("JPEG", progressive=progressive)
            self.assertEqual(metadata.clean_bytes(before, Path("sample.jpg"), False).cleaned, before)
            with self.assertRaises(metadata.ImageMetadataError):
                metadata.clean_bytes(before[:-2], Path("sample.jpg"), False)

    def test_unknown_mixed_metadata_is_not_dropped(self):
        jpeg = encoded_image("JPEG")
        for marker, payload in ((0xE1, b"unknown OpenAI and unrelated rights"),
                                (0xED, b"unknown OpenAI and unrelated author"),
                                (0xEB, b"JP mixed JUMBF records")):
            before = jpeg[:2] + metadata.jpeg_segment(marker, payload) + jpeg[2:]
            with self.assertRaises(metadata.ImageMetadataError):
                metadata.clean_bytes(before, Path("sample.jpg"), False)
        with self.assertRaises(metadata.ImageMetadataError):
            metadata.webp_reason({"type": b"TEST", "payload": b"OpenAI and unrelated data"}, False)

    def test_png_mixed_xmp_preserves_properties(self):
        for compressed in (False, True):
            info = PngInfo()
            info.add_itxt("XML:com.adobe.xmp", XMP.decode(), zip=compressed)
            before = encoded_image("PNG", pnginfo=info)
            result = metadata.clean_bytes(before, Path("sample.png"), False)
            with Image.open(io.BytesIO(result.cleaned)) as image:
                packet = image.info["XML:com.adobe.xmp"]
                self.assertNotIn("OpenAI", packet)
                self.assertIn("Example Studio", packet)
                self.assertIn("Keep this title", packet)
                self.assertIn('Orientation="6"', packet)
            self.assertEqual(result.cleaned, metadata.clean_bytes(result.cleaned, Path("sample.png"), False).cleaned)
            self.assertEqual(result.encoded_hash, metadata.encoded_hash_for(result.cleaned, Path("sample.png")))

    def test_png_rendering_and_rights_preservation(self):
        info = PngInfo()
        info.add_text("Software", "OpenAI")
        info.add_text("Copyright", "Example Studio")
        before = encoded_image("PNG", pnginfo=info)
        result = metadata.clean_bytes(before, Path("sample.png"), False)
        self.assertNotIn(b"OpenAI", result.cleaned)
        self.assertIn(b"Example Studio", result.cleaned)
        self.assertIsNone(metadata.png_reason({"type": b"iCCP", "payload": b"OpenAI rendering"}, False))
        self.assertEqual(result.encoded_hash, metadata.encoded_hash_for(result.cleaned, Path("sample.png")))
        self.verify_pixels(before, result.cleaned)

    def test_webp_selective_and_gif_animation(self):
        before = encoded_image("WEBP", xmp=XMP, lossless=True)
        result = metadata.clean_bytes(before, Path("sample.webp"), False)
        self.assertNotIn(b"ChatGPT", result.cleaned)
        self.assertIn(b"Example Studio", result.cleaned)
        self.assertEqual(result.encoded_hash, metadata.encoded_hash_for(result.cleaned, Path("sample.webp")))
        self.verify_pixels(before, result.cleaned)
        stream = io.BytesIO()
        Image.new("RGB", (10, 10), "red").save(stream, format="GIF", save_all=True,
            append_images=[Image.new("RGB", (10, 10), "blue")], duration=[100, 200], loop=0, comment=b"OpenAI")
        before = stream.getvalue()
        result = metadata.clean_bytes(before, Path("sample.gif"), False)
        self.assertNotIn(b"OpenAI", result.cleaned)
        with Image.open(io.BytesIO(result.cleaned)) as image:
            self.assertEqual(image.n_frames, 2)
            self.assertEqual(image.info["loop"], 0)
            image.seek(1)
            self.assertEqual(image.info["duration"], 200)
        self.assertIsNone(metadata.gif_reason({"kind": "extension", "label": 1, "payload": b"OpenAI visible"}, True))

    def test_exif_guard_inspection_and_copy_modes(self):
        jpeg = encoded_image("JPEG")
        before = jpeg[:2] + metadata.jpeg_segment(0xE1, b"Exif\0\0OpenAI") + jpeg[2:]
        with self.assertRaises(metadata.ImageMetadataError):
            metadata.clean_bytes(before, Path("sample.jpg"), False)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "sample.jpg"
            source.write_bytes(jpeg[:2] + metadata.jpeg_segment(0xE1, metadata.XMP_HEADER + XMP) + jpeg[2:])
            initial = digest(source)
            inspected = run_cli(metadata, [source])
            self.assertEqual(inspected.returncode, 0, inspected.stderr)
            self.assertEqual(initial, digest(source))
            aliased = run_cli(metadata, [source, "--output-dir", root])
            self.assertEqual(aliased.returncode, 1)
            self.assertEqual(initial, digest(source))
            copied = run_cli(metadata, [source, "--output-dir", root / "copies"])
            self.assertEqual(copied.returncode, 0, copied.stderr)
            self.assertEqual(initial, digest(source))
            self.assertIn("PASS", copied.stdout)


if __name__ == "__main__":
    unittest.main()
