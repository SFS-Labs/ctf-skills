---
name: napalm
kind: tool
class: JS
layer: L3
repo: ConsenSysDiligence/napalm
install: "npm -g"
triggers: [napalm, installation, running, scans, workflow, installing, packages, using, module, L3]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# napalm — JS-Fuzzing (Off-Chain)

**Repo:** `ConsenSysDiligence/napalm` · **Layer:** L3 · **Klasse:** JS · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

## Zweck
JS-Fuzzing (Off-Chain).

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`napalm --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

