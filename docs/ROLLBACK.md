# V8 — Rollback

Alle Aenderungen sind dateibasiert und lokal. Es gibt keine Migration, keine Datenbank und
keinen Dienst, der zurueckgesetzt werden muesste.

## Was V8 hinzugefuegt hat

| Datei | Art |
|---|---|
| `bin/skill-orchestrator.py` | neu (loest keinen V7-Bestand ab) |
| `bin/compare-v7-v8` | neu |
| `tests/test_orchestrator.py`, `tests/test_probe.py`, `tests/test_v8_execution.py` | neu im Repo |
| `docs/skill-orchestration-research.md`, `docs/V8-REPORT.md`, `docs/ROLLBACK.md` | neu |
| `skill/ctf-skill-index.SKILL.md` | V8-Fassung; V7-Original in `skill/ctf-skill-index.pre-v8.md` |
| `install-freebuff.sh` | V8-Installer |
| `~/.agents/skills/ctf-skill-index/SKILL.md` + `references/v8-orchestration.md` | Installation, mit `*.backup-<stamp>` |
| `.gitignore` | drei Eintraege fuer lokale V8-Artefakte |

**Nicht veraendert:** `bin/skill`, `bin/gen_skills`, `bin/doctor`, `bin/fetch`, `bin/push`,
`manifest.json`, `MANIFEST.yaml`, `INDEX.md`, `STATUS.md` (nur ergaenzt), `VERIFICATION.md`
(nur ergaenzt), `knowledge/`, `vendor/`, `venvs/`, `tools/`, `corpora/`.

## Rueckfall

### 1. Einzelne Dateien

Jede ersetzte Datei hat eine Sicherung mit Zeitstempel:

```bash
cd ~/ctf-skills
ls bin/*.backup-* ~/.agents/skills/ctf-skill-index/*.backup-* 2>/dev/null
cp -p bin/skill-orchestrator.py.backup-<stamp> bin/skill-orchestrator.py   # falls gewuenscht
cp -p ~/.agents/skills/ctf-skill-index/SKILL.md.backup-<stamp> \
      ~/.agents/skills/ctf-skill-index/SKILL.md
```

### 2. Vollstaendiger Stand vor V8

```bash
cd ~
tar xzf ~/ctf-skills/backups/pre-v8-20261121T225722Z.tar.gz -C ~/ctf-skills
# oder in ein leeres Pruefverzeichnis entpacken und vergleichen:
mkdir -p /tmp/v7-check && tar xzf ~/ctf-skills/backups/pre-v8-*.tar.gz -C /tmp/v7-check
```

Das Archiv enthaelt den gesamten versionierten Bestand inklusive `bin/skill`, `manifest.json`,
`knowledge/`, `skill/` und `corpora/` — ohne `vendor/`, `venvs/`, `tools/`, `logs/`.

### 3. Freebuff-Skill

- Account-Skill: in den Freebuff-Einstellungen die vorherige Fassung wiederherstellen
  (Inhalt von `skill/ctf-skill-index.pre-v8.md`).
- Dateiinstallation: `~/.agents/skills/ctf-skill-index/` loeschen oder aus dem Backup ersetzen.
- Sitzung neu starten, damit die Skill-Discovery die Aenderung sieht.

### 4. Wirkung des Rollbacks

Nach dem Rollback ist der Zustand von V7 wiederhergestellt: `bin/skill` funktioniert unveraendert,
der Katalog ist unberuehrt, es laufen keine Dienste. Der Orchestrator ist optional und wird von
keinem V7-Pfad aufgerufen.

## Pruefung nach dem Rollback

```bash
cd ~/ctf-skills
python3 -m unittest discover -s tests        # nur relevant, wenn tests/ bleibt
bin/skill list --layer=L2 | head
python3 bin/doctor                            # V7-Messung, unveraendert
```
