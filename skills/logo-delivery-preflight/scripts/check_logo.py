"""Inspect ONE named export in an already prepared local delivery folder."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import sys
import xml.etree.ElementTree as ET

SVG = "{http://www.w3.org/2000/svg}"
LIMIT = 8 * 1024 * 1024


def need(condition):
    if not condition:
        raise ValueError


def local_file(name):
    # Check the spelling before normalization or any filesystem access.
    need(not name.startswith(("//", "\\\\")) and "://" not in name)
    p = Path(name)
    need(".." not in p.parts and not p.drive.startswith("\\\\"))
    p = p.absolute()
    for part in [*reversed(p.parents), p]:
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400)
    need(stat.S_ISREG(info.st_mode) and info.st_size <= LIMIT)
    with p.open("rb") as stream:
        data = stream.read(LIMIT + 1)
    need(len(data) <= LIMIT)
    return data


def svg_checks(data):
    # Parse UTF-8 only. No DTD, processing instructions, fetching, or rendering.
    source = data.decode("utf-8-sig").lstrip()
    source = re.sub(r"^<\?xml\s+[^?]*\?>", "", source, count=1)
    need("<!" + "DOCTYPE" not in source and "<!" + "ENTITY" not in source
         and "<?" not in source and "\0" not in source)
    root = ET.fromstring(source)
    need(root.tag == SVG + "svg")
    failures, notes, ids, refs = set(), set(), set(), set()
    shapes = {"path", "rect", "circle", "ellipse", "polygon", "polyline", "line"}
    supported = shapes | {"svg", "g", "defs", "use", "title", "desc", "linearGradient",
                          "radialGradient", "stop", "clipPath"}
    geometry = False
    for node in root.iter():
        tag = node.tag.removeprefix(SVG)
        geometry |= tag in shapes
        if tag == "image":
            failures.add("image-content-in-vector-delivery")
        elif tag in {"script", "foreignObject"}:
            failures.add("active-or-foreign-content")
        elif tag in {"text", "tspan"}:
            notes.add("live-text-confirm-font-and-outline-policy")
        elif tag not in supported:
            notes.add("unsupported-svg-feature")
        for key, value in node.attrib.items():
            attr = key.rsplit("}", 1)[-1]
            if attr == "id":
                if value in ids:
                    failures.add("duplicate-reference-id")
                ids.add(value)
            if attr == "href":
                if value.startswith("#"):
                    refs.add(value[1:])
                else:
                    failures.add("nonlocal-reference")
            if attr.lower().startswith("on"):
                failures.add("active-content")
            if attr in {"style", "class", "base"}:
                notes.add("style-or-base-needs-inspection")
            for ref in re.findall(r"url\(\s*([^)]*?)\s*\)", value, re.I):
                ref = ref.strip("'\"")
                if ref.startswith("#"):
                    refs.add(ref[1:])
                else:
                    failures.add("nonlocal-reference")
    if refs - ids:
        failures.add("unresolved-reference")
    if not geometry:
        notes.add("no-supported-geometry")
    return failures, notes


def inspect(name, background, size=None):
    failures, notes = set(), set()
    try:
        need(bool(re.fullmatch("#[0-9a-fA-F]{6}", background)))
        if size:
            need(len(size) == 2 and all(type(n) is int and n > 0 for n in size))
        data = local_file(name)
        digest = hashlib.sha256(data).hexdigest()
        suffix = Path(name).suffix.lower()
        if suffix == ".svg":
            failures, notes = svg_checks(data)
            notes.add("visual-check-on-requested-background")
            if size:
                notes.add("vector-size-not-measured")
        elif suffix == ".png":
            from PIL import Image, ImageChops
            with Image.open(io.BytesIO(data)) as image:
                need(image.format == "PNG" and image.width * image.height <= 16_000_000)
                image.verify()
            with Image.open(io.BytesIO(data)) as image:
                need(image.n_frames == 1)
                if size and tuple(size) != image.size:
                    failures.add("wrong-pixel-dimensions")
                back = Image.new("RGBA", image.size, background)
                composite = Image.alpha_composite(back, image.convert("RGBA"))
                if not ImageChops.difference(back.convert("RGB"), composite.convert("RGB")).getbbox():
                    failures.add("invisible-on-background")
        else:
            notes.add("unsupported-format")
    except FileNotFoundError:
        return {"status": "BLOCK", "findings": ["required-input-missing"]}
    except (ValueError, ImportError, OSError, ET.ParseError, SyntaxError, OverflowError):
        return {"status": "REVIEW", "findings": ["input-refused-unreadable-or-decoder-unavailable"]}
    return {"status": "BLOCK" if failures else "REVIEW" if notes else "CHECKS_PASS",
            "findings": sorted(failures | notes), "sha256": digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export")
    parser.add_argument("--background", required=True, help="Intended background, e.g. #ffffff")
    parser.add_argument("--size", nargs=2, type=int, metavar=("WIDTH", "HEIGHT"))
    args = parser.parse_args()
    try:
        result = inspect(args.export, args.background, args.size)
    except Exception:
        # Some decoders have format-specific exceptions. Never print embedded values.
        result = {"status": "REVIEW", "findings": ["inspection-incomplete"]}
    print(json.dumps(result))
    return {"CHECKS_PASS": 0, "BLOCK": 1, "REVIEW": 2}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
