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

## Zweck
Stellar/Soroban-Detektoren.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
`soroban-detectors --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

