# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | the record's commit, named in `plan.md`'s Status (the shards are 340dc6fa and 65c8ed98) |
| Ran by | smith on Opus 5.5 (a second smith, on another machine) |

## What this phase was asked

Two halves, each a spawn of its own. The first: make the Windows leg write
`.test_durations` with `pytest-split`'s `--store-durations` and upload it as
an artifact, with `pytest-split` on the pip line and the pins of Q9 kept
green, and shard nothing. The second, once that push's run finished: download
the artifact from run 37458654434, read the Windows tables and counts of that
run and of run 37457228586 (the last run before the shards, S4), compute `K`
against Q1's default (the slowest shard at or under 12 minutes), and commit
the durations file and the Windows shard matrix, with every new or changed
case seen red. The sharded run on the pull request is the confirming
measurement, and the orchestrator starts it.

## What this phase found

### The two runs, `executed` 2026-10-06

Both are pull request #845's runs, both green on every job. Read with
`gh run view <id> --json jobs` and `gh run view --job <id> --log`.

| Run | SHA | What it is | Windows job | Windows pytest summary | ubuntu job | macOS job |
|---|---|---|---|---|---|---|
| 37457228586 | 922ded29 | the leg after 4b, the last run before the shards (S4) | 36 m 03 s | `12836 passed, 206 skipped in 2132.60s` | 6 m 40 s, `12961 passed, 81 skipped in 385.25s` | 19 m 52 s, `12954 passed, 88 skipped in 1166.87s` |
| 37458654434 | 8a69b393 | the same suite with `--store-durations` on Windows | 33 m 36 s | `12836 passed, 206 skipped in 1973.63s` | 7 m 58 s, `12963 passed, 79 skipped in 463.38s` | 16 m 27 s, `12955 passed, 87 skipped in 964.15s` |

**S4's baseline is 12,836 passed and 206 skipped**, 13,042 cases, on both
runs. The four shards' counts have to sum to that, less whatever a case
added since then (this phase adds three: the new module below).

**The Windows table, top lines of each run.** The same cases lead both, in
nearly the same order:

| Case | 37457228586 | 37458654434 | run 37429940700 (phase 1) |
|---|---|---|---|
| `test_no_shape_the_base_stops_reads_silent` | 55.13 s | 52.49 s | 36.44 s |
| `test_nothing_the_base_read_as_a_switch_goes_quiet` | 37.19 s | 36.24 s | 25.12 s |
| `test_the_guard_is_never_silent_where_the_writer_records` | 34.62 s | 31.73 s | 23.27 s |
| `test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item` | 29.86 s | 29.12 s | 17.14 s |
| `test_a_reason_the_checker_does_not_recognise_passes` | 28.18 s | 25.91 s | 20.36 s |
| the top 50, summed | 828.9 s | 758.5 s | 652.4 s |

### The runner varies more than 4b moved anything

The case at the top of the table did not change between be8a4115 and
922ded29, and it ran 36.4 s in phase 1's run and 55.1 s and 52.5 s in these
two. The leading cases are 1.4 to 1.7 times phase 1's figures across the
board, and the whole Windows leg took 1,791 s of pytest time then against
2,133 s and 1,974 s now. The ubuntu and macOS legs moved the same way (352 s
then, 385 s and 463 s now; 793 s then, 1,167 s and 964 s now). A slowdown
that uniform, on cases nobody edited, is the runner and not the suite.

**What this means for 4b.** Its effect on the Windows leg cannot be read
off these runs: whatever it saved is smaller than the swing between two runs
of the same day. `phases/phase-4.md` stated its bound from phase 1's table
(at most 2.7 minutes), and that stands as the only figure.

