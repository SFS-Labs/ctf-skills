#!/usr/bin/env bash
# diffusc ohne git installieren — belegter Weg (getestet 2026-11-21).
#
# Warum kein git noetig ist:
#   `setup.py` deklariert genau eine git-Abhaengigkeit:
#       "slither-analyzer@git+https://github.com/webthethird/slither.git@dev-diffusc-testing"
#   Der Code selbst ruft nirgends git auf (verifiziert per grep ueber *.py).
#   -> Wir holen den Fork als codeload-TARBALL und installieren ihn lokal.
#
# Zwei lokale Patches sind noetig (beide idempotent):
#   1. diffusc/diffusc.py: `require("diffusc")[0].version` -> feste Version.
#      pkg_resources.require() scheitert an der git-URL in Requires-Dist (VersionConflict).
#   2. solc_select im venv: urllib ohne User-Agent bekommt 403 von binaries.soliditylang.org
#      (sowohl list.json als auch der solc-Download via urlretrieve).
#
# Zusatz: forge muss im PATH sein, sonst waehlt crytic-compile das Foundry-Plugin und
# scheitert mit FileNotFoundError: 'forge'. Alternativ Ziel ohne foundry.toml nutzen.
#
# Zusatz 2 (von bin/smoke gefunden): Pfade muessen einen Verzeichnis-Separator enthalten.
#   slither_provider.py:155 rechnet path.rsplit(os.sep, 1)[1] -> bei "VaultV1.sol"
#   IndexError: list index out of range. Also absolute Pfade uebergeben, nie nackte Dateinamen.
set -euo pipefail
H="${HOME}/ctf-skills"
export PATH="${HOME}/.local/bin:${HOME}/.foundry/bin:${HOME}/.cargo/bin:${PATH}"
TOKEN="$(cat "${HOME}/.config/gh-token" 2>/dev/null || echo "${GITHUB_TOKEN:-}")"
VPY="${H}/venvs/diffusc/bin/python"

echo "[1/5] Slither-Fork als Tarball (kein git)"
mkdir -p /tmp/slither-fork
curl -sSL -H "Authorization: Bearer ${TOKEN}" -o /tmp/slither-fork.tgz \
  "https://codeload.github.com/webthethird/slither/tar.gz/refs/heads/dev-diffusc-testing"
tar -xzf /tmp/slither-fork.tgz -C /tmp/slither-fork --strip-components=1

echo "[2/5] venv + Abhaengigkeiten"
uv venv "${H}/venvs/diffusc" --python 3.10
uv pip install --python "${VPY}" /tmp/slither-fork
uv pip install --python "${VPY}" --no-deps -e "${H}/vendor/crytic/diffusc"
uv pip install --python "${VPY}" colorama 'setuptools<81' packaging eth_typing eth_utils \
  "crytic-compile>=0.3.1,<0.4.0" "web3<7" "requests~=2.28.2"

echo "[3/5] Patch 1: pkg_resources.require in diffusc.py"
python3 - "${H}/vendor/crytic/diffusc/diffusc/diffusc.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
if 'require("diffusc")[0].version' in s:
    open(p, "w").write(s.replace('require("diffusc")[0].version', '"0.1.1"'))
    print("  gepatcht")
else:
    print("  bereits gepatcht")
PY

echo "[4/5] Patch 2: solc_select User-Agent (list.json + Download)"
python3 - "${H}/venvs/diffusc/lib/python3.10/site-packages/solc_select/solc_select.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
UA = "{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}"
s = s.replace(
    "list_json = urllib.request.urlopen(list_url).read()",
    f"list_json = urllib.request.urlopen(urllib.request.Request(list_url, headers={UA})).read()")
s = s.replace(
    'urllib.request.urlretrieve(url, artifact_file_dir.joinpath(f"solc-{version}"))',
    f'_req = urllib.request.Request(url, headers={UA})\n'
    '        with urllib.request.urlopen(_req) as _r, open(artifact_file_dir.joinpath(f"solc-{version}"), "wb") as _o:\n'
    '            _o.write(_r.read())')
open(p, "w").write(s)
print("  gepatcht")
PY

echo "[5/5] Smoke-Test"
"${H}/venvs/diffusc/bin/diffusc" --help 2>&1 | grep -vE 'UserWarning|pkg_resources' | head -3
echo "Aufruf: diffusc <v1.sol> <v2.sol> -d <out/>   (Dateinamen VaultV1.sol/VaultV2.sol, Contract 'Vault')"
