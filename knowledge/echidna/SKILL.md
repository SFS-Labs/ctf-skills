---
name: echidna
kind: tool
class: RS
layer: L3
repo: crytic/echidna
install: "release-binary"
triggers: [features, usage, executing, test, runner, writing, invariants, testing, modes, collecting, visualizing, coverage]
pairs_with: [medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# echidna — Property-Fuzzer; Counterexample = Beweis

**Repo:** `crytic/echidna` · **Layer:** L3 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
Property-Fuzzer; Counterexample = Beweis.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`echidna --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

