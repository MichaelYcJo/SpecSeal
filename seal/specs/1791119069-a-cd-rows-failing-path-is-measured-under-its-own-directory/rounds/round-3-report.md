# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — review round 3 report

Ran by: specseal:warden on claude-opus-5-5
Target SHA: cdcc9d1f72e06d8cf18b16e5626fa523f15d0e7a (PR #787, base `release/v0.18.2` at 94d7b2e0)
Round kind: verifying, and the last round of the run. The target is round 2's fix range `20cbdcd9..c91587ca` and the closing commit `cdcc9d1f`. Round 2 was the run's one reopening, so this record ends the run whatever it finds, and what it opens is reported as `deferred <home>` candidates.
Worked in: a `git clone --no-local` at the target, under `<scratchpad>/<work-item-id>/round-3/clone`. That clone, its virtualenv, two probe files and the scratch projects beside them were deleted before handover.

## Summary

Round 2's fixes close their four findings. The two pins go red when their
clauses are deleted, the `SUMMARIES` comment matches pytest 9.1.1 and
pytest-xdist 3.8.0, and the survivor rows excuse what they say they excuse.
Over real pytest runs, the new reading gives the measured word in every shape
round 2 named: plain, `-q`, `-n 2`, `-x` with and without xdist, a run with
no failures under `-rA`, and an inner empty run plain, under `-n 2` and under
`-s`. 73ba018c gave the wrong word in each of those shapes.

One of the two places the smith left on purpose is stated only by half, and
the missing half is a regression against 0.18.1:

1. **Under `-s`, an inner pytest run that a failing base test writes to stderr now hides the run's own `FAILED` lines (🟡 1).**
   The gate reads stdout and then stderr, so the inner run's
   `short test summary info` rule stands after pytest's own rule. The base
   reading takes everything after the last rule. That is now the inner run's
   lines alone, so the file the base fails reads `new`. 0.18.1 and 73ba018c
   both read it `failing on base too`. `overview.md` says only that an inner
   run there "can still decide". Rule 3 and the changelog fragment say
   nothing. Executed end to end through `compare_at_base`.
2. **A run that has no rule or summary line of its own reads an inner run's line as its own (⬜ 2).**
   This happens under `-rN`, under a `-r` whose chars give pytest no line of
   its own (`-rP`, or `-rfEP` on a run with no failures), and under `-qq` for
   the summary line. The code behaves as 73ba018c did, so this is not a
   regression. The `SHORT_SUMMARY_RE` comment and round 2's "closed as a
   class" still claim more than the code does.

Both findings belong to the same ground as #789: one output that holds more
than one pytest run's lines. #789's proposed fix counts summaries in the
output. An inner pytester run adds a summary too, so that count would turn
every failing file of a suite that tests a pytest plugin into `new?`. The
deferral should carry that warning.

## What the account claimed, and what was checked

| Claimed (round-2.md, the fix commits, `overview.md`, the ledger fragment) | Found |
|---|---|
| pytest prints every test's captured output first, then the `short test summary info` rule with the `FAILED`/`ERROR` lines under it, then its `!` rules, then the summary | **Holds.** In pytest 9.1.1's `_pytest/terminal.py`, `pytest_sessionfinish` calls the terminal-summary hook, then writes the `!` rules (shouldfail, interrupt, shouldstop), then calls `summary_stats`. The terminal reporter's own hook wrapper writes the failure sections first, lets other plugins write, and in its `finally` writes the short summary and then a second warnings summary. Read |
| The rule is written only when lines follow it, so a run with no rule printed no `FAILED` line of its own (`-rN`) | **Holds as a statement about pytest.** `short_test_summary` writes the rule only `if lines`, and `"P"` maps to no action there. The converse does not hold, and the reading relies on it: a rule present can be a test's own (⬜ 2). Read and executed · NAME NOT IN TREE |
| "Everything a test printed stands above it, so a run's own lines are the ones after the last one" (`SHORT_SUMMARY_RE` comment) | **Holds for captured output and for stdout under `-s`. Fails for stderr under `-s` (🟡 1) and for a run that wrote no rule (⬜ 2).** Executed |
| `measured_summary`: only the last summary line decides, and a nothing-collected line at or after it vetoes | **Holds.** Inner `no tests ran` in captured output: measured, `failing on base too`, plain, `-n 2` and `-s`. 73ba018c gave `new?`. Under `-qq` pytest writes no summary, and an inner run's `1 failed in …` in captured output is read as this run's (⬜ 2; the words there were still right). Executed |
| `failing_files` keeps every `FAILED` line because reading after the last rule would drop the first runner's files in a `;` row, and the gate fails the suite either way, so the cost is an extra line and never a seal | **True.** A `;` row's output carries both runs' rules, and the last is the second runner's. In `gate`, a failed suite arm is appended to `failures` whatever `compare_at_base` returns. Read |
| `-s` stderr: "An inner run written there can still decide" | **True, and only half.** The inner run's lines decide in both directions. A file the inner run names reads `failing on base too`, which 73ba018c also gave. The run's own file the base fails reads `new`, which is new to this fix: 73ba018c and 94d7b2e0 read it `failing on base too` (🟡 1). Executed |
| All new cases red at 73ba018c except the stop-with-no-rule row | **Holds.** 9 failed, 20 passed with 73ba018c's `broad_gate.py` checked out in the clone: three new `MEASURED_ENDINGS` rows, two `SUMMARIES` rows and the four e2e cases. Executed |
| ⬜ 2 and ⬜ 3 pins red with the clause dropped | **Holds.** Each clause deleted from `templates/config.md` in turn turns `test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written` red. Executed |
| ⬜ 4: `KNOWN_TYPES` has three subtests types, and under xdist an all-deselected run ends `no tests ran` | **Holds.** `KNOWN_TYPES` ends `subtests passed`, `subtests failed`, `subtests skipped`. `-k nomatch` printed `1 deselected in 0.00s` plain and `no tests ran in 0.22s` with `-n 2`. Read and executed |
| c91587ca: the third survivor row's quote has no hash, so the records arm reads no stamp there | **Holds.** `evidence-check --strict` exits 0. survivor-check over `94d7b2e0..HEAD` and over the fix range exits 0, and both 0.18.1 rows show as excused. Row 2's Grounds keeps `verdicts_at_base@8fed3ba4`, which has no path, so it is not read as a stamp. Executed |

## Findings from execution

### 🟡 1 — under `-s`, a file the base fails reads `new` once an inner run on stderr carries a rule

`skills/verify/scripts/broad_gate.py:1944`, the three lines of
`verdicts_at_base` that take `own` from the last `SHORT_SUMMARY_RE` match.
Also `overview.md:37`, which states the limit.

`run` builds the text as stdout, a newline, then stderr. With `-s`, a test's
stderr is not captured, so whatever a test writes there lands after
pytest's summary line. Take a failing base test that writes an inner pytest
run's report to stderr, where that inner run had a failure. The text then
ends with that run's rule, its `FAILED` line and its summary. The last rule
is the inner one, so `own` holds the inner run's lines alone.

Measured through `compare_at_base` at the target. The base's
`tests/test_err.py` fails and writes an inner run of a failing
`tests/test_g.py` to stderr, and the base's `tests/test_g.py` passes.

| Row | Target | 73ba018c |
|---|---|---|
| `pytest -q -s` | `test_err.py` **`new`**, `test_g.py` `failing on base too` | `test_err.py` `failing on base too`, `test_g.py` `failing on base too` |
| `pytest -q` | `test_err.py` `failing on base too`, `test_g.py` `new` (both right) | both `failing on base too` |

`new` is the direction #761 exists to stop: a word that blames the branch
for a failure the base shares. `overview.md` names the shape, but its
"can still decide" reads as the old permissive half only, and its "still"
says the shape is unchanged when the `new` half is new. The row author is
the reader who could avoid the shape, and rule 3 does not mention it. The
changelog fragment says the run "is read from pytest's own last lines only",
with no exception.

Narrow: it needs a row with `-s`, and a failing base test that writes a
pytest run's report to stderr. pytester echoes an inner run's stdout to
stdout, so a pytester suite does not reach it. Telling the streams apart
needs `run` to keep them apart, which is mechanism, so the fix here is the
statement and its pin.

### ⬜ 2 — a run with no rule of its own reads a test's rule as its own

`skills/verify/scripts/broad_gate.py:1853`, the comment over
`SHORT_SUMMARY_RE`. The same reading is in `verdicts_at_base`'s docstring
("Where there is no rule, pytest printed no such line").

These were measured over real runs. The asked files are a failing
pytester test that runs an inner failing `tests/test_g.py`, and a passing
`tests/test_g.py`:

- `-q -rN`: pytest writes no rule. The inner rule is last, so the failing file reads `new` and the passing one reads `failing on base too`.
- `-q -rP` on a run with no failures: no rule of pytest's own, because `"P"` has no action in `short_test_summary`. The passes section shows the inner rule, so a file the base passes reads `failing on base too`. NAME NOT IN TREE
- `-qq`: pytest writes the rule but no summary line. `measured_summary` reads the inner run's `1 failed in …` as this run's. The words were right, because the rule was pytest's. Rule 3 says a `-qq` runner "is run but not read: each reads `new?`", which is not what happens when a test printed a summary line.

73ba018c gives the same words in all three, so the release ships nothing
new here. The finding is that the comment and round 2's "closed as a class"
claim a guarantee only pytest's own rule gives.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Under `-s`, an inner pytest run that a failing base test writes to stderr lands after pytest's own lines, and its rule hides the run's own `FAILED` lines, so a file the base fails reads `new` where 0.18.1 and 73ba018c read `failing on base too`. `overview.md` states only that such a run "can still decide", and rule 3 and the changelog fragment state nothing | `skills/verify/scripts/broad_gate.py:1944` | deferred #789 | executed: `compare_at_base` end to end at the target and with 73ba018c's module, rows `pytest -q -s` and `pytest -q`. The statement half (rule 3, `overview.md:37`, the changelog fragment) is in text this run wrote, so it is rung 1's if the orchestrator takes it. The code half needs `run` to keep stdout and stderr apart, which is the ground #789 needs: one output carrying more than one pytest run's lines |
| ⬜ 2 | A run in which pytest wrote no rule (`-rN`, or `-rP` with no failures) or no summary line (`-qq`) reads a test's printed rule or summary as its own. The `SHORT_SUMMARY_RE` comment and round 2's "closed as a class" claim otherwise | `skills/verify/scripts/broad_gate.py:1853` | deferred #789 | executed: real pytest 9.1.1 runs read by the target's and 73ba018c's functions, which give the same words. Not a regression |
| 🟢 | round 2's 🟡 1 is closed — an inner run's `no tests ran` or `FAILED` line in captured output no longer decides | `skills/verify/scripts/broad_gate.py:1967` | confirmed | executed: real runs plain, `-q`, `-n 2`, `-n 2 -q`, `-s`, `-x`, `-x -n 2`, `-rA` with no failures, and an inner empty run plain, `-n 2` and `-s`, all measured right at the target and wrong at 73ba018c; the 9 new cases red at 73ba018c |
| 🟢 | round 2's ⬜ 2 is closed — the two-runner sentence names a same-named file that passes at the base, and its pin holds it | `templates/config.md:333` | confirmed | executed: clause deleted, pin red; the sentence's truth rests on round 2's p1c, and the code under it changed only in a way that gives a passing first runner no rule, so it still reads `new` |
| 🟢 | round 2's ⬜ 3 is closed — the "never `new` unless it ran alone" clause is pinned | `templates/config.md:333` | confirmed | executed: clause deleted, pin red |
| 🟢 | round 2's ⬜ 4 is closed — the `SUMMARIES` comment names the three subtests types and the xdist all-deselected ending | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4626` | confirmed | read against pytest 9.1.1's `KNOWN_TYPES`; executed `-k nomatch` plain and `-n 2` |
| 🟢 | the survivor rows for 0.18.1's frozen B3 excuse the coordinate list, and c91587ca's hashless quote leaves no stamp for the records arm | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/survivors.md:13` | confirmed | executed: survivor-check over `94d7b2e0..HEAD` and over the fix range, exit 0; `evidence-check --strict`, exit 0 |
| 🟢 | the `failing_files` place left on purpose is stated truly | `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:36` | confirmed | read: a `;` row's last rule is the second runner's, and a failed suite arm joins `failures` whatever the words |
| carried | rounds 1 and 2's confirmations: scope 1–6, the divergences, `Corrected · B3` / `Corrected · S5`, round 1's findings closed, and round 2's ⬜ 5 answered | `skills/verify/scripts/broad_gate.py:2089` | confirmed | carried from rounds 1 and 2; the code under them changed only in the base reading, judged above |

## Executed probes

| What was run | Result |
|---|---|
| Real pytest 9.1.1 / pytest-xdist 3.8.0 runs in a scratch project: a pytester test whose inner run fails `tests/test_g.py` and the outer fails; a pytester test whose inner run is empty; a subprocess test that writes an inner run to stderr; a passing pytester test that prints an inner failing run. Each output joined the way `run` joins it and read by `measured_summary` and `verdicts_at_base` at the target and at 73ba018c | target right, 73ba018c wrong: plain, `-q`, `-n 2`, `-n 2 -q`, `-s`, `-x`, `-x -n 2`, `-rA` with no failures, inner empty run plain/`-n 2`/`-s`, stderr inner run without `-s`. Target wrong: stderr inner run with `-s` and with `-s -n 2` (🟡 1). Both wrong alike: `-rN`, `-rP` with no failures (⬜ 2). `-qq`: both measured off the inner summary, words right (⬜ 2) |
| `compare_at_base` end to end on a scratch git repository, rows `pytest -q -s` and `pytest -q`, target module and 73ba018c's | `-s`: target `test_err.py` `new`, 73ba018c `failing on base too`. Without `-s`: target right on both files |
| The new cases with 73ba018c's `broad_gate.py` checked out in the clone (`-k` over the base-run, summary and inner-output cases) | 9 failed, 20 passed; the file restored with `git checkout` |
| The narrow cases at the target (`-k` over the summary, measured, inner-output, solo-runs, nothing-collected and warnings cases) | 64 passed |
| Each of the two rule-3 clauses deleted from `templates/config.md` in the clone, then the solo-runs pin | red both times; the file restored |
| `pytest -q -k nomatch` plain and `-n 2` | `1 deselected in 0.00s`; `no tests ran in 0.22s` |
| survivor-check `--range 94d7b2e0..HEAD` and `--range 20cbdcd9..c91587ca`, each with `--exempt` on this work item's `survivors.md` | exit 0 both; the fix range shows two 0.18.1 survivors, each excused |
| `evidence-check --strict` in the clone at the target | exit 0 |
| The full suite, lint and typecheck (the broad gate) | not yet — not run in this round; the sealer's, once the run ends |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1: under `-s`, an inner run on stderr hides the base run's own lines, and a file the base fails reads `new` | #789, as a comment: same ground (one output carrying more than one pytest run's lines). Its proposed summary count must not count an inner pytester run's summary in captured output, or every failing file of a pytest-plugin suite reads `new?` | #789's owner, the repository owner, who filed it as a `bug` in the review-chain backlog |
| ⬜ 2: a run with no rule or summary of its own (`-rN`, `-rP`, `-qq`) reads a test's printed rule or summary as its own | #789, as a comment, on the same ground | #789's owner, the repository owner |

## Paste-ready fixes

### 🟡 1

`templates/config.md` rule 3: insert after the sentence that ends "is run but not read: each reads `new?`.":

```
A runner with `-s` lets a test write to stderr, and the gate reads stdout and then stderr, so what a failing test writes there stands after pytest's own lines: an inner pytest run written there is read as the run's own, so a file it names reads `failing on base too` and a file the base fails can read `new`. Read either word on such a row as the row's claim rather than a measurement.
```

`tests/test_the_seal_is_taken_once_by_the_sealer.py`: a new entry in the tuple of `test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`:

```python
        # #761 round 3's 🟡 1: an inner run a `-s` test writes to stderr.
        "an inner pytest run written there is read as the run's own, so a file "
        "it names reads `failing on base too` and a file the base fails can "
        "read `new`.",
```

`seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/overview.md:37`, the whole bullet:

```
- Under `-s` a test's output is written live, and what it writes to stderr lands after pytest's own lines, because the gate joins stdout and then stderr. An inner pytest run written there is read as the run's own in both directions: a file it names reads `failing on base too`, and its `short test summary info` rule hides the run's own `FAILED` lines, so a file the base fails reads `new` — which 0.18.1 read `failing on base too`. Telling the two streams apart needs `run` to keep them apart, which a fix pass may not add; `templates/config.md` rule 3 names the shape, and #789 holds the ground.
```

The changelog fragment, after the paragraph that ends "an inner `no tests ran` hid a failure the base shares.":

```
  Under `-s`, what a test writes to stderr lands after pytest's own lines,
  so an inner run written there is still read as the run's own, and a file
  the base fails can read `new`; `templates/config.md` rule 3 names it.
```

### ⬜ 2

`skills/verify/scripts/broad_gate.py:1853`, the comment over `SHORT_SUMMARY_RE`:

```python
# The rule pytest writes above its own `FAILED` and `ERROR` lines, padded
# with `=` to the terminal's width (#761 round 2). What a test printed into
# its captured output stands above it, so where pytest wrote this rule a
# run's own lines are the ones after the last one. pytest writes it only
# where a line follows (none under `-rN`, and none for `-rP` on a run with
# no failures), and a test's stderr under `-s` lands after it; in those
# runs the last rule can be one a test printed (#761 round 3).
```

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `MEASURED_ENDINGS`, with #789's fix and not before: pytest's own rule and `FAILED tests/err.py::…`, its summary, then an inner run's rule, `FAILED tests/g.py::test_g` and `1 failed in …` as if from stderr. Files `tests/err.py` and `tests/g.py`; the words the fix decides on, which must not be `new` for `tests/err.py`. Planted now, it would pin the wrong word.
- The same module, the solo-runs pin above, with the 🟡 1 sentence.

## Facts for the evidence ledger

- Measured 2026-10-05, pytest 9.1.1 and pytest-xdist 3.8.0: with `-s`, a test's stderr follows pytest's summary in the gate's joined text. An inner run written there makes `verdicts_at_base` read `new` for a file the base fails (`compare_at_base`, row `pytest -q -s`). 73ba018c read `failing on base too`.
- Read in `_pytest/terminal.py`: `short_test_summary` writes its rule only when a line follows, `"P"` has no action there, and `summary_stats` returns under `-qq`. So under `-rN`, under `-rP` with no failures, and under `-qq` for the summary, the last rule or summary line in the output can be one a test printed. NAME NOT IN TREE

Needs a fix: yes — 🟡 1 (under `-s`, an inner run a failing base test writes to stderr hides the base run's own `FAILED` lines, so a file the base fails reads `new` where 0.18.1 read `failing on base too`, and only half of that is stated); the run is capped, so it is a `deferred #789` candidate.
Loses a record or crashes: no

## Proof block

Files opened at the target in the clone, or read from the installed tools:

- `skills/verify/scripts/broad_gate.py`: lines 1795–1810 (`failing_files`), 1830–2000 (`ERROR_RE` through `measured_summary`), 2089–2230 (`compare_at_base`), 1421–1470 (`run`), 3315–3365 (the gate's use of the base words), the fix-range diff, and `verdicts_at_base` at 94d7b2e0.
- `templates/config.md`: rule 3, through the fix-range diff.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the fix-range diff, lines 4145–4160 and 4664–4680.
- `seal/specs/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory/`: `rounds/round-2.md`, `rounds/round-2-report.md`, `overview.md` lines 34–38, and the diffs of `changelog.md`, `overview.md` and `survivors.md` (78c8132e, c91587ca).
- `seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`: through the fix-range diff.
- `seal/releases/0.18.1.md`: the B3 row.
- `docs/review-chain-spec.md`: §*The reopening — one, and then the run is capped*, §*The cap bounds rounds, and not the fixes of the round it stopped*, §*Where a leftover goes — the ladder, and why a new issue is not the default*.
- `tests/test_a_record_states_what_the_tree_has.py`: its module docstring.
- `bin/test`, `bin/survivor-check`.
- Issue #789: body and labels.
- pytest 9.1.1's `_pytest/terminal.py`: `KNOWN_TYPES`, `getreportopt`, `pytest_sessionfinish`, `pytest_terminal_summary`, `short_test_summary`, `summary_stats`, `_report_keyboardinterrupt` · NAME NOT IN TREE