**Whether the two runs' overlap coloured them.** They overlapped from 11:46
to 12:09 UTC. Each GitHub-hosted job runs on a fresh virtual machine of its
own (`read`, from GitHub's documentation of hosted runners), so our two runs
did not share a machine. That they agree with each other within 8% and both
sit well above phase 1's run points the same way: the variation is between
runner hosts or times, and the overlap is not its cause. Nothing here can
rule out a slower host pool at that hour.

**What it means for phase 5.** Q6's rule sets the budget at 1.5 times the
measured figure. The same code just measured 1.19 times slower from one run
to the next on Windows (2,133 s against 1,791 s), and per case up to 1.7
times. A budget at 1.5 times one run's figure would sit at the edge of that
swing; phase 5 should take the slower of several runs as its base, and this
phase's two runs are two of them.

### `K`, from the durations file

The artifact `test-durations-windows-latest` of run 37458654434 holds
13,042 cases summing to 7,530 s of setup, call and teardown. The leg ran
that in 1,973.63 s of pytest time, 1.05 times 7,530 / 4: four xdist workers
(`read`: GitHub gives a hosted `windows-latest` four cores, and the log names
`[gw2]`) kept almost fully busy. Around pytest, the job spent 37 s on
checkout, Python and the pip install, and about 25 s more from the step's
start to the first case.

`pytest-split`'s default algorithm, `duration_based_chunks`, divides the · NAME NOT IN TREE
cases in collection order, so a module stays in one shard and its session
fixtures, 4b's templates among them, are built once there. Run offline over
this file (`executed`, the algorithm imported from the 0.11.0 wheel), it
gives groups within 0.2% of each other:

| `K` | worker-seconds per group | a shard's job, on run 37458654434's pace | on run 37457228586's pace (1.08 times slower) |
|---|---|---|---|
| 3 | 2,508 to 2,513 | 37 + 25 + 1,949 / 3 = 712 s, 11.9 min | 765 s, 12.8 min |
| 4 | 1,881 to 1,884 | 37 + 25 + 1,949 / 4 = 549 s, 9.2 min | 589 s, 9.8 min |
| 5 | 1,498 to 1,510 | 452 s, 7.5 min | 484 s, 8.1 min |

**`K` is 4.** Three meets Q1's 12 minutes on the faster run only, and by
seconds; four meets it on both with two minutes to spare, which is the
smallest count that does. Five buys another 1.7 minutes for one more
runner's 62 s of fixed cost. The slowest single case, 52.5 s, is far under
any shard.

### What was built

- `.github/workflows/test.yml`: four Windows entries carrying
  `split: "--splits 4 --group <g>"`, the pytest line ending in
  `${{ matrix.split }}`, empty on ubuntu and macOS, which stay one job
  each. The first half's `store` entry and its upload step are gone: the
  file they produced is committed, and storing it again is a one-run change
  of the same two lines (below).
- `.test_durations` at the repository root, the artifact as downloaded, with
  its CRLF line ends made LF (`.gitattributes` says `eol=lf`) and nothing
  else changed: 13,042 entries, ASCII, no user path but `/Users/x/`.
- `CONTRIBUTING.md` §*Running the checks*: the CI sentence counts the shards.
- `tests/test_the_windows_leg_runs_in_shards_that_make_the_whole.py`, three
  cases: every Windows entry is a shard of one count `K`, its groups are 1 to
  `K` exactly once, no other leg carries a split; the pytest line ends in the
  split; the durations file parses and names `tests/…::…` cases with
  non-negative seconds.
- `tests/test_the_release_check_watches_what_ships.py`: `.test_durations`
  classified as staying home. The case went red on the new top-level entry in
  the narrow run before this line was added, which is its red.

**Refreshing the file.** It goes stale as cases are added. A stale file
unbalances the shards and drops nothing: a case it does not name is given
the average and runs in one shard. To refresh, one run of the Windows leg
unsharded with `--store-durations` and the upload step of 43326715, then the
file is downloaded and committed. Phase 5's per-case ceiling and the shards'
own `--durations` tables say when it is due.

### Seen red, `executed` 2026-10-06

Each through `bin/mutation-check` over the new module:

| Break | Verdict |
|---|---|
| group 4 named as group 3 | `red`: the groups case |
| one entry saying `--splits 5` | `red`: the groups case |
| ubuntu given a split | `red`: the groups case |
| `${{ matrix.split }}` dropped from the pytest line | `red`: the line case |
| a node id in the file without `tests/` and `::` | `red`: the file case |
| the file's opening `{` made `[` | `red`: the file case |

The first half's extension of `test_ci_installs_the_parser_the_runner_pins`
was seen red the same way, three times: the pip line's version changed to
0.10.0, `pytest-split` dropped from the line, and `PYTEST_SPLIT` put into
`PACKAGES`.

**Narrow runs.** Every module that reads `.github/workflows/`,
`run_tests.py`, `CONTRIBUTING.md` or the tracked tree (60 modules):
`1 failed, 4117 passed, 8 skipped`, the one being the classification above;
after it, that module and the new one: `40 passed`. Exit codes read
directly. `ruff check` and `ruff format --check` exit 0 on every Python file
touched.

### What the confirming run must show (S4)

The sharded run's four Windows jobs: each one's `passed` and `skipped`,
summing to 12,836 and 206 plus the three new cases; each job's wall time,
the slowest at or under 12 minutes; and each shard's `--durations=50`
table, which phase 5 reads for its ceiling. If a shard collects a different
suite from the others, xdist and `pytest-split` will say so at collection.

### The sharded run, `executed` 2026-10-06 — S4

Run 37465328899 at 98b817ad, pull request #845's run, green on every job.
Read with `gh run view 37465328899 --json jobs` and each job's log.

| Job | Wall time | pytest's summary |
|---|---|---|
| windows, group 1 | 6 m 22 s | `2798 passed, 17 skipped in 355.31s` |
| windows, group 2 | 5 m 57 s | `6920 passed, 33 skipped in 328.94s` |
| windows, group 3 | 10 m 03 s | `917 passed, 105 skipped in 567.98s` |
| windows, group 4 | 5 m 38 s | `2203 passed, 53 skipped in 313.15s` |
| ubuntu | 5 m 40 s | `12967 passed, 79 skipped in 324.32s` |
| macOS | 17 m 38 s | `12959 passed, 87 skipped in 1034.86s` |

**The four shards make the whole suite.** They ran 12,838 passed and 208
skipped, 13,046 cases, which is ubuntu's 13,046 at the same SHA. Against the
last unsharded run, 13,042 (12,836 and 206), the difference is the four
cases 98b817ad's range added: the new module's three and one more parameter
of `test_nothing_that_stays_home_is_watched`, for `.test_durations`. The
split between passed and skipped is not the invariant: the same leg's skip
count moves between runs of one suite (ubuntu read 81 and 79 on the two
runs above), so S4 is read on the total. `pytest-split` gives each shard a
disjoint part, so a total equal to the whole suite's means no case ran twice
and none ran nowhere (`read`, from its `plugin.py`; nothing in the logs
lists every case).

**The slowest shard is 10 m 03 s, under Q1's 12 minutes.** The Windows
pull request wait went from 36 m 03 s and 33 m 36 s, the two runs before
the shards, to 10 m 03 s. macOS is now the slowest leg at 17 m 38 s.

**Group 3 was slow because its runner was.** The groups were balanced to
within 0.2% by the file, and three of them finished in 5 m 38 s to 6 m
22 s. On the cases in each group's table, groups 1, 2 and 4 ran at 0.63 to
0.68 of the file's figures and group 3 at 1.11: the same kind of case, 1.6
to 1.8 times slower on one of four machines in one run. That is the same
runner swing phase 3's first runs showed, now inside a single run, and it
is the figure phase 5's budget has to absorb.

**Each shard's `--durations=50` table.**

#### Group 1

    15.89s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_reason_the_checker_does_not_recognise_passes
    15.03s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_reframed_record_is_written_and_starts_the_count_at_no[True]
    14.00s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_quiet_record_between_the_two_does_not_restart_the_count
    13.33s call     tests/test_a_finding_id_is_a_bare_integer.py::test_a_hand_edited_record_still_meets_the_rule_at_close
    10.11s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_second_landing_in_a_run_reads_second_and_prints_the_stop
    9.71s call     tests/test_a_folded_statement_names_what_enforces_it.py::test_every_bound_statement_in_docs_has_the_shape
    9.70s call     tests/test_a_document_has_room_for_the_next_fold.py::test_this_repository_passes_the_command_with_no_flags
    9.60s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_run_that_removed_nothing_is_silent_and_says_what_it_read
    9.51s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_three_dot_range_resolves_through_the_merge_base
    8.12s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[d2f2c0dc]
    7.49s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_record_after_an_unreframed_second_is_refused
    7.39s call     tests/test_a_new_returnable_value_is_a_contract_change.py::test_the_derivation_agrees_with_an_independent_one_over_the_whole_tree
    6.92s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[576fe39d]
    6.15s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_declaration_does_not_reach_a_work_item_that_did_not_write_it
    6.00s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[cc49ae64]
    5.96s call     tests/test_a_released_row_is_read_again_in_a_fragment.py::test_the_run_writes_the_same_bytes_in_any_ledger_order[six files]
    5.75s call     tests/test_a_gate_that_fails_says_so.py::test_json_a_gate_prints_that_is_not_a_hooks_output_ends_nothing
    5.63s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_four_real_ranges_report_their_prose_and_none_of_their_code[3dd24073]
    5.57s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_two_tied_sentences_on_one_line_print_in_one_order_whatever_the_hash_seed
    5.46s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_the_measured_range_that_removed_three_rows_reports_nothing
    5.32s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_places_tied_on_score_print_in_path_order_whatever_the_hash_seed
    5.25s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_outside_the_units_the_fixes_wrote_reads_no
    5.19s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_whose_severity_commissions_nothing_does_not_land[\u2b1c]
    5.05s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_inside_a_unit_the_fixes_changed_reads_first
    4.91s call     tests/test_a_fix_of_a_fix_is_counted.py::test_every_location_shape_that_carries_its_path_lands[`mod.py#u`]
    4.86s call     tests/test_a_fix_of_a_fix_is_counted.py::test_every_location_shape_that_carries_its_path_lands[`mod.py::u`]
    4.82s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_the_report_already_closed_does_not_land
    4.68s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_fixed_verdict_naming_no_commit_passes
    4.64s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_inside_a_unit_the_fixes_added_says_added
    4.48s call     tests/test_a_fix_of_a_fix_is_counted.py::test_an_orphan_second_is_no_stop_to_the_generator
    4.37s call     tests/test_a_fragment_left_behind_is_named.py::test_each_commit_is_attributed_to_the_range_that_holds_it
    3.89s call     tests/test_a_fragment_left_behind_is_named.py::test_of_several_merged_heads_the_one_descending_from_round_one_is_the_tip
    3.74s call     tests/test_a_reference_root_is_read_and_never_taken.py::test_a_planted_team_specs_changes_no_checks_verdict
    3.69s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_re_add_on_a_side_branch_with_an_older_clock_is_the_latest_add
    3.46s setup    tests/test_a_fix_of_a_fix_is_counted.py::test_a_location_that_lands_in_no_written_unit_reads_no[`README.md`]
    3.40s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_whose_severity_commissions_nothing_does_not_land[\U0001f7e2]
    3.28s call     tests/test_a_finding_id_is_a_bare_integer.py::test_a_severity_marker_still_leads_the_cell[\u2b1c]
    3.24s call     tests/test_a_fix_of_a_fix_is_counted.py::test_the_depth_restarts_at_a_stop
    3.23s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_record_deleted_and_re_added_after_the_fix_is_judged_on_the_later_add
    3.21s call     tests/test_a_fragment_left_behind_is_named.py::test_a_commit_after_the_last_round_says_so[True]
    3.20s call     tests/test_a_fragment_left_behind_is_named.py::test_only_the_commits_after_the_fragments_last_change_are_named
    3.18s call     tests/test_a_record_precedes_the_fixes_it_commissions.py::test_a_re_add_merged_back_from_a_side_branch_is_the_latest_add
    3.12s call     tests/test_a_fragment_left_behind_is_named.py::test_the_ci_merge_ref_names_the_items_commit_and_not_the_siblings[True]
    3.11s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_a_reworded_sentence_reports_the_pin_it_left_behind
    3.09s call     tests/test_a_fragment_left_behind_is_named.py::test_an_honest_fragment_on_the_ci_merge_ref_is_not_named
    3.09s call     tests/test_a_fragment_left_behind_is_named.py::test_a_merge_on_the_branch_keeps_the_branch_as_the_tip
    3.08s call     tests/test_a_finding_id_is_a_bare_integer.py::test_every_no_digit_shape_the_corpus_holds_is_admitted[\u2705]
    3.06s call     tests/test_a_corrected_sentence_survives_elsewhere.py::test_an_exemption_whose_quote_is_gone_stops_holding
    2.97s call     tests/test_a_fix_of_a_fix_is_counted.py::test_a_finding_whose_severity_commissions_nothing_does_not_land[\u2753]
    2.95s call     tests/test_a_finding_id_is_a_bare_integer.py::test_a_severity_marker_still_leads_the_cell[\U0001f534]

#### Group 2

    29.91s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_no_shape_the_base_stops_reads_silent
    20.43s call     tests/test_guard_resolves_the_tree_it_judges.py::test_nothing_the_base_read_as_a_switch_goes_quiet
    14.60s call     tests/test_settle_reads_before_it_removes.py::test_no_row_of_this_repositorys_ledger_anchors_inside_a_work_item
    9.91s call     tests/test_a_signers_ci_prints_its_pact.py::test_a_pact_headed_as_0_18_wrote_it_is_counted_and_the_rename_named[failing]
    7.60s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_commit_found_before_a_nesting_too_deep_still_stops
    7.04s call     tests/test_every_reader_ends_a_line_where_gfm_does.py::test_a_reports_quoted_character_survives_into_its_record
    6.69s call     tests/test_a_signers_ci_prints_its_pact.py::test_a_pact_headed_as_0_18_wrote_it_is_counted_and_the_rename_named[passing]
    6.60s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_header_nesting_keeps_the_commits_found[f() { ]
    6.36s setup    tests/test_a_runner_reached_unit_reads_pytest_only.py::test_a_pytest_test_function_reads_pytest_only
    5.79s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_cd_behind_a_redirection_is_not_read_as_staying_put
    5.63s call     tests/test_an_automation_run_meets_no_commit_prompt.py::test_without_the_press_the_answer_is_the_bases
    5.32s call     tests/test_guard_resolves_the_tree_it_judges.py::test_no_twin_is_asked_unless_an_operator_cuts_the_segment
    4.96s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_header_nesting_keeps_the_commits_found[case a in a) ]
    4.94s call     tests/test_an_automation_run_meets_no_commit_prompt.py::test_three_measured_shapes_are_refused_under_the_press
    4.90s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<EOF git]
    4.84s call     tests/test_chain_check_at_the_pull_request.py::test_a_clean_copy_in_the_working_tree_cannot_hide_a_committed_failure
    4.76s call     tests/test_gate_judges_the_repo_it_commits_to.py::test_the_same_root_forms_answer_what_the_release_did
    4.72s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <>f git]
    4.72s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<<x git]
    4.66s call     tests/test_the_chain_goes_back_to_its_framer.py::test_without_the_second_the_same_tree_is_refused_by_the_floor
    4.62s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2> >(tee log) git]
    4.56s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <f git]
    4.54s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2>&1 git]
    4.52s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: command cd]
    4.47s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: time cd]
    4.46s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[$(]
    4.43s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2>/dev/null, then an assignment]
    4.39s call     tests/test_no_shape_the_base_stops_reads_silent.py::test_a_deep_nesting_is_read_to_a_bound[<(]
    4.29s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: 2>&1 cd]
    4.27s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: builtin cd]
    4.24s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <( )]
    4.16s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2> /dev/null git]
    4.09s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: << EOF git]
    4.07s call     tests/test_arm_check.py::test_a_command_that_never_returns_is_recorded_as_unmeasured
    4.07s call     tests/test_arm_check.py::test_the_report_does_not_call_a_mutated_arm_unmutated[every pair times out]
    3.99s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<-EOF git]
    3.99s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: cd $W unset]
    3.97s call     tests/test_the_chain_goes_back_to_its_framer.py::test_the_floor_does_not_reach_across_a_second
    3.90s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <&0 git]
    3.86s call     tests/test_a_signers_ci_prints_its_pact.py::test_the_pacts_repository_prints_how_many_signers_it_lists
    3.82s setup    tests/test_guard_resolves_the_tree_it_judges.py::test_every_name_git_moves_the_tree_on_is_read_as_a_switch[C1 a branch, checkout --detach N]
    3.81s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: !]
    3.80s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[#686 ;: pushd]
    3.79s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: 2>/dev/null git]
    3.76s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: $( )]
    3.75s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: (bash -c) after a list]
    3.75s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: <<< x git]
    3.74s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: (sh -c)]
    3.73s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: >&2 git]
    3.72s call     tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py::test_every_file_the_plugin_reads_or_writes_names_its_encoding

