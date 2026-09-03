# 1788433011-every-spawn-prompt-is-retyped-from-memory — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` (the goal a design is chosen against; fragments, never
             the shared file), `CONTRIBUTING.md` §What a change to a gate must
             carry, `docs/review-handoff-protocol.md` §§385–467, issue #107 and
             its two comments, this work item's `routing.md`
· evidence: none yet — the ledger fragment is written in phase 6
· verified: read — every coordinate named in `plan.md`'s Technical context.
             executed — `$CLAUDE_PLUGIN_ROOT` is unset in this subagent;
             `tests/test_the_handoff_before_round_one.py` passes at 623487f
             (9 passed)

## Why this work exists

Half of every spawn prompt was identical to the last one and was retyped from
memory, so a rule that failed to be recalled went missing with nothing
recording that it had; this work moves the universal half into one file every
agent reads and each agent's own half into its own definition, leaving the
prompt holding only what is specific to the round.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The contract's home | #107 item 1 says `docs/agent-contract.md`, beside `docs/review-handoff-protocol.md` | raised as Q1 rather than built | `tests/test_the_release_check_watches_what_ships.py:52` classifies `docs` as `STAYS_HOME` — *"None of it reaches a user through the plugin"* — which an agent reading it at runtime contradicts; and `$CLAUDE_PLUGIN_ROOT` was measured unset inside this subagent, so the path an agent would resolve is not one this work can promise. A ticket is a request, not an authority (`implement` §1) |
| Which layer *no writes into `rounds/`* belongs to | #107's own table puts it in the right-hand column as universal; its comment's Layer 2 puts it under the warden | split: the general form (*you return a report; you write no durable record*) is universal, the warden's instances stay in `agents/warden.md` | the issue contradicts itself, so the split had to be decided rather than copied. The general form is what a fourth agent inherits; `rounds/` and the review mark exist only for one agent |
| What phase 1 touches | `plan.md`'s phase-1 row names the contract, its test and the wrap list | both READMEs' skills row edited too (22 → 23, on-demand 11 → 12, `agent-contract` listed) | `tests/test_chain_hooks_hardening.py` derives the README's skill count from the `skills/*/SKILL.md` glob, so a new skill is red in both editions until the row moves. Phase 2 moves the name again, into the agents column, and the preloaded group becomes five — a spelling that test does not yet carry |
| The opening line's first clause | `spec.md` decided *Read the agent contract before your first tool call* | rewritten to *The agent contract binds you, and you already have it* — `agent-contract` is in the `skills:` list above, so it arrived at startup | Q1 answered B′, where nothing is read and no path is resolved. An imperative to go and read it describes a delivery this work item measured and did not build, and it contradicts the contract's own first paragraph — *You received this file at startup*. `spec.md` carries the new text, so the decided sentence and the three definitions are one string, which is what `test_every_agent_reads_the_contract.py`'s identity case holds them to |
| What a pin is | `plan.md` phase 1: *one phrase per section that cannot survive the drift it guards* | the pin is a sentence from the section's BODY, matched inside that section only; the heading is excluded by construction | the first draft pinned eight headings, and the move check was red for the wrong reason: a heading that outlives its rule satisfied the pin. `tests/test_the_agent_contract_holds_the_universal_rules.py`'s docstring records it |
| Where the `seal/…` root rule lives | `spec.md`'s universal table has no row for it, and phase 1 declined to add a section because the split is decided in the spec rather than by an implementer | **contract §16**, appended as the next number; `agents/warden.md` gives its copy up | §11 is already in the contract and sends an agent to `config.md` *under the `seal/` root* without saying where the root is, so the contract could not be followed as it stood. The rule needs no per-role exception, which is the universality test the contract applies to itself. And the definition that carried no copy — `agents/scribe.md` — is the one that reads `seal/parity.md` through `legacy-parity`, which is §11's own missing-copy failure one file over. `spec.md` is left as written: a divergence row is how a difference between spec and tree is recorded, and editing the table would erase the thing being recorded. Phase 4 follows this for `agents/smith.md` |
| §9's account of what the gate counts | phase 1 condensed the two agent paragraphs into §9 | the phrase *command position* restored, with the sentence that a whole fixture file is clean and a fragment of one is not | found by re-pointing `test_edits_go_through_the_edit_tool.py` at the contract: the case went red because the condensation had dropped the half that explains why only some fragments trip. Without it a reader cannot apply the command-word rule to their own patch |
| The warden's paste-ready fix | `agents/warden.md` said *a paste-ready fix for blocking items* | *each 🔴 and each 🟡* | narrower than the format the same sentence points at. `skills/code-review/SKILL.md:345` makes 🟡 *fix or justify* rather than blocking, and `:351` already asks for a paste-ready fix for both — read, this session |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and typecheck at this branch head | the orchestrator, once, after the review rounds settle |
| That a `skills:` frontmatter entry preloads for a **newly added** skill name in an installed plugin build (observed only for skills that already ship) | the orchestrator, with `/reload-plugins` and one spawn once this branch is installed. Phase 2 could not: the copy in force is the 0.5.0 version cache, which holds no `agent-contract/` at all, and neither a reload nor a spawn is an agent's to make |
| ✅ That `$CLAUDE_PLUGIN_ROOT` is unset for every agent kind and not only this one | moot — Q1 answered B′, and phase 1 (37f8c11) reads no path |
| That the user's `/` menu omits `agent-contract` under `user-invocable: false` (the experiment's stated gap; the cost if not is a listed entry nobody should run, not a contract that fails to arrive) | the repository owner, at the first 0.6.0 install |

## Not done

- **`agents/scribe.md` does not load `writing-style`.** It is the only agent
  without it, and its report is prose a person reads. Out of #107's scope and
  left deliberately rather than folded in — it is a change to what a third
  agent reads, and this work item is already changing that surface for all
  three. It belongs in its own item so its own review round can judge it.
- **`agents/smith.md` and `agents/scribe.md` are not brought under
  `tests/test_docs_line_wrap.py`.** Their prose maxima are 148 and 160
  columns; bringing them under is a sweep that would bury this diff. The
  contract itself is written wrapped and joins `COVERED` at birth.

  Phase 3 measured the ground under that sentence and it has shrunk. After
  the move `agents/scribe.md` has exactly **one** prose line over the limit
  (`:22`, 160 columns) — not a sweep, a rewrap. `agents/warden.md` is already
  covered and its two long lines are table rows, which the check excludes.
  The decision still stands, for a different reason than the one `spec.md`
  gave: *at birth* is the precedent for a file written wrapped from its first
  line, this file is not being born, and adding a path to `COVERED` changes
  what a test guards — which `CONTRIBUTING.md` asks a separate argument for.
  Doing it for the scribe while `agents/smith.md` stays out would also read
  as an oversight rather than a decision. The row is in `seal/follow-up.md`
  so the two definitions can be taken together, once.
- **`chain_check.py` gains no required field.** That is #119's, and it is a
  change to a gate needing the argument `CONTRIBUTING.md` asks for.

## Fed back into the spec

<none yet — phase 6>
