# SFS | CTF Skill Index V8 — Abschlussbericht

Stand: 2026-11-22 (UTC) · Node: sfs-linux-node (Linux, x86_64, 4 CPU, 7,8 GiB RAM)
Ausgangsbasis: V7-Skill-Fabrik in `~/ctf-skills` (133 Skills, 134 Quellen, 1 Alias)
Eingabepaket: `SFS_CTF_SKILL_INDEX_V8_FULL_PACKAGE.json` (`SFS-FULL-PACKAGE-JSON-v1`)

**Gesamtstatus: `PARTIAL_ACCEPTED`.** Alle lokalen technischen Abnahmen sind bestanden.
Punkt 10/11 der Definition of Done (erzwungene Freebuff-Runtime-Aktivierung + Trace) sind
`BLOCKED`: dieser Freebuff-Build ist eine kompilierte Desktop-Anwendung ohne CLI-/SDK-Hook und
ohne Trace-Ausgabe. Diese Lücke wird nicht als bestanden ausgegeben.

---

## 1. Integritaetspruefung des Pakets

| Pruefung | Ergebnis |
|---|---|
| JSON parsebar, Format `SFS-FULL-PACKAGE-JSON-v1` | PASS |
| `entry_count` / `file_count` / `directory_count` | 7 / 7 / 0, konsistent mit `entries` |
| Base64-Dekodierung je Eintrag (`validate=True`) | 7/7 PASS |
| Groesse je Eintrag gegen `size_bytes` | 7/7 PASS |
| SHA-256 je Eintrag gegen `sha256` | 7/7 PASS |
| UTF-8-`content` bytegleich zu `content_base64` | 7/7 PASS |
| Eingebettetes Original-ZIP: 21.312 Bytes, `testzip()` sauber | PASS |
| ZIP-SHA-256 = `c476e3720fed3ffbf8b857b0219d14a3f2afede0732397d5de876b7e317fced8` | PASS |
| Jeder ZIP-Member bytegleich zum JSON-Eintrag | 7/7 PASS |
| Kein ZIP-Member ohne JSON-Eintrag | PASS |
| Rekonstruktion in isoliertem `.v8_staging/` (kein `..`, kein absoluter Pfad, kein Overwrite) | PASS |
| Python-Syntax (`py_compile`) und Shell-Syntax (`bash -n`) | PASS |

Rekonstruierte Dateien: `bin/skill-orchestrator.py`, `.agents/skills/ctf-skill-index/SKILL.md`,
`README.md`, `docs/skill-orchestration-research.md`, `install-freebuff.sh`,
`tests/test_orchestrator.py`, `tests/test_probe.py`.

## 2. Ausgangszustand und Erhalt von V7

- V7-Bestand aufgenommen: `manifest.json` (133 Slugs), `MANIFEST.yaml`, `INDEX.md`, `STATUS.md`,
  `VERIFICATION.md`, `bin/skill`, `bin/gen_skills`, `bin/doctor`, `knowledge/` (133 Karten),
  `corpora/verify`, `vendor/`, `venvs/`, `tools/`.
- Backup vor jeder Aenderung: `backups/pre-v8-20261121T225722Z.tar.gz` (787 KB, ohne vendor/venvs/tools).
- `bin/skill` (V7-Router), `bin/gen_skills`, `bin/doctor`, `manifest.json`, `INDEX.md`, `STATUS.md`
  wurden **nicht** veraendert. V7-Regeln (sieben Regeln, L0-L9-Menue) stehen unveraendert im Skill.
- V7-Skilldefinition gesichert: `skill/ctf-skill-index.pre-v8.md` (8.818 Bytes, Original).
- Repo-Stand und GitHub konnten nicht verglichen werden: `git` ist nicht im `PATH`
  (gebuendelte Binary `/opt/Freebuff/resources/git/bin/git` vorhanden), der hinterlegte Token ist
  laut `STATUS.md` ungueltig (401). Es wurde nichts gepusht.

## 3. Implementierte Architektur

`bin/skill-orchestrator.py` (ein Einstiegspunkt, keine neuen Abhaengigkeiten):

