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

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/flashbots/rollup-boost mit cargo/go noetig

## Zweck
Rollup/Sequencer.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
kein Kommando — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/flashbots/rollup-boost mit cargo/go noetig; Quelle: `vendor/flashbots/rollup-boost`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

