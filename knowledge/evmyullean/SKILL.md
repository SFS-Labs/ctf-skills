---
name: evmyullean
kind: source
class: SRC
layer: L1
repo: paradigmxyz/evmyullean
install: "keine Installation (Quell-Referenz)"
triggers: [requirements, project, structure, primops, conformance, testing, semantics, tests, limitations, fallback, function, receiving]
pairs_with: [crytic-compile, solc-select, surya, solar, slither, surya, bytecode-verifier, slither-mcp]
---

# evmyullean — Yul/EVM-Semantik in Lean

**Repo:** `paradigmxyz/evmyullean` · **Layer:** L1 · **Klasse:** SRC · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

## Zweck
Yul/EVM-Semantik in Lean.

## Wann anwenden
sobald Quellcode/Bytecode vorliegt: Karte bauen, Compiler pinnen.

## Kommando
kein Kommando — Quelle bei Semantikfragen nachschlagen

## Deutung der Ausgabe
Semantik-Nachschlagewerk: ‚was tut die EVM hier wirklich'.

## Blinde Flecken
- kein fertiges Werkzeug; Referenz zum Nachschlagen von Semantik.
- kennt die Absicht des Autors nicht.

## Kombination
Zusammen mit: `crytic-compile`, `solc-select`, `surya`, `solar`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.


## Sibling
solidity-lean (gleiche Semantik-Basis, Yul-Teil)
