---
name: evm-opcodes
kind: knowledge
class: DOC
layer: L5
repo: crytic/evm-opcodes
install: "keine Installation"
triggers: [ethereum, opcodes, instruction, reference, notes, table, details, pushx, call, L5]
pairs_with: [evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation]
---

# evm-opcodes — Opcode-Referenz inkl. Gas

**Repo:** `crytic/evm-opcodes` · **Layer:** L5 · **Klasse:** DOC · **Bezogen:** ja (branch `master`, Lizenz Apache-2.0)

## Zweck
Opcode-Referenz inkl. Gas.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
kein Kommando — Karte lesen, Regel auf das Ziel abbilden

## Deutung der Ausgabe
Text ist Muster, keine Messung: auf das Ziel abbilden und gegen Code prüfen.

## Blinde Flecken
- kein ausfuehrbares Artefakt; Wissen muss aktiv auf das Ziel abgebildet werden.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`.
Nach diesem Skill weiter mit Layer L6.

