---
name: Projeto Barracao LIC Branco - Estado do trabalho
description: Projeto Archicad 2022.06.07_Barracao_LIC_Branco.emcurso - limpeza e reorganizacao de atributos para RJUE portugues (sessao 2026-04-22)
type: project
originSessionId: 2ebd81aa-31b3-4ace-9d69-28e52627199a
---
Projeto Archicad: `C:\Users\José Ferreira\OneDrive\Desktop\2022.06.07_Barracao_LIC_Branco.emcurso . 08.04.2026.pln` (porta 19723). Template de referencia: FA_Template_RJUE_v1 (porta 19724).

**Why:** Limpeza e reorganizacao de atributos para conformidade com pratica RJUE portuguesa - nomes PT, folders reais, sem duplicados.

**How to apply:** Consultar antes de retomar trabalho no projeto para nao repetir passos.

## Estado atual (2026-04-22 fim de sessao)

### Camadas — ✅ CONCLUIDO
- 94 camadas em **20 Attribute Folders reais** (criados via `CreateAttributeFolders` + `MoveAttributesAndFolders`)
- Nomes curtos, sem acentos, sem prefixo `@ 2D_` ou `@ 3D_` (o folder serve para isso)
- Folder root `Archicad Layer` (sistema) fora dos 20 folders
- 20 folders: 00 Anotacoes, 01 Cotas, 02 Documentacao, 03 Plantas, 04 CNI 2D, 10-17 3D *, 20 Edificacao Fases, 21 Arranjos Exteriores, 22 Estacionamento, 30 Perfis Tramas, 31 Zonas e Limites, 32 Vegetacao e Terreno, 99 Sistema

### Composites — ✅ 6 total
- `@ Parede Dupla Interior | 0,15` — skin core reparada (era missing, agora `Tijolo Ceramico 11`)
- 5 do template importados junto com BMs via Attribute Manager: `@ PE - Reboco/Tijolo 11/Reboco - 14cm`, `15/18cm`, `22/25cm`, `30/33cm`, `ETICS/Bloco Termico/27cm`

### Building Materials — ✅ 32 total (FA System v1 implementado 2026-04-26)
- 28 BMs no FA System v1 (19 originais com IDs alvo + 5 criados FASE 5.C + 4 reconciliados FASE 5/6) + 4 GENERICOs do template
- Priorities ordenadas hierarquicamente 30→900: Air Space=30, Terra Natural=80, Brita=100, Estuque/Gesso=190-200, Aluminio=300, Isolamentos=330-360, Metal Zinco=380, Cermica=450, Betonilha/Madeira=480, Argamassa/Reboco/Limpeza=500, Impermeab=550, Betao Leve=600, Tijolos=620-680, Bloco Termico=680, Bloco Cimento=700, Aco Estrutural=800, Betao Aparente=900
- BMs criados via Tapir nesta semana com cutSurface vazio (bug Tapir): Terra Natural, Metal Zinco (ja antes), Betao Leve, Gesso Cartonado, Ceramica Pavimento, Betonilha, Impermeab, Aco Estrutural, Aluminio, Madeira Lamelada, Betao Limpeza — 11 a corrigir manualmente no GUI
- Composite `@ PI - Laje Macica / Enchimento / Ceramico / Teto Falso - 40cm` (GUID 35c33feb, 0,400m, 7 skins, BET-APA core) criado e funcional

### Zone Categories — ✅ 15 PT
- Importadas do template via Attribute Manager: Generico, Area Util, Volumetria, Area Logradouro, Area Impermeavel, Area Permeavel, Area Terreno, Area Construcao, Area Implantacao, Area Bruta Privativa, Area Bruta Dependente, Areas Comuns, Varandas e Terracos, Estacionamento, Arrumos
- 3 EN eliminadas: Generic, Office, Residential and Recreation
- 38 zonas do projeto todas com categoryAttributeId PT valido (maioria em `Generico`)

### Fills — 51 total, alguns pendentes
- 7 duplicados `@ ARQ - Reboco (1..4)` e `@ GEN - Solido 25pct (1..3)` eliminados manualmente
- Em uso por BMs (nao mexer): `Air Space`, `Earth`, `@ ARQ - Reboco`, `@ GEN - Solido 25pct`, `@ ISO - Isolamento`
- **Pendente (proxima sessao):** renomear ~25 fills para PT no GUI (Blue, BRICK, CROSS, DOTS, Glass, Gabiao, JARDIM, Zinco, etc.) + decidir sobre 4 suspeitos (`sandwich`, `wood-000`, `00-wood tile 3`, `AR-B816,_O`)

