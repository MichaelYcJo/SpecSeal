# 1789296200-the-record-before-the-fix-sequence-has-no-arm — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | <this commit> |
| Ran by | specseal:smith on claude-opus-5[1m] — the spawn prompt named no model; the segment's own harness line is the source |

## What this phase was asked

Build the escape and the trace it writes: one flag carrying a reason, an empty
reason refused in the shape `nobody — <why>` already takes, and the reason
reaching the record in the home `questions.md` Q3 settles, where `close` does
not lose it. Settle by EXECUTION, before the home is fixed, whether `close`
preserves a field row it does not recognise — the framer left that as a read it
did not make, and acceptance A7 pins the answer. Verified by A3, A4 and A7, each
seen red first: A3 by having the escape write nothing, A4 by dropping the
emptiness test, A7 by having `close` rewrite the field block wholesale.

## What this phase found

### Q3 is answered, and it was answered by running something

**`close` preserves a field row it does not recognise.** A probe built a
scratch repository, ran `new`, inserted `| Written late | … |` under
`Target SHA` by hand, committed, and ran `close` with a `fixed` row against a
real fix commit. The row came back untouched, with `**fixed**` written into the
verdict cell beside it — so `close` did its work and did not rebuild the block.
Reading `close` says why: it computes `field_index` for each label it knows and
assigns into `raw` at that index, and the one insertion it makes is a comment
after the last field row. Nothing walks the block as a block.

So **Q3's answer is a new field row**, not prose inside the existing
`Target SHA` cell. Had the probe come back the other way, the reason would have
had to ride that cell — Q3's stated default — and `written_late` would have had
to pull prose out of a cell whose job is SHAs.

The probe is deleted and its scratch repository removed (`agent-contract` §7).
`tests/test_a_record_says_why_it_was_written_late.py#test_close_keeps_the_row_when_it_applies_the_fix_table`
is what holds the answer now, and it is red under a `close` that drops the row.

### Q4 is answered: `Written late`, and the vocabulary was already written

`spec.md` §*Naming constraint* rules out **declaration** and **arm**. The row is
`| Written late | … |` and the flag is `--written-late`, which take neither and
tie the cell to `chain_check.written_late` — the refusal a reader meeting this
row has just been stopped by.

The value is **`no`, or `yes — <why>`**, which is not a new vocabulary: it is
`Needs a fix`'s and `Loses a record or crashes`'s, and `chain_check.yes_or_no`
already reads both. A third spelling of one vocabulary is the drift
`chain_check.py` closes everywhere else, and the shape already carries the rule
this row needs — a bare `yes` names nothing, which is exactly what
`nobody — <why>` and `unknown — <why>` are refused for.

**The flag carries the reason and never the cell.** `written_late_cell` joins
the `yes` to it, so a caller cannot half-write the vocabulary, and the reason is
stripped of the separators `yes` would be joined by — a reason typed with the
dash already in front of it does not land with two.

### The row is unconditional, and the template is why

`| Written late | no |` is written whether or not the flag is given.
`tests/test_the_record_is_generated.py#test_the_field_rows_are_the_templates_in_the_templates_order`
derives the expected rows from `templates/sdd-round.md` itself, so a row that
is sometimes absent is a row that cannot be in the template — and every row in
that block is unconditional. `no` is also the honest landing value: the record
is being written now, and where it is not, the orchestrator has just been told
so by phase 2's line and passes the flag.

**A `no` that is wrong costs nothing new.** It is exactly the silence every
record carries today, and the pull request still refuses the record, because
phase 4 relaxes only for a reason that is present.

**`templates/sdd-round.md`'s ROW lands in this phase rather than in phase 5**,
where `plan.md` puts it. The order case above ties the template and the
generator together in one assertion, so the two files cannot land in different
commits without one of them being red in between. Phase 5 keeps the prose —
`docs/review-chain-spec.md`'s states table and
`skills/code-review/orchestration.md`'s sequence section.

### Phase 2's sentence is now appended

`head_moved_line` gains its last sentence, the one phase 2 deliberately left
out because a commit whose output names a flag that does not exist is false of
itself. Nothing phase 2's cases pin was deleted: they assert presence, never the
end of the text, and that module is green unchanged.

### §15 — what the failure looked like

Driven from `scratchpad/red_phase3.py`, each substitution asserted (§9), the
source restored from a copy taken before the first mutation and never from HEAD.

| Mutation | Result |
|---|---|
| `written_late_cell` returns `no` for every input — the escape writes nothing | **8 failed, 3 passed.** A3 red, and the A4 cases with it, because a flag that writes nothing also refuses nothing |
| the emptiness test dropped, so an empty reason writes a bare `yes — ` | **5 failed, 6 passed.** Every A4 case red, A3 green — which is the half that shows A4 is not passing on A3's mechanism |
| `close` filters out a field row it does not recognise, just before it writes | **1 failed, 10 passed.** A7 alone, which is the case being exactly as narrow as it claims |

Restored, `11 passed`. `tests/test_the_fixes_close_the_record.py` and
`tests/test_new_says_when_head_is_not_the_target.py` are green beside it, 60
passed over the three modules; `tests/test_the_record_is_generated.py` is 103
passed with the new template row.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
