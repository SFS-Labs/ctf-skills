# STATUS

Stand: 2026-11-21 05:35

Verifikationsnachweis: siehe `VERIFICATION.md` (echte Laeufe, keine --help-Tests).
Sicherung: privates Repo `SFS-Labs/ctf-skill-factory`; Wiederherstellung per `git clone` + `python3 bin/fetch`.
`vendor/`, `venvs/`, `tools/`, `logs/` liegen bewusst **nicht** im Repo (siehe `README.md`).

## Ausfuehrbare Skills

| Skill | Binary | Status | Antwort |
|---|---|---|---|
| `cryo` | `cryo` | OK | cryo 0.3.2 |
| `crytic-compile` | `crytic-compile` | OK | 0.4.2 |
| `daedaluzz` | `daedaluzz` | OK | daedaluzz version 0.0.1 |
| `diffusc` | `diffusc` | OK | 0.1.1 |
| `echidna` | `echidna` | OK | Echidna 2.4.0 |
| `etheno` | `etheno` | kein CLI-Flag (Bibliothek) | antwortet auf keinen Probe-Flag — Binary vorhanden |
| `evm-cfg-builder` | `evm-cfg-builder` | kein CLI-Flag (Bibliothek) | antwortet auf keinen Probe-Flag — Binary vorhanden |
| `fuzz-utils` | `fuzz-utils` | kein CLI-Flag (Bibliothek) | antwortet auf keinen Probe-Flag — Binary vorhanden |
| `medusa` | `medusa` | OK | medusa version 1.5.1 |
| `mev-inspect-py` | `inspect-block` | kein CLI-Flag (Bibliothek) | antwortet auf keinen Probe-Flag — Binary vorhanden |
| `mythril` | `myth` | OK | Mythril version v0.24.8 |
| `pyevmasm` | `evmasm` | OK | usage: evmasm [-h] (-a | -d | -t) [-bi] [-bo] [-i [INPUT]] [-o [OUTPUT]] |
| `rbuilder` | `rbuilder` | OK | version:    v1.3.15 |
| `scribble` | `scribble` | OK | 0.7.10 |
| `slither` | `slither` | OK | 0.11.6 |
| `solc-select` | `solc-select` | OK | usage: solc-select [-h] {install,use,versions,upgrade} ... |
| `surya` | `surya` | OK | 0.4.13 |

**17 ausfuehrbar, 0 fehlgeschlagen, 83 Referenz-Skills**

## Referenz ohne Binary (bewusst)

