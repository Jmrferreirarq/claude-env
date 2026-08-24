---
name: interior-redesign-workflow
description: Setup and workflow for photoreal interior renders via Nano Banana (Gemini) in the Nanobana project
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f15889a-5692-401e-a6a0-56956625988e
---

The user runs photoreal interior redesign renders from room photos using the `interior-redesign-studio` skill (Google Nano Banana / Gemini image model), paired with `interior-design-expert` for layout/color/lighting theory.

**Setup (verified working 2026-06-22):**
- `GEMINI_API_KEY` is set at the Windows **User** scope. `generate.py` now auto-resolves it from `HKCU\Environment` when not in the process env, so it works from any shell (Bash or PowerShell) with no manual loading.
- `generate.py` also **auto-detects the aspect ratio** from the source image (pass `--aspect` only to override).
- The skill's `SKILL.md` was truncated mid-sentence (ended at step 2); completed with steps 3 (run) and 4 (review/iterate) on 2026-06-22.
- Python 3.14 with `google-genai` + `pillow` installed.
- Script: `~/.claude/skills/interior-redesign-studio/scripts/generate.py` (default model `gemini-3-pro-image-preview`).
- Project folder: `C:\Users\José Ferreira\Nanobana`. Folder convention: source images in `source\`, all generated images in `renders\`.

**Source images come from Archicad** (BIM model) — real dimensions exist, so pull true measurements (archicad-fa-pro skill / Tapir MCP, or a dimensioned export) when scale fidelity matters instead of estimating.

**Image handoff gotcha:** images pasted into chat are NOT on disk and not in the clipboard — ask the user to save them into `Nanobana\source\`, then read the file path.

**Workflow:** Phase 1 = photoreal render from the source image; Phase 2 = humanization (feed Phase 1 back as `--image`, add candid people, n=4, pick cleanest). Style must follow [[style-from-images]] — derive it from the analyzed space, don't impose a preset.

**Contact sheet:** for multi-variation runs, compose a labeled grid with `scripts/contact_sheet.py` (`--inputs "renders/<stem>-*.png" --cols 2 --title ... --out renders/contact_sheet.png`) so the user picks fast.

**Skill alignment (done 2026-06-22):** `interior-design-expert` no longer points to Stability/Ideogram MCPs — it now hands photoreal rendering to this skill (Nano Banana) and references Archicad/Blender for the 3D source.
