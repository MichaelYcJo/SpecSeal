# 1789621028-nothing-reads-a-record-against-the-tree — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 558226a2 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Close #427's read half. An arm in `chain_check.py` names a record whose
`Grounds` cell carries its own close prefix twice — the arm that makes a
standing duplicate visible instead of leaving it to two commits and a reader.
Acceptance: a planted record at exit 1 naming the file, the finding number and
the repeated text; this repository's committed records at exit 0. The phase
**discloses** that the tree holds zero instances today, so the green run is
not reported as a catch.

## What this phase found

**The corpus does not measure the way the frame said, and two of its three
numbers are wrong.** Re-measured at this branch tip on 2026-09-17, since the
whole class here is a record asserting what nobody measured:

| Figure | `plan.md` / `spec.md` | Measured here |
|---|---|---|
| Committed round records with a Verdicts table | 223 | **227**, out of 229 `round-N.md` files |
| Fix-table files | 39 | **39** — holds |
| Of those stating a range in their first eight lines | 11 | **15** |
| Of those naming `HEAD` | 2 | **5** |
| Distinct spellings of the range sentence | eleven | **8** across the 15 files |
| Surviving doubled close prefixes | zero | **zero** — holds, over 3331 `Grounds` cells |

Three of those are the framer's own instance of #344's class, in the document
that frames #344. None of them changes a decision: 15 files in 8 spellings
with 5 naming `HEAD` refuses the prose-parsing alternative more firmly than 11
in eleven with 2 did, and the zero that the phase's disclosure rests on is the
one that reproduced exactly. **What must not happen is any of them being
copied forward**, so the changelog fragment, the ledger fragment and
`overview.md` carry the measured figures and not the framed ones. Phase 5
corrects the frame's own lines.

**The arm has no cutoff, and that is a decision rather than an omission.**
Every other rule this module added came with a `*_FROM` second, on the ground
that a record written before the rule has no honest repair. A doubled cell is
not that shape: it is not an ABSENT row but a present cell that says a thing
twice, the repair is restoring it from the round's report, and that repair is
available to whoever wrote the record whenever it was written. `fix_surface`
already draws exactly this line in its own docstring — the grandfathering
reaches the absent row, and a row present and malformed fails on any record.
The measurement is what makes it safe: zero standing instances, so no cutoff
is protecting anybody.

**Only one of the three fix words leaves a shape behind, and the arm says so
rather than implying three.** `close` writes `fixed at <sha>` for `fixed` and
the author's own words for `answered` and `deferred`. A standing duplicate of
either of those is indistinguishable from prose that repeats itself, so the
read half covers `fixed` alone while the write half covers all three. The cost
is written into the arm's docstring: a record whose `answered` grounds were
doubled before the guard landed stays unreadable and nothing will name it.

**`verdict_table` returns its header now, which is a contract change with
three call sites.** The cell has to be located by the name at the top of its
column, and only the walk that already read that row knows it. The module's
own docstring for that function is what decided it — *a second walk of the
same markdown is exactly the split this file spends its docstrings closing
everywhere else, so the walk happens here and the questions are asked of what
it returns*. A private helper doing a second walk would have contradicted the
sentence directly above it. The return is `(rows, col, header, errors)`;
`open_blocking`, `closed_with_a_fix` and `commissioned_fixes` are the three
call sites, all in this module.

**The measurements, executed 2026-09-17.** Exit codes read from
`subprocess.run().returncode`; the checker and the case module mutated from
bytes kept in the driver and restored from those bytes.

| Run | Exit | What it printed |
|---|---|---|
| `tests/test_chain_check_at_the_pull_request.py`, whole module | **0** | 118 passed |
| The four new cases, arm in place | **0** | 4 passed, 114 deselected |
| Arm not wired into the dispatch | **1** | the two planted-record cases failed |
| Threshold raised from two prefixes to three | **1** | the same two failed |
| Threshold widened to one prefix | **1** | `test_a_grounds_cell_closed_once_is_not_named` failed — the control that pins a correct close is not named |
| The repository walk's pattern matching nothing | **1** | `test_the_records_in_this_repository_carry_no_doubled_grounds` failed on its population assertion |
| `chain_check.py --baseline release/v0.12.1 --root .` over this repository | **1** | one complaint, and it is this work item's own: *holds no `round-N.md`*, because its rounds have not run. **No existing record was named by the new arm** |
| Neighbouring modules — 13 of them, every module that drives `chain_check` or `round_record` | **0** | 587 passed |
| `uvx ruff check` over `skills/code-review/scripts/` and `tests/` | **0** | |

Each of the four cases is red against what it actually pins, and two of them
cannot be reddened by deleting the arm: the control pins an absence, and the
repository-wide case pins that the walk found a corpus. Green over an empty
corpus is the shape of a check that cannot fail, which is why the population
is asserted beside the verdict.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `verdict_table`'s three-value return | Nothing needs to own it — the header was already parsed inside the function and thrown away, and the three call sites now name it `_header` where they do not want it |
