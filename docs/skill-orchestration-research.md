# Evidence for SFS CTF Skill Index V8 design (2026-11-21)

## First-party and peer-reviewed sources

1. **AgentSkillOS**, Li et al. (2026), https://arxiv.org/abs/2603.02176 ; implementation https://github.com/ynulihao/AgentSkillOS . Findings: capability-tree discovery and DAG composition outperform unstructured flat invocation with the same set in a 30-task multi-format benchmark. This supports *composition*, not a promise of EVM exploit performance.
2. **SkillRouter**, Zheng et al. (2026), https://arxiv.org/abs/2603.22455 ; code https://github.com/eejd/py-skill-router . Full skill body rather than metadata-only was crucial in their 80K-skill/75-query retrieval benchmark (29–44 percentage point declines when removed, dependent on method); proposed two-stage encoder/reranker reported 74% top-1. Our Python lexical scoring is **not** that model and must be benchmarked separately.
3. **Skill Is Not Document / R3**, Wang et al. (2026), https://arxiv.org/abs/2606.03565 . Conditional compatibility and negative skill pairings matter; two top-ranked skills are not necessarily compatible. SFS uses ordered stages and resource checks, not naive simultaneous invocation.
4. **SkillsBench 1.1**, https://www.skillsbench.ai/blogs/skillsbench-1-1 . 87 paired tasks, 18 model-harness configurations; reported mean 33.9 → 50.5% (+16.6pp), with 13 tasks worse with skills, and 2–3 skill bundles outperforming 4+ in average lift (+19.0pp vs +10.1pp). These are associations on this suite, not a universal hard limit.
5. **SWE-Skills-Bench**, https://arxiv.org/abs/2603.15401 . Controlled pinned repo tasks with acceptance tests and without-vs-with-skill paired comparisons. Directly relevant to SFS benchmark methodology.
6. **Anthropic skill-creator**, https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md . Encourages task-specific trigger evaluation, negative examples, run traces, and blind A/B comparison. Description determines discoverability; final task results matter.
7. **Agent Skills specification**, https://agentskills.io/specification ; best practices https://agentskills.io/skill-creation/best-practices . Progressive disclosure: names+descriptions first, SKILL.md and resources only on demand.
8. **MCP client best practices (2026-07-28)**, https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/2026-07-28/develop/clients/client-best-practices.mdx . Hundreds of up-front tool definitions are wasteful; progressive tool discovery and programmatic tool invocation should be separated.
9. **Alibaba skill-up**, https://github.com/alibaba/skill-up . Concrete skill evaluation runner with task conditions, deterministic/script/agent judging and CI outputs. An optional later evaluation integration; not installed by V8.
10. **Freebuff source**, https://github.com/CodebuffAI/freebuff/blob/main/cli/src/utils/codebuff-client.ts and https://github.com/CodebuffAI/freebuff/blob/main/cli/src/utils/trace-writer.ts . The CLI opts into home skills and has optional trace logging. This is evidence of *possible* loading/instrumentation, not evidence that SFS skills were invoked in prior runs.

## Practitioners (anecdotal, not general performance guarantees)

- Scott Spence, empirical Claude Code hook tests, https://www.reddit.com/r/ClaudeCode/comments/1qzjy2h/claude_code_skills_went_from_84_to_100_activation/ : forced skill evaluation performed strongly on selected prompts; more difficult negative prompts exposed false positives from LLM-based ranking. **Claude-specific**; cannot copy a hook and assume it works in Freebuff.
- hussi9/skill-router, https://github.com/hussi9/skill-router : routes skill chains and keeps logs comparing announced vs invoked skills; author reports 18/20 path routing in a small test. Self-reported, not independent EVM validation.
- Community report on detection blind spots across clients, https://www.reddit.com/r/ClaudeAI/comments/1wcml4h/we_measured_whether_our_20_skills_actually_fire/ : some clients read SKILL.md directly rather than call a `Skill` tool; audits must instrument both. Anecdotal.

## Why a limited implementation instead of a new platform

SFS already has a 134-entry manifest, skill cards, pair metadata, local CLI tools and native Freebuff skill loader. The immediate missing capability is **closed-loop integration and attributable evidence**, not another 8 GB copy of vendor sources. A full AgentSkillOS clone, local embedding model or multi-agent runtime on the 8-GB Mac mini would add cost and resource risks before there is proof of routing lift.

V8 therefore ships:
- Local zero-cost Python lexical + capability retrieval over actual manifest/skill cards (no embeddings or network calls).
- Typed ordered DAG steps, each requiring specific real evidence.
- Actual bounded static `surya`/`slither` subprocess orchestration on authorized Solidity files, sequential, with hard timeouts and provenance logs.
- Structural artifact hash assessment and a task-facing SKILL.md that requires real execution of chosen tools.
- Synthetic unit and negative tests to prove CLI behavior. **Not yet** a measured successful Freebuff trigger rate, full 134-asset Mac run, strong semantic retrieval system, automated Foundry exploit creator, or reproducible end-to-end benchmark lift.

### Minimum next empirical question

Does V8 cause Freebuff on the same pinned source-audit tasks to produce more **valid counterexamples** (without leaks or extra false positives), at comparable cost, than the existing V7 native skill? Until matched trials show that, V8 remains a tested prototype rather than a validated performance improvement.
