---
name: dstack
kind: tool
class: RS
layer: L7
repo: Dstack-TEE/dstack
install: "release-binary"
triggers: [open, framework, confidential, dstack, supported, platforms, features, getting, started, docker-compose.yaml, architecture, repository]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# dstack — TEE-Attestierung/Confidential Compute

**Repo:** `Dstack-TEE/dstack` · **Layer:** L7 · **Klasse:** RS · **Bezogen:** ja (branch `next`, Lizenz Apache-2.0)

## Zweck
TEE-Attestierung/Confidential Compute.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`dstack --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

