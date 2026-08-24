---
name: Tapir create_surfaces ignora ambient/diffuse/specularReflection
description: attributes_create_surfaces aplica nome/textura/cores mas ignora silenciosamente os valores de reflection — surface fica preta no viewport interno até ajuste manual GUI
type: feedback
originSessionId: 280e40f1-0c3c-48d6-8604-5e8dbcdd3264
---
`attributes_create_surfaces` (Tapir Archicad 28) aceita os campos `ambientReflection`, `diffuseReflection`, `specularReflection` no payload mas **persiste sempre 0** em todos os três, mesmo após `overwriteExisting:true` com `attributeId` correto. Confirmado 2026-04-29 no projeto Barracao com a Surface `@ Betao Aparente`: 2 tentativas (create + overwrite) com valores 70/80/15 — ambos resultaram em 0/0/0 no read-back.

Outros campos passam OK: `name`, `materialType`, `surfaceColor`, `specularColor`, `emissionColor`, `transparency`, `shine`, `texture.name`. Os campos de textura mais avançados (`xSize`, `ySize`, `mirrorX`, `FillRectangle`) também não aparecem no read-back — incerto se aplicados.

**Why:** Bug do wrapper Tapir. A surface fica criada com identidade certa mas **completamente preta no viewport 3D interno do Archicad** porque sem reflexão não interage com luz. Em motores PBR externos (Enscape, Twinmotion) pode funcionar na mesma se a textura for albedo PBR.

**How to apply:**
- Após criar Surface via API, **avisar utilizador imediatamente** que tem de abrir Options > Element Attributes > Surfaces e meter à mão os 3 valores (ambient/diffuse/specular) e os parâmetros de textura (xSize/ySize)
- Não confiar no `overwriteExisting` para corrigir — não funciona para estes campos
- Para Enscape/PBR puro, registar que a surface "funciona" mesmo com 0/0/0 mas isso é exceção, não regra
