---
name: fuzz-utils
kind: tool
class: PY
layer: L3
repo: crytic/fuzz-utils
install: "uv tool"
triggers: [automated, utility, tooling, smart, contract, fuzzers, features, installation, pre-requisites, tools, generating, unit]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# fuzz-utils — Fuzz-Harness-Hilfen

**Repo:** `crytic/fuzz-utils` · **Layer:** L3 · **Klasse:** PY · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
Fuzz-Harness-Hilfen.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`fuzz-utils` (via `uv tool`); Hilfe: `fuzz-utils --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

