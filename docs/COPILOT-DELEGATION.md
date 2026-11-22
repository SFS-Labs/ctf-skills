# Copilot-Delegation - Freebuff fuehrt, Copilot arbeitet begrenzt

**Status: `IMPLEMENTED` · `LOCALLY_TESTED` · `MOCK_VERIFIED` ·
`RUNTIME_VERIFIED` (nur AGENTS.md-Ladepfad) · `LIVE_DELEGATION_BLOCKED`.** Es gab
noch keine echte Copilot-Delegation. Alle Ablaeufe in diesem Dokument liefen
gegen simulierte GitHub-Antworten; echte Lesezugriffe sind als solche
gekennzeichnet. Damit ist die Integration nachgewiesen, nicht ein
Copilot-Beitrag. `PRODUCTION_VERIFIED` ist nicht erreicht.

## Integration

- **Branch:** `v9/copilot-delegation-integration`, Basis `main` `ff27da99`
- **Commits:** `3d15920` (V8 + V9 + V7-Katalog), `deac305` (Worktree-Push-Fix)
- **Draft-PR:** [#6](https://github.com/SFS-Labs/ctf-skill-factory/pull/6)
- **Tests:** 84 Tests, 1 Skip; `selftest` 8/8, `real_api_calls=0`,
  `paid_spend=0`; `selfcheck` OK; `bin/push --check` MATCH
- **AGENTS.md:** Der Orchestrator laedt die Datei beim Session-Start ueber
  `deriveKnowledgeFiles` als Projektanweisung. Eine neue Sitzung wurde nicht
  automatisiert gestartet; die Modellaktivierung ist nicht erzwungen.
- **PR-Erstellung:** Der PAT darf keine PR-API (403); die verbundene
  SFS-Labs-GitHub-App hat den Draft-PR erstellt. Kein Merge.

## Warum

Freebuff bleibt die einzige Oberflaeche. Copilot uebernimmt nur klar abgegrenzte,
unabhaengig pruefbare Teilaufgaben. Der Standard liegt in
`docs/COPILOT_PROFICIENCY_OPERATING_STANDARD.md` (verbatim) plus
`docs/COPILOT-PROFICIENCY-STANDARD.md` (lokale Betriebsergaenzung); das
Trigger-Verhalten in `AGENTS.md`.

## Architektur

```
Freebuff (Orchestrator)
  bin/skill-orchestrator.py copilot ...        # ein Einstiegspunkt
  bin/copilot-delegate.py                      # Delegationsschicht
    standard   -> Remote-Standard oder hashgepruefte vendorte Fassung
    preflight  -> nur Lesen: Auth, Repo, Actor, Routen, Gate
    detect     -> Brief mit Ziel, Pfaden, Abnahme, Tests, Grenzen
    delegate   -> Issue + GraphQL-Assignment oder Agent Task (dry-run default)
    watch      -> Issue/Task, PR, Head-SHA, CI, Quota, Timeout
    review     -> Diff, Scope, Secret-Scan, CI, optional lokale Tests
    proficiency-> ausschliesslich echte, belegte Aktivitaet
    demo/selftest -> kompletter Lebenszyklus gegen lokalen Mock
```

Zustaende:

```
PLANNED -> DELEGATED -> QUEUED/IN_PROGRESS -> PR_OPENED -> CI_PENDING
        -> COMPLETED -> REVIEWED
Fehler: BLOCKED_PAID_GATE, BLOCKED_ROUTE, FAILED, QUOTA_BLOCKED, TIMED_OUT,
        CANCELLED, WATCH_ERROR, WATCH_LIMIT_REACHED, CHANGES_REQUIRED
```

`COMPLETED` heisst: Copilot hat einen PR mit bestandener CI geliefert. Es heisst
nicht: mergerfolgreich oder sicher. Erst `REVIEWED`/`VERIFIED` ist die
unabhaengige Freigabe; der Merge bleibt menschlich.

## Kommandos

```bash
# 1. Nur Lesen: Auth, Rechte, Copilot-Actor, Routen, Standard, Gate
python3 bin/copilot-delegate.py preflight --repo SFS-Labs/ctf-skill-factory

# 2. Teilaufgabe erkennen und Brief schreiben
python3 bin/copilot-delegate.py detect \
  --task "Add a bounded fix in src/fix.py and a regression test." \
  --path src/fix.py --out .copilot/brief.json

# 3. Standardfall: kein Schreibzugriff
python3 bin/copilot-delegate.py delegate --brief .copilot/brief.json

# 4. Spaeter, nur mit geoeffnetem Gate und vorhandenem Guthaben
python3 bin/copilot-delegate.py policy --credits-restored --allow-paid
python3 bin/copilot-delegate.py delegate --brief .copilot/brief.json \
  --execute --allow-paid --route issue

# 5. Beobachten und unabhaengig pruefen
python3 bin/copilot-delegate.py watch --id <delegation-id> --follow
python3 bin/copilot-delegate.py review --id <delegation-id> \
  --local-repo . --test-profile python-unittest

# 6. Evidenz (Simulationen werden ausgeschlossen)
python3 bin/copilot-delegate.py proficiency --markdown
```

Der Orchestrator reicht dieselben Argumente durch:

```bash
python3 bin/skill-orchestrator.py copilot preflight
```

## Routen

| Route | Aufruf | Voraussetzung |
|---|---|---|
| Issue (primaer) | `POST /repos/{owner}/{repo}/issues`, dann GraphQL `replaceActorsForAssignable` mit der Bot-ID aus `suggestedActors` | Issues aktiviert, Issues-API-Schreibrecht, `copilot-swe-agent` assignbar |
| Agent Task (alternativ) | `POST /agents/repos/{owner}/{repo}/tasks` mit `prompt`, `base_ref`, `create_pull_request` | Agent-Tasks-Repo-Recht (Read/Write), Copilot-Plan des Accounts |

Die Bot-ID wird nie geraten: `preflight` liest sie aus
`repository.suggestedActors(capabilities:[CAN_BE_ASSIGNED])`. Fehlt sie, ist die
Issue-Route blockiert.

## Kontingent-Gate

`delegate` schreibt standardmaessig nichts. Ein kostenpflichtiger Aufruf braucht
**beides**:

1. lokale Policy: `paid_delegation_allowed=true` **und** `credits_exhausted=false`;
2. `--execute --allow-paid` auf der Kommandozeile.

Die Policy liegt in `.copilot/policy.json` (nicht versioniert). `policy
--credits-restored --allow-paid` oeffnet sie; `--forbid-paid` und
`--credits-exhausted` schliessen sie wieder. Ein fehlendes Gate erzeugt einen
Audit-Datensatz `BLOCKED_PAID_GATE` und sendet keinen Schreibzugriff.

Aktuell gilt: Credits aufgebraucht, Gate zu. Es werden nur kostenlose
Lesezugriffe und der lokale Mock genutzt.

## Beobachtung

`watch` liest:

- Issue-Zustand, Assignees, Timeline (`copilot_work_started`,
  `cross-referenced`), Bot-Kommentare;
- Agent-Task-Zustand, Sessions, Fehler, Usage, Artefakte (`pull`, `branch`);
- PR: Autor, Draft, Basis, Head-Ref, Head-SHA, Diff-Umfang;
- CI: Check-Runs und Combined Status fuer genau diesen Head-SHA.

Quota-Erkennung: Bot-Kommentar oder Task-Fehler mit
`insufficient|exhausted ... credits` fuehrt zu `QUOTA_BLOCKED` (terminal), nicht
zu Erfolg. Ein lokales Poll-Budget endet in `WATCH_LIMIT_REACHED` und ist
wiederholbar; ein echtes Agent-Task-`timed_out` in `TIMED_OUT`.

## Review

`review` prueft unabhaengig:

- Autor ist `copilot-swe-agent[bot]` (oder Committer-Nachweis),
- Basis-Branch entspricht dem Brief,
- Head-SHA des Reviews entspricht dem PR; CI gilt nur fuer diesen SHA,
- alle Dateien liegen in den erlaubten Pfaden; Workflows, `.git`, `vendor/`,
  `venvs/`, `tools/`, `backups/`, Secrets-Dateien sind tabu,
- Secret-Muster in hinzugefuegten Zeilen,
- Diff-Groesse,
- CI Erfolg; ohne CI hoechstens `VERIFIED_LOCAL`,
- optional: Diff in einen temporaeren Git-Worktree anwenden und ein fest
  konfiguriertes Testprofil ausfuehren (`python-unittest`, `python-pytest`,
  `node-test`, `custom` mit argv-Liste, kein Shell-String).

Ergebnis: `VERIFIED`, `VERIFIED_LOCAL`, `UNVERIFIED` oder `CHANGES_REQUIRED` mit
konkreten `next_actions`. Der Receipt enthaelt den kompakten Evidenzblock des
Standards (`Copilot evidence`, `Skill areas`, `Proof`, `Uncovered`, `Decision`);
er wird nicht automatisch als PR-Kommentar gepostet. Es gibt keinen Merge-Aufruf
im Code.

## Gemessener Preflight (echte Lesezugriffe)

Stand 2026-11-22, Account `SFS-Labs`:

| Pruefung | Ergebnis |
|---|---|
| `GET /user` | 200, `login=SFS-Labs` |
| `GET /repos/SFS-Labs/ctf-skill-factory` | 200, privat, `has_issues=false`, `permissions.admin=true` |
| `suggestedActors` | `copilot-swe-agent` (`BOT_kgDOC9w8XQ`) auf beiden geprueften Repos |
| `GET /agents/tasks` | 200, leer (User-Scope lesbar) |
| `GET /agents/repos/SFS-Labs/ai-knowledge-ops-lab/tasks` | 403, `user does not have read access` (Fine-grained-Token ohne Agent-Tasks-Recht) |
| `GET /repos/SFS-Labs/ctf-skill-factory/issues` | 403, `Resource not accessible by personal access token` |
| `SFS-Labs/sfs-ai-development-gateway` | PAT `404`; verbundene GitHub-App `200`; Standard verbatim vendored (Blob `277ad8a`, SHA-256 `b8d0548`) |
| Credits | laut Nutzer aufgebraucht; Policy `credits_exhausted=true` |

Folge: **keine Route ist derzeit schreibfaehig.** Die Issue-Route scheitert an
deaktivierten Issues und fehlendem Issues-Recht; die Agent-Tasks-Route am
fehlenden Repo-Recht. Das ist ein Rechte-/Kontingent-Blocker, kein Codefehler.
Der Code behandelt ihn als `BLOCKED_ROUTE` und macht keinen Schreibversuch.

## Verifikation (lokal)

```bash
python3 -m py_compile bin/copilot-delegate.py
python3 bin/copilot-delegate.py selftest
python3 -m unittest discover -s tests -p 'test_copilot_delegation.py'
```

`selftest` startet fuer jedes Szenario einen lokalen HTTP-Server mit simulierten
GitHub-Antworten und fuehrt den echten Client, die echte Zustandsmaschine und das
echte Review aus:

| Szenario | Erwartung | Ergebnis |
|---|---|---|
| happy (Issue) | `REVIEWED` / `VERIFIED` | bestanden |
| agent-task | `REVIEWED` / `VERIFIED` | bestanden |
| rate-limit | Retry, dann `REVIEWED` / `VERIFIED` | bestanden |
| ci-failure | `CHANGES_REQUIRED` (CI) | bestanden |
| scope-violation | `CHANGES_REQUIRED` (Workflow-Datei) | bestanden |
| secret | `CHANGES_REQUIRED` (Secret im Diff) | bestanden |
| quota | `QUOTA_BLOCKED` | bestanden |
| timeout | `WATCH_LIMIT_REACHED` | bestanden |

Alle Szenarien: `paid_spend=0`, `real_api_calls=0`. Die Proficiency-Ausgabe
meldet fuer Simulationen `proven_domains=0` und `simulated_excluded>0`.

## Grenzen

- Keine echte Delegation getestet; Credits und Token-Rechte fehlen.
- Der Fine-grained-PAT kann das private Gateway nicht lesen (`404`) und keine
  Pull-Requests lesen/schreiben (`403`). Der Draft-PR wurde ueber die verbundene
  GitHub-App erstellt; der Push lief ueber `bin/push`.
- Der Standard
  wurde ueber die verbundene GitHub-App abgerufen, verbatim vendored und per
  Blob-/SHA-256 geprueft; das CLI nutzt diese Fassung und weist den PAT-Status
  separat aus.
- GitHub liefert keinen Nachweis ueber im Agenten tatsaechlich genutzte
  MCP-/CLI-Tools. `agent-configuration` und `tool-context-integration` bleiben
  daher ohne expliziten Zusatznachweis `UNPROVEN`; es wird nichts erfunden.
- Der Review-Merge bleibt menschlich. Kein Auto-Merge, keine Veroeffentlichung.
