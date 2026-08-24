# Dicas e Truques Archicad — Produtividade Diária

Compilação curada de técnicas de utilizadores avançados. Aplicar e ensinar estas técnicas quando o utilizador estiver a trabalhar na UI do Archicad. A lista completa de atalhos vive em Options > Work Environment > Keyboard Shortcuts (exportável para browser/impressão).

## 1. Seleção e navegação

- **TAB** — alterna entre elementos sobrepostos sob o cursor (ex.: selecionar a Zona em vez da Laje). Resolve o problema nº1 de seleção em plantas densas.
- **Spacebar com a Seta ativa** — ativa/desativa temporariamente a seleção de elementos pelas superfícies (não só pelas arestas).
- **Shift + clique** — seleção rápida sem mudar para a ferramenta Seta.
- **Ctrl/Cmd+F (Find & Select)** — seleção por critérios (tipo, layer, material, propriedade). Combinar com "+" para adicionar critérios; essencial para correções em massa antes de recorrer ao Tapir.
- **Marquee fino vs grosso** — fino seleciona só no piso atual; grosso atravessa todos os pisos. Marquee + F5 mostra só essa área em 3D.

## 2. Edição rápida (os que poupam mais tempo)

- **Alt + clique (conta-gotas)** — captura todos os parâmetros do elemento clicado para a ferramenta.
- **Ctrl+Alt + clique (seringa)** — injeta os parâmetros capturados no elemento de destino. O par conta-gotas/seringa substitui 90% das idas aos diálogos de settings.
- **Espaço + clique (varinha mágica)** — gera elementos a partir de contornos existentes (laje a partir de paredes, zona a partir de um espaço fechado, fill a partir de geometria).
- **Q (Force Guide Line Display)** — força a exibição de guide lines durante a introdução de elementos, com o cursor pousado num ponto do elemento.
- **Alt+Shift** — move a origem do utilizador para um nó de elemento existente (reset do tracker). Fundamental para cotas relativas durante a modelação.
- **Enter** — confirma os valores atuais do Tracker; escrever dimensões diretamente durante o desenho em vez de ajustar depois.
- **Ctrl/Cmd + clique numa aresta (Adjust)** — estende/apara o elemento selecionado até à aresta clicada.
- **Pet Palette pelo nó vs pela aresta** — opções diferentes; nós dão stretch/move de vértice, arestas dão offset/curvatura. Conhecer a diferença evita cliques perdidos.

## 3. Visualização e verificação

- **` (acento grave)** — liga/desliga o Trace Reference. Usar para comparar pisos, fases (licenciado vs alterado) e verificar alinhamentos verticais.
- **True Line Weights on/off** — verificar o aspeto final das espessuras de caneta antes de publicar (View > On-Screen View Options); atribuir-lhe atalho próprio.
- **F2/F3 (Planta/3D)** e **F5 (mostrar seleção/marquee em 3D)** — o ciclo planta→3D→planta deve ser reflexo, não menu.
- **Cortes 3D e estilos 3D** — guardar estilos 3D nomeados (branco, com sombras, esquemático) para apresentação imediata.

## 4. Modelação inteligente

- **Solid Element Operations (SEO)** — subtrações/uniões mantêm-se associativas: o operador continua a "cortar" mesmo quando os elementos mudam. Usar para encontros complexos cobertura/parede e negativos em lajes; lembrar que elementos operadores podem viver numa layer oculta dedicada.
- **Prioridades de Building Materials resolvem junções** — antes de ajustar manualmente um encontro de parede/laje, verificar prioridades (ver `references/nomenclatura.md`). Junção mal resolvida = prioridade mal definida, quase sempre.
- **Favoritos por fase** — gravar configurações completas de ferramenta como Favoritos organizados por fase de projeto; clicar num favorito substitui abrir o diálogo de settings (alinhado com o backlog FA e a auditoria bimarq).
- **Opening Tool para nichos, courettes e fachadas** — aberturas associativas que atravessam múltiplos elementos; preferir a SEOs quando o vazio é "técnico" (courettes, ventilações).
- **Expressões em Propriedades** — propriedades calculadas (ex.: contagem automática de tijolo/área de cofragem) que alimentam schedules sem cálculo manual.

## 5. Documentação

- **Zero de cota por compartimento** — dimensões de nível podem referenciar o zero da zona/piso em vez do zero do projeto, útil em desníveis interiores.
- **Etiquetas associativas** — labels ligadas ao elemento atualizam com o modelo; nunca usar texto solto para informação que o modelo conhece (referência de vão, material, área).
- **Autotextos no carimbo** — nome do projeto, escala, data e nº de desenho como autotexto no Master Layout; eliminam erros de carimbo em revisões.
- **Publisher Sets por destino** — publicar conjuntos completos (PDF/A licenciamento, DWG especialidades, BIMx cliente) num clique; nunca imprimir folha a folha (ver `references/licenciamento.md`).

## 6. Work Environment e disciplina

- Personalizar atalhos em Options > Work Environment > Keyboard Shortcuts; se já estiver atribuído, o Archicad avisa e permite substituir.
- Princípios para definir atalhos próprios: comandos frequentes ficam acessíveis a uma mão (lado esquerdo do teclado para destros com rato); agrupar por proximidade; evitar combinações que exijam esticar a mão.
- **Exportar o esquema FA de atalhos e Work Environment** — guardar como perfil partilhável; mesma configuração em todas as máquinas FA e onboarding instantâneo de colaboradores.
- Aprendizagem incremental: dominar primeiro edição básica (mover, rodar, espelhar), depois navegação e 3D — um atalho novo por semana cola melhor do que decorar listas.

## 7. Ficheiro e segurança

- Gravar antes de qualquer operação em massa (Tapir incluído — ver protocolo em `references/tapir-mcp.md`).
- Conhecer a pasta de autosave e os .bpn para recuperação rápida de crashes.
- Em entregas: purge + gravação de cópia de arquivo + consolidação de bibliotecas (ver `references/template-projeto.md` e `references/graphisoft-recursos.md`).
