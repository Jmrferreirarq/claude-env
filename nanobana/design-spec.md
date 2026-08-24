# Design Spec — Moradia DavidAfonso (casa completa)

> Documento específico deste projeto (fonte: 18 vistas em `source\` + modelo Archicad
> "DavidAfonso", porta 19723). Moradia de **2 pisos**. NÃO é template global.

## Modo de fidelidade (DECIDIDO)
**Fiel + só trocas acordadas.** Preservar exatamente arquitetura e elementos construídos; mudar só
o aprovado, por tipologia. Default = preservar. Limite: a IA é generativa (teto de fidelidade) →
para rigor absoluto, **CineRender no Archicad**.

## Conceito (toda a casa)
**Minimalismo quente com contraste.** Branco nas paredes; **carvalho** como fio quente (escada +
soalho do P1 + peças soltas); contraste pela **porta preta + candeeiros antracite**; guardas em
vidro. Acento **terracota** na zona social; quartos com **ligeira variação** (ver tipologias).

### Carvalho de referência (tom único — usar igual em TODA a casa)
O modelo não tem carvalho personalizado (surfaces são do template genérico; a escada usa um wood
*stock*, provavelmente Walnut → daí ler escura). Por isso o tom **define-se** e fixa-se aqui:
> **Carvalho médio quente, natural, mate** — castanho-mel, veio reto subtil; **nem amarelado, nem
> espresso/wengé**. É o MESMO em: degraus da escada (cobertor+espelho) · soalho flutuante do P1 · cabeceiras dos quartos ·
> móveis de I.S. · mobiliário solto da social. Colar esta descrição *verbatim* em todos os prompts.

## Pisos (modelo — GetStories)
R/C **0.0** · Piso 1 **+3.00** · topo **+5.80**. Zona social com **duplo pé-direito ~5.8 m**;
quartos/suite do Piso 1 a +3.0. Geo/Norte = **default (não fiável)** → orientação por indicação do
arquiteto.

## Lista de vistas (limpa — há números repetidos na pasta)
| Espaço | Piso | Ficheiro |
|---|---|---|
| Entrada (corredor + porta) | 0 | 01 Entrada / 02 Entrada |
| Arrumos | 0 | 03 Arrumos |
| Zona Social (estar/jantar/cozinha) | 0 | 03 Zona Social · 07 · 08 · 06 Cozinha |
| I.S. piso 0 | 0 | 04 I.S. Piso 00 · 05 I.S. Piso 00 |
| Quartos piso 0 | 0 | 09 Quarto Piso 00 · 12 Quarto Piso 00 |
| Lavandaria | 0 | 11 Lavandaria |
| Circulação / galeria | 1 | 10 Circulação · 11 Circulação |
| Suite | 1 | 13 Suite Piso 01 |
| Closet | 1 | 14 Closet Piso 01 |
| I.S. da suite (com banheira) | 1 | 15 I.s. Suite Piso 01 |
| I.S. piso 1 | 1 | 16 I.s. Piso 01 |

## 🔒 PRESERVAR — intocável (geral)
- Arquitetura, geometria, **vãos/envidraçados** como modelados.
- **Guardas/balaustradas em VIDRO** (vazio social + galeria do Piso 1) — nunca prumos metálicos.
- **Escada FECHADA (degraus sólidos):** degraus em **volumes sólidos empilhados — SEM espelhos
  abertos, SEM vãos/transparência entre degraus** (NÃO é escada flutuante/aberta; nunca usar
  "floating"). Faces laterais e intradorso (soffit) **em off-white (cor das paredes)**; **só o
  cobertor (piso) + o espelho (face vertical) de cada degrau em CARVALHO** de referência. Não fazer
  a escada toda em madeira.
- **Porta de entrada preta** full-height.
- **Candeeiros cónicos antracite** (social) e restantes luminárias — podem melhorar-se (ver Luz),
  não inventar formas absurdas.
- **Marcenaria de cozinha em BRANCO** (armários, roupeiros, frentes, lados da ilha), **EXCETO a
  frente ripada vertical da ilha (virada à sala), que é em CARVALHO de referência** (mesmo tom da
  escada). **Bancada pedra greige.** Sem outra madeira na cozinha.
- **Manter o layout dos armários, divisões de portas/gavetas e eletrodomésticos embutidos EXATAMENTE
  como no modelo** — não acrescentar, mover nem redesenhar. *(Elemento onde a IA deriva →
  fidelidade real só em CineRender/Twinmotion.)*
- **Eletrodomésticos em AÇO INOX:** frigorífico, forno e micro-ondas com acabamento **inox**; o
  **frigorífico é uma coluna alta com PEGA VERTICAL**. Manter posições — só o acabamento é inox; a
  restante marcenaria fica branca. **Frigorífico identificado (Tapir):** objeto "Refrigerator",
  **coluna 0,60 × 0,60 × 2,00 m**, no troço da cozinha (planta ~105.83, 46.54) — inox, pega vertical.
- **I.S. (acabamentos a preservar):** porcelânico cinza grande formato; **parede de realce
  terrazzo/granito claro** no duche; **móvel suspenso em carvalho + tampo preto + lavatório
  pousado**; espelho; duche walk-in em vidro; loiça suspensa. **Suite:** banheira em mármore +
  duplo lavatório (registo mais luxe).
- **Pavimentos (regra por piso):**
  - **R/C (Piso 0) = porcelânico greige** grande formato, **60×120 alinhado**, junta fina — em
    TODA a área do r/c, **incluindo quartos** ("piso inferior sempre cerâmico").
  - **Piso 1 = flutuante em CARVALHO** (mesmo tom da escada).
- **Rodapés:** manter a **cor existente (escura)** — NÃO alterar sem pedido expresso.

## 🎨 ALTERAR — aprovado, por tipologia
**Zona Social:** sofá → linho oatmeal · poltrona → bouclé **terracota** (era amarela) · mesa centro
→ carvalho · **tapete** oatmeal c/ fio terracota · mesa refeições → carvalho · cadeiras →
carvalho+rush · paredes → off-white cremoso. (Madeira só nas peças soltas; nunca nos embutidos.)

**Quartos:** paredes off-white · **têxteis quentes** (linho/lã, oatmeal/terra) · **cabeceira/painel
em carvalho** · **um acento subtil por quarto**: **suite = terracota** · **quarto A = azeitona/
sálvia** · **quarto B = mostarda/ocre**.

**I.S. / Lavandaria / Circulação:** **modo fiel** — só fotorrealismo + luz + verdes/decoração leve.
Sem trocas de acabamento (já têm carácter próprio: terrazzo + carvalho + pedra).

**Torneiras e lava-loiça (casa toda):** todas as **torneiras/misturadoras** (cozinha + I.S. +
chuveiros) e o **lava-loiça da cozinha** em **AÇO INOX ESCOVADO** — substitui quaisquer
torneiras/loiças pretas ou cromadas do modelo.

## ➕ ADICIONAR (se se adaptar)
Verdes/plantas · pequenos objetos/utensílios · animais · **iluminação** coerente (melhorar/adicionar).
Nunca alteram a lista PRESERVAR.

## Luz natural (definição do arquiteto)
Geo/norte do modelo = default. **Âncora real (confirmada): envidraçado principal da zona social a
NORTE** → luz fria/indireta, **sem sol direto**, aquecida por candeeiros 2700–3000K. O **Norte
verdadeiro será definido pelo arquiteto no Archicad** segundo esta âncora (para o sol do
CineRender). Restantes divisões: orientação **derivada por leitura do modelo** (relativa a esta
âncora) ou indicada pelo arquiteto, quando chegarmos a cada vista.

## Narrativa (visita à casa — 2 pisos)
**Logline:** *Casa de família serena — minimalismo quente, carvalho e branco, contraste discreto;
um fim de tarde tranquilo de fim-de-semana.*
**Momento/luz único:** fim de tarde de fim-de-semana (luz natural + candeeiros quentes já acesos),
igual em todas as vistas.
**Elenco (incidental):** casal + criança + gato; roupa em tons terrosos. *(IA não garante a mesma
cara entre imagens — manter de fundo.)*
**Arco:** **Chegada** (entrada/porta preta) → **Coração** (zona social, duplo pé-direito) →
**Privado R/C** (quartos + I.S.) → **Subida** (escada de carvalho + galeria de vidro) → **Topo**
(suite → closet → I.S. com banheira). Continuidade: mesma luz, mesmo elenco, carvalho + branco +
acento terracota como fio.

## 💡 Iluminação (PODES intervir)
Melhorar/corrigir luminárias existentes e **adicionar** luz em camadas (ambiente+tarefa+acento),
quente 2700–3000K, CRI ≥ 90; manter posições coerentes; não achatar o duplo pé-direito.

## Método (por vista)
1. **Compatibilizar com o BIM** (Tapir): pisos/pés-direitos, dimensões, materiais.
2. **Prompt fiel** com a lista PRESERVAR explícita + o **carvalho de referência** *verbatim*;
   geometria/viewpoint da imagem-fonte.
3. **Proporção 3:2** por defeito (4:5 para pé-direito alto, 16:9 panorâmica).
4. **QA elemento-a-elemento** antes de mostrar.

## Estratégia para a casa toda (18 vistas)
- **Âncoras por grupo de coerência** (não uma só): **Social**, **Quartos**, **I.S.**, **Piso 1
  (madeira/galeria)**. Renderizar e validar **a âncora de cada grupo primeiro**.
- **⚠️ Encadeamento de referência sobrepõe o ENQUADRAMENTO:** ao passar a âncora como 2.ª imagem, o
  modelo agarra a **composição** da âncora (testado: a 06 saiu igual à 07). Por isso: **só encadear**
  quando a nova vista tem enquadramento semelhante; para **vistas com enquadramento próprio,
  renderizar SÓ com a fonte** (`--image fonte`) e levar a coerência pelo **texto** (carvalho de
  referência + paleta + lista PRESERVAR). Confirmado que assim a 06 acerta vista + correções.
- **Fase 2 (humanização) só nos heróis**: zona social (e talvez a suite). I.S., circulação, closet,
  lavandaria ficam **sem pessoas**.
- **Nomenclatura de saída**: `renders\<NN>_<espaço>_p1.png` (resolve os números duplicados da pasta).
- **Folha de contacto por grupo/piso** (`contact_sheet.py`) para QA de coerência.
- **Ordem sugerida**: Social → Entrada → Quartos+I.S. R/C → Circulação/galeria → Suite+closet+I.S.

## REGRA DURA — não alterar NEM remover a composição/estrutura
É **proibido alterar a composição/estrutura da imagem original** e **proibido remover/omitir/
simplificar qualquer elemento** (armários, eletrodomésticos, nichos, detalhes — tudo o que existe
na fonte tem de aparecer). A IA generativa (Nano Banana)
**regenera a imagem toda** e **não consegue trancar a estrutura** (provado 4× na 06: escada e
candeeiros a mudar). Logo: **vistas estruturais (escada, cozinha, casca) → CineRender, NUNCA IA.**
Não reinsistir na IA para estas vistas. (IA com estrutura trancada exigiria ControlNet/depth — outro
setup, não disponível.)

## Motor por vista (HÍBRIDO) dentro das 2 fases
**Fase 1 — fotorrealismo (motor por vista):**
- **CineRender (Archicad, pelo arquiteto):** casca pesada — Entrada (01,02), Social (03,06,07,08),
  Circulação (10,11), Arrumos, Lavandaria, I.S. (04,05,15,16). Fidelidade de escada/cozinha/
  terrazzo/aço escovado. *(Materiais e Norte definidos pelo ARQUITETO no Archicad; o assistente só
  verifica/assiste e LÊ dados via Tapir — não modifica o modelo nem dispara o render.)*
- **IA (Nano Banana, assistente):** Quartos (09,12), Suite (13), Closet (14) — casca simples,
  staging quente fiável.
**Fase 2 — humanização (IA):** só **heróis** (social + suite); pessoas/vida sobre a imagem da
**Fase 1 já aprovada** (base CineRender ou IA); **1 imagem**; **perguntar sempre**. Ressalva:
humanizar uma base CineRender re-processa a imagem (pequeno risco de tocar a casca → manter
pessoas incidentais).

## ✅ Checklist QA por vista
- [ ] Guardas em VIDRO (não metálicas)
- [ ] **Cozinha branca, EXCETO a frente ripada vertical da ilha em CARVALHO** (tom da escada); bancada pedra greige
- [ ] **Escada FECHADA (degraus sólidos, sem vãos) — laterais/soffit off-white + cobertor+espelho em carvalho**; **soalho P1 carvalho**; **R/C porcelânico greige 60×120 (incl. quartos)**
- [ ] **Rodapés mantêm a cor existente (escura)** — não alterados
- [ ] I.S. preservadas (terrazzo + móvel carvalho + tampo preto + vidro); suite com banheira mármore
- [ ] **Torneiras/misturadoras + lava-loiça em aço inox escovado** (cozinha + I.S. + chuveiros)
- [ ] Candeeiros antracite / luminárias coerentes
- [ ] Porta preta, vãos/envidraçados como na fonte
- [ ] Madeira só em soltos; acento certo por divisão (terracota social; subtil nos quartos)
- [ ] Luz coerente com a orientação; pés-direitos corretos
- [ ] Enquadramento = fonte; nada inventado
