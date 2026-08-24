---
name: Tapir nao tem CreateFills nem rename/delete de Fills
description: API Tapir Archicad 28 nao expoe ferramenta para criar/renomear/eliminar Fills — sempre manual GUI
type: feedback
originSessionId: 280e40f1-0c3c-48d6-8604-5e8dbcdd3264
---
A API Tapir Archicad 28 **não tem** `attributes_create_fills` (nem rename nem delete de Fills). Confirmado 2026-04-30 via discovery: existe apenas `attributes_get_fill_attributes` e `attributes_get_attributes_by_type` para leitura. Outros tipos (Surfaces, BMs, Composites, Layers, LayerCombinations, Profiles) têm `Create...` que faz overwrite, Fills não.

**Why:** Limitação da versão atual do Tapir/Archicad. Pode mudar em versões futuras.

**How to apply:**
- Quando precisar de Fills novos para um composite/atributo, **pedir ao utilizador para os criar primeiro no GUI** (Options > Element Attributes > Fill Types) com nomes específicos
- Após o utilizador criar, validar via `get_attributes_by_type` que os nomes estão exatamente como esperado (utilizador tende a deixar trailing spaces, nomes incompletos por copy-paste de tabelas markdown, ou duplicados com nome partido — todos estes erros já aconteceram)
- Indicar exemplos exatos de nomes (não usar tabelas markdown que possam ser copiadas inteiras para o input do Archicad)
- Após Fills criados, podem ser referenciados por GUID ou index em `cutFillIndex` de BMs e separators de Composites — esses funcionam normalmente
