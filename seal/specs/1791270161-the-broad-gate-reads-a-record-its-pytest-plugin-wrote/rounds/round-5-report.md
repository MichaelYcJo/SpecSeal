# Review round 5 — the verifying round for round 4's fixes

Target `d2f9f8a5`, base `a9d7b0e5`; the fixes judged are `70bce95b..acb85a74`
(round 4's three fixes, its one answer, and the orchestrator's strict `new`).
Reviewed in a `git clone --no-local` at the target, under this round's
scratchpad directory. Round 5 is a verifying round: it answers whether each of
round 4's closed verdicts is closed, and judges the units round 4's `New
units` row names as code.

Two findings, both inside units round 4's fixes wrote:

- 🔴 1 — the crashed-worker fix finds the crash's path by node id, and node
  ids are not unique, so a crash lands on another file's name. At the base
  that file reads `failing on base too` when the branch breaks it. Executed on
  pytest 7.4.4 with xdist 3.8.0.
- 🟡 2 — the strict `new` demotes on any `unplaced` count, including one from
  a base session that exited 0. A session that exited 0 failed nothing, so
  its uncounted reports cannot be the file's failure. An ordinary green base
  with one session-parented item now turns every `new` into `new?`. The
  module's own case was changed to pin that. Executed.

Round 4's 🔴 1 and 🟡 3 are closed. Round 4's 🟡 2 is closed for the case it
named, and finding 1 is what its fix opened. ⬜ 4's answer stands.

## What the account claimed, and what the code does

