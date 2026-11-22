---
name: cloudexec
kind: docker
class: DK
layer: L3
repo: crytic/cloudexec
install: "docker (auf dieser Maschine nicht verfuegbar)"
triggers: [cloudexec, getting, started, installation, install, release, configure, credentials, launch, remote, specify, custom]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# cloudexec — Verteilte Fuzz-Kampagnen (Docker)

**Repo:** `crytic/cloudexec` · **Layer:** L3 · **Klasse:** DK · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
Verteilte Fuzz-Kampagnen (Docker).

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
Docker erforderlich — Rezept liegt in `recipes/cloudexec.sh`, hier nicht lauffähig

## Deutung der Ausgabe
—

## Blinde Flecken
- braucht Docker; auf dieser Maschine nicht lauffaehig -> nur Referenz.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

