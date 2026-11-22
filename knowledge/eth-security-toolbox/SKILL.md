---
name: eth-security-toolbox
kind: docker
class: DK
layer: L2
repo: trailofbits/eth-security-toolbox
install: "docker (auf dieser Maschine nicht verfuegbar)"
triggers: [ethereum, security, toolbox, quickstart, usage, workflow, triggers, container, image, labels, getting, help]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# eth-security-toolbox — Ein-Container-Werkbank (Docker-Fallback)

**Repo:** `trailofbits/eth-security-toolbox` · **Layer:** L2 · **Klasse:** DK · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
Ein-Container-Werkbank (Docker-Fallback).

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
Docker erforderlich — Rezept liegt in `recipes/eth-security-toolbox.sh`, hier nicht lauffähig

## Deutung der Ausgabe
—

## Blinde Flecken
- braucht Docker; auf dieser Maschine nicht lauffaehig -> nur Referenz.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

