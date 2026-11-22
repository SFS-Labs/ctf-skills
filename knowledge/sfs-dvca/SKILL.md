---
name: sfs-dvca
kind: tool
class: JS
layer: L3
repo: SFS-Labs/DamnVulnerableCryptoApp
install: "npm -g"
triggers: [build, will, install, necessary, dependencies, frontend, backend, case, already, have, want, them]
pairs_with: [echidna, medusa, properties, scribble, diligence-fuzzing, mythril, manticore]
---

# sfs-dvca — Web3-Angriffsuebungen: Wallet/Key-Handling, Client-Flows

**Repo:** `SFS-Labs/DamnVulnerableCryptoApp` · **Layer:** L3 · **Klasse:** JS · **Bezogen:** ja (branch `master`, Lizenz MIT)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo

## Zweck
Web3-Angriffsuebungen: Wallet/Key-Handling, Client-Flows.

## Wann anwenden
wenn eine Annahme pruefbar wird: Invariante formulieren und brechen lassen.

## Kommando
kein Kommando — kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo; Quelle: `vendor/SFS-Labs/DamnVulnerableCryptoApp`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- JS-Werkzeuge sehen nur, was sie parsen; Build-/Deploy-Kontext fehlt oft.
- findet nur, wofuer jemand eine Invariante formuliert hat.

## Kombination (pairs_with)
Zusammen mit: `echidna`, `medusa`, `properties`, `scribble`, `diligence-fuzzing`, `mythril`, `manticore`.
Nach diesem Skill weiter mit Layer L4.

