# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | b3137bd3 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 2 and `spec.md` S17: run every layout of the first build's
record (its round reports and its post-review check) and its 96-run
inner-run matrix through the gate at a3aa139a and at phase 1's head, end to
end against real pytest 9.1.1 and pytest-xdist 3.8.0 in scratch projects
outside the worktree, and table the words. **The acceptance test:** no
`failing on base too` where a3aa139a did not give it, except the S3–S5
shapes, where the base truly fails the file, each named with its reason. If
any layout leaked the permissive word, stop and report it rather than patch
around it. Then plant one parametrized end-to-end case for every layout
whose own record calls a `failing on base too` wrong at some commit, under
its own row and under the files-only row, seen red against the first
build's gate at fb698f90 where that build regressed.

## What this phase found

**The verdict: no layout leaks.** Across the 87 corpus runs (46 layouts,
under their own row and the files-only row where the two differ) and the
384 words of the inner-run matrix, every `failing on base too` given
here is one a3aa139a also gave, except 18 matrix words, all the S3–S5 shape
below. `questions.md` Q3 is answered.

**The 18, by name.** All are `tests/test_err.py` under the files-only row,
where the base fails that file's one test, the test runs pytest itself, and
the branch's run named the file from the row's one runner:

- an inner run on stderr: `-q -s`, `-q --capture=sys`, `-q -rN`, `-q -rP`,
  `-q -n 2 -s`, `-q -n 2 -rN` (6);
- an inner run on stdout: `-q -rN`, `-q -rP`, `-q -n 2 -s`, `-q -n 2 -rN`
  (4);
- pytester in-process: `-q -rN`, `-q -rP`, `-q -n 2 -s`, `-q -n 2 -rN` (4);
- pytester in a subprocess: the same four flag sets (4).

a3aa139a read each of them `new`, `STOPPED_EARLY` or `NO_RUNNER`, off an
inner run's lines, which is #789's members 2 and 3. Here each file ran alone,
its report held the one failing test, and its proof showed one session
listing it. In the same matrix a3aa139a gave `failing on base too` to
`tests/test_g.py`, a file the base passes, 52 times; here none of the 384
words does.

**Two existing cases also gained the word at this phase, and both are the base's — corrected below: both read `new?` since fd98c2c8**
(`phases/phase-1.md` lists them): `tests/test_one.py` of
test_a_run_of_several_that_counted_only_warnings_sends_each_file_alone, and
`tests/test_two.py` of test_a_file_the_base_cannot_collect_is_measured_alone
under the files-only row. In each the base fails the file, the file ran
alone in the directory the branch's one runner named it from, and its proof
listed it alone.

**Every other `failing on base too` here is a file the base fails, and
a3aa139a gave the same word**: P5, P6, Q4c, Q7, R4's non-ASCII file, R5,
R6, N6 and N7 under the files-only row, Q12 under its own wrapper row, and
N1c's package module. Under the layouts' own rows, which name `tests`, a
directory or a second runner, each of those reads `new?` instead: the
strictness the frame accepted (`spec.md` Scope 7).

**Rebuilt from their descriptions.** The records carry code for P1, P2, P3,
Q1, Q3, Q4b, Q4c, R1, R2, R2b, R3, N1 and N3. Every other layout is rebuilt
here from its one-line description, and the table's words are this
rebuild's: Q2 (`--rootdir=sub sub/tests`), Q3b (`a/pytest.ini` and a handed
`a/b/tests/test_two.py`), Q4 (the mixin module collects no test), Q5 (P1
under `-n 2`), Q7, Q8, Q10, Q10b, Q11 (an ini file in `sub` and the row run
at the root with `sub`), Q12 (an `argparse` wrapper knowing only
`--junitxml`), Qf (row, environment, ini), Qs and Qs2 (`PYTEST_ADDOPTS`
preset, a kept directory with spaces), R4, R5 (a nested class, ids holding
`/`, `.` and `::`, and a doctest), R6, N1b (an imported test function and a
fixture of the package's own), N1c (the files-only row, the package module
still failing), N4 (a case-only rename the base passes), N5, N6, N7 and the
three P7 layouts. The 96-run matrix is rebuilt from the first frame's Axis
A: four inner kinds by the base failing or passing the outer test by twelve
flag sets, here each under the files-only row and the row naming `tests`.

