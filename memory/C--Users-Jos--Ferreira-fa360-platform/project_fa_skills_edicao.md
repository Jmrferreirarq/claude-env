---
name: fa-skills-edicao
description: Como se editam as skills FA (plugin claude.ai) e onde ficam os blocos pendentes
metadata: 
  node_type: memory
  type: project
  originSessionId: 86696413-0db9-43b4-b94e-386ea25f3748
  modified: 2026-09-01T18:53:42.002Z
---

As skills FA (`fa-design-system`, `fa-comunicacao`, etc.) vivem num plugin gerido no claude.ai (`fa-crivo-de-forma` / `anthropic-skills`). O agente NÃO consegue editá-las do disco: a pasta que aparece ao invocar a skill (`AppData\Roaming\Claude\local-agent-mode-sessions\...`) é uma materialização efémera da sessão, e a cópia em `Documents\Codex\2026-08-19\adm-skills-fa\outputs\` está desatualizada (jul/2026, a skill ativa é muito mais rica).

**Fluxo estabelecido**: escrever o bloco "pronto a colar" em `fa360-platform/design-system/MIGRACAO-SKILLS.md` e o José cola-o no editor de skills do claude.ai. Exemplo: bloco de contraste dos templates públicos, acrescentado e colado a 2026-09-01.

**A cópia do plugin congela no arranque da sessão**: uma alteração colada no editor só é visível (e verificável) numa sessão NOVA. Não vale a pena reinvocar a Skill nem reler a pasta `rpm/` da sessão corrente para confirmar uma edição feita entretanto.

Relacionado: [[fa360-propostas-regras]]
