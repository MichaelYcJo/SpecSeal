<!-- seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md

What this work item settled by opening code, one row per claim. The release
that ships it folds this file into `seal/ledger.md` and removes it.

**T1 carries a claim forward from a row this branch removed.** `seal/ledger.md`
carried R2 under `1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency`:
*`size: now` is defined where labels are defined, in the prefix form, in two
states, and **nothing reads it***. The last conjunct stopped being true here —
`close-issues-on-release.yml` reads the label, and only to take a spent one off
the issue it is closing — so the row was REMOVED there rather than re-pointed,
which `CLAUDE.md` §*A change writes fragments* and §*Appended is the word, and
a removal is not one* between them license, and the corrected claim is written
here against the coordinates that carry it now. Both of R2's anchors still
resolve; what failed was the claim, not the anchor, and a row whose claim has
gone false is not one to re-stamp.

R2's own Notes said the gap out loud: *nothing pins the label against the
tracker — a label that is never created, or created under a different
spelling, leaves the document describing something absent, and no check can
see that.* T2 is that gap closed from the only side a check can reach: the
declaration and the document are held together in the tree, and the workflow
is what carries the declaration to the tracker.

**What deliberately has no row.** The release-note workflow (phase 1) and the
directory command (phase 3) are new mechanism whose whole behaviour is pinned
by their own modules, case for case; a row per arm would be an inventory of
the diff. What earns a row here is a judgment a later tidy-up would undo in
good faith — a delegation that looks like indirection, an invariant that
looks like it was simply relaxed, and a claim about a document that a reader
cannot check without the tracker in front of them.

Every hash here was stamped by `evidence-check --reverify --ledger '<this
fragment>'`, the scoped WRITE form, never by an unscoped run. -->

| Clause | Code grounds | Verified behavior | Checked | Notes |
|---|---|---|---|---|
| T1 · `size: now` is still defined where labels are defined, in the prefix form and in two states, and **one thing reads it — only to spend it**. No workflow, no check and no script reads it to decide what happens next; `close-issues-on-release.yml` removes it from each issue it closes, after the close rather than before | `docs/issues-and-milestones.md#"## A label answers *what it is about*, and survives the move"@3a50630a`, `.github/scripts/close_issues_on_release.py#main@419b5454`, `.github/scripts/close_issues_on_release.py#drop_label@f50fccb5`, `.github/scripts/close_issues_on_release.py#spend_label@dfb24ccf`, `tests/test_a_release_is_sized_by_a_criterion.py#test_the_label_is_two_states_and_nothing_schedules_from_it@1d7b8fbe`, `tests/test_a_declared_label_reaches_the_tracker.py#test_the_close_comes_first_so_a_failed_label_write_cannot_cost_it@475ab90c` | **Executed** 2026-09-22. The reworded sentence's literal was moved in the same commit and the case re-run green; deleting either half of the new sentence reds it. The ordering case asserts the close's index in the recorded call list precedes the label edit's, rather than asserting both happened — both succeeding says nothing about which survives the other failing — and the refusing-tracker case leaves the issue closed with `could not remove … closed either way` on stdout | 2026-09-22 | **This replaces `seal/ledger.md`'s R2**, whose final conjunct this work falsified. The ordering is the part a later tidy-up undoes in good faith: reading the two writes as one act invites putting the cheaper one first. An issue that closed and kept a stale label is a wrong answer on a tracker; an issue left open because a label write failed is a release that did not finish, and only the second is unrecoverable without a person. That asymmetry is why `drop_label` is the one place this script does not fail loudly, against a docstring three paragraphs long about why it otherwise does. **Re-anchored 2026-09-22 in round 1's fix pass (finding 4)**: the case this row cites was named `…_and_nothing_reads_it` while its body asserted that one thing does read it, so the coordinate a reader opens to check this claim was named for the claim's negation. The case is `…_and_nothing_schedules_from_it` now and the anchor follows it; nothing about the claim changed |
| T2 · a label a document specifies is reconciled onto the tracker by the workflow that already runs when `main` moves, and the declaration names the document that specifies each | `.github/scripts/tracker_labels.py#LABELS@e00775d9`, `.github/scripts/tracker_labels.py#missing@37ed496e`, `.github/workflows/close-issues-on-release.yml#"- name: create the labels the documents specify and the tracker lacks"@e4b83795`, `tests/test_a_declared_label_reaches_the_tracker.py#test_a_missing_label_is_created_with_the_documents_own_sentence@5bab8784`, `tests/test_a_declared_label_reaches_the_tracker.py#test_reconciling_an_already_complete_tracker_writes_nothing@3cf690f5` | **Executed** 2026-09-22 over a fake tracker: a missing label produces exactly one `gh label create` carrying the document's own sentence, and a complete tracker produces no write at all. **Read** 2026-09-22: `gh label list` on the live tracker still does not list `size: now`, which reproduces #450's 2026-09-20 measurement — the label has never existed and the specifying section has described an absent object since 0.11.1 | 2026-09-22 | **The act was a person's, and that is what made it invisible.** The work item that wrote the section ended its changelog entry with *creating the label and applying it are the repository owner's, after this merges*; a person has no queue this repository can read, so three releases were cut with nothing anywhere to notice. The `specified_by` field is the part that looks droppable: it is never read by code and never printed except in the missing-label report, and without it this file is a copy of a decision whose original a reader cannot find. A gate for a missing label was rejected rather than forgotten — it would be red on the very branch that adds one, since no agent in this repository's chain may write to the tracker, and it would grow `broad_gate.py`'s partition as well |
| T3 · an issue's labels are read in one place, by the module that owns the 404-tolerant read they are built on, and the sibling delegates | `.github/scripts/close_issues_on_release.py#issue_labels@1c7a1dce`, `.github/scripts/label_merged_on_release_branch.py#issue_labels@7afd8565`, `tests/test_a_declared_label_reaches_the_tracker.py#test_the_label_reader_has_one_source@a549f867` | **Executed** 2026-09-22: `tests/test_a_merged_ticket_says_so_on_the_tracker.py` re-run green unchanged, which is the load-bearing half — its fixtures monkeypatch `closer._issue_api`, and the delegation still reaches that patch, so the sibling's whole suite is a control on the move | 2026-09-22 | The reader lived in the sibling while the sibling was its only caller, reaching for `closer._issue_api` with a docstring explaining that reaching for a private name was deliberate. The closing script then needed the same read, and two near-identical readers is the exact thing that script's own docstring says it exists not to have. **The case pins the CALL, not the word**: a first version asserted `_issue_api` appeared nowhere in the sibling and went red on the docstring sentence explaining the history, which would have made recording why the move happened the thing that fails |
