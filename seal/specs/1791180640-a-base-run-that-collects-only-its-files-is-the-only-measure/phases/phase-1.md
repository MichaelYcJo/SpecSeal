# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 6f80c650 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 1, against `spec.md` Scope 1–8 and S1–S16, with S18 as a
probe: every run at the base appends `--junitxml=<path>` and its report is
read for counts only (no `classname`, `name` or `file`, no family option);
the 0.18.2 candidate split is kept, a group gives only `new`, and every other
file runs alone and reads Scope 4's table; a file the base fails is proven by
one whole-row run with the file inserted after the measuring runner and
` --collect-only -o verbosity_test_cases=-2 -vv` added to `PYTEST_ADDOPTS`,
and `failing on base too` needs exactly one trailer, a listing of that file
alone summing to it, and at most one collection error naming it; the text
readers retire; the four reasons, rule 3, the **New?** bullet,
`compare_at_base`'s docstring and the release-hygiene exemptions change and
are pinned in the same commit; every earlier case asserting `failing on base
too` is listed here with its row. Each new case is seen red at a3aa139a.
`questions.md` Q1 was answered with its default (a) by the orchestrator under
`automation` before the spawn; Q4 is this phase's.

## What this phase found

**The frame holds, with three divergences, each recorded in `overview.md`.**

- **A group of one file runs alone from the start.** Scope 4 runs "every
  other failing file in one group first". Where that group holds one file,
  its run is the same command as the file's run alone, and the lone table
  decides everything the group rule decides and more. Running both would
  spend one more run of every prefix for nothing. So a single file the base
  carries is numbered and run as a file alone, after the candidates.
- **A group whose walk writes no report at any prefix reads `NO_RUNNER`
  without running each file alone.** Scope 4's "every other case" lists
  outcomes of a report (a failure, an error, no test, a non-zero exit). A
  row that wrote no report for several files writes none for one of them
  either, because what drops the option is the row, not the files.
- **S16's "every other word assertion is unchanged" cannot hold**, because
  STOPPED_EARLY retires (Scope 6) and Scope 4 sends a group that decides
  nothing to run file by file. Three earlier cases changed word, each to the
  word the base truly gives, listed in the table below.

**Q4 is answered here.** The two new reasons are `COLLECTED_BEYOND` and
`MULTI_RUNNER`, and the not-ended reason replacing STOPPED_EARLY is
`NOT_ENDED`, formatted with the exit and the kept run. `NO_RUNNER` takes the
first build's reviewed wording. All four are pinned whole in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it`. The two proof
reasons are formatted with the number of the file's run alone, so each names
its kept `collected-at-base-<n>.txt`.

**Measured before building (pytest 9.1.1 and pytest-xdist 3.8.0, a scratch
project outside the tree).** The pass's output matched `spec.md` M1, M4 and
M5 line for line. Two shapes the frame did not name: at `-qqqq` with `-vv`
added, pytest prints the listing and no trailer, so the file reads
`MULTI_RUNNER`; and under `-rN` a file pytest cannot collect gets no
`ERROR <path>` line, only the `ERROR collecting` banner, so such a file reads
`COLLECTED_BEYOND`. Both are strict. The second is named here and in
`overview.md` Not done rather than in rule 3, which names the rows a person
can fix by writing them differently.

**Every earlier case that asserted `failing on base too`, with its row (S16).**

