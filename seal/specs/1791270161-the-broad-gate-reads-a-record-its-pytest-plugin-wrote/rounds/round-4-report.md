# 1791270161 — review round 4 report (the redesign's first round)

Target `a1b1caf3`, judged as `a9d7b0e5..a1b1caf3` with the redesign
`0c5b9b2c..a1b1caf3` (the reframe at `f1960194`, phases 5–7 at
`88d8affd..83612bd7`, the survivors file at `a1b1caf3`) read closest. Reviewed
in a `git clone --no-local` at the target, `<scratchpad>/1791270161/round-4/clone`,
with this repository's `bin/test` (pytest 9.1.1, pytest-xdist 3.8.0, Python
3.14.3) and, for the floor, `uv` virtualenvs holding pytest 7.4.4, 8.0.2 and
9.1.1 with pytest-reportlog. The base moved (`275a7ce0`, #831); the branch has
not merged it and was not judged against it.

The redesign does what round 3 asked of the frame for the branch it was built
around: no line's path is made from a node id any more, and every layout
rounds 1–3 refused is written under the node's own path. Three things are
still wrong, and the first is the run's own class:

- 🔴 1: carrying the node's own path assumes that the node a failed collection
  is reported on is the thing that failed. pytest does not promise that. On
  pytest 7.4, a conftest's import error anywhere below the root is reported
  on the **session**, whose path is the rootdir, so two different breakages
  in two directories are both written as `.`, and the branch's own reads
  `failing on base too`. Seen end to end through the gate. Round 2's guard
  refused exactly this line; the reframe retired the guard with the
  derivation.
- 🟡 2: xdist builds the report for a test whose worker crashed outside the
  hook that carries the path, so that failure is dropped; the file's passing
  test is still written, and a file the base's own run fails reads `new`.
  This is the shape `plan.md` Alternative U was rejected to avoid. Seen end to
  end; at `0c5b9b2c` the same report was written failing.
- 🟡 3: round 3's 🟡 3 is closed for the cause it named, and the reworded
  `NO_RECORD` names two causes where the module's own case A5 plants a
  third: the row at the base ended before it started any pytest.

None of the three sits in a unit a previous round's fixes wrote: phases 5–7
are a reframe, `plan.md` says the round after it starts the fix-of-a-fix count
at `no`, and every unit below was written by phase 5 or 6.

## What the account claimed, and what the code does

- **Claimed** (`spec.md` §*The class*, "Two files at one path"): "Closed by
  construction: a node's path is its own … so no rootdir, initial path,
  argument, symlink or conftest-built collector enters it", and "The one node
  whose path is no file of its own is an item a conftest or a plugin parents
  to the session or to a directory". **Found**: true of the path, not of the
  node. A failed collection is reported on the collector whose `collect()`
  raised, and on pytest 7.4 that is the session for a conftest below the
  root (executed, 🔴 1). The session is a second node whose path is no file
  of its own, and its `collect` line is written.
- **Claimed** (`plan.md` Technical context, the failure scenario): a report
  without the attribute "goes unplaced, the record holds fewer files, never a
  wrong one". **Found**: fewer *lines*, and a file whose other tests were
  written then reads a word its base did not give it (executed, 🟡 2).
- **Claimed** (`questions.md` Q-M3): the attribute arrives on the
  controller's copy on 7.4, 8.0, 8.1 and 9.1. **Found**: consistent with what
  I ran — every line written under `-n 2` on 9.1.1 carried it — with the one
  exception of a report the controller builds itself (🟡 2), which Q-M3's
  probe did not plant.
- **Claimed** (the recorder's comment over `PATH_ATTRIBUTE`): "so no field
  pytest or another plugin reads moves". **Found**: no field moves, and one is
  added to everything that writes a report whole: a `--report-log` file
  carries `specseal_path` with the recorder loaded and not without it
  (executed, ⬜ 4).
- **Claimed** (`spec.md` Scope 6 as reframed; the commit `e4b1187b`):
  `NO_RECORD_AT_HEAD` and `NO_RECORD` "name both causes of a missing record".
  **Found**: they name two; `test_a_part_that_fails_at_the_base_before_the_runner_measures_nothing`
  asserts `NO_RECORD` for a third, a row whose first part fails at the base
  so no pytest starts (read, 🟡 3).
- **Claimed** (spec Scope 1): the recorder "changes no outcome". **Found**:
  holds for what I ran. S25's case passes, the `-W error` case passes, and
  the hookwrappers import nothing and read only the node; pluggy 1.6.0 raises
  no warning for the old-style `hookwrapper=True` spelling (read).
- **Claimed** (the orchestrator): `survivor-check` and `evidence-check
  --strict` exit 0 at `a1b1caf3`, 763 passed at `83612bd7`. Not re-run here;
  carried as the orchestrator's.

## 🔴 1 — a failed collection laid on the session is written under the rootdir

`pytest_make_collect_report`'s hookwrapper (`specseal_pytest_record.py:135`)
sets `str(collector.path)` on every collect report. For the session
collector that path is the rootdir, and the reader names it `.`.

On pytest 7.4, `Session.collect` loads each directory's conftest as it walks,
and an import error there propagates out of the session's own collection:
the report is `ERROR collecting test session`, node id `""`, and the
collector is the session (executed: tests in `tests/a` and `tests/b`, a
broken `conftest.py` in either; both runs wrote one `collect` line, node id
`""`, path the rootdir; the same layout under a package `tests/pkg/__init__.py`
did the same). On 8.0.2 and 9.1.1 the same layouts are laid on the directory
(`tests/a`, `tests/b`, `tests/pkg/a`) and are told apart. On 9.1.1 a plugin
whose `pytest_collect_directory` raises while the session walks its arguments
lays the failure on the session too (executed: `.` written).

Through the gate, with the row `<v74>/bin/python -m pytest -q -p no:cacheprovider tests`,
the base breaking `tests/a/conftest.py` and the branch fixing it and breaking
`tests/b/conftest.py`:

```
failing test files, compared at the base:
  .  failing on base too
```

Both records hold `{"kind": "collect", "nodeid": "", "path": <the worktree>}`.
The branch broke `tests/b` and the gate says the base did. That is the
permissive word from a line the run itself did not cause, which is the class
this work item exists to close (`spec.md` §*The class*, "Two files at one
path"). At `0c5b9b2c` the guard's `empty` test refused a `collect` line whose
path is the rootdir and abandoned the record (executed with that recorder:
no record file, the strict side). The reframe retired the guard as a
re-derivation of node naming, but that one test was not about naming: it was
the only thing standing between a session-level failure and the rootdir's
word.

The recorder claims pytest 7.4 by measurement in its own docstring, and
`spec.md` Scope 1 sets its floor at 6.1.

**Why the fix sits here.** The session is no file and no directory of the
tree's own: whatever failed while it walked is not identified by its path.
That is decided from the node, not from an id: the session is the one node
whose `session` attribute is itself. Its failed collection carries no path,
so the recorder writes no line and counts it, as it does for a session-parented
item. That is the strict side: at `HEAD` the failure is in no list and the
count says so; at the base the files the session never reached read
`NOT_REACHED`. Executed in the clone: the probes above then wrote no line and
counted one, the gate's failure form printed the unplaced sentence instead
of `.  failing on base too`, the recorder module passed 27, the gate module
passed 165 under `-k "record or base or measured or collect or unplaced or pyargs or rootdir"`,
and `uvx ruff check` and `ruff format --check` passed.

§14: the unplaced sentence, rule 3's "It leaves two kinds of report out of
every list" and the **New?** bullet's "A test with no file of its own is in
no list at all" each gain the session's failed collection, and their pins in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it` and
`test_what_a_line_names_a_file_by_is_told_where_each_reader_meets_it` move
with them. `spec.md` §*The class* says the session beside the
session-parented item.

What is left after the fix, named rather than closed: on pytest 8 and later a
`Dir` or `Package` whose own `collect()` raises is written under the
directory, which the spec chose (`test_a_directory_that_cannot_be_collected_is_recorded_by_its_own_path`).
Its conftest's failure is its own, but a plugin's `pytest_collect_file` that NAME NOT IN TREE
raises for one file during that walk is laid on the directory as well, so two
files of one directory broken that way would share its word. I did not plant
that shape.

## 🟡 2 — a test whose xdist worker crashed is dropped, and its file reads `new`

xdist's `DSession.handle_crashitem` builds the report for the test a dead
worker was running itself — `pytest.TestReport(nodeid=…, outcome="failed", when="???")` —
on the controller, and hands it to `pytest_runtest_logreport` without
`pytest_runtest_makereport` ever running (read, xdist 3.8.0 `dsession.py:432`). NAME NOT IN TREE
So it carries no `specseal_path`, `path_of` (`specseal_pytest_record.py:152`)
counts it unplaced, and nothing of the failure reaches the record.

Through the gate, row `FILES_ROW -n 2 tests`, the base's `tests/test_two.py`
holding a passing `test_ok` and a `test_crash` that calls `os._exit(1)`, the NAME NOT IN TREE
branch changing `test_crash` to `assert False` (NAME NOT IN TREE):

```
failing test files, compared at the base:
  tests/test_two.py  new
```

The base's own run printed `FAILED tests/test_two.py::test_crash - worker 'gw0' crashed …`;
its record holds `test_ok`'s three lines, `test_crash`'s `setup` line passed, NAME NOT IN TREE
and `{"kind": "end", "exitstatus": 1, "unplaced": 1}`. The file is collected
and nothing of it failed, so `base_word` gives `new`. The base's `unplaced`
count is printed nowhere, since the failure form reads only the head's.
At `0c5b9b2c` the same report was written `failing` under the file (executed:
the old recorder wrote `{"nodeid": "tests/test_two.py::test_crash", "when": "???", "outcome": "failed"}`),
so this word moved with the redesign. A worker crash is how a segfault in a
C extension, `os._exit` or a `pytest-timeout` thread-method kill ends under
`-n`.

`plan.md` Alternative U rejected dropping a line whose file is gone because
"the base's record would hold the file collected and passing: a permissive
word for a failure". This is the same record, reached by a report the
controller built. At `HEAD` the same crash leaves the file out of the list
and the unplaced sentence says the test "had no file of its own", which is
false for it (executed: no listing under a branch that adds the crash).

**Why the fix sits here.** The crashed test's `setup` report went through the
hook and carried the node's path; the crash report is the same node in the
same session. Reusing the path an earlier report of that node carried is a
lookup of what pytest held for the node, not a path made from its id.
Executed in the clone: the base then read `failing on base too`, the head
case read `new` against a passing base, and the 27 and 165 cases above
passed with it. What it leaves: a worker that dies in a test's `setup`
before any report of the node reached the controller. That one stays
unplaced, and `base_word` cannot see it. Giving `new?` wherever the base's
record counted an unplaced *failing* report would close it at the price of
a second count on the `end` line. That is a question for the orchestrator,
and the fix below does not make it.

## 🟡 3 — `NO_RECORD` names two causes, and the module's own case is a third

`NO_RECORD_CAUSES` (`broad_gate.py:2023`) gives both reasons "none loaded it,
or the one that did could not write its record and warned … in {kept}", and
`NO_RECORD` follows them with `EARNS_THE_WORD`, which tells a row how to pass
the environment on. `test_a_part_that_fails_at_the_base_before_the_runner_measures_nothing`
plants `LINT_FIRST_ROW` with the lint stand-in failing at the base only: `&&`
stops the row before any pytest starts, and the case asserts `NO_RECORD`. Its
own docstring says "no pytest at the base loads the recorder" — vacuously
true. The person is pointed at the recorder and the environment, for a row
whose first part failed at the base. This repository's own row is that shape
(`uvx ruff check . && uvx ruff format --check . && bin/test -q`) whenever the
base carries a lint failure the branch fixed.

Round 3's 🟡 3 was this exact sentence shape — "a sentence that names one
cause as the only one sends a person after a problem the row does not have"
(`spec.md` Scope 6) — and the reframe answered it by listing the causes
rather than by asking what makes a base run leave no session. A third cause
exists by construction: the row's run need not reach a pytest at all. At
`HEAD` the same shape leaves no `FAILED` line and so no file, which is why
only `NO_RECORD` needs the clause. Read, not executed: the case exists and
passes in the orchestrator's 763.

## ⬜ 4 — the carrier writes itself into every whole-report log

`pytest_report_to_serializable` copies a report's `__dict__`, and pytest-reportlog NAME NOT IN TREE
writes that dict for every report. With the recorder loaded, a row's
`--report-log` file carries `specseal_path`, an absolute path. Without it, it
does not (executed on 9.1.1). No outcome changes. But `plan.md` Alternative P
rejected `user_properties` (NAME NOT IN TREE) because "`--junitxml` writes every property into
the XML a row keeps, so the gate would change a file a person reads", and N
does the same to a different kept file. The comment over `PATH_ATTRIBUTE`
and rule 3 say nothing of it. The behaviour stays right, so this is ⬜:
one sentence in the comment and in rule 3, and Alternative P's grounds
corrected.

## Round 3's findings, answered

- 🔴 1 (the refusal imported the row's package): closed. The refusal and
  every module lookup are gone. `test_the_recorder_runs_none_of_the_rows_code`
  plants round 3's layout and passes (executed, among the 27).
- 🔴 2 (a collector built below the root, failed collection under
  `sub/tests`): closed for that layout. A collector's own path is the
  module's file, `test_a_collector_built_below_the_root_names_its_files_by_their_own_paths`
  asserts `ext/test_new.py  new` and `ext/test_old.py  failing on base too`
  (read; the recorder-level case executed). 🔴 1 above is the same class on a
  collector the redesign did not consider: a failure laid on a node whose path
  is not the thing that failed.
- 🟡 3: closed for the cause it named. Both reasons now name a recorder that
  loaded and could not write. 🟡 3 above is a cause it did not name.
- ⬜ 4: closed. A session-parented item is written as no line, counted once
  and said in the failure form; a self-removing module keeps its line
  (`test_a_test_with_no_file_of_its_own_is_left_out_and_counted`,
  `test_a_module_that_removes_its_own_file_is_still_recorded_under_it`,
  executed).
- ⬜ 5: closed. `spec.md` Scope 1 and §*The class* are rewritten for the
  reframe (read).

## Earlier rounds, carried

Round 1's 🟡 3 (the warning under warnings as errors) still holds:
`give_up` is unchanged and its case passes. Round 1's 🟡 2 (rule 3 names
Q2's whole class) still holds: the `-I`, `-E` and wrapper sentence stands.
Round 2's ⬜ 3 (a base not checked out gets its own heading) still holds in
`failure_lines`. Round 2's ⬜ 4 (the `--pyargs` `exists` skip) is moot: the
skip retired with the refusal. Its case was rewritten as
`test_a_pyargs_module_inside_the_rootdir_is_recorded_under_its_own_path`.
The ledger coordinates were carried, not re-derived: the orchestrator's
`evidence-check --strict` at the target is their check.

## `survivors.md` — 142 excuses, sampled where the text is live

Of the 142 rows, 118 sit in other work items' records (`1791076832`,
`1791119069`, `1791180640`) or in released ledgers. Those are frozen or
historic, and every released row I checked against the fragment that #825
made false has its `Corrected ·` row (`0.10.0` S5; `0.18.1` B2; `0.18.3` R1–R5,
D1, D2, B3, B4, S5). The 24 in live text were each opened at their line:

- `tests/test_the_seal_is_taken_once_by_the_sealer.py` 4361, 4362, 6611, 6626
  are entries of `for gone in (…)` lists. They carry the retired wording to
  assert it is absent, which is what they are for.
- 3833 ("CI runs `windows-latest` … `compare_at_base` is driven there") is
  still true. 3854 ("used to lose the measurement") is past tense, and the
  same docstring goes on to say what #825 changed.
- The two planted `FAILED` lines are fixtures of the fallback and of the
  inner-run class.
- `broad_gate.py:330` is `COUNTS_RE`, which `suite_counts` still reads.
  `broad_gate.py:1690` is `handed_to_shell`'s docstring on `cmd.exe`, still
  true.
- `seal_stamp.py:638` is `admitted`'s docstring and says nothing about the
  comparison.
- The seven `VERSIONS_OF_ANOTHER_PRODUCT` rows are git's, not pytest's.
- The summary-line and JUnit fixtures belong to `suite_counts` and the
  release seal's reader.

None of the 24 states retired behaviour, so none should have been a
correction. One caution, not a finding: `1791180640`'s `spec.md` and
`post-review-check.md` carry 62 of the rows, and that item awaits `settle`.
Its folding has to drop what #825 retired rather than carry it into `docs/`.

## The PR's checks at `a1b1caf3`

`gh pr checks 846`, read twice: `lint`, `ledger`, `release`,
`arm-check-grammar (3.13)` and `(3.14)` pass; `pytest (ubuntu-latest, 3.12)`
passes in 5m38s and `pytest (macos-latest, 3.12)` in 8m28s. `pytest
(windows-latest, 3.12)` was still pending at my last read, so the Windows leg
— S18's posix listing and `PYTHONPATH` with `;` — is unread at this target.

## Regression tests to plant

- `tests/test_the_recorder_writes_what_its_process_ran.py`: the session's
  failed collection is left out and counted (🔴 1's case below). Executed in
  probe form at the target, where it wrote `.`, and with the fix, where it
  wrote no line and counted 1. I did not run the pasted text as a planted
  case.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: a worker that
  crashed at the base leaves its file failing there (🟡 2's case below).
  Executed in probe form at the target, `new`, and with the fix,
  `failing on base too`.
- The same module: case A5 asserts that the `NO_RECORD` it prints names the
  row ending before any pytest (🟡 3), with the pin of
  `test_the_unmeasured_word_says_so_and_every_reader_is_told_it` moved.

## Facts for the evidence ledger

- pytest 7.4.4 lays a conftest's import error below the root on the session
  (node id `""`, path the rootdir); 8.0.2 and 9.1.1 lay it on the directory.
  Executed, in this round's probes.
- pytest-xdist 3.8.0 builds a crashed worker's report on the controller in
  `DSession.handle_crashitem`, outside `pytest_runtest_makereport`. Read. NAME NOT IN TREE
- pytest-reportlog writes `specseal_path` into `--report-log` when the
  recorder is loaded. Executed on 9.1.1.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A failed collection pytest lays on the session itself is written under the rootdir, so on pytest 7.4 two conftest breakages in two directories share `.` and the branch's own reads `failing on base too` | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:135` | open | executed: the gate printed `.  failing on base too` for a branch that broke `tests/b/conftest.py` over a base that broke `tests/a/conftest.py`, row on pytest 7.4.4; the recorder at `0c5b9b2c` wrote no record there; with the fix no line, unplaced 1, 27 recorder and 165 gate cases pass, ruff passes |
| 🟡 2 | A test whose xdist worker crashed is dropped from the record, so at the base its file reads `new` though the base's own run failed it, and at `HEAD` it is in no list | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:152` | open | executed: `tests/test_two.py  new` under `-n 2` with the base's run printing the crash; the recorder at `0c5b9b2c` wrote the crash report failing; with the fix `failing on base too`, same 27 and 165 pass; read: `handle_crashitem` in xdist 3.8.0 · NAME NOT IN TREE |
| 🟡 3 | `NO_RECORD` names two causes, and the module's own case A5 plants a third — the row at the base ended before any pytest started — for which the sentence points at the environment | `skills/verify/scripts/broad_gate.py:2023` | open | read: `test_a_part_that_fails_at_the_base_before_the_runner_measures_nothing` asserts `NO_RECORD` for a lint part failing at the base; round 3's 🟡 3 was this sentence shape |
| ⬜ 4 | The carrier attribute is written into every whole-report log (`--report-log`), the objection `plan.md` Alternative P raised against `user_properties`; the comment and rule 3 are silent · NAME NOT IN TREE | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:84` | open | executed: a `--report-log` file carries `specseal_path` with the recorder and not without it, pytest 9.1.1; no outcome changes |
| 🟢 | round 3's blocking finding 1 is closed — the recorder looks nothing up and imports none of the row's code | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:140` | confirmed | executed: `test_the_recorder_runs_none_of_the_rows_code` among 27 passed at the target; read: no module lookup left in the module |
| 🟢 | round 3's blocking finding 2 is closed — a collector built below the root names its files by their own paths | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4643` | confirmed | read: the gate case asserts each file's own word; executed: the recorder-level collector case among the 27; finding 1 above is the same class on the session |
| 🟢 | round 3's finding 3 is closed for the cause it named — both reasons name a recorder that loaded and could not write | `skills/verify/scripts/broad_gate.py:2023` | confirmed | read; finding 3 above is the cause it did not name |
| 🟢 | round 3's finding 4 is closed — a test with no file of its own is left out, counted and said, and a self-removing module keeps its line | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:152` | confirmed | executed: both recorder cases among the 27 |
| 🟢 | round 3's finding 5 is closed — `spec.md` Scope 1 and §The class describe the reframe | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:103` | confirmed | read |
| 🟢 | `survivors.md`'s 24 rows in live text are each true or a pin of an absence, and no live sentence needed a correction | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/survivors.md:25` | confirmed | read: each of the 24 opened at its line; the released rows checked against the fragment's `Corrected ·` rows |
| ❓ | The `pytest (windows-latest, 3.12)` check at `a1b1caf3` had not finished | PR #846 | ❓ out of verified scope | the other seven checks pass; the orchestrator reads the Windows leg before the sealer is spawned |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q tests/test_the_recorder_writes_what_its_process_ran.py` in the clone at `a1b1caf3` | 27 passed |
| Gate, row on pytest 7.4.4, base breaks `tests/a/conftest.py`, branch fixes it and breaks `tests/b/conftest.py` | `.  failing on base too`; both records hold a `collect` line, node id `""`, path the worktree |
| Recorder alone, a broken conftest in `tests/a` or `tests/b`, plain and under a package, on 7.4.4 and 9.1.1, with the target's recorder and `0c5b9b2c`'s | 7.4.4: target writes `.` both times, `0c5b9b2c` writes no record; 9.1.1: both write `tests/a` / `tests/b` (and `tests/pkg/a` / `tests/pkg/b`) |
| The same on 8.0.2, target recorder | `tests/a` and `tests/b`, told apart |
| Recorder alone on 9.1.1, a `-p` plugin whose `pytest_collect_directory` raises when its parent is the session | target writes `.`; with the fix no line, unplaced 1 |
| Gate, `FILES_ROW -n 2 tests`, base `test_crash` calling `os._exit(1)` beside a passing `test_ok`, branch makes it `assert False` · NAME NOT IN TREE | `tests/test_two.py  new`; base record: `test_crash` setup only, `unplaced` 1 |
| Recorder alone under `-n 2`, the same crashing file, target recorder and `0c5b9b2c`'s | target: no line for the crash, `unplaced` 1; `0c5b9b2c`: a `when: "???"` line, `failed` |
| Gate, the branch adds the crash over a passing base | no listing; the unplaced sentence printed |
| pytest 9.1.1 with pytest-reportlog, `--report-log`, with and without the recorder | `specseal_path` among the keys with it, absent without |
| The two fixes below applied in the clone: the probes above again | `.` gone, unplaced 1; crash at base `failing on base too`; crash at head `new` |
| The two fixes applied: the recorder module, the gate module `-k "record or base or measured or collect or unplaced or pyargs or rootdir"`, `uvx ruff check`, `uvx ruff format --check` | 27 passed; 165 passed; both pass |
| `gh pr checks 846` at `a1b1caf3` | seven pass; Windows pending at the last read |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: not run by this round. It is the sealer's, once, after the rounds settle; with 🔴 1 open it has not come due |

## Paste-ready fixes

### 🔴 1

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_make_collect_report(collector):
    outcome = yield
    # The session's own collection is no file's and no directory's: pytest 7
    # lays a conftest's import error anywhere below the root there, and a
    # plugin's hook can on any build, so two different breakages would share
    # the rootdir's word (#825 round 4). Its report carries no path, and a
    # failed one is counted on the `end` line, never written.
    if collector is getattr(collector, "session", None):
        return
    _carry_the_path(outcome, collector)
```

```python
UNPLACED = (
    "{count} of the tests and collections the row's pytest reported had no "
    "file of their own and are in no list: a test a conftest or a plugin "
    "parents to the session or to a directory, a failed collection of the "
    "whole session, or a report a plugin built without its path (counted as "
    "unplaced on the end line of each record under records/)"
)
```

```python
SESSION_WALK_FAILS = """\
def pytest_collect_directory(path, parent):
    if parent is parent.session:
        raise RuntimeError("the session's own walk fails")
"""


def test_a_failed_collection_of_the_session_itself_is_left_out_and_counted(
    tmp_path,
):
    """#825 round 4. pytest lays a failure it meets while the session walks
    its arguments on the session itself, whose path is the rootdir: pytest 7
    does so for a conftest's import error anywhere below the root, and a
    plugin's hook can on every build. Written, two different breakages
    shared the rootdir's word and the branch's own read `failing on base
    too`. The session is no file of the tree's, so its failed collection is
    written as no line and counted."""
    root, records = project(tmp_path, {"test_ok.py": "def test_ok():\n    pass\n"})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "session_walk.py").write_text(SESSION_WALK_FAILS, encoding="utf-8")
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(root)])
    result = pytest_in(root, env, "-p", "session_walk", "tests")
    assert result.returncode == 2, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert [line for line in lines if line["kind"] == "collect"] == [], lines
    assert lines[-1]["unplaced"] == 1, lines
```

Rule 3's sentence, in place of "It leaves two kinds of report out of every list … rebuilt itself.":

```
It leaves three kinds of report out of every list, counts them on the record's `end` line, and the gate says how many under the failing files: a test with no file of its own, which a conftest or a plugin parents to the session or to a directory; a failed collection of the whole session, which is where pytest 7 lays a conftest's import error anywhere below the root; and a report that reached the recorder without its path, one a plugin built or rebuilt itself.
```

### 🟡 2

```python
        self.unplaced = set()
        self.paths = {}

    def path_of(self, report, kind):
        """The path the report carries, or None where it carries none, or
        where a test's is a directory: neither is a file of its own, and the
        node is counted rather than written.

        A report built outside the two hooks carries no path -- xdist builds
        one for a test whose worker crashed (`DSession.handle_crashitem`) --
        and where an earlier report of the same node in this session carried
        one, that is the node's own path, so it is used: a lookup of what
        pytest held for this node, never a path made from its id (#825
        round 4)."""
        path = getattr(report, PATH_ATTRIBUTE, None)
        if isinstance(path, str):
            self.paths.setdefault((kind, report.nodeid), path)
        else:
            path = self.paths.get((kind, report.nodeid))
        if not isinstance(path, str) or (kind == "test" and os.path.isdir(path)):
            self.unplaced.add((kind, report.nodeid))
            return None
        return path
```

```python
CRASHES_ITS_WORKER = """\
import os


def test_ok():
    pass


def test_crash():
    os._exit(1)
"""


@pytest.mark.skipif(not XDIST, reason=NO_XDIST)
def test_a_test_whose_worker_crashed_at_the_base_fails_there(tmp_path):
    """#825 round 4. xdist builds the report for a test whose worker crashed
    itself, on the controller and outside the hook that carries the node's
    path, so the recorder wrote it as no line; the file's passing test was
    written, and the base's record held the file collected and passing:
    `new` for a file the base's own run fails (`plan.md` Alternative U's
    shape). The crashed test's `setup` report carried its path, and the
    crash report takes it."""
    repo = base_then_feature(
        tmp_path / "repo",
        files_row(True) + " tests",
        {"tests/test_two.py": CRASHES_ITS_WORKER},
        {"tests/test_two.py": CRASHES_ITS_WORKER.replace("os._exit(1)", "assert False")},
    )
    keep = tmp_path / "keep"
    out = run_gate(repo, keep=keep)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert verdict_of(out.stdout, "tests/test_two.py") == gate.ON_BASE, out.stdout
    assert failing_in_base_record(keep, "tests/test_two.py")
```

### 🟡 3

```python
# Where the row's run at the base left no record carrying the base's key: the
# row may have ended before it started any pytest -- a part before the runner
# that fails at the base stops `&&` there -- or one of the two causes above.
NO_RECORD = (
    f"{NOT_MEASURED}: the row ran once at the base, and no pytest it ran there "
    "left a record of the gate's recorder (the row may have ended before it "
    "started any pytest, as a part before the runner that fails at the base "
    "does; otherwise "
    f"{NO_RECORD_CAUSES.format(kept='suite-at-base.txt')}; records/ is beside "
    f"it). {EARNS_THE_WORD}"
)
```

Rule 3's clause "where no pytest at the base left a record — none loaded the recorder, or the one that did could not write its record and warned in `suite-at-base.txt` — `new?`" becomes:

```
where no pytest at the base left a record — the row ended before it started one, none loaded the recorder, or the one that did could not write its record and warned in `suite-at-base.txt` — `new?`
```

The **New?** bullet's "no pytest the row ran at the base left a record, for either of those causes" becomes:

```
no pytest the row ran at the base left a record, because the row ended there before it started one or for either of those causes
```

### ⬜ 4

```python
# The attribute the two hookwrappers set on a report: the node's own path.
# The recorder's own name, so no field pytest or another plugin reads moves.
# A plugin that writes a report whole -- pytest-reportlog's `--report-log`
# writes what `pytest_report_to_serializable` returns -- writes it too.
PATH_ATTRIBUTE = "specseal_path"
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🔴 1 (a failed collection laid on the session is written under the rootdir, and on pytest 7.4 a branch's conftest breakage reads `failing on base too`), 🟡 2 (a crashed xdist worker's test is dropped and its file reads `new` at a base that fails it), 🟡 3 (`NO_RECORD` names two causes where the module's own case A5 is a third)
Loses a record or crashes: no

## Proof

Opened at `a1b1caf3`: `skills/verify/scripts/pytest_record/specseal_pytest_record.py` (whole);
`skills/verify/scripts/broad_gate.py` (the redesign's diff; 320–335,
1675–1700, 2058–2130); `skills/verify/SKILL.md` and `templates/config.md`
(the redesign's diff); `skills/verify/scripts/seal_stamp.py` 628–645;
`tests/test_the_recorder_writes_what_its_process_ran.py` (the redesign's diff,
65–130); `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the redesign's
diff's tests and asserts; 3820–3885, 3907–3930, 3958–3986, 4345–4370,
4460–4500, 4760–4790, 4846–4872, 6600–6635); this work item's `spec.md`,
`plan.md` (whole), `questions.md` Q-M3, `phases/phase-5.md` 1–60,
`changelog.md`, `rounds/round-3.md`, `survivors.md` (whole), its ledger
fragment's `Corrected ·` rows; `seal/releases/0.18.2.md` and `0.18.3.md` (the
rows survivors quotes). In the clone's virtualenv: xdist 3.8.0
`dsession.py` 432–448, pytest 9.1.1 `_pytest/main.py` 745–775 and 899–960,
`_pytest/subtests.py` (the report builders), pluggy 1.6.0 `_hooks.py`
(the `hookwrapper` option). Every probe ran in
`<scratchpad>/1791270161/round-4/`, and that directory, the clone and its
probe file `tests/test_tmp_round4.py` included, was removed before the NAME NOT IN TREE
handover.
