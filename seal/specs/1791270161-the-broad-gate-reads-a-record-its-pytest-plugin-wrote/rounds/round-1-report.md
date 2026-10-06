# Round 1 report — 1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 1bbbdca9 |
| Base | origin/release/v0.20.0 |
| Reviewed by | warden on Opus 5.5 |

## Summary

One blocking finding, two to fix or justify, and two paperwork corrections.

1. 🔴 1. Phase 4 made the recorder write a test's path as the rootdir
   joined to `report.fspath`. That holds only where pytest names a file
   against its rootdir. A file outside the rootdir is named against the
   argument that reached it, so the joined path names no real file, and two
   files under two arguments get one name. Executed: the branch breaks
   `sub/test_x.py`, the base fails a different file, `tests/test_x.py`, and
   the gate says `failing on base too` for `sub/test_x.py`. No `-c` is
   needed: `pytest tests sub` with a `pytest.ini` in `sub/` does it. The
   regression corpus already holds this shape (Q3b, "own" row). There it
   names the root's files under `a/` today, and only luck of naming keeps the
   word right. This is the permissive word, and rule 3 says only a forged
   record can produce it.
2. 🟡 2. Q2's class is wider than the one row rule 3 names. Under
   `python -I`, under `python -E`, or under a wrapper that passes
   `PYTEST_ADDOPTS` but not `PYTHONPATH` (tox with `PYTEST_*` passed through),
   a green suite fails at the gate with exit 1. Rule 3 tells the reader such
   wrappers "write no record; its files read `new?`".
3. 🟡 3. The recorder's one warning becomes an exception out of a hook when
   the row runs with warnings as errors. Executed: `python -W error` with an
   unwritable records directory ends in INTERNALERROR, exit 3. The recorder
   promises that it "never raises out of a hook".
4. ⬜ 4 and ⬜ 5 are paperwork. The spec was not fed back after phase 4's
   divergence. The failure form's heading says "compared at the base" over
   rows where the base was not run.

## What this round was asked

Round 1 of the branch at 1bbbdca9 against `origin/release/v0.20.0`, spec
compliance first and quality second. The caller asked me to judge phase 4's
divergence from `spec.md` R4 (the recorder writes `report.fspath`, not
`report.location[0]`) and to say whether the spec was fed back. Q1 and Q2
belong to the owner and are built as (a). They are not reopened here.

## Spec compliance

Read against `spec.md` Scopes 1 to 11 and S1 to S22, `plan.md`,
`questions.md`, `overview.md` and the four phase records.

- **Q1 built as (a): matches.** `base_word` (`skills/verify/scripts/broad_gate.py:2038`)
  returns `NOT_REACHED` with the exit for a file in no base session on a
  non-zero exit. It returns `new` only on exit 0. Rule 3 and the **New?**
  bullet both say a file the branch added reads `new?` on a red base.
- **Q2 built as (a): matches for the row Q2 names.** A row that replaces
  `PYTHONPATH` fails at the gate. Rule 3 tells the author to put the row's
  directory in front. The case named in Q2,
  `test_a_row_that_replaces_pythonpath_cannot_load_the_recorder`, holds it.
  What (a) does not cover is the rest of its class, which is 🟡 2. That is
  not a reopening of the trade.