### Surfaces — 37 total, renames pendentes
- `M_40d6511e_600c_4a8c_b2ca_d2033e223adc (from Converted Object)` ELIMINADA via API (era lixo de conversao)
- Tentativa de rename das 23 EN→PT via API **FALHOU** (CreateSurfaces com overwrite nao renomeia, so atualiza propriedades numericas)
- **Pendente (proxima sessao):** renomear 23 surfaces no GUI (Surf-White→`@ Branco Base`, Wd-Pine→`@ Pinho`, Mtl-*→`@ Ferro/Aluminio/Aco Inox`, Stucco-Yellow→`@ Reboco Amarelo Rugoso`, Glass→`@ Vidro`, etc.)
- Manter Enscape.* sem mexer (binding de biblioteca)

### Lines — 24 total
- 4 duplicados eliminados via API: `Dashed (1)`, `Long Dashed (1)`, `Dot & Dashed (1)`, `Break (1)`
- **Efeito colateral:** eliminar estes lines criou 5 novos `Solid Line (1..5)` como placeholders (os elementos que os usavam foram convertidos para Solid Line). Se quiser voltar atras, Ctrl+Z antes de gravar (mas ja gravou)

## Limitacoes API confirmadas hoje

- **Rename via API funciona APENAS para Layers** (CreateLayers com overwriteExisting+attributeId). Para BMs/Surfaces/Fills/Lines/Composites o CreateXxx com overwrite aceita e atualiza propriedades numericas/cores mas IGNORA o name silenciosamente
- **Delete via API nao valida uso** — elementos referenciados sao convertidos para defaults (lines) ou ficam com skin missing (composites). Usar Purge Unused do GUI em vez de delete direto
- **GUID da surface `Surf-White`:** `0c113dd2-7420-44ad-971f-610c886709e8` (cutSurface default usado em 15 BMs)

## Limpeza concluida em 2026-04-22

Fills (36 @ PT), Surfaces (37 PT), Lines (19, sem placeholders), Pen Table `\x14` eliminado, 4 MEP Systems PT (Incendios, Ar Fresco, Aquecimento, Cabos), Operation Profile `Nao Climatizado`. Fills `sandwich`→`@ Painel Sandwich`, `wood-000`→`@ Madeira Base`, `00-wood tile 3` e `AR-B816,_O` eliminados.

## RJUE - Infraestrutura configurada (2026-04-22)

**Pen Tables:**
- `Amarelos e Vermelhos` (GUID 844c9923) — usar em desenhos RJUE Vermelhos e Amarelos
- `Preto e Branco` (GUID 51443e4f) — versao final licenca
- `@ Jé` (GUID f5e20c67) — pen table ativo Model View + Layout Book

**Layer Combinations:**
- `PL_Vermelhos_Amarelos` (GUID e9ad1717) — set de camadas para fases RJUE

**Graphic Override:**
- **Rules existentes:** `Existing Elements`, `Elements to be Demolished`, `New Elements` (configuradas para amarelo/vermelho)
- **Combination nova criada:** `Amarelos e Vermelhos` (usa as 3 regras acima)

**Views configuradas (6 no folder `ViewMap → Turismo de Portugal → Plantas 1.100 Amarelos e Vermelhos`):**
Todas com Layer Combination `PL_Vermelhos_Amarelos`, Pen Set `Amarelos e Vermelhos`, Graphic Override `Amarelos e Vermelhos`. Settings aplicados via API `navigator_set_view_settings`. Views:
- Cota 30,20 | Platibanda (guid f16d909d)
- Cota 28.90 | Cobertura Cotada (e1e4f553)
- Cota 25.90 | Piso 01 Cotada (7b664522)
- Cota 21.10 | Piso Rés do Chão Cotada (c7659972)
- Cota 17.60 Mezanino e Estacionamento Cotada (71c2886a)
- Cota 14.00 | Piso Salão Cotada (8d091216)

## Pendente manual GUI (nao API)

- **Renovation Filter em cada das 6 views** (API `SetViewSettings` nao expoe este campo — so GUI): tipicamente `02 Demolicao` (plantas alteracoes) ou `04 Obra Nova` (plantas proposta)
- **Validacao visual:** abrir uma view e confirmar amarelos/vermelhos aplicados corretamente
- **Renovation Status dos elementos** (se nao estiver atribuido, aparecem todos como Existing). Nao ha API built-in facil para consultar/setar — usar Archicad directamente
