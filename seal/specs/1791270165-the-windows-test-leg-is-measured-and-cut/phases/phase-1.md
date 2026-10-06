# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | b9435eda (the workflow edit; the phase closes when the dispatch tables below are recorded) |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

The `test.yml` edit of `plan.md` phase 1 and its local checks: a
`workflow_dispatch` trigger with a boolean `windows_defender_off` input · NAME NOT IN TREE
(default `true`), `--durations=50` on the `pytest` line with its
`- run: pytest tests/ -q -n auto` head kept, the phase 2 Defender step in the
same edit gated on the input, and the "198 s against 24 s" comment dated and
pointed here. No push and no dispatch: the session runs those, and this
record gains the three legs' top-50 tables from the dispatch run.

The close, asked of a second smith on another machine: find out why each
`pytest` leg and the `ledger` job of run 37429940700 concluded `failure`
before using the tables, record the three tables with run id, SHA, date and
wall time, answer Q2, and fill `plan.md`'s Status for this phase.

## What this phase found

**The Defender step is not in the tree.** Writing the step
(`Set-MpPreference -DisableRealtimeMonitoring $true`, `shell: pwsh`, gated
on `runner.os == 'Windows'`) was refused by the harness's permission
classifier as weakening a security control. The refusal covers the outcome,
so the step was not written by any other route. Its input had no other use,
so `workflow_dispatch` landed bare. Whether the step goes in is the
repository owner's decision (`questions.md` Q10); until it is, phase 2 has
nothing to measure and one dispatch measures phase 1.

**The plan's `if:` would never have run the step on a dispatch.** It read
`inputs.windows_defender_off == 'true'`. The `inputs` context keeps a
boolean input a boolean, and an Actions expression compares unlike types as
numbers, where `'true'` is NaN, so the comparison is false for both
answers. The step, if the owner allows it, reads the input bare. This is
`read` from the Actions expression documentation and not `executed`: no
dispatch has run.

**Six modules read `test.yml`, not four.** `tests/test_the_gate_names_every_step_ci_runs.py`
and `tests/test_deferral_check.py` name the file too, so the local check ran
all six:

    bin/test tests/test_arm_check.py tests/test_release_hygiene.py
      tests/test_the_suite_has_a_command_that_is_cheap_twice.py
      tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py
      tests/test_the_gate_names_every_step_ci_runs.py
      tests/test_deferral_check.py -q

`322 passed, 2 skipped in 8.96s`, exit 0 read directly (`executed`,
2026-10-06, at the tree of b9435eda).

### The baseline run, `executed` 2026-10-06

Run 37429940700, `workflow_dispatch` at be8a4115 (the phase 4a close, so the
twins case is already sampled), started 2026-10-06 07:29 UTC. Read with
`gh run view 37429940700 --json jobs` and `gh run view --job <id> --log` on
2026-10-06.

| Leg | Job wall time (`startedAt` to `completedAt`) | pytest's summary |
|---|---|---|
| windows-latest | 30 m 33 s | `2 failed, 12833 passed, 207 skipped in 1791.48s (0:29:51)` |
| macos-latest | 13 m 31 s | `2 failed, 12952 passed, 88 skipped in 792.91s (0:13:12)` |
| ubuntu-latest | 6 m 05 s | `2 failed, 12959 passed, 81 skipped in 351.70s (0:05:51)` |

### Why every job concluded `failure`, and what it does to the tables

**The three `pytest` legs failed the same two cases, and both are this work
item's own records.** Neither is a timeout, a crash or a runner error. Each
leg ran all 13,042 cases to the end and printed its table, so the durations
are a whole-suite measurement.

- `tests/test_a_record_states_what_the_tree_has.py::test_this_repositorys_own_records_state_nothing_the_tree_lacks`
  failed on 14 `NOT-IN-TREE` lines in this item's `overview.md`, `plan.md`,
  `questions.md`, `spec.md` and this file: names the tree does not carry
  yet, or no longer carries, without the marker. The framer marked twelve
  at a321fbcb, and this close marks the last two (`overview.md` line 52 and
  line 12 above).
