#!/bin/bash
# Installiert die geprueften V8-Komponenten; V7 bleibt erhalten.
# Dry-Run ist Standard. Schreibt nur nach Pruefung der Quellen.
set -euo pipefail
PATCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${SFS_CTF_SKILLS_ROOT:-$PATCH_DIR}"
TARGET="${FREEBUFF_SKILL_DIR:-$HOME/.agents/skills/ctf-skill-index}"
V8_PROJECT_TARGET="$ROOT/.agents/skills/ctf-skill-index-v8"
V8_SKILL_SOURCE="$PATCH_DIR/.agents/skills/ctf-skill-index-v8/SKILL.md"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

if [[ ! -f "$ROOT/manifest.json" ]]; then
  echo "ERROR: manifest.json fehlt in $ROOT. Keine Aenderung." >&2
  exit 2
fi
if [[ ! -f "$PATCH_DIR/bin/skill-orchestrator.py" ]]; then
  echo "ERROR: Orchestrator fehlt im Patch-Verzeichnis. Keine Aenderung." >&2
  exit 2
fi

if [[ ! -f "$V8_SKILL_SOURCE" ]]; then
  echo "ERROR: projektlokaler V8-Skill fehlt: $V8_SKILL_SOURCE" >&2
  exit 2
fi

printf 'Patch     : %s\nKatalog   : %s\nOrchestr. : %s\nSkill     : %s\n' \
  "$PATCH_DIR" "$ROOT" "$ROOT/bin/skill-orchestrator.py" "$TARGET/SKILL.md"
echo "Backups   : <datei>.backup-$STAMP"

if [[ "${1:-}" != "--apply" ]]; then
  echo "DRY RUN. Keine Schreibvorgaenge. Nach Review: --apply"
  exit 0
fi

# 1. Quellen syntaktisch pruefen, bevor irgendetwas installiert wird.
python3 -m py_compile "$PATCH_DIR/bin/skill-orchestrator.py"
"$PATCH_DIR/bin/skill-orchestrator.py" selfcheck --root "$ROOT" >/dev/null

# 2. Bestehende Dateien sichern (kein Ueberschreiben ohne Backup).
for dest in "$ROOT/bin/skill-orchestrator.py" "$ROOT/bin/compare-v7-v8" \
            "$TARGET/SKILL.md" "$TARGET/references/v8-orchestration.md" \
            "$V8_PROJECT_TARGET/SKILL.md"; do
  if [[ -f "$dest" ]]; then
    cp -p "$dest" "$dest.backup-$STAMP"
  fi
done

# 3. Komponenten installieren. Liegt Patch == Katalog (In-Place-Betrieb),
#    wird dieselbe Datei nicht kopiert, sondern nur der Modus gesetzt.
put() {
  local src="$1" dst="$2" mode="$3"
  if [[ "$(readlink -f "$src")" == "$(readlink -f "$dst")" ]]; then
    chmod "$mode" "$dst"
  else
    install -m "$mode" "$src" "$dst"
  fi
}
mkdir -p "$ROOT/bin" "$ROOT/docs" "$ROOT/tests" "$TARGET/references" "$V8_PROJECT_TARGET"
put "$PATCH_DIR/bin/skill-orchestrator.py" "$ROOT/bin/skill-orchestrator.py" 755
put "$PATCH_DIR/bin/compare-v7-v8" "$ROOT/bin/compare-v7-v8" 755
put "$PATCH_DIR/tests/test_orchestrator.py" "$ROOT/tests/test_orchestrator.py" 644
put "$PATCH_DIR/tests/test_probe.py" "$ROOT/tests/test_probe.py" 644
put "$PATCH_DIR/tests/test_v8_execution.py" "$ROOT/tests/test_v8_execution.py" 644
put "$PATCH_DIR/docs/skill-orchestration-research.md" \
  "$ROOT/docs/skill-orchestration-research.md" 644

# 4. Skill: V8-Dokument als Referenz, V7-Datei bleibt inhaltlich erhalten.
put "$PATCH_DIR/skill/ctf-skill-index.SKILL.md" "$TARGET/references/v8-orchestration.md" 644
# Eindeutiger V8-Name: projektlokal, ohne den gebuendelten Account-/V7-Skill zu ersetzen.
put "$V8_SKILL_SOURCE" "$V8_PROJECT_TARGET/SKILL.md" 644
if [[ "$(sed -n '2p' "$V8_PROJECT_TARGET/SKILL.md")" != "name: ctf-skill-index-v8" ]]; then
  echo "ERROR: V8-Frontmatter passt nicht zum Skill-Verzeichnis." >&2
  exit 2
fi
if [[ ! -s "$TARGET/SKILL.md" ]]; then
  put "$PATCH_DIR/skill/ctf-skill-index.SKILL.md" "$TARGET/SKILL.md" 644
else
  cp -p "$TARGET/SKILL.md" "$TARGET/SKILL.md.pre-v8-$STAMP"
  python3 - "$TARGET/SKILL.md" "$PATCH_DIR/skill/ctf-skill-index.SKILL.md" <<'PY'
from pathlib import Path
import sys
target, v8 = Path(sys.argv[1]), Path(sys.argv[2])
body = target.read_text(encoding="utf-8")
bridge = """
<!-- SFS-V8-ORCHESTRATION-BEGIN -->
## V8: ausfuehrender Orchestrator (alle V7-Regeln bleiben gueltig)

Vor jeder materiellen Analyse:

```bash
python3 "$HOME/ctf-skills/bin/skill-orchestrator.py" route --task "<aktuelle Aufgabe>"
python3 "$HOME/ctf-skills/bin/skill-orchestrator.py" run \\
  --task "<aktuelle Aufgabe>" --target <datei.sol> [--project <dir>] [--contract <Name>] \\
  --out <evidenzverzeichnis> --allow-exec
python3 "$HOME/ctf-skills/bin/skill-orchestrator.py" verify \\
  --report <evidenzverzeichnis>/evidence-report.json
```

`route` ist eine Empfehlung. `run` fuehrt die Adapter wirklich aus und schreibt Receipts.
`verify` prueft Inhalte (Assertion im Testrumpf, Negativkontrolle, State-Delta), nicht nur Hashes.
Vollstaendige Anleitung: `references/v8-orchestration.md` dieses Skills.
<!-- SFS-V8-ORCHESTRATION-END -->
"""
marker_begin = "<!-- SFS-V8-ORCHESTRATION-BEGIN -->"
marker_end = "<!-- SFS-V8-ORCHESTRATION-END -->"
if marker_begin in body:
    start = body.index(marker_begin)
    end = body.index(marker_end) + len(marker_end)
    body = body[:start].rstrip() + "\n" + body[end:].lstrip()
body = body.rstrip() + "\n" + bridge
target.write_text(body, encoding="utf-8")
print(f"V7-Inhalt erhalten, V8-Bruecke ergaenzt: {target}")
PY
fi

# 5. Nachweis: Tests und Selbsttest laufen, ohne externe Werkzeuge zu starten.
( cd "$PATCH_DIR" && python3 -m unittest discover -s tests >/dev/null )
echo "INSTALLED: eindeutiger projektlokaler V8-Skill, V7 erhalten. Tests gruen. Neue Freebuff-Sitzung fuer Runtime-Abnahme erforderlich."
