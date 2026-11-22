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

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo

## Zweck
ABI-Rekonstruktion ohne Quelle.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
kein Kommando — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo; Quelle: `vendor/openchainxyz/abi-guesser`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`.
Nach diesem Skill weiter mit Layer L6.

