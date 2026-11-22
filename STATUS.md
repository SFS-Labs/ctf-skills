# STATUS

Stand: 2026-11-21 11:18

Gemessen von `bin/doctor` (jeder Eintrag einzeln aufgerufen), Beweislaeufe in `VERIFICATION.md`, Reproduktion mit `bin/smoke`.
Die Spalte `install` im Manifest ist die urspruengliche Plan-Annahme; die Spalte `status` (binary/bibliothek/referenz/wissen/korpus/quelle) stammt aus `bin/tool_matrix.py`. Maszgeblich ist die Messung unten.
Sicherung: privates Repo `SFS-Labs/ctf-skill-factory`, letzter erfolgreicher Push `fcf11d7` (2026-11-21 05:42); `bin/push --check` ist erst mit gueltigem Token wieder aussagekraeftig.
`vendor/`, `venvs/`, `tools/`, `logs/` liegen bewusst **nicht** im Repo.

## Rechnung: 133 Plansoll, 134 Quellen, 133 Skills

| Groesse | gemessen |
|---|---|
| Plansoll aus dem Plan (Phase 1) | 133 |
| Datenzeilen in `repos.tsv` (Quellen) | 134 |
| davon eigenstaendige Skills | 133 |
| davon Alias-Zeilen (kein eigener Skill) | 1 |
| eindeutige Repos | 134 |
| Manifest-Slugs | 133 |
| vendor-Baeume | 133 |
| Wissenskarten | 133 |
| Plansoll - Manifest | 0 |


### Aliasse — gepinnt, nicht behauptet

Jede Alias-Zeile traegt ihren Beweis in `repos.tsv` Spalte 6 (`alias_of`, `tree_sha256`, `files`). `bin/doctor` rechnet den Digest bei jedem Lauf ueber den aktuellen `vendor/`-Baum; `bin/alias-check` vergleicht denselben Digest gegen den Remote (anonym, ohne Token).

| Alias | Ziel | tree_sha256 (gepinnt) | Dateien | Baum jetzt |
|---|---|---|---|---|
| `evmyullean-nethermind` | `evmyullean` | `f27de34679ad5b6573a3ff387f14405b88f7bb98eb8fcc4c54a9a156c1210126` | 109 | stimmt (f27de34679ad…) |

- `solidity-lean` bleibt ein eigener Skill (andere Semantik-Ebene); der Plan-Satz 'EVMYulLean/solidity-lean = ein Skill' war ungenau — der echte Fork ist `NethermindEth/EVMYulLean` -> `paradigmxyz/evmyullean`.

## Werkzeuge — gemessen, nicht angenommen

