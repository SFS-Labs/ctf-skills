# Verifikation — echte Laeufe (Stand 2026-11-21)

Ziel: `corpora/verify/Vulnerable.sol` — Vault mit Reentrancy, `tx.origin`-Sweep und unchecked Low-Level-Call.
Kein `--help`-Test, sondern Findings an einem Programm mit bekannten Fehlern.

| Layer | Werkzeug | Ergebnis |
|---|---|---|
| L1 | `solc-select` / `crytic-compile` | solc **0.8.28** gepinnt, AST/ABI gebaut |
| L1 | `surya` | Contract-Map erzeugt (deposit, withdraw, sweep, forceSend) |
| L2 | `slither` | `reentrancy-eth` in `Vault.withdraw()` + Arbitrary-Send in `Vault.sweep()` |
| L4 | `mythril` | SWC-115 *Dependence on tx.origin* in `Vault` |
| L3 | `echidna` | Counterexample: `deposit → sweep` bricht `echidna_solvent` (Reason `ReturnFalse`) |
| L3 | `medusa` | 36.995 Calls, Coverage-Report erzeugt — flaggt die Invariante **nicht** |
| PoC | `forge` | 3/3 Tests grün: Invariante hält anfangs, Sweep bricht sie, Reentrancy drainiert den Vault |

## Divergenz-Befund (Emergenz-Regel 3)

Echidna findet den Bruch, Medusa nicht — bei identischer Quelle und identischen Sendern.
Damit ist belegt, warum ein einzelnes Tool kein „sauber" liefern darf: Medusa allein hätte hier
einen Fehlalarm-negativen Befund produziert. Die Regel „zwei Signale aus verschiedenen Schichten"
ist damit empirisch, nicht nur behauptet.

## Was zusätzlich nachgewiesen wurde

- `forge test` läuft ohne forge-std (eigene `Vm`-Interface-Deklaration für `prank(sender, origin)`).
- Reentrancy-Test korrigiert: die Solvenz-Invariante bleibt scheinbar wahr, weil `totalDeposits`
  mit sinkt — der Diebstahl zeigt sich nur am Guthaben (`balance <= 1 ether`). Genau diese
  Falle ist der Grund, warum Counterexample + PoC zusammen geprüft werden müssen.
- `exploitdb`: GitHub-Repo ist **archiviert und geleert** (nur noch README); Daten kommen vom
  offiziellen Nachfolger `gitlab.com/exploit-database/exploitdb` — 10,2 MB Exploit-CSV + 220 KB Shellcodes.

## Grenzen (ehrlich, nicht behoben)

| Skill | Grund |
|---|---|
| ~~`cryo`~~, ~~`diffusc`~~, ~~`daedaluzz`~~ | **behoben** (siehe Nachtrag unten): Selbstbau bzw. Userspace-Go, alle drei laufen |
| `attacknet`, `eth-security-toolbox`, `cloudexec`, `paradigm-ctf-infra` | brauchen Docker; Rezepte liegen in `recipes/` |
| `ida-evm`, `ethersplay` | IDA nicht installiert; Bytecode-Schicht läuft über `etheno`/`evmasm`/`evm-cfg-builder` |
| Repo-Versionierung | kein `git` → Updates über `python3 bin/fetch` (authentifizierte Tarballs) |

## Nachtrag 2026-11-21: cryo, diffusc, daedaluzz lauffähig gemacht

Alle drei waren als "nicht lauffähig" dokumentiert. Die echten Ursachen waren andere als vermutet
und sind hier mit Beweis-Kommando festgehalten.

### daedaluzz — Go, nicht Python
`go.mod` sagt `go 1.15`, es ist ein Go-Programm (`main.go`, Deps logrus + urfave/cli).
Fix: Userspace-Go 1.23.4 nach `~/.local/opt` (kein Root), dann `go build` im vendor-Baum.
Rezept: `recipes/daedaluzz-build.sh`.

```
$ cd /tmp/proof-daedaluzz && daedaluzz        # exit=0
$ ls -l generated-maze.sol                     # 32560 bytes
$ solc --bin generated-maze.sol | grep -c '^======= '   # 1 Contract (Maze) kompiliert
```

### diffusc — git war nie das Laufzeitproblem
`setup.py` deklariert genau eine git-Abhängigkeit (`slither-analyzer@git+https://github.com/webthethird/slither.git@dev-diffusc-testing`).
Der Code ruft nirgends git auf (grep über alle `*.py`). Fix: Fork als codeload-Tarball installieren,
diffusc mit `--no-deps` dazu. Zwei Folgeprobleme mussten gelöst werden:

