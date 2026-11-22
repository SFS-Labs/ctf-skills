# Security-Skill-Index (Router)

Zweck: Ein Ziel aus einem autorisierten Bug-Bounty-/Audit-Programm nehmen und die 134 lokalen
Skills komponiert anwenden — nicht sequenziell abarbeiten, sondern Schichten kreuzen.

## Wo alles liegt

- Home: `~/ctf-skills/` (im Projekt erreichbar als `.skills`)
- Quellen: `vendor/<org>/<repo>/` (134 Repos, authentifiziert als Tarball geholt)
- Karten: `knowledge/<slug>/SKILL.md` (Zweck, wann, Kommando, Deutung, blinde Flecken)
- Manifest: `MANIFEST.yaml` / `manifest.json` · Index: `INDEX.md` · Wahrheit: `STATUS.md`
- CLI: `skill list [--layer=L2] [--kind=tool]`, `skill show <slug>`, `skill find <wort>`, `skill plan <ziel>`
- `bin/doctor` prüft jedes Binary; nur was dort grün ist, gilt als einsatzfähig.

## Neun Schichten

- **L0 Realität** — `safe-harbor`, `seal-frameworks`, `seal-911`: Scope, Rechte, Meldeweg. Immer zuerst.
- **L1 Karte** — `solc-select`, `crytic-compile`, `surya`, `solar`, `solidity-lean`: Compiler pinnen, AST/CFG/Inheritance.
- **L2 Statik** — `slither`, `slither-mcp`, `bytecode-verifier`, `solhint`: Breite über alle In-Scope-Artefakte.
- **L3 Dynamik** — `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `fuzz-utils`: Counterexamples.
- **L4 Symbolisch** — `mythril`, `manticore`: konkrete Pfade und Werte.
- **L5 Bytecode** — `evm-cfg-builder`, `evmasm` (pyevmasm), `etheno`, `rattle`, `abi-guesser`, `canonical-signatures`, `evm-opcodes`: wenn keine Quelle existiert.
- **L6 Diff** — `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`: was sich geändert hat (Upgrade, Deployment, Fork).
- **L7 Ökonomie** — `cryo`, `mev-inspect-py`, `rbuilder`, `transaction-decoder`, `blocklists`, `dstack`, `reth`, `go-ethereum`: Geld, Reihenfolge, Inclusion, Vertrauen.
- **L8 Wissen** — `not-so-smart-contracts`, `smart-contract-best-practices`, `building-secure-contracts`, `slowmist-knowledge-base`, `tob-publications`, `zellic-publications`, `ethernaut`, `damn-vulnerable-defi`, `paradigm-ctf-*`, `evmbench`: Musterabgleich.
- **L9 Prozess** — `seal-911`, `drill-template`, `blocklists`, `advisories`: beweisen, melden, eskalieren.

Fremd-VMs: Solana `solana-lints`/`slowmist-solana-bp`; Move `movevm`/`move-over-ctf`/`amarna`;
Cairo `cairo-contracts`/`caracal`/`tayt`; Algorand `tealer`; Stellar `soroban-detectors`.

## Sieben Regeln (das eigentliche Werkzeug)

1. **Zwei-Signal-Regel** — Hypothese erst verfolgen, wenn zwei unabhängige Schichten sie stützen.
2. **Beweiskraft** — Counterexample (L3) > konkreter Pfad (L4) > statischer Treffer (L2) > Muster (L8).
3. **Divergenz ist das Signal** — wenn L2 „sauber" sagt und L3 bricht, sitzt der Fehler in einer Annahme. (Belegt: Echidna fand den Bruch, Medusa nicht.)
4. **Kreuz-Trigger** — jeder L2-Fund öffnet Property (L3), Diff (L6), Muster (L8), Tracing (L7).
5. **Negativraum führen** — am Ende jeder Runde auflisten, was kein Tool adressiert: Governance, Timing, Cross-Chain, Anreize, Deployment-OpSec.
6. **Karte nach jedem Fund neu zeichnen** — neue Invariante, neuer Suchraum.
7. **Zeitbudget pro Schleife** — danach Schicht wechseln, nicht Tiefe erhöhen.

## Ablauf bei einem Programm-Link

Scope/Adressen/Chains zuerst → Quellen oder Bytecode-only feststellen → L1 Compiler pinnen →
L2+L3 parallel über alle In-Scope-Verträge → Tiefe nur wo Signale → L7 + Negativraum →
PoC mit forge (`corpora/verify` als Vorlage) → Schweregrad nach Programm-Taxonomie → Bericht mit Fix.

Nur im autorisierten Rahmen testen: keine Fremdsysteme, keine Datenexfiltration über den PoC hinaus.

## Bekannte Grenzen (Stand der Maschine)

- Docker fehlt: `attacknet`, `eth-security-toolbox`, `cloudexec`, `paradigm-ctf-infra` nur als Rezept.
- `cryo` (openssl-sys/libssl-dev), `diffusc` (braucht git), `daedaluzz` (Go-Toolchain) derzeit nicht lauffähig — als Referenz nutzen.
- Kein git: Updates laufen über `python3 bin/fetch` (Tarballs, authentifiziert).
