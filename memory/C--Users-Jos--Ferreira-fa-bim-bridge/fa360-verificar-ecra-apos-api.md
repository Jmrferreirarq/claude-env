---
name: fa360-verificar-ecra-apos-api
description: "Depois de criar/alterar uma proposta FA-360 por API, abrir a página e ler o ECRÃ — o significado dos campos não se vê no JSON"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5ee310dd-5ac7-4c66-9935-fd9101a51a72
  modified: 2026-08-20T16:14:54.763Z
---

Depois de criar ou alterar uma proposta por API, **abrir a página da proposta e ler o que o ecrã mostra**. Os totais que o cliente e o Arqt.º veem são os do ecrã, não os do JSON.

**Porquê:** a 20-08-2026, as propostas 716/717 tinham a API a devolver `value: 58500` certo e fases a somar 58.500 — e o ecrã mostrava outra coisa, duas vezes: (1) a PH em `valueCadernos` aparecia como "opcional, fora do valor base" (57.650 + 850 opcional vs 58.500 do documento); (2) fases de marcos com `discipline` atribuída criavam grupos com subtotais sem significado (ARQ 29.250 vs 34.150). **O que estava errado era o significado dos campos, não os números** — e isso só se vê no ecrã.

**Como aplicar:** após qualquer escrita de proposta/fases via `fa360_*` ou calculador, abrir `/propostas/{id}` no browser (sessão do Arqt.º) e conferir: valor base vs total, secções "opcionais" inesperadas, subtotais por grupo de fases. Semânticas a respeitar: `valueCadernos` = caderno de encargos VERDADEIRO (opcional, fora do valor base); marcos contratuais sobre o total = fases `discipline: "outro"`; faseamento por disciplina tem de fechar no valor da disciplina.

Relacionado: [[fa360-pr-workflow]].
