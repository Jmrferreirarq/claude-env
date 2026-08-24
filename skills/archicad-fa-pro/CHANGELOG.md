# CHANGELOG — archicad-fa-pro

Convenção: MAJOR (reestruturação/referências novas com impacto no routing) · MINOR (conteúdo novo em referências existentes) · PATCH (correções).

## [2.1.0] — 2026-07-29
- **Adicionado** a `template-projeto.md` §5: tabela de códigos de projeto FA substitui a lista corrida; registado **FA-2018-002 · Barracão · Lomboser (Vagos)**
- **Adicionado** §5.1 nomenclatura de ficheiros de modelo — data ISO `AAAA.MM.DD` obrigatória, sem acentos, sufixo PascalCase, ficheiro corrente único na raiz
- **Adicionado** §5.2 estrutura da pasta de modelação — `00 . Arquivo` / `01 . Trocas` / `02 . Recursos` / `03 . Alteracoes`
- **Adicionado** a §7 duas lições: leitura offline de hotlinks/xrefs no binário do .pln antes de renomear ou mover; origem de texturas e mobiliário em `Z:\05_Bibliotecas`, nunca no Ambiente de Trabalho
- Aplicado ao processo Barracão: 55 .pln normalizados de `MM.DD.AAAA` para o standard FA, integridade verificada byte a byte
## [2.0.0] — 2026-06-10
Release consolidada: 1 SKILL.md + 7 referências. Introduzido versionamento formal e este changelog.
- **Adicionado** `references/dicas-truques.md` — ~35 técnicas de produtividade em 7 secções (seleção, edição, visualização, modelação, documentação, work environment, segurança de ficheiro)
- **Adicionado** ao routing do SKILL.md

## [1.5.0] — 2026-06-10
- **Adicionado** a `graphisoft-recursos.md`: 7 fontes curadas do ecossistema (Graphisoft Learn, Shoegnome Open Template, MasterTemplate/Bobrow, BIMx, BCF+BIMcollab, Grasshopper Live Connection/Param-O)
- **Adicionado** ao backlog: validador automático de nomenclatura FA (scripts/ via Tapir) e fluxo BIMx com Publisher Set FA

## [1.4.0] — 2026-06-10
- **Adicionado** a `template-projeto.md` §6: protocolo de auditoria bimarq 5.0 → FA_Template_28 com filtro de pertinência PT-BR/PT-PT (transfere-se vs não se transfere), tradução de fases EP/PL/PE → fases RJUE, e processo ABSORVER/IGNORAR/JÁ MELHOR NA FA
- Princípio registado: licença bimarq é de uso individual — só decisões FA adaptadas entram no skill, nunca conteúdo em bruto

## [1.3.0] — 2026-06-10
- **Adicionado** a `graphisoft-recursos.md` §5: fontes comunitárias (canal Lucas Bacelar com salvaguardas PT-BR vs RJUE; Graphisoft Community como fonte preferente)
- **Adicionado** §6 backlog inicial: fase de apresentação/render, favoritos por fase, detalhamento executivo e interiores

## [1.2.0] — 2026-06-10
- **Expandido** `tapir-mcp.md` §4: cadeia IA→MCP→Tapir→Archicad, servidor recomendado tapir-archicad-mcp (~137 comandos, pesquisa semântica local, multi-instância), config uvx para Claude Desktop, alternativas, troubleshooting (macOS unsigned, portas, claude.ai vs localhost)

## [1.1.0] — 2026-06-10
- **Adicionado** `references/graphisoft-recursos.md`: documentação oficial (Help Center 28, GDL Reference PDF, JSON API, wrapper Python), ecossistema de bibliotecas (Archicad Library, BIMcomponents, Library Part Maker, fabricantes), gestão de library parts
- **Adicionada** regra inviolável nº6 ao SKILL.md: fonte oficial antes de afirmar (consulta via web_fetch)

## [1.0.0] — 2026-06-10
Versão inicial: SKILL.md (regras invioláveis, routing, workflow padrão, formatos FA, lições aprendidas) + 5 referências:
- `nomenclatura.md` — norma completa de atributos FA com checklist de validação
- `tapir-mcp.md` — pipeline FA BIM Bridge, capacidades/limites Tapir, protocolo de escrita
- `template-projeto.md` — workflow de projeto, manutenção e versionamento do template, purge
- `ifc-bim.md` — IfcSpace, mapas automáticos, verificação regulamentar RGEU
- `licenciamento.md` — RJUE/Portaria 71-A/2024, peças, carimbo, checklist de submissão

---
Documento associado (fora do pacote): `FA_Template_28_v2_Blueprint.md` — especificação completa do template master.
Próxima revisão programada: após teste em trabalho real (auditoria bimarq) — alinhar com revisão trimestral do template.
