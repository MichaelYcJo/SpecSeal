# 1790263216-the-older-statements-name-what-enforces-them — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 4856c2cf |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

`docs/issues-and-milestones.md` (5 statements, 3 bold openings),
`docs/worktree-guard-spec.md` (2, 2 bold) and `docs/one-root-by-lifetime.md`
with its `.ko.md` edition (9 and 9, 3 bold each). The editions test was to
compare `Enforced by:` values (`spec.md` §*Scope* item 4). The Korean lines
copy the English targets byte for byte, and a `nothing` reason is written in
Korean. The new case was to be shown red first, with a planted pair whose
targets differ, and the real-tree case was to pass.

## What this phase found

The format is phase 1's. The nine Korean statements are D107–D115. Each
carries the same target as the English statement in the same row, D98–D106,
so each pair is listed once and not repeated.

| # | Statement | Rule | Breaking edit | Target | Seen |
|---|---|---|---|---|---|
| D91 | issues §A milestone · `1789172128` | a milestone answers *when*, and a release is sized by what has to be in effect next | the criterion sentence dropped, or a second document stating a release's size | `test_the_rule_states_the_criterion_and_not_the_count`, `test_one_document_states_a_releases_size` | read |
| D92 | issues §A label · `1788661274`, `1788486395` | `flow-measurement` has exactly one open issue, rolled only when a version shipped | a roll that guesses between two open logs; a roll on a push that shipped nothing | `test_two_open_issues_fails_loudly_without_retrying`, `test_a_push_that_shipped_no_new_version_rolls_nothing` | read |
| D93 | same § · `1788844200` | a rolling log is titled after the version it rolled from | the roll writing a title its next run cannot read | `test_the_title_the_roll_writes_is_the_title_the_next_roll_reads`, `test_rolled_from_reads_only_the_title_the_roll_itself_writes` | read |
| D94 | issues §A label says a ticket is already in · `1789108681` | a claimed issue carries `merged: X.Y.Z` before the release ships | the script labelling nothing, or labelling on another trigger | `test_it_labels_the_issue_the_keyword_named_and_nothing_else`, `test_the_trigger_is_a_push_to_a_release_branch_and_nothing_else` | read |
| D95 | issues §A keyword · `1788844400` | a closing keyword claims the one number after it | the checker not warning on *Closes #1 and #2* | `test_the_sentence_that_lost_an_issue`, `test_the_two_lists_say_what_closes_and_what_does_not` | read |
| D96 | worktree §Creation consent · `1788817291` | the first creation in a session is the question, and a later one is allowed | every creation asked, or the first one allowed | `test_the_first_creation_is_still_a_question`, `test_a_second_creation_in_the_same_session_is_allowed` | read |
| D97 | worktree §Activity · `1788846800` | a session is active on any signal within the idle window | an active transcript event not counted; background agents not scanned | `test_fresh_active_event_counts`, `test_transcript_scan_reaches_background_agents` | read |
| D98 / D107 | one-root §The change in four lines · `1788331011` | one root the plugin owns holds everything | a shipped document naming an old root; the old directory read as an opt-in | `test_no_shipped_document_names_the_old_roots`, `test_the_legacy_directory_is_not_an_opt_in` | read |
| D99 / D108 | §The opt-in signal · `1788817289` | a repository is opted in when `seal/` exists at its mode's location | the shared root not winning, or the git directory not read second | `test_new_home_opts_in`, `test_the_git_directory_is_the_second_place`, `test_the_shared_root_wins_when_both_exist` | mutated (M21) |
| D100 / D109 | §What first setup asks · `1788354065` | the one moment a question is allowed is first setup | a repository with a root asked again; the two options reordered | `test_a_repository_with_the_root_at_either_place_is_never_asked`, `test_the_two_options_are_named_in_order_with_shared_as_the_default` | read |
| D101 / D110 | §Shared or local · `1788411058`, `1788398967` | the mode question is whether CI and collaborators see the workflow | an option that does not say what it creates and installs; a local root that could be committed | `test_each_option_says_what_it_creates_and_what_it_installs`, `test_the_local_root_is_never_a_commit_candidate_and_needs_no_gitignore` | read |
| D102 / D111 | §What the repository decides · `1788420761` | a setting nobody can find is one nobody has | a template row the config skill does not name | `test_the_skill_names_every_row_the_template_ships`, `test_the_skill_shows_rows_that_are_absent` | read |
| D103 / D112 | same § · `1788360817` | the language is the repository's answer | the skill fixing a language instead of naming the row | `test_the_skill_names_the_file_and_the_row`, `test_the_mirror_is_named_for_its_own_language` | read |
| D104 / D113 | same § · `1788420760` | two language rows, because one cannot say the middle | the template losing `Record language`; a document naming a row that does not ship | `test_the_template_is_one_item_value_table_whose_first_row_is_the_language`, `test_every_document_that_names_a_language_row_names_the_shipped_one` | read |
| D105 / D114 | same § · `1789598366` | an escaped pipe is content, and an unparseable line is named | the reader stopping at a piped row; an unparseable line ending the table silently | `test_an_escaped_pipe_is_one_row_and_the_rows_below_it_still_arrive`, `test_a_line_that_will_not_parse_is_named_and_the_hook_still_says_nothing` | read |
| D106 / D115 | same § · `1788789329` | a git call that fails is not one that answered nothing | an unreadable remote exported or imported as *no remote* | `test_the_export_omits_a_remote_it_could_not_read`, `test_an_unreadable_remote_here_refuses_the_import`, `test_a_git_that_cannot_answer_does_not_report_no_submodule` | read |

