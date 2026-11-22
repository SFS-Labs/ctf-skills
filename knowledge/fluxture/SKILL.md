---
name: fluxture
kind: tool
class: RS
layer: L3
repo: crytic/fluxture
install: "release-binary"
triggers: [fluxture, quickstart, usage, geolocation, topological, analysis, programmatic, interface, license, acknowledgements, L3]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# fluxture — Contract-Fuzzing/Deployment-Infrastruktur

**Repo:** `crytic/fluxture` · **Layer:** L3 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz Apache-2.0)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/crytic/fluxture mit cargo/go noetig

## Zweck
Contract-Fuzzing/Deployment-Infrastruktur.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
kein Kommando — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/crytic/fluxture mit cargo/go noetig; Quelle: `vendor/crytic/fluxture`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

