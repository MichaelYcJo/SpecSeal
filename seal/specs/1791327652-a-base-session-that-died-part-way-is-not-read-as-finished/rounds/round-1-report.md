# Review round 1 — a base session that died part-way is not read as finished (#849)

Target `30ca8903` (the head of draft PR #851), base `6de64c19`, range
`origin/release/v0.20.0...HEAD`. I reviewed it in a `git clone --no-local` at
the target, under this round's scratchpad directory, which is now removed.
This is the work item's first round, so there is no earlier record of this
item. The frame is round 6 of work item 1791270161, read for its coordinates.

How the findings relate:

```
round 6's finding 1: plain pytest killed by a test at the base -> no `end` line -> `new`
   └─ this branch: a session with no `end` line counts as unended -> `new?`   (closes that instance)
        ├─ 🟡 1: a base session that stopped part-way but still wrote its `end` line
        │        (exit 2: KeyboardInterrupt, pytest.exit, xdist -x) -> still `new`
        └─ 🟡 2: the same stopped session at HEAD -> the failing list omits the file
                 that stopped it, and nothing says a session stopped
round 6's finding 2: the worker map keyed on id()
   └─ this branch: keyed on the worker object, with a hash guard
        └─ 🟡 3: the guard catches only TypeError, and keying by equality
                 merges two distinct nodes that compare equal
⬜ 4: phase-1.md counts the re-stamped rows wrong (a paperwork correction)
```

## Spec compliance first

**Claimed** (spec Scope 1, the U1 row, the overview): `read_record` counts a
keyed session with no `end` line as `unended`, and `base_word` gives
`UNENDED_AT_BASE` where it would give `new`, after the `unplaced_red` check.
**The code** at `skills/verify/scripts/broad_gate.py:1978` and `:2131` does
that. S1 and S2 are red at `6de64c19`'s gate (both read `new`) and pass at the
target. I executed that myself.

**Claimed** (spec Scope 2, U2): `last_sent` is keyed on the worker itself.
**The code** at `skills/verify/scripts/pytest_record/specseal_pytest_record.py:198`
and `:200` does that, with a hash guard at `:191` that the spec does not
describe and the overview records as a divergence. 🟡 3 is about that guard.

**Claimed** (spec Scope 3): 1791270161's overview gains the strict-`new` row.
**The overview** at line 49 of that item has it. The row correctly says the
`end` line decides the word since round 4, reads `exitstatus` since round 5,
and adds `UNENDED_AT_BASE` since #849.

**Spec S3** (existing `new` cases stay green): both modules pass whole at the
target, 468 cases. I executed that.

## Does counting sessions with no `end` line close the class

The class is *a base session that stopped part-way is read as having
measured what it never finished*. I enumerated it against pytest's run
protocol and the recorder's write points. The recorder writes its `session`
line in `pytest_sessionstart`, flushes every line, and writes `end` in
`pytest_sessionfinish`.

| How the session stopped | What the record holds | What the file reads now | How I know |
|---|---|---|---|
| a test kills plain pytest, in its body or a fixture | no `end` line | `new?` (unended) | executed, the S1 and S2 cases |
| the xdist controller dies | no `end` line | `new?` (unended) | executed: a conftest kills the controller in `pytest_sessionfinish` |
| the process dies mid-write, so the last line is cut | the cut line is skipped | a cut `end` line reads `new?` (unended); a cut `session` line leaves no session, so the run reads `NO_RECORD` | executed at `read_record` |
| the process dies before its first line | no file, or an empty file | not a session at all: `NO_RECORD` if it was the only one, otherwise its files are uncollected and read `NOT_REACHED`, or `new` only where the row exits 0, which is Q1's trade and out of scope | read |
| the session is interrupted and still writes `end` with exit 2 | `end` line, `unplaced` 0 | **`new`** | executed, 🟡 1 |
| the same, at HEAD | the stopping test has no failing line | **the file is missing from the list** | executed, 🟡 2 |

So the fix closes the *died* half of the class and not the *interrupted*
half. Every row that stops part-way without a write failure goes through
pytest's own exit and writes its `end` line.

## 🟡 1 — a base session that pytest interrupted still reads `new`

**What is wrong.** Without a dead process, pytest can still stop a session
part-way:

- a `KeyboardInterrupt` raised in a test;
- `pytest.exit()` called in a test;
- xdist under `-x` or `--maxfail`, where the controller raises `Interrupted`
  once the first failure arrives;
- an internal error during the run loop.

In each case `wrap_session` · NAME NOT IN TREE still calls `pytest_sessionfinish`. The recorder
writes `end` with `exitstatus` 2 (3 for the internal error) and `unplaced` 0.
The new check at `skills/verify/scripts/broad_gate.py:1978` only asks whether
an `end` line exists. The `unplaced_red` check adds 0. So a file whose earlier
tests passed before the stop reads `new`.

**Executed.** I ran the gate on a fixture repository under `FILES_ROW tests`
without `-n`. The base's `tests/test_two.py` raises `KeyboardInterrupt` in
`test_crash`, and the branch makes it `assert False`. The result was exit 1
and `tests/test_two.py  new`, with a base `end` line of `exitstatus` 2 and
`unplaced` 0. `pytest.exit("stopped here")` gave the same result.

Under `-n 2 -x --dist loadfile`, the base's `tests/test_a.py` fails after
0.5 s while `tests/test_b.py` is still running. The branch fixes `test_a` and
breaks `test_b.py::test_late`, a test the base never reached. The result was
`tests/test_b.py  new`. The base record holds only `test_first` and
`test_slow_1` (NAME NOT IN TREE, the probe's own) of that file, and an
`end` line with `exitstatus` 2.

**Why it matters.** This is the same false `new` as round 6's finding,
reached through pytest's own stop instead of a dead process. The xdist `-x`
case is the most ordinary of them: a gate row with `-x -n auto` makes every
partly-run file of a failing base read `new` for tests the base never ran.

**The fix.** Count a session as stopped part-way where its `end` line's
`exitstatus` is not one of a session that ran to its end (0, 1, 5).

- **Executed.** I applied the logic in the clone. Both probes above then read
  `new?`, and both modules pass, apart from the S5 case that 🟡 3's fix
  changes on purpose.
- **Not executed.** The reason text, rule 3's sentence and their pins still
  name only the *no end* cause. They need the interrupted cause under §14,
  and the fix below proposes the text.

Plain pytest's `-x` exits 1 and is not counted. That is correct: without
xdist a run stops right after the failing test, so no other file is left
partly run.

## 🟡 2 — at HEAD, a stopped session's file is missing from the failing list

**What is wrong.** The suite branch at
`skills/verify/scripts/broad_gate.py:3380` takes the failing files from the
HEAD record's failing lines. A test that kills plain pytest at HEAD writes a
passing `setup` line and nothing more, so its file never enters that list.
Nothing under the list says a session stopped.

**Executed.** The branch makes `tests/test_a.py` fail normally and makes
`tests/test_two.py::test_crash` call `os._exit(1)`, with no `-n`. The form
reads:

```
failing test files, compared at the base:
  tests/test_a.py  new
no pytest summary in this output, so this exit code is not a count of failing tests: the row may have stopped before any test ran
```

`tests/test_two.py` is not named. The one hint is `NO_SUMMARY`, and it
misdescribes the case: tests did run.

**Why it matters.** The person acts on the listed files. The UNPLACED
sentence exists for exactly this reason: *a person reading the list alone
would not know they ran*. A session that stopped part-way hides more than an
unplaced report does, because the test that stopped it is the failure, and
the list leaves it out. This is the HEAD half of the same class. The branch
had already computed `head.unended` and did not read it.

**The fix.** Pass `head.unended` to `failure_lines` and add a line under the
list. **Executed** in the clone: the probe then shows that line, and both
modules stay green.

## 🟡 3 — the hash guard lets one input raise out of a hook, and merges two equal nodes

**What is wrong.** The guard at
`skills/verify/scripts/pytest_record/specseal_pytest_record.py:191` catches
only `TypeError`. A `node` whose hash method raises anything else now escapes
`path_of` and the report hook. Keying on the object also swaps identity for
equality: two distinct nodes that compare equal share one entry.

**Executed** at the unit:

- a `node` whose hash method raises `ValueError` makes `path_of` raise
  `ValueError`;
- two distinct objects that compare equal, the first sending a `setup` for
  `t::x`: a pathless `t::x` report from the second took `/r/a.py`.

**Why it matters.** The module docstring promises that the recorder "never
raises out of a hook". The overview gives that promise as the guard's own
ground. At `6de64c19` the `id()` key accepted every object, so this input is
newly able to raise. Raised from `pytest_runtest_logreport`, it would end the
row's pytest in INTERNALERROR. I read that last step and did not execute it.
No known plugin sets `report.node` to such an object, so the smith may answer
this with grounds rather than a fix. The fix below also removes the guard and
the equality question at once.

**The fix.** Key on `id()` and hold the sender in the value. A held object
keeps its address, so no later object can take it, which is what round 6
asked for. No hashing is needed, so no guard is needed.

**Executed** in the clone:

- the recorder module passes, 33 cases, with the S5 case's unhashable part
  rewritten as below;
- the rewritten S5 case is red against the target's recorder;
- with the sender not held (`None` stored in its place), S5 is red;
- the two probe inputs above return their own path and no inherited path.

## ⬜ 4 — phase-1.md says "the other 30 rows"; the others are 27

`phases/phase-1.md:19` of this work item says W5, W8 and `Corrected · D1`
were edited and "the other 30 rows … were re-stamped". The fragment's diff
changes 30 rows in all, and those three are among them, so the others number
27. The overview's own wording ("its 30 rows … re-stamped") is right. This is
a paperwork correction and is not counted in `Needs a fix`.

## What the round was asked to judge, answered

**The hash guard.** The guard is bound by a case. With the guard removed, the
S5 case fails on `TypeError: unhashable type: 'list'` (executed). It is not
fully right, which is 🟡 3.

**Round 6's finding 2: the mutation that survives alone.** The mutation keys
only the setter on `id()`. S5 alone stays green under it. **Executed** on the
recorder module, it is red in three cases, not one:

- `test_a_crash_report_takes_a_path_only_from_its_own_workers_report_of_it`;
- `test_a_test_whose_worker_crashed_is_recorded_failing_under_its_file`;
- `test_a_crash_is_never_placed_by_a_node_id_another_file_shares` (body).

The last two run real xdist end to end. S5 pins the negative and these pin
the positive, so the unit is bound in both directions. This is binding
enough.

**The in-place edits to 1791270161's fragment.** W5, W8 and `Corrected · D1`
read faithfully against the code at `skills/verify/scripts/broad_gate.py:2129`
to `:2133` and against rule 3. W5's "where that count is 0" matches the
truthiness test on `unplaced_red`. A word-level diff of the fragment shows
that the other 27 changed rows differ only in their anchors' hashes. I read
every changed row that lists causes of `new` or `new?` (W10, R4, D2, B4, R5),
and #849 contradicts none of them. The CI `ledger` job passes at the target.
One weakness I am not counting as a finding: W5's and W8's **Executed** cells
are still dated 2026-10-06 and cite U1 and U3 for the #849 clause instead of
holding its evidence themselves.

**CI.** At 23:34 UTC, `gh pr checks 851` shows ten jobs passing: lint, both
`arm-check-grammar` jobs, `ledger`, `release`, ubuntu, and all four Windows
groups. `pytest (macos-latest, 3.12)` is still pending. A pending job is a
question, not a pass. The three other workflows
under `.github/workflows/` do not trigger on a pull request.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the 🟡 1 probe as a
  case. Parametrize the base's `test_crash` over `raise KeyboardInterrupt`
  and `pytest.exit("stopped here")`; the branch makes it `assert False`; the
  word is the stopped-part-way reason, never `NEW`. Seen red at the target:
  both read `new` (executed above).
- The same module, with xdist: `-n 2 -x --dist loadfile`, base `test_a.py`
  failing fast and `test_b.py` running slow tests, branch fixing `test_a.py`
  and breaking `test_b.py`'s last test. Seen red at the target: `new`.
- The same module, at `read_record`: a keyed file whose `end` line has
  `exitstatus` 2 counts one stopped session, and 0, 1 and 5 count none.
- The same module, at the failure form: a HEAD row where one file fails and
  another file's test calls `os._exit`. The form carries the stopped-session
  line under the list. Seen red at the target: no such line (executed above).
- `tests/test_the_recorder_writes_what_its_process_ran.py`: the S5 case's
  unhashable part, rewritten as in 🟡 3's fix, with a `node` whose hash method
  raises `ValueError`. Seen red at the target.

## Facts for the evidence ledger

- U1: the unended count covers a session with no `end` line, and after 🟡 1's
  fix also a session whose `end` line shows `exitstatus` 2 or 3.
- U2: after 🟡 3's fix, the map is keyed on `id()` and holds the worker in the
  value, so no guard is needed. Its **Read** cell about the xdist controller
  class defining no equality or hash methods stops being needed.
- The xdist dead-controller layout was executed this round (a conftest calls
  `os._exit` in the controller's `pytest_sessionfinish`). It reads
  `UNENDED_AT_BASE` naming 1, and U1 may cite it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A base session that pytest itself stopped part-way (exit 2 from a `KeyboardInterrupt` or `pytest.exit()` in a test, or xdist under `-x`) writes its `end` line, so neither the unended nor the unplaced check demotes it, and the file reads `new` for tests the base never finished | `skills/verify/scripts/broad_gate.py:1978` | open | executed: the gate under `FILES_ROW tests` reads `new` with a base `end` line of `exitstatus` 2 for both causes; under `-n 2 -x --dist loadfile` `tests/test_b.py` reads `new` for a test the base never ran; with the exit check applied in the clone both read `new?` |
| 🟡 2 | At HEAD a session that stopped part-way leaves the file whose test stopped it out of the failing list, and nothing under the list says a session stopped; `NO_SUMMARY` says tests may never have run | `skills/verify/scripts/broad_gate.py:3380` | open | executed: the branch fails `tests/test_a.py` and kills pytest in `tests/test_two.py`; the form lists only `tests/test_a.py  new`; with the HEAD count passed to `failure_lines` in the clone, the form carries the line and both modules pass |
| 🟡 3 | The hash guard catches only `TypeError`, so a node whose hash method raises anything else escapes `path_of` and the report hook, which the `id()` key never did; keying by equality also merges two distinct nodes that compare equal | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:191` | open | executed at the unit: `ValueError` raised out of `path_of`; an equal second node took the first node's `/r/a.py`; keyed on `id()` with the sender held in the value, both return their own path and the recorder module passes |
| ⬜ 4 | `phases/phase-1.md` says "the other 30 rows" were re-stamped; 30 rows changed in all, W5, W8 and D1 among them, so the others are 27 | `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/phases/phase-1.md:19` | open | read: the fragment's diff changes 30 rows; a paperwork correction |
| 🟢 | The frame's first finding is closed for every way a base process dies after its first line: body, fixture, a dead xdist controller, a cut last line | `skills/verify/scripts/broad_gate.py:1978` | confirmed | executed: S1 and S2 read `new` at the gate of `6de64c19` and pass at the target; the dead-controller probe reads `UNENDED_AT_BASE` naming 1; a cut `end` line counts unended |
| 🟢 | The frame's second finding is closed and bound: the worker map no longer loses a freed worker's address to a new object | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:198` | confirmed | executed: S5 is red at the recorder of `6de64c19`; the setter-only `id()` mutation is red in three recorder cases; removing the guard turns S5 red |
| 🟢 | The frame's third finding is closed: 1791270161's overview carries the strict-`new` row | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:49` | confirmed | read against `base_word` and rounds 4 and 5 of that item |
| 🟢 | The in-place edits to W5, W8 and `Corrected · D1`, and the re-stamped rows, are faithful | `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md:5` | confirmed | read: the three clauses match `base_word` and rule 3; a word diff shows the other 27 rows changed only in anchor hashes; the CI `ledger` job passes |
| ❓ | The `pytest (macos-latest, 3.12)` CI job had not finished | PR #851 | ❓ out of verified scope | read at 23:34 UTC: still pending; the other ten jobs pass, Windows group 3 among them; the orchestrator answers it by reading `gh pr checks 851` again before closing this record |

## Paste-ready fixes

### 🟡 1

`skills/verify/scripts/broad_gate.py`, above `read_record` (executed in the
clone):

```python
# The `end` exits of a pytest session that ran to its end: its tests passed,
# some failed, or it collected none. pytest's interrupted exit (2) -- a
# `KeyboardInterrupt` or `pytest.exit()` in a test, or xdist under `-x` or
# `--maxfail` -- and its internal-error exit (3) are a session that stopped
# part-way and still wrote its `end` line (#849 round 1).
RAN_TO_ITS_END = (0, 1, 5)
```

In `read_record`, replacing the unended check (executed in the clone):

```python
        # A session stopped part-way where it wrote no `end` line -- its
        # process died, or its recorder stopped writing (#849, #825 round 6)
        # -- or where its `end` line shows an exit pytest gives a session it
        # stopped itself (#849 round 1).
        ends = [value for value in parsed[1:] if value.get("kind") == "end"]
        if not ends or any(end.get("exitstatus") not in RAN_TO_ITS_END for end in ends):
            record.unended += 1
```

The reason, with its pin in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it` changed to
match (not executed):

```python
UNENDED_AT_BASE = (
    f"{NOT_MEASURED}: the row ran once at the base, and {{count}} of its pytest "
    "sessions stopped part-way, because the process died, the recorder stopped "
    "writing, or pytest ended the session interrupted, so this file's tests "
    "there may not have finished and whether the base fails it was not "
    "measured (kept as suite-at-base.txt, with records/ beside it)"
)
```

Rule 3's sentence in `templates/config.md`, with its pin in
`test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written`
and the matching sentence of the **New?** bullet (not executed):

```
Either `new` reads `new?` naming the count, too, where a session of the base
stopped part-way: it wrote no `end` line to its record, because its process
died, as plain pytest does on a test that calls `os._exit` or segfaults, or
its recorder stopped writing, a disk that filled among the causes; or its
`end` line shows pytest's interrupted or internal-error exit, as a
`KeyboardInterrupt` or `pytest.exit()` in a test and xdist under `-x` give.
Either way the file's tests there may not have finished.
```

### 🟡 2

`skills/verify/scripts/broad_gate.py`, beside `UNPLACED` (executed in the
clone, text included):

```python
# The line under the listing where a session of the row's pytest at `HEAD`
# stopped part-way: the test that stopped it wrote no failing line, so its
# file is in no list above (#849 round 1).
UNENDED_HERE = (
    "{count} of the row's pytest sessions here stopped part-way -- the process "
    "died, the recorder stopped writing, or the session ended interrupted -- "
    "so the test that stopped it, and any test after it, is in no list above "
    "(the records under records/ hold what ran)"
)
```

In `failure_lines`:

```python
def failure_lines(check, verdicts=None, unplaced=0, unended=0):
    ...
    if unplaced:
        lines.append(UNPLACED.format(count=unplaced))
    if unended:
        lines.append(UNENDED_HERE.format(count=unended))
```

In the gate's suite branch:

```python
        verdicts, unplaced, unended = None, 0, 0
        if name == SUITE:
            ...
            head = read_record(records_dir(keep), head_key, root)
            unplaced, unended = head.unplaced, head.unended
            ...
        failures.append((name, failure_lines(check, verdicts, unplaced, unended)))
```

### 🟡 3

`skills/verify/scripts/pytest_record/specseal_pytest_record.py`, in
`Recorder.path_of`, replacing the guard and the two map accesses (executed in
the clone):

```python
        path = getattr(report, PATH_ATTRIBUTE, None)
        sender = getattr(report, "node", None)
        if isinstance(path, str):
            if sender is not None:
                when = getattr(report, "when", None)
                # Keyed on the worker's id() and holding the worker, so its
                # address cannot be freed and handed to a later object
                # (#849); no hash or equality of the worker is asked for.
                self.last_sent[id(sender)] = (sender, report.nodeid, when, path)
        elif sender is not None:
            last = self.last_sent.get(id(sender), (None, None, None, None))
            if last[1] == report.nodeid and last[2] != "teardown":
                path = last[3]
```

The docstring's last two sentences:

```
        The map is keyed on the worker's `id()` and holds the worker in the
        value, so a worker xdist makes to replace a crashed one cannot take
        the freed one's address and its last report with it (#849). Nothing
        is asked of the worker but its identity, so any `node` is a sender.
```

`tests/test_the_recorder_writes_what_its_process_ran.py`, the end of
`test_a_worker_made_after_another_is_freed_inherits_none_of_its_reports`
(executed in the clone; red against the target's recorder):

```python
    # Keyed on identity, a `node` no dict could key, or one whose `__hash__`
    # raises, is a sender like any other, and nothing raises.
    class Unhashable:
        def __hash__(self):
            raise ValueError("no hash")

    for unkeyable in ([], Unhashable()):
        assert recorder.path_of(
            Report("t::z", "call", unkeyable, "/r/z.py"), "test"
        ) == ("/r/z.py")
        assert recorder.path_of(Report("t::z", "???", unkeyable), "test") == "/r/z.py"
    assert recorder.unplaced == {("test", "t::x")}
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on the recorder module and the gate module, in the clone at `30ca8903` | 468 passed |
| The S5 case and both S1/S2 parameters with the gate and recorder of `6de64c19` checked out in the clone | 3 failed: S5 `assert '/r/a.py' is None`; S1 and S2 `assert 'new' != 'new'` |
| The recorder module with only the setter keyed on `id(sender)` | 3 failed (the three cases named above), 30 passed; S5 passed |
| The recorder module with the hash guard removed | 1 failed: S5, `TypeError: unhashable type: 'list'` |
| The gate on a fixture repository, `FILES_ROW tests` without `-n`, base `test_crash` raising `KeyboardInterrupt`, then calling `pytest.exit`, branch `assert False` | exit 1, `tests/test_two.py  new` both times; base `end` line `exitstatus` 2, `unplaced` 0 |
| The gate under `-n 2 -x --dist loadfile`, base `test_a.py` failing after 0.5 s and `test_b.py` running slow tests, branch fixing `test_a.py` and breaking `test_b.py::test_late` | exit 1, `tests/test_b.py  new`; the base record holds only `test_first` and `test_slow_1` of that file; `end` line `exitstatus` 2 (the probe's own names · NAME NOT IN TREE) |
| The gate under `-n 2` with a base conftest calling `os._exit(1)` in the controller's `pytest_sessionfinish` (tryfirst) | `UNENDED_AT_BASE` naming 1; no `end` line in the base record |
| A first try at the same, a conftest killing the controller from `pytest_runtest_logreport` | the hook did not fire, the base ended with `exitstatus` 0; not evidence either way |
| The gate, the branch failing `tests/test_a.py` and killing pytest in `tests/test_two.py`, no `-n` | the form lists only `tests/test_a.py  new`, then `NO_SUMMARY`; `tests/test_two.py` is not named |
| `read_record` on a keyed file with a cut `end` line, a cut `session` line, and an empty file | cut `end`: sessions 1, unended 1, skipped 1, word `UNENDED_AT_BASE`; cut `session`: sessions 0, word `NO_RECORD`; empty: sessions 0 |
| `Recorder.path_of` with a node whose hash method raises `ValueError`, and with two distinct nodes that compare equal | `ValueError` raised; the second node's pathless report took `/r/a.py` |
| All of the above again, with 🟡 1's exit check, 🟡 2's HEAD line and 🟡 3's identity key applied in the clone | the interrupted and `-x` probes read `new?` (with the reason text unchanged); the HEAD form carries the new line; `path_of` returns `/r/v.py` and `None`; both modules 467 passed, 1 failed (the S5 part the fix rewrites) |
| The recorder module with 🟡 3's fix and the rewritten S5 case; the rewritten case against the target's recorder; the fix with the sender not held | 33 passed; red (`assert None == '/r/z.py'`); red (S5) |
| `gh pr checks 851` and `gh run view` at 23:29 and 23:34 UTC | at 23:34, ten jobs pass; `pytest (macos-latest, 3.12)` pending |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: not run by this round. It is the sealer's, once, after the rounds settle; it comes due when a round leaves nothing open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (a base session pytest interrupted still reads `new`), 🟡 2 (at HEAD a stopped session's file is missing from the failing list), 🟡 3 (the hash guard lets a raising hash out of the report hook; the smith may answer it with grounds)
Loses a record or crashes: yes — 🟡 3: `path_of` raises out of `pytest_runtest_logreport` for a node whose hash method raises other than `TypeError` (executed at the unit; the INTERNALERROR that follows is read)

## Proof block

Files opened this round:

- this work item's `routing.md`, `spec.md`, `plan.md`, `overview.md`,
  `phases/phase-1.md` and `changelog.md`;
- work item 1791270161's `rounds/round-6-report.md`, and the diff of its
  `overview.md`;
- the full diffs of
  `seal/ledger/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote.md`
  (word-level, and rows 5, 8 and 16 whole) and of
  `seal/ledger/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished.md`;
- `skills/verify/scripts/pytest_record/specseal_pytest_record.py` whole;
- `skills/verify/scripts/broad_gate.py` from `recording_env` to
  `compare_at_base`, `failure_lines` with its constants, and the gate's suite
  branch;
- the branch's diffs of `skills/verify/SKILL.md`, `templates/config.md`,
  `tests/test_the_recorder_writes_what_its_process_ran.py` and
  `tests/test_the_seal_is_taken_once_by_the_sealer.py`, and that module's
  helpers (`base_then_feature`, `verdict_of`, `base_records`, `files_row`,
  the crash constants);
- `seal/config.md`, `docs/the-record-layout.md` (the changelog row), `bin/test`,
  and the triggers of the five files under `.github/workflows/`.