- **Scope 2 to 5 (environment, reader, HEAD list, one base run): built as
  specified.** I read `recording_env`, `read_record`, `record_path`,
  `base_word`, `compare_at_base` and the failure loop in `gate`. There is
  one `run(...)` at the base and one at HEAD. The base is not run where HEAD
  left no record. `failing_files` is read only in that fallback, with
  `FAILED_RE` widened (#813).
- **The recorded divergences are grounded.** They are `RunRecord`, the
  first-line key, `NO_RECORD_AT_HEAD` for an `env -i` row alone, a row that
  sets `PYTHONPATH`, and the kept shell-selection case. Each overview row
  quotes both sides and gives grounds I could check against the code.
- **Phase 4's divergence (R4) is right about inheritance and incomplete.**
  The measurement in `phases/phase-4.md` is sound. `report.location[0]`
  names the module that defines a test function, and nine corpus cases were
  red with it. But `report.location[0]` is pytest's best relative path from
  the rootdir, so it is correct for a file outside the rootdir.
  `report.fspath` is the node id's path, and pytest makes that relative to
  the rootdir only for files under it. The switch closed the inheritance
  case and opened the outside-rootdir case (🔴 1). Neither field alone is
  the collecting module's absolute path in every layout.
- **Fed back: no.** `spec.md` still says `report.location[0]` (Scope 1,
  line 154) and still carries R4 (line 79). §*The class* still says "Two
  files at one relative path ... coincide only for one file" (line 117),
  which 🔴 1 shows false. `overview.md` §*What was fed back into the spec*
  reads "none — phase 2 added no clause". It was written at phase 2 and not
  revisited at phase 4. The divergence is recorded in `overview.md`'s
  divergence table and in ledger row W1, so nothing is lost. But the
  section that says what was fed back now says something false (⬜ 4).

## Findings — from execution

### 🔴 1 — a file pytest names outside its rootdir is recorded under the wrong path, and two files share one name

`skills/verify/scripts/pytest_record/specseal_pytest_record.py:144` (test
lines) and `:158` (collect lines) write
`os.path.normpath(os.path.join(rootdir, report.fspath))`. `report.fspath` is
the node id's path. pytest 9.1.1 makes a node id relative to the rootdir
only when the file lies under it. Otherwise the node id comes from the
initial path that reached the file (pytest's nodes module, the helper
that checks initial paths for a relative path, read in the built
environment). So the recorder joins a path relative to one directory onto
another.

The rootdir moves away from the files in more cases than `-c` and
`--rootdir`. pytest looks for a config file in each argument's directory,
so `pytest tests sub` with `sub/pytest.ini` makes `sub/` the rootdir and
puts `tests/` outside it.

What happened, executed through `broad_gate.py`'s own `recording_env`,
`read_record` and `compare_at_base` over a two-commit repository:

| Layout | HEAD record | Word |
|---|---|---|
| `-c ci/pytest.ini tests_a tests_b`. The base fails `tests_b/test_x.py` and passes `tests_a/test_x.py`. The branch breaks `tests_a/test_x.py` | both files recorded as `ci/test_x.py`, which does not exist | `ci/test_x.py  failing on base too` |
| `--rootdir=ci tests_a tests_b`, same files | same | same |
| `pytest tests sub` with `sub/pytest.ini`, no `-c`. The base fails `tests/test_x.py::test_root` and passes `sub/test_x.py::test_sub`. The branch breaks `test_sub` (NAME NOT IN TREE) | `tests/test_x.py` recorded as `sub/test_x.py` | `sub/test_x.py  failing on base too` |

In the last row the branch broke `sub/test_x.py` and the base passes it.
The base's failure belongs to another file. The gate gives the one word
whose job is to let a person set a failure aside. `compare_at_base`'s
docstring, rule 3's last sentence and `plan.md` all say the only way to that
wrong word is a forged record.

The corpus already plants the shape. Q3b runs `pytest tests a` with
`a/pytest.ini`, so `tests/` lies outside the rootdir `a/`. Its root files
are recorded under `a/` today. The case passes only because the names do
not collide.

**The fix is on the strict side.** A session whose arguments reach outside
its rootdir writes no record. HEAD then falls back to `NO_RECORD_AT_HEAD`,
and the base to `NO_RECORD`. Applied in the clone, executed:

- the three layouts above read `NO_RECORD_AT_HEAD`, and none reads
  `failing on base too`;
- the recorder module's ten cases pass;
- the gate module's cases selected by
  `cd_row or two_runners or rootdir or every_layout or symlinked or twice`
  pass, 68 of 69, all 55 corpus cases included. The one red is Q3b's "own"
  row, whose expected word moves from `not-reached:1` to the HEAD fallback,
  as the fix intends;
- the planted case below is red without the fix (`sub/test_x.py  failing
  on base too`) and green with it.

Finer fixes exist, such as mapping each initial path. They have to resolve
the collision pytest itself makes, two files with one node id, and nothing
in the report can do that. The strict refusal is the one that matches
"every failure of the mechanism falls on the strict side".

`--pyargs` arguments are module names and resolve to no path under the
invocation directory. The proposed check skips them. A `--pyargs` row whose
package lies outside the rootdir keeps today's behaviour. Its paths come
from an installed package, so they are outside both worktrees and compare
equal only to themselves.

### 🟡 2 — Q2's class is wider than the row rule 3 names

`-p specseal_pytest_record` reaches pytest through `PYTEST_ADDOPTS`, and the
module reaches `sys.path` only through `PYTHONPATH`. Anything that keeps the
first and drops the second makes pytest exit 1 with `ImportError: Error
importing plugin "specseal_pytest_record"` before any test. Q2 found one
instance, a row that replaces `PYTHONPATH`. Executed with a one-test green
suite under `recording_env`:

| Interpreter | Exit | Record |
|---|---|---|
| `python -m pytest` | 0 | one file |
| `python -I -m pytest` | 1, the import error | none |
| `python -E -m pytest` | 1, the import error | none |

Read: tox 4.64.9's default pass-env list passes neither variable, so a
default tox row records nothing, as rule 3 says. A tox file whose pass-env setting names `PYTEST_*` or `PYTEST_ADDOPTS`
is a wrapper that keeps one variable and drops the other.

Rule 3 (`templates/config.md:334`) tells the reader that "a wrapper that
rebuilds the environment writes no record ... its files read `new?`". It
names only the replaced `PYTHONPATH` as failing outright. A person whose
green suite fails at the gate under `python -I` finds nothing in rule 3
that says why. This is a document fix inside Q2's (a). It does not change
the trade.

### 🟡 3 — the recorder's warning raises out of a hook under warnings-as-errors

`skills/verify/scripts/pytest_record/specseal_pytest_record.py:103`,
`give_up`, calls `warnings.warn` under whatever filters are in force. With
`python -W error`, and with `SPECSEAL_RECORD_DIR` pointing at a directory
that does not exist, pytest ended in `INTERNALERROR> UserWarning:
specseal_pytest_record: no record written: ...`, exit 3. The suite's own
result is lost.

By reading, the same holds inside a test's run phase under pytest's
`-W error` or `filterwarnings = error`. That is a common configuration, and
pytest applies those filters around `pytest_runtest_logreport`. In both
forms the warning fires only when the record file cannot be opened or
written. The gate creates the directory, so the trigger is a disk that
fills, a directory removed mid-run, or permissions. The module docstring
and `spec.md` Scope 1 promise "never raises out of a hook".

Fix, executed in the clone: show the warning under its own filter. With it,
the same run printed the `UserWarning` once and exited 1 (the probe's
planted failure), with no INTERNALERROR. The recorder module's ten cases
pass.

## Findings — from reading

### ⬜ 4 — the spec was not fed back after phase 4, and the overview says nothing was

Paperwork under `seal/specs/`, reported as a correction:

- `overview.md:48`: "none — phase 2 added no clause to `spec.md`". Phase 4
  corrected R4 and §*The class*, and this section is where that belongs.
- `spec.md:79` (R4), `spec.md:117` (§*The class*, "Two files at one relative
  path"), `spec.md:154` (Scope 1, `report.location[0]`).
- `plan.md:89` (the six-months-on scenario names `report.location`) and
  `plan.md:115` (Alternative M's grounds).

After 🔴 1's fix, the fed-back clause should say what the recorder now
writes and what it refuses.

### ⬜ 5 — "compared at the base" heads rows whose base was never run

`skills/verify/scripts/broad_gate.py:2940` prints "failing test files,
compared at the base:" over every verdict map. Since this branch, that
includes the `NO_RECORD_AT_HEAD` map, built where the base was not run.
Each row's own reason says "the base was not run", so the reader is told
twice and the two statements disagree. The behaviour and the words are
right. Only the heading reads badly.

## What was checked and holds

- The key rule. The `pop` at import plus the claim-once in
  `pytest_configure` mean a child pytest and an xdist worker hold no key.
  Read, and S2 to S4's cases ran in the orchestrator's run.
- `record_path`. `realpath` on both sides, `..` refused as outside, and a
  Windows drive change handled by `ValueError`. The `/` spelling is
  unverified on Windows, and `overview.md` names CI as its answerer.
- `recording_env`. Prepend and append, `os.pathsep`, the records directory
  is absolute, and the base gets its own key. A repeated `-p` from an outer
  gate run is skipped by pytest (R2).
- A row run with `-n 2 -x --dist=loadfile`, where the base stops early, did
  NOT produce a false `new` for a partly-run file. xdist ran the stopped
  worker's whole file. Executed, no finding.
- The neighbouring modules that read what this change touches. They are
  the new shipped `.py`, rule 3, the **New?** bullet, the ledger fragment
  and the overview. They are listed under executed probes. All pass at
  1bbbdca9.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the outside-rootdir
  case below (🔴 1), and the Q3b "own" row's word moved in the corpus table.
- `tests/test_the_recorder_writes_what_its_process_ran.py`: a case that runs
  the recorder with an unwritable directory under `python -W error` and
  asserts pytest's own exit, not 3 (🟡 3).
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`, the rule-3 pin: the
  widened Q2 sentence (🟡 2).

## Facts for the evidence ledger

- pytest 9.1.1 names a test file outside its rootdir against the initial
  path that reached it, so the node id's path, `report.fspath`, is not
  relative to the rootdir there. A config file in one argument's directory
  moves the rootdir there. Executed in this round. It belongs beside W1,
  which states "the rootdir joined to `report.fspath`" as the collecting
  module's absolute path without that condition.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The recorder joins `report.fspath` to the rootdir, which names a file outside the rootdir against the wrong directory; two files share one name and a file the branch broke reads `failing on base too` from another file's failure at the base | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:144` | open | executed: `pytest tests sub` with `sub/pytest.ini`, and `-c ci/pytest.ini`, `--rootdir=ci` over two `test_x.py` files, each gave `failing on base too` to a file the base passes; the strict fix turns each into `NO_RECORD_AT_HEAD`, the planted case is red without it and green with it, and the corpus's Q3b "own" row moves |
| 🟡 2 | Rule 3 names only a replaced `PYTHONPATH` as failing at the gate; `python -I`, `python -E` and a wrapper passing `PYTEST_ADDOPTS` alone fail a green suite the same way, while rule 3 says such wrappers' files read `new?` | `templates/config.md:334` | open | executed: a one-test green suite exits 1 with the recorder's import error under `-I` and `-E`, and 0 plain; read: tox 4.64.9's default pass-env list |
| 🟡 3 | The recorder's warning raises out of a hook under warnings-as-errors, ending the measured run in INTERNALERROR | `skills/verify/scripts/pytest_record/specseal_pytest_record.py:103` | open | executed: `python -W error` with an unwritable records directory, exit 3; with the warning under its own filter, exit 1 (the planted test) and no INTERNALERROR |
| ⬜ 4 | Phase 4's correction of R4 was not fed back: `spec.md` still says `report.location[0]` and "two files at one relative path coincide only for one file", and `overview.md` says nothing was fed back | `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/overview.md:48` | open | read; paperwork correction, not counted in Needs a fix; also `spec.md:79`, `spec.md:117`, `spec.md:154`, `plan.md:89`, `plan.md:115` |
| ⬜ 5 | The failure form heads `NO_RECORD_AT_HEAD` rows with "compared at the base", where the base was not run | `skills/verify/scripts/broad_gate.py:2940` | open | read; each row's reason says the base was not run, so behaviour and fact are right |
| 🟢 | Q1 and Q2 built as (a) | `skills/verify/scripts/broad_gate.py:2038`, `templates/config.md:334` | confirmed | read: `base_word` gives `NOT_REACHED` with the exit on a non-zero base for a file in no session; rule 3 and the Q2 case hold the replaced-`PYTHONPATH` row failing at the gate |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🔴 1 — `skills/verify/scripts/pytest_record/specseal_pytest_record.py`, `Recorder`

Add the method and call it first in `pytest_sessionstart`. Its docstring
replaces nothing, but the module docstring's paragraph beginning "A path
is the rootdir joined to `report.fspath`" should gain the sentence after
this block.

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

Module docstring, appended to the paragraph on paths:

```
That holds only where pytest names files against the rootdir, which it does
for every file under it. A session handed a path outside its rootdir names
those files against the argument instead, so it writes no record, and its
files read `new?` (#825 round 1).
```

### 🔴 1 — `tests/test_the_seal_is_taken_once_by_the_sealer.py`, the planted case

Seen red without the fix and green with it in this round's clone.

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

### 🔴 1 — the corpus, Q3b's "own" row and `word_for`

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

### 🔴 1 — `templates/config.md` rule 3, and its pin

Replace the last sentence of rule 3, and the pinned sentence with it:

```
One limit is named rather than closed: a test written to append to the record file the recorder is writing, or to write a record of its own with the gate's key, can put a line into a keyed record, and that is the one way to a wrong `failing on base too`. A pytest handed a path outside its rootdir — `-c` or `--rootdir` elsewhere, or a config file in one of its arguments' directories — names those files against the argument rather than the rootdir, so it writes no record and its files read `new?`
```

### 🟡 2 — `templates/config.md` rule 3, the Q2 sentence, and its pin

```
A row that keeps `PYTEST_ADDOPTS` and loses `PYTHONPATH` fares worse — one that replaces `PYTHONPATH`, an interpreter run with `-I` or `-E`, a wrapper that passes `PYTEST_ADDOPTS` or `PYTEST_*` on and not `PYTHONPATH`: pytest cannot import the module the `-p` names and exits 1 before any test runs, so the row fails at the gate.
```

The pin in
`test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written`
takes the same sentence in place of the "A row that replaces `PYTHONPATH`
and keeps `PYTEST_ADDOPTS` fares worse" entry.

### 🟡 3 — `skills/verify/scripts/pytest_record/specseal_pytest_record.py`, `give_up`

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

Needs a fix: yes — 🔴 1 (a file outside pytest's rootdir is recorded under
the wrong path, and a file the branch broke reads `failing on base too`),
🟡 2 (rule 3 does not name the rest of Q2's class), 🟡 3 (the recorder's
warning raises out of a hook under warnings-as-errors)

Loses a record or crashes: yes — 🟡 3: with the records file unwritable and
warnings as errors, the measured pytest ends in INTERNALERROR, exit 3, and
its own result is lost

## Proof block

Files opened this round, at 1bbbdca9 in the worktree or its clone:
`skills/verify/scripts/pytest_record/specseal_pytest_record.py` (whole);
`skills/verify/scripts/broad_gate.py` (the diff, `run`, `recording_env` to
`base_word`, `compare_at_base`, `failure_lines`, `gate`'s failure loop);
`templates/config.md` (rule 3); `skills/verify/SKILL.md` (the **New?**
bullet); `tests/test_release_hygiene.py`,
`tests/test_every_reader_ends_a_line_where_gfm_does.py`,
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
`tests/test_the_gate_hands_cmd_a_path_it_can_run.py` (their diffs);
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the list of cases the
diff added and removed, `test_a_path_holding_a_space_is_named_and_compared`,
the corpus's Q3b row, `word_for`, the rule-3 pin);
`tests/test_the_recorder_writes_what_its_process_ran.py` (its case list);
the work item's `spec.md`, `questions.md`, `overview.md`, `routing.md`,
`handoff.md`, `plan.md` (technical context and alternatives),
`phases/phase-4.md`; the ledger fragment's W1 and Corrected R5 rows;
`skills/implement/SKILL.md` (the memo's four sections);
`templates/sdd-overview.md`; `.github/scripts/run_tests.py` (its docstring);
pytest 9.1.1's config module (the function that decides the arguments)
and nodes module (the initial-path helper); tox 4.64.9's default
pass-env lists.
