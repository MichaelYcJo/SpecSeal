# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — review round 3

| Field | Value |
|---|---|
| Target SHA | 3066abf6e88067ba2c26d7b8b496691cb5bf968f |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #846 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `2240347308d44d366442b4f0b9d5a086c07e7ad9..2240347308d44d366442b4f0b9d5a086c07e7ad9`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | second — 🔴 1 at skills/verify/scripts/pytest_record/specseal_pytest_record.py#Recorder, a unit round-2's fixes changed; 🔴 2 at skills/verify/scripts/pytest_record/specseal_pytest_record.py#Recorder, a unit round-2's fixes changed; the fix passes stop here and the work item goes back to its framer |
| Needs a fix | yes — 🔴 1 (a dotted `--pyargs` name is imported at `pytest_sessionstart` and the recorder changes an outcome), 🔴 2 (a failed collection named after a parent below the root records two files under one directory and the gate gives a file the branch broke `failing on base too`), 🟡 3 (the gate says no pytest loaded the recorder where one loaded it and refused) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the verifying round for round 2's fixes at `daecd505..e8d4b77c`, which had recorded the run's first fix of a fix. The reviewer was asked to judge the fix pass's derivation of the 🔴's class from pytest 9.1.1's source against that source, to open every fix, inheriting rounds 1 and 2, and to judge the rest of `origin/release/v0.20.0..3066abf6`, without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the four changed Python files and four modules (615 passed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The refusal's `find_spec` imports a dotted `--pyargs` name's package at `pytest_sessionstart`, before a conftest's own hook, so the recorder changes an outcome: a passing test fails under the gate (spec Scope 1: it never changes an outcome) | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:192` | deferred the frame | the frame — the second fix of a fix in the run; executed: `--pyargs pkg.test_a` with a conftest setting at sessionstart what the package reads at import, exit 0 without the recorder and exit 1 with it; the locator fix below passes it, 19 recorder and 6 gate cases pass with it; the proposed case red at the target and green with the fix |
| 🔴 2 | A failed collection of a collector a conftest builds below the root for files outside the rootdir is recorded under the parent directory, and the gate gives a file the branch broke `failing on base too` | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:115` | deferred the frame | the frame — the second fix of a fix in the run; executed: the gate printed `sub/tests  failing on base too` for a branch that broke `ext/test_new.py`, the base failing `ext/test_old.py`; with the fix, the case passes, 19 recorder and 169 gate cases pass; the case red at the target |
| 🟡 3 | Where the recorder loaded and refused or abandoned its record, the gate says no pytest loaded the recorder and points at the environment | `skills/verify/scripts/broad_gate.py:2015` | deferred the frame | the frame — the second fix of a fix in the run; executed: `test_a_file_pytest_names_outside_its_rootdir_earns_no_word` passes asserting this text for a row whose pytest loads the recorder; read: `NO_RECORD` at line 2021 says the same of the base |
| ⬜ 4 | The guard abandons a whole record, silently, for a test with no file of its own or one whose module removes itself, and rule 3 names neither | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:115` | deferred the frame | the frame — the second fix of a fix in the run; executed: a session-parented item and a self-removing module each left no record and no warning; read: pytest-mypy 1.0.1 parents its status item to a file and is not affected; strict side, no wrong word |
| ⬜ 5 | `spec.md` Scope 1 and §The class still describe round 1's refusal only | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:161` | deferred the frame | the frame — the second fix of a fix in the run; read; paperwork correction, not counted in Needs a fix |
| 🟢 | round 2's blocking finding is closed — a `--pyargs` package outside, a namespace package, a rootdir or argument through a symlink and a collector built at the root no longer record under another file's name, and a symlinked directory under the rootdir is recorded | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:157` | confirmed | executed: eight mutants of the refusal and the guard, each red against its case; 19 recorder cases pass at the target; finding 2 above is a further branch of the same class |
| 🟢 | round 2's ⬜ 2 is closed — rule 3 says the refused files are measured as a runner's that did not load the recorder | `templates/config.md:334` | confirmed | read: rule 3 and the `compare_at_base` docstring |
| 🟢 | round 2's ⬜ 3 is closed — a base that could not be checked out gets its own heading | `skills/verify/scripts/broad_gate.py:2951` | confirmed | read: `failure_lines` and `compare_at_base`, which gives the word to every file or none; the new case pins the three headings |
| 🟢 | round 2's ⬜ 4 is closed — the `--pyargs` case pins the `exists` skip | `tests/test_the_recorder_writes_what_its_process_ran.py:319` | confirmed | executed: the skip deleted, the case red |
| 🟢 | round 1's 🟡 3 is closed — the recorder's warning is never raised under warnings as errors | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:140` | confirmed | read: `give_up` unchanged; executed: the `-W error` case passes among the 19 |
| 🟢 | round 1's 🟡 2 is closed — rule 3 names Q2's whole class | `templates/config.md:334` | confirmed | read: the `-I`, `-E` and wrapper sentence still stands |

