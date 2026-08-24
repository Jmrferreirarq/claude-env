# Tapir MCP e FA BIM Bridge — Automação do Archicad

## 1. Arquitetura do pipeline FA

```
Archicad 28 (modelo aberto)
        ↓ porta 19723
Tapir (add-on JSON API / MCP)
        ↓
FA BIM Bridge — Flask, porta 8766 (Windows; 8765 dá conflito de socket)
        ↓ endpoints REST
FA_MapasArchicad.html (dashboard) / Claude
```

Arranque do servidor: `arrancar.bat` no Desktop da máquina FA.

### Endpoints do FA BIM Bridge
| Endpoint | Devolve |
|---|---|
| `/health` | Estado do servidor e da ligação Tapir |
| `/extract/all` | Extração completa do modelo |
| `/openings` | Vãos (portas/janelas) com dimensões e referências |
| `/elements` | Elementos por tipo |
| `/materials` | Building Materials em uso |
| `/quantities` | Quantidades (áreas, volumes) |

Extração validada em produção: projeto "26.05.22_SusanaSantos_AltemEspecialidades" — 116 vãos, 66 compartimentos, 907,95 m².

## 2. O que o Tapir CONSEGUE (leitura + escrita)

- Listar/criar/modificar **elementos** (paredes, lajes, vãos) e as suas propriedades
- Modificar **atributos em massa**: layers, building materials, classificações IFC
- Corrigir nomenclatura FA em todos os elementos de uma vez (ex.: 27 correções de referências de vãos PE/PI/PC/PS/JE/PJ aplicadas no projeto David Rodrigues FA-2025-001)
- Extrair hierarquia de pisos, IfcSpace, áreas, materiais, quantidades
- Descoberta de comandos via `archicad_discover_tools` + execução via `archicad_call_tool`

## 3. O que o Tapir NÃO consegue — nunca prometer

- **Interactive Schedules** dentro do Archicad — fluxo híbrido obrigatório: Tapir extrai → Claude gera XLSX → utilizador importa/atualiza no Archicad
- **Layout Book, carimbo (Master Layout), Publisher Sets** — configuração manual; Claude fornece especificação exata
- **Ficheiro .tpl** — formato proprietário, impossível gerar externamente
- **`AutomaticZoneGeometry` em compartimentos não delimitados** — falha confirmada; criação de zona é manual na UI nesses casos
- **Import de XML de atributos no Archicad 28** — falha de compatibilidade independente do conteúdo; preferir escrita via Tapir ou guia manual para Attribute Manager

## 4. Servidores MCP para Archicad — setup e ecossistema

Cadeia de comunicação completa:
```
Agente IA (Claude) → Cliente MCP (Claude Desktop / Claude Code) → Servidor MCP (Python) → Tapir Add-On (C++) → Archicad
```

### Requisitos
- Archicad 27+ com **Tapir Add-On instalado** (Options > Add-On Manager > Edit List of Available Add-Ons > Add; releases em https://github.com/ENZYME-APD/tapir-archicad-automation/releases)
- Python 3.12+ com `uv`/`uvx`
- Cliente MCP: Claude Desktop ou Claude Code

### Servidor recomendado: `tapir-archicad-mcp` (PyPI)
- Expõe ~137 comandos unificando a API Tapir comunitária e a JSON API oficial, com pesquisa semântica de ferramentas 100% local (sem chaves API, sem dados a sair da máquina)
- Suporta múltiplas instâncias Archicad em simultâneo
- Assenta na biblioteca `multiconn_archicad`
- Configuração no Claude Desktop (`%APPDATA%\Claude\claude_desktop_config.json` no Windows; `~/Library/Application Support/Claude/claude_desktop_config.json` no macOS):
```json
{
  "mcpServers": {
    "ArchicadTapir": {
      "command": "uvx",
      "args": ["--from", "tapir-archicad-mcp", "archicad-server"]
    }
  }
}
```
O `uvx` descarrega e atualiza o pacote automaticamente do PyPI — sem clone manual.

### Alternativas
- `archicad-mcp` (lgradisar) — FastMCP; compila ferramentas a partir dos ficheiros de definição JSON do Tapir. Atenção: se os ficheiros de definição não estiverem em sincronia com a versão do add-on, há comandos desfasados — atualizar a partir do repo Tapir.
- Servidor próprio FA BIM Bridge (secção 1) — REST em vez de MCP; usado pelo dashboard.

### Padrão de utilização no Claude
1. `archicad_discover_tools` / pesquisa semântica → encontrar o comando certo (não adivinhar nomes)
2. `archicad_call_tool` com parâmetros validados contra a doc (https://enzyme-apd.github.io/tapir-archicad-automation/archicad-addon/)
3. Aplicar SEMPRE o protocolo de escrita da secção 6

### Categorias de comandos Tapir (namespace `TapirCommand`)
Aplicação/projeto (versão, info, localização) · Elementos (listar, filtrar, criar, modificar, eliminar) · Atributos (layers, BMs, composites, surfaces, pens) · Propriedades e classificações (IFC incluído) · Zonas e quantidades · Teamwork · Navegação (views, layouts). A lista cresce a cada release — confirmar na doc antes de usar.

### Resolução de problemas
- Add-On não assinado no macOS: permitir em Security Settings e reiniciar o Archicad
- Comandos em falta: versão do Tapir desatualizada vs. doc — atualizar o add-on
- Ligação falha: confirmar Archicad aberto com projeto, porta 19723 livre, e (no caso do bridge FA) Flask ativo na 8766
- Claude.ai (web/mobile) não acede a `localhost` — MCP local só via Claude Desktop/Code

## 5. Contexto de execução

| Contexto | Quando usar |
|---|---|
| **Chat** | Consultas pontuais, validações, geração de outputs (listas, XLSX, relatórios) |
| **Cowork** | Sequências longas no modelo ("cria estes 12 BMs, valida e confirma"), edições do dashboard HTML |
| **Claude Code** | Servidor Flask, scripts Python/Tapir, pipelines de extração, desenvolvimento do bridge |

Nota: claude.ai não liga a MCP local (`localhost`) — Tapir direto só em Claude Code/Desktop. No Chat, trabalhar com exports ou via BIM Bridge se exposto.

## 6. Protocolo de escrita no modelo (obrigatório)

1. Extrair estado atual e apresentar diagnóstico.
2. Gerar plano antes/depois (tabela: elemento/atributo, valor atual, valor proposto).
3. **Aguardar confirmação explícita do utilizador.**
4. Executar em lotes pequenos; após cada lote, re-ler e verificar.
5. Reportar discrepâncias imediatamente; nunca "assumir que correu bem".
6. Recomendar gravação/backup do .pln antes de operações em massa.

## 7. Melhorias em fila para o dashboard (contexto Cowork)

Porta configurável, histórico de snapshots JSON, preços por projeto, indicadores de materiais em falta, separador Portas.
