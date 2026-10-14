# 1791934661-every-doc-states-the-current-rule-only — phase 8

| Field | Value |
|---|---|
| Phase | 8 |
| Commit | the commit that adds this record, which `plan.md`'s Status cell names; the rewrite is `7900b60e` and `e5567941`, and the budget rows below are written at the rebase |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

Rewrite `docs/branch-and-release.md` (≤ 15,000 B), `docs/release-checklist.md`
(≤ 11,000 B) and `docs/issues-and-milestones.md` (≤ 13,000 B) to the current
rule only, keeping the merge-method needle `CLAUDE.md`'s repo rule and its pins
read. The same rule census as phases 1 and 6, with one-line summaries of what
left; no ledger rows and no `survivors.md` rows, the drifted released rows
listed by count only; `seal/budgets.md` and every checker untouched. The rules
are `not exercisable` by agent cases, so no eval runs.

## What this phase found

**Before and after** (`measure.py`, `executed`, at `5c7d5e21` and `e5567941`;
`wc -lc` agrees).

| Measure | `branch-and-release` | `release-checklist` | `issues-and-milestones` |
|---|---|---|---|
| Bytes | 27,016 → 14,508 | 27,564 → 10,992 | 25,081 → 11,903 |
| Lines | 442 → 249 | 451 → 206 | 407 → 207 |
| History lines, #930 marks · widened | 11 · 9 → 0 · 0 | 11 · 9 → 0 · 0 | 8 · 7 → 0 · 0 |
| Bold-led paragraphs · over 8 lines | 28 · 10 → 26 · 2 | 12 · 5 → 12 · 0 | 26 · 8 → 31 · 2 |
| Lines in paragraphs that open with no rule | 113 → 26 | 223 → 62 | 113 → 5 |
| Headings · fold markers · `Enforced by:` lines | kept, the targets unchanged | kept, the targets unchanged | kept, the targets unchanged |
| Pin modules (literals found verbatim) | 17 (64) → 17 (63) | 31 (62) → 27 (57) | 15 (42) → 13 (37) |
| `BASELINE` pair with each other | — | 2 runs → 0, entry removed | (the same pair) |

Budget rows owed at the rebase: `bytes:` 14,508, 10,992 and 11,903;
`history:` 0, 0 and 0. The checklist's lines (206) sit over the frame's line
target (200), and its bytes under; the orchestrator's bar was bytes.

**One dated reading stays, and it is a rule's.** The §6 directory box says
*SpecSeal's listing is a Console listing, by the repository owner's reading of
the Console page on 2026-10-07*, because
`test_the_directory_box_records_which_kind_of_listing_it_is_with_a_date`
requires whose reading it is and when, so a reader can tell it has aged. It
counts as a rule line because the box follows the bold *Two acts follow the
tag* paragraph with no blank line between.

**Two quoted-line anchors held.** The 3 released rows on
`docs/branch-and-release.md#"**The fold refuses while a verified fact has not
reached the ledger.** A"` and `#"one `###` section per work item marked with
…,"` still find their line, kept byte for byte, so they drift rather than
break.

**The drifted released rows, by count** (`evidence-check --strict`,
`executed`, exit 2 before and after): 68 more drifted rows than at `5c7d5e21`
(107 → 175) — 13 on `branch-and-release`, 32 on `release-checklist`, 14 on
`issues-and-milestones`, and 9 on the test units this phase edited
(`test_release_hygiene.py#timers_in` 3,
`#test_a_version_below_the_running_one_is_history_and_is_kept` 1,
`test_the_release_seal_is_drawn.py#test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it` 2,
`test_the_contributor_has_a_procedure.py#RELEASE_BRANCH_HISTORY` 1 and
`#test_the_widened_pin_reads_a_file_the_four_surfaces_never_held` 1,
`test_the_rules_claude_md_names_have_one_home.py#RULES` 1) — and one more
broken (6 → 7): the row on
`tests/test_a_release_is_sized_by_a_criterion.py#test_the_two_releases_are_cited_without_a_version_number`,
the case this phase removed. All are #944's.

