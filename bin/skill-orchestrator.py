#!/usr/bin/env python3
"""SFS CTF Skill Index V8 - adaptiver Orchestrator mit echter Werkzeugausfuehrung.

Zustandsmodell (verbindlich):
    DISCOVERED -> SELECTED -> READY -> INVOKED -> COMPLETED -> VERIFIED
    terminale Ausgaenge: FAILED, UNAVAILABLE, BLOCKED, KNOWLEDGE_ONLY, SKIPPED

Teilbefehle:
    route      Kandidaten + DAG; fuehrt NICHTS aus (Status ROUTED_NOT_EXECUTED)
    plan       ausfuehrbarer Dependency-Graph mit Adaptern, Verfuegbarkeit, Recovery
    run        fuehrt die ausgewaehlten Adapter wirklich aus, beobachtet, adaptiert
    probe      Kompatibilitaet: zwei begrenzte statische Probes (surya, slither)
    assess     strukturelle Evidenzpruefung (Hash/Existenz) + Inhaltsprüfung
    verify     inhaltliche, frische Verifikation aus Artefakten
    selfcheck  Katalog-, Adapter- und Evidenz-Selbsttest
    copilot    GitHub-Copilot-Delegation (preflight/detect/delegate/watch/review)

Grundsaetze: keine Shell, feste Argumentlisten mit ganzzahligen Platzhaltern,
Prozessgruppe wird bei Timeout beendet, Logs sind gekappt, jeder Lauf erzeugt
einen Receipt. Ein Exit-Code 0 ist kein Sicherheitsbeweis.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys

# --------------------------------------------------------------------------
# Taxonomie
# --------------------------------------------------------------------------
CAPABILITIES = {
    "reentrancy": (r"\breentranc\w*|\breentrant\b", ["slither", "echidna", "medusa", "not-so-smart-contracts"]),
    "underflow": (r"\bunderflow\b|\bunchecked\b|\bbalance\s+accounting\b|\bwithdrawal\b", ["slither", "echidna", "properties", "smart-contract-best-practices"]),
    "access-control": (r"\baccess[ -]?control\b|\bauthori[sz]\w*|\bonlyowner\b|\bpermissionless\b", ["slither", "mythril", "not-so-smart-contracts"]),
    "signature": (r"\beip[- ]?712\b|\bsignature\b|\bsigner\b|\breplay\b|\becrecover\b", ["canonical-signatures", "slither", "mythril", "pyevmasm"]),
    "bytecode": (r"\bbytecode\b|\bdisassembl\w*|\bverified source missing\b", ["evm-cfg-builder", "pyevmasm", "abi-guesser", "canonical-signatures"]),
    "upgrade": (r"\bupgrade\b|\bproxy\b|\bstorage layout\b|\bdiff\b", ["diffusc", "bytecode-verifier", "oz-upgrades", "slither"]),
    "chain-data": (r"\bfork\b|\bhistorical\b|\bon[- ]?chain\b|\bblock\s*\d+", ["cryo", "transaction-decoder", "evm-tracing-ref"]),
    "economic": (r"\bprofit\b|\bmev\b|\barbitrage\b|\beconomic\b", ["cryo", "mev-inspect-py", "mev-research"]),
    "compile": (r"\bcompil\w*|\bsolc\b|\bbuild\b|\bversion\b", ["solc-select", "crytic-compile", "solar"]),
}
SECURITY_INTENT = re.compile(r"\b(audit|auditing|vulnerab\w*|exploit|attacker|security|reproduc\w*|analy[sz]\w*|review|bug|withdrawal|claim|reentranc\w*|underflow|unchecked|eip[- ]?712|bytecode|signer|permissionless|fuzz|invariant|upgrade|proxy|storage[ -]?layout|smart[ -]?contract)\b", re.I)
SUPPORTED_DOMAIN = re.compile(r"\b(solidity|evm|erc[- ]?\d+|smart[ -]?contract|contract audit|defi|dex|token|bsc|bnb chain|ethereum|claim|nonce|reentranc\w*|underflow|unchecked|eip[- ]?712|bytecode|foundry|forge|anvil|eth_call|on[- ]?chain)\b", re.I)
OTHER_CHAINS = re.compile(r"\b(solana|anchor|cairo|starknet|movevm|aptos|sui|algorand|teal|soroban|stellar)\b", re.I)
TOKEN = re.compile(r"[a-z0-9][a-z0-9_+.-]{1,}")
STOP = {"and", "for", "the", "with", "this", "that", "from", "into", "have", "been", "when", "here", "using", "about", "code", "tool", "more", "skill", "skills", "security", "analysis", "test", "tests"}

# Nicht-EVM-Domaenen: Wissensrouting statt EVM-Werkzeugaufruf (Grenze dokumentieren).
DOMAIN_SKILLS = {
    "solana": ["solana-lints", "slowmist-solana-bp", "not-so-smart-contracts", "safe-harbor"],
    "move": ["movevm", "move-over-ctf", "amarna", "safe-harbor"],
    "cairo": ["cairo-contracts", "caracal", "tayt", "safe-harbor"],
    "algorand": ["tealer", "safe-harbor"],
    "stellar": ["soroban-detectors", "safe-harbor"],
}

STATES = ["DISCOVERED", "SELECTED", "READY", "INVOKED", "COMPLETED", "FAILED",
          "UNAVAILABLE", "VERIFIED", "BLOCKED", "KNOWLEDGE_ONLY", "SKIPPED"]
FAILED_STATES = {"FAILED", "UNAVAILABLE", "BLOCKED", "SKIPPED"}

BINARIES = {
    "slither": "slither", "surya": "surya", "mythril": "myth", "echidna": "echidna",
    "medusa": "medusa", "cryo": "cryo", "diffusc": "diffusc", "pyevmasm": "evmasm",
    "solc-select": "solc-select", "scribble": "scribble", "rbuilder": "rbuilder",
    "crytic-compile": "crytic-compile", "daedaluzz": "daedaluzz", "solar": "solar",
    "evm-cfg-builder": "evm-cfg-builder", "etheno": "etheno", "legions": "legions",
}

# --------------------------------------------------------------------------
# Adapter: feste Argumentlisten, keine Shell, ganzzahlige Platzhalter
# --------------------------------------------------------------------------
ADAPTERS = {
    "surya-describe": {
        "tool": "surya", "family": "map", "requires": ["source"], "timeout": 90,
        "argv": ["describe", "{target}"], "artifact": "surya-describe.txt",
        "acceptance": "Vertrags- und Funktionsliste aus echter Quelle geparst",
        "fallback": [],
    },
    "slither-json": {
        "tool": "slither", "family": "static", "requires": ["source"], "timeout": 240,
        # Slither beendet mit 255, wenn es Befunde gibt: Exit-Code allein ist kein Fehler.
        "ok_exit": [0, 255], "requires_json": True,
        "argv": ["{target}", "--json", "{outdir}/slither.json"], "artifact": "slither.json",
        "acceptance": "Slither-JSON mit results.detectors erfolgreich geschrieben",
        "fallback": ["myth-json"],
    },
    "slither-json-solc": {
        # Gleicher Scanner, andere Compiler-Annahme: isoliert Framework-Fehler.
        "tool": "slither", "family": "static", "requires": ["source"], "timeout": 240,
        "ok_exit": [0, 255], "requires_json": True,
        "argv": ["{target}", "--compile-force-framework", "solc",
                 "--json", "{outdir}/slither-solc.json"], "artifact": "slither-solc.json",
        "acceptance": "Slither-JSON mit erzwungenem solc-Framework",
        "fallback": ["myth-json"],
    },
    "myth-json": {
        # Bewusst knapp: symbolische Ausfuehrung ist auf diesem Node der teuerste
        # Adapter. Ein Timeout ist ein dokumentierter Blocker, kein Befund.
        "tool": "mythril", "family": "static", "requires": ["source"], "timeout": 60,
        "ok_exit": [0], "requires_json": True,
        "argv": ["analyze", "{target}", "--execution-timeout", "{myth_timeout}",
                 "--max-depth", "64", "-o", "json", "-j", "{outdir}/myth.json"],
        "artifact": "myth.json",
        "acceptance": "Mythril-JSON mit issues-Liste geschrieben",
        "fallback": [],
    },
    "solc-compile": {
        "tool": "solc-select", "family": "compile", "requires": ["source"], "timeout": 120,
        "argv": ["--bin", "{target}"], "artifact": None,
        "acceptance": "solc kompiliert die Quelle ohne Fehler (Bytecode erzeugt)",
        "fallback": [],
    },
    "forge-test": {
        "tool": "forge", "family": "counterexample", "requires": ["project"], "timeout": 300,
        "argv": ["test", "--json"], "cwd": "{project}", "artifact": None,
        "acceptance": "forge --json liefert je Test einen Status; Counterexample-Test besteht",
        "fallback": ["echidna-assertion", "medusa-fuzz"],
    },
    "forge-match": {
        "tool": "forge", "family": "negative_control", "requires": ["project"], "timeout": 300,
        "argv": ["test", "--json", "--match-test", "{match_test}"], "cwd": "{project}", "artifact": None,
        "acceptance": "Negativkontrolle besteht unter der Gegenbedingung",
        "fallback": [],
    },
    "echidna-assertion": {
        "tool": "echidna", "family": "counterexample", "requires": ["source", "contract"], "timeout": 240,
        # Exit 1 bedeutet: Property falsifiziert - ein Befund, kein Werkzeugausfall.
        # Das gilt nur mit parsebarer JSON-Ausgabe; sonst ist es ein Werkzeugfehler.
        "ok_exit": [0, 1], "requires_json_stdout": True,
        "argv": ["{target}", "--contract", "{contract}", "--test-mode", "assertion",
                 "--test-limit", "{test_limit}", "--format", "json"], "artifact": "echidna.json",
        "acceptance": "Echidna-Property/Assertion mit Status falsified oder sauber fuzzing",
        "fallback": ["medusa-fuzz"],
    },
    "echidna-assertion-solc": {
        "tool": "echidna", "family": "counterexample", "requires": ["source", "contract"],
        "timeout": 240, "ok_exit": [0, 1], "requires_json_stdout": True,
        "argv": ["{target}", "--contract", "{contract}", "--test-mode", "assertion",
                 "--test-limit", "{test_limit}", "--format", "json",
                 "--crytic-args", "--compile-force-framework solc"], "artifact": "echidna-solc.json",
        "acceptance": "Echidna mit erzwungenem solc-Framework",
        "fallback": ["medusa-fuzz"],
    },
    "medusa-fuzz": {
        "tool": "medusa", "family": "counterexample", "requires": ["source", "contract"], "timeout": 240,
        "ok_exit": [0, 1],
        "argv": ["fuzz", "--target-contracts", "{contract}", "--test-limit", "{test_limit}",
                 "--timeout", "{medusa_timeout}", "--workers", "1"], "artifact": None,
        "acceptance": "Medusa-Campaign beendet, Coverage/Assertions ausgewertet",
        "fallback": [],
    },
    "evmasm-disassemble": {
        "tool": "pyevmasm", "family": "bytecode", "requires": ["bytecode"], "timeout": 60,
        "argv": ["-d", "-i", "{target}"], "artifact": "evmasm.txt",
        "acceptance": "Disassembly der Bytecode-Datei erzeugt",
        "fallback": [],
    },
    "diffusc-diff": {
        "tool": "diffusc", "family": "diff", "requires": ["source", "source_v2"], "timeout": 300,
        "argv": ["{target}", "{target_v2}", "-d", "{outdir}"], "artifact": "DiffFuzzUpgrades.sol",
        "acceptance": "Diff-Fuzz-Contract zwischen alter und neuer Version erzeugt",
        "fallback": [],
    },
    "cryo-blocks": {
        "tool": "cryo", "family": "chain-data", "requires": ["network", "block"], "timeout": 120,
        "argv": ["blocks", "--blocks", "{block}", "-r", "{rpc}", "-o", "{outdir}/cryo"],
        "artifact": None,
        "acceptance": "Parquet fuer den gepinnten Block geschrieben (nur lesend)",
        "fallback": [],
    },
}

COMPILER_HINT = re.compile(r"Cannot execute .?forge|CryticCompile|Couldn.t compile|compile-force|solc", re.I)
COUNTEREXAMPLE_NAME = re.compile(r"(reentr|drain|exploit|attack|steal|bypass|double|sweep|break|violat|counterexample|drain_vault)", re.I)
CONTROL_NAME = re.compile(r"(initial|holds|baseline|control|negative|healthy|no_?reentr)", re.I)

MAX_LOG = 200_000


# --------------------------------------------------------------------------
# Katalog
# --------------------------------------------------------------------------
def terms(x):
    return set(t for t in TOKEN.findall(str(x).lower()) if t not in STOP)


def default_root():
    checked_out = Path(__file__).resolve().parent.parent
    if checked_out.joinpath("manifest.json").exists():
        return checked_out
    return Path.home() / "ctf-skills"


def read_manifest(root, override=None):
    path = Path(override) if override else root / "manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    if not isinstance(skills, list):
        raise ValueError("invalid manifest: skills must be a list")
    return skills


def card_body(root, slug):
    card = root / "knowledge" / slug / "SKILL.md"
    try:
        return card.read_text(encoding="utf-8")[:12000]
    except OSError:
        return ""


def classify(text, mode):
    tags = [name for name, (regex, _) in CAPABILITIES.items() if re.search(regex, text, re.I)]
    if mode in ("fork", "historical") and "chain-data" not in tags:
        tags.append("chain-data")
    if mode == "bytecode" and "bytecode" not in tags:
        tags.append("bytecode")
    relevant = bool(SUPPORTED_DOMAIN.search(text) and SECURITY_INTENT.search(text)) or mode in ("source", "fork", "historical", "bytecode")
    if OTHER_CHAINS.search(text) and not re.search(r"\b(solidity|evm|ethereum|bsc|bnb chain)\b", text, re.I):
        relevant = False
    return relevant, tags


def detected_domains(text):
    found = []
    for domain, pattern in (("solana", r"\b(solana|anchor)\b"), ("move", r"\b(movevm|aptos|sui|move)\b"),
                            ("cairo", r"\b(cairo|starknet)\b"), ("algorand", r"\b(algorand|teal)\b"),
                            ("stellar", r"\b(soroban|stellar)\b")):
        if re.search(pattern, text, re.I):
            found.append(domain)
    return found


def _semantic_pick(task, skills, slugs):
    """Vom Agenten (Freebuff-Modell) gewaehlte Kandidaten validieren.

    Kein Embedding-Dienst: die semantische Bewertung liefert das vorhandene
    Modell, der Orchestrator prueft nur Existenz, Obergrenze und Verfuegbarkeit.
    """
    by = {s.get("slug"): s for s in skills}
    picked, rejected = [], []
    for slug in slugs[:16]:
        slug = str(slug).strip()
        if slug in by:
            picked.append(slug)
        else:
            rejected.append(slug)
    return picked, rejected


def score_candidates(skills, root, query, tags, top_k, semantic=None):
    query_terms = terms(query)
    corpus = []
    for x in skills:
        slug = str(x.get("slug", ""))
        text = " ".join([slug, str(x.get("role", "")), " ".join(x.get("triggers", [])),
                         card_body(root, slug)[:4000]])
        corpus.append((x, text))
    doc_freq = Counter(t for _, doc in corpus for t in terms(doc))
    total = max(1, len(corpus))
    ranked = []
    requested = {s for tag in tags for s in CAPABILITIES[tag][1]}
    if not tags:
        requested.update(["slither", "surya", "echidna", "medusa"])
    # Source-Mapping geht jeder Quellanalyse voraus, auch ohne Triggerwort.
    if "bytecode" not in tags:
        requested.add("surya")
    semantic = list(semantic or [])
    for x, body in corpus:
        slug = x.get("slug", "")
        if not slug:
            continue
        slug_terms = terms(slug.replace("-", " "))
        role_terms = terms(x.get("role", ""))
        trig_terms = terms(" ".join(x.get("triggers", [])))
        body_terms = terms(body)
        overlap = query_terms & body_terms
        relevance = sum((1.0 + math.log((total + 1) / (doc_freq[t] + 1))) *
                        (4.0 if t in slug_terms else 2.0 if t in role_terms else 0.6 if t in trig_terms else 0.8)
                        for t in overlap)
        if slug in requested:
            relevance += 12.0
        if slug == "safe-harbor":
            relevance += 4.0
        if slug in semantic:
            # Modellauswahl ist ein starker, aber nachpruefbarer Hinweis.
            relevance += 15.0
        # Betriebsstatus: eine Referenzkarte ist kein ausfuehrbares Werkzeug.
        status = str(x.get("status", ""))
        relevance += {"binary": 5.0, "bibliothek": 1.0, "referenz": -4.0,
                      "wissen": -1.0, "korpus": -2.0, "quelle": -2.0}.get(status, 0.0)
        if x.get("kind") == "tool":
            relevance += 1.0
        if slug in requested and BINARIES.get(slug) and shutil.which(BINARIES[slug]):
            relevance += 5.0
        if relevance > 0:
            ranked.append((round(relevance, 3), slug, x))
    pending = list(ranked)
    selected = []
    while pending and len(selected) < max(0, top_k):
        def adjusted(row):
            score, slug, data = row
            neighbors = set(data.get("pairs_with", []))
            connected = sum(1 for other in selected if
                            (other[1] in neighbors or slug in set(other[2].get("pairs_with", [])))
                            and other[2].get("layer") != data.get("layer"))
            same_layer = sum(1 for other in selected if other[2].get("layer") == data.get("layer"))
            # Schichtvielfalt: kein Layer darf die Auswahl dominieren.
            return score + min(3.0, connected * 1.5) - max(0, same_layer - 1) * 2.0
        best = max(pending, key=lambda row: (adjusted(row), -len(row[1])))
        pending.remove(best)
        selected.append(best)
    out = []
    for score, slug, x in selected:
        binary = BINARIES.get(slug)
        available = None if binary is None else shutil.which(binary) is not None
        out.append({
            "slug": slug,
            "layer": x.get("layer"),
            "kind": x.get("kind"),
            "role": str(x.get("role", ""))[:90],
            "status": x.get("status"),
            "reason": "capability-match" if slug in requested else
                      "semantic-pick" if slug in semantic else "relevance+pair-graph",
            "score": score,
            "command_available": available,
            "binary": binary,
            "executable": bool(available),
            "knowledge_only": available is False,
            "capabilities": [tag for tag, (_, members) in CAPABILITIES.items() if slug in members],
            "blind_spots": x.get("blind_spots", [])[:2],
        })
    return out


def graph(mode, tags, selected):
    chosen = [x["slug"] for x in selected]
    chains = []

    def add(step, depends, purpose, tools, verify):
        chains.append({"id": step, "depends_on": depends, "goal": purpose,
                       "suggested_skills": [x for x in tools if x in chosen],
                       "acceptance": verify, "status": "PENDING"})
    add("SCOPE", [], "Confirm authorization, benchmark blindness, environment and allowed network calls", ["safe-harbor"], "scope recorded; reference answers excluded")
    add("MAP", ["SCOPE"], "Map external entrypoints, ownership and cross-contract dependencies", ["surya", "slither", "evm-cfg-builder", "pyevmasm"], "real source/ABI/bytecode anchored to target")
    previous = "MAP"
    if mode in ("fork", "historical"):
        add("FORK", ["MAP"], "Pin chain, exact block and state; verify archive endpoint", ["cryo", "transaction-decoder"], "same block, code hash, balances and fork state independently verified")
        previous = "FORK"
    add("HYPOTHESES", [previous], "Enumerate invariants and attacker-controlled paths; include negative space", ["not-so-smart-contracts", "smart-contract-best-practices", "properties", "slither"], "reproduction hypothesis, preconditions and concrete failure condition")
    add("TRIANGULATE", ["HYPOTHESES"], "Use independent methods; inspect disagreement instead of voting", ["slither", "mythril", "medusa", "echidna", "pyevmasm"], "two independently sourced signals or explicit unresolved disagreement")
    add("COUNTEREXAMPLE", ["TRIANGULATE"], "Run a local executable reproducer; record before/after invariants", ["echidna", "medusa", "properties"], "local Foundry/Anvil or fuzz counterexample with zero live transactions")
    add("IMPACT", ["COUNTEREXAMPLE"], "Check transfer recipient, loss, profit, limitations and non-exploit alternatives", ["cryo", "mev-inspect-py", "evm-tracing-ref"], "independent balance/state evidence, not event logs alone")
    add("FREEZE", ["IMPACT"], "Freeze original report even on failure before reference-evaluator access", ["safe-harbor"], "result hash, known gaps, provenance and external grading separated")
    return chains


def route(task, root, manifest=None, mode="auto", top_k=7, semantic=None):
    requested_mode = mode
    if mode == "auto":
        mode = "fork" if re.search(r"\bhistorical\b|\bfork\b|\bblock\s*\d+", task, re.I) else \
               "bytecode" if re.search(r"\bbytecode\b|unverified\b", task, re.I) else "source"
    relevant, tags = classify(task, mode if requested_mode != "auto" else "auto")
    if mode in ("fork", "historical") and "chain-data" not in tags:
        tags.append("chain-data")
    if mode == "bytecode" and "bytecode" not in tags:
        tags.append("bytecode")
    domains = detected_domains(task)
    if not relevant:
        answer = {"status": "NO_MATCH", "task": task, "mode": mode, "candidates": [], "dag": [],
                  "next": "No Solidity/EVM routing; do not force security tools."}
        if domains:
            skills = read_manifest(root, manifest)
            by = {s.get("slug"): s for s in skills}
            answer["domain"] = domains
            answer["domain_candidates"] = [
                {"slug": slug, "layer": by[slug].get("layer"), "role": str(by[slug].get("role", ""))[:90],
                 "execution": "knowledge-only", "reason": f"{domains[0]}: keine lokale Ausfuehrungskette"}
                for slug in DOMAIN_SKILLS.get(domains[0], []) if slug in by]
            answer["status_detail"] = ("NO_MATCH bedeutet: keine EVM-Ausfuehrungskette. "
                                      "Die Aufgabe ist nicht irrelevant; sie wird als "
                                      f"{domains[0]}-Wissensrouting gefuehrt.")
            answer["next"] = ("Domaenenspezifische Karten lesen (" +
                              ", ".join(c["slug"] for c in answer["domain_candidates"]) +
                              "); diese Domaene hat auf diesem Node keine ausfuehrbaren Adapter. "
                              "Grenze dokumentieren, keinen EVM-Adapter erzwingen.")
        return answer
    skills = read_manifest(root, manifest)
    selected = score_candidates(skills, root, task, tags, top_k, semantic)
    return {"status": "ROUTED_NOT_EXECUTED", "task": task, "mode": mode, "features": tags,
            "catalog_entries": len(skills), "candidates": selected,
            "dag": graph(mode, tags, selected),
            "next": ("Agent must actually run and verify relevant tools, adapt to evidence; "
                     "this command only retrieves and builds a DAG."),
            "blind_boundary": "Do not inspect benchmark answers, patches or incident reports before freeze."}


# --------------------------------------------------------------------------
# Ausfuehrbarer Plan
# --------------------------------------------------------------------------
def availability(adapter_id):
    spec = ADAPTERS[adapter_id]
    binary = spec.get("tool")
    path = shutil.which(BINARIES.get(binary, binary)) if binary else None
    return {"adapter": adapter_id, "tool": binary, "binary_path": path,
            "available": bool(path), "family": spec["family"]}


def compose(task, root, manifest=None, mode="auto", top_k=7, ctx=None, semantic=None):
    """Erzeugt den ausfuehrbaren Graphen inklusive Recovery-Kanten."""
    ctx = ctx or {}
    routed = route(task, root, manifest, mode, top_k, semantic)
    if routed["status"] != "ROUTED_NOT_EXECUTED":
        return {"task": task, "routing": routed, "steps": [], "status": "NO_MATCH"}

    source_ok = bool(ctx.get("target") and Path(str(ctx["target"])).is_file())
    project_ok = bool(ctx.get("project") and Path(str(ctx["project"])).is_dir())
    tests_ok = project_ok and any(Path(str(ctx["project"])).glob("test/*.sol"))
    bytecode_ok = bool(ctx.get("target") and str(ctx["target"]).lower().endswith((".bin", ".hex", ".runtime")))
    mode_eff = routed["mode"]

    steps = []

    def step(sid, capability, adapter, depends, accepts, inputs=None, override=None, note=None):
        info = availability(adapter) if adapter else {"available": None}
        steps.append({
            "id": sid, "capability": capability, "adapter": adapter,
            "depends_on": depends, "inputs": {k: (str(v) if v is not None else None)
                                                    for k, v in (inputs or {}).items()},
            "acceptance": accepts,
            "argv_override": override, "note": note,
            "availability": info,
            "status": "DISCOVERED" if info.get("available") else
                      "UNAVAILABLE" if adapter else "KNOWLEDGE_ONLY",
            "on_failure": ADAPTERS.get(adapter, {}).get("fallback", []),
        })

    step("SCOPE", "scope", None, [], "Scope, Rechte, Offline-Grenze notiert")
    map_adapter = "surya-describe" if source_ok and not bytecode_ok else None
    step("MAP", "map", map_adapter, ["SCOPE"],
         "Entrypoints/Funktionen aus echter Quelle oder Bytecode",
         inputs={"target": ctx.get("target")},
         note=None if map_adapter else "kein Quell-/Bytecode-Ziel uebergeben")

    static_adapter = "slither-json" if source_ok else None
    if source_ok and mode_eff == "bytecode":
        static_adapter = None
    step("STATIC", "static", static_adapter, ["MAP"],
         "maschinenlesbares Analyseergebnis mit Detektoren",
         inputs={"target": ctx.get("target")},
         note=None if static_adapter else "keine Quelle oder Quellanalyse nicht anwendbar")

    step("HYPOTHESES", "hypotheses", None, ["STATIC"],
         "Invariante, Vorbedingung, konkrete Verletzungsbedingung formuliert")

    if tests_ok:
        repro, repro_note = "forge-test", "Projekt mit test/*.sol gefunden"
    elif source_ok and ctx.get("contract"):
        repro, repro_note = "echidna-assertion", "kein Foundry-Test, Property-Fuzzer als Reproducer"
    elif source_ok:
        repro, repro_note = "echidna-assertion", "kein Foundry-Test; Contract-Name noetig"
    else:
        repro, repro_note = None, "kein lokales Reproduktionsziel"
    step("COUNTEREXAMPLE", "counterexample", repro, ["HYPOTHESES"],
         "lokaler Lauf mit konkreter Assertion und Zustandsbeobachtung",
         inputs={"target": ctx.get("target"), "project": ctx.get("project"),
                 "contract": ctx.get("contract")},
         note=repro_note)

    control_adapter = "forge-match" if tests_ok else None
    control_override = ["test", "--json", "--match-test", "test_invariant_holds_initially"] if tests_ok else None
    step("NEGATIVE_CONTROL", "negative_control", control_adapter, ["COUNTEREXAMPLE"],
         "Gegenbedingung reproduziert den Fehler nicht",
         inputs={"project": ctx.get("project")},
         override=control_override,
         note="Negativkontrolle ohne zweiten unabhaengigen Test nicht belegbar"
              if not control_adapter else None)

    step("IMPACT", "impact", None, ["COUNTEREXAMPLE", "NEGATIVE_CONTROL"],
         "Wirkung (Zustands-/Vermögensdelta) unabhaengig gemessen")
    step("VERIFY", "verify", None, ["IMPACT"], "Inhaltspruefung der Artefakte, kein Hash-Gate allein")
    step("FREEZE", "freeze", None, ["VERIFY"], "Ergebnis eingefroren, offene Fragen benannt")

    ids = {s["id"] for s in steps}
    for s in steps:
        s["depends_on"] = [d for d in s["depends_on"] if d in ids]
    return {"task": task, "routing": routed, "steps": steps,
            "status": "PLANNED_NOT_EXECUTED",
            "context": {k: str(v) for k, v in ctx.items() if v},
            "state_machine": STATES}


# --------------------------------------------------------------------------
# Ausfuehrung
# --------------------------------------------------------------------------
def enough_memory():
    """Honor the SFS Linux node's max(15% RAM, 1 GiB) spawn threshold."""
    try:
        fields = {}
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith(("MemTotal:", "MemAvailable:")):
                name, value = line.split(":", 1)
                fields[name] = int(value.strip().split()[0]) * 1024
        return fields["MemAvailable"] >= max(1024 ** 3, int(fields["MemTotal"] * .15))
    except (KeyError, ValueError, OSError):
        return False