| Baustein | Funktion |
|---|---|
| Discovery | `manifest.json` + `knowledge/<slug>/SKILL.md` (gekappt auf 4.000 Zeichen) + `pairs_with` + `blind_spots` + realer Binary-Status |
| Selection | BM25-artige Relevanz, Capability-Boost, Betriebsstatus-Gewicht (`binary`/`bibliothek`/`referenz`/`wissen`), Ausfuehrbarkeits-Bonus, Schichtvielfalt; `--pick` nimmt die Modellauswahl auf und validiert sie |
| Domaenengate | Solana/Move/Cairo/Algorand/Stellar → `NO_MATCH` fuer EVM-Ausfuehrung, aber `domain_candidates` als Wissensrouting mit `status_detail` |
| Composition | Schritte mit ID, Eingaben, Abhaengigkeiten, Adapter, Verfuegbarkeit, Akzeptanzkriterium, `on_failure` |
| Adapter | 13 feste Adapter (surya, slither, slither-solc, myth, solc, forge, forge-match, echidna, echidna-solc, medusa, evmasm, diffusc, cryo) |
| Execution | `shell=False`, Platzhalter nur aus festem Namensraum, Options-Injektion und `..` abgelehnt, Timeout, `killpg`, Log-Kappung (200k), Receipt mit Version/Zeit/Exit/Artefakt-Hash |
| Erfolgsvertrag | Adapter definieren `ok_exit` und JSON-Vertrag: `slither` 255 = Befund, `echidna` 1 = falsifiziert, aber nur mit parsebarer JSON-Ausgabe |
| Adaptation | Verfuegbarkeits-Fallback, Compiler-Diagnose (`-solc`-Variante), Counterexample-Fallback, Widerspruchserkennung, dokumentierter Blocker |
| Verification | Inhaltspruefung: Slither-/Mythril-Schema, forge-Teststatus, Assertion im Testrumpf, Zustandsbeobachtung, Negativkontrolle, State-Delta-Arithmetik, Claim-Abgleich |
| Zustandsmaschine | `DISCOVERED · SELECTED · READY · INVOKED · COMPLETED · FAILED · UNAVAILABLE · VERIFIED · BLOCKED` + `KNOWLEDGE_ONLY` |

## 4. Tests

| Lauf | Ergebnis |
|---|---|
| Prototyp-Baseline vor Aenderung (16 Tests) | 16/16 OK |
| Gesamtsuite danach (16 unveraendert + 33 neue) | **49/49 OK** |
| Mit `SFS_V8_REAL=1` (inkl. echtem Korpuslauf) | **49/49 OK**, kein Skip |
| `selfcheck` (Katalog, Adapter, Negativproben) | 133 Eintraege, alle Adapter verfuegbar, gefaelschte Evidenz → `INVALID` |

Abgedeckte Negativfaelle: fehlende Datei, Hash-Mismatch, `success:false` bei Slither,
Counterexample ohne Assertion im Quellrumpf, fehlende Negativkontrolle, widerspruechlicher
Teststatus, erfundenes Detektor-Claim, Options-Injektion, Pfad-Traversal, Timeout,
fehlende Projektangabe, Ressourcenreserve.

## 5. Reale Werkzeugausfuehrung (Hauptlauf)

Auftrag: *"Audit the Solidity Vault: withdraw reentrancy and unchecked low-level call; prove
locally with a counterexample"* · Ziel `corpora/verify/Vulnerable.sol` · Projekt `corpora/verify`.

| Schritt | Adapter | Status | Exit | Dauer | Version |
|---|---|---|---|---|---|
| MAP | `surya describe` | COMPLETED | 0 | 0,78 s | 0.4.13 |
| STATIC | `slither --json` | COMPLETED | 255 | 0,85 s | 0.11.6 |
| COUNTEREXAMPLE | `forge test --json` | COMPLETED | 0 | 0,08 s | 1.10.0 |
| NEGATIVE_CONTROL | `forge test --json --match-test test_invariant_holds_initially` | COMPLETED | 0 | 0,05 s | 1.10.0 |

Ergebnis: 10 Detektoren, darunter `reentrancy-eth`, `tx-origin`, `arbitrary-send-eth`,
`unchecked-lowlevel`. Drei ausfuehrbare Counterexample-Tests bestehen
(`test_reentrancy_drains_vault`, `test_sweep_breaks_solvency`,
`test_aggregate_invariant_blind_to_reentrancy`), die Negativkontrolle
(`test_invariant_holds_initially`) besteht ebenfalls. Verdict: **`VERIFIED_LOCAL`**,
unabhaengige Methoden `static:slither` + `dynamic:forge`. Wandzeit gesamt 2,9 s.
Der unabhaengige `verify`-Lauf ueber `evidence-report.json` bestaetigt dasselbe Ergebnis.

