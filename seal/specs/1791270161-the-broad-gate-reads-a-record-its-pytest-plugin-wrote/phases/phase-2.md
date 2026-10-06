# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 1bc4fb42 |
| Ran by | smith on Opus 5.5 (filled by the orchestrating session; the spawn prompt named neither) |

## What this phase was asked

Phase 2 of `plan.md`, from `handoff.md`'s list: `recording_env`,
`read_record`, the `HEAD` run recording with the `FAILED`-line fallback,
`compare_at_base` rewritten to one base run and the five-row table, the
retirements of `spec.md` Scope 7; in the same commit rule 3, the **New?**
bullet and their pins. Re-read the roughly sixty end-to-end cases into this
record (Q-W1), run Q-W3's grep before the retirement commit, and decide
Q-W2, whose default no longer fit because the recorder holds no three-part
version token. Q1 stays the owner's and its default (a), strict `new?`, is
what gets built. No push, no pull request, nothing posted; the modules
touched are run, never the whole suite.

## What this phase found

**Does the frame hold? Mostly, and one reading does not.** `spec.md`
§*The class* and `plan.md` Alternative A read a row that sets `PYTHONPATH`
itself as a row that merely loses the recorder (`new?`). Measured before the
first edit, in a scratch project on pytest 9.1 with `PYTEST_ADDOPTS="-p
specseal_pytest_record"` and `PYTHONPATH=/nonexistent`: pytest stops with
`ModuleNotFoundError: No module named 'specseal_pytest_record'` and exits 1
before any test runs. Such a row fails at the gate though every test passes.
Built as measured: rule 3 names it and the remedy (add to the variable),
`test_a_row_that_replaces_pythonpath_cannot_load_the_recorder` holds it, and
`questions.md` Q2 asks the owner whether that is the trade. S13's second
layout uses a row that sets `PYTEST_ADDOPTS` instead, which does lose only
the recorder. Two smaller readings of the spec did not hold either and are
divergence rows in `overview.md`: S12's lone `env -i` runner reads
`NO_RECORD_AT_HEAD`, not `NO_RECORD`; and a part after the runner runs at the
base only where the base's suite passes.

**Files are named from the repository root now, and that moves every `cd`
case.** The record carries absolute paths, so a `cd sub` row's failing file
is `sub/tests/test_two.py` on the branch and at the base alike, where pytest's
`FAILED` line named it `tests/test_two.py`. The #761 class — a root file
sharing the name — has no instance left under this naming.

