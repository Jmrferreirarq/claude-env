# Prompt Recipes — Interior Redesign

Reusable patterns. Fill the `[brackets]`. Keep prompts concrete: name pieces, finishes, light and
palette. **Default mode is FAITHFUL** (preserve everything, change only what's approved) — the
restyle recipes near the bottom are for when the user explicitly asks to restyle.

Always end realism prompts with: `full-frame DSLR, ~35mm, magazine quality not a render, realistic
shadows and reflections, keep the source framing, no text, no watermark.`

---

## FAITHFUL MODE (default)

### A0. Faithful realization (preserve everything, just make it real)
```
Make this 3D model view a real architectural photograph — magazine quality, not a render. Keep the
EXACT same camera, geometry, layout and proportions. Preserve ALL built elements unchanged:
[glass balustrade — slim glass, NOT metal bars], staircase, [built-in cabinetry/kitchen fronts and
their finish], windows/glazing, ceilings, and the floor tiling (module + joint positions). Do not
redesign anything. Light it well: [orientation-correct daylight] plus warm 2700-3000K lamps,
CRI-accurate, soft realistic contact shadows. Tactile, slightly imperfect materials. No cartoon or
3D-render look, no cold blue cast, no text, no watermark.
```

### A1. Faithful + approved swaps (the everyday workflow)
```
Make this a real architectural photograph; keep the EXACT camera, geometry and proportions.
PRESERVE unchanged: [glass railings (glass, not bars), staircase, built-in cabinetry/kitchen in
WHITE, windows, ceilings, ceiling heights, floor 60x120 aligned tiling]. CHANGE ONLY (approved):
[sofa -> oatmeal linen; armchair -> terracotta boucle; coffee table/TV unit/dining table -> oak;
walls -> creamy off-white]. Wood appears ONLY on those loose pieces and must NOT spread to built-ins
or walls. ADD: potted greenery / small props / a pet, if it suits. Light: [orientation-correct],
warm 2700-3000K layered. Photoreal, tactile materials. No metal-bar railing, no wood on built-ins,
no cold cast, no text, no watermark.
```

### A2. Coherent extra view (reference-image chaining)
Pass two images: `--image source/<view>.png --image renders/<approved-anchor>.png`.
```
Make this a real photo. Keep the geometry, camera, floor tiling and ALL built elements from the
FIRST image. Match the furniture, finishes, wood tone, accent colour and lighting established in
the SECOND image. Change nothing else. [orientation-correct light]. Photoreal, no text, no watermark.
```

### C. Targeted edit (feed the previous render back in)
```
Keep everything in this image identical — same room, layout, camera, lighting and all built
elements — but [one single change]. Photorealistic, consistent shadows, no text, no watermark.
```

---

## RESTYLE MODE (only when the user explicitly asks to restyle)

### R1. Full redesign (keep the architecture)
```
Redesign this [room] in a [style] style. Keep the existing architecture, openings, ceiling height,
built elements and natural-light direction unchanged. Furnish with [2-4 key pieces + materials].
Palette: [anchor], [secondary], [accent]. Lighting: [direction + warmth]. Photorealistic, eye-level,
35mm, realistic shadows, no text, no watermark, no people.
```

### R2. Virtual staging (empty room)
```
Stage this empty [room] as a [style] [function]. Add [furniture set]. Respect the real floor, walls,
windows and light. Palette: [3 colors]. Magazine-quality, photorealistic, 35mm, no text, no watermark.
```

### R3. Palette-led restyle
```
Restyle this [room] around a [mood] palette of [c1], [c2], [c3]. Update upholstery and textiles to
match while keeping the furniture layout, architecture and built elements. Photorealistic, 35mm,
no text, no watermark, no people.
```

### R4. Material swap (a finish the user approved to change)
```
Keep this room's layout, architecture and other finishes. Change ONLY [surface] to [material/finish].
Do not let the new material spread to other surfaces. Photorealistic, consistent light, no text, no watermark.
```

### R5. Same room, multiple styles
Swap only the style block between runs so the space stays comparable.

---

## Tips
- **Preserve by naming.** To keep a real feature, name it explicitly ("keep the existing GLASS
  balustrade", "keep the white kitchen fronts"). The model drops/changes what you don't name.
- **Stop material spread.** Always add "wood/<material> only on [pieces]; not on built-ins/walls."
- **Ground the light in the real orientation.** North glazing = cool indirect, no direct sun; only
  add direct sun on façades that really get it. Model geo/north may be defaults — verify.
- One clear instruction per edit beats many at once — iterate.
- Evening: "warm 2700K lamp light, layered ambient + task + accent." Bright: "soft overcast daylight."
- Aspect is auto-detected from the source; override with `--aspect` only when needed.
- If text/labels appear, repeat "no text, no signage, no watermark."
