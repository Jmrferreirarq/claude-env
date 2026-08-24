# Protocolo de Qualidade Consistente — Render → Foto

Objetivo: obter SEMPRE o nível do `quality-benchmark.png`. Tratar como protocolo, não como sorte.
Documento canónico. (Versão divergente do Cowork arquivada em `PROTOCOLO-QUALIDADE_HISTORICO-cowork-com-erros.md`.)

---

## ⚠️ FACTOS DA API (ler primeiro — evita mitos já cometidos)
- **Motor / id real:** `gemini-3-pro-image` (alias "Nano Banana Pro"), endpoint `:generateContent`, 2K via `generationConfig.imageConfig` (aspectRatio + imageSize "2K").
- **NÃO existe seed numérica controlável.** Não prometer "fixar a seed". Coerência entre vistas = **prompt fixo + re-injetar a vista vencedora como imagem de referência**.
- **NÃO existe slider de força/denoise.** Na API, o "não inventar / não derivar" controla-se **só pelo prompt**. (denoise/strength existem no ControlNet — Caminho B/passo 1 — NÃO no Gemini.)
- **Chave:** env var `GEMINI_API_KEY` (HKCU\Environment). Nunca colar no chat.

---

## 🛑 PASSO 0 — Compatibilização com o Archicad (OBRIGATÓRIO, BLOQUEANTE)
**Nenhuma imagem avança sem o Passo 0.**
1. Identificar o **projeto/modelo certo** — NÃO assumir pela pasta do ficheiro (ver Proveniência). `discovery_list_active_archicads` (pode haver vários modelos abertos).
2. Ler os **acabamentos reais** do modelo: Building Materials, superfícies `@`, tons, vãos.
3. **Ancorar o prompt** a esses acabamentos reais.
4. Só **depois** gerar.
5. **Dúvida de proveniência → PARAR e perguntar.** Nunca gerar com dúvida.

---

## A regra de ouro
**Gerar 4 variações por vista e escolher a melhor.** O modelo é aleatório — uma tiragem sai
fotorrealista, outra plástica. Selecionar a vencedora é o que transforma "às vezes" em "sempre".

## Os três caminhos
| Caminho | Quando | Motor |
|---|---|---|
| **A — Nano Banana só** (PADRÃO) | maioria dos casos; com prompt strict resolve quase tudo, incluindo entorno limpo | `gemini-3-pro-image` |
| **B — ControlNet só** (denoise 0.35) | geometria milimétrica obrigatória; teto de realismo mais baixo | RealVisXL + ControlNet |
| **C — Híbrido** (exceção) | só vistas mesmo difíceis (muito céu/fundo) onde A ainda inventa | ControlNet → Gemini |

> Default = **A**. O Caminho A + **prompt strict** já deu entorno limpo sem invenções (Paula Silva v2),
> com menos passos e sem o teto de realismo do ControlNet. O C é exceção, não recomendação geral.

## 🛑 Regra das rampas / desníveis (planos inclinados)
Os modelos generativos (Caminho A) **achatam planos inclinados** (rampas, taludes, escadas exteriores,
desníveis de terreno) e **isso NÃO se corrige por prompt**.
- Vista com **rampa / talude / escada exterior / desnível → Caminho B ou C** (depth), **nunca A só**.
- **Validar SEMPRE** os planos inclinados contra o render original (é o desvio típico do Caminho A).

## Receita fixa (não improvisar)
1. **Motor:** `gemini-3-pro-image`, 2K. Sempre o mesmo.
2. **Prompt:** o fixo correspondente (interior / strict / exterior — abaixo), colado igual. Não reescrever.
3. **Origem:** render o mais mate possível (sem reflexos tipo espelho) — menos CGI à entrada = foto mais fiável à saída.
4. **Lote:** gerar 4 → escolher a melhor.
5. **Coerência entre vistas:** prompt fixo + re-injetar a vencedora como referência (NÃO há seed).
6. **Validar:** as DUAS condições (ver secção própria). Só então "validado".

