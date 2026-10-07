# 1791270161 — review round 2 report (the verifying round)

Target `2a6762a1`, fix range `80e74544..fa1c6044` plus the round-1 record commit. Reviewed in a `git clone --no-local` at the target in this round's scratch directory; nothing was written in the worktree except this file.

## What the account claimed, and what the code does

- **Claimed** (commit `17badc11`, rule 3, the recorder's docstring, the changelog fragment, `spec.md` §*The class*): a pytest naming files outside its rootdir is refused, "the refusal above closes it; no third is known". **Found**: the refusal decides from the argument strings with `os.path.realpath`, while pytest decides from what it resolves, lexically. Three shapes still record a file under a name that is not its own, and one shape that names files correctly is refused. Finding 🔴 1.
- **Claimed** (the docstring of the planted `--pyargs` case): it holds that a `--pyargs` module name is passed over rather than read as a path. **Found**: deleting the `os.path.exists` skip leaves the case green, executed. Finding ⬜ 4.
- 🟡 2 and 🟡 3 of round 1 hold as claimed; ⬜ 4 of round 1 holds; ⬜ 5 of round 1 holds for the one word it names and misses its sibling (⬜ 3 below).

## 🔴 1 — the rootdir refusal misses `--pyargs` modules and a rootdir named through a symlink, and the gate still gives a file the branch broke `failing on base too`

`skills/verify/scripts/pytest_record/specseal_pytest_record.py:135-139` (`Recorder.an_argument_lies_outside_the_rootdir`).

pytest names a module against the rootdir with `path.relative_to(config.rootpath)`, which is lexical, and falls back to naming it against an initial path when that fails (`_pytest/nodes.py:593-595` in pytest 9.1.1, NAME NOT IN TREE). The initial path is what `resolve_collection_argument` makes of the argument: under `--pyargs` the module's location through `search_pypath`, otherwise `absolutepath(invocation_dir / arg)`, never resolved through a symlink (`_pytest/main.py:1134-1142`). The refusal instead joins the raw argument string to the invocation directory and calls `realpath` on both sides. So it differs from pytest in three ways, and each was measured with the recorder at `2a6762a1` on pytest 9.1.1:

| Shape | What pytest names | What the recorder does at `2a6762a1` |
|---|---|---|
| `--pyargs extpkg`, the package outside the rootdir | `extpkg/test_a.py` as `test_a.py` | records it as the rootdir's own `test_a.py`, a file that exists and passes |
| `--pyargs extpkg.test_a other.test_b`, both outside | each module's node id is empty | records both as the rootdir itself, one name for two files |
| `--pyargs tests`, where `./tests` exists but `tests` imports from elsewhere first | the external `tests/test_q.py` as `test_q.py` | records it; the argument exists inside, so nothing is refused |
| `--rootdir=<a symlink to the repository>` or `-c <symlink>/pytest.ini`, then `tests` | `tests/test_x.py` as `test_x.py`, lexically outside the symlinked rootdir | records `link/test_x.py`, which the gate's `record_path` resolves to the repository's own root-level `test_x.py` |
| `shared_tests`, a symlink under the rootdir pointing outside it | `shared_tests/test_y.py`, correct | **refuses**, while the same layout run with no argument records it under that name |

The first four are the class round 1's 🔴 1 named: a file outside the rootdir recorded under a name that is not its own. The fix closed only the instance where the argument is a path string that resolves outside. §12 asks for every instance the same cause produces, and the cause is that the refusal reads the arguments differently from pytest.

**End to end through the gate**, executed in the clone: a row `cd sub && PYTHONPATH=..:$PYTHONPATH <python> -m pytest -q -p no:cacheprovider --pyargs extpkg.test_a extpkg.test_b`, with `sub/pytest.ini` making `sub` the rootdir. `extpkg/test_b.py` fails on the base. The feature breaks `extpkg/test_a.py`. At `2a6762a1` the gate prints:

```
failing test files, compared at the base:
  sub  failing on base too
```

The branch's regression reads as a failure the base already had. That is the consequence round 1 rated 🔴, through a shape the refusal passes over. With the fix below, no record is written, the base is not run, and no `failing on base too` is printed.

How likely is the shape? `--pyargs` over an installed package is the documented way to test an installed build, and a row that installs before testing (`pip install . && pytest --pyargs pkg`) is the pattern where the branch's code and the base's code both reach the comparison. The symlink shapes are rarer; they are in the fix because the same two lines close them.

**Why the fix sits here.** Matching pytest's own rule is one change to one unit: compare lexically with `os.path.abspath` on both sides, as pytest's `absolutepath` and `relative_to` do, and under `--pyargs` resolve each argument the way pytest's `search_pypath` does before comparing (NAME NOT IN TREE). The cost is named: under `--pyargs`, `importlib.util.find_spec` imports a dotted name's parent packages at `pytest_sessionstart`, which pytest's own collection does moments later in the same process; on an xdist controller, which collects nothing, it is an import that did not happen before. A name it cannot resolve falls through to the path rule, as pytest's does, and an unresolvable non-path is skipped by the existing `exists` check, after which pytest itself stops with a usage error.

The paste-ready fix is in the fences below: the recorder change, three recorder cases and one gate case (each seen red at `2a6762a1` and green with the fix, executed), and the sentences of rule 3, the recorder docstring and the changelog fragment that name the class. The pinned sentence in `test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written` has to move with rule 3.

With the fix applied in the clone, the recorder module and the gate module filtered to the record, rootdir, `--pyargs`, symlink, layout and base cases passed, 175 of 175. That includes round 1's planted `-c` and `pytest tests sub` cases and the Q3b corpus row (executed).

## ⬜ 2 — rule 3 says a refused session's files read `new?`, and beside a second runner they are listed nowhere

`templates/config.md:334`, and the same sentence in `compare_at_base`'s docstring (`skills/verify/scripts/broad_gate.py:2079-2081`) and the changelog fragment.

Where a row runs two pytests and only the one outside its rootdir is refused, the other's session carries the head key. The failing files then come from that record alone. The refused session's failures stay in `suite.txt` and out of the list, which rule 3 already says for "one runner loaded it and another did not". The new sentence "so it writes no record and its files read `new?`" is true only for a row whose every pytest was refused. The behaviour is the strict side: no word is given, and none is wrong. The fix is wording: "…so it writes no record, and its files are measured as a runner that did not load the recorder is."

## ⬜ 3 — the heading still says "compared at the base" over files whose base could not be checked out

`skills/verify/scripts/broad_gate.py:2947`.

Round 1's ⬜ 5 was the heading over rows where the base was not run. The fix tests for `NO_RECORD_AT_HEAD` alone. `compare_at_base` also returns "new? the base could not be checked out for comparison" for every file (`broad_gate.py:2097`), and the base was not compared there either, yet the heading reads `COMPARED_AT_BASE`. Each row says so itself, so behaviour and fact stay right. A heading test that reads the rows rather than one word closes both: `compared = any(word not in NOT_COMPARED for word in verdicts.values())`, with that set holding both words (NAME NOT IN TREE).

## ⬜ 4 — the planted `--pyargs` case does not pin the line its docstring describes

`tests/test_the_recorder_writes_what_its_process_ran.py:319`.

Its docstring says a `--pyargs` module name "is passed over rather than read as" a path. The name `test_mixed` joined to the invocation directory, which is the rootdir, lies inside the rootdir whether or not it exists. Deleting the `if not os.path.exists(path): continue` lines leaves the case green (executed: 1 passed). What it does pin is that a refusal never treats a missing argument as outside. Under 🔴 1's fix the case stays valid as the inside half of the `--pyargs` pair, and the outside half is planted beside it. §15 is the rule this misses.

## Round 1's findings, answered

- 🔴 1 of round 1: closed for an argument that is a path resolving outside the rootdir (round 1's two layouts, executed green in the clone). It is open for the rest of its class, which is 🔴 1 here.
- 🟡 2: the rule-3 sentence names a replaced `PYTHONPATH`, `-I`, `-E` and a wrapper passing `PYTEST_*` alone (read). The pinned sentences and the retired one are in the rule-3 case (read). Closed.
- 🟡 3: `give_up` warns under its own `catch_warnings` with `simplefilter("always")`. Reverting it to a bare `warnings.warn` turns the planted `-W error` case red (executed: 1 failed), and it passes at the target. Inside pytest's own recording context the inner filter only overrides the action, and the warning still reaches pytest's summary (read). Closed.
- ⬜ 4 of round 1: `spec.md` R4, §*The class*, Scope 1, `plan.md` and `overview.md` now carry the corrections (read). Closed, and paperwork. 🔴 1's fix moves the same sentences again.
- ⬜ 5 of round 1: closed for `NO_RECORD_AT_HEAD`; its sibling is ⬜ 3.

## Regression tests to plant

- `tests/test_the_recorder_writes_what_its_process_ran.py`: the three recorder cases in the fence for 🔴 1 (a `--pyargs` package outside the rootdir writes no record; a rootdir named through a symlink writes no record; a symlinked directory under the rootdir is recorded under its own name). Each was red at `2a6762a1` and green with the fix (executed).
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the gate case for `--pyargs` modules outside the rootdir. At `2a6762a1` it printed `sub  failing on base too`; with the fix, no such word appears (executed).

## Facts for the evidence ledger

- W1's clause "a session handed a path outside its rootdir writes no record" should become: a session in which pytest names any initial path outside its rootdir by pytest's own lexical rule, a `--pyargs` module resolved as pytest resolves it included, writes no record. The anchor list gains the three new recorder cases and the gate case.
- W8's and Corrected R4's "a pytest handed a path outside its rootdir writing no record" follow rule 3's new sentence.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The rootdir refusal reads arguments with `realpath` and as path strings, where pytest resolves `--pyargs` modules and compares lexically: a `--pyargs` module outside the rootdir, or a rootdir named through a symlink, still records a file under another file's name, and the gate gives a file the branch broke `failing on base too`; a symlinked directory under the rootdir that pytest names correctly is refused | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:135` | open | executed: five shapes with the recorder at 2a6762a1 on pytest 9.1.1, and a gate run over `--pyargs extpkg.test_a extpkg.test_b` printing `sub  failing on base too`; the fix below makes all four planted cases go from red to green, and 175 recorder and gate cases pass with it; read: pytest 9.1.1 `nodes.py:593` and `main.py:1134` |
| ⬜ 2 | Rule 3 says a session refused for a path outside its rootdir has its files read `new?`, but beside a second runner that did record, those files are in no list | `templates/config.md:334` | open | read: `gate` takes the failing files from the head record wherever any session carries the key; strict side, no wrong word; also `skills/verify/scripts/broad_gate.py:2079` and the changelog fragment |
| ⬜ 3 | The failure form still heads rows "compared at the base" where every row reads that the base could not be checked out | `skills/verify/scripts/broad_gate.py:2947` | open | read: `compare_at_base` returns that word for every file at line 2097, and the heading checks only for `NO_RECORD_AT_HEAD`; each row says it, so behaviour and fact stay right |
| ⬜ 4 | The planted `--pyargs` case stays green with the `exists` skip deleted, so it does not pin what its docstring says | `tests/test_the_recorder_writes_what_its_process_ran.py:319` | open | executed: the skip deleted in the clone, the case passed |
| 🟢 | round 1's 🟡 2 is closed — rule 3 names Q2's whole class | `templates/config.md:334` | confirmed | read: the sentence and its pins in the rule-3 case, the retired sentence asserted gone |
| 🟢 | round 1's 🟡 3 is closed — the recorder's warning is never raised under warnings as errors | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:117` | confirmed | executed: `give_up` reverted to a bare `warnings.warn` turns the planted `-W error` case red, and it is green at the target |
| 🟢 | round 1's ⬜ 4 is closed — phase 4's correction is fed back into the spec, plan and overview | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:79` | confirmed | read: R4, §*The class*, Scope 1, `plan.md`'s scenario and Alternative M, `overview.md` |

## Paste-ready fixes

### 🔴 1 — the recorder

```python
def _module_location(name):
    """Where pytest's `--pyargs` finds `name`, the way its `search_pypath`
    does: a module's file, a package's directory, or None where it finds
    none and reads the argument as a path. `find_spec` imports a dotted
    name's parent packages, which pytest's own collection does next."""
    import importlib.util

    try:
        spec = importlib.util.find_spec(name)
    except Exception:
        return None
    if spec is None:
        return None
    locations = list(spec.submodule_search_locations or ())
    if not locations:
        return spec.origin
    if spec.origin is None or spec.origin == "namespace":
        return locations[0]
    return os.path.dirname(spec.origin)
```

```python
    def an_argument_lies_outside_the_rootdir(self):
        """Whether pytest was handed a path outside its rootdir, by pytest's
        own rule: lexical, as its `absolutepath` and `relative_to` are, never
        through a symlink, and with a `--pyargs` module where pytest finds
        it. pytest names a file there against the argument that reached it,
        not against the rootdir, so its node id's path joined to the rootdir
        names no file of its own (#825 rounds 1 and 2). An argument that is
        no path and no module pytest can find is passed over: pytest stops
        on it with a usage error."""
        root = os.path.abspath(self.rootdir)
        here = _invocation_dir(self.config)
        option = getattr(self.config, "option", None)
        pyargs = bool(getattr(option, "pyargs", False))
        for argument in getattr(self.config, "args", None) or ():
            name = str(argument).split("::")[0]
            located = _module_location(name) if pyargs else None
            path = os.path.abspath(os.path.join(here, located or name))
            if not os.path.exists(path):
                continue
            try:
                inside = os.path.commonpath([root, path]) == root
            except ValueError:
                inside = False
            if not inside:
                return True
        return False
```

### 🔴 1 — the recorder's cases, in `tests/test_the_recorder_writes_what_its_process_ran.py`

```python
def pytest_in(root, env, *args):
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", *args],
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=240,
    )


def records_written(records):
    return [f for f in os.listdir(str(records)) if f.endswith(".jsonl")]


def test_a_pyargs_module_outside_the_rootdir_writes_no_record(tmp_path):
    """#825 round 2. pytest finds a `--pyargs` package where Python imports
    it from, outside the rootdir here, and names its `test_mixed.py` against
    the package: `test_mixed.py`, the name a file at the rootdir has. The
    argument is no path, so the refusal used to pass it over and the record
    named another file."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    package = tmp_path / "site" / "extpkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    env = recording_env(records)
    env["PYTHONPATH"] = os.pathsep.join([env["PYTHONPATH"], str(tmp_path / "site")])
    result = pytest_in(root, env, "--pyargs", "extpkg")
    assert result.returncode == 1, result.stdout + result.stderr
    assert records_written(records) == [], records_of(records)


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_a_rootdir_named_through_a_symlink_writes_no_record(tmp_path):
    """#825 round 2. pytest compares a path with its rootdir lexically, so a
    `--rootdir` spelled through a symlink puts `tests/` outside it, and
    `tests/test_mixed.py` is named `test_mixed.py`. A `realpath` comparison
    called it inside."""
    root, records = project(tmp_path, {"test_mixed.py": PASSING_AND_FAILING})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    link = tmp_path / "link"
    link.symlink_to(root, target_is_directory=True)
    result = pytest_in(root, recording_env(records), "--rootdir", str(link), "tests")
    assert result.returncode == 1, result.stdout + result.stderr
    assert records_written(records) == [], records_of(records)


@pytest.mark.skipif(os.name == "nt", reason="a symlink needs privileges on Windows")
def test_a_symlinked_directory_under_the_rootdir_is_recorded_by_its_own_name(
    tmp_path,
):
    """#825 round 2. A directory under the rootdir that is a symlink to a
    place outside it is named by pytest under the rootdir, and it was
    refused only when it was spelled as an argument."""
    root, records = project(tmp_path, {})
    (root / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    shared = tmp_path / "shared"
    shared.mkdir()
    (shared / "test_mixed.py").write_text(PASSING_AND_FAILING, encoding="utf-8")
    (root / "shared_tests").symlink_to(shared, target_is_directory=True)
    result = pytest_in(root, recording_env(records), "shared_tests")
    assert result.returncode == 1, result.stdout + result.stderr
    _, lines = the_one_record(records)
    failed = {
        os.path.relpath(line["path"], str(root))
        for line in lines
        if line["kind"] == "test" and line["outcome"] == "failed"
    }
    assert failed == {os.path.join("shared_tests", "test_mixed.py")}, lines
```

### 🔴 1 — the gate's case, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`

```python
def test_pyargs_modules_outside_the_rootdir_earn_no_word(tmp_path):
    """#825 round 2. `sub/pytest.ini` makes `sub` the rootdir, and the row's
    `--pyargs` modules live in `extpkg/`, outside it, so pytest gives each an
    empty node id and both were recorded as `sub`. The base fails
    `test_b`, the feature breaks `test_a`, and `sub` read `failing on base
    too`. A session whose `--pyargs` module lies outside its rootdir writes
    no record, so the base is not run."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"cd sub && PYTHONPATH=..:$PYTHONPATH {FILES_ROW} "
        "--pyargs extpkg.test_a extpkg.test_b",
        {
            "sub/pytest.ini": "[pytest]\n",
            "extpkg/__init__.py": "",
            "extpkg/test_a.py": "def test_a():\n    assert True\n",
            "extpkg/test_b.py": "def test_b():\n    assert False, 'on the base'\n",
        },
        {"extpkg/test_a.py": "def test_a():\n    assert False, 'the branch'\n"},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    assert gate.ON_BASE not in out.stdout, out.stdout
```

### 🔴 1 — rule 3's sentence in `templates/config.md`, and its pin in the rule-3 case

```
A pytest that names a file outside its rootdir — one handed a path outside it, `-c` or `--rootdir` elsewhere or spelled through a symlink, a config file in one of its arguments' directories, or a `--pyargs` module Python imports from outside it — names those files against the argument rather than the rootdir, so it writes no record, and its files are measured as a runner's that did not load the recorder.
```

```python
        # #825 rounds 1 and 2.
        "A pytest that names a file outside its rootdir — one handed a path "
        "outside it, `-c` or `--rootdir` elsewhere or spelled through a "
        "symlink, a config file in one of its arguments' directories, or a "
        "`--pyargs` module Python imports from outside it — names those files "
        "against the argument rather than the rootdir, so it writes no record, "
        "and its files are measured as a runner's that did not load the "
        "recorder.",
```

```python
        # #825 round 2: the refusal named by its path arguments alone.
        "A pytest handed a path outside its rootdir — `-c` or `--rootdir` "
        "elsewhere, or a config file in one of its arguments' directories — "
        "names those files",
```

### 🔴 1 — the recorder's docstring paragraph

```
That holds only where pytest names a file against the rootdir, which it does
for every file under it by its own lexical rule. A file outside the rootdir
is named against the argument that reached it, so the node id's path joined
to the rootdir names a file that is not the test's, and two files under two
arguments can share one name. A session in which pytest would name any
argument outside its rootdir -- a path outside it, `-c` or `--rootdir`
elsewhere or spelled through a symlink, a config file in one argument's
directory, a `--pyargs` module Python imports from outside it -- therefore
writes no record at all: the strict side (#825 rounds 1 and 2).
```

### 🔴 1 — the changelog fragment's bullet

```
- **A pytest that names a file outside its rootdir writes no record.** A
  path outside the rootdir, `-c` or `--rootdir` elsewhere or spelled through
  a symlink, a config file in one argument's directory, or a `--pyargs`
  module installed outside the repository makes pytest name those files
  against the argument rather than the rootdir, and two of them can share
  one name. Such a row's files are not measured.
```

## Executed probes

| What was run | Result |
|---|---|
| The recorder at 2a6762a1 on pytest 9.1.1 (the worktree's virtualenv, run read-only) over nine layouts: `--pyargs` package outside; two `--pyargs` modules outside; `--pyargs tests` resolving elsewhere; `--rootdir` and `-c` through a symlink; a symlinked directory under the rootdir, as an argument and not; `testpaths` outside; a control | recorded under another file's name in the first four shapes (`test_a.py`; `.` for both modules; `test_q.py`; `link/test_x.py`); refused the symlinked directory spelled as an argument and recorded it unspelled; refused `testpaths` outside; recorded the control correctly |
| The same nine layouts with 🔴 1's fix in the clone | no record for every shape pytest names outside its rootdir; the symlinked directory recorded under its own name either way; the control unchanged |
| A gate run in the clone over `cd sub && … --pyargs extpkg.test_a extpkg.test_b`, base failing `test_b`, feature breaking `test_a` | at 2a6762a1: `sub  failing on base too`; with the fix: no record at HEAD, no base run, no `failing on base too` |
| The three proposed recorder cases at 2a6762a1, then with the fix | 3 failed, then 3 passed |
| The recorder module, and the gate module with `-k "recorder or record or rootdir or pyargs or symlink or cd_row or every_layout or twice or two_runners or base or measured"`, `-n auto`, with the fix in the clone | 175 passed |
| `uvx ruff check` and `uvx ruff format --check` on the fixed recorder | pass |
| The `exists` skip deleted from the refusal, the planted `--pyargs` case | 1 passed, so the case does not pin that line |
| `give_up` reverted to a bare `warnings.warn`, the planted `-W error` case | 1 failed, so the case pins round 1's 🟡 3 fix |
| The full suite, lint and typecheck over the branch (the broad gate) | not yet: not run by this round. It is the sealer's, once, after the rounds settle. With 🔴 1 open, it has not come due |

Needs a fix: yes — 🔴 1 (a `--pyargs` module outside the rootdir, or a rootdir named through a symlink, still records a file under another file's name, and the gate gives a file the branch broke `failing on base too`)
Loses a record or crashes: no

## Proof block

Files opened in the clone at `2a6762a1`: `skills/verify/scripts/pytest_record/specseal_pytest_record.py` (whole), `skills/verify/scripts/broad_gate.py` (1844-2120, 2924-2970, 3205-3280), `templates/config.md:334`, `tests/test_the_recorder_writes_what_its_process_ran.py` (helpers, 280-352), `tests/test_the_seal_is_taken_once_by_the_sealer.py` (759-802, 3879-3960, the fix-range hunks), `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/rounds/round-1.md`, the fix range's diff of `spec.md`, `plan.md`, `overview.md`, `changelog.md` and the ledger fragment, `skills/code-review/orchestration.md` §*A fix of a fix twice sends the work item back to its framer*. pytest 9.1.1's `_pytest/nodes.py` (536-607), `_pytest/main.py` (1040-1165), `_pytest/config/findpaths.py` (rootdir lines) and `_pytest/reports.py` (163-166), in the worktree's virtualenv. The clone, its probe files and the scratch layouts are removed after this report.
