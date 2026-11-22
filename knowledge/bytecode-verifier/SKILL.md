---
name: bytecode-verifier
kind: tool
class: RS
layer: L6
repo: ConsenSysDiligence/bytecode-verifier
install: "release-binary"
triggers: [bytecode, verifier, installation, quick, usage, ethv, verify, chainchoice, list, compiler, contributing, acknowledgement]
pairs_with: [diffusc, oz-upgrades, chainsecurity-deployment-validation, cryo, mev-inspect-py, transaction-decoder, rbuilder]
---

# bytecode-verifier — Bytecode-/Upgrade-Verifikation

**Repo:** `ConsenSysDiligence/bytecode-verifier` · **Layer:** L6 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz None)

## Zweck
Bytecode-/Upgrade-Verifikation.

## Wann anwenden
wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork).

## Kommando
`bytecode-verifier --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- findet keine Altlasten, die schon immer da waren.

## Kombination
Zusammen mit: `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`.
Nach diesem Skill weiter mit Layer L7.