---

## Prompt fixo — INTERIORES (anti-CGI)
```
Transform this 3D render into a realistic amateur real-estate photograph of the same interior.
Keep the exact same layout, geometry, perspective, furniture, colours and materials — change
nothing in the design, only make it look like a real photo shot with a DSLR, 35mm lens.
Make materials matte and believable: realistic satin wood, NOT glossy mirrors — remove strong
reflections. Real, slightly imperfect plants. Natural surface texture, subtle dust, micro-detail.
Lighting: one soft directional daylight source from the window with natural falloff and warm
bounce, realistic soft shadows — not flat even lighting. Subtle film grain, shallow depth of
field, faint atmospheric depth, slightly warm white balance.
Real estate magazine photograph, photographic and slightly imperfect, not a perfect render.
No people, no text, no watermark, no changes to the layout or objects.
```
Se ficar plástico: 2ª passagem "keep everything identical, only make materials matte and plants real."
Se ficar render: trocar luz para "warm late-afternoon, long soft shadows".

## Prompt — CENA VAZIA / render cru (modo "strict")
Usar quando o source é vazio ou pobre (corredores, entradas, arrumos, I.S. sem decoração).
O prompt de interiores, pela linha "Real, slightly imperfect plants", **inventa objetos** (planta,
cortina, interruptor) em cenas vazias — comprovado na entrada 01. Nesses casos:
```
Transform this 3D render into a realistic amateur real-estate photograph of the same interior.
Keep the exact same layout, geometry, perspective, openings, doors, walls, colours and materials —
change nothing in the design, only make it look like a real photo shot with a DSLR, 35mm lens.
CRITICAL: do NOT add any object, plant, decor, furniture, curtain, rug, artwork, switch or fixture
that is not already present in the original render. Only re-light and re-texture what already exists.
If the scene is empty, keep it empty.
Make materials matte and believable: realistic satin wood and plaster, NOT glossy mirrors — remove
strong reflections. Natural surface texture, subtle dust, micro-detail on walls, floor tiles and door.
Lighting: soft natural daylight with gentle falloff and warm bounce, realistic soft shadows — not flat
even lighting. Subtle film grain, shallow depth of field, faint atmospheric depth, slightly warm WB.
Real estate magazine photograph, photographic and slightly imperfect, not a perfect render.
No people, no text, no watermark, no new elements, no changes to the layout or objects.
```
No script: `run_nb_one.py "<src>" "<out>" "<label>" strict`

## Prompt — EXTERIOR (no-invention; validado na Paula Silva v2)
```
Convert this 3D model into a realistic exterior photograph of the same house. Keep the exact same
building geometry, roof, windows, wood-slat cladding, walls and layout — change nothing structural
and add NO new elements.
Do not invent or add anything that is not in the original: no extra buildings, no neighbouring houses,
no added trees, no extra fences or gates, no people, no cars, no garden furniture, and NO exposed
rafters, beams or structural soffit lining under the roof eaves unless they exist in the model — keep
the eave undersides as plain smooth flat soffits. Keep the boundary walls and fences exactly as in the
model. Keep the surroundings simple and empty. A plain natural sky is allowed.
Only make it photorealistic: realistic render-plaster, wood and concrete textures, natural daylight
with soft shadows, real grass, realistic materials. Photographic, slightly imperfect, not a perfect
render. No text, no watermark.
```
Anexar, quando os acabamentos reais forem conhecidos do modelo, uma cláusula curta de tons
(ex.: Paula Silva = reboco cinza médio · telha plana antracite · ripado madeira clara · metal preto).
No script: `run_nb_one.py "<src>" "<out>" "<label>" exterior`

