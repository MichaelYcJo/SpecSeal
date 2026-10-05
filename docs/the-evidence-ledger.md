# The evidence ledger — what a row claims, and what reads it

A ledger row pairs a claim with the code that makes it true.
`seal/releases/<X.Y.Z>.md` holds the rows one release gathered, and
`seal/ledger.md` the notation and the rows from before the fragments existed;
neither changes after its release. `seal/ledger/<work-item-id>.md` holds the
rows, re-reads and corrections one branch is still writing. This document is
the standing account of what a row is, how a released row is read again, what
each checker over it refuses, and what a merge can take out of one without
anybody noticing. Where each kind of record lives is
`docs/the-record-layout.md`.

It is a policy document: it outranks the SDD set, and a work item that finds
it wrong corrects it rather than working around it.

## A row is a content anchor, and it names no commit

<!-- specs/1788229400-every-branch-appends-to-the-same-two-files -->
**A coordinate names content, never a position:** `path#major@hash`, or
`path#major>minor@hash` where a claim needs narrowing. The major level is the
enclosing unit — a function or a class for code, a heading path for a
document. A row carries no line number and no commit SHA, and the check calls
git for nothing — the one exception is `--migrate`, a one-shot writer that
consults the old stamp's commit before it trusts a line number.

That removes a whole chain rather than one rule from it. A line number moves
for edits unrelated to the claim, so the coordinate rotted, so the row was
re-anchored, so its baseline reset, so a stamp was needed, so a squash
orphaned the stamp. The measured instance: a commit seven rows named was not
an ancestor of the default branch after a rewrite, so a fresh clone and CI
both read those rows as broken — for a history operation none of the seven
claims was about.

**An anchor degrades to `DRIFTED`, never to `BROKEN`.** Only the major level
can be broken. A stale minor anchor widens to its unit and says re-read,
because `BROKEN` means *go edit the ledger* and that is the bookkeeping this
removes. **A row whose anchor a change removes is `REMOVED`, not re-pointed**
— its claim went with the code, and the new claim is a new row. Under the
freeze a released row is never removed: a `Corrected ·` row retires it, or
re-points a moved one (§*A released row is read again in the branch's
fragment*).

**Which file a change writes is `docs/the-record-layout.md` §*A change
writes fragments, never a shared file*.** The checker reads `seal/ledger.md`,
the `seal/releases/*.md` glob and the `seal/ledger/*.md` glob alike, and a
row is a content anchor, so the release that folds a fragment into its
release file changes no row's status. The `ok` total counts a
`(coordinate, hash)` pair once per file, so a move can change it.
Enforced by: tests/test_a_row_points_by_content.py::test_no_ledger_row_carries_a_line_number_or_a_commit, tests/test_a_row_points_by_content.py::test_the_checker_asks_git_for_nothing

<!-- specs/1788761915-a-record-states-what-nothing-reads -->
**A work item whose ledger fragment still exists has not shipped.** The fold
removes the fragment at the release, so the fragment's presence is the
boundary — and it is the one a check over unshipped work items uses, rather
than a date or a branch name. A released work item's records are records of a
moment, and holding them to a rule written later is holding them to nobody's
rule.
Enforced by: tests/test_a_record_states_what_the_tree_has.py::test_a_work_item_with_a_ledger_fragment_has_not_shipped, tests/test_a_record_states_what_the_tree_has.py::test_a_work_item_whose_fragment_was_folded_away_has_shipped

