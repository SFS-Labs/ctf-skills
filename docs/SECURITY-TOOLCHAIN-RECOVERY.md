# SFS | Cybersecurity — Freebuff EVM toolchain recovery (2026-11-22)

Scope: only the **local, authorized** EVM challenge environment. This is a provisioning and verification plan, not an exploit, not a Freebuff runtime trace, and not official benchmark grading. Never include reference answers, grader files, task secrets, API keys, local private case evidence or benchmark ground truth in this **public** repository.

## Baseline and non-destructive first check

The screenshot is a snapshot from another machine. No item is considered repaired until a fresh probe on the Mac mini establishes it. Run within the **local Code/Codex session**, not in a remote GitHub Actions runner:

```bash
cd ~/ctf-skills
python3 bin/security-toolchain-preflight.py \
  --project ~/sfs-cyber-blind-eval \
  --skills-root ~/ctf-skills \
  --out ~/sfs-cyber-blind-eval/toolchain-preflight.json
bash scripts/security-toolchain-repair.sh check
```

Keep `toolchain-preflight.json` **local**, outside Git: it includes local paths and machine information. Avoid storing benchmark answers in the same output folder.

## Controlled repairs (one at a time; preserve all existing artifacts)

1. **Git**: `bash scripts/security-toolchain-repair.sh git` when the preflight reports `BUNDLED_OUTSIDE_PATH`. Creates only `~/.local/bin/git` → bundled Freebuff Git; refuses to replace an existing file. This **does not guarantee** GUI Freebuff inherits `~/.local/bin` in PATH. Verify `command -v git && git --version` **inside a newly started Freebuff process**. If unavailable, Codex should inspect systemd-user/PATH propagation, use the already installed OS package `git` or a local launcher, and re-test. Never overwrite application bundles.
2. **Docker**: after package/OS/available-memory check and review of existing `docker`, `containerd`, and `podman` services, run `bash scripts/security-toolchain-repair.sh docker` **only on the Mac**. Official Ubuntu Noble amd64 packages, conflict gate, no silent removal, no membership in root-equivalent `docker` group. Observe actual `sudo docker info`, `sudo docker compose version` and a constrained `--network none` smoke test. Docker **Engine availability does not make** `attacknet`, `eth-security-toolbox`, `cloudexec` or `paradigm-ctf-infra` executable: each needs its own reviewed, version-pinned image/source and independent smoke test. No automatic startup of heavyweight analysis containers. [Docker Engine installation](https://docs.docker.com/engine/install/ubuntu/) · [Docker privileges](https://docs.docker.com/engine/install/linux-postinstall/).
3. **Manticore**: project `trailofbits/manticore` is archived/maintenance-mode; first capture exact `manticore --version` error and Python dependency versions. Do not repair by modifying the system Python or trying unlimited pip upgrades. Prefer a compatible isolated venv or reviewed, digest-pinned upstream container, then test a small local EVM fixture with deterministic timeout/memory limits and verify a **real** output. If this cannot be made reproducible, mark `UNAVAILABLE` and use the existing `mythril`/Foundry/Slither routes; do not mislabel them as Manticore. [Upstream](https://github.com/trailofbits/manticore).
4. **OpenZeppelin Foundry Upgrades**: this is **a project dependency**, not a global executable. Diagnose the exact failing `require` in the affected Foundry project; check `foundry.toml`, relevant submodules/node_modules, remappings, Node/NPM, `ffi`, `ast`, `build_info`, `extra_output=["storageLayout"]`, then install the official supported Foundry library with `forge install OpenZeppelin/openzeppelin-foundry-upgrades` or NPM alternative as appropriate. In a disposable copy of an authorized fixture, compile and run a test that invokes an upgrade safety validation, including an invalid storage layout negative control. Avoid changing challenge source or frozen evidence. [Official Foundry Upgrades docs](https://docs.openzeppelin.com/upgrades-plugins/foundry/foundry-upgrades).
5. **IDA/ethersplay**: `ida-evm` requires an actual compatible IDA installation and its license; no free installation claim. Inspect license eligibility, version/API compatibility and test bytecode loading. If absent, use an **explicitly named non-IDA alternative** (e.g. existing `pyevmasm`, `evm-cfg-builder`, Foundry disassembly routes) with real fixture output. Distinguish `KNOWLEDGE_ONLY` from executed. [ida-evm](https://github.com/crytic/ida-evm).
6. **Freebuff V8 activation & evidence**: a skill file, `cloud_read_skill`, `route`, or the receipt from a manually issued script **does not prove** that Freebuff invoked its `skill` tool. Launch a **new Freebuff project session** whose actual root includes `.agents/skills/ctf-skill-index-v8/SKILL.md`, with matching YAML `name`; confirm `AGENTS.md` is the intended checkout. Observe a genuine tool call `skill(name="ctf-skill-index-v8")`, body, project root, and subsequent genuine `run --allow-exec` and `verify` receipts in that session. Run an unrelated prompt as a negative activation control. If Freebuff exposes no tool-call logs/hooks, mark `RUNTIME_UNVERIFIED` — a wrapper cannot manufacture a native Codebuff trace. The official CLI or SDK, **if supported and explicitly verified on the installed build**, can provide a separate executor pathway, not retroactive proof for the desktop agent. [Freebuff project](https://github.com/CodebuffAI/freebuff).

## Run-A/B evidence boundary

- Recheck `validateUserOp`, `execute`, `executeBatch` and authorization for historical EIP-7702 delegations in RUN-A. `Needs fixes` is not resolved by toolchain installation.
- Verify whether the 393-file bundle expectation is correct and why only 48 files were extracted; determine whether `case-b/task.json` is required for the actual task. Preserve original archive hashes and report precisely what was read. No post-freeze rewriting of original evidence; append new recheck material and a new manifest rather than silently replacing the originals.
- To claim blind isolation, check the actual accessible filesystem, model context, tool logs, file search scope, network routes and whether grader/reference materials were mounted or read. Absence of an apparent leak is not proof of technical isolation. Ideally the **evaluator keeps ground truth outside the Freebuff-accessible environment** until immutable freeze.
- Keep official benchmark status `NOT_VERIFIED` unless a genuine authorized evaluator run produces a trace and results. RUN-A/RUN-B local tests and benchmark correctness are distinct.

## Acceptance matrix

| Capability | Evidence for PASS | Otherwise |
| --- | --- | --- |
| Git | `git` resolves and executes inside a **fresh Freebuff tool shell** | PATH_FIX_PREPARED / BLOCKED |
| Docker | daemon + Compose + constrained container smoke on actual host | INSTALLED_ONLY / BLOCKED |
| Docker recipes | relevant pinned environment genuinely starts and completes a fixture | KNOWLEDGE_ONLY / BLOCKED |
| Manticore | real symbolic EVM fixture run and verified output | UNAVAILABLE / BLOCKED |
| OpenZeppelin | official upgrade validation and negative test in isolated Foundry fixture | INSTALLED_ONLY / BLOCKED |
| IDA | license, EVM loader and real bytecode run | NOT_AVAILABLE / ALTERNATIVE_ONLY |
| V8 runtime | native skill invocation + body + orchestrator receipt + negative control | RUNTIME_UNVERIFIED |
| Blindtest | objective isolation audit with evaluator inaccessible before freeze | ISOLATION_UNVERIFIED |
| Benchmark | official evaluator execution | OFFICIAL_EVALUATION_NOT_VERIFIED |

Operational constraints: Linux Mint 22.3 on a Mac mini with limited RAM. No parallel heavyweight analysis/IDE/browser processes, at most two browser and terminal windows, monitor `MemAvailable`, swap and CPU before starting containers. Do not replace local artifacts, open public ports, launch live exploits or incur new costs. Operate `OBSERVE → DIAGNOSE → CHANGE → TEST → RECORD`. Final statuses reflect actual results, not an installation plan.
