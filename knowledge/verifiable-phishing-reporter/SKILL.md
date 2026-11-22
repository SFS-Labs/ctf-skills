---
name: verifiable-phishing-reporter
kind: tool
class: JS
layer: L9
repo: security-alliance/verifiable-phishing-reporter
install: "npm -g"
triggers: [verifiable, phishing, reporter, usage, configuration, troubleshooting, connection, opened, attestation, generated, sure, page]
pairs_with: [seal-911, seal-frameworks, blockchain-security-contacts, slither, surya, bytecode-verifier, slither-mcp]
---

# verifiable-phishing-reporter — Meldeweg

**Repo:** `security-alliance/verifiable-phishing-reporter` · **Layer:** L9 · **Klasse:** JS · **Bezogen:** ja (branch `main`, Lizenz None)

## Zweck
Meldeweg.

## Wann anwenden
sobald ein Fund existiert: beweisen, melden, eskalieren.

## Kommando
`verifiable-phishing-reporter --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- ist kein Analysewerkzeug.

## Kombination
Zusammen mit: `seal-911`, `seal-frameworks`, `blockchain-security-contacts`, `slither`, `surya`, `bytecode-verifier`, `slither-mcp`.
Nach diesem Skill weiter mit Layer L2.

