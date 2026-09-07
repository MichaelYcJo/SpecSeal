# 1788789330-the-update-notice-names-the-expensive-move — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `d361b06` |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

`skills/update/SKILL.md` names `/reload-plugins` and says what it does that a
restart also does. Six sentences were named as coordinates — `:11`, `:32`,
`:79`, `:83`, `:87` and the user-facing output template at `:111` — and the
template says the cheap move first. The hooks and agent-definitions half is
stated at whatever confidence it actually has.

## What this phase found

**`:87` is the sentence that stops the change from backfiring, and the
handoff's coordinate list did not say why it was in it.** *"It does not restart
anything"* was a scope statement about one move. Naming a second move without
widening it leaves a procedure that names `/reload-plugins` and never says it
will not type it — and the ticket's *Not this* is precisely that act. So the
sentence now covers both moves and gives the reason for the second one: a
built-in CLI command is not a skill, so no procedure can invoke it.

**The skill is where the boundary fits and the notice is not.** Both texts
carry the same three-part fact, and they carry it at different lengths on
purpose. A session-start banner competes for a user's first screen, so it gets
one sentence per part; the skill has room for a table, the run that would
settle the open row, and one line saying why *not measured* and *not needed*
must not be collapsed into each other. Splitting it this way is the reason the
notice's wording could stay short without becoming an assertion.

**The overview had to be opened here rather than at the records phase.**
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_
the_ladder_has_an_overview` fails the moment `spec.md` and `plan.md` exist
without `overview.md`, and it fired at this phase's boundary run. That is the
check agreeing with `skills/implement/SKILL.md` §4 — the memo is opened at the
first unverified item, not written at the end — and this work item had five
unverified items before its first line of prose. Recorded because the plan had
the overview in phase 4 and the plan was wrong.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| *"There is nothing to restart for."* | replaced in place at `:32`, now naming neither move rather than one |
| Step 5's old title and body — *"Say that a restart is needed, and why it is safe to finish first"* | replaced in place. The *safe to finish first* half survives verbatim in the new body; only the single-move framing is gone |
| *"It does not restart anything."* as a one-move scope statement | replaced in place at `:87`, widened to cover the reload |
| The output template's *"Restart Claude Code to load it."* | replaced in place. Nothing else carried that line |
