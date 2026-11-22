---
name: transaction-decoder
kind: tool
class: JS
layer: L7
repo: openchainxyz/transaction-decoder
install: "npm -g"
triggers: [transaction, decoder, L7]
pairs_with: [cryo, mev-inspect-py, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# transaction-decoder — Transaktions-Dekodierung

**Repo:** `openchainxyz/transaction-decoder` · **Layer:** L7 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz None)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** npm-Paket ohne bin; require scheitert (MODULE_NOT_FOUND)

## Zweck
Transaktions-Dekodierung.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
kein Kommando — npm-Paket ohne bin; require scheitert (MODULE_NOT_FOUND); Quelle: `vendor/openchainxyz/transaction-decoder`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `cryo`, `mev-inspect-py`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

