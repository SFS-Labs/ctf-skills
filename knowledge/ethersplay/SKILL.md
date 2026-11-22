---
name: ethersplay
kind: knowledge-archived
class: ARCH
layer: L5
repo: crytic/ethersplay
install: "keine Installation (archiviert, Wissen only)"
triggers: [ethersplay, installation, plugin, manager, manual, plugins, render, flowgraphs, manticore, coverage, L5]
pairs_with: [evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation]
---

# ethersplay — IDA-EVM-Plugin (interaktiv)

**Repo:** `crytic/ethersplay` · **Layer:** L5 · **Klasse:** ARCH · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
IDA-EVM-Plugin (interaktiv).

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

