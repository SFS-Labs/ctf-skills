---
name: sfs-dvca
kind: tool
class: JS
layer: L3
repo: SFS-Labs/DamnVulnerableCryptoApp
install: "npm -g"
triggers: [build, will, install, necessary, dependencies, frontend, backend, case, already, have, want, them]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# sfs-dvca — Web3-Angriffsuebungen: Wallet/Key-Handling, Client-Flows

**Repo:** `SFS-Labs/DamnVulnerableCryptoApp` · **Layer:** L3 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz MIT)

## Zweck
Web3-Angriffsuebungen: Wallet/Key-Handling, Client-Flows.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`sfs-dvca --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

