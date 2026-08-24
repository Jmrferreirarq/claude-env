---
name: claude-env-backup
description: Backup do ambiente Claude vive em ~/claude-env → github.com/Jmrferreirarq/claude-env (privado); atualizar com bash sync.sh + git push
metadata: 
  node_type: memory
  type: reference
  originSessionId: 77e0203a-5fa5-4dc8-b170-4cdb77f67814
  modified: 2026-08-24T03:17:21.274Z
---

O ambiente Claude Code tem backup versionado em `C:\Users\José Ferreira\claude-env` →
**github.com/Jmrferreirarq/claude-env** (privado). Cobre: skills locais, `memory/` de todos os
projetos, `settings.json` + `statusline.py`, docs de `C:\comfy_dl` (só .md/.py/.json, nunca os
PNGs) e docs do Nanobana. **Atualizar:** `bash ~/claude-env/sync.sh` (commit automático) +
`git push`. Sugerir a sincronização no fim de sessões que alterem skills/memórias/protocolos.
NÃO misturar com o repo do produto `fa360` (deploy Railway; decisão do utilizador 2026-08-24).
`settings.local.json` fica fora por design (permissões são por máquina).
