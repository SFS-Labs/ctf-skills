# SFS | Security Benchmark Gateway

One GitHub Actions workflow, **both sources immediately selectable**:
- CyberChainBench: `defai-labs/CyberChainBench`
- ReEVMBench: `blocksecteam/ReEVMBench`

Open [Actions / Security benchmark gateway](https://github.com/SFS-Labs/ctf-skill-factory/actions/workflows/security-benchmark-gateway.yml) on the default branch. Choose **Run workflow**.

## Operations

| Operation | Inputs | Result |
| --- | --- | --- |
| `catalog` | choose either `source`; ignore `case_id` | `catalog.json`: pinned upstream case IDs for evaluator selection |
| `smoke` | any `source`; `case_id` empty | **Both adapters** are exercised against public upstream samples. Produces `smoke.json`. |
| `prepare` | `source`, `case_id`, `phase=detect` | `brief.json`: answer-masked Freebuff V7 audit assignment |
| `prepare` | `phase=reproduce` after freeze | historical context for reproduction (when in source); not the exploit |
| `grade` | `source`, `case_id`, `submission_json` | `grade.json`: reference metadata comparison after the report was frozen |

All output files are attached to the **individual Actions run as artifacts** (7-day retention). There are no automatic model calls, no unapproved RPCs and no scheduled runs. The workflow also runs the local unit-test suite before the requested operation.

### Input examples

- `source=cyberchainbench`, `operation=prepare`, `case_id=bench-01`, `phase=detect`.
- `source=reevmbench`, `operation=prepare`, `case_id=2023-07-pooltogether`, `phase=detect`.
- `operation=smoke`: exercises CyberChainBench `bench-01` and ReEVMBench `2024-06-thorchain` (including a missing-`base_commit` case).
- `operation=grade` with `submission_json` set to the **frozen** Freebuff report:
  `{"findings":[{"type":"hypothesis-from-code","function":"function-under-investigation","evidence_path":"test/PoC.t.sol"}],"notes":"Local evidence frozen before grading."}`
  This format is illustrative, not a recommended finding. Do not feed benchmark answers into the auditor.

For grading, `submission_json` avoids a second Git commit. Alternatively, `submission` may name an existing JSON file under `benchmarks/submissions/`. Output includes a SHA-256 of the frozen JSON.

## Independence boundary

1. **Evaluator (GitHub Actions)** chooses the case via `catalog` and generates `prepare`. Its selection and ground truth remain outside the Freebuff conversation.
2. **Freebuff (local)** receives *only* the downloaded `brief.json`. Its native `ctf-skill-index` V7, existing 133 skill cards and locally installed analysis tools remain enabled. The agent independently examines the code/chain, records findings and executable evidence, then freezes the report.
3. **Evaluator (GitHub Actions)** receives the report using `grade`. Only *after* freeze, it compares labels or presents reference findings for review.

**CyberChainBench**: detect metadata gives chain and vulnerable contract address only. The source's known `type`, `function`, `fix_description`, incident name, attack transactions and profit are deliberately omitted. Post-freeze grading checks exact normalized `type + function` labels, which is **not** proof of exploitability.

**ReEVMBench**: extracts the code repository and historical `base_commit` from the benchmark's audit recipe, not its finding titles. Some official audit configurations have **no** `base_commit`; in that case the gateway records the public upstream HEAD SHA at preparation and labels its provenance `upstream_head_at_preparation`. This is reproducible as a source snapshot but **not proven to be the original audit-time commit**. Post-freeze grading outputs the withheld finding titles for independent comparison; it does not turn ID matches into an official vulnerability score. Some non-Git-based ClaraHacks incidents are not supported by the current ReEVMBench adapter; the catalog lists the repository-based detect split.

## Boundaries and costs

- This is a **two-source GitHub handoff and reference evaluator**, not the official CyberChainBench Harbor evaluator or ReEVMBench EVMbench runner. It does **not** run a Freebuff agent, exploit, live trade or smart-contract deployment in Actions.
- Real historic fork experiments require archive RPCs, verified source retrieval and a separate test runner. Those dependencies have not been provisioned automatically.
- Public cases and known attacks can be discovered on the internet by an unconstrained model. The gateway masks accidental exposure only; **it is not an isolation sandbox**.
- Each manual workflow consumes applicable GitHub Actions compute/storage quota. No free-tier balance is assumed.
- Benchmarks' data/licenses belong to their respective upstream sources. CyberChainBench's case data includes AGPL-3.0-derived material; no raw datasets are redistributed in this repository.
- No changes to Linux services, GitHub secrets, Freebuff account skills, Tailscale, SSH or the existing local working tree.

Source revisions are pinned in [sources.json](sources.json). Update these deliberately; they must not float with upstream `main`.

## Local unit tests

```bash
python3 -m unittest discover -s benchmarks/tests -v
```

The `smoke` Actions operation is the **first real network integration check**. Until it has produced a successful Actions run and artifacts, do not report end-to-end PASS.
