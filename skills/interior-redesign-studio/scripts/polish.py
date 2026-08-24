#!/usr/bin/env python3
"""Non-generative photoreal polish — color grade + contrast + sharpen + optional upscale.

Operates ONLY on existing pixels (Pillow). It does NOT regenerate the image, so it can never
alter volumetry/structure or hallucinate — it just grades and sharpens an already-rendered photo.

Usage:
  python polish.py --image in.png --out out.png [--warmth 0.04] [--contrast 1.08]
                   [--color 1.06] [--brightness 1.01] [--sharpen 1.0] [--upscale 1.0]
"""
import argparse
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Non-generative photoreal polish.")
    p.add_argument("--image", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--warmth", type=float, default=0.04, help="0..0.12 warm white-balance shift")
    p.add_argument("--contrast", type=float, default=1.08)
    p.add_argument("--color", type=float, default=1.06, help="saturation")
    p.add_argument("--brightness", type=float, default=1.01)
    p.add_argument("--sharpen", type=float, default=1.0, help="extra unsharp strength multiplier")
    p.add_argument("--upscale", type=float, default=1.0, help="e.g. 2.0 to double size")
    args = p.parse_args()

    try:
        from PIL import Image, ImageEnhance, ImageFilter
    except ImportError:
        print("ERROR: pip install pillow", file=sys.stderr)
        sys.exit(2)

    im = Image.open(args.image).convert("RGB")

    # Warm white-balance: gently lift red, lower blue (subtle, structure untouched).
    w = max(0.0, min(0.12, args.warmth))
    if w > 0:
        r, g, b = im.split()
        r = r.point(lambda v: min(255, int(v * (1 + w))))
        b = b.point(lambda v: int(v * (1 - w)))
        im = Image.merge("RGB", (r, g, b))

    im = ImageEnhance.Color(im).enhance(args.color)
    im = ImageEnhance.Contrast(im).enhance(args.contrast)
    im = ImageEnhance.Brightness(im).enhance(args.brightness)

    # Gentle cinematic S-curve (lifts midtone contrast without crushing).
    lut = []
    for v in range(256):
        x = v / 255.0
        # smooth S-curve around 0.5
        y = x + 0.10 * (x - 0.5) * (1 - abs(2 * x - 1))
        lut.append(max(0, min(255, int(y * 255))))
    im = im.point(lut * 3)

    # Subtle detail sharpening.
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=int(70 * args.sharpen), threshold=3))

    if args.upscale and args.upscale != 1.0:
        im = im.resize((int(im.width * args.upscale), int(im.height * args.upscale)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=40, threshold=3))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=95)
    print(f"SAVED {out} ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
