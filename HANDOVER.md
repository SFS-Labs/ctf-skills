# ÜBERGABE — CTF Skill Factory / Security-Research-MCP

Stand: 2026-11-21, 11:30 lokale Zeit — **Revision 3**
Arbeitsbaum: `~/ctf-skills` (Linux Mint 22.3, 4 Kerne, 7,6 GB RAM, 63 GB frei)
Dieser Bericht ist **Istzustand**, keine Erfolgsmeldung. „Revalidiert“ heißt: am 21.11. zwischen 11:15 und 11:20 erneut mit Kommando + Exitstatus geprüft. „Früher belegt“ stammt aus dem Verlauf und wurde **nicht** erneut ausgeführt.

**Revision 3 (Verifikation von Abgabe 2) korrigiert:** `scribble` ist npm (`eth-scribble` 0.7.10), nicht `uv tool`; `slither-mcp` ist Paket 2.3.2, `initialize` meldet aber FastMCP 2.14.7; `tools/list` und `tools/call` wurden mit dem exakten `ValueError` reproduziert; die unbelegte „12 Findings“-Zahl ist entfernt; `oz-foundry-upgrades` scheitert mit `MODULE_NOT_FOUND` (globales Paket), nicht „kein CLI“; „kein MCP-Code“ gilt nur für eigenen Code, nicht für `vendor/trailofbits/slither-mcp`; `bin/__pycache__` ist vorhanden und gitignored.

**Revision 2 korrigiert gegenüber Revision 1:** untracked 6 statt 5; 144 tracked = 143 modifiziert + 1 gelöscht (alte Alias-Karte); Alias ist eine Zeile, kein zweiter Vendor-Baum; `bin/push --check` braucht `GH_TOKEN`/`GITHUB_TOKEN` in der Umgebung; Freebuff-Build-Metadaten liegen in `orchestrator/build-info.json`; Bun ist ein ELF-Binary; `bin/doctor` schreibt `STATUS.md`/`INDEX.md`, `bin/smoke` schreibt `STATUS.md`/`logs/smoke.json` — beides keine reinen Lesechecks.

---

## 1. Ziel

Zwei Ziele, nacheinander:

1. **Skill-Fabrik** (abgeschlossen): 133 Security-Skills aus 134 Quellen (1 Alias) als abrufbares, komponierbares System — Manifest, Wissenskarten, Router-CLI, installierte Werkzeuge, Verifikation.
2. **Aktuelles Ziel (offen): „COMPLETE MCP DELIVERY“** — die Fabrik zu einem wirklich nutzbaren, MCP-erreichbaren Research-System machen:
   - Volltextsuche über **echte Quellinhalte** (nicht nur Metadaten),
   - belegbare Quellen-Zitate mit Repo/Pfad/Zeile,
   - Cross-Repo-Recherche + iterative Hypothesen,
   - read-only MCP-Server (stdio), registriert in Freebuff,
   - T1–T8 Abnahmetests, danach READY/PARTIAL/BLOCKED.

Nicht verhandelbar: nichts committen/pushen/PR ohne Freigabe; keine Secrets in Chat/Logs/argv; keine Vendor-Neudownloads; kein Reset/Clean des Arbeitsbaums.

---

## 2. Was unternommen wurde (Verlauf)

### Phase 0–1: Bootstrap + Quellen
- Ohne Root: `uv` 0.13.9 nach `~/.local/bin`, `foundry` (forge/cast/anvil), `npm -g` (surya, solhint, eth-scribble, OZ-Pakete), `rustup` nur als Fallback.
- **Kein Git im PATH** (das gebündelte Git 2.53.0 unter `/opt/Freebuff/resources/git/bin/git` wurde erst später gefunden) → alle 133 Bäume als codeload-Tarballs nach `vendor/<org>/<repo>/`, `.fetched`-Marker, idempotent. `bin/fetch` ist der Wiederholer.
- 134 Quellenzeilen in `repos.tsv`, **133 eigenständige Skills**, 1 Alias: `NethermindEth/EVMYulLean` → `evmyullean` (gepinnter `tree_sha256` + Dateizahl in Spalte 6, von `bin/doctor` und `bin/alias-check` nachgerechnet).
- `bin/gen_skills` erzeugt aus `bin/tool_matrix.py` (einzige PROBE/LIB/REF-Quelle): `knowledge/<slug>/SKILL.md` (133), `MANIFEST.yaml`, `manifest.json`, `INDEX.md`.

