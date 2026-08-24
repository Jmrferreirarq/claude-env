# Presets — Ready-to-Use Photoreal Prompts

Battle-tested prompts for turning a 3D model / render into natural photoreal interior photos,
and for adding life. Workflow: generate the **base** once, then **edit** by feeding the previous
render back in as `--image` and applying one preset at a time. Prefer the Pro model
(`gemini-3-pro-image-preview`).

General realism tail to keep on most prompts:
`Photorealistic, 35mm full-frame, natural soft contrast, true tactile materials, no text, no signage, no watermark.`

> **Respect the fidelity contract (see SKILL.md):** in faithful mode, name the PRESERVE elements
> (glass railings, built-in cabinetry/finish, fixtures, floor tiling) and add "approved material
> only on named loose pieces — not on built-ins/walls." The presets below light & style the scene;
> they do NOT license changing built elements unless the user asked for a restyle.

---

## TWO-PHASE PIPELINE (default)
- **PHASE 1 — photoreal + best lighting** → use preset **P1 (master)** below, or **0 → 1** plus a
  lighting variant (**2 golden / 3 evening / 4 bright**). Output = best realistic empty shot.
- **PHASE 2 — humanization** → feed the approved Phase 1 image back in and use preset **5**.
  Never humanize a non-photoreal source; always humanize the Phase 1 output.

### P1 (master) — photoreal + best possible lighting, in one shot
Run on the original 3D model / render. Combines fidelity + realism + great lighting + light styling.
```
Turn this 3D model / render into a real architectural photograph, shot on a full-frame DSLR
with a 35mm lens — magazine quality, not a render. Keep the exact same room, layout, camera
angle, proportions, colors and materials; do not redesign anything, only make it real and
light it beautifully.

Lighting: soft directional daylight raking from the large window on the left with natural
falloff toward the back, warm light bounce off the wood and floor, soft realistic contact
shadows, gentle global illumination and subtle color bleed; recessed ceiling lights dim and
warm, secondary to the daylight. Warm, inviting, balanced exposure with detail kept in
highlights and shadows.

Materials tactile and slightly imperfect: matte greige porcelain floor with faint sheen and
soft reflections, walnut with real grain and low satin sheen, fabrics with visible weave,
stone countertop with fine texture. Subtle tasteful styling (no people): low-pile textured
rug under the living area, a folded throw on the sofa, a few design books and a ceramic bowl
on the coffee table, a wooden board and a bowl of fruit on the island.

35mm, gentle depth of field, faint atmospheric haze, neutral-warm white balance, subtle
vignette. Photorealistic, true tactile materials. No people, no text, no signage, no watermark.
```
Lighting swap-ins (replace the first lighting sentence): golden → `warm golden-hour sun raking
low across the floor, long soft shadows, amber glow`; evening → `evening, pendants and recessed
lights glowing warm 2700K, dusk through the windows, cozy pools of light`; bright → `bright soft
overcast daylight, airy and fresh, crisp neutral-warm tones`.

---

## 0. BASE — 3D model → photoreal (faithful)
Use on the original 3D/render. Keeps layout, colors and materials; just makes it real.
```
A real interior photograph of an open-plan living-dining-kitchen, shot on a full-frame DSLR
with a 35mm lens, natural and candid like an architecture magazine — not a render. Keep the
same layout, camera angle, proportions, colors and materials as the reference; only make it
look like a real photo. Soft natural daylight from a large window out of frame on the left,
gentle falloff toward the back, realistic soft shadows, warm light bounce off wood and floor,
subtle color bleed. Tactile, slightly imperfect materials. Recessed ceiling lights dim and
warm, secondary to the daylight. Gentle global illumination, soft contact shadows, faint
atmospheric haze, neutral-warm white balance. No people, no text, no watermark.
```

## 1. HERO — warm, natural, lightly styled
Edit of the base. The everyday go-to look.
```
Keep this exact interior photograph — same room, layout, camera, colors and materials — but
elevate it into a warm, natural architecture-magazine shot. Shift white balance slightly
warmer; add soft late-morning daylight raking from the left with gentle falloff so the room
has depth and direction. Warm bounce off the walnut and wood floor, soft contact shadows.
Subtle tasteful styling (no people): low-pile textured wool rug under the living area, a
folded throw over the charcoal sofa, stacked design books and a small ceramic bowl on the
round coffee table, a wooden board and a bowl of fruit on the kitchen island. Everything else
identical. 35mm, gentle depth of field (foreground table sharp), faint haze, subtle vignette.
Inviting, minimal, lived-in. No people, no text, no watermark.
```
Note: if the result gets too amber, add: `pull warmth back ~15%, let the yellow armchair and
walnut keep their true color; add a touch of clarity so back shadows don't crush.`

## 2. GOLDEN HOUR — warm, cinematic
Swap the light line in the HERO preset for:
```
warm golden-hour sunlight raking low across the floor from the left, long soft shadows,
amber glow on the walls, cozy cinematic atmosphere.
```

## 3. EVENING / AMBIANCE — dusk, lamps on
Swap the light line in the HERO preset for:
```
evening interior after sunset, deep blue dusk through the windows, pendants and recessed
lights glowing warm 2700K, table and floor lamps casting cozy overlapping pools of light,
soft warm reflections on wood and stone, intimate relaxed mood.
```
Note: keep highlights from blowing out — `lamps glow softly, no harsh hotspots; preserve
detail in the dark corners`.

## 4. BRIGHT / AIRY — fresh daylight
Swap the light line in the HERO preset for:
```
bright soft overcast daylight filling the room evenly, airy and fresh, crisp neutral-warm
tones, light shadows, clean and open feel, high-key but not blown out.
```

## 5. HUMANIZE — add candid people (PHASE 2)
Feed the **approved Phase 1 photo** back in as `--image`. Never run on a non-photoreal source.
Generate 3–4 variations and pick the cleanest (hands/faces can glitch — zoom-check before use).
```
Keep this exact interior photograph identical — same room, architecture, layout, furniture,
colors, materials, lighting, white balance and camera angle. Do NOT redesign, move, add or
remove anything in the space. Only add candid, natural people living in the room, shot
documentary-style.

Add 2-3 people that fit this home, in relaxed everyday poses with casual clothing in muted
tones that suit the palette (e.g. someone reading on the sofa, a person walking toward the
kitchen with a mug; optionally a child playing on the rug or a sleeping cat). Realistic
human proportions and correct anatomy, natural hands, believable scale and contact with the
floor and furniture. The people inherit the existing lighting, shadows and depth of field.

Candid lifestyle interior photography, 35mm, gentle depth of field. No text, no watermark,
no distortion, no changes to the room.
```
Fixes if a person looks off: re-run (cheapest), or add `correct the hands and face of the
person on the left, keep everything else identical`. Reduce crowding with `only 1-2 people,
more negative space`.
