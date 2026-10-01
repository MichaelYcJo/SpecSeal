# 1790835051-the-preflight-asks-seals-own-refusals — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 8e9528c2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The records: `changelog.md` (`### Added` for `--check` and the ask,
`### Changed` for the tail), `seal/ledger/<id>.md` with one row per scenario
the build verified, `overview.md` with S12's empty diff, Q3's number and the
drifted-row re-read, and a `phases/phase-N.md` per closed phase. The re-read
and re-stamp of every row the edits drifted, `--checked 2026-10-01`, each
claim corrected in place where false. A `survivors.md` row for each place
`survivor-check --range e83db346..HEAD` reports wording this branch removed
still standing.

## What this phase found

**The plan's count of drifted rows was short: 35 rows in 15 files, not 26
in 11.** The plan counted the rows on `seal`, `seal_record` and `gate`. The
build also edited `sealed_record`'s docstring, `main`'s `--preflight` help
and `PREFLIGHT_RECORD`. It also edited four document sections that rows
anchor on whole: the spawn section of `skills/code-review/orchestration.md`,
the acts table of `skills/implement/orchestration.md`, `verify`'s broad-gate
section, and `templates/config.md`'s `Broad gate` section. Two rows anchor
on whole files: `templates/config.md` (0.5.0 S8) and
`skills/code-review/orchestration.md` (0.9.3). `evidence-check` named every
one of them. **Corrected 2026-10-02 by round 1's fix pass:** 35 is the
number of drifted coordinates `evidence-check` reports, one per coordinate
per file; the rows that cite them are 48, in the same 15 files, and all 48
were re-stamped in `8e9528c2`. Every row was read against the edit, file by file, and every
claim still held: the six `raise` sites, the one `kept_broad_gate` path, the
single read of `args.base`, the full run's two endings, #638's P1–P6, and the
document claims, which are about content this work did not alter. So none
was corrected. Each was re-stamped with `--reverify --checked 2026-10-01
--ledger <file>`, one file at a time, and the diff of the re-stamp changed
only anchors' hashes and date cells.

**The frame's own coordinates were BROKEN from the frame commit on.**
`spec.md` §Scope and `plan.md` §*The ledger* wrote three coordinates with
short paths and their `e83db346` hashes. The records arm of `evidence-check
--strict .` reads a work item's records and found six BROKEN lines. That arm
is the preflight's own `ledger` arm, so this branch could not preflight
green whatever the build did. The lines are corrected in place to full paths
without a hash, each with a dated note that also corrects the row count. The
same mistake reappeared twice while writing the notes and the overview,
because quoting the broken form is itself a stamp; the notes now describe
the form instead of quoting it.

**`survivor-check` reported two places, both in #638's `spec.md`.** That
spec states what #638's preflight did, which was true of #638, and this work
leaves #638's records as they stand. Both are in `survivors.md` with a quote
and grounds, and the re-run reports every survivor excused.

**#638's `overview.md` has an open `## Not verified` row that this work
answers.** It says the preflight does not ask `seal`'s refusals and names
alternative E. It is #638's record and its answerer is the repository owner,
so it is left open and named in `overview.md` §*Not done* and the hand-back.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The three short-path coordinates with `e83db346` hashes in `spec.md` and `plan.md` | the same sentences, with full paths and a dated correction note |
