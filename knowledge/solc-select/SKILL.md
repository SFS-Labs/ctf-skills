---
name: solc-select
kind: tool
class: PY
layer: L1
repo: crytic/solc-select
install: "uv tool"
triggers: [solc-select, installation, using, running, macos, newer, linux, usage, quick, start, install, specific]
pairs_with: [crytic-compile, surya, solar, slither, surya, bytecode-verifier, slither-mcp]
---

# solc-select — Compiler-Pinning, Reproduzierbarkeit

**Repo:** `crytic/solc-select` · **Layer:** L1 · **Klasse:** PY · **Bezogen:** ja (branch `dev`, Lizenz AGPL-3.0)

## Zweck
Compiler-Pinning, Reproduzierbarkeit.

## Wann anwenden
sobald Quellcode/Bytecode vorliegt: Karte bauen, Compiler pinnen.

## Kommando
`solc-select` (via `uv tool`); Hilfe: `solc-select --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- kennt die Absicht des Autors nicht.

## Kombination
Zusammen mit: `crytic-compile`, `surya`, `solar`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

