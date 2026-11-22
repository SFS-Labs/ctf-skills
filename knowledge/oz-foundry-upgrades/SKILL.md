---
name: oz-foundry-upgrades
kind: tool
class: JS
layer: L6
repo: OpenZeppelin/openzeppelin-foundry-upgrades
install: "npm -g"
triggers: [openzeppelin, foundry, upgrades, installing, using, contracts, optional, alternative, installation, methods, defender, integration]
pairs_with: [diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier, cryo, mev-inspect-py, transaction-decoder, rbuilder]
---

# oz-foundry-upgrades — Storage-Layout-Diff fuer Foundry

**Repo:** `OpenZeppelin/openzeppelin-foundry-upgrades` · **Layer:** L6 · **Klasse:** JS · **Bezogen:** ja (branch `main`, Lizenz MIT)

> **Bibliothek — kein eigenes CLI.** installiert; Nutzung als Modul, kein CLI

## Zweck
Storage-Layout-Diff fuer Foundry.

## Wann anwenden
wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork).

## Kommando
kein CLI — als Modul einbinden; Import-Test (ob er gelingt, misst `bin/doctor`): `NODE_PATH=$(npm root -g) node -e "require('@openzeppelin/foundry-upgrades')"`

## Deutung der Ausgabe
keine Ausgabe — die Bibliothek wird aus eigenem Code aufgerufen.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- findet keine Altlasten, die schon immer da waren.

## Kombination (pairs_with)
Zusammen mit: `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`, `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`.
Nach diesem Skill weiter mit Layer L7.

