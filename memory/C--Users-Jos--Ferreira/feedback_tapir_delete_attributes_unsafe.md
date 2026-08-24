---
name: Tapir attributes_delete_attributes não protege atributos em uso
description: A API do Tapir apaga BMs/surfaces/etc. mesmo quando referenciados por composites e elementos; ainda reporta success:true para default BMs que não chega a apagar
type: feedback
originSessionId: 9fdb2f96-18f4-4ef7-ba50-bed5a04f9dc6
---
`mcp__ArchicadTapir__archicad_call_tool` com `attributes_delete_attributes` **não valida se o atributo está em uso**. Apaga BMs que são skins de composites custom e deixa os composites com `buildingMaterialId` em erro "Attribute is missing" — partindo todas as paredes/lajes que usem esse composite. Também observado: reporta `success:true` para BMs de sistema (ex. "Air Space" index 42) sem os apagar de facto — ou seja, o success flag não é fiável como confirmação.

**Why:** 2026-04-22 — apaguei em lote 58 BMs da primeira página acreditando que a API filtraria os em uso. Os 3 composites `@ Parede Dupla` do projeto Barracão LIC Branco ficaram com todos os skins partidos. Utilizador teve de restaurar backup.

**How to apply:** Antes de qualquer `attributes_delete_attributes` em BMs/surfaces/line types/fills, **primeiro** obter `GetCompositeAttributes` de todos os composites e `GetDetailsOfElements` de todos os elementos para compor um set de GUIDs "não-apagar". Só apagar o complemento. Para cleanup não-crítico, preferir a opção GUI do Archicad (File → Libraries and Objects → Purge Unused…) que é validada pelo próprio motor. Não confiar em `success:true` como prova — confirmar sempre relistando.