### Phase 2: Werkzeuge
- `uv tool`: slither 0.11.6, crytic-compile, solc-select, mythril, pyevmasm, evm-cfg-builder, fuzz-utils, etheno, legions, mev-inspect, slither-mcp 2.3.2, dulwich (Git-Ersatz). `scribble` 0.7.10 läuft über npm (`eth-scribble`), nicht über uv; die Manifest-Spalte `install` ist laut `STATUS.md` Plansoll und führt es als `uv tool` (Ist: npm).
- Release-Binaries: echidna 2.4.0, medusa 1.5.1, cryo 0.3.2, rbuilder 1.3.15, diffusc, daedaluzz, iron-proxy, mev-boost, solar.
- `solc-select`: 4 Compiler, aktiv 0.8.19.
- Endstand laut `STATUS.md`; am 21.11. 11:18 von `bin/doctor` erneut gemessen (Exit 0): **22 ausführbar · 3 Bibliothek · 26 Referenz · 0 FAIL** (51 Einträge klassifiziert). „Ausführbar“ heißt: Entrypoint startet/`--help`; die MCP-Tool-Ebene von `slither-mcp` ist separat kaputt (siehe MCP-Befund).

### Phase 3: Verifikation
- `VERIFICATION.md`: Slither `reentrancy-eth` + Arbitrary-Send, Mythril SWC-115, Echidna-Counterexample, Medusa-Negativbefund, Forge 3/3 — an `corpora/verify/Vulnerable.sol`.
- `bin/smoke` (letzter Lauf 08:23, `logs/smoke.json`): cryo/diffusc/daedaluzz OK + Redaktions-Selbsttest von `bin/push` (4 OK, 0 FAIL, 0 SKIP). **Achtung:** `bin/smoke` schreibt den Smoke-Block in `STATUS.md`, `bin/doctor` schreibt `STATUS.md` und `INDEX.md` neu — beides ist kein rein lesender Check.

### Reparaturen
- **GitHub-Token**: war durch Bracketed-Paste-Marker korrupt. `bin/token` bereinigt Paste-/ANSI-Sequenzen, validiert strikt, `--repair`/`--check`, trennt 401/403/404. Ergebnis: 93 Zeichen (+ Newline, 94 Bytes), Modus 0600, `~/.config/gh-token`; Auth 200 (Login `SFS-Labs`), privates Repo 200. `bin/push --check` liest den Token **nicht** selbst aus der Datei, sondern nur aus `GH_TOKEN`/`GITHUB_TOKEN`; ohne Export meldet es „keine Credentials“. Früher belegt: MATCH bei `fcf11d7`. In Revision 2 wurde der Remote-HEAD stattdessen über die GitHub-API bestätigt: HTTP 200, `fcf11d7` (Commit-Datum `2026-11-21T04:39:26Z`).
- **SSH**: iPhone-Key war aus `authorized_keys` gefallen; aus `authorized_keys.bak` zurückgeholt, Datei byte-identisch zum Backup, ShellDrop wieder funktionsfähig. Snapshot vorher: `logs/authorized_keys.pre-restore-20261121`.

