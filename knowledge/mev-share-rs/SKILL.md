---
name: mev-share-rs
kind: tool
class: RS
layer: L7
repo: paradigmxyz/mev-share-rs
install: "release-binary"
triggers: [mev-share-rs, server-sent-events, sending, bundles, license, share, L7]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# mev-share-rs — MEV-Share-Client

**Repo:** `paradigmxyz/mev-share-rs` · **Layer:** L7 · **Klasse:** RS · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/paradigmxyz/mev-share-rs

## Zweck
MEV-Share-Client.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
kein Kommando — Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/paradigmxyz/mev-share-rs; Quelle: `vendor/paradigmxyz/mev-share-rs`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

