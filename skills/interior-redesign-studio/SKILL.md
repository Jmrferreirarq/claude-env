---
name: interior-redesign-studio
description: Turn a single room photo into professional interior redesign concepts using Google's Nano Banana (Gemini) image model. The skill writes the professional image prompt for you — describing light, materials, scale, palette and style — then generates and iteratively edits photoreal renders from the user's real space. Activate on "redesign this room", "redesenha esta sala/quarto/cozinha", "interior makeover from a photo", "show me this room in [style]", "change the sofa/walls/floor", "stage this empty room", "what would this look like in Japandi/Scandinavian/etc". Pairs with the interior-design-expert skill for layout/color/lighting theory. NOT for exterior/landscape, floor-plan CAD, or pure text design.
allowed-tools: Read, Write, Edit, Bash
metadata:
  category: Design & Creative
  pairs-with:
  - skill: interior-design-expert
    reason: Use its space-planning, Munsell color and IES lighting theory to inform the image prompt
  tags:
  - interior
  - redesign
  - image-generation
  - nano-banana
  - gemini
  - staging
---

# Interior Redesign Studio

Turn one room photo into photoreal redesign concepts. The model (Google **Nano Banana** / Gemini
image) does the rendering; **this skill's job is to write the prompt like a designer**, ground it
in the real model, run the generation, and refine on command. Pairs with **interior-design-expert**
for space-planning / colour / lighting theory.

## When to Use

✅ Use for:
- Redesigning / restyling an existing room from a photo (new palette, furniture, mood)
- **Faithful** photoreal realization of a 3D/BIM model (keep everything, just make it real)
- Virtual staging of an empty room
- Targeted edits ("change the sofa to boucle", "warmer walls", "remove the rug")
- 2–3 style variations of the same space

❌ Do NOT use for:
- Exterior / landscape design
- Technical floor plans or CAD
- Brand / UI / graphic design

## Prerequisites (one-time)

1. **Google AI Studio API key** → https://aistudio.google.com/apikey
2. Set it as `GEMINI_API_KEY`.
3. Python deps: `pip install google-genai pillow`

> **Windows API key:** `generate.py` auto-resolves the key — if it's not in the process
> environment it reads the **User**-scope value (`setx`, stored in `HKCU\Environment`) directly
> from the registry, so it works from any shell with no manual loading.

## Honest limits — and when to use CineRender instead

- Nano Banana / Gemini is **generative**: it re-creates the image every time. It does **NOT**
  guarantee element-level fidelity even with a reference image — it will drift on railings, light
  fixtures, finishes and tile joints unless tightly constrained, and even then only approximately.
- Use AI for **fast concepts, staging, atmosphere, mood and lighting studies**.
- For **rigorous fidelity** (client deliverables, exact materials/joints) render in **Archicad
  CineRender** (real materials + geometry) and use AI only for post-atmosphere/people. Decide
  per view which output you need.
- **Source quality matters:** a low-res source PNG invites hallucination. Ask for a
  **high-resolution export** (2000 px+) from the model, surfaces visible — it cuts drift a lot.

## PASSO 0 — Compatibilização com o Archicad (OBRIGATÓRIO e BLOQUEANTE)

Nenhuma imagem (Caminho A/B/C) avança sem isto. Uma pasta NÃO prova o projeto — o incidente
`Teste . Paula Silva.jpg` (guardada na pasta do David Afonso mas era a casa da Paula Silva)
produziu uma reconciliação com o IFC errado e o palete todo errado.
1. Identificar o **projeto/modelo certo** — `discovery_list_active_archicads` (podem estar vários
   modelos abertos em portas diferentes). Confirmar pelo nome do ficheiro E perguntar ao utilizador.
2. Ler os **acabamentos reais** do modelo: Building Materials, superfícies `@`-prefixadas
   (`attributes_get_attributes_by_type` Surface → `attributes_get_surface_attributes`). Nota:
   superfícies com textura têm RGB branco (1,1,1) — o tom vive no bitmap; confirmar tons com o
   arquiteto.
