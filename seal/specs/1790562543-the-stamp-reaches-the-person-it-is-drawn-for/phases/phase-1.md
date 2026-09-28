# 1790562543-the-stamp-reaches-the-person-it-is-drawn-for — phase 1

<!-- seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | cde753c2 |
| Ran by | unknown — the spawn prompt did not hand this value over, and the template forbids a segment to source it from its own idea of what it is; the orchestrator fills it |

## What this phase was asked

Build `plan.md`'s Phase 1: the gate signals, and a values file can be drawn
by hand. `seal_stamp.DEFAULT_SCALE = 0.90` with its reason and the 0.75
candidate, both commands defaulting to it; the values reader and `--from`
with claim-before-draw; in `broad_gate.gate`, a terminal draws once and a
pipe draws nothing, writing the file and printing the `SEALED` line on a
recorded seal (S14 and S15 wording included); `pick_shape`'s two answers
split so the terminal question is asked before the reconfigure; the gate
cases that read panel rows off a pipe moved (Q5), and each absence that
stopped proving anything given "and no values file exists", seen red under a
mutant. Documents: the two docstrings, `bin/seal-stamp`'s comment, and
`agents/sealer.md` §*The command*. The spawn also handed over Q2's reading
(equal ids, `agent_id` the only field telling `SubagentStop` from `Stop`),
recorded in `questions.md` Q2, and asked for `CLAUDE_CODE_SESSION_ID` to be
set or cleared explicitly in every gate case (Q7).

## What this phase found

- **The frame holds.** Every coordinate `plan.md` §*Technical context* names
  was where it said, and the trigger point is the code path itself: the new
  branch sits after `seal_record` returned 0, so no red or refused run can
  reach the write. Nothing in the frame was contradicted.
- **Q5, case by case.** Seven positive readings moved, and six of them were
  seen red under a mutant after the move; the seventh, the allowed-forms
  case, reads the same kept text the panel row was made from and was not
  mutated:
  `test_a_repository_shipping_no_gate_runs_the_invoked_copy` (the `gate` row),
  `test_the_gate_with_record_seals_the_item_and_counts_its_rounds` (`rounds`)
  and `test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter`
  (`row`, no `clean`) now read the values file of a `--record` run;
  `test_the_forms_that_stay_allowed_are_sealed_exactly_as_today` reads
  `suite_counts` of the kept `suite.txt`, the same text the panel row is made
  from, because its fixture has no record; the range module's
  `test_the_panel_names_the_ref_the_base_came_from` renders `panel`'s rows
  through `seal_stamp.stamp` and asks the run's `SEALED` line for the
  resolved commit; the workflow module's
  `test_the_stamp_says_how_many_steps_the_seal_did_not_answer` renders
  `panel_rows` the same way; and
  `test_a_green_tree_is_sealed_with_every_check_run_in_order` became S9.
  Two absences in the workflow module (`not answered` not on stdout) were not
  given a values-file check, because those fixtures have no record: one now
  asserts `workflow_text(root) is None`, the input the stamp's row is made
  from, and the other already asserted it. Five absences that could have
  been reached by a stamp gained `not values_files(repo)`: the red run (S7),
  the refused record, both chain-after-write endings, and the in-process
  exit-1 stub (S8).
- **`--shape` on a pipe draws nothing.** Every existing gate case passes
  `--shape`, and S1 keeps it, so the case also proves the flag is no way back
  to a piped drawing. `--shape` now means only which form a terminal gets.
- **The session variable is cleared for every case.** `env_without_a_pull_request`
  and the module's autouse fixture both drop it, and a case that wants one
  passes `session=`. Before that the live session's id would have keyed every
  fixture's file (Q7). The values land in each fixture's own git dir, so this
  was about determinism, as Q7 said.
- **S15 is driven with a FILE where the directory goes**, not a permission
  bit, because a CI runner as root ignores the bit.
- **A hook below the interpreter floor draws nothing.** `seal_stamp.py`
  refuses under Python 3.12 at import, and a hook runs under whatever
  `python3` the harness finds, which is 3.9 on a stock macOS. Phase 2's hook
  therefore draws nothing there and says nothing, like every other failure
  of that hook. The `SEALED` line still names the file, and `seal-stamp
  --from` under a 3.12 interpreter still draws it. Stated in the hook's
  docstring and in the hand-back rather than built around.
- **The editor's formatter removed three imports** added before their first
  use, and the next run failed on `os`. Recorded because the next phase adds
  a module and the same order will do the same thing.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The piped run's drawing: the letter twin a sealer's report carried | `hooks/sealer-stamp.py`, Phase 2, draws the same rows from the values file. Between the phases the tree draws nothing for a sealer's run, as `plan.md` says |
| `agents/sealer.md`'s *the drawing arrives as letters … pass it through as it came* | the same section's new paragraph: the gate draws nothing in a sealer, and neither does the sealer |
| Seven panel readings off a piped stdout (Q5) | the values file of a `--record` run, `seal_stamp.stamp` over `panel`'s rows, or the kept `suite.txt`, each named above |
