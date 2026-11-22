---
name: surya
kind: tool
class: JS
layer: L1
repo: ConsenSysDiligence/surya
install: "npm -g"
triggers: [sūrya, solidity, inspector, getting, started, command, list, graph, ftrace, flatten, describe, inheritance]
pairs_with: [crytic-compile, solc-select, solar, slither, bytecode-verifier, slither-mcp]
---

# surya — Call-Graph, Inheritance, Contract-Doku

**Repo:** `ConsenSysDiligence/surya` · **Layer:** L1 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz Apache-2.0)

## Zweck
Call-Graph, Inheritance, Contract-Doku.

## Wann anwenden
sobald Quellcode/Bytecode vorliegt: Karte bauen, Compiler pinnen.

## Kommando
`surya --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- kennt die Absicht des Autors nicht.

## Kombination
Zusammen mit: `crytic-compile`, `solc-select`, `solar`, `slither`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