## Paste-ready fixes

```python
def _spec_without_importing(name):
    """The spec `--pyargs` finds for `name`, found without running any of
    the package's code. `importlib.util.find_spec` imports every parent of
    a dotted name, and the recorder asks at `pytest_sessionstart`, before
    the hooks a conftest or a plugin runs there, so its import would run
    the package earlier than pytest does and could change an outcome (#825
    round 3). The first part is looked up as `find_spec` looks it up, which
    imports nothing; each later part only in its parent's search locations.
    None where it cannot be found that way."""
    import importlib.util
    from importlib.machinery import PathFinder

    parts = name.split(".")
    try:
        spec = importlib.util.find_spec(parts[0])
        for end in range(2, len(parts) + 1):
            places = list(getattr(spec, "submodule_search_locations", None) or ())
            if not places:
                return None
            spec = PathFinder.find_spec(".".join(parts[:end]), places)
    except Exception:
        return None
    return spec
```
```python
            name = str(argument)
            located = None
            if pyargs:
                # pytest splits the selection off before it looks the name up.
                name = name.partition("[")[0].split("::")[0]
                spec = _spec_without_importing(name)
                if spec is None and not os.path.exists(os.path.join(here, name)):
                    # Found only by importing a parent, or not at all: pytest
                    # stops on the second, and the first is not read here.
                    return True
                places = list(getattr(spec, "submodule_search_locations", None) or ())
                if places and namespaces:
                    located = places[0]
                elif places and spec.origin not in (None, "namespace"):
                    located = os.path.dirname(spec.origin)
```
```python
SETS_AT_SESSIONSTART = """\
import os


def pytest_sessionstart(session):
    os.environ["RECORDER_PROBE_READY"] = "1"
"""


def test_a_dotted_pyargs_name_is_located_without_importing_its_package(tmp_path):
    """#825 round 3. `find_spec` imports a dotted name's parent package, and
    the recorder asked it at `pytest_sessionstart`, before a conftest's own
    `pytest_sessionstart`, so a package that reads at import what that hook
    sets was imported too early and a passing test failed under the gate.
    The recorder never changes an outcome (`spec.md` Scope 1)."""
    root, records = project(tmp_path, {})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (root / "conftest.py").write_text(SETS_AT_SESSIONSTART, encoding="utf-8")
    package = root / "pkg"
    package.mkdir()
    (package / "__init__.py").write_text(
        "import os\nREADY = os.environ.get('RECORDER_PROBE_READY')\n",
        encoding="utf-8",
    )
    (package / "test_ready.py").write_text(
        "import pkg\n\n\ndef test_ready():\n    assert pkg.READY == '1'\n",
        encoding="utf-8",
    )
    env = recording_env(records)
    env.pop("RECORDER_PROBE_READY", None)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(root)])
    result = pytest_in(root, env, "--pyargs", "pkg.test_ready")
    assert result.returncode == 0, result.stdout + result.stderr
    _, lines = the_one_record(records)
    assert {line["outcome"] for line in lines if line["kind"] == "test"} == {
        "passed"
    }, lines
```
```python
        kind, path = line.get("kind"), line.get("path")
        empty = os.path.normpath(str(path)) == os.path.normpath(self.rootdir)
        # A failed collection whose node id carries `::` is named after its
        # parent. Under a class that is the module's file; anything else is a
        # collector pytest named after the directory above it (#825 round 3).
        parents = "::" in str(line.get("nodeid", "")) and not os.path.isfile(path)
        if (kind == "test" and not os.path.isfile(path)) or (
            kind == "collect" and (empty or parents)
        ):
```
```python
BUILDS_A_DIR_BELOW_THE_ROOT = """\
from pathlib import Path

import pytest

OUTSIDE = Path(__file__).resolve().parents[2] / "ext"


def pytest_collect_directory(path, parent):
    if path.name == "inner":
        return pytest.Dir.from_parent(parent, path=OUTSIDE)
"""


def test_a_collector_built_below_the_root_for_files_outside_it_earns_no_word(tmp_path):
    """#825 round 3. A conftest in `sub/tests` builds a collector for `ext/`,
    outside the rootdir `sub`, under `tests`, so pytest names each of its
    modules `tests::ext::<file>` and a failed collection's line names the
    directory `sub/tests`. The base cannot collect `ext/test_old.py`, the
    branch breaks `ext/test_new.py`, and both were recorded as `sub/tests`:
    the file the branch broke read `failing on base too`."""
    posix_row_shell_or_skip()
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && {FILES_ROW} tests",
        {
            "sub/pytest.ini": "[pytest]\n",
            "sub/tests/conftest.py": BUILDS_A_DIR_BELOW_THE_ROOT,
            "sub/tests/inner/README.txt": "a directory pytest walks\n",
            "sub/tests/test_near.py": "def test_near():\n    pass\n",
            "ext/test_old.py": "import no_such_module_on_the_base\n",
            "ext/test_new.py": "def test_new():\n    pass\n",
        },
        {"ext/test_new.py": "import no_such_module_on_the_branch\n"},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert gate.ON_BASE not in out.stdout, out.stdout
```
```python
# Where the row's run at `HEAD` left no record carrying its key: no pytest
# loaded the recorder, or the one that did refused to write (rule 3 of
# `templates/config.md`). The files come from the `FAILED` lines of
# `suite.txt`, and the base is not run.
NO_RECORD_AT_HEAD = (
    f"{NOT_MEASURED}: no pytest the row ran here left a record of the gate's "
    "recorder (none loaded it, or the one that did named a file outside its "
    "rootdir and wrote none, templates/config.md rule 3), so this file is "
    "named only by a FAILED line of suite.txt and the base was not run. "
    f"{EARNS_THE_WORD}"
)
# Where the row's run at the base left no record carrying the base's key.
NO_RECORD = (
    f"{NOT_MEASURED}: the row ran once at the base, and no pytest it ran there "
    "left a record of the gate's recorder (none loaded it, or the one that did "
    "named a file outside its rootdir and wrote none; kept as "
    f"suite-at-base.txt, with records/ beside it). {EARNS_THE_WORD}"
)
```

