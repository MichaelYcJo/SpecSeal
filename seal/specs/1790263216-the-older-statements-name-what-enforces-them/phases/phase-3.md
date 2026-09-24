# 1790263216-the-older-statements-name-what-enforces-them — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 03265a16 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`docs/review-chain-spec.md` (9 statements, 2 bold openings) and
`docs/commit-review-gate-spec.md` (8 statements, 4 bold openings): the review
cycle and the commit gate, read together because the second was split out of
the first (#526). `review-chain-spec.md` stays at or under 963 lines.

## What this phase found

The format is phase 1's.

| # | Statement | Rule | Breaking edit | Target | Seen |
|---|---|---|---|---|---|
| D33 | review-chain §The cap bounds rounds · `1790076060` | three and five count rounds; a capped run may still write a fix, and ownership decides | the owner's sentence, or a carrier's link to it, dropped | `test_the_owner_states_the_rule` (rule 13), `test_every_link_names_the_owner` **Corrected in round 1's fix pass:** rule 13 pins the statement's third bold sentence and not its opening, so the line now says `nothing — no case reads the opening yet`. | read: rule 13 pins *What decides between a fix and a home is who owns the unit now* and seven carriers' links |
| D34 | same § · `1790076060` | two bounds end a run `capped`, and only the round cap permits a fix | `chain_check` accepting a second fix-closing record after a floor `no` | `test_a_second_fix_closing_record_after_the_floor_is_refused`, `test_a_capped_run_has_a_legal_end` | read |
| D35 | §The floor · `1788472135` | the floor row is read on every record | `chain_check` passing a record with no floor row; a run going past its stop | `test_a_record_without_the_floor_row_fails`, `test_three_quiet_rounds_after_the_floor_are_still_refused` | read |
| D36 | §Where a leftover goes · `1790076060` | a finding is filed where somebody will act on it | the headline sentence reworded, or a carrier's link to it dropped | `test_the_owner_states_the_rule` (rule 14), `test_every_link_names_the_owner` | mutated (M12) |
| D37 | same § · `1790076060` | two refusal messages lag the ladder | — | nothing (case 3): a record of two messages' wording and of a decision left to the owner. The rule they lag is D36's | — |
| D38 | §When the record was written · `1788501054` | a round record is committed before the fixes it commissions | `chain_check` reading the last commit instead of the adding one | `test_a_record_added_after_its_own_fix_fails_after_the_cutoff`, `test_a_record_updated_in_place_when_the_fixes_landed_passes` | read |
| D39 | §The survivor sweep · `1788873640` | `survivor-check` reports every place still carrying removed wording | the report dropping a survivor or the corrected sentence | `test_a_reworded_sentence_reports_the_pin_it_left_behind`, `test_the_report_names_the_sentence_that_was_corrected_too` | read |
| D40 | same § · `1788912166` | a range removing a section whole takes one row, anchored on the range and the work item | a range row excusing every range | `test_a_whole_range_row_excuses_the_survivors_of_that_range`, `test_a_whole_range_row_does_not_reach_a_different_range` | read |
| D41 | same § · `1789211172` | a round record is outside the corpus on both sides | `records_a_past_state` no longer matching a round record | `test_a_record_of_a_past_round_is_not_a_survivor`, `test_a_round_record_the_range_edited_does_not_become_a_source` | mutated (M11) |
| D42 | commit-gate §Which repository · `1788305134` | the repository judged is the one the command commits into | the gate judging the shell's directory | `test_a_commit_aimed_elsewhere_is_judged_there`, `test_a_cd_reaches_the_repository_the_commit_lands_in` | read |
| D43 | same § · `1788184145` | a file edit goes through the `Edit` tool, because the gate reads a body as shell | the instruction dropped from its carriers; the gate skipping a heredoc body | `test_the_rule_names_the_tool_and_pairs_its_two_reasons`, `test_an_interpreter_fed_heredoc_body_that_commits_stops` | read |
| D44 | same § · `1788305134` | a failure branch waits for the operator that runs it | the reader binding `\|\|` only to the segment right before it | `test_a_failure_branch_survives_an_intervening_segment` | read |
| D45 | §Review arm · `1790154759` | the review arm reads no paths | a docs-only or seal-only commit passing the review arm | `test_the_review_arm_asks_on_a_document_only_commit` | read: parametrised over `docs/` and `seal/`, asserts a deny naming `[no-review]` |
| D46 | §The declaration · `1789518345` | the gate reads `routing.md` first | a declared commit asked or denied | `test_a_declared_chain_item_commits_without_a_prompt`, `test_a_declared_direct_item_commits_without_a_prompt` | read |
| D47 | same § · `1789518345` | a retired declaration is not one the pull request made | `chain_check` refusing a declaration `settle --retire` removed | `test_a_declaration_this_branch_retired_is_not_one_it_made`, `test_a_declaration_the_rule_arm_retired_is_not_one_it_made` | read |
| D48 | §review-history-guard · `1788844300` | posting a review with no record reminds; reading a review with one reminds | either reminder dropped | `test_history_guard_reminds_posting_without_record`, `test_history_guard_reminds_reading_with_record` | mutated (M9) |
| D49 | §implementer-mark · `1788310269` | a spawn leaves a mark, and a commit with no mark gets one line | the mark hook writing nothing | `test_spawning_smith_leaves_a_mark`, `test_a_declared_smith_with_no_mark_is_noticed_after_a_commit` | mutated (M10) |

Sixteen decisions name targets, and one says `nothing`, of case 3.

**Mutations, each restored from kept bytes and executed 2026-09-25 on top
of `03265a16`:**

| # | Mutation | Case run | Result |
|---|---|---|---|
| M9 | the posting branch of `hooks/review-history-guard.py` never prints | `test_history_guard_reminds_posting_without_record` | red, 1 failed |
| M10 | `hooks/implementer-mark.py` never calls `implementer.write` | `test_spawning_smith_leaves_a_mark` | red, 1 failed |
| M11 | `records_a_past_state` skips its round-record branch | `test_a_record_of_a_past_round_is_not_a_survivor` | red, 1 failed |
| M12 | the ladder's headline sentence reworded in `docs/review-chain-spec.md` | `test_the_owner_states_the_rule` | red, 1 of 6 parametrised cases |

**The six bold openings.**

- Three bold an existing sentence where it already stood first: D42's, whose
  inner `**into**` became `*into*` so the bold does not nest, and D46's.
- D35 swaps its first two sentences, so that *The row is read on every
  record* opens the statement. The words are unchanged.
- Three have no sentence stating the rule, only a table, so one restating
  sentence was written. D38 restates its heading. D48 restates the
  reminder table. D49 restates the two-hook table: a `framer` or `smith`
  spawn leaves a mark, and a commit on a branch whose declaration names that
  agent, with none standing, gets one line.
- No ledger anchor quotes any of these lines.

**What D33's pin holds, and what it does not.** Rule 13 pins the third bold
sentence of the statement and seven carriers' links to the section. It does
not pin *Three and five count rounds*. A carrier that links the owner and
also says the opposite passes, and `test_the_rules_have_one_owner.py` says
so beside rule 14. The pin is still what catches the edit this rule is
about: a session reads the rule through its carriers, and the pin is what
keeps the owner's wording and the links in place.

**The overview was missing, and a case read it.** Phase 3's test set
included `test_chain_hooks_hardening.py`, whose
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` failed
because this work item has a `spec.md` and no `overview.md`. Phases 1 and 2
did not run that module, since it reads neither of their documents. The
overview was written in this phase with its first two sections filled, and
the module passed on the re-run. It is completed as the phases close.

**What the common checks returned** (executed 2026-09-25):

- `bin/fold-check --shape-from 0` went from 107 problem lines to 84: 17
  missing lines and 6 bold openings. **66 statements remain.**
- `bin/fold-check` exits 0. `review-chain-spec.md` is 960 lines, under its
  963 budget. `commit-review-gate-spec.md` is 568.
- `bin/evidence-check .` named five drifted anchors. The rows are 0.13.1's
  C1, C3 and C4, 0.14.0's G4, 0.4.0's opt-in-headings row, and 0.8.0's F1.
  Each was re-read, noted `Re-read 2026-09-25` and re-stamped in its file.
  The note on 0.4.0's row drifted one more row: 0.13.1's row anchored on
  the 0.4.0 section itself. It was re-read, noted and re-stamped in a
  second pass, the same two-pass shape its earlier notes describe. The run
  after that is 2089 ok, 0 drifted.
- 42 modules ran in one command. The first run had one failure, the
  overview case above. On the re-run of the two modules that read
  overviews, 202 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
