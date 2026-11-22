# Freebuff V8 Runtime-Abnahme — Skill-Kollision und echter Toolaufruf

Stand: 2026-11-22. **Status: TOOLCHAIN_EXECUTED / SESSION_ACTIVATION_UNVERIFIED.**
Installation und Ausfuehrung des Orchestrators sind auf dem Node belegt (Abschnitt
"Beobachteter Lauf"). Ein `skill`-Toolaufruf mit `name=ctf-skill-index-v8` durch einen
*neu gestarteten* Agenten ist **nicht** belegt und bleibt `RUNTIME_UNVERIFIED`.

## Technische Diagnose

- Freebuff-Quelle `sdk/src/skills/load-skills.ts`: projektlokales `.agents/skills/` hat
  Vorrang vor den globalen Skill-Verzeichnissen; ein Skill wird nur geladen,
  wenn Verzeichnis und `name` im YAML-Frontmatter uebereinstimmen.
- Freebuff-Quelle `packages/agent-runtime/src/tools/handlers/tool/skill.ts`: der
  `skill`-Toolaufruf bevorzugt die Projektdatei vor dem Sitzungs-Cache.
- Der vorherige `cloud_read_skill`-Readback war fuer den Account-Skill nicht
  beweiskraeftig (V7-Bundled-Shadow / Account-Only-Lookup).
- Der eigenstaendige Name `ctf-skill-index-v8` vermeidet diese
  Namenskollision, **erzwingt aber nicht automatisch Modellaktivierung**.
- Die Freebuff-Cloud-Sitzung muss wirklich mit Projektroot `~/ctf-skills`
  beziehungsweise dem Checkout mit diesem Skill gestartet werden.

## Repository- und Dateiabnahme

```bash
cd ~/ctf-skills
python3 -m unittest discover -s tests
python3 bin/skill-orchestrator.py selfcheck
bash -n install-freebuff.sh
bash install-freebuff.sh           # nur Vorschau
bash install-freebuff.sh --apply   # nur nach Kontrolle von Quelle und Ziel
sed -n '1,6p' .agents/skills/ctf-skill-index-v8/SKILL.md
```

Erwartet: `name: ctf-skill-index-v8`, `name` passt zum Verzeichnis,
`ctf-skill-index` bleibt unveraendert beziehungsweise nur mit bestehender V8-Bruecke,
und der Orchestrator ist ausfuehrbar. Tests auf dem *echten Node* erneut ausfuehren;
GitHub-Datei-Readbacks sind keine lokalen Testnachweise.

## Echte Runtime-Abnahme (neue Freebuff-Sitzung)

1. Eine **neue** Freebuff-Desktop-Sitzung mit dem Projektverzeichnis starten.
   Eine laufende alte Sitzung beweist keine neue `AGENTS.md`-/Skill-Discovery.
2. Benutzerauftrag ohne explizite Skill-Nennung:
   > Audit the authorized local Solidity Vault in corpora/verify for withdraw
   > reentrancy; verify with a reproducible local test and negative control.
3. Im Agenten-Toolprotokoll muss ein echter `skill`-Aufruf mit
   `name=ctf-skill-index-v8` erscheinen; Skill-Antwort muss die V8-Orchestrierung
   enthalten. Ein `cloud_read_skill`-Readback oder die bloße Skill-Liste genuegt nicht.
4. Im selben Agentenlauf muss ein **tatsaechlicher** Prozessaufruf
   `python3 bin/skill-orchestrator.py run ... --allow-exec` protokolliert sein,
   mit lokalem autorisiertem Ziel, Exit-Code und erzeugtem `evidence-report.json`.
5. `verify --report ...` ausfuehren; Counterexample, Negativkontrolle und
   Tool-Receipts anhand der Artefakte pruefen. Der Agentenbericht allein ist
   keine unabhaengige Evidenz.
6. Negativkontrolle: Neue, sachfremde Anfrage (z. B. Marketingtext) darf
   V8 nicht ohne fachlichen Anlass aktivieren.
7. Umgebungsgrenzen ausdruecklich pruefen: Wenn die Freebuff-Cloud den
   `~/ctf-skills`-Node nicht erreicht, keine lokale Toolausfuehrung vortaeuschen.

## Beobachteter Lauf — 2026-11-22, Freebuff-Sitzung auf `~/ctf-skills`

Gemessen auf dem echten Node, nicht simuliert. Aufruf durch den Freebuff-Agenten
selbst im Projektverzeichnis `~/ctf-skills`.

| Schritt | Befehl | Ergebnis |
|---|---|---|
| Suite | `python3 -m unittest discover -s tests` | **91/91 OK** (2 Skips: realer Korpuslauf + statusbedingter Vertragstest), 24,9 s |
| Selbsttest | `python3 bin/skill-orchestrator.py selfcheck` | Katalog 133, Adapter verfuegbar, Negativproben `INVALID`, Reserve `ok` |
| Syntax | `bash -n install-freebuff.sh` | Exit 0 |
| Vorschau | `bash install-freebuff.sh` | Dry-Run, keine Schreibvorgaenge |
| Installation | `bash install-freebuff.sh --apply` | Exit 0, Backup `SKILL.md.pre-v8-20261122T015857Z` |
| Ziel | `.agents/skills/ctf-skill-index-v8/SKILL.md` | vorhanden, `name: ctf-skill-index-v8`, Verzeichnis passt |
| V7 | `~/.agents/skills/ctf-skill-index/SKILL.md` | erhalten (133 Zeilen, "Sieben Regeln (V7, unveraendert gueltig)", L0-L9) + V8-Bruecke |

