# Skill-Index

133 Skills · generiert 2026-11-21 08:24 · Home `/home/sfs-linux-node/ctf-skills`

Abruf: `skill list` · `skill show <slug>` · `skill find <wort>` · `skill plan <ziel>`

## L0 — immer zuerst: Scope, Rechte, Meldeweg klaeren

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `safe-harbor` | knowledge | wissen | Rechtlicher Schutzrahmen | ja |

## L1 — sobald Quellcode/Bytecode vorliegt: Karte bauen, Compiler pinnen

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `crytic-compile` | tool | binary | Klebstoff: ein Interface fuer alle Toolchains | ja |
| `evmyullean` | source | quelle | Yul/EVM-Semantik in Lean · Alias: evmyullean-nethermind | ja |
| `solar` | tool | binary | Moderner Solidity-Compiler | ja |
| `solc-select` | tool | binary | Compiler-Pinning, Reproduzierbarkeit | ja |
| `solidity-lean` | source | quelle | Formale Solidity-Semantik (Lean 4) | ja |
| `surya` | tool | binary | Call-Graph, Inheritance, Contract-Doku | ja |

## L2 — Breite zuerst: alle In-Scope-Artefakte statisch abklopfen

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `amarna` | knowledge-archived | referenz | Move-Statik (Wissen) | ja |
| `caracal` | knowledge-archived | referenz | Cairo/StarkNet-Statik (Wissen) | ja |
| `eth-security-toolbox` | docker | referenz | Ein-Container-Werkbank (Docker-Fallback) | ja |
| `legions` | tool | binary | Aeltere Schwachstellen-Suite | ja |
| `optik` | tool | referenz | EVM-Optimizer-/Instrumentierungs-Analyse | ja |
| `slither` | tool | binary | Statik-Rueckgrat: Detektoren, Printer, SlithIR, Dataflow | ja |
| `slither-action` | corpus | korpus | CI-Gate-Rezept | ja |
| `slither-docs-action` | corpus | korpus | Doku-Generierung | ja |
| `slither-mcp` | tool | binary | Slither als MCP-Server | ja |
| `solana-lints` | knowledge-archived | referenz | Solana/Anchor-Lint-Regelkatalog | ja |
| `soroban-detectors` | tool | referenz | Stellar/Soroban-Detektoren | ja |
| `tayt` | knowledge-archived | referenz | StarkNet-Analyse (Wissen) | ja |
| `tealer` | knowledge-archived | referenz | Algorand TEAL-Analyse | ja |
| `vscode-solidity-auditor` | tool | referenz | Interaktive Audit-Ansicht | ja |

## L3 — wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `attacknet` | docker | referenz | Chaos-Testing auf Kubernetes (Docker) | ja |
| `cloudexec` | docker | referenz | Verteilte Fuzz-Kampagnen (Docker) | ja |
| `daedaluzz` | tool | binary | Coverage-gefuehrter Fuzzer | ja |
| `diligence-fuzzing` | tool | referenz | Fuzz-Harness-Generator | ja |
| `diligence-fuzzing-action` | corpus | korpus | CI-Rezept | ja |
| `echidna` | tool | binary | Property-Fuzzer; Counterexample = Beweis | ja |
| `echidna-action` | corpus | korpus | CI-Fuzz-Rezept | ja |
| `fluxture` | tool | referenz | Contract-Fuzzing/Deployment-Infrastruktur | ja |
| `fuzz-utils` | tool | binary | Fuzz-Harness-Hilfen | ja |
| `medusa` | tool | binary | Coverage-Fuzzer, Go-Assertions, schnelle Breite | ja |
| `napalm` | tool | referenz | JS-Fuzzing (Off-Chain) | ja |
| `properties` | corpus | korpus | Fertige ERC20/ERC4626-Invarianten fuer Echidna | ja |
| `scribble` | tool | binary | Spezifikation zu Runtime-Instrumentierung | ja |
| `sfs-dvca` | tool | referenz | Web3-Angriffsuebungen: Wallet/Key-Handling, Client-Flows | ja |

## L4 — wenn ein statischer Treffer einen konkreten Pfad braucht

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `manticore` | tool | referenz | Symbolische Ausfuehrung | ja |
| `manticore-ui` | knowledge-archived | referenz | GUI zu Manticore | ja |
| `mythril` | tool | binary | Symbolische Ausfuehrung, konkrete Pfade | ja |
| `mythx-cli` | knowledge-archived | referenz | Abgeloest (API tot) | ja |

