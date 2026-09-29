# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — phase 4

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-4.md -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 7b7b70e8 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 4: the ledger is true, re-stamped with the new flag.
Re-read every shared row phases 1–3 drifted, reading every row that cites
each drifted coordinate; re-stamp them in their own files with
`--reverify --checked <date>` and a dated note, narrowed with `--ledger` to
the files read; correct any claim the edits made false with a
`Corrected <date>` note; write `changelog.md`. Verified by the lenient check
naming only this work's drift, and `correction-check` over the range.

## What this phase found

- **35 rows in 17 files cited a drifted coordinate** (executed: a read-only
  listing over `ledger_table_rows` and `check_ledger`, printing each row's
  claim). Four were work item A's own fragment rows, which A's squash left on
  the release branch; the rest were in fifteen `seal/releases/` files. None
  was in `seal/ledger.md`. Each claim was read against this branch's diff to
  the anchored unit.
- **Two claims were false and were corrected in place first.**
  - A's O4 said `--reverify`'s overflowing row keeps having its hashes
    rewritten where they resolve. Under `--checked`, a headerless
    overflowing row has more cells than `LEDGER_COLUMNS`, so it has no date
    cell and is left whole. The claim now says so; without the flag it held.
  - 0.9.0's R1 said a record may not state a name "nothing outside
    `seal/specs/` carries". The fragments had been out of the corpus since
    that row's own work item, and #508 took `seal/follow-up.md` out; the
    claim names all three.
- **The other 33 hold**, and each carries a `Re-read 2026-09-29 by work item
  1790635414` note saying what moved in the anchored unit and why the claim
  survives it.
- **The re-stamp was the flag's first real use, and it did what it says.**
  36 rows dated once each (35, then one more below), every cell's earlier
  dates kept and ` · 2026-09-29` appended, and no row left for want of a
  date cell. `--ledger` named the files read, as the documents now tell a
  reader to.
- **One more row drifted because of the notes themselves.** `seal/releases/
  0.13.1.md`'s row anchored on the `### 1788331011` section of
  `seal/releases/0.4.0.md` hashes the rows this phase annotated. It was read
  (its claim is about anchors into retired `spec.md` files, which nothing
  here touched), noted and re-stamped in a second pass: the two-pass shape
  its own notes record from earlier work items.
- **A slip, caught before it wrote anything.** The first attempt passed the
  seventeen `--ledger` flags through an unquoted shell variable, which zsh
  does not split, so the call carried one malformed argument and wrote
  nothing. The rows were then re-stamped with the flags written out.
- **After the phase:** `bin/evidence-check .` reads `2706 ok · 0 drifted ·
  0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow` and
  `0 refused` on the records arm, exit 0; `correction-check --range
  origin/release/v0.16.0...HEAD` examined the one merge in the range and
  found no correction marker dropped, exit 0 (both executed).
- **Phase 5 edits `evidence_check.py` again**, so rows citing the units it
  touches will drift a second time; phase 5 re-reads and re-stamps those.
  The plan's order puts this phase first, and it was kept.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
