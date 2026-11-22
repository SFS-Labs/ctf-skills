---
name: oz-upgrades
kind: tool
class: JS
layer: L6
repo: OpenZeppelin/openzeppelin-upgrades
install: "npm -g"
triggers: [assets, banner.svg, openzeppelin, upgrades, height, 40px, installation, usage, plugins, work, proxy, patterns]
pairs_with: [diffusc, chainsecurity-deployment-validation, bytecode-verifier, cryo, mev-inspect-py, transaction-decoder, rbuilder]
---

# oz-upgrades — Storage-Layout-Diff bei Upgrades

**Repo:** `OpenZeppelin/openzeppelin-upgrades` · **Layer:** L6 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz MIT)

> **Bibliothek — kein eigenes CLI.** installiert; Nutzung als Modul, kein CLI

## Zweck
Storage-Layout-Diff bei Upgrades.

## Wann anwenden
wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork).

## Kommando
kein CLI — als Modul einbinden; Import-Test (ob er gelingt, misst `bin/doctor`): `NODE_PATH=$(npm root -g) node -e "require('@openzeppelin/upgrades-core')"`

## Deutung der Ausgabe
keine Ausgabe — die Bibliothek wird aus eigenem Code aufgerufen.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- findet keine Altlasten, die schon immer da waren.

## Kombination (pairs_with)
Zusammen mit: `diffusc`, `chainsecurity-deployment-validation`, `bytecode-verifier`, `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`.
Nach diesem Skill weiter mit Layer L7.

