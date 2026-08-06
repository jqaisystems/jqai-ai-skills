#!/usr/bin/env python3
"""Assign layouts and colourways across a set of thumbnail candidates.

The problem this solves: ask a generator for seven thumbnails and you get seven
variations of the same idea. Ask for seven specific, different layouts paired
with rotating colours and you get real choices.

The rotation is seeded from the subject, so the same subject always produces the
same plan, and different subjects usually enter the rotation at a different
point. Usually, not always: with seven colourways two subjects collide about one
time in seven. Check the previous plan if back-to-back sameness matters, and pass
--lead to force a different start. Nothing is random at run time.

Standard library only. Edit LAYOUTS and COLOURWAYS to match your own brand;
the ones here are a neutral starting set, not anyone's house style.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

# Seven distinct compositions. Distinct means the eye lands somewhere different,
# not that the crop moved. Replace freely, but keep them genuinely different.
LAYOUTS = [
    ("A", "Face left, big claim right",
     "Subject on the left third, two or three huge words stacked on the right."),
    ("B", "Giant number",
     "One figure dominates the frame; subject smaller, reacting to it."),
    ("C", "Two people facing off",
     "Host and guest in opposition, tension in the gap between them."),
    ("D", "Prop hero",
     "A single physical object carries the story; subject holds or points at it."),
    ("E", "Full-bleed face",
     "Expression fills the frame, minimal text, emotion does the work."),
    ("F", "Before and after",
     "Split frame, a visible transformation across the divide."),
    ("G", "Subject small against scale",
     "Subject dwarfed by something large; the contrast is the message."),
]

# Neutral, high-contrast accents that survive at small size. Swap in your brand.
COLOURWAYS = [
    ("c1", "Signal red", "#E8262B"),
    ("c2", "Electric blue", "#1B5CFF"),
    ("c3", "Acid yellow", "#F5C518"),
    ("c4", "Deep teal", "#0E8F86"),
    ("c5", "Hot magenta", "#D6208A"),
    ("c6", "Warm orange", "#F26A1B"),
    ("c7", "Cool violet", "#7A4DD6"),
]


def seed_for(subject: str) -> int:
    """Stable across machines and runs. hash() is not, so do not use it."""
    return int(hashlib.sha256(subject.encode("utf-8")).hexdigest()[:8], 16)


def plan(subject: str, count: int, lead: tuple[str, str] | None = None) -> list[dict]:
    """Pair each layout with a colourway, offset by subject.

    Layouts and colourways advance at different rates, so a layout does not
    always carry the same colour across subjects.
    """
    if count < 1:
        raise ValueError("count must be at least 1")
    seed = seed_for(subject)
    colour_offset = seed % len(COLOURWAYS)
    layout_offset = (seed // len(COLOURWAYS)) % len(LAYOUTS)

    order = list(range(count))
    # An explicit lead pair puts a proven combination first, which is what a
    # winner-tracking loop feeds back in once it has enough decisions.
    rows = []
    for slot in order:
        layout = LAYOUTS[(slot + layout_offset) % len(LAYOUTS)]
        colour = COLOURWAYS[(slot * 3 + colour_offset) % len(COLOURWAYS)]
        if lead and slot == 0:
            layout = next((l for l in LAYOUTS if l[0] == lead[0]), layout)
            colour = next((c for c in COLOURWAYS if c[0] == lead[1]), colour)
        rows.append({
            "slot": slot + 1,
            "layout_id": layout[0],
            "layout": layout[1],
            "layout_note": layout[2],
            "colourway_id": colour[0],
            "colourway": colour[1],
            "hex": colour[2],
        })

    # A repeated pair inside one set wastes a slot. With count above the number
    # of layouts this is unavoidable, so say so rather than hiding it.
    pairs = {(r["layout_id"], r["colourway_id"]) for r in rows}
    if len(pairs) < len(rows):
        print(f"WARNING: {len(rows) - len(pairs)} duplicate layout/colour pairs; "
              f"reduce count or add more layouts", file=sys.stderr)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plan a set of distinct thumbnail candidates.")
    parser.add_argument("subject", help="Video title, episode name, or any stable subject string")
    parser.add_argument("--count", type=int, default=7, help="How many candidates (default 7)")
    parser.add_argument("--lead", help="Force slot 1 to a proven pair, e.g. B:c3")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    lead = None
    if args.lead:
        if ":" not in args.lead:
            print("ERROR: --lead expects LAYOUT:COLOURWAY, e.g. B:c3", file=sys.stderr)
            return 1
        layout_id, colour_id = args.lead.split(":", 1)
        lead = (layout_id.strip(), colour_id.strip())

    try:
        rows = plan(args.subject, args.count, lead)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"subject": args.subject, "candidates": rows}, indent=2))
        return 0

    print(f"Plan for: {args.subject}\n")
    for r in rows:
        print(f"  {r['slot']}. [{r['layout_id']}] {r['layout']}")
        print(f"     {r['layout_note']}")
        print(f"     accent: {r['colourway']} {r['hex']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
