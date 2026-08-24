# Recursos Graphisoft — Documentação Oficial, Bibliotecas e APIs

Mapa curado das fontes oficiais Graphisoft para o Archicad 28. Quando uma questão exigir detalhe que não está neste skill (parâmetros de ferramenta, sintaxe GDL, comando da API), consultar a fonte oficial via web_fetch ANTES de responder — nunca inventar parâmetros ou comandos.

## 1. Documentação oficial (Archicad 28)

| Recurso | URL | Quando usar |
|---|---|---|
| Help Center / Reference Guide AC28 | https://help.graphisoft.com/AC/28/INT/ | Ferramentas, settings, workflows de documentação (Layout Book, dimensões, labels) |
| Reference Guide em PDF | Help Center > Getting Help > PDF Reference Guide | Consulta offline/extensa |
| GDL Reference Guide (PDF completo) | https://help.graphisoft.com/AC/28/INT/GDL.pdf | Sintaxe GDL: scripts 2D/3D, parâmetros, comandos (não vem incluído no AC28 por defeito) |
| Graphisoft Community | https://community.graphisoft.com | Knowledgebase, tutoriais, troubleshooting, fórum Python API |
| Support Site | https://support.graphisoft.com | Artigos de resolução de problemas |

### Novidades AC28 relevantes para a FA
- **Documentação orientada a dados**: sistema automatizado de anotação que integra especificações e legendas — explorar para os mapas FA
- **IDS import** (Information Delivery Specification): validação de qualidade de dados IFC — útil para garantir entregas BIM às especialidades
- **AI Visualizer** integrado para conceção
- Propriedades de orientação de portas em Schedules

## 2. APIs e automação (complementa references/tapir-mcp.md)

| Recurso | URL | Conteúdo |
|---|---|---|
| Archicad JSON Interface (oficial) | https://archicadapi.graphisoft.com/JSONInterfaceDocumentation/ | Comandos JSON nativos AC28 (v28.0.0.3001) |
| Python wrapper oficial (`archicad` no pip) | https://archicadapi.graphisoft.com/archicadPythonPackage/archicad.html | Binding Python: GetProfileAttributes, GetPropertyDefinitionAvailability, etc. |
| Tapir Add-On — comandos adicionais | https://enzyme-apd.github.io/tapir-archicad-automation/archicad-addon/ | Comandos no namespace `TapirCommand`, chamados via `ExecuteAddOnCommand` |
| Tapir GitHub (releases, instalação) | https://github.com/ENZYME-APD/tapir-archicad-automation | Add-on instalado via Options > Add-On Manager |
| multiconn_archicad | https://github.com/SzamosiMate/multiconn_archicad | Toolkit Python multi-instância que unifica API oficial + Tapir (namespace `unified`) — candidato para evoluir o FA BIM Bridge |

Padrão de chamada Tapir em Python:
```python
from archicad import ACConnection
conn = ACConnection.connect()
acc, act = conn.commands, conn.types
resp = acc.ExecuteAddOnCommand(act.AddOnCommandId('TapirCommand', 'NomeDoComando'), params)
```

Regra: antes de escrever um script que use um comando, confirmar a sua existência e assinatura na documentação acima — a lista de comandos cresce a cada release e nomes de memória podem estar errados.

## 3. Ecossistema de bibliotecas

### Archicad Library 28 (oficial, incluída)
Biblioteca standard ligada por defeito ao template. Regras FA:
- Manter a Archicad Library 28 como **linked library** — nunca dispersar cópias
- Objetos personalizados FA vão para a **Embedded Library** do projeto OU para as `.pla` FA (perfis, surfaces) — nunca alterar objetos da biblioteca oficial diretamente
- Migração de versão: usar o Library Manager para migrar bibliotecas antigas; objetos legados ficam em "Archicad Library Migration"

### BIMcomponents.com (portal oficial Graphisoft)
- Base de dados cloud de objetos GDL paramétricos, genéricos e de fabricante
- Objetos individuais: drag & drop direto para o Archicad → ficam na Embedded Library
- Bibliotecas completas: download como **LCF** (container com todas as dependências)
- Registo gratuito; permite também publicar objetos FA se um dia fizer sentido

### Fontes externas de objetos (fabricantes)
- **BIMobject.com** — objetos de fabricante filtráveis por formato Archicad (mobiliário, materiais, iluminação)
- **NBS Source**, **ARCAT**, **Modlar**, **Eptar** — catálogos GDL adicionais
- Regra FA: objeto de fabricante entra primeiro em projeto-piloto, valida-se (peso do ficheiro, 2D limpo nas escalas FA-050/100, classificação IFC correta) e só depois entra no template

