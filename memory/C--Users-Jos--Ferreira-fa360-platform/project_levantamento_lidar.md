---
name: project-levantamento-lidar
description: "FA a avaliar levantamento do existente por nuvem de pontos (2026-09-02); Cartographer descartado, teste de campo com SiteScape no iPhone Pro pendente"
metadata: 
  node_type: memory
  type: project
  originSessionId: 64fad330-4eab-4247-9600-f1921afaf0cd
  modified: 2026-09-02T17:34:21.723Z
---

Em 2026-09-02 o José pediu análise do Cartographer (SLAM da Google, abandonado desde jan/2024) e alternativas. Conclusão: SLAM open source não serve à FA; o que interessa é nuvem de pontos do existente para Archicad.

Patamares definidos:
- 0: iPhone Pro + app SiteScape (FARO, gratuita; exportação E57 incluída no plano Free; Pro a 49,99 USD/mês só para cloud). Precisão ~2,5 cm. Limite 12 M pontos por scan, portanto uma ou duas divisões por captura.
- 1: XGRIDS Lixel Kity K1 (~1,2 cm, abaixo de 10 mil euros).
- 2: aluguer BLK2GO/FARO Orbis via Grupo Acre, ou topógrafo com BLK360.

Estado: o José decidiu avançar com o teste do patamar 0. Resultado do teste de campo ainda desconhecido.

**Why:** reabilitações com plantas antigas erradas; evitar compra de scanner sem validar necessidade.

**How to apply:** se o José voltar ao tema, perguntar como correu o teste com a SiteScape antes de recomendar compra. Nuvem entra no Archicad 28 via File > Interoperability > Import Point Cloud; limpar no CloudCompare se > 2 GB. Não prometer scan-to-BIM automático. Ver [[user-architect]] e [[reference-ferreira-arquitetos]].
