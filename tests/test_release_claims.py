"""Exercise the installed-style CLI with synthetic evidence only."""
import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/release-announcement-writer/scripts/check_release_claims.py"


def row(field, value, scope="current", **extra):
    return dict(scope=scope, field=field, value=value, **extra)


class ReleaseClaimsTests(unittest.TestCase):
    def setUp(self):
        self.record = dict(tag="v2.0", release_tag="v2.0", tag_commit="a" * 40,
                           release_commit="a" * 40, state="published", count=4,
                           url="https://example.com/releases/v2.0")

    def call(self, data, code):
        p = subprocess.run([sys.executable, "-B", str(SCRIPT)], input=data,
                           capture_output=True, timeout=8)
        self.assertEqual(p.returncode, code, p.stdout)
        self.assertEqual(p.stderr, b"")
        self.assertNotIn(b"example.com", p.stdout)
        return json.loads(p.stdout)

    def check(self, rows, expected, code, anchor="matches"):
        pack = {"version": 1, "release": self.record, "claims": rows}
        result = self.call(json.dumps(pack).encode(), code)
        self.assertEqual(result["identity"], anchor)
        self.assertEqual(result["claims"], [dict(row=n, result=v) for n, v in enumerate(expected, 1)])

    def test_live_page_and_dated_note(self):
        self.check([row("state", "draft"), row("count", 3), row("tag", "v2.0"),
                    row("state", "draft", "historical", as_of="2025-01-03")],
                   ["conflicts", "conflicts", "matches", "historical: retain"], 1)

    def test_version_conflict_and_count_control(self):
        self.check([row("tag", "v1.9"), row("count", 4), row("commit", "A"*40)],
                   ["conflicts", "matches", "matches"], 1)

    def test_working_wrong_link_and_unknown_mirror(self):
        self.check([row("url", "https://example.com/releases/v1.9"),
                    row("link_status", "confirmed-present"), row("link_status", "unknown"),
                    row("link_status", "confirmed-missing")],
                   ["conflicts", "matches", "not verified", "conflicts"], 1)

    def test_ambiguous_scope_and_bad_history_date(self):
        self.check([row("state", "draft", "uncertain"), row("state", "draft", "historical", as_of="2025-02-31")],
                   ["not verified", "not verified"], 2)

    def test_tag_or_commit_mismatch_blocks_inference(self):
        for field, value in [("release_tag", "v1.9"), ("release_commit", "b" * 40)]:
            with self.subTest(field=field):
                before = self.record[field]
                self.record[field] = value
                self.check([row("count", 3)], ["not verified"], 1, "conflicts")
                self.record[field] = before

    def test_missing_identity_or_inventory(self):
        del self.record["count"]
        self.check([row("count", 4)], ["not verified"], 2)
        self.record["release_commit"] = "main"
        self.check([row("tag", "v2.0")], ["not verified"], 2, "not verified")

    def test_prerelease_not_final_and_typed_counts(self):
        self.record["state"] = "prerelease"
        self.check([row("state", "published"), row("count", True)], ["conflicts", "not verified"], 1)
        self.check([row("state", "prerelease")], ["matches"], 0)
        self.check([], [], 2)

    def test_invalid_packs_never_clear(self):
        for data in [b'not JSON', b'{"version":true}', b'{"version":1,"version":1}',
                     b'{"version":1,"release":{},"claims":[[]]}', b' ' * (1024 * 1024 + 1)]:
            with self.subTest(size=len(data)):
                self.assertIn("error", self.call(data, 2))


if __name__ == "__main__":
    unittest.main()
