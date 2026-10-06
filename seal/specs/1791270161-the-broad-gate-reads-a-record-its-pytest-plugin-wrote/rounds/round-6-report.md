# Review round 6 — the verifying round for round 5's fixes

Target `475a3875` (the PR head), base `a9d7b0e5`; the fixes judged are
`4e3b41e0..0fc26b5e` (round 5's 🔴 1 and 🟡 2, their cases and their
paperwork). Reviewed in a `git clone --no-local` at the target, under this
round's scratchpad directory. The release branch's later commits (#831, #841)
are not merged in and were not reviewed. This round is the run's last record:
the reopening is spent.

How the findings relate:

```
round 4's 🟡 2: `new` for a file whose test crashed the base, under xdist
   ├─ round 4's fix: demote `new` where the base's `end` lines count unplaced reports
   │     └─ round 5's 🔴 1: the crash placed by node id   → fixed, closes its class
   │     └─ round 5's 🟡 2: a green session demotes too  → fixed, closes its class
   └─ this round's 🟡 1: the same crash without xdist kills pytest itself,
        so the session writes no `end` line and nothing demotes: `new` again
```

- 🟡 1 — on plain pytest, a test that kills its process at the base leaves a
  session with no `end` line. The demotion reads only `end` lines, so the
  file reads `new`. Executed through the gate, crash in the body and in a
  fixture.
- ⬜ 2 — the worker map is keyed on `id()` of an object the map does not
  hold. Read.
- ⬜ 3 — a paperwork correction: the overview's divergence table has no row
  for the strict `new`, which spec Scope 1 and Scope 5 do not describe.

Round 5's two findings are closed, each by an executed check. Every workflow
of PR #846 passes at `475a3875`.

## Spec compliance first

**Claimed** (round 5's fix commit and the `path_of` docstring): a crash
report takes a path only from the same worker's last report, of the same
node and not its teardown. **The code** at
`skills/verify/scripts/pytest_record/specseal_pytest_record.py:184` to
`:197` does that. Read against xdist 3.8.0: `worker_testreport` · NAME NOT IN TREE sets
`rep.node` on every forwarded test report, `handle_crashitem` sets it on the
crash report, and the crash item is the head of the worker's pending list,
the test it was running. Failed collect reports are forwarded without
`rep.node`, so they never touch the map.

**Claimed** (the `UNPLACED_AT_BASE` comment, rule 3, the **New?** bullet):
a session that exited 0 failed nothing, so only sessions that ended non-zero
demote `new`. **The code** at `skills/verify/scripts/broad_gate.py:1974`
adds a session's count to `unplaced_red` where its `end` line's
`exitstatus` is not 0. pytest counts a pathless failed report toward the
exit (`Session.pytest_runtest_logreport` · NAME NOT IN TREE), so the premise holds.

**Not described by the spec.** Scope 1 says "nothing in its table depends
on the line", and Scope 5's table has five rows. Since round 4 a sixth word
depends on the `end` line. That is ⬜ 3, a correction to the overview.

## Does each fix close its class

### `path_of` keyed on the sending worker — closes it

The class is every way a pathless report could take another node's path.
Enumerated against xdist 3.8.0 and pytest's run protocol:

| Where the worker died | The worker's last report | What the crash report gets |
|---|---|---|
| in the test's body | that node's `setup` | its own path |
| in the test's fixture | the previous test's `teardown`, or none | nothing; counted |
| in the test's teardown | that node's `call` | its own path |
| in a node sharing the previous node's id, before any report | the other node's `teardown` | nothing; counted |
| after a teardown, before the protocol completes | that node's `teardown` | nothing; counted |
| a plain run, or a report a plugin built in-process | no `report.node` | nothing; counted |

No row places a crash on another file. The remaining reach of node ids is
the `unplaced` set, keyed `(kind, nodeid)`: two colliding nodes left out
together count once. That changes only the number in a sentence, never a
word, so it is not a finding.

### `unplaced_red` — closes its class, and the class next to it is open

A session that exited 0 no longer demotes, whether it is alone or beside a
red one, and whatever the row's own exit was. Executed: with the exit test
mutated to always count, two cases go red. The over-strictness that remains
(a red session whose left-out reports all passed) is named in rule 3, the
**New?** bullet and the changelog.

The fix reads the sessions that wrote an `end` line. A session that never
wrote one is the reddest session there is, and it is not read. That is
🟡 1.

## 🟡 1 — a test that kills plain pytest at the base still reads `new`

**What is wrong.** Without xdist, a test that calls `os._exit`, segfaults or
is killed by a timeout's thread method ends the pytest process itself.
`pytest_sessionfinish` never runs, so the record holds the session line and
the lines written before the crash, with no `end` line. `read_record` adds
nothing to `unplaced_red` for that session. The crashed test's `setup` line,
or its file's earlier tests, put the file in `collected` with nothing
failing. `base_word` (`skills/verify/scripts/broad_gate.py:2105`) then gives
`new`, because nothing demotes it.

**Executed** (probe file `tests/test_tmp_plain_crash.py` · NAME NOT IN TREE, deleted).
The gate ran on a fixture repository under `FILES_ROW` with `tests` and no
`-n`. The base holds `CRASHES_ITS_WORKER` and, separately,
`CRASHES_ITS_WORKER_IN_SETUP`; the branch makes the crashing test
`assert False`. Both give the same result:

```
EXIT 1
WORD new
base record: session; tests/test_one.py setup/call/teardown passed;
             tests/test_two.py::test_ok setup/call/teardown passed;
             tests/test_two.py::test_crash setup passed   (body crash only)
             -- no end line
```

**Why it matters.** `new` says the branch broke `tests/test_two.py`. The
base's own run crashed in that file, so whether the base fails it was not
measured. This is round 4's 🟡 2, word for word, without xdist: the same two
module constants, the same branch edit, the same false `new`. Round 4's fix
and round 5's narrowing both read the demotion off `end` lines, so neither
reaches it. A recorder that gave up writing part-way (a disk that filled)
leaves the same shape.

**Where the line is.** The defect predates round 5: `base_word` gave `new`
here at round 4's target too. It is reported in the units round 5's fixes
changed (`read_record`, `base_word`) because that is where the class would
have been enumerated.

**The fix.** Count the base's sessions that wrote no `end` line, and demote
`new` where any did. **Executed** with the fix below applied in the clone:
both probe layouts read `new?` with the new reason; the gate module passes
whole (431 passed) and the recorder module's selected cases pass (49
passed). Rule 3, the **New?** bullet, the changelog and the module's
pinned-sentence cases need the new reason under §14; that text is not
written here.

## ⬜ 2 — the worker map is keyed on `id()` of an object it does not hold

`self.last_sent[id(sender)]` (`specseal_pytest_record.py:189`) keeps a
tuple, not the worker. CPython reuses an address once its object is freed.
xdist replaces a crashed worker with a new controller object. Where the old
one is freed, the new one can take its id and inherit the old entry. That
entry is the crashed node's `setup` or `call`. A node sharing that node's
id, crashing on the new worker before any report, would then take the old
file's path.

Read, not executed. The terminal reporter keeps every failed report, and the
crash report holds the old worker in `rep.node`, so in an ordinary run the
old object stays alive and no id is reused. Keying on the worker object
itself removes the dependence on that.

## ⬜ 3 — the overview does not record the strict `new` as a divergence

`spec.md` Scope 1 (`:235`) says nothing in the comparison table depends on
the `end` line, and Scope 5's table has five rows. Since round 4 the
`end` line decides a sixth word, and since round 5 it reads the line's
`exitstatus` too. The overview's divergence table
(`seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:37`)
has no row for it; only the prose above it mentions the change. Add a row:
spec says the table ignores the `end` line, the code demotes `new` on a red
session's count, chosen by the orchestrator in round 4's fix pass, narrowed
in round 5.

## Round 5's findings, answered

- 🔴 1, a crash placed by a colliding node id — **closed**. Executed: the
  two new recorder cases and the `path_of` unit case are red with
  `4e3b41e0`'s recorder in place (3 failed) and pass at the target. The W1
  probe reproduces (below).
- 🟡 2, a green base demoting `new` — **closed**. Executed: the
  `exitstatus` test mutated to always count turns
  `test_the_unplaced_counts_of_this_runs_records_are_summed` and
  `test_the_failure_form_says_how_many_tests_the_record_left_out` red; at the
  target both pass.
- ❓, the macOS and Windows `pytest` legs — **answered**: both pass at
  `475a3875`.

Round 5's `New units` (the collision constants, the two recorder cases, the
renamed `base_word` case) were read as code. The collision case plants the
shared id through a conftest's `Module.from_parent(..., nodeid=...)` and
asserts the collision happened before asserting the path, so it cannot pass
on a run where the ids differ. No finding in them.

