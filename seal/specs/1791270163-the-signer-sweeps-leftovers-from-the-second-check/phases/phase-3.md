# 1791270163-the-signer-sweeps-leftovers-from-the-second-check — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | the commit that adds this record (its hash is in `plan.md`'s Status cell for phase 3) |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 3: the records. The fragment from `bin/evidence-check --reverify --into seal/ledger/1791270163-the-signer-sweeps-leftovers-from-the-second-check.md --checked 2026-10-06`, with `questions.md` M1 measured by it; R1's row turned `Corrected · R1 ·` with ⬜ 4's wording, every coordinate R1 rests on and the post-review check 2 fact; `changelog.md` under `### Fixed`; `overview.md` with `## Not verified` naming the broad gate's answerer; `phases/phase-1..3.md`. The spawn prompt added: no broad run, no push, `Ran by` as Opus 5.5.

## What this phase found

- **M1: three rows, exit 0.** `Re-read · Corrected · P8`, `Re-read · R1`, `Re-read · R6`, `3 citing rows written · 0 released rows left`. The grep's three were the whole set.
- The `Re-read · R1` row was rewritten as `Corrected · R1`, keeping the citation the run computed (`"reads the table of"`) and carrying all fifteen of R1's coordinates, `read_table` and the S4 case at the hashes the run wrote. R6's row keeps its `Re-read ·` shape and gains phase 1's plants in its grounds.
- **The plan's own text read as stamps.** `bin/evidence-check`'s records half reported two DRIFTED lines in `plan.md` §*Technical context*, which quoted the released rows' coordinates in the stamp shape. The hashes stay, written outside that shape (`overview.md` §*Where spec and implementation diverged*). After that: ledger 6417 ok · 0 drifted · 0 broken, records 0 drifted, exit 0.
- `git diff --stat origin/release/v0.20.0 -- seal/releases/ seal/ledger.md` was empty. `gather_changelog.py --dry-run --version 0.20.0` exited 0 with the fragment under `### Fixed`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
