#!/usr/bin/env python3
"""Verify website route status and required or forbidden response text."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field


@dataclass
class Check:
    kind: str
    expected: str
    passed: bool


@dataclass
class RouteResult:
    url: str
    final_url: str | None = None
    status: int | None = None
    error: str | None = None
    checks: list[Check] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.error is None and all(check.passed for check in self.checks)


def split_spec(value: str) -> tuple[str, str]:
    if "::" not in value:
        raise argparse.ArgumentTypeError("Expected URL::VALUE")
    url, expected = value.split("::", 1)
    if not url or not expected:
        raise argparse.ArgumentTypeError("Expected non-empty URL::VALUE")
    return url, expected


def fetch(url: str, timeout: float) -> tuple[int | None, str | None, str, str | None]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return None, None, "", "Only absolute HTTP or HTTPS URLs are supported"
    if "@" in parsed.netloc:
        return None, None, "", "URLs must not contain authentication values"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "website-change-verifier/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body_bytes = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            body = body_bytes.decode(charset, errors="replace")
            return response.status, response.geturl(), body, None
    except urllib.error.HTTPError as exc:
        body_bytes = exc.read()
        charset = exc.headers.get_content_charset() or "utf-8"
        body = body_bytes.decode(charset, errors="replace")
        return exc.code, exc.geturl(), body, None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, None, "", str(exc)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify route status and response text using Python standard library only."
    )
    parser.add_argument("--url", action="append", default=[], help="URL expected to return 200")
    parser.add_argument(
        "--expect-status",
        action="append",
        default=[],
        type=split_spec,
        metavar="URL::CODE",
        help="Override the expected HTTP status for a URL",
    )
    parser.add_argument(
        "--contains",
        action="append",
        default=[],
        type=split_spec,
        metavar="URL::TEXT",
        help="Require response text",
    )
    parser.add_argument(
        "--not-contains",
        action="append",
        default=[],
        type=split_spec,
        metavar="URL::TEXT",
        help="Forbid response text",
    )
    parser.add_argument("--timeout", type=float, default=10.0, help="Timeout per URL in seconds")
    parser.add_argument("--json", action="store_true", help="Print JSON results")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    expected_status: dict[str, int] = {url: 200 for url in args.url}
    for url, raw_code in args.expect_status:
        try:
            expected_status[url] = int(raw_code)
        except ValueError:
            parser.error(f"Invalid HTTP status for {url}: {raw_code}")

    contains: dict[str, list[str]] = {}
    forbidden: dict[str, list[str]] = {}
    for url, text in args.contains:
        contains.setdefault(url, []).append(text)
        expected_status.setdefault(url, 200)
    for url, text in args.not_contains:
        forbidden.setdefault(url, []).append(text)
        expected_status.setdefault(url, 200)

    if not expected_status:
        parser.error("Provide at least one --url, --expect-status, --contains, or --not-contains")

    results: list[RouteResult] = []
    for url, wanted_status in expected_status.items():
        status, final_url, body, error = fetch(url, args.timeout)
        result = RouteResult(url=url, final_url=final_url, status=status, error=error)
        result.checks.append(
            Check(kind="status", expected=str(wanted_status), passed=status == wanted_status)
        )
        for text_value in contains.get(url, []):
            result.checks.append(
                Check(kind="contains", expected=text_value, passed=text_value in body)
            )
        for text_value in forbidden.get(url, []):
            result.checks.append(
                Check(kind="not-contains", expected=text_value, passed=text_value not in body)
            )
        results.append(result)

    if args.json:
        print(json.dumps([asdict(result) | {"passed": result.passed} for result in results], indent=2))
    else:
        for result in results:
            label = "PASS" if result.passed else "FAIL"
            status = result.status if result.status is not None else "NO_RESPONSE"
            destination = f" -> {result.final_url}" if result.final_url else ""
            print(f"{label} {status} {result.url}{destination}")
            if result.error:
                print(f"  ERROR {result.error}")
            for check in result.checks:
                check_label = "PASS" if check.passed else "FAIL"
                print(f"  {check_label} {check.kind}: {check.expected}")

    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
