---
name: properties
kind: corpus
class: DATA
layer: L3
repo: crytic/properties
install: "keine Installation"
triggers: [properties, testing, fuzzing, erc20, tests, uncomment, following, line, external, erc721, erc4626, L3]
pairs_with: [echidna, medusa, scribble, diligence-fuzzing, mythril, manticore]
---

# properties — Fertige ERC20/ERC4626-Invarianten fuer Echidna

**Repo:** `crytic/properties` · **Layer:** L3 · **Klasse:** DATA · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
Fertige ERC20/ERC4626-Invarianten fuer Echidna.

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
Zusammen mit: `echidna`, `medusa`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

