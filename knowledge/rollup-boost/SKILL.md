---
name: rollup-boost
kind: tool
class: RS
layer: L7
repo: flashbots/rollup-boost
install: "release-binary"
triggers: [rollup, boost, usage, command-line, options, environment, variables, example, core, system, workflow, calls]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# rollup-boost — Rollup/Sequencer

**Repo:** `flashbots/rollup-boost` · **Layer:** L7 · **Klasse:** RS · **Bezogen:** ja (branch `main`, Lizenz MIT)

## Zweck
Rollup/Sequencer.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`rollup-boost --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