### Library Part Maker (add-on gratuito Graphisoft)
- Criação de objetos, portas, janelas, claraboias e peças MEP **sem programar GDL**
- Representações 2D/3D sensíveis à escala (detail level) — alinha com os pen sets FA
- Importação de dados de folhas de cálculo para os parâmetros ("o I do BIM")
- Caminho recomendado FA para objetos novos antes de recorrer a GDL puro
- Download: https://www.graphisoft.com/downloads/addons/lpm/int/

### GDL (quando o Library Part Maker não chega)
- Library part = ficheiro `.gsm` com scripts GDL (2D, 3D, parâmetros, UI)
- Consultar SEMPRE o GDL Reference Guide (PDF acima) para sintaxe — não escrever GDL de memória
- Objetos FA com GDL: manter código comentado e versionado na biblioteca FA

## 4. Gestão de bibliotecas no fluxo FA

1. **Auditoria**: Library Manager > verificar missing/duplicate objects antes de qualquer entrega
2. **Consolidação**: na entrega, File > Libraries and Objects > Consolidate para embeber o necessário; arquivo em `.pla` quando o destinatário não tem as bibliotecas FA
3. **Atualização do template**: novos objetos validados → `FA_Biblioteca_Perfis.pla` / `FA_Surfaces_Pack.pla` → registo no guia de atributos
4. **Diagnóstico de objetos em falta** (pontos de interrogação no modelo): identificar via Library Manager, recuperar do BIMcomponents/fabricante ou substituir por equivalente FA — nunca entregar com missing parts

## 5. Fontes comunitárias de aprendizagem (consulta pontual)

| Fonte | Conteúdo | Nota |
|---|---|---|
| Lucas Bacelar — canal YouTube (youtube.com/c/lucasbacelar) | Workflows Archicad: planta humanizada, favoritos/predefinições, fluxo por fases de projeto, integração Twinmotion, interiores e acabamentos | Arquiteto e BIM Manager certificado Graphisoft. ATENÇÃO: método calibrado para o Brasil (fases EP/PL/PE, NBR) — a mecânica Archicad transfere-se; o enquadramento regulamentar NÃO substitui RJUE/Portaria 71-A/2024. Usar apenas conteúdo público gratuito; curso e Template bimarq são produtos pagos proprietários — nunca extrair |
| Graphisoft Community (community.graphisoft.com) | Knowledgebase, tutoriais, troubleshooting, fórum Python API | Fonte oficial — preferir em caso de conflito |
| Graphisoft Learn (learn.graphisoft.com) | Cursos oficiais gratuitos e certificações Graphisoft | Certificação tem peso comercial para a FA |
| Shoegnome Open Template (Jared Banks) | Template open-source + artigos sobre filosofia de templates (porquê de cada layer, view, override) | Leitura de referência para reestruturações do FA_Template_28 |
| MasterTemplate (Eric Bobrow, AECbytes) | Documentação pública de metodologia de template (EUA) | Estudar abordagem, não comprar — comparar com bimarq/FA |
| BIMx (Graphisoft) | Hyper-modelos navegáveis para apresentação a cliente; publica via Publisher Set | Prioridade para a lacuna de apresentação |
| BCF + BIMcollab | Gestão de issues sobre IFC na coordenação de especialidades | Substitui emails com PDFs anotados; issues georreferenciadas no modelo |
| Grasshopper–Archicad Live Connection / Param-O | Geometria paramétrica sem GDL | Evolução futura dos perfis FA — não urgente |

Regra: fontes comunitárias servem para técnica e produtividade; questões regulamentares resolvem-se sempre com a legislação portuguesa em `references/licenciamento.md`.

## 6. Áreas do skill a desenvolver (backlog)

Identificadas como lacunas face ao estado atual (forte em atributos/licenciamento, fraco em apresentação):
1. **Fase de apresentação** — planta humanizada, estilos 3D, render (AI Visualizer AC28, Twinmotion), imagens para cliente e candidaturas (ex.: FORMA)
2. **Favoritos por fase de projeto** — estruturar o FA_Template_28 com favoritos organizados por fase (estudo prévio → licenciamento → execução), inspirado na arquitetura de método por fases
3. **Detalhamento executivo e interiores** — fluxo de pormenorização e mapas de acabamentos a nível de projeto de execução
4. **Validador automático de nomenclatura FA** — script (pasta `scripts/` do skill) que corre via Tapir/BIM Bridge e devolve relatório de conformidade de BMs, composites, layers e vãos contra `references/nomenclatura.md`
5. **Fluxo BIMx** — Publisher Set FA para hyper-modelos de apresentação a cliente
Quando o utilizador trabalhar nestes temas, recolher o aprendido e propor atualização do skill.