| Case (as named at a3aa139a) | Row | Now |
|---|---|---|
| test_a_failure_the_base_shares_is_labelled_failing_on_base_too | `SUITE_ROW` | moved to `FILES_ROW`, keeps the word |
| test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict | `SUITE_ROW` | moved to `FILES_ROW`, keeps both words |
| test_a_part_that_is_not_pytest_is_passed_over_though_it_prints_counts | cargo line `&&` `SUITE_ROW` | moved to `FILES_ROW`, keeps the word |
| test_a_file_named_below_a_cd_is_run_at_the_base_and_not_called_new | `cd sub && SUITE_ROW` | unchanged: `sub/tests` holds the file alone at the base, so the proof lists it alone |
| test_a_runner_first_row_runs_once_at_the_base | `SUITE_ROW && LINT` | moved to `FILES_ROW`, keeps the word; kept names now `suite-at-base-1-1.txt` and `collected-at-base-1.txt` |
| test_a_row_is_cut_at_the_semicolon_its_shell_reads | `FORMAT; SUITE_ROW` | moved to `FILES_ROW`, keeps the word |
| test_a_lint_first_row_finds_a_failure_the_base_shares | `LINT_FIRST_ROW` | `LINT_FIRST_ROW` now ends in `FILES_ROW`, keeps the word |
| test_a_base_run_stopped_by_a_collection_error_names_only_what_it_ran | `SUITE_ROW` | now test_a_file_the_base_cannot_collect_is_measured_alone, both rows: `FILES_ROW` gives both files `failing on base too` (`test_two` was STOPPED_EARLY, and the base does fail it), `SUITE_ROW` gives both `COLLECTED_BEYOND` (S11) |
| test_a_cd_rows_file_the_root_carries_differently_is_run_at_the_base | `cd sub && suite_row` | unchanged: `sub/tests` holds the file alone |
| test_a_cd_rows_shared_and_new_files_each_get_a_measured_word | `cd sub && suite_row` | unchanged, the same reason |
| test_a_root_run_row_measures_the_module_the_branch_added | `suite_row && LINT` | moved to `files_row`, keeps both words; kept names `suite-at-base-1-1.txt`, `suite-at-base-1-2.txt` |
| test_what_a_test_printed_is_not_read_as_pytests_own_lines | `suite_row` | moved to `files_row`, keeps both params' words |

**Three other word assertions changed** (S16's divergence above):

| Case (as named at a3aa139a) | a3aa139a's word | Now | Why it is the base's word |
|---|---|---|---|
| test_a_base_run_stopped_at_its_first_failure_names_only_what_it_ran | STOPPED_EARLY | `COLLECTED_BEYOND`, renamed test_a_base_run_stopped_at_its_first_failure_is_not_measured | strict; the row names `tests` |
| test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd | `NO_RUNNER` | `new`, renamed …_is_measured_alone_under_a_cd | the file's run alone in `sub` exits 4 with no test: the base has no test there |
| test_a_run_of_several_that_counted_only_warnings_is_not_measured | `NO_RUNNER` twice | `tests/test_one.py` `failing on base too`, `tests/test_two.py` `new`, renamed …_sends_each_file_alone | the base fails `sub/tests/test_one.py` under the one runner the row has, and its proof lists that file alone under `sub`'s own ini; `sub/tests/test_two.py` does not exist at the base |

*Corrected at fd98c2c8 by round 1's fix pass:* the third row's
`tests/test_one.py` and the files-only `tests/test_two.py` of the
cannot-collect case, listed in the first table, read `new?` with
`COMPANY` now (`phases/phase-2.md`, the correction).

The middle row of the second table is a `failing on base too` where
a3aa139a gave `new?`. It is not a placement: the run collected one file in
the directory the branch's runner named it from, and the base fails that
file. Phase 2's corpus table carries it among the existing cases so the
acceptance check sees it.

**Seen red at a3aa139a (§15).** The new and moved cases ran in a scratch
copy of this tree whose `broad_gate.py` was a3aa139a's, with stub names for
the constants that do not exist there (none of them a word a3aa139a gives).
Every new parameter, and every moved one whose assertion changed, failed
there except the four named below. The words a3aa139a gave include
`failing on base too` for S2, S7's p1b, P7 and Q8, S10's root ini and S11's
`SUITE_ROW` row; `new` for P3 and the `-p no:junitxml` runner, S8's two
droppers and S3–S5's inner files reversed; `NO_RUNNER` for S6, S12 and the
two cases whose words changed; and a missing kept or marker file for S1, S9's
runner-first row and the relative-keep case. Four were green there and are
named: S10's ini where the runner runs (a3aa139a's word was right), S9's
lint-first row (the marker half is the runner-first row), S13's passing base
(the guard), and the stale-report case, which pins a unit a3aa139a does not
have and was shown red by mutation instead. The not-ended case, added after
that run, was run there on its own: `new` for both files of its first
parameter and `NO_RUNNER` for its second, both red.

