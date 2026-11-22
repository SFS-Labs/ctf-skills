---
name: optik
kind: tool
class: RS
layer: L2
repo: crytic/optik
install: "release-binary"
triggers: [optik, hybrid, echidna, usage, installation, runs, docker, container, mounting, local, directory, into]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# optik — EVM-Optimizer-/Instrumentierungs-Analyse

**Repo:** `crytic/optik` · **Layer:** L2 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz NOASSERTION)

## Zweck
EVM-Optimizer-/Instrumentierungs-Analyse.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
`optik --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

