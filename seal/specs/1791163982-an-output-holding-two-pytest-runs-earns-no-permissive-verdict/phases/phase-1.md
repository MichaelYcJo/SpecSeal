# 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | c2967fff |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Scope 1–3, 5 and 6 of `spec.md`, and the Scope 7 sentences that go with
them: every run at the base appends `--junitxml=<path>`, a prefix settles
where its report is written, the words come from a reader of that report,
the text readers retire and their unit tables become one table over reports,
`NO_RUNNER` is reworded and `UNPLACED` and `NOTHING_TOGETHER` are added, and
rule 3, the **New?** bullet and the pins change in the same commit. Every
0.18.2 end-to-end word assertion is kept. A probe settles `questions.md` Q1
(this repository's own row) and Q2 (the names), and the phase decides Q3.
Each new case is seen red against a3aa139a's gate before it is committed.

## What this phase found

**Q1 is (a), measured.** `bin/test -q tests/test_tmp_c_q1.py
--junitxml=<scratch>/q1.xml` on a failing probe file (deleted afterwards)
exited 1 and wrote a report naming tests.test_tmp_c_q1 / test_q1 with a
`failure`, under the runner's default `-n auto`. `run_tests.py#main` hands
its arguments to pytest as the reading said, so this repository's row stays
measured and nothing changes in the runner.

**Q2: every shape the frame left open places.** A scratch project under
pytest 9.1.1, 8.3.5 and 7.4.4 wrote the same names in each: a doctest in a
module is `tests.test_doc`/`test_doc.f`, a doctest text file is
`tests.test_doc.txt`/`test_doc.txt`, `--import-mode=importlib` names tests
exactly as the default mode does, a parametrised id holding `/`, `.` and
`::` stays in `name`, and with the ini file in `sub` a row run from the
root names `sub/pkg/tests/test_x.py` as `pkg.tests.test_x`. One shape is
ambiguous by construction and reads `UNPLACED`: a doctest text file beside a
module of the same stem, because `tests.test_doc.txt` also reads as a class
`txt` in `tests/test_doc.py`. The table's `doctest-text-beside-its-module`
row holds it. pytest 8.3.5 reports a teardown error as a second count in
`tests` but one `testcase`, so the reader counts `testcase` elements and not
the attribute.

**The fixtures' rootdir is the `tests` directory itself.** No fixture writes
an ini file, so pytest takes the arguments' common directory as the rootdir
and names `tests/test_two.py` `test_two`. Offset -1 is therefore the common
case in this module, and the either-direction match is what every
end-to-end case leans on.

**Divergence — what a failure placed on no appended file means.** `spec.md`
Scope 3 says a failing test that could be placed "on none of them" gives
`new?` "for every file not named". Read as *every file no failure names*,
that turns `test_what_a_test_printed_is_not_read_as_pytests_own_lines`'s
`an-inner-failed-line` case from `new` to `new?`: `SUITE_ROW` collects all of
`tests`, and the base's failing `tests/test_one.py` is in the report without
being appended. S5 says every 0.18.2 word assertion is kept, so the build
reads it differently. A failing test placed on no appended file is a failure
of a file the row collected besides them, and decides nothing. A file the
report names no test of reads `UNPLACED`. That keeps the protection the
scope sentence was for: a name the reader cannot place hides the file's
passing tests as well as its failing one, so the file is not named and
cannot read `new`. The S5 case passes unchanged.

**Divergence — one file named at two offsets reads `UNPLACED`.** Not in
`spec.md`. The either-direction match alone gives `failing on base too` to
`tests/test_two.py` where the row collects both it and
`other/tests/test_two.py` and only the second fails at the base: the failure
matches the first at offset 1, and no other appended file. One run has one
rootdir, so a file named at two offsets is two files of the run, and the
reader refuses it. Constructed, not measured (`two-offsets` row).

**What the build does not close.** A file that holds no test at the base,
beside another collected module whose failing test matches the file's
dotted name at a non-zero offset, reads `failing on base too`. Constructed
from the rule, not measured: it needs an empty module at the base, a
same-named module one directory up or down, and a row that collects both.
It stays here and in `overview.md`'s Not done.

**Divergence — the reader takes a fifth argument, `alone`.** Scope 3 names
four inputs. They do not tell a candidate's run of one file from a run of
the others that happens to hold one file, and rule 3's pinned limit sentence
says the second reads `new?` (`test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd`).
So `report_words` is told which run it is.

**S3 needed a branch that names its files.** Under `-rN` and `-rP` the
branch's own run writes no `FAILED` line either, so `failing_files` found
nothing and the gate compared nothing. The branch's failing test prints the
two `FAILED` lines in its captured output (`spec.md` Axis C), and the case
says why.

**S6 uses a base that passes the file.** With the base failing it, the
`sh -c` row runs its own `tests` at the base, fails the file there, and
a3aa139a read `failing on base too`, true by coincidence. The counterfeit
`new` the scope names appears where the base passes the file, so both rows
of the case are built that way. Both read `new` at a3aa139a.

**Seen red at a3aa139a's gate** (the new cases planted first and run
against `broad_gate.py` as 0944697e holds it, unchanged since a3aa139a): S1
plain and xdist gave
`tests/test_err.py` `new` and `tests/test_g.py` `failing on base too`; S2
under `-s` and `--capture=sys` gave `tests/test_g.py` `failing on base too`;
S3 under `-rN` and `-rP` gave the S1 pair reversed, and on the passing base
`tests/test_g.py` `failing on base too`; S4's first row gave `NO_RUNNER`, and
its second held, as the frame said it would; S6 gave `new` on both rows.
The report table's rows and the two kept-directory cases pin units that do
not exist at a3aa139a, so each was shown red by breaking its unit through
`bin/mutation-check` instead. Twenty-nine breaks at c2967fff, every one red:
each direction of `offsets` dropped, the ambiguity rule, each half of the
nothing-collected rule, the two-offsets rule, the not-named rule, the
`error` element, the `name` fallback, the `.py` drop, the bare-`testsuite`
root, the root check, the parse guard, `failed` dropped from placement, the
stop, the stale-report removal, `abspath`, the `alone` flag, the stop
argument and the appended option in `compare_at_base`; each of the three
reworded or added reasons, the **New?** bullet's pinned phrase, and each of
the five rule-3 sentences or clauses changed in this phase.

