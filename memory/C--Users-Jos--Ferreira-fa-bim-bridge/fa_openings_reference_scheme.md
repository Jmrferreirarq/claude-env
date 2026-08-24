---
name: fa-openings-reference-scheme
description: Esquema de referências para vãos (portas e janelas) em modelos Archicad do estúdio FA — usar em todos os projectos FA-YYYY-NNN
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9aea5006-6d91-4deb-9be3-27ad9cd9ff9a
---

Esquema de referências de vãos para projectos do estúdio FA (BIM Archicad). Aplicar à propriedade built-in `General_ElementID` via Tapir MCP (`properties_set_property_values_of_elements`).

**Categorias e prefixos:**
- `PE-NNN` — Portas exteriores (entradas, batente para o exterior)
- `PI-NNN` — Portas interiores de batente
- `PC-NNN` — Portas de correr (inclui pocket doors **e** correr exteriores)
- `PS-NNN` — Portas especiais (garagem, técnicas, blindadas, etc.)
- `JE-NNN` — Janelas (peitoril ≥ ~0,90 m) e janelas altas até ao pavimento mas com largura < 0,70 m (sem passagem humana)
- `PJ-NNN` — Porta-janelas (peitoril ≤ ~0,10 m **e** largura ≥ 0,70 m)

**Regras de atribuição:**
1. Regra geral: **mesma combinação (LibPart + Largura + Altura + Peitoril) = mesma referência** partilhada por todos os elementos.
2. Excepção pocket doors: numerar **individualmente** (PC-002, PC-003…) mesmo quando todas têm a mesma dimensão — facilita marcação na planta e mapas de vãos.
3. Numeração sequencial dentro de cada categoria, **ordenada por largura crescente** (excepto PC que segue ordem de leitura do projecto).
4. Vãos com geometria anómala (peitoril negativo, sobreposições, libPart inconsistente com dimensões) ficam **PENDENTES** — manter ref antiga intacta até o autor corrigir o modelo; nunca aplicar referência nova "para tapar".

**Heurística JE vs PJ (quando o libPart é "Window" mas o peitoril é 0):**
- Largura < 0,70 m → **JE** (janela alta, sem passagem)
- Largura ≥ 0,70 m + peitoril ≤ 0,10 m → **PJ**

**Workflow recomendado:**
1. `elements_get_elements_by_type` (Door, Window) → recolher GUIDs
2. `elements_get_details_of_elements` → `libPart.name` (tipologia)
3. `properties_get_property_values_of_elements` com `WindowDoor_WHSize` (`c0ca0fc8-…` neste projecto — re-resolver por nome em projectos novos) e `WindowDoor_SillHeightFromAnchor` → dimensões + peitoril
4. Apresentar tabela ao utilizador, **aguardar confirmação**
5. Batch `properties_set_property_values_of_elements` com a property `General_ElementID`

**Why:** As bibliotecas standard do Archicad usam IDs auto-incrementais (DOO-NNN, WD-NNN) que não distinguem tipologia nem agrupam por dimensão — gera o problema típico de uma só ref partilhada por elementos com geometrias completamente diferentes. Este esquema dá rastreabilidade para mapas de vãos e medições.

**How to apply:** Sempre que pedirem "corrigir referências de vãos", "renumerar portas/janelas" ou "limpar IDs" num projecto FA. Mostrar sempre a proposta antes de escrever no modelo (regra geral do utilizador). Referência aplicada com sucesso em [[fa-2025-001-david-rodrigues]] (2026-05-25, 27 vãos).
