# Nomenclatura e Atributos FA — Archicad 28

Norma interna da Ferreira Arquitetos para todos os atributos Archicad. Validar SEMPRE antes de criar ou modificar.

## 1. Building Materials

Formato: `[CATEGORIA] - [Nome]`

| Categoria | Significado | Prioridade de intersecção |
|---|---|---|
| EST | Estrutura (betão, aço estrutural) | 850–950 |
| ALV | Alvenarias | 600–750 |
| REV | Revestimentos | 450–550 |
| COB | Coberturas | 400–600 |
| ISO | Isolamentos | 300–450 |
| PAV | Pavimentos | 350–500 |
| MAD | Madeiras | 300–500 |
| MET | Metais | 200–400 |
| ACB | Acabamentos | 150–250 |
| TER | Terrenos | 50–150 |
| ESP | Espaços/ar (caixas de ar) | 10–50 |
| ACB/ALV/COB/ESP/EST/ISO/MAD/MET/PAV/REV/TER | lista fechada — não inventar categorias | — |

Exemplos válidos: `EST - Betão Armado C25/30`, `ISO - XPS 60mm`, `ALV - Tijolo 22`.

Ao criar um BM, definir SEMPRE: nome conforme, prioridade dentro do range da categoria, Cut Fill coerente (fill FA correspondente), surface por defeito, e propriedades térmicas quando relevante para REH/REC.

**Regra de prioridades:** estrutura corta tudo (mais alta), ar/terreno cede a tudo (mais baixa). Se duas camadas se intersectam mal num corte, o diagnóstico começa pelas prioridades.

## 2. Fills

Formato: `FA/[CATEGORIA]/[Nome]` — mesmas categorias dos BMs.
Exemplo: `FA/EST/Betão Armado`, `FA/ISO/XPS`.

## 3. Composites

Formato: `@ [TIPO] - [Descrição] - [Espessura]cm`

| Tipo | Uso |
|---|---|
| PE | Parede exterior |
| PI | Parede interior |
| LJ | Laje |
| CB | Cobertura |
| PV | Pavimento (térreo/exterior) |

Exemplo: `@ PE - ETICS + Tijolo 22 + Reboco - 32cm`.
O `@` força os composites FA para o topo das listas. Espessura no nome = soma real das camadas (validar aritmética). Cada camada referencia um BM FA com prioridade correta — o corte resolve-se sozinho se as prioridades estiverem bem.

## 4. Layers

Formato: `FA-[DISCIPLINA]-[FUNÇÃO]-[SUBFUNÇÃO]`
Nunca purgar layers `FA-` mesmo vazias — fazem parte da estrutura do template.

Layer Combinations de projeto seguem `@ [CÓDIGO]-[NN]` (ex.: `@ BC-01` a `@ BC-05` no Barracão LIC Branco) — uma por fase/tipo de output (licenciamento, execução, apresentação, 3D, especialidades).

## 5. Pen Sets

Três conjuntos oficiais, associados à escala de trabalho:
- **FA-050** — escala 1:50 (execução/pormenor)
- **FA-100** — escala 1:100 (licenciamento)
- **FA-200** — escala 1:200 (implantação/enquadramento)

Associar o pen set à escala da view, nunca misturar.

## 6. Profiles (perfis paramétricos)

Formato: `FA—[LETRA].[NN]` (travessão longo). Biblioteca atual:
- `FA—A.01` — Rodapé / base de parede
- `FA—B.02` — Sanca (correção geométrica aplicada — não reutilizar versões antigas)
- `FA—I.01` — Nariz de degrau
- `FA—J.03` — Guarda interior em vidro com perfil U (redesenhado, 9 erros corrigidos)

Tipologias J = guardas interiores, K = guardas exteriores — separadas por requisitos regulamentares distintos (alturas, esforços). Não cruzar.

## 7. Vãos — referências

Sistema de referenciação de vãos FA:
- **PE** porta exterior · **PI** porta interior · **PC** porta corta-fogo · **PS** porta de correr
- **JE** janela exterior · **PJ** porta-janela

Numeração sequencial por tipo (PE01, PI01…). Validar consistência entre modelo, mapa de vãos e desenhos.

## 8. Checklist de validação (correr antes de qualquer criação/alteração)

1. Nome segue o formato exato da categoria? (incluindo espaços, hífenes, `@`, `FA/`)
2. Categoria pertence à lista fechada?
3. Prioridade dentro do range? Sem colisões ilógicas (ex.: ISO acima de EST)?
4. Cut Fill atribuído e coerente com a categoria?
5. Composite: espessura no nome = soma das camadas?
6. Layer destino existe e é `FA-`?
7. Em renomeações em massa: gerar tabela antes/depois e obter aprovação antes de tocar no modelo.
