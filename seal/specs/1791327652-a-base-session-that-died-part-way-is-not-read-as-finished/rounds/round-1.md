# 1791327652-a-base-session-that-died-part-way-is-not-read-as-finished — review round 1

| Field | Value |
|---|---|
| Target SHA | 30ca8903849995226a94873430c6ab29ae4c2858 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #851 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1 (a base session pytest interrupted still reads `new`), 🟡 2 (at HEAD a stopped session's file is missing from the failing list), 🟡 3 (the hash guard lets a raising hash out of the report hook; the smith may answer it with grounds) |
| Loses a record or crashes | yes — 🟡 3: `path_of` raises out of `pytest_runtest_logreport` for a node whose hash method raises other than `TypeError` (executed at the unit; the INTERNALERROR that follows is read) |

- [ ] Pass

## What this round was asked

Round 1 of #849's review run, at 30ca8903, the head of draft PR #851, over `origin/release/v0.20.0...HEAD` from 6de64c19. The frame is round 6 of work item 1791270161. The reviewer was asked to judge:
- whether counting sessions with no `end` line closes the class of a base session that stopped part-way, including a session killed before its first line, a record cut mid-line and a dead xdist controller;
- the hash guard the smith added to `path_of`;
- whether ⬜ 2's mutation, which survives alone and is caught with round 5's case, is bound enough;
- the in-place edits to 1791270161's fragment and its 30 re-stamped rows;
- every workflow of `gh pr checks 851`.

It did not run the full suite.

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

```python
# The `end` exits of a pytest session that ran to its end: its tests passed,
# some failed, or it collected none. pytest's interrupted exit (2) -- a
# `KeyboardInterrupt` or `pytest.exit()` in a test, or xdist under `-x` or
# `--maxfail` -- and its internal-error exit (3) are a session that stopped
# part-way and still wrote its `end` line (#849 round 1).
RAN_TO_ITS_END = (0, 1, 5)
```
```python
        # A session stopped part-way where it wrote no `end` line -- its
        # process died, or its recorder stopped writing (#849, #825 round 6)
        # -- or where its `end` line shows an exit pytest gives a session it
        # stopped itself (#849 round 1).
        ends = [value for value in parsed[1:] if value.get("kind") == "end"]
        if not ends or any(end.get("exitstatus") not in RAN_TO_ITS_END for end in ends):
            record.unended += 1
```
```python
UNENDED_AT_BASE = (
    f"{NOT_MEASURED}: the row ran once at the base, and {{count}} of its pytest "
    "sessions stopped part-way, because the process died, the recorder stopped "
    "writing, or pytest ended the session interrupted, so this file's tests "
    "there may not have finished and whether the base fails it was not "
    "measured (kept as suite-at-base.txt, with records/ beside it)"
)
```
```
Either `new` reads `new?` naming the count, too, where a session of the base
stopped part-way: it wrote no `end` line to its record, because its process
died, as plain pytest does on a test that calls `os._exit` or segfaults, or
its recorder stopped writing, a disk that filled among the causes; or its
`end` line shows pytest's interrupted or internal-error exit, as a
`KeyboardInterrupt` or `pytest.exit()` in a test and xdist under `-x` give.
Either way the file's tests there may not have finished.
```
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
```python
def failure_lines(check, verdicts=None, unplaced=0, unended=0):
    ...
    if unplaced:
        lines.append(UNPLACED.format(count=unplaced))
    if unended:
        lines.append(UNENDED_HERE.format(count=unended))
```
```python
        verdicts, unplaced, unended = None, 0, 0
        if name == SUITE:
            ...
            head = read_record(records_dir(keep), head_key, root)
            unplaced, unended = head.unplaced, head.unended
            ...
        failures.append((name, failure_lines(check, verdicts, unplaced, unended)))
```
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
```
        The map is keyed on the worker's `id()` and holds the worker in the
        value, so a worker xdist makes to replace a crashed one cannot take
        the freed one's address and its last report with it (#849). Nothing
        is asked of the worker but its identity, so any `node` is a sender.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
