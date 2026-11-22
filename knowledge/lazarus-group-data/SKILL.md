---
name: lazarus-group-data
kind: corpus
class: DATA
layer: L7
repo: security-alliance/lazarus-group-data
install: "keine Installation"
triggers: [lazarus, group, data, layout, validate, locally, propose, record, correction, licence, after, merge]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# lazarus-group-data — APT-Muster

**Repo:** `security-alliance/lazarus-group-data` · **Layer:** L7 · **Klasse:** DATA · **Bezogen:** ja (branch `main`, Lizenz CC-BY-4.0)

## Zweck
APT-Muster.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
kein Kommando — Daten indexieren, Muster abfragen

## Deutung der Ausgabe
Treffer sind Ähnlichkeit, kein Beweis.

## Blinde Flecken
- Datenmenge ohne Semantik: Muster erkennen, nicht blind uebernehmen.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

