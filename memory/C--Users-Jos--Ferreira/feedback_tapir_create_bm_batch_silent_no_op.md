---
name: Tapir create_building_materials batch pode falhar silenciosamente
description: attributes_create_building_materials em batch retorna success mas pode nao aplicar — sempre validar por re-leitura
type: feedback
originSessionId: 80da65a5-2c27-4044-8921-c714450958d9
---
`attributes_create_building_materials` com `overwriteExisting:true` em **batch grande** pode devolver `attributeIds` (success) mas **não aplicar nenhuma das alterações**. Confirmado em 2026-04-26 no projeto Barracao LIC Branco: batch de 6 BMs (priority changes) — 6 GUIDs devolvidos como success, re-leitura mostrou os 6 valores antigos. Single (1 BM) imediatamente a seguir aplicou correctamente. Batch de 5 (subset dos restantes) imediatamente a seguir também aplicou correctamente.

Não foi possível identificar causa exacta (sem modal dialog, sem erro, sem mudança de active database).

**Update 2026-04-30 (mesmo projeto Barracao):** batch de 8 BMs (criação raw, sem overwrite) **funcionou** — todos os 8 nomes/IDs/priorities/propriedades físicas (thermalConductivity/density/heatCapacity) aplicados corretamente. Batch de 8 BMs (overwrite com cutFillIndex novo) também **funcionou** — todos os 8 cutFillIds atribuídos. Sugere que o bug é intermitente, não sistemático. A regra "sempre validar por re-leitura" mantém-se obrigatória.

**Why:** Bug intermitente do Tapir/Archicad. O wrapper devolve sucesso optimista sem confirmar que as escritas foram persistidas. Provável race condition ou problema de transacção.

**How to apply:**
- **Sempre validar via re-leitura** (`get_building_material_attributes`) após qualquer batch de overwrite — não confiar só no success
- Se batch falhar silenciosamente, retentar em batches menores (4-5 BMs ou single) — costuma aplicar
- Aplicar mesma cautela a `create_composites` e `create_surfaces` (provavelmente mesmo bug)
- Logar a tentativa falhada e o retry no AUDIT_LOG