### MCP-Befund (der Auslöser für das aktuelle Ziel)
- **Es gibt keinen Research-MCP-Router im Projekt.** Kein eigener `FastMCP`/`mcp.server`-Code, keine `mcp.json`, kein Prozess, kein Port. `bin/` enthält nur Fabrik-Skripte plus `__pycache__` — kein `index`/`mcp`. Fremdcode liegt in `vendor/trailofbits/slither-mcp`, ist aber nicht als Projekt-Server registriert.
- `slither-mcp` 2.3.2 (Paket; `initialize` meldet `2.14.7`, die FastMCP-Version; `mcp` 1.30.0) startet, `initialize` ist OK, aber **`tools/list` und `tools/call` crashen**: `ValueError: Circular reference detected (id repeated)` in `mcp/shared/session.py::_send_response` → `pydantic.model_dump`. Ein direkter `list_contracts`-Call mit korrektem `request`-Schema endet ebenfalls in diesem Fehler.
- Freebuff hatte zu diesem Zeitpunkt **keine** MCP-Registrierung: kein `mcpServers` in `state.json`/`project.json`, kein `~/.agents/mcp.json`; nur der Skill `ctf-skill-index` war aktiv. Dieser Skill ist ein **Account-Skill (Cloud)**, keine Datei im Repo; sein Text ist veraltet (134 Repos, cryo/diffusc/daedaluzz „nicht lauffähig“, „Kein git“).
- Damals als **PARTIAL** berichtet: Katalog 133/133, inhaltliche/MCP-Anbindung 0/133.

### Aktuelles Ziel: Stand der Umsetzung
**Noch keine Implementierung.** Der Nutzer hat die Ausführung gestartet, dann aber abgebrochen und um diesen Übergabebericht gebeten. In der Sitzung, die Revision 1 erzeugte, liefen ausschließlich lesende Kommandos (Inventar, Versionen, Git-Status via Dulwich, Asar-Strings); es wurden **keine** Dateien außer diesem Bericht angelegt/geändert. Die Revalidierung für Revision 2 hat `bin/doctor` ausgeführt; dadurch wurden `STATUS.md` und `INDEX.md` neu geschrieben (11:18) — das ist ein Schreibvorgang, kein Lesecheck.

---

## 3. Gemessener Istzustand

### 3.1 Inventar (jetzt geprüft)
| Größe | Wert | Prüfung |
|---|---|---|
| Manifest-Einträge / eindeutige Slugs / Vendor-Pfade | 133 / 133 / 133 | `manifest.json` (Key `vendor`, alle Verzeichnisse existieren) |
| Org/Repo-Verzeichnisse unter `vendor/` | 133 | `find vendor -mindepth 2 -maxdepth 2 -type d` |
| `.fetched`-Marker | 133 (alle Bäume) | `find vendor -name .fetched` |
| Wissenskarten | 133 auf Platte; HEAD hat 134 | `find knowledge -name SKILL.md`; `git ls-tree` |
| Vendor-Größe / Dateien | 9,1 GB / 301.566 | `du -sh`, `find -type f` |
| Quellenzeilen | 134 (133 Skills + 1 Alias) | `repos.tsv` |
| Freier Platz | 63 GB (70 % belegt) | `df -h` |

**Alias statt Zweitklon:** Der Alias ist eine **Zeile** in `repos.tsv`, kein eigener Vendor-Baum. Es gibt 133 Org/Repo-Verzeichnisse und 133 `.fetched`; die Zeile `evmyullean-nethermind` verweist auf `evmyullean` (`vendor/paradigmxyz/evmyullean`). Dessen Tree-Digest ist `f27de34679ad5b65…` über **109 Dateien** — `tree_digest` zählt `.fetched` nicht mit, auf Platte liegen deshalb 110 Dateien. `bin/alias-check` verglich den lokalen Baum und das Nethermind-Archiv (anonym, ohne Token): beide `f27de346…`, 109 Dateien, **0 Abweichungen**, Exit 0.

### 3.2 Was existiert **nicht**
- Kein Index: `ls bin | grep -E "mcp|index|search"` → nichts; `find` nach `*.db`/`*.sqlite`/`*.fts*` → nichts.
- Kein eigener MCP-Server-Code im Projekt (Fremdcode: `vendor/trailofbits/slither-mcp`), kein MCP-Listener (`ss -ltnp`), kein Projekt-MCP-Prozess. `pgrep -af mcp` fand bei der Prüfung nur einen fremden Codex-Prozess, keinen Server dieses Projekts.
- Kein `~/.agents/`-Verzeichnis (also auch keine `mcp.json`).
- `mcp`-SDK ist **nicht** im System-Python installiert (`ModuleNotFoundError: No module named 'mcp'`); nur im slither-mcp-Venv liegt `mcp` 1.30.0.

