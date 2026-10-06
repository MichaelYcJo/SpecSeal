# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — review round 1

| Field | Value |
|---|---|
| Target SHA | 1bbbdca9457ea9fddee51b6dd198869e3660b52f |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #846 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | no |
| Needs a fix | yes — 🔴 1 (a file outside pytest's rootdir is recorded under the wrong path, and a file the branch broke reads `failing on base too`), 🟡 2 (rule 3 does not name the rest of Q2's class), 🟡 3 (the recorder's warning raises out of a hook under warnings-as-errors) |
| Loses a record or crashes | yes — 🟡 3: with the records file unwritable and warnings as errors, the measured pytest ends in INTERNALERROR, exit 3, and its own result is lost |

- [ ] Pass

## What this round was asked

Round 1 of the chain the owner chose (`routing.md`, `automation`). The reviewer was asked to judge spec compliance first against `spec.md`, `plan.md`, `questions.md`, `overview.md` and the phase records over `origin/release/v0.20.0..1bbbdca9`, including phase 4's divergence from `spec.md` R4 (the recorder writes the collecting module), without reopening the owner's Q1 and Q2, then quality, without running the full suite, and to consider which neighbouring modules read what the change touches. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the eight changed Python files, the changed test modules with five neighbouring hygiene modules (873 passed, 1 skipped), and `bin/evidence-check --strict .` (exit 0).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The recorder joins `report.fspath` to the rootdir, which names a file outside the rootdir against the wrong directory; two files share one name and a file the branch broke reads `failing on base too` from another file's failure at the base | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:144` | open | executed: `pytest tests sub` with `sub/pytest.ini`, and `-c ci/pytest.ini`, `--rootdir=ci` over two `test_x.py` files, each gave `failing on base too` to a file the base passes; the strict fix turns each into `NO_RECORD_AT_HEAD`, the planted case is red without it and green with it, and the corpus's Q3b "own" row moves |
| 🟡 2 | Rule 3 names only a replaced `PYTHONPATH` as failing at the gate; `python -I`, `python -E` and a wrapper passing `PYTEST_ADDOPTS` alone fail a green suite the same way, while rule 3 says such wrappers' files read `new?` | `templates/config.md:334` | open | executed: a one-test green suite exits 1 with the recorder's import error under `-I` and `-E`, and 0 plain; read: tox 4.64.9's default pass-env list |
| 🟡 3 | The recorder's warning raises out of a hook under warnings-as-errors, ending the measured run in INTERNALERROR | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:103` | open | executed: `python -W error` with an unwritable records directory, exit 3; with the warning under its own filter, exit 1 (the planted test) and no INTERNALERROR |
| ⬜ 4 | Phase 4's correction of R4 was not fed back: `spec.md` still says `report.location[0]` and "two files at one relative path coincide only for one file", and `overview.md` says nothing was fed back | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:48` | open | read; paperwork correction, not counted in Needs a fix; also `spec.md:79`, `spec.md:117`, `spec.md:154`, `plan.md:89`, `plan.md:115` |
| ⬜ 5 | The failure form heads `NO_RECORD_AT_HEAD` rows with "compared at the base", where the base was not run | `skills/verify/scripts/broad_gate.py:2940` | open | read; each row's reason says the base was not run, so behaviour and fact are right |
| 🟢 | Q1 and Q2 built as (a) | `skills/verify/scripts/broad_gate.py:2038`, `templates/config.md:334` | confirmed | read: `base_word` gives `NOT_REACHED` with the exit on a non-zero base for a file in no session; rule 3 and the Q2 case hold the replaced-`PYTHONPATH` row failing at the gate |

## Paste-ready fixes

```python
    def an_argument_lies_outside_the_rootdir(self):
        """Whether pytest was handed a path outside its rootdir (`-c` or
        `--rootdir` elsewhere, or a config file in one argument's directory).
        pytest names a file there against the argument that reached it, not
        against the rootdir, so its node id's path joined to the rootdir names
        no file, and two files under two arguments share one name. Such a
        session writes no record: the strict side."""
        root = os.path.realpath(self.rootdir)
        here = _invocation_dir(self.config)
        for argument in getattr(self.config, "args", None) or ():
            path = os.path.realpath(os.path.join(here, str(argument).split("::")[0]))
            if not os.path.exists(path):
                continue
            try:
                inside = os.path.commonpath([root, path]) == root
            except ValueError:
                inside = False
            if not inside:
                return True
        return False

    def pytest_sessionstart(self, session):
        if self.an_argument_lies_outside_the_rootdir():
            return
        name = f"{self.key}-{os.getpid()}.jsonl"
```
```
That holds only where pytest names files against the rootdir, which it does
for every file under it. A session handed a path outside its rootdir names
those files against the argument instead, so it writes no record, and its
files read `new?` (#825 round 1).
```
```python
def test_a_file_pytest_names_outside_its_rootdir_earns_no_word(tmp_path):
    """#825 round 1. `pytest tests sub` with `sub/pytest.ini` makes `sub`
    pytest's rootdir, and pytest names `tests/test_x.py` against the argument
    that reached it, `test_x.py` — the name `sub/test_x.py` has. Joined to the
    rootdir, the base's failure in `tests/` was recorded as `sub/test_x.py`'s,
    and the file the branch broke read `failing on base too`."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{FILES_ROW} tests sub",
        {
            "sub/pytest.ini": "[pytest]\n",
            "tests/__init__.py": "",
            "sub/__init__.py": "",
            "tests/test_x.py": "def test_root():\n    assert False\n",
            "sub/test_x.py": "def test_sub():\n    assert True\n",
        },
        {"sub/test_x.py": "def test_sub():\n    assert False, 'planted on the feature'\n"},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert gate.ON_BASE not in out.stdout, out.stdout
    assert verdict_of(out.stdout, "sub/test_x.py") == gate.NO_RECORD_AT_HEAD, (
        out.stdout
    )
```
```python
    # `tests` lies outside the rootdir `a/` that `a/pytest.ini` makes, so
    # the row's pytest writes no record and the base is not run.
    ("Q3b", "own"): {"a/b/tests/test_two.py": "no-record-at-head"},
```
```python
    if kind == "no-record-at-head":
        return gate.NO_RECORD_AT_HEAD
    if kind == "no-record":
        return gate.NO_RECORD
```
```
One limit is named rather than closed: a test written to append to the record file the recorder is writing, or to write a record of its own with the gate's key, can put a line into a keyed record, and that is the one way to a wrong `failing on base too`. A pytest handed a path outside its rootdir — `-c` or `--rootdir` elsewhere, or a config file in one of its arguments' directories — names those files against the argument rather than the rootdir, so it writes no record and its files read `new?`
```
```
A row that keeps `PYTEST_ADDOPTS` and loses `PYTHONPATH` fares worse — one that replaces `PYTHONPATH`, an interpreter run with `-I` or `-E`, a wrapper that passes `PYTEST_ADDOPTS` or `PYTEST_*` on and not `PYTHONPATH`: pytest cannot import the module the `-p` names and exits 1 before any test runs, so the row fails at the gate.
```
```python
    def give_up(self, error):
        # Shown, never raised: a row that runs with warnings as errors
        # (`python -W error`, `filterwarnings = error`) would otherwise turn
        # this one warning into an exception out of a hook (#825 round 1).
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            warnings.warn(
                f"specseal_pytest_record: no record written: {error}", stacklevel=2
            )
        stream, self.stream = self.stream, None
        if stream is not None:
            try:
                stream.close()
            except (OSError, ValueError):
                pass
```

## Executed probes

| What was run | Result |
|---|---|
| Recorder under `-c ci/pytest.ini` and `--rootdir=ci` over `tests_a/test_x.py` and `tests_b/test_x.py` (a test_tmp probe in the round's scratch directory, worktree `.venv`, pytest 9.1.1) | both recorded as `ci/test_x.py`, which does not exist; `read_record` lists one failing file for two |
| End to end through `recording_env`, `read_record` and `compare_at_base`: `-c` layout; `pytest tests sub` with `sub/pytest.ini` | `failing on base too` for the file the branch broke, in both |
| The same, `-n 2 -x --dist=loadfile`, a base stopped early on another file | no false `new`: xdist ran the stopped worker's whole file; no finding |
| 🔴 1's fix applied in the clone: the probe; the recorder module; the gate module `-k "cd_row or two_runners or rootdir or every_layout or symlinked or twice"` | no record outside the rootdir; 10 passed; 68 passed, 1 failed (Q3b "own", the expected word move) |
| 🔴 1's planted case in the clone, without and then with the fix | 1 failed (`sub/test_x.py  failing on base too`), then 1 passed |
| A green one-test suite under `recording_env` run as `python`, `python -I`, `python -E` | exit 0 with a record; exit 1, import error; exit 1, import error |
| `uvx --from tox` reading tox's default pass-env lists | tox 4.64.9 passes neither `PYTHONPATH` nor `PYTEST_ADDOPTS` by default |
| Recorder with an absent records directory, plain and `python -W error` | exit 1 (planted failure) with a warning; exit 3, INTERNALERROR |
| 🟡 3's fix applied in the clone, the same `-W error` run; the recorder module | exit 1, no INTERNALERROR, the warning shown once; 10 passed |
| Neighbouring modules in the clone at 1bbbdca9, `-n auto`: interpreter, encoding, document-names-a-script, broad-gate rule, rules-have-one-owner, no-passage-pasted, docs line wrap, absence claims, gate-names-every-step, broad-gate cell, released-row re-read, merge-drops-a-correction, unverified rows, mutation bytecode, mode row, parallel-agent scratch, printed ledger name, records carried out and in | 1362 passed, 7 skipped, exit 0 |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet — not run by this round; the sealer's, once, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