## The pytest 7.4 probe held in ledger W1's executed cell — it holds

W1's cell says: pytest 7.4.4 and xdist 3.8.0 through `uvx`, `-n 1`,
`--import-mode=importlib`, rootdir forced to a sibling with `--rootdir=. -c
pytest.ini`, arguments `../a/test_m.py ../b/test_m.py` and `../a ../b`; a
body crash written failing under `b/test_m.py`, a fixture crash written as
no line with `unplaced` 1, and `a` passing in all four.

Executed with exactly those flags, at the target's recorder and at
`4e3b41e0`'s:

| Recorder | Crash | Arguments | Crash line | `unplaced` | `a` |
|---|---|---|---|---|---|
| target | body | files, dirs | failed under `b/test_m.py` | 0 | passing |
| target | fixture | files, dirs | none | 1 | passing |
| `4e3b41e0` | body | files, dirs | failed under `a/test_m.py` | 0 | failing |
| `4e3b41e0` | fixture | files, dirs | failed under `a/test_m.py` | 0 | failing |

The node ids collide as claimed: `::test_crash` for file arguments and
`test_m.py::test_crash` for directory arguments. Every claim in the cell
holds, and the old recorder shows the probe can fail.

## PR #846's checks at `475a3875`

Read with `gh pr checks 846`; both runs' `headSha` is `475a3875`, event
`pull_request`.