3. **Ancorar o prompt** a esses acabamentos reais.
4. Só **depois** gerar.
5. **Dúvida de proveniência → PARAR e perguntar. Nunca gerar com dúvida.**
Outputs com palete errado ficam no disco mas renomeados a sinalizar (`*_ERRADO_palete-*`).

## Quality protocol — Caminhos A/B/C (canónico: `C:\comfy_dl\PROTOCOLO-QUALIDADE.md`)

Qualidade de foto de benchmark é um **protocolo, não sorte**. Três caminhos (resumo em
`ESTRUTURA.md` §4):
- **A — Nano Banana só (DEFAULT):** máxima qualidade fotográfica; com o prompt strict dá
  resultados no-invention limpos. **4 variações → escolher a melhor**; nunca confiar num único
  draw (a aleatoriedade era o "às vezes sim, às vezes não"). Aceita **micro-desvios de geometria**
  — o trade-off deliberado.
- **B — ControlNet só (denoise 0.35):** só quando a geometria tem de ser milimétrica. Teto de
  realismo mais baixo. Pipeline instalado e validado → `references/pipelines-locais.md`.
- **C — Híbrido (ControlNet → Gemini), EXCEÇÃO:** só vistas difíceis onde A ainda inventa.
- **Factos da API Gemini (não repetir mitos antigos):** modelo `gemini-3-pro-image` (Nano Banana
  Pro), 2K via `imageConfig`; **NÃO há seed numérica NEM strength/denoise** — coerência entre
  vistas = prompt fixo + reinjetar a vista vencedora como referência; "don't invent" é só prompt.
- **"validado" exige AMBOS:** (1) parece foto real (vs `quality-benchmark.png`) E (2) fiel ao
  render original — nada movido/removido/inventado. Falhar um = não validado.
- Registar cada vista em `ESTRUTURA.md` §10 (receita = engine+seed; coluna **Tipo**: ver
  fiel/variante abaixo).

## Modos de falha conhecidos do gerador (verificar SEMPRE)

- **Achata planos inclinados** (rampas, taludes, escadas exteriores, desníveis) — **não se
  corrige por prompt**. Vista com rampa/talude → Caminho B/C (depth), nunca A sozinho. Validar
  sempre os inclinados contra o original. E a partir de um **clay não há caminho** que dê foto +
  rampa fiel: produzir primeiro um render texturado (Archicad/Enscape) dessa vista e
  fotorrealizar esse.
- **Preenche superfícies lisas/vazias/ambíguas com o detalhe "esperado":** divisão vazia →
  plantas/cortinas/interruptores; entorno vazio → casas vizinhas/árvores/portões; sofito liso →
  caibros/vigas. Travar com o prompt strict/no-invention + **descrever o que a superfície É**
  (não basta "não inventes"); se persistir → máscara + recolor.
- **Fonte clay = acabamentos AUTORADOS:** um clay não pode dar "conversão fiel" — a IA autora os
  acabamentos (microcimento, aro preto). Só geometria/vãos são fiéis. Registar como **`variante`**
  (alteração de projeto assumida), nunca `fiel`; reconciliar com a spec do Archicad. `fiel` só
  quando a fonte já define os acabamentos.
- **Render acabado NÃO tem headroom de realismo:** um render Enscape polido já é fotorrealista —
  qualquer passe generativo só o degrada (materiais mudam, mobiliário deriva, escadas partem).
  "Converte para fotorrealismo" sobre um render acabado → perguntar QUE defeito concreto corrigir;
  permitido apenas acabamento não-generativo (upscale limpo, grade não-destrutivo).
- **Acabamento existente respeita-se, sempre:** num render acabado, nunca "corrigir" um
  acabamento existente (nem latão → aço escovado para satisfazer uma regra geral de materiais).
  Regras gerais guiam design NOVO; no existente, no máximo sinalizar a discrepância.
- **Adaptar o trabalho a CADA imagem:** análise fresca do estado real de cada vista; nunca herdar
  seeds, negativos, denoise, enquadramento ou premissas de outra vista. Confirmar qual ficheiro é
  o render final antes de construir o [SCENE].

