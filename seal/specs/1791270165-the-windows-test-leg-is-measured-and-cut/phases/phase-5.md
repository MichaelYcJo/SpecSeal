# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | f1ea5d6c (the budget is a600768e; macOS's timeout re-based in f1ea5d6c) |
| Ran by | smith on Opus 5.5 (a second smith, on another machine) |

## What this phase was asked

The budget, by `questions.md` Q6's rule (a): the per-case ceiling in
`tests/conftest.py` and the three `timeout-minutes` values, taking as the
base the slower of the runs measured (phase 3 found the runner swinging by
more than the rule's margin), with each constant's comment naming the run
ids it was set from, and saying what macOS's timeout is set from now that it
is the slowest leg. Every new case seen red. Q8's after-figure from the last
run. Then the closing records: `changelog.md`, one ledger row per scenario,
`overview.md` closed.

## What this phase found

### The base each value was set from, before the confirming run

The confirming run below was slower still, and macOS's value moved to 35
when the rule was applied to it; this section is the first setting.

Q6 (a): the ceiling is 1.5 times the slowest call on the Windows leg after
phases 3 and 4, rounded up to 30 s; each `timeout-minutes` is 1.5 times the
leg's measured wall time after phases 3 and 4, rounded up to 5 minutes. The
runs after phase 4 are 37457228586 (922ded29), 37458654434 (8a69b393) and
37465328899 (98b817ad, sharded). The slowest of them is the base, because
phase 3 measured the same suite 1.19 times slower from one run to the next
and one shard 1.7 times slower than its siblings inside one run.

| Value | Base | Rule | Set |
|---|---|---|---|
| `CASE_CEILING_S` | 55.13 s, `test_no_shape_the_base_stops_reads_silent`, run 37457228586 (52.49 s in 37458654434, 29.91 s in 37465328899) | 82.7 s, up to 30 | 90 s |
| ubuntu `timeout-minutes` | 7 m 58 s, run 37458654434 (6 m 40 s, 5 m 40 s) | 11.95, up to 5 | 15 |
| macOS `timeout-minutes` | 19 m 52 s, run 37457228586 (16 m 27 s, 17 m 38 s) | 29.8, up to 5 | 30 |
| each Windows shard's `timeout-minutes` | 10 m 03 s, group 3 of run 37465328899, the only sharded run (the other groups 5 m 38 s to 6 m 22 s) | 15.1, up to 5 | 20 |

**macOS's 30 minutes was its own figure, not Windows'.** macOS is now the
longest leg and was never cut: the item's title names Windows, and
`spec.md` Out leaves macOS's time to the budget. Its base is its slowest job
of the three runs, 19 m 52 s, and 1.5 times that lands at 29.8, just under
the rounding. The margin is 1.51 times: a macOS run slower than the slowest
seen by half again fails.

**One value per ceiling, on every platform.** `spec.md` Data & interfaces
introduces no platform factor until a measured case needs one. The case
with the highest call on macOS and ubuntu is 18.76 s and 13.90 s in run
37465328899, and 21.33 s and 24.13 s in the confirming run 37469595104, so
the ceiling binds on Windows first.

**The ceiling also binds `bin/test`.** A case under 90 s on a CI runner can
pass that on a loaded laptop: on the second smith's machine, while other
sessions ran suites, one sealer case took 32.6 s that ran in 12 s on the
Windows leg. No case in the suite is near 90 s locally today, and the
ceiling's comment says what it was set from, so raising it is a visible
decision rather than a quiet one.

### What was built

- `tests/conftest.py`: `CASE_CEILING_S = 90` with its comment; `over_the_ceiling(nodeid, seconds)`, the sentence or None; and a `pytest_runtest_makereport` hook wrapper that turns a PASSING call over the ceiling into a failure whose whole report is that sentence. A call that failed on its own keeps its own report.
- `.github/workflows/test.yml`: a `timeout` on every matrix entry and `timeout-minutes: ${{ matrix.timeout }}` on the job, with the comment above the entries naming each base and run.
- `tests/test_a_slow_case_names_itself.py`, five cases: the sentence, pinned verbatim (§14); nothing at or under the ceiling; the constant; the hook driven through a real inner pytest run that loads this repository's `conftest.py` with the ceiling lowered to 0.3 s (a slow passing case fails with the sentence, a quick one passes, a slow failing one keeps its own failure); every leg has a timeout and the job reads it.
- `CONTRIBUTING.md` §*Running the checks*: what a case over the ceiling asks of a contributor, where the timeouts come from, and how to refresh `.test_durations`.

### Seen red, `executed` 2026-10-06

S7 itself: a `test_tmp_*` probe sleeping 91 s against the real, unpatched
ceiling, beside a quick case, run once and deleted (§7):
`tests/test_tmp_ceiling_probe.py::test_tmp_sleeps_past_the_ceiling ran 91.0 s, over the 90 s ceiling (#841)`,
`1 failed, 1 passed in 91.06s`.

Each through `bin/mutation-check` over the new module:

| Break | Verdict |
|---|---|
| `<=` made `<` in `over_the_ceiling` | `red` |
| the seconds printed with no decimal | `red` |
| the hook sets `passed` where it sets `failed` | `red` |
| the hook also rewrites a call that failed on its own | `red` |
| `CASE_CEILING_S = 120` | `red` |
| the job's `timeout-minutes` line removed | `red` |
| ubuntu's `timeout` removed | `red` |

GitHub failing a job past its `timeout-minutes` is GitHub's, and `read`.

### Q8 before the confirming run

The last run measured is 37465328899 at 98b817ad, before this phase's
budget: the slowest Windows shard took 10 m 03 s, against 37-40 minutes on
0.19.0's pull requests and 36 m 03 s and 33 m 36 s on this branch's two
runs before the shards. The longest leg a pull request waits on is now
macOS, at 17 m 38 s. Windows meets Q1's 12 minutes with two minutes to
spare. The orchestrator's push of this phase is the confirming
run; its figures belong beside these, and a shard over 12 minutes there is
the runner swing above, which the 20-minute timeout absorbs.

### The confirming run, `executed` 2026-10-06

Run 37469595104 at d6587217, pull request #845's run with the budget in
place, green on every job. Read with `gh run view 37469595104 --json jobs`
and each job's log.

| Job | Wall time | Timeout | pytest's summary |
|---|---|---|---|
| windows, group 1 | 9 m 27 s | 20 | `2800 passed, 17 skipped in 524.67s` |
| windows, group 2 | 9 m 55 s | 20 | `6923 passed, 33 skipped in 550.81s` |
| windows, group 3 | 10 m 34 s | 20 | `918 passed, 104 skipped in 593.54s` |
| windows, group 4 | 10 m 15 s | 20 | `2203 passed, 53 skipped in 584.07s` |
| ubuntu | 9 m 03 s | 15 | `12972 passed, 79 skipped in 527.80s` |
| macOS | 20 m 52 s | 30 at that SHA | `12963 passed, 88 skipped in 1226.07s` |

- **The shards make the whole suite.** 12,844 passed and 207 skipped, 13,051
  cases, which is ubuntu's 13,051 and macOS's 13,051 at the same SHA. Against
  98b817ad's 13,046, the difference is the five cases of
  `tests/test_a_slow_case_names_itself.py`.
- **Every job finished under its timeout.**
- **No case failed the ceiling.** No log carries `over the 90 s ceiling`.
  The slowest call of the run is `test_no_shape_the_base_stops_reads_silent`
  at 55.77 s, in group 2.
- **The whole runner was slower again.** ubuntu took 9 m 03 s against 5 m
  40 s an hour earlier, and every Windows shard took 9 to 11 minutes where
  three of four had taken about 6. The split is balanced; the machines were
  not.

### Q6's rule applied again, with this run as a base

The runs after phase 4 are now four for ubuntu and macOS and two sharded
ones for Windows. This run is the slowest for ubuntu, macOS and the
Windows shards, and its 55.77 s is the slowest call:

| Value | New base | 1.5 times, rounded up | Before | Now |
|---|---|---|---|---|
| `CASE_CEILING_S` | 55.77 s, run 37469595104 | 83.7 s, to 90 | 90 | 90 |
| ubuntu | 9 m 03 s, run 37469595104 | 13.6, to 15 | 15 | 15 |
| macOS | 20 m 52 s, run 37469595104 | 31.3, to 35 | 30 | **35** |
| each Windows shard | 10 m 34 s, group 3 of run 37469595104 | 15.9, to 20 | 20 | 20 |

**macOS's timeout moves to 35 minutes, and it is the only value that
moves.** At 30 its margin over this run was 1.43 times, under the rule's
1.5: the rule no longer held with the slowest base. The commit after
d6587217 sets 35 and re-bases every comment on the runs that are now the
slowest: `test.yml`'s timeout comment and `CASE_CEILING_S`'s comment (whose
value does not change). The fragment and the S8 ledger row say 35.

**What this says about the rule.** Four runs of one day moved the macOS leg
between 16 m 27 s and 20 m 52 s, 1.27 times, and the Windows shards between
5 m 38 s and 10 m 34 s. A base taken from one run would already have been
broken by the next. The rule holds while it is re-applied to the slowest
run, which is what the comments now name; a fifth run slower than 20 m 52 s
by half again would still be stopped by GitHub, and that is the failure
direction the frame chose (*block more*).

### Q8: the leg after the work

Run 37469595104 at d6587217: the slowest Windows shard took 10 m 34 s,
against 37-40 minutes on 0.19.0's pull requests and 36 m 03 s and 33 m 36 s
on this branch before the shards. A pull request now waits longest on macOS,
20 m 52 s on this run. Windows meets Q1's 12 minutes on both sharded runs.

**Each shard's `--durations=50` table, run 37469595104.**

#### Group 1

    20.52s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_reason_the_checker_does_not_recognise_passes
    19.00s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_quiet_record_between_the_two_does_not_restart_the_count
    17.42s call     tests/test_a_finding_id_is_a_bare_integer.py::test_a_row_with_no_id_does_not_decide_pass
    17.31s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframed_record_is_written_and_starts_the_count_at_no[True]
    16.49s call     tests/test_a_gate_that_fails_says_so.py::test_json_a_gate_prints_that_is_not_a_hooks_output_ends_nothing
    15.60s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_record_after_an_unreframed_second_is_refused
    13.93s call     tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape
    11.31s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_second_landing_in_a_run_reads_second_and_prints_the_stop
    11.19s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_three_dot_range_resolves_through_the_merge_base
    10.22s call     tests/test_a_document_has_room_for_the_next_fold.py::test_this_repository_passes_the_command_with_no_flags
    9.87s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_run_that_removed_nothing_is_silent_and_says_what_it_read
    9.60s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[d2f2c0dc]
    9.22s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_whose_severity_commissions_nothing_does_not_land[\u2753]
    8.73s call     tests/test_a_fix_of_a_fix_is_counted.py::test_an_orphan_second_is_no_stop_to_the_generator
    8.71s call     tests/test_a_record_says_why_it_was_written_late.py::test_close_keeps_the_row_when_it_applies_the_fix_table
    8.26s call     tests/test_a_reference_root_is_read_and_never_taken.py::test_a_planted_team_specs_changes_no_checks_verdict
    8.13s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_re_add_on_a_side_branch_with_an_older_clock_is_the_latest_add
    7.94s call     tests/test_a_new_returnable_value_is_a_contract_change.py::test_the_derivation_agrees_with_an_independent_one_over_the_whole_tree
    7.58s call     tests/test_a_released_row_is_read_again_in_a_fragment.py::test_the_run_writes_the_same_bytes_in_any_ledger_order[six files]
    7.50s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_re_add_merged_back_from_a_side_branch_is_the_latest_add
    7.45s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[576fe39d]
    7.32s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_two_tied_sentences_on_one_line_print_in_one_order_whatever_the_hash_seed
    7.24s call     tests/test_a_fix_of_a_fix_is_counted.py::test_every_location_shape_that_carries_its_path_lands[`mod.py::u`]
    7.10s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_record_this_branch_did_not_add_makes_no_claim
    6.64s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_outside_the_units_the_fixes_wrote_reads_no
    6.63s setup    tests/test_a_fix_of_a_fix_is_counted.py::test_a_location_that_lands_in_no_written_unit_reads_no[`README.md`]
    6.60s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_measured_range_that_removed_three_rows_reports_nothing
    6.52s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_fix_sha_this_repository_cannot_see_makes_no_claim
    6.51s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_whose_severity_commissions_nothing_does_not_land[\u2b1c]
    6.40s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_depth_restarts_at_a_stop
    6.39s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_fixed_verdict_naming_no_commit_passes
    6.38s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_whose_severity_commissions_nothing_does_not_land[\U0001f7e2]
    6.33s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_the_report_already_closed_does_not_land
    6.32s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_inside_a_unit_the_fixes_changed_reads_first
    6.15s call     tests/test_a_fix_of_a_fix_is_counted.py::test_every_location_shape_that_carries_its_path_lands[`mod.py#u`]
    6.11s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_places_tied_on_score_print_in_path_order_whatever_the_hash_seed
    6.10s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_location_that_lands_in_no_written_unit_reads_no[`f.py#x` and `#w`, beside `mod.py#v`]
    6.05s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[cc49ae64]
    5.91s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_inside_a_unit_the_fixes_added_says_added
    5.89s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_fix_range_of_no_commits_lands_nowhere
    5.73s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_foreign_range_with_no_open_row_reads_no
    5.70s call     tests/test_a_fragment_left_behind_is_named.py::test_an_instruction_is_behaviour[agents/smith.md]
    5.70s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_record_restored_from_the_bases_history_makes_no_claim
    5.68s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_row_removed_while_its_anchors_resolve_stays_measured
    5.67s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_location_that_lands_in_no_written_unit_reads_no[`mod.py#v`; see #w]
    5.65s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_row_corrected_in_place_while_its_heading_is_retitled_is_a_correction
    5.64s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_path_order_does_not_decide_which_departure_is_the_source
    5.54s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[3dd24073]
    5.43s call     tests/test_a_finding_id_is_a_bare_integer.py::test_every_shape_the_corpus_holds_is_refused_by_name[1b]
    5.20s call     tests/test_a_finding_id_is_a_bare_integer.py::test_a_severity_marker_still_leads_the_cell[\U0001f7e1]

#### Group 2

    55.77s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_no_shape_the_base_stops_reads_silent
    37.47s call     tests/test_guard_resolves_the_tree_it_judges.py::test_nothing_the_base_read_as_a_switch_goes_quiet
    28.42s call     tests/test_settle_reads_before_it_removes.py::test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item
    18.35s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<<x git]
    17.83s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <>f git]
    17.71s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<EOF git]
    17.34s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<< x git]
    16.23s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_commit_found_before_a_nesting_too_deep_still_stops
    13.68s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_header_nesting_keeps_the_commits_found[f() { ]
    11.16s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_cd_behind_a_redirection_is_not_read_as_staying_put
    10.35s call     tests/test_guard_resolves_the_tree_it_judges.py::test_no_twin_is_asked_unless_an_operator_cuts_the_segment
    9.87s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[$(]
    9.80s call     tests/test_an_automation_run_meets_no_commit_prompt.py::test_without_the_press_the_answer_is_the_bases
    9.64s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_header_nesting_keeps_the_commits_found[case a in a) ]
    9.59s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[<(]
    9.29s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <f git]
    9.18s setup    tests/test_a_runner_reached_unit_reads_pytest_only.py::test_a_pytest_test_function_reads_pytest_only
    9.15s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: >&2 git]
    8.90s call     tests/test_an_automation_run_meets_no_commit_prompt.py::test_three_measured_shapes_are_refused_under_the_press
    8.81s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: >/dev/null git]
    7.95s call     tests/test_gate_judges_the_repo_it_commits_to.py::test_the_same_root_forms_answer_what_the_release_did
    7.82s call     tests/test_the_chain_goes_back_to_its_framer.py::test_the_three_values_pass
    7.61s call     tests/test_every_reader_ends_a_line_where_gfm_does.py::test_a_reports_quoted_character_survives_into_its_record
    7.41s call     tests/test_the_chain_goes_back_to_its_framer.py::test_the_floor_does_not_reach_across_a_second
    7.25s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: time cd]
    7.24s call     tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py::test_every_file_the_plugin_reads_or_writes_names_its_encoding
    7.23s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound["$(]
    7.13s call     tests/test_the_chain_goes_back_to_its_framer.py::test_without_the_second_the_same_tree_is_refused_by_the_floor
    7.11s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: cd $W unset]
    7.11s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2> /dev/null git]
    6.92s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2> >(tee log) git]
    6.84s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: &>f git]
    6.80s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: (bash -c) after a list]
    6.74s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2>&1 git]
    6.72s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2>/dev/null git]
    6.68s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: (sh -c)]
    6.42s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: >>log git]
    6.38s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: pushd]
    6.38s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: 2>&1 cd]
    6.38s call     tests/test_a_signers_ci_prints_its_pact.py::test_the_pacts_repository_prints_how_many_signers_it_lists
    6.33s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: builtin cd]
    6.29s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_header_nesting_keeps_the_commits_found[coproc ]
    6.20s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<-EOF git]
    6.15s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: $( ) in double quotes]
    6.11s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: command cd]
    6.05s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: $( )]
    6.03s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: !]
    6.02s call     tests/test_a_signers_ci_prints_its_pact.py::test_a_signer_prints_its_pact_and_its_exit_status_does_not_move[failing]
    5.97s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <( )]
    5.95s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <&0 git]