- `advisories` (corpus, L8) — keine Installation
- `amarna` (knowledge-archived, L2) — keine Installation (archiviert, Wissen only)
- `artemis` (knowledge-archived, L7) — keine Installation (archiviert, Wissen only)
- `attacknet` (docker, L3) — docker (auf dieser Maschine nicht verfuegbar)
- `awesome-ethereum-security` (knowledge, L8) — keine Installation
- `blockchain-security-contacts` (corpus, L9) — keine Installation
- `blockchain-security-db` (corpus, L8) — keine Installation
- `blocklists` (corpus, L7) — keine Installation
- `building-secure-contracts` (knowledge, L8) — keine Installation
- `cairo-contracts` (source, L6) — keine Installation (Quell-Referenz)
- `caracal` (knowledge-archived, L2) — keine Installation (archiviert, Wissen only)
- `chainsafe-audits` (knowledge, L8) — keine Installation
- `chainsecurity-audits` (knowledge, L8) — keine Installation
- `chainsecurity-dv-files` (corpus, L8) — keine Installation
- `cloudexec` (docker, L3) — docker (auf dieser Maschine nicht verfuegbar)
- `code4rena-initia-move` (corpus, L8) — keine Installation
- `diligence-fuzzing-action` (corpus, L3) — keine Installation
- `drill-template` (knowledge, L9) — keine Installation
- `echidna-action` (corpus, L3) — keine Installation
- `eth-security-toolbox` (docker, L2) — docker (auf dieser Maschine nicht verfuegbar)
- `ethersplay` (knowledge-archived, L5) — keine Installation (archiviert, Wissen only)
- `evm-analyzer-benchmark-suite` (corpus, L8) — keine Installation
- `evm-opcodes` (knowledge, L5) — keine Installation
- `evm-tracing-ref` (knowledge, L7) — keine Installation
- `evmyullean` (source, L1) — keine Installation (Quell-Referenz)
- `evmyullean-nethermind` (source, L1) — keine Installation (Quell-Referenz)
- `exploitdb` (corpus, L8) — keine Installation
- `flashbots-pm` (knowledge, L8) — keine Installation
- `forest` (source, L7) — keine Installation (Quell-Referenz)
- `go-ethereum` (source, L7) — keine Installation (Quell-Referenz)
- `gossamer` (source, L7) — keine Installation (Quell-Referenz)
- `honeypot-data` (corpus, L7) — keine Installation
- `ida-evm` (knowledge-archived, L5) — keine Installation (archiviert, Wissen only)
- `kava` (source, L7) — keine Installation (Quell-Referenz)
- `lazarus-group-data` (corpus, L7) — keine Installation
- `lodestar` (source, L7) — keine Installation (Quell-Referenz)
- `manticore-ui` (knowledge-archived, L4) — keine Installation (archiviert, Wissen only)
- `mev-geth` (knowledge-archived, L7) — keine Installation (archiviert, Wissen only)
- `mev-research` (knowledge, L7) — keine Installation
- `mostly-harmless` (knowledge, L8) — keine Installation
- `move-over-ctf` (source, L8) — keine Installation (Quell-Referenz)
- `movevm` (source, L7) — keine Installation (Quell-Referenz)
- `mythx-cli` (knowledge-archived, L4) — keine Installation (archiviert, Wissen only)
- `near-intents` (source, L7) — keine Installation (Quell-Referenz)
- `not-so-smart-contracts` (knowledge, L8) — keine Installation
- `openai-math` (knowledge, L8) — keine Installation
- `oz-contracts` (source, L6) — keine Installation (Quell-Referenz)
- `oz-contracts-upgradeable` (source, L6) — keine Installation (Quell-Referenz)
- `oz-skills` (knowledge, L8) — keine Installation
- `paradigm-ctf-2021` (corpus, L8) — keine Installation
- `paradigm-ctf-2022` (corpus, L8) — keine Installation
- `paradigm-ctf-2023` (corpus, L8) — keine Installation
- `paradigm-ctf-infra` (docker, L8) — docker (auf dieser Maschine nicht verfuegbar)
- `php-src` (source, L7) — keine Installation (Quell-Referenz)
- `properties` (corpus, L3) — keine Installation
- `rattle` (knowledge-archived, L5) — keine Installation (archiviert, Wissen only)
- `reth` (source, L7) — keine Installation (Quell-Referenz)
- `reverse-skill` (knowledge, L5) — keine Installation
- `safe-harbor` (knowledge, L0) — keine Installation
- `seal-911` (knowledge, L9) — keine Installation
- `seal-frameworks` (knowledge, L9) — keine Installation
- `secure-development-cookbook` (knowledge, L8) — keine Installation
- `sfs-awesome-crypto-security` (knowledge, L8) — keine Installation
- `sfs-ctf-skills` (knowledge, L8) — keine Installation
- `slither-action` (corpus, L2) — keine Installation
- `slither-docs-action` (corpus, L2) — keine Installation
- `slowmist-audit-guide` (knowledge, L8) — keine Installation
- `slowmist-dark-forest` (knowledge, L8) — keine Installation
- `slowmist-knowledge-base` (knowledge, L8) — keine Installation
- `slowmist-roadmap` (knowledge, L8) — keine Installation
- `slowmist-solana-bp` (knowledge, L8) — keine Installation
- `slowmist-tracing` (knowledge, L7) — keine Installation
- `smart-contract-best-practices` (knowledge, L8) — keine Installation
- `solana-lints` (knowledge-archived, L2) — keine Installation (archiviert, Wissen only)
- `solidity-lean` (source, L1) — keine Installation (Quell-Referenz)
- `solidus` (knowledge-archived, L7) — keine Installation (archiviert, Wissen only)
- `suave-geth` (knowledge-archived, L7) — keine Installation (archiviert, Wissen only)
- `tayt` (knowledge-archived, L2) — keine Installation (archiviert, Wissen only)
- `tealer` (knowledge-archived, L2) — keine Installation (archiviert, Wissen only)
- `tob-publications` (knowledge, L8) — keine Installation
- `zellic-publications` (knowledge, L8) — keine Installation
- `zk-eth-rng` (knowledge, L8) — keine Installation
- `zkdocs` (knowledge, L8) — keine Installation

## Nachgezogene Werkzeuge — Lauf wiederholen

| Tool | Rezept (Setup) | Beweis-Kommando |
|---|---|---|
| `cryo` | `recipes/cryo-build.sh` | `cryo blocks --blocks 19000000 -r https://ethereum-rpc.publicnode.com -o /tmp/cryo-out` |
| `diffusc` | `recipes/diffusc-setup.sh` | `diffusc VaultV1.sol VaultV2.sol -d /tmp/out` (Dateiname = Contract-Name, `forge` im PATH) |
| `daedaluzz` | `recipes/daedaluzz-build.sh` | `cd /tmp && daedaluzz` → schreibt `generated-maze.sol` |

Ursachen, Patches und Rohausgaben: `VERIFICATION.md`, Abschnitt 'Nachtrag 2026-11-21'.

<!-- smoke:begin -->

## Letzter Smoke-Lauf — 2026-11-21 05:39

Automatisiert von `bin/smoke`: echte Laeufe in temporaeren Verzeichnissen, Artefakte inhaltlich geprueft.

| Werkzeug | Ergebnis | Dauer | Beweis (Kernausgabe) |
|---|---|---|---|
| `cryo` | OK | 0.2 s | 1 Row, 8 Spalten, block_number=19000000 (3276 B) — pyarrow-Read |
| `diffusc` | OK | 3.2 s | DiffFuzzUpgrades.sol (3254 B) + CryticConfig.yaml (92 B) |
| `daedaluzz` | OK | 0.4 s | generated-maze.sol (32560 B), solc 0.8.19 kompiliert |
| `push` | OK | 0.1 s | 6 synthetische Lecks redigiert (Token, URL-Userinfo, Bearer, Query) |

4 OK.

Wiederholen: `bin/smoke` — Kommandos im Detail: `bin/smoke --keep`.

<!-- smoke:end -->

## Bezug

- 134/134 Skills mit Quellstand in `vendor/`
