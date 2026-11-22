# Skill-Index

134 Skills · generiert 2026-11-21 04:08 · Home `/home/sfs-linux-node/ctf-skills`

Abruf: `skill list` · `skill show <slug>` · `skill find <wort>` · `skill plan <ziel>`

## L0 — immer zuerst: Scope, Rechte, Meldeweg klaeren

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `safe-harbor` | knowledge | Rechtlicher Schutzrahmen | ja |

## L1 — sobald Quellcode/Bytecode vorliegt: Karte bauen, Compiler pinnen

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `crytic-compile` | tool | Klebstoff: ein Interface fuer alle Toolchains | ja |
| `evmyullean` | source | Yul/EVM-Semantik in Lean | ja |
| `evmyullean-nethermind` | source | Fork von solidity-lean (Divergenz-Vergleich) | ja |
| `solar` | tool | Moderner Solidity-Compiler | ja |
| `solc-select` | tool | Compiler-Pinning, Reproduzierbarkeit | ja |
| `solidity-lean` | source | Formale Solidity-Semantik (Lean 4) | ja |
| `surya` | tool | Call-Graph, Inheritance, Contract-Doku | ja |

## L2 — Breite zuerst: alle In-Scope-Artefakte statisch abklopfen

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `amarna` | knowledge-archived | Move-Statik (Wissen) | ja |
| `caracal` | knowledge-archived | Cairo/StarkNet-Statik (Wissen) | ja |
| `eth-security-toolbox` | docker | Ein-Container-Werkbank (Docker-Fallback) | ja |
| `legions` | tool | Aeltere Schwachstellen-Suite | ja |
| `optik` | tool | EVM-Optimizer-/Instrumentierungs-Analyse | ja |
| `slither` | tool | Statik-Rueckgrat: Detektoren, Printer, SlithIR, Dataflow | ja |
| `slither-action` | corpus | CI-Gate-Rezept | ja |
| `slither-docs-action` | corpus | Doku-Generierung | ja |
| `slither-mcp` | tool | Slither als MCP-Server | ja |
| `solana-lints` | knowledge-archived | Solana/Anchor-Lint-Regelkatalog | ja |
| `soroban-detectors` | tool | Stellar/Soroban-Detektoren | ja |
| `tayt` | knowledge-archived | StarkNet-Analyse (Wissen) | ja |
| `tealer` | knowledge-archived | Algorand TEAL-Analyse | ja |
| `vscode-solidity-auditor` | tool | Interaktive Audit-Ansicht | ja |

## L3 — wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `attacknet` | docker | Chaos-Testing auf Kubernetes (Docker) | ja |
| `cloudexec` | docker | Verteilte Fuzz-Kampagnen (Docker) | ja |
| `daedaluzz` | tool | Coverage-gefuehrter Fuzzer | ja |
| `diligence-fuzzing` | tool | Fuzz-Harness-Generator | ja |
| `diligence-fuzzing-action` | corpus | CI-Rezept | ja |
| `echidna` | tool | Property-Fuzzer; Counterexample = Beweis | ja |
| `echidna-action` | corpus | CI-Fuzz-Rezept | ja |
| `fluxture` | tool | Contract-Fuzzing/Deployment-Infrastruktur | ja |
| `fuzz-utils` | tool | Fuzz-Harness-Hilfen | ja |
| `medusa` | tool | Coverage-Fuzzer, Go-Assertions, schnelle Breite | ja |
| `napalm` | tool | JS-Fuzzing (Off-Chain) | ja |
| `properties` | corpus | Fertige ERC20/ERC4626-Invarianten fuer Echidna | ja |
| `scribble` | tool | Spezifikation zu Runtime-Instrumentierung | ja |
| `sfs-dvca` | tool | Web3-Angriffsuebungen: Wallet/Key-Handling, Client-Flows | ja |

## L4 — wenn ein statischer Treffer einen konkreten Pfad braucht

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `manticore` | tool | Symbolische Ausfuehrung | ja |
| `manticore-ui` | knowledge-archived | GUI zu Manticore | ja |
| `mythril` | tool | Symbolische Ausfuehrung, konkrete Pfade | ja |
| `mythx-cli` | knowledge-archived | Abgeloest (API tot) | ja |

