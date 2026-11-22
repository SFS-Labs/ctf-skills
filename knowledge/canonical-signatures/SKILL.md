---
name: canonical-signatures
kind: tool
class: JS
layer: L5
repo: openchainxyz/canonical-signatures
install: "npm -g"
triggers: [canonical, signatures, contributing, L5]
pairs_with: [evm-cfg-builder, pyevmasm, etheno, abi-guesser, diffusc, oz-upgrades, chainsecurity-deployment-validation, bytecode-verifier]
---

# canonical-signatures — Signatur-/Selector-Datenbank

**Repo:** `openchainxyz/canonical-signatures` · **Layer:** L5 · **Klasse:** JS · **Bezogen:** ja (branch `main`, Lizenz MIT)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo

## Zweck
Signatur-/Selector-Datenbank.

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
kein Kommando — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo; Quelle: `vendor/openchainxyz/canonical-signatures`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`, `bytecode-verifier`.
Nach diesem Skill weiter mit Layer L6.