#### Group 3

    32.79s call     tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records
    14.14s call     tests/test_the_fixes_close_the_record.py::test_a_section_that_accounts_for_the_coordinates_under_an_earlier_round_is_silent
    11.85s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a redirected commit in $( )]
    11.22s call     tests/test_the_fixes_close_the_record.py::test_each_verdict_shape_is_written_and_read_back
    10.90s call     tests/test_the_guard_asks_once_per_session.py::test_the_order_of_a_switch_and_a_creation_does_not_decide
    10.08s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: a while condition]
    9.32s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: time]
    8.95s call     tests/test_the_hook_surface_git_offers.py::test_only_git_commit_hands_reference_transaction_an_author_date
    8.90s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_rider_check_never_leaves_both_readings
    8.84s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: inside a heredoc body a shell runs]
    8.80s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_config_reader_never_leaves_both_readings
    8.73s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a case arm]
    8.64s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r1: nice -C w, then $'\u2026']
    8.57s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_routing_reader_never_leaves_both_readings
    8.55s call     tests/test_the_guard_asks_once_per_session.py::test_a_command_with_both_is_never_weaker_than_either_alone
    8.50s call     tests/test_the_fixes_close_the_record.py::test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused
    8.39s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_a_commit_typed_while_a_rebase_is_paused_is_still_met
    8.35s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_where_the_walk_claims_to_be_exact_it_is
    8.28s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[position: followed by 2>&1 | tail]
    8.25s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: inside ${ }]
    8.24s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: >|f git]
    8.09s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: xargs -I]
    7.74s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: sh -c 2>&1]
    7.60s call     tests/test_the_hook_surface_git_offers.py::test_a_sequencer_that_stopped_on_a_conflict_commits_with_the_date
    7.56s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: a negation in a body]
    7.45s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: an if condition]
    7.41s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: then]
    7.41s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: a coprocess]
    7.41s call     tests/test_the_fixes_close_the_record.py::test_a_closed_record_reads_back_through_the_next_round
    7.38s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r1: do -C w, then $'\u2026']
    7.36s call     tests/test_the_fixes_close_the_record.py::test_the_documented_repair_still_closes
    7.30s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r1: timeout -C w, then $'\u2026']
    7.12s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: xargs sh -c]
    7.11s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a function body]
    7.06s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a shell string inside a substitution]
    6.99s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a coprocess]
    6.69s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_concluding_a_conflicted_merge_is_judged
    6.68s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: timeout]
    6.63s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a command in the string behind a list opener]
    6.60s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: env -S glued]
    6.60s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a while condition]
    6.54s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r2: mv, then cd, on lines]
    6.50s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r2: perl -e after the heredoc]
    6.49s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: inside an arithmetic expansion]
    6.49s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: strace]
    6.48s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: a group in a body]
    6.48s call     tests/test_the_fixes_close_the_record.py::test_a_correction_closed_answered_lands_on_no_fixes_to_check
    6.46s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r3: perl, # glued]
    6.46s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r2: ${...;...} before it]
    6.45s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: elif]

