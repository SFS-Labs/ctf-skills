# CTF Skill Factory integration

The public `SFS-Labs/ctf-skills` repository is the canonical destination for consolidating `SFS-Labs/ctf-skill-factory`.

## Existing components

- CTF Agent Skills: existing `ctf-*/` directories, installation scripts, tests and CI. Retain the upstream MIT license and attribution to Lukasz Jagiello.
- Skill Factory: 134 knowledge cards, `bin/` router and tooling, `MANIFEST.yaml`, `manifest.json`, `repos.tsv`, `INDEX.md`, `recipes/`, `corpora/`, `benchmarks/`, `STATUS.md`, and `VERIFICATION.md`.

## Required integration

1. Import the factory's source files, excluding its root `README.md` and `.gitignore`, into their original relative paths. Preserve executable modes for `bin/*` and shell recipes. Keep both factory GitHub Actions workflows under `.github/workflows/`.
2. Merge the factory `.gitignore` exclusions into the destination `.gitignore`; never commit tokens, vendor trees, venvs, generated outputs, or runtime logs.
3. Consolidate the README into one coherent installation and usage guide. Document the two complementary skill groups without implying that 134 knowledge cards are all executable tools.
4. Preserve original project attribution and licenses. Do not rewrite the upstream `ctf-*/` skills as SFS-authored work.
5. Check links, tool invocation paths, workflow security and secret exposure; update references to `SFS-Labs/ctf-skill-factory` where they are now obsolete.
6. Validate existing CTF tests and factory gateway unit tests, router commands, manifest consistency, smoke-test behavior and relevant workflows. Record which checks actually ran.
7. Merge through reviewed PR after successful checks. Archive the source repository only after verifying the integrated public repository and ensuring old links remain discoverable.

## Verified integration status

- **Imported:** all 170 factory source files other than the factory's original root `README.md` and `.gitignore`, which were consolidated with the canonical repository equivalents.
- **Exact source comparison:** 170/170 files present; zero executable-mode differences. Of these, 163 have byte-identical Git blob hashes and seven intentional, reviewable changes (portable paths for factory utilities, explicit public-push protection, and one workflow description).
- **Existing CTF source:** original `ctf-*/` trees, `solve-challenge/`, upstream MIT copyright and test suite preserved.
- **CI verified:** [PR workflow 44978080763](https://github.com/SFS-Labs/ctf-skills/actions/runs/44978080763) and [push workflow 44978077340](https://github.com/SFS-Labs/ctf-skills/actions/runs/44978077340) both succeeded. Combined pytest result: **77 passed, 1616 subtests passed**. The manifest/card/count check, executable permissions, shell syntax, offline router commands, and synthetic token-redaction selftest passed.
- **Not executed:** large external vendor downloads, local cryptographic tool installations, native exploit scoring, and live exploit smoke tests; these depend on optional local tooling and external test inputs. Historical `STATUS.md` and `VERIFICATION.md` are inherited, not current CI results.
- **Change record:** [PR #2](https://github.com/SFS-Labs/ctf-skills/pull/2). The original factory repository has been archived (GitHub repository metadata `archived=true`).

GitHub connector edits and Actions results are **not** proof of GitHub Copilot product usage. Copilot proficiency evidence: **not verified**.

## V8/V9 continuation after original merge

The initial PR #2 migrated the pre-V7 catalog snapshot. The later [historical V9 PR #6](https://github.com/SFS-Labs/ctf-skill-factory/pull/6) in the archived source contains subsequent work not present in that snapshot. The continuation port uses source commit `d0bae5b6565a97711c60e2776afb5b1da397806f`, preserves the canonical CTF Agent Skills/attribution/license/workflows, and integrates the V8 Freebuff skill, V8 orchestrator, Copilot delegate, the V7 catalog alias verification and tests.

The later catalog has **133 independently represented skills from 134 source records**: `NethermindEth/EVMYulLean` is a verified alias of `paradigmxyz/evmyullean`, not a second distinct skill. CI checks this invariant. The earlier 134-card snapshot is preserved in Git history. The additional alias card is retired only because its information is already represented within the canonical card and alias proof in `repos.tsv`.

The historical Freebuff acceptance is an *external local-node report*, not proof that this CI runner invoked a Freebuff desktop skill. Copilot delegate's mock tests are not actual Copilot execution, and no paid delegation is enabled. The migrated `bin/push` retains an explicit `--allow-public` write gate.
