---
name: iron-proxy
kind: tool
class: RS
layer: L7
repo: paradigmxyz/iron-proxy
install: "release-binary"
triggers: [iron-proxy, problem, does, installation, quick, start, production, usage, generate, create, docker, network]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# iron-proxy — Proxy-/Traffic-Ebene

**Repo:** `paradigmxyz/iron-proxy` · **Layer:** L7 · **Klasse:** RS · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

## Zweck
Proxy-/Traffic-Ebene.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`iron-proxy --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

