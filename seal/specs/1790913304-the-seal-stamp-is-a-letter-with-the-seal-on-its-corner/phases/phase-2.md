# 1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | COMMIT |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`broad_gate.py#panel` loses every `None` row, the `chain` row, the `exit`
row under the suite's counts and the `drifted` row under the ledger's `ok`,
and prints `("CI also", f"{n} more steps")` in the `workflow` row's place;
the docstring's row diagram and the module docstring's stamp paragraph
follow; `ledger_counts` stays. `seal_stamp.SAMPLE_ROWS` mirrors the new
sequence, with its comment. `skills/verify/SKILL.md` §*A seal says what it
did not answer* and `agents/sealer.md`'s *the `workflow` count* sentence name
the new row. Ledger: `1790815615` N5 and N10 corrected in place, N8 re-read,
`0.12.2` R5 and G6 re-read, new rows in this item's fragment. Cases A6, A7,
A8 and A19, and a document pin for the two sentences, each red first.

## What this phase found

**The frame holds for this phase**, with two cases its grep missed (Q5, as
the row expected). `test_a_base_that_is_its_own_commit_has_no_ref_row_under_it`
asserted that the row after `base` is a `None`, and
`test_the_documents_say_the_count_is_over_the_steps_ci_runs` pinned the
sealer's *the `workflow` count* sentence. Both went red in this phase's
module run and were moved: the first asserts the row after `base` is
`("suite", "exit 0")`, the second the `CI also` wording.
`test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter` read the
suite's `exit 0` row too and was in the frame's list only by its line number;
it asserts the ledger's row after the suite's now. Its name still says
*reports the row's exit code*, which is no longer true of a run with counts;
it was not renamed, because the name's second half — no linter asserted —
is what the case is for, and its docstring says what moved.

**`CI also` at 0 reads `0 more steps`** (Q4). The row prints, the way the
stderr line does not go quiet, and
`test_a_seal_that_answers_every_step_says_so` now asserts it on the panel.

**`1 more steps` is kept as the owner chose it.** The plural is not adjusted
for one; the A6 fixture's rendered twin carries `CI also  1 more steps`, and
the case pins that spelling.

**The suite and ledger cases were renamed**, to
`test_the_suite_carries_its_counts_and_nothing_under_them` and
`test_the_ledger_carries_its_ok_count_and_nothing_beneath`, because the old
names stated what is now false. No ledger row cited either name. `spec.md`
§*What was measured* names them as the frame found them, and
`evidence-check`'s record walk refused that line; it now says they were
renamed and carries `NAME NOT IN TREE`. The same walk refused `hook_success`
on line 79, which is a field of the harness's transcript and not a name in
the tree; that line carries the marker too. Both are notes added to the
framer's record, not changes to what it measured.

**`steps_for` is no longer called by `panel`.** The total it gave the panel
left with the denominator; `unanswered` still reads it, and the coverage
line still prints it.

**Red, as shown.** Against the unchanged `panel` and documents, 12 of the 13
selected cases were red; the one that passed is the suite case's no-counts
shape, whose row did not change. Ten mutations through `bin/mutation-check`,
each red: the label put back to `workflow`; the wording cut to `<n> steps`;
`ok` printed from the drifted count; the `drifted` row put back; the suite's
`exit 0` put back under its counts; a `chain` row put back; a `""` row
before `rounds`; the sample's `CI also` row deleted; and each document's old
name put back.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The panel's `chain  exit <N>` row | `SEALED`, which a drawn panel says only on success; the `NOT SEALED` form keeps the chain's `exit N` (`failure_lines`) |
| The `exit <N>` row under the suite's counts | `SEALED`; where there are no counts the `suite` row itself still reads `exit N` |
| The `<D> drifted . <B> broken` row under the ledger's `ok` | `SEALED` under `--strict`; the failure form's `ledger` entry ends with the `total:` line |
| The `<n> of <m>` denominator on the panel | the stderr coverage line, unchanged |
| Every `None` row `panel` returned | none: the sheet draws no blank line, and `read_values` still accepts a `null` an older file carries |
