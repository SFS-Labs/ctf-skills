---
name: defender-sdk
kind: tool
class: JS
layer: L9
repo: OpenZeppelin/defender-sdk
install: "npm -g"
triggers: [logo.svg, openzeppelin, defender, packages, height, 40px, important, notice, usage, development, setup, testing]
pairs_with: [seal-911, seal-frameworks, blockchain-security-contacts, slither, surya, bytecode-verifier, slither-mcp]
---

# defender-sdk — Automatisierung/Response

**Repo:** `OpenZeppelin/defender-sdk` · **Layer:** L9 · **Klasse:** JS · **Bezogen:** ja (branch `main`, Lizenz MIT)

## Zweck
Automatisierung/Response.

## Wann anwenden
sobald ein Fund existiert: beweisen, melden, eskalieren.

## Kommando
`defender-sdk --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- ist kein Analysewerkzeug.

## Kombination
Zusammen mit: `seal-911`, `seal-frameworks`, `blockchain-security-contacts`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

