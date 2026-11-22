#!/usr/bin/env python3
"""tool_matrix — eine Klassifikation fuer Messung (`bin/doctor`) und Karte (`bin/gen_skills`).

Warum ein Modul:
  Vorher lagen PROBE/LIB/REF nur in `bin/doctor`. `bin/gen_skills` wusste davon nichts und
  schrieb fuer jedes Werkzeug `"<slug> --help"` in die Karte — auch fuer die 26 Eintraege,
  die gar kein CLI haben (npm 404, kein Linux-Binary, Web-App). Die Karte behauptete damit
  einen Aufruf, den die Messung eine Datei weiter als unmoeglich auswies.

  Jetzt gibt es genau eine Tabelle. `doctor` probiert die PROBE-Binaries wirklich aus,
  `gen_skills` uebernimmt REF/LIB woertlich und prueft PROBE nur per `shutil.which`
  (kein Start, keine Laufzeitbehauptung).

Datenpflege: Aenderungen hier gelten fuer beide Seiten; ein Eintrag, der in keiner der drei
Tabellen steht, ist in `doctor` ein FAIL und in der Karte `unklassifiziert`.
"""

# --- Werkzeuge: Binary, das antworten muss ------------------------------------
PROBE = {
    "cryo": "cryo", "diffusc": "diffusc", "echidna": "echidna", "medusa": "medusa",
    "rbuilder": "rbuilder", "solar": "solar", "iron-proxy": "iron-proxy",
    "mev-boost": "mev-boost", "surya": "surya", "slither": "slither",
    "crytic-compile": "crytic-compile", "mythril": "myth", "pyevmasm": "evmasm",
    "etheno": "etheno", "daedaluzz": "daedaluzz", "slither-mcp": "slither-mcp",
    "solc-select": "solc-select", "scribble": "scribble",
    "evm-cfg-builder": "evm-cfg-builder", "fuzz-utils": "fuzz-utils",
    "mev-inspect-py": "inspect-block", "legions": "legions",
}

# --- Bibliotheken: installiert, aber ohne eigenes CLI --------------------------
LIB = {
    "oz-upgrades": ("node", "@openzeppelin/upgrades-core"),
    "defender-sdk": ("node", "@openzeppelin/defender-sdk"),
    "oz-foundry-upgrades": ("node", "@openzeppelin/foundry-upgrades"),
}

# --- Referenz: kein Lauf ohne Bau, Docker oder Nutzerentscheidung --------------
R_NOASSET = ("kein Linux-Binary im letzten Release (API-Abfrage 2026-11-21); "
             "Bau aus {p} mit cargo/go noetig")
R_404 = "Repo-API 404 (Quelle nicht mehr oeffentlich); Quellbaum liegt in {p}"
R_CARGO_P = "Rust/Cargo-Projekt ohne Prebuilt ({p}); cargo build noetig"
R_NONPM = "kein npm-Paket dieses Namens (Registry 404); Inhalt ist Web-App/Repo"
R_NOBIN = "npm-Paket ohne bin; require scheitert (MODULE_NOT_FOUND)"
R_VSIX = "VS-Code-Extension (.vsix), nicht headless aufrufbar"
R_WEBAPP = "Web-App (frontend/backend/assets), kein CLI"
R_CARGO = "Rust/Cargo-Projekt ohne Prebuilt; cargo build im vendor-Baum noetig"
R_MANTICORE = ("uv tool installiert (3.9/3.10); Start scheitert an protobuf-Descriptor "
               "bzw. wasm/collections.Callable -> gepinnte Umgebung noetig")

REF = {
    # release-binary ohne Prebuilt / ohne oeffentliche Quelle
    "bytecode-verifier": R_404, "mev-share-rs": R_404, "r55": R_404,
    "diligence-fuzzing": R_NOASSET, "dstack": R_NOASSET, "fluxture": R_NOASSET,
    "mev-boost-relay": R_NOASSET, "optik": R_NOASSET, "rollup-boost": R_NOASSET,
    "soroban-detectors": R_NOASSET,
    # uv tool, aber kein CLI bzw. Bau noetig
    "evmbench": R_WEBAPP, "chainsecurity-deployment-validation": R_CARGO_P,
    "manticore": R_MANTICORE,
    # npm -g, aber kein nutzbares CLI
    "abi-guesser": R_NONPM, "canonical-signatures": R_NONPM, "damn-vulnerable-defi": R_NONPM,
    "ethernaut": R_NONPM, "openchain-monorepo": R_NONPM, "openchain-tx-viewer": R_NONPM,
    "oz-monitor": R_NONPM, "seal-intel-sdk": R_NONPM, "sfs-dvca": R_NONPM,
    "verifiable-phishing-reporter": R_NONPM,
    "napalm": R_NOBIN, "transaction-decoder": R_NOBIN,
    "vscode-solidity-auditor": R_VSIX,
}

__all__ = ["PROBE", "LIB", "REF", "R_CARGO"]
