#!/usr/bin/env bash
# paradigm-ctf-infra (paradigmxyz/paradigm-ctf-infrastructure) braucht Docker. Auf dieser Maschine: nicht installiert.
# Wenn Docker verfuegbar ist, ist dies der Weg:
set -eu
echo "Docker erforderlich. Pruefen: docker info"
# Quelle liegt bereit unter: /home/sfs-linux-node/ctf-skills/vendor/paradigmxyz/paradigm-ctf-infrastructure
# Slither/echidna-Docker-Workflow (generisch):
#   docker run --rm -v "$PWD":/src -w /src trailofbits/eth-security-toolbox \
#     -c "solc-select install 0.8.28 && solc-select use 0.8.28 && slither ."
