# Kit ControlNet (depth-lock) — ComfyUI + SDXL
**Objetivo:** fotorrealismo/realce **sem alucinação** — a geometria fica trancada pelo mapa de
profundidade/linhas; só mudam materiais/luz. + humanização por inpaint (só onde quiseres).
Máquina: **RTX 3070 8 GB** (viável; usar offload). Custo: software grátis; €0/imagem.

---

## 1. Instalar o ComfyUI
1. Vai a **github.com/comfyanonymous/ComfyUI** → secção *"Installing"* → **Windows Portable** (ficheiro `.7z`, versão NVIDIA).
2. Extrai (ex.: `C:\ComfyUI`). Corre **`run_nvidia_gpu.bat`**. Abre no browser (127.0.0.1:8188).
3. **ComfyUI Manager** (essencial para instalar nós/modelos): github.com/ltdrdata/ComfyUI-Manager — segue o "Installation" (clonar para `ComfyUI/custom_nodes/`). Reinicia o ComfyUI. Passa a ver o botão **Manager**.

## 2. Nós e modelos (instalar pelo Manager — evita links errados)
No **Manager → Install Custom Nodes**:
- **comfyui_controlnet_aux** (pré-processadores: Depth Anything V2, MLSD, LineArt).
No **Manager → Install Models** (procura e instala):
- **Checkpoint SDXL fotorrealista:** *RealVisXL V5.0* (ou *Juggernaut XL*) → `models/checkpoints/`.
- **ControlNet SDXL Union** (*xinsir / controlnet-union-sdxl-1.0*) — um só modelo faz **depth + canny + mlsd** (ideal para 8 GB) → `models/controlnet/`.
- (opcional) **SDXL VAE** → `models/vae/`.
> Em 8 GB: se faltar memória, arranca com `run_nvidia_gpu.bat` editado para `--lowvram` (ou `--medvram`).

## 3. Workflow A — "Realce com estrutura trancada" (img2img + ControlNet)
Monta este grafo (arrasta os nós; o Manager instala em falta ao carregar):
1. **Load Image** → o teu render (Enscape/Archicad).
2. **Load Checkpoint** → RealVisXL.
3. **Depth Anything V2 (Preprocessor)** ← Load Image → **Apply ControlNet** (modelo Union, *type=depth*), **weight ≈ 0.7**.
4. **MLSD ou LineArt (Preprocessor)** ← Load Image → **Apply ControlNet** (Union, *type=mlsd/lineart*), **weight ≈ 0.5** (encadeado a seguir ao depth).
5. **CLIP Text Encode (Positivo)** = prompt de realce · **(Negativo)** = `cartoon, cgi, plastic, 3d render, lowres, blurry, deformed, watermark, text`.
6. **VAE Encode** ← Load Image → **Latent** (isto é img2img).
7. **KSampler:** latent do passo 6; **denoise ≈ 0.45** (↓ = mais fiel, ↑ = mais transforma); steps 28; cfg 6; sampler **dpmpp_2m**, scheduler **karras**. Liga o `model`/condicionamento já com os ControlNets aplicados.
8. **VAE Decode** → **Save Image**.

**Diais de fidelidade (o segredo):**
- **denoise 0.40–0.55** + **ControlNet depth weight 0.7** → casca trancada, só refina.
- Sai a derivar? **baixa o denoise** (0.35) e **sobe o depth weight** (0.8).

## 4. Workflow B — Humanização por inpaint (sala bloqueada)
Sobre a imagem boa do Workflow A:
1. **Load Image** (resultado A) → abre o **MaskEditor** e **pinta só a zona da pessoa** (junto à ilha / no banco).
2. **VAE Encode (for Inpainting)** com a máscara.
3. **KSampler denoise ≈ 0.85** (só a área mascarada muda); prompt: `a real photographed person standing at the island, casual earth-tone clothes, natural skin texture, soft natural light`.
4. VAE Decode → Save. **Fora da máscara nada muda** → sala intacta, pessoa realista.
> Alternativa de realismo máximo de pessoas: continua a ser **pessoas do Enscape + re-render**.

## 5. Prompts-template
**Realce (Workflow A):**
`high-end photoreal interior photograph, keep architecture and materials, rich realistic materials, soft natural daylight + warm 2700-3000K lamps, magazine quality, full-frame 35mm`
(O depth-lock + denoise baixo fazem a preservação — o prompt é leve.)
**Inpaint pessoas (Workflow B):** ver passo 4.

## 6. Notas honestas
- 8 GB é **suficiente mas justo**: ~30–90 s/imagem; usa `--lowvram` se preciso. Fallback rápido: **SD1.5 + ControlNet** (mais leve, menos qualidade).
- Primeira montagem ~1–2 h + alguma afinação de denoise/weights.
- Depois disto: **renders fiéis e bonitos, sem alucinação** — o que faltava.
