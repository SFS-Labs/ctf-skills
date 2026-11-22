---
name: diligence-fuzzing-action
kind: corpus
class: DATA
layer: L3
repo: ConsenSysDiligence/diligence-fuzzing-github-action
install: "keine Installation"
triggers: [diligence, fuzzing, action, usage, configuration, inputs, L3]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# diligence-fuzzing-action — CI-Rezept

**Repo:** `ConsenSysDiligence/diligence-fuzzing-github-action` · **Layer:** L3 · **Klasse:** DATA · **Bezogen:** ja (branch `main`, Lizenz None)

## Zweck
CI-Rezept.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
kein Kommando — Daten indexieren, Muster abfragen

## Deutung der Ausgabe
Treffer sind Ähnlichkeit, kein Beweis.

## Blinde Flecken
- Datenmenge ohne Semantik: Muster erkennen, nicht blind uebernehmen.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

