#!/usr/bin/env python3
"""Read local media measurements and evaluate a versioned rules profile."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import warnings

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi"}
RANGES = {"width", "height", "aspect_ratio", "duration"}
COMMON = RANGES | {"formats", "max_bytes", "filename_pattern"}
ALLOWED = {"image": COMMON | {"animated"}, "video": COMMON | {"codecs"}}


class MeasurementError(ValueError):
    """A deliberately public-safe diagnostic authored by this helper."""


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_rules(data):
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        raise ValueError("Rules require schema_version 1")
    if set(data) - {"schema_version", "image", "video"} or not ({"image", "video"} & set(data)):
        raise ValueError("Rules require image and/or video sections and no unknown keys")
    for kind in ("image", "video"):
        if kind not in data:
            continue
        rules = data[kind]
        if not isinstance(rules, dict) or not rules or set(rules) - ALLOWED[kind]:
            raise ValueError(f"Invalid or empty {kind} rules")
        for key, value in rules.items():
            if key in RANGES:
                if not isinstance(value, dict) or not value or set(value) - {"min", "max"}:
                    raise ValueError(f"{key} requires min and/or max")
                if any(not number(v) or v < 0 for v in value.values()):
                    raise ValueError(f"{key} bounds must be finite nonnegative numbers")
                if value.get("min", 0) > value.get("max", math.inf):
                    raise ValueError(f"{key} min exceeds max")
            elif key in {"formats", "codecs"}:
                if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v for v in value):
                    raise ValueError(f"{key} requires a nonempty string list")
            elif key == "max_bytes":
                if type(value) is not int or value <= 0:
                    raise ValueError("max_bytes must be a positive integer")
            elif key == "animated" and type(value) is not bool:
                raise ValueError("animated must be boolean")
            elif key == "filename_pattern":
                if not isinstance(value, str) or len(value) > 256:
                    raise ValueError("filename_pattern must be a regex of at most 256 characters")
                re.compile(value)
    return data


def linked(path):
    info = path.lstat()
    return path.is_symlink() or bool(getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def local_path(value):
    if "://" in str(value) or str(value).startswith(("\\\\", "//")):
        raise ValueError("Only local filesystem paths are accepted")
    path = Path(value).expanduser().absolute()
    if any(linked(p) for p in [path, *path.parents] if p.exists()):
        raise ValueError("Linked paths are not followed")
    if not path.exists():
        raise ValueError("Input does not exist")
    return path


def collect(path, recursive):
    if path.is_file():
        return [path]
    found = []
    for root, dirs, files in os.walk(path, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not linked(Path(root) / d))
        for name in sorted(files):
            item = Path(root) / name
            if not linked(item):
                found.append(item)
        if not recursive:
            break
    if not found:
        raise ValueError("No files found")
    return sorted(found)


def image_info(path):
    try:
        from PIL import Image
    except ImportError as exc:
        raise MeasurementError("Pillow is unavailable; image measurements are unverified") from exc
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            im.load()
            width, height = im.size
            if im.getexif().get(274) in {5, 6, 7, 8}:
                width, height = height, width
            frames = getattr(im, "n_frames", 1)
            duration = None
            if frames > 1:
                times = []
                for frame in range(frames):
                    im.seek(frame)
                    im.load()
                    delay = im.info.get("duration")
                    if not number(delay) or delay < 0:
                        times = []
                        break
                    times.append(delay)
                if times:
                    duration = sum(times) / 1000
            return {"format": im.format.lower(), "width": width, "height": height,
                    "aspect_ratio": width / height, "animated": frames > 1,
                    "duration": duration}


def finite_float(value):
    try:
        result = float(value)
        return result if math.isfinite(result) and result >= 0 else None
    except (TypeError, ValueError):
        return None


def video_info(path, timeout):
    executable = shutil.which("ffprobe")
    if not executable:
        raise MeasurementError("ffprobe is unavailable; video measurements are unverified")
    command = [
        executable, "-v", "error", "-protocol_whitelist", "file",
        "-format_whitelist", "mov,matroska,webm,avi",
        "-show_entries",
        "format=format_name,duration:stream=codec_type,codec_name,width,height,sample_aspect_ratio,duration:"
        "stream_disposition=attached_pic:stream_tags=rotate:stream_side_data=rotation",
        "-of", "json", str(path),
    ]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise MeasurementError("ffprobe timed out") from exc
    if proc.returncode:
        raise MeasurementError("ffprobe could not inspect the permitted local container")
    try:
        data = json.loads(proc.stdout)
        videos = [s for s in data.get("streams", []) if s.get("codec_type") == "video"
                  and not s.get("disposition", {}).get("attached_pic")]
        if len(videos) != 1:
            raise MeasurementError("Expected exactly one non-cover video stream")
        stream = videos[0]
        width, height = stream.get("width"), stream.get("height")
        if not number(width) or not number(height) or width <= 0 or height <= 0:
            raise MeasurementError("Video dimensions unavailable")
        sar_text = stream.get("sample_aspect_ratio")
        sar = None
        if sar_text not in {None, "N/A", "0:1"}:
            parts = sar_text.split(":")
            sar = float(parts[0]) / float(parts[1])
            if not math.isfinite(sar) or sar <= 0:
                raise MeasurementError("Invalid sample aspect ratio")
        rotation = stream.get("tags", {}).get("rotate", 0)
        for item in stream.get("side_data_list", []):
            if "rotation" in item:
                rotation = item["rotation"]
        angle = float(rotation) % 360
        aspect = width * sar / height if sar is not None else None
        if angle in (90, 270):
            width, height, aspect = height, width, 1 / aspect if aspect is not None else None
        elif angle != 0 and angle != 180:
            raise MeasurementError("Non-right-angle display rotation is unverified")
        format_info = data.get("format", {})
        duration = finite_float(format_info.get("duration"))
        if duration is None:
            duration = finite_float(stream.get("duration"))
        return {"format": format_info.get("format_name"), "width": width, "height": height,
                "aspect_ratio": aspect, "duration": duration, "codec": stream.get("codec_name")}
    except (KeyError, TypeError, ZeroDivisionError, IndexError, json.JSONDecodeError) as exc:
        raise MeasurementError("Invalid ffprobe measurements") from exc


def evaluate(measurements, rules, filename):
    checks = []
    for key, expected in rules.items():
        field = {"formats": "format", "codecs": "codec", "max_bytes": "bytes"}.get(key, key)
        observed = filename if key == "filename_pattern" else measurements.get(field)
        if observed is None:
            checks.append({"rule": key, "status": "unverified", "reason": "Measurement unavailable"})
            continue
        if key in RANGES:
            ok = expected.get("min", -math.inf) <= observed <= expected.get("max", math.inf)
        elif key == "formats":
            # ffprobe reports several aliases for one container.
            ok = bool(set(observed.lower().split(",")) & {v.lower() for v in expected})
        elif key == "codecs":
            ok = observed.lower() in {v.lower() for v in expected}
        elif key == "max_bytes":
            ok = observed <= expected
        elif key == "filename_pattern":
            ok = re.fullmatch(expected, filename) is not None
        else:
            ok = observed == expected
        checks.append({"rule": key, "status": "pass" if ok else "fail", "observed": observed,
                       "expected": expected})
    return checks


def inspect_file(path, base, rules, timeout):
    name = path.name if base.is_file() else path.relative_to(base).as_posix()
    suffix = path.suffix.lower()
    kind = "image" if suffix in IMAGE_EXTENSIONS else "video" if suffix in VIDEO_EXTENSIONS else None
    result = {"file": name, "kind": kind, "status": "unverified", "measurements": {}, "checks": []}
    if not kind or kind not in rules:
        result["reason"] = "Unsupported file type or no applicable rule section"
        return result
    try:
        measurements = image_info(path) if kind == "image" else video_info(path, timeout)
        measurements["bytes"] = path.stat().st_size
        result["measurements"] = measurements
        result["checks"] = evaluate(measurements, rules[kind], path.name)
        statuses = {item["status"] for item in result["checks"]}
        result["status"] = "fail" if "fail" in statuses else "unverified" if "unverified" in statuses else "pass"
    except Exception as exc:
        # Do not leak decoder diagnostics, arbitrary tags, or machine paths.
        safe = str(exc) if isinstance(exc, MeasurementError) else "Media could not be safely inspected"
        result["reason"] = safe if not any(x in safe for x in (str(path), "Traceback")) else "Inspection failed"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--rules", required=True, type=Path)
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--timeout", type=float, default=15)
    args = parser.parse_args(argv)
    try:
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise ValueError("timeout must be positive and finite")
        rules_path = local_path(args.rules)
        rules = validate_rules(json.loads(rules_path.read_text(encoding="utf-8-sig")))
        root = local_path(args.path)
        results = [inspect_file(p, root, rules, args.timeout) for p in collect(root, args.recursive)]
        counts = {s: sum(r["status"] == s for r in results) for s in ("pass", "fail", "unverified")}
        check_counts = {s: sum(check["status"] == s for result in results for check in result["checks"])
                        for s in ("pass", "fail", "unverified")}
        has_unverified = bool(counts["unverified"] or check_counts["unverified"])
        report = {"schema_version": 1, "counts": counts, "check_counts": check_counts,
                  "has_unverified": has_unverified, "files": results,
                  "scope": "Container measurements, not a full playback or visual-quality certification"}
        if args.json:
            print(json.dumps(report, ensure_ascii=True, indent=2))
        else:
            for result in results:
                print(f"{result['status'].upper()}: {result['file']}")
                for check in result["checks"]:
                    if check["status"] != "pass":
                        detail = check.get("reason") or f"measured={check.get('observed')}; required={check.get('expected')}"
                        print(f"  {check['rule']}: {check['status']}; {detail}")
                if result.get("reason"):
                    print("  " + result["reason"])
            print("SUMMARY: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
        return 2 if has_unverified else 1 if counts["fail"] else 0
    except (OSError, ValueError, re.error) as exc:
        message = str(exc) if not isinstance(exc, OSError) else "Cannot read the input or rules file"
        if args.json:
            print(json.dumps({"schema_version": 1, "error": message}))
        else:
            print("ERROR: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
