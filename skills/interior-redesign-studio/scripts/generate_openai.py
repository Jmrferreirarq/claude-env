#!/usr/bin/env python3
"""Interior render via OpenAI gpt-image-1 (alternative engine to test image adherence).

Usage:
  python generate_openai.py --prompt "..." [--image room.png ...] [--out out.png]
                            [--size landscape|portrait|square|auto|1536x1024]
                            [--quality high|medium|low|auto] [--n 1]

Setup:
  pip install openai pillow
  setx OPENAI_API_KEY "sk-..."   (User scope; this script reads it from the registry on Windows)
  Key at https://platform.openai.com/api-keys  (requires a billed OpenAI account)

Notes:
  - With --image it runs the EDIT endpoint (keeps the input image as basis). Repeat --image for refs.
  - Without --image it runs text-to-image.
  - gpt-image-1 is generative: it does NOT guarantee structural fidelity (no ControlNet).
"""
import argparse
import base64
import datetime
import os
import sys
from pathlib import Path


def eprint(*a):
    print(*a, file=sys.stderr)


def resolve_api_key():
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    if os.name == "nt":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                try:
                    val, _ = winreg.QueryValueEx(k, "OPENAI_API_KEY")
                    if val:
                        return val
                except FileNotFoundError:
                    pass
        except Exception:  # noqa: BLE001
            pass
    return None


SIZE_ALIASES = {
    "landscape": "1536x1024",
    "portrait": "1024x1536",
    "square": "1024x1024",
    "auto": "auto",
}


def main():
    p = argparse.ArgumentParser(description="Generate/edit interior images with OpenAI gpt-image-1.")
    p.add_argument("--prompt", required=True)
    p.add_argument("--image", action="append", default=[],
                   help="Input image(s) for the edit endpoint. Repeatable. Omit for text-to-image.")
    p.add_argument("--out", default=None, help="Output PNG path. Default: auto-named in ./renders/")
    p.add_argument("--model", default=os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1"))
    p.add_argument("--size", default="landscape",
                   help="landscape(1536x1024)|portrait(1024x1536)|square(1024x1024)|auto, or WxH.")
    p.add_argument("--quality", default="high", help="high|medium|low|auto")
    p.add_argument("--background", default=None, help="transparent|opaque|auto (gpt-image-1)")
    p.add_argument("--n", type=int, default=1)
    args = p.parse_args()

    api_key = resolve_api_key()
    if not api_key:
        eprint("ERROR: OPENAI_API_KEY not set. Run: setx OPENAI_API_KEY \"sk-...\" then reopen the shell.")
        sys.exit(2)

    try:
        from openai import OpenAI
    except ImportError:
        eprint("ERROR: missing dependency. Run: pip install openai")
        sys.exit(2)

    size = SIZE_ALIASES.get(args.size, args.size)
    client = OpenAI(api_key=api_key)

    files = []
    try:
        for img_path in args.image:
            if not os.path.exists(img_path):
                eprint(f"ERROR: input image not found: {img_path}")
                sys.exit(2)
            files.append(open(img_path, "rb"))  # noqa: SIM115

        saved = []
        for i in range(args.n):
            kwargs = {"model": args.model, "prompt": args.prompt, "size": size, "quality": args.quality}
            if args.background:
                kwargs["background"] = args.background
            try:
                if files:
                    resp = client.images.edit(image=files if len(files) > 1 else files[0], **kwargs)
                else:
                    resp = client.images.generate(**kwargs)
            except Exception as e:  # noqa: BLE001
                eprint(f"ERROR calling model: {e}")
                sys.exit(1)

            b64 = resp.data[0].b64_json
            img_bytes = base64.b64decode(b64)

            if args.out and args.n == 1:
                out_path = Path(args.out)
            else:
                outdir = Path("renders")
                outdir.mkdir(parents=True, exist_ok=True)
                ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                stem = Path(args.out).stem if args.out else "openai"
                out_path = outdir / f"{stem}-{ts}-{i + 1}.png"

            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            saved.append(str(out_path))
            print(f"SAVED {out_path}")
    finally:
        for f in files:
            try:
                f.close()
            except Exception:  # noqa: BLE001
                pass

    print("DONE " + " ".join(saved))


if __name__ == "__main__":
    main()
