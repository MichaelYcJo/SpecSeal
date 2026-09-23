# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 14ab81c8 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Re-read the code work item 0 landed before editing anything, and record the
names: `chain_check.py`'s reopening reader, `stopping_floor`, `run_reopened`,
`round_record.py#floor_and_fixes` and `#bound_line`. Then #218: a stopped
count walk that reached two fires with `running = False`; `bound_line` prints
the gate's own error as the bound; the inner `break` becomes load-bearing.
Rewrite `docs/review-chain-spec.md`'s `What new prints` row for `one
reopening remains` (A17). Cases A9, A10, A11; the differential over #218's
sequences as a `test_tmp_*` probe, run once and deleted. Ledger R3 and R4
re-read. The spawn prompt replaced the plan's rebase step: the branch already
sits on 0's landed code at `0b8dc4b2`, so nothing was rebased.

## What this phase found

**The frame holds for this phase, with one relocation.** Every coordinate
`plan.md` §*Technical context* names was opened at `9461c0a1` and says what
the plan says. The names read off the tree (Q5): the reopening reader is
`chain_check.py#says_reopened` (True / False / None); `stopping_floor` reads
its own row through it and `run_reopened` returns it; `floor_and_fixes` reads
`chain.says_reopened(...) is True` at the `reopened` binding and its count
walk is the shape #218's paste-ready assumes — `counted, counted_at = 0,
None` and `if not stopped and spent > counted` — so the paste-ready applied
as written minus the `FLOOR_YES` line 0 had already removed. **Q5 answer:
unchanged count walk.** `bound_line` is byte-identical to what 0 left. The
relocation: `spec.md` A9 names `tests/test_a_record_precedes_the_fixes_it_commissions.py`
for the case, but every `bound_line` case, 0's A6 included, lives in
`tests/test_the_record_is_generated.py` under *the bound the next round is
under*, so A9 went there.

**One thing in the frame did not hold, and it was found by the check rather
than by reading.** `spec.md` §Data & interfaces wrote four ledger coordinates
as a short path beside a hash, `round_record.py#floor_and_fixes@3d71e88a` <!-- NAME NOT IN TREE -->
and three more of that shape. `evidence-check --strict`'s records arm reads a `@hash` as a
stamp and refused all four as *file not found* the moment this work item
gained a ledger fragment (the arm reads only work items that have one, so
the frame passed the check while it had none). The hashes were also already
stale: R3's row read `173bf4ff` at the frame's own commit. The stamps are
dropped and the units named bare; the marker for the name #217 proposes,
`aside_held` <!-- NAME NOT IN TREE --> until phase 3, was split across a
line wrap and is now on the line that carries the name.

**A11, executed:** `grep -n 'FLOOR_YES' skills/code-review/scripts/round_record.py`
returns six lines, none a reopening read — three in `terminal_value` (the
writer's own bare-`yes` refusal, 0's B3), two in `written_late_cell`, and one
comment in `floor_and_fixes` saying the read goes through `chain.says_reopened`.
No `== chain.FLOOR_YES` anywhere in the file.

**Q2, executed: 0 disagreements after the fix, 16 before.** The probe
`tests/test_tmp_218_differential.py` (deleted, contract §7) <!-- NAME NOT IN TREE --> built every sequence of
length ≤ 3 over 8 record shapes — floor `no` / `yes — a record leaves`,
`Needs a fix` `no` / `yes — 🔴 1`, verdict `answered` / `fixed` — 584
sequences, and for each read `bound_line(n = len + 1)` beside
`stopping_floor` over the same files with `WORKTREE` on, on the sequence as
it stands, on the sequence plus a quiet record, and on the sequence plus a
fix-closing record. Four classes were counted. At `9461c0a1`: 16 sequences
where the gate refuses the sequence as it stands and the line says `one
reopening remains` — #218's class exactly, every one of them a floor `no`
whose walk counted a quiet record and then a reopening — and the same 16
where a quiet next record is refused and the line does not say the run
ends; 0 over-strict, 0 silent. At `14ab81c8`: all four classes 0. The line
counts moved from ends 336 · one 164 · none 84 to ends 352 · one 148 ·
none 84.

**A9 seen red at `9461c0a1`** (executed):

```
>       assert "this record ends the run" in line, line
E       AssertionError: round-record: one reopening remains — round-1.md met the floor and no later record has closed on a fix. If this round's own verdicts close on one, the record after it ends the run whatever it finds
FAILED tests/test_the_record_is_generated.py::test_a_stopped_count_walk_that_reached_two_is_not_a_reopening_left
1 failed, 122 deselected in 0.28s
```

Then green: `bin/test tests/test_the_record_is_generated.py -q -k "bound or
floor or reopening or quiet or walk"` — 15 passed, 108 deselected. A10 is the
existing cases in that selection, all green, `test_the_floor_record_is_the_earliest_and_not_the_latest`
still asserting `(0, False, None)`.

**Five mutations, one at a time, restored from kept bytes** (executed,
`tests/__pycache__` cleared between): M1 the inner `break` dropped — 2 red
(`test_the_floor_record_is_the_earliest_and_not_the_latest`,
`test_an_intermediate_floor_record_starts_a_count_walk_of_its_own`), which is
the ticket's ninth survivor closing; M2 a stopped walk fires at one — the
same 2 red; M3 `running` always True — A9 red; M4 the stopped branch in
`bound_line` removed — A9 red; M5 a stopped walk never fires — A9 red.

**The exits table (A17) now reads**, for the reviewer:

> | `one reopening remains` | an earlier record's floor row reads `no`, no later record has closed on a fix, and no floor record's count walk has fired — a running walk with a record already spent, or a stopped walk that reached two |
> | `this record ends the run` | one later record closed on a fix — or every record after some floor record was quiet, so this one is the gate's second counted record — or an earlier floor record's count walk already reached two before it stopped, so the gate returns an error at that record now, before this one exists (#218) |

**Ledger:** R3 and R4 re-read with a dated note and their hashes recomputed;
0's B1 in `seal/ledger/1790173106-….md` anchors `floor_and_fixes` too and was
re-read the same way; the four rows anchored on the spec's `### Review arm`
and `##### The reopening` headings (363, R5, C2, C6) drifted on the table
edit alone and carry a dated note each. `bin/evidence-check --strict` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/review-chain-spec.md`'s condition *and the count walk has not already spent a record* on the `one reopening remains` row — false since #218 measured it | replaced in the same row by the condition the code implements; nothing else carried the sentence |
