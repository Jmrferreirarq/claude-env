# Template FA e Gestão de Projeto — Archicad 28

## 1. Ficheiros de referência FA

| Ficheiro | Conteúdo |
|---|---|
| `FA_Template_28.pln` | Template principal com todos os atributos |
| `FA_Biblioteca_Perfis.pla` | Perfis paramétricos exportados (FA—A.01, B.02, I.01, J.03…) |
| `FA_Surfaces_Pack.pla` | Pack de surfaces FA |
| `FA_Composites_v1.pln` | Referência de composites com amostras |
| `FA_Layer_Rename_Guide.xlsx` | Guia de renomeações manuais pendentes |

## 2. Workflow de novo projeto

1. Abrir `FA_Template_28.pln` (File > New from Template)
2. Gravar imediatamente como `FA-YYYY-NNN_NomeProjeto.pln`
3. Verificar atributos importados (Attribute Manager)
4. Ajustar Layer Combinations ao tipo de projeto
5. Criar surfaces específicas do projeto (substituir genéricas)
6. Associar Pen Set correto à escala principal (FA-050/100/200)
7. Confirmar Renovation Filters e Graphic Overrides (ex.: demolido a amarelo visível em 3D — correção aplicada no Barracão LIC Branco)

## 3. Manutenção do template

| Ação | Frequência |
|---|---|
| Importar BMs/Composites novos desenvolvidos em projeto | Por projeto concluído |
| Purge de atributos não usados | Na entrega de projeto |
| Exportar perfis novos para biblioteca | Quando desenvolvidos |
| Verificação geral de prioridades e nomenclatura | Trimestral |
| Backup versionado (`FA_Template_28_vX.X.pln`) | Após cada atualização major |

### Versionamento
- **Patch (X.X.1)** — correções de nomenclatura, ajustes de prioridade
- **Minor (X.1.0)** — novos composites, surfaces ou perfis
- **Major (2.0.0)** — reestruturação de layers, novos pen sets, nova versão Archicad

## 4. Purge — regras

1. Attribute Manager > Delete Unused para Fills, Lines, Surfaces, BMs e Composites sem referência.
2. **Nunca purgar layers `FA-`**, mesmo vazias — são estrutura do template.
3. Profiles: purgar apenas os sem referência ativa.
4. Gravar cópia de arquivo ANTES de entregar ficheiro purgado.

## 5. Códigos de projeto FA (formato público FA-YYYY-NNN)

O ano é o de **início do processo**, não o da fase em curso. O número é sequencial dentro do ano.

| Código | Projeto |
|---|---|
| FA-2018-001 | PF Housing |
| FA-2018-002 | Barracão · Lomboser (Vagos) |
| FA-2020-001 | CVCN |
| FA-2022-001 | JL |
| FA-2022-002 | Izakaya |
| FA-2022-003 | Panedge |
| FA-2025-001 | David Afonso |
| FA-2025-002 | ISPM Cacia |
| FA-2026-001 | CDR Taveiro |
| FA-2026-002 | Paula Silva |

Ao referenciar ou criar documentação, usar sempre o código público.

### 5.1 Nomenclatura de ficheiros de modelo

```
FA-YYYY-NNN_NomeProjeto_AAAA.MM.DD[_Sufixo].pln
```

| Regra | Porquê |
|---|---|
| Data em **ISO `AAAA.MM.DD`** | Garante que a ordenação alfabética é sempre cronológica. `MM.DD.AAAA` e `DD.MM.AAAA` parecem funcionar dentro do mesmo ano e partem na viragem |
| **Sem acentos** no nome | Evita falhas em scripts, em portais camarários e na leitura por processos automáticos |
| Sufixo em **PascalCase**, sem espaços | `_OpcaoC`, `_LICBranco`, `_ParqueEstacionamento` |
| **Um único ficheiro corrente** na raiz | Quem abre a pasta não hesita; as versões anteriores vivem em `00 . Arquivo` |

