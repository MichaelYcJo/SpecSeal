# 1790206437-a-second-fold-writes-a-second-heading — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | b384328c |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Verify: the ledger fragment `seal/ledger/<work-item-id>.md` in one pass from
the drafted rows; `changelog.md` (three entries); `overview.md` with
`## Not verified` naming the sealer for the broad gate;
`survivor-check --range origin/release/v0.15.1...HEAD` with a `survivors.md`
row for anything reported; `evidence-check --strict .` exit 0;
`unverified-check --baseline origin/release/v0.15.1 seal/specs/` exit 0;
`git diff --stat` against the base read against the spec's unchanged list;
every test module that reads an edited document or imports an edited script
run, not a sample.

## What this phase found

**The fragment's first line.** The two 0.15.0 fragments this branch's
neighbours wrote began with their own `<!-- specs/<id> -->` line, and the
fold copied it under the marker it writes: `grep -c` of each marker line in
`seal/ledger.md` reads 2 for `1790173106` and for `1790174138`, so
`--check`'s *118 work items marked* is two above the folded sections. This
fragment carries no marker line and its comment says why. The two standing
duplicates are outside the three tickets and go to the hand-back
(`overview.md` §Not done).

**The frame's own stamps broke the records arm.** `spec.md` S15 and
`plan.md` §Technical context wrote four coordinates as a short path beside
a hash (the `section` unit of `fold_ledger.py` with its 0.4.0 stamp, and
three more — not repeated here, because this record is read by the same
arm). The moment this
work item gained a fragment, `evidence-check --strict .` refused two of
them as *file not found*, exit 2 — the arm reads only work items that have
a fragment, which is why every earlier phase passed. The stamps are dropped
and the units named with their full paths; `overview.md` records it.

**The 25 coordinates were written as `@00000000` and stamped by
`evidence-check --reverify .`** (25 rows re-verified, exit 0), then
`--strict .`: `1686 ok · 0 drifted · 0 broken`, exit 0 — 1662 before the
fragment plus 24 distinct coordinates, `main` cited twice.

**Q4 measured: none.** `bin/survivor-check --range origin/release/v0.15.1...HEAD`
at `1c6e82d4` and again at `b384328c`: 396 then 399 files examined against
30 removed sentences, *no removed wording is still standing*, exit 0. No
`survivors.md` is written; the gatherer's date line was not reported.
`bin/correction-check --range origin/release/v0.15.1...HEAD`: exit 0.

**`bin/unverified-check --baseline origin/release/v0.15.1 seal/specs/`:**
exit 0, this item's one open row named with the sealer as its answerer (15
overviews · 31 open · 4 closed · 0 unreadable).

**`git diff --stat origin/release/v0.15.1...HEAD` against S14's unchanged
list:** 21 files. Of the spec's *Unchanged on purpose* list,
`.github/workflows/hygiene.yml`, `gather_changelog.py`, `chain_check.py`,
`templates/`, `agents/smith.md`, `agents/sealer.md` and `bin/` are
untouched; `skills/code-review/orchestration.md` is changed by two clauses,
the divergence phase 3 recorded. Nothing under `skills/code-review/scripts/`
changed in phase 4; `round_record.py`'s 18 lines are phase 3's two blocks
and a re-wrap.

**Every reader, executed.** The 87 test modules that name an edited
document or script (`agents/warden.md`, `skills/code-review/SKILL.md`,
`docs/review-chain-spec.md`, `docs/release-checklist.md`,
`docs/review-handoff-protocol.md`, `skills/code-review/orchestration.md`,
`fold_ledger.py`, `round_record.py`, `seal/ledger.md`, or one of the four
edited test modules), of 123 in the tree: `bin/test <87 modules> -q`,
**3589 passed, 8 skipped in 825.95 s, exit 0**. The 36 modules not run name
none of those files. The whole suite, the repository-wide lint and the
format check are the sealer's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| four short-path stamps from `spec.md` S15 and `plan.md` §Technical context | nowhere — the hashes are the ledger rows' own, and the rows carry the re-stamped ones |
