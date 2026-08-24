---
name: fa360-pr-creation-method
description: Como criar PRs na FA-360 quando o gh CLI não está instalado
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5ee310dd-5ac7-4c66-9935-fd9101a51a72
---

Neste ambiente Windows o **`gh` CLI não está instalado**. Para abrir PRs no repo `Jmrferreirarq/fa360`:
- Obter o token via `git credential fill` (input `protocol=https\nhost=github.com\n\n`, ler a linha `password=`).
- `POST https://api.github.com/repos/Jmrferreirarq/fa360/pulls` com `{title, head, base:"main", body}` e header `Authorization: Bearer <token>`.
- Fazê-lo num script Python à parte (escrito com a tool Write e apagado no fim) — evita problemas de escaping de backticks/`$()` quando se mete Python dentro de strings de shell.
- No Windows definir `PYTHONIOENCODING=utf-8` antes de correr, senão acentos/emojis rebentam (cp1252).
- O push normal (`git push -u origin <branch>`) funciona com as credenciais guardadas.

Ver [[fa360-pr-workflow]].
