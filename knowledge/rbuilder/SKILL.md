---
name: rbuilder
kind: tool
class: RS
layer: L7
repo: flashbots/rbuilder
install: "release-binary"
triggers: [rbuilder, running, backtesting, live, benchmarking, testing, fake, relay, end-to-end, local, replaces, home]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# rbuilder — Block-Building: Ordering/Inclusion

**Repo:** `flashbots/rbuilder` · **Layer:** L7 · **Klasse:** RS · **Bezogen:** ja (branch `develop`, Lizenz Apache-2.0)

## Zweck
Block-Building: Ordering/Inclusion.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`rbuilder --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

