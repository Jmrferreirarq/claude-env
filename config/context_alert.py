#!/usr/bin/env python3
"""Stop-hook: alerta por toast do Windows quando o contexto da sessao cruza limiares.

Corre localmente no fim de cada resposta (zero tokens, nao chama o modelo).
Silencioso ate 60%; alerta em 60% / 85% / 95%, uma vez por limiar por sessao
(reset automatico quando o contexto desce, p.ex. apos compact ou /clear).
`python context_alert.py --test` dispara um toast de teste.
"""
import sys, os, json, subprocess

THRESHOLDS = [
    (95, "URGENTE: contexto a {pct}% — auto-compact iminente"),
    (85, "Contexto a {pct}% — fecha o raciocinio em curso"),
    (60, "Contexto a {pct}% ({used}/{limit})"),
]
STATE_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
                         "claude-context-alert")


def toast(title, msg):
    ps = (
        '[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, '
        'ContentType = WindowsRuntime] | Out-Null; '
        '$x=[Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent('
        '[Windows.UI.Notifications.ToastTemplateType]::ToastText02); '
        '$t=$x.GetElementsByTagName("text"); '
        f'$t.Item(0).AppendChild($x.CreateTextNode("{title}")) | Out-Null; '
        f'$t.Item(1).AppendChild($x.CreateTextNode("{msg}")) | Out-Null; '
        '[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('
        '"Claude Code").Show([Windows.UI.Notifications.ToastNotification]::new($x))'
    )
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                   capture_output=True, timeout=15)


def last_usage(path, tail_bytes=300 * 1024):
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - tail_bytes))
            tail = f.read().decode("utf-8", "ignore")
    except Exception:
        return None
    usage = None
    for line in tail.splitlines():
        line = line.strip()
        if not line.startswith("{") or '"usage"' not in line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") == "assistant" and not o.get("isSidechain"):
            u = (o.get("message") or {}).get("usage")
            if u and "input_tokens" in u:
                usage = u
    return usage


def fmt_k(n):
    return f"{n/1000:.0f}k" if n < 1_000_000 else f"{n/1_000_000:.2f}M"


def main():
    if "--test" in sys.argv:
        toast("Claude Code — teste", "Alertas de contexto ativos (60/85/95%)")
        return
    sys.stdin.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    u = last_usage(data.get("transcript_path") or "")
    if not u:
        return
    used = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
            + u.get("cache_creation_input_tokens", 0))
    limit = 1_000_000 if used > 200_000 else 200_000
    pct = round(used / limit * 100)

    sid = (data.get("session_id") or "unknown")[:36]
    os.makedirs(STATE_DIR, exist_ok=True)
    state_file = os.path.join(STATE_DIR, sid + ".txt")
    try:
        last_alerted = int(open(state_file).read().strip())
    except Exception:
        last_alerted = 0

    if pct < 60:
        if last_alerted:  # contexto desceu (compact/clear) -> rearmar
            try: os.remove(state_file)
            except OSError: pass
        return

    for threshold, template in THRESHOLDS:
        if pct >= threshold:
            if threshold > last_alerted:
                toast("Claude Code — consumo",
                      template.format(pct=pct, used=fmt_k(used), limit=fmt_k(limit)))
                open(state_file, "w").write(str(threshold))
            break


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # um hook nunca deve partir a sessao
