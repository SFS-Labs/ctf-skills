---
name: mev-boost-relay
kind: tool
class: GO
layer: L7
repo: flashbots/mev-boost-relay
install: "release-binary"
triggers: [mev-boost, relay, also, components, dependencies, beacon, nodes, clients, security, background, usage, running]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# mev-boost-relay — Relay-Seite: Vertrauensannahmen

**Repo:** `flashbots/mev-boost-relay` · **Layer:** L7 · **Klasse:** GO · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
Relay-Seite: Vertrauensannahmen.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`mev-boost-relay --help` (Release-Binary, falls vorhanden)

## Deutung der Ausgabe
Assertion-Verletzung mit Call-Sequenz; Coverage sagt, was überhaupt erreichbar war.

## Blinde Flecken
- wie RS: Qualitaet der Properties entscheidet, nicht die Worker-Zahl.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