Wichtig: Der Exit-Code 255 von Slither ist ein **Befund**, kein Ausfall. Genau diese Verwechslung
verhindert der Adapter-Vertrag.

## 6. Adaptive Recovery (real, nicht behauptet)

Umgebung: `forge` aus dem `PATH` entfernt (nur diese Binary verborgen).

| Schritt | Adapter | Status | Exit | Dauer |
|---|---|---|---|---|
| MAP | surya | COMPLETED | 0 | 0,50 s |
| STATIC | slither | FAILED | 1 | 0,46 s |
| STATIC_SOLC | slither `--compile-force-framework solc` | COMPLETED | 255 | 0,99 s |
| COUNTEREXAMPLE_FALLBACK | echidna | FAILED | 1 | 0,27 s |
| COUNTEREXAMPLE_FALLBACK_SOLC | echidna `--crytic-args "--compile-force-framework solc"` | COMPLETED | 0 | 2,97 s |

Entscheidungen im Receipt: *"Compiler-/Framework-Fehler im Log erkannt → Compiler-Annahme
isolieren statt blind wiederholen"*, danach *"alternativen Adapter einsetzen"*.
Ergebnis: 12 statische Befunde (inkl. `reentrancy-eth`), Echidna fuzzt 9 Assertions ohne
Falsifikation → Verdict **`STRUCTURAL_ONLY`**, Status `COMPLETED_UNVERIFIED`. Das ist korrekt:
ein statischer Treffer ohne Reproduktion ist kein Beweis.

**Nebenbefund (wichtig fuer Unabhaengigkeit):** Slither und Echidna scheitern beide, weil
`crytic-compile` fuer dieses Foundry-Projekt `forge` aufruft. Zwei Scanner mit demselben
Compiler-Stack sind **keine** methodisch unabhaengigen Signale. Der Orchestrator behandelt sie
deshalb nicht als zwei Beweise.

## 7. V7/V8-Vergleich (reproduzierbar)

`bin/compare-v7-v8` ueber acht feste Faelle (5 EVM, 2 Fremd-VM, 1 sachfremd), Soll je Fall
handgesetzt. Gemessen:

| Metrik | V7 (`bin/skill plan`) | V8 (`route`) |
|---|---|---|
| mittlere Precision | 0,224 | **0,586** |
| mittlere Recall | 0,893 | **1,000** |
| durchschnittlich gewaehlte Skills | 11,75 | **5,38** |
| Fehlaktivierung bei sachfremder Aufgabe | **ja** (8 Skills) | **nein** (0) |

Rohdaten: `logs/compare-v7-v8-<stamp>.json`. Einschraenkung: gemessen wird die
**Auswahlqualitaet** gegen ein handgesetztes Soll, nicht die Zahl geloester Audits. Ein
Outcome-Vergleich ueber mehrere echte Ziele wurde nicht durchgefuehrt (`PARTIAL`).

## 8. Ressourcenverbrauch

| Groesse | gemessen |
|---|---|
| MemAvailable waehrend des Laufs | 3.328 MB von 7.813 MB |
| Swap | 15 GiB, 3,1 GiB belegt (Bestand) |
| Freier Datentraeger | 66,5 GB |
| CPU | 4 Kerne, Last ~2,1 |
| Ausfuehrung | strikt sequenziell, max. 1 Werkzeug gleichzeitig |
| Groesstes Einzelartefakt | `slither.json` 79 KB (Logs gekappt auf 200k Zeichen) |

Keine Dienste gestartet, keine Systemaenderung, keine Netzwerkoperation, keine Transaktion.

## 9. Bekannte Einschraenkungen / Blocker

