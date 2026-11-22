#!/usr/bin/env bash
# slither gegen einen Contract aus dem vendor-Baum — End-to-End ohne Zusatz-Setup.
#
# Warum: die Karten behaupten, slither sei das Statik-Rueckgrat. Dieser Lauf zeigt es
# an einem *geholten* Skill (Manifest -> vendor/<org>/<repo>), nicht an einem Fixture.
# Der Contract wird in ein temporaeres Verzeichnis kopiert, damit slither keine
# Fremdimporte aus dem Repo zu ziehen versucht; der vendor-Baum bleibt unberuehrt.
#
# Aufruf: recipes/slither-vendor.sh [slug] [pfad/datei.sol]
# Standard: evmyullean (der Nethermind-Fork EVMYulLean ist Alias darauf, keine zweite Kopie)
# Exit:   0 analysiert · 2 Contract/Pfad fehlt · 3 slither-Fehler
set -euo pipefail
H="${HOME}/ctf-skills"
slug="${1:-evmyullean}"
rel="${2:-EvmYul/Yul/YulSemanticsTests/Storage.sol}"

src=$(python3 - "$H/manifest.json" "$slug" "$rel" <<'PY'
import json, os, sys
m = {s["slug"]: s for s in json.load(open(sys.argv[1]))["skills"]}
if sys.argv[2] not in m:
    sys.exit("unbekannter Slug: %s" % sys.argv[2])
print(os.path.join(os.path.expanduser("~"), "ctf-skills", m[sys.argv[2]]["vendor"], sys.argv[3]))
PY
) || { echo "Slug/Pfad nicht aufloesbar"; exit 2; }
[ -f "$src" ] || { echo "Contract nicht gefunden: $src"; exit 2; }

work=$(mktemp -d)
cp "$src" "$work/"
cd "$work"
echo "Skill  : $slug"
echo "Quelle : $src"
echo "solc   : $(solc --version 2>/dev/null | sed -n '2p')"

slither "$(basename "$src")" --json report.json >slither.log 2>&1 || true
summary=$(grep -m1 "analyzed (" slither.log | sed 's/^INFO:Slither://' || true)
[ -n "$summary" ] || { echo "slither hat nichts analysiert:"; tail -n 8 slither.log; exit 3; }
echo "slither : $summary"
python3 - report.json <<'PY' || exit 3
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except (OSError, ValueError) as exc:
    sys.exit("kein slither-JSON (%s)" % exc)
res = d.get("results", {}).get("detectors", [])
print("Ergebnis: %d Befund(e) im JSON" % len(res))
for r in res[:5]:
    print("  - %s (%s, %s)" % (r.get("check"), r.get("impact"), r.get("confidence")))
PY
