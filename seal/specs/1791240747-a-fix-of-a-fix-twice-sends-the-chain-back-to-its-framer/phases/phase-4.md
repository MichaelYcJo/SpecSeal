# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 093ccd3d |
| Ran by | unknown — the spawn prompt did not name the model, and a segment does not name itself |

## What this phase was asked

The fragments and the replay. `changelog.md` with one `### Changed` entry a
reader of the release notes can act on; `seal/ledger/1791240747-….md` with a
row per acceptance claim and the `Re-read ·` rows the moved anchors owe, by
`evidence-check --reverify --into`; S12 executed as a `test_tmp_*` probe
replaying the two 0.18.3 chains with their fix ranges from the pull request
heads, widened to Q1's corpus; `overview.md` closed; `evidence-check --strict`
at exit 0, nothing under `seal/releases/` or `seal/ledger.md` changed, and
`survivor-check` over the branch.

## What this phase found

**S12 holds, executed.** A probe outside the tree (`test_tmp_replay.py`, run
then deleted) loaded the shipped `round_record.py`, read every round record
at a tag through `git show`, set each finding the fix table had answered back
to `open`, and asked `landings` of each record against the previous record's
`Fix range`, counting per run. At `v0.18.3`: #814 (`1791180640`) reads
`first` at round 2 (🔴 1 in `compare_at_base`, 🟡 2 in `proof_refused`, 🟡 3
in `COMPANY`, added) and `second` at round 3 (🟡 1 in `proof_refused`); #801
(`1791163980`) reads `first` at round 2 and `second` at round 3, both in
`reverify`. This matches `plan.md`'s measured table.

**Q1, widened: 18 of 57 work items would have stopped.** At `v0.18.0` the
reading resolved 76 records (16 did not) and stopped 15 of 53 work items; at
`v0.18.3` 7 records and 3 of 4. At `v0.18.1` and `v0.18.2` no record's range
resolves in this clone (23 records). Nearly every stop falls at round 3.

**Notes were the first thing the measurement moved.** The first replay
counted every open row and stopped 24 work items, six of them on ⬜ rows
alone — a ⬜ is "fixed in passing or not at all" and `round_record.py`'s own
`OWED_MARKERS` comment says 🟢, ❓ and ⬜ commission nothing. The spec's
Grounding widens the severity to "any finding that commissions a fix" while
its Scope says "its verdict is open"; the build takes the Grounding, as
`COMMISSIONS_NOTHING`, with a case and a mutation seen red (`1b4b82c6`).

**The hunk grain does not rescue the count.** The same probe asked
Alternatives C's question — a `path:line` inside a hunk the previous range
changed — and it stops 10, missing #801. The grain stays the unit, and Q4 puts
the 18 to the repository owner.

**The ledger: seven claims, 54 re-reads, three corrections.** The released
rows whose anchors this work moved were each read against the edit first;
three had become false once a `second` or a `Reframed` line exists — the
printed bound's R3 and R4 (keyed across the whole work item) and the gfm row
G8 (the mark as the last line) — and are `Corrected ·` rows. The rest are the
`Re-read ·` rows the tool wrote. One line added to `docs/review-chain-spec.md`'s reopening
section (a `second` ends a run too) owed three more re-reads; the file stands
at 999 lines.

**Executed checks.** `evidence-check --strict` exit 0, 6135 ok and 0 drifted;
`git diff --stat origin/release/v0.19.0...HEAD -- seal/releases seal/ledger.md`
printed nothing; `survivor-check --range e6d5a05..093ccd3d` reported no removed
wording standing.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
