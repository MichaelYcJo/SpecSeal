# 1790206437-a-second-fold-writes-a-second-heading — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | deade859 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

The fold joins (#540): `section_heading`, `insert`, `doubled_versions` in
`.github/scripts/fold_ledger.py` under the gatherer's names, so step D
(#547) rebases over additions; the kept date, the dry-run heading, the
`(appended into the existing section)` message, the `--check` refusal
naming both lines; the module docstring; one sentence in
`docs/release-checklist.md` §2. The `date = args.date or …` line
byte-identical. Cases S3–S8 red first, S8's real-tree red against
`git show 9f846733:seal/ledger.md` in a scratch root. §0.4.0's rows on
`fold_ledger.py#section`/`#main`/`#append` re-read and re-stamped. Minimal
and local.

## What this phase found

**The frame holds, with one line it drew that the code did not need.** The
plan's `main` carried a kept-date override beside the date line — `date =
found.group(1)` where the ledger already heads the version. Written, then
measured dead by mutation: disabling it left both kept-date cases green,
because `insert` drops the block's heading and `main` prints the file's
own (`heading = found.group(0)`), so the date a joined section keeps is a
property of those two lines and not of `date` at all. The override is
removed (`deade859`), the comment beside `heading` says where the kept date
comes from, and the date line stands byte-identical as the plan asked. The
gatherer's `existing_date` is dead in the same way and is not touched: it
is on the spec's unchanged list.

**`insert` splits on `\n` alone, not `splitlines()`.** The gatherer's
`insert` uses `splitlines()`; the fold's cannot, because round 1 of #78
already paid for `splitlines()` breaking a row on U+2028
(`test_a_row_holding_a_line_separator_arrives_as_one_row`), and a row the
first fold moved byte for byte would arrive at the second fold as two lines.
`block.rstrip("\n").split("\n")[2:]` is the equivalent of the gatherer's
`block.splitlines()[2:]`, which drops the trailing empty element for free.

**Q2 decided: two readers.** `doubled_versions` in the script and
`duplicated_version_headings` in the hygiene module read one regex each,
and the hygiene module does not start importing a release script. Each is
pinned by its own case.

**Q5 measured:** no case in the fold module expected the second date; the
module's first run after the change passed 48, and the gather and hygiene
modules with it (120 passed, exit 0).

**The plan's `--dry-run --version 0.15.1` over this tree** cannot print a
heading: `seal/ledger/` holds no fragment on this branch, so the run stops
at *nothing to fold* with exit 1 before any heading is built. Executed and
recorded as such; the fresh-heading path is covered by
`test_dry_run_writes_and_removes_nothing` on the fixture.

**Red first, executed.** `bin/test tests/test_the_ledger_fragments_fold_at_release.py -q -k "second_fold or kept_date or wherever_it_stands or heads_a_version_twice"`
against the unedited script at `dcd060ef`: 5 failed, exit 1 — a second
`0.4.0 — 2026-09-16` heading (S3), `0.4.0 — 2026-09-23` with no `--date`
(S5, today in UTC), the join breaking on the appended area (S4), the dry run
printing a fresh heading (S6), `--check` exit 0 over the planted file (S8).
Real tree: `python3 .github/scripts/fold_ledger.py --check --root <scratch
root holding 9f846733:seal/ledger.md>` exit 0 before the arm, and after it
exit 1 with `0.9.3  at lines 1673, 1764`; over this tree exit 0 with
`118 work items marked` unchanged.

**Mutations, one at a time, restored from kept bytes, `tests/__pycache__`
cleared between:** `insert` always appending — 3 failed (the three join
cases), 1 passed (the dry run writes nothing, as it should); the printed
heading taken from the block — 2 failed (S3's message, S6); `doubled_versions`
returning nothing — 1 failed (S8); the dry-run sentence dropped — 1 failed
(S6). Bytes identical to the kept copy after each.

**The ledger.** `evidence-check --strict .` reported one drift,
`fold_ledger.py#main`; the three rows citing it (§0.4.0, lines 297, 303,
311) were re-read, given a `Re-read 2026-09-24` note each, and re-stamped
by `--reverify` (`2e8fcb28 → 28658ed4 → 9b580650`, once per `main` edit);
the row on `#section` alone (line 302) got its note and no re-stamp,
`section` being byte-identical; `#append` is untouched. Strict: exit 0,
`1662 ok · 0 drifted · 0 broken`.

**Ruff:** one `RUF015` in the new S4 case (a single-element slice), fixed to
`next(...)`; `uvx ruff check` and `uvx ruff format --check` over the script
and the module exit 0. `tests/test_docs_line_wrap.py` and
`tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` over the
edited checklist: 71 passed, 7 skipped, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — `append` stays and `insert` calls it for a new section; the dead `date` override was added and removed inside this phase | none |