#### Group 3

    33.70s call     tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records
    13.85s call     tests/test_the_fixes_close_the_record.py::test_a_section_that_accounts_for_the_coordinates_under_an_earlier_round_is_silent
    11.87s call     tests/test_the_fixes_close_the_record.py::test_each_verdict_shape_is_written_and_read_back
    10.61s call     tests/test_the_guard_asks_once_per_session.py::test_the_order_of_a_switch_and_a_creation_does_not_decide
    10.42s call     tests/test_the_fixes_close_the_record.py::test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused
    8.83s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: inside a heredoc body a shell runs]
    8.82s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a case arm]
    8.67s call     tests/test_the_fixes_close_the_record.py::test_a_finding_the_report_already_closed_needs_no_row
    8.59s call     tests/test_the_gate_names_every_step_ci_runs.py::test_the_same_branch_against_its_release_branch_is_not_sealed
    8.53s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r1: nice -C w, then $'\u2026']
    8.31s call     tests/test_the_hook_surface_git_offers.py::test_only_git_commit_hands_reference_transaction_an_author_date
    8.24s call     tests/test_the_guard_asks_once_per_session.py::test_a_command_with_both_is_never_weaker_than_either_alone
    7.69s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: inside ${ }]
    7.67s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: >|f git]
    7.67s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: xargs -I]
    7.51s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[position: followed by 2>&1 | tail]
    7.42s call     tests/test_the_fixes_close_the_record.py::test_a_correction_closed_answered_lands_on_no_fixes_to_check
    7.41s call     tests/test_the_fixes_close_the_record.py::test_a_row_that_commissions_nothing_does_not_stop_the_reach
    7.35s call     tests/test_the_hook_surface_git_offers.py::test_a_sequencer_that_stopped_on_a_conflict_commits_with_the_date
    7.26s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_rider_check_never_leaves_both_readings
    7.22s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_where_the_walk_claims_to_be_exact_it_is
    7.20s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: a coprocess]
    7.15s call     tests/test_the_fixes_close_the_record.py::test_the_reach_forward_refuses_a_coordinate_the_verdict_table_lacks
    7.11s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_routing_reader_never_leaves_both_readings
    7.05s call     tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_config_reader_never_leaves_both_readings
    7.03s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r1: timeout -C w, then $'\u2026']
    7.00s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r1: do -C w, then $'\u2026']
    7.00s call     tests/test_the_fixes_close_the_record.py::test_a_repeated_coordinate_resolves_to_one_row_on_both_sides
    6.87s call     tests/test_the_fixes_close_the_record.py::test_a_closed_record_reads_back_through_the_next_round
    6.86s call     tests/test_the_fixes_close_the_record.py::test_the_documented_repair_still_closes
    6.77s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_a_commit_typed_while_a_rebase_is_paused_is_still_met
    6.64s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[position: P5, behind 2>/dev/null]
    6.64s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: git 2>&1 commit]
    6.62s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r2: $(...) before the interpreter]
    6.49s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: a group in a body]
    6.42s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: an assignment's value]
    6.40s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: elif]
    6.40s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r3: # glued to the delimiter]
    6.39s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: a subshell in a body]
    6.35s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[shape: strace]
    6.29s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a spaced subshell]
    6.29s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: bash -c]
    6.27s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r2: control, a missing cd]
    6.26s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r2: a bundled -Bc]
    6.25s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: a group]
    6.19s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: env -S]
    6.18s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r2: mv, then cd]
    6.18s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: inside an arithmetic expansion]
    6.12s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[ns: r3: an invalid name prefix]
    6.11s call     tests/test_the_commit_gate_decides_at_the_commit.py::test_s2_a_commit_bash_makes_into_an_undeclared_repository_does_not_land[handed: command]

