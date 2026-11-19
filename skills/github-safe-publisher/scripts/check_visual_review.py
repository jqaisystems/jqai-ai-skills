"""Compare a private review receipt with one exact local screenshot placement."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import sys


def digest(name):
    p = Path(name)
    if name.startswith(("//", "\\\\")) or "://" in name or ".." in p.parts or p.drive.startswith("\\\\"):
        raise ValueError
    p = p.absolute()
    for entry in [*reversed(p.parents), p]:
        s = entry.lstat()
        if stat.S_ISLNK(s.st_mode) or getattr(s, "st_file_attributes", 0) & 0x400:
            raise ValueError
    if not stat.S_ISREG(s.st_mode):
        raise ValueError
    with p.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("image", "artifact", "placement"):
        cli.add_argument("--" + name, required=True)
    cli.add_argument("--state", choices=["unchecked", "reviewed", "skipped"], default="unchecked")
    cli.add_argument("--finding", choices=["unknown", "clear", "exposed", "recoverable"], default="unknown")
    cli.add_argument("--recorded-key", default="")
    a = cli.parse_args()
    key = None
    try:
        if not a.placement.strip():
            raise ValueError
        record = ["visual-review-v1", digest(a.image), digest(a.artifact), a.placement]
        key = hashlib.sha256(json.dumps(record, separators=(",", ":")).encode("ascii")).hexdigest()
    except (ValueError, OSError):
        pass
    if a.finding in {"exposed", "recoverable"}:
        state, reason, code = "BLOCK", "reported-exposure", 1
    elif not key:
        state, reason, code = "REVIEW", "measurement-incomplete", 2
    elif a.state != "reviewed" or a.finding != "clear" or a.recorded_key != key:
        state, reason, code = "REVIEW", "clear-review-not-matched", 2
    else:
        state, reason, code = "MATCH", "reported-clear-review-matches-placement", 0
    print(json.dumps({"status": state, "reason": reason, "review_key": key}))
    return code


if __name__ == "__main__":
    sys.exit(main())
