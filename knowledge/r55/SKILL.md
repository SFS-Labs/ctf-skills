---
name: r55
kind: tool
class: RS
layer: L7
repo: r55-eth/r55
install: "release-binary"
triggers: [off-the-shelf, tooling, pure, clean, rust, smart, contracts, client, integration, relevant, links, prerequisites]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# r55 — Alternative EVM-Implementierung

**Repo:** `r55-eth/r55` · **Layer:** L7 · **Klasse:** RS · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/r55-eth/r55

## Zweck
Alternative EVM-Implementierung.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
kein Kommando — Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/r55-eth/r55; Quelle: `vendor/r55-eth/r55`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

