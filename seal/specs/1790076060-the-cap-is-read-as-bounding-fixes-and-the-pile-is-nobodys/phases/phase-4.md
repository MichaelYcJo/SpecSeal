# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | ccf3d921 |
| Ran by | specseal:smith on claude-opus-5[1m] |

Three commits: the fragments and the re-verification at `f616533e`, the
closing correction to `round_record.py`'s two comments at `71599c54`, and the
`Re-read` markers at the commit in the cell above.

## What this phase was asked

The sweep and the fragments. `survivor-check` against the base, answered line
by line — corrected where the wording should have moved, recorded in
`survivors.md` with grounds where it stands by design. `changelog.md` and,
for any claim verified against a coordinate,
`seal/ledger/<work-item-id>.md`. `evidence-check --reverify` for any row whose
anchor this branch drifted.

## What this phase found

**The sweep reported nothing, and the reason is worth writing down.**
`survivor-check --range 6d410023..HEAD` examined 1,202 files against the 24
sentences the range removed and answered *no removed wording is still
standing*, exit 0. No `survivors.md` was written: a file with no rows records
nothing, and one written to say so would be a row nobody can anchor.

**The seven standing copies of *every finding still open becomes an issue*
are not what the sweep was blind to.** Every one of them is about the
reopening bound, where the sentence is still true — the range removes that
wording nowhere, which is exactly why the sweep is silent about them and why
the silence is correct. What the sweep genuinely cannot see is one place the
wording has gone imprecise without having been removed anywhere:
`chain_check.py`'s `CAPPED_EXIT`, the refusal message naming the exit. Under
the ladder a finding at that exit may take rung 2 or rung 4 instead of
becoming a new issue. It is a line a person reads and acts on, so rewording it
is a gate change this work item is scoped out of; it is in `overview.md`
§*Not verified* with the repository owner named. This is the class
`tests/test_the_rules_have_one_owner.py` already documents — *survivor-check
is exit 0 on that class and cannot see it* — met a third time.

**Ten shared ledger anchors drifted, and none was falsified.** Their anchors are
headings and units that enclose text this branch edited, so the drift is the
anchor widening over an edit rather than a claim going false. Each was
re-read against what it claims — the two opt-in headings, the smith's mutation
rule and fix-table rule, the reopening subsection's rule and exit, the label
section's title format and version rule and `size: now`, `New units` as a
finding surface, the contiguity of the orchestration split, the sealer's one
write and `seal`'s refusal of a `round-N` on the last record, the release
sizing criterion, and the verdict cell's two-cell shape — and every one of
them still holds. `evidence-check --reverify` rewrote 27 hashes across the
shared file and this work item's fragment, and the tree is 1,448 ok, 0
drifted, 0 broken.

**Ten anchors, but twenty-two rows — and the markers go in the rows.**
`evidence-check` reports drift once per anchor, and several anchors are cited
by more than one row, so the first count in this record was of the wrong
thing. Six rows carrying a re-verified anchor had not been read at all when
it was written; they were read afterwards and hold, and two of them cost a
measurement rather than a reading — `seal` still has exactly six `raise
Refused` sites, re-counted from the AST, and `tests/test_one_word_one_meaning.py`
is 18 green, which is what rows 2203 and 2253 rest on.

**Every one of the twenty-two now carries a `Re-read 2026-09-22` marker and
today's `Checked` date.** This record is not on the path `correction-check`
walks: `CLAUDE.md` says that check reads the `Corrected` and `Re-read`
markers in the rows to name what a merge dropped from a row that still
stands, and a row reverted to a superseded state is byte-identical to one
nobody touched, so nothing downstream can see the loss. Three sibling
branches of this release merge into `release/v0.13.1` beside this one and one
of them re-stamps rows in this same file, so the marker is load-bearing here
rather than hypothetically. The conflict argument that first kept them out
does not reach either: `--reverify` had already rewritten those exact lines,
so the hunks exist whatever the `Notes` cell says.

