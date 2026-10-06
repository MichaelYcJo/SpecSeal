# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 44c3058b |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The gate and the boundary. `chain_check.py` gains `runs_of`; `main` hands
`stopping_floor` and the new arm `fix_of_a_fix` the current run; the arm
carries the eight rows of the spec's gate table; `frame_mark` reads the foot
block and `frame` holds the `Reframed` line's `<who>` to `Planning`;
`round_record.py`'s printed bound reads the current run; what `reach_back`
does to a `no fixes to check` predecessor is settled and pinned (Q3); and
`docs/round-record-spec.md`'s section gets the gate table. S8–S11 are cases,
each refusal seen red before its arm, and `cutoff_item_is_traceable(REFRAME_FROM)`.

## What this phase found

**Q3 needed no line.** `round_record.py#reach_back` already leaves a cell
reading `no fixes to check` standing and prints that it did, so the
redesign's first record does not claim it read fixes the stop never wrote.
The S7 case in `tests/test_a_fix_of_a_fix_is_counted.py` pins both the cell
and the printed line.

**The arm takes the run, not `later`.** The spec named
`fix_of_a_fix(reader, root, rel, earlier, later)`. Nothing in the eight rows
reads the records after this one, and the resumption row needs the `second`
the run began after, so the signature is `(reader, root, rel, earlier,
stopped)`.

**A `Reframed` line above the `Framed` line is refused by the resumption row,
not by the frame arm.** `frame_foot` reads up from the last line and stops at
the mark, so such a line is outside the foot and permits nothing; the record
after the `second` then fails for want of one. The frame arm stays quiet about
it, because a spec without a `second` has nothing such a line could permit.

**The fixture cost phase 1 named was 47 cases in six modules**, every one the
absent row on a hand-written record for `1799000000`. Each builder gained
`| Fix of a fix | no |` with a comment naming `REFRAME_FROM`, the way the
`Fix range` row was carried in for `RANGE_FROM`. Records `new` writes needed
nothing.

**§15, shown red by mutation.** Every row of the arm was broken once
(`if False:` on the absent row's cutoff, the malformed branch, the miscount,
the third landing, the fix under a `second`, the resumption), and so were
`runs_of`'s cut, `main` handing `stopping_floor` the whole tail instead of the
run, the `Reframed` `<who>` and placeholder checks in `frame`, `frame_mark`
read back to the last line alone, and `bound_line` read over every earlier
record. All red. S10's red half is the same tree with the `second` replaced by
`no`, which the floor refuses.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `frame_mark`'s own last-line loop | `chain_check.py#frame_foot`, which reads the foot block and returns the same mark where no `Reframed` line stands |
