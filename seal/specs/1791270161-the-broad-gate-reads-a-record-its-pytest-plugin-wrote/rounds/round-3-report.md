# 1791270161 — review round 3 report (the verifying round, the last of the run)

Target `3066abf6`, fix range `daecd505..e8d4b77c` (round 2's four fixes) plus the round-2 record commit. Reviewed in a `git clone --no-local` at the target in this round's scratch directory, with pytest 9.1.1 and pytest-xdist 3.8.0 in the clone's own runner environment; nothing was written in the worktree except this file. The clone and every probe file are removed.

Two of round 2's fixes open a new defect each. Both sit in units round 2's fixes changed (`Recorder.write` and `Recorder.an_argument_lies_outside_the_rootdir`), and both were seen end to end:

- 🔴 1: the `--pyargs` branch added to the refusal imports the user's package at `pytest_sessionstart`, and a test that passes without the recorder fails with it.
- 🔴 2: the derivation table misses one half of a row. A failed collection of a collector a conftest builds for files outside the rootdir, placed below the root rather than at it, is recorded under a directory. The gate then gives a file the branch broke `failing on base too`, which is the exact word this work item exists to stop.
- 🟡 3 is older and depth 0. Wherever the recorder refuses or abandons a record, the gate tells the person that no pytest loaded the recorder, which is false.

## What the account claimed, and what the code does

- **Claimed** (`phases/phase-2.md` §*Round 2*, the recorder's docstring, rule 3, the changelog fragment): the refusals "close every branch of pytest's naming rule that reaches it". **Found**: the table matches pytest 9.1.1's source for every branch it lists, and each planted case pins its branch (eight mutants, all red, executed). One half of the *outside rootpath and every initial path* row is missing. For a `collect` line the guard catches only a path equal to the rootdir, and a collector parented below the root gives a failed collection the parent directory's path. That is 🔴 2.
- **Claimed** (the comment at `specseal_pytest_record.py:187`): `find_spec` "imports a dotted name's parent packages, which pytest's own collection does next". **Found**: "next" is not what happens. The recorder's `pytest_sessionstart` is registered at `pytest_configure`, after every conftest, so it runs before a conftest's own `pytest_sessionstart`. The import therefore lands earlier than pytest's would. `spec.md` Scope 1 says the recorder "never changes an outcome", and a planted shape flips a pass to a fail (executed). That is 🔴 1.
- **Claimed** (`phases/phase-2.md`): two branches of round 2's paste-ready fix had no observable effect under the guard, so they were removed. These are the split at `[` and `::`, and the plain module's location. **Found**: true at the target. `resolve_collection_argument` refuses `::` parts on a directory or package (`_pytest/main.py:1150`), so only a file argument carries them, and its node id path is empty. The fix for 🔴 1 below brings the split back, because that fix reads an unlocated name differently. NAME NOT IN TREE
- **Claimed** (the ledger fragment's W1 row and its re-stamped anchors): the ledger holds. **Found**: `evidence-check` over the fragment gives 216 ok, 0 drifted, 0 broken (executed).

## The derivation, judged against pytest 9.1.1

Read in the worktree's virtualenv:

- `FSCollector.__init__` at `_pytest/nodes.py:591-598`: `relative_to(rootpath)`, otherwise the initial path that holds the node, otherwise None.
- The initial-path helper at `_pytest/nodes.py:539-549`: `""` for an initial path itself, otherwise the path relative to the nearest initial parent. NAME NOT IN TREE
- `Node.__init__` at `_pytest/nodes.py:195-201`: with no node id, the parent's node id plus `::` and the node's name.
- `BaseReport.fspath` at `_pytest/reports.py:163-165`: the node id up to `::`.
- `search_pypath` at `_pytest/main.py:1040-1073` and `resolve_collection_argument` at `1087-1163`. NAME NOT IN TREE
- `Session.perform_collect` and `Session.collect` at `_pytest/main.py:805-936`, and the args decision at `_pytest/config/__init__.py:1395-1438`. NAME NOT IN TREE

The table's rows agree with that source on these points:

- The lexical comparison.
- The `--pyargs` package location. The recorder's namespace and regular-package branches are `search_pypath`'s branches in the same order.
- `testpaths`. pytest reads them only where the invocation directory is `rootpath`, and with `--pyargs` it passes them on as module names.
- xdist.

The `confcutdir` row says it "touches no node id". That is imprecise, though no file is misnamed: `confcutdir` decides which parent `Dir` nodes `Session.collect` builds above a non-`--pyargs` argument (`main.py:922-928`). Those nodes carry no tests and get node ids that are never a file.

**Each case exercises its branch**, executed with `bin/mutation-check` and one mutant per branch, every one red:

- the namespace branch off;
- the regular-package branch off;
- the lexical comparison made `realpath`, which turns all three symlink cases red;
- the `test`-line guard off, at the recorder and at the gate's `--pyargs` case;
- the `collect`-line guard off;
- the `exists` skip off;
- the located path ignored.

**The missing half** is the row *outside `rootpath` and every initial path*. Its case, `test_a_collector_built_for_a_path_no_argument_holds_writes_no_record`, plants a collector whose parent is the root `Dir`, whose node id is `.`. Its tests are named `.::outside::…` and its failed collections are named `.::outside::…` too. Both reach the rootdir, and the guard catches both. Parented one directory lower, a test line still names a directory, which `isfile` catches, but a failed collection names the directory. The guard checks a `collect` line only against the rootdir itself, so that line is written. This is 🔴 2.

## 🔴 1 — a dotted `--pyargs` name imports the package at `pytest_sessionstart`, and a passing test fails under the gate

`skills/verify/scripts/pytest_record/specseal_pytest_record.py:192` (`Recorder.an_argument_lies_outside_the_rootdir`, called from `pytest_sessionstart` at line 212).

`importlib.util.find_spec("pkg.test_a")` imports `pkg` to read its `__path__`. The recorder asks at `pytest_sessionstart`. pluggy calls the plugin registered last first, so the recorder runs before any conftest's `pytest_sessionstart`. pytest itself imports `pkg` only later, in `perform_collect`. A package that reads, at import, something a `pytest_sessionstart` hook sets is therefore imported before it is set. The suite's outcome now depends on whether the gate measured it. NAME NOT IN TREE

Executed in the clone with a planted shape. `conftest.py` sets an environment variable in `pytest_sessionstart`, `pkg/__init__.py` reads it at import, and `pkg/test_a.py` asserts on it. `pytest --pyargs pkg.test_a` gives exit 0, `1 passed`, without the recorder and exit 1, `1 failed`, with it. The package lies inside the rootdir, so this is an ordinary `--pyargs mypkg.tests` row. The mirror is a false pass: a package whose import-time read masks a failure. I read that from the same mechanism and did not run it.

Why it matters: `spec.md` Scope 1 says the recorder "never prints, never changes an outcome". Under this defect the gate reports a red suite that is green without it, or the reverse, and the base run carries the same flip.

The class (§12) is user code run earlier than pytest runs it, and `find_spec` on a dotted name is its one instance in the recorder. The rest of the module imports nothing of the row's. I tried two fixes in the clone:

- **`@pytest.hookimpl(trylast=True)` on `pytest_sessionstart`.** It closes the planted shape (exit 0, record written). It still leaves an earlier import ahead of a conftest's own `trylast` hook, and ahead of any collection hook wrapper that runs before pytest's lookup.
- **Locating the name without importing (the fenced fix below).** `find_spec` is used for the first part only, which imports nothing, and `PathFinder.find_spec` searches each later part in its parent's search locations. This closes the class. A name that can be found only by running a parent's code (a package path extended at import) is refused instead. That is the strict side, and pytest stops with a usage error on a name it cannot find at all. Results with this fix: the planted shape passes with the record written, the recorder module gives 19 passed, the gate's `pyargs or rootdir or recorder` cases give 6 passed, and `uvx ruff check` and `format --check` pass. The proposed case below fails at `3066abf6` and passes with the fix, both executed.

## 🔴 2 — a failed collection of a collector built below the root is recorded under a directory, and the gate gives a file the branch broke `failing on base too`

`skills/verify/scripts/pytest_record/specseal_pytest_record.py:115-116` (`Recorder.write`, the `collect` clause of the guard round 2 added).

Executed through the gate in the clone, as a case in the gate's module, using its `base_then_feature` and `run_gate`:

- `sub/pytest.ini` makes `sub` the rootdir, and the row is `cd sub && <python> -m pytest … tests`.
- `sub/tests/conftest.py` returns `pytest.Dir.from_parent(parent, path=<repo>/ext)` from `pytest_collect_directory` for `sub/tests/inner`.
- The base cannot collect `ext/test_old.py`. The branch breaks `ext/test_new.py`'s collection.

At `3066abf6` the gate printed:

```
failing test files, compared at the base:
  sub/tests  failing on base too
```

The records held `{"kind": "collect", "nodeid": "tests::ext::test_new.py", "path": "<repo>/sub/tests"}` at HEAD and the same line for `test_old.py` at the base. Two files outside the rootdir got one name, a directory, and the file the branch broke was hidden behind the base's failure. That is the consequence of round 2's 🔴 1, through a branch the fix pass's table did not split.

Why this shape: the node is outside `rootpath` and outside every initial path, so pytest gives it the parent's node id plus `::` and its name (`nodes.py:201`). Its `fspath` is the parent's path. For a test, that path is a directory and `isfile` abandons the record. For a failed collection, the guard compares the path only with the rootdir.

The fix: a `collect` line whose node id carries `::` must name a file, as a test line must. A legitimate failed collection either has no `::` (a module, a `Dir`, a `Package`, named by its own path) or carries it below a module (a class), where the path is the module's file. Executed in the clone with that fix:

- the new gate case passes, and it fails at `3066abf6`;
- the recorder module gives 19 passed;
- the gate's cases under `-k "pyargs or rootdir or recorder or record or base or measured or collect"` give 169 passed;
- `uvx ruff check` and `format --check` pass.

## 🟡 3 — the gate tells a person that no pytest loaded the recorder where one loaded it and refused to write

`skills/verify/scripts/broad_gate.py:2015` (`NO_RECORD_AT_HEAD`), and `:2021` (`NO_RECORD`) for the base.

Every refusal and every abandoned record since round 1 leaves no keyed record, and the gate words that as "no pytest the row ran here loaded the gate's recorder". `EARNS_THE_WORD` follows it and tells the person to add to `PYTHONPATH` and `PYTEST_ADDOPTS` rather than replace them. For a row refused for a rootdir reason, that environment is already right. The person is sent after a problem the row does not have. Rule 3 does say such files "are measured as a runner's that did not load the recorder", but the line the person actually reads at the console states a false cause.

Executed: `test_a_file_pytest_names_outside_its_rootdir_earns_no_word` passes at the target among the 169 and asserts this exact text, for a row whose pytest loads the recorder with the environment intact. The fix only rewords the two strings. Their pins in `tests/test_the_seal_is_taken_once_by_the_sealer.py` follow (§14). Depth 0: both strings date from `d4d1ca3`, and no fix range touched them.

## ⬜ 4 — the record-abandoning guard reaches tests that are not misnamed, silently, and rule 3 does not name them

`skills/verify/scripts/pytest_record/specseal_pytest_record.py:115`.

Executed:

- A conftest that appends an item parented to the session in `pytest_collection_modifyitems` gets node id `::status` and `fspath` `""`. That abandons the whole record, and the ordinary failing `tests/test_a.py` beside it goes unmeasured.
- A test module that removes its own file while it runs does the same.

Neither prints anything, so the person sees 🟡 3's sentence and nothing else. This is the strict side, so no word is wrong, and `pytest-mypy` 1.0.1, the plugin I expected to hit this, parents its status item to a `MypyFile` and is not affected (its source read through `uvx`). It is ⬜ because behaviour and facts stay right. A sentence in rule 3 would make it findable: "and so does a session in which a test has no file of its own (an item a conftest or plugin attaches to the session) or loses its file while it runs". So would a call to `give_up` in place of the silent abandon.

## ⬜ 5 — `spec.md` still describes round 1's refusal only

`seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:161`, and `:120` in §*The class*.

Both still say "a pytest handed a path outside its rootdir writes no line at all (round 1)". Round 2's lexical comparison, its `--pyargs` location and its guard are in `overview.md` and `phases/phase-2.md`, but not in the spec. The overview bullet cites `spec.md` §*The class* and Scope 1 as the places the correction lives. This is a paperwork correction and does not count toward `Needs a fix`.

## Earlier rounds

- Round 2's 🔴 1 is closed for every shape it named: a `--pyargs` package or module outside the rootdir, a namespace package, a rootdir or an argument spelled through a symlink, a symlinked directory under the rootdir, and a collector built at the root. Each was shown by a red mutant, executed. 🔴 2 above is a further branch of the same class, which the table did not split.
- Round 2's ⬜ 2: rule 3 now says the refused files "are measured as a runner's that did not load the recorder", and the `compare_at_base` docstring agrees (read).
- Round 2's ⬜ 3: `failure_lines` gives `BASE_NOT_CHECKED_OUT` where every word is `NOT_CHECKED_OUT`. `compare_at_base` returns that word for all files or for none, so the heading cannot be mixed (read). The new case pins all three headings (read; the orchestrator's 615-case run at the target covers it).
- Round 2's ⬜ 4: the `exists` skip mutant is red now, executed.
- Round 1's 🟡 2 and 🟡 3, ⬜ 4 and ⬜ 5 were carried as round 2 confirmed them, and re-derived:
  - 🟡 2: rule 3 still carries the `-I`/`-E` sentence (read).
  - 🟡 3: `give_up` is unchanged at lines 140-149 (read), and the `-W error` case passes among the 19 (executed).
  - ⬜ 5: superseded by round 2's ⬜ 3 (read).
  - ⬜ 4: phase 4's correction is in `spec.md` (read). ⬜ 5 above is the same kind of omission, one round later.
- Coordinates carried rather than re-established: the gate's helpers, the location of `base_word`, and the case helpers in both test modules were opened at the coordinates round 2 named.

## Regression tests to plant

- `tests/test_the_recorder_writes_what_its_process_ran.py`: `test_a_dotted_pyargs_name_is_located_without_importing_its_package` (🔴 1). It fails at `3066abf6` (1 failed) and passes with the fix (1 passed), both executed. NAME NOT IN TREE
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: `test_a_collector_built_below_the_root_for_files_outside_it_earns_no_word` (🔴 2). It fails at `3066abf6` (1 failed) and passes with the fix (1 passed), both executed. NAME NOT IN TREE
- The `NO_RECORD_AT_HEAD` and `NO_RECORD` pins move with 🟡 3's text.

## Facts for the evidence ledger

- pytest 9.1.1 names a node outside `rootpath` and outside every initial path after its parent (`nodes.py:201`), so a failed collection of such a collector has its parent's path. That is a directory under the rootdir wherever the parent is not the root `Dir`. W1's guard clause should say `collect` lines are held to the same rule as `test` lines once 🔴 2 is fixed.
- `importlib.util.find_spec` on a dotted name imports every parent package. pluggy calls the plugin registered last first, so a plugin registered at `pytest_configure` runs its `pytest_sessionstart` before a conftest's.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The refusal's `find_spec` imports a dotted `--pyargs` name's package at `pytest_sessionstart`, before a conftest's own hook, so the recorder changes an outcome: a passing test fails under the gate (spec Scope 1: it never changes an outcome) | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:192` | open | executed: `--pyargs pkg.test_a` with a conftest setting at sessionstart what the package reads at import, exit 0 without the recorder and exit 1 with it; the locator fix below passes it, 19 recorder and 6 gate cases pass with it; the proposed case red at the target and green with the fix |
| 🔴 2 | A failed collection of a collector a conftest builds below the root for files outside the rootdir is recorded under the parent directory, and the gate gives a file the branch broke `failing on base too` | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:115` | open | executed: the gate printed `sub/tests  failing on base too` for a branch that broke `ext/test_new.py`, the base failing `ext/test_old.py`; with the fix, the case passes, 19 recorder and 169 gate cases pass; the case red at the target |
| 🟡 3 | Where the recorder loaded and refused or abandoned its record, the gate says no pytest loaded the recorder and points at the environment | `skills/verify/scripts/broad_gate.py:2015` | open | executed: `test_a_file_pytest_names_outside_its_rootdir_earns_no_word` passes asserting this text for a row whose pytest loads the recorder; read: `NO_RECORD` at line 2021 says the same of the base |
| ⬜ 4 | The guard abandons a whole record, silently, for a test with no file of its own or one whose module removes itself, and rule 3 names neither | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:115` | open | executed: a session-parented item and a self-removing module each left no record and no warning; read: pytest-mypy 1.0.1 parents its status item to a file and is not affected; strict side, no wrong word |
| ⬜ 5 | `spec.md` Scope 1 and §The class still describe round 1's refusal only | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:161` | open | read; paperwork correction, not counted in Needs a fix |
| 🟢 | round 2's blocking finding is closed — a `--pyargs` package outside, a namespace package, a rootdir or argument through a symlink and a collector built at the root no longer record under another file's name, and a symlinked directory under the rootdir is recorded | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:157` | confirmed | executed: eight mutants of the refusal and the guard, each red against its case; 19 recorder cases pass at the target; finding 2 above is a further branch of the same class |
| 🟢 | round 2's ⬜ 2 is closed — rule 3 says the refused files are measured as a runner's that did not load the recorder | `templates/config.md:334` | confirmed | read: rule 3 and the `compare_at_base` docstring |
| 🟢 | round 2's ⬜ 3 is closed — a base that could not be checked out gets its own heading | `skills/verify/scripts/broad_gate.py:2951` | confirmed | read: `failure_lines` and `compare_at_base`, which gives the word to every file or none; the new case pins the three headings |
| 🟢 | round 2's ⬜ 4 is closed — the `--pyargs` case pins the `exists` skip | `tests/test_the_recorder_writes_what_its_process_ran.py:319` | confirmed | executed: the skip deleted, the case red |
| 🟢 | round 1's 🟡 3 is closed — the recorder's warning is never raised under warnings as errors | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:140` | confirmed | read: `give_up` unchanged; executed: the `-W error` case passes among the 19 |
| 🟢 | round 1's 🟡 2 is closed — rule 3 names Q2's whole class | `templates/config.md:334` | confirmed | read: the `-I`, `-E` and wrapper sentence still stands |

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

## Paste-ready fixes

### 🔴 1 — locate a `--pyargs` name without importing its package

In `skills/verify/scripts/pytest_record/specseal_pytest_record.py`, above `class Recorder`:

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

and in `an_argument_lies_outside_the_rootdir`, the `--pyargs` branch of the loop:

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

The docstring's sentence on an argument "that is no path and no module pytest can find" then reads: under `--pyargs`, a name found only by importing a parent is refused. The case, for `tests/test_the_recorder_writes_what_its_process_ran.py`:

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

### 🔴 2 — a `collect` line named after its parent abandons the record, as a `test` line does

In `Recorder.write`:

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

The case, for `tests/test_the_seal_is_taken_once_by_the_sealer.py` beside `test_pyargs_modules_outside_the_rootdir_earn_no_word`:

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

The guard's comment and the docstring's paragraph on the collector "a conftest or a plugin builds" gain the `collect` half: a failed collection named after a parent below the root names a directory, and abandons the record.

### 🟡 3 — name both causes of a missing record

In `skills/verify/scripts/broad_gate.py`, the two strings. Their pins in `tests/test_the_seal_is_taken_once_by_the_sealer.py` follow:

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

Needs a fix: yes — 🔴 1 (a dotted `--pyargs` name is imported at `pytest_sessionstart` and the recorder changes an outcome), 🔴 2 (a failed collection named after a parent below the root records two files under one directory and the gate gives a file the branch broke `failing on base too`), 🟡 3 (the gate says no pytest loaded the recorder where one loaded it and refused)
Loses a record or crashes: no

## Proof block

Opened in this round:

- `skills/verify/scripts/pytest_record/specseal_pytest_record.py` (whole, at `3066abf6`)
- `skills/verify/scripts/broad_gate.py` (the fix diff; lines 2004-2036; `failure_lines` and the headings around 2945-2980)
- `templates/config.md` (the fix diff of rule 3)
- `tests/test_the_recorder_writes_what_its_process_ran.py` (the fix diff; helpers at 58-113)
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the fix diff; helpers at 764-786, 881-903, 3904-3980, 4502-4530)
- `skills/verify/scripts/mutation_check.py` (arguments), `bin/test`, `bin/mutation-check`, `.github/scripts/run_tests.py` (venv lines)
- `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/`: `rounds/round-1.md`, `rounds/round-2.md`, `rounds/round-2-report.md` (opening), `phases/phase-2.md` §*Round 2*, `spec.md` (140-175 and its rootdir lines), `changelog.md`, the `overview.md` and ledger-fragment diffs
- pytest 9.1.1 in the worktree's virtualenv: `_pytest/nodes.py` (195-201, 539-610), `_pytest/main.py` (805-1000, 1040-1215), `_pytest/reports.py` (160-171), `_pytest/config/findpaths.py` (`determine_setup`'s rootdir lines), `_pytest/config/__init__.py` (1395-1438) NAME NOT IN TREE
- `pytest-mypy` 1.0.1's module source, lines 195-240, through `uvx`

Suite state: unverified. The full suite, lint and typecheck were not run by this round; the sealer answers it once the rounds settle.