| Workflow | Job | State |
|---|---|---|
| tests | `pytest (ubuntu-latest, 3.12)` | pass, 8m30s |
| tests | `pytest (macos-latest, 3.12)` | pass, 21m18s |
| tests | `pytest (windows-latest, 3.12)` | pass, 37m23s |
| hygiene | `arm-check-grammar (3.13)` | pass |
| hygiene | `arm-check-grammar (3.14)` | pass |
| hygiene | `ledger` | pass |
| hygiene | `lint` | pass |
| hygiene | `release` | pass |

The other three workflows under `.github/workflows/` trigger on a push to
`main` or `release/*` or on a tag, so none is expected on a pull request.
Nothing is red or missing.

## Earlier rounds, carried

Round 5 carried rounds 1 to 4's closures. Round 5's fixes touch what those
verdicts rest on only at `path_of` and the demotion, both judged above. So
rounds 1 to 4 are carried from round 5's record, not re-derived; the 49
recorder and gate cases passing at the target are the executed check under
them.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py` — the probe's shape
  as a case: `files_row(False) + " tests"`, base `CRASHES_ITS_WORKER` and
  `CRASHES_ITS_WORKER_IN_SETUP` (parametrized), branch `assert False`; the
  word is the new reason and never `NEW`. Seen red at the target: both read
  `new` (executed above).
- The same module, at `read_record`: a keyed file with a session line and a
  test line and no `end` line counts one unended session; a file with an
  `end` line counts none.
- `pytest_record` unit case: a second worker object created after the first
  is dropped does not inherit its entry, if ⬜ 2 is taken.

## Facts for the evidence ledger

- W8 and the **New?** bullet: after 🟡 1's fix, `new` also reads `new?`
  where a session of the base wrote no `end` line.
- W1: the round 5 probe is reproduced at the target (this round's table
  above); the cell needs no change.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Without xdist a test that kills pytest at the base leaves a session with no `end` line, which the demotion never reads, so the file reads `new` though the base crashed in it: round 4's 🟡 2 without xdist | `skills/verify/scripts/broad_gate.py:1974` | open | executed: the gate on `FILES_ROW tests`, base `CRASHES_ITS_WORKER` and `CRASHES_ITS_WORKER_IN_SETUP`, branch `assert False`, reads `new` both times with a base record that has no `end` line; with the fix applied both read `new?`, the gate module 431 passed |
| ⬜ 2 | The worker map is keyed on `id()` of a worker it does not hold, so a replacement worker could inherit a freed worker's entry | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:189` | open | read: the terminal reporter keeps the crash report, which holds the old worker, so an ordinary run reuses no id |
| ⬜ 3 | The overview's divergence table has no row for the strict `new`, which spec Scope 1 and Scope 5 do not describe | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:37` | open | read: `spec.md:235` says nothing in the table depends on the `end` line; a correction to the run's paperwork |
| 🟢 | round 5's blocking finding 1 is closed — a crash is placed only by its own worker's last report | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:184` | confirmed | executed: the three new cases are red with `4e3b41e0`'s recorder and pass at the target; the W1 probe on pytest 7.4.4 reproduces in all four layouts |
| 🟢 | round 5's finding 2 is closed — a session that exited 0 demotes nothing | `skills/verify/scripts/broad_gate.py:1977` | confirmed | executed: the exit test mutated to always count turns two cases red; both pass at the target |
| 🟢 | round 5's question is answered — the macOS and Windows `pytest` legs pass | PR #846 | confirmed | read: `gh pr checks 846`, every job of both workflows passes at `475a3875` |
| carried | rounds 1 to 4's closures, as round 5 carried them | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/rounds/round-5.md` | confirmed | carried, not re-derived: round 5's fixes touch only `path_of` and the demotion, judged above; 49 recorder and gate cases pass at the target |

## Paste-ready fixes

### 🟡 1

