---
name: rattle
kind: knowledge-archived
class: ARCH
layer: L5
repo: crytic/rattle
install: "keine Installation (archiviert, Wissen only)"
triggers: [rattle, example, usage, dependencies, troubleshooting, presentation, license, L5]
pairs_with: [evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation]
---

# rattle — EVM-Bytecode-SSA-Recovery

**Repo:** `crytic/rattle` · **Layer:** L5 · **Klasse:** ARCH · **Bezogen:** ja (branch `master`, Lizenz None)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** archiviert/ueberholt — Regeln nutzen, Tool nicht betreiben

## Zweck
EVM-Bytecode-SSA-Recovery.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
kein Kommando — archiviert/ueberholt — Regeln nutzen, Tool nicht betreiben; Quelle: `vendor/crytic/rattle`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- Original ist archiviert/ueberholt: Regeln und Ideen nutzen, nicht betreiben.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`.
Nach diesem Skill weiter mit Layer L6.

