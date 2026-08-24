#!/usr/bin/env python3
"""Statusline nativa para Claude Code: barra de uso do context window.

Le o JSON da sessao no stdin (transcript_path, model), extrai o usage do
ultimo assistant message do transcript JSONL e imprime uma linha:
  modelo | barra ###----- | usados/limite (pct)
Sem dependencias externas. Falha em silencio para uma linha minima.
"""
import sys, os, json

def read_stdin():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}

def last_usage(path, tail_bytes=300*1024):
    try:
        size = os.path.getsize(path)
        with open(path, 'rb') as f:
            f.seek(max(0, size - tail_bytes))
            tail = f.read().decode('utf-8', 'ignore')
    except Exception:
        return None
    usage = None
    for line in tail.splitlines():
        line = line.strip()
        if not line.startswith('{') or '"usage"' not in line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get('type') == 'assistant' and not o.get('isSidechain'):
            u = (o.get('message') or {}).get('usage')
            if u and 'input_tokens' in u:
                usage = u
    return usage

def fmt_k(n):
    return f"{n/1000:.0f}k" if n < 1_000_000 else f"{n/1_000_000:.2f}M"

def main():
    data = read_stdin()
    model = ((data.get('model') or {}).get('display_name')
             or (data.get('model') or {}).get('id') or 'Claude')
    out = sys.stdout
    u = last_usage(data.get('transcript_path') or '')
    if not u:
        out.write(model)
        return
    used = (u.get('input_tokens', 0)
            + u.get('cache_read_input_tokens', 0)
            + u.get('cache_creation_input_tokens', 0))
    # janela: 200k por defeito; se ja passou disso, e uma sessao de 1M
    limit = 1_000_000 if used > 200_000 else 200_000
    pct = used / limit
    # cor: verde <60%, amarelo <85%, vermelho depois (perto do auto-compact)
    color = '\033[32m' if pct < 0.60 else ('\033[33m' if pct < 0.85 else '\033[31m')
    reset, dim = '\033[0m', '\033[2m'
    width = 10
    fill = min(width, round(pct * width))
    bar = color + '█' * fill + dim + '░' * (width - fill) + reset
    line = f"{model} {dim}|{reset} {bar} {color}{fmt_k(used)}{reset}{dim}/{fmt_k(limit)} ({pct*100:.0f}%){reset}"
    cost = (data.get('cost') or {}).get('total_cost_usd')
    if isinstance(cost, (int, float)) and cost > 0:
        line += f" {dim}| ${cost:.2f}{reset}"
    out.write(line)

if __name__ == '__main__':
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        main()
    except Exception:
        print('Claude')