**The files-only variant of a two-runner row needs one change.** A runner at
the root handed no path collects `sub` too, meets two modules named
`test_two`, and the branch's own run ends in a collection error before any
comparison. In the rows that run pytest at the root and again in `sub`, the
root runner gains `--ignore=sub`, in this table and in the planted case
alike.

**N4 and N5 differ from the record.** N4's record reads `new` at a3aa139a
and the description says only "case-only rename"; the rebuild has the base
pass the file, so every gate reads `new`. N5's branch run names the file
`../tests/test_two.py` under pytest 9.1.1, where the record wrote
`test_two.py`; a3aa139a reads that name `failing on base too` (the base does
fail the test), the first build `new?`, and this one `new?`.

**Seen red at fb698f90 (§15).** The planted case, test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives,
holds 55 parameters. Against fb698f90's gate (stub constants for the two
reasons it lacks) 52 failed, N1, N1-xdist, N1b, N1c and N3 among them, the
five that build gave `failing on base too`; the three green there are N1,
N1-xdist and N1b under the files-only row, where every gate reads `new`.
Against a3aa139a's gate 48 failed and 7 were green: N1c, the files-only rows
of N1, N1-xdist, N1b, N3 and R3, and N7's files-only row, where a3aa139a's
word is the word here.

**Run**: three copies of the tree at this phase's head, differing only in
`broad_gate.py` (here, a3aa139a's, fb698f90's), each driving the corpus
through `base_then_feature` and the gate in a subprocess, 279 runs at each of
the first two and 87 at the third, with a supplement for the two-runner rows'
files-only variant. The probe file was deleted afterwards.

### Corrected at fd98c2c8 by round 1's fix pass

Round 1 of review found two more classes this phase's corpus did not hold,
both regressions against a3aa139a, and the orchestrator chose the strict
variant of the fix. The statements above are corrected here rather than
rewritten, so the record still says what phase 2 saw.