def resources():
    out = {}
    try:
        text = Path("/proc/meminfo").read_text()
        for key in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree"):
            m = re.search(rf"^{key}:\s+(\d+) kB", text, re.M)
            if m:
                out[key + "_mb"] = int(m.group(1)) // 1024
    except OSError:
        pass
    try:
        st = os.statvfs(str(Path.home()))
        out["disk_free_gb"] = round(st.f_bavail * st.f_frsize / 1e9, 1)
    except OSError:
        pass
    out["cpu_count"] = os.cpu_count()
    return out


def reserve_ok(min_free_gb=1.0):
    info = resources()
    if info.get("disk_free_gb") is not None and info["disk_free_gb"] < min_free_gb:
        return False, f"disk_free_gb {info['disk_free_gb']} < {min_free_gb}"
    if not enough_memory():
        return False, "MemAvailable unter max(15%, 1 GiB)"
    return True, "ok"


def render_argv(argv, ctx):
    """Platzhalter aus einem festen Namensraum; keine Shell, keine Options-Injektion.

    Erlaubt ist `{outdir}/name.json` (Praefix-Komposition), nicht aber ein Wert,
    der als Option beginnt (`-rf`) oder Pfad-Traversal enthaelt. Damit bleibt die
    Argumentliste datengetrieben, ohne beliebige Shell-Kommandos auszufuehren.
    """
    out = []
    for token in argv:
        token = str(token)
        if "{" in token or "}" in token:
            def replace(match):
                key = match.group(1)
                if key not in ctx or ctx[key] in (None, ""):
                    raise ValueError(f"missing placeholder {{{key}}}")
                value = str(ctx[key])
                if any(c in value for c in "\x00\n\r"):
                    raise ValueError(f"illegal control character in {{{key}}}")
                if value.startswith("-"):
                    raise ValueError(f"option-like value for {{{key}}} rejected")
                return value
            rendered = re.sub(r"\{(\w+)\}", replace, token)
            if "{" in rendered or "}" in rendered:
                raise ValueError(f"unknown placeholder in {token}")
            parts = Path(rendered).parts
            if ".." in parts:
                raise ValueError(f"path traversal rejected in {rendered}")
            out.append(rendered)
        elif "}" in token:
            raise ValueError(f"invalid placeholder syntax: {token}")
        else:
            out.append(token)
    return out


