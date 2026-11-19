"""Offline, invented fixtures only; no production art or review receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from PIL import Image, ImageDraw

SKILLS = Path(__file__).resolve().parents[1] / "skills"
LOGO = SKILLS / "logo-delivery-preflight/scripts/check_logo.py"
REVIEW = SKILLS / "github-safe-publisher/scripts/check_visual_review.py"


class VisualPreflight(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.png = self.root / "mark.png"
        self.svg = self.root / "mark.svg"
        self.screen = self.root / "screen.png"
        self.guide = self.root / "guide.html"
        mark = Image.new("RGBA", (32, 32))
        ImageDraw.Draw(mark).ellipse((4, 4, 27, 27), outline="white", width=3)
        mark.save(self.png)
        self.draw_screen("Sample board")
        self.guide.write_text('<img alt="Sample board" src="screen.png">', encoding="utf8")

    def draw_screen(self, label):
        image = Image.new("RGB", (180, 60), "white")
        ImageDraw.Draw(image).text((8, 8), label, fill="black")
        image.save(self.screen)

    def cli(self, script, expected, *args):
        result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def logo(self, path, expected, bg="#101820", size=32):
        return self.cli(LOGO, expected, path, "--background", bg, "--size", size, size)

    def svg_case(self, body, expected):
        self.svg.write_text('<svg xmlns="http://www.w3.org/2000/svg">' + body + '</svg>', encoding="utf8")
        return self.logo(self.svg, expected)["findings"]

    def review(self, expected, *extra, slot="figure-1"):
        return self.cli(REVIEW, expected, "--image", self.screen, "--artifact",
                        self.guide, "--placement", slot, *extra)

    def test_reverse_mark(self):
        original = self.png.read_bytes()
        self.assertEqual(self.logo(self.png, 0)["sha256"], hashlib.sha256(original).hexdigest())
        self.assertIn("invisible-on-background", self.logo(self.png, 1, "#ffffff")["findings"])
        self.assertIn("wrong-pixel-dimensions", self.logo(self.png, 1, size=16)["findings"])
        self.assertEqual(self.png.read_bytes(), original)

    def test_absent_empty_native_corrupt(self):
        self.logo(self.root / "missing.svg", 1)
        Image.new("RGBA", (32, 32)).save(self.png)
        self.logo(self.png, 1)
        other = self.root / "mark.native"
        other.write_bytes(b"example")
        self.logo(other, 2)
        self.png.write_bytes(b"not an image")
        self.logo(self.png, 2)

    def test_vector_and_live_type(self):
        self.assertIn("visual-check-on-requested-background", self.svg_case(
            '<defs><circle id="mark" r="2"/></defs><use href="#mark"/>', 2))
        self.assertIn("live-text-confirm-font-and-outline-policy", self.svg_case(
            '<text>Example Studio</text>', 2))

    def test_refs_raster_and_active_content(self):
        for body, finding in [
            ('<use href="#missing"/>', "unresolved-reference"),
            ('<path fill="url(#missing)"/>', "unresolved-reference"),
            ('<image href="sample.png"/>', "nonlocal-reference"),
            ('<image href="data:image/png;base64,AA=="/>', "image-content-in-vector-delivery"),
            ('<script/>', "active-or-foreign-content"),
        ]:
            with self.subTest(finding=finding):
                self.assertIn(finding, self.svg_case(body, 1))

    def test_malformed_svg(self):
        self.svg.write_text('<svg>', encoding="utf8")
        self.logo(self.svg, 2)

    def test_receipt_states_and_no_mutations(self):
        originals = [p.read_bytes() for p in (self.screen, self.guide)]
        record = self.review(2)["review_key"]
        for state, finding in [("unchecked", "clear"), ("skipped", "clear"), ("reviewed", "unknown")]:
            self.review(2, "--state", state, "--finding", finding, "--recorded-key", record)
        self.review(2, "--state", "reviewed", "--finding", "clear")
        match = self.review(0, "--state", "reviewed", "--finding", "clear", "--recorded-key", record)
        self.assertEqual(match["status"], "MATCH")
        self.assertEqual(originals, [p.read_bytes() for p in (self.screen, self.guide)])

    def test_changed_placements_and_artifacts(self):
        record = self.review(2)["review_key"]
        receipt = ["--state", "reviewed", "--finding", "clear", "--recorded-key", record]
        self.review(2, *receipt, slot="figure-2")
        initial = self.guide.read_bytes()
        self.guide.write_bytes(initial + b'<p>Updated sample</p>')
        self.review(2, *receipt)
        self.guide.write_bytes(initial)
        self.draw_screen("Different sample")
        self.review(2, *receipt)
        self.screen.unlink()
        self.assertIsNone(self.review(2, *receipt)["review_key"])

    def test_exposure_and_removable_overlay(self):
        # Simulate a reviewer inspecting both pixels and the shipping HTML source.
        self.draw_screen("Fictional private note")
        self.review(1, "--finding", "exposed")
        self.guide.write_text('<img src="screen.png"><div style="position:absolute;inset:0;background:black"></div>',
                              encoding="utf8")
        key = self.review(2)["review_key"]
        self.assertEqual(self.review(1, "--state", "reviewed", "--finding", "recoverable",
                                     "--recorded-key", key)["status"], "BLOCK")


if __name__ == "__main__":
    unittest.main()
