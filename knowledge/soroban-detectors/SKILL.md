---
name: soroban-detectors
kind: tool
class: RS
layer: L2
repo: OpenZeppelin/soroban-security-detectors-sdk
install: "release-binary"
triggers: [soroban, security, detectors, features, crate, structure, quick, start, prerequisites, build, workspace, scan]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# soroban-detectors — Stellar/Soroban-Detektoren

**Repo:** `OpenZeppelin/soroban-security-detectors-sdk` · **Layer:** L2 · **Klasse:** RS · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/OpenZeppelin/soroban-security-detectors-sdk mit cargo/go noetig

## Zweck
Stellar/Soroban-Detektoren.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
kein Kommando — kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); Bau aus vendor/OpenZeppelin/soroban-security-detectors-sdk mit cargo/go noetig; Quelle: `vendor/OpenZeppelin/soroban-security-detectors-sdk`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination (pairs_with)
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

