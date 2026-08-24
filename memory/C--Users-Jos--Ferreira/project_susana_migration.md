---
name: Migração projeto Susana Santos para template FA_Template_RJUE_v1
description: Estado da migração do projeto 26.02.19_SusanaSantos_AltemEspecialidades.pln (porta 19723) para atributos PT do template
type: project
originSessionId: 657834d2-a2a6-489a-88b9-96c1f8300e03
---
Projeto Archicad: `26.02.19_SusanaSantos_AltemEspecialidades.pln` (hostel).
Portas: projeto=19723, template FA_Template_RJUE_v1=19724.

**Why:** Integrar um projeto existente com a estrutura PT do template RJUE (BMs, composites, camadas, surfaces, zone categories).

**How to apply:** Ao retomar, consultar o estado abaixo e continuar pelos pendentes.

## Concluído (via API)

- ✅ **Building Materials:** 52 migrados (nomes PT do template)
- ✅ **Composites:** 40 PT criados + 24 EN eliminados; mapping de BM GUIDs template→projeto via nome
- ✅ **Layer Combinations:** migradas do template
- ✅ **Camadas:**
  - 42 camadas EN padrão Archicad eliminadas (Interior-, Structural-, MEP-, Finish-, Marker-, etc.)
  - 5 camadas residuais eliminadas (Shell-Roof, DE_PILARES, Marker-Section, Model Unit-Zone, -Hidden)
  - 319 elementos reatribuídos para camadas PT (ARQ_Escadas, ARQ_Paredes, ARQ_Mobiliario, ANN_Marcadores, ANN_Areas, ARQ_Pilares, AUX_Referencia, ARQ_Coberturas)
- ✅ **Surfaces:** 35 surfaces PT criadas (texturas referenciam biblioteca do template — precisa carregar biblioteca no projeto para verem-se)
- ✅ **Zone Categories:** 15 PT importadas via Attribute Manager; 11 EN eliminadas via API

## Pendente

### Manual (utilizador)
- **Reatribuir categoria às 47 zonas:** ficaram sem categoria após eliminação de "Generic" EN. Fazer via Archicad: Edit > Find & Select > Element Type = Zone > selecionar todas > Info Box > Zone Category = "Area Util"
- **Gravar projeto (Ctrl+S)** após reatribuição

### Opcional (podem fazer-se via API depois)
- Algumas zonas seriam mais corretamente classificadas como `Areas Comuns` (halls, distribuições) ou outras categorias — ajuste fino manual
- Composites criados mas nenhum elemento os usa — paredes/lajes/coberturas usam BMs simples. Atribuir composites aos elementos no Archicad se desejado
- Camadas PT específicas do template não têm elementos (ESP_*, STR_*, TOP_*, URB_*, DGR_*) — estrutura preparada para uso futuro
- Camadas `@` específicas do projeto mantidas (@ Hostel, @ Beirado, @ Alçado, @ Envolvente 3D, etc.)

## Limitações API conhecidas (este projeto)

- `SetDetailsOfElements` NÃO aceita `categoryAttributeId` no schema → não é possível alterar categoria de zona existente via Tapir
- `API.DeleteAttributes` direto erra com 4002 (campo `attributeType` não aceite) — usar sempre MCP tool `attributes_delete_attributes`
- `TapirCommand.DeleteAttributes` → erro 4010 (não registado nesta versão)
- `TapirCommand.CreateZoneCategories` → erro 4010 (não existe) — ZoneCategories só criáveis via Attribute Manager manual
