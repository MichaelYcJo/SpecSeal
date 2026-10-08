# 1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | aae8f2bd |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The documents (`spec.md` D7): a new section in `docs/the-evidence-ledger.md`,
placed after §*A released row is read again in the branch's fragment* and
before §*What the checker refuses*, stating D1–D5 with `Enforced by:` lines
naming phases 1–3's cases; `templates/ledger.md` showing both row forms;
`skills/evidence-check/SKILL.md` §*Verdicts and what to do* and §*Re-verifying
is recomputing the hash*; `skills/evidence-ci/SKILL.md` §*Updating later*. A
pin per changed sentence, each seen red with its sentence removed, and the
text hygiene modules green.

## What this phase found

**The new section is `## A claim held by a test`, five marked statements.**
Each opens bold and carries one `Enforced by:` line under the marker
`<!-- specs/1791384153-a-ledger-rows-claim-is-the-test-that-enforces-it -->`,
the shape `docs/the-pact.md`'s #756 statements were written in by their own
work item. `bin/fold-check` reads 176 statements where it read 171 and binds
every one, exit 0. The two neighbouring sections' regions are unchanged:
the section ends the released-row section at its own heading, and the next
section starts where it did.

**D6 got a statement of its own** — "`path::name` has one resolver" —
which `spec.md` D7 does not list among D1–D5. The resolver is a rule a
reader of `fold-check` meets as much as a reader of the ledger, and its
`Enforced by:` line names phase 3's cases.

**`skills/evidence-ci/SKILL.md` names no version.**
`tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one`
refused the first draft's *from SpecSeal 0.21.0 on*: a loaded file naming
the release it ships in goes red on that release's own preparation commit.
The sentence names the function a copy must carry, `held_by_tests`, instead.

**The template shows the two forms in a fenced block**, so neither example
row is read as a claim (`docs/the-evidence-ledger.md` §*A row inside a fence
is an example*), and its header stays the one `LEDGER_COLUMNS` is pinned
against.

**Seen red (§15):** the eleven pinned sentences of
`test_the_documents_state_the_test_row` were each broken through
`bin/mutation-check` against aae8f2bd, one word apiece, and every one went
red.

Executed, output read: the new module, 48 passed; `bin/fold-check`, exit 0;
`test_docs_line_wrap`, `test_a_shrunken_corpus_declines_to_judge`,
`test_a_rider_reaches_its_file`, `test_every_reader_ends_a_line_where_gfm_does`,
`test_one_word_one_meaning`, `test_no_real_identifiers`,
`test_a_record_states_what_the_tree_has`, `test_release_hygiene`,
`test_a_row_wider_than_its_header_is_named`,
`test_a_document_has_room_for_the_next_fold`,
`test_both_editions_carry_the_same_folds` and
`test_the_ledger_rules_have_one_home`, green after the version sentence was
rewritten (the first run: 1 failed, 534 passed, the failure above).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
