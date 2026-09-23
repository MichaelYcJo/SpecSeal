# 1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | e852f49c |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

#138 at the writer and the printed bound. `round_record.py#terminal_value`
refuses a bare `yes` for both labels in `written_late_cell`'s shape;
`bound_line` reads the reopening through phase 1's function. Cases A5 and A6
in the round-record suites, seen red first. Ledger: the rows on
`stopping_floor`, `run_reopened`, `yes_or_no`, `bound_line` and
`terminal_value` re-read with `evidence-check --reverify`; F8 REMOVED from
`seal/ledger.md` and re-founded in `seal/ledger/<id>.md`; the `changelog.md`
fragment for #138.

## What this phase found

**One coordinate in the frame is a function off, and the plan's list of
rows is one row wider than what drifted.** The inline
`chain.yes_or_no(...)[0] == chain.FLOOR_YES` the plan places in
`round_record.py#bound_line` sits in `round_record.py#floor_and_fixes`, the
helper `bound_line` calls; the edit went there, and `bound_line` itself is
byte-identical. `evidence-check` after the edits reported five drifted
anchors — `stopping_floor`, `run_reopened`, `floor_and_fixes`,
`terminal_value` and the spec's *Review arm* `###` region (the `Needs a fix`
table sits inside it) — and neither `yes_or_no` nor `bound_line` moved,
because phase 1 added `says_reopened` AFTER `yes_or_no` rather than inside
it. Ten rows were annotated with a re-read note and re-stamped; F8 was
removed and re-founded as the fragment's B2.

**A5 and A6 seen red at `d835e75b`** (executed;
`bin/test tests/test_the_record_is_generated.py -q -k bare_yes`):

```
A5 [Needs a fix]:               `new` wrote round-1.md, then chain-check refused it
                                  (`Needs a fix` says `yes` and does not say what) — exit 1, not 2
A5 [Loses a record or crashes]: the same, one command late
A6: assert 'this record ends the run' in "round-record: one reopening remains —
    round-1.md met the floor and no later record has closed on a fix. …"
3 failed, 119 deselected
```

After the fix: `tests/test_the_record_is_generated.py` and
`tests/test_a_record_precedes_the_fixes_it_commissions.py`, 173 passed
(executed). `uvx ruff check` and `ruff format --check` clean on the two files.

**Mutations, restored from kept bytes** (executed after `2d51d52f`;
`git status` clean after each):

| Mutation | Killed by |
|---|---|
| M5 `terminal_value` loses the bare-`yes` refusal | A5 for both labels — 2 failed |
| M6 `floor_and_fixes` compares the cell with its own `== FLOOR_YES` again | A6 alone — 1 failed |

**The records check reads this work item now, and it refused four names.**
`evidence-check --strict` came back exit 2 with the fragment in place — not on
a ledger row but on the records: `word_needs` in `spec.md`, `plan.md` and
`phases/phase-1.md` (the local phase 1 removed) and `NEEDS_REASON_FROM` in
`plan.md` (a rejected alternative that never existed). Each line carries
`NAME NOT IN TREE` with the reason, the sanctioned form
(`seal/specs/1790138190-…/overview.md`'s precedent); the strict check is exit
0 afterwards with 1565 rows ok and 0 refused.

**Q1 stands answered at zero**, and the fragment's B2 carries the
measurement, so no cutoff was added.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md` row F8 — *one reader answers both `no`/`yes` rows, and the only cell that tells a correct implementation of it from a lax one is `yes` with a separator and nothing after it*, whose Notes said the floor refuses a bare `yes` and `Needs a fix` does not because that row's reason is the verdict table below the cell | `seal/ledger/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row.md` B2, which re-founds the claim on the new reading; its `yes_or_no` anchor and the two test anchors it cited still stand and are cited by B1 and B2 |
| `round_record.py#floor_and_fixes`'s own `== chain.FLOOR_YES` read of `Needs a fix` | `chain_check.py#says_reopened`, read there through `chain.says_reopened(...) is True` |