## L5 — wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment)

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `abi-guesser` | tool | ABI-Rekonstruktion ohne Quelle | ja |
| `canonical-signatures` | tool | Signatur-/Selector-Datenbank | ja |
| `etheno` | tool | Bytecode zu lesbarer Struktur | ja |
| `ethersplay` | knowledge-archived | IDA-EVM-Plugin (interaktiv) | ja |
| `evm-cfg-builder` | tool | CFG-Recovery aus Bytecode | ja |
| `evm-opcodes` | knowledge | Opcode-Referenz inkl. Gas | ja |
| `ida-evm` | knowledge-archived | IDA-EVM-Prozessor | ja |
| `pyevmasm` | tool | Assembler/Disassembler-Bausteine | ja |
| `rattle` | knowledge-archived | EVM-Bytecode-SSA-Recovery | ja |
| `reverse-skill` | knowledge | Reverse-Engineering-Methodik (CN) | ja |

## L6 — wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork)

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `bytecode-verifier` | tool | Bytecode-/Upgrade-Verifikation | ja |
| `cairo-contracts` | source | Cairo-Referenz | ja |
| `chainsecurity-deployment-validation` | tool | Deploy-Parameter-Verifikation | ja |
| `diffusc` | tool | Diff-Fuzzing alter vs. neuer Stand | ja |
| `oz-contracts` | source | Referenz-Standard; Diff-Basis | ja |
| `oz-contracts-upgradeable` | source | Upgrade-sichere Varianten | ja |
| `oz-foundry-upgrades` | tool | Storage-Layout-Diff fuer Foundry | ja |
| `oz-upgrades` | tool | Storage-Layout-Diff bei Upgrades | ja |

## L7 — wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `artemis` | knowledge-archived | MEV-Bot-Framework (Rust, eingestellt) | ja |
| `blocklists` | corpus | Adress-Blocklisten | ja |
| `cryo` | tool | On-Chain-Daten-Extraktion | ja |
| `dstack` | tool | TEE-Attestierung/Confidential Compute | ja |
| `evm-tracing-ref` | knowledge | Tracing-Felder-Referenz | ja |
| `forest` | source | Filecoin-Client (Rust) | ja |
| `go-ethereum` | source | Referenz-Client; EVM-Semantik nachschlagen | ja |
| `gossamer` | source | Polkadot-Client (Go) | ja |
| `honeypot-data` | corpus | Honeypot-/Scanner-Traffic | ja |
| `iron-proxy` | tool | Proxy-/Traffic-Ebene | ja |
| `kava` | source | Cosmos-Kette (Go) | ja |
| `lazarus-group-data` | corpus | APT-Muster | ja |
| `lodestar` | source | Consensus-Client (TS) | ja |
| `mev-boost` | tool | PBS-Seite | ja |
| `mev-boost-relay` | tool | Relay-Seite: Vertrauensannahmen | ja |
| `mev-geth` | knowledge-archived | Historisch | ja |
| `mev-inspect-py` | tool | MEV-/Angriffs-Muster aus Bloecken | ja |
| `mev-research` | knowledge | Forschungsstand MEV | ja |
| `mev-share-rs` | tool | MEV-Share-Client | ja |
| `movevm` | source | Move-VM-Interna | ja |
| `near-intents` | source | Intents-/Solver-Modell | ja |
| `openchain-monorepo` | tool | Rohdaten-Dekodierung | ja |
| `openchain-tx-viewer` | tool | Transaktions-Viewer-UI | ja |
| `oz-monitor` | tool | On-Chain-Monitoring/Alerting | ja |
| `php-src` | source | PHP-Interna (Web-Scope) | ja |
| `r55` | tool | Alternative EVM-Implementierung | ja |
| `rbuilder` | tool | Block-Building: Ordering/Inclusion | ja |
| `reth` | source | Client-Interna | ja |
| `rollup-boost` | tool | Rollup/Sequencer | ja |
| `seal-intel-sdk` | tool | Threat-Intel-Anbindung | ja |
| `slowmist-tracing` | knowledge | Mittelabfluss-Analyse | ja |
| `solidus` | knowledge-archived | Fruehe RPC/EVM-Arbeit | ja |
| `suave-geth` | knowledge-archived | SUAVE: Confidential-Compute-Konzepte | ja |
| `transaction-decoder` | tool | Transaktions-Dekodierung | ja |

