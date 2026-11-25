"""Black-box tests using only fictional inputs and the public CLI."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills/publication-ledger"
SCRIPT = SKILL / "scripts/publication_ledger.py"
SAMPLE = SKILL / "assets/example-ledger.json"


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.pack = json.loads(SAMPLE.read_bytes())

    def call(self, pack, success=True):
        data = pack if isinstance(pack, bytes) else json.dumps(pack).encode()
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, "-B", str(SCRIPT)], cwd=tmp, input=data,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8)
            self.assertEqual(list(Path(tmp).iterdir()), [])
        self.assertEqual(p.returncode, 0 if success else 2, p.stderr)
        if success:
            self.assertEqual(p.stderr, b"")
            return p.stdout.decode("utf-8")
        self.assertFalse(p.stdout)
        self.assertNotIn(b"private-marker", p.stderr)
        return p.stderr

    def test_fictional_acceptance(self):
        history, queue = self.call(self.pack).split("# Review queue")
        atlas, garden = history.split("## sample-garden / garden-note")
        for dest, state in [("newsletter", "scheduled"), ("social", "conflicting evidence"), ("website", "verified")]:
            self.assertRegex(atlas, rf"\| {dest} \| first \|[^\n]*\| {state} \|")
        self.assertIn("no evidence supplied", garden)
        self.assertIn("post-note-c", atlas)
        self.assertIn("review-note-d", atlas)
        self.assertNotIn("| atlas-note | first | website |", queue)
        for key in ("atlas-note | first | newsletter", "atlas-note | first | social", "garden-note | first | website"):
            self.assertEqual(queue.count(key), 1)

    def test_edition_isolation_and_permutation(self):
        self.pack["inventory"].append(dict(self.pack["inventory"][0], edition="revised"))
        first = self.call(self.pack)
        self.assertIn("| atlas-note | revised | website | no evidence supplied", first)
        self.pack["inventory"].reverse()
        self.pack["observations"].reverse()
        self.assertEqual(self.call(self.pack), first)

    def test_progression_and_conflicting_evidence(self):
        self.pack["inventory"] = self.pack["inventory"][:1]
        event = self.pack["observations"][0]
        self.pack["observations"] = [
            dict(event, at="2025-03-04T10:15:00+01:00", kind="scheduled", ref="booking"),
            dict(event, at="2025-03-04T10:00:00Z", kind="reported published", ref="report"),
            event]
        result = self.call(self.pack)
        self.assertIn("09:15:00 scheduled [booking]", result)
        self.assertIn("No unresolved rows", result)
        for changes in [dict(kind="scheduled", at="2025-03-04T12:00:00Z"),
                        dict(kind="scheduled"), dict(kind="disputed")]:
            with self.subTest(changes=changes):
                self.pack["observations"].append(dict(event, **changes, ref="extra"))
                history, queue = self.call(self.pack).split("# Review queue")
                self.assertIn("conflicting evidence", queue)
                for ref in ("booking", "report", "web-check-a", "extra"):
                    self.assertIn("[" + ref + "]", history)
                self.pack["observations"].pop()

    def test_delivery_identity_and_no_votes(self):
        event = self.pack["observations"][0]
        event["delivery_id"] = "delivery-a"
        self.pack["observations"].extend([event, dict(event, delivery_id="delivery-b")])
        history, queue = self.call(self.pack).split("# Review queue")
        self.assertIn("delivery: delivery-b", history)
        self.assertIn("| atlas-note | first | website | conflicting evidence", queue)

    def test_no_observations(self):
        self.pack["observations"] = []
        history, queue = self.call(self.pack).split("# Review queue")
        self.assertEqual(history.count("no evidence supplied"), 4)
        self.assertEqual(queue.count("no evidence supplied"), 4)

    def test_unsafe_or_ambiguous_input(self):
        for changes in [dict(destination="other"), dict(edition="other"), dict(work_id="private-marker"),
                        dict(kind=None), dict(at="2025-02-31T00:00:00Z"), dict(at="2025-02-03"),
                        dict(ref="../private-marker"), dict(extra="private-marker")]:
            with self.subTest(change=changes):
                p = copy.deepcopy(self.pack)
                p["observations"][0].update(changes)
                self.call(p, False)
        self.call(dict(self.pack, version=True), False)
        self.call(dict(self.pack, inventory=[]), False)
        self.call(b'{"version":1,"version":1,"private-marker":true}', False)
        self.call(b' ' * (2 * 1024 * 1024 + 1), False)
        self.pack["inventory"].append(self.pack["inventory"][0])
        self.call(self.pack, False)

    def test_alias_collision_and_markdown_title(self):
        self.pack["inventory"][1]["project"] = "other"
        self.call(self.pack, False)
        self.pack["inventory"][1]["project"] = "sample-atlas"
        self.pack["inventory"][0]["title"] = "Example | " + chr(96) + " <b>Å</b>"
        result = self.call(self.pack)
        self.assertIn("Example \\| ", result)
        self.assertIn(chr(96)*2 + " Example", result)
        self.pack["inventory"][0]["title"] = "multi\nline"
        self.call(self.pack, False)


if __name__ == "__main__":
    unittest.main()
