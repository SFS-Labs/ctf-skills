---
name: mythril
kind: tool
class: PY
layer: L4
repo: ConsenSysDiligence/mythril
install: "uv tool"
triggers: [mythril, installation, setup, usage, building, documentation, vulnerability, remediation, L4]
pairs_with: [manticore, evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures]
---

# mythril — Symbolische Ausfuehrung, konkrete Pfade

**Repo:** `ConsenSysDiligence/mythril` · **Layer:** L4 · **Klasse:** PY · **Bezogen:** ja (branch `develop`, Lizenz MIT)

## Zweck
Symbolische Ausfuehrung, konkrete Pfade.

## Wann anwenden
wenn ein statischer Treffer einen konkreten Pfad braucht.

## Kommando
`mythril` (via `uv tool`); Hilfe: `mythril --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- Pfad-Explosion, Loops und Hash-/Krypto-Logik brechen es.

## Kombination
Zusammen mit: `manticore`, `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`.
Nach diesem Skill weiter mit Layer L5.

