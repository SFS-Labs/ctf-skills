---
name: oz-monitor
kind: tool
class: JS
layer: L7
repo: OpenZeppelin/openzeppelin-monitor
install: "npm -g"
triggers: [openzeppelin, monitor, features, supported, networks, notification, channels, users, installation, running, developers, technical]
pairs_with: [cryo, mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# oz-monitor — On-Chain-Monitoring/Alerting

**Repo:** `OpenZeppelin/openzeppelin-monitor` · **Layer:** L7 · **Klasse:** JS · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
On-Chain-Monitoring/Alerting.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`oz-monitor --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- sagt nichts ueber Code-Korrektheit.

## Kombination
Zusammen mit: `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