**The `Checked` column takes today's date on all twenty-two.** `CLAUDE.md`
says it holds the date somebody read the code and that re-verifying *is*
re-reading followed by `--reverify`. It does not claim the row's executed
evidence was re-run — the `Verified behavior` cell keeps saying when that
happened, with its own date inside it.

**One row would not parse, and it was a defect.** Row 2203 had six cells
against a five-column header and no closing `|`, so the
`**Re-verified 2026-09-16**` marker a previous work item left on it sat past
the column count where a renderer drops it — a marker written to be read by
somebody, invisible to everybody. Its stray separator is now a full stop and
the row is terminated, which puts that marker back inside `Notes`. The
excess-cell shape exists elsewhere in the file where a row quotes table
syntax in its prose; those are left alone, because there the dropped text is
a quoted example rather than a marker.

**Q3's answer is a positive measurement rather than an absence.**
`stopping_floor` re-verified to `db4e9292`, byte-identical to the hash row F1
of `seal/ledger.md` already carried, and `git diff 6d410023..HEAD` over
`chain_check.py` is eight added docstring lines at line 230 and nothing else.
`DEFERRED_HEADER` re-verified to `ab8ad6ea` and `seal` to `30a3d14c` — the
hash row 2197 already held — which is scenario A10 measured rather than
asserted for both files at the moment the fragments were written.

**Then the closing grep found two more carriers, in `round_record.py`, and
they were corrected.** Scenario A3 asks that no sentence claim a capped
record's `Fixes checked by` reads `no fixes to check` unconditionally, and
`grep -rn "reads \`no fixes to check\`"` over the tree turned up two — one in
`seal`'s docstring and one in a comment inside it — both saying *a capped run
reads `no fixes to check` here, so this costs it nothing*. Read against the
corrected rule that is a half-truth: it holds of a capped run's LAST record
and not of a capped record that wrote fixes, for which the refusal is exactly
what sends the run to spawn its verifying round first. Both now say which
record, and both name the owner. `spec.md` §Out licenses a comment or
docstring correction in these two files, and nothing either of them computes
changed — `ruff check` and `ruff format --check` pass on the file, and 402
cases across the generator, sealer and fix-table modules are green. The edits
land inside `seal`, so its rows drifted a second time and were re-verified;
`DEFERRED_HEADER` at line 257 is untouched, so C4's reading of it still
holds.

**This is the same enumeration failure this work item is about, met inside
the work item.** The first pass corrected the sentence where the plan named
carriers and stopped; the class was one grep wider. Finding it cost one grep
and would have cost a review round.

**What was run.** `survivor-check` (exit 0), `evidence-check` (exit 0, 1,448
ok), `unverified-check --baseline 6d410023` (exit 0, and it reads this work
item's two open rows), and six modules covering the work-item shape and the
repository's hygiene rules: 269 passed.

After the marker pass: `evidence-check` again (1,448 ok, 0 drifted — **no
hash moved, so `--reverify` was not run a third time**), `correction-check
--range 6d410023...HEAD` (exit 0, *no merge commit in the range, so no
correction can have been dropped at one*), and every module that reads
`seal/ledger.md` — `test_a_merge_cannot_silently_drop_a_correction`,
`test_a_row_points_by_content`, `test_evidence_check`,
`test_a_narrowed_ledger_read_says_what_it_skipped`,
`test_the_ledger_fragments_fold_at_release`,
`test_the_printed_ledger_name_is_the_file_that_was_read`,
`test_a_record_states_what_the_tree_has`, `test_the_ledger_migrates_itself`,
plus the three hygiene modules and the work-item-shape pair: 540 passed
across the two runs, exit 0 each. The marker pass itself was line-addressed
and content-verified — each row had to still carry the hash the
re-verification wrote and a bare date in its `Checked` cell, or nothing was
written at all, which is how row 2203's shape was found rather than
overwritten. The full suite is the sealer's.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none from the tree. The phase added two fragments and rewrote three `questions.md` cells with their measured answers | none |
