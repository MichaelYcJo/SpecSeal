# The pact — one contract kept by several repositories

Some work items commit in more than one repository, and some of those
repositories keep a contract together: a response shape one serves and
another reads, a field list two of them write. This document is the standing
account of where that contract lives, how each repository knows about it,
and what checks it.

It is a policy document: it outranks the SDD set, and a work item that finds
it wrong corrects it rather than working around it.

## The words

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**The pact is the one copy of what two or more repositories keep together,
and every repository of such a work item is a signatory, the one holding
the pact included.** The pact is `seal/pact.md` in one of them. That
repository has no noun of its own: it is the pact's repository, identified
by holding the file, and where more than one pact can be meant, a text says
which by naming where it is held. `pact-check` is the command that reads
every signatory from there. The three names are the owner's (#647, given
2026-10-03); the working words of the issue's thread name nothing here, and
a case holds them out of the shipped text.
Enforced by: tests/test_one_word_one_meaning.py::test_the_pacts_words_keep_one_meaning, tests/test_a_signatory_declares_its_pact.py::test_the_routing_step_mints_one_id_and_declares_only_in_gated_repositories

## When there is a pact at all

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**A sentence is contract when another repository's code would be wrong if it
changed, and a pact exists only where a work item commits in more than one
repository and those repositories share contract.** The rule is the owner's
(#647, decision 5) and it decides two things: whether the structure exists,
and which sentences go in `seal/pact.md`. A work item that only commits in
several repositories gets a routing declaration in each and nothing else. A
sentence only one repository's code depends on stays in that repository's
own documents, because a pact that collects those sends every signatory to
re-read changes that were never theirs. `templates/pact.md` states the rule
where the file is begun.
Enforced by: tests/test_a_signatory_declares_its_pact.py::test_the_routing_step_mints_one_id_and_declares_only_in_gated_repositories

## One routing answer, one id, every gated repository

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**The routing question is asked once, the work-item id is minted once, and
a declaration goes into every repository the work item commits in that
already has a `seal/` root, and into no other.** The id names the directory
in every repository, so each share's ledger fragment, changelog fragment and
fold marker are keyed alike, and a directory named differently in each would
have to be renamed later, moving all three. A repository with no root is
named in the handback and left alone, because writing into it would create
its root, which is the bootstrap's decision and the person's. Nothing checks
that every share carries one id: an id minted twice cannot be told from a
signatory's own work item that cites the pact without changing it.
`skills/implement/orchestration.md` §*A work item that commits in more than
one repository* is the procedure.
Enforced by: tests/test_a_signatory_declares_its_pact.py::test_the_routing_step_mints_one_id_and_declares_only_in_gated_repositories, tests/test_every_orchestrator_act_names_its_delivery.py::test_every_orchestrator_act_names_its_delivery

## How a signatory names the pact

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**Every signatory but the pact's repository names the pact in a `Pact` row
of its `seal/config.md`, and says in `Pact notify` what it asks to be told,
and one reader answers both rows for every caller.** `Pact` is the origin
remote URL of the pact's repository, several separated by `;`, compared
normalised; its last path segment is the name an anchor carries, so two
pacts ending in one segment are refused. `Pact notify` is `always`,
`when the pact is touched` or `never`, `when the pact is touched` where it
is absent. The value decides which of the signatory's re-reads leave a
record of a pact change (§*A signatory records a pact change*) and which of
those `pact-check` reads. `hooks/config.py#pact_declaration` refuses
what will not parse in a sentence and stops nothing, so the print at a
signatory's pull request and the refusal at the pact's repository are about
the same rows.
Enforced by: tests/test_a_signatory_declares_its_pact.py::test_one_pact_reads_normalised_with_the_default_notify, tests/test_a_signatory_declares_its_pact.py::test_a_notify_value_outside_the_vocabulary_is_refused_naming_all_three, tests/test_a_signatory_declares_its_pact.py::test_a_row_that_will_not_parse_is_refused_and_never_read_as_absent, tests/test_a_signatory_records_a_pact_change.py::test_s10_notify_decides_what_is_recorded

## The pact anchor

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**A signatory cites a clause as `pact:<name>/"<heading path>"@<hash>`, and
its own evidence check reads past it.** Every `##` heading of
`seal/pact.md` below its `| Signatory |` table is a clause, and a `###`
narrows inside one. The hash is the content hash `evidence-check` gives the
clause's region, the value a local coordinate to that heading carries. A
signatory writes the anchor in a spec's Grounding, recording what the work
was built against, and in a ledger row's `Clause` cell beside its own code
coordinate, which is the link that outlives `settle`. No coordinate pattern
of the signatory's checker matches inside the anchor, and the readers that
blank coordinates before reading a line another way blank pact anchors
first, so a version in a clause heading is never an old-format coordinate
there.
Enforced by: tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py::test_no_coordinate_pattern_matches_inside_a_pact_anchor, tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py::test_a_pact_anchor_in_the_clause_cell_leaves_the_local_coordinate_alone, tests/test_a_pact_anchor_is_no_coordinate_of_the_signatory.py::test_migrate_leaves_a_pact_anchor_alone

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**A token begins a pact anchor where `pact:<name>` is followed at once by
`/` or `#`, or by the rest of an anchor with its `/` missing, and
`pact-check` refuses a token that begins one and does not go on to parse.**
The rest of an anchor is a quoted heading path closed by `@`, or `@` and a
hash, at once or after one mark or one space, so the commonest typos are
named rather than read by nobody. Anything else naming the pact is a
mention and is left alone: `pact:<name>` followed by punctuation, a space or
the end of a code span. The one form that begins an anchor and is not an
attempt is the one this plugin prints to show the shape, its heading path a
placeholder, `/"<heading path>"`. So `pact:<name>/` written in prose is
refused, and the refusal names both ways out: quote the heading path and
give it a hash, or, where the text shows the shape rather than citing a
clause, put it in a fenced code block, which nothing reads.
Enforced by: tests/test_pact_check.py::test_an_anchor_missing_its_slash_is_refused, tests/test_pact_check.py::test_the_refusal_names_both_remedies, tests/test_pact_check.py::test_prose_naming_the_pact_is_not_a_citation, tests/test_pact_check.py::test_a_pact_anchor_that_does_not_parse_is_refused

## A signatory records a pact change

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**When a signatory's `evidence-check --reverify` moves the hash of a ledger
row that cites a clause of a pact its `Pact` row declares, or leaves a
coordinate of one BROKEN, the same command records a pact change, and that
test is the whole trigger.** It needs no judgment: a row carrying a pact
anchor and a local coordinate is the link, and a re-read is the one act at
which a session says code under a row moved. The record is written in both
of the re-read's forms, a re-stamp in place and a `Re-read ·` row under
`--into`, before the hash it read is gone, one row per ledger row. `Pact
notify` decides what is recorded: `when the pact is touched` records rows
citing a clause of a declared pact, `always` also records every other row
whose code moved, with `—` for its clause, and `never` records nothing. The
work item the record is named for is the `--into` fragment's, else the one a
`routing.md` declares for the branch; with neither, nothing is recorded, the
row is named on a `LEFT` line with both ways to name one, and the exit is 1.
Where the record is written, the ledger is written exactly as it would be
without it. **Where a change is owed and cannot be recorded, nothing is
re-stamped either**: no work item, a record that will not read or parse,
`Pact` rows that will not read, a copy of the checker with no `hooks/`, or a
run that dies part way. Every ledger file the run wrote is put back byte for
byte, because the re-stamp is what clears the drift, and a re-stamp without
its record would leave the next run nothing to record.
Enforced by: tests/test_a_signatory_records_a_pact_change.py::test_s7_a_drifted_row_citing_a_clause_is_recorded, tests/test_a_signatory_records_a_pact_change.py::test_s8_a_released_row_drifted_is_recorded_beside_its_reread, tests/test_a_signatory_records_a_pact_change.py::test_s9_a_declared_branch_names_the_record, tests/test_a_signatory_records_a_pact_change.py::test_s9_with_no_work_item_nothing_is_recorded_and_the_row_is_left, tests/test_a_signatory_records_a_pact_change.py::test_s7_the_ledger_is_written_exactly_as_before, tests/test_a_signatory_records_a_pact_change.py::test_a_change_left_is_recorded_by_the_remedy_it_names, tests/test_a_signatory_records_a_pact_change.py::test_a_pact_row_that_will_not_read_leaves_the_row, tests/test_a_signatory_records_a_pact_change.py::test_under_the_freeze_the_reread_row_is_taken_back_too

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**The record is `seal/pact-changes/<work-item-id>.md` directly under the
signatory's `seal/`, permanent, one file per work item, never folded and
never edited by hand.** It outlives its work item, so it cannot sit in
`seal/specs/<id>/`, which `settle --retire` removes, and one file per work
item keeps two branches from appending to one file. Each row names the
clause as the ledger row cites it, the ledger row, what moved (each
coordinate from its recorded hash to its current one, or `BROKEN`) and the
date; the file's name says why, through that work item's `spec.md`. A row
already in the file is not appended again, so a second run records nothing
twice, and a record that will not read or parse is named and left, with
nothing appended.
Enforced by: tests/test_a_signatory_records_a_pact_change.py::test_s11_a_broken_coordinate_is_recorded_and_the_row_left, tests/test_a_signatory_records_a_pact_change.py::test_s11_a_second_run_records_nothing_twice, tests/test_a_signatory_records_a_pact_change.py::test_a_record_that_will_not_parse_is_left_and_named

## A signatory's CI prints and verifies nothing

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**At a pull request, `chain-check` prints the pact a signatory names and how
many pact anchors its declared work item cites, and no exit status moves on
anything about the pact.** There is no token for a pull request to read
another repository with (#647, decision 2), so a signatory's CI can see one
side only. It prints the pact's repository, the notify value and the anchor
count, a notice for a row that will not parse or an anchor naming an
undeclared pact, and in the pact's repository how many signatories the pact
lists, and every one of them says that `pact-check` at the pact's repository
is where the reconciliation runs.
Enforced by: tests/test_a_signatorys_ci_prints_its_pact.py::test_a_signatory_prints_its_pact_and_its_exit_status_does_not_move, tests/test_a_signatorys_ci_prints_its_pact.py::test_a_row_that_will_not_parse_is_a_notice_and_never_a_failure, tests/test_a_signatorys_ci_prints_its_pact.py::test_the_pacts_repository_prints_how_many_signatories_it_lists

## `pact-check` reconciles, locally

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**`pact-check`, run at the pact's repository, reads every signatory the pact
lists and says which way each mismatch points.** It finds each checkout
through `~/.claude/specseal/pact-paths.md` or the one sibling directory with
that origin, guessing nothing; refuses a signatory whose config does not
name the pact; and grades every anchor naming the pact. `SUPERSEDED` means
HEAD's own history gave the clause that hash, so the signatory was built
against a replaced clause; `NOT TAKEN` means only another ref did, and names
it, so the pact has not taken the signatory's recorded change; `UNMATCHED`
means no commit did; `BROKEN` means the heading path names no single clause.
Git decides the direction and never decides `OK`. Exit 1 is a mismatch or a
checkout not found, and exit 2 is unusable input, the classes
`evidence-check` keeps.
Enforced by: tests/test_pact_check.py::test_s8_a_hash_from_heads_own_history_is_superseded, tests/test_pact_check.py::test_s9_a_hash_only_another_ref_holds_is_not_taken_and_names_it, tests/test_pact_check.py::test_s10_a_heading_path_that_resolves_to_nothing_is_broken, tests/test_pact_check.py::test_s11_a_relationship_recorded_on_one_side_is_refused, tests/test_pact_check.py::test_s12_a_signatory_citing_the_current_clause_is_clean

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**`pact-check` reads every signatory's records of pact changes, following
that signatory's `Pact notify` as read now, and reports a row citing a
clause of this pact as `NOT TAKEN`, exit 1, until a pact review here takes
it.** This is the second source of `NOT TAKEN` that #735's frame named, and
the report keeps its name. The line names the signatory, the record and its
line, the clause, the work item, and the record's content hash, which is the
value a pact review writes. A `—` row from a signatory whose notify is
`always` is `NOTED`, printed until a pact review takes it and in no exit
class, because a pact review is owed only where a clause is cited (#647's
decision 4). Under `when the pact is touched` a `—` row is not read, and
under `never` no row is. A record that will not read is `UNREADABLE` and one
that will not parse `REFUSED`, both exit 2. The `READ` line and the summary
count the pact changes read and taken.
Enforced by: tests/test_a_pact_review_takes_a_pact_change.py::test_s12_an_untaken_pact_change_is_not_taken, tests/test_a_pact_review_takes_a_pact_change.py::test_s13_a_row_citing_no_clause_is_noted_under_always, tests/test_a_pact_review_takes_a_pact_change.py::test_s13_a_row_citing_no_clause_is_not_read_when_the_pact_is_touched, tests/test_a_pact_review_takes_a_pact_change.py::test_s13_under_never_no_row_is_read, tests/test_a_pact_review_takes_a_pact_change.py::test_s17_a_record_that_will_not_read_or_parse_is_exit_2

## A pact review takes a pact change

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**A pact review is an ordinary work item at the pact's repository, opened
when `pact-check` reports a `NOT TAKEN` from a pact change, and it takes a
record by a row of `seal/pact-reviews/<work-item-id>.md` naming the
signatory and the record at its current content hash.** The row's `Change`
is the signatory's work-item id, `@`, and the content hash `pact-check`
printed; its verdict is `holds`, the clause stands and the change keeps it,
or `amended`, this work item amends the clause to take the change. The
builder judges each change against its clause in the signatory's checkout,
and the review chain's warden verifies those judgments there; where the
routing answer skips the review chain, the builder's judgment is the whole
pact review. The record is begun from `templates/pact-review.md`.
`skills/implement/orchestration.md` §*A pact review at the pact's
repository* is the procedure.
Enforced by: tests/test_a_pact_review_takes_a_pact_change.py::test_s14_a_pact_review_at_the_current_hash_takes_it, tests/test_a_pact_review_takes_a_pact_change.py::test_s16_amended_is_taken_where_the_clause_moved

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**A record is taken at the content hash a pact review row names and no
other, and a row that cannot be true is refused at exit 2.** A commit SHA is
never the key, because a signatory's feature branch squashes and the SHA
stops resolving. So a record that gains rows after its pact review reads
`NOT TAKEN` again, naming the hash the review took and the hash it holds now,
and a change that keeps its clause can still be taken, which a key on the
clause's own hash would forbid. `pact-check` refuses a row naming a
signatory the pact does not list, a record that signatory does not hold, a
verdict other than the two, a change not written `<work-item-id>@<hash>`,
and `amended` where a clause the record cites still has the hash the record
recorded.
Enforced by: tests/test_a_pact_review_takes_a_pact_change.py::test_s15_a_record_grown_after_its_review_is_not_taken_again, tests/test_a_pact_review_takes_a_pact_change.py::test_s16_a_pact_review_row_that_cannot_be_true_is_refused, tests/test_a_pact_review_takes_a_pact_change.py::test_s17_a_review_that_will_not_read_or_parse_is_exit_2

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**A clause the pact's repository changes owes no pact review.** `SUPERSEDED`
already sends every signatory citing the clause to re-read it against its
own code and re-anchor, which is checked where that code is, and nothing on
a pull request can see which signatories cite a clause (#647's decision 2).
A pact review answers the other direction alone: a signatory's code moved
under a clause it cites.
Enforced by: tests/test_pact_check.py::test_s8_a_hash_from_heads_own_history_is_superseded

## What this does not see

<!-- specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it -->
**A pact whose history was squashed, or that lives under the git directory,
reads every old version as `UNMATCHED`, and a renamed heading breaks every
anchor to it.** A repository that squashes its pact edits loses the
intermediate clauses, so a signatory built against one reads `UNMATCHED`
where `SUPERSEDED` was true; both are exit 1 and both say to read the two
sides, so the reading degrades without going quiet. A pact under local mode
has no history at all, and `pact-check` says so in its summary. A clause's
heading is its address, so rewording the prose is a change every citing
signatory re-reads, and renaming the heading is one each of them has to
re-coordinate. And `pact-check` runs where a person runs it: nothing on a
pull request reconciles anything.
Enforced by: tests/test_pact_check.py::test_a_pact_under_local_mode_has_no_history_and_says_so, tests/test_pact_check.py::test_s10_a_hash_no_commit_gave_is_unmatched

<!-- specs/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed -->
**A hash edited by hand bypasses the writer, a vendored copy of
`evidence_check.py` records nothing, and a pact under local mode keeps its
pact reviews on one machine.** The record is written inside `--reverify`, so
a signatory that types a new hash into a ledger row leaves no pact change,
and nothing can see that it should have. A copy of the checker with no
`hooks/` beside it cannot read the `Pact` row; it names each row citing a
pact, says it recorded nothing, and re-stamps nothing, so the plugin's own
checker records the change where the signatory is checked out. A pact under
local mode keeps
`seal/pact-reviews/` under the git directory, so another clone of the pact's
repository reads the same changes as `NOT TAKEN`, which is loud in the right
direction.
Enforced by: tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_says_it_recorded_nothing