## The fidelity contract: PRESERVE / CHANGE / ADD (agree this FIRST)

Before any prompt, establish — and write into the project's `design-spec.md` — three explicit
lists. **Default is conservative/faithful**: preserve everything, change only what the user
approves. Go broad ("restyle") ONLY if the user explicitly asks.

- **🔒 PRESERVE (never alter):** architecture, geometry, openings/glazing, **railings/balustrades
  (glass stays glass — never invent metal bars)**, staircase, **built-in cabinetry / wardrobes /
  kitchen fronts and their finish**, ceilings, ceiling heights, floor stereotomy. Lock **each
  finish explicitly** — a material approved for loose furniture (e.g. oak) must **NEVER spread**
  to built-ins or adjacent surfaces; the model spreads materials unless told not to.
- **🎨 CHANGE (only the approved items, piece by piece):** the specific furniture/finishes the
  user signs off. Anything not on this list defaults to PRESERVE.
- **➕ ADD (when it suits the space):** greenery/plants, small objects/props/tableware, pets, and
  **lighting** (see policy). Additions must not alter anything in PRESERVE.

## Lighting policy

Unless the user says otherwise, you MAY **correct/improve existing fixtures** and **add
atmosphere-coherent layered lighting** (ambient + task + accent), warm **2700–3000K, CRI ≥ 90**,
keeping fixture positions coherent and not flattening double-height volumes. If the user wants
fixtures untouched, treat them as PRESERVE. When unsure, ask.

## Narrative layer (define after concept + atmosphere)

Once the concept and atmosphere are agreed, build a **narrative** that runs across the whole set —
it turns disconnected renders into a guided "visit", reinforces cross-view coherence, and feeds
Phase 2. Write it into `design-spec.md` and let it drive render order, time-of-day, cast and props.
- **Logline** — one sentence: who lives here + the feeling + the moment.
- **Arc / sequence** — the views as a journey (arrival → reveal → dwell → gather → overview); each
  view is a scene.
- **Cast** — consistent inhabitants (+ pet) that thread through scenes, not random people per image.
- **Light/time plan** — choose deliberately: one coherent moment (max coherence) OR a day-arc
  (morning → golden hour → evening). Keep it grounded in the real orientation.
- **Beat per scene** — what's happening + the props/life that imply it + a short caption.
- **Continuity** — what must flow across scenes (season, time, cast, clothing tones, prop family).

> **Honest limit:** generative models do NOT keep consistent faces/identity across renders — the
> "same family" won't have the same faces. Keep people incidental/background, with consistent
> clothing tones, treated as representative figures. Light/life/prop narrative is reliable; faces
> are not. Narrative NEVER overrides the fidelity contract (built elements stay preserved).

## Workflow

> **Style is derived, not preset.** Read the analyzed image(s) — architecture, materials,
> finishes, proportions, mood — and infer the most coherent direction for THAT space. Propose it;
> only ask the user to choose when there are genuinely multiple reasonable directions. Never lead
> with a fixed style menu. If the user names a style, honour it.

> **Never render automatically. Ask for explicit permission before EVERY render — including
> re-renders and corrections.** First discuss and agree the concept AND the fidelity contract.
> Do NOT run `generate.py` on your own initiative — even to fix an error the user just flagged,
> ask first. Render only the specific view the user names, one at a time. With multiple views,
> ask which one; never pick for them.