def tool_version(binary, deadline=5):
    try:
        proc = subprocess.run([binary, "--version"], capture_output=True, timeout=deadline,
                              stdin=subprocess.DEVNULL, text=True)
        line = (proc.stdout or proc.stderr or "").strip().splitlines()
        return (line[0] if line else "")[:200]
    except (OSError, subprocess.SubprocessError):
        return ""


def run_adapter(adapter_id, ctx, outdir, timeout=None):
    """Fuehrt genau einen Adapter aus und schreibt Log + Receipt-Zeile."""
    spec = ADAPTERS[adapter_id]
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    binary = shutil.which(BINARIES.get(spec["tool"], spec["tool"]))
    row = {"adapter": adapter_id, "tool": spec["tool"], "family": spec["family"]}
    if not binary:
        row.update({"status": "UNAVAILABLE", "exit_code": None,
                    "detail": f"{spec['tool']} nicht im PATH"})
        return row
    ok, why = reserve_ok()
    if not ok:
        row.update({"status": "BLOCKED", "exit_code": None, "detail": f"Ressourcenreserve: {why}"})
        return row
    argv = render_argv(spec["argv"], {**ctx, "outdir": str(outdir)})
    if spec.get("cwd"):
        key = str(spec["cwd"]).strip("{}")
        if not ctx.get(key):
            row.update({"status": "BLOCKED", "exit_code": None,
                        "detail": f"Arbeitsverzeichnis {{{key}}} fehlt"})
            return row
        cwd = str(Path(str(ctx[key])).resolve())
        if not Path(cwd).is_dir():
            row.update({"status": "BLOCKED", "exit_code": None,
                        "detail": f"Arbeitsverzeichnis {cwd} existiert nicht"})
            return row
    else:
        cwd = str(Path.cwd())
    limit = int(timeout or spec.get("timeout", 120))
    row.update({"argv": [binary, *argv], "cwd": cwd, "timeout_s": limit,
                "started_at": datetime.now(timezone.utc).isoformat()})
    started = datetime.now(timezone.utc)
    try:
        child = subprocess.Popen([binary, *argv], shell=False, cwd=cwd,
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 start_new_session=True)
        try:
            raw, _ = child.communicate(timeout=limit)
            # Erfolg ist der Vertrag des Adapters, nicht die Zahl 0: slither liefert
            # 255 bei Befunden, echidna 1 bei falsifizierter Property.
            exit_code = child.returncode
            state = "COMPLETED" if exit_code in spec.get("ok_exit", [0]) else "FAILED"
        except subprocess.TimeoutExpired:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            raw, _ = child.communicate()
            state, exit_code = "TIMEOUT", None
    except OSError as exc:
        raw = str(exc).encode()
        state, exit_code = "FAILED", None
    except ValueError as exc:
        row.update({"status": "BLOCKED", "exit_code": None, "detail": str(exc)})
        return row
    text = (raw or b"").decode("utf-8", "replace")
    truncated = len(text) > MAX_LOG
    if truncated:
        text = text[:MAX_LOG // 4] + "\n...[truncated]...\n" + text[-MAX_LOG:]
    log = outdir / f"{adapter_id}.log"
    log.write_text(text, encoding="utf-8")
    artifact = spec.get("artifact")
    if state == "COMPLETED" and spec.get("requires_json"):
        if not artifact or _read_json(outdir / artifact) is None:
            state = "FAILED"
            row["detail"] = "JSON-Vertrag nicht erfuellt"
    if state == "COMPLETED" and spec.get("requires_json_stdout"):
        if not isinstance(_json_from(text), dict):
            state = "FAILED"
            row["detail"] = "JSON-Ausgabe auf stdout fehlt oder ist unparsebar"
    row.update({
        "status": state, "exit_code": exit_code,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "duration_s": round((datetime.now(timezone.utc) - started).total_seconds(), 3),
        "version": tool_version(binary),
        "log": str(log), "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
        "log_truncated": truncated, "output_chars": len(text),
        "artifact": str(outdir / artifact) if artifact else None,
        "artifact_sha256": (hashlib.sha256((outdir / artifact).read_bytes()).hexdigest()
                            if artifact and (outdir / artifact).is_file() else None),
    })
    return row


def _json_from(text):
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except ValueError:
                return None
    return None


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None


def _log_text(row):
    path = row.get("log")
    if not path or not Path(path).is_file():
        return row.get("log_text", "") or ""
    return Path(path).read_text(encoding="utf-8", errors="replace")


def observe(adapter_id, row, outdir):
    """Wandelt ein Werkzeugartefakt in strukturierte Fakten (keine Interpretation)."""
    outdir = Path(outdir)
    # Varianten (-solc) teilen den Parser mit dem Basisadapter, nicht das Artefakt.
    base_id = adapter_id[:-5] if adapter_id.endswith("-solc") else adapter_id
    artifact = ADAPTERS[adapter_id].get("artifact")
    facts = {"adapter": adapter_id, "family": ADAPTERS[adapter_id]["family"],
            "ok": row.get("status") == "COMPLETED"}
    if base_id == "slither-json":
        data = _read_json(outdir / artifact) if artifact else None
        if isinstance(data, dict) and isinstance(data.get("results"), dict):
            dets = data["results"].get("detectors", [])
            facts.update({"parsed": True, "success": data.get("success"),
                          "findings": len(dets),
                          "checks": sorted({d.get("check") for d in dets if d.get("check")}),
                          "high": sorted({d.get("check") for d in dets if d.get("impact") == "High"}),
                          "error": data.get("error")})
        else:
            facts.update({"parsed": False, "findings": 0, "checks": []})
    elif base_id == "myth-json":
        data = _read_json(outdir / artifact) if artifact else None
        issues = (data or {}).get("issues", []) if isinstance(data, dict) else []
        facts.update({"parsed": isinstance(data, dict), "findings": len(issues),
                      "checks": sorted({str(i.get("title", "")).split()[0] for i in issues if i.get("title")})})
    elif base_id in ("forge-test", "forge-match"):
        data = _json_from(_log_text(row))
        tests = {}
        if isinstance(data, dict):
            for suite, body in data.items():
                if not isinstance(body, dict):
                    continue
                for name, result in (body.get("test_results") or {}).items():
                    tests[name] = {"status": result.get("status"), "suite": suite}
        facts.update({"parsed": bool(tests), "tests": tests,
                      "passed": sum(1 for t in tests.values() if t["status"] == "Success"),
                      "failed": sum(1 for t in tests.values() if t["status"] != "Success"),
                      "counterexamples": sorted(n for n, t in tests.items()
                                                if t["status"] == "Success" and COUNTEREXAMPLE_NAME.search(n)),
                      "controls": sorted(n for n, t in tests.items()
                                         if t["status"] == "Success" and CONTROL_NAME.search(n))})
    elif base_id == "echidna-assertion":
        data = _json_from(_log_text(row))
        tests = (data or {}).get("tests", []) if isinstance(data, dict) else []
        falsified = [t for t in tests if t.get("status") in ("falsified", "failed")]
        facts.update({"parsed": isinstance(data, dict), "tests": len(tests),
                      "falsified": len(falsified),
                      "counterexamples": [t.get("name") for t in falsified],
                      "success": (data or {}).get("success") if isinstance(data, dict) else None})
    elif base_id == "medusa-fuzz":
        log = _log_text(row)
        facts.update({"parsed": bool(log.strip()), "failed_assertions":
                      len(re.findall(r"\[FAILED\]|Assertion failed", log)),
                      "coverage_lines": len(re.findall(r"coverage", log, re.I))})
    elif base_id == "solc-compile":
        log = _log_text(row)
        facts.update({"parsed": bool(log.strip()), "bytecode_emitted": "=======" in log})
    elif base_id == "surya-describe":
        log = _log_text(row)
        facts.update({"parsed": bool(log.strip()), "functions": len(re.findall(r"^\s*-\s*\[", log, re.M))})
    elif base_id == "evmasm-disassemble":
        log = _log_text(row)
        facts.update({"parsed": bool(log.strip()), "instructions": len(re.findall(r"^\s*[0-9A-Fa-f]{4}:", log, re.M))})
    else:
        log_path = row.get("log")
        facts.update({"parsed": bool(log_path and Path(log_path).is_file())})
    return facts


# --------------------------------------------------------------------------
# Evidenzpruefung (Inhalt, nicht nur Hash)
# --------------------------------------------------------------------------
def _function_body(text, test_name):
    """Schneidet den Rumpf einer Testfunktion aus der Quelle."""
    needle = re.escape(test_name.split("(")[0])
    m = re.search(rf"function\s+{needle}\s*\([^)]*\)[^{{]*\{{", text)
    if not m:
        return ""
    depth, start = 1, m.end()
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i]
    return text[start:]


