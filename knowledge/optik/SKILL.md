---
name: optik
kind: tool
class: RS
layer: L2
repo: crytic/optik
install: "release-binary"
triggers: [optik, hybrid, echidna, usage, installation, runs, docker, container, mounting, local, directory, into]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# optik — EVM-Optimizer-/Instrumentierungs-Analyse

**Repo:** `crytic/optik` · **Layer:** L2 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz NOASSERTION)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/crytic/optik mit cargo/go noetig

## Zweck
EVM-Optimizer-/Instrumentierungs-Analyse.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
kein Kommando — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/crytic/optik mit cargo/go noetig; Quelle: `vendor/crytic/optik`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination (pairs_with)
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

