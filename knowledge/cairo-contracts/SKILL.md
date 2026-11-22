---
name: cairo-contracts
kind: source
class: SRC
layer: L6
repo: OpenZeppelin/cairo-contracts
install: "keine Installation (Quell-Referenz)"
triggers: [openzeppelin, contracts, cairo, usage, prepare, environment, project, install, library, using, packages, learn]
pairs_with: [diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier, cryo, mev-inspect-py, transaction-decoder, rbuilder]
---

# cairo-contracts — Cairo-Referenz

**Repo:** `OpenZeppelin/cairo-contracts` · **Layer:** L6 · **Klasse:** SRC · **Bezogen:** ja (branch `main`, Lizenz MIT)

## Zweck
Cairo-Referenz.

## Wann anwenden
wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork).

## Kommando
kein Kommando — Quelle bei Semantikfragen nachschlagen

## Deutung der Ausgabe
Semantik-Nachschlagewerk: ‚was tut die EVM hier wirklich'.

## Blinde Flecken
- kein fertiges Werkzeug; Referenz zum Nachschlagen von Semantik.
- findet keine Altlasten, die schon immer da waren.

## Kombination (pairs_with)
Zusammen mit: `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`, `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`.
Nach diesem Skill weiter mit Layer L7.

