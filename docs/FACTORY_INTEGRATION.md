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

## Current status

This file is an integration specification, **not evidence that the repositories have already been merged**. The source repository remains public and active until acceptance.
