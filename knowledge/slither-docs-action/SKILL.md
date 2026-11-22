---
name: slither-docs-action
kind: corpus
class: DATA
layer: L2
repo: crytic/slither-docs-action
install: "keine Installation"
triggers: [document, slither, usage, options, examples, example, hardhat, foundry, docs, action, L2]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# slither-docs-action — Doku-Generierung

**Repo:** `crytic/slither-docs-action` · **Layer:** L2 · **Klasse:** DATA · **Bezogen:** ja (branch `main`, Lizenz NOASSERTION)

## Zweck
Doku-Generierung.

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