## Executed probes

| What was run | Result |
|---|---|
| The recorder module in the clone at `3066abf6`, `bin/test` | 19 passed |
| `bin/mutation-check` on the recorder, eight mutants, each against its own cases with `-p no:xdist`: namespace branch off; regular-package branch off; comparison made `realpath`; test-line guard off (recorder case and the gate's `--pyargs` case); collect-line guard off; `exists` skip off; located path ignored | all eight red |
| A conftest setting an environment variable at sessionstart, a package reading it at import, `pytest --pyargs pkg.test_a`, without and with the recorder | exit 0 `1 passed` without; exit 1 `1 failed` with, the record holding the failure |
| The same with `@pytest.hookimpl(trylast=True)` on the recorder's `pytest_sessionstart` | exit 0 with the recorder; 19 recorder cases pass |
| The same with the non-importing locator (the fix below) | exit 0, record written; 19 recorder cases pass; gate `-k "pyargs or rootdir or recorder"` 6 passed; `uvx ruff check` and `format --check` pass |
| The proposed 🔴 1 case, at the target and with the fix | 1 failed, then 1 passed |
| A gate run over `cd sub && … tests`, a conftest building a `Dir` for `ext/` under `sub/tests`, base failing `ext/test_old.py`'s collection, branch breaking `ext/test_new.py`'s | `sub/tests  failing on base too`; both records hold a `collect` line with path `sub/tests` |
| The proposed 🔴 2 case, at the target and with the guard fix | 1 failed, then 1 passed; with the fix, 19 recorder cases and 169 gate cases under `-k "pyargs or rootdir or recorder or record or base or measured or collect"` pass; ruff passes |
| A conftest appending a session-parented item beside a failing test; a module that removes its own file | each: no record, no warning |
| `pytest-mypy` 1.0.1's source, read through `uvx --with pytest-mypy` | its status item is parented to a `MypyFile`, so its node id path is a file |
| `bin/evidence-check --ledger` on the work item's ledger fragment | 216 ok, 0 drifted, 0 broken, exit 0 |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: not run by this round. It is the sealer's, once, after the rounds settle; with 🔴 1 and 🔴 2 open it has not come due |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