### 3.3 Laufzeitumgebung
| Komponente | Stand |
|---|---|
| Python | 3.12.3 (`/usr/bin/python3`), **kein pip** |
| SQLite | 3.45.1, **FTS5 verfügbar** (getestet) |
| uv | 0.13.9 in `~/.local/bin` (kann `uv venv` + `uv pip install`) |
| MCP-SDK | nur im slither-mcp-Tool-Venv: `mcp` **1.30.0** |
| slither-mcp | Paket v2.3.2; `initialize` meldet FastMCP **2.14.7** — bekannter Serialisierungsbug |
| Git | **nicht im PATH**; gebündelt: `/opt/Freebuff/resources/git/bin/git` **2.53.0** |
| Bun | `/opt/Freebuff/resources/bun/bun` (**ELF-Binary**, kein Verzeichnis) |

### 3.4 Git-Lage (via gebündeltem Git 2.53.0 geprüft)
- Branch `main`, HEAD `fcf11d7fa2ce819d4b282a9deea6a8cd1022c60b`, Remote `origin https://github.com/SFS-Labs/ctf-skill-factory.git`.
- **0 staged · 144 tracked Änderungen (143 modifiziert + 1 gelöscht) · 6 untracked**; `git diff --stat`: 144 Dateien, +1878/−752 (Stand 11:18).
- Gelöscht (unstaged): `knowledge/evmyullean-nethermind/SKILL.md` — die alte separate Alias-Karte. Der Alias `evmyullean-nethermind -> evmyullean` bleibt in `repos.tsv` und im Manifest belegt; HEAD hatte 134 Karten, auf Platte sind 133. Das ist die Alias-Bereinigung, kein Datenverlust.
- Untracked: `recipes/slither-vendor.sh`, `bin/tool_matrix.py`, `bin/token`, `bin/repos_tsv.py`, `bin/alias-check`, `HANDOVER.md` (dieser Bericht).
- Remote `main` steht auf `fcf11d7` (am 21.11. 11:18 per GitHub-API bestätigt, HTTP 200, Commit-Datum `2026-11-21T04:39:26Z`); die 144 tracked Änderungen und 6 untracked sind **nicht gepusht**.
- `.gitignore` schließt `vendor/`, `venvs/`, `tools/`, `logs/` und Secrets aus — passend für den geplanten Index (muss dort ebenfalls ergänzt werden, z. B. `index/`).

### 3.5 Freebuff Desktop (neu geprüft)
- Installation: `/opt/Freebuff` (deb, Electron), Binary `/usr/bin/freebuff` → `/opt/Freebuff/freebuff`. Paketversion laut `dpkg-query -W freebuff`: **0.0.204**; Produktstring im Asar: **„Freebuff 2.0.0“**.
- Build-Metadaten: `/opt/Freebuff/resources/orchestrator/build-info.json` → `commitSha=787e705f262120065bf3f26927406c76a4742c0c`, `builtAt=2026-11-17T18:53:23.055Z` (exakt; Revision 1 gab nur Sekunden an). Eine saubere `--version`-Ausgabe gibt es nicht (`freebuff --help` druckt nur Path-Repair/Launch-Zeilen).
- **MCP-Loader ist im Desktop-Code vorhanden** (`app.asar`, 22× `loadMCPConfig`, 55× `mcpServers`):
  - Suchpfade: `{cwd}/.agents/mcp.json`, `{cwd}/../.agents/mcp.json`, `{homedir}/.agents/mcp.json`. Die Asar-Strings bestätigen die Suffixe `/.agents/mcp.json` und `/../.agents/mcp.json`; die Home-Variante wird im Loader aus dem Home-Verzeichnis zusammengesetzt.
  - Schema: `{"mcpServers": {"name": {"command": "...", "args": [...], "env": {...}}}}` (stdio) bzw. `{"type":"http","url":...,"headers":...}`.
  - Kommentar im Code: spätere Verzeichnisse haben Vorrang; Umgebungsvariablen werden aus `process.env` aufgelöst.
