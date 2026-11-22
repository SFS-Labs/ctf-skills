---
name: scribble
kind: tool
class: PY
layer: L3
repo: ConsenSysDiligence/scribble
install: "uv tool"
triggers: [principles, design, goals, usage, extension, code, documentation, development, installation, prerequisites, clone, build]
pairs_with: [echidna, medusa, properties, diligence-fuzzing, mythril, manticore]
---

# scribble — Spezifikation zu Runtime-Instrumentierung

**Repo:** `ConsenSysDiligence/scribble` · **Layer:** L3 · **Klasse:** PY · **Bezogen:** ja (branch `develop`, Lizenz Apache-2.0)

## Zweck
Spezifikation zu Runtime-Instrumentierung.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`scribble` (via `uv tool`); Hilfe: `scribble --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

