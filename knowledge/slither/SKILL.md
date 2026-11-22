---
name: slither
kind: tool
class: PY
layer: L2
repo: crytic/slither
install: "uv tool"
triggers: [features, usage, install, using, recommended, haven, already, slither, tool, without, installation, brew]
pairs_with: [surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble, diligence-fuzzing]
---

# slither — Statik-Rueckgrat: Detektoren, Printer, SlithIR, Dataflow

**Repo:** `crytic/slither` · **Layer:** L2 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
Statik-Rueckgrat: Detektoren, Printer, SlithIR, Dataflow.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
`slither` (via `uv tool`); Hilfe: `slither --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination (pairs_with)
Zusammen mit: `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`.
Nach diesem Skill weiter mit Layer L3.