- **Das ist Code-Evidenz, kein Laufzeitnachweis.** Ob die installierte Desktop-Version die Server tatsächlich startet und die Tools dem Agenten anbietet, ist **ungetestet**.
- `~/.config/freebuff-desktop/state.json` enthält keine `mcpServers`; `project.json` ebenfalls nicht.

### 3.6 Früher belegt / teilweise revalidiert
- Token gültig: `bin/doctor` am 21.11. 11:18 → HTTP 200; Datei 93 Zeichen (+ Newline, 94 Bytes), Modus 0600. `bin/push --check` wurde ohne Export ausgeführt und brach mit „keine Credentials“ ab (es liest den Token nicht selbst); Remote-HEAD stattdessen per API bestätigt (`fcf11d7`, HTTP 200). Es wurde kein Secret ausgegeben oder als Argument übergeben.
- SSH-Zugang wiederhergestellt (iPhone-Key, byte-identisch zum Backup).
- Tool-E2E-Nachweise in `VERIFICATION.md`, Smoke-Lauf 08:23 in `STATUS.md`.

---

## 4. Wo wir jetzt stehen

| Schicht | Status |
|---|---|
| Quellinventar (133 Skills, 134 Quellen, Alias-Beweis) | **fertig, verifiziert** |
| Wissenskarten / Manifest / `INDEX.md` (Katalog) / Router-CLI | **fertig** (`bin/skill list/show/find/plan`) |
| Werkzeuge (22 ausführbar, 3 Lib, 26 Referenz, 0 FAIL) | **fertig; am 21.11. 11:18 von `bin/doctor` erneut gemessen (Exit 0)** |
| Volltext-Index über Quellinhalte | **fehlt vollständig** |
| Evidence-/Cross-Source-Schicht | **fehlt** (`bin/skill find` ist Metadaten-only; `find delegatecall` → kein Treffer) |
| MCP-Server (search_sources/read_source/research_context/index_status) | **fehlt** |
| Freebuff-Registrierung + Verifikation | **fehlt** (Loader-Code vorhanden, keine Config) |
| T1–T8 | **nicht gestartet** |

Kurz: **Die Fabrik ist gebaut, der Research-MCP-Teil ist null.** Nichts davon ist kaputt — er ist einfach noch nicht implementiert.

---

## 5. Nächste Schritte (Reihenfolge für das neue Fenster)

1. **Index**: `bin/index` (Python 3.12, `sqlite3` + FTS5) über `vendor/` + `knowledge/` + `repos.tsv`/`manifest.json`.
   - Deterministische IDs (repo, relpfad), `INSERT OR REPLACE` in Transaktionen, `PRAGMA journal_mode=WAL`, `synchronous=NORMAL`.
   - Ausschlüsse: Binaries, `node_modules`, `.git`, Build-Artefakte, minifizierte/generated Dateien, >X MB.
   - Inkrementell über `(size, mtime)`/Hash; Fortschrittstabelle → Resume; Batch-Commit; `--limit`/`--repo` für Ressourcenbudget.
   - Health: erwartete 133 Repos vs. indexierte, Dateien, Chunks, Skip-Gründe, Fehler, letzter Lauf.