1. `pkg_resources.require("diffusc")` → VersionConflict wegen der git-URL in `Requires-Dist`
   → lokaler Patch: feste Version im `--version`-Zweig.
2. `solc_select` fragt `binaries.soliditylang.org` per urllib **ohne User-Agent** an → HTTP 403
   (sowohl `list.json` als auch der solc-Download via `urlretrieve`) → Patch mit UA-Header.

Zusätzlich: `forge` muss im PATH sein, sonst wählt crytic-compile das Foundry-Plugin
(`FileNotFoundError: 'forge'`), und der **Dateiname** bestimmt den Contract-Namen
(`VaultV1.sol` → Contract `Vault`; `VaultA.sol` → IndexError).
Rezept: `recipes/diffusc-setup.sh`.

```
$ diffusc /tmp/diffusc-src/VaultV1.sol /tmp/diffusc-src/VaultV2.sol -d /tmp/proof-diffusc
  * tainted_functions: ...
  * Fuzzing contract generated and written to /tmp/proof-diffusc/DiffFuzzUpgrades.sol
  * Echidna configuration file generated and written to /tmp/proof-diffusc/CryticConfig.yaml
My work here is done. Thanks for using me, have a nice day!
```

### cryo — kein Release-, sondern ein Header- und Compiler-Problem
Die Releases-API von `paradigmxyz/cryo` hat genau ein Release (`0.2.0`) **ohne Assets** — ein
fertiges Binary gibt es nicht, Selbstbau ist zwingend. Der Abbruch lag an zwei Dingen:

1. `openssl-sys` (über alloy/reqwest, native-tls) braucht Dev-Header. `libssl.so.3` ist vorhanden,
   `libssl-dev` nicht. `apt-get download libssl-dev` funktioniert **ohne Root**; mit `dpkg-deb -x`
   nach `~/.local/openssl-dev` entpacken und `OPENSSL_INCLUDE_DIR`/`OPENSSL_LIB_DIR` setzen.
   Wichtig: `opensslconf.h`/`configuration.h` liegen im Multiarch-Zweig
   (`usr/include/x86_64-linux-gnu/openssl/`) und müssen nach `usr/include/openssl/` kopiert werden.
2. Danach `ethnum 1.5.0`: `error[E0512]: cannot transmute between types of different sizes`
   auf rustc 1.100 → `cargo update -p ethnum` (1.5.3).

Rezept: `recipes/cryo-build.sh`.

```
$ cryo --version
cryo 0.3.2
$ cryo blocks --blocks 19000000 -r https://ethereum-rpc.publicnode.com -o /tmp/cryo-out
- blocks collected: 1
- rows written: 1
$ ls /tmp/cryo-out/*.parquet
ethereum__blocks__19000000_to_19000000.parquet      # 1 Row, Schema blocks
```

## Automatisierte Beweislaeufe — `bin/smoke` (2026-11-21)

Die Nachweise oben sind ab jetzt reproduzierbar statt einmalig: `bin/smoke` faehrt sie in
temporaeren Verzeichnissen und prueft die Artefakte **inhaltlich**, nicht nur auf Existenz.

| Werkzeug | Kommando (so ruft `bin/smoke` es auf) | inhaltliche Pruefung |
|---|---|---|
| `cryo` | `cryo blocks --blocks 19000000 -r <rpc> -o <tmp>/out` | Parquet per pyarrow gelesen: 1 Row, 8 Spalten, `block_number == 19000000` |
| `diffusc` | `diffusc <tmp>/VaultV1.sol <tmp>/VaultV2.sol -d <tmp>/out` | `DiffFuzzUpgrades.sol` enthaelt `contract`, `CryticConfig.yaml` nicht leer |
| `daedaluzz` | `daedaluzz` im leeren Verzeichnis | `generated-maze.sol` > 5 kB, `pragma solidity` + `contract`, mit `solc --bin` kompiliert |
| `push` | `bin/push --selftest` | sechs synthetische Lecks (dulwich-Erfolgszeile, URL-Userinfo, Bearer-Header, Query-Token) muessen redigiert sein; kein `LEAK` |

Fixtures liegen jetzt im Repo: `corpora/smoke/VaultV1.sol` / `VaultV2.sol` (vorher nur unter `/tmp`).
Ergebnis: `logs/smoke.json` (maschinenlesbar, nicht versioniert) und ein Block in `STATUS.md`,
den `bin/doctor` beim Neuschreiben erhaelt.