#### Group 4

    9.73s setup    tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_with_record_seals_the_item_and_counts_its_rounds
    9.44s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_run_with_no_session_says_so_and_names_the_hand_command
    9.26s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_pull_request_the_record_names_reaches_the_values_file
    9.17s setup    tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing
    9.09s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_values_that_cannot_be_written_leave_the_seal_standing
    9.01s setup    tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_repository_shipping_no_gate_runs_the_invoked_copy
    8.75s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_gate_reads_the_real_seals_two_endings_apart
    8.51s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_fixed_at_verdict_in_a_verifying_round_fails_the_preflight
    8.22s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry
    8.02s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_runners_event_payload_judges_the_fixture_and_fails_its_gate
    7.71s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_settled_item_preflights_green_and_names_the_record_it_asked
    7.61s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_keeps_the_earlier_run_and_the_reader_takes_the_newest
    7.60s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed
    7.51s call     tests/test_the_record_is_generated.py::test_the_target_is_the_flag_and_it_has_to_resolve
    6.88s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_part_that_is_not_pytest_is_passed_over_though_it_prints_counts
    6.77s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_re_seal_at_the_same_commit_against_another_base_keeps_both
    6.65s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_first_runner_without_the_gates_environment_costs_the_word
    6.46s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_capped_run_is_sealed_with_its_deferral_on_the_stamp
    6.29s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_work_item_with_rounds_still_seals_onto_its_last_record
    6.16s call     tests/test_the_record_is_generated.py::test_a_record_reading_the_reopenings_fixes_says_it_ends_the_run
    5.98s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_generated_unread_fixes_fail_the_preflight_at_seal
    5.75s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_writes_the_last_records_cell_and_nothing_else
    5.63s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_cd_rows_shared_and_new_files_each_get_a_measured_word[xdist]
    5.63s call     tests/test_the_record_is_generated.py::test_prose_below_the_terminal_block_is_not_swallowed
    5.56s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_first_seal_is_byte_identical_to_a_cell_that_was_never_a_list
    5.26s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_direct_declaration_seals_into_its_own_home_even_with_rounds
    5.24s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[P3-no-junitxml-files]
    5.15s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_person_at_a_terminal_sees_the_stamp_drawn_once
    5.13s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_seal_refuses_and_writes_nothing[spent-sha]
    5.12s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_the_write_path_refuses[two-rows]
    5.10s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_root_run_row_measures_the_module_the_branch_added[xdist]
    5.01s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_what_a_test_printed_is_not_read_as_pytests_own_lines[an-inner-empty-run-xdist]
    4.92s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_preflight_with_record_is_refused_and_writes_no_cell
    4.90s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_the_write_path_refuses[open-comment]
    4.89s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_refuses_what_the_write_path_refuses[no-row]
    4.77s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[N1-xdist-files]
    4.76s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_check_passes_what_seal_would_seal_and_writes_nothing[settled]
    4.73s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_refuses_a_cell_with_no_sha_in_it
    4.65s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[P3-no-junitxml-own]
    4.57s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_seal_refuses_a_sha_the_target_descends_from
    4.52s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_failing_test_is_not_sealed_and_is_new_when_the_base_passes
    4.50s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[Q5-own]
    4.48s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_an_inner_run_on_stderr_under_s_is_not_read_as_the_runs_own[xdist]
    4.42s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives[N1-xdist-own]
    4.41s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_file_the_base_holds_no_test_in_reads_new[xdist]
    4.39s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_line_is_absent_where_the_cells_file_is_committed
    4.37s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_the_wrapper_runs_the_same_gate
    4.35s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_cd_rows_file_the_root_carries_differently_is_run_at_the_base[xdist]
    4.32s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_file_the_base_fails_alone_is_proven_by_one_session_listing_it[xdist]
    4.22s call     tests/test_the_seal_is_taken_once_by_the_sealer.py::test_a_row_that_runs_pytest_twice_gives_no_permissive_word[Q8-a-first-runner-with-its-own-report]


## What this phase removes

| Removed item | Where it must land |
|---|---|
| The one unsharded Windows job | the four shard entries of the same matrix |
| The first half's `store` entry and its upload step (43326715) | `.test_durations`, committed; the refresh above names the two lines to put back for one run |
