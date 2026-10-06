# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — review round 5

| Field | Value |
|---|---|
| Target SHA | d2f9f8a5ad9f58b05bfd090c014e1f2739cf4eb5 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #846 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | first — 🔴 1 at skills/verify/scripts/pytest_record/specseal_pytest_record.py#Recorder, a unit round-4's fixes changed; 🟡 2 at skills/verify/scripts/broad_gate.py#base_word, a unit round-4's fixes changed |
| Needs a fix | yes — 🔴 1 (a crash report's path looked up by node id lands on another file where two nodes share one, and that file reads `failing on base too`), 🟡 2 (a base session that exited 0 still turns `new` into `new?`) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 5, the verifying round for the redesign's round 4, whose fixes at `70bce95b..acb85a74` included one the orchestrator decided past the report: where the base run's record counts `unplaced` > 0, a file that would read `new` reads `new?`. The reviewer was asked to open each fix, judge that decision on a red base and an ordinary green run, inherit rounds 1–4, judge the rest of `a9d7b0e5..d2f9f8a5` and read every workflow's checks, without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the four changed Python files, `bin/survivor-check --range a9d7b0e5...HEAD --exempt <item>/survivors.md` (exit 0) and five modules (653 passed). The orchestrator accepts 🟡 2: the decision it gave the fix pass was over-strict on a green base.

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

## Paste-ready fixes

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
```
names none, unless the same xdist worker's last report was of the same node
and not its teardown, as the `setup` report of a test whose worker then
crashed is.
```
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
```
Either `new` reads `new?` naming the count instead where a session of the
base that ended non-zero left any test or collection out of every list,
because one of them may be the file's failure: a test whose xdist worker died
in its setup, before any report of it reached the controller, is one. A
session that exited 0 failed nothing, so what it left out cannot be.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:144` | round 1's 🔴 1 — fixed |
| round-1 | `templates/config.md:334` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:103` | round 1's 🟡 3 — fixed |
| round-1 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:48` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2940` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2038`, `templates/config.md:334` | round 1's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:135` | round 2's 🔴 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2947` | round 2's ⬜ 3 — fixed |
| round-2 | `tests/test_the_recorder_writes_what_its_process_ran.py:319` | round 2's ⬜ 4 — fixed |
| round-2 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:117` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:79` | round 2's 🟢 — confirmed |
| round-3 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:192` | round 3's 🔴 1 — deferred |
| round-3 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:115` | round 3's 🔴 2 — deferred |
| round-3 | `skills/verify/scripts/broad_gate.py:2015` | round 3's 🟡 3 — deferred |
| round-3 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:161` | round 3's ⬜ 5 — deferred |
| round-3 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:157` | round 3's 🟢 — confirmed |
| round-3 | `skills/verify/scripts/broad_gate.py:2951` | round 3's 🟢 — confirmed |
| round-3 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:140` | round 3's 🟢 — confirmed |
| round-4 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:152` | round 4's 🟡 2 — fixed |
| round-4 | `skills/verify/scripts/broad_gate.py:2023` | round 4's 🟡 3 — fixed |
| round-4 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:84` | round 4's ⬜ 4 — answered |
| round-4 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4643` | round 4's 🟢 — confirmed |
| round-4 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:103` | round 4's 🟢 — confirmed |
| round-4 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/survivors.md:25` | round 4's 🟢 — confirmed |
| round-4 | PR #846 | round 4's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
