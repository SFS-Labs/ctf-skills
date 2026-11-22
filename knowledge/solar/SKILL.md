---
name: solar
kind: tool
class: RS
layer: L1
repo: paradigmxyz/solar
install: "release-binary"
triggers: [solar, features, goals, performance, works, getting, started, library, usage, binary, compile, single]
pairs_with: [crytic-compile, solc-select, surya, slither, surya, bytecode-verifier, slither-mcp]
---

# solar — Moderner Solidity-Compiler

**Repo:** `paradigmxyz/solar` · **Layer:** L1 · **Klasse:** RS · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

## Zweck
Moderner Solidity-Compiler.

## Wann anwenden
sobald Quellcode/Bytecode vorliegt: Karte bauen, Compiler pinnen.

## Kommando
`solar --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- kennt die Absicht des Autors nicht.

## Kombination
Zusammen mit: `crytic-compile`, `solc-select`, `surya`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

