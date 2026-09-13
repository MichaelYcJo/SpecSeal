# 1789296100-the-seal-and-ci-read-one-ledger-differently — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `acb496e` |
| Ran by | unknown — the spawn prompt named no model, and the value is the spawning session's to fill |

## What this phase was asked

`evidence_check.py` prints the sentence where its answer is exit 1 and nowhere
else, in the wording `questions.md` Q1 (a) fixed: `broad-gate` runs this check
with `--strict`, where drift is exit 2, and this tree would come back
`NOT SEALED`. Phase 1's behavioural case goes green, and the two ledger
modules show that no existing reader's exit code moved (S7).

## What this phase found

**Q2, measured, and the answer is zero.**
`bin/test tests/test_a_row_points_by_content.py tests/test_a_record_states_what_the_tree_has.py tests/test_a_narrowed_ledger_read_says_what_it_skipped.py -q`
was run at the top of this phase and again after the edit: **182 passed** both
times. No existing case asserts on this script's stdout in a way one appended
line breaks. Reading had said the assertions were substrings over the totals
lines; the run says the same thing, and Q2 is now closed by a run rather than
by a read.

**The condition is the exit code, because the grading became a function.** The
four `return` statements that ended `main` are now
`exit_code(totals, refused, drifted, strict)`, and `main` closes on:

```python
code = exit_code(totals, refused, drifted, args.strict)
if code == 1:
    print(f"\n{LENIENT_NOTICE}")
return code
```

There is no second spelling of the rule to drift from the first, which is what
`plan.md` §Technical context asked for. The extraction is a refactor that
changed no grading, and phase 1's case asserts the unit across the whole table
— both ledger totals and both records-arm counts — so a grading that moved
under the refactor would have been caught rather than assumed.

**The five silence cases were shown red by mutation, not by the unfixed tree.**
An absence assertion cannot fail against a checker that prints nothing, which
phase 1 recorded as a debt. Three mutations were run, each restored from bytes
kept in the mutating process rather than from HEAD, with `tests/__pycache__`
cleared between them:

| Mutation | Result |
|---|---|
| **A.** the `if code == 1:` guard deleted, so the notice prints on every exit code | **5 failed, 8 passed.** `test_the_deciding_form_does_not_repeat_itself`, `test_a_clean_tree_is_silent`, `test_a_broken_anchor_is_silent`, `test_an_old_format_row_is_silent` all went red — every silence case, S2 and all three of S3 |
| **B.** `--strict` deleted from `broad_gate.py`'s `checks[LEDGER]` call | **2 failed, 11 passed.** `test_the_gate_still_passes_the_flag_the_notice_names` went red. This is S4's own red: the checker's sentence asserts something about another file, and the case is what makes that go red instead of quiet |
| **C.** `exit_code` returns 1 for drift whether or not `strict` | **3 failed, 10 passed.** `test_the_grading_is_one_function_and_the_line_reads_its_answer` and `test_the_deciding_form_does_not_repeat_itself` went red — the flag's effect and the notice's silence under it are pinned by two different cases |

`test_no_document_describes_the_lenient_reader_alone` was red in all three
runs and in the unmutated one: it is S5, and phase 3 is what closes it.

**After the edit: 12 passed, 1 failed** — the one failure being S5. Nothing
else in the module is outstanding.

**Nothing was added to the argument parser and no exit code moved.** `--strict`
is untouched, `bin/evidence-check` and its `.cmd` sibling are untouched, and
the workflow's `ledger` step reads `$?` rather than the text — so the sentence
reaches the job log inside the script's stdout with the step unchanged, which
is Q3's reading. Phase 3 opens the workflow and closes Q3 against it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the four inline `return` statements that ended `main` (`evidence_check.py`, the exit block) | `exit_code()`, in the same file, unchanged in behaviour and now callable by a case |