1. **Freebuff-Runtime (BLOCKED).** `/usr/bin/freebuff` ist ein kompiliertes Desktop-ELF ohne
   CLI-Unterbefehle (Aufruf liefert nur `path-repair`/`linux-launch`). Es gibt keinen
   Tool-Call-Hook und keine `trace.jsonl`-Ausgabe in dieser Installation
   (`~/.freebuff`, `~/.codebuff` existieren nicht). Die Aktivierung ist damit
   **modellvermittelt** ueber die Skill-Beschreibung, nicht erzwungen. Installiert wurden:
   `~/.agents/skills/ctf-skill-index/SKILL.md` + `references/v8-orchestration.md` (mit Backup)
   sowie die Account-Skill-Definition. Ein Trace-Nachweis im Sinne von `CODEBUFF_TRACE=1`
   ist in diesem Build nicht erzeugbar.
2. **V7/V8-Outcome-Vergleich (PARTIAL).** Nur Routing-Qualitaet plus ein realer Korpuslauf;
   keine Serie echter Audit-Ziele.
3. **Mythril auf diesem Node (TIMEOUT).** Symbolische Ausfuehrung ueberschreitet 60 s trotz
   `--max-depth 64`; wird als dokumentierter Blocker gefuehrt, nicht als Befund.
4. **Echidna-Assertion-Modus** falsifiziert `assert_solvent` bei 5.000 Transaktionen nicht,
   waehrend der forge-Test den Drain reproduziert. Das ist Divergenz, kein Widerspruch —
   und der Grund, warum Counterexample plus Negativkontrolle verlangt werden.
5. **Git/GitHub.** `git` nicht im `PATH`; Token laut `STATUS.md` ungueltig. Kein Push, kein Merge,
   keine Repository-Aktion. Rollback erfolgt lokal ueber Backup und Dateikopien.
6. **Docker/IDA** unveraendert nicht vorhanden (V7-Bestand).

## 10. Rollback

Siehe `docs/ROLLBACK.md`. Kurzfassung: `bin/skill` und der Katalog wurden nicht angefasst; die
V8-Dateien werden aus `*.backup-<stamp>` bzw. `backups/pre-v8-*.tar.gz` zurueckgerollt, der
`~/.agents`-Skill aus `SKILL.md.backup-<stamp>`.

## 11. Maschinenlesbarer Zustand

```json
{
  "schema": "sfs-ctf-skill-index-acceptance-v1",
  "generated_at": "2026-11-22T00:00:00Z",
  "overall": "PARTIAL_ACCEPTED",
  "items": [
    {"id": 1, "name": "json_package_integrity", "status": "PASS"},
    {"id": 2, "name": "v7_preserved", "status": "PASS"},
    {"id": 3, "name": "catalog_selection_real", "status": "PASS", "catalog_entries": 133},
    {"id": 4, "name": "context_capability_availability_dependencies", "status": "PASS"},
    {"id": 5, "name": "real_tool_execution", "status": "PASS", "adapters": 13},
    {"id": 6, "name": "results_change_selection", "status": "PASS"},
    {"id": 7, "name": "evidence_beyond_hash", "status": "PASS"},
    {"id": 8, "name": "known_vulnerability_reproduced", "status": "PASS", "verdict": "VERIFIED_LOCAL"},
    {"id": 9, "name": "error_recovery_negative_tests", "status": "PASS", "tests": "49/49"},
    {"id": 10, "name": "freebuff_enforced_activation", "status": "BLOCKED",
     "reason": "desktop build without CLI tool-call hook or trace"},
    {"id": 11, "name": "routing_confirmed_in_trace", "status": "BLOCKED",
     "reason": "no trace facility in this build"},
    {"id": 12, "name": "reproducible_v7_v8_comparison", "status": "PARTIAL",
     "scope": "routing quality + one real corpus run"},
    {"id": 13, "name": "rollback_documented", "status": "PASS"}
  ],
  "blockers": [
    "freebuff_runtime_hook_absent",
    "freebuff_trace_absent",
    "mythril_timeout_on_node",
    "git_unavailable_and_token_invalid"
  ]
}
```

## 12. Evidenzindex (auf dieser Maschine vorhanden)

