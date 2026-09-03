# 1788433011-every-spawn-prompt-is-retyped-from-memory — questions for the planner

<!-- seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

Four rows, all four answerable in one batch before the first implementation
spawn. Every one has a default the phases are written to build, so a silence
does not stop the work — it only picks the option marked *default*.

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Where does the contract live, and how does an agent reach it? | **A — `docs/agent-contract.md`, named as a path in each definition.** What #107 asks for verbatim. Costs: `$CLAUDE_PLUGIN_ROOT` was measured **unset** inside this smith subagent, so a plugin-cache path may not resolve, and a bare `docs/agent-contract.md` resolves against the *user's* repository, where the file does not exist. And `tests/test_the_release_check_watches_what_ships.py:52` classifies `docs` as `STAYS_HOME` — *"None of it reaches a user through the plugin"* — which stops being true the moment an agent reads it at runtime, so a contract edit would need a version bump the workflow does not ask for. **B — `skills/agent-contract/SKILL.md`, listed in each agent's `skills:` frontmatter.** The harness preloads it; no path to resolve, no `Read` call, and `skills` is already in `SHIPS`. This is how `implement` and `writing-style` reached this session. Costs: it appears in the user-facing skill listing as though it were an invocable procedure, and it is not one. **C — the file in `docs/` and a thin skill that only points at it.** Two copies of the answer, which is what #107 forbids. | **B** — the only option measured to work. #107's reasoning for a path (*"an agent has no `Skill` tool and cannot load a skill itself"*) is about loading mid-run; frontmatter preloading is a different mechanism and is already in use by all three agents. `docs/agent-contract.md` is then not created, and `docs/review-handoff-protocol.md` §385 points at the skill. | ✅ **B′** — `skills/agent-contract/SKILL.md` with `user-invocable: false` in its frontmatter, listed in each agent's `skills:`. Measured 2026-09-03 by the orchestrator: a sentinel line and the flag were planted in the installed copy — `~/.claude/plugins/cache/specseal/specseal/0.5.0/skills/writing-style/SKILL.md`, which is what loads, not the marketplace clone — and after `/reload-plugins` a spawned smith reported PRESENT with `writing-style` still listed. So the flag does not block preload, the copy in force is the version cache, and preloaded bodies refresh on `/reload-plugins` rather than at spawn. Three earlier ABSENTs came from editing the marketplace clone, which nothing loads. The description must say the skill is injected into agents and is not a command to run. |
| Q2 | How deep does the re-homing go? | **A — full.** The contract is the single home for every universal rule in `spec.md`'s first table; each definition keeps only its own application; the existing cases that assert a moved sentence inside `agents/*.md` are re-pointed at the contract, never deleted, and each must still be able to fail. Costs: eight test modules assert moved sentences — `test_broad_gate_rule`, `test_edits_go_through_the_edit_tool`, `test_a_probe_that_commits_says_so`, `test_a_probe_does_not_outlive_its_round`, `test_the_handoff_before_round_one`, `test_the_last_rounds_fixes_are_checked`, `test_one_word_one_meaning`, `test_the_pull_request_language_is_the_repositorys`. **B — additive only.** The contract carries only the rules that today live nowhere but a prompt (exit codes, the report-labelling duty, do-not-post/push/spawn, the probe naming); `agents/*.md` keeps everything it already has. Costs: the broad-gate, `Edit`-tool, batching and record-language rules stay duplicated across two files, and #84's framer and #30's sealer still inherit nothing — which is the failure #107 opens with. | **A**. B leaves the tree in the state the issue describes and calls the fix tidiness. The eight modules are a real price and it is paid once. | ✅ **A** — full. The eight modules are re-pointed, never deleted, and each must still fail without the sentence it asserts. |
| Q3 | Do the four method lessons go into the contract, or stay in `docs/review-handoff-protocol.md`? | **A — into the contract**, with the protocol keeping a one-line pointer. #107's comment says they belong *"wherever the agents' method is written rather than in each prompt"*, and each of the four is true of any agent that fixes or reviews. **B — stay in the protocol**, which is a document about handoffs and is where they sit today. Costs: they then reach an agent only if a prompt names the protocol, which is the retyping this work item exists to end. | **A** | ✅ **A** — into the contract; the protocol keeps a one-line pointer. |
| Q4 | Does the contract bind the orchestrator, and does this work item say so? | #107's headline failure is the **orchestrator** breaking a rule it had written into every prompt it sent. The orchestrator reads `skills/implement/SKILL.md` and `skills/code-review/SKILL.md`, never `agents/*.md`, so a contract reached only through agent definitions cannot bind the party that broke it. **A — one line in each of those two skills** naming the contract and saying the orchestrator is bound by the same exit-code and labelling rules. Two lines of diff, and it closes the loop the issue names. **B — leave it.** #107 item 1 says *"every agent definition"* and nothing else, and #119 may be where the orchestrator's duties land. | **A**, worded as a pointer rather than a second copy of the rules | ✅ **A** — one line in each of the two orchestrator skills. It is what binds: `user-invocable: false` lets the orchestrator load the contract, it does not oblige it to. |

Answered 2026-09-03 by the repository owner in one batch before the first implementation spawn; Q1 after the probe above.

Answered rows feed back into `docs/` (policy clause or open-questions
section) before this directory's work merges.

## Assumed in writing, because a different answer would not change what is built

- **The contract is English regardless of `Record language`.** `seal/config.md`
  has no such row, so English is the value anyway; and the contract is an
  agent instruction rather than a work record, which is the class
  `templates/config.md` already keeps in English.
- **The contract goes into `tests/test_docs_line_wrap.py`'s `COVERED` at
  birth**, written wrapped from its first line. That test's own comments state
  the precedent for a file joining at birth rather than after a sweep, and it
  holds under either answer to Q1.
- **Nothing here adds a prompt.** No hook changes, no gate changes, so the
  prompt budget `CONTRIBUTING.md` asks for is zero. Stated in the pull request
  body, because nothing counts interruptions.
