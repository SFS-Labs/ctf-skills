---
name: echidna-action
kind: corpus
class: DATA
layer: L3
repo: crytic/echidna-action
install: "keine Installation"
triggers: [echidna, action, inputs, outputs, examples, basic, usage, example, workflow, hardhat, foundry, L3]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# echidna-action — CI-Fuzz-Rezept

**Repo:** `crytic/echidna-action` · **Layer:** L3 · **Klasse:** DATA · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
CI-Fuzz-Rezept.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
kein Kommando — Daten indexieren, Muster abfragen

## Deutung der Ausgabe
Treffer sind Ähnlichkeit, kein Beweis.

## Blinde Flecken
- Datenmenge ohne Semantik: Muster erkennen, nicht blind uebernehmen.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

