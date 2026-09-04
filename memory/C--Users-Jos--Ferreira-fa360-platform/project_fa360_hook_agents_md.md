---
name: fa360-hook-seguranca
description: "Regras operacionais desde 2026-09-02 no fa360-platform: hook PreToolUse ativo (bloqueia por TEXTO do comando), CLAUDE.md é a única fonte de verdade e AGENTS.md regenera-se do cabeçalho; sessões paralelas partilham o checkout, trabalhar em worktree"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4eeeb2de-e305-41a4-be56-1fd430ce5308
  modified: 2026-09-02T18:03:21.314Z
---

Desde 2026-09-02 (PRs #171 e #175, fundidos pelo José):

**Hook `.claude/hooks/pre-tool-safety.mjs`** (Node, esquema oficial em `settings.json`, matcher `Bash|Write|Edit`):
- Bloqueia (`exit 2`): `DROP TABLE/DATABASE/SCHEMA`, `TRUNCATE <tabela>`, `DELETE FROM` em `billing_phases|proposals|projects|clients|suppliers`; `DATABASE_URL` em Write/Edit dentro de `artifacts/fa360`.
- Pede confirmação (`permissionDecision: ask`): `git reset --hard`, `git clean -f`, `git push --force`/`-f`, `rm -rf`.
- Inspeciona o TEXTO do comando, não a intenção: um `echo`, um `git commit -m` ou um caso de teste inline com essas palavras é bloqueado. Ver [[bash-heredoc-backslashes]] para a solução (texto vai para ficheiro, `git commit -F`, `node script.mjs`).
- Matriz de 16 casos existe só no scratchpad da sessão; se o hook mudar, reescrever os casos num script em ficheiro.

**AGENTS.md** (guia lido pelo Codex): é cabeçalho + cópia integral do `CLAUDE.md` abaixo da linha `=====`. Nunca editar o corpo diretamente; editar o `CLAUDE.md` e correr o comando de regeneração que está no cabeçalho do `AGENTS.md` (verificado byte a byte). O `CLAUDE.md` tem desde então a secção "Mapa do repositório".

**Agentes em `.claude/agents/`** só carregam com frontmatter YAML (`name`, `description`, `tools`); `fa360-analyst.md` está em CRLF, os outros em LF, ambos funcionam.

**Why:** o hook anterior nunca correu (formato errado) e o AGENTS.md contradizia o código (React Router, pool.query, FA-YYYY-NNN). Descobriu-se ao auditar com o plugin `claude-code-setup`, que não vale instalar.

**How to apply:** o José costuma ter outra sessão Claude a trabalhar no mesmo checkout (mudou o branch por baixo de mim duas vezes em 2026-09-02). Para qualquer branch de trabalho, usar `git worktree add .claude/worktrees/<nome> -b <branch> origin/main` em vez de `git checkout`, e remover o worktree após o merge. Nunca fazer merge; pós-merge apagar branch local e remoto e sincronizar `main` com `git fetch origin main:main`.
