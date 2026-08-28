---
name: fa360-graphify
description: "Grafo de conhecimento graphify do fa360-platform — código-só (zero LLM), usar query na fase de reconhecimento, --update no arranque de auditorias"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5ee310dd-5ac7-4c66-9935-fd9101a51a72
  modified: 2026-08-25T14:21:37.147Z
---

O repo `fa360-platform` tem um grafo de conhecimento **graphify** em `graphify-out/` (gitignorado; construído 25-08-2026: 4.108 nós / 6.930 arestas, 467 ficheiros de código).

**Como aplicar:**
- Nas fases de **reconhecimento** de auditorias ("quem chama X", "que caminho liga A a B"), consultar primeiro o grafo (`graphify query "..."` no root do repo, interpretador em `graphify-out/.graphify_python`) em vez de greps + leituras de ficheiros grandes — é para poupar créditos/contexto.
- No **arranque de sessões de auditoria**, correr `/graphify . --update` (incremental, zero LLM para código).
- **Política código-só**: o repo contém ~600 PDFs + ~300 imagens (arquivo de propostas) — NUNCA os incluir na extração graphify: exigiriam extração semântica por LLM (custa créditos, contra o objetivo). Filtrar o detect para `code` apenas, como na build original.
- Arestas `INFERRED` são palpites (ex.: `saveEdit`→whoop era colisão de nomes `clientId`, falso positivo) — confirmar sempre no código antes de afirmar.
- A precisão (auditar briefings, editar, validar) continua a exigir leitura integral do código real — o grafo não substitui isso.

Relacionado: [[fa360-pr-workflow]], [[fa360-verificar-ecra-apos-api]].
