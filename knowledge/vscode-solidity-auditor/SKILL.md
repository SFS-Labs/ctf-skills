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

> **Referenzkarte — kein Betrieb auf dieser Maschine.** VS-Code-Extension (.vsix), nicht headless aufrufbar

## Zweck
Interaktive Audit-Ansicht.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
kein Kommando — VS-Code-Extension (.vsix), nicht headless aufrufbar; Quelle: `vendor/ConsenSysDiligence/vscode-solidity-auditor`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination (pairs_with)
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

