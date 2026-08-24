---
name: Tapir MCP setup (Archicad)
description: O utilizador já tem o MCP ArchicadTapir registado no user scope do Claude Code, lançado via C:\tapir_home\start_tapir.bat
type: reference
originSessionId: 63bba1df-9037-476f-a180-21a5d53c85d6
---
Setup do MCP Tapir para Archicad 28 no computador do utilizador:

- **Nome do MCP:** `ArchicadTapir` (scope: user)
- **Comando de arranque:** `cmd /c C:\tapir_home\start_tapir.bat`
- **Verificar estado:** `claude mcp list`
- **Ferramentas Python:** `uvx 0.11.3`, `Python 3.14.2` instalados globalmente
- **Repositório de referência do MCP:** https://github.com/SzamosiMate/tapir-archicad-MCP
- **Add-on Tapir no Archicad:** https://github.com/ENZYME-APD/tapir-archicad-automation

**How to apply:**
- Antes de pedir info do Archicad, confirmar que o Archicad está aberto com um projecto e que o Tapir está activo no Add-On Manager.
- Se `claude mcp list` mostrar `✓ Connected` mas as tools `mcp__ArchicadTapir__*` não aparecerem no ToolSearch, sugerir reiniciar o Claude Code — o registo de tools MCP faz-se no arranque da sessão.
- Não tentar reinstalar via `claude mcp add` (já existe no user config); se for preciso reconfigurar, usar `claude mcp remove ArchicadTapir --scope user` primeiro.
