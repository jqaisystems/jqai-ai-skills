#!/usr/bin/env python3
"""Read-only verification of default selective cleanup, with optional Pillow decoding."""
from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import warnings

CHECKS = ("supported_metadata_absent", "selective_changes_only", "encoded_payload",
          "dimensions", "orientation", "colour_information", "decoded_frames",
          "transparency", "frame_timing", "loop_behaviour")
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_DECODED_PIXELS = 100_000_000
MAX_FRAMES = 1000


def cleaner_module():
    name = "_cleanup_verification_cleaner"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("clean_image_metadata.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def read_local(value):
    raw = str(value)
    if "://" in raw or raw.startswith(("\\\\", "//")):
        raise ValueError("local_file_required")
    path = Path(os.path.abspath(raw))
    for part in [*reversed(path.parents), path]:
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("link_refused")
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_FILE_BYTES:
        raise ValueError("input_limit_or_type")
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("input_limit_or_type")
    return data


def sha(data):
    return hashlib.sha256(data).hexdigest()


def container_evidence(data, cleaner):
    placeholder = Path("image")
    kind = cleaner.detect_format(data, placeholder)
    if kind == "PNG":
        chunks = cleaner.parse_png(data, placeholder)
        payload = b"".join(c["raw"] for c in chunks if c["type"] in {b"IDAT", b"fdAT", b"acTL", b"fcTL"})
        colour = b"".join(c["raw"] for c in chunks if c["type"] in {
            b"IHDR", b"PLTE", b"tRNS", b"gAMA", b"cHRM", b"iCCP", b"sRGB", b"sBIT", b"bKGD"})
    elif kind == "JPEG":
        segments = cleaner.parse_jpeg(data, placeholder)
        payload = cleaner.jpeg_encoded_hash(segments).encode()
        colour = b"".join(s["raw"] for s in segments if s["marker"] in {0xE0, 0xE2, 0xEE})
    elif kind == "WebP":
        chunks = cleaner.parse_webp(data, placeholder)
        payload = b"".join(c["raw"] for c in chunks if c["type"] in {
            b"VP8 ", b"VP8L", b"ALPH", b"ANIM", b"ANMF"})
        colour = b"".join(c["raw"] for c in chunks if c["type"] == b"ICCP")
    elif kind == "GIF":
        blocks = cleaner.parse_gif(data, placeholder)
        payload = b"".join(b["raw"] for b in blocks if b["kind"] == "image")
        colour = blocks[0]["raw"]
    else:
        raise ValueError("unsupported_container")
    return {"format": kind, "payload": sha(payload), "colour": sha(colour)}


def decoded_evidence(data, image_module):
    frames, alpha, timing = [], [], []
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with image_module.open(BytesIO(data)) as image:
            count = getattr(image, "n_frames", 1)
            if count > MAX_FRAMES:
                raise ValueError("decode_limit")
            dimensions = image.size
            orientation = image.getexif().get(274, 1)
            loop = image.info.get("loop")
            pixels = 0
            for index in range(count):
                image.seek(index)
                pixels += image.width * image.height
                if pixels > MAX_DECODED_PIXELS:
                    raise ValueError("decode_limit")
                frame = image.convert("RGBA")
                frames.append((frame.size, sha(frame.tobytes())))
                alpha.append(sha(frame.getchannel("A").tobytes()))
                timing.append(image.info.get("duration", 0))
    return {"dimensions": dimensions, "orientation": orientation,
            "decoded_frames": frames, "transparency": alpha,
            "frame_timing": timing, "loop_behaviour": loop}


def verify(before, after):
    checks = {name: {"status": "unverified", "reason": "not_checked"} for name in CHECKS}
    def set_check(name, same, reason="comparison"):
        checks[name] = {"status": "pass" if same else "fail", "reason": reason}
    try:
        original, cleaned = read_local(before), read_local(after)
    except (OSError, ValueError):
        return {"status": "unverified", "checks": checks, "reason": "local_input_unavailable_or_refused"}
    cleaner = cleaner_module()
    try:
        result = cleaner.clean_bytes(cleaned, Path("after"), False)
        set_check("supported_metadata_absent", not result.removals, "known_supported_markers_only")
    except Exception:
        checks["supported_metadata_absent"]["reason"] = "unsupported_or_malformed_metadata"
    try:
        expected = cleaner.clean_bytes(original, Path("before"), False)
        set_check("selective_changes_only", expected.cleaned == cleaned, "default_cleaner_output_comparison")
    except Exception:
        checks["selective_changes_only"]["reason"] = "unsupported_or_malformed_metadata"
    try:
        left, right = container_evidence(original, cleaner), container_evidence(cleaned, cleaner)
        set_check("encoded_payload", left["format"] == right["format"] and left["payload"] == right["payload"])
        set_check("colour_information", left["format"] == right["format"] and left["colour"] == right["colour"])
    except Exception:
        checks["encoded_payload"]["reason"] = "unsupported_or_malformed_container"
        checks["colour_information"]["reason"] = "unsupported_or_malformed_container"
    try:
        from PIL import Image
    except ImportError:
        for key in CHECKS[3:]:
            if key != "colour_information":
                checks[key]["reason"] = "pillow_unavailable"
    else:
        try:
            left, right = decoded_evidence(original, Image), decoded_evidence(cleaned, Image)
            for key in left:
                set_check(key, left[key] == right[key])
        except Exception:
            # Decoder exceptions can contain filenames or embedded text; do not export them.
            for key in ("dimensions", "orientation", "decoded_frames", "transparency", "frame_timing", "loop_behaviour"):
                checks[key] = {"status": "unverified", "reason": "decoder_failed_or_limit_exceeded"}
    states = {item["status"] for item in checks.values()}
    status = "fail" if "fail" in states else "unverified" if "unverified" in states else "pass"
    return {"status": status, "checks": checks,
            "scope": "supported_default_cleanup_not_authenticity_or_platform_label_detection"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(args.before, args.after)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Overall:", result["status"])
        for name, check in result["checks"].items():
            print(f"{name}: {check['status']} ({check['reason']})")
    return {"pass": 0, "fail": 1, "unverified": 2}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())

