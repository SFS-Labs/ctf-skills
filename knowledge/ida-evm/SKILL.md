---
name: ida-evm
kind: knowledge-archived
class: ARCH
layer: L5
repo: crytic/ida-evm
install: "keine Installation (archiviert, Wissen only)"
triggers: [ida-evm, installation, L5]
pairs_with: [evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation]
---

# ida-evm — IDA-EVM-Prozessor

**Repo:** `crytic/ida-evm` · **Layer:** L5 · **Klasse:** ARCH · **Bezogen:** ja (branch `master`, Lizenz Apache-2.0)

## Zweck
IDA-EVM-Prozessor.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
kein Kommando — Regeln/Ideen entnehmen, Tool nicht betreiben

## Deutung der Ausgabe
Historische Regeln; Detektoren können veraltet sein.

## Blinde Flecken
- Original ist archiviert/ueberholt: Regeln und Ideen nutzen, nicht betreiben.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`.
Nach diesem Skill weiter mit Layer L6.

