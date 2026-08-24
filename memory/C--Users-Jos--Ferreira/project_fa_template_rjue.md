---
name: FA_Template — Estado atual (renomeado de FA_Template_RJUE_v1)
description: Template Archicad RJUE em estado avançado; supera Teste 02 (Logic BIM) para uso PT
type: project
originSessionId: 280e40f1-0c3c-48d6-8604-5e8dbcdd3264
---
Template Archicad para prática RJUE portuguesa. Ficheiro: `FA_Template.pln` em `C:\Users\José Ferreira\OneDrive\Desktop\` (renomeado a partir de `FA_Template_RJUE_v1.pln`).

**Why:** Base para todos os projetos RJUE; tem de estar limpo e profissional antes de derivar outros projetos.

**How to apply:** Quando o utilizador retomar trabalho no template ou quiser criar novos projetos, este é o ponto de partida correto. NÃO confundir com Teste 01 (template BR) ou Teste 02 (Logic BIM PT) que estão na Desktop como referências.

## Estado atual (verificado 2026-04-28)

**Bem alinhado:**
- ✅ Geo CRS oficial PT: ETRS89 / Portugal TM06 + Datum Altimétrico de Cascais (Lisboa, alt 50m)
- ✅ ~50 Building Materials em PT-PT sem acentos (Tijolo Ceramico 11/15/22/30, Bloco Termico, Reboco Exterior ETICS, Pedra Natural, Telha, Zinco, Pintura, OSB, XPS, EPS, La de Rocha, Gesso Cartonado, Madeira Macica, etc.)
- ✅ 40 Composites no formato FA System v1 abreviado (`@ PE -`, `@ PI -`, `@ LJ -`, `@ CB -`, `@ MS -`, `@ TF -`, `@ PAV -`)
- ✅ 15 Zone Categories sem acentos, granulares para RJUE (Area Util/Implantacao/Construcao/Terreno/Bruta Privativa/Bruta Dependente/Logradouro/Permeavel/Impermeavel/Volumetria/Areas Comuns/Varandas e Terracos/Estacionamento/Arrumos)
- ✅ 91 Layers com esquema sem acentos (ARQ_/ANN_/ESP_/STR_/TOP_/URB_/AUX_/DGR_/INT_/TEMP_)
- ✅ 35 Layer Combinations organizadas por fase RJUE (EP_/ANT_/PL_Licenciamento_/PE_Execucao_/CE_)
- ✅ Project Info com placeholders [Codigo], [Numero], [Cidade], [Distrito]
- ✅ Keywords: "RJUE, Licenciamento, Habitacao"
- ✅ 5 stories: Fundações(-1), Piso 00(0), Piso 01(3), Piso 02(6), Cobertura(9)

**Pontos pendentes a corrigir:**
1. Story " Fundações" tem **espaço inicial e acento** → mudar para "Fundacoes" (manual GUI; Tapir set_stories quebrado)
2. ~~Layer Combinations com acentos~~ → corrigidas via API: PE_Execucao_Detalhes, PE_Execucao_Geral, PL_Licenciamento_Alcados
3. Project Info: dados pessoais do José Ferreira no campo CLIENT_* → movidos para CONTACT_* via API (CLIENT_* deve ser variável por projeto)
4. BM `│ GENERICO - ESTRUTURAL` (com pipe especial) → renomear via GUI (BM rename via API silenciosamente ignorado)
5. Composite `│ Membrana Impermeabilizante` → o nome é de BM não composite; verificar
6. Modelação vazia (0 walls/slabs/etc) — normal num template

**Comparação:**
- Versus Teste 02 (Logic BIM PT): FA_Template é superior para RJUE (CRS oficial PT, Zone Categories sem acentos e granulares, composites @ FA System v1)
- Versus Teste 01 (Bimarq BR): incompatível com workflow RJUE PT (terminologia BR, parâmetros urbanísticos BR)
