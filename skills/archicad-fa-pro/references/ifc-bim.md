# IFC4, Zonas e Mapas — Extração BIM para Documentação

## 1. Princípio

Toda a documentação automática FA depende de um modelo bem classificado. Antes de gerar qualquer mapa, validar: cada compartimento tem IfcSpace com nome, número e área; cada vão tem referência FA (PE/PI/PC/PS/JE/PJ); cada elemento tem classificação IFC4 e BM corretos. Se a base estiver suja, o primeiro entregável é o diagnóstico de lacunas, não o mapa.

## 2. Codificação de espaços (IfcSpace)

| Código | Espaço | Nota de área |
|---|---|---|
| RES-ARR | Arrumos/Despensa | Separar de A.U. se necessário |
| RES-GAR | Garagem | Área bruta dependente |
| RES-VAR | Varanda/Marquise | 50% para ABC conforme CIMI |
| RES-TER | Terraço acessível | Área bruta dependente |
| COM-LOJ | Loja | Área bruta comercial |
| COM-ESC | Escritório | Uso serviços |
| SER-TEC | Sala técnica | Não habitável |
| COM-ZCO | Zona comum de edifício | Não contar em fração |
| EXT-LOG | Logradouro | Exterior privado |
| EXT-JDM | Jardim | Exterior privado |

(Compartimentos habitacionais correntes — sala, quartos, cozinha, IS — seguem a nomenclatura do projeto, com área útil em NetFloorArea.)

## 3. Mapas gerados automaticamente (fluxo Tapir → Claude → ficheiro)

| Mapa | Fonte no modelo | Output |
|---|---|---|
| **Mapa de Vãos** | IfcDoor/IfcWindow: largura, altura, tipo, material, RF, acústica, referência FA | XLSX/HTML formato FA |
| **Mapa de Áreas / Quadro Sinóptico** | IfcSpace + NetFloorArea | XLSX/ODS (exigência Portaria 71-A/2024) |
| **Mapa de Acabamentos** | IfcSpace + materiais por superfície (teto/parede/pavimento/rodapé) | HTML interativo padrão FA (referência: David Afonso 00082, ISPM Cacia) |
| **Mapa de Compartimentos** | Hierarquia de pisos: designação, A.U., A.B., pé-direito, uso | XLSX |
| **Quantidades / Orçamentação** | `/quantities` do BIM Bridge: áreas, volumes por BM | XLSX com preços por projeto |

## 4. Verificação regulamentar automática

Cruzar áreas extraídas com mínimos RGEU e sinalizar incumprimentos ANTES da submissão:
- Sala ≥ 10,5 m² (T0/T1; cresce com tipologia)
- Quarto principal ≥ 10,5 m²; restantes ≥ 9 m² (duplo) / valores RGEU Art. 66.º
- Cozinha ≥ 6 m²
- Pé-direito mínimo habitável: 2,70 m (2,40 m em zonas não habitáveis/sanitárias, vãos de teto inclinado conforme RGEU)

Reportar como tabela: compartimento, área modelo, mínimo aplicável, estado (✓/✗). Em caso de dúvida sobre o mínimo aplicável, citar o artigo e pedir confirmação — não inventar valores.

## 5. Mapa de Acabamentos FA — estrutura standard

Sistema de materiais M1–M10 por projeto; tabela de 7 colunas (FA Design System); secção por compartimento com cabeçalho Dark+Gold 9mm; swatches 22×14mm; extração IFC como fonte única de verdade. Para HTML interativo, seguir o padrão estabelecido (15–20 secções, navegação por âncoras, dados BIM incorporados).

## 6. Fluxo de schedules (híbrido obrigatório)

```
Tapir extrai dados → Claude valida + formata XLSX → utilizador importa no Archicad
```
O schedule fica no Archicad ligado ao modelo, mas a criação do Interactive Schedule em si é manual. Indicar sempre este passo ao utilizador.
