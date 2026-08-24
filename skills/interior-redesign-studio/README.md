# interior-redesign-studio

A Claude Code skill that turns one room photo into photoreal interior redesign concepts.
Claude writes the designer-grade prompt, grounds it in the real BIM model, runs the
generation and QAs the result. Pairs with `interior-design-expert` (theory) and
`archicad-fa-pro` (BIM data via Tapir).

**Engines** (chosen per view — see `SKILL.md` "Quality protocol"):
- **Caminho A — Nano Banana / Gemini** (default): best photo quality; 4 variations → pick best;
  accepts micro-geometry deviation.
- **Caminho B — ComfyUI + ControlNet** (installed, `C:\ComfyUI_windows_portable`): depth+canny
  structure lock for zero-distortion views (ramps, stairs, kitchens). See
  `references/pipelines-locais.md`.
- **Caminho C — hybrid** (exception): ControlNet → Gemini for hard views.
- Plus: SAM text→mask object inpaint, IC-Light, non-generative `relight.py`, Redraw
  (arch.redraw.pro, 500-char prompt cap).

**Hard rules baked into the skill** (learned on real projects — do not relearn them):
- **PASSO 0 (blocking):** confirm the right Archicad project + read real finishes before any
  generation; provenance doubt → stop and ask.
- Never render without explicit permission; one image by default.
- Fidelity contract (PRESERVE/CHANGE/ADD); floor stereotomy is sacred; finishes that exist in a
  finished render are respected, always.
- `fiel` vs `variante`: a clay source can only ever produce a `variante` (authored finishes).
- Known generator failure modes: flattens slopes (→ Caminho B/C), fills blank surfaces with
  "expected" detail (→ strict/no-invention prompts), degrades already-photoreal renders (→
  non-generative finishing only).

Canonical quality docs: `C:\comfy_dl\PROTOCOLO-QUALIDADE.md` + `ESTRUTURA.md`.

## Install (Claude Code)
Copy this folder to your skills directory:
- Personal: `C:\Users\<you>\.claude\skills\interior-redesign-studio\`
- Project:  `<project>\.claude\skills\interior-redesign-studio\`

Final path must be: `...\.claude\skills\interior-redesign-studio\SKILL.md`

## One-time setup
1. Get a Google AI Studio API key: https://aistudio.google.com/apikey
2. Set it: `setx GEMINI_API_KEY "your-key"` (Windows) — `generate.py` auto-resolves it from
   `HKCU\Environment`, so no manual loading in any shell.
3. Install deps: `pip install google-genai pillow`

## Use
Restart Claude Code, then say e.g.:
"Redesenha esta sala, mantendo as janelas" and give the photo path
(sources in `<project>\source\`, outputs land in `<project>\renders\`).

## Models (Gemini API)
- `gemini-3-pro-image-preview` (Nano Banana Pro) — default, best fidelity (~$0.13/img)
- `gemini-2.5-flash-image` (Nano Banana) — fast/cheap (~$0.04/img)
- API facts: 2K via `imageConfig`; **no numeric seed, no denoise/strength** — cross-view
  coherence is fixed prompt + winning view re-injected as reference.

## Notes
- Outputs carry Google's invisible SynthID watermark.
- Each render uses real API credits — that's why rendering is never automatic.
- Third-party model; use a dedicated API key.
