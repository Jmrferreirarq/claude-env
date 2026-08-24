---
name: FA Building Materials System v1 - regras de nomenclatura e priority
description: Regras permanentes para Building Materials, Fills e Composites em projetos FA. Validar antes de criar/alterar.
type: reference
originSessionId: 80da65a5-2c27-4044-8921-c714450958d9
---
Regras permanentes do FA System v1 para Archicad. Aplicam-se a Building Materials, Fills e Composites em projetos do utilizador (Barracao LIC Branco e qualquer outro projeto FA). Validar SEMPRE antes de criar/alterar atributos via Tapir ou propor alterações ao utilizador.

## R1 — Building Materials

Formato: `[CATEGORIA] - [Nome do Material]`

Categorias válidas (11) e intervalos de Intersection Priority:

| Sigla | Significado | Priority |
|---|---|---|
| ACB | Acabamento interior (estuques, gesso cartonado, tintas) | 150-250 |
| ALV | Alvenaria (blocos, tijolos, pedra) | 600-750 |
| COB | Cobertura (impermeabilizacao, substratos) | 400-600 |
| ESP | Espaco/Vazio (air space, camaras de ar) | 10-50 |
| EST | Estrutural (betao, aco estrutural, prefabricados) | 850-950 |
| ISO | Isolamento (termico, acustico, ETICS) | 300-450 |
| MAD | Madeira (lamelada, OSB, ripado, soalho) | 300-500 |
| MET | Metal (zinco, aluminio, aco inox) | 200-400 |
| PAV | Pavimento (ceramica, betonilha, resina) | 350-500 |
| REV | Revestimento exterior (rebocos, argamassas, membranas) | 450-550 |
| TER | Terreno (terra, brita, betao de limpeza) | 50-150 |

## R2 — Fills

Formato: `FA/[CATEGORIA]/[Nome do Fill]`

Categorias alinhadas com R1 excepto ESP (espacos usam `Empty Fill`): FA/ACB/, FA/ALV/, FA/COB/, FA/EST/, FA/ISO/, FA/MAD/, FA/MET/, FA/PAV/, FA/REV/, FA/TER/.

## R3 — Composites

Formato: `@ [TIPO] - [Descricao] - [Espessura]cm`

Tipos validos (5): `@ PE` (Parede Exterior), `@ PI` (Parede Interior), `@ LJ` (Laje), `@ CB` (Cobertura), `@ PV` (Pavimento sem laje).

Exemplo: `@ PE - ETICS / Bloco Cimento / Reboco - 35cm`

## R4 — Validacao obrigatoria

Ao criar/alterar BMs, Fills, Composites:
1. Validar formato do nome (R1/R2/R3)
2. Validar priority dentro do intervalo da categoria (R1)
3. Validar Cut Fill atribuido (nao vazio) — atencao bug Tapir cutSurfaceIndex ignorado, avisar utilizador para corrigir GUI
4. Registar no AUDIT_LOG com antes/depois/estado

## R5 — Hierarquia de priorities

- Nunca dois BMs da mesma categoria com a mesma priority
- Nunca priority fora do intervalo da categoria (R1)
- Air Space/camaras de ar: priority < 50
- Estrutural betao: priority >= 850

**Why:** Sistema de organizacao definido pelo utilizador para garantir consistencia de modelacao, leitura grafica em corte (priorities determinam intersecoes 3D) e auditabilidade dos projetos RJUE em Archicad.

**How to apply:** Antes de qualquer chamada `attributes_create_building_materials` / `_create_composites` / discussao sobre criar fills/BMs/composites, verificar que o nome+priority+formato seguem estas regras. Se o utilizador propuser algo fora das regras, sinalizar e propor alternativa conforme antes de executar.
