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

> **Referenzkarte — kein Betrieb auf dieser Maschine.** archiviert/ueberholt — Regeln nutzen, Tool nicht betreiben

## Zweck
IDA-EVM-Plugin (interaktiv).

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
kein Kommando — archiviert/ueberholt — Regeln nutzen, Tool nicht betreiben; Quelle: `vendor/crytic/ethersplay`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- Original ist archiviert/ueberholt: Regeln und Ideen nutzen, nicht betreiben.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`.
Nach diesem Skill weiter mit Layer L6.

