---
name: slither-action
kind: corpus
class: DATA
layer: L2
repo: crytic/slither-action
install: "keine Installation"
triggers: [slither, action, options, advanced, compilation, fail, behavior, using, different, version, triaging, results]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# slither-action — CI-Gate-Rezept

**Repo:** `crytic/slither-action` · **Layer:** L2 · **Klasse:** DATA · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
CI-Gate-Rezept.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
kein Kommando — Daten indexieren, Muster abfragen

## Deutung der Ausgabe
Treffer sind Ähnlichkeit, kein Beweis.

## Blinde Flecken
- Datenmenge ohne Semantik: Muster erkennen, nicht blind uebernehmen.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

