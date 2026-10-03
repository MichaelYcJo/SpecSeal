# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | ee6d49a5 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`evidence-check` reads citing rows: the family union (D3), supersession by
`Corrected ·`, the citation checked as a coordinate, and three refusals named
— a citation into a fragment, a citing row without a marker, a citation whose
row is gone. The docstring and `--help` say what a citing row is. Scenarios
S1–S4, each case seen red against 233f0455's checker, in a new module run
alone, with `tests/test_evidence_check.py` and
`tests/test_a_row_points_by_content.py` run as the touched modules. M2
measured here, and W1 (the literal rule) decided with the tool that writes it.

## What this phase found

**The frame holds for this phase.** `evidence_check.py#check_text` classified
coordinate occurrences deduplicated per file, as `plan.md` §*Technical
context* says, and `ANCHOR_RE`, `heading_path`, `literal_statements` and
`minor_region` resolve a citation with no new grammar. No ledger row began
with either verb at 70709b73 (`grep -E '^\| *(Re-read|Corrected) · '` over
`seal/ledger.md` and `seal/releases/*.md`: no match), so nothing existing is
reread as a citing row.

**How the family is built.** `ledger_families` reads every ledger the caller
reads and owns the rows that cite a released row or are cited by one;
`check_ledger` blanks those lines before its own walk, offsets kept, and adds
the family's findings. A ledger with no citing row is read exactly as before
(executed: the checker over this tree at 70709b73 and at this phase's tip
gives the same totals apart from this branch's own drift, below). The
per-occurrence reading moved out of `check_text` into `classify`, extracted
through `ast` so every `findings.append(...); continue` became a `return`;
`tests/test_a_row_points_by_content.py#test_the_two_commands_that_must_know_ask_for_the_flag`
named the consumer by function and now names `classify`.

**Two callers needed the whole view.** `main` reads the default ledger set
beside a `--ledger` narrowing, for its citing rows alone, because a narrowing
chooses what is reported and a released row reported DRIFTED because its
re-read sat in an unread file is a false finding.
`hooks/evidence-advisor.py#failing_rows` called `check_ledger` once per file,
so a removal correction would have left its released row BROKEN at every
commit; it now builds one view and passes it to each call.

**W1, decided: the citation `citation_for` writes.** The heading is tried
nearest first, then the path of every enclosing heading, then each enclosing
heading alone outward; a heading holding a backtick is skipped, because it
would close the code span the citation sits in. The literal is the shortest
run of whole words, at least 16 characters where the run has them, from the
first run of the first cell free of `\`, `"` and a backtick that is on no
other line of the section; failing that, the cell's last run with its closing
pipe, written `\|`. That last rule exists because the phase's own case found
a row whose whole first cell starts a longer row's. Spelled out in
`overview.md` as a divergence from D2's *a prefix of the row's first cell*.

**M2, measured (executed).** For every coordinate-bearing table row of
`seal/ledger.md` and the 37 `seal/releases/*.md` at this phase's tip, the
citation was built with `citation_for` and resolved with `cited_row`; a row
passed when the citation came back `OK` naming that same row. 1,083 rows
(the frame counted 1,084; the instrument here is `ledger_table_rows` and an
`ANCHOR_RE` match on the line). A plain first-cell prefix left 68 with no
citation, all cells opening with a code span; cutting at the quoting
characters left 22, all under a heading holding a backtick
(`seal/releases/0.5.0.md`'s *`extractall`, and what refusing it actually
buys*, and one in 0.4.0); with the rule above, **0 fail**. Literal length:
minimum 1, median 17, maximum 30 characters. The probe script was in the
scratchpad and is deleted.

**M3 for phase 1 (executed): 16 drifted coordinate findings in released
files**, none in `seal/ledger.md`, and 0 at 70709b73 (the same checker run
over `git archive 70709b73`, `total: 3594 ok · 0 drifted`). They are
`evidence_check.py#check_text`, `#check_ledger` and `#main` and
`hooks/evidence-advisor.py#failing_rows`, cited from `0.4.0`, `0.5.0`,
`0.8.3`, `0.9.0`, `0.15.1`, `0.15.3`, `0.15.4` and `0.16.0`. They are re-read
at phase 2's end with phase 2's tool, as `plan.md` says.

**Cost (executed).** `--strict .` over this tree took 9.02 s and 9.33 s with
70709b73's checker and 9.13 s and 9.05 s with this one (`/usr/bin/time -p`,
two runs each), so the view adds nothing measurable to the advisor's commit
path.

**Seen red (§15).** Executed with `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py -p no:xdist`
against the unchanged checker before any code: 8 failed, 4 passed. The four
were the control (expected green), S2 (green because 233f0455 deduplicates the
two identical coordinates), the stale correcting coordinate, and the drifted
citation (both checked by the old path). Each of those three, and every unit
this phase added, was then broken with `mutation-check` one at a time and
each went red: 26 breaks, among them membership widened to the next row (S2),
the correcting row's family skipped, and the citation's hash check removed.
`cell_index` survived its first break, against a case expecting the very
refusal the break produced, and went red against S1.

**Narrow runs (executed).** The new module: 21 passed. The 26 test modules
that name `evidence_check` or `evidence-advisor`: 1,522 passed, 6 skipped, 1
failed, `test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
because this work item had no `overview.md`. It has one now.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the anchor loop's body inside `check_text` | `evidence_check.py#classify`, which `check_text` and `ledger_families` both call |
