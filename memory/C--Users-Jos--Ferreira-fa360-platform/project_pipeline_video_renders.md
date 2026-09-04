---
name: pipeline-video-renders
description: "Fluxo padrao FA para animar renders (imagem-para-video) em projetos futuros, com criterios de escolha de imagem e de ferramenta"
metadata: 
  node_type: memory
  type: project
  originSessionId: 202daeac-459b-4831-9737-1f439f13cf34
  modified: 2026-08-29T02:41:01.262Z
---

**Pipeline FA: render → video** (validado 2026-08-29 com a moradia David Rodrigues)

Quando um projeto precisar de um clip animado de um render, o fluxo é:

1. **Encontrar os renders**: `\\192.168.1.10\empresa\03_Trabalhos\<Projeto>\1 . Modelação\3 . JPEG\<data>\` (exports Enscape; as pastas por data têm as versões full-res A/B; as subpastas Facebook/Histórias/Instagram são crops sociais).
2. **Escolher a imagem** por estes critérios: camadas de profundidade (primeiro plano + edifício + fundo), vegetação e céu com nuvens (vendem o movimento), figuras humanas paradas ou sentadas (nunca a andar, é onde os modelos falham), e mar/horizonte se existir.
3. **Ferramenta primeira escolha: Gemini app (secção Vídeos), conta do José com plano Google AI Plus** — Veo/Omni, 10s 720p, custo marginal zero, upload manual ou via Chrome do José. Provou qualidade igual ou melhor que o Higgsfield free no mesmo render.
4. **Alternativa: Higgsfield MCP** (conector já ligado, conta @ferreiraarquitetos) — usar `cinematic_studio_video_v2` (5 créditos/5s sem áudio no free); Kling/Veo lá dentro exigem plano pago. Só considerar subscrição (29 USD/mês) se a produção de reels com vídeo escalar e os resultados medidos o justificarem.
5. **Prompt que funciona**: movimento único e lento (dolly-in ou drone flyover), "architecture perfectly rigid and unchanged", brisa subtil na vegetação, nuvens a derivar, "no camera shake", figuras mantêm-se como estão.
6. **QA obrigatório**: extrair frames com ffmpeg e verificar arquitetura rígida, pessoas sem deformação, luz consistente, antes de mostrar ao José.

**Regras fixas**: publicação leva rótulo IA conforme a escada da fa-imagem ([[fa-imagem]]); nada disto entra em peças de licenciamento nem substitui renders contratuais Enscape; primeiro clip candidato a publicação: o 01A da David Rodrigues (existe em versão Veo 10s e Higgsfield 5s).

Relacionado: [[higgsfield-fa]] (estado da conta e testes), [[gemini-api-nano-banana]].
