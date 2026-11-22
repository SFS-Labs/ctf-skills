---
name: cryo
kind: tool
class: RS
layer: L7
repo: paradigmxyz/cryo
install: "release-binary"
triggers: [cryo, example, usage, installation, python, data, schemas, code, guide, documentation, L7]
pairs_with: [mev-inspect-py, transaction-decoder, rbuilder, not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut]
---

# cryo — On-Chain-Daten-Extraktion

**Repo:** `paradigmxyz/cryo` · **Layer:** L7 · **Klasse:** RS · **Bezogen:** ja (branch `main`, Lizenz Apache-2.0)

## Zweck
On-Chain-Daten-Extraktion.

## Wann anwenden
wenn Geld, Reihenfolge, Inclusion oder Vertrauen im Spiel ist.

## Kommando
`cryo --help` (Release-Binary in ~/.local/bin, falls vorhanden)

## Deutung der Ausgabe
Counterexample = harter Beweis. Sauberer Lauf = nur so gut wie die formulierte Invariante.

## Blinde Flecken
- schnelle Breite, aber ohne Invarianten findet der Fuzzer nichts.
- sagt nichts ueber Code-Korrektheit.

## Kombination (pairs_with)
Zusammen mit: `mev-inspect-py`, `transaction-decoder`, `rbuilder`, `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`.
Nach diesem Skill weiter mit Layer L8.

## Lokaler Zustand
**Laeuft** (Selbstbau, kein Release-Asset vorhanden). Rezept: `recipes/cryo-build.sh`. Binary: `tools/cryo/bin/cryo`. Aufruf: `cryo help` bzw. `cryo blocks --blocks 19000000:19000000 -r <rpc>`.

