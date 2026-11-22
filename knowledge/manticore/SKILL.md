---
name: manticore
kind: tool
class: PY
layer: L4
repo: trailofbits/manticore
install: "uv tool"
triggers: [warning, project, archived, manticore, features, installation, usage, example, script, collatz, function, given]
pairs_with: [mythril, evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures]
---

# manticore — Symbolische Ausfuehrung

**Repo:** `trailofbits/manticore` · **Layer:** L4 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

## Zweck
Symbolische Ausfuehrung.

## Wann anwenden
wenn ein statischer Treffer einen konkreten Pfad braucht.

## Kommando
`manticore` (via `uv tool`); Hilfe: `manticore --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- Pfad-Explosion, Loops und Hash-/Krypto-Logik brechen es.

## Kombination
Zusammen mit: `mythril`, `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`.
Nach diesem Skill weiter mit Layer L5.

