---
name: fluxture
kind: tool
class: RS
layer: L3
repo: crytic/fluxture
install: "release-binary"
triggers: [fluxture, quickstart, usage, geolocation, topological, analysis, programmatic, interface, license, acknowledgements, L3]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# fluxture — Contract-Fuzzing/Deployment-Infrastruktur

**Repo:** `crytic/fluxture` · **Layer:** L3 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz Apache-2.0)

## Zweck
Contract-Fuzzing/Deployment-Infrastruktur.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`fluxture --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