Beim Automatisieren gefunden und im Rezept vermerkt: diffusc bricht mit `IndexError` in
`slither_provider.py:155` ab, wenn der Pfad **keinen** Verzeichnis-Separator enthaelt
(`path.rsplit(os.sep, 1)[1]`) — also nie nackte Dateinamen uebergeben.

`bin/smoke` endet mit Exit 0, wenn kein Werkzeug `FAIL` ist. `SKIP` heisst: Umgebung fehlt
(Binary, `forge`, `solc` oder Netz) — kein bestandener Test, aber auch kein stilles Rot.

## Endzustand 2026-11-21 (gemessen, nicht behauptet)

`bin/doctor` ruft jeden der 51 Werkzeug-Einträge einzeln auf, prüft 133 Vendor-Bäume samt
`.fetched`-Marker, 133 Wissenskarten auf die sechs Pflichtabschnitte und die Wrapper im PATH:

```
ok=22 lib=3 ref=26 fail=0 | vendor=133/133 karten=133/133 | skills=133 quellen=134 alias=1
```

Differenz Manifest → vendor-Baum: **0** (jeder Eintrag hat Baum und lesbaren Marker;
`exploitdb` bewusst nur als CSV-Index, weil das GitHub-Repo archiviert und geleert ist).

### 133 gegen 134: der Fork-Alias

`repos.tsv` enthält **134** Quellen. `NethermindEth/EVMYulLean` hat denselben Baum wie
`paradigmxyz/evmyullean` und wird deshalb nicht als zweiter Skill gehalten. Der Beweis ist eine
Zeile, keine Prosa: `repos.tsv` trägt
`alias_of=evmyullean; tree_sha256=f27de34679ad5b6573a3ff387f14405b88f7bb98eb8fcc4c54a9a156c1210126; files=109`.
Derselbe Digest wird

- von `bin/doctor` bei jedem Lauf über den aktuellen `vendor/`-Baum gerechnet,
- von `bin/alias-check` zusätzlich anonym gegen
  `github.com/NethermindEth/EVMYulLean/archive/HEAD.tar.gz` geprüft,
- von `bin/gen_skills` verweigert, wenn Baum und Pin auseinanderlaufen.

`bin/fetch` legt für Alias-Zeilen keinen zweiten Klon an; `bin/gen_skills` schreibt die
Alias-Records (`slug`, `repo`, `tree_sha256`, `files`) ins Manifest und in die Karte, und
Baum/Karte existieren nur einmal. Ändert sich der Upstream-Baum, wird der Lauf rot, bis
`bin/alias-check --update` den neuen Digest nach erfolgreicher Remote-Prüfung pinnt — kein
datierter Behauptungssatz.

Damit: **134 Quellen − 1 Alias = 133 Skills = 133 Bäume = 133 Karten = Plansoll**. Der Plan-Satz
„EVMYulLean/solidity-lean = ein Skill" war ungenau: `solidity-lean` ist ein eigenständiges Repo
(andere Semantik-Ebene) und bleibt ein eigener Skill.

### Was dabei repariert wurde (Ursachen, nicht Symptome)

| Befund | Ursache | Fix |
|---|---|---|
| `etheno`, `evm-cfg-builder`, `fuzz-utils`, `mev-inspect`: `ModuleNotFoundError: pkg_resources` | `setuptools>=81` hat `pkg_resources` entfernt | uv-Tools mit `--with 'setuptools<81'` neu installiert |
| `etheno` nach `--force`: `pysha3` baut nicht | `pysha3` unterstützt Python 3.12 nicht | `--python 3.10` |
| `legions`: `FileFinder.find_module` fehlt | `nubia` nutzt die in 3.12 entfernte API | `--python 3.9` |
| `inspect-block`: `No module named 'cli'`, dann `sqlalchemy`, dann `getargspec` | 2021er-Projekt, Entry-Point importiert Repo-Root-Modul und Postgres-Stack, Code nicht 3.11+-fähig | Installation aus `vendor/`, `--python 3.10`, `sqlalchemy`+`psycopg2-binary`, Repo-Root per `.pth` |
| `forge`, `cast`, `anvil`, `solar` „nicht im PATH" | foundry legt sie nur in `~/.foundry/bin` ab | Symlinks nach `~/.local/bin` (statt rc-Änderung) |
| `skill`-Wrapper fehlte | Symlink nie angelegt | `~/.local/bin/skill -> bin/skill` |
| `iron-proxy`, `mev-boost` als Referenz geführt | vorgebaute `linux_amd64`-Assets waren ungenutzt | Release-Tarball nach `tools/`, Symlink, Aufruf verifiziert |
| STATUS zählte 17 ausführbar + 83 Referenz = 100 von 134 | `doctor` kannte nur 23 Slugs und ließ 28 still fallen | `doctor` klassifiziert jetzt **alle** 51 Werkzeug-Einträge in AUSFÜHRBAR / BIBLIOTHEK / REFERENZ und exitet 1 bei jeder unklassifizierten Zeile |