## L8 — durchgehend: Musterabgleich gegen bekannte Bug-Klassen und Audit-Erfahrung

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `advisories` | corpus | Advisory-Muster | ja |
| `awesome-ethereum-security` | knowledge | Oekosystem-Landkarte | ja |
| `blockchain-security-db` | corpus | Vorfall-Datenbank | ja |
| `building-secure-contracts` | knowledge | Programmatik: Properties formulieren, Assurance-Reife | ja |
| `chainsafe-audits` | knowledge | Audit-Muster | ja |
| `chainsecurity-audits` | knowledge | Audit-Muster | ja |
| `chainsecurity-dv-files` | corpus | Damn-Vulnerable-DeFi-Challenges | ja |
| `code4rena-initia-move` | corpus | Contest-Findings mit Schweregraden | ja |
| `damn-vulnerable-defi` | tool | DeFi-Angriffs-Korpus | ja |
| `ethernaut` | tool | CTF-Korpus kanonischer Bug-Klassen | ja |
| `evm-analyzer-benchmark-suite` | corpus | Ground Truth: welches Tool findet was | ja |
| `evmbench` | tool | Benchmark mit Ground Truth | ja |
| `exploitdb` | corpus | Exploit-Korpus; Index zuerst, Volltext on demand | ja |
| `flashbots-pm` | knowledge | Projektlandkarte | ja |
| `mostly-harmless` | knowledge | Krypto-/Go-Praxiswissen | ja |
| `move-over-ctf` | source | Move-CTF-Korpus | ja |
| `not-so-smart-contracts` | knowledge | Bug-Klassen-Katalog mit Minimalbeispielen | ja |
| `openai-math` | knowledge | Mathe-Referenz (auffaellig, beim Klonen pruefen) | ja |
| `oz-skills` | knowledge | Skill-Format-Vorbild | ja |
| `paradigm-ctf-2021` | corpus | CTF-Korpus (Foundry) | ja |
| `paradigm-ctf-2022` | corpus | CTF-Korpus (Foundry) | ja |
| `paradigm-ctf-2023` | corpus | CTF-Korpus (Foundry) | ja |
| `paradigm-ctf-infra` | docker | Challenge-Deployment-Vorlage (Docker) | ja |
| `secure-development-cookbook` | knowledge | Prozess-/Checklisten-Ebene | ja |
| `sfs-awesome-crypto-security` | knowledge | Landkarte Krypto-Security | ja |
| `sfs-ctf-skills` | knowledge | CTF-Vorgehens-Skills, Format-Vorbild fuer Skill-Karten | ja |
| `slowmist-audit-guide` | knowledge | Audit-Prozess | ja |
| `slowmist-dark-forest` | knowledge | Selbstschutz/Wallet-OpSec | ja |
| `slowmist-knowledge-base` | knowledge | Bug-Klassen und Faelle | ja |
| `slowmist-roadmap` | knowledge | Curriculum, Vertiefungsreihenfolge | ja |
| `slowmist-solana-bp` | knowledge | Solana-Kanon | ja |
| `smart-contract-best-practices` | knowledge | Kanon der Praktiken | ja |
| `tob-publications` | knowledge | Audit-Erfahrung als Musterbibliothek | ja |
| `zellic-publications` | knowledge | Forschungsberichte | ja |
| `zk-eth-rng` | knowledge | ZK-/RNG-Trust-Modelle | ja |
| `zkdocs` | knowledge | ZK-Dokumentations-/Trust-Modelle | ja |

## L9 — sobald ein Fund existiert: beweisen, melden, eskalieren

| Slug | Kind | Rolle | Bezogen |
|---|---|---|---|
| `blockchain-security-contacts` | corpus | Incident-Eskalation | ja |
| `defender-sdk` | tool | Automatisierung/Response | ja |
| `drill-template` | knowledge | Notfall-Uebungsvorlage | ja |
| `seal-911` | knowledge | Incident-Response-Kontakte | ja |
| `seal-frameworks` | knowledge | SEAL-Frameworks (Krisenmanagement) | ja |
| `verifiable-phishing-reporter` | tool | Meldeweg | ja |

