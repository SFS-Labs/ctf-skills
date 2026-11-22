---
name: seal-intel-sdk
kind: tool
class: JS
layer: L7
repo: security-alliance/seal-intel-sdk
install: "npm -g"
triggers: [seal, intel, usage, setup, functions, L7]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# seal-intel-sdk — Threat-Intel-Anbindung

**Repo:** `security-alliance/seal-intel-sdk` · **Layer:** L7 · **Klasse:** JS · **Bezogen:** ja (branch `main`, Lizenz None)

## Zweck
Threat-Intel-Anbindung.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`seal-intel-sdk --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