def _forge_parse(blob, base, roots=None):
    """Prueft forge-JSON inhaltlich: Status, Assertion im Rumpf, Zustandsbeobachtung."""
    search_roots = [Path(r) for r in (roots or [base])]
    data = _json_from(blob if isinstance(blob, str) else json.dumps(blob))
    if not isinstance(data, dict):
        return {"valid": False, "reason": "kein parsebares forge-JSON"}
    tests, counter, controls, contradictions = {}, [], [], []
    for suite, body in data.items():
        if not isinstance(body, dict):
            continue
        path = Path(str(suite).split(":")[0])
        source = ""
        for root in search_roots:
            for candidate in (root / path, root / "test" / path.name, root / path.name):
                if candidate.is_file():
                    source = candidate.read_text(encoding="utf-8", errors="replace")
                    break
            if source:
                break
        for name, result in (body.get("test_results") or {}).items():
            status = result.get("status")
            tests[name] = status
            if status == "Success" and COUNTEREXAMPLE_NAME.search(name):
                body_text = _function_body(source, name)
                has_assert = bool(re.search(r"\b(require|assert|assertEq|assertTrue|assertLt|assertGt)\s*\(", body_text))
                observes_state = bool(re.search(r"\.balance|\.totalDeposits\(|balances\(|\.calls\(", body_text))
                counter.append({"test": name, "suite": suite, "assertion_in_source": has_assert,
                                "state_observed": observes_state, "source": str(path)})
            if status == "Success" and CONTROL_NAME.search(name):
                controls.append({"test": name, "suite": suite})
            if status != "Success" and COUNTEREXAMPLE_NAME.search(name):
                contradictions.append({"test": name, "status": status})
    valid_counter = [c for c in counter if c["assertion_in_source"] and c["state_observed"]]
    return {"tests": tests, "counterexamples": valid_counter,
            "counterexamples_unasserted": [c for c in counter if c not in valid_counter],
            "controls": controls, "contradictions": contradictions,
            "reason": "ok" if valid_counter and not contradictions else
                      "Counterexample nicht belegt" if not valid_counter else "widerspruechlicher Teststatus"}


