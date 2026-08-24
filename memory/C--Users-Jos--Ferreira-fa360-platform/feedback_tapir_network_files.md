---
name: tapir-ficheiros-sincronizados-smb-onedrive-crasham-o-archicad
description: "Nao correr operacoes Tapir/MCP sobre `.pln` em pastas sincronizadas (SMB share OU OneDrive) — copiar para pasta local pura primeiro"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 07fd2fca-0dd6-47e8-b317-006d06e2714f
---

Quando um `.pln` esta em **qualquer pasta sincronizada** — servidor SMB `\\192.168.1.10\empresa\...` da Ferreira Arquitetos, OU pasta OneDrive (incluindo `OneDrive\Desktop`) — **nunca correr operacoes em lote via Tapir/MCP**. O risco e o mesmo: o sync bloqueia o ficheiro a meio de uma escrita, o Archicad fica num estado inconsistente, e crasha.

**Why — dois incidentes confirmam:**

1. **SMB (2026-05-08):** durante limpeza de `26.03.29_Luzzo_EPR.pln` no servidor, `navigator_delete_navigator_items` (4 subsets, 10 layouts, 42 drawings) sobre SMB falhou com `WinError 64 - O nome de rede especificado ja nao esta disponivel` e crashou o Archicad. 13 layers separadoras apagados antes evaporaram (sem Save).

2. **OneDrive\Desktop (2026-05-19/20):** `.pln` de 280 MB (`26.05.19_SusanaSantos_AltemEspecialidades.pln`) em `C:\Users\José Ferreira\OneDrive\Desktop\` sofreu cascata de **6 crashes** em 24h. Primeiro foi bug de encoding (UTF-8 vs CP1252 no stdout), mas depois o autosave-recovery trouxe o modelo corrompido de volta — `OA::GetOwnerObject`, `GeneralElem::GetProject` em referencias orfas. A correr scripts Tapir num `.pln` que o OneDrive estava a sincronizar em paralelo, qualquer comando que modifique o ObjectDatabase crasha. Recuperacao final: `.pla` round-trip via GUI nativo (`Save As .pla` → reabrir → `Save As .pln`).

**How to apply:**

- **Antes de qualquer Tapir num `.pln`, perguntar onde esta o ficheiro.** Se for `\\...\` ou `OneDrive\...`, pedir ao user para mover/copiar para pasta local pura **fora do OneDrive** — `C:\Users\José Ferreira\Documents\<subpasta>\` (NAO o Desktop, que e OneDrive-sincronizado neste sistema). Trabalhar local, copiar/mover de volta no fim.
- Se o user nao puder mover, **pausar o OneDrive sync** (ou Save Online → Always keep on this device → Free up space + pause) antes de correr qualquer comando Tapir de escrita.
- Para purgas reais (Purge Unused de Layers/Surfaces/Composites/Profiles/Materials, eliminar Layout subsets, Library Manager → Consolidate, Save As `.pla` → reabrir → `.pln`) **recomendar sempre o GUI nativo do Archicad**, nao a API. O GUI conhece referencias internas que a API nao ve (Layer Combinations, MVOs, Schedules, Hotlinks).
- Operacoes Tapir seguras em rede/OneDrive: `discovery_list_active_archicads`, `project_get_*`, `elements_get_*`, `attributes_get_*`, `navigator_get_*` — leitura e OK. Escrita so em ficheiros locais nao-sincronizados.
- Apos crash com `.pln` aberto via Tapir, **NUNCA reabrir do AutoSave e continuar a correr scripts** — o modelo recuperado tem referencias orfas e crasha em cascata. Fazer `.pla` round-trip primeiro para reconstruir a base de dados de elementos.
- Lembrar o user de `Ctrl+S` apos cada operacao Tapir bem-sucedida — alteracoes via API ficam so em memoria ate gravar.
