---
name: bash-heredoc-backslashes
description: "Neste ambiente Windows/Git Bash, heredocs (mesmo com 'EOF' quoted) via tool Bash colapsam `\\\\` em `\\`; escrever ficheiros com regex/escapes pelo tool Write, e testar hooks a partir de scripts em ficheiro"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4eeeb2de-e305-41a4-be56-1fd430ce5308
  modified: 2026-09-02T17:29:09.755Z
---

Heredocs pelo tool Bash colapsaram `\\` em `\` duas vezes em 2026-09-02 (um `.replace(/\\/g, ...)` virou `/\/g` e um `` `\\b` `` num template string virou backspace). Barras simples (`\b`, `\s` em literais regex) sobreviveram.

**Why:** quebrou silenciosamente o hook `.claude/hooks/pre-tool-safety.mjs` (SyntaxError num caso, regex que nunca casava noutro). Só a matriz de testes apanhou.

**How to apply:** ficheiros com escapes, regex ou caminhos Windows escrevem-se com o tool Write ou Edit, nunca por heredoc. O hook PreToolUse do FA-360 bloqueia comandos Bash cujo TEXTO contenha `DROP TABLE`, `TRUNCATE <tabela>` ou `DELETE FROM <tabela de produção>`, portanto casos de teste e mensagens de commit com essas palavras vão para ficheiro (`git commit -F`, `node script.mjs`) em vez de inline. Ver [[fa360-hook-seguranca]].