### 1. Gather the brief + reconcile with the model
- **The photo**: path on disk (required for redesign). Images pasted into chat are **NOT on disk** —
  ask the user to save the file first. **Folder convention:** sources in `<project>\source\`,
  outputs in `<project>\renders\` (names like `<view>_phase1.png`).
- **Always analyze the Archicad model and reconcile each view with it (Tapir MCP).** Feed
  confirmed values into the prompt; flag conflicts with the spec. Useful commands:
  - `project_get_stories` — floor-to-floor + double-height heights.
  - `elements_get_selected_elements` + `elements_get_details_of_elements` — ask the user to select
    the floor slab / key element; read polygon (real dims), thickness, level.
  - `elements_get_elements_by_type` + `attributes_get_attributes_by_type` — elements + the
    material / fill / surface catalog.
  - `project_get_geo_location` — location + true north. **Verify, don't trust:** these are often
    Archicad **defaults** (e.g. Budapest, north 90° unrotated) → orientation is NOT reliable;
    real daylight comes from a real Project North or the architect's statement of which façade
    faces where.
  - Notes: floor tiling/surfaces are often **non-parametric** (generic material) → get the tile
    module/joints from the architect. No saved **Camera** elements is normal → the viewpoint comes
    from the source image; Tapir is the **data layer**, not the camera. A modal dialog open in
    Archicad blocks Tapir — ask the user to close it and retry.
- **Goal**: faithful realization / approved swaps / restyle / single edit.
- **Style**: only if the user volunteers one — otherwise infer (see note above).
- **Floor stereotomy is sacred:** preserve the exact tile module/size and joint positions; state
  it in every prompt (critical in top-down / floor-heavy views).
- **Aspect ratio**: `generate.py` **normalizes any source to a photographic 3:2** (oriented to the
  source) by default — the best ratio for interiors (matches the 35mm DSLR framing). Override per
  scene: **4:5** for tall/double-height heroes, **16:9** for wide panoramas; `--aspect match` to
  mirror the source. Note: re-framing to a different ratio than the source makes the model
  re-compose the edges (slight extension/crop) — expected when standardizing the output.

### 2. Write the prompt like a designer
Build ONE precise prompt, structured around the fidelity contract:
1. **Action + fidelity — front-load a strict volumetry lock.** Open the Phase-1 prompt with one
   short, forceful sentence BEFORE anything else: *"STRICTLY FORBIDDEN to alter OR remove
   anything — keep the volumetry, proportions, dimensions, structure, geometry, all cabinets,
   appliances, fixtures, skirting boards (and their existing colour) and details, camera, perspective
   and framing EXACTLY; do not omit or simplify any existing element. This is a faithful photograph of the SAME model; ONLY finishes, materials,
   furniture and lighting may change."* (Generative models tend to simplify/omit built detail — this
   reduces it but does not guarantee; absolute = CineRender/Twinmotion.) Then
   keep ALL architecture, glazing, railings (glass stays glass), built-in cabinetry and its finish,
   staircase, ceilings and floor tiling EXACTLY; spell out the PRESERVE list. Keep this lock ONE tight
   sentence at the head (not a long list — long prompts go bland). Honest: this maximizes fidelity on
   a generative model but does NOT guarantee it; absolute structure-lock = ControlNet/CineRender/Twinmotion.
2. **Approved CHANGES only:** name each piece + finish. Add explicitly: "wood/<material> appears
   ONLY on these loose pieces and must not spread to built-ins or walls."
3. **ADD:** greenery, props, pets, lighting — as agreed.
4. **Light:** direction + quality grounded in the REAL orientation (e.g. north glazing = cool
   indirect, no direct sun; warm 2700–3000K lamps; layered).
5. **Camera & realism:** "full-frame DSLR, 35mm, magazine quality, not a render; tactile slightly
   imperfect materials, neutral-warm white balance, gentle depth of field; keep the source framing."
6. **Negatives (folded into prose):** "no metal-bar railing (keep glass), no wood on built-ins,
   no clutter, no cold blue cast, no cartoon/3D-render look, no oversaturation, no text, no watermark."

See `references/presets.md` (P1 master, 0 base, 1 hero, 2 golden, 3 evening, 4 bright, 5 humanize)
and `references/prompt-recipes.md` / `references/style-guide.md`. For the local engines beyond
Nano Banana — Redraw (500-char cap), ComfyUI/ControlNet (Caminho B), IC-Light, SAM text→mask
inpaint, non-generative relight — see `references/pipelines-locais.md`.

### 3. Run the generator
`scripts/generate.py` (default model `gemini-3-pro-image-preview`; key auto-resolved; aspect
auto-detected). Outputs to `renders/`.
```
# Faithful / Phase 1 render from the source view
python scripts/generate.py --image "source/<view>.png" --prompt "<designer prompt>" --out "renders/<view>_phase1.png"

