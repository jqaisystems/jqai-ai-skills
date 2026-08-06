#!/usr/bin/env python3
"""Score thumbnail candidates at the size people actually see them.

A thumbnail is judged at roughly 168 pixels wide in search results and
sidebars, not at the 1280 or 2048 pixels you designed it at. Most images that
look great full size fail there. This measures what survives.

Requires Pillow:  python -m pip install Pillow
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    from PIL import Image, ImageFilter
except ImportError:
    print("ERROR: this script needs Pillow. Install it with: python -m pip install Pillow",
          file=sys.stderr)
    raise SystemExit(1)

# YouTube search and sidebar render around this size. Match your platform if
# it differs; the point is to measure at display size, not design size.
TINY_W, TINY_H = 168, 94
SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}

# Thresholds tuned on real thumbnail sets. They flag risk, not failure.
LOW_CONTRAST = 40
DARK = 45
BRIGHT = 200
MUTED_POP = 12


def channel_stats(image: Image.Image) -> tuple[list[float], list[float]]:
    """Per-channel mean and standard deviation, 0 to 255."""
    means, stdevs = [], []
    for channel in image.split()[:3]:
        histogram = channel.histogram()
        total = sum(histogram)
        if not total:
            means.append(0.0)
            stdevs.append(0.0)
            continue
        mean = sum(value * count for value, count in enumerate(histogram)) / total
        variance = sum(count * (value - mean) ** 2 for value, count in enumerate(histogram)) / total
        means.append(mean)
        stdevs.append(variance ** 0.5)
    return means, stdevs


def score(path: Path) -> dict:
    with Image.open(path) as original:
        original.load()
        full_w, full_h = original.size
        image = original.convert("RGB")

        # Cover-crop to the target aspect, the way a feed does, then downscale.
        target = TINY_W / TINY_H
        source = image.width / image.height
        if source > target:
            new_w = int(image.height * target)
            box = ((image.width - new_w) // 2, 0, (image.width + new_w) // 2, image.height)
        else:
            new_h = int(image.width / target)
            box = (0, (image.height - new_h) // 2, image.width, (image.height + new_h) // 2)
        tiny = image.resize((TINY_W, TINY_H), Image.LANCZOS, box=box)

    means, stdevs = channel_stats(tiny)
    brightness = sum(means) / 3
    contrast = sum(stdevs) / 3
    pop = max(means) - min(means)

    # Detail that survives a heavy blur is what reads in a fast scroll.
    _, blurred_stdevs = channel_stats(tiny.filter(ImageFilter.GaussianBlur(radius=2)))
    glance = sum(blurred_stdevs) / 3

    # Drained of colour, a thumbnail must still have structure.
    gray = tiny.convert("L")
    _, gray_stdev = channel_stats(gray.convert("RGB"))
    grayscale_contrast = sum(gray_stdev) / 3

    flags = []
    if contrast < LOW_CONTRAST:
        flags.append("low contrast at small size")
    if brightness < DARK:
        flags.append("dark, may sink into a dark-mode feed")
    if brightness > BRIGHT:
        flags.append("very bright, may wash out on white")
    if pop < MUTED_POP:
        flags.append("muted colours, may not stand out in the feed")
    if glance < LOW_CONTRAST * 0.6:
        flags.append("little structure survives a glance, likely reads as mush while scrolling")
    if grayscale_contrast < LOW_CONTRAST * 0.75:
        flags.append("leans on colour for separation, weak in grayscale")

    return {
        "file": path.name,
        "size": f"{full_w}x{full_h}",
        "brightness": round(brightness),
        "contrast": round(contrast),
        "pop": round(pop),
        "glance": round(glance),
        "grayscale_contrast": round(grayscale_contrast),
        "flags": flags,
    }


def collect(inputs: list[Path], recursive: bool) -> list[Path]:
    found: list[Path] = []
    for item in inputs:
        item = item.expanduser()
        if not item.exists():
            raise FileNotFoundError(f"Path not found: {item}")
        if item.is_file():
            found.append(item.resolve())
            continue
        iterator = item.rglob("*") if recursive else item.iterdir()
        found.extend(p.resolve() for p in iterator
                     if p.is_file() and p.suffix.lower() in SUPPORTED)
    unique = sorted(set(found), key=lambda p: str(p).lower())
    if not unique:
        raise FileNotFoundError("No supported PNG, JPEG, or WebP files found")
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score thumbnail candidates at real display size.")
    parser.add_argument("inputs", nargs="+", type=Path, help="Image file(s) or folder(s)")
    parser.add_argument("--recursive", action="store_true", help="Include nested folders")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    args = parser.parse_args()

    try:
        files = collect(args.inputs, args.recursive)
    except (FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    rows = []
    for path in files:
        try:
            rows.append(score(path))
        except Exception as exc:  # a single unreadable file must not stop the sweep
            print(f"ERROR: {path.name}: {exc}", file=sys.stderr)

    if not rows:
        return 1

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    width = max(len(r["file"]) for r in rows)
    print(f"{'file'.ljust(width)}  bright  contr  pop  glance  gray")
    for r in rows:
        print(f"{r['file'].ljust(width)}  {r['brightness']:>6}  {r['contrast']:>5}  "
              f"{r['pop']:>3}  {r['glance']:>6}  {r['grayscale_contrast']:>4}")
    print()
    flagged = [r for r in rows if r["flags"]]
    for r in flagged:
        print(f"{r['file']}:")
        for flag in r["flags"]:
            print(f"  - {flag}")
    print(f"\nSUMMARY: measured at {TINY_W}x{TINY_H}; files={len(rows)}; "
          f"flagged={len(flagged)}; clean={len(rows) - len(flagged)}")
    print("These are risk signals measured on pixels, not a verdict. "
          "Look at the images at this size before deciding.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
