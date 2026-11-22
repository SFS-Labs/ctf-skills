---
name: diligence-fuzzing
kind: tool
class: RS
layer: L3
repo: ConsenSysDiligence/diligence-fuzzing
install: "release-binary"
triggers: [diligence, fuzzing, getting, started, installing, linux, macos, windows, basic, usage, create, configuration]
pairs_with: [echidna, medusa, properties, scribble, mythril, manticore]
---

# diligence-fuzzing — Fuzz-Harness-Generator

**Repo:** `ConsenSysDiligence/diligence-fuzzing` · **Layer:** L3 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz NOASSERTION)

## Zweck
Fuzz-Harness-Generator.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`diligence-fuzzing --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

