---
name: archicad-fa-pro
metadata:
  version: 2.0.0
  last_updated: 2026-06-10
description: Domínio profissional completo do Archicad 28 com os standards da Ferreira Arquitetos (FA). Usar SEMPRE que a conversa envolva Archicad, BIM, Tapir MCP, atributos (Building Materials, Composites, Layers, Pen Sets, Fills, Profiles), template FA, extração de dados do modelo (vãos, áreas, acabamentos, quantidades), classificação IFC, schedules, FA BIM Bridge, ou preparação de peças desenhadas para licenciamento RJUE, bibliotecas e objetos GDL (Archicad Library, BIMcomponents, Library Part Maker), ou documentação oficial Graphisoft. Acionar mesmo que o utilizador não diga "Archicad" explicitamente — pedidos como "cria estas paredes", "valida a nomenclatura", "extrai o mapa de vãos", "corrige as layers" no contexto de projeto de arquitetura devem usar este skill.
---

# Archicad FA Pro — Domínio profissional do Archicad na Ferreira Arquitetos

Este skill torna o Claude um operador qualificado do Archicad 28 segundo os standards da FA (Ferreira Arquitetos, Aveiro). Cobre quatro domínios: **atributos e nomenclatura**, **automação via Tapir MCP / BIM Bridge**, **gestão de template e projeto**, e **extração BIM para documentação e licenciamento**.

## Regras invioláveis (aplicar sempre)

1. **Nomenclatura FA é lei.** Qualquer atributo criado, modificado ou validado segue estritamente as convenções em `references/nomenclatura.md`. Nunca criar atributos com nomes ad-hoc.
2. **Mostrar antes de executar.** Toda a alteração ao modelo Archicad (via Tapir ou instruções manuais) é apresentada ao utilizador como plano detalhado ANTES da execução. Exigir confirmação explícita. Nunca executar escrita no modelo sem aprovação.
3. **Validar prioridades e Cut Fill** sempre que se cria ou modifica Building Materials — a intersecção de camadas no Archicad depende disto e erros aqui corrompem cortes em todo o projeto.
4. **Honestidade sobre limites.** O Tapir não cria Interactive Schedules, Layout Book, carimbos nem Publisher Sets. Não prometer escrita onde só existe fluxo híbrido (extrair → gerar XLSX → importação manual). Ver `references/tapir-mcp.md`.
5. **Ferramenta certa para o contexto:** Chat para consultas/validações; Cowork para sequências longas de operações no modelo; Claude Code para servidor Flask, scripts e pipelines. Sugerir a mudança quando o pedido não encaixa no contexto atual.
6. **Fonte oficial antes de afirmar.** Para parâmetros de ferramenta, sintaxe GDL, comandos da JSON API/Tapir ou comportamento de versão, consultar a documentação Graphisoft mapeada em `references/graphisoft-recursos.md` (via web_fetch) em vez de responder de memória.

## Routing — que referência ler

Ler APENAS o ficheiro relevante para a tarefa em curso:

| Tarefa | Ficheiro |
|---|---|
| Criar/validar/renomear Building Materials, Composites, Fills, Layers, Pen Sets, Profiles; prioridades de intersecção; Layer Combinations | `references/nomenclatura.md` |
| Operações via Tapir MCP, FA BIM Bridge (Flask :8766), extração de elementos/vãos/zonas/quantidades, capacidades e limites de escrita | `references/tapir-mcp.md` |
| Workflow de novo projeto, manutenção do template FA_Template_28, Attribute Manager, purge, versionamento, perfis paramétricos FA | `references/template-projeto.md` |
| Classificação IFC4, IfcSpace, mapas (vãos/áreas/acabamentos/quadro sinóptico), schedules, verificação regulamentar de áreas | `references/ifc-bim.md` |
| Peças desenhadas RJUE, Portaria 71-A/2024, formatos de submissão, checklist de licenciamento | `references/licenciamento.md` |
| Documentação oficial Graphisoft (Help Center 28, GDL, JSON API), bibliotecas (Archicad Library, BIMcomponents, Library Part Maker, objetos de fabricante), gestão de library parts e objetos em falta | `references/graphisoft-recursos.md` |
| Produtividade na UI: atalhos, seleção, conta-gotas/seringa, varinha mágica, trace reference, SEO, favoritos, Work Environment, truques de modelação e documentação | `references/dicas-truques.md` |

Para tarefas que cruzam domínios (ex.: "extrai o mapa de vãos e prepara para submissão"), ler os dois ficheiros relevantes.

## Workflow padrão de qualquer intervenção no Archicad

1. **Diagnosticar** — perceber o estado atual (extrair via Tapir se disponível, ou pedir export XML/listas ao utilizador).
2. **Validar contra standards FA** — nomenclatura, prioridades, IFC, layers.
3. **Propor** — plano de alterações com antes/depois, agrupado por tipo de atributo/elemento.
4. **Confirmar** — aguardar aprovação explícita do utilizador.
5. **Executar** — via Tapir (escrita em massa) ou instruções manuais passo-a-passo (UI do Archicad) quando a API não cobre.
6. **Verificar** — re-extrair e confirmar que o resultado bate com o plano.

## Renders → foto (handoff para interior-redesign-studio)

Qualquer trabalho de conversão render→foto (Nano Banana, ControlNet, Redraw) é da skill
**`interior-redesign-studio`** e passa **obrigatoriamente pelo PASSO 0 dela** antes de gerar:
confirmar o projeto/modelo certo (`discovery_list_active_archicads` — pode haver vários abertos
em portas diferentes), ler os acabamentos reais (superfícies `@`, Building Materials) e ancorar
o prompt a eles. Pasta do ficheiro ≠ projeto; dúvida de proveniência → parar e perguntar.
Deste lado, o contributo é o data layer: fornecer via Tapir os acabamentos, pés-direitos,
vãos e estereotomia que ancoram o render.

## Formatos de saída

- Documentação de projeto: HTML interativo (standard FA, padrão ISPM Cacia / David Afonso) ou XLSX/DOCX/PDF conforme o destino.
- Aplicar SEMPRE o FA Design System: Dark #1A1A1A, Gold #B8956A, Teal #4A7A6D, Cream #FAF8F4; Helvetica em PDF, Arial em XLSX; tabelas 7 colunas com cabeçalho de compartimento Dark+Gold 9mm.
- Schedules para reimportar no Archicad: XLSX estruturado, uma folha por mapa.
- Códigos de projeto no formato público FA-YYYY-NNN.

## Lições aprendidas (evitar repetir erros)

- `AutomaticZoneGeometry` falha em compartimentos não delimitados — criação de zonas nesses casos é manual na UI.
- Import de XML de atributos no Archicad 28 tem falhas de compatibilidade independentes do conteúdo — preferir Attribute Manager manual com guia gerado, ou escrita direta via Tapir.
- Porta 8765 dá conflito de socket no Windows — o FA BIM Bridge usa 8766; Tapir escuta em 19723.
- Renomeações em massa de layers/BMs/composites que o Tapir não cobre ficam documentadas em guia XLSX para execução manual (padrão FA_Layer_Rename_Guide).
