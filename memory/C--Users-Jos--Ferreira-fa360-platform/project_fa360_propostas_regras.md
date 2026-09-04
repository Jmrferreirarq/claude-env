---
name: fa360-propostas-regras-set2026
description: "Decisões do Arqt.º (01-09-2026) sobre propostas FA-360 — email pessoal, adicionais opcionais, mapeamento a parcelas, Gestão Técnica de Especialidades"
metadata: 
  node_type: memory
  type: project
  originSessionId: 22c9f040-9e5d-4bfe-8fbc-43333701584b
  modified: 2026-09-03T13:52:53.737Z
---

Decisões fixadas a 01-09-2026 a partir da leitura da proposta 718:

- **Email pessoal (jmrferreirarq@gmail.com) nunca em documentos que chegam a clientes**: rotas públicas (/p, /variantes, /portal, /loteamento), PDF de proposta e prints do /calc usam só ferreira@ferreira-arquitetos.pt. O gmail fica apenas no Cc do rascunho de email do /calc (função de arquivo). Aplicado no PR #166.
- **Antiguidade do atelier calcula-se** com `anosAtividade()` de `contacto.ts` (constituição 03-07-2019) — nunca literal.
- **Serviços adicionais do calculador são OPCIONAIS**: a página /variantes declara-os "faturáveis apenas se confirmados". Por isso NÃO se mapeiam às parcelas ao gravar — mapeiam-se **quando o cliente confirma a opção**. Mapa: `proj_exec_base`/`proj_exec` → valueExecucao; **`orcamentacao` e `caderno_encargos` → valueCadernos**; `value` mantém-se igual à soma das parcelas.
- **Linha "Gestão Técnica do Processo de Especialidades"**: 500 € por defeito (editável), fixa nas 3 variantes (não escala com −15%/+25%), soma aos totais, só propostas novas. Fase 1 aprovada: valor guardado em `proposals.pdfOverrides` (JSONB já existente) — a coluna `value_gestao` só depois do restauro de backup testado (gate de esquema ativo). Rótulos −15%/+25% mantêm-se com nota a dizer que se aplicam a arquitetura e especialidades. Não usar o nome "Coordenação de Especialidades" (já é item da lista — leria como cobrança duplicada).
- **Travessões nos templates**: a regra fa-sem-travessao aplica-se ao CÓDIGO dos templates públicos do fa360. `semTravessao.test.mjs` (ligado ao `npm test` da SPA) falha se U+2014/U+2013 voltarem aos 4 templates públicos, ao CalcHonorarios ou aos catálogos do calcEngine. Placeholders de valor vazio usam "a indicar". Commit messages também sem travessões. Pendente: proposalPdf.ts ainda tem ~30 (sessão de limpeza).
- **Contraste (passe 01-09-2026, PR #170)**: regra de fronteira do Arqt.º — cumpre 4.5:1 tudo o que seja número, condição contratual, rótulo de secção ou texto que o cliente leia para decidir; ornamento e chips decorativos ficam de fora. Não perseguir os casos menores. `contrasteHeadings.test.mjs` guarda os headings com conversão oklch e assert de sanidade da matemática.
- **Dourado profundo #755631**: token NOVO de identidade nascido no passe de contraste (texto Standard e fundos com texto branco; o #B8956A mantém-se em bordas/fundos suaves). PENDENTE: registá-lo na skill **fa-design-system** (a autoridade da identidade FA é a skill, não o código) numa sessão própria — até lá, DOCX e PDF externos saem com o dourado antigo.
- **FEITO (PR #178, 03-09-2026)**: nota e tags das percentagens da /variantes DERIVAM dos coeficientes efetivos (`pctVsBase`/`fmtPctAjuste` em variantScope.ts, com testes; `variantesTagOverride` continua a mandar). Regra permanente: percentagens nunca se escrevem no template — calcular, nunca escrever (classe "literal que mente": 9 anos, nota ESP, ICHPOP "1.º trimestre 2026" ainda por auditar).
- **useGrouping "always" (02-09-2026)**: milhares agrupam sempre (9 072,50). Registado: propostas antigas reabertas mudam de aspeto no histórico — aceite.
- **Menores /variantes (lista do Arqt.º, 03-09-2026, "para depois")**: "300 m²" do cabeçalho parte com o m² sozinho (falta NBSP); o email parte no rodapé; as fases dos 3 cartões de faseamento não alinham horizontalmente entre colunas; os 5 círculos do processo sobem em escada e o 03 é dourado enquanto os outros são verde/azul; "18+ meses" devia ler "mais de 18 meses".
- **Desenho a pensar (Arqt.º 03-09-2026, sem urgência)**: com o quadro "Projeto de Execução" uniformizado, as 3 colunas ficam idênticas quando nenhuma variante inclui o PE — honesto mas vazio; considerar colapsar para UMA linha quando as três coincidem.
- **"Caro(a)" ainda vive no rascunho de email do /calc** (CalcHonorarios ~linha 2123, gera o corpo que se cola no email ao cliente) — mesma classe do defeito corrigido na carta da /variantes (PR #177); por corrigir quando houver ordem.
- **saudacao**: campo do snapshot calc-proposals (data.saudacao); sem UI no calculador; escrever via PUT /api/calc-proposals/:token AUTENTICADO (só o GET é público).
- Relacionado: [[ferreira-arquitetos]]