#### Group 4

    22.70s setup    tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_repository_shipping_no_gate_runs_the_invoked_copy
    17.45s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed
    16.93s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_pull_request_the_record_names_reaches_the_values_file
    16.69s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_run_with_no_session_says_so_and_names_the_hand_command
    16.60s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_reads_the_real_seals_two_endings_apart
    16.32s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_values_that_cannot_be_written_leave_the_seal_standing
    13.47s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry
    12.72s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_keeps_the_earlier_run_and_the_reader_takes_the_newest
    12.64s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_fixed_at_verdict_in_a_verifying_round_fails_the_preflight
    12.55s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_capped_run_is_sealed_with_its_deferral_on_the_stamp
    12.52s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_settled_item_preflights_green_and_names_the_record_it_asked
    12.52s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_runners_event_payload_judges_the_fixture_and_fails_its_gate
    11.70s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_writes_the_last_records_cell_and_nothing_else
    11.14s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_first_runner_without_the_gates_environment_costs_the_word
    10.77s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_direct_declaration_seals_into_its_own_home_even_with_rounds
    10.28s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_generated_unread_fixes_fail_the_preflight_at_seal
    10.11s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_work_item_with_rounds_still_seals_onto_its_last_record
    9.56s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_root_run_row_measures_the_module_the_branch_added[xdist]
    9.22s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_cd_rows_shared_and_new_files_each_get_a_measured_word[xdist]
    9.18s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_file_the_base_fails_only_alone_is_not_called_failing_on_base_too[a-file-with-no-count-alone]
    9.17s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_the_write_path_refuses[open-comment]
    9.07s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_at_the_same_commit_against_another_base_keeps_both
    8.90s call     tests/test_the_record_is_held_to_the_floor_and_the_depth.py::test_the_floors_refusal_names_both_stops_and_refuses_the_false_way_out
    8.86s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_the_write_path_refuses[two-rows]
    8.54s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_the_write_path_refuses[no-row]
    8.52s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_an_inner_run_on_stderr_under_s_is_not_read_as_the_runs_own[xdist]
    8.37s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_refuses_a_sha_the_target_descends_from
    8.35s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_passes_what_seal_would_seal_and_writes_nothing[settled]
    8.35s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_seal_refuses_and_writes_nothing[spent-sha]
    8.31s call     tests/test_the_printed_ledger_name_is_the_file_that_was_read.py::test_the_refusal_above_can_actually_fail
    8.31s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_what_a_test_printed_is_not_read_as_pytests_own_lines[an-inner-empty-run-xdist]
    8.18s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_line_is_absent_where_the_cells_file_is_committed
    8.18s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[Q5-own]
    8.01s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_cd_rows_file_the_root_carries_differently_is_run_at_the_base[xdist]
    8.00s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_refuses_a_cell_with_no_sha_in_it
    7.99s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_person_at_a_terminal_sees_the_stamp_drawn_once
    7.91s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[N1-xdist-own]
    7.77s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_file_the_base_fails_alone_is_proven_by_one_session_listing_it[xdist]
    7.74s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_row_that_runs_pytest_twice_gives_no_permissive_word[Q8-a-first-runner-with-its-own-report]
    7.61s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_row_that_runs_pytest_twice_gives_no_permissive_word[p1b]
    7.57s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_with_record_prints_no_stamp_when_the_record_refuses
    7.55s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[N1-xdist-files]
    7.53s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_root_run_row_measures_the_module_the_branch_added[plain]
    7.50s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_run_of_several_that_counted_only_warnings_sends_each_file_alone[xdist]
    7.44s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_preflight_with_record_is_refused_and_writes_no_cell
    7.43s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_what_a_test_printed_is_not_read_as_pytests_own_lines[an-inner-empty-run-plain]
    7.34s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[Q5-files]
    7.33s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[N7-own]
    7.25s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_what_a_test_printed_is_not_read_as_pytests_own_lines[an-inner-failed-line-xdist]
    7.15s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_first_seal_is_byte_identical_to_a_cell_that_was_never_a_list


### The ledger

One row per scenario, S1, S2 and S4 to S9 (S3 withdrawn), appended to
`seal/ledger/1791270165-…md` with `@00000000` and stamped by `evidence-check
--reverify --ledger <the fragment> --checked 2026-10-06`. `evidence-check
--strict .` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
