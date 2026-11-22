---
name: medusa
kind: tool
class: GO
layer: L3
repo: crytic/medusa
install: "release-binary"
triggers: [medusa, features, documentation, install, contributing, license, L3]
pairs_with: [echidna, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# medusa — Coverage-Fuzzer, Go-Assertions, schnelle Breite

**Repo:** `crytic/medusa` · **Layer:** L3 · **Klasse:** GO · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
Coverage-Fuzzer, Go-Assertions, schnelle Breite.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`medusa --help` (Release-Binary, falls vorhanden)

## Deutung der Ausgabe
Assertion-Verletzung mit Call-Sequenz; Coverage sagt, was überhaupt erreichbar war.

## Blinde Flecken
- wie RS: Qualitaet der Properties entscheidet, nicht die Worker-Zahl.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `echidna`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

