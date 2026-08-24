#!/usr/bin/env bash
# Sincroniza o ambiente Claude para este repo e faz commit.
# Uso: bash sync.sh   (de qualquer diretório)
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
CL="$HOME/.claude"

# 1. Skills (sem caches/backups)
rm -rf "$REPO/skills"
mkdir -p "$REPO/skills"
cp -r "$CL/skills/." "$REPO/skills/"
find "$REPO/skills" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$REPO/skills" \( -name "*.pyc" -o -name "*.bak*" \) -delete 2>/dev/null || true

# 2. Memorias de todos os projetos
rm -rf "$REPO/memory"
mkdir -p "$REPO/memory"
for d in "$CL/projects/"*/memory; do
  [ -d "$d" ] || continue
  proj="$(basename "$(dirname "$d")")"
  mkdir -p "$REPO/memory/$proj"
  cp -r "$d/." "$REPO/memory/$proj/"
done

# 3. Config (sem settings.local.json — permissoes sao por maquina)
mkdir -p "$REPO/config"
cp -f "$CL/settings.json" "$REPO/config/" 2>/dev/null || true
cp -f "$CL/statusline.py" "$REPO/config/" 2>/dev/null || true

# 4. Protocolos comfy_dl (so documentos, nunca os PNGs de trabalho)
mkdir -p "$REPO/comfy_dl"
find /c/comfy_dl -maxdepth 1 \( -name "*.md" -o -name "*.py" -o -name "*.json" \) -exec cp -f {} "$REPO/comfy_dl/" \;

# 5. Docs do projeto Nanobana
mkdir -p "$REPO/nanobana"
cp -f "$HOME/Nanobana/design-spec.md" "$HOME/Nanobana/prompts.md" "$HOME/Nanobana/prompts-template.md" "$REPO/nanobana/" 2>/dev/null || true
rm -rf "$REPO/nanobana/controlnet"
cp -r "$HOME/Nanobana/controlnet" "$REPO/nanobana/controlnet"

# 6. Commit se houver alteracoes
cd "$REPO"
git add -A
if git diff --cached --quiet; then
  echo "Sem alteracoes — nada a fazer."
else
  git commit -m "sync $(date +%Y-%m-%d_%H%M)"
  echo "Commit feito. Para enviar: git push"
fi
