# 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote — review round 2

| Field | Value |
|---|---|
| Target SHA | 2a6762a1eae68c5ae87bb50bc34cc69da23d1bc5 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | #846 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `daecd5059dadac536ea4bf93500c37c7eaaa99d8..e8d4b77c7c41ec49f1da63223e17d042e30ad8f4`, 5 commits |
| Contract changes | none |
| New units | NOT_CHECKED_OUT (depth 1); BASE_NOT_CHECKED_OUT (depth 1); pytest_in (depth 1); records_written (depth 1); test_a_pyargs_module_outside_the_rootdir_writes_no_record (depth 1); test_a_namespace_package_outside_the_rootdir_writes_no_record (depth 1); test_a_pyargs_module_outside_that_cannot_be_collected_writes_no_record (depth 1); test_a_rootdir_named_through_a_symlink_writes_no_record (depth 1); test_an_argument_named_through_a_symlink_writes_no_record (depth 1); test_a_symlinked_directory_under_the_rootdir_is_recorded_by_its_own_name (depth 1); BUILDS_A_COLLECTOR_ELSEWHERE (depth 1); test_a_collector_built_for_a_path_no_argument_holds_writes_no_record (depth 1); test_each_failing_files_heading_says_what_was_compared (depth 1); test_pyargs_modules_outside_the_rootdir_earn_no_word (depth 1) |
| Fix of a fix | first — 🔴 1 at skills/verify/scripts/pytest_record/specseal_pytest_record.py#Recorder, a unit round-1's fixes changed |
| Needs a fix | yes — 🔴 1 (a `--pyargs` module outside the rootdir, or a rootdir named through a symlink, still records a file under another file's name, and the gate gives a file the branch broke `failing on base too`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round for round 1's fixes at `80e74544..fa1c6044`. The reviewer was asked to open each fix, inheriting round 1's verdicts, and in particular to judge whether the rootdir refusal refuses every shape that would misname a file and no shape that would not, then the rest of `origin/release/v0.20.0..2a6762a1`, without running the full suite. Before the round the orchestrator ran `uvx ruff check` and `ruff format --check` on the four changed Python files and three touched modules (449 passed); the fix pass had run its modules with the 18 neighbouring hygiene modules (2111 passed, 8 skipped).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The rootdir refusal reads arguments with `realpath` and as path strings, where pytest resolves `--pyargs` modules and compares lexically: a `--pyargs` module outside the rootdir, or a rootdir named through a symlink, still records a file under another file's name, and the gate gives a file the branch broke `failing on base too`; a symlinked directory under the rootdir that pytest names correctly is refused | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:135` | **fixed** `2648f56b` | fixed at 2648f56b — 6c14f4c0; executed: five shapes with the recorder at 2a6762a1 on pytest 9.1.1, and a gate run over `--pyargs extpkg.test_a extpkg.test_b` printing `sub  failing on base too`; the fix below makes all four planted cases go from red to green, and 175 recorder and gate cases pass with it; read: pytest 9.1.1 `nodes.py:593` and `main.py:1134` |
| ⬜ 2 | Rule 3 says a session refused for a path outside its rootdir has its files read `new?`, but beside a second runner that did record, those files are in no list | `templates/config.md:334` | **fixed** `2648f56b` | fixed at 2648f56b; read: `gate` takes the failing files from the head record wherever any session carries the key; strict side, no wrong word; also `skills/verify/scripts/broad_gate.py:2079` and the changelog fragment |
| ⬜ 3 | The failure form still heads rows "compared at the base" where every row reads that the base could not be checked out | `skills/verify/scripts/broad_gate.py:2947` | **fixed** `4184e2f0` | fixed at 4184e2f0; read: `compare_at_base` returns that word for every file at line 2097, and the heading checks only for `NO_RECORD_AT_HEAD`; each row says it, so behaviour and fact stay right |
| ⬜ 4 | The planted `--pyargs` case stays green with the `exists` skip deleted, so it does not pin what its docstring says | `tests/test_the_recorder_writes_what_its_process_ran.py:319` | **fixed** `dcd42e77` | fixed at dcd42e77; executed: the skip deleted in the clone, the case passed |
| 🟢 | round 1's 🟡 2 is closed — rule 3 names Q2's whole class | `templates/config.md:334` | confirmed | read: the sentence and its pins in the rule-3 case, the retired sentence asserted gone |
| 🟢 | round 1's 🟡 3 is closed — the recorder's warning is never raised under warnings as errors | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:117` | confirmed | executed: `give_up` reverted to a bare `warnings.warn` turns the planted `-W error` case red, and it is green at the target |
| 🟢 | round 1's ⬜ 4 is closed — phase 4's correction is fed back into the spec, plan and overview | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/spec.md:79` | confirmed | read: R4, §*The class*, Scope 1, `plan.md`'s scenario and Alternative M, `overview.md` |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:144` | round 1's 🔴 1 — fixed |
| round-1 | `templates/config.md:334` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:103` | round 1's 🟡 3 — fixed |
| round-1 | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:48` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2940` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2038`, `templates/config.md:334` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
