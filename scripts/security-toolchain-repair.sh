#!/usr/bin/env bash
# Narrow, idempotent local repair. No changes by default; no challenge execution.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
usage() { printf 'Usage: %s check | git | docker\n  check = read-only\n  git = user-local symlink if missing\n  docker = install official Docker Engine for Ubuntu 24.04 after local preflight\n' "$0"; }
case "${1:-check}" in
check)
  python3 "$ROOT/bin/security-toolchain-preflight.py" "${@:2}"
  ;;
git)
  if command -v git >/dev/null 2>&1; then git --version; exit 0; fi
  source_git="/opt/Freebuff/resources/git/bin/git"
  if [[ ! -x "$source_git" ]]; then echo "BLOCKED: bundled git not executable; inspect OS package manager" >&2; exit 2; fi
  install -d -m 700 "$HOME/.local/bin"
  if [[ -e "$HOME/.local/bin/git" || -L "$HOME/.local/bin/git" ]]; then
    echo 'BLOCKED: ~/.local/bin/git already exists; no overwrite' >&2; exit 2
  fi
  ln -s "$source_git" "$HOME/.local/bin/git"
  "$HOME/.local/bin/git" --version
  echo 'SYMLINK_READY: verify ~/.local/bin is in PATH of a NEW Freebuff tool process.'
  ;;
docker)
  if ! command -v apt-get >/dev/null || ! command -v sudo >/dev/null; then
    echo 'BLOCKED: apt and sudo required' >&2; exit 2
  fi
  . /etc/os-release
  if [[ "${UBUNTU_CODENAME:-}" != "noble" ]]; then
    echo 'BLOCKED: expected Ubuntu 24.04/Noble-based Mint; inspect distribution' >&2; exit 2
  fi
  if [[ "$(dpkg --print-architecture)" != "amd64" ]]; then
    echo 'BLOCKED: expected amd64; inspect architecture' >&2; exit 2
  fi
  for pkg in docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc; do
    if dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q 'install ok installed'; then
      echo "BLOCKED: potential conflicting package $pkg; reconcile manually; no removal" >&2; exit 2
    fi
  done
  if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    echo 'Docker already operational; no changes'; exit 0
  fi
  # Docker official Ubuntu repository. No unattended conflict removal or group privilege grant.
  sudo -v
  sudo apt-get update
  sudo apt-get install -y ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  printf 'Types: deb\nURIs: https://download.docker.com/linux/ubuntu\nSuites: noble\nComponents: stable\nArchitectures: amd64\nSigned-By: /etc/apt/keyrings/docker.asc\n' \
    | sudo tee /etc/apt/sources.list.d/docker.sources >/dev/null
  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo systemctl is-active docker
  sudo docker info --format '{{.ServerVersion}}'
  sudo docker compose version
  echo 'DOCKER_ENGINE_READY: container isolation/smoke tests remain separate; docker group not granted.'
  ;;
*) usage; exit 2 ;;
esac
