# claude-env — backup do ambiente Claude Code (FA)

Backup versionado do capital intelectual do ambiente Claude Code:

- `skills/` — skills locais (`archicad-fa-pro`, `interior-redesign-studio`, `interior-design-expert`)
- `memory/<projeto>/` — memorias persistentes por projeto
- `config/` — `settings.json` + `statusline.py` (sem `settings.local.json`: permissoes sao por maquina)
- `comfy_dl/` — protocolos de qualidade e workflows API (`PROTOCOLO-QUALIDADE.md`, `ESTRUTURA.md`, scripts)
- `nanobana/` — design-spec, prompts e guias ControlNet do projeto Nanobana

**Atualizar o backup:** `bash sync.sh` (copia tudo + commit automatico), depois `git push`.

Privado — contem referencias a projetos de clientes.