**Sofitos / faces inferiores de beirado:** proibir caibros, vigas ou forro estrutural à vista, a menos
que existam no modelo. O gerador **inventa estrutura sob beirados salientes** (mesmo padrão das
plantas/entorno: preenche superfícies lisas com o detalhe "esperado"). Travar por **negativo +
descrição do sofito real** (no Caminho B/C vai no campo NEG; no Gemini vai na frase no-invention do
prompt). Se persistir: **máscara + recolor** da zona do sofito.

---

## CRÍTICO — `fiel` vs `variante` (source clay)
Um source **clay / sem materiais** (paredes lisas, sem acabamento definido) **não pode** dar uma
"conversão fiel" dos acabamentos: o modelo **autora** o material (microcimento, telha, etc.). Nesses
casos **só a geometria/layout/vãos são fiéis**; os acabamentos são uma **proposta assumida**.

Dois estados de saída (nunca confundir):
- **`fiel`** = foto **E** geometria **E** acabamentos do source preservados. Só quando o source já define os acabamentos.
- **`variante`** = foto + geometria fiel, mas **acabamentos autorais/alterados**. Marcar SEMPRE como alteração de projeto assumida; reconciliar com o modelo antes de aprovar.

Nunca apresentar uma `variante` como `fiel`.

## Proveniência + reconciliação BIM (lição Paula Silva)
- **A pasta de um ficheiro NÃO prova o projeto.** `Teste . Paula Silva.jpg` estava na pasta do David
  Afonso mas era a casa da Paula Silva → reconciliar com o IFC errado dá tudo errado.
- Antes de reconciliar acabamentos: confirmar a QUE projeto pertence a imagem (nome do ficheiro +
  perguntar + `discovery_list_active_archicads` — podem estar vários Archicad abertos em portas diferentes).
- Ler os acabamentos REAIS do modelo certo: `attributes_get_attributes_by_type` (Surface) → superfícies
  `@`-prefixadas do projeto → `attributes_get_surface_attributes`. As superfícies são por **textura**
  (RGB = branco 1,1,1), logo o tom vive no bitmap — **confirmar tons com o arquiteto**.

## Caminho C — Híbrido (passo a passo, EXCEÇÃO)
Para vistas difíceis onde A ainda inventa. Resolve adições porque o 2º passo já não recebe vazios.
1. **Passo 1 — ControlNet** (depth+lineart, **denoise 0.35**) sobre o render → base fiel, sem invenções.
2. **Passo 2 — Gemini** SOBRE o output do passo 1 (não o render original). **O "não inventar" controla-se
   só pelo prompt — NÃO há strength/denoise na API.** Prompt:
```
Make this image photorealistic. Keep everything exactly as it is — same geometry, layout, materials,
colours, framing and surroundings. Do NOT add, remove or move anything; do not invent new buildings,
fences, trees, people or objects. Only improve realism: natural material textures, believable light and
shadows, slight imperfection, film grain. Real photograph, not a render. No text, no watermark.
```
3. Validar (as 2 condições) antes de "validado". Mais passos = mais risco de deriva; usar só quando preciso.

## "validado" = DUAS condições (ambas)
1. Parece **foto real** (vs `quality-benchmark.png`), E
2. É **fiel ao original** — nada movido/removido/inventado (acabamentos do source, ou tons reais do modelo).
Falha uma → não é "validado" (é, no máximo, `variante`).

## Checklist por vista
- [ ] **PASSO 0** feito (projeto certo + acabamentos reais lidos + prompt ancorado); dúvida → parar
- [ ] Se há rampa/talude/escada exterior/desnível → Caminho B/C (não A só)
- [ ] Render de origem mate
- [ ] `gemini-3-pro-image`, 2K, prompt fixo certo (interior / strict / exterior)
- [ ] 4 variações geradas
- [ ] Melhor escolhida (coerência por referência, NÃO por seed)
- [ ] "validado" = 2 condições (foto real E fiel) — senão marcar `variante`
- [ ] Acabamentos reconciliados com o modelo certo (se aplicável)
- [ ] Linha atualizada no §10 do ESTRUTURA.md
