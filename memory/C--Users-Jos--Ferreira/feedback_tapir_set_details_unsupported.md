---
name: Tapir set_details_of_elements não suporta todos os tipos de elemento
description: elements_set_details_of_elements reporta success:true mas ignora silenciosamente mutações em tipos "Not yet supported" (p.ex. Railing)
type: feedback
originSessionId: 26598d7f-0fe9-4881-9b5f-d5d2bec10da4
---
`elements_set_details_of_elements` (Tapir MCP) devolve `success:true` mesmo quando o tipo de elemento não é suportado pela implementação. Para `Railing`, a mutação do `floorIndex` não foi aplicada — a releitura mostrou o valor antigo, e `elements_get_details_of_elements` reporta `details.error: "Not yet supported element type"` para Railing. Provavelmente afeta outros tipos listados como não suportados (Stair, CurtainWall sub-elementos, Morph, Skylight, etc.).

**Why:** 2026-04-24 — tentei mudar Home Story de uma guarda (BARANDILLA - 023, piso 25 → 15) via set_details_of_elements no projeto Barracao LIC Branco. API reportou success:true duas vezes seguidas, mas floorIndex manteve-se em 25. Mesmo padrão já registado para attributes_delete_attributes.

**How to apply:** Antes de usar set_details_of_elements, verificar se `get_details_of_elements` retorna `details.error: "Not yet supported"` para o tipo — se sim, a mutação vai falhar silenciosamente. Nestes casos, remeter o utilizador para a GUI do Archicad (Selection Settings) em vez de insistir na API. Confirmar sempre com releitura; nunca confiar em `success:true` isolado como prova de efeito.

**Update 2026-04-26 — confirmado também para Slab:** tentei mudar drawIndex de 1 para 999 via set_details_of_elements em SLA-002 (composite slab). API devolveu success:true mas re-leitura confirma drawIndex continua em 1.0. Slab também está afectado pelo silent no-op. Para slabs, o schema `typeSpecificDetails` só tem `WallSettings` definido — todos os outros tipos (Slab, Roof, Mesh, etc.) ignoram silenciosamente as mutações. Para mexer em Floor Plan Display / Show on Stories / Outline pen / drawIndex de Slab, **remeter sempre para GUI**.
