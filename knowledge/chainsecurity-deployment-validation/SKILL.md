---
name: chainsecurity-deployment-validation
kind: tool
class: PY
layer: L6
repo: ChainSecurity/deployment_validation
install: "uv tool"
triggers: [content, prerequisites, validation, creation, installation, building, source, using, docker, configuration, basic, usage]
pairs_with: [diffusc, oz-upgrades, bytecode-verifier, cryo, mev-inspect-py, transaction-decoder, rbuilder]
---

# chainsecurity-deployment-validation — Deploy-Parameter-Verifikation

**Repo:** `ChainSecurity/deployment_validation` · **Layer:** L6 · **Klasse:** PY · **Bezogen:** ja (branch `main`, Lizenz AGPL-3.0)

## Zweck
Deploy-Parameter-Verifikation.

## Wann anwenden
wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork).

## Kommando
`chainsecurity-deployment-validation` (via `uv tool`); Hilfe: `chainsecurity-deployment-validation --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- findet keine Altlasten, die schon immer da waren.

## Kombination
Zusammen mit: `diffusc`, `oz-upgrades`, `bytecode-verifier`, `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`.
Nach diesem Skill weiter mit Layer L7.

