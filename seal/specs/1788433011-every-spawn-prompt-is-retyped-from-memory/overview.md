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

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, repository-wide lint and typecheck at this branch head | the orchestrator, once, after the review rounds settle |
| That a `skills:` frontmatter entry preloads for a **newly added** skill name in an installed plugin build (observed only for skills that already ship) | the implementation spawn for phase 2, if Q1 answers B |
| That `$CLAUDE_PLUGIN_ROOT` is unset for every agent kind and not only this one | the implementation spawn for phase 1, if Q1 answers A |

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
- **`chain_check.py` gains no required field.** That is #119's, and it is a
  change to a gate needing the argument `CONTRIBUTING.md` asks for.

## Fed back into the spec

<none yet — phase 6>
