# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 9b04c90c |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 2, the routing step across repositories: a `###` subsection
under `skills/implement/orchestration.md` §*Orchestrator: how the work is
routed* covering decision 5's two conditions; a declaration in every gated
repository under one id minted once, each in its own command with
`git -C <path>`; ungated repositories named and never written; the `Pact`
rows written where both conditions hold. The acts table gains its row.
Verified by `tests/test_every_orchestrator_act_names_its_delivery.py` and
S4's pinned sentences in the phase-1 module.

## What this phase found

**The frame holds for this phase.** The section sits as the last `###` under
the routing heading, after *What the answer writes*, whose text runs to the
next `##`; placing it anywhere earlier would have split that subsection's
prose in two.

**The acts-table row reads `check: hooks/commit-review-gate.py`.** When the
orchestrator forgets the step in one repository, that repository's review arm
asks at its first commit, which is the same delivery the parent section's row
names. The grounds say what it does not reach: an id minted twice, and a
missing `Pact` row, which only `pact-check` at the pact's repository notices.
The grounds name `bin/pact-check`, which phase 5 adds.

**The section names `docs/the-pact.md` and `templates/pact.md` before they
exist**; phases 3 and 6 add them. No module that reads `orchestration.md`
resolves those paths today, and the run below is what says so.

**This work item needed its `overview.md` from phase 1 on.**
`tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview`
failed on it in this phase's run, because phase 1's normaliser move was the
first divergence and the memo opens there. It is open now, with both
divergences so far written in.

**Ledger rows this phase drifted (Q13, phase 2).** Seven rows cite the two
`##` regions this phase edited: three on the routing section
(`seal/releases/0.12.0.md` two, `0.15.5.md` one) and four on the acts table
(`0.13.1.md` two, `0.17.0.md` two). Each was read against the edit, each
claim holds, and each carries a dated note. `evidence-check .` then reported
nothing drifted, broken or malformed.

**Verified, executed.** Red: with `orchestration.md` stashed, the S4 case
failed on the absent section (1 failed, 22 passed with the acts-table
module). Green: the 36 modules naming `orchestration.md` and the phase-1
module gave 1914 passed, 6 skipped, 1 failed, the overview case above; with
the memo written, that module and `tests/test_unverified_rows_close.py` gave
235 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
