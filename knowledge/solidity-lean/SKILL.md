---
name: solidity-lean
kind: source
class: SRC
layer: L1
repo: paradigmxyz/solidity-lean
install: "keine Installation (Quell-Referenz)"
triggers: [solidity-lean, machine-checked, solidity, semantics, solidcore, spec, hunt, find, divergence, credited, validation, continuously]
pairs_with: [crytic-compile, solc-select, surya, solar, slither, surya, bytecode-verifier, slither-mcp]
---

# solidity-lean — Formale Solidity-Semantik (Lean 4)

**Repo:** `paradigmxyz/solidity-lean` · **Layer:** L1 · **Klasse:** SRC · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

## Zweck
Formale Solidity-Semantik (Lean 4).

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

