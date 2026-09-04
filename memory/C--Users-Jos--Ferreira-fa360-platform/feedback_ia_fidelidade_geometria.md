---
name: ia-fidelidade-geometria
description: "Correcao do Jose (2026-08-31): nao apresentar geracoes IA de vistas novas como fieis ao projeto; verificar contra o clay antes de declarar coerencia"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 202daeac-459b-4831-9737-1f439f13cf34
  modified: 2026-08-31T02:11:58.284Z
---

Em 2026-08-31, no estudo de materialidade David & Olga, apresentei gerações Nano Banana de vistas novas como "coerentes" quando tinham geometria e elementos inventados (jardim, vedações, pérgolas, carros, câmaras alteradas). O José interrompeu: "Estás a alucinar."

**Why:** num atelier de arquitetura, a geometria É o projeto. Uma imagem plausível mas inventada é pior do que uma imagem crua: desinforma o arquiteto e, se escapar, o cliente.

**How to apply:**
- Fluxo imagem-para-imagem só é fiável em duas passagens SOBRE A MESMA VISTA (materialidade → fotografia). Funciona: A1→A2.
- Vistas novas do mesmo projeto: em sessão de chat o modelo copia a composição antiga; fora de sessão inventa envolvente e elementos. Ambos falham fidelidade.
- Antes de entregar qualquer geração, comparar lado a lado com o clay de origem (vãos, muros, câmaras, elementos) e reportar drift explicitamente; nunca declarar "geometria mantida" sem essa verificação.
- Para conjuntos multi-vista fotorealistas fiéis, a via é Enscape com surfaces reais ([[fa-imagem]]); a IA fica para estudo de paleta numa vista única, N3.
