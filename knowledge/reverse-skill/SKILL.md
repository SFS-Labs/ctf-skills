---
name: reverse-skill
kind: knowledge
class: DOC
layer: L5
repo: zhaoxuya520/reverse-skill
install: "keine Installation"
triggers: [about, current, status, sponsors, built, getting, started, prerequisites, installation, usage, supported, scenarios]
pairs_with: [evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures, diffusc, oz-upgrades, chainsecurity-deployment-validation]
---

# reverse-skill — Reverse-Engineering-Methodik (CN)

**Repo:** `zhaoxuya520/reverse-skill` · **Layer:** L5 · **Klasse:** DOC · **Bezogen:** ja (branch `main`, Lizenz MIT)

## Zweck
Reverse-Engineering-Methodik (CN).

## Wann anwenden
wenn kein Quellcode existiert (Bytecode-only, Proxy, fremdes Deployment).

## Kommando
kein Kommando — Karte lesen, Regel auf das Ziel abbilden

## Deutung der Ausgabe
Text ist Muster, keine Messung: auf das Ziel abbilden und gegen Code prüfen.

## Blinde Flecken
- kein ausfuehrbares Artefakt; Wissen muss aktiv auf das Ziel abgebildet werden.
- Off-Chain-Verhalten und Deployment-Kontext fehlen.

## Kombination (pairs_with)
Zusammen mit: `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`, `diffusc`, `oz-upgrades`, `chainsecurity-deployment-validation`.
Nach diesem Skill weiter mit Layer L6.