All 25 lines name targets. This phase has no `nothing` line, so no Korean
reason was needed.

**Mutations, each restored from kept bytes and executed 2026-09-25 on top
of `65153457`:**

| # | Mutation | Case run | Result |
|---|---|---|---|
| M19 | the Korean edition's D108 line narrowed to its first target | `test_every_paired_document_carries_the_same_folds_under_the_same_headings` | red, 1 failed |
| M20 | `enforcement` skips every line | `test_an_enforced_by_line_naming_other_targets_is_named` | red, 1 failed |
| M21 | `hooks/optin.py#home_at` asks the local root before the shared one | `test_the_shared_root_wins_when_both_exist` | red, 1 failed |

**The editions comparison (§15).** The three planted cases were written
first and run against `disagreements` without the comparison: 3 failed and
8 passed. With the comparison they pass, and so does the real-tree case over
`one-root-by-lifetime`. M19 is the real-tree case red on a Korean line that
names fewer targets than its English statement.

`enforcement` pairs a statement by heading position and marker ids, the two
keys `outline` already compares. It reads the span and the
targets-or-`nothing` value through `fold_check.py#numbered_statements` and
`#names_targets`, so it has no second spelling of the shape. Its row is E1
in this work item's fragment. 0.14.0's E1 row, which anchors
`disagreements`, was re-read and noted as widened rather than false.

**The eight bold openings.**

- D91's statement opens with a table, so its bold sentence sits on the line
  before the table. It restates the heading and the section's criterion in
  the one document the sizing sweep allows to state it.
- D94, D95 and D96 had no rule sentence first, so each gained one that
  restates the heading.
- D97 bolds its existing first line.
- D98 moves its rule sentence (*After this change one root the plugin owns
  holds everything …*) first. D100 and D101 bold their existing first
  sentences.
- The Korean D107, D109 and D110 do the same with their own sentences.

**`CONTRIBUTING.md`'s pairing sentence is now narrower than the check.** It
says the editions carry *the same heading levels and, under each heading
position, the same fold markers*, and a ledger row quotes that line. It is
not false, so it was not touched. It no longer names everything the case
compares, and the overview's *Not done* records it.

**What the common checks returned** (executed 2026-09-25):

- `bin/fold-check --shape-from 0` **exits 0** and reads 136 statements, of
  which the cutoff `0` binds 136. **0 statements remain.**
- `bin/fold-check` exits 0.
- `bin/evidence-check .` named seven drifted anchors, across eight rows:
  - 0.11.1's R1 and R3;
  - 0.13.1's T1 and C5;
  - 0.8.2's G5;
  - 0.9.2's S4;
  - 0.14.0's E1, on two of its anchors;
  - 0.5.0's S12.

  Each was re-read and noted `Re-read 2026-09-25` by a script that asserts
  the row's line and tail, and each file was re-stamped with `--reverify`.
  With the fragment in place this work item's records are now read: 2 work
  items, 253 names, 0 refused. The run is 2094 ok, 0 drifted.
- 37 modules ran in one command: 1745 passed, 1 skipped.
- `uvx ruff check` and `uvx ruff format --check` passed on the changed test
  module.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
