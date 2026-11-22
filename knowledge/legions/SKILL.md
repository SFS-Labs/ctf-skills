---
name: legions
kind: tool
class: PY
layer: L2
repo: ConsenSysDiligence/Legions
install: "uv tool"
triggers: [legions, L2]
pairs_with: [slither, surya, bytecode-verifier, slither-mcp, echidna, medusa, properties, scribble]
---

# legions — Aeltere Schwachstellen-Suite

**Repo:** `ConsenSysDiligence/Legions` · **Layer:** L2 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz MIT)

## Zweck
Aeltere Schwachstellen-Suite.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
`legions` (via `uv tool`); Hilfe: `legions --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `slither-mcp`, `echidna`, `medusa`, `properties`, `scribble`.
Nach diesem Skill weiter mit Layer L3.

