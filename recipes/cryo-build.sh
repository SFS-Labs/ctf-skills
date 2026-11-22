#!/usr/bin/env bash
# cryo ohne Root bauen — belegter Weg (getestet 2026-11-21, Linux Mint 22.3 / glibc 2.39).
#
# Warum das noetig ist:
#   * cryo hat KEIN Release-Asset (GitHub-Releases-API: 1 Release "0.2.0" ohne Assets),
#     also ist ein fertiges Binary nicht verfuegbar -> Selbstbau ist der einzige Weg.
#   * cryo zieht ueber alloy/reqwest `openssl-sys` (native-tls). Auf diesem System fehlen
#     die Dev-Header (nur libssl.so.3 ist installiert), libssl-dev ist nicht installiert.
#   * `apt-get download` braucht KEIN Root — es laedt nur das .deb in das aktuelle Verzeichnis.
#     Mit dpkg-deb -x entpacken wir es nach ~/.local und zeigen openssl-sys per
#     OPENSSL_INCLUDE_DIR / OPENSSL_LIB_DIR darauf.
#   * ethnum 1.5.0 kompiliert auf rustc >= 1.8x nicht mehr (E0512, transmute(())).
#     `cargo update -p ethnum` hebt es auf eine kompatible 1.x-Version.
#
# Ergebnis: ~/ctf-skills/tools/cryo/bin/cryo
set -euo pipefail
H="${HOME}/ctf-skills"
export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${PATH}"
OSSL="${HOME}/.local/openssl-dev"

echo "[1/4] libssl-dev ohne Root holen und entpacken"
mkdir -p "${OSSL}" /tmp/cryo-build
cd /tmp/cryo-build
apt-get download libssl-dev >/dev/null
dpkg-deb -x libssl-dev_*.deb "${OSSL}"

echo "[2/4] Header und Linker-Stubs an den erwarteten Ort legen"
mkdir -p "${OSSL}/usr/include/openssl" "${OSSL}/usr/lib/x86_64-linux-gnu"
cp -n "${OSSL}"/usr/include/x86_64-linux-gnu/openssl/*.h "${OSSL}/usr/include/openssl/" 2>/dev/null || true
for lib in libssl.so.3 libcrypto.so.3; do
  [ -e "${OSSL}/usr/lib/x86_64-linux-gnu/${lib}" ] || \
    ln -s "/usr/lib/x86_64-linux-gnu/${lib}" "${OSSL}/usr/lib/x86_64-linux-gnu/${lib}"
done

echo "[3/4] ethnum auf kompatible Version heben"
cd "${H}/vendor/paradigmxyz/cryo"
cargo update -p ethnum

echo "[4/4] bauen"
export OPENSSL_INCLUDE_DIR="${OSSL}/usr/include"
export OPENSSL_LIB_DIR="${OSSL}/usr/lib/x86_64-linux-gnu"
mkdir -p "${H}/tools/cryo"
cargo install --path "${H}/vendor/paradigmxyz/cryo/crates/cli" --bin cryo --root "${H}/tools/cryo"
ln -sf "${H}/tools/cryo/bin/cryo" "${HOME}/.local/bin/cryo"
echo "fertig: $(command -v cryo) -> $("${H}/tools/cryo/bin/cryo" --version 2>&1 | head -1)"