2. **MCP-Server**: eigenes Venv (`uv venv`, `uv pip install mcp==1.30.0`), stdio, **nur stderr** für Logs, bounded JSON, Pfad-Validierung gegen `vendor/`-Roots, Timeouts. Vier Tools wie gefordert; keine Shell, kein Netz, keine Schreibzugriffe.
3. **Registrierung**: `~/.agents/mcp.json` (global, überlebt Projektwechsel) — absolute Pfade, `cwd` korrekt, bestehende Einträge nicht löschen; vorher Backup.
4. **Tests T1–T8** mit echtem MCP-Client (nicht nur Import): `initialize` → `tools/list` → je ein `tools/call`, plus Ungültig-Eingabe und fehlende Quelle; dann frische Session (Persistenz).
5. **Regression**: `bin/skill list/show/find`, `bin/doctor`, `bin/smoke` weiter grün.
6. **Doku**: `README.md`/`STATUS.md` um Index + MCP ergänzen; `HANDOVER.md` am Ende aktualisieren.

### Fallstricke, die schon bekannt sind
- `mcp` 1.30.0 nutzt die 1.x-API (`mcp.server.fastmcp.FastMCP`), **nicht** v2-Muster. Keine FastMCP-v1-Beispiele mit v2-Interfaces mischen.
- slither-mcp-Bug darf sich nicht wiederholen: keine Objekte mit Zyklen/`__dict__`-Rekursion zurückgeben, nur primitive, JSON-serialisierbare Strukturen.
- Auf stdio darf **nichts** nach stdout außer Protokollnachrichten.
- Git nur über `/opt/Freebuff/resources/git/bin/git` (nicht im PATH); kein `git clean`, kein Reset.
- 8-GB-Knoten: Index sequenziell, Batch-Commits, kein Vollbaum im RAM.
- `daedaluzz` nur in leerem Temp-Verzeichnis starten: ohne Ziel schreibt es `generated-maze.sol` ins cwd (bei der Verifikation passiert, Datei entfernt; `bin/smoke` nutzt Temp-Verzeichnisse).
- Vendor ist gitignored — Index-Verzeichnis ebenfalls aufnehmen, nicht versehentlich committen.
- **`bin/doctor` und `bin/smoke` sind nicht read-only:** doctor schreibt `STATUS.md` + `INDEX.md`, smoke schreibt den Smoke-Block in `STATUS.md` und `logs/smoke.json`. Nach jedem Lauf Git-Status neu lesen, statt „unverändert“ anzunehmen.
- **`bin/push --check` liest den Token nicht aus `~/.config/gh-token`:** `GH_TOKEN`/`GITHUB_TOKEN` muss exportiert sein; Token niemals als Argument übergeben.
- **Alias ist eine Zeile, kein Vendor-Baum:** 133 Bäume, 134 Quellenzeilen. Keinen zweiten Klon für `NethermindEth/EVMYulLean` anlegen; `vendor/paradigmxyz/evmyullean` hat 110 Dateien inkl. `.fetched`, der Digest zählt 109.

---

## 6. Offene Blocker (unverändert, unabhängig vom MCP-Ziel)

- **Docker-Skills** (`attacknet`, `cloudexec`, `eth-security-toolbox`, `paradigm-ctf-infra`): kein Docker, nur Referenzkarten + Rezepte.
- **IDA-Plugins** (`ida-evm`): IDA Pro nicht vorhanden/kostenpflichtig.
- **`manticore`**: Start scheitert (Exit 1) an `TypeError: Descriptors cannot be created directly` (protobuf-Descriptor); `STATUS.md` nennt zusätzlich wasm/`collections.Callable`. Gepinnte Umgebung nötig.
- **`oz-foundry-upgrades`**: `require('@openzeppelin/foundry-upgrades')` scheitert mit `MODULE_NOT_FOUND` (Paket nur global installiert; kein lokales CLI).
- **26 Referenz-Einträge** (kein eigenes Binary; Gründe je Eintrag in `STATUS.md`).
- **Remote veraltet**: 144 tracked Änderungen (143 M + 1 D) + 6 untracked nicht gepusht (Push nur nach Freigabe).
- **`ctf-skill-index`-Skilltext** (Account-Skill, Cloud — keine Repo-Datei) nennt fälschlich 134 Repos, „cryo/diffusc/daedaluzz nicht lauffähig“ und „Kein git“ — veraltet; präzise wäre: 133 Skills/134 Quellen, die drei Werkzeuge laufen (Smoke 08:23), Git existiert gebündelt, aber nicht im PATH.

