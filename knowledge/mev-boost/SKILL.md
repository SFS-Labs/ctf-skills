---
name: mev-boost
kind: tool
class: GO
layer: L7
repo: flashbots/mev-boost
install: "release-binary"
triggers: [mev-boost, does, work, background, installing, binaries, source, install, clone, build, default, develop]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# mev-boost — PBS-Seite

**Repo:** `flashbots/mev-boost` · **Layer:** L7 · **Klasse:** GO · **Bezogen:** ja (branch `develop`, Lizenz MIT)

## Zweck
PBS-Seite.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`mev-boost --help` (Release-Binary, falls vorhanden)

## Deutung der Ausgabe
Assertion-Verletzung mit Call-Sequenz; Coverage sagt, was überhaupt erreichbar war.

## Blinde Flecken
- wie RS: Qualitaet der Properties entscheidet, nicht die Worker-Zahl.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