- `tests/test_no_real_identifiers.py::test_only_fixture_user_paths` failed
  on `overview.md` line 31, a real home directory in the `git -C` command
  the first smith wrote for the push. This close replaces it with a
  placeholder.

**The `ledger` job failed on the same records.** Its `evidence-check
--strict .` exited 2 on the same 14 `NOT-IN-TREE` lines. It also printed
`DRIFTED` for `spec.md` line 14, the Grounding row quoting D1's released
hash, but a drift alone exits 1 and the job turns 1 into a warning. The
framer reworded that row at a321fbcb. After this close the command exits 0
(`executed`, below).

So a failure changes nothing a figure in the tables means. The two failing
cases take well under a second each and are not in any table.

### The Windows leg's `--durations=50` table

    36.44s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_no_shape_the_base_stops_reads_silent
    25.12s call     tests/test_guard_resolves_the_tree_it_judges.py::test_nothing_the_base_read_as_a_switch_goes_quiet
    23.27s call     tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records
    20.86s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_depth_restarts_at_a_stop
    20.36s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_reason_the_checker_does_not_recognise_passes
    17.87s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a while condition]
    17.36s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_quiet_record_between_the_two_does_not_restart_the_count
    17.14s call     tests/test_settle_reads_before_it_removes.py::test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item
    16.91s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_record_after_an_unreframed_second_is_refused
    16.47s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframed_record_is_written_and_starts_the_count_at_no[True]
    16.44s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframed_record_is_written_and_starts_the_count_at_no[False]
    15.54s call     tests/test_the_fixes_close_the_record.py::test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused
    15.48s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframe_naming_another_round_does_not_permit_the_record
    14.83s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_run_whose_report_names_no_failure_and_exits_otherwise_is_not_measured[tests-none-failing]
    12.86s call     tests/test_the_gate_names_every_step_ci_runs.py::test_a_seal_that_answers_every_step_says_so
    12.54s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_values_that_cannot_be_written_leave_the_seal_standing
    12.53s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_pull_request_the_record_names_reaches_the_values_file
    12.41s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_second_landing_in_a_run_reads_second_and_prints_the_stop
    12.40s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_repository_shipping_no_gate_runs_the_invoked_copy
    12.19s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_with_record_seals_the_item_and_counts_its_rounds
    12.05s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_run_with_no_session_says_so_and_names_the_hand_command
    12.00s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter
    11.85s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_recorded_seal_says_the_cell_is_written_and_not_committed
    11.77s call     tests/test_a_document_has_room_for_the_next_fold.py::test_this_repository_passes_the_command_with_no_flags
    11.71s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing
    11.67s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_values_file_holds_this_runs_panel
    11.66s call     tests/test_the_fixes_close_the_record.py::test_a_section_that_accounts_for_the_coordinates_under_an_earlier_round_is_silent
    11.43s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_reads_the_real_seals_two_endings_apart
    11.14s call     tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape
    10.65s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_settled_item_preflights_green_and_names_the_record_it_asked
    10.57s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: an assignment's value]
    10.48s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed
    10.37s call     tests/test_the_fixes_close_the_record.py::test_the_reach_takes_the_row_the_inherited_table_attributed_it_to
    10.24s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_fixed_verdict_naming_no_commit_passes
    10.04s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_runners_event_payload_judges_the_fixture_and_fails_its_gate
    9.97s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_fixed_at_verdict_in_a_verifying_round_fails_the_preflight
    9.95s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_three_dot_range_resolves_through_the_merge_base
    9.92s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_one_commit_named_two_ways_is_one_failure
    9.73s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[d2f2c0dc]
    9.57s call     tests/test_a_new_returnable_value_is_a_contract_change.py::test_the_row_names_the_unit_and_its_reach
    9.57s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_commit_found_before_a_nesting_too_deep_still_stops
    9.46s call     tests/test_a_gate_that_fails_says_so.py::test_json_a_gate_prints_that_is_not_a_hooks_output_ends_nothing
    8.97s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_location_that_lands_in_no_written_unit_reads_no[`mod.py#v`; see #w]
    8.84s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_first_runner_without_the_gates_environment_costs_the_word
    8.71s setup    tests/test_the_commit_gate_decides_at_the_commit.py::test_s3_no_verify_into_the_declared_worktree_goes_through
    8.28s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_header_nesting_keeps_the_commits_found[f() { ]
    8.25s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_the_pending_surface_cutoff_is_this_work_items_own_second
    8.22s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: an assignment, then 2>/dev/null git]
    8.16s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_generated_unread_fixes_fail_the_preflight_at_seal
    8.15s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_capped_run_is_sealed_with_its_deferral_on_the_stamp

### The macOS leg's `--durations=50` table

    10.44s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_no_shape_the_base_stops_reads_silent
    10.31s call     tests/test_settle_reads_before_it_removes.py::test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item
    9.61s call     tests/test_guard_resolves_the_tree_it_judges.py::test_nothing_the_base_read_as_a_switch_goes_quiet
    9.34s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_cuts_every_admitted_body_where_the_reader_does[zsh-through eval]
    8.86s call     tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records
    8.56s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_cuts_every_admitted_body_where_the_reader_does[zsh-directly]
    8.31s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_cuts_every_admitted_body_where_the_reader_does[bash-through eval]
    8.22s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_cuts_every_admitted_body_where_the_reader_does[bash-directly]
    6.89s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_quiet_record_between_the_two_does_not_restart_the_count
    6.81s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_run_that_removed_nothing_is_silent_and_says_what_it_read
    6.58s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_depth_restarts_at_a_stop
    6.44s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframed_record_is_written_and_starts_the_count_at_no[True]
    6.20s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_three_dot_range_resolves_through_the_merge_base
    6.11s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body[bash-through eval]
    5.90s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body[zsh-through eval]
    5.74s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[d2f2c0dc]
    5.63s call     tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape
    5.60s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body[zsh-directly]
    5.30s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body[bash-directly]
    5.30s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframed_record_is_written_and_starts_the_count_at_no[False]
    5.15s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_record_after_an_unreframed_second_is_refused
    4.88s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_reason_the_checker_does_not_recognise_passes
    4.64s call     tests/test_a_released_row_is_read_again_in_a_fragment.py::test_the_run_writes_the_same_bytes_in_any_ledger_order[six files]
    4.45s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[3dd24073]
    4.32s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[576fe39d]
    4.28s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_recorded_seal_says_the_cell_is_written_and_not_committed
    4.12s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_values_that_cannot_be_written_leave_the_seal_standing
    4.09s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframe_naming_another_round_does_not_permit_the_record
    4.09s call     tests/test_arm_check.py::test_the_report_does_not_call_a_mutated_arm_unmutated[every pair times out]
    4.07s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing
    4.06s call     tests/test_arm_check.py::test_a_command_that_never_returns_is_recorded_as_unmeasured
    3.99s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_with_record_seals_the_item_and_counts_its_rounds
    3.97s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_repository_shipping_no_gate_runs_the_invoked_copy
    3.93s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_run_with_no_session_says_so_and_names_the_hand_command
    3.89s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_measured_range_that_removed_three_rows_reports_nothing
    3.85s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_person_at_a_terminal_sees_the_stamp_drawn_once
    3.84s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_commit_found_before_a_nesting_too_deep_still_stops
    3.82s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_reads_the_real_seals_two_endings_apart
    3.80s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_pull_request_the_record_names_reaches_the_values_file
    3.73s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[<(]
    3.63s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[$(]
    3.60s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[cc49ae64]
    3.59s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_values_file_holds_this_runs_panel
    3.55s call     tests/test_a_new_returnable_value_is_a_contract_change.py::test_the_derivation_agrees_with_an_independent_one_over_the_whole_tree
    3.54s call     tests/test_the_fixes_close_the_record.py::test_a_section_that_accounts_for_the_coordinates_under_an_earlier_round_is_silent
    3.48s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter
    3.47s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_second_landing_in_a_run_reads_second_and_prints_the_stop
    3.46s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed
    3.39s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry
    3.35s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_cd_rows_shared_and_new_files_each_get_a_measured_word[xdist]

### The ubuntu leg's `--durations=50` table

    16.22s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r1: 500 nested substitutions]
    12.67s call     tests/test_settle_reads_before_it_removes.py::test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item
    8.60s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_three_dot_range_resolves_through_the_merge_base
    8.06s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_run_that_removed_nothing_is_silent_and_says_what_it_read
    7.51s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[d2f2c0dc]
    6.87s call     tests/test_a_new_returnable_value_is_a_contract_change.py::test_the_derivation_agrees_with_an_independent_one_over_the_whole_tree
    6.59s call     tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape
    6.10s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[576fe39d]
    5.25s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[3dd24073]
    5.14s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_measured_range_that_removed_three_rows_reports_nothing
    5.01s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[cc49ae64]
    4.93s call     tests/test_the_printed_ledger_name_is_the_file_that_was_read.py::test_the_refusal_above_can_actually_fail
    4.66s call     tests/test_a_document_has_room_for_the_next_fold.py::test_this_repository_passes_the_command_with_no_flags
    4.33s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_commit_found_before_a_nesting_too_deep_still_stops
    4.20s call     tests/test_a_released_row_is_read_again_in_a_fragment.py::test_the_run_writes_the_same_bytes_in_any_ledger_order[six files]
    4.03s call     tests/test_arm_check.py::test_a_command_that_never_returns_is_recorded_as_unmeasured
    4.03s call     tests/test_arm_check.py::test_the_report_does_not_call_a_mutated_arm_unmutated[every pair times out]
    4.00s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[$(]
    3.73s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[<(]
    3.32s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body[bash-through eval]
    3.30s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_rider_check_never_leaves_both_readings
    3.27s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_config_reader_never_leaves_both_readings
    3.20s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_no_shape_the_base_stops_reads_silent
    3.15s call     tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py::test_every_file_the_plugin_reads_or_writes_names_its_encoding
    3.15s call     tests/test_one_heredoc_shape_agrees_with_the_shell.py::test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body[bash-directly]
    3.11s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_cd_rows_shared_and_new_files_each_get_a_measured_word[xdist]
    3.04s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_routing_reader_never_leaves_both_readings
    3.04s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_where_the_walk_claims_to_be_exact_it_is
    2.96s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_reworded_sentence_reports_the_pin_it_left_behind
    2.91s call     tests/test_no_passage_is_pasted_into_a_second_file.py::test_a_removed_copy_passes_without_a_baseline_edit
    2.90s call     tests/test_no_passage_is_pasted_into_a_second_file.py::test_a_count_over_its_baseline_is_named_and_one_at_it_is_not
    2.88s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_root_run_row_measures_the_module_the_branch_added[xdist]
    2.81s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_correction_at_one_coordinate_reports_the_class[seal/ledger.md]
    2.79s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_report_names_the_sentence_that_was_corrected_too
    2.79s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_record_of_a_past_round_is_not_a_survivor
    2.78s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_correction_at_one_coordinate_reports_the_class[seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md]
    2.71s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound["$(]
    2.69s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_file_the_base_fails_alone_is_proven_by_one_session_listing_it[xdist]
    2.67s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_person_at_a_terminal_sees_the_stamp_drawn_once
    2.65s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframed_record_is_written_and_starts_the_count_at_no[False]
    2.61s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_quiet_record_between_the_two_does_not_restart_the_count
    2.61s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_pull_request_the_record_names_reaches_the_values_file
    2.60s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_depth_restarts_at_a_stop
    2.57s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_what_a_test_printed_is_not_read_as_pytests_own_lines[an-inner-empty-run-xdist]
    2.56s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_recorded_seal_says_the_cell_is_written_and_not_committed
    2.55s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_an_inner_run_on_stderr_under_s_is_not_read_as_the_runs_own[xdist]
    2.55s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[P3-sh-own]
    2.54s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_values_file_holds_this_runs_panel
    2.51s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[P3-sh-files]

### What the tables say (Q2)

**The Windows top 50, by module** (seconds of call time summed over the
module's cases in the table):

| Module | Cases | Seconds |
|---|---|---|
| `test_the_seal_is_taken_once_by_the_sealer.py` | 18 | 201.5 |
| `test_a_fix_of_a_fix_is_counted.py` | 8 | 124.9 |
| `test_no_shape_the_base_stops_reads_silent.py` | 3 | 54.3 |
| `test_a_record_precedes_the_fixes_it_commissions.py` | 4 | 48.8 |
| `test_the_commit_gate_decides_at_the_commit.py` | 4 | 45.4 |
| `test_the_fixes_close_the_record.py` | 3 | 37.6 |
| `test_guard_resolves_the_tree_it_judges.py` | 1 | 25.1 |
| `test_the_guard_asks_once_per_session.py` | 1 | 23.3 |
| seven modules with one or two cases each | 8 | 91.5 |

The twins case is not in the table, so after 4a it runs under 8.15 s on
Windows. The heredoc shell oracle is absent too, as the frame expected:
`conftest.shell_probe` skips it on `windows-latest`.

**The top 50 hold about a tenth of the Windows leg's work, not most of it.**
They sum to 652 s of call time. The leg ran 1,791 s on at least three xdist
workers, since the log names `[gw2]`; GitHub's documentation gives a hosted
`windows-latest` four cores (`read`, not measured here). Three or four
workers make 5,370 to 7,170 worker-seconds, of which the top 50 are 9 to
12%. The other 12,990 cases average about 0.35 to 0.5 s each on Windows.
The ubuntu leg averages about 0.1 s for the same cases.

**The slowdown is spread across the suite, not held by a few cases.** The
whole Windows leg ran 5.1 times as long as ubuntu's (1,791 s against
352 s). The cases that appear in both tables run 4.6 to 11.4 times as long
on Windows when they spawn processes (the sealer and fix-of-a-fix cases, the
guard case), and 1.2 to 2.5 times when they mostly read files
(`test_settle_reads_before_it_removes.py`,
`test_a_corrected_sentence_survives_elsewhere.py`).

**What this does to the frame.** The issue reasoned that "a minority of
cases carry most of the growth", and `plan.md` puts 4b before the shards on
that reading. On Windows at be8a4115 the reading does not hold. If every
case in the Windows table went to zero, the leg would lose 652
worker-seconds, about 2.7 minutes of wall time on four workers, out of
30. Phase 4b is still worth building, because a case on the table is a
per-case floor that the shards and phase 5's ceiling will both meet. But
the leg's minutes are phase 3's to take. Recorded here rather than sent
back to the framer (`agents/smith.md`, phase 1).

**One run, one SHA.** Run 37429940700's Windows leg took 30 m 33 s. The
last two Windows legs on `main`'s pull requests before it took 39 m 34 s
and 37 m 30 s (`plan.md` Technical context), and 4a's sampling sits between
them and this one. One run on a shared runner image cannot say how much of
that difference 4a bought, and this record does not claim it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `test.yml` sentence "That is the whole of why the windows leg took 198s against ubuntu's 24s" as a present-tense claim | the same comment, now dated, pointing at this record |
