---
name: oz-contracts
kind: source
class: SRC
layer: L6
repo: OpenZeppelin/openzeppelin-contracts
install: "keine Installation (Quell-Referenz)"
triggers: [logo.svg, openzeppelin, height, 40px, overview, release, tags, installation, usage, learn, more, security]
pairs_with: [diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier, cryo, mev-inspect-py, transaction-decoder, rbuilder]
---

# oz-contracts — Referenz-Standard; Diff-Basis

**Repo:** `OpenZeppelin/openzeppelin-contracts` · **Layer:** L6 · **Klasse:** SRC · **Bezogen:** ja (branch `master`, Lizenz MIT)

## Zweck
Referenz-Standard; Diff-Basis.

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