- **The two existing cases that gained the word no longer do.** The
  warnings-only group's `tests/test_one.py` and the interrupted group's
  `tests/test_two.py` (files-only row) read `new?` with `COMPANY`: the
  files run together at the base failed fewer tests than they fail one by
  one, so the row as written did not show the failure. The interrupted
  group's `tests/test_three.py` moves the same way, from the `failing on
  base too` a3aa139a also gave it to `new?`.
- **Round 1's layouts** — a sibling that puts a module on `sys.path` (A),
  a sibling that sets state at import (A2), a session fixture's teardown
  error (B), and a first runner that keeps its report and environment to
  itself (C) — read `new?` at fd98c2c8, where a3aa139a read `new` for the
  file it got wrong. Each is planted.
- **The corpus re-run at fd98c2c8** (the 46 layouts here, round 1's four,
  and the 96-run matrix, each under both rows, against a3aa139a's gate):
  491 words, and the only `failing on base too` a3aa139a did not give are
  the same 18 matrix words named above, the S3–S5 shape. No layout leaks.
  The planted corpus case keeps every word of the table below.

### Corrected by round 2's fix pass

Round 2 of review found two more regressions against a3aa139a: a group
whose count another file made up, and a measuring runner whose output never
reached the gate. The owner decided the first: a group of several failing
files never earns `failing on base too`. At the round 2 fix head every file
of a group whose run at the base did not give `new` reads `new?`, and the
proof needs the measuring runner's own node ids.

- **The S3–S5 shape is no longer an exception.** Its 18 matrix words read
  `new?`: the outer file is one of two failing files of one run at the base.
- **The corpus re-run at the round 2 fix head** (the 46 layouts here, round
  1's four and round 2's ten, and the 96-run matrix, each under both rows,
  against a3aa139a's gate): 516 words, and no `failing on base too` that
  a3aa139a did not give. The table below is phase 2's and stays as it was
  measured then.

### The corpus, word by word

`own` is the row the record ran the layout with, `files` the same row
handing pytest no path of its own. "beyond", "two runners" and "no report"
are `COLLECTED_BEYOND`, `MULTI_RUNNER` and `NO_RUNNER`; "unplaced" and
"nothing together" are the first build's reasons; "no summary" and
"stopped early" are a3aa139a's.

| Layout | Row | File | a3aa139a | fb698f90 | Here |
|---|---|---|---|---|---|
| N1 | files | tests/test_api.py | `new` | `new` | `new` |
| N1 | own | tests/test_api.py | `new` | **failing on base too** | `new?` beyond |
| N1-xdist | files | tests/test_api.py | `new` | `new` | `new` |
| N1-xdist | own | tests/test_api.py | `new` | **failing on base too** | `new?` beyond |
| N1b | files | tests/test_api.py | `new` | `new` | `new` |
| N1b | own | tests/test_api.py | `new` | **failing on base too** | `new?` beyond |
| N1c | own | tests/test_api.py | `new` | **failing on base too** | `new` |
| N1c | own | tests/test_api/test_users.py | **failing on base too** | `new?` unplaced | **failing on base too** |
| N3 | files | vendor/tests/test_two.py | `new` | `new?` unplaced | `new` |
| N3 | own | vendor/tests/test_two.py | `new` | **failing on base too** | `new?` beyond |
| N4 | files | tests/test_two.py | `new` | `new` | `new` |
| N4 | own | tests/test_two.py | `new` | `new?` unplaced | `new` |
| N5 | own | ../tests/test_two.py | **failing on base too** | `new?` unplaced | `new?` beyond |
| N5 | own | test_two.py | not compared | not compared | not compared |
| N5 | own | tests/test_two.py | not compared | not compared | not compared |
| N6 | files | tests/test_two.py | **failing on base too** | `new?` unplaced | **failing on base too** |
| N6 | own | tests/test_two.py | **failing on base too** | `new?` unplaced | `new?` beyond |
| N7 | files | tests/test_two.py | **failing on base too** | `new?` unplaced | **failing on base too** |
| N7 | own | tests/test_two.py | **failing on base too** | `new?` unplaced | `new?` beyond |
| P1 | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| P1 | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| P2 | files | tests/test_two.py | `new?` no summary | `new?` nothing together | `new` |
| P2 | own | tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| P3-nojunit | files | tests/test_two.py | `new` | `new?` unplaced | `new?` two runners |
| P3-nojunit | own | tests/test_two.py | `new` | `new?` unplaced | `new?` two runners |
| P3-sh | files | tests/test_two.py | `new` | `new?` two runners | `new?` two runners |
| P3-sh | own | tests/test_two.py | `new` | `new?` two runners | `new?` two runners |
| P4 | files | tests/test_two.py | `new?` no summary | `new?` nothing together | `new` |
| P4 | own | tests/test_two.py | `new` | `new?` unplaced | `new` |
| P5 | files | tests/test_two.py | **failing on base too** | **failing on base too** | **failing on base too** |
| P5 | own | tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |
| P6 | files | tests/test_two.py | **failing on base too** | **failing on base too** | **failing on base too** |
| P6 | own | tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |
| P7-both | files | tests/test_x.py | `new` | `new` | `new` |
| P7-both | files | tests/test_y.py | **failing on base too** | `new?` unplaced | `new?` two runners |
| P7-both | files | tests/test_z.py | `new` | `new?` unplaced | `new` |
| P7-both | own | tests/test_x.py | `new` | `new` | `new` |
| P7-both | own | tests/test_y.py | **failing on base too** | `new?` unplaced | `new?` two runners |
| P7-both | own | tests/test_z.py | `new` | `new?` unplaced | `new?` two runners |
| P7-mixed | files | tests/test_w.py | `new` | `new` | `new` |
| P7-mixed | files | tests/test_y.py | **failing on base too** | **failing on base too** | `new?` two runners |
| P7-mixed | own | tests/test_w.py | `new` | `new` | `new?` two runners |
| P7-mixed | own | tests/test_y.py | **failing on base too** | **failing on base too** | `new?` two runners |
| P7-p1b | files | tests/test_x.py | `new` | `new` | `new` |
| P7-p1b | files | tests/test_y.py | **failing on base too** | **failing on base too** | `new?` two runners |
| P7-p1b | files | tests/test_z.py | `new` | `new` | `new` |
| P7-p1b | own | tests/test_x.py | `new` | `new` | `new` |
| P7-p1b | own | tests/test_y.py | **failing on base too** | **failing on base too** | `new?` two runners |
| P7-p1b | own | tests/test_z.py | `new` | `new` | `new?` two runners |
| Q1 | files | tests/test_two.py | `new?` no summary | `new?` nothing together | `new` |
| Q1 | own | tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| Q10 | files | tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |
| Q10 | own | tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |
| Q10b | files | tests/test_two.py | **failing on base too** | `new?` unplaced | `new?` beyond |
| Q10b | own | tests/test_two.py | **failing on base too** | `new?` unplaced | `new?` beyond |
| Q11 | own | sub/tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |
| Q12 | own | tests/test_two.py | **failing on base too** | `new?` no report | **failing on base too** |
| Q2 | own | sub/tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |
| Q3 | files | a/tests/test_two.py | `new?` no summary | `new?` nothing together | `new` |
| Q3 | own | a/tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| Q3b | files | a/b/tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| Q3b | own | a/b/tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| Q4 | files | tests/test_two.py | `new?` no summary | `new?` nothing together | `new` |
| Q4 | own | tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| Q4b | files | tests/test_two.py | `new` | `new` | `new` |
| Q4b | own | tests/test_two.py | `new` | `new` | `new?` beyond |
| Q4c | files | tests/test_two.py | **failing on base too** | `new?` unplaced | **failing on base too** |
| Q4c | own | tests/test_two.py | **failing on base too** | `new?` unplaced | `new?` beyond |
| Q5 | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| Q5 | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| Q7 | files | tests/test_two.py | **failing on base too** | **failing on base too** | **failing on base too** |
| Q7 | own | tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |
| Q8 | files | tests/test_two.py | `new` | `new?` unplaced | `new?` two runners |
| Q8 | own | tests/test_two.py | `new` | `new?` unplaced | `new?` two runners |
| Qf-env | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| Qf-env | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| Qf-ini | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| Qf-ini | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| Qf-row | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| Qf-row | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| Qs | files | tests/test_two.py | not compared | not compared | not compared |
| Qs | own | tests/test_two.py | not compared | not compared | not compared |
| Qs2 | files | tests/test_two.py | `new` | `new?` two runners | `new?` two runners |
| Qs2 | own | tests/test_two.py | `new` | `new?` two runners | `new?` two runners |
| R1-ini | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| R1-ini | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| R1-row | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| R1-row | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| R2 | files | tests/test_api.py | `new?` no summary | `new?` nothing together | `new` |
| R2 | own | tests/test_api.py | `new` | `new?` unplaced | `new?` beyond |
| R2b | files | tests/test_two.py | `new?` no summary | `new?` nothing together | `new` |
| R2b | own | tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| R3 | files | vendor/tests/test_two.py | `new` | `new?` unplaced | `new` |
| R3 | own | vendor/tests/test_two.py | `new` | `new?` unplaced | `new?` beyond |
| R4 | files | tests/sp ace/test_sp.py | not compared | not compared | not compared |
| R4 | files | tests/test_é.py | **failing on base too** | **failing on base too** | **failing on base too** |
| R4 | own | tests/sp ace/test_sp.py | not compared | not compared | not compared |
| R4 | own | tests/test_é.py | **failing on base too** | **failing on base too** | `new?` beyond |
| R5 | files | tests/test_r5.py | **failing on base too** | **failing on base too** | **failing on base too** |
| R5 | own | tests/test_r5.py | **failing on base too** | **failing on base too** | `new?` beyond |
| R6 | files | tests/test_two.py | **failing on base too** | **failing on base too** | **failing on base too** |
| R6 | own | tests/test_two.py | **failing on base too** | **failing on base too** | `new?` beyond |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
