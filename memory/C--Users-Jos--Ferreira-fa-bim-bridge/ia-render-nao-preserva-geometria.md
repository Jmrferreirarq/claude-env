---
name: ia-render-nao-preserva-geometria
description: "IA generativa de imagem não preserva geometria de renders BIM; usar render do modelo (Bonsai/Cycles, CineRender)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 052b665b-c336-4161-9ad5-a86961cb8e21
---

Para tornar renders clay do Archicad fotorrealistas **mantendo a geometria exata**, a IA generativa de imagem **não serve** — Replicate (SD1.5 img2img + ControlNet) e Nano Banana/Gemini **recriam a imagem inteira** e a estrutura deriva sempre (ângulo, layout, elementos construídos), por muito que se aperte o strength ou o prompt.

**Why:** estes modelos são generativos, não editam pixels — sintetizam uma imagem nova condicionada na original. Não existe modo "mantém tudo e só melhora materiais/luz".

**How to apply:** quando o José quer fidelidade total ao render/projeto → renderizar o **modelo 3D** (via [[fa-render-pro]] IFC→Bonsai→Cycles, ou CineRender/Enscape no Archicad), onde a geometria É o modelo. IA fica só para concepts/mood/staging em vistas "soft" (quartos), nunca para vistas estruturais (cozinhas, escadas, embutidos). Confirmar SEMPRE qual dos dois objetivos ele quer antes de avançar: (A) imagem exata fotorrealista, ou (B) imagem nova inspirada.
