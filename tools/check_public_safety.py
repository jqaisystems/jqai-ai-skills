#!/usr/bin/env python3
"""Run the public safety scanner and fail only on blocking findings."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "skills" / "github-safe-publisher" / "scripts" / "scan_public_safety.py"


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_public_safety", SCANNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load scanner: {SCANNER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    scanner = load_scanner()
    findings = scanner.scan(ROOT)
    blocking = [finding for finding in findings if finding.severity == "block"]
    review = [finding for finding in findings if finding.severity == "review"]

    print(f"Public safety scanner: {len(blocking)} blocking, {len(review)} review finding(s).")
    for finding in blocking:
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        print(f"BLOCK {location}: {finding.kind} - {finding.detail}")

    if review:
        print("Review findings are allowed in CI but should be intentional.")

    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
