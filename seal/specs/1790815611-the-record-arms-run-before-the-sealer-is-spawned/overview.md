# 1790815611-the-record-arms-run-before-the-sealer-is-spawned — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `CLAUDE.md` §*The goal a design is chosen against*; `skills/agent-contract/SKILL.md` §2, §15; `docs/review-chain-spec.md` via `skills/code-review/orchestration.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run*; `skills/verify/SKILL.md` §*The broad gate*; this work item's `spec.md` S1–S10, `plan.md` phases 1–4, `questions.md` Q1–Q4; #638's body
· evidence: `seal/ledger/1790815611-the-record-arms-run-before-the-sealer-is-spawned.md` P1–P11 added; 27 rows across 12 `seal/releases/*.md` files re-read and re-stamped, one of them (0.15.7 N2) corrected in place
· verified: executed — every new case seen red first, 17 mutations each red (11, 3 and 3 by phase), the modules named in each phase's `Verified by` cell, `evidence-check --strict` over the whole ledger, the preflight on the fixture and on this repository; read — `chain_check.py#checked_by`'s ready-pull-request branch; unverified — the full suite, repository-wide lint and the broad gate (the sealer's)

## Why this work exists

A refusal on one of the gate's record arms cost a whole suite, because the
row runs first; `broad-gate --preflight` lets the orchestrator find it in
seconds, before the sealer is spawned.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the preflight's failure head is rendered | `plan.md` Q4 default (a): "a `head` keyword on `seal_stamp.not_sealed` with the old first line as its default". The code calls `not_sealed` once, as before, and `gate()` replaces the form's first line | the code | 1790815615's `plan.md`, phase 1: "`seal_stamp.py`: `not_sealed` takes the names", so a keyword here would collide inside the same function body. The per-check lines stay `not_sealed`'s (`phases/phase-1.md`) |
| How S7's fixture reaches `no fixes to check` | `questions.md` Q1 (a): "built with `generate` … then `Fixes checked by` set to `no fixes to check`". Neither `new` nor `close` writes that value beside a fix word today, so the fixture writes the cell by hand | by hand | measured: `new` lands `nobody — the fixes are not yet written` and `close` corrects it to `nobody — the fixes are written and no round has opened them`, and both exit 0 on a draft (`phases/phase-2.md`) |
| A seventh case the spec did not list | spec §*Data & interfaces*, step 2: "The coverage line is not printed". S1–S10 pin no case for it, and no fixture carries a workflow | `test_the_preflight_prints_no_coverage_line` added | an unpinned line is the next edit's to take back silently (contract §14) |
| A file the spec did not list | spec §*Data & interfaces*, *Documents touched*, lists two test modules. `tests/test_the_rules_have_one_owner.py::test_the_order_opens_the_draft_between_the_build_and_the_rounds` pins the order step's arrows verbatim | the pin moved with the order | spec §Scope: "the preflight is written in as the step before it", which changes the arrows that case reads. The case's other assertions are untouched |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the broad gate over this branch. Each phase ran the modules its `Verified by` cell names and the modules that read what it edited (2,707 passed and one red that phase 4 closed: `test_every_spec_directory_that_reached_the_ladder_has_an_overview`, red only until this file existed) | the orchestrator, through the sealer |
| This repository's own preflight took 30.86 s in the build, on a loaded machine with two DRIFTED rows. Round 1 measured 10.79 s at `7ff69cb4`, the `ledger` arm about 6.6 s, and `evidence-check --strict .` alone 7.06 s, so none of it is the preflight's own doing. **Corrected 2026-10-01** from round 1's ⬜ 3, where this row said why the ledger arm costs that was not measured | the repository owner |
| A verifying round's `fixed at` verdict, as `round_record.py` writes it today, leaves `Pass` beside `nobody — the fixes are not yet written` on the last record. The preflight passes it (exit 0, executed in round 1), and the sealer's run refuses it at `round_record.py seal` with exit 2 after every check has passed, because `seal` accepts only `no fixes to check` on the last record (executed in round 1). So #535's instance, as written today, still costs a suite: it is a `seal` refusal, not a record-arm refusal, and the preflight does not ask `seal`'s refusals (`plan.md` alternative E). **Corrected 2026-10-01** from round 1's 🟡 1, where this row said the instance passes the sealer and fails only at a ready pull request | the repository owner |
| Q3: how many `NOT SEALED` runs had only a record arm failing over 0.17.0 | the flow-log sweep that follows 0.17.0 (`questions.md` Q3) |

## Not done

A dry run of `round_record.py seal`'s three record refusals was not built
(`plan.md` alternative E). Two instances therefore still reach the sealer and
are refused after its suite: #456's unchecked `Pass` box, and #535's
`fixed at` in a verifying round as `round_record.py new` writes it today
(`nobody` on the last record, which `seal` refuses; round 1 executed it). It
is named here as a follow-up for the owner, as the plan asked.

`skills/verify/SKILL.md` §*The broad gate* cites *The last record's `Broad
gate` cell is read at a READY pull request* as a section of
`skills/code-review/orchestration.md`. It is a bold paragraph lead inside
§*Orchestrator: the pull request opens before round 1, and a phase is re-run*.
That reference predates this branch and was left as it stands.

## Fed back into the spec

None. The spec's clauses were built as written; the divergences above are
the places the build answered what the spec left to it.