def _dynamic_content(blob, base, roots=None):
    """Counterexample-Familie: forge-JSON, forge-Text oder echidna-JSON."""
    data = _json_from(blob)
    if isinstance(data, dict) and any(isinstance(v, dict) and "test_results" in v
                                      for v in data.values()):
        parsed = _forge_parse(blob, base, roots)
        valid = bool(parsed["counterexamples"]) and not parsed["contradictions"]
        return {"valid": valid, "kind": "forge", **parsed}
    if isinstance(data, dict) and isinstance(data.get("tests"), list):
        return _echidna_content(blob)
    passes = re.findall(r"\[PASS\]\s+(\S+)", blob)
    failures = re.findall(r"\[FAIL[^\]]*\]\s+(\S+)", blob)
    hits = [n for n in passes if COUNTEREXAMPLE_NAME.search(n)]
    return {"valid": bool(hits) and not any(COUNTEREXAMPLE_NAME.search(n) for n in failures),
            "kind": "forge-text", "tests": {n: "Success" for n in passes},
            "counterexamples": [{"test": n, "assertion_in_source": None, "state_observed": None}
                                for n in hits],
            "controls": [{"test": n} for n in passes if CONTROL_NAME.search(n)],
            "contradictions": [{"test": n, "status": "Failed"} for n in failures
                               if COUNTEREXAMPLE_NAME.search(n)],
            "reason": "Textbeleg ohne Quell-Assertion" if hits else "kein Counterexample im Text"}


def _control_content(blob, base, roots=None):
    """Negativkontrolle: dieselbe Bedingung ohne Angriff muss halten."""
    data = _json_from(blob)
    if isinstance(data, dict) and any(isinstance(v, dict) and "test_results" in v
                                      for v in data.values()):
        parsed = _forge_parse(blob, base, roots)
        valid = bool(parsed["controls"]) and not parsed["contradictions"]
        return {"valid": valid, "kind": "forge", "controls": parsed["controls"],
                "tests": parsed["tests"], "contradictions": parsed["contradictions"],
                "reason": "ok" if valid else "keine bestandene Kontrolle"}
    passes = re.findall(r"\[PASS\]\s+(\S+)", blob)
    hits = [n for n in passes if CONTROL_NAME.search(n)]
    return {"valid": bool(hits), "kind": "forge-text", "controls": [{"test": n} for n in hits],
            "reason": "ok" if hits else "keine Kontrolle im Text"}


def _echidna_content(blob):
    data = _json_from(blob)
    if not isinstance(data, dict):
        return {"valid": False, "reason": "kein parsebares echidna-JSON"}
    tests = data.get("tests") or []
    falsified = [t for t in tests if t.get("status") in ("falsified", "failed")]
    return {"valid": bool(falsified), "tests": len(tests), "falsified": len(falsified),
            "counterexamples": [{"name": t.get("name"), "transactions": t.get("transactions")} for t in falsified],
            "reason": "ok" if falsified else "keine falsifizierte Property"}


def _static_content(blob):
    data = _json_from(blob)
    if not isinstance(data, dict):
        return {"valid": False, "reason": "kein parsebares Analyse-JSON"}
    if isinstance(data.get("results"), dict):
        dets = data["results"].get("detectors") or []
        return {"valid": bool(data.get("success")) and isinstance(dets, list),
                "tool": "slither", "findings": len(dets),
                "checks": sorted({d.get("check") for d in dets if d.get("check")}),
                "reason": "ok" if data.get("success") else f"slither error: {data.get('error')}"}
    issues = data.get("issues")
    if isinstance(issues, list):
        return {"valid": True, "tool": "mythril", "findings": len(issues),
                "checks": sorted({str(i.get("title", "")).split()[0] for i in issues if i.get("title")}),
                "reason": "ok"}
    return {"valid": False, "reason": "unbekanntes Analyseschema"}


