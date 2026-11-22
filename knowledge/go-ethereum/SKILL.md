---
name: go-ethereum
kind: source
class: SRC
layer: L7
repo: ethereum/go-ethereum
install: "keine Installation (Quell-Referenz)"
triggers: [ethereum, building, source, executables, running, geth, hardware, requirements, full, node, main, network]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# go-ethereum — Referenz-Client; EVM-Semantik nachschlagen

**Repo:** `ethereum/go-ethereum` · **Layer:** L7 · **Klasse:** SRC · **Bezogen:** ja (branch `master`, Lizenz LGPL-3.0)

## Zweck
Referenz-Client; EVM-Semantik nachschlagen.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
kein Kommando — Quelle bei Semantikfragen nachschlagen

## Deutung der Ausgabe
Semantik-Nachschlagewerk: ‚was tut die EVM hier wirklich'.

## Blinde Flecken
- kein fertiges Werkzeug; Referenz zum Nachschlagen von Semantik.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

