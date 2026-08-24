#!/usr/bin/env python3
"""Non-generative relight — adjust ONLY the light of an image, content 100% intact.

Operates on existing pixels (Pillow): exposure, contrast, warmth, a soft directional/ambient
GLOW (screen-blended), and optional dodge (brighten) / burn (darken) elliptical regions.
It cannot change geometry or content — it only redistributes light/colour.

Usage:
  python relight.py --image in.png --out out.png [--exposure 1.04] [--contrast 1.03] [--warmth 0.03]
     [--glow 0.0 --glow-x 0.7 --glow-y 0.4 --glow-radius 0.5 --glow-color #FFE6C2]
     [--dodge 0.0 --dodge-x .. --dodge-y .. --dodge-r .. ]  (brighten a soft ellipse)
     [--burn 0.0 --burn-x .. --burn-y .. --burn-r .. ]      (darken a soft ellipse, e.g. kill a halo)
"""
import argparse
import sys
from pathlib import Path


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main():
    p = argparse.ArgumentParser(description="Non-generative relight.")
    p.add_argument("--image", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--exposure", type=float, default=1.0)
    p.add_argument("--contrast", type=float, default=1.0)
    p.add_argument("--warmth", type=float, default=0.0, help="0..0.15 warm white-balance")
    p.add_argument("--glow", type=float, default=0.0, help="0..1 intensity of a soft light glow")
    p.add_argument("--glow-x", type=float, default=0.5)
    p.add_argument("--glow-y", type=float, default=0.4)
    p.add_argument("--glow-radius", type=float, default=0.5, help="fraction of image diagonal")
    p.add_argument("--glow-color", default="#FFE6C2")
    p.add_argument("--dodge", type=float, default=0.0, help="0..1 brighten an ellipse")
    p.add_argument("--dodge-x", type=float, default=0.5); p.add_argument("--dodge-y", type=float, default=0.5)
    p.add_argument("--dodge-r", type=float, default=0.25)
    p.add_argument("--burn", type=float, default=0.0, help="0..1 darken an ellipse (e.g. remove a halo)")
    p.add_argument("--burn-x", type=float, default=0.5); p.add_argument("--burn-y", type=float, default=0.5)
    p.add_argument("--burn-r", type=float, default=0.15)
    args = p.parse_args()

    try:
        from PIL import Image, ImageEnhance, ImageDraw, ImageFilter, ImageChops
    except ImportError:
        print("ERROR: pip install pillow", file=sys.stderr); sys.exit(2)

    im = Image.open(args.image).convert("RGB")
    W, H = im.size
    diag = (W ** 2 + H ** 2) ** 0.5

    if args.warmth > 0:
        w = min(0.15, args.warmth)
        r, g, b = im.split()
        r = r.point(lambda v: min(255, int(v * (1 + w))))
        b = b.point(lambda v: int(v * (1 - w)))
        im = Image.merge("RGB", (r, g, b))
    if args.exposure != 1.0:
        im = ImageEnhance.Brightness(im).enhance(args.exposure)
    if args.contrast != 1.0:
        im = ImageEnhance.Contrast(im).enhance(args.contrast)

    def soft_ellipse(cx, cy, r):
        m = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(m)
        rx = int(r * diag); ry = int(r * diag)
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
        return m.filter(ImageFilter.GaussianBlur(rx * 0.6))

    # GLOW: screen-blend a coloured soft light
    if args.glow > 0:
        col = hex2rgb(args.glow_color)
        glow = Image.new("RGB", (W, H), col)
        mask = soft_ellipse(int(args.glow_x * W), int(args.glow_y * H), args.glow_radius)
        mask = mask.point(lambda v: int(v * args.glow))
        screened = ImageChops.screen(im, glow)
        im = Image.composite(screened, im, mask)

    # DODGE: brighten a soft region
    if args.dodge > 0:
        mask = soft_ellipse(int(args.dodge_x * W), int(args.dodge_y * H), args.dodge_r)
        mask = mask.point(lambda v: int(v * args.dodge))
        bright = ImageEnhance.Brightness(im).enhance(1.35)
        im = Image.composite(bright, im, mask)

    # BURN: darken a soft region (e.g. kill a hotspot/halo)
    if args.burn > 0:
        mask = soft_ellipse(int(args.burn_x * W), int(args.burn_y * H), args.burn_r)
        mask = mask.point(lambda v: int(v * args.burn))
        dark = ImageEnhance.Brightness(im).enhance(0.6)
        im = Image.composite(dark, im, mask)

    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=95)
    print(f"SAVED {out} ({W}x{H})")


if __name__ == "__main__":
    main()
