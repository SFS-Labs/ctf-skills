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

## Zweck
Storage-Layout-Diff fuer Foundry.

## Wann anwenden
wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork).

## Kommando
`oz-foundry-upgrades --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- findet keine Altlasten, die schon immer da waren.

## Kombination
Zusammen mit: `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`, `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`.
Nach diesem Skill weiter mit Layer L7.