**Mutations (S14), each through `bin/mutation-check` on the committed tree,
54 in all, every one red.** Report reader: the root check, the bare
`testsuite`, the `error` child, the parse guard, the failing count, the
`None` guard. Proof reader: one trailer, the sum, the names, the error
lines, the error count each way, the colour strip, the selected count, the
long clock, the all-deselected trailer. `compare_at_base`: the stale-report
removal, `abspath`, the group's decision and its exit, the proof skipped,
exit 0 and exit 4 or 5 for `new`, the proof's environment, `-vv`, the
listing option, the inserted file, the rest of the row, a group of one run
alone, the report appended, the fallback to runs alone, and the proof's
number. The proof's number survived first (C16): the cases never asserted
the kept proof's name, so the group case now does, and it is red. Texts: the
four reasons, three phrases of the **New?** bullet, one word in each of the
13 pinned rule-3 sentences, and the rule-3 reason pin.

**S18, this repository's own row (executed, a probe).** A clone of this
branch with a test file planted at a base commit, and `compare_at_base`
called with `uvx ruff check . && uvx ruff format --check . && bin/test -q`.
Where the base fails the file it reads `failing on base too`: prefixes 1
and 2 (the two `ruff` parts) write no report, prefix 3 does, and
`collected-at-base-1.txt` shows one session listing that file alone under
`bin/test`'s `-n auto`. Where the base passes it, it reads `new`. The
branch side was not run, because it is the full suite. The first attempt's
file used `assert False`, which `ruff` refuses, and every prefix stopped
there with `NO_RUNNER`: the no-runner reading, as the frame said.

**What the next phase needs.** The corpus layouts are in prose in the first
build's records, and several (Q2, Q3b, Q4, Q5, Q7, Q8, Q10–Q12, Qf, Qs,
Qs2, R4–R6, N1b, N1c, N4–N7, the P7 variants) carry no code. Phase 2
rebuilds each from its description and says which were rebuilt.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| ERROR_RE, STOPPED_EARLY_RE, SHORT_SUMMARY_RE, PYTEST_SUMMARY_RE, NOTHING_COLLECTED_RE and their comments | the comments over `JUNIT_REPORT`, `COLLECT_ONLY`, `COLLECTED_RE`, `LISTED_RE` and `ERROR_LINE_RE` in `skills/verify/scripts/broad_gate.py`, which say what replaced each and carry the measurements |
| verdicts_at_base, collected_nothing, measured_summary | `report_counts`, `written_report`, `proof_refused` and `compare_at_base`'s table |
| STOPPED_EARLY | `NOT_ENDED` |
| MEASURED_ENDINGS, SUMMARY_LINES, SUMMARIES, NOTHING_COLLECTED and their four cases | `REPORTS` and `PROOFS` with test_the_report_is_read_for_two_counts_and_nothing_else and test_the_proof_needs_one_session_listing_the_file_alone |
| test_the_one_counterfeit_the_gate_cannot_see_is_named | test_a_part_that_drops_the_gates_arguments_gives_no_word (S8) |
| test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written | test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written |
| Rule 3's summary-line reason, its two-runner sentence, its `-s` sentence, its summary-line clause and its "one shape the gate cannot see through" sentence | rule 3's report, proof, earn, cost and limit sentences, pinned in the case above |
| The four renamed cases' old names | the new names in the second table above |
