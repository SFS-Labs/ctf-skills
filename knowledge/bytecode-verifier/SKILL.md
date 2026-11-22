---
name: bytecode-verifier
kind: tool
class: RS
layer: L6
repo: ConsenSysDiligence/bytecode-verifier
install: "release-binary"
triggers: [bytecode, verifier, installation, quick, usage, ethv, verify, chainchoice, list, compiler, contributing, acknowledgement]
pairs_with: [diffusc, oz-upgrades, chainsecurity-deployment-validation, cryo, mev-inspect-py, transaction-decoder, rbuilder]
---

# bytecode-verifier — Bytecode-/Upgrade-Verifikation

**Repo:** `ConsenSysDiligence/bytecode-verifier` · **Layer:** L6 · **Klasse:** RS · **Bezogen:** ja (branch `master`, Lizenz None)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/ConsenSysDiligence/bytecode-verifier

## Zweck
Bytecode-/Upgrade-Verifikation.

## Wann anwenden
wenn sich Code/Parameter geaendert haben (Upgrade, Deployment, Fork).

## Kommando
kein Kommando — Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in vendor/ConsenSysDiligence/bytecode-verifier; Quelle: `vendor/ConsenSysDiligence/bytecode-verifier`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- findet keine Altlasten, die schon immer da waren.

## Kombination (pairs_with)
Zusammen mit: `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `cryo`, `mev-inspect-py`, `transaction-decoder`, `rbuilder`.
Nach diesem Skill weiter mit Layer L7.

