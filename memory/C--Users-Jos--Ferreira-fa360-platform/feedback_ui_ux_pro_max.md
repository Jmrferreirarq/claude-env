---
name: feedback-ui-ux-pro-max
description: Plugin ui-ux-pro-max instalado (scope user) — usar só como auditor UX; o --design-system dele nunca sobrepõe os tokens FA
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 585febab-c67d-43fa-9d26-cac327b2304d
  modified: 2026-09-01T11:38:19.103Z
---

Plugin **ui-ux-pro-max** (nextlevelbuilder, v2.13.0) instalado 2026-09-01 no scope de utilizador, a pedido do José (veio de um Reel "Claude killed website designers").

**Why:** Testado em `Fornecedores.tsx` do FA-360: as pesquisas por domínio (`--domain ux`, `--domain icons`) encontraram problemas reais em minutos (contraste `text-white` sobre `bg-primary` dourado, botões só-ícone sem aria-label, ações só-hover invisíveis a teclado). Mas o gerador `--design-system` propõe paleta e fontes próprias que violam a identidade FA.

**How to apply:** Usar o skill para auditar UX página a página (acessibilidade, hover, dark mode, checklist pré-entrega). Ignorar sempre as sugestões de cor/tipografia — `DESIGN.md` + `design-system/tokens/fa-tokens.json` são a autoridade única. Convive com o `frontend-design` da Anthropic; se houver conflito de skills, desativar um com `claude plugin disable`.
