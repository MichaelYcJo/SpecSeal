# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 2f2590b8 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrator fills this row |

## What this phase was asked

`plan.md` phase 3: `gate` reads the head record once after the suite arm and
hands it to `failure_lines` and `panel`; both print `suite_counts(record)`;
the failure form carries a no-record line built on `NO_RECORD_CAUSES`;
`COUNTS_RE`, the text `suite_counts` and `NO_SUMMARY` are retired, with
`agents/sealer.md`'s sentence, the registry row in
`tests/test_every_reader_ends_a_line_where_gfm_does.py` and the copy of
`NO_SUMMARY` in `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`. Cases
S1 with the decoy, S2, S3, and every case that read a printed summary
re-aimed or retired (Q-W1).

## What this phase found

**`panel` takes the run record as `run`, beside `record`.** `panel`'s
`record` was already the work item's round record, which `rounds_rows`
reads and #866 is changing, so the head `RunRecord` arrives under a name of
its own at the end of the signature; the `rounds_rows(item, record)` call
and its neighbours are untouched (`plan.md` §*Seams*).

**The no-record line is said only where no session carries the key.** A
record with sessions and no count — a line that did not parse, or a session
that ran nothing — prints nothing in that place: `UNREAD_HERE` has already
said why no count follows, and a sentence saying *no pytest left a record*
over a record would be false. A mutant that printed it everywhere survived
the first cases and the unread case gained the assertion (2f2590b8).

**A session that died at `HEAD` now shows what it counted.** #849's case of
a test that kills plain pytest used to end with `NO_SUMMARY`; its record
holds `1 failed, 2 passed` from the lines written before the death, under
`UNENDED_HERE`, which says the session stopped part-way. That is what the
form prints now.

**Q-W1, before and after:**

| Case | Before | After |
|---|---|---|
| `test_the_forms_that_stay_allowed_are_sealed_exactly_as_today` | `summary_counts` of the kept `suite.txt` is `1 passed` | `suite_counts` of the head record, read with its own key (`head_run`), is `1 passed` |
| `test_a_failing_row_with_no_summary_says_so_on_the_form` | `exit 1` prints `NO_SUMMARY`; `echo 1 failed in 0.01s && exit 1` prints `1 failed` | renamed `…_no_record_says_so_on_the_form`: both print `NO_RECORD_HERE`, and the echoed line is counted nowhere (S3, the decoy at the gate's level) |
| `test_no_value_on_the_panel_is_wider_than_the_frame_gives`, `test_the_widest_panel_the_tree_can_produce_fits_at_the_first_rung` | `LONG_SUITE`, a printed line | `LONG_SUITE`, a dict of counts, handed as `run` |
| `test_the_suite_carries_its_counts_and_nothing_under_them` | three printed lines | three runs: two of counts and none, which reads `exit 0` |
| `test_the_result_rows_carry_a_tick_and_a_blank_row_stands_before_them`, `test_the_sample_carries_every_row_the_panel_can` | `1 passed in 1s` printed | `run` counting one `passed` |
| `test_the_suite_row_reads_pytests_counts_and_not_a_linters` | six inputs to the text reader | the class it pinned held over the record: a linter's lines after the runner reach no row, and a skipped-only run shows `✓ 3 skipped` |
| `test_a_session_that_stopped_part_way_here_is_counted_under_the_list` | `NO_SUMMARY` in the form | the dead session's counts, and no `NO_RECORD_HERE` |
| `test_a_failing_suite_with_no_summary_says_it_is_not_a_count` (`tests/test_the_gate_hands_cmd_a_path_it_can_run.py`) | `NO_SUMMARY` copied and pinned; the printed line was the count | renamed `…_no_record_…`: `NO_RECORD_HERE` copied and pinned; a printed line with no record prints the no-record line; a record's counts are what the form shows |
| the `summary_counts` registry row | a line reader | removed: no reader of the row's text for counts is left |
| new | — | `test_the_suite_row_reads_the_record_and_nothing_the_row_printed` (S1), `test_the_failure_form_ends_the_suite_with_the_records_counts_in_pytests_order` (S2) |

**Q-M2 was not measured over the whole suite.** The plan asked for one run
of this repository's suite through `bin/test -q` with the recorder's
variables set. That is a full-suite run, which `skills/agent-contract`
§2 assigns to the sealer and the spawn prompt also forbade; phase 1 measured
it over four modules instead, and S5's case measures it on every run over a
tree carrying every category. The sealer's broad gate is the full
comparison: the panel's `suite` row is `suite_counts` of the record, and
`suite.txt` holds pytest's own line beside it (`overview.md` §*Not
verified*).

Shown red: at 5623d728's gate, the panel over a suite output ending
`see: 999 passed in 1s` printed `('suite', '✓ 999 passed')`, the decoy;
S1, S2, the re-aimed linter case, both end-to-end no-record rows, the
died-at-`HEAD` case and the `cmd` module's A5 parameters failed there
(6 failed, 12 errors at collection, the old `RunRecord` having no
`counts`). Mutation: the panel's counts not read, the form's counts not
written, the no-record line's two conditions each narrowed and widened, and
the head record not read were each red through `bin/mutation-check`; one
widened condition survived first and was answered in 2f2590b8.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `COUNTS_RE` and `summary_counts`, pytest's printed summary read backwards for a wall clock | `suite_counts(record)`, over the record's categories |
| `NO_SUMMARY`, *no pytest summary in this output …* | `NO_RECORD_HERE`, built on `NO_RECORD_CAUSES`; a pytest that died part-way is `UNENDED_HERE`'s |
| the registry row for `summary_counts` | none: no such reader is left |
| `agents/sealer.md`'s *carries pytest's counts, or, where its output has no pytest summary …* | the same sentence about the recorded counts and the no-record line |
