#!/usr/bin/env python3
"""Composite a transparent-background figure onto a base image (non-generative).

Keeps the base pixels 100% intact and pastes the figure with a soft contact shadow.
Position/scale are fractions of the base so placement is easy to iterate.

Usage:
  python composite.py --base base.png --overlay person.png --out out.png \
      --x 0.30 --feet-y 0.82 --height 0.5 [--flip] [--shadow 0.45]
"""
import argparse
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Composite a cutout figure onto a base image.")
    p.add_argument("--base", required=True)
    p.add_argument("--overlay", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--x", type=float, default=0.3, help="horizontal center of the figure (0..1)")
    p.add_argument("--feet-y", type=float, default=0.82, help="vertical position of the feet (0..1)")
    p.add_argument("--height", type=float, default=0.5, help="figure height as fraction of base height")
    p.add_argument("--flip", action="store_true", help="mirror the figure horizontally")
    p.add_argument("--shadow", type=float, default=0.45, help="contact-shadow opacity 0..1 (0=off)")
    p.add_argument("--warm", type=float, default=0.0, help="0..0.12 warm tint on the figure to match scene")
    p.add_argument("--fig-bright", type=float, default=1.0, help="figure brightness (e.g. 0.92 to darken)")
    args = p.parse_args()

    try:
        from PIL import Image, ImageFilter, ImageDraw
    except ImportError:
        print("ERROR: pip install pillow", file=sys.stderr)
        sys.exit(2)

    base = Image.open(args.base).convert("RGBA")
    ov = Image.open(args.overlay).convert("RGBA")

    # Trim overlay to its alpha bounding box so 'height' refers to the actual figure.
    bbox = ov.getbbox()
    if bbox:
        ov = ov.crop(bbox)
    if args.flip:
        ov = ov.transpose(Image.FLIP_LEFT_RIGHT)

    # Light-match the figure to the scene: warm tint + brightness, preserving alpha.
    if args.warm > 0 or args.fig_bright != 1.0:
        from PIL import ImageEnhance
        r, g, b, a = ov.split()
        if args.warm > 0:
            w = min(0.12, args.warm)
            r = r.point(lambda v: min(255, int(v * (1 + w))))
            b = b.point(lambda v: int(v * (1 - w)))
        rgb = Image.merge("RGB", (r, g, b))
        if args.fig_bright != 1.0:
            rgb = ImageEnhance.Brightness(rgb).enhance(args.fig_bright)
        r, g, b = rgb.split()
        ov = Image.merge("RGBA", (r, g, b, a))

    bw, bh = base.size
    target_h = int(args.height * bh)
    scale = target_h / ov.height
    ov = ov.resize((max(1, int(ov.width * scale)), target_h), Image.LANCZOS)

    feet_x = int(args.x * bw)
    feet_y = int(args.feet_y * bh)
    top_left = (feet_x - ov.width // 2, feet_y - ov.height)

    canvas = Image.new("RGBA", base.size, (0, 0, 0, 0))

    # Soft elliptical contact shadow at the feet.
    if args.shadow > 0:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(sh)
        ell_w = int(ov.width * 0.6)
        ell_h = max(6, int(ov.width * 0.12))
        cx, cy = feet_x, feet_y
        d.ellipse([cx - ell_w // 2, cy - ell_h // 2, cx + ell_w // 2, cy + ell_h // 2],
                  fill=(0, 0, 0, int(255 * args.shadow)))
        sh = sh.filter(ImageFilter.GaussianBlur(ell_h * 0.8))
        canvas = Image.alpha_composite(canvas, sh)

    canvas.alpha_composite(ov, top_left)
    out_img = Image.alpha_composite(base, canvas).convert("RGB")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(out, quality=95)
    print(f"SAVED {out} ({out_img.width}x{out_img.height}) figure h={target_h}px at ({feet_x},{feet_y})")


if __name__ == "__main__":
    main()
