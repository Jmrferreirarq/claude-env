---
name: Classificação de zonas Archicad para RJUE
description: Referência de qual categoria de zona atribuir a cada tipo de compartimento em projetos RJUE portugueses
type: reference
originSessionId: 657834d2-a2a6-489a-88b9-96c1f8300e03
---
Documento de consulta completo em `C:\Users\José Ferreira\OneDrive\Desktop\RJUE_Classificacao_Zonas.md`.

## Resumo — mapeamento compartimento → categoria

### Interior habitável (fração) → `Area Util`
Sala, Cozinha, Quartos, Suíte, IS, Hall privativo, Distribuição, Corredor, Lavandaria, Escritório

### Envelope total da fração → `Area Bruta Privativa` (ABP)
Usar como zona "container" ao nível do fogo (não somar com Area Util).

### Anexas não habitáveis → `Area Bruta Dependente` (ABD)
Garagem privativa em moradia, arrecadações, despensas separadas

### Comum em PH → `Areas Comuns`
Halls/escadas/corredores de edifícios multifamiliares

### Exterior coberto privativo → `Varandas e Terracos`
Varandas, terraços, alpendres

### Exterior do lote
- Pavimentos: `Area Impermeavel`
- Jardins/verdes: `Area Permeavel`
- Total lote: `Area Terreno`
- Implantação edifício: `Area Implantacao`

### Memória descritiva / estudo
- Somatório pisos: `Area Construcao`
- Volume edificado: `Volumetria`

## Regras críticas

- **Não somar Area Util + ABP** (dupla contagem)
- **Sem acentos** nos nomes (preferência)
- **Nomes únicos** por zona no projeto

## Legislação

DL 555/99 (RJUE), Portaria 216-B/2008, PDM municipal aplicável.
