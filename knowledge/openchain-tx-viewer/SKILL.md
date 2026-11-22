---
name: openchain-tx-viewer
kind: tool
class: JS
layer: L7
repo: openchainxyz/ethereum-transaction-viewer-frontend
install: "npm -g"
triggers: [ethereum-tracing-srv, frontend, openchain, viewer, L7]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# openchain-tx-viewer — Transaktions-Viewer-UI

**Repo:** `openchainxyz/ethereum-transaction-viewer-frontend` · **Layer:** L7 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz None)

## Zweck
Transaktions-Viewer-UI.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`openchain-tx-viewer --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

