---
name: daedaluzz
kind: tool
class: PY
layer: L3
repo: ConsenSysDiligence/daedaluzz
install: "uv tool"
triggers: [daedaluzz, L3]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# daedaluzz — Coverage-gefuehrter Fuzzer

**Repo:** `ConsenSysDiligence/daedaluzz` · **Layer:** L3 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz Apache-2.0)

## Zweck
Coverage-gefuehrter Fuzzer.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
`daedaluzz` (via `uv tool`); Hilfe: `daedaluzz --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

## Lokaler Zustand
**Laeuft** (Go, nicht Python). Rezept: `recipes/daedaluzz-build.sh` (Go 1.23.4 nach `~/.local/opt`). Binary: `~/.local/bin/daedaluzz`. Aufruf: `daedaluzz` im Zielverzeichnis -> schreibt `generated-maze.sol`.

