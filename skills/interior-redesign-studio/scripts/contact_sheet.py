#!/usr/bin/env python3
"""Contact sheet — compose a labeled grid from a set of renders for quick comparison.

Usage:
  python contact_sheet.py --inputs "renders/*.png" --out renders/contact_sheet.png
  python contact_sheet.py --inputs a.png b.png c.png --cols 2 --title "Japandi — Phase 2"

Notes:
  --inputs accepts a glob pattern OR an explicit list of files.
  Each cell is captioned with the file name so picks are unambiguous.
"""
import argparse
import glob
import os
import sys
from pathlib import Path


def eprint(*a):
    print(*a, file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description="Build a labeled contact sheet from images.")
    p.add_argument("--inputs", nargs="+", required=True,
                   help="Glob pattern (e.g. 'renders/*.png') or explicit list of image files.")
    p.add_argument("--out", default="contact_sheet.png", help="Output PNG path.")
    p.add_argument("--cols", type=int, default=2, help="Number of columns (default 2).")
    p.add_argument("--cell", type=int, default=560, help="Cell width in px (default 560).")
    p.add_argument("--title", default=None, help="Optional title across the top.")
    args = p.parse_args()

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        eprint("ERROR: missing Pillow. Run: pip install pillow")
        sys.exit(2)

    # Resolve inputs: expand any globs, keep explicit files, sort for stable order.
    files = []
    for item in args.inputs:
        matched = glob.glob(item)
        files.extend(matched if matched else ([item] if os.path.exists(item) else []))
    files = sorted(dict.fromkeys(files))
    if not files:
        eprint("ERROR: no input images found.")
        sys.exit(2)

    pad = 16
    cap_h = 30
    title_h = 48 if args.title else 0
    cols = max(1, args.cols)
    rows = (len(files) + cols - 1) // cols

    # Load + scale thumbnails to a uniform cell width, preserving aspect.
    thumbs = []
    cell_w = args.cell
    max_cell_h = 0
    for f in files:
        try:
            im = Image.open(f).convert("RGB")
        except Exception as e:  # noqa: BLE001
            eprint(f"WARN: skipping {f}: {e}")
            continue
        w, h = im.size
        new_h = int(h * (cell_w / w))
        im = im.resize((cell_w, new_h), Image.LANCZOS)
        thumbs.append((Path(f).name, im))
        max_cell_h = max(max_cell_h, new_h)

    if not thumbs:
        eprint("ERROR: no readable images.")
        sys.exit(2)

    cell_total_h = max_cell_h + cap_h
    sheet_w = cols * cell_w + (cols + 1) * pad
    sheet_h = title_h + rows * cell_total_h + (rows + 1) * pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), (244, 241, 235))
    draw = ImageDraw.Draw(sheet)

    def font(size):
        for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(name, size)
            except Exception:  # noqa: BLE001
                continue
        return ImageFont.load_default()

    if args.title:
        draw.text((pad, pad), args.title, fill=(44, 39, 34), font=font(26))

    for idx, (name, im) in enumerate(thumbs):
        r, c = divmod(idx, cols)
        x = pad + c * (cell_w + pad)
        y = title_h + pad + r * (cell_total_h + pad)
        sheet.paste(im, (x, y))
        draw.text((x + 2, y + im.size[1] + 6), name, fill=(90, 80, 61), font=font(15))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"SAVED {out} ({sheet_w}x{sheet_h}, {len(thumbs)} images)")


if __name__ == "__main__":
    main()