### End-to-End-Lauf eines Rezepts gegen einen geholten Skill

`recipes/slither-vendor.sh` (Default-Slug `evmyullean`) löst den Slug über `manifest.json` auf,
kopiert `EvmYul/Yul/YulSemanticsTests/Storage.sol` aus `vendor/paradigmxyz/evmyullean` in ein
temporäres Verzeichnis und analysiert mit dem gepinnten `solc 0.8.19`:

```
slither : Storage.sol analyzed (2 contracts with 102 detectors), 3 result(s) found
Ergebnis: 3 Befund(e) im JSON   # solc-version, 2x low-level-calls
```

Laufzeit 1,0 s, Exit 0. `bin/smoke` bestätigt zusätzlich die vier Beweisläufe
(cryo, diffusc, daedaluzz, Redaktions-Selbsttest) mit `4 OK`.

### Was offen bleibt (Blocker mit nächstem Schritt)

- **GitHub-Token ungültig** (HTTP 401 `Bad credentials`, Datei unverändert vom 03:21): neue
  fine-grained PAT mit `Contents: Read and write` auf `SFS-Labs/ctf-skill-factory`, Eingabe per
  `ctf-token`. Öffentliche Quellen werden anonym gelesen (HTTP 200), `bin/fetch` läuft also weiter.
- **Zehn Release-Binaries ohne Linux-Artefakt** (`bytecode-verifier`, `diligence-fuzzing`,
  `dstack`, `fluxture`, `mev-boost-relay`, `mev-share-rs`, `optik`, `r55`, `rollup-boost`,
  `soroban-detectors`): Referenz mit Quellbaum; nächster Schritt ist `cargo build`/`go build`
  im jeweiligen `vendor/`-Baum. Nicht im Plan vorgesehen, deshalb nicht gebaut.
- **Docker** (4 Skills) und **IDA** (`ida-evm`) bleiben Referenz; Rezepte bzw. Karten liegen bereit.

## V8 — echte Orchestrator-Laeufe (2026-11-22)

### Integritaet des Eingabepakets

7/7 Eintraege bytegenau (Groesse, SHA-256, ZIP-Member), ZIP-SHA-256
`c476e3720fed3ffbf8b857b0219d14a3f2afede0732397d5de876b7e317fced8`, `testzip()` sauber,
Rekonstruktion in `.v8_staging/` ohne Traversal/Overwrite.

### Hauptlauf (`--allow-exec`)

| Schritt | Adapter | Exit | Artefakt |
|---|---|---|---|
| MAP | `surya describe` 0.4.13 | 0 | `surya-describe.log` |
| STATIC | `slither --json` 0.11.6 | 255 (Befund) | `slither.json`, 79 KB, 10 Detektoren |
| COUNTEREXAMPLE | `forge test --json` 1.10.0 | 0 | 3 bestehende Counterexample-Tests |
| NEGATIVE_CONTROL | `forge test --match-test test_invariant_holds_initially` | 0 | Kontrolle besteht |

Verdict `VERIFIED_LOCAL`, unabhaengige Methoden `static:slither` + `dynamic:forge`.
Ein separater `verify`-Lauf ueber `evidence-report.json` reproduziert dasselbe Ergebnis.

### Recovery ohne `forge`

`slither` scheitert (Foundry-Framework) → Compiler-Diagnose → `slither-json-solc` mit
`--compile-force-framework solc` liefert 12 Befunde; `echidna` scheitert am selben Grund →
`echidna-assertion-solc` fuzzt 9 Assertions ohne Falsifikation. Verdict `STRUCTURAL_ONLY`:
statischer Befund ohne Reproduktion ist kein Beweis. Nebenbefund: Slither und Echidna teilen
den `crytic-compile`/`forge`-Stack und sind daher keine unabhaengigen Signale.

### Grenzen

Freebuff-Aktivierung ist modellvermittelt; dieser Build hat keinen Tool-Call-Hook und keine
Trace-Ausgabe. `myth` ueberschreitet 60 s und wird als Blocker gefuehrt.

