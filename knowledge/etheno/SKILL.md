---
name: etheno
kind: tool
class: PY
layer: L5
repo: crytic/etheno
install: "uv tool"
triggers: [etheno, features, quickstart, install, system, dependencies, usage, ganache, integration, json, server, multiplexing]
pairs_with: [evm-cfg-builder, pyevmasm, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier]
---

# etheno — Bytecode zu lesbarer Struktur

**Repo:** `crytic/etheno` · **Layer:** L5 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
Bytecode zu lesbarer Struktur.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
`etheno` (via `uv tool`); Hilfe: `etheno --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`.
Nach diesem Skill weiter mit Layer L6.

