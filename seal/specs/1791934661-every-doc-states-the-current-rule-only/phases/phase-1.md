# 1791934661-every-doc-states-the-current-rule-only — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | not closed — the build ends at the commit that adds this record (the rewrite is `0de2d55a`, `aa9e06bc`, `6a8712ad`); the phase closes once its released rows are answered and its budget rows written at the rebase, so `plan.md`'s Status cell stays empty |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

Rewrite `docs/worktree-guard-spec.md` to the current rule only, ≤ 35,000 B and
≤ 600 lines, every heading kept; every rule of the old file mapped in a census
to its new coordinate or a `## Removes` row, each `not exercisable — no agent
case opens this file; held by <test ids>`; the 9 pin modules re-pointed or
removed with a row, a re-pointed pin seen red first; outside `§` citations
resolving; before and after recorded with the frame's `measure.py`. No eval.
Do not touch `seal/budgets.md` or any checker: #923's check and #930's
budgets are not on this branch, and the rows go in at the rebase. Mid-phase
the orchestrator narrowed it: write no `Re-read ·` or `Corrected ·` ledger
row — the owner decides how released rows into rewritten docs are handled —
and list the affected rows here instead; what was removed goes here as one
summary, not per sentence. Do not start phase 2.

## What this phase found

**Before and after.** `measure.py` (`executed`) at `431c6754` and at
`6a8712ad`, its #930 columns from `budget_check.classify` in the 930
worktree as it stood on 2026-10-14; `wc -lc` agrees on bytes and lines.

| Measure | Before | After |
|---|---|---|
| Bytes | 74,355 | 34,973 |
| Lines | 999 | 501 |
| History lines, #930 marks · widened marks | 39 · 36 | 0 · 0 |
| Rule lines (#930) | 309 | 273 |
| Bold-led paragraphs · over 8 lines | 50 · 16 | 82 · 2 |
| Lines in paragraphs that open with no rule | 463 | 27 |
| Headings · fold markers · `Enforced by:` lines | 16 · 4 · 9 | 16 · 4 · 9, the `Enforced by:` lines byte-identical |
| Pin modules (literals found verbatim) | 9 (52) | 8 (43) |
| `BASELINE` pair with `commit-review-gate-spec.md` | 1 run | 0 runs, entry removed |

The `bytes:` and `history:` rows for this file are owed at the rebase onto
#923 phase 1: `bytes:docs/worktree-guard-spec.md` 34,973 and
`history:docs/worktree-guard-spec.md` 0 (`docs-history:` 0 where #930 alone
has merged).

**The frame's count of quoted-line anchors does not hold.** `plan.md`
phase 1 says "the 3 quoted-line anchors corrected" and `plan.md`
§*Technical context* counts `worktree-guard-spec` 3 of the five; `spec.md`'s
table and `measure.txt` say 0, and the 103 anchors in the 79 rows are seven
heading paths (`read`, by extracting every `docs/worktree-guard-spec.md#`
coordinate from `seal/ledger.md` and `seal/releases/*.md`). The rewrite kept
every heading, so `evidence-check --strict` finds 0 BROKEN.

**The 79 rows are 18 families, and the phase drifted a 19th.**
`evidence-check --reverify` without `--into` (`executed`, writes nothing here)
names 18 released rows left for this file, one per family root, because most
of the 79 are earlier `Re-read ·` rows of the same families, and a 19th for
the `BASELINE` entry this phase removed. `--strict` exits 2 and the lenient
run 1 on these alone (80 drifted coordinates, 0 broken). **Resolution: they
are not re-read or corrected — #944 retires the released ledger files.** The
roots, with this phase's reading of each claim against the new text (`read`;
nothing written):