---

## 7. Wenn nur eine Sache zählt

Der nächste Schritt ist **nicht** „MCP registrieren“, sondern **der Index**. Ohne ihn liefert jeder MCP-Server nur Metadaten und fällt in T2 (`delegatecall` → OpenZeppelin-Treffer mit echten Zeilen) durch. Reihenfolge: Index → Health-Zahlen → MCP-Tools → Registrierung → T1–T8.

---

## 8. Revalidierungsprotokoll Revision 2/3 (21.11., 11:15–11:30)

| Prüfung | Kommando / Quelle | Ergebnis |
|---|---|---|
| Inventar | `manifest.json`, `find vendor -name .fetched`, `find knowledge -name SKILL.md` | 133 Einträge, 133 Slugs, 133 Vendor-Pfade, 133 `.fetched`, 133 Karten auf Platte (HEAD 134) |
| Vendor | `du -sh vendor`, `find vendor -type f`, `df -h` | 9,1 GB, 301.566 Dateien, 63 GB frei (70 %) |
| Alias | `bin/alias-check` | 1 Alias, lokal + remote `f27de346…`, 109 Dateien, 0 Abweichungen, Exit 0 |
| Git | `/opt/Freebuff/resources/git/bin/git status --porcelain=v1` | 0 staged, 143 M + 1 D, 6 untracked; `git diff --stat`: 144 Dateien, +1878/−752 |
| Remote | GitHub API `commits/main` (Token nur im Header, nie ausgegeben) | HTTP 200, `fcf11d7…`, Commit `2026-11-21T04:39:26Z` |
| Push-Check | `bin/push --check` ohne Export | Exit 2, „keine Credentials“ — Token wird nur aus `GH_TOKEN`/`GITHUB_TOKEN` gelesen |
| Token | `stat` + `bin/doctor` | Modus 0600, 94 Bytes (93 Zeichen + Newline), HTTP 200 |
| Werkzeuge | `bin/doctor` | Exit 0; ok=22, lib=3, ref=26, fail=0 |
| Index/MCP | `ls bin`, `find` nach DB/FTS, `ss -ltnp`, `pgrep -af mcp`, `python3 -c "import mcp"` | kein Index, kein Listener, kein Projekt-Prozess, `~/.agents` fehlt, System-Python ohne `mcp` |
| slither-mcp | Python-Client: `initialize` → `tools/list` / `tools/call` | `initialize` OK; `tools/list` und `tools/call` enden im Server-`ValueError: Circular reference detected (id repeated)`; Paket 2.3.2, `initialize` meldet 2.14.7 (FastMCP) |
| Provenienz | `uv tool list`, `npm ls -g`, `command -v scribble` | `scribble` 0.7.10 kommt von `eth-scribble` (npm), nicht aus `uv tool` |
| Freebuff | `orchestrator/build-info.json`, Asar-Strings, `state.json`/`project.json` | Commit/`builtAt` bestätigt; 22× `loadMCPConfig`, 55× `mcpServers`; 0× `mcpServers` in State/Projekt |
| Blocker | `command -v docker`, `command -v ida64`, `manticore --version` | Docker/IDA fehlen; manticore Exit 1, `TypeError: Descriptors cannot be created directly` |
| Router | `bin/skill list`, `bin/skill plan`, `bin/skill find delegatecall` | 133 Zeilen; 8 Skills im Plan; `find` ohne Treffer, Exit 0 |
| Skilltext | `ctf-skill-index` (Cloud-Skill) | 134 Repos, cryo/diffusc/daedaluzz, „Kein git“ — veraltet |

**Nicht erneut ausgeführt:** `bin/doctor` (Lauf 11:18, `logs/tool-status.json`), `bin/smoke` (letzter Lauf 08:23, `logs/smoke.json`: 4 OK / 0 FAIL), Tool-E2E in `VERIFICATION.md`, SSH-Restore. Diese bleiben „früher belegt“.
