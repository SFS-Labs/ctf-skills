---
name: honeypot-data
kind: corpus
class: DATA
layer: L7
repo: 0x4D31/honeypot-data
install: "keine Installation"
triggers: [honeypot, datasets, reports, available, observation, data, L7]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# honeypot-data — Honeypot-/Scanner-Traffic

**Repo:** `0x4D31/honeypot-data` · **Layer:** L7 · **Klasse:** DATA · **Bezogen:** ja (branch `main`, Lizenz CC-BY-4.0)

## Zweck
Honeypot-/Scanner-Traffic.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
kein Kommando — Daten indexieren, Muster abfragen

## Deutung der Ausgabe
Treffer sind Ähnlichkeit, kein Beweis.

## Blinde Flecken
- Datenmenge ohne Semantik: Muster erkennen, nicht blind uebernehmen.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