| Root row | Drifted coordinates | Reading |
|---|---|---|
| `seal/releases/0.18.0.md:135` K6 | `## Known limits` | the limit stands; *would have stopped 9 of D1's 27,351 pairs* left the doc for work item 1790993140's `phases/phase-3.md`, which the limit links — `Corrected ·` |
| `seal/releases/0.18.0.md:168` Corrected · G17 | `## Known limits` | the Windows count is unusable — holds |
| `seal/releases/0.18.3.md:68` T2 | `## Choice sites` | holds |
| `seal/releases/0.20.0.md:96` Corrected · K7 | `## Creation consent…`, `### Which tree…` | holds except *candidate C and the two rules read past the base are named as gone*: no longer named — `Corrected ·` |
| `seal/releases/0.20.0.md:97` Corrected · I9 | `## Creation consent…` | holds |
| `seal/releases/0.20.0.md:111` S12 | `## Decision matrix`, `## Known limits`, `### Which tree…`, two test units | holds; every `Enforced by:` target unchanged |
| `seal/releases/0.20.0.md:115` F4 | `## Known limits` | holds |
| `seal/releases/0.20.0.md:116` F5 | `## Known limits`, `### Which tree…` | holds |
| `seal/releases/0.20.0.md:118` F7 | `## Decision matrix` | holds; its three example commands left |
| `seal/releases/0.20.0.md:119` F8 | `## Decision matrix` | holds |
| `seal/releases/0.20.0.md:224` R3 | `## Decision matrix`, test unit | holds; the `git -C w checkout` example left |
| `seal/releases/0.20.0.md:225` R4 | `## Known limits`, test unit | holds |
| `seal/releases/0.21.0.md:381` S15a | `## Creation consent…` | holds |
| `seal/releases/0.21.0.md:385` S27 | `## Decision matrix`, `## Known limits` | the shell-built word holds; *the hidden-spelling bullet and the `sh -c` bullet read as at 0.20.0* and *names #856's four forms* do not (reworded; #856 not named) — `Corrected ·` |
| `seal/releases/0.21.0.md:724` S9 | `## Decision matrix`, `## Known limits` | holds |
| `seal/releases/0.21.1.md:6` S5 | `## Creation consent…` | holds |
| `seal/releases/0.21.1.md:71` Corrected · S13 | five headings | holds |
| `seal/releases/0.21.1.md:90` S14 | four headings | holds |
| `seal/releases/0.18.1.md:370` O4 | `tests/test_no_passage_is_pasted_into_a_second_file.py#BASELINE` | holds; drifted by the entry this phase removed, and every later phase that lowers `BASELINE` drifts it again |