# Humanize the APPROVED render (ONE image by default)
python scripts/generate.py --image "renders/<view>_phase1.png" --prompt "<humanize prompt>" --n 1 --out "renders/<view>_phase2.png"
```
Add `--aspect` only to override; `--n N` only when the user explicitly asks for multiple.

### 4. Review — run the QA checklist BEFORE showing
Check element-by-element against the source and the PRESERVE list (adapt per project):
- [ ] Railings/balustrades as built (glass = glass, not metal bars)
- [ ] Built-in cabinetry / kitchen finish preserved (approved wood did NOT spread)
- [ ] Light fixtures coherent (improved ok, not invented)
- [ ] Staircase, doors, windows/glazing as source
- [ ] Floor stereotomy / joints correct
- [ ] Ceiling heights / double-height correct
- [ ] Natural light matches the real orientation
- [ ] Wood only on approved loose furniture; accent only where approved
- [ ] Framing = source; nothing invented; hands/faces ok (Phase 2)

Flag any drift and fix it (re-render with the anchor / a tighter prompt) before delivery. Edits =
feed the chosen render back in as `--image` with a small change instruction; keep all else identical.

## Cross-view coherence (multiple views of one project)

Views of one project must agree (same furniture, finishes, wood tone, accent, lighting). Each
generation is independent, so enforce it — **built per project from its analysis, NOT a fixed
template; coherence ≠ identical images.**
1. **Per-project `design-spec.md` ("bible").** Locked PRESERVE/CHANGE/ADD lists + reusable "fixed
   prompt block" reused verbatim across views.
2. **Reference-image chaining — use with care (it can override the viewpoint).** Tested: passing
   the anchor as a 2nd image made the model reproduce the ANCHOR's composition, not the source's
   framing. So: **only chain the anchor when the new view shares a similar framing.** For views with
   their **own distinct viewpoint, render source-only** (`--image source/XX.png`) and carry
   coherence through the **prompt text** (reference oak tone + palette + PRESERVE list) instead of
   the anchor image. When chaining is appropriate, pass `--image source --image anchor` and say
   "match furniture/finishes/palette of the second image; keep geometry, tiling and built elements
   from the first."
3. **QA pass.** Contact sheet of the finals; verify shared elements match; re-render drift using
   the anchor. `scripts/contact_sheet.py --inputs "renders/<stem>-*.png" --cols 2 --out renders/contact_sheet.png`

## Two-phase pipeline (faithful by default)

- **Phase 1 — photoreal conversion.** Analyze the furniture/space and the model; propose furniture
  improvements as **options to approve** — never auto-restyle. Apply the fidelity contract; one image.
  **Hybrid engine (per view) — HARD RULE:** generative AI re-creates the whole image and CANNOT
  preserve composition/structure. If the user requires the structure unchanged, AI is the WRONG
  tool — no prompt fixes it. So built-element-heavy / structural views (staircases, kitchens,
  bathrooms, built-ins) → **CineRender in Archicad ONLY** (assistant preps materials/sun/cameras via
  Tapir, read-only; the architect renders). Use **AI only for soft views** (bedrooms/suite/closet)
  where minor reinterpretation is acceptable. Never keep re-rendering a structural view in AI hoping
  to fix drift — stop and switch to CineRender, or to the **installed ControlNet pipeline
  (Caminho B — depth+canny locks structure; see `references/pipelines-locais.md`)**.
- **Phase 2 — humanization.** Feed the approved Phase 1 render back as `--image`; add candid people
  (and pets) that fit, WITHOUT changing the room, layout, lighting, materials or styling. **One
  image by default (`--n 1`)** — never auto-generate multiple; zoom-check hands/faces; ask before
  re-rolling; render multiple only on explicit request. Never humanize a non-photoreal source.
