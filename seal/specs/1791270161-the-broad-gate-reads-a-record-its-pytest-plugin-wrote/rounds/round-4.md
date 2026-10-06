# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — review round 4

| Field | Value |
|---|---|
| Target SHA | a1b1caf39d3b1cda9aa5e163e1d11710ef1b40ba |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #846 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (a failed collection laid on the session is written under the rootdir, and on pytest 7.4 a branch's conftest breakage reads `failing on base too`), 🟡 2 (a crashed xdist worker's test is dropped and its file reads `new` at a base that fails it), 🟡 3 (`NO_RECORD` names two causes where the module's own case A5 is a third) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 4, the redesign's first round after the run stopped at round 3 and the framer reframed (`Reframed 2026-10-06 by framer, after round 3.`). The reviewer was asked to judge the rebuilt recorder of phases 5–7 against the reframed frame and Q-M3's measured answer — whether carrying each node's own path on the report closes the misnaming class rounds 1–3 found, whether it changes an outcome, what it does to reports a plugin builds — and to judge the 142 excuses in `survivors.md`, sampling the 24 in live text, over `a9d7b0e5..a1b1caf3`, without running the full suite, reading every workflow's checks on the pull request. Before the round the orchestrator ran `bin/survivor-check --range a9d7b0e5...HEAD --exempt <item>/survivors.md` and `bin/evidence-check --strict .` (both exit 0), and at 83612bd7 lint and eight touched and neighbouring modules (763 passed).

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

## Paste-ready fixes

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
```
It leaves three kinds of report out of every list, counts them on the record's `end` line, and the gate says how many under the failing files: a test with no file of its own, which a conftest or a plugin parents to the session or to a directory; a failed collection of the whole session, which is where pytest 7 lays a conftest's import error anywhere below the root; and a report that reached the recorder without its path, one a plugin built or rebuilt itself.
```
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
```
where no pytest at the base left a record — the row ended before it started one, none loaded the recorder, or the one that did could not write its record and warned in `suite-at-base.txt` — `new?`
```
```
no pytest the row ran at the base left a record, because the row ended there before it started one or for either of those causes
```
```python
# The attribute the two hookwrappers set on a report: the node's own path.
# The recorder's own name, so no field pytest or another plugin reads moves.
# A plugin that writes a report whole -- pytest-reportlog's `--report-log`
# writes what `pytest_report_to_serializable` returns -- writes it too.
PATH_ATTRIBUTE = "specseal_path"
```

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