| Skill | Binary | Status | Antwort (erste Zeile) |
|---|---|---|---|
| `cryo` | `cryo` | OK | cryo 0.3.2 |
| `crytic-compile` | `crytic-compile` | OK | 0.4.2 |
| `daedaluzz` | `daedaluzz` | OK | daedaluzz version 0.0.1 |
| `diffusc` | `diffusc` | OK | 0.1.1 |
| `echidna` | `echidna` | OK | Echidna 2.4.0 |
| `etheno` | `etheno` | OK | ToB/v0.3.2/source/Etheno |
| `evm-cfg-builder` | `evm-cfg-builder` | OK | 0.3.1 |
| `fuzz-utils` | `fuzz-utils` | OK | 0.2.0 |
| `iron-proxy` | `iron-proxy` | OK | 0.59.0 |
| `legions` | `legions` | OK | Legion Version: v0.8.4 |
| `medusa` | `medusa` | OK | medusa version 1.5.1 |
| `mev-boost` | `mev-boost` | OK | mev-boost 1.12 |
| `mev-inspect-py` | `inspect-block` | OK | Usage: inspect-block [OPTIONS] BLOCK_NUMBER |
| `mythril` | `myth` | OK | Mythril version v0.24.8 |
| `pyevmasm` | `evmasm` | OK | usage: evmasm [-h] (-a | -d | -t) [-bi] [-bo] [-i [INPUT]] [-o [OUTPUT |
| `rbuilder` | `rbuilder` | OK | version:    v1.3.15 |
| `scribble` | `scribble` | OK | 0.7.10 |
| `slither` | `slither` | OK | 0.11.6 |
| `slither-mcp` | `slither-mcp` | OK | usage: slither-mcp [-h] [--enhanced-error-reporting] [--disable-metric |
| `solar` | `solar` | OK | solar 0.3.0-dev+commit.e7a91fc7 |
| `solc-select` | `solc-select` | OK | usage: solc-select [-h] {install,use,versions,upgrade} ... |
| `surya` | `surya` | OK | 0.4.13 |

**22 ausfuehrbar · 3 Bibliothek · 26 Referenz · 0 FAIL**

## Bibliothek (installiert, kein CLI — so gedacht)

- defender-sdk — `@openzeppelin/defender-sdk` installiert, require ok
- oz-foundry-upgrades — `@openzeppelin/foundry-upgrades` installiert, require scheitert: node:internal/modules/cjs/loader:1568 (kein CLI)
- oz-upgrades — `@openzeppelin/upgrades-core` installiert, require ok

## Referenz ohne Binary — je Eintrag der Grund

- `abi-guesser` (npm -g, L5) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `bytecode-verifier` (release-binary, L6) — Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/ConsenSysDiligence/bytecode-verifier
- `canonical-signatures` (npm -g, L5) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `chainsecurity-deployment-validation` (uv tool, L6) — Rust/Cargo-Projekt ohne Prebuilt (vendor/ChainSecurity/deployment_validation); cargo build noetig
- `damn-vulnerable-defi` (npm -g, L8) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `diligence-fuzzing` (release-binary, L3) — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/ConsenSysDiligence/diligence-fuzzing mit cargo/go noetig
- `dstack` (release-binary, L7) — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/Dstack-TEE/dstack mit cargo/go noetig
- `ethernaut` (npm -g, L8) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `evmbench` (uv tool, L8) — Web-App (frontend/backend/assets), kein CLI
- `fluxture` (release-binary, L3) — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/crytic/fluxture mit cargo/go noetig
- `manticore` (uv tool, L4) — uv tool installiert (3.9/3.10); Start scheitert an protobuf-Descriptor bzw. wasm/collections.Callable -> gepinnte Umgebung noetig
- `mev-boost-relay` (release-binary, L7) — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/flashbots/mev-boost-relay mit cargo/go noetig
- `mev-share-rs` (release-binary, L7) — Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/paradigmxyz/mev-share-rs
- `napalm` (npm -g, L3) — npm-Paket ohne bin; require scheitert (MODULE_NOT_FOUND)
- `openchain-monorepo` (npm -g, L7) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `openchain-tx-viewer` (npm -g, L7) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `optik` (release-binary, L2) — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/crytic/optik mit cargo/go noetig
- `oz-monitor` (npm -g, L7) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `r55` (release-binary, L7) — Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/r55-eth/r55
- `rollup-boost` (release-binary, L7) — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/flashbots/rollup-boost mit cargo/go noetig
- `seal-intel-sdk` (npm -g, L7) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `sfs-dvca` (npm -g, L3) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `soroban-detectors` (release-binary, L2) — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/OpenZeppelin/soroban-security-detectors-sdk mit cargo/go noetig
- `transaction-decoder` (npm -g, L7) — npm-Paket ohne bin; require scheitert (MODULE_NOT_FOUND)
- `verifiable-phishing-reporter` (npm -g, L9) — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo
- `vscode-solidity-auditor` (npm -g, L2) — VS-Code-Extension (.vsix), nicht headless aufrufbar

## Blocker (ohne Nutzerentscheidung nicht loesbar)

- **Docker-Skills** (`attacknet`, `cloudexec`, `eth-security-toolbox`, `paradigm-ctf-infra`): kein Docker auf dieser Maschine. Rezepte liegen in `recipes/*.sh`; naechster Schritt: Docker installieren (Root) oder jeweils am Zielrechner ausfuehren.
- **IDA-Plugins** (`ida-evm`): IDA Pro ist kostenpflichtig und nicht installiert. Wissen bleibt nutzbar, Betrieb nicht.
- **Git-Token**: gueltig (HTTP 200). Oeffentliche Repos lesen anonym (HTTP 200), private Schreibpfade brauchen einen neuen fine-grained PAT (Contents: Read/Write auf `SFS-Labs/ctf-skill-factory`), Ablage `~/.config/gh-token`, Eingabe per `ctf-token`.

## Bezug (geprueft)

- `133/133` Manifest-Eintraege mit Tarball-Baum und lesbarem `.fetched`-Marker
- `133/133` Wissenskarten mit allen sechs Abschnitten
- `51/51` Werkzeug-Eintraege klassifiziert (AUSFUEHRBAR/BIBLIOTHEK/REFERENZ)
- `1/1` Alias-Beweise stimmen mit dem gepinnten Digest des aktuellen Baums
- `exploitdb`: GitHub-Repo archiviert und geleert; Daten kommen vom offiziellen Nachfolger gitlab.com/exploit-database/exploitdb. Nur CSV-Index, Volltexte on demand.
- solc-Pinning: 4 Versionen installiert, aktiv 0.8.19

## Nachgezogene Werkzeuge — Lauf wiederholen

| Tool | Rezept (Setup) | Beweis-Kommando |
|---|---|---|
| `cryo` | `recipes/cryo-build.sh` | `cryo blocks --blocks 19000000 -r https://ethereum-rpc.publicnode.com -o /tmp/cryo-out` |
| `diffusc` | `recipes/diffusc-setup.sh` | `diffusc VaultV1.sol VaultV2.sol -d /tmp/out` (Dateiname = Contract-Name) |
| `daedaluzz` | `recipes/daedaluzz-build.sh` | `cd /tmp && daedaluzz` → `generated-maze.sol` |
| `slither` | `recipes/slither-vendor.sh` | `recipes/slither-vendor.sh evmyullean-nethermind` (analysiert einen Contract aus `vendor/`) |

<!-- smoke:begin -->

## Letzter Smoke-Lauf — 2026-11-21 08:23

Automatisiert von `bin/smoke`: echte Laeufe in temporaeren Verzeichnissen, Artefakte inhaltlich geprueft.

| Werkzeug | Ergebnis | Dauer | Beweis (Kernausgabe) |
|---|---|---|---|
| `cryo` | OK | 0.3 s | 1 Row, 8 Spalten, block_number=19000000 (3276 B) — pyarrow-Read |
| `diffusc` | OK | 3.7 s | DiffFuzzUpgrades.sol (3254 B) + CryticConfig.yaml (92 B) |
| `daedaluzz` | OK | 0.5 s | generated-maze.sol (32560 B), solc 0.8.19 kompiliert |
| `push` | OK | 0.1 s | 6 synthetische Lecks redigiert (Token, URL-Userinfo, Bearer, Query) |

4 OK.

Wiederholen: `bin/smoke` — Kommandos im Detail: `bin/smoke --keep`.

<!-- smoke:end -->

## V8 — Orchestrator (gemessen 2026-11-22)

| Groesse | Wert |
|---|---|
| Katalogeintraege im Routing | 133 |
| Adapter | 13 (surya, slither, slither-solc, myth, solc, forge, forge-match, echidna, echidna-solc, medusa, evmasm, diffusc, cryo) |
| Tests | 49/49 OK (`SFS_V8_REAL=1` inkl. echtem Korpuslauf) |
| Prototyp-Baseline | 16/16 OK, unveraendert |
| Hauptlauf | `VERIFIED_LOCAL` — Slither 10 Detektoren (u. a. `reentrancy-eth`), 3 forge-Counterexamples, 1 Negativkontrolle, 2,9 s |
| Recovery-Lauf ohne `forge` | Compiler-Diagnose → `slither --compile-force-framework solc` 12 Befunde; Verdict `STRUCTURAL_ONLY` (keine Falsifikation durch Echidna) |
| V7/V8-Routing | Precision 0,224 → 0,586 · Recall 0,893 → 1,000 · gewaehlte Skills 11,75 → 5,38 · Fehlaktivierung ja → nein |

Blocker: Freebuff-Desktop-Build ohne CLI-Tool-Call-Hook und ohne Trace-Ausgabe; `myth` laeuft
auf diesem Node in den Timeout; `git` nicht im PATH, Token ungueltig. Details: `docs/V8-REPORT.md`.
