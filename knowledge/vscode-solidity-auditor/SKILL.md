---
name: vscode-solidity-auditor
kind: tool
class: JS
layer: L2
repo: ConsenSysDiligence/vscode-solidity-auditor
install: "npm -g"
triggers: [solidity, visual, developer, features, installation, tour, ethereum, account, address, actions, semantic, function]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# vscode-solidity-auditor — Interaktive Audit-Ansicht

**Repo:** `ConsenSysDiligence/vscode-solidity-auditor` · **Layer:** L2 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz GPL-3.0)

## Zweck
Interaktive Audit-Ansicht.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
`vscode-solidity-auditor --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

