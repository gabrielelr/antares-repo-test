#!/usr/bin/env python3
"""
Antares DS — Weekly Report Generator
Messaggio 1: report strutturato (componenti, date, autori, progetti)
Messaggio 2+: post conversazionale per ogni componente (Claude)
"""

import os
import json
import re
import subprocess
import urllib.request
import urllib.error
from datetime import datetime

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
CLAUDE_MODEL = "claude-sonnet-4-6"
FIGMA_BASE_URL = "https://www.figma.com/file/"

TYPE_EMOJI = {
    "new": "🆕",
    "updated": "✏️",
    "update": "✏️",
    "bug fix": "🐛",
    "fix": "🐛",
    "removed": "🗑️",
    "deprecated": "⚠️",
}

def get_emoji(change_type: str) -> str:
    return TYPE_EMOJI.get(change_type.lower(), "•")


# ─── Git ─────────────────────────────────────────────────────────────────────

def get_last_report_tag():
    result = subprocess.run(
        ["git", "tag", "--list", "report-*", "--sort=-version:refname"],
        capture_output=True, text=True
    )
    tags = [t for t in result.stdout.strip().split("\n") if t]
    return tags[0] if tags else None


def get_changed_changelog_files(since_ref):
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
    base = datetime.now().strftime("%Y-%m-%d")
    tag = f"report-{base}"
    # Se il tag esiste già (run multipli nello stesso giorno) aggiungi orario
    existing = subprocess.run(
        ["git", "tag", "--list", tag], capture_output=True, text=True
    ).stdout.strip()
    if existing:
        tag = f"report-{datetime.now().strftime('%Y-%m-%d-%H%M')}"
    subprocess.run(["git", "tag", tag], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)
    return tag


# ─── Parsing ─────────────────────────────────────────────────────────────────

def parse_frontmatter(content: str) -> dict:
    meta = {"component": "", "figma_id": "", "last_updated": ""}
    if not content.startswith("---"):
        return meta
    end = content.find("---", 3)
    if end == -1:
        return meta
    for line in content[3:end].strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"')
    return meta


def parse_entries(content: str) -> list:
    """
    Estrae le voci changelog come lista di dict:
    {date, type, description, author, project}
    """
    entries = []
    current_date = ""
    body = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL)
    body = re.sub(r"^#(?!#)[^\n]*\n", "", body, flags=re.MULTILINE)  # rimuove solo # non ##

    for line in body.split("\n"):
        date_match = re.match(r"^###\s+(.+)", line)
        if date_match:
            current_date = date_match.group(1).strip()
            continue

        entry_match = re.match(r"^-\s+\*\*(.+?)\*\*\s*[·•]\s*(.+)", line)
        if entry_match and current_date:
            change_type = entry_match.group(1).strip()
            rest = entry_match.group(2).strip()
            parts = rest.split(" — ")
            description = parts[0].strip()
            author, project = "", ""
            if len(parts) > 1:
                m = re.match(r"\*(.+?)\*\s*[·•]?\s*(.*)", parts[1])
                if m:
                    author = m.group(1).strip()
                    project = m.group(2).strip()
                else:
                    author = parts[1].strip()
            entries.append({
                "date": current_date,
                "type": change_type,
                "description": description,
                "author": author,
                "project": project,
            })
    return entries


# ─── Messaggio 1: Report strutturato (Python, no LLM) ────────────────────────

def build_weekly_report(changelogs_data: list) -> str:
    today = datetime.now().strftime("%d %b %Y")
    n_components = len([d for d in changelogs_data if d["entries"]])
    lines = [
        f"📋 *Antares DS — Weekly Report* | {today}",
        f"_{n_components} {'componente aggiornato' if n_components == 1 else 'componenti aggiornati'} questa settimana_",
        "",
    ]

    for item in changelogs_data:
        meta = item["meta"]
        entries = item["entries"]
        if not entries:
            continue

        component_name = meta.get("component") or item["filepath"].split("/")[1].title()
        dates = list(dict.fromkeys(e["date"] for e in entries))
        lines.append(f"*{component_name}* · {', '.join(dates)}")

        for e in entries:
            emoji = get_emoji(e["type"])
            line = f"  {emoji}  {e['type']} · {e['description']}"
            if e["author"]:
                line += f"  —  {e['author']}"
            if e["project"]:
                line += f"  ·  _{e['project']}_"
            lines.append(line)

        lines.append("")

    return "\n".join(lines).strip()