## L5 — wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment)

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `abi-guesser` | tool | referenz | ABI-Rekonstruktion ohne Quelle | ja |
| `canonical-signatures` | tool | referenz | Signatur-/Selector-Datenbank | ja |
| `etheno` | tool | binary | Bytecode zu lesbarer Struktur | ja |
| `ethersplay` | knowledge-archived | referenz | IDA-EVM-Plugin (interaktiv) | ja |
| `evm-cfg-builder` | tool | binary | CFG-Recovery aus Bytecode | ja |
| `evm-opcodes` | knowledge | wissen | Opcode-Referenz inkl. Gas | ja |
| `ida-evm` | knowledge-archived | referenz | IDA-EVM-Prozessor | ja |
| `pyevmasm` | tool | binary | Assembler/Disassembler-Bausteine | ja |
| `rattle` | knowledge-archived | referenz | EVM-Bytecode-SSA-Recovery | ja |
| `reverse-skill` | knowledge | wissen | Reverse-Engineering-Methodik (CN) | ja |

## L6 — wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork)

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `bytecode-verifier` | tool | referenz | Bytecode-/Upgrade-Verifikation | ja |
| `cairo-contracts` | source | quelle | Cairo-Referenz | ja |
| `chainsecurity-deployment-validation` | tool | referenz | Deploy-Parameter-Verifikation | ja |
| `diffusc` | tool | binary | Diff-Fuzzing alter vs. neuer Stand | ja |
| `oz-contracts` | source | quelle | Referenz-Standard; Diff-Basis | ja |
| `oz-contracts-upgradeable` | source | quelle | Upgrade-sichere Varianten | ja |
| `oz-foundry-upgrades` | tool | bibliothek | Storage-Layout-Diff fuer Foundry | ja |
| `oz-upgrades` | tool | bibliothek | Storage-Layout-Diff bei Upgrades | ja |

## L7 — wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `artemis` | knowledge-archived | referenz | MEV-Bot-Framework (Rust, eingestellt) | ja |
| `blocklists` | corpus | korpus | Adress-Blocklisten | ja |
| `cryo` | tool | binary | On-Chain-Daten-Extraktion | ja |
| `dstack` | tool | referenz | TEE-Attestierung/Confidential Compute | ja |
| `evm-tracing-ref` | knowledge | wissen | Tracing-Felder-Referenz | ja |
| `forest` | source | quelle | Filecoin-Client (Rust) | ja |
| `go-ethereum` | source | quelle | Referenz-Client; EVM-Semantik nachschlagen | ja |
| `gossamer` | source | quelle | Polkadot-Client (Go) | ja |
| `honeypot-data` | corpus | korpus | Honeypot-/Scanner-Traffic | ja |
| `iron-proxy` | tool | binary | Proxy-/Traffic-Ebene | ja |
| `kava` | source | quelle | Cosmos-Kette (Go) | ja |
| `lazarus-group-data` | corpus | korpus | APT-Muster | ja |
| `lodestar` | source | quelle | Consensus-Client (TS) | ja |
| `mev-boost` | tool | binary | PBS-Seite | ja |
| `mev-boost-relay` | tool | referenz | Relay-Seite: Vertrauensannahmen | ja |
| `mev-geth` | knowledge-archived | referenz | Historisch | ja |
| `mev-inspect-py` | tool | binary | MEV-/Angriffs-Muster aus Bloecken | ja |
| `mev-research` | knowledge | wissen | Forschungsstand MEV | ja |
| `mev-share-rs` | tool | referenz | MEV-Share-Client | ja |
| `movevm` | source | quelle | Move-VM-Interna | ja |
| `near-intents` | source | quelle | Intents-/Solver-Modell | ja |
| `openchain-monorepo` | tool | referenz | Rohdaten-Dekodierung | ja |
| `openchain-tx-viewer` | tool | referenz | Transaktions-Viewer-UI | ja |
| `oz-monitor` | tool | referenz | On-Chain-Monitoring/Alerting | ja |
| `php-src` | source | quelle | PHP-Interna (Web-Scope) | ja |
| `r55` | tool | referenz | Alternative EVM-Implementierung | ja |
| `rbuilder` | tool | binary | Block-Building: Ordering/Inclusion | ja |
| `reth` | source | quelle | Client-Interna | ja |
| `rollup-boost` | tool | referenz | Rollup/Sequencer | ja |
| `seal-intel-sdk` | tool | referenz | Threat-Intel-Anbindung | ja |
| `slowmist-tracing` | knowledge | wissen | Mittelabfluss-Analyse | ja |
| `solidus` | knowledge-archived | referenz | Fruehe RPC/EVM-Arbeit | ja |
| `suave-geth` | knowledge-archived | referenz | SUAVE: Confidential-Compute-Konzepte | ja |
| `transaction-decoder` | tool | referenz | Transaktions-Dekodierung | ja |