| Verzeichnis | Dateien | Status / Verdict |
|---|---|---|
| `logs/v8/run-final-20261121T233228Z` | 9 | VERIFIED / VERIFIED_LOCAL |
| `logs/v8/recovery-no-forge-20261121T233036Z` | 10 | COMPLETED_UNVERIFIED / STRUCTURAL_ONLY |
| `logs/v8/recovery-no-forge-20261121T233007Z` | 10 | COMPLETED_UNVERIFIED / STRUCTURAL_ONLY |
| `logs/v8/recovery-no-forge-20261121T232725Z` | 8 | COMPLETED_UNVERIFIED / INVALID |
| `logs/v8/recovery-no-forge-20261121T232516Z` | 6 | unvollstaendig (abgebrochen) |
| `logs/v8/recovery-no-forge-20261121T231946Z` | 4 | unvollstaendig (abgebrochen) |
| `logs/v8/recovery-no-slither-20261121T231423Z` | 5 | unvollstaendig (abgebrochen) |
| `logs/v8/recovery-no-slither-20261121T231404Z` | 7 | COMPLETED_UNVERIFIED / PARTIAL |
| `logs/v8/run-20261121T231200Z` | 9 | VERIFIED / VERIFIED_LOCAL |
| `logs/v8/run-20261121T231031Z` | 9 | VERIFIED / VERIFIED_LOCAL |

| Vergleich | `logs/compare-v7-v8-20261121T231200Z.json` | |
| Backup | `backups/pre-v8-20261121T225722Z.tar.gz` | |
| Installierte Skill-Datei | `~/.agents/skills/ctf-skill-index/SKILL.md` | |

---

## 13. Nachtrag 2026-11-22 — GitHub-Stand und Freebuff-Skill-Kollision

**Dieser Nachtrag hat Vorrang vor den historischen GitHub-/Token-Angaben in Abschnitt 2 und 9.**

- Der zuvor fehlgeschlagene GitHub-Transport wurde spaeter ueber das bestehende
  redigierende `bin/push` mit bereits vorhandenem Token funktionsfaehig gemacht.
- Der V8-Branch `v8/adaptive-orchestrator` wurde mit Commit
  `24394eb7ee518556d1cdb3f29e29f2df37203c6d` erfolgreich gepusht.
- Die seinerzeit 22 fehlenden `main`-Commits wurden bereits im separaten
  Integrationsbranch `v9/copilot-delegation-integration` beruecksichtigt.
  Dieser baut auf `main` `ff27da99c2b86a9d808f7e38986e8a86b333e986` auf.