Realer Orchestratorlauf, Aufgabe **ohne** Nennung des Skill-Namens:

> Audit the local Solidity Vault in corpora/verify for withdraw reentrancy.
> Produce a reproducible local counterexample, negative control and independently
> verified evidence.

| Schritt | Adapter | Status | Dauer |
|---|---|---|---|
| MAP | `surya describe` | COMPLETED | 1,32 s |
| STATIC | `slither --json` | COMPLETED, 12 Befunde | 1,55 s |
| COUNTEREXAMPLE | `forge test --json` | COMPLETED, 3 Tests Success | 0,15 s |
| NEGATIVE_CONTROL | `forge test --match-test test_invariant_holds_initially` | COMPLETED | 0,08 s |

Wandzeit 5,20 s, max. RSS 95.844 kB, strikt sequenziell. `verify` ueber
`evidence-report.json`: `VERIFIED_LOCAL`, `content_verified_families` =
`counterexample`, `negative_control`, `static`; unabhaengige Methoden `static:slither`
und `dynamic:forge`; keine Widersprueche.

Negative Aktivierungsprobe (sachfremd, Marketingtext): `route` → `NO_MATCH`,
0 Kandidaten, 0 Domaenenkandidaten. Kein Security-Skill aktiviert.

### Tatsaechliche technische Grenze

- `/usr/bin/freebuff` ist ein Launcher-ELF ohne Unterbefehls-Dispatch: `--help`,
  `--version` und `headless` liefern ausschliesslich `[path-repair]` und
  `[linux-launch]` und starten die GUI. Es gibt keinen automatisierbaren
  Sitzungsstart, kein Headless-Ziel und keinen Tool-Call-Hook.
- Skill-Discovery geschieht beim **Sitzungsstart**. Diese Sitzung begann, bevor
  `.agents/skills/ctf-skill-index-v8/SKILL.md` installiert war; im Skill-Register
  der Sitzung steht deshalb nur der Account-Skill `ctf-skill-index`. Ein
  nachtraeglicher `cloud_read_skill`-Readback ist laut AGENTS.md kein Nachweis.
- **Checkout-Versatz:** `~/ctf-skills` ist auf `v8/adaptive-orchestrator`
  ausgecheckt, damit der historische Branch unveraendert bleibt. Die dort
  geladene Projektanweisung ist dessen `AGENTS.md` **ohne** den V8-Abschnitt;
  der V9-Branch mit dieser Anweisung liegt im Worktree
  `/tmp/ctf-v9-integration`. Fuer die Sitzungsabnahme muss der Workspace auf dem
  V9-Checkout liegen. Der projektlokale Skill selbst ist in `~/ctf-skills`
  installiert und damit fuer eine dort gestartete Sitzung auffindbar.
- Folge: `SKILL_LOADED` ist in dieser Sitzung nicht beobachtbar. Belegt sind
  Installation, eindeutiger Name, reale Orchestratorausfuehrung, reale Artefakte,
  `verify` und die negative Aktivierungsprobe. Das ist `TOOLCHAIN_EXECUTED`,
  nicht `RUNTIME_VERIFIED`.

## Maschinenlesbare Abnahme

Nur nach beobachtetem Lauf im existierenden `VERIFICATION.md` oder unter
`logs/v8/runtime-acceptance-<timestamp>.json` festhalten:

```json
{
  "skill_name": "ctf-skill-index-v8",
  "skill_installed": true,
  "skill_tool_invoked": false,
  "skill_body_confirmed": false,
  "orchestrator_run_invoked": true,
  "report_verified": true,
  "negative_activation_test": "PASS",
  "tests": "91/91 OK (2 skips)",
  "status": "TOOLCHAIN_EXECUTED"
}
```

Zusatzbefunde: zwei unabhaengige `run`-Laeufe liefern beide `VERIFIED` /
`VERIFIED_LOCAL`; ein manipulierter SHA-256 im Evidenzbericht ergibt `INVALID`.

`skill_installed`, `orchestrator_run_invoked`, `report_verified` und
`negative_activation_test` sind in dieser Sitzung beobachtet.
`skill_tool_invoked` und `skill_body_confirmed` bleiben `false`, weil der Build
keinen Sitzungsstart erlaubt und die Sitzung vor der Installation begann.
`tests/test_freebuff_v8_runtime_contract.py` haelt diese Status-Boolean-Konsistenz
maschinell fest, damit `RUNTIME_VERIFIED` nicht ohne echten `skill`-Aufruf
dokumentiert werden kann.

Status nur bei belegter Evidenz hochstufen: `SKILL_LOADED` nach echtem
`skill`-Aufruf, `ORCHESTRATOR_EXECUTED` nach realem `run`,
`RUNTIME_VERIFIED` erst bei belastbarem End-to-End-Nachweis einschließlich
negativer Aktivierungskontrolle.

## GitHub- und Copilot-Abgrenzung

- Runtime-Fix erfolgt auf dem bestehenden Draft-PR #6, Branch
  `v9/copilot-delegation-integration` gegen `main`.
- Historischen Branch `v8/adaptive-orchestrator` nicht aendern und nichts mergen.
- Copilot-Credits aufgebraucht: keine kostenpflichtige Delegation.
- Ein normaler GitHub-Commit beweist keine Copilot-Proficiency-Aktivitaet.
- Vor anschliessendem Bug-Bounty-Einsatz: konkretes Programm und dessen Scope,
  erlaubte Testmethoden, Disclosure-Regeln und Reproduzierbarkeit pruefen.

Quellen: `CodebuffAI/freebuff` SDK-Skill-Loader und Skill-Handler; bestehende
SFS-Labs-Dokumentation und Projektdateien.