## Copilot-Delegation (2026-11-22, lokal getestet)

Geprueft wurde die Delegationsschicht `bin/copilot-delegate.py` mit echten Lesezugriffen
und einem lokalen HTTP-Mock fuer alle Schreibpfade. **Es gab keine echte
Copilot-Delegation.**

| Pruefung | Ergebnis |
|---|---|
| `GET /user`, `GET /rate_limit` | 200, Login `SFS-Labs` |
| Repository `SFS-Labs/ctf-skill-factory` | 200, privat, `has_issues=false`, Admin-Recht |
| `suggestedActors` | `copilot-swe-agent` / `BOT_kgDOC9w8XQ` assignbar |
| Agent-Tasks User-Scope | 200, leer |
| Agent-Tasks Repo-Scope | 403, fehlendes Token-Recht |
| Issues-API | 403, Fine-grained-Token ohne Issues-Recht |
| Standard-Quelle `SFS-Labs/sfs-ai-development-gateway` | PAT 404; verbundene GitHub-App 200; verbatim vendored (Blob `277ad8a`, SHA-256 `b8d0548`) |
| Kontingent-Gate | geschlossen (`credits_exhausted=true`) |

Mock-Lebenszyklus (echter HTTP-Client, echte Zustandsmaschine, echte Review-Logik):

| Szenario | Ergebnis |
|---|---|
| happy (Issue), agent-task, rate-limit | `REVIEWED` / `VERIFIED` |
| ci-failure, scope-violation, secret | `CHANGES_REQUIRED` mit Befund |
| quota | `QUOTA_BLOCKED` |
| timeout | `WATCH_LIMIT_REACHED` |

`python3 -m unittest discover -s tests`: **84 Tests, 1 Skip** (opt-in `SFS_V8_REAL`).
Davon 35 neue Copilot-Tests. Alle Mock-Laeufe: `paid_spend=0`, `real_api_calls=0`,
`proven_domains=0`. Details: `docs/COPILOT-DELEGATION.md`.

## Integration V9 (2026-11-22)

Der Integrationsstand liegt auf `v9/copilot-delegation-integration`, aufgebaut auf
`main` `ff27da99` (22 Commits neuer als der alte V8-Branch). Der V8-Commit wurde
als `2845b72` konfliktfrei nachgezogen; der lokale V7-Katalog und das Tooling
wurden mit versioniert, weil `main` in den 22 Commits ausschliesslich
`benchmarks/` und `.github/` veraendert hat. Der erste Integrationscommit ist
`3d15920`; `deac305` behebt die HEAD-Erkennung von `bin/push` in linked
worktrees.

| Pruefung | Ergebnis |
|---|---|
| Vollstaendige Suite | 84 Tests, 1 Skip, OK (21,9 s) |
| Copilot-`selftest` | 8/8 Szenarien, `real_api_calls=0`, `paid_spend=0` |
| Orchestrator-`selfcheck` | 133 Katalogeintraege, 13/13 Adapter, Negativproben OK |
| `bin/push --check` | lokal = remote, MATCH |
| Draft-PR | [#6](https://github.com/SFS-Labs/ctf-skill-factory/pull/6), 173 Dateien, Basis `main`, `draft=true`, `mergeable_state=clean` |
| GitHub Checks | keine Check-Runs/Commit-Statuses gemeldet; kein CI-Erfolg behauptet |

**AGENTS.md-Runtime:** Der installierte Orchestrator nimmt `AGENTS.md` ueber
`deriveKnowledgeFiles` in `knowledgeFiles` auf; diese werden beim Session-Start
als Projektinstructions injiziert. Das ist der belegte Ladepfad. Eine neue
Freebuff-Sitzung wurde in dieser Ausfuehrung nicht automatisiert gestartet (die
Desktop-App hat keinen headless Prompt-Einstieg); eine erzwungene
Modellaktivierung wird daher nicht behauptet. Der aktuelle Chat begann vor
Anlage der Datei.

**Status:** `IMPLEMENTED`, `LOCALLY_TESTED`, `MOCK_VERIFIED`;
`RUNTIME_VERIFIED` nur fuer den AGENTS.md-Ladepfad; `LIVE_DELEGATION_BLOCKED`;
`PRODUCTION_VERIFIED` nicht erreicht.

**PR-Berechtigung:** Der Fine-grained-PAT kann Inhalte pushen, aber
Pull-Requests weder lesen noch schreiben (403). Der Draft-PR wurde ueber die
verbundene SFS-Labs-GitHub-App erstellt; es wurde nichts gemergt.
