# ESTRUTURA DO PIPELINE — Moradia Unifamiliar (David Afonso)

> Documentação fixa do sistema de renders fotorrealistas fiéis.
> Atualizado: 2026-06-26. Fonte: estado real em disco (não de memória).

---

## 1. Ambiente / Hardware
- **SO:** Windows 11 Pro
- **GPU:** RTX 3070 **8 GB VRAM** → obriga a gerar em base reduzida (1536 px) + upscale.
- **Motor:** ComfyUI portable em `C:\ComfyUI_windows_portable`
- **API:** `http://127.0.0.1:8188` (endpoints usados: `/prompt`, `/history/<id>`, `/view`, `/system_stats`, `/upload/image`)
- **Python do motor:** `C:\ComfyUI_windows_portable\python_embeded\python.exe`
  (é o único que lê bem caminhos com acentos — usar sempre este para correr os scripts)

## 2. Modelos instalados
| Tipo | Ficheiro |
|---|---|
| Checkpoint principal | `RealVisXL_V5.0_fp16.safetensors` |
| Checkpoint alternativo | `RealisticVision_V6_B1.safetensors` |
| ControlNet | `controlnet_union_sdxl_promax.safetensors` (carregado 2×: depth + canny) |
| Upscaler | `RealESRGAN_x4plus.pth` |
| Preprocessador depth | `depth_anything_v2_vitl.pth` |

Local: `C:\ComfyUI_windows_portable\ComfyUI\models\{checkpoints,controlnet,upscale_models}`

## 3. Pastas
| Função | Caminho |
|---|---|
| Scripts | `C:\comfy_dl\` |
| Entregáveis (renders) | `C:\Users\José Ferreira\Nanobana\renders\` |
| Input ComfyUI (ASCII, p/ LoadImage) | `C:\ComfyUI_windows_portable\ComfyUI\input\` |
| Fonte original Enscape | `…\Moradia Unifamiliar — David Afonso\Imagens Interiores\` |
| Memória persistente | `C:\Users\José Ferreira\.claude\projects\C--Users-Jos--Ferreira-Nanobana\memory\` |

**Gotcha de caminhos:** paths com "José" e ".@ David Afonso" partem stdin/ls do shell.
Passar sempre os caminhos dentro de strings Python (Image.open lê bem) e copiar imagens
para a pasta input ASCII antes de usar LoadImage.

---

## 4. OS CAMINHOS (decisão de base) — detalhe em `PROTOCOLO-QUALIDADE.md`

| Caminho | Quando | Motor |
|---|---|---|
| **A — Qualidade de foto** (PADRÃO) | maioria dos casos; com prompt strict resolve quase tudo | `gemini-3-pro-image` (Nano Banana Pro) |
| **B — Distorção zero** | geometria milimétrica obrigatória | pipeline ControlNet (receita conservadora abaixo) |
| **C — Híbrido** (exceção) | vistas difíceis onde A ainda inventa | ControlNet → Gemini |

- **Caminho A** = padrão para entregáveis. Aceita **micro-desvios de geometria** por realismo de lente real. Regra de ouro: gerar **4 variações → escolher a melhor**. ⚠️ A API **não tem seed nem strength**: coerência por prompt fixo + re-injetar a vencedora como referência.
- 🛑 **PASSO 0 (bloqueante):** antes de gerar QUALQUER imagem — identificar o projeto/modelo certo (não pela pasta), ler acabamentos reais do Archicad (Building Materials, superfícies `@`, tons, vãos), ancorar o prompt a eles; dúvida de proveniência → parar e perguntar. Detalhe no PROTOCOLO.
- 🛑 **Rampas/desníveis:** o Caminho A **achata planos inclinados** (rampas, taludes, escadas exteriores) e não se corrige por prompt → usar **B ou C** (depth). Validar sempre os inclinados contra o original.
- **"validado" exige DUAS condições** (ambas): (1) parece **foto real** (vs `quality-benchmark.png`) **E** (2) é **fiel ao render original** — nada movido, removido ou inventado. Se falhar uma, não é "validado".
- **Caminho B** = quando não pode haver qualquer desvio. Mais fiel, teto de realismo mais baixo.
- Ambos os docs estão agora em `C:\comfy_dl\` (já não na pasta volátil de sessão).

> As receitas ControlNet abaixo são o detalhe técnico do **Caminho B**.

### ✅ CONSERVADORA — a que funciona (fiel + fotográfica)
```
Checkpoint : RealVisXL_V5.0_fp16
ControlNet : union promax  ->  depth + canny (dois ControlNetApplyAdvanced em cadeia)
  depth  strength 0.60   start 0.0   end 1.00
  canny  strength 0.85   start 0.0   end 0.85    (CannyEdge high 200 / low 100 / res 1024)
  depth preproc: DepthAnythingV2 (depth_anything_v2_vitl.pth, res 1024)
