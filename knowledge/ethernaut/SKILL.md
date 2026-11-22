---
name: ethernaut
kind: tool
class: JS
layer: L8
repo: OpenZeppelin/ethernaut
install: "npm -g"
triggers: [ethernaut, deployed, versions, install, build, running, locally, sepolia, network, tests, building, deploying]
pairs_with: [not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, seal-911, seal-frameworks, blockchain-security-contacts]
---

# ethernaut — CTF-Korpus kanonischer Bug-Klassen

**Repo:** `OpenZeppelin/ethernaut` · **Layer:** L8 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
CTF-Korpus kanonischer Bug-Klassen.

## Wann anwenden
durchgehend: Musterabgleich gegen bekannte Bug-Klassen und Audit-Erfahrung.

## Kommando
`ethernaut --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- Aktualitaet und projektspezifische Besonderheit.

## Kombination
Zusammen mit: `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `seal-911`, `seal-frameworks`, `blockchain-security-contacts`.
Nach diesem Skill weiter mit Layer L9.

