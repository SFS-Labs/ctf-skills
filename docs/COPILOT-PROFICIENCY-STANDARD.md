# Lokale Betriebsergaenzung zum SFS-Labs Copilot Proficiency Standard

Der verbindliche Text liegt **verbatim** in
[`docs/COPILOT_PROFICIENCY_OPERATING_STANDARD.md`](COPILOT_PROFICIENCY_OPERATING_STANDARD.md).
Diese Datei ist nur die Freebuff-Implementierungsnotiz; bei Widerspruch gilt der
Standard.

## Herkunft

| Feld | Wert |
|---|---|
| Repository | `SFS-Labs/sfs-ai-development-gateway` (privat) |
| Pfad / Ref | `docs/COPILOT_PROFICIENCY_OPERATING_STANDARD.md` @ `main` |
| Blob-SHA | `277ad8a4d45043b2fc6c9b463aa0d989596e976e` |
| SHA-256 des Inhalts | `b8d05485661c3dd3e349939096846b18e698fa12dec9d35321769a2b336c8b2c` |
| Abruf | 2026-11-22 ueber die verbundene GitHub-App; der Fine-grained-PAT des CLIs erhaelt weiterhin `404` |
| Begleitnachweis | `docs/COPILOT_PROFICIENCY_OPERATING_STANDARD.provenance.json` |

Der Preflight markiert die Quelle deshalb als `local-vendored` und nennt den
PAT-Status `404` separat. Es wird nicht behauptet, das CLI selbst koenne das
private Gateway lesen.

## Umsetzung in Freebuff

Freebuff bleibt die einzige Oberflaeche und der fuehrende Orchestrator. Copilot
ist ein optionaler Executor fuer klar abgegrenzte, unabhaengig pruefbare Aufgaben.

- **Trigger:** `AGENTS.md`; bei jeder GitHub-/SFS-Labs-Aufgabe automatisch
  Standard, `preflight`, `detect`, Gate und Review anwenden.
- **Fuenf Bereiche:** AI Collaboration, Prompting, Code Generation & Validation,
  Agent Configuration, Tool & Context Integration. Es wird kein Level und kein
  Punktwert behauptet.
- **Delegation:** bevorzugt Issue an `copilot-swe-agent[bot]`; Agent Tasks API nur
  als Alternative bei nachgewiesenem Recht. Keine kuenstlichen Aufgaben.
- **Kontingent:** `paid_delegation_allowed=false` und `credits_exhausted=true` sind
  der Standard. Kostenpflichtig wird nur mit lokaler Policy-Freigabe **und**
  `--execute --allow-paid`; aktuell bleibt das Gate zu.
- **Evidenz:** Assignment allein zaehlt nicht. Noetig sind beobachtete
  Copilot-Aktivitaet, Copilot-PR, exakter Head-SHA, CI und ein unabhaengiges
  Review. Simulationen werden ausgeschlossen; GitHub bleibt die Autoritaet fuer
  das Proficiency-Level.
- **Grenzen:** Kein Auto-Merge, kein Deployment/Publish, keine Live-Transaktion,
  keine Secrets, keine Repo-Administration. Der Mensch entscheidet ueber Merge.

Ausfuehrung und Nachweise: `bin/copilot-delegate.py`,
`docs/COPILOT-DELEGATION.md`, `VERIFICATION.md`.

## Nachweisstand (2026-11-22)

`IMPLEMENTED` · `LOCALLY_TESTED` · `MOCK_VERIFIED` · `RUNTIME_VERIFIED` (nur
AGENTS.md-Ladepfad) · `LIVE_DELEGATION_BLOCKED`. Der Integrationsbranch
`v9/copilot-delegation-integration` basiert auf `main` `ff27da99`; Draft-PR
[#6](https://github.com/SFS-Labs/ctf-skill-factory/pull/6). 84 Tests (1 Skip),
8/8 Mock-Szenarien, `real_api_calls=0`, `paid_spend=0`. Es gibt keine belegte
Copilot-Aktivitaet und kein Proficiency-Level; `PRODUCTION_VERIFIED` ist nicht
erreicht.
