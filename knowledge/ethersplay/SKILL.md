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

# ethersplay — Binary Ninja EVM-Plugin (interaktiv)

**Repo:** `crytic/ethersplay` · **Layer:** L5 · **Klasse:** ARCH · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** archiviert/ueberholt — Regeln nutzen, Tool nicht betreiben

## Zweck
EVM-Disassembler und interaktive Analyse als Plugin für **Binary Ninja**, nicht IDA Pro.

## Wann anwenden
bei Bytecode-only-Analyse, sofern Binary Ninja und kompatibles Plugin vorhanden sind. Fuer RUN-A/RUN-B mit Solidity-Quelle ist diese optionale GUI kein notwendiges Werkzeug.

## Kommando
kein Kommando — archiviert/ueberholt — Regeln nutzen, Tool nicht betreiben; Quelle: `vendor/crytic/ethersplay`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- Diese Factory-Karte ist knowledge-archived; das ist kein selbststaendiger Nachweis, dass das Upstream-GitHub-Repository archiviert ist. Binary Ninja ist als Host-Anwendung erforderlich; bei fehlender Installation ohne Ausfuehrung nur KNOWLEDGE_ONLY.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`.
Nach diesem Skill weiter mit Layer L6.