**Pins.** Seven pin points moved, each seen red through `mutation-check`
(`executed`, seven `red`, the tree clean after each):

| Pin | Change | Seen red by |
|---|---|---|
| `test_release_hygiene.py::test_the_document_says_where_an_issue_actually_closes` | `left no LINK either…` → `leaves no LINK either, though the mention survives`; the `#37`/`#38`/`#39` loop dropped | the old `left` put back |
| `test_the_release_tail_does_not_end_at_the_tag.py#squash_rule` | end marker `**This is enforced, and it was not always.**` → `**Two rulesets enforce the method**` | the marker reworded: both cases red |
| `test_the_release_seal_is_drawn.py::test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it` | `(#718)` and `(#832)` dropped from its two needles | `(#718)` put back; `which the job installs` reworded |
| `test_the_rules_claude_md_names_have_one_home.py#RULES` merge | the hotfix-incident needle → `The last two rows are one rule: **anything reaching \`main\` is a merge commit.**`, found in no carrier | the needle reworded |
| `test_the_contributor_has_a_procedure.py` | the `docs/issues-and-milestones.md` allowance removed with its sentence; the S16 fixture uses the `agents/smith.md` allowance | the fixture's sentence reworded |
| `test_no_passage_is_pasted_into_a_second_file.py#BASELINE` | the issues/checklist entry removed at 0 runs | the labels sentence pasted back into the checklist |
| `test_a_release_is_sized_by_a_criterion.py` | `test_the_two_releases_are_cited_without_a_version_number` removed: it pinned the two releases the criterion was argued from | — (a removal) |

Two docstrings in `test_release_hygiene.py` (`timers_in`,
`test_a_version_below_the_running_one_is_history_and_is_kept`) said the issues
document carries the `release/v0.3.0` sentence; they now say a document can.

**What left, in one summary per file.** `branch-and-release`: the untagged
release, the 310-entry marketplace measurement, the hotfix squash, the three
pull requests whose keywords did not fire, the three-branch changelog
collision, the ledger's growth and `--split`, and the alternative of
collecting numbers into the release body; the checklist's commands are not
restated. `release-checklist`: what each step once caught, the old baseline
footing, the shared checklist, the `.test_durations` recipe (held by
`CONTRIBUTING.md` §*Running the checks*), the #386 and #359 stories, the
release note's and directory's descriptions (held by `branch-and-release`),
the floor and survivor answers a fold owes (held by `skills/settle/SKILL.md`),
and the labels' reason (held by the tracker document).
`issues-and-milestones`: the two releases the criterion was argued from, the
`from-review` share of 2026-09-22, the 0.8.0 and #162 keyword loss, the #266
masking history, the #136 and #30 worked examples, the `release/v0.3.0`
example, and the bare `now` proposal.

**Census: 79 rows over the three files; 77 stand in the new text, one moves to
the file that already holds it, and one leaves with the case that pinned it.**
Every row is `not exercisable — a release
is the session's act; held by` the node ids named, or by no test where it says
so. Several old rules sharing one new paragraph are one row.