**Two units the build found and pinned.** A report left in a `--keep-output`
directory by an earlier run would settle a prefix that wrote nothing, so the
report's path is removed before each run. And a relative `--keep-output`
handed to pytest through a `cd` part would be written under the scratch
worktree's `sub`, so the path is made absolute. Each has a case.

**Two existing word assertions moved, as Scope 5 says.** A run that is not
a candidate's and whose report counts no test now settles at the runner and
reads `NOTHING_TOGETHER`, where the walk used to go on and end in
`NO_RUNNER`:
`test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd`
and both parameters of
`test_a_run_of_several_that_counted_only_warnings_is_not_measured`.

**Q3 is (a).** Starting a later group at the prefix the first group settled
at would move no kept-file assertion, but it would make rule 3's pinned cost
sentence false — "one more run of each prefix up to and including the
runner per such file" — and that pin is an existing assertion. So each group
walks from prefix 1, as before.

**The seal.** The sealer runs this gate. A green suite never reaches the
comparison, so a green seal is unchanged. On a failing suite, this
repository's row now appends `--junitxml=<path>` to `bin/test -q` at the
base, and to the two `uvx ruff` prefixes before it, which refuse the option,
write no report, and are passed over as they were.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `ERROR_RE`, `SHORT_SUMMARY_RE`, `PYTEST_SUMMARY_RE`, `NOTHING_COLLECTED_RE` and their comments | `JUNIT_REPORT`'s comment, which says what the report replaced and why; `STOPPED_EARLY_RE` stays |
| `verdicts_at_base`, `collected_nothing`, `measured_summary` | `report_words`, `report_cases`, `dotted` and `offsets` in `skills/verify/scripts/broad_gate.py` |
| `MEASURED_ENDINGS`, `SUMMARY_LINES`, `SUMMARIES`, `NOTHING_COLLECTED` and their four cases | `REPORTS` and `test_the_base_run_is_read_off_pytests_report`, with `test_what_is_not_a_report_settles_nothing` |
| test_the_one_counterfeit_the_gate_cannot_see_is_named | `test_a_part_that_drops_the_gates_arguments_gives_no_word` (S6) |
| Rule 3's `-s` sentence, its "one shape the gate cannot see through" sentence, and its "output goes to a file, or whose summary line the gate does not read" clause | rule 3's report sentences and its sentence on a part that does not hand the arguments on, pinned in `test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written` |
