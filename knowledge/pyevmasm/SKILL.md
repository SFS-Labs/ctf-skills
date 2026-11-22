---
name: pyevmasm
kind: tool
class: PY
layer: L5
repo: crytic/pyevmasm
install: "uv tool"
triggers: [pyevmasm, examples, evmasm, python, installation, documentation, L5]
pairs_with: [evm-cfg-builder, etheno, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier]
---

# pyevmasm — Assembler/Disassembler-Bausteine

**Repo:** `crytic/pyevmasm` · **Layer:** L5 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz Apache-2.0)

## Zweck
Assembler/Disassembler-Bausteine.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
`pyevmasm` (via `uv tool`); Hilfe: `pyevmasm --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination
Zusammen mit: `evm-cfg-builder`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`.
Nach diesem Skill weiter mit Layer L6.

