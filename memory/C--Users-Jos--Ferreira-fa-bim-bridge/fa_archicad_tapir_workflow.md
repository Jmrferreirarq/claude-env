---
name: fa-archicad-tapir-workflow
description: "Padrão de trabalho com Archicad via Tapir MCP — descobrir tools, obter GUIDs, sempre confirmar antes de escrever"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9aea5006-6d91-4deb-9be3-27ad9cd9ff9a
---

Workflow para tarefas Archicad via Tapir MCP no estúdio FA.

**Regra de ouro:** **nunca** escrever no modelo sem mostrar primeiro a proposta ao utilizador e aguardar confirmação explícita — mesmo quando a tarefa parece trivial.

**Passos:**
1. `discovery_list_active_archicads` → obter porta da instância (varia por sessão).
2. `archicad_discover_tools` com queries semânticas em **inglês** (a search semântica do Tapir é EN; queries PT devolvem vazio).
3. Para propriedades built-in, usar `properties_get_property_ids` com nomes não-localizados (ex.: `General_ElementID`, `WindowDoor_WHSize`, `WindowDoor_SillHeightFromAnchor`). Cuidado: muitos nomes intuitivos não existem — usar `properties_get_all_property_names` quando há dúvida.
4. **Não** confiar em `elements_get_gdl_parameters_of_elements` — schema do MCP server tem bug de validação (campos `dimension1`/`dimension2` em falta) que faz a chamada falhar em pisos completos. Para dimensões de vãos, usar `WindowDoor_WHSize` em vez disso.
5. `elements_get_details_of_elements` devolve `libPart.name` mas **não** devolve largura/altura — confirmar via property values.
6. Escritas em batch com `properties_set_property_values_of_elements` (uma só chamada para N elementos) — não fazer loop.
7. **Verificar sempre** o resultado lendo de volta com `properties_get_property_values_of_elements`.

**Why:** O utilizador prefere agir com cuidado em ficheiros .pln partilhados via OneDrive — uma escrita errada num modelo BIM pode propagar-se a desenhos, mapas e medições. Confirmar é barato; reverter não.

**How to apply:** Em qualquer tarefa que envolva o servidor `ArchicadTapir` ou `tapir`, seguir este workflow. Se a tarefa for só de leitura, podes saltar a confirmação; se for de escrita (set/modify/create/delete), confirmação obrigatória.