KSampler   : denoise 0.35 · 30 steps · cfg 6.0 · dpmpp_2m / karras
Init       : VAEEncode da LoadImage (img2img ao denoise indicado)
Upscale    : UltimateSDUpscale · denoise 0.20 · RealESRGAN_x4plus · x2.0–2.5
             tiles 1024 · mode Linear · mask_blur 8 · tile_padding 32
             seam_fix None · tiled_decode True
Base input : 1536 px de largura  (H = round(1536*srcH/srcW/8)*8)
```
**Resultado:** preserva geometria + materiais + a escada aberta de aço/vidro/espelho
sem deformar. Produziu a boa cozinha, a 08 e a social 06.

### ❌ "REALISMO" — a que DEGRADA (não usar nestes renders)
```
denoise 0.65 · canny 0.45 · depth 0.70
```
Reinterpreta a cena: muda materiais (mesa madeira→cinza), reestrutura mobília
(estante navy), escurece e parte a escada aberta. Foi a causa de toda a
inconsistência da sessão. **Só aceitável com proteção por composite (ver §6).**

---

## 5. Scripts principais (`C:\comfy_dl\`)
| Script | Seed | Função |
|---|---|---|
| `run_pipeline.py` | 70414 | receita conservadora original → boa cozinha (referência-mãe) |
| `run_06_faithful.py` | 60606 | **social 06 fiel** (depth .6/canny .85/denoise .35) |
| `run_08_faithful.py` | 70414 | sala-jantar 08 fiel + lift de sombras (gamma 0.90) |
| `run_p4_v3.py` | 70414 | cozinha realismo 0.65 + proteção de escada (composite) |
| `run_06_real.py`, `run_06.py` | — | tentativas realismo na social 06 |
| `run_08.py` | 80818 | 1ª tentativa 08 a 0.65 (falhou: mesa→cinza) |
| `run_06_clean.py`, `run_06_grade2.py` | — | upscale limpo + grade não-destrutivo |
| `prep_*`, `recolor*`, `sam_mask.py`, `run_inpaint.py`, `run_handles.py` | — | utilitários (máscaras, inpaint, puxadores, recolor) |

## 6. Técnicas de apoio

### Proteção dura de elemento frágil (escada/espelho) — composite por máscara
Só necessária em passagens de denoise alto. A 0.35 a geometria aguenta sozinha.
1. gerar o render de realismo;
2. fazer RealESRGAN-upscale do ORIGINAL limpo (não-generativo);
3. `Image.composite(original_limpo, render, mascara_feather)` sobre a zona frágil.
Garante geometria idêntica. Provado em 06 e cozinha p4v3.

### Grade não-destrutivo (PIL/numpy) — recuperar sub-exposição, sem mexer geometria
```
a = np.power(a, 0.90)              # lift de sombras
a = (a-0.5)*1.03 + 0.5            # micro-contraste
a = np.where(a>0.88, 0.88+(a-0.88)*0.7, a)   # rolloff de altas-luzes
ImageEnhance.Color 1.03 · UnsharpMask(radius=50, percent=8)  # clarity
# SEM grão, SEM sharpen pesado (estraga renders CG limpos)
```

## 7. Entregáveis-chave (`renders\`)
- **Finais fiéis (a usar):** `p06_faithful.png` (social 4K), `p08_faithful.png` (sala-jantar 4K), `cozinha_enscape_v1.png` (cozinha).
- **Provas de fidelidade:** `p06_faithful_stair_check.png`, `p06_faithful_compare.png`, `p08_faithful_stair_check.png`, `cozinha_p4v3_stair_proof.png`.
- **Originais Enscape:** `06_cozinha_p1..p5.png`, `06_final.png`, `01_entrada_*`, `07_zona_social_p1`.
- **Descartados mas guardados** (regra "nada se perde"): `cozinha_gptimage`, `cozinha_humanizada*`, `06_openai_test`, `p08_realism_nostair`, etc.

## 8. Regras fixas do projeto
- Nunca alterar composição / estrutura / acabamentos do original; só passagem fiel.
- Respeitar acabamentos existentes (ex.: torneira latão fica latão).
- Nunca renderizar sem pedido; discutir conceito primeiro.
- Não apagar trabalho — tudo fica em disco.
- Verificar escada/espelho com crop-prova **antes** de apresentar.
- API keys (GEMINI/OPENAI) lidas do registry do Windows, nunca no chat.

---

## 9. Como correr (exemplo)
```bash
PY="C:/ComfyUI_windows_portable/python_embeded/python.exe"
cd /c/comfy_dl && "$PY" run_06_faithful.py
```
Cada script: prepara a base 1536 → submete o grafo ao ComfyUI → faz poll do
`/history` → descarrega o resultado → upscale → grade subtil → grava provas.

---

## 10. Registo por vista
> Uma linha por vista. Atualizar sempre que uma vista avança.
> **Tipo:** `fiel` = geometria E acabamentos do source preservados · `variante` = alteração de projeto assumida (autoral), NÃO é conversão fiel.

| Vista | Render de origem | Receita + seed | Ficheiro final | Tipo | Estado |
|---|---|---|---|---|---|
| Cozinha | `06_cozinha_p4.png` | conservadora · 70414 | `cozinha_enscape_v1.png` | fiel | OK |
| Social | `06.png` | conservadora · 60606 | `p06_faithful.png` | fiel | OK (validado) |
| Sala-jantar | `08.png` | conservadora · 70414 | `p08_faithful.png` | fiel | OK |
| Entrada | `01 Entrada.jpg` (clay) | NB · gemini-3-pro-image · strict · #2 | `entrada01_VARIANTE_aro-preto-microcimento.png` | **variante** | ADOTADA (proposta de projeto): aro preto + microcimento autorais; geometria fiel (source clay sem acabamentos) |

### Paula Silva — PROJETO SEPARADO
> `\\192.168.1.10\empresa\3 . Trabalhos\Paula Silva` · Archicad porta **19723** (`26.06.24_PaulaSilva_EPR`). NÃO misturar com o David Afonso.

| Vista | Render de origem | Receita | Ficheiro final | Tipo | Estado |
|---|---|---|---|---|---|
| Exterior | `Teste . Paula Silva.jpg` (clay) | A · gemini-3-pro-image · exterior · **#1** | `paulasilva_exterior_VARIANTE-bim.png` | **variante** (reconciliada c/ BIM) | **OK com ressalva — NÃO validado.** Desvio: **rampa de acesso aplanada.** Tratamento tentado (B 0.45/0.62, C, Gemini c/ prompt explícito da rampa): generativo **achata sempre** o inclinado (vira pátio+degrau); ControlNet preserva a rampa mas fica aspeto de maqueta (clay sem materiais). **Sem solução foto+rampa a partir do clay.** Fix real: render texturado do Archicad/Enscape desta vista (com materiais + rampa) → depois fotorrealizar. Acabamentos: reboco cinza médio · telha plana antracite · ripado madeira clara · metal preto |
