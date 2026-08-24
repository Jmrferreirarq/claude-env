# prompts-template.md — Pipeline ControlNet (ComfyUI + SDXL, RealVisXL)

> Objetivo: fotorrealismo **fiel ao render Enscape**, sem alucinar arquitetura.
> A geometria fica trancada pelo ControlNet (depth+canny); o prompt só descreve **materiais/luz**.
> Para cada vista: copiar o preâmbulo fixo + preencher o bloco **[SCENE]** com os acabamentos
> REAIS desse render (derivados da imagem, não de um preset) + negativo fixo.

---

## Preâmbulo fixo (preservação)
```
high-end photoreal interior photograph, keep architecture, openings, layout, the staircase and tile sizes exactly; move/remove nothing; rich realistic materials, magazine quality, full-frame 35mm.
```

## [SCENE] — acabamentos reais (preencher por render)

### 06_cozinha_p4 (base Enscape escolhida — 2026-06-25)
```
Open-plan kitchen-living. Warm off-white matte walls and sloped ceiling with recessed downlights. White kitchen island with a pale light-stone (quartz) worktop, black induction hob and a wood chopping board; brushed stainless steel sink and tap on the near side. Three pale cream conical pendant lamps on thin black cords over the island. Back wall: wall-mounted black flat TV above a long low light-oak media console. Oatmeal fabric sofa and one terracotta/tan armchair. Light oak dining table with light oak chairs; a leafy green plant. Large sliding glass wall to a green garden, with pale sheer translucent curtains drawn to the sides. Staircase on the right: solid oak treads with white structure and white wall, closed steps (no gaps). Greige large-format porcelain floor tiles; keep existing skirting. Bright soft even natural daylight, airy, gentle soft shadows.
```

## Negativo fixo
```
cartoon, cgi, plastic, 3d render look, lowres, blurry, deformed, distorted perspective, extra windows, extra stairs, added doors, changed layout, green curtains, green chairs, bar stools, slatted tv wall, watermark, text, people
```
> Nota: os negativos `green curtains, green chairs, bar stools, slatted tv wall` existem de
> propósito para impedir que voltem as alucinações da versão gpt-image.

---

## Parâmetros do pipeline (validados — 8 GB)
- **Checkpoint:** RealVisXL_V5.0_fp16.safetensors · **ControlNet:** controlnet-union-sdxl (depth+canny)
- **ControlNet weights:** depth ≈ 0.6 · **canny ≈ 0.85**
- **Pré-processadores:** Depth Anything V2 + Canny (sobre o render Enscape)
- **img2img denoise base:** **0.35** (fiel)
- **Ultimate SD Upscale denoise:** **0.20** (só nitidez/textura, não inventa)
- **Sampler:** dpmpp_2m · **scheduler:** karras · **steps:** 30 · **cfg:** 6
- **Luz:** daylight (no prompt) · **seed fixa documentada por render** (ver tabela abaixo)

### Seeds documentadas
| Render | seed | denoise base | canny | notas |
|---|---|---|---|---|
| 06_cozinha_p4 | **70414** | 0.35 | 0.85 | base Enscape; depth 0.6; UltimateSDUpscale 2x denoise 0.20 (RealESRGAN_x4plus); → cozinha_enscape_v1.png (3072x2064). Sem correções por objeto (nada derivou). |

---

## Aprendizagens (2026-06-25)

**(a) Recolor vs inpaint — escolher pela natureza da alteração:**
- **Só mudança de cor numa peça fina/pequena** (ex.: puxadores) → **recolor não-generativo**
  (Pillow, remapeamento de cor preservando luminância) OU inpaint de baixa denoise. Não vale a
  pena gerar — é mais seguro e não toca na forma. Ver [[redraw-tool]].
- **Mudança de material ou de forma** (ex.: estofo→madeira, cortina verde→linho branco) →
  **inpaint mascarado generativo** (crop-stitch + SetLatentNoiseMask + composição por máscara).

**(b) Inpaint de material pede denoise alto:** para uma **mudança de material/forma** usar
**denoise 0.6–0.75**, NÃO 0.5. A 0.5 a alteração não "pega" quando os tons de partida e
destino são próximos (estofo beige vs carvalho ficou praticamente igual a 0.50; só a 0.72
apareceu o grão de madeira). Recolor/cor+luz puro pode ficar por ~0.55.
