---
name: Tapir navigator items do Project Map são read-only
description: navigator_rename_navigator_item retorna erro 7403 em Sections/Elevations/etc. do Project Map; só funciona em itens do View Map
type: feedback
originSessionId: 80da65a5-2c27-4044-8921-c714450958d9
---
`navigator_rename_navigator_item` retorna **código 7403 "Navigator item cannot be modified"** quando aplicado a itens do **Project Map** (Sections, Elevations, Interior Elevations, Worksheets, Details, 3D Documents, Schedules — markers fonte). Confirmado em 4/4 tentativas no projeto Barracao LIC Branco em 2026-04-25.

**Why:** Os itens do Project Map são a source of truth do modelo Archicad — o Archicad protege-os contra mutação via API. A API só aceita renames em itens do **View Map** (clones criados pelo utilizador no painel View Map).

**How to apply:**
- Para renomear Sections/Elevations/etc. **fonte**, instruir manualmente: Project Map → right-click → Rename Section… (ou F2)
- Para renomear Views (clones), o `navigator_rename_navigator_item` funciona normalmente
- Antes de propor batch renames de cortes/alçados, avisar o utilizador que terá de fazer manualmente
- Aplicável também: provável bloqueio análogo em `clone_project_map_item` para certos tipos
