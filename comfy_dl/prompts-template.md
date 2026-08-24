# Render → Photo · Reusable Prompt Template (ControlNet pipeline)

Standing template for EVERY image. Two layers: **Layer 1 is fixed** (never rewrite);
**Layer 2 is filled per scene** (ideally auto-derived from the render / Archicad spec).

## Per-image workflow (Claude Code)
1. Analyze the new render and auto-fill the `[SCENE]` block below (list the real finishes you see).
2. Show me the filled SCENE block to confirm/correct before generating.
3. Generate with the FIXED RECIPE (depth+canny). Then Ultimate SD Upscale.
4. Save as `<view>_v#.png` and produce an Enscape | result comparison.

---

## FIXED RECIPE (Layer 1 — always)
- ControlNet: **depth + canny**, daylight conversion
- canny weight **~0.85**, base **denoise 0.35**, upscale **denoise 0.20**
- seed: keep a fixed seed per view (document it) for reproducible compares
- target: lock geometry, volume, perspective, layout — never change structure

## GLOBAL POSITIVE (Layer 1 — prepend to every prompt)
```
photorealistic architectural interior photograph, natural daylight, real tactile
materials, faithful to the existing design and finishes, accurate proportions and
perspective, soft natural shadows, realistic reflections, warm 2700K accent lighting,
high detail, shot on 35mm. Keep the exact same geometry, layout and viewpoint.
```

## GLOBAL NEGATIVE (Layer 1 — structural, always)
```
distorted geometry, warped lines, bent walls, changed layout, moved furniture,
extra objects, duplicated or removed elements, wrong perspective, cartoon, cgi,
3d render, illustration, plastic, lowres, blurry, oversaturated, text, watermark
```

---

## [SCENE] — Layer 2 (auto-fill per image, then confirm)
Fill only what exists in the render. Be specific about color + material + finish.

```
SCENE FINISHES (positive — append after the global positive):
- Cabinetry / millwork: <e.g. matte cream handleless tall units; light oak uppers>
- Countertops / island: <e.g. white stone waterfall top; oak slatted island base>
- Hardware / metals: <e.g. BLACK handles; brushed-steel appliances; black taps>
- Flooring: <e.g. light oak wood planks>
- Walls / ceiling: <e.g. off-white matte; grey large-format tile>
- Joinery / feature: <e.g. oak slatted TV wall with black surround>
- Seating / upholstery: <e.g. oak-top stools, black frames; green fabric chairs>
- Window treatment: <e.g. white sheer curtains>
- Other fixed items: <sanitaryware, shower, lighting fixtures, etc.>
- Context through glazing: <e.g. green garden visible>

SCENE NEGATIVES (drift-watch — append after the global negative):
<list the finishes that tend to drift on THIS scene, e.g. brass handles, green
curtains, cushioned stool tops — items that are WRONG for this specific image>
```

---

## Notes
- Never globalize SCENE finishes or SCENE negatives — they are wrong for other rooms
  (a bathroom has no stools; green may be correct elsewhere).
- If a finish still drifts after one regen, fix only that area with **inpaint at denoise ~0.25**
  instead of regenerating the whole image.
- Best source for Layer 2 = the project's Archicad material schedule (hook for later:
  export finishes per room and auto-populate the SCENE block).
```