## L8 — durchgehend: Musterabgleich gegen bekannte Bug-Klassen und Audit-Erfahrung

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `advisories` | corpus | korpus | Advisory-Muster | ja |
| `awesome-ethereum-security` | knowledge | wissen | Oekosystem-Landkarte | ja |
| `blockchain-security-db` | corpus | korpus | Vorfall-Datenbank | ja |
| `building-secure-contracts` | knowledge | wissen | Programmatik: Properties formulieren, Assurance-Reife | ja |
| `chainsafe-audits` | knowledge | wissen | Audit-Muster | ja |
| `chainsecurity-audits` | knowledge | wissen | Audit-Muster | ja |
| `chainsecurity-dv-files` | corpus | korpus | Damn-Vulnerable-DeFi-Challenges | ja |
| `code4rena-initia-move` | corpus | korpus | Contest-Findings mit Schweregraden | ja |
| `damn-vulnerable-defi` | tool | referenz | DeFi-Angriffs-Korpus | ja |
| `ethernaut` | tool | referenz | CTF-Korpus kanonischer Bug-Klassen | ja |
| `evm-analyzer-benchmark-suite` | corpus | korpus | Ground Truth: welches Tool findet was | ja |
| `evmbench` | tool | referenz | Benchmark mit Ground Truth | ja |
| `exploitdb` | corpus | korpus | Exploit-Korpus; Index zuerst, Volltext on demand | ja |
| `flashbots-pm` | knowledge | wissen | Projektlandkarte | ja |
| `mostly-harmless` | knowledge | wissen | Krypto-/Go-Praxiswissen | ja |
| `move-over-ctf` | source | quelle | Move-CTF-Korpus | ja |
| `not-so-smart-contracts` | knowledge | wissen | Bug-Klassen-Katalog mit Minimalbeispielen | ja |
| `openai-math` | knowledge | wissen | Mathe-Referenz (auffaellig, beim Klonen pruefen) | ja |
| `oz-skills` | knowledge | wissen | Skill-Format-Vorbild | ja |
| `paradigm-ctf-2021` | corpus | korpus | CTF-Korpus (Foundry) | ja |
| `paradigm-ctf-2022` | corpus | korpus | CTF-Korpus (Foundry) | ja |
| `paradigm-ctf-2023` | corpus | korpus | CTF-Korpus (Foundry) | ja |
| `paradigm-ctf-infra` | docker | referenz | Challenge-Deployment-Vorlage (Docker) | ja |
| `secure-development-cookbook` | knowledge | wissen | Prozess-/Checklisten-Ebene | ja |
| `sfs-awesome-crypto-security` | knowledge | wissen | Landkarte Krypto-Security | ja |
| `sfs-ctf-skills` | knowledge | wissen | CTF-Vorgehens-Skills, Format-Vorbild fuer Skill-Karten | ja |
| `slowmist-audit-guide` | knowledge | wissen | Audit-Prozess | ja |
| `slowmist-dark-forest` | knowledge | wissen | Selbstschutz/Wallet-OpSec | ja |
| `slowmist-knowledge-base` | knowledge | wissen | Bug-Klassen und Faelle | ja |
| `slowmist-roadmap` | knowledge | wissen | Curriculum, Vertiefungsreihenfolge | ja |
| `slowmist-solana-bp` | knowledge | wissen | Solana-Kanon | ja |
| `smart-contract-best-practices` | knowledge | wissen | Kanon der Praktiken | ja |
| `tob-publications` | knowledge | wissen | Audit-Erfahrung als Musterbibliothek | ja |
| `zellic-publications` | knowledge | wissen | Forschungsberichte | ja |
| `zk-eth-rng` | knowledge | wissen | ZK-/RNG-Trust-Modelle | ja |
| `zkdocs` | knowledge | wissen | ZK-Dokumentations-/Trust-Modelle | ja |

## L9 — sobald ein Fund existiert: beweisen, melden, eskalieren

| Slug | Kind | Status | Rolle | Bezogen |
|---|---|---|---|---|
| `blockchain-security-contacts` | corpus | korpus | Incident-Eskalation | ja |
| `defender-sdk` | tool | bibliothek | Automatisierung/Response | ja |
| `drill-template` | knowledge | wissen | Notfall-Uebungsvorlage | ja |
| `seal-911` | knowledge | wissen | Incident-Response-Kontakte | ja |
| `seal-frameworks` | knowledge | wissen | SEAL-Frameworks (Krisenmanagement) | ja |
| `verifiable-phishing-reporter` | tool | referenz | Meldeweg | ja |

<!-- toolstatus:begin -->

## Ausfuehrbarkeit (gemessen 2026-11-21 11:18)

22 ausfuehrbar · 3 Bibliothek · 26 Referenz · 0 FAIL — Details, Gruende und Blocker in `STATUS.md`.
<!-- toolstatus:end -->