- **Claimed** (the docstring of `path_of`, round 4's fix 8a3fa923): the
  crash report's path is "a lookup of what pytest held for this node, never a
  path made from its id". **The code** at
  `skills/verify/scripts/pytest_record/specseal_pytest_record.py:182` and
  `:184` keys that lookup on `(kind, report.nodeid)`. A lookup keyed by id
  relies on node ids being unique, which is the premise the reframe after
  round 3 retired. Finding 1 shows a run where they are not unique.
- **Claimed** (the spawn prompt, and the comment over `UNPLACED_AT_BASE`):
  where the base's record counts any unplaced report, "one of them may be
  this file's failure". **The code** at `skills/verify/scripts/broad_gate.py:2087`
  tests `record.unplaced`, a sum over every session. That sum includes
  sessions that exited 0, and a session that exited 0 failed nothing. The
  claim holds only for sessions that ended non-zero. That is finding 2.
- **Claimed** (round 4's record): the session's own failed collection is left
  out and counted. **The code** at `:151` returns before carrying a path when
  the collector is its own session, and `path_of` then counts the report.
  Confirmed, executed by
  `test_a_failed_collection_of_the_session_itself_is_left_out_and_counted`
  and `test_a_failed_collection_of_the_session_reads_no_word_of_the_root`
  among the 46 passed.

## 🔴 1 — a crash is recorded under another file's name where two nodes share an id

**What is wrong.** `Recorder.path_of` keeps the first path it saw for each
`(kind, nodeid)` and gives that path to a later report that carries none.
xdist builds such a report on the controller when a worker dies (the
`DSession.handle_crashitem` of xdist 3.8.0 · NAME NOT IN TREE). Two different
nodes can share one node id. On pytest 7 a file outside the rootdir is named
relative to the argument it came from, so `../a/test_m.py` and
`../b/test_m.py` both yield `::test_crash`, and the directories `../a` and
`../b` both yield `test_m.py::test_crash`. A conftest that builds collectors
can produce the same collision on any build. Where `a`'s test ran first and
`b`'s test then crashed its worker, the crash report takes `a`'s path.

**Executed** (probe file `test_tmp_collision.py` · NAME NOT IN TREE, pytest
7.4.4, pytest-xdist 3.8.0, `-n 1`, rootdir forced to a sibling directory with
`--rootdir=. -c pytest.ini`; the record lines below are trimmed to the fields
that matter):

```
target d2f9f8a5, crash in b's call
{'nodeid': '::test_crash', 'when': 'setup', 'outcome': 'passed', 'path': 'a/test_m.py'}
{'nodeid': '::test_crash', 'when': 'call', 'outcome': 'passed', 'path': 'a/test_m.py'}
{'nodeid': '::test_crash', 'when': 'teardown', 'outcome': 'passed', 'path': 'a/test_m.py'}
{'nodeid': '::test_crash', 'when': 'setup', 'outcome': 'passed', 'path': 'b/test_m.py'}
{'nodeid': '::test_crash', 'when': '???', 'outcome': 'failed', 'path': 'a/test_m.py'}
{'kind': 'end', 'exitstatus': 1, 'unplaced': 0}
```

The directory-argument form (`../a ../b`) gives the same lines under the id
`test_m.py::test_crash`. A crash inside `b`'s fixture, before any report of
`b` arrived, also lands on `a`: `'when': '???', 'outcome': 'failed', 'path':
'a/test_m.py'`, with `unplaced` 0.

**Why it matters** (read: `base_word`). This record at the base holds `a`
failing and `b` collected with nothing failed. A branch that breaks `a` reads
`a  failing on base too`, so the branch's own breakage is laid on the base.
That is the outcome this work item exists to end, and rounds 1 to 4 rated it
🔴. A branch that breaks `b` reads `new` with `unplaced` 0, which is round
4's 🟡 2 back again under a collision. Before round 4's fix the crash was
counted as unplaced. So the fix moved this run from the strict side to the
lenient one.

**The fix.** xdist sets `report.node` to the sending worker on every report
it forwards, and to the crashed worker on the crash report. A worker runs one
test at a time. So the crash belongs to the worker's last report when that
report was of the same node and was not that node's teardown, and to nothing
otherwise. **Executed** with the fix below applied in the clone: the call
crash is written under `b/test_m.py`; the setup crash is counted
(`unplaced` 1) and `a` stays passing; the recorder module and the gate's two
crash cases pass (part of 44 passed).
`test_a_test_whose_worker_crashed_is_recorded_failing_under_its_file`,
`test_a_test_whose_worker_crashed_at_the_base_fails_there` and
`test_a_base_record_that_left_a_test_out_gives_no_new` keep passing. The fix
also stops the map from holding one entry per test node: it holds one per
worker.

## 🟡 2 — a base session that exited 0 still turns `new` into `new?`

**What is wrong.** `base_word` returns `UNPLACED_AT_BASE` wherever
`record.unplaced` is non-zero (`skills/verify/scripts/broad_gate.py:2087`),
and `read_record` sums `unplaced` over every session's `end` line whatever
that session's `exitstatus` was. pytest counts every failed report toward a
non-zero exit, a report it was handed without a path included. So in a
session that exited 0, no report failed, counted or not. The reason the
sentence gives, "one of them may be this file's failure", is false there.

**What it does to an ordinary green run** (asked by the spawn prompt). A row
whose base passes, with one item a conftest or plugin parents to the session,
now reads every failing file `new?` with the count, on every run. Before
round 4 it read `new`, and that was measured. The module's own case
`test_the_failure_form_says_how_many_tests_the_record_left_out` was changed
in 4e328ce1 to assert exactly this on a green base: `test_a` passes there and
the session item passes. `test_a_base_record_with_anything_unplaced_turns_only_new_into_new_question`
pins `base_word(record, 0, ...)` as `new?`, which is the same claim on the
exit-0 row of the table. **Executed**: with the fix below applied in the
clone, those two cases are the only failures (2 failed, 44 passed), and the
left-out case then reads `new`. That shows its base exited 0.

**What it does to a red base** (asked). A file collected at a base that
ended non-zero, nothing of it failing, reads `new?` with the count where any
session of that base ended non-zero with something unplaced. The xdist worker
that died in a test's setup is that case, and the strict reading is right
there. `failing on base too`, `NOT_REACHED` and `NO_RECORD` are untouched.
This round keeps that half and narrows only the count it reads. One
over-strictness remains after the fix: a red session whose unplaced reports
all passed (a passing session-parented item) still demotes. The recorder
knows each unplaced report's outcome and could count failing ones alone. That
is a choice of design and is left to the smith, not commissioned here.

**The fix** counts `unplaced` toward the demotion only from sessions whose
`end` line has a non-zero `exitstatus`. A row whose last part masks a failing
first pytest (`pytest a; pytest b`) still demotes, because the first session's
own `end` line is read, not the row's exit.

## Round 4's findings, answered

- 🔴 1, the session's failed collection — **closed**. Read at `:151`: the
  hookwrapper returns before carrying a path for the session's own collector,
  and `path_of` counts the report. Executed: both cases above among the 46
  passed at the target.
- 🟡 2, the crashed worker's test — **closed for the case it named** (a
  unique node id): executed, the recorder and gate cases pass at the target.
  The fix's lookup by id is finding 1, which is a new defect in the fix and
  not this finding reopened.
- 🟡 3, `NO_RECORD`'s causes — **closed**. Read: `NO_RECORD_CAUSES` names the
  row that started no pytest first; the A5 case pins the phrase; the SKILL
  bullet, rule 3 and the changelog say "any of those three causes" and pin
  the retired "for either of those causes" as gone.
- ⬜ 4, `--report-log` — **answer stands**. Read: the comment over
  `PATH_ATTRIBUTE`, rule 3 and the changelog state it, each pinned in
  `test_what_a_line_names_a_file_by_is_told_where_each_reader_meets_it`.

## Earlier rounds, carried

Round 4 confirmed rounds 1 to 3's closures at `a1b1caf3`, and round 4's fixes
do not touch what those verdicts rest on except at `path_of`. Finding 1 is a
new defect there and not one of rounds 1 to 3's. So those verdicts are carried
from round 4's record, not re-derived. The recorder module's 27 cases plus
round 4's two, all among the 46 passed at the target, are the executed check
under them.

## The PR's checks at `d2f9f8a5`

Read three times with `gh pr checks 846`. `ledger`, `lint`, `release`, both
`arm-check-grammar` legs and `pytest (ubuntu-latest, 3.12)` pass. The macOS
and Windows `pytest` legs were still pending at the last read.

## Regression tests to plant

- `tests/test_the_recorder_writes_what_its_process_ran.py` — two files share
  one node id, `a`'s test passes, then `b`'s test crashes its worker under
  `-n 1`. Assert the crash line's path is `b`'s, and with the crash in a
  fixture assert no line names `a` failing and `unplaced` is 1. The test
  environment's pytest is not 7, so plant the collision through a conftest
  `pytest_collect_file` · NAME NOT IN TREE, which hands two files the same `nodeid` on
  `Module.from_parent`. Unverified that `from_parent` accepts `nodeid` on
  every supported build; the smith answers it by seeing the case red against
  the target.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` — at `base_word`, a
  record with `unplaced` from a session that ended 0 gives `new` at code 0
  and at code 1. A record with two sessions, the green one carrying the
  count, gives `new`. Revert
  `test_the_failure_form_says_how_many_tests_the_record_left_out` to assert
  `gate.NEW` and keep its `UNPLACED` sentence assertion.

## Facts for the evidence ledger

- W1 says a report carrying no path takes the path "an earlier report of
  the same node in the session carried". After finding 1's fix it is the
  same worker's last report, of the same node, not its teardown. Re-read W1
  and the recorder's module docstring together.
- W8 and the **New?** bullet say "where the base's record left any test or
  collection out of every list". After finding 2's fix it is "where a session
  of the base that ended non-zero left any". Re-read both, and the comment
  over `UNPLACED_AT_BASE` and the `compare_at_base` docstring.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A crash report's path is looked up by node id, so where two nodes share one (pytest 7 names a file outside the rootdir from its argument) a crashed worker's test is written failing under the other file's path, and at the base that file reads `failing on base too` for the branch's own breakage | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:182` | open | executed: pytest 7.4.4 and xdist 3.8.0 under `-n 1`, `b`'s crash written under `a/test_m.py`, for a call crash and a fixture crash, file args and directory args; with the fix applied, `b/test_m.py` and `unplaced` 1 respectively; read: `base_word` gives `failing on base too` for a file in `failing` |
| 🟡 2 | The strict `new` demotes on every session's `unplaced`, including a base session that exited 0 and so failed nothing, and a green base with one session-parented item reads every failing file `new?` | `skills/verify/scripts/broad_gate.py:2087` | open | executed: with the fix applied, the two cases pinning the exit-0 demotion fail and nothing else does (2 failed, 44 passed); the left-out case then reads `new`, so its base exited 0; read: `read_record` sums `unplaced` regardless of `exitstatus` |
| 🟢 | round 4's blocking finding 1 is closed — the session's own failed collection is counted and written as no line | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:151` | confirmed | executed: `test_a_failed_collection_of_the_session_itself_is_left_out_and_counted` and `test_a_failed_collection_of_the_session_reads_no_word_of_the_root` among 46 passed at the target |
| 🟢 | round 4's finding 2 is closed for a crashed test whose node id is its own | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:184` | confirmed | executed: both recorder-level and gate-level crash cases among 46 passed; finding 1 above is a new defect in the fix's lookup |
| 🟢 | round 4's finding 3 is closed — every cause of a missing record is named, the row that started no pytest first | `skills/verify/scripts/broad_gate.py:2027` | confirmed | read: `NO_RECORD_CAUSES`, the A5 case and the three prose homes, each pinned with the retired phrase as gone; executed: those cases among the 46 |
| 🟢 | round 4's finding 4's answer stands — `--report-log` carrying the attribute is stated and pinned | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:90` | confirmed | read |
| carried | rounds 1 to 3's closures, as round 4 confirmed them at `a1b1caf3` | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/rounds/round-4.md` | confirmed | carried, not re-derived: round 4's fixes touch none of what they rest on beyond `path_of`, whose new defect is finding 1; the recorder's 27 cases pass at the target |
| ❓ | The macOS and Windows `pytest` legs of PR #846 at `d2f9f8a5` had not finished | PR #846 | ❓ out of verified scope | `ledger`, `lint`, `release`, both grammar legs and the ubuntu `pytest` leg pass; the orchestrator reads the two pending legs before the fix pass lands on top of them |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on the recorder module and the gate module `-k "recorder or unplaced or crash or session or left_out or unmeasured or measurement_its_cost or what_a_line_names or before_the_runner or record_files"`, in the clone at `d2f9f8a5` | 46 passed |
| Recorder alone, pytest 7.4.4 and pytest-xdist 3.8.0 under `-n 1`, rootdir forced to a sibling directory, `../a/test_m.py ../b/test_m.py` with `b`'s test calling `os._exit(1)`, target recorder | crash line `'when': '???'`, failed, path `a/test_m.py`; `unplaced` 0 |
| The same with directory arguments `../a ../b` | the same, under node id `test_m.py::test_crash` |
| The same with `b`'s crash inside a fixture, target recorder | crash line failed under `a/test_m.py`; `unplaced` 0 |
| Both fixes below applied in the clone: the call-crash and fixture-crash probes again | call crash written under `b/test_m.py`; fixture crash written as no line, `unplaced` 1 |
| Both fixes applied: the 46 cases again | 2 failed, 44 passed; the two failures are the cases pinning the exit-0 demotion, and the left-out case reads `new` |
| pytest-mypy 1.0.1 read for a session-parented status item | none: its status item is parented to the first `MypyFile`, a file, so it is not an example of finding 2 |
| `gh pr checks 846`, three times | six pass, ubuntu `pytest` among them; macOS and Windows `pytest` pending |
| `bin/round-record new` on this report, in the clone | exit 0; the record parsed, `Fix of a fix` reads first for both findings, and one reopening remains |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: not run by this round. It is the sealer's, once, after the rounds settle; with 🔴 1 open it has not come due |

## Paste-ready fixes

### 🔴 1

`skills/verify/scripts/pytest_record/specseal_pytest_record.py`, in
`Recorder.__init__` replace `self.paths = {}`, and replace `path_of`:

```python
        self.last_sent = {}
```

```python
    def path_of(self, report, kind):
        """The path the report carries, or None where it carries none, or
        where a test's is a directory: neither is a file of its own, and the
        node is counted rather than written.

        A report built outside the two hooks carries no path -- xdist builds
        one on the controller for a test whose worker crashed, and sets
        `report.node` to that worker, as it does on every report it forwards.
        A worker runs one test at a time, so where the last report the same
        worker sent was of the same node and was not its teardown, the crash
        is that node's and its path is used. Never a lookup by node id alone:
        two nodes can share one -- pytest 7 names a file outside the rootdir
        from the argument it came from -- and the crash would be written
        under the other node's file (#825 round 5)."""
        path = getattr(report, PATH_ATTRIBUTE, None)
        sender = getattr(report, "node", None)
        if isinstance(path, str):
            if sender is not None:
                when = getattr(report, "when", None)
                self.last_sent[id(sender)] = (report.nodeid, when, path)
        elif sender is not None:
            nodeid, when, carried = self.last_sent.get(id(sender), (None, None, None))
            if nodeid == report.nodeid and when != "teardown":
                path = carried
        if not isinstance(path, str) or (kind == "test" and os.path.isdir(path)):
            self.unplaced.add((kind, report.nodeid))
            return None
        return path
```

The module docstring's sentence changes with it:

```
names none, unless the same xdist worker's last report was of the same node
and not its teardown, as the `setup` report of a test whose worker then
crashed is.
```

### 🟡 2

`skills/verify/scripts/broad_gate.py`, `RunRecord`, `read_record` and
`base_word`:

```python
    __slots__ = (
        "collected",
        "failing",
        "sessions",
        "skipped",
        "unplaced",
        "unplaced_red",
    )

    def __init__(self):
        self.sessions, self.skipped, self.unplaced = 0, 0, 0
        self.unplaced_red = 0
        self.failing, self.collected = {}, set()
```

```python
            if value.get("kind") == "end" and type(unplaced) is int:
                record.unplaced += unplaced
                # A session that exited 0 failed nothing, counted or not.
                if value.get("exitstatus") != 0:
                    record.unplaced_red += unplaced
```

```python
    if path in record.collected or code == 0:
        if record.unplaced_red:
            return UNPLACED_AT_BASE.format(count=record.unplaced_red)
        return NEW
```

The prose that states the rule, in rule 3, the **New?** bullet, the comment
over `UNPLACED_AT_BASE` and the `compare_at_base` docstring:

```
Either `new` reads `new?` naming the count instead where a session of the
base that ended non-zero left any test or collection out of every list,
because one of them may be the file's failure: a test whose xdist worker died
in its setup, before any report of it reached the controller, is one. A
session that exited 0 failed nothing, so what it left out cannot be.
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🔴 1 (a crash report's path looked up by node id lands on another file where two nodes share one, and that file reads `failing on base too`), 🟡 2 (a base session that exited 0 still turns `new` into `new?`)

Loses a record or crashes: no

## Proof

Opened in the clone at `d2f9f8a5`:
`skills/verify/scripts/pytest_record/specseal_pytest_record.py` (whole),
`skills/verify/scripts/broad_gate.py` (`RunRecord` to `compare_at_base`,
`failure_lines`, the suite failure loop),
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the left-out case and
its conftest; round 4's new cases through the fix diff),
`tests/test_the_recorder_writes_what_its_process_ran.py` (round 4's new
cases through the fix diff), `templates/config.md` rule 3 and
`skills/verify/SKILL.md`'s **New?** bullet (through the fix diff),
`seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/rounds/round-4.md`,
`routing.md`, and the W1 and W8 rows of the ledger fragment. Outside the
tree: the `handle_crashitem` of xdist 3.8.0 · NAME NOT IN TREE and the
pytest-mypy 1.0.1 collector, both in the probe's virtual environment.
