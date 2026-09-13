# 1789296200-the-record-before-the-fix-sequence-has-no-arm — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `72c8eb5` |
| Ran by | specseal:smith on claude-opus-5[1m] — the spawn prompt named no model; the segment's own harness line is the source |

## What this phase was asked

Make `chain_check.written_late` read the reason phase 3 writes and print
instead of failing on it. A record without the reason is judged exactly as
today. Verified by A5 and A6 in
`tests/test_a_record_precedes_the_fixes_it_commissions.py`, A5 seen red by
having `written_late` ignore the cell and A6 being the existing
`test_a_record_added_after_its_own_fix_fails_after_the_cutoff`, which must stay
green and unmodified. Then that module whole, because this phase edits one with
39 existing cases.

## What this phase found

### It is a third branch, not the early return the frame asked for

`spec.md` §*Data & interfaces* asks for *one new early return, keyed on a value
read from the record's own field table*. An early return cannot do the job.
`spec.md` §Scope item 4 says the check **prints** instead of failing, and an
early return before the message is built prints nothing — the record, the
adding commit, the fix and the row would all go unnamed, which is the whole of
what makes the state checkable by whoever reads it.

So the read is a third branch inside the existing loop, ahead of the
`ORDER_FROM` grandfathering, and it carries the full message with the reason
appended. `overview.md` records the divergence.

### Four states buy nothing, and one of them needed saying out loud

`written_late_reason` is `run_reopened`'s shape, reading `WRITTEN_LATE` through
the same `yes_or_no`. It answers None — judge exactly as before — for the row
absent, the cell unreadable, the cell `no`, and **a bare `yes` with nothing
after it**.

The last is the one with a case of its own.
`round_record.py#written_late_cell` refuses to write a bare `yes`, but nothing
stops a record being hand-edited to carry one, and a relaxation bought with an
empty cell is a waiver with no author — which is the third of the three bad
exits this row exists to replace, wearing a flag. The case is parametrized over
all four.

### The label has one spelling and the case had to be rewritten to catch drift

The first spelling of that case asserted
`round_record.WRITTEN_LATE is chain_check.WRITTEN_LATE` across two separately
loaded modules and went red on two equal strings. Equal **values** would not
have caught the drift either: they are equal right up to the rename. What it
asserts now is that the generator has no literal of its own to rename —
`WRITTEN_LATE = chain.WRITTEN_LATE` present, and the label's text absent as a
string literal.

### §15 — what the failure looked like

`scratchpad/red_phase45.py`, each substitution asserted (§9), each file restored
from a copy taken before its first mutation.

| Mutation | Result |
|---|---|
| `said = written_late_reason(…)` replaced by `said = None`, so `written_late` ignores the cell | **1 failed, 49 passed.** A5 alone |

**A6 stayed green under that mutation and under all four of phase 5's**, which
is what it is for: the existing refusal is untouched, and this work item added
no line to it.

The module is `50 passed` restored. The count before this branch was 39, which
is `plan.md`'s own figure, so the seven this phase added and the four phase 5
added account for all of it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
