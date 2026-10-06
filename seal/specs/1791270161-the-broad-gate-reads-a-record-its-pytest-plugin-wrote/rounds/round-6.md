# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — review round 6

| Field | Value |
|---|---|
| Target SHA | 475a3875d632cf79a9b011b033e3a56788d0e3d9 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #846 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | second — 🟡 1 at skills/verify/scripts/broad_gate.py#read_record, a unit round-5's fixes changed; the fix passes stop here and the work item goes back to its framer |
| Needs a fix | yes — 🟡 1 (a test that kills plain pytest at the base leaves a session with no `end` line, and the file reads `new`) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 6, the verifying round for round 5's fixes at `4e3b41e0..0fc26b5e` and the review run's last record: round 5 was the redesign run's first fix of a fix, and the reopening is spent. The reviewer was asked to open `path_of` keyed on the sending worker and `unplaced_red` and judge whether each closes its class or only round 5's instance, inherit rounds 1–5, judge the pytest 7.4 probe held in ledger W1's executed cell, and read every workflow of `gh pr checks 846`, without running the full suite. The release branch had moved (#831 at 275a7ce0, #841 at 86cbd9a2) and was not merged in; the round reviewed the branch's own range at 475a3875, the PR head.

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
| round-5 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:182` | round 5's 🔴 1 — fixed |
| round-5 | `skills/verify/scripts/broad_gate.py:2087` | round 5's 🟡 2 — fixed |
| round-5 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:151` | round 5's 🟢 — confirmed |
| round-5 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:184` | round 5's 🟢 — confirmed |
| round-5 | `skills/verify/scripts/broad_gate.py:2027` | round 5's 🟢 — confirmed |
| round-5 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:90` | round 5's 🟢 — confirmed |
| round-5 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/rounds/round-4.md` | round 5's carried — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
