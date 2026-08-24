# Protocolo de Qualidade Consistente — Render → Foto

Objetivo: obter SEMPRE o nível do `quality-benchmark.png`. Tratar como protocolo, não como sorte.

## A regra de ouro
**Gerar 4 variações por vista e escolher a melhor.** O modelo é aleatório — uma tiragem sai
fotorrealista, outra plástica. Selecionar a vencedora é o que transforma "às vezes" em "sempre".

## Receita fixa (não improvisar)
1. **Motor:** Nano Banana 2.0 (Gemini 3 image), qualidade máxima. Sempre o mesmo, sem trocar.
2. **Prompt:** o anti-CGI fixo (abaixo), colado igual todas as vezes. Não reescrever.
3. **Origem:** render Enscape o mais mate possível antes de converter (mesa mate, plantas
   realistas, sem reflexos tipo espelho) — menos CGI à entrada = foto mais fiável à saída.
4. **Lote:** gerar 4 → escolher a melhor.
5. **Seed:** fixar a seed da vencedora e reutilizar nas outras vistas do mesmo projeto (look coerente).
6. **Validar:** comparar a escolhida com `quality-benchmark.png`. Só então marcar "validado".

## Prompt fixo (anti-CGI)
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

## Qual ferramenta para quê — três caminhos
- **Caminho A — Nano Banana 2.0 só:** rápido, realismo máximo, aceita micro-desvios de geometria.
  Vistas fáceis (interiores definidos, pouco "vazio" na imagem).
- **Caminho B — ControlNet só (`/render-foto`, denoise 0.35):** fidelidade máxima, realismo mais
  baixo. Quando a geometria tem de ser milimétrica.
- **Caminho C — Híbrido (ControlNet → Nano Banana):** o melhor dos dois, mais lento. Para vistas
  difíceis: exteriores com muito céu/fundo, ou quando fidelidade E realismo são ambos críticos.

## Caminho C — Híbrido (passo a passo)
Resolve as adições/alucinações porque o 2º passo já não recebe vazios para inventar.
1. **Passo 1 — ControlNet** (depth+lineart) sobre o render → base fiel, sem elementos inventados.
2. **Passo 2 — Nano Banana** SOBRE o output do Passo 1 (não o render original), força baixa
   (denoise/strength ~0.3–0.4), só para levantar realismo. Prompt:
```
Make this image photorealistic. Keep everything exactly as it is — same geometry, layout,
materials, colours, framing and surroundings. Do NOT add, remove or move anything; do not
invent new buildings, fences, trees, people or objects. Only improve realism: natural material
textures, believable light and shadows, slight imperfection, film grain. Real photograph, not
a render. No text, no watermark.
```
3. Validar contra o benchmark (realismo) E contra o render original (fidelidade) antes de "validado".
Nota: reservar para vistas difíceis — são mais passos e cada passagem pode derivar um pouco.

## Checklist por vista (rápido)
- [ ] Render de origem mate
- [ ] Nano Banana 2.0, qualidade máx, prompt fixo
- [ ] 4 variações geradas
- [ ] Melhor escolhida + seed registada
- [ ] Comparada com o benchmark → "validado"
- [ ] Linha atualizada no §10 do ESTRUTURA.md
