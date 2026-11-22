# SFS-Labs | GitHub Copilot Proficiency Operating Standard

**Status:** proposed operating procedure, 2026-11-13. **Scope:** every SFS-Labs task that actually uses GitHub, regardless of whether the owner explicitly names GitHub. The goal is fast, useful engineering **and** maximally efficient development of genuine GitHub Copilot Proficiency up to the currently published Expert capability profile. This is NOT an autonomous workflow, a GitHub policy bypass, or a scoring algorithm.

Authoritative references:
- [GitHub Copilot Verified Proficiency and FAQ](https://learn.github.com/proficiencies/copilot/)
- [Official Copilot learning pathway, Beginner to Expert](https://learn.github.com/learning-pathways/github-copilot)
- [GitHub Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)

## 1. Automatic trigger and task routing

**Trigger:** If a ChatGPT task concerns an SFS-Labs repository, PR, GitHub Issue, Actions, code, documentation, review, or architecture that will be handled through GitHub, apply this procedure **without a keyword, @-mention, $-mention, or further request.** This includes tasks implicitly routed to GitHub. It is not triggered by unrelated conversations.

1. Inspect the target repository, README, existing instructions, current tasks, protected paths, PRs and relevant tests. Do not assume all SFS-Labs repositories are original projects; some may be forks or externally maintained.
2. Define the smallest deliverable: problem, outcome, in/out of scope, validation and owner-required decisions. Preserve existing trust boundaries.
3. **Choose the Copilot surface most relevant to genuine value and uncovered skill areas.** For substantive, bounded code/docs changes, prefer a Copilot Cloud Agent issue assignment when permitted. For PRs, use Copilot review / summarization when supported, alongside independent checks. For exploratory decisions, use GitHub.com Copilot Chat when available. For editing, use IDE chat/inline/next-edit or Copilot CLI when the owner is actually using such an environment.
4. Where the connected GitHub API only supports ordinary issues, comments, file changes or reviews, use it honestly. **Non-Copilot GitHub connector work is not itself evidence of Copilot Proficiency.** A Copilot assignment is an attempt until GitHub accepts it; a PR/agent event is not a verified score increment.
5. Do the useful task first. Reuse a fitting Copilot capability instead of creating fake issues, dummy prompts, meaningless commits or new projects. If Copilot is unavailable, unsuitable, paid outside an approved budget, or blocked by policy, use the appropriate alternative and record the gap.
6. Review exact changed files, CI and test evidence before recommending merge. Never auto-merge; sensitive infrastructure and protected-path maintenance follow their separately documented owner procedure.

No automatic persistence of ChatGPT's own instructions is created by storing this file in GitHub. For ordinary chats, use **account-level Custom Instructions**; for ChatGPT Projects, also add **Project instructions**, because project instructions take precedence over global instructions (see section 7). Repository-specific Copilot files affect their own repositories, not every SFS-Labs repository. A link to this document does not guarantee it will be fetched: the assistant should retrieve it through the connected GitHub app when relevant and possible.

## 2. Known evaluation logic and what remains unknown

GitHub says its observable proficiency model considers **Breadth** (range of tasks/skills), **Depth** (sophisticated valuable work), and **Consistency** (retained capability, not one-offs) across five skills. It uses Copilot product activity, not raw GitHub activity, and scoring details are not public. The assessment currently reaches **Proficient**. **Advanced** and **Expert** are published learning/capability profiles but their scoring methodology is in development; do not promise a timeline, threshold, or earned Expert badge.

| Critical skill | Real, task-aligned Copilot evidence | Minimum-friction opportunity |
| --- | --- | --- |
| AI Collaboration | Copilot cloud coding agent, GitHub.com chat, PR summary and code review; IDE chat where actually used | Delegate a bounded meaningful issue, inspect Copilot PR, use review |
| Prompting | Clear context, success criteria, iterative troubleshooting or alternative approaches **inside Copilot** | Supply a precise brief and follow up on actual errors |
| Code Generation & Validation | Copilot-supported code changes, tests, failure analysis, refactor and independent test/review | Pair implementation with a real regression/negative test |
| Agent Configuration | Repo instructions, custom agents, prompts, agent skills and configuration actually used in Copilot | Maintain concise, repo-specific instructions; reuse only where warranted |
| Tool & Context Integration | Copilot with relevant MCP, external context, CLI/SDK or project integrations actually invoked | Reuse an existing safe MCP integration when it solves the task |

**Proficient (known current target):** purposeful sustained use across multiple repositories and extended periods; use of appropriate GitHub.com and IDE surfaces, model selection and genuine customizations; exploration of CLI, agentic features, mobile, Copilot API/SDK or MCP where relevant. A one-time cloud agent assignment alone does **not** fulfill this profile. Do not claim IDE use when no IDE was used.

**Advanced (published capability profile, not scorable yet):** deliberately design, orchestrate, evaluate and improve Copilot-based workflows, choosing context, model, tools and configurations based on trade-offs and limits. Opportunistic examples: compare two legitimate approaches, measure task outcome, explain why the chosen approach was superior.

**Expert (published capability profile, not scorable yet):** build reusable, reliable AI-assisted capabilities; coordinate agents, tools and workflows; apply explicit evaluation, memory/state discipline, guardrails and operations; decide when deterministic code is better. Opportunistic examples: a reusable, tested agent skill for an already repetitive process; orchestrated review plus deterministic validation; recorded recovery from failure. **Do not add multi-agent architecture to simple tasks** merely to imitate Expert.

## 3. Assignment template — generated automatically by the assistant

For a nontrivial Copilot-appropriate task use an issue containing:
- **Outcome:** user-visible/engineering change and why.
- **Repository context:** relevant paths, existing architecture and approved branch.
- **Boundaries:** files/behaviors to avoid, data classification, cost restrictions, no unapproved integration, no merge.
- **Acceptance:** executable checks and observable pass/fail cases; include a negative/failure case when material.
- **Copilot skill opportunity:** only relevant features from section 2; make an explicit reasoning choice when selecting agent/tool/model/context.
- **Evidence:** exact PR/diff, actual tests, limitations, open risks. Never invent tool usage.

Prefer direct small tasks where a full Copilot delegation would create unnecessary overhead. Keep the task-to-surface mapping adaptable as GitHub changes product availability.

## 4. Coverage without gaming: ongoing decision rule

At each substantive GitHub task, ask internally:
1. What is the best engineering path?
2. Which of the five skill areas are naturally exercised by this work **inside Copilot**?
3. Which official Proficient practices remain unobserved (notably IDE, model choice, CLI, integrations) and can be added at negligible marginal cost *without distorting the task*?
4. Is there a real Advanced/Expert step (evaluation, reusable customization, agent orchestration, state or guardrail design) that makes the result more robust or reusable?
5. Would doing it cost more time, money or risk than it saves? If yes, omit it.

Use **breadth × depth × consistency** as a qualitative review framework, **not** a numeric score prediction. Real benefit, testability and trustworthy attribution always take precedence.

## 5. Minimal evidence and follow-up

Where relevant, append a compact evidence note to the **existing** issue/PR (do not create a separate bureaucracy):
```text
Copilot evidence: [actual GitHub Copilot surface used, or "not verified"]
Skill areas: [only directly evidenced areas]
Advanced/Expert practice: [concrete reusable/evaluated action, or none]
Proof: [issue/PR/agent event/test URLs]; Tests: [passed/failed/not run + context]
Uncovered: [one material missing surface, e.g. IDE/CLI]
Decision: [keep/adjust/skip; brief reason]
```
Use GitHub's actual proficiency dashboard as the **only authoritative level**. When it changes, update prioritization. Intermediate is the user's 2026-11-13 supplied snapshot; it is not an independently confirmed API result.

## 6. Security, availability, cost and truthfulness

- The GitHub-connected ChatGPT tools cannot themselves launch an IDE session or guarantee Copilot Chat, CLI or MCP usage; do not claim otherwise. Copilot cloud agent assignment is supported only where GitHub accepts the assignee and policies permit it.
- Obey repository-specific `AGENTS.md`, branch protection, PR validation, human review, private-data restrictions and spending caps. Never weaken controls to make Copilot tasks succeed.
- Never disclose secrets or private client/employer material to new services. Avoid unnecessary always-on infrastructure, paid seats or requests.
- Keep customer results, synthetic data, old test results and real executions distinguishable. No fabricated performance, usage, credentials or badge.
- Owner remains responsible for approving sensitive changes and final merge.

## 7. ChatGPT configuration: global + project (November 2026)

**Account level (ordinary chats):** ChatGPT iOS Settings → **Customize ChatGPT** (or **Personalization → Custom Instructions**, depending on interface) → enable customization → append this short rule in the **Custom Instructions** field, preserving existing instructions:

> Whenever a task actually uses GitHub or an SFS-Labs repository, even if GitHub is not named, automatically apply the Copilot Proficiency Operating Standard at https://github.com/SFS-Labs/sfs-ai-development-gateway/blob/main/docs/COPILOT_PROFICIENCY_OPERATING_STANDARD.md using the connected GitHub app where available. Optimize meaningful Copilot usage for the fastest credible progress toward Proficient and the published Advanced/Expert capabilities (breadth, depth, consistency across five skill areas). Do useful work first, verify true Copilot activity, honor repository safeguards and budgets, and avoid artificial actions or claims. No special keyword, @-mention or $-mention needed.

**ChatGPT Projects:** Open each ChatGPT project in which GitHub work occurs → **••• → Project settings → Project instructions**. Add the detailed rule below **to relevant projects**; Project instructions override account-level Custom Instructions, so the global rule alone is not a universal guarantee inside projects:

> Whenever a task actually uses GitHub or SFS-Labs repositories, even implicitly and without the word GitHub, automatically retrieve and apply the SFS-Labs Copilot Proficiency Operating Standard at https://github.com/SFS-Labs/sfs-ai-development-gateway/blob/main/docs/COPILOT_PROFICIENCY_OPERATING_STANDARD.md via the connected GitHub app where possible. Optimize legitimate Copilot usage for **the fastest credible progress toward current Proficient and the published Advanced/Expert competencies**, by choosing the right Copilot surface, maximizing useful breadth, depth and consistency, and validating the real work. Prefer available direct Copilot issue delegation, repo instructions, code review, agent skills and MCP/CLI/IDE where genuinely available and valuable. Do not add artificial activity, make unverifiable score claims or weaken repo safeguards. Apply without a special trigger, plugin mention or repeated confirmation; report actual tool actions separately from unexecuted opportunities. No automatic merge or unapproved spending.

**Scope and limitations:** ChatGPT Global Custom Instructions apply to ordinary chats and have a character limit. Project instructions only apply in their own projects. Neither setting is a scheduler, a guarantee of tool access, or an autonomous background trigger. Project Memory is supplementary context, not a substitute for instructions. GitHub repo instructions guide GitHub Copilot only in their relevant repository and do not install ChatGPT instructions.

**Verified product documentation:**
- [ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt)
- [ChatGPT Projects (Project settings and instruction precedence)](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
