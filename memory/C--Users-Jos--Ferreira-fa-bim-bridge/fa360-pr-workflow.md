---
name: fa360-pr-workflow
description: "Como o utilizador quer que eu entregue alterações na FA-360 (branch, diff, validação, PR)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5ee310dd-5ac7-4c66-9935-fd9101a51a72
---

Fluxo de entrega que o utilizador segue consistentemente na FA-360 (repo Jmrferreirarq/fa360):
1. Uma branch nova por feature, a partir de `origin/main` (após sync).
2. Implementar e **mostrar o `git diff` antes de fechar** — ele revê.
3. Ele **valida em `npm run dev`** (frontend `vite dev`; quando há backend, também `tsx dev` do api-server).
4. Só faço **commit + push + PR depois de ele dar luz verde explícita** ("avança"/"fecha"). 1 PR por feature (backend+frontend juntos quando aplicável).
5. **Nunca faço merge** — ele revê (CodeRabbit Free, só sumário) e faz o merge. Railway/Vercel fazem deploy automático no merge.
6. Depois do merge, sincronizo o `main` local (`git checkout main && git merge --ff-only origin/main`).

**Why:** ele quer controlo e validação em dev antes de qualquer coisa ir para produção.
**How to apply:** não commitar/abrir PR sem pedido; apresentar sempre o diff e um roteiro de teste em dev. Ver [[fa360-pr-creation-method]].