def _state_delta_content(blob):
    data = _json_from(blob)
    if not isinstance(data, dict):
        return {"valid": False, "reason": "kein parsebares Delta-JSON"}
    before, after = data.get("before"), data.get("after")
    relation, metric = data.get("relation"), data.get("metric")
    if not isinstance(before, (int, float)) or not isinstance(after, (int, float)):
        return {"valid": False, "reason": "before/after fehlen oder sind nicht numerisch"}
    checks = {"lt": after < before, "gt": after > before, "eq": after == before}
    if relation not in checks:
        return {"valid": False, "reason": f"unbekannte Relation {relation}"}
    return {"valid": checks[relation], "metric": metric, "before": before,
            "after": after, "relation": relation,
            "reason": "ok" if checks[relation] else f"{after} {relation} {before} ist falsch"}


def verify_evidence(report, base):
    """Inhaltliche Pruefung. Ein Hash beweist Integritaet, nicht Wahrheit."""
    base = Path(base)
    roots = [base] + [Path(str(r)) for r in (report.get("source_roots") or [])]
    rows = report.get("evidence", [])
    artifacts, content, families, content_ok, independent = [], {}, set(), set(), set()
    for row in rows:
        p = Path(str(row.get("path", "")))
        if not p.is_absolute():
            p = base / p
        family = str(row.get("family", ""))
        exists = p.is_file() and p.stat().st_size > 0
        digest = hashlib.sha256(p.read_bytes()).hexdigest() if exists else None
        hash_ok = bool(exists and row.get("sha256") and digest == row.get("sha256"))
        blob = p.read_text(encoding="utf-8", errors="replace") if exists else ""
        if family == "counterexample":
            check = _dynamic_content(blob, base, roots) if exists else {"valid": False, "reason": "Datei fehlt"}
        elif family == "negative_control":
            check = _control_content(blob, base, roots) if exists else {"valid": False, "reason": "Datei fehlt"}
        elif family == "static":
            check = _static_content(blob) if exists else {"valid": False, "reason": "Datei fehlt"}
        elif family == "state_delta":
            check = _state_delta_content(blob) if exists else {"valid": False, "reason": "Datei fehlt"}
        else:
            check = {"valid": bool(exists), "reason": "nur Existenz geprueft"}
        artifacts.append({"path": str(p), "family": family, "exists_nonempty": bool(exists),
                          "sha256_match": hash_ok, "content_valid": bool(check.get("valid")),
                          "check": check})
        if exists and hash_ok:
            families.add(family)
            content[family] = check
            if check.get("valid"):
                content_ok.add(family)
                if family in ("counterexample", "negative_control"):
                    independent.add("dynamic:forge")
                if family == "static":
                    independent.add("static:" + str(check.get("tool")))
                if family == "state_delta":
                    independent.add("state:delta")
    counter = content.get("counterexample", {})
    control = content.get("negative_control")
    static = content.get("static")
    # Widersprueche zaehlen auch dann, wenn die Familie inhaltlich durchfaellt.
    contradictions = list(counter.get("contradictions", [])) if isinstance(counter, dict) else []
    for a in artifacts:
        if a["family"] in ("counterexample", "negative_control"):
            contradictions.extend(a.get("check", {}).get("contradictions") or [])
    # Deklarierte Behauptungen gegen die tatsaechlich extrahierten Checks pruefen.
    claims = []
    for c in report.get("claims", []) or []:
        family, detector = c.get("family"), c.get("detector")
        got = (content.get(family) or {}).get("checks") or []
        claims.append({"family": family, "detector": detector,
                       "supported": bool(detector) and detector in got})
    structural_ready = bool("local_counterexample" in families or
                            (families & {"counterexample"}) and len(families) >= 2)
    # Kompatibilitaet mit der V8-Prototyp-Semantik: local_counterexample + >=2 Familien.
    structural_ready = structural_ready or bool("local_counterexample" in families and len(families) >= 2)
    if contradictions:
        verdict = "INVALID"
    elif (counter and counter.get("valid") and control and control.get("valid")
          and static and static.get("valid")):
        verdict = "VERIFIED_LOCAL"
    elif counter and counter.get("valid"):
        verdict = "PARTIAL"
    elif artifacts and all(a["exists_nonempty"] and a["sha256_match"] for a in artifacts):
        verdict = "STRUCTURAL_ONLY"
    else:
        verdict = "INVALID"
    if claims and not all(c["supported"] for c in claims) and verdict != "INVALID":
        verdict = "PARTIAL"
    return {
        "valid": verdict in ("VERIFIED_LOCAL", "PARTIAL"),
        "verdict": verdict,
        "evidence_families": sorted(families),
        "content_verified_families": sorted(content_ok),
        "artifacts": artifacts,
        "content": content,
        "independent_methods": sorted(independent),
        "contradictions": contradictions,
        "claims": claims,
        "structural_evidence_ready": structural_ready,
        "requires_fresh_independent_execution": True,
        "can_claim_verified_exploit": False,
        "claim": "lokal reproduziert und gegengeprueft" if verdict == "VERIFIED_LOCAL"
                 else "nicht vollstaendig verifiziert",
        "next": ("Ergebnis ist lokal belegt; Freeze vor Referenzzugriff." if verdict == "VERIFIED_LOCAL"
                 else "Fehlende Familie (Counterexample/Negativkontrolle/Statik) nachziehen; "
                      "ohne sie bleibt der Status offen."),
    }


def assess(report, base):
    """Kompatibilitaets-API des V8-Prototyps, jetzt mit Inhaltsprüfung."""
    result = verify_evidence(report, base)
    legacy = {
        "structural_evidence_ready": result["structural_evidence_ready"],
        "evidence_families": result["evidence_families"],
        "artifacts": [{"path": a["path"], "exists_nonempty": a["exists_nonempty"],
                       "sha256_match": a["sha256_match"], "family": a["family"]}
                      for a in result["artifacts"]],
        "requires_fresh_independent_execution": True,
        "can_claim_verified_exploit": False,
        "next": result["next"],
    }
    legacy["content_checks"] = result["content"]
    legacy["verdict"] = result["verdict"]
    return legacy


