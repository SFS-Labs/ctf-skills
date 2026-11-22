#!/usr/bin/env bash
# daedaluzz ohne Root bauen — belegter Weg (getestet 2026-11-21).
#
# daedaluzz ist ein Go-Programm (go.mod: "go 1.15", Deps: logrus, urfave/cli).
# Es ist KEIN Python-Tool — die fruehere Einordnung im Plan war falsch.
#
# Vorgehen: Go-Toolchain als Userspace-Tarball nach ~/.local/opt (kein Root, keine
# Systemdateien), dann `go build` im vendor-Baum. Caches bleiben unter tools/daedaluzz.
set -euo pipefail
H="${HOME}/ctf-skills"
GO_VERSION="1.23.4"

echo "[1/3] Go-Toolchain nach ~/.local/opt"
if [ ! -x "${HOME}/.local/opt/go/bin/go" ]; then
  curl -sSL --max-time 600 -o /tmp/go.tgz "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz"
  mkdir -p "${HOME}/.local/opt"
  tar -C "${HOME}/.local/opt" -xzf /tmp/go.tgz
fi
export PATH="${HOME}/.local/opt/go/bin:${HOME}/.local/bin:${PATH}"
go version

echo "[2/3] bauen"
mkdir -p "${H}/tools/daedaluzz"
cd "${H}/vendor/ConsenSysDiligence/daedaluzz"
GOFLAGS=-mod=mod GOCACHE="${H}/tools/daedaluzz/.gocache" \
  go build -o "${H}/tools/daedaluzz/daedaluzz" .
ln -sf "${H}/tools/daedaluzz/daedaluzz" "${HOME}/.local/bin/daedaluzz"

echo "[3/3] Smoke-Test (generiert generated-maze.sol im aktuellen Verzeichnis)"
mkdir -p /tmp/daedaluzz-out && cd /tmp/daedaluzz-out
daedaluzz --help | head -3
daedaluzz
ls -l generated-maze.sol