<!-- specs/1790208643-the-spec-is-split-and-its-sentences-are-settled -->
**A `|` inside a ledger cell is escaped, and a row with more cells than its
table's header fails.** An unescaped pipe splits the row, and the text after it
lands in the next column, so a claim runs into its grounds and a date into its
notes. At `31937b9f`, 22 rows stood split that way: two of them carried a
second date-and-notes pair in one Notes cell, and one a Notes cell split in
three (#562; #568 joined each into one reading). A row under no header is
counted against the five columns `templates/ledger.md` declares for a ledger
row, because a fragment has no header by rule and the fold copies it into its
release file as it stands — without that width, every fragment row was read
and none was counted (#501). The shipped checker names such a row `OVERFLOW`
in every repository that installs the plugin (#585), graded like `MALFORMED`,
and this repository's own case holds its ledgers to that reading on every
pull request.
Enforced by: skills/evidence-check/scripts/evidence_check.py::overflow_rows, tests/test_release_hygiene.py::test_no_ledger_row_splits_into_more_cells_than_its_header

## A released row is read again in the branch's fragment

**A released ledger file never changes.** Where `seal/config.md` declares
`Ledger frozen from`, as this repository does, `seal/ledger.md` and every
`seal/releases/<X.Y.Z>.md` are not edited after their release: no row in one
is re-stamped, corrected or removed there. Two branches re-reading one row
used to meet on its line at their squash, after the broad gate had run; with
nothing written to the released file, they meet nowhere.
`templates/config.md` §*The ledger freeze* documents the row.

**A re-read or a correction is a citing row in the branch's own fragment.**
Its first cell opens `Re-read · ` or `Corrected · `. The first coordinate of
its Code grounds cell names the released row by content —
`seal/releases/<X.Y.Z>.md#"### <work-item-id>">"<the start of the row's
first cell>"@<the hash of that line>` — and the rest names the code the
claim rests on now. Its Notes carry `Re-read <date>` or `Corrected <date>`,
the markers `correction-check` reads. A claim that went with its code is a
`Corrected ·` row whose grounds hold the citation alone: a released row is
never removed. Adding a new claim is a new row in the same fragment, as it
always was.

**The checker reads a released row together with the rows that read it, as
one family:** the row, every `Re-read ·` row citing it, and every one citing
those. Of the members that record a coordinate, only the readings with the
newest `Checked` date count, and readings that tie on that date are a union:
the coordinate is OK when one of them recorded what it holds now, DRIFTED
when none did, and BROKEN by the rules above. A `Checked` date the calendar
does not have, such as `2026-13-45`, orders nothing, and a reading dated only
by such dates is named with each of them as written, because fixing them is
the repair.
A `Corrected ·` row supersedes
the family of the row it cites, whose coordinates are not checked again, and
starts a family of its own. That is §*A correction a merge dropped*'s halves
rule computed rather than applied by hand: two branches re-reading one row on
one day tie, the side that edited a unit is the side whose hash matches it,
and where both edited it, neither matches. Its cost is stated: content that
returns to a hash only an older reading recorded reads DRIFTED — a partial
revert, one unit back at an old reading while another sits at a newer one,
and a whole revert of one unit alike — though somebody once read the claim
against it. The cost is a re-read, never a question. What it buys is that a
coordinate is held to its newest reading, so a revert to content a newer
reading superseded is caught. Coordinates are still judged one at a time, as
the halves rule judges units: two branches re-reading different units of one
row leave a pair no single reading recorded, and it reads OK, because each
side read the unit it edited. A same-day pair of readings from two branches is
a union, so a revert to either reads OK.

**A citation that does not hold is named.** One into a fragment is refused,
because a fragment moves at the fold — re-stamp that fragment's row in place
instead. A citing row without its marker is refused. A citation whose row is
gone is BROKEN, and one whose released file changed under it is DRIFTED.
A released row corrected by two or more `Corrected ·` rows is two claims
nothing has reconciled, so each of those rows is DRIFTED, naming the others:
read them together and keep one claim. The second branch cannot cite the
first one's row before the fold, so the repair is one row merging the two.
Once both have folded, a `Corrected ·` row citing one of them retires it.

**`evidence-check --reverify --into seal/ledger/<work-item-id>.md --checked
<YYYY-MM-DD>` writes the re-reads.** It re-stamps the fragments in place,
then writes one `Re-read ·` row for each released row with a drifted
coordinate — one per row, never one per coordinate — and names each row it
wrote. Without `--into`, `--reverify` writes no released file and names each
row it left. Narrowed with `--ledger`, either form answers for every family
that a file it read holds a member of, released or fragment, by the family's
root row, whichever members carry the drifted coordinate: a coordinate only
fragment re-reads carry is owed a re-read of a released root too. The
`Checked` column holds the date somebody read the code, and
`--checked` writes that date into every row whose hash it moves; it says
every such row was re-read, so read each row citing a drifted coordinate
first, or narrow the write with `--ledger` to the files you read. No such
reading is owed where the family already holds a coordinate, or where a
`Corrected ·` row supersedes the family, so an in-place re-stamp leaves that
coordinate's hash and date as they are (#785). On a row it dates for another
coordinate it moves a held one's hash too, since that date makes the row its
newest reading. A `Re-read ·` row is a reading dated `--checked`, so where a
coordinate it would carry has a reading dated later, that reading outranks it
and the row would
clear nothing: the run writes no row for it, still records the pact changes
its moved coordinates owe, names it with both dates and the place of the
later reading, and exits 1. Read the code again and date that reading; a date
equal to the newest ties and is written, and a newest reading dated after
today, which no `--checked` reaches, takes a `Corrected ·` row. The record is
written by the refusing run because a `Corrected ·` row is never re-read
again, and a pact change is never lost. A released row whose anchor moved is
not cleared by a re-read, because the family is keyed on the coordinate, and
a `Corrected ·` row re-points it. That row supersedes the whole released row,
so it carries every coordinate the claim still rests on, the moved one at its
new place: a coordinate it leaves out is not checked again.

**`correction-check` holds a pull request to the freeze.** A range that adds
a work item at or above the cutoff, or adds none, may not change
`seal/ledger.md` or a release file its merge base already had; a range whose
work items all sit below it is read under the rule it was cut under, and says
so in one line. Adding a release file is allowed, and so is the base's own
version's file on a `release/vX.Y.Z` base (#540). A `Corrected ·` row a merge
drops while the released row it cites stands is reported as a loss.

**Without the row, a released row is kept true where it stands.** A
repository that does not declare the freeze re-stamps a re-read row in place
with a dated note, corrects a false claim in place with a `Corrected <date>`
note, and removes a row whose claim went with its code, writing the new claim
into the branch's own fragment. That is what every installed copy does until
it adds the row. Where citing rows exist anyway, a `--reverify` narrowed with
`--ledger` names, by its root row, each family that a file it read holds a
member of, released or fragment, where no in-place re-stamp of the files it
read clears that family, whichever members carry the drifted coordinate, and
exits 1. The root is named even where the
narrowing left its file out, because the root is the row a `Re-read ·` cites.
The line names a remedy per coordinate, by why the family is still owed one
(#792). Only where a newest reading of it sits in a file the run did not
write does it say to run without `--ledger`. Where the run left the
coordinate itself, its claim quoting text the run rewrote or its row left
whole for want of a date cell, the line says so and points at the line naming
why, and a run over every ledger names such a family too. Where neither is
found it names no remedy.

**Five things `--reverify` leaves at exit 0 while `--strict` exits 2.** This
holds without the freeze, under it, and under it with `--into`, over every
ledger or narrowed with `--ledger` to the file holding a row `--strict`
names, unless a sentence below says otherwise. Each repair is an edit or a
correction, which a person makes.

- A released row corrected by two `Corrected ·` rows. Each correcting row is
  DRIFTED and names the others, and which claim stays is a person's choice.
- A BROKEN coordinate. Only where a released row carries it under the freeze
  does `--reverify` name it, with the `Corrected ·` repair, and exit 1. Where
  only fragment rows carry it, or without the freeze, it exits 0.
- A family rooted in a fragment, a `Corrected ·` row there, whose anchored
  statement is gone. The in-place re-stamp has nothing to hash and leaves it,
  and a family rooted in a fragment is owed no released re-read. Under a
  released root the same coordinate is named, and the run exits 1.
- A citing row refused `MALFORMED`: one without its marker, or one whose
  citation names a fragment row.
- A citation whose released line changed under it. Under the freeze that is a
  folded citing row whose cited release file was edited, which
  `correction-check` refuses at the pull request. Without the freeze it is
  not among them: one run over every ledger re-stamps a released row and every
  citation of it that it moves, because it walks a cited file before every
  file citing it (#772). A release file citing a row of itself, which a
  second fold writes, is walked again until it settles. A run narrowed with
  `--ledger` that moves a line cited from a file it left out names the citing
  row on a `LEFT` line and exits 1.

A `Re-read ·` row with a `--checked` older than the newest reading is not
among them: `--into` names it and exits 1, as its paragraph above says.

## What the checker refuses, and what it says while refusing

<!-- specs/1789296100-the-seal-and-ci-read-one-ledger-differently -->
**One ledger, two readings, and the lenient one says so.** The checker's
default reading is lenient and the broad gate runs it with `--strict`. A run
whose answer is exit 1 — and only then — says that the strict reading would
refuse this tree, so every reader gets it: both wrappers, the CI job, and a
bare invocation of the script. A tool whose two callers disagree about the
verdict, and which tells neither caller so, is a tool that reports clean to
whoever asked first.
Enforced by: tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py::test_a_drifted_tree_is_told_what_the_gate_would_say

<!-- specs/1788686494-the-printed-ledger-name-collapses-through-relpath -->
**A name a person reads is the file that was actually opened.** Turning a
ledger path into a display name goes through one helper, at every site that
prints one. A relative path computed against the wrong base collapses to
something that names no file, and a header naming a file nobody read is worse
than no header: the reader takes the rows below it for that file's rows.

**What a narrowed read did not look at is part of its answer.** A scoped read
is right for writing — it keeps a re-verify off a row somebody else owns —
and a silent partial answer is not right for reading. The checker names what
it skipped, because guidance binds a session that reads the guidance and a
session that narrows on its own initiative still gets an answer it will
believe.
Enforced by: tests/test_the_printed_ledger_name_is_the_file_that_was_read.py::test_no_ledger_path_reaches_relpath, tests/test_a_narrowed_ledger_read_says_what_it_skipped.py::test_a_narrowed_run_names_the_shared_ledger_it_did_not_read

<!-- specs/1790154760-the-ledger-grows-and-nothing-takes-a-row-out -->
**The checker parses each Python file once per process, so a file that many
rows cite costs one parse.** The answer is memoised on the file's text and
never on its path, because `--reverify` and the suite read one path twice
with different content in one process, and a path key would hand the second
read the first read's spans. Each caller gets a fresh copy, so no caller can
change the answer the next one gets. #519 asked whether a ledger that only
grows should take rows out, and measured before choosing: every anchor
resolved, the release sections mostly do not repeat what `docs/` states, and
the 15.2 to 15.4 s that every `git commit` paid in the evidence advisor was 1,328
parses of 126 files (`cProfile` and `/usr/bin/time -p` over `--strict .` on
this repository, 2026-09-23). Parsed once per file, the same commit waits
about 1.7 s. The cost was the parse and not the rows, so no row left: a row
still leaves the ledger only with its code.
Enforced by: tests/test_a_row_points_by_content.py::test_rows_citing_one_file_cost_one_parse, tests/test_a_row_points_by_content.py::test_a_file_edited_between_two_reads_gets_its_new_spans

## A correction a merge dropped

<!-- specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections -->
**When a ledger file two branches both edited conflicts — a fragment stacked
branches share, or a released file where the freeze is not declared —
resolve it hunk by hunk and read both sides.** Never *ours* and never
*theirs*. A released file under the freeze takes no edit, so it cannot
conflict. A whole-file choice is
wrong by construction once both branches have been correcting: the measured
instance resolved two hunks in opposite directions, because each side was the
superset in one of them, and taking a side reverted three corrections that had
each turned a false claim true.

**Nothing downstream can see that, which is why the reading is a person's.**
A row reverted to a superseded state is byte-identical to a row nobody
touched. There is no marker on it, and the hash the checker reads is correct
for the restored text.

So a second check reads the markers instead. For every merge commit in a
range, a `Corrected <date>` or `Re-read <date>` marker present in **either
parent's** ledger text and absent from the result, **while the row carrying
it survives**, is reported with the file, the marker and the parent it came
from. Row survival is the one distinction that check exists to draw: a marker
that vanishes with its whole row is a removal and is correct; a marker that
vanishes while its row stands is the defect. A `Corrected ·` row is the one
whole row whose loss is also reported, because the released row it corrected
still stands. It reports the loss after the fact and cannot prevent it.

It reads the shared file, every release file and every fragment, because a
fragment becomes part of a release file at the release and a check that
skipped fragments would go blind exactly while the rows are being written.
Enforced by: tests/test_a_merge_cannot_silently_drop_a_correction.py::test_a8_both_guides_send_the_reader_to_the_rules_home, tests/test_a_merge_cannot_silently_drop_a_correction.py::test_the_policy_document_owns_the_conflict_and_the_re_read

<!-- specs/1790208643-the-spec-is-split-and-its-sentences-are-settled -->
**Hunk by hunk has two halves, and only the notes are a union.** A row's
`Re-read <date>` and `Corrected <date>` notes are both sides', because each
records a reading somebody performed. The anchor's hash is not a union: it
belongs to the side that edited the anchored unit, and to neither side where
both did, because the merged unit is then content neither side hashed. A
resolution that keeps a hash the merge made stale names content that no
longer exists anywhere, and the marker check above cannot see it, because no
marker was dropped. So run `evidence-check` after the resolution: a drifted
anchor is the tool naming the row, and the row is re-read against every edit
the merged unit carries, one side's or both, before it is re-stamped. For a
released row under the freeze the checker computes this itself
(§*A released row is read again in the branch's fragment*).
Enforced by: tests/test_a_merge_cannot_silently_drop_a_correction.py

<!-- specs/1789996780-the-census-and-the-tie-that-nothing-holds -->
**A bound over the corpus is stated with its instrument and the moment it was
taken.** A case that asserts a bound covers every candidate site takes its own
census over the real corpus, says how the number was taken, and says what it
does when the corpus grows past it — the property, never a spelling and never
a bare number. A sentence stating a count with no instrument beside it is a
claim nobody can re-derive, and two such sentences in one module were
arithmetically false about the module's own corpus.

**Where a merge has two parents and both could be named, the tie falls to the
first.** A rule that leaves a tie unstated is a rule with a case nobody wrote.
Enforced by: nothing — no case reads it yet. A case that read every census-taking
case for the instrument beside its count would; the tie rule is held by
`test_a_tie_falls_to_the_first_parent`.

## The unverified record, and the baseline it is read against

<!-- specs/1788873600-the-baseline-is-the-moving-pull-request-base -->
**A baseline reference is resolved once, to a merge base, and every arm reads
that commit.** A branch name is not a commit: it moves while the pull request
is open, so two arms reading it a second apart can compare against two
different trees. The report names the revision it actually compared against,
and a reference sharing no history with the head is exit 2 — a comparison
against nothing is not a comparison.
Enforced by: tests/test_unverified_rows_close.py::test_a_row_the_base_gained_after_the_fork_is_not_a_deletion, tests/test_unverified_rows_close.py::test_a_work_item_squashed_after_the_fork_is_not_this_branchs_removal

## The fold, and what tells it from a deletion

<!-- specs/1790154761-folded-statements-pile-into-one-spec -->
**Every folded statement has the fold's shape: the cutoff binds every statement
from work item `0` on.** The shape and the placement rule are stated in
`skills/settle/SKILL.md` §*2. Write one standing statement per
segment*, and this section holds only this repository's values for them. The
cutoff is the id in the marker, and ids are epoch-prefixed, so it is a
comparison rather than a list. It was `1790154761`, the work item that gave the
fold its shape, and the statements it did not bind had been written with no
line naming what reads any of them; review found one of them false. #565 gave
each of them its `Enforced by:` line and lowered the cutoff to `0`. Counted
by `fold-check --shape-from 0` on 2026-09-25, before the lines were written:
136 statements under `docs/`, 115 of them without the line.
Enforced by: skills/settle/scripts/fold_check.py::bound, tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape

<!-- specs/1790154761-folded-statements-pile-into-one-spec -->
<!-- specs/1790208643-the-spec-is-split-and-its-sentences-are-settled -->
**A top-level document under `docs/` stays at or under 1000 lines, and one
over that ceiling takes no new statement.** Two folds had put 29 statements
into `docs/review-chain-spec.md`, 2,159 lines long while the next
largest document was 839, because nothing said where a fold lands. It was
split along its own headings by MichaelYcJo/SpecSeal#526 into itself,
`docs/commit-review-gate-spec.md` and `docs/round-record-spec.md`, its fold
markers carried across whole. A document the next fold would take past the
ceiling is split the same way first, or the rule goes to the document for
its own sub-subject. No document is listed over the ceiling now.
`docs/commit-review-gate-spec.md` was, after #692 took it to 1,039 lines,
until MichaelYcJo/SpecSeal#727 cut it the same way into itself,
`docs/the-commit-gate-inside-git.md` and `docs/the-review-and-parity-arms.md`,
and its entry went with the cut. The cutoff, the ceiling and the list are
rows of this repository's `seal/config.md`, which `fold-check` reads, and a
pin holds the rows and this section to the same numbers.
Enforced by: skills/settle/scripts/fold_check.py::ceiling_problems, tests/test_a_document_has_room_for_the_next_fold.py::test_the_evidence_ledger_states_the_values_the_config_rows_hold

<!-- specs/1790154761-folded-statements-pile-into-one-spec -->
**A fold into a document with a `.ko.md` edition is a fold into both, under the
same heading position.** The first fold wrote a section and ten markers into
`docs/one-root-by-lifetime.md` and nothing into its Korean edition, and nothing
noticed, because the one pin compared a single section's cell count. The two
editions are prose in two languages, so the check compares what is
language-neutral: the sequence of heading levels, and the fold-marker ids under
each heading position. Whether a Korean paragraph says what its English one
says is review's to read. `CONTRIBUTING.md` §*House rules* owns the rule.
Enforced by: tests/test_both_editions_carry_the_same_folds.py::disagreements

<!-- specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built -->
**A released work item's directory is folded into a policy document and then
removed, and the removal is the second half of the fold, never its own act.**
A directory removed before a document absorbed it takes the reasoning with
it, and that is the one loss nothing can undo. The command reads and groups;
the session judges and writes. Folding *only what is still true* is a
judgment about truth, so the tool writes no sentence into a policy document
and its second arm removes only what one of them already absorbed.

**The marker is the fold's record, and there is no second file.** A folded
sentence carries `<!-- specs/<work-item-id> -->` on a line of its own, and
that comment is read to know what has been folded — so nothing has to be kept
in step, and a run interrupted between writing the prose and removing the
directory picks up where it left off. The removal of a directory and a branch
deleting one are otherwise byte-identical to every reader; the marker is what
tells them apart, which is why a reader of removed work reports a fold rather
than a deletion.
Enforced by: tests/test_settle_reads_before_it_removes.py::test_retire_removes_only_what_docs_records

<!-- specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft -->
**A marker counts only on a live line, and one function decides what live
means.** A line begins live when it begins outside a fenced block, outside an
HTML comment and outside a code span. A marker quoted inside a fence is a
description; one inside a commented-out draft is a parked one; neither
records a fold, and both used to excuse a removal nothing had absorbed. Every
reader of the fold record and of the ledger's own sections asks the same
function, so the rule cannot be spelled twice and drift.

Where markdown will not answer without a block model — a backtick run with no
partner on its own line is literal text if the paragraph ends first and a code
span if it does not — **both readings are computed and a line is live only
where both call it live.** Nothing decides where the block ends; the
disagreement is resolved toward keeping a work item's directory. The cost is
a fold reported as a deletion, which a person sees at exit 1 and can act on,
and that is the cheaper of the two mistakes.

**The fold reads the top level of `docs/` and no deeper.** A fold writes into
a flat policy directory — merge into a document that exists, create one only
for an area with none — so a marker below the top level is somebody's notes,
and a scratch file quoting one excused a removal nothing had absorbed.
Enforced by: tests/test_unverified_rows_close.py::test_a_marker_inside_a_commented_out_draft_is_not_a_fold_record, tests/test_unverified_rows_close.py::test_a_marker_inside_a_fenced_block_is_not_a_fold_record

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
<!-- specs/1790138190-settle-leaves-twelve-directories-with-no-way-out -->
**A released work item that wrote no `spec.md` states no rule, and it is
retired by that rule, with no marker.** Such an item was below the SDD
ladder: a release entry, a renumbering, a CI repair, a pull request's record.
Those are records of a moment, and a moment states nothing to fold — which is
also why nothing has to be carried out of one, so `settle` prints these under
their own heading and `settle --retire` removes them without writing a marker
into `docs/` (#517). **One condition narrows it: nothing in the record may
still be open.** An open `## Not verified` row or an open `evidence-todo.md`
row is a claim with an answerer rather than a rule, so a directory holding one
is kept and named with its rows, and closing each row — a row re-homed is
closed too, ✅ naming where it went — in a pull request merged before the one
that retires the directory is what lets the next retirement take it. The CI
readers ask the rule of the merge base, so a closure in the same pull request
as the removal is still open where they look. `settle` asks it at the merge
base of `--released-at` and `HEAD`, which is where they look until the base
moves past the fork and earlier after, and keeps a directory whose closure
has reached the working branch and not that base (#602). One predicate
decides the rule,
and `settle`, `unverified-check`, `chain-check` and the survivor sweep all ask
it, so the four cannot disagree about one tree. Whether the item wrote a
`spec.md` is asked of its history, so a spec deleted in one commit, or in an
earlier pull request, and the directory in the next is still a deletion. That
condition is a judgment the repository owner may overturn. An ungrouped item
that did write a `spec.md` is folded where that spec's rule belongs. One more
reason keeps a directory: **a permanent
ledger row anchored inside it**, which holds the directory until the row is
answered — so a work item with a row anchored in its `rounds/` stays on disk,
and the fold does not remove it to tidy the list. Keeping the directory rather
than removing the row is a default, and the repository owner is who can trade
it the other way: remove the row, carry its claim into the prose it evidences,
and let the next `settle --retire` take the directory. For `1788184145`, the
one directory held this way when the guard below shipped, that trade was
taken (#517): the row was removed, and its claim stands in
`docs/review-chain-spec.md` §*Two records, and what each of them says*.
Enforced by: tests/test_settle_reads_before_it_removes.py::test_the_rule_arm_removes_it_with_no_marker, tests/test_settle_reads_before_it_removes.py::test_a_closure_the_base_has_not_seen_keeps_the_directory

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
<!-- specs/1790138190-settle-leaves-twelve-directories-with-no-way-out -->
**A retirement would break every ledger row anchored inside the directory it
removes, so the retirement refuses that directory first.** An anchor into a
work item's `spec.md` or its round records is a file path like any other, and
after a removal the checker reports it broken. So `settle` reads every ledger
the checker reads — `seal/ledger.md`, every `seal/ledger/*.md`, every
`seal/releases/*.md` and any `docs/**/_evidence.md` — and every line of each.
The rows above the first section marker are included because the checker
reads those too. The rows inside a fence are included although the checker
skips a fence that closes (#444), because a guard that reads more than the
checker keeps a directory the checker would not break, which is the
direction to be wrong in. It names each row anchored inside a
released directory, and `settle --retire` keeps every directory such a row
anchors into, removes the rest, and exits 1 naming each row (#511). It says
per row what §*A row is a content anchor, and it names no commit* requires: a
row whose every anchor goes is REMOVED, never re-pointed, and its claim is
written anew where a work item still holds it; a row that keeps a live anchor
beside the dead one loses only the dead one, and whether it should be removed
instead is the repository owner's question, recorded against the ledger row
that first met it. Under the freeze a row in a released file says `released`
instead: a `Corrected ·` row in the fold's own fragment answers it, and a row
a correction supersedes holds no directory. The command names the rows and
edits none of them, because which row goes is a judgment about a claim.
Enforced by: tests/test_settle_reads_before_it_removes.py::test_a_row_anchored_inside_a_candidate_keeps_that_directory

<!-- specs/1790138190-settle-leaves-twelve-directories-with-no-way-out -->
**A fold is not a work item, and it adds no work item's rows to the
ledger.** It opens no directory under `seal/specs/`. Under the freeze it
writes its readings and corrections into a fragment named for the moment,
`seal/ledger/<unix-seconds>-fold.md`, which the release folds like any other;
without the freeze a ledger file changes on a fold branch only by removal and
re-verification: a row the guard named REMOVED goes, a row it named narrow
loses its dead anchor, and a row whose anchored unit the fold's own prose
edited is re-read and re-verified. Its commits are waived one command at a time and its
judgment is reviewed at its pull request (#517). What it leaves already has a
home — the marker, the pull request, git history — so it keeps no log of its
own. A fold that opened a work item left a directory for the next fold to
retire, and that fold opened one of its own, so no fold could ever finish.
Enforced by: tests/test_settle_reads_before_it_removes.py::test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row, tests/test_settle_reads_before_it_removes.py::test_the_skill_says_what_a_fold_does_to_the_ledger

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
<!-- specs/1790119502-four-shipped-work-items-wait-unfolded -->
**A population floor over the records is replaced, never lowered.** A check
asserting that a sweep of `seal/specs/` read *enough* — `len(records) > 200` —
is answering *did the walk read anything* with a literal that stops being true
the moment the corpus shrinks, and a fold shrinks it by design. The repair
compares the walk against an independent listing of the same tree —
`git ls-tree HEAD` — which holds at any size, and a property the real corpus no
longer exercises moves to a record built in `tmp_path`. A repair is green
before the fold and after it; one green only once the directories are gone is
a lowering. `skills/settle/SKILL.md` §3 gives the three answers.
Enforced by: tests/test_settle_reads_before_it_removes.py::test_the_skill_names_the_floors_a_fold_has_to_answer

<!-- specs/1790138190-settle-leaves-twelve-directories-with-no-way-out -->
**A `seal/` root with no work item under it is the state a complete fold ends
in, and it reads as settled, never as unusable.** Git keeps no empty
directory, so the state is two: the tree that ran `settle --retire` holds an
empty `seal/specs/`, and a fresh checkout of that commit holds none. Read as
unusable, `settle` exited 2 on its own finished work, and `unverified-check
--baseline` read the root's own `specs` path as a typo, which would turn every
pull request after a complete fold red, the shipped `templates/hygiene.yml`
included. Only that one path is settled; any other missing path is still
refused, which keeps a misspelt path from passing in silence.
Enforced by: tests/test_settle_reads_before_it_removes.py::test_a_settled_root_is_green_and_says_so, tests/test_unverified_rows_close.py::test_the_roots_own_specs_path_is_settled_when_nothing_is_under_it

<!-- specs/1790076070-the-fold-ships-and-the-corpus-is-still-on-disk -->
**A fold marker on a line of its own is exempt from the wrap limit.** The
marker is matched whole, so wrapping a long work item id stops it being a fold
record, and `tests/test_docs_line_wrap.py` skips a line that is exactly one
marker rather than asking a document to choose between the two. The chain
checker's reading of a retired declaration is
`docs/the-review-and-parity-arms.md`'s, under *The declaration, and where the
check went instead*.
Enforced by: tests/test_docs_line_wrap.py::test_a_fold_marker_is_skipped_and_the_line_beside_it_is_not