# --------------------------------------------------------------------------
# Kompatibilitaets-Probe (unveraendert)
# --------------------------------------------------------------------------
def execute_static(target, outdir, allow_execute=False, timeout=90):
    """One-at-a-time bounded static probes on an authorized local Solidity file.

    Not a security sandbox: do not use on unknown/untrusted projects without
    reviewing dependencies first. No shell, no automatic installs, no RPC,
    no wallet, no fuzz harness or benchmark answer lookup.
    """
    if not allow_execute:
        raise ValueError("execution requires explicit --allow-exec")
    target = Path(target).resolve(strict=True)
    if not target.is_file() or target.suffix.lower() != ".sol":
        raise ValueError("target must be a regular .sol file")
    if not 1 <= timeout <= 180:
        raise ValueError("timeout must be 1..180 seconds")
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    commands = [
        ("surya", ["surya", "describe", str(target)]),
        ("slither", ["slither", str(target), "--json", str(outdir / "slither.json")]),
    ]
    rows = []
    for name, command in commands:
        start = datetime.now(timezone.utc).isoformat()
        if not enough_memory():
            rows.append({"tool": name, "status": "SKIPPED_RESOURCE_PRESSURE", "command": command[:2]})
            break
        binary = shutil.which(command[0])
        if not binary:
            rows.append({"tool": name, "status": "UNAVAILABLE", "command": command[:2]})
            continue
        try:
            child = subprocess.Popen([binary, *command[1:]], shell=False,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     cwd=str(target.parent), start_new_session=True)
            try:
                raw, _ = child.communicate(timeout=timeout)
                output = (raw or b"")[-500_000:].decode("utf-8", "replace")
                exit_code = child.returncode
                state = "EXECUTED_NONZERO" if exit_code else "EXECUTED_ZERO"
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                raw, _ = child.communicate()
                output = (raw or b"")[-100_000:].decode("utf-8", "replace")
                state = "TIMEOUT"
                exit_code = None
        except OSError as exc:
            output = str(exc)
            state = "EXECUTION_ERROR"
            exit_code = None
        log = outdir / (name + ".log")
        log.write_text(output, encoding="utf-8")
        rows.append({"tool": name, "started_at": start, "status": state,
                     "exit_code": exit_code, "log": str(log),
                     "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()})
    receipt = {"target": str(target), "time_utc": datetime.now(timezone.utc).isoformat(),
               "runs": rows, "completion": "STATIC_ONLY; no proof of exploitability",
               "next": "Review output; construct local Foundry/fuzz counterexample and independent state check."}
    (outdir / "execution-receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return receipt


# --------------------------------------------------------------------------
# Laufzeit: Plan ausfuehren, beobachten, adaptieren
# --------------------------------------------------------------------------
def _evidence_rows(outdir, facts):
    """Eine Zeile je Familie; die tatsaechlich erzeugten Artefakte entscheiden."""
    rows = []
    outdir = Path(outdir)

    def add(name, family):
        p = outdir / name
        if p.is_file() and p.stat().st_size:
            rows.append({"path": p.name, "family": family,
                         "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
            return True
        return False
    if not add("slither.json", "static"):
        if not add("slither-solc.json", "static"):
            add("myth.json", "static")
    if not add("forge-test.log", "counterexample"):
        echidna = (facts or {}).get("COUNTEREXAMPLE_FALLBACK", {})
        if echidna.get("falsified"):
            add("echidna-assertion.log", "counterexample")
    add("forge-match.log", "negative_control")
    return rows


def run_plan(plan, outdir, allow_exec=False, allow_network=False, timeout_scale=1.0):
    """Fuehrt die Adapter des Plans aus, beobachtet, adaptiert, verifiziert."""
    if not allow_exec:
        raise ValueError("execution requires explicit --allow-exec")
    if plan.get("status") != "PLANNED_NOT_EXECUTED":
        return {"status": "NO_PLAN", "plan_status": plan.get("status"),
                "routing": plan.get("routing")}
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    ctx = dict(plan.get("context") or {})
    ctx.setdefault("target", plan["context"].get("target"))
    ctx.update({"outdir": str(outdir), "myth_timeout": "30",
                "test_limit": "5000", "medusa_timeout": "60",
                "match_test": "test_invariant_holds_initially"})
    steps = [dict(s) for s in plan["steps"]]
    receipts, facts, decisions, states = [], {}, [], {}
    extra_all = []
    extra = []
    queue = list(steps)

    def find(sid):
        return next((s for s in queue + extra if s["id"] == sid), None)

    while queue:
        step = queue.pop(0)
        sid = step["id"]
        deps = [find(d) for d in step["depends_on"]]
        dep_failed = [d["id"] for d in deps if d and d.get("status") in FAILED_STATES]
        if step["adapter"] is None:
            step["status"] = "KNOWLEDGE_ONLY"
            states[sid] = step["status"]
            decisions.append({"after": sid, "observation": "kein Adapter (Wissens-/Pruefschritt)",
                              "decision": "als Wissensschritt gefuehrt", "effect": "keine Ausfuehrung"})
            continue
        if dep_failed and sid not in ("STATIC",):
            step["status"] = "BLOCKED"
            states[sid] = "BLOCKED"
            decisions.append({"after": sid, "observation": f"Vorbedingung fehlt: {dep_failed}",
                              "decision": "Schritt blockiert", "effect": "dokumentierter Blocker"})
            continue
        info = step.get("availability") or availability(step["adapter"])
        if not info.get("available"):
            step["status"] = "UNAVAILABLE"
            states[sid] = "UNAVAILABLE"
            decisions.append({"after": sid, "observation": f"{step['adapter']} nicht im PATH",
                              "decision": "UNAVAILABLE, Fallback pruefen",
                              "effect": f"Kandidaten: {ADAPTERS[step['adapter']]['fallback']}"})
            for fb in ADAPTERS[step["adapter"]]["fallback"]:
                # Adapter-Label != Binary-Name (mythril -> myth).
                fb_bin = BINARIES.get(ADAPTERS[fb]["tool"], ADAPTERS[fb]["tool"]) if fb in ADAPTERS else None
                if fb in ADAPTERS and fb_bin and shutil.which(fb_bin):
                    extra.append({"id": f"{sid}_FALLBACK", "capability": step["capability"],
                                  "adapter": fb, "depends_on": list(step["depends_on"]),
                                  "inputs": {"target": ctx.get("target"),
                                             "project": ctx.get("project"),
                                             "contract": ctx.get("contract")},
                                  "acceptance": ADAPTERS[fb]["acceptance"], "argv_override": None,
                                  "availability": availability(fb), "status": "READY",
                                  "on_failure": []})
                    decisions.append({"after": sid, "observation": f"Fallback {fb} verfuegbar",
                                      "decision": "alternativen Adapter einsetzen", "effect": fb})
                    break
            continue
        if step["adapter"] == "cryo-blocks" and not allow_network:
            step["status"] = "BLOCKED"
            states[sid] = "BLOCKED"
            decisions.append({"after": sid, "observation": "Netzwerkadapter ohne --allow-network",
                              "decision": "keine Netzwerkoperation", "effect": "BLOCKED"})
            continue
        step["status"] = "READY"
        states[sid] = "READY"
        # forge-match braucht einen Override, der Adapter heisst forge-match
        adapter = step["adapter"]
        if step.get("argv_override"):
            saved = ADAPTERS[adapter]["argv"]
            ADAPTERS[adapter]["argv"] = step["argv_override"]
            try:
                row = run_adapter(adapter, ctx, outdir, ADAPTERS[adapter]["timeout"] * timeout_scale)
            finally:
                ADAPTERS[adapter]["argv"] = saved
        else:
            row = run_adapter(adapter, ctx, outdir, ADAPTERS[adapter]["timeout"] * timeout_scale)
        states[sid] = "INVOKED"
        row["step_id"] = sid
        if row.get("log") and Path(row["log"]).is_file():
            row["log_text"] = Path(row["log"]).read_text(encoding="utf-8", errors="replace")
        receipts.append(row)
        step["status"] = "COMPLETED" if row["status"] == "COMPLETED" else row["status"]
        states[sid] = "COMPLETED" if row["status"] == "COMPLETED" else row["status"]
        observed = observe(adapter, row, outdir)
        facts[sid] = observed
        decisions.append({"after": sid, "observation": {k: observed[k] for k in
                                                          ("findings", "checks", "counterexamples", "controls",
                                                           "falsified", "passed", "failed") if k in observed},
                          "decision": "beobachten", "effect": step["status"]})
        # --- Adaption an das Ergebnis ---
        if sid == "STATIC" and observed.get("findings") == 0 and row["status"] == "COMPLETED":
            decisions.append({"after": sid, "observation": "Statik ohne Treffer",
                              "decision": "kein statischer Treffer ist kein Sicherheitsbeweis",
                              "effect": "dynamische Gegenprobe bleibt erforderlich"})
        solc_variant = adapter + "-solc"
        compiler_error = (row["status"] == "FAILED" and solc_variant in ADAPTERS
                          and COMPILER_HINT.search(_log_text(row))
                          and shutil.which(BINARIES.get(ADAPTERS[solc_variant]["tool"],
                                                        ADAPTERS[solc_variant]["tool"])))
        if compiler_error:
            # Diagnose statt Wiederholung: gleiche Methode, andere Compiler-Annahme.
            extra.append({"id": f"{sid}_SOLC", "capability": step["capability"],
                          "adapter": solc_variant, "depends_on": list(step["depends_on"]),
                          "inputs": {"target": ctx.get("target"), "project": ctx.get("project"),
                                     "contract": ctx.get("contract")},
                          "acceptance": ADAPTERS[solc_variant]["acceptance"],
                          "argv_override": None, "availability": availability(solc_variant),
                          "status": "READY", "on_failure": []})
            decisions.append({"after": sid,
                              "observation": "Compiler-/Framework-Fehler im Log erkannt",
                              "decision": "Compiler-Annahme isolieren statt blind wiederholen",
                              "effect": solc_variant})
        elif (row["status"] in ("FAILED", "UNAVAILABLE", "TIMEOUT")
                and ADAPTERS[adapter]["fallback"]):
            for fb in ADAPTERS[adapter]["fallback"]:
                fb_bin = BINARIES.get(ADAPTERS[fb]["tool"], ADAPTERS[fb]["tool"]) if fb in ADAPTERS else None
                if fb in ADAPTERS and fb_bin and shutil.which(fb_bin):
                    extra.append({"id": f"{sid}_FALLBACK", "capability": step["capability"],
                                  "adapter": fb, "depends_on": list(step["depends_on"]),
                                  "inputs": {"target": ctx.get("target"),
                                             "project": ctx.get("project"),
                                             "contract": ctx.get("contract")},
                                  "acceptance": ADAPTERS[fb]["acceptance"], "argv_override": None,
                                  "availability": availability(fb), "status": "READY",
                                  "on_failure": []})
                    decisions.append({"after": sid, "observation": f"{adapter} {row['status']} (exit={row.get('exit_code')})",
                                      "decision": "Diagnose statt Wiederholung", "effect": f"Fallback {fb}"})
                    break
        if sid == "COUNTEREXAMPLE" and adapter == "forge-test":
            obs = facts.get(sid, {})
            if obs.get("contradictions"):
                decisions.append({"after": sid, "observation": "Counterexample-Test schlaegt fehl",
                                  "decision": "Widerspruch zwischen Werkzeug und Test",
                                  "effect": "discriminating test erforderlich"})
            elif not obs.get("counterexamples"):
                decisions.append({"after": sid, "observation": "kein Counterexample-Test im Projekt",
                                  "decision": "Fuzzer als Gegenprobe einsetzen",
                                  "effect": "echidna-assertion"})
                if shutil.which("echidna") and ctx.get("contract"):
                    extra.append({"id": "COUNTEREXAMPLE_ALT", "capability": "counterexample",
                                  "adapter": "echidna-assertion", "depends_on": ["HYPOTHESES"],
                                  "inputs": {"target": ctx.get("target"), "contract": ctx.get("contract")},
                                  "acceptance": ADAPTERS["echidna-assertion"]["acceptance"],
                                  "argv_override": None,
                                  "availability": availability("echidna-assertion"),
                                  "status": "READY", "on_failure": []})
        if sid == "COUNTEREXAMPLE" and adapter == "echidna-assertion":
            obs = facts.get(sid, {})
            if obs.get("falsified"):
                decisions.append({"after": sid, "observation": f"{obs['falsified']} falsifizierte Propertie(s)",
                                  "decision": "Counterexample vorhanden",
                                  "effect": "Verifikation der Wirkung noetig"})
                if not any(s["id"] == "forge-match" for s in queue + extra) and ctx.get("project"):
                    extra.append({"id": "NEGATIVE_CONTROL", "capability": "negative_control",
                                  "adapter": "forge-match", "depends_on": ["COUNTEREXAMPLE"],
                                  "inputs": {"project": ctx.get("project")},
                                  "acceptance": "Gegenbedingung haelt",
                                  "argv_override": ["test", "--json", "--match-test",
                                                    "test_invariant_holds_initially"],
                                  "availability": availability("forge-match"),
                                  "status": "READY", "on_failure": []})
        if extra:
            extra_all.extend(extra)
        queue.extend(extra)
        extra = []

    # Verifikation aus den tatsaechlichen Artefakten
    rows = _evidence_rows(outdir, facts)
    report = {"task": plan["task"], "created_at": datetime.now(timezone.utc).isoformat(),
              "evidence": rows,
              "source_roots": [ctx[k] for k in ("project",) if ctx.get(k)]}
    (outdir / "evidence-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    verification = verify_evidence(report, outdir)
    summary = {
        "task": plan["task"],
        "mode": plan["routing"].get("mode"),
        "outdir": str(outdir),
        "resources": resources(),
        "steps": [{k: s.get(k) for k in ("id", "capability", "adapter", "depends_on", "status", "acceptance")}
                  for s in steps + []],
        "extra_steps": [{k: s.get(k) for k in ("id", "capability", "adapter", "depends_on", "status")}
                        for s in extra_all],
        "states": states,
        "decisions": decisions,
        "receipts": receipts,
        "facts": facts,
        "evidence_report": str(outdir / "evidence-report.json"),
        "verification": verification,
        "status": "VERIFIED" if verification["verdict"] == "VERIFIED_LOCAL" else
                  "COMPLETED_UNVERIFIED" if any(r["status"] == "COMPLETED" for r in receipts) else
                  "BLOCKED",
        "state_machine": STATES,
    }
    (outdir / "run-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("route", help="Retrieve relevant skills and dependency DAG as JSON; does NOT run them")
    p.add_argument("--task", required=True)
    p.add_argument("--mode", choices=["auto", "source", "fork", "historical", "bytecode"], default="auto")
    p.add_argument("--root", type=Path, default=default_root())
    p.add_argument("--manifest", type=Path)
    p.add_argument("--top-k", type=int, default=7)
    p.add_argument("--pick", default="", help="Komma-getrennte Modellauswahl (semantische Bewertung)")

    pl = sub.add_parser("plan", help="Executable plan: adapters, availability, recovery, acceptance")
    pl.add_argument("--task", required=True)
    pl.add_argument("--mode", choices=["auto", "source", "fork", "historical", "bytecode"], default="auto")
    pl.add_argument("--target", type=Path)
    pl.add_argument("--project", type=Path)
    pl.add_argument("--contract")
    pl.add_argument("--root", type=Path, default=default_root())
    pl.add_argument("--manifest", type=Path)
    pl.add_argument("--top-k", type=int, default=7)
    pl.add_argument("--pick", default="")

    r = sub.add_parser("run", help="Actually execute the planned adapters, observe, adapt, verify")
    r.add_argument("--task", required=True)
    r.add_argument("--mode", choices=["auto", "source", "fork", "historical", "bytecode"], default="auto")
    r.add_argument("--target", type=Path)
    r.add_argument("--project", type=Path)
    r.add_argument("--contract")
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("--root", type=Path, default=default_root())
    r.add_argument("--manifest", type=Path)
    r.add_argument("--top-k", type=int, default=7)
    r.add_argument("--pick", default="")
    r.add_argument("--allow-exec", action="store_true")
    r.add_argument("--allow-network", action="store_true")
    r.add_argument("--timeout-scale", type=float, default=1.0)

    e = sub.add_parser("probe", help="Compatibility: bounded local static probes (surya, slither)")
    e.add_argument("--target", type=Path, required=True)
    e.add_argument("--out", type=Path, required=True)
    e.add_argument("--allow-exec", action="store_true")
    e.add_argument("--timeout", type=int, default=90)

    v = sub.add_parser("assess", help="Check evidence files and hash provenance; not an exploit proof")
    v.add_argument("--report", type=Path, required=True)

    vf = sub.add_parser("verify", help="Content-level verification of evidence artifacts")
    vf.add_argument("--report", type=Path, required=True)

    sc = sub.add_parser("selfcheck", help="Catalog, adapter and evidence-engine sanity checks")
    sc.add_argument("--root", type=Path, default=default_root())

    cp = sub.add_parser("copilot", help="GitHub Copilot delegation workflow (Freebuff-led)",
                        add_help=False)
    cp.add_argument("args", nargs=argparse.REMAINDER,
                    help="subcommand and flags for bin/copilot-delegate.py")

    args, extra = parser.parse_known_args()
    if extra and args.cmd != "copilot":
        parser.error("unrecognized arguments: " + " ".join(extra))
    try:
        if args.cmd == "route":
            if not (1 <= args.top_k <= 16):
                parser.error("top-k must be 1..16")
            pick = [s for s in args.pick.split(",") if s.strip()]
            result = route(args.task, args.root, args.manifest, args.mode, args.top_k, pick)
        elif args.cmd == "plan":
            ctx = {"target": args.target, "project": args.project, "contract": args.contract}
            pick = [s for s in args.pick.split(",") if s.strip()]
            result = compose(args.task, args.root, args.manifest, args.mode, args.top_k, ctx, pick)
            if pick and result.get("routing", {}).get("candidates") is not None:
                skills = read_manifest(args.root, args.manifest)
                kept, rejected = _semantic_pick(args.task, skills, pick)
                result["semantic_selection"] = {"accepted": kept, "rejected": rejected}
        elif args.cmd == "run":
            ctx = {"target": args.target, "project": args.project, "contract": args.contract}
            pick = [s for s in args.pick.split(",") if s.strip()]
            plan = compose(args.task, args.root, args.manifest, args.mode, args.top_k, ctx, pick)
            result = run_plan(plan, args.out, args.allow_exec, args.allow_network, args.timeout_scale)
        elif args.cmd == "probe":
            result = execute_static(args.target, args.out, args.allow_exec, args.timeout)
        elif args.cmd == "verify":
            result = verify_evidence(json.loads(args.report.read_text(encoding="utf-8")),
                                     args.report.resolve().parent)
        elif args.cmd == "selfcheck":
            result = selfcheck(args.root)
        elif args.cmd == "copilot":
            sys.exit(run_copilot(list(args.args or []) + list(extra or [])))
        else:
            result = assess(json.loads(args.report.read_text(encoding="utf-8")),
                            args.report.resolve().parent)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"orchestrator error: {exc}", file=sys.stderr)
        sys.exit(2)


def run_copilot(argv):
    """Delegate to the Copilot layer in-process (no shell, same interpreter)."""
    import importlib.util
    path = Path(__file__).resolve().parent / "copilot-delegate.py"
    spec = importlib.util.spec_from_file_location("sfs_copilot_delegate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main(list(argv or []))


def selfcheck(root=None):
    root = Path(root or default_root())
    skills = read_manifest(root)
    table = {aid: availability(aid) for aid in ADAPTERS}
    # Negativtests der Evidenz-Engine: gefaelschte Evidenz darf nicht bestehen.
    probes = []
    probes.append({"case": "missing-file", "verdict":
                   verify_evidence({"evidence": [{"path": "nope.json", "family": "static", "sha256": "0" * 64}]},
                                   root)["verdict"]})
    probes.append({"case": "hash-mismatch", "verdict":
                   verify_evidence({"evidence": [{"path": str(root / "README.md"), "family": "static",
                                                  "sha256": "0" * 64}]}, root)["verdict"]})
    return {
        "root": str(root),
        "catalog_entries": len(skills),
        "states": STATES,
        "adapters": table,
        "available_adapters": sorted(k for k, v in table.items() if v["available"]),
        "unavailable_adapters": sorted(k for k, v in table.items() if not v["available"]),
        "resources": resources(),
        "reserve": reserve_ok(),
        "negative_probes": probes,
        "negative_probes_pass": all(p["verdict"] == "INVALID" for p in probes),
    }


if __name__ == "__main__":
    main()