### 5.2 Estrutura da pasta de modelação

```
0 . PLN
├── FA-YYYY-NNN_NomeProjeto_AAAA.MM.DD.pln   ← corrente, único na raiz
├── 00 . Arquivo\        versões anteriores, agrupadas por período
├── 01 . Trocas\         ficheiros de terceiros (engenharia, topografia, cliente)
├── 02 . Recursos\       texturas, mapas — sem data de versão do modelo
└── 03 . Alteracoes\     alterações em curso
```

Ficheiros vindos de terceiros nomeiam-se pela **data e origem** (`2026.05.08_LomboSer_Implantacao`), nunca pela abreviatura de quem enviou.

## 6. Auditoria bimarq 5.0 → FA_Template_28 (protocolo de absorção)

A FA tem licença do Template bimarq 5.0 (Lucas Bacelar, AC28/29). Objetivo: absorver as boas ideias ADAPTADAS à realidade portuguesa — nunca copiar a estrutura verbatim (licença de uso individual; o skill regista apenas as decisões FA resultantes).

### Filtro de pertinência (aplicar a cada item analisado)

**TRANSFERE-SE (mecânica Archicad, independente de país):**
- Organização de favoritos por fase de projeto e por ferramenta
- Graphic Overrides de apresentação (planta humanizada, esquemas)
- Estrutura do View Map e lógica de clones por fase
- Truques de produtividade: predefinições, work environment, atalhos
- Soluções de modelação (composites inteligentes, perfis, prioridades)

**NÃO SE TRANSFERE (contexto brasileiro):**
- Fases EP/PL/PE → traduzir para fases FA: Estudo Prévio/PIP → Licenciamento (RJUE) → Execução → Assistência
- Quantitativos e tabelas NBR → substituir por mapas Portaria 71-A/2024 (quadro sinóptico, mapa de vãos FA)
- Alvenaria estrutural BR, detalhes construtivos tropicais → ignorar salvo interesse pontual
- Nomenclatura bimarq de layers/atributos → converter SEMPRE para nomenclatura FA (`FA-`, `@`, categorias)

### Processo
1. Extrair atributos do bimarq (Tapir em Cowork/Code, ou export do Attribute Manager)
2. Tabela comparativa bimarq vs FA por domínio: layers, favoritos, overrides, pen sets, view map, BMs/composites
3. Classificar cada diferença: ABSORVER (com tradução FA) / IGNORAR (contexto BR) / JÁ MELHOR NA FA
4. Plano de implementação no FA_Template_28 com aprovação prévia
5. Decisões finais entram neste skill como standard FA — nunca conteúdo bimarq em bruto

## 7. Lições de sessões anteriores

- A criação do template master ficou documentada em DOCX (guia de atributos) + XLSX (checklist de validação) + script de extração Tapir — manter os três sincronizados quando o template mudar.
- Em ficheiros legados, mapear e eliminar layers órfãs antes de aplicar a estrutura FA (caso Barracão: 19 layers legadas removidas, 5 Layer Combinations criadas).
- Sempre que o trabalho automático for impossível (XML import quebrado, zonas não delimitadas), produzir um guia passo-a-passo para a UI com capturas/caminhos exatos de menu — nunca deixar o utilizador sem caminho de execução.

- Nomenclatura de .pln do Barracao normalizada em 2026.07.29: 55 ficheiros de MM.DD.AAAA para FA-2018-002_Barracao_AAAA.MM.DD. Antes de renomear ou mover .pln, ler os caminhos gravados no binario (hotlinks, xrefs, texturas) sem abrir o Archicad -- e a unica forma de saber o risco com a aplicacao fechada.
- Texturas e mobiliario descarregado nao devem entrar no modelo a partir do Ambiente de Trabalho: quando o perfil muda, os caminhos partem-se. Origem correta: Z:\05_Bibliotecas.
