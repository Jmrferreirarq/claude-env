#!/usr/bin/env python3
"""Interior Redesign Studio - image generation/editing via Google Gemini (Nano Banana).

Usage:
  python generate.py --prompt "..." [--image room.jpg ...] [--out out.png]
                     [--model gemini-3-pro-image] [--aspect 16:9] [--size 2K]
                     [--n 1] [--session NAME]

Setup:
  pip install google-genai pillow
  export GEMINI_API_KEY=...   (Windows: setx GEMINI_API_KEY "...")
  Get a key at https://aistudio.google.com/apikey

Notes:
  --image can be repeated to send multiple reference images (e.g. the room + a
  style reference).
  For iterative edits prefer --session NAME (Google-recommended chat mode): the
  conversation history is replayed on every call, so "make the sofa green" edits
  the previous render with full context. Session state lives in
  renders/.sessions/NAME.json next to the renders. One-off edits can still pass
  the previous render back as --image.
"""
import argparse
import datetime
import json
import mimetypes
import os
import sys
from pathlib import Path


def eprint(*a):
    print(*a, file=sys.stderr)


def resolve_api_key():
    """Find the Gemini key. On Windows, fall back to the User-scope env var
    (set via `setx`, stored in HKCU\\Environment) which a freshly-spawned shell
    may not have inherited into its process environment."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key
    if os.name == "nt":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                    try:
                        val, _ = winreg.QueryValueEx(k, name)
                        if val:
                            return val
                    except FileNotFoundError:
                        continue
        except Exception:  # noqa: BLE001
            pass
    return None


# Aspect ratios Gemini image accepts, with their decimal value.
STD_ASPECTS = {
    "1:1": 1.0, "5:4": 1.25, "4:3": 4 / 3, "3:2": 1.5, "16:9": 16 / 9, "21:9": 21 / 9,
    "4:5": 0.8, "3:4": 0.75, "2:3": 2 / 3, "9:16": 9 / 16,
}


def nearest_aspect(width, height):
    """Map pixel dimensions to the closest supported aspect-ratio string."""
    if not width or not height:
        return None
    r = width / height
    return min(STD_ASPECTS, key=lambda a: abs(STD_ASPECTS[a] - r))


def main():
    p = argparse.ArgumentParser(
        description="Generate/edit interior images with Gemini (Nano Banana)."
    )
    p.add_argument("--prompt", required=True, help="The designer-written image prompt.")
    p.add_argument("--image", action="append", default=[],
                   help="Input image(s) to redesign/edit. Repeatable. Omit for text-to-image.")
    p.add_argument("--out", default=None,
                   help="Output PNG path. Default: auto-named in ./renders/")
    p.add_argument("--model", default=os.environ.get("NB_MODEL", "gemini-3-pro-image"),
                   help="gemini-3-pro-image (Nano Banana Pro, high quality) or "
                        "gemini-3.1-flash-image (Nano Banana 2, fast).")
    p.add_argument("--aspect", default=None,
                   help="Aspect ratio e.g. 3:2, 4:5, 16:9. Default: normalize to a photographic 3:2 "
                        "(oriented to the source). Use 'match' to mirror the source's nearest ratio.")
    p.add_argument("--size", default=None, choices=["1K", "2K", "4K"],
                   help="Output resolution (gemini-3-pro-image only). E.g. 2K for client-facing renders.")
    p.add_argument("--n", type=int, default=1, help="Number of variations to render.")
    p.add_argument("--session", default=None,
                   help="Chat session name for iterative editing. Reuses conversation history from "
                        "renders/.sessions/<NAME>.json; each call adds one turn.")
    args = p.parse_args()

    api_key = resolve_api_key()
    if not api_key:
        eprint("ERROR: GEMINI_API_KEY not set. Get one at https://aistudio.google.com/apikey")
        sys.exit(2)

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        eprint("ERROR: missing dependency. Run: pip install google-genai pillow")
        sys.exit(2)
    try:
        from PIL import Image
    except ImportError:
        eprint("ERROR: missing Pillow. Run: pip install pillow")
        sys.exit(2)

    client = genai.Client(api_key=api_key)

    contents = [args.prompt]
    for img_path in args.image:
        if not os.path.exists(img_path):
            eprint(f"ERROR: input image not found: {img_path}")
            sys.exit(2)
        contents.append(Image.open(img_path))

    # Source dimensions (for orientation / 'match').
    src_w = src_h = None
    if args.image:
        try:
            with Image.open(args.image[0]) as _im:
                src_w, src_h = _im.size
        except Exception:  # noqa: BLE001
            src_w = src_h = None

    aspect = args.aspect
    if aspect in (None, "auto", "default"):
        # Always normalize to a photographic 3:2, oriented to the source
        # (portrait source -> 2:3). This standardizes any input format.
        if src_w and src_h and src_h > src_w * 1.05:
            aspect = "2:3"
        else:
            aspect = "3:2"
        print(f"ASPECT {aspect} (default photographic 3:2)")
    elif aspect == "match":
        aspect = nearest_aspect(src_w, src_h) if (src_w and src_h) else None
        print(f"ASPECT {aspect} (matched to source)")

    cfg_kwargs = {"response_modalities": ["IMAGE"]}
    img_cfg_kwargs = {}
    if aspect:
        img_cfg_kwargs["aspect_ratio"] = aspect
    if args.size:
        if "pro-image" not in args.model:
            eprint(f"WARNING: --size is only supported by gemini-3-pro-image; ignoring for {args.model}.")
        else:
            img_cfg_kwargs["image_size"] = args.size
    if img_cfg_kwargs:
        cfg_kwargs["image_config"] = types.ImageConfig(**img_cfg_kwargs)
    config = types.GenerateContentConfig(**cfg_kwargs)

    # Chat session (Google-recommended pattern for iterative image editing):
    # replay prior turns as history so edits keep full conversational context.
    session_file = None
    session = {"model": args.model, "turns": []}
    chat = None
    if args.session:
        if args.n != 1:
            eprint("WARNING: --session implies --n 1 (one turn per call); rendering 1.")
            args.n = 1
        session_file = Path("renders") / ".sessions" / f"{args.session}.json"
        if session_file.exists():
            try:
                session = json.loads(session_file.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                eprint(f"ERROR: corrupt session file {session_file}: {e}")
                sys.exit(2)
        history = []
        for turn in session["turns"]:
            parts = [types.Part.from_text(text=turn["prompt"])]
            for ip in turn.get("images", []):
                if os.path.exists(ip):
                    mime = mimetypes.guess_type(ip)[0] or "image/png"
                    parts.append(types.Part.from_bytes(
                        data=Path(ip).read_bytes(), mime_type=mime))
            history.append(types.Content(role="user", parts=parts))
            out = turn.get("output")
            if out and os.path.exists(out):
                history.append(types.Content(role="model", parts=[
                    types.Part.from_bytes(data=Path(out).read_bytes(),
                                          mime_type="image/png")]))
        chat = client.chats.create(model=args.model, config=config, history=history)
        if history:
            print(f"SESSION {args.session} ({len(session['turns'])} previous turn(s))")

    saved = []
    for i in range(args.n):
        try:
            if chat is not None:
                resp = chat.send_message(contents)
            else:
                resp = client.models.generate_content(
                    model=args.model, contents=contents, config=config
                )
        except Exception as e:  # noqa: BLE001
            eprint(f"ERROR calling model: {e}")
            sys.exit(1)

        img_bytes = None
        for cand in (resp.candidates or []):
            parts = getattr(cand.content, "parts", None) or []
            for part in parts:
                inline = getattr(part, "inline_data", None)
                if inline and getattr(inline, "data", None):
                    img_bytes = inline.data
                    break
            if img_bytes:
                break

        if not img_bytes:
            eprint("ERROR: no image returned (request may have been blocked, or "
                   "the model replied with text only).")
            try:
                if resp.text:
                    eprint("Model text:", resp.text)
            except Exception:  # noqa: BLE001
                pass
            sys.exit(1)

        if args.out and args.n == 1:
            out_path = Path(args.out)
        else:
            outdir = Path("renders")
            outdir.mkdir(parents=True, exist_ok=True)
            ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            stem = Path(args.out).stem if args.out else "redesign"
            out_path = outdir / f"{stem}-{ts}-{i + 1}.png"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        saved.append(str(out_path))
        print(f"SAVED {out_path}")

        if session_file is not None:
            session["turns"].append({
                "prompt": args.prompt,
                "images": [str(Path(ip).resolve()) for ip in args.image],
                "output": str(out_path.resolve()),
            })
            session_file.parent.mkdir(parents=True, exist_ok=True)
            session_file.write_text(
                json.dumps(session, ensure_ascii=False, indent=2), encoding="utf-8")

    print("DONE " + " ".join(saved))


if __name__ == "__main__":
    main()
