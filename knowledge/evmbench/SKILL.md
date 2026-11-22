---
name: evmbench
kind: tool
class: PY
layer: L8
repo: paradigmxyz/evmbench
install: "uv tool"
triggers: [works, architecture, end-to-end, flow, security, backendoaikeymode, proxy, oaiproxyaeskey, services, repo, layout, quickstart]
pairs_with: [not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut, seal-911, seal-frameworks, blockchain-security-contacts]
---

# evmbench — Benchmark mit Ground Truth

**Repo:** `paradigmxyz/evmbench` · **Layer:** L8 · **Klasse:** PY · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

## Zweck
Benchmark mit Ground Truth.

## Wann anwenden
durchgehend: Musterabgleich gegen bekannte Bug-Klassen und Audit-Erfahrung.

## Kommando
`evmbench` (via `uv tool`); Hilfe: `evmbench --help`

## Deutung der Ausgabe
Exit-Code plus Findings/Detektor-IDs. Jeder Treffer ist eine Hypothese; bestätigt wird über L3 (Counterexample) oder L4 (Pfad).

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- Aktualitaet und projektspezifische Besonderheit.

## Kombination
Zusammen mit: `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`, `seal-911`, `seal-frameworks`, `blockchain-security-contacts`.
Nach diesem Skill weiter mit Layer L9.

