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

> **Referenzkarte — kein Betrieb auf dieser Maschine.** npm-Paket ohne bin; require scheitert (MODULE_NOT_FOUND)

## Zweck
JS-Fuzzing (Off-Chain).

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
kein Kommando — npm-Paket ohne bin; require scheitert (MODULE_NOT_FOUND); Quelle: `vendor/ConsenSysDiligence/napalm`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

