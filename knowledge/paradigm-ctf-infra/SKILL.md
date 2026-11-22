---
name: paradigm-ctf-infra
kind: docker
class: DK
layer: L8
repo: paradigmxyz/paradigm-ctf-infrastructure
install: "docker (auf dieser Maschine nicht verfuegbar)"
triggers: [paradigm, infra, getting, started, create, cluster, doesn, exist, build, image, push, kind]
pairs_with: [not-so-smart-contracts, smart-contract-best-practices, slowmist-knowledge-base, ethernaut, seal-911, seal-frameworks, blockchain-security-contacts]
---

# paradigm-ctf-infra — Challenge-Deployment-Vorlage (Docker)

**Repo:** `paradigmxyz/paradigm-ctf-infrastructure` · **Layer:** L8 · **Klasse:** DK · **Bezogen:** ja (branch `main`, Lizenz None)

## Zweck
Challenge-Deployment-Vorlage (Docker).

## Wann anwenden
durchgehend: Musterabgleich gegen bekannte Bug-Klassen und Audit-Erfahrung.

## Kommando
Docker erforderlich — Rezept liegt in `recipes/paradigm-ctf-infra.sh`, hier nicht lauffähig

## Deutung der Ausgabe
—

## Blinde Flecken
- braucht Docker; auf dieser Maschine nicht lauffaehig -> nur Referenz.
- Aktualitaet und projektspezifische Besonderheit.

## Kombination
Zusammen mit: `not-so-smart-contracts`, `smart-contract-best-practices`, `slowmist-knowledge-base`, `ethernaut`, `seal-911`, `seal-frameworks`, `blockchain-security-contacts`.
Nach diesem Skill weiter mit Layer L9.