- Draft-PR [#6](https://github.com/SFS-Labs/ctf-skill-factory/pull/6) existiert.
  Weder `main` noch der historische V8-Branch wurden gemergt beziehungsweise
  durch die nachtraegliche Runtime-Arbeit ersetzt.
- Die Freebuff-Account-Skill-Definition wurde laut lokalem Probeversuch
  gespeichert. `cloud_read_skill` ist aber fuer account-only Skills kein
  zuverlaessiger Readback: der gleichnamige gebuendelte V7-Skill kann den
  Eintrag bei der Abfrage ueberschatten.
- Der im GitHub-Code von Freebuff dokumentierte Projektpfad
  `.agents/skills/<skill-name>/SKILL.md` und die Prioritaet projektlokaler
  Skills sind die Basis fuer den neuen eindeutigen Skill
  `.agents/skills/ctf-skill-index-v8/SKILL.md`.
- `install-freebuff.sh` installiert diesen Skill im Projekt, ohne
  `ctf-skill-index` V7 zu loeschen. Tests der Dateistruktur sind hinzugefuegt.
- **Offen:** In diesem Chat besteht kein steuerbarer Zugriff auf eine neue
  Freebuff-Desktop-Sitzung. Automatische Skill-Aktivierung und realer V8-
  Orchestrator-Aufruf durch einen neu gestarteten Agenten sind daher
  `RUNTIME_UNVERIFIED`, nicht `PASS`.
- Der reale Orchestratoraufruf ist inzwischen dennoch belegt (Abschnitt 14):
  Installation, echter `run --allow-exec`, echte Artefakte, `verify` und die
  negative Aktivierungsprobe wurden auf dem Node gemessen. Nicht belegt ist
  allein der `skill`-Toolaufruf der neuen Sitzung.
- Copilot-Delegation und Proficiency sind getrennt. Keine echten
  Copilot-Delegationen, kein zusaetzlicher Credit-Verbrauch, kein Auto-Merge.

## 14. Nachtrag 2026-11-22 — reale Runtime-Ausfuehrung und Bug-Bounty-Reife

Gegenstand: V9-Integrationsbranch `v9/copilot-delegation-integration` auf
`0f1e6fd38782db0379f494acbbcfe360dc84b033`, Arbeitsverzeichnis `~/ctf-skills`.

### 14.1 Ausgefuehrt, mit Messwerten

| Pruefung | Ergebnis |
|---|---|
| `python3 -m unittest discover -s tests` | **91/91 OK** (2 Skips), 24,9 s |
| `python3 bin/skill-orchestrator.py selfcheck` | Katalog 133, Adapter verfuegbar, Negativproben `INVALID`, Reserve `ok` |
| `bash -n install-freebuff.sh` | Exit 0 |
| `bash install-freebuff.sh --apply` | Exit 0, Backup `SKILL.md.pre-v8-20261122T015857Z` |
| `.agents/skills/ctf-skill-index-v8/SKILL.md` | vorhanden, `name: ctf-skill-index-v8` |
| `~/.agents/skills/ctf-skill-index/SKILL.md` | V7-Inhalt erhalten (133 Zeilen, sieben Regeln, L0-L9) + V8-Bruecke |
| `run --allow-exec` auf `corpora/verify` | `VERIFIED`, 5,20 s, max. RSS 95.844 kB |
| `verify --report` | `VERIFIED_LOCAL`, 3/3 Inhaltsfamilien, keine Widersprueche |
| Wiederholungslauf | zweiter `run` ebenfalls `VERIFIED` / `VERIFIED_LOCAL` |
| Manipulierter Evidenzbericht | `verify` → `INVALID` (SHA-256-Mismatch erkannt) |
| Negativprobe (Marketingtext) | `NO_MATCH`, 0 Kandidaten |

Statische Seite: `slither` 12 Befunde (u. a. `reentrancy-eth`, `arbitrary-send-eth`,
`unchecked-lowlevel`). Dynamische Seite: `test_reentrancy_drains_vault`,
`test_sweep_breaks_solvency`, `test_aggregate_invariant_blind_to_reentrancy` alle
`Success`; Negativkontrolle `test_invariant_holds_initially` `Success`.
Unabhaengige Methoden: `static:slither` + `dynamic:forge`.

### 14.2 Bug-Bounty-Reife (nur lokaler autorisierter Korpus)

| Kriterium | Befund |
|---|---|
| Automatische Skill-Auswahl | `route` waehlt `echidna` (33,96) und `slither` (25,32); sachfremd → `NO_MATCH` |
| Reproduzierbare lokale Tests | forge-Laeufe deterministisch, Exit 0, Testnamen stabil |
| Counterexample + Negativkontrolle | beide real vorhanden und im Evidenzvertrag erzwungen |
| Inhaltliche Evidenzpruefung | `verify` prueft Assertion im Testrumpf, Negativkontrolle, Detektor-Claims |
| Adaptive Recovery | im Vertrag getestet; real ohne `forge` belegt (Abschnitt 6) |
| Ressourcenkontrolle | 95,8 MB RSS, 5,2 s, sequenziell, Reserve-Gate aktiv |
| Nachvollziehbare Findings | `evidence-report.json` mit SHA-256 je Artefakt, `run-summary.json` 24 KB |

**Verdikt: `PARTIAL`.** Die Pipeline ist fuer autorisierte lokale Korpusziele
end-to-end belegt. Fuer externe Programme fehlen die Programmauswahl, der
schriftlich zulaessige Scope, die Disclosure-Regeln und eine Zielserie; `myth`
laeuft auf diesem Node weiterhin in den Timeout, Docker ist nicht vorhanden.

### 14.3 Abgrenzung

- Der `skill`-Toolaufruf mit `name=ctf-skill-index-v8` ist **nicht** belegt:
  dieser Desktop-Build hat keinen automatisierbaren Sitzungsstart
  (`/usr/bin/freebuff` liefert nur `path-repair`/`linux-launch`), und die Sitzung
  begann vor der Installation. Status bleibt `RUNTIME_UNVERIFIED` fuer die
  Aktivierung, `TOOLCHAIN_EXECUTED` fuer die Ausfuehrung.
- Copilot: Governance geladen, `preflight` blockiert (Issues 403, Agent-Tasks 403,
  Credits aufgebraucht). Keine Delegation, kein Credit-Verbrauch, kein Auto-Merge.

Abnahmeverfahren: `docs/FREEBUFF-V8-RUNTIME-ACCEPTANCE.md`.
