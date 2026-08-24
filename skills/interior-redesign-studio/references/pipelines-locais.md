# Pipelines locais — Redraw, ComfyUI/ControlNet, IC-Light, SAM inpaint, relight

Receitas validadas nesta máquina (RTX 3070 8GB). Consolidado da memória `redraw-tool` em 2026-08-24.
Docs canónicos do protocolo de qualidade: `C:\comfy_dl\PROTOCOLO-QUALIDADE.md` + `ESTRUTURA.md`.

## Redraw (us.arch.redraw.pro, "Melhorar render")

- Redraw **já analisa e preserva a imagem-fonte**; o prompt é só para instruções específicas.
  O boilerplate "preserve everything" é desnecessário E era truncado.
- **Campo de prompt limitado a 500 caracteres** — prompts curtos, só os deltas
  (acabamentos/mobiliário a mudar), nunca o ensaio de preservação.
- **Modos:** Fidelidade (máx. fidelidade), Realismo (mais fotográfico, mais drift), Premium,
  Iluminação. **O utilizador prefere Realismo.** Como o Realismo deriva mais, front-load das
  âncoras críticas de "keep" (escada fechada, layout da cozinha, mover/remover nada) antes dos
  deltas. Se escada/cozinha derivarem em Realismo → essa vista passa a Fidelidade.
- Workflow: Fase 1 = melhorar render com o delta-prompt curto; Fase 2 = repetir sobre a imagem
  aprovada com um curto "add people".

## ComfyUI / ControlNet — structure-lock (Caminho B) — INSTALADO E VALIDADO (2026-06-23)

- `C:\ComfyUI_windows_portable` (correr `run_nvidia_gpu.bat`, serve http://127.0.0.1:8188).
- **RealVisXL_V5.0_fp16** (checkpoint) + **controlnet_union_sdxl_promax** + `comfyui_controlnet_aux`
  + ComfyUI-Manager. Driven via API (`/upload/image`, `/prompt`, `/history`, `/view`).
- **Receita validada (sem alucinação + rica):** img2img + ControlNet Union **depth (0.6) +
  canny/lineart (0.5)**, **denoise ~0.5 fiel / ~0.6 sweet spot / 0.7 mais transformação**
  (drift de pequenos detalhes), RealVisXL, dpmpp_2m/karras, 28–30 steps, fonte a ~1536px (8GB).
- Graphs API: `C:\comfy_dl\workflow_A_api.json` (depth) e `workflow_A2_depth_lineart.json`
  (depth+canny). Guia completo: `Nanobana/controlnet/GUIA-ControlNet.md`.

## Relighting

- **"SÓ a luz, conteúdo 100%" → PÓS-PRODUÇÃO, não IC-Light.**
  `scripts/relight.py` (Pillow, não-generativo): exposição/contraste/temperatura + GLOW
  direcional (janela/candeeiro, cor+posição) + dodge (aclarar zona) + burn (matar halo/hotspot).
  Conteúdo matematicamente intocado. Limite honesto: ajusta o look da luz, não projeta sombras
  novas (isso faz-se no modelo).
- **IC-Light (generativo) — INSTALADO (2026-06-23):** ComfyUI-IC-Light (kijai) +
  `iclight_sd15_fc.safetensors` (models/unet) + checkpoint SD1.5 `RealisticVision_V6_B1`
  (IC-Light é SD1.5, não SDXL). Re-renderiza e MUDA conteúdo (cadeiras/materiais derivam) —
  rejeitado pelo utilizador para interiores completos; reservar para quando mudança de conteúdo
  é aceitável. Nodes: LoadAndApplyICLightUnet, ICLightConditioning, LightSource, DetailTransfer.
  cfg ~2, denoise 1.0, ~1024×576 → relight, depois upscale. Graph:
  `Nanobana/controlnet/workflow_D_iclight.json`.

## Texto→máscara + inpaint por objeto — INSTALADO E VALIDADO (2026-06-25)

- `comfyui_segment_anything` (storyicon). **Dois patches** em
  `local_groundingdino\models\GroundingDINO\bertwarper.py` para o `transformers` novo:
  (1) linha ~25 `get_head_mask` fallback getattr
  (`lambda head_mask,num_hidden_layers,is_attention_chunked=False:[None]*num_hidden_layers`);
  (2) linha ~109 remover o arg posicional `device` em
  `get_extended_attention_mask(attention_mask, input_shape)`.
- Modelos auto-descarregados: SAM ViT-B (375MB) + GroundingDINO_SwinT_OGC (694MB) + bert-base.
- Graph: LoadImage → SAMModelLoader + GroundingDinoModelLoader →
  GroundingDinoSAMSegment(prompt="<objeto>", threshold≈0.3) → mask (index 1).
- **Receita crop-stitch (VRAM-safe, arquitetura-safe):** máscara SÓ do alvo → crop com padding →
  upscale 2× → inpaint → downscale → `Image.composite(generated, original_region, blurred_mask)` →
  paste no original full-res. Tudo fora da máscara fica byte-idêntico.
  Graph: região + máscara → ImageToMask(red) → VAEEncode → **SetLatentNoiseMask**
  (NÃO VAEEncodeForInpaint — apaga píxeis e força denoise alto) → KSampler (dpmpp_2m/karras,
  28–30 steps, cfg 6) → VAEDecode.
- **Denoise por tipo de edição:** recolor (puxadores latão→preto) ~0.55; mudança de material
  (almofada bege→carvalho) ~0.70–0.72; cor+luminosidade (cortinas verde→branco sheer) ~0.55.
- Scripts: `C:\comfy_dl\run_inpaint.py` (runner genérico) e `sam_mask.py` (texto→máscara).
- **Gotchas de máscara:** o SAM agarra o objeto INTEIRO ("seat tops" devolveu o banco todo;
  "curtains" agarrou a parede da TV) — refinar por connected-components (manter banda superior
  sólida; descartar componentes por centróide x). Objetos finos de baixa saturação (puxadores
  latão): SAM E color-key falham → detetar por grooves escuros. Grow via `MaxFilter(2k+1)` +
  `GaussianBlur`. **Caminho acentuado:** correr de `C:\comfy_dl` (ASCII), imagens em
  `ComfyUI\input\`; só o stdin do PowerShell parte com "José".

## Luz preferida (utilizador, 2026-06-23)

Luz natural clara, suave e UNIFORME — arejada, exposição warm-neutral equilibrada, sombras
suaves, downlights recessed subtis; NÃO moody/noturna/quente-escura. O ControlNet NÃO trava a
luz (só geometria/edges) — a linha de "bright daylight" vai no prompt, denoise ~0.5, e fixa-se
a seed de um bom resultado para o reproduzir. Para PESSOAS realistas: biblioteca de pessoas do
Enscape + re-render, ou inpaint mascarado; pessoas geradas por IA parecem "fake".
