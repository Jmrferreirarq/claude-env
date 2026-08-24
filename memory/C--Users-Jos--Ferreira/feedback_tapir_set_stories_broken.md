---
name: Tapir project_set_stories falha com erro 'result'
description: project_set_stories devolve erro de parsing "'result'" e não aplica alterações; mutação da estrutura de stories não é fiável via Tapir
type: feedback
originSessionId: 80da65a5-2c27-4044-8921-c714450958d9
---
`project_set_stories` no Tapir MCP atual devolve erro `Error executing tool archicad_call_tool: 'result'` mesmo com payload válido (testado com 26 stories completas, schema correto). Estado do projeto **fica inalterado** após a tentativa (confirmado por `project_get_stories` pós-falha).

**Why:** O adapter Tapir tenta extrair um campo `result` da resposta do Archicad que não existe — provavelmente bug do shape de resposta nesta build. Mesmo se o erro fosse cosmético, o projeto não muda → o comando não chega a aplicar-se.

**How to apply:**
- Não confiar em `project_set_stories` para mutar `dispOnSections`, `level` ou `name` — sempre instruir manual via `Design → Story Settings…` (Ctrl+7)
- `project_get_stories` (read-only) **funciona** corretamente
- Se o utilizador insistir em automatizar mutação de stories, alertar para a falha e pedir confirmação antes de tentar
- Aplicável ao Archicad 28 (testado em 2026-04-25, projeto Barracao LIC Branco)
