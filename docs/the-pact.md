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
is absent. Nothing acts on that value until the record of a pact change
exists, which is #647's next step, and it is read and printed now so the row
has a reader from the first day. `hooks/config.py#pact_declaration` refuses
what will not parse in a sentence and stops nothing, so the print at a
signatory's pull request and the refusal at the pact's repository are about
the same rows.
Enforced by: tests/test_a_signatory_declares_its_pact.py::test_one_pact_reads_normalised_with_the_default_notify, tests/test_a_signatory_declares_its_pact.py::test_a_notify_value_outside_the_vocabulary_is_refused_naming_all_three, tests/test_a_signatory_declares_its_pact.py::test_a_row_that_will_not_parse_is_refused_and_never_read_as_absent

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
