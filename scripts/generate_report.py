#!/usr/bin/env python3
"""
Antares DS — Weekly Report Generator
Legge i changelog modificati dall'ultimo report, chiama Claude,
posta un riassunto + post per componente su Slack.
"""

import os
import json
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
CLAUDE_MODEL = "claude-sonnet-4-6"


# ─── Git helpers ────────────────────────────────────────────────────────────

def get_last_report_tag():
    """Restituisce l'ultimo tag report-* o None se non esiste."""
    result = subprocess.run(
        ["git", "tag", "--list", "report-*", "--sort=-version:refname"],
        capture_output=True, text=True
    )
    tags = [t for t in result.stdout.strip().split("\n") if t]
    return tags[0] if tags else None


def get_changed_changelog_files(since_ref):
    """
    Restituisce i path dei changelog.md modificati dall'ultimo report.
    Se non esiste nessun tag, usa i commit degli ultimi 7 giorni.
    """
    if since_ref:
        cmd = ["git", "diff", "--name-only", since_ref, "HEAD"]
    else:
        cmd = ["git", "log", "--name-only", "--pretty=format:", "--since=7 days ago"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    return list(set(
        f for f in files
        if f.endswith("changelog.md") and f.startswith("components/")
    ))


def create_report_tag():
    """Crea e pusha un tag report-YYYY-MM-DD per segnare questa run."""
    today = datetime.now().strftime("%Y-%m-%d")
    tag = f"report-{today}"
    subprocess.run(["git", "tag", tag], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)
    return tag


# ─── Claude ─────────────────────────────────────────────────────────────────

def call_claude(changelogs: dict) -> dict:
    """
    Manda i changelog a Claude e riceve JSON con summary + post per componente.
    """
    changelog_text = "\n\n---\n\n".join(
        f"### {path}\n{content}" for path, content in changelogs.items()
    )

    prompt = f"""Sei il comunicatore del Design System Antares.
Questa settimana sono stati aggiornati i seguenti componenti:

{changelog_text}

Il tuo compito è generare due cose:

1. UN MESSAGGIO RIASSUNTIVO GENERALE (3-4 righe max) che introduce la settimana del DS.
   Tono: caldo, diretto, in italiano. Inizia con "Ciao a tutti! 👋"

2. UN POST SLACK PER OGNI COMPONENTE modificato.
   Scrivi come farebbe un designer che racconta il suo lavoro ai colleghi:
   - Prima persona, tono conversazionale
   - Spiega il "perché" della modifica, non solo il "cosa"
   - Menziona il nome del componente in grassetto (*NomeComponente*)
   - Qualche emoji ma senza esagerare
   - Chiudi sempre con "Grazie, DS Team"
   - Lunghezza: 4-8 righe

Rispondi ESCLUSIVAMENTE con un oggetto JSON valido, senza testo prima o dopo:
{{
  "summary": "testo del messaggio riassuntivo",
  "component_posts": [
    {{
      "component": "nome componente",
      "post": "testo del post Slack"
    }}
  ]
}}"""

    body = json.dumps({
        "model": CLAUDE_MODEL,
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        raw = result["content"][0]["text"].strip()
        return json.loads(raw)


# ─── Slack ───────────────────────────────────────────────────────────────────

def post_to_slack(text: str):
    """Posta un messaggio su Slack via Incoming Webhook."""
    body = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                print(f"⚠️  Slack ha risposto con status {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"❌ Errore Slack: {e.code} — {e.read().decode()}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("🔍 Cerco l'ultimo tag report...")
    last_tag = get_last_report_tag()
    print(f"   Ultimo tag: {last_tag or 'nessuno — uso gli ultimi 7 giorni'}")

    print("📂 Cerco changelog modificati...")
    changed_files = get_changed_changelog_files(last_tag)

    if not changed_files:
        print("✅ Nessun changelog modificato questa settimana. Nessun post inviato.")
        return

    print(f"   Trovati: {changed_files}")

    changelogs = {}
    for filepath in changed_files:
        if os.path.exists(filepath):
            changelogs[filepath] = open(filepath).read()
        else:
            print(f"⚠️  File non trovato localmente: {filepath}")

    if not changelogs:
        print("❌ Nessun file leggibile. Esco.")
        return

    print(f"🤖 Chiamo Claude ({CLAUDE_MODEL})...")
    result = call_claude(changelogs)

    print("📤 Invio su Slack...")

    # 1 — Messaggio riassuntivo
    post_to_slack(result["summary"])
    print("   ✅ Riassunto inviato")

    # 2 — Un post per ogni componente
    for item in result.get("component_posts", []):
        post_to_slack(item["post"])
        print(f"   ✅ Post inviato: {item['component']}")

    print("🏷️  Creo tag report...")
    tag = create_report_tag()
    print(f"   ✅ Tag creato: {tag}")

    print("🎉 Report completato.")


if __name__ == "__main__":
    main()
