---
name: abi-guesser
kind: tool
class: JS
layer: L5
repo: openchainxyz/abi-guesser
install: "npm -g"
triggers: [guesser, installation, usage, L5]
pairs_with: [evm-cfg-builder, pyevmasm, etheno, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier]
---

# abi-guesser — ABI-Rekonstruktion ohne Quelle

**Repo:** `openchainxyz/abi-guesser` · **Layer:** L5 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz None)

## Zweck
ABI-Rekonstruktion ohne Quelle.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
`abi-guesser --help` (npm global)

## Deutung der Ausgabe
Graph/Report als Landkarte; Aussagen über Laufzeitverhalten sind daraus nicht ableitbar.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`.
Nach diesem Skill weiter mit Layer L6.

