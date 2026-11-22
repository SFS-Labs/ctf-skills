---
name: mev-inspect-py
kind: tool
class: PY
layer: L7
repo: flashbots/mev-inspect-py
install: "uv tool"
triggers: [mev-inspect-py, install, dependencies, monolithic, non-kubernetes, instructions, usage, inspect, single, block, many, blocks]
pairs_with: [cryo, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# mev-inspect-py — MEV-/Angriffs-Muster aus Bloecken

**Repo:** `flashbots/mev-inspect-py` · **Layer:** L7 · **Klasse:** PY · **Bezogen:** ja (branch `main`, Lizenz MIT)

## Zweck
MEV-/Angriffs-Muster aus Bloecken.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`mev-inspect-py` (via `uv tool`); Hilfe: `mev-inspect-py --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

