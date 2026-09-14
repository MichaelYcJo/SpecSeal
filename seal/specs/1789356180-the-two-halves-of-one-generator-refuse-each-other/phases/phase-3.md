# 1789356180-the-two-halves-of-one-generator-refuse-each-other — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 9d1e324 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

What `close` preserves in the Grounds cell. No verdict word discards a cell it
was not asked to change: a `deferred` row keeps the fix pass's prose beside its
home, an `answered` row keeps the reviewer's grounds the way a `fixed` row
does, and the empty code span at `fix_table`'s `note` line is gone. Q6 is this
phase's own — whether the repair carries a migration arm over the 66 reduced
rows and the 103 empty spans already committed, with the default being no.

## What this phase found

**Q6 is answered `no migration arm`, and the measurement makes it stronger
than the plan's grounds.** Executed 2026-09-14 over the 66 rows whose Grounds
cell is its home repeated:

| | How many |
|---|---|
| rows reduced to the home alone | 66 |
| of those, with a committed `round-N-fixes.md` beside the record | **15** |
| of those, whose fix row's third cell carried prose the record does not hold | **11** |
| of those, with no committed fixes file at all | **51** |

So the loss is real — #391's own example, rows 15 and 16 of
`1788926756-…/rounds/round-2.md` citing `#309`, reproduces — and for 51 of the
66 the prose is not recoverable from anything in the tree, because a fix table
is an input file and is usually not committed. A migration arm could not run
over them even if one were wanted. For the 11 where it could, rewriting the row
now would assert a state that was not true at the record's own `Target SHA`,
which is `plan.md`'s reason and is unchanged. Nothing found here overturns it.

**The frame's 103 empty spans is 210.** Executed with `fixed at <sha>` followed
by an empty code span, over the committed corpus: 210 rows, not 103. The frame
read this one and the reading was low by more than half.

**The class is three wide and the repair is one line.** `fixed` was already the
only word that preserved what stood, because it alone appended `; {old}`.
Rather than adding that suffix to two more branches, the three branches now
compute `grounds` and one line joins the reviewer's cell to it — so a fourth
verdict word cannot be added without the join.

**The standing `# RIDER:` is right about WHERE and wrong about WHY, measured.**
It says the repair belongs at the `note` line and not in `chain.SEPARATORS`,
because widening that constant would strip the backticks off a home
deliberately written as a code span. But `chain.EMPHASIS` is `[*_`]+` and
`fix_table` applies it to the verdict cell one line before `SEPARATORS` is
reached, so `` deferred `seal/follow-up.md` `` already arrives as `deferred
seal/follow-up.md` — the consequence the rider warns about is already the
behaviour, by a different mechanism. Its conclusion still holds for the other
two callers of the constant, which nothing here measured, so the constant is
left alone and the rider is replaced by a comment recording both halves.

The case that was going to pin the rider's stated consequence was re-aimed
rather than deleted: it now asserts `chain.SEPARATORS` carries no backtick and
that the cut is still at the `note` line, which is what is actually
load-bearing and checkable.

**The cut is widened to the commit's own code span, not to a pattern over the
cell.** Removing every `` `` `` from the note would also remove a legitimate
empty span a fixer wrote; removing the two characters adjacent to where the sha
was cut removes exactly what the cut created. Verified by probe: a cell reading
``| 1 | fixed | `511d6b2` — `token_totals` is summed before the guard |``
lands as `fixed at 511d6b2 — `token_totals` is summed before the guard`, with
the second code span intact.

**Six existing cases asserted the overwrite and were updated, not weakened.**
Each now asserts the joined cell — `the rest is never passed; read` where it
said `the rest is never passed` — so the reviewer's own sentence is what the
case is watching for, which is the property #391 is about.

**Nothing machine-reads a verdict row's Grounds cell.** Checked across
`skills/`, `hooks/` and `.github/`: `round_record.py` is the only reader, and
`survivor_check.py`'s `| Path | Quote | Grounds |` is a different table. So
widening what the cell holds breaks no reader.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the `# RIDER:` at `round_record.py#fix_table` | spent — it asked for the empty-span repair and this phase made it. Replaced in place by a comment recording that its stated reason did not hold at this site, and that the constant is still left alone for the other two callers |
| the overwrite of the Grounds cell by `answered` and `deferred` | the join, which all three verdict words now share. The reviewer's grounds are kept after `; ` exactly as `fixed` already kept them |
| the empty code span beside a fix commit | nothing needs it — it was the tell for a format string joining a value that had been cut in half |