**Q-W1, every end-to-end case over the comparison, with its word at
a9d7b0e5 and now.** `on` is `failing on base too`. The row is the table's
(`compare_at_base`'s docstring): *failing* — a failing test or failed
collection in the base's record; *collected* — collected, nothing failed;
*absent, exit 0*; *absent, exit N* — `NOT_REACHED`; *no base record* —
`NO_RECORD`; *no head record* — `NO_RECORD_AT_HEAD`, base not run.

| Case (name now; the old name where it changed) | a9d7b0e5 | Now | Row |
|---|---|---|---|
| `test_a_failing_test_is_not_sealed_and_is_new_when_the_base_passes` | `new`; four prefixes' kept files | `new`; `suite-at-base.txt` alone | absent, exit 0 |
| `test_a_failure_the_base_shares_is_labelled_failing_on_base_too` | `on` | `on` | failing |
| `test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict` | two `on`, three `new` | two `on`, three `NOT_REACHED` exit 1 | failing; absent, exit 1 (Q1) |
| `test_a_part_that_is_not_pytest_is_passed_over_though_it_prints_counts` | `on` | `on` | failing |
| `test_a_file_named_below_a_cd_is_run_at_the_base_and_not_called_new` | `tests/test_two.py` `on` | `sub/tests/test_two.py` `on` | failing |
| `test_a_runner_first_row_runs_once_at_the_base` | `on`; `suite-at-base-1-1.txt`, `collected-at-base-1.txt` | `on`; `suite-at-base.txt` | failing |
| `test_a_row_with_a_semicolon_runs_whole_at_the_base` (was `…_is_cut_at_the_semicolon_its_shell_reads`) | `on`; two prefix files | `on`; one kept run | failing |
| `test_a_lint_first_row_finds_a_failure_the_base_shares` | `on`; three prefix files | `on`; one kept run | failing |
| `test_a_lint_first_row_finds_a_failure_the_branch_introduced` | `new` | `new` | collected |
| `test_a_row_that_runs_no_pytest_gives_no_measured_word` | `NO_RUNNER` | `NO_RECORD_AT_HEAD`, nothing kept at the base | no head record |
| `test_a_row_that_sets_pytest_addopts_itself_records_nothing` (new, S13) | — | `NO_RECORD_AT_HEAD`, no record file | no head record |
| `test_a_row_that_replaces_pythonpath_cannot_load_the_recorder` (new) | sealed, exit 0 | the suite fails, `suite.txt` names the recorder | the finding above |
| `test_a_part_that_fails_at_the_base_before_the_runner_measures_nothing` | `NO_RUNNER` | `NO_RECORD` | no base record |
| `test_a_file_the_base_cannot_collect_beside_another_is_not_measured` ×2 rows | `COMPANY` both | three `on`, two `NOT_REACHED` exit 2 | failing (collect line); absent, exit 2 |
| `test_a_base_run_stopped_at_its_first_failure_is_not_measured` | `COLLECTED_BEYOND` | `NOT_REACHED` exit 1 | absent, exit 1 (S9) |
| `test_a_cd_rows_file_the_root_carries_differently_is_run_at_the_base` ×plain, xdist | `tests/test_two.py` `on`; two prefix files | `sub/tests/test_two.py` `on`; one kept run | failing |
| `test_a_cd_rows_shared_and_new_files_are_named_from_the_root` (was `…_each_get_a_measured_word`) ×2 | two `on`, three `new` | `sub/…` two `on`, three `NOT_REACHED` exit 1 | failing; absent, exit 1 |
| `test_a_module_the_branch_added_beside_a_failure_the_base_shares` (was `test_a_root_run_row_measures_the_module_the_branch_added`) ×2 | two `on`, three `new`; two runs alone | two `on`, three `NOT_REACHED` exit 1; one run | failing; absent, exit 1 |
| `test_a_file_the_base_carries_only_at_the_root_is_measured_alone_under_a_cd` | `tests/test_two.py` `new` | `sub/tests/test_two.py` `new` | absent, exit 0 |
| `test_a_candidate_whose_run_at_the_base_crashes_is_not_measured` | `NO_RUNNER` | `NOT_REACHED` exit 3 | absent, exit 3 (the session line was written before collection) |
| `test_a_run_of_several_that_counted_only_warnings_sends_each_file_alone` ×2 | `COMPANY` both | `sub/…` one `on`, two `NOT_REACHED` exit 1 | failing; absent, exit 1 |
| `test_what_a_test_printed_is_not_read_as_pytests_own_lines` ×2 layouts ×2 | `on`; `new` | `on`; `new` | failing; collected |
| `test_a_file_the_base_fails_is_failing_in_the_bases_own_record` ×files, suite ×plain, xdist (was `…_fails_alone_is_proven_by_one_session_listing_it`, and folds in `test_a_row_that_collects_beyond_its_file_gives_no_permissive_word`) | files `on`; suite `COLLECTED_BEYOND` | `on` all four, one kept run, one base session, the record line asserted | failing (S6) |
| `test_a_path_holding_a_space_is_named_and_compared` (new, S17) | sealed: no file named | `tests/test_a b.py` `on` | failing |
| `test_the_fallback_names_a_path_holding_a_space` (new, S17) | the path cut at its blank | named whole | `FAILED_RE` |
| `test_an_inner_run_on_stderr_under_s_is_not_read_as_the_runs_own` ×2 | `COMPANY` both | err `on`, g `new` | failing; collected (S16) |
| `test_an_inner_run_on_stdout_beside_a_passing_base_gives_no_word` ×2 | `new` both | `new` both | collected |
| `test_a_run_with_no_rule_of_its_own_is_read_off_its_report` rN, rP, rP-passing | `COMPANY` ×2, `COMPANY` ×2, `new` ×2 | (`on`, `new`), (`on`, `new`), `new` ×2 | failing; collected |
| `test_a_run_with_no_summary_line_is_read_off_its_report` ×2 | `new`; `on` | `new`; `on` | collected; failing |
| `test_a_row_that_runs_pytest_twice_reads_each_runners_own_record` p1b, P7, Q8 (was `…_gives_no_permissive_word`) | `tests/test_y.py` `MULTI_RUNNER` | `sub/tests/test_y.py` `NOT_REACHED` exit 1 | absent, exit 1: the base's root runner fails and `&&` never reaches `sub` |
| the same, P3-dropper-first, no-report-writer | `MULTI_RUNNER` | `tests/test_y.py` `on` | failing |
| `test_two_runners_in_two_directories_each_name_their_own_file` `;`, `sh -c` (new, S10) | `MULTI_RUNNER` | `sub/tests/test_two.py` `on`, `tests/test_two.py` `new`, two base sessions | failing; collected |
| `test_a_part_that_hands_its_runner_the_environment_is_measured` sh-c, no-junitxml × passing, failing base (was `test_a_part_that_drops_the_gates_arguments_gives_no_word`; failing base new, S11) | `NO_RUNNER` | `new`; `on` | collected; failing |
| `test_a_part_that_is_not_pytest_runs_as_the_row_runs_it_at_the_base` lint/runner-first × failing/passing base (was `…_keeps_the_word_and_runs_once_in_the_proof`) | `on`; runner-first's marker written by the proof | failing base `on`, marker not written; passing base `new`, marker written | failing; collected |
| `test_a_cd_rows_file_is_named_from_the_root_wherever_pytests_rootdir_is` ini in `sub`, ini at root (was `…_proof_holds_where_pytests_rootdir_is_its_directory`) | `on`; `COLLECTED_BEYOND` | `sub/tests/test_two.py` `on` both | failing |
| `test_a_base_run_that_exits_otherwise_measures_only_what_it_collected` tests-none-failing, no-test (was `test_a_run_whose_report_names_no_failure_and_exits_otherwise_is_not_measured`) | `NOT_ENDED` both | `new`; `NOT_REACHED` exit 3 | collected; absent, exit 3 |
| `test_a_file_the_base_holds_no_test_in_reads_new` ×2 | `new` | `new` | absent, exit 0 |
| `test_two_failing_files_each_read_their_own_word_from_one_base_run` passes-both, fails-one (was `test_a_group_decides_only_new`, S14) | (`new`, `new`); `COMPANY` both | (`new`, `new`); three `on`, two `new`; one kept run | collected; failing |
| `test_a_file_the_base_fails_only_alone_is_not_called_failing_on_base_too` path, state, no-count-alone | `COMPANY` both | a `on`, b `new` | failing; collected (S15) |
| the same, teardown | `COMPANY` both | a, b `new`; `tests/test_one.py` `on` — the row's last test carries the teardown error at the base and on the branch | collected; failing |
| `test_a_first_runner_without_the_gates_environment_costs_the_word` | `MULTI_RUNNER` | `NO_RECORD_AT_HEAD`, nothing kept at the base | no head record (S12) |
| `test_a_runner_without_the_environment_beside_one_with_it_adds_no_file` (new, S12) | `COMPANY` both | two `on`; the box's file not listed, its `FAILED` line in `suite.txt` | failing |
| `test_a_count_another_file_makes_up_does_not_earn_the_word` | b `COMPANY` | b `new`, a and c `on` | collected; failing |
| `test_a_runner_whose_output_goes_to_a_file_is_still_recorded` (was `test_a_measuring_runner_whose_output_the_gate_never_sees_earns_no_word`) | i `MULTI_RUNNER`; u not listed | i `new`, u `on` | collected; failing |
| `test_a_runner_that_collects_nothing_at_the_base_ends_the_row_otherwise` ×2 (was `test_a_silent_measuring_runner_beside_an_empty_session_earns_no_word`) | i `MULTI_RUNNER` | i `NOT_REACHED` exit 5, u `on` | absent, exit 5; failing |
| `test_a_record_an_earlier_run_left_settles_nothing` (was `test_a_report_an_earlier_run_left_settles_nothing`) | `new` | `new`; the stale record's file not listed | collected |
| `test_a_relative_kept_directory_still_receives_the_record_under_a_cd` (was `…_the_report_…`) | `tests/test_two.py` `on`, `.xml` kept | `sub/tests/test_two.py` `on`, `records/` holds both runs | failing |
| `test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives` | the corpus words | skipped, phase 4 named | phase 4 |

Every permissive move above — `COMPANY`, `MULTI_RUNNER` or
`COLLECTED_BEYOND` to `on` — is a file whose own failing test is in the
base's record, written by the pytest process that collected it; the cases
where that is not obvious from the layout (S6, S10, the stderr inner run,
the uncollectable file) assert the record line too.

**Seen red (§15), executed.** With a9d7b0e5's `broad_gate.py` put in place
and `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` and
`tests/test_release_hygiene.py` run against it, 76 cases failed — every new
case and every case above whose word or kept file moved, plus the release
hygiene sweep, because the old gate's `9.1.1` has lost its exemption.
With a9d7b0e5's `templates/config.md` and `skills/verify/SKILL.md` put in
place, the four pins of rule 3 and the **New?** bullet failed. Both files
were restored with `git checkout` from the committed phase. Every unit added
was then broken once through `bin/mutation-check`, listed next.

**Mutations, executed, each `bin/mutation-check skills/verify/scripts/broad_gate.py`
with the cases named, each red:** `record_key` made constant;
`records_dir` without `abspath`; the recorder's directory put last on
`PYTHONPATH`; the `-p` not appended; the records directory not made; the key
not handed; `record_path` without `realpath` on the worktree; a path outside
the worktree read as inside; the session key unchecked; an unparsable line,
a non-object line, a blank line counted wrongly; `collected` not filled;
`failed` read as anything but `passed`; record files read in reverse order;
an unlistable directory raising; each of the four rows of `base_word`; the
base run without the recorder; the base record read against `root`; the
`HEAD` run without the recorder; the `HEAD` record ignored; the fallback's
words dropped; `FAILED_RE` narrowed back to `\S+?`.

Three guards were folded away on the way, because a mutant of each
survived: `read_record`'s filename prefix filter, its `kind == "session"`
check, and its `kind == "collect"` test, each implied by the key or the
`outcome`; and `record_path`'s `os.path.isabs(rel)` and `rel == os.pardir`
became one question. `record_path`'s `replace(os.sep, "/")` is the identity
on POSIX, so its mutant survives here by construction; CI's Windows leg is
its answer (`overview.md`, *Not verified*).

**S21, a probe over this repository's own row — executed, and a probe, not
a seal.** A scratch clone of abf822d0, a `base` branch planting
`tests/test_tmp_s21_planted.py` failing, a `feature` branch failing it once
more, and `broad_gate.py --base base` over the row `uvx ruff check . && uvx
ruff format --check . && bin/test -q`. The `HEAD` run took 934 s under
`-n auto` (3 failed, 12856 passed, 142 skipped) and wrote ONE record file,
the xdist controller's, 14 MB; the base run wrote one more, 13 MB, and was
kept once as `suite-at-base.txt`. Both failing files read `failing on base
too`. One of them was not planted:
`tests/test_every_reader_ends_a_line_where_gfm_does.py::test_every_splitlines_call_left_is_named_with_its_reason`
failed on `read_record`'s new `splitlines` call, at the base as on the
branch, since the base was this branch's tip — the word is right, and the
defect is this phase's. It is named in that module's `OUT_OF_CLASS` with its
reason at 1bc4fb42, and the module is green. The same run's ledger arm shows
phase 3 what it inherits: 48 broken rows (anchors on `row_prefixes`,
`report_counts`, `proof_refused`, `JUNIT_REPORT`, `NO_RUNNER`,
`NOTHING_COLLECTED_EXITS` and on renamed or retired cases) and 162 drifted
ones (`broad_gate.py#gate`, `#run`, `#compare_at_base`, `#failing_files`,
rule 3's and the **New?** bullet's headings, the re-worded cases). The probe's
clone and output were deleted.

**The cost the records add.** A green suite of this size writes about 14 MB
of JSON Lines under the kept output, and a failing one twice that. Nobody
priced this before the probe; it is a fact for the review, not a decision
made here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `row_prefixes`, `POSIX_CUTS`, `CMD_CUTS`, `JUNIT_REPORT`, `NOTHING_COLLECTED_EXITS`, `COLLECT_ONLY`, `OWN_LISTING`, `COLLECTED_RE`, `LISTED_RE`, `NODE_RE`, `ERROR_LINE_RE`, `COLOUR_RE`, `RAN_RE`, `report_counts`, `written_report`, `proof_refused`, the `ElementTree` import | nowhere: the mechanism they served retired (`spec.md` Scope 7) |
| the reasons `NO_RUNNER`, `NOT_ENDED`, `COLLECTED_BEYOND`, `MULTI_RUNNER`, `COMPANY` | replaced by `NO_RECORD_AT_HEAD`, `NO_RECORD`, `NOT_REACHED`; `test_the_unmeasured_word_says_so_and_every_reader_is_told_it` asserts the five gone |
| the cases `test_a_row_is_cut_where_sh_cuts_it`, `test_a_row_is_cut_where_cmd_exe_cuts_it`, `test_the_report_is_read_for_two_counts_and_nothing_else`, `test_the_proof_needs_one_session_listing_the_file_alone`, the tables `REPORTS` and `PROOFS`, the helper `collected_at_base` | nowhere: the units they held retired |
| the kept names `suite-at-base-<k>[-<n>].txt`, `.xml`, `collected-at-base-<n>.txt` | `suite-at-base.txt` and `records/` |
| the release-hygiene exemptions `(broad_gate.py, 9.1.1)` and `(broad_gate.py, 3.8.0)` | nowhere (Q-W2, `overview.md`) |
| the regression corpus case, running | phase 4: re-derive `REGRESSED_WORDS`, reduce `word_for`, remove the `skip` |
