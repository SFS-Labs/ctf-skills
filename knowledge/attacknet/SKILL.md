---
name: attacknet
kind: docker
class: DK
layer: L3
repo: crytic/attacknet
install: "docker (auf dieser Maschine nicht verfuegbar)"
triggers: [attacknet, capabilities, getting, started, installation, building, setting, other, bits, usage, configuration, contributing]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# attacknet — Chaos-Testing auf Kubernetes (Docker)

**Repo:** `crytic/attacknet` · **Layer:** L3 · **Klasse:** DK · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** braucht Docker; auf dieser Maschine nicht lauffaehig

## Zweck
Chaos-Testing auf Kubernetes (Docker).

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
Docker erforderlich — Rezept liegt in `recipes/attacknet.sh`, hier nicht lauffähig

## Deutung der Ausgabe
keine Ausgabe — auf dieser Maschine nicht lauffaehig; Rezept in `recipes/attacknet.sh`.

## Blinde Flecken
- braucht Docker; auf dieser Maschine nicht lauffaehig -> nur Referenz.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

