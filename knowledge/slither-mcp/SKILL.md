---
name: slither-mcp
kind: tool
class: PY
layer: L2
repo: trailofbits/slither-mcp
install: "uv tool"
triggers: [slither, server, overview, features, installation, install, dependencies, development, mode, usage, basic, claude]
pairs_with: [slither, surya, bytecode-verifier, echidna, medusa, properties, scribble, diligence-fuzzing]
---

# slither-mcp — Slither als MCP-Server

**Repo:** `trailofbits/slither-mcp` · **Layer:** L2 · **Klasse:** PY · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
Slither als MCP-Server.

## Wann anwenden
Breite zuerst: alle In-Scope-Artefakte statisch abklopfen.

## Kommando
`slither-mcp` (via `uv tool`); Hilfe: `slither-mcp --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- sieht zeitliche, oekonomische und Cross-Contract-Fehler nicht.

## Kombination
Zusammen mit: `slither`, `surya`, `bytecode-verifier`, `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`.
Nach diesem Skill weiter mit Layer L3.