```python
    __slots__ = (
        "collected",
        "failing",
        "sessions",
        "skipped",
        "unended",
        "unplaced",
        "unplaced_red",
    )

    def __init__(self):
        self.sessions, self.skipped, self.unplaced = 0, 0, 0
        self.unplaced_red, self.unended = 0, 0
        self.failing, self.collected = {}, set()
```

```python
        record.sessions += 1
        # A session with no `end` line stopped part-way: its process died,
        # or its recorder stopped writing (#825 round 6).
        if not any(value.get("kind") == "end" for value in parsed[1:]):
            record.unended += 1
```

```python
# Formatted with how many of the base's sessions wrote no `end` line, where a
# file would read `new`: such a session stopped part-way -- its process died,
# as plain pytest does on a test that calls `os._exit` or segfaults, or its
# recorder stopped writing -- so what it held passing may not have finished
# (#825 round 6, round 4's 🟡 2 without xdist).
UNENDED_AT_BASE = (
    f"{NOT_MEASURED}: the row ran once at the base, and {{count}} of its pytest "
    "sessions wrote no end to their record, because the process died or the "
    "recorder stopped writing part-way through, so this file's tests there may "
    "not have finished and whether the base fails it was not measured (kept "
    "as suite-at-base.txt, with records/ beside it)"
)
```

```python
    if path in record.collected or code == 0:
        if record.unplaced_red:
            return UNPLACED_AT_BASE.format(count=record.unplaced_red)
        if record.unended:
            return UNENDED_AT_BASE.format(count=record.unended)
        return NEW
```

```
Either `new` reads `new?` naming the count instead where a session of the
base wrote no end to its record, because its process died part-way --
plain pytest on a test that calls `os._exit` or segfaults -- or its recorder
stopped writing.
```

### ⬜ 2

```python
        if isinstance(path, str):
            if sender is not None:
                when = getattr(report, "when", None)
                self.last_sent[sender] = (report.nodeid, when, path)
        elif sender is not None:
            last = self.last_sent.get(sender, (None, None, None))
            if last[0] == report.nodeid and last[1] != "teardown":
                path = last[2]
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on the recorder module and the gate module `-k "recorder or unplaced or crash or session or left_out or unmeasured or measurement_its_cost or what_a_line_names or before_the_runner or record_files or base_word or new_question"`, in the clone at `475a3875` | 49 passed |
| The three cases round 5 planted in the recorder module, with `4e3b41e0`'s recorder copied over the target's | 3 failed: the crash written under `a`, and the unit case's `/r/a.py` where None was expected |
| The gate module's `-k "unplaced or left_out or new_question"` with `read_record`'s exit test replaced by `if True:` | 2 failed, 1 passed |
| W1's probe: pytest 7.4.4 and pytest-xdist 3.8.0 through `uvx`, `-n 1`, `--import-mode=importlib`, `--rootdir=. -c pytest.ini`, file and directory arguments, body and fixture crash, at the target's recorder and at `4e3b41e0`'s | as the W1 table above: target places the body crash under `b`, counts the fixture crash, `a` passes; `4e3b41e0` writes both under `a` |
| The gate on a fixture repository, `FILES_ROW tests` without `-n`, base `CRASHES_ITS_WORKER` and `CRASHES_ITS_WORKER_IN_SETUP`, branch `assert False` | exit 1, `tests/test_two.py  new` both times; the base record has no `end` line |
| The same, with 🟡 1's fix applied in the clone | both read `new?` with the unended reason |
| The gate module whole, with 🟡 1's fix applied in the clone | 431 passed |
| `gh pr checks 846`, and `gh run view` on both runs | eight jobs pass; both runs at `475a3875` |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: not run by this round. It is the sealer's, once, after the rounds settle; it comes due when the orchestrator closes this record |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (a test that kills plain pytest at the base leaves a session with no `end` line, and the file reads `new`)
Loses a record or crashes: no

## Proof block

Files opened this round: `handoff.md`, `overview.md`, `routing.md`,
`rounds/round-5.md` and `rounds/round-5-report.md` of this work item;
`spec.md` (§*The class*, Scope 1 to 6, the foot); the ledger fragment's W1;
`skills/verify/scripts/pytest_record/specseal_pytest_record.py` whole;
`skills/verify/scripts/broad_gate.py` from `RunRecord` to
`compare_at_base`, the failure form and the gate's suite branch; the fix
range's diff of `tests/test_the_recorder_writes_what_its_process_ran.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, `skills/verify/SKILL.md`,
`templates/config.md`, the changelog fragment and `survivors.md`; xdist
3.8.0's `dsession.py`, `workermanage.py` and `scheduler/load.py` · NAME NOT IN TREE; the
five files under `.github/workflows/`.