# ─── Messaggio 2+: Post per componente (Claude) ───────────────────────────────

def call_claude(changelogs_data: list) -> dict:
    components_text = ""
    for item in changelogs_data:
        meta = item["meta"]
        entries = item["entries"]
        if not entries:
            continue

        component_name = meta.get("component") or item["filepath"].split("/")[1].title()
        figma_id = meta.get("figma_id", "").strip().strip('"')
        figma_url = f"{FIGMA_BASE_URL}{figma_id}" if figma_id else None

        components_text += f"\n### {component_name}\n"
        if figma_url:
            components_text += f"Link Figma: {figma_url}\n"
        components_text += "Modifiche:\n"
        for e in entries:
            line = f"- [{e['type']}] {e['description']}"
            if e["author"]:
                line += f" (di {e['author']})"
            if e["project"]:
                line += f" — progetto: {e['project']}"
            components_text += line + "\n"

    prompt = f"""Sei il comunicatore del Design System Antares. Scrivi in italiano.

Questa settimana sono stati aggiornati questi componenti:
{components_text}

Per ogni componente scrivi UN POST SLACK seguendo questo stile esatto:

ESEMPIO:
---
Ciao a tutti! 👋

Ho appena pubblicato un aggiornamento al componente *Button* — da adesso lo stato hover è molto più leggibile su sfondi chiari.

Questa modifica è arrivata perché diversi team ci avevano segnalato difficoltà nel distinguere lo stato hover su alcuni layout. Ho aumentato il contrasto e allineato tutto alle linee guida di accessibilità.

🔗 Componente su Figma: https://www.figma.com/file/xxx

⚠️ Ricordate di aggiornare le librerie nei vostri file di lavoro per ricevere questa modifica — qualsiasi file in cui usate il Button andrà refreshato.

Grazie, DS Team
---

REGOLE:
- Prima persona, tono caldo e diretto
- Inizia sempre con un saluto ("Ciao a tutti! 👋" o "Hey! 👋" o simile)
- Spiega il PERCHÉ della modifica — il problema che risolve, non solo cosa è cambiato
- Se il link Figma è disponibile includilo, altrimenti ometti la riga
- Includi SEMPRE il reminder di aggiornare le librerie con menzione dei file impattati
- Chiudi sempre con "Grazie, DS Team"
- In Slack grassetto = *asterischi*, corsivo = _underscore_
- Usa emoji con misura

Rispondi ESCLUSIVAMENTE con un oggetto JSON valido, senza testo prima o dopo:
{{
  "component_posts": [
    {{
      "component": "nome componente",
      "post": "testo completo del post Slack"
    }}
  ]
}}"""

    body = json.dumps({
        "model": CLAUDE_MODEL,
        "max_tokens": 3000,
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
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        return json.loads(raw)


# ─── Slack ────────────────────────────────────────────────────────────────────

def post_to_slack(text: str):
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


# ─── Main ─────────────────────────────────────────────────────────────────────

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

    changelogs_data = []
    for filepath in changed_files:
        if os.path.exists(filepath):
            content = open(filepath).read()
            entries = parse_entries(content)
            print(f"   📄 {filepath} → {len(entries)} entry trovate")
            if not entries:
                # Stampa le prime 20 righe per debug formato
                preview = "\n".join(content.splitlines()[:20])
                print(f"   ⚠️  Nessuna entry parsificata. Anteprima file:\n{preview}\n")
            changelogs_data.append({
                "filepath": filepath,
                "content": content,
                "meta": parse_frontmatter(content),
                "entries": entries,
            })
        else:
            print(f"⚠️  File non trovato: {filepath}")

    if not changelogs_data:
        print("❌ Nessun file leggibile. Esco.")
        return

    # Messaggio 1 — Report strutturato
    print("📤 Invio report strutturato su Slack...")
    post_to_slack(build_weekly_report(changelogs_data))
    print("   ✅ Report settimanale inviato")

    # Messaggi 2+ — Post per componente
    print(f"🤖 Chiamo Claude per i post per componente...")
    result = call_claude(changelogs_data)
    for item in result.get("component_posts", []):
        post_to_slack(item["post"])
        print(f"   ✅ Post inviato: {item['component']}")

    print("🏷️  Creo tag report...")
    tag = create_report_tag()
    print(f"   ✅ Tag creato: {tag}")
    print("🎉 Report completato.")


if __name__ == "__main__":
    main()