| # | Old rule | New coordinate | Exercised by |
|---|---|---|---|
| B1 | *Cutting a release*: two things carry the version, the tag pushed | **Two things carry the version, and a release has both.** | not exercisable — a release is the session's act; held by tests/test_version_check.py |
| B2 | **A release pull request that changes what the plugin ships moves the version.** | unchanged | not exercisable — a release is the session's act; held by tests/test_the_release_check_watches_what_ships.py::test_every_shipping_root_is_watched, tests/test_the_release_check_watches_what_ships.py::test_the_release_document_names_the_same_roots |
| B3 | **Every act the release performs once it reaches `main`…** | unchanged, the three-acts story gone | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_label_acts_are_fired_by_the_merge_to_main_not_the_tag |
| B4 | **The release note publishes itself.** and **Then the release's seal is attached** | the same bullet | not exercisable — a release is the session's act; held by tests/test_a_release_publishes_its_note.py::test_the_workflow_fires_on_the_tag_and_writes_one_release_one_asset_one_edit, tests/test_the_release_seal_is_drawn.py::test_the_release_tail_says_the_seal_is_a_second_act_that_never_fails_it |
| B5 | **The marketplace files are read by a command…** | the same bullet; its exit-0 grounds stand in the checklist §6 box | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_directory_check_reads_the_marketplace_files_and_not_the_directory |
| B6 | **A label a document specifies is created and spent by a workflow.** | the same bullet | not exercisable — a release is the session's act; held by tests/test_a_declared_label_reaches_the_tracker.py::test_the_workflow_runs_the_apply_arm_and_needs_no_new_permission |
| B7 | *Work accumulates*: `main` moves once per release | **`main` moves once per release…** | not exercisable — a release is the session's act; held by tests/test_the_rules_claude_md_names_have_one_home.py::test_each_home_states_its_rule_under_its_section |
| B8 | **Which button, for each direction.** and its table | unchanged | not exercisable — a release is the session's act; held by tests/test_the_rules_claude_md_names_have_one_home.py::test_each_home_states_its_rule_under_its_section, tests/test_the_rules_claude_md_names_have_one_home.py::test_a_restored_copy_is_named |
| B9 | anything reaching `main` is a merge commit | unchanged, the hotfix incident gone | not exercisable — a release is the session's act; held by tests/test_the_rules_claude_md_names_have_one_home.py::test_each_home_states_its_rule_under_its_section |
| B10 | **What breaks when the last row is squashed** | unchanged | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_an_outside_directory_is_in_the_enumeration |
| B11 | **A `# RIDER:` comment's stamp names content…** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_rider_reaches_its_file.py::test_no_rider_stamp_names_a_commit |
| B12 | **A third reader points at those commits now…** | unchanged, the counts gone | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_an_outside_directory_is_in_the_enumeration |
| B13 | **The plugin's name is fixed, and that is not a style question.** | **The plugin's name is fixed.** | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_fixed_name_sentence_sits_beside_it |
| B14 | **This is enforced, and it was not always.** and **What that costs…** | **Two rulesets enforce the method** | not exercisable — a release is the session's act; held by no test — the rulesets are repository settings |
| B15 | the four sequence bullets | the same bullets | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_the_document_says_where_an_issue_actually_closes, tests/test_the_changelog_is_gathered_at_release.py::test_the_documents_send_a_change_to_its_own_fragment |
| B16 | **The changelog entries arrive as fragments…** | unchanged | not exercisable — a release is the session's act; held by tests/test_the_changelog_is_gathered_at_release.py::test_the_release_sequence_names_the_gather_step |
| B17 | a fragment carries no `## ` line; it closes every block | **A fragment carries no line starting `## `**, one paragraph with the closing rule | not exercisable — a release is the session's act; held by tests/test_the_changelog_is_gathered_at_release.py::test_the_documents_say_a_fragment_carries_no_section_line |
| B18 | **The ledger fragments fold in the same commit.** | unchanged; the older-version refusal stands in the checklist §2 statement | not exercisable — a release is the session's act; held by tests/test_the_ledger_fragments_fold_at_release.py::test_the_release_sequence_names_the_fold_beside_the_gather |
| B19 | **The fold refuses while a verified fact has not reached the ledger.** | unchanged | not exercisable — a release is the session's act; held by tests/test_the_ledger_fragments_fold_at_release.py::test_an_open_evidence_todo_row_refuses_the_fold_and_touches_nothing |
| B20 | **The two merge shapes are not interchangeable.** | unchanged | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_the_document_says_where_an_issue_actually_closes |
| B21 | **A closing keyword does nothing when the base is `release/vX.Y.Z`.**, **They left no LINK either…**, **The squash commit message does not carry the keyword either** | one paragraph, **Such a pull request leaves no LINK either…** | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_the_document_says_where_an_issue_actually_closes |
| B22 | **So a workflow reads the keywords instead…**, **A second workflow reads the same keywords earlier…**, only-ever-closes | one paragraph | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_only_a_keyword_before_a_number_closes_anything, tests/test_a_merged_ticket_says_so_on_the_tracker.py::test_the_trigger_is_a_push_to_a_release_branch_and_nothing_else |
| B23 | **One issue the tracker refuses does not leave the rest open.** | unchanged | not exercisable — a release is the session's act; held by tests/test_the_closer_carries_on_past_a_refusal.py |
| B24 | the `Closes #88` example, the repeated keyword, `Part of #N` | unchanged | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_the_document_says_where_an_issue_actually_closes |
| B25 | **The version is provisional…**, **`main` stays the default branch.** | unchanged | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_the_document_says_where_an_issue_actually_closes (the first); no test (the second, a repository setting) |
| C1 | §0 green at the commit that merged | box 1 | not exercisable — a release is the session's act; held by no test |
| C2 | **Squash the work items back to back.**, **Never rebase a work item's branch** | box 2 | not exercisable — a release is the session's act; held by tests/test_unverified_rows_close.py::test_the_documents_state_the_merge_base_footing, tests/test_a_merge_cannot_silently_drop_a_correction.py::test_the_policy_document_owns_the_conflict_and_the_re_read |
| C3 | **The milestone `release: X.Y.Z` holds what this release is actually carrying…** | box 3 | not exercisable — a release is the session's act; held by tests/test_a_release_cannot_ship_an_untrue_milestone.py |
| C4 | no other session in the checkout | box 4 | not exercisable — a release is the session's act; held by no test |
| C5 | **Refresh `.test_durations` now…** | box 5; the recipe is `CONTRIBUTING.md` §*Running the checks*'s | not exercisable — a release is the session's act; held by tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py::test_the_durations_file_prices_the_suite |
| C6 | §1 the preparation branch | unchanged; its ruleset reason is `branch-and-release`'s | not exercisable — a release is the session's act; held by no test |
| C7 | **The preparation commit gathers… and folds…** and the staging | unchanged, one command block | not exercisable — a release is the session's act; held by tests/test_the_ledger_fragments_fold_at_release.py::test_check_fails_while_a_fragment_is_left |
| C8 | **The fold writes the release's own file, and never an older one.** | unchanged | not exercisable — a release is the session's act; held by tests/test_the_ledger_fragments_fold_at_release.py::test_a_fold_into_an_older_release_is_refused_and_writes_nothing |
| C9 | **A second gather for the same version appends into its section.** | **A second gather or fold for the same version joins its section and keeps its date** | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py |
| C10 | **First, the process record. This part is never skipped.** | unchanged | not exercisable — a release is the session's act; held by tests/test_settle_retires_the_process_record.py |
| C11 | **Then the fold.**, **This is a separate branch and a separate pull request from step 2.** | one paragraph | not exercisable — a release is the session's act; held by tests/test_settle_reads_before_it_removes.py::test_the_release_checklist_carries_the_by_hand_step |
| C12 | **A fold is not a work item**, the floor answers and no `survivors.md` row | the first kept; the other two are `skills/settle/SKILL.md`'s | not exercisable — a release is the session's act; held by tests/test_settle_reads_before_it_removes.py::test_the_release_checklist_carries_the_by_hand_step |
| C13 | §3 the whole gate runs here | **The whole gate runs here, every exit code read directly.** | not exercisable — a release is the session's act; held by no test |
| C14 | **A sweep that walks a git listing judges what remains…** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_shrunken_corpus_declines_to_judge.py::test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard |
| C15 | §3's four failure rows | the `evidence-check` row; the timer row is §5's statement; the `chain_check` row a comment on the fetch line | not exercisable — a release is the session's act; held by tests/test_the_ledger_fragments_fold_at_release.py::test_the_checklist_repairs_preparation_drift_the_way_the_freeze_accepts |
| C16 | §4 the `no work item` answer and the title's fragment count | unchanged; the count is the commit placeholder | not exercisable — a release is the session's act; held by tests/test_the_direct_answer_owes_the_sealers_record.py::test_the_release_checklist_names_the_waiver_as_the_no_work_item_answer |
| C17 | **Wait for CI on the pull request head…**, the `gh api` body edit | one box | not exercisable — a release is the session's act; held by no test |
| C18 | §5 merge commit, never squash | *Create a merge commit*; the reason is `branch-and-release`'s | not exercisable — a release is the session's act; held by no test |
| C19 | **The survivor check's unit is a fix pass's range…** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_workflow_step_skips_a_release_range_and_says_why |
| C20 | **A loaded file naming a version at or above the running one is a timer.** | unchanged; the tagged-version grounds are the tracker document's | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one |
| C21 | **A contributor whose base is wrong is told the base is wrong.** | unchanged | not exercisable — a release is the session's act; held by tests/test_the_contributor_has_a_procedure.py::test_the_procedure_is_the_first_section_of_the_guide |
| C22 | §6 tag and describe; **This section used to stop here…** | the command block; **Two acts follow the tag, each a box** | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_two_boxes_follow_the_tag_and_each_carries_its_command |
| C23 | **A GitHub Release exists at `vX.Y.Z`** | the same box; the note's description is `branch-and-release`'s | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_note_box_says_it_confirms_rather_than_performs, tests/test_the_release_seal_is_drawn.py::test_the_checklist_box_says_where_a_missing_seal_is_explained |
| C24 | **The marketplace files and the directory's page have been read** | the same box | not exercisable — a release is the session's act; held by tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_directory_box_says_it_never_fails_a_release, tests/test_the_release_tail_does_not_end_at_the_tag.py::test_the_directory_box_records_which_kind_of_listing_it_is_with_a_date |
| C25 | **A notice telling somebody an update landed names the move it costs them.** | unchanged | not exercisable — a release is the session's act; held by tests/test_version_check.py::test_the_warning_names_the_cheap_move_before_the_expensive_one |
| C26 | the close-issues workflow reads the **pull request bodies** | `branch-and-release` §*Work accumulates*, **So a workflow reads the keywords instead…**, which holds it | removed from this file — held there |
| C27 | **Every issue the run named is closed**, the labels stay, the next branch from `main` | the same boxes; the labels' reason is the tracker document's | not exercisable — a release is the session's act; held by tests/test_the_closer_carries_on_past_a_refusal.py |
| I1 | **A milestone answers *when*…** and the due-date sentence | unchanged | not exercisable — a release is the session's act; held by tests/test_a_release_is_sized_by_a_criterion.py::test_the_rule_states_the_criterion_and_not_the_count |
| I2 | **A release is sized by what has to be in effect…** | unchanged, its two releases gone | not exercisable — a release is the session's act; held by tests/test_a_release_is_sized_by_a_criterion.py::test_the_rule_states_the_criterion_and_not_the_count, tests/test_a_release_is_sized_by_a_criterion.py::test_one_document_states_a_releases_size |
| I3 | **Three or four is a ceiling, not a target.** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_release_is_sized_by_a_criterion.py::test_the_count_survives_as_a_ceiling_in_the_wording_the_cap_already_uses |
| I4 | **The two releases above are named rather than numbered on purpose.** | `spec.md` §*Removes* names no such row; an overview divergence | removed — it explained a citation that left |
| I5 | **What the criterion does not change.** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_release_is_sized_by_a_criterion.py::test_the_rule_says_what_it_does_not_change |
| I6 | `backlog:` leaves in one act; a milestone's description | **An issue leaves `backlog:` in one act…** | not exercisable — a release is the session's act; held by no test |
| I7 | `log:` holds no work | **`log:` holds what is not work…** | not exercisable — a release is the session's act; held by no test |
| I8 | a concern that outlives a schedule is a label | bold, unchanged in substance | not exercisable — a release is the session's act; held by tests/test_a_declared_label_reaches_the_tracker.py::test_every_declared_label_says_which_document_specifies_it |
| I9 | **`from-review` marks an issue a review round filed.** | unchanged, its share of a date gone | not exercisable — a release is the session's act; held by no test |
| I10 | **`flow-measurement` is a label that is not an index.**, **A log rolled with no comment…** | one paragraph | not exercisable — a release is the session's act; held by tests/test_a_release_rolls_the_flow_measurement_issue.py::test_two_open_issues_fails_loudly_without_retrying, tests/test_a_release_rolls_the_flow_measurement_issue.py::test_the_tracker_doc_states_the_condition_the_roll_carries |
| I11 | **A rolling log is titled after the version it rolled from**, **A version below the running one…** | unchanged | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_the_illustrative_version_is_allowed_in_any_loaded_file, tests/test_release_hygiene.py::test_a_version_below_the_running_one_is_history_and_is_kept |
| I12 | **A title that does not begin with `chore: flow measurement — after `…** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_release_rolls_the_flow_measurement_issue.py::test_rolled_from_reads_only_the_title_the_roll_itself_writes |
| I13 | **`size: now` says this ticket has to be in effect…** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_release_is_sized_by_a_criterion.py::test_the_label_is_two_states_and_nothing_schedules_from_it |
| I14 | **The prefix is what keeps it inside the rule…**, `chain: reframed` | **The subject sits in the prefix and the verdict in the value** | not exercisable — a release is the session's act; held by no test |
| I15 | **Nothing schedules from this label**, **One thing reads it, and only to spend it.** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_release_is_sized_by_a_criterion.py::test_the_label_is_two_states_and_nothing_schedules_from_it, tests/test_release_hygiene.py::test_the_script_closes_and_takes_off_one_named_label_and_nothing_else |
| I16 | **The judgment is made at filing…**, **No sweep of the standing backlog is owed…** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_declared_label_reaches_the_tracker.py::test_the_document_answers_what_it_left_open, tests/test_a_declared_label_reaches_the_tracker.py::test_the_no_sweep_rule_carries_its_reason |
| I17 | **`merged: X.Y.Z` goes on earlier…**, **What it does not decide…** | one paragraph | not exercisable — a release is the session's act; held by no test |
| I18 | **Closing the open `flow-measurement` issue leaves zero open…** | unchanged | not exercisable — a release is the session's act; held by tests/test_a_release_rolls_the_flow_measurement_issue.py::test_two_open_issues_fails_loudly_without_retrying |
| I19 | the completeness check **refuses the release**; what it compares | **`release_completeness_check.py` refuses the release…** | not exercisable — a release is the session's act; held by tests/test_a_release_cannot_ship_an_untrue_milestone.py |
| I20 | **A missing `Closes #N` still costs an issue…** | **A missing `Closes #N` leaves an issue in the milestone…** | not exercisable — a release is the session's act; held by tests/test_a_release_cannot_ship_an_untrue_milestone.py::test_a_pull_request_body_with_no_closing_keyword_refuses_the_release |
| I21 | **An issue a pull request into a release branch claimed carries `merged: X.Y.Z`…** and its three bullets | unchanged | not exercisable — a release is the session's act; held by tests/test_a_merged_ticket_says_so_on_the_tracker.py::test_it_labels_the_issue_the_keyword_named_and_nothing_else |
| I22 | **A closing keyword claims the one number after it.**, **Write the keyword in front of every number** | one paragraph, neutral numbers | not exercisable — a release is the session's act; held by tests/test_a_body_naming_two_issues_claims_one.py::test_the_sentence_that_lost_an_issue, tests/test_a_body_naming_two_issues_claims_one.py::test_the_document_that_teaches_the_rule_carries_no_instance_of_it |
| I23 | **A keyword inside a fence or a code span claims nothing…** | unchanged | not exercisable — a release is the session's act; held by tests/test_release_hygiene.py::test_an_html_comment_is_still_read_as_a_claim |
| I24 | the body owes no reconciling; **Consolidate the body**, **Leave the body…** | **An issue is read whole, and its body owes the reader no reconciling.** | not exercisable — a release is the session's act; held by no test |
| I25 | the ledger issue keeps its body | bold, unchanged in substance | not exercisable — a release is the session's act; held by no test |
| I26 | an issue is titled like a commit | bold, unchanged in substance | not exercisable — a release is the session's act; held by no test |
| I27 | the signal is the tag, not the branch | **The signal is the tag, not the branch.**, the `release/v0.3.0` example gone | not exercisable — a release is the session's act; held by no test |

B rows are `branch-and-release` (25), C rows `release-checklist` (27), I rows
`issues-and-milestones` (27). C26 moved to `branch-and-release`, I4 left with
the case that pinned it, and C12 stands with two of its answers left to
`skills/settle/SKILL.md`, which already holds them.
