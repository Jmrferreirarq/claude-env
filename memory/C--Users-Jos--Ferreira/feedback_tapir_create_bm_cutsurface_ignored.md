---
name: Tapir CreateBuildingMaterials ignora cutSurfaceIndex
description: attributes_create_building_materials aceita cutSurfaceIndex no schema mas não aplica o valor; BM fica criado com cutSurface vazio (Attribute is missing)
type: feedback
originSessionId: 80da65a5-2c27-4044-8921-c714450958d9
---
`attributes_create_building_materials` no Tapir MCP atual **aceita** `cutSurfaceIndex` no schema mas **não aplica** o valor. O BM criado (ou atualizado via overwriteExisting) fica com `cutSurfaceId` vazio — `get_building_material_attributes` devolve `code 6100 Attribute is missing` para esse campo. Testado com idx 135 (`@ Terra`) e idx 154 (`@ Branco Base`/Surf-White), ambos ignorados em 2026-04-25 no projeto Barracao LIC Branco.

Restantes campos (`name`, `id`, `connPriority`, `cutFillIndex`, `cutFillPen`) são aplicados corretamente.

**Why:** Bug do adapter Tapir nesta build. Não há workaround via API — `set_details_of_attributes` ou similar para BMs não existe.

**How to apply:**
- Após criar/overwrite BM via Tapir, **avisar o utilizador** que precisa de definir `Cut Surface` manualmente: `Options → Element Attributes → Building Materials → [BM] → tab Cut Fill → Cut Surface dropdown`
- Não tentar workarounds com `cutSurfaceIndex` em re-overwrites — não funciona
- O BM criado **funciona em corte** (cut fill + pen aplicados); o cut surface só afeta visualização 3D da face do corte
