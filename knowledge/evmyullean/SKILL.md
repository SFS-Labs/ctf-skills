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

## Kombination (pairs_with)
Zusammen mit: `crytic-compile`, `solc-select`, `surya`, `solar`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

## Zweiter Remote
`NethermindEth/EVMYulLean` ist Alias, kein zweiter Klon: derselbe Baum (`tree_sha256` `f27de34679ad5b6573a3ff387f14405b88f7bb98eb8fcc4c54a9a156c1210126`, 109 Dateien, gepinnt in `repos.tsv`). Pruefen: `bin/alias-check --local` (Baum) bzw. `bin/alias-check` (gegen den Remote).

