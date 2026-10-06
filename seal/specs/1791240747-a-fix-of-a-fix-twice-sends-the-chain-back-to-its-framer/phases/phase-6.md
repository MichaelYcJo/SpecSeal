# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | b81773fc |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

The records and the replay. Correct and stamp the ledger fragment — A1 to the
path-only reading, the rows anchored on the removed cases REMOVED, the new
cases' claims as new rows. Rewrite the changelog's paragraph on what never
counts, carry the reframe in `overview.md`, re-read `survivors.md`. Answer
round 3's ⬜ 2 by removal. Run Q6 the way round 1's reviewer did, in a scratch
clone with `refs/pull/*/head` fetched, and record the stop count beside Q1's
26 of 64, with #814 and #801 checked.

## What this phase found

**Q6, executed: 26 stops, the same as Q1's 26.** A fresh bare clone of
`origin` in the scratchpad, `refs/pull/*/head` fetched (138 heads) with the
four `v0.18.x` tags. A probe, `test_tmp_q6.py`, run once and then deleted with
the clone, loaded `round_record.py` at `ba4957f9` from the worktree. It read
every `round-K.md` with a `round-(K-1).md` beside it at each tag, set every
row closed `fixed`, `agreed, fixed`, `answered` or `deferred` back to open (the
reviewer's method), and asked `landings` against the previous record's
`Fix range`, counting per work item.

- 122 records have a previous record; 119 resolve and 3 do not, as Q1's
  correction found.
- **26 work items reach `second`**, every one at round 3; 36 reach `first`.
- #814 (`1791180640`): `first` at round 2 (🔴 1 `compare_at_base`, 🟡 2
  `proof_refused`, 🟡 3 `COMPANY`), `second` at round 3 (🟡 1
  `proof_refused`).
- #801 (`1791163980`): `first` at round 2, `second` at round 3, both in
  `reverify`.

The probe counted 72 work items carrying a round record at some tag. The
reviewer's 64 is another count of the same corpus that was not re-derived, so
the comparison stands on the stop count: requiring the path lost no stop
anybody measured, which is what the reading of the records predicted.

**The ledger anchors were coordinates, not rows.** The plan asked for the four
rows anchored on the removed cases to be REMOVED. They were four coordinates
inside A1, beside three on the removed units. A1 is corrected in place — the
fragment is this work item's own and above the freeze — with those seven
coordinates taken out and a dated note naming them, and S5 and S5b's claim is
the new row A8. `evidence-check --strict` read 7 BROKEN before and 0 after.

**Records cite names the tree no longer carries.** `evidence-check`'s record
walk refused 15 lines across `plan.md`, `spec.md`, `phases/phase-5.md` and two
round reports, each naming a removed case or `TRACKED_FILES`. The records are
right about what they describe, so the names stand in a comment above
`NAMED_FILES`, as phase 5 kept the removed readings' names above
`fof_count_of`.

**One ledger claim read as a coordinate.** A8's first draft quoted
`` `mod.py:5` `` in its claim, which the checker read as an old-format
`path:line` coordinate; the claim says "the `.py` path with a line" instead.

**`survivors.md`.** Round 2's three rows quoted a list of what lands nowhere
that the reframe rewrote in all three places, so they quote nothing and are
gone. The redesign's range adds one row, a code fragment the module's `MOD`
fixture shares with a removed case's fixture.

**Executed checks.** `evidence-check --strict` exit 0 (6172 ok, 0 drifted, 0
broken, 0 refused); `git diff --stat origin/release/v0.19.0...HEAD --
seal/releases seal/ledger.md` printed nothing; `survivor-check --range
9c32e7f6..HEAD` exit 0, one survivor excused; `unverified-check` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| A1's coordinates on `names_a_file`, `range_carriers`, `CELL_WORD_RE` and the four bare-name cases | none — the units left the tree in phase 5; A1's dated note names them, and A8 carries S5 and S5b |
| `survivors.md`'s three round-2 rows | none — the text they quoted no longer stands |
| the changelog's tracked-file and carrier clauses | the same paragraph, now saying a finding counts only through the `.py` path its location carries |
