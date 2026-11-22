---
name: evm-cfg-builder
kind: tool
class: PY
layer: L5
repo: crytic/evm_cfg_builder
install: "uv tool"
triggers: [builder, features, usage, command-line, library, install, using, requirements, getting, help, license, L5]
pairs_with: [pyevmasm, etheno, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier]
---

# evm-cfg-builder — CFG-Recovery aus Bytecode

**Repo:** `crytic/evm_cfg_builder` · **Layer:** L5 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
CFG-Recovery aus Bytecode.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
`evm-cfg-builder` (via `uv tool`); Hilfe: `evm-cfg-builder --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`.
Nach diesem Skill weiter mit Layer L6.

