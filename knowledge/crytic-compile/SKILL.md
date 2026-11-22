---
name: crytic-compile
kind: tool
class: PY
layer: L1
repo: crytic/crytic-compile
install: "uv tool"
triggers: [crytic-compile, installation, usage, library, linking, crytic, compile, L1]
pairs_with: [solc-select, surya, solar, slither, surya, bytecode-verifier, slither-mcp]
---

# crytic-compile — Klebstoff: ein Interface fuer alle Toolchains

**Repo:** `crytic/crytic-compile` · **Layer:** L1 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
Klebstoff: ein Interface fuer alle Toolchains.

## Wann anwenden
sobald Quellcode/Bytecode vorliegt: Karte bauen, Compiler pinnen.

## Kommando
`crytic-compile` (via `uv tool`); Hilfe: `crytic-compile --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- kennt die Absicht des Autors nicht.

## Kombination
Zusammen mit: `solc-select`, `surya`, `solar`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

