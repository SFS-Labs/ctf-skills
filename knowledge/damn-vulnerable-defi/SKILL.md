---
name: damn-vulnerable-defi
kind: tool
class: JS
layer: L8
repo: OpenZeppelin/damn-vulnerable-defi
install: "npm -g"
triggers: [play, troubleshooting, disclaimer, damn, vulnerable, defi, L8]
pairs_with: [not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut, seal-911, seal-frameworks, blockchain-security-contacts]
---

# damn-vulnerable-defi — DeFi-Angriffs-Korpus

**Repo:** `OpenZeppelin/damn-vulnerable-defi` · **Layer:** L8 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz MIT)

## Zweck
DeFi-Angriffs-Korpus.

## Wann anwenden
durchgehend: Musterabgleich gegen bekannte Bug-Klassen und Audit-Erfahrung.

## Kommando
`damn-vulnerable-defi --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- Aktualitaet und projektspezifische Besonderheit.

## Kombination
Zusammen mit: `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`, `seal-911`, `seal-frameworks`, `blockchain-security-contacts`.
Nach diesem Skill weiter mit Layer L9.