**Only two of the nine pin modules read this file.**
`tests/test_guard_resolves_the_tree_it_judges.py` (`_policy_text`) and
`tests/test_one_word_one_meaning.py` (`once per session per direction`) open
it; the other seven share literals with it because they assert on hook output
or command text, and none opens the doc. Three pinned sentences narrated
(*The guard stops more than it did*, *Nothing is read past the base's words
since #826*, *left with #826*); each pin now holds the sentence that states
the rule, and each was seen red through `mutation-check` with that sentence
broken in the doc (`executed`, three `red`). No literal was dropped.

**Survivor sweep: retired by #944.**

**Every outside citation resolves by heading, and one names a table that
left.** All sixteen headings stand, so each `§` from `hooks/`, `tests/`,
`skills/implement/orchestration.md` and the READMEs names a section that is
there (`read`), and the bold leads they cite (*Which commands reach these
rows*, rule 4, *Under the press*) are kept. `hooks/worktree_consent.py`'s
`automation_answered` docstring said §*Creation consent* "holds the table",
and the consent tables were folded into prose; it says the section "states
it" now (`d134d586`).

**`tests/test_release_hygiene.py#VERSIONS_OF_ANOTHER_PRODUCT` exempted
`("docs/worktree-guard-spec.md", "2.54.0")`, and the doc named no `2.54.0`
before this phase either.** The dead entry is removed (`bbe41914`).

**What left the doc, in one summary.** The provenance of each rule — the
issue, round and work item that produced it — and every measurement: the
sixteen setups of 1791779434, the 31,193 and 27,351 command pairs, the eleven
shapes round 1 executed, the six-creation budget sequence, the Windows CI
run id, the 2026-05-06 activity table header and its observations. The
narratives of what a rule replaced: the Agent path's two failed token
readings, the writer that minted consent from an unjudged first segment, the
ladder row put in the table twice, the walk that missed the other order,
`#692`'s `post-checkout` attempt, the brace reader built and taken out, the
two rules read past the base. The two consent comparison tables became three
sentences of *The routing answer is the second consent*. Examples that
illustrated rather than defined a rule (`git rebase - feature/x`, `./git` and
four more paths, `"(VS Code 터미널)"`, `cd>/dev/null W`, `git notes`). Two
statements that are other files' to hold: what the commit gate's reading
reads for a foreign hooks slot, and the gate's own consent read since #773.

**Census: 50 rules, 50 kept, 0 removed.** Every rule of the old file opens
bold or is a numbered rule; each row's new coordinate is a section and the
bold lead of the paragraph that holds it now. Every row is `not exercisable —
no agent case opens this file; held by` the node ids named.

| # | Old rule | New coordinate | Exercised by |
|---|---|---|---|
| 1 | §A *The tracked-changes row has two readers too (#894)* | §A *The tracked-changes row has two readers too* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_under_the_press_the_dirty_row_is_a_deny_to_the_model, tests/test_the_guard_asks_once_per_session.py::test_the_press_is_read_from_the_sessions_own_root, tests/test_the_guard_asks_once_per_session.py::test_the_token_does_not_reach_the_dirty_row_under_the_press_either |
| 2 | §A *Why the row's own sentences predict nothing* | §A *The deny states what the guard read and predicts nothing about git* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_one_text_for_every_switch_form, tests/test_the_guard_asks_once_per_session.py::test_a_compound_stash_and_switch_meets_the_deny, tests/test_the_guard_asks_once_per_session.py::test_the_ways_on_pass_the_guard |
| 3 | §A *The failure direction* (the tracked-changes row) | §A *The deny states what…*, its last sentence | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_plain_retry_meets_todays_rows |
| 4 | §A *Which commands reach these rows (#826)* | §A *Which commands reach these rows* | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_a_listed_shape_is_silent_in_every_tree_and_spawns_nothing, tests/test_guard_resolves_the_tree_it_judges.py::test_the_guard_policy_says_which_shapes_reach_the_rows_and_who_reads_the_stop |
| 5 | §A **listed** | §A **listed** | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_no_listed_form_moves_head_under_git, tests/test_worktree_guard.py::test_a_rebase_naming_a_branch_is_unrecognised, tests/test_guard_resolves_the_tree_it_judges.py::test_no_redirection_makes_a_moving_verb_listed_wherever_it_stands |
| 6 | §A **a switch** | §A **a switch** | not exercisable — no agent case opens this file; held by tests/test_guard_resolves_the_tree_it_judges.py::test_the_guard_policy_says_which_shapes_reach_the_rows_and_who_reads_the_stop |
| 7 | §A **unrecognised** | §A **unrecognised** | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_an_unrecognised_shape_stops_where_the_tree_matters |
| 8 | §A *The stop for an unrecognised shape*, with the paragraphs under it | §A *An unrecognised shape stops only where the tree matters*, *The stop has two readers*, *Approving the `ask` would run every segment*, *Each shape is judged in the tree its segment names* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_under_the_press_the_stop_is_a_deny_to_the_model, tests/test_worktree_guard.py::test_no_approval_runs_a_line_past_an_active_tree, tests/test_guard_resolves_the_tree_it_judges.py::test_a_shape_in_a_clean_tree_takes_no_stop_from_one_in_a_dirty_tree, tests/test_worktree_guard.py::test_the_stop_names_each_tree_that_matters_in_both_languages, tests/test_worktree_guard.py::test_a_cut_group_is_judged_in_the_tree_its_own_c_names |
| 9 | §A *The failure direction* (the stop) | §A *The failure direction* | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_the_same_shapes_are_silent_in_a_clean_single_stream_tree, tests/test_guard_resolves_the_tree_it_judges.py::test_the_guard_policy_says_which_shapes_reach_the_rows_and_who_reads_the_stop |
| 10 | §B *An isolated agent is concurrent work by construction…* | §B's subsection, its three paragraphs | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_an_isolated_agent_asks_without_counting_sessions, tests/test_worktree_guard.py::test_the_agent_verdict_does_not_depend_on_the_prompt |
| 11 | *Creation consent* *The first worktree creation in a session is the question…* | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_first_creation_is_still_a_question, tests/test_the_guard_asks_once_per_session.py::test_a_second_creation_in_the_same_session_is_allowed |
| 12 | *What separates the first creation from the sixth…* | *The consent record is written after the answer* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_creation_that_ran_leaves_a_record, tests/test_the_guard_asks_once_per_session.py::test_the_pre_tool_use_arm_records_nothing |
| 13 | *The routing answer is the second consent…*, with both tables | *The routing answer is the second consent…*, *A `routing.md` is not read…* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_measured_automation_run_is_not_stopped, tests/test_the_guard_asks_once_per_session.py::test_a_bare_creation_after_the_automation_answer_is_allowed |
| 14 | *What exactly is read* | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_consent_fails_closed_on_any_exception |
| 15 | rule 1 *This session's own main transcript* | rule 1 | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_subagents_own_path_falls_back_to_the_parents_transcript |
| 16 | rule 2 *A harness-written `AskUserQuestion` result* | rule 2 | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_result_not_linked_to_an_ask_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_a_shape_the_reader_did_not_expect_keeps_the_guards_deny |
| 17 | rule 3 *The routing question* | rule 3 | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_labels_match_the_routing_question_the_orchestrator_asks, tests/test_the_guard_asks_once_per_session.py::test_a_typed_answer_that_qualifies_the_preset_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_question_1_alone_and_the_boxes_beside_it_read_the_same_press, tests/test_the_guard_asks_once_per_session.py::test_the_boxes_asked_alone_neither_give_nor_take_back_the_press |
| 18 | rule 4 *The same clone* | rule 4 | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_an_answer_given_in_another_clone_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_an_answer_from_a_linked_worktree_is_the_same_clone |
| 19 | rule 5 *The last answer stands* | rule 5 | not exercisable — no agent case opens this file; held by tests/test_an_automation_run_meets_no_commit_prompt.py::test_a_later_routing_answer_takes_the_press_back, tests/test_an_automation_run_meets_no_commit_prompt.py::test_an_answer_to_another_question_leaves_the_press_standing |
| 20 | *The record.* | *The record is an empty file at…* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_directory_at_the_record_path_is_not_a_record, tests/test_the_guard_asks_once_per_session.py::test_a_session_id_that_is_only_separators_has_no_record_path |
| 21 | **A third directory, not a value in `specseal-worktree-choice/create/`** | **Not the choice marker** | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_an_unrecordable_consent_asks_rather_than_crashing |
| 22 | **The common git directory, not the per-worktree one** | **In the common git directory** | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_record_follows_the_clone_not_the_worktree |
| 23 | **The clone the guard judged** | unchanged | not exercisable — no agent case opens this file; held by tests/test_guard_resolves_the_tree_it_judges.py::test_the_writer_files_under_the_clone_the_guard_judged, tests/test_guard_resolves_the_tree_it_judges.py::test_the_guard_policy_says_the_record_is_filed_where_the_guard_judged |
| 24 | **No expiry and no pruning** | **No expiry** | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_second_creation_in_the_same_session_is_allowed |
| 25 | **A failed `git worktree add` records too** | the same bullet | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_failed_creation_still_records_the_approval |
| 26 | **An unwritable record leaves none** | the same bullet | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_an_unrecordable_consent_asks_rather_than_crashing |
| 27 | *Why the allow is bounded* | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_consent_record_buys_silence_for_a_compound_not_a_second_prompt |
| 28 | *And a segment is more than its command word* | *A segment is worktree creation only when its command word is exactly the word `git`…* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_wrapper_in_front_of_the_creation_carries_no_allow, tests/test_the_guard_asks_once_per_session.py::test_a_backgrounded_creation_is_still_only_a_creation |
| 29 | *The first test is exact equality, because a basename is not an identity* | the same paragraph as 28, and *Outside that class nothing reaches `allow`…* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_path_qualified_git_carries_no_allow, tests/test_the_guard_asks_once_per_session.py::test_the_command_word_class_is_what_the_allow_covers |
| 30 | *A creation the guard never judged used to mint the record* | *The creation ladder is reached whatever segment comes first* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_creation_anywhere_in_the_command_records, tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records |
| 31 | *So the creation is judged between the ladder's two halves* | unchanged, with its table | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned |
| 32 | *Reading "the three rows above all deny" off that first row…* | the table's IDLE row (*both, and the branch decides*) | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned |
| 33 | *The same walk missed the other order (#620)* | *The walk keeps the first switch and the first creation, in either order* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_switch_written_after_a_creation_is_judged, tests/test_the_guard_asks_once_per_session.py::test_the_order_of_a_switch_and_a_creation_does_not_decide, tests/test_the_guard_asks_once_per_session.py::test_a_command_with_both_is_never_weaker_than_either_alone |
| 34 | *The property, measured rather than the shapes* | *For a session with no consent, the guard denies or asks about the creation wherever the writer would record* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records, tests/test_the_guard_asks_once_per_session.py::test_a_dirty_tree_does_not_decide_whether_the_creation_is_questioned |
| 35 | *Why the Agent/Task path is silent rather than an allow* | §B *With consent the path is silent, never an allow…* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_agent_path_reads_the_record_a_bash_creation_wrote |
| 36 | *What does not change* | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_creation_consent_does_not_reach_the_switch_direction, tests/test_the_guard_asks_once_per_session.py::test_the_answer_does_not_reach_the_switch_direction |
| 37 | *The prompt budget* | unchanged | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_second_creation_in_the_same_session_is_allowed, tests/test_the_guard_asks_once_per_session.py::test_a_path_qualified_git_carries_no_allow |
| 38 | *Decided before git runs* *A worktree creation is decided before git runs…* | unchanged | not exercisable — no agent case opens this file; held by tests/test_a_creation_is_judged_before_git_runs.py::test_a_refused_dash_capital_b_leaves_the_branch_where_it_was, tests/test_a_creation_is_judged_before_git_runs.py::test_no_git_hook_judges_a_creation |
| 39 | *A creation the guard lets through is recorded as before…* | *A creation the guard lets through is recorded from the command that ran* | not exercisable — no agent case opens this file; held by tests/test_a_creation_is_judged_before_git_runs.py::test_an_answered_creation_runs_and_the_record_follows_it |
| 40 | §Choice sites *The two branches have opposite standing…* | *Only the deny branch protects anything* | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_a_spent_choose_budget_does_not_decide_whether_the_creation_is_questioned |
| 41 | *Once per session per direction* | unchanged | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_each_direction_carries_its_own_question, tests/test_one_word_one_meaning.py::test_the_worktree_spec_is_still_the_model |
| 42 | *Not the same record as creation consent* | *Once per session per direction*, its last sentence | not exercisable — no agent case opens this file; held by tests/test_the_guard_asks_once_per_session.py::test_the_pre_tool_use_arm_records_nothing |
| 43 | *Under the press all four choice sites deny on every attempt…* | the same lead, and *Under the press no choice reason names a question tool…* | not exercisable — no agent case opens this file; held by tests/test_the_idle_session_rows_ask_nobody.py::test_under_the_press_a_choice_row_denies_every_attempt, tests/test_a_creation_in_another_clone_asks_nobody.py::test_under_the_press_a_creation_row_denies_every_attempt, tests/test_a_creation_in_another_clone_asks_nobody.py::test_the_transcript_is_read_at_most_twice_per_creation |
| 44 | *Retry tokens, one per direction* | *Retry tokens are matched as bare words of the command, never substrings* | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_a_token_inside_quoted_prose_is_not_consent, tests/test_worktree_guard.py::test_a_quoted_separator_does_not_hide_a_real_token |
| 45 | *Where the token is read from* | unchanged | not exercisable — no agent case opens this file; held by tests/test_guard_resolves_the_tree_it_judges.py::test_the_guard_policy_and_readmes_say_a_body_token_is_not_read |
| 46 | *The token check runs before the choice sites* | *The token check runs right after the ACTIVE-session row* | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_the_token_site_does_not_spend_the_switch_questions_budget |
| 47 | *Each choice hands back the other direction's token* | the same paragraph as 46 | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_the_split_option_carries_the_creation_token |
| 48 | *What `[shared-tree-ok]` cannot reach* | *`[shared-tree-ok]` reaches neither the ACTIVE-session row nor the dirty row* | not exercisable — no agent case opens this file; held by tests/test_worktree_guard.py::test_the_token_does_not_cross_an_active_session, tests/test_worktree_guard.py::test_the_token_does_not_answer_the_dirty_tree_question |
| 49 | *Activity* *Active = ANY signal within `WORKTREE_GUARD_IDLE_MIN` minutes* | unchanged | not exercisable — no agent case opens this file; held by tests/test_worktree_guard_signals.py::test_fresh_active_event_counts, tests/test_worktree_guard_signals.py::test_transcript_scan_reaches_background_agents |
| 50 | *What a blocking prompt must show* **host app**, **disaggregated signals** | the same bullets | not exercisable — no agent case opens this file; held by tests/test_worktree_guard_signals.py::test_ancestors_includes_self_and_parent, tests/test_worktree_guard.py::test_an_unidentified_sessions_line_prints_its_kind_and_age |

The paragraphs that opened with no rule became rules too: §*Unknowns resolve
conservatively*, the eight of §*Which tree*, and the sixteen Known-limits
bullets, now fourteen bold paragraphs. Its first bullet (*Neither a switch nor
a creation is judged by git*) is §*Which tree* *The command's text is read on
every git, permanently*, and the `automation`-press bullet and the Windows
bullet keep every clause the S9, S13 and S14 rows name.
