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

> **Bibliothek — kein eigenes CLI.** installiert; Nutzung als Modul, kein CLI

## Zweck
Automatisierung/Response.

## Wann anwenden
sobald ein Fund existiert: beweisen, melden, eskalieren.

## Kommando
kein CLI — als Modul einbinden; Import-Test (ob er gelingt, misst `bin/doctor`): `NODE_PATH=$(npm root -g) node -e "require('@openzeppelin/defender-sdk')"`

## Deutung der Ausgabe
keine Ausgabe — die Bibliothek wird aus eigenem Code aufgerufen.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- ist kein Analysewerkzeug.

## Kombination (pairs_with)
Zusammen mit: `seal-911`, `seal-frameworks`, `blockchain-security-contacts`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

