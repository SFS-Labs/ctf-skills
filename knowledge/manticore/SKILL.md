---
name: manticore
kind: tool
class: PY
layer: L4
repo: trailofbits/manticore
install: "uv tool"
triggers: [warning, project, archived, manticore, features, installation, usage, example, script, collatz, function, given]
pairs_with: [mythril, evm-cfg-builder, pyevmasm, etheno, abi-guesser, canonical-signatures]
---

# manticore — Symbolische Ausfuehrung

**Repo:** `trailofbits/manticore` · **Layer:** L4 · **Klasse:** PY · **Bezogen:** ja (branch `master`, Lizenz AGPL-3.0)

> **Referenzkarte — kein Betrieb auf dieser Maschine.** uv tool installiert (3.9/3.10); Start scheitert an protobuf-Descriptor bzw. wasm/collections.Callable -> gepinnte Umgebung noetig

## Zweck
Symbolische Ausfuehrung.

## Wann anwenden
wenn ein statischer Treffer einen konkreten Pfad braucht.

## Kommando
kein Kommando — uv tool installiert (3.9/3.10); Start scheitert an protobuf-Descriptor bzw. wasm/collections.Callable -> gepinnte Umgebung noetig; Quelle: `vendor/trailofbits/manticore`

## Deutung der Ausgabe
keine Ausgabe — laeuft hier nicht; Nutzen ist der Quellbaum im vendor-Baum.

## Blinde Flecken
- Findings sind Hypothesen; kein Beweis ohne Gegenbeispiel oder Pfad.
- Pfad-Explosion, Loops und Hash-/Krypto-Logik brechen es.

## Kombination (pairs_with)
Zusammen mit: `mythril`, `evm-cfg-builder`, `pyevmasm`, `etheno`, `abi-guesser`, `canonical-signatures`.
Nach diesem Skill weiter mit Layer L5.

