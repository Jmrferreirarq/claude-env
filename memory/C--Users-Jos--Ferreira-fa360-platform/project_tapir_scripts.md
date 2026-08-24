---
name: tapir-custom-scripts-localizacao-e-estado
description: "Onde vivem os scripts Python do Tapir do user, o que esta corrigido e o que falta encontrar"
metadata: 
  node_type: memory
  type: project
  originSessionId: 07fd2fca-0dd6-47e8-b317-006d06e2714f
---

## Pasta documentada

Segundo `README_CustomScripts.md`, o Tapir Add-On le scripts de:
`C:\Users\José Ferreira\tapir-repo\builtin-scripts\`

Tem `01_*` a `23_*` + `0_WORKFLOW_PIP.py`, `0_WORKFLOW_Licenciamento.py`, `0_Index.py`, `99_ClearHighlights.py`, e os 3 originais do Tapir (`AutomaticNumberingBasedOnPolyline.py`, `OrthoWallFinder.py`, `UnusedViewCleaner.py`).

## Scripts NAO encontrados em 2026-05-20

A Tapir Palette no Archicad mostra scripts da serie **50+/60+** (`54_TermoResponsabilidade.py`, `61_DashboardSubmissao v1`) que **nao estao em `builtin-scripts/`** e cuja localizacao no disco nao foi encontrada apos procura em Desktop, Documents, OneDrive (6 niveis), sandbox, `.tapir_mcp`, e config do Graphisoft.

O `61_DashboardSubmissao` foi o que crashou o Archicad (assertion UTF-8 no `TapirAddOn_AC28_Win.apx` por output em CP1252).

**Na proxima sessao: NAO andar a procura. Perguntar logo ao user onde estao os scripts da serie 50/60.** Sao provavelmente os mais usados em entregas reais.

## Branch com o fix de encoding

No repo `C:\Users\José Ferreira\tapir-repo\` existe a branch `fa-custom-scripts` (separada de `main` que segue o upstream do Tapir):

- `0bea59e` — baseline dos 28 scripts custom que estavam untracked
- `d5b8064` — fix `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` no `aclib/__init__.py` (cobre os 23 numerados + OrthoWallFinder + AutomaticNumbering por importarem aclib), nos 2 workflows (+ `subprocess.run(..., encoding='utf-8')`), e em `UnusedViewCleaner.py`

**Fix NUNCA validado in-app** — pediu-se ao user para correr `01_LayerInventory` apos Reload scripts mas o teste nao foi reportado. Os scripts `54`/`61` NAO estao cobertos pelo fix (vivem noutra pasta).

## Padrao do bug

Tapir Add-On capta stdout dos scripts e converte para `UniString` assumindo UTF-8. No Windows PT o default do Python e CP1252: caminhos com acentos (`C:\Users\José...`) sao bytes invalidos em UTF-8 → assert em `GSRoot\String\Unicode.cpp line 329` → processo Archicad termina. Fix: `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` no topo de cada script (ou no `aclib` partilhado).

## Output dos scripts

Convencao: cada script grava em `<pasta-do-projeto>/_TapirReports/<NomeDoScript>_<timestamp>.{csv,html}`. Encontrar essa pasta ao lado do `.pln` aberto e a forma de saber o que foi corrido recentemente.
