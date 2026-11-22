---
name: diligence-fuzzing
kind: tool
class: RS
layer: L3
repo: ConsenSysDiligence/diligence-fuzzing
install: "release-binary"
triggers: [diligence, fuzzing, getting, started, installing, linux, macos, windows, basic, usage, create, configuration]
pairs_with: [echidna, medusa, properties, scribble, mythril, manticore]
---

# diligence-fuzzing — Fuzz-Harness-Generator

**Repo:** `ConsenSysDiligence/diligence-fuzzing` · **Layer:** L3 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz NOASSERTION)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/ConsenSysDiligence/diligence-fuzzing mit cargo/go noetig

## Zweck
Fuzz-Harness-Generator.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
kein Kommando — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/ConsenSysDiligence/diligence-fuzzing mit cargo/go noetig; Quelle: `vendor/ConsenSysDiligence/diligence-fuzzing`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

