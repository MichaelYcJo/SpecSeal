# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 09c50f8f |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#448, the report. `failure_lines` adds one line for the `suite` check when
it failed and `suite_counts` found no pytest summary: the output carries no
summary, so this is not a count of failing tests. The exit code stays 1, and
the panel and `gate` are not touched. The sentence is pinned verbatim, and
`agents/sealer.md` is checked for any wording about reading the failure form
that the new line would contradict.

## What this phase found

- **The line sits where the count would.** `failure_lines` already appended
  pytest's counts for `suite` when there were some. The new line is the
  other branch of that same read, so a failing suite's form always carries
  exactly one of the two, just above `full output:`. The sentence lives in a
  module constant, `NO_SUMMARY`, and the cases pin its text literally rather
  than by importing it, so a rewording turns them red.
- **`agents/sealer.md` did not contradict the line, and it did not name it
  either.** Its *Exit 1, not sealed* bullet listed what the failure form
  prints, and the list would have been one line short. It now says a failing
  `suite` carries the counts or this line, and that the line is the gate's
  words, handed on unedited like `new` and `failing on base too`. Its
  *Report* section already begins with the gate's output whole and unedited,
  so nothing there changes. The bullet sits in `## The command`, and four
  rows anchored there were re-read: `seal/releases/0.12.0.md`'s absent-row
  row, `0.12.2.md` R7, and `0.15.1.md` G3 and N1. None of their claims reach
  the bullet, and each holds.
- **Two of those rows carried two dates in `Checked`.** Each was written as
  the one date of this reading. `plan.md` did not foresee this, and the
  release branch's #588 treats a row carrying one reading as its rule, so a
  merge may meet these cells from the other side.
- **Seen red (§15).** The mutation *line dropped* is the code as it was
  before this phase, and it turned 3 cases red: the two no-summary unit
  outputs and the end-to-end `exit 1` row. The line on every check turned
  the `ledger` output red. The line beside a count turned the two
  summary-present unit outputs and the end-to-end summary row red. The
  sentence reworded turned 3 red. Every mutation ran at `017758c2` from a
  script that restored the file from the bytes it read.
- **Verified by (executed, 2026-09-25):** the new module and
  `tests/test_the_seal_is_taken_once_by_the_sealer.py`, together with every
  module that reads `agents/`, `templates/config.md` or a ledger file. That
  was 53 modules in one `bin/test` call: 2412 passed, 7 skipped.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
