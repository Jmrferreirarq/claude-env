---
name: claude-mem-avaliado
description: Plugin claude-mem (thedotmack) avaliado em 2026-09-02 e rejeitado para o ambiente FA-360; motivos e o que ficou aproveitado
metadata: 
  node_type: memory
  type: project
  originSessionId: 41a72c4d-f492-418d-bdbd-523f11a9c8fc
  modified: 2026-09-02T17:29:24.211Z
---

O plugin claude-mem (github.com/thedotmack/claude-mem, v13.23.x) foi analisado em 2026-09-02 e a decisão foi **não instalar** no ambiente FA-360.

**Why:** o hook PostToolUse envia input e output de cada ferramenta (incluindo respostas dos tools `fa360_*` com dados reais de clientes) a um modelo observador; o instalador pré-seleciona o serviço comercial cmem.ai, telemetria PostHog ligada por omissão, consumo do plano Claude por cada chamada de ferramenta, 7 hooks bash + worker Bun/uv/Chroma frágeis no Windows, e o File Read Gate substitui leituras reais por resumos antigos (contra a regra "ler o ecrã").

**How to apply:** se o José voltar a mencionar claude-mem ou memória persistente entre sessões, não reavaliar do zero; lembrar que o padrão de pesquisa em três camadas (índice compacto → ids → detalhe íntegro) já existe no conector MCP (`fa360_list_proposals compact` + `fa360_get_proposal`). O sinal para rever seria eu repetir descobertas de sessões anteriores; a resposta seria evoluir a memória em ficheiros e o [[graphify]], nunca um worker de terceiros sobre dados de clientes.
