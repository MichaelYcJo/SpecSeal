# Round 1 report — 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure

| Field | Value |
|---|---|
| Target SHA | cdb57895 |
| Base | `release/v0.18.3` at a3aa139a |
| Pull request | #814 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

The decisive property does not hold. `failing on base too` comes from one
code path, and the proof pass guarding it is sound for what it asks: whether
the base run of one file collected only that file. What it does not ask is
whether that run is the base's run as the row ran the file. Two shapes break
the property, each executed end to end against real pytest 9.1.1, and in each
the target gives the permissive word where a3aa139a gave `new`:

1. **A file the base passes beside the other failing files and fails alone**
   (🔴 1). The target sends every file of a failing group to run alone, and
   a3aa139a never did. A sibling module that puts a directory on `sys.path`,
   state a sibling sets at import, and a session fixture whose teardown
   error pytest gives to the last test of each session all produce it.
2. **A runner without the gate's environment that comes first** (🔴 2). A
   container-style runner whose report the gate cannot see is passed over,
   so the measurement settles at a later host runner. The proof pass then
   sees one trailer, because the first runner ignores `PYTEST_ADDOPTS`.
   Rule 3 names this class only for a *later* runner, and says the words are
   "as they were before". For a first runner that sentence is false.

Both are regressions against a3aa139a. A verified paste-ready fix for both is
below: it turns all four probe layouts to `new?`, keeps the normal case and
the S3–S5 shape, and passes the three gate modules unchanged (597 passed,
1 skipped). The planted corpus (53 of 55 parameters, 64 file words, at three
gates) has no leak, which matches phase 2's table. It just contains neither
class.

## Enumeration: every path to `failing on base too`

Read at cdb57895. `ON_BASE` is assigned at one site,
`skills/verify/scripts/broad_gate.py:2274`. It is reached only from a proof
pass, and a proof pass is queued only at `:2295`, for a file whose run alone
settled with `failing > 0`. A file runs alone in three ways:

| Route | Code | Also alone at a3aa139a? |
|---|---|---|
| a candidate (path absent from the base's root tree) | `:2226` | yes |
| the single non-candidate (`len(others) == 1`) | `:2227-2228` | yes (a group of one) |
| a file of a group of several whose run did not decide it | `:2291` | **no**, a3aa139a judged the group's run |

So the target diverges from a3aa139a in two places. The third route is new.
The settling prefix also changed: the first prefix that writes a report,
where a3aa139a used the first that prints a pytest summary. 🔴 1 is the third
route and 🔴 2 is the changed settling prefix. I found no other divergence.

What the proof checks and holds (executed, table under Executed probes):
one trailer, the listing names, the count sum, error lines, colour,
deselection and `-n 2`, across pytest 8.1.1, 8.3.5 and 9.1.1. A tail that
cuts listing lines is caught by the sum check (read). A conftest or a later
part printing a trailer-shaped line adds a session, so it reads stricter
(read). A conftest printing a listing line naming `h` cannot hide another
file's real listing line (read). Collection does not differ between the run
alone and the proof: same prefix, same cwd, same environment plus
`--collect-only -vv -o …` (read). `testpaths` is ignored once a path is
handed, and an ini `addopts` that adds a path lists that path's files, so
the result is beyond (read).

## Findings — from execution

### 🔴 1 — a file the base passes beside the others and fails alone reads `failing on base too`

`skills/verify/scripts/broad_gate.py:2291` (the group's fallback to runs
alone) and `:2274` (the word). **Regression against a3aa139a: yes.**

When a group of several fails at the base, each file runs alone, and a file
whose run alone fails and whose proof lists it alone reads `failing on base
too`. The proof shows the base run collected only `h`. It does not show that
the base, running `h` beside the other failing files the way the row ran it,
fails `h`. Those differ whenever a test depends on a sibling. The phase-1
table (`Now` column, the cannot-collect case) is where this route first gave
the word. The spec's construction (`spec.md` §*The frame*, condition 1, "`h`
ran alone") treats running alone as the cure and never treats it as a cause.

Executed, through each gate's `compare_at_base` on scratch repositories with
pytest 9.1.1, row `python -m pytest -q`:

| Layout | File | a3aa139a | fb698f90 | target |
|---|---|---|---|---|
| A: `test_a` puts `tests/lib` on `sys.path`, `test_b` imports from it; the branch breaks the helper | `tests/test_b.py` | `new` | `new` | **failing on base too** |
| A2: `test_a` sets an environment variable at import that `test_b` reads; the branch regresses `test_b` | `tests/test_b.py` | `new` | `new` | **failing on base too** |
| B: a session fixture's teardown raises at the base; the branch regresses both files | `tests/test_a.py` | `new` | `new` | **failing on base too** |

In A, `test_b`'s run alone at the base is a collection error (`No module
named 'helper'`). Its proof reads `no tests collected, 1 error` with
`ERROR tests/test_b.py`, which `proof_refused` accepts. In B, the teardown
error lands on the last test of each session. Run alone, every file's last
test carries it, and the report counts it as an `error` child of that file's
testcase. In each layout the branch's regression is new, and the gate would
seal it as inherited.

Who meets it: a sibling module that edits `sys.path` (older suites, and the
`prepend` import mode's own per-directory insertion), test pollution
through `os.environ` or module globals, and a session fixture with a broken
teardown. These are ordinary, and a release branch with one known failing
file plus one new one is exactly a group of several.

The fix (paste-ready below, verified) compares counts the gate already has,
with no new run. A group that ran every test its files hold alone but failed
fewer tests than they fail one by one shows that some failure alone is not a
failure beside the others. No count says whose failure that is, so every
file of that group that earned the word alone falls back to `new?` with a
new reason. A group that ran fewer tests than its files hold alone gives no
company evidence: it stopped, was interrupted, or was handed a path it
lacks. That group keeps the target's words, so both phase-1 gains stand
(see the ❓ row).

- **What remains checked**: layouts A, A2 and B read `new?`. The normal
  shape (a pre-existing failing file plus a new one the base passes) keeps
  `failing on base too` and `new`.
- **What it costs**: in a group where one file is company-dependent, a
  file that is truly pre-existing loses its word too (`tests/test_a.py` in A
  reads `new?`). a3aa139a gave that file `failing on base too`. The result is
  stricter, never permissive.
- **What it does not close**: two dependencies whose counts cancel out (one
  file passes only beside the others, another fails only beside them). Name
  it in rule 3. A leave-one-out run (the group without `h`) is the finer
  alternative and costs one run per file the base fails alone.

### 🔴 2 — a first runner without the gate's environment hands the measurement to the host runner after it

`skills/verify/scripts/broad_gate.py:2008` (`proof_refused` counts only
collect-only trailers), and `templates/config.md:333`, rule 3's "Two limits
still read a word the gate did not measure … Both are as they were before
the proof run existed." **Regression against a3aa139a: yes.**

Executed, with row `python box.py -q -m box && python -m pytest -q -m 'not
box'`. Here `box.py` emulates a container: it forwards its arguments,
rewrites `--junitxml=` to a path inside "the box", and runs pytest with an
environment of its own. At the base the box passes the file's
`box`-marked test. On the host, the file's other test is a pre-existing
failure. The branch regresses the box test, so the box fails and `&&`
stops.

| Gate | Word for `tests/test_two.py` |
|---|---|
| a3aa139a | `new` (it settled at prefix 1: the box printed pytest's summary) |
| fb698f90 | `failing on base too` |
| target | **failing on base too** |

The target's prefix 1 writes no report the gate can see, so prefix 2
settles on the host runner, which fails the file's other test. The proof's
output holds the box's ordinary `1 passed, 1 deselected in 0.01s` and the
host's single collect-only trailer listing `tests/test_two.py: 1`. That
counts as one session. A `docker compose run … pytest -m db && pytest -m
"not db"` row is this shape, and so are `ssh`, `kubectl exec`, and a
`sudo` that resets the environment.

The fix (paste-ready below, verified) uses the fact that under the proof no
session that received `PYTEST_ADDOPTS` runs a test. So pytest's outcome line
(`N passed in Ts`) in the proof's output comes from a runner without the
gate's environment, and it reads `MULTI_RUNNER`. This only ever makes a
word stricter. It also closes the rule-3 limit for a *later* env-less
runner, wherever that runner prints its outcome line. Rule 3 then needs its
sentence narrowed (fenced below): runners at `-qq` or quieter print no
outcome line and remain a limit.

## Findings — from reading

### ⬜ 3 — rule 3's `pytest -q tests` example is measured under pytest 8.1–8.3

`templates/config.md:333`, "Each of these reads `new?` for every file the
base fails: a row whose runner collects beyond the files appended to it
(`pytest -q tests`, …)". Executed: under pytest 8.1.1 and 8.3.5,
`pytest -q tests tests/test_two.py` collects only `tests/test_two.py`, in
the real run and under the proof alike. Its proof is therefore proven, and
the word is true. Under 9.1.1 it collects all of `tests`. The behaviour is
right and the example is version-dependent. Replace "a row whose runner
collects beyond the files appended to it (`pytest -q tests`, `pytest -q
tests/unit`)" with "a row whose runner collects beyond the files appended to
it (`pytest -q tests/unit` with a file outside `tests/unit`, or `pytest -q
tests` under pytest 9)".

### ⬜ 4 — the PR body's acceptance sentence

PR #814's body says "No `failing on base too` appears where a3aa139a did not
give it, except the S3–S5 shapes". Phase 2 itself records two more
(`phases/phase-2.md`, "Two existing cases also gained the word"), and this
round adds three layouts plus one runner shape. The orchestrator owns the
body.

### ❓ — two gains outside the S3–S5 shape: the acceptance rule's call

The acceptance test (`spec.md` S17, as the orchestrator restated it) admits
only S3–S5. Phase 2 records two more `failing on base too` words where
a3aa139a was stricter, and calls both "the base's". I checked each:

- `test_a_run_of_several_that_counted_only_warnings_sends_each_file_alone`:
  a3aa139a gave `NO_RUNNER`. The base's row as written (`cd sub && pytest …
  tests`) runs only `sub/tests/test_one.py` there, and the base fails it
  (`FAILING_TEST`). The word is the row's own truth.
- `test_a_file_the_base_cannot_collect_is_measured_alone[files-only]`
  (`test_two`): a3aa139a gave its stopped-early reason. At the base the row
  as written is interrupted by `test_three`'s collection error and never
  runs `test_two`. The word comes from `test_two` run alone, which fails a
  plain test.

Neither is the S3–S5 shape, and neither is wrong for the file alone. The
fix for 🔴 1 leaves both standing because their groups ran in no company. The
strict variant (drop the `tests >=` guard) turns both back to `new?` and
changes those two assertions plus the case's `xdist` parameter. I measured
it: 3 failed, 498 passed. Who answers it: the orchestrator, against the
owner's acceptance rule.

## What was checked and holds

- **The S3–S5 shape (executed, one of the 18)**: an outer test that runs
  pytest in a subprocess and fails, under row `pytest -q -rN -s`. a3aa139a
  gives `new` and the target gives `failing on base too`, and the base does
  fail that file. The other 17 matrix words are carried from phase 2's
  statement (read).
- **The planted corpus (executed, 53 of 55 parameters)**: I ran every
  parameter of
  `test_every_layout_the_first_build_reopened_reads_the_word_the_base_gives`
  except N3's symlink pair, through a3aa139a's, fb698f90's and the target's
  `compare_at_base`, which gave 64 file words. No target `failing on base too`
  appears where a3aa139a was stricter. Every row I compared against phase
  2's table matches, including P1/P2/Q1 `files` → `new`, the P7 layouts
  → `new?`, N1c and N7 `files` → `failing on base too`, and N7 `own`
  → `new?`.
- **The overview's three divergences (read)**: a one-file group runs alone
  from the start (`:2225-2228`, numbered at `:2241-2243`). A group with no
  report reads `NO_RUNNER` for each file (`:2283-2285`), which is strict.
  Three assertions changed word: the two gains are in the ❓ above, and the
  third is `new`, which is stricter than `failing on base too`.
- **Rule 3's stricter rows against the code (executed for the reader, read
  for the rest)**: a runner that collects beyond gives `COLLECTED_BEYOND`
  (with ⬜ 3's version caveat). A rootdir that differs from the runner's
  directory fails the name check (listing nodeids are rootdir-relative,
  `FAILED` lines cwd-relative). An unknown `verbosity_test_cases` (pytest
  before 8.1) prints a tree with no `name: count` line, so the sum fails. A
  row that sets `PYTEST_ADDOPTS` itself runs tests and prints no trailer,
  which gives `MULTI_RUNNER`. At `-qqqq` there is no trailer (executed:
  `MULTI_RUNNER` on all three versions). A `( … )` group cuts no prefix, so
  the appended arguments break the shell line and nothing settles. Each
  reads `new?` as the text says. The cost sentences match the loop.
- **The seal (read)**: a green run never reaches `compare_at_base`. Its one
  call (`:3434`) is inside `if name == SUITE` and `if files`, and no hunk of
  this diff touches `gate`. This repository's row ends in `bin/test -q`, and
  `.github/scripts/run_tests.py:644` hands pytest `argv or ["tests"]`, so a
  handed file is the only path, as the PR says. Phase 1's S18 probe executed
  it; carried.
- **§2 audit**: `overview.md` labels the full suite, lint and typecheck
  `unverified` and names the sealer as the one who runs them. The label is
  honest: nothing in the record claims a broad run.

## Regression tests to plant

Destination: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside
the S13 group case. Seen red at cdb57895 (4 failed, each on
`'failing on base too' != 'failing on base too'`) and green with the fix
below (4 passed), executed in the clone. Also pin the new reason whole in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it`, and pin
rule 3's new sentences in
`test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written`.

```python
PRE_EXISTING = "def test_old():\n    assert False, 'pre-existing'\n"


@pytest.mark.parametrize(
    "at_base, on_feature",
    [
        pytest.param(
            {
                "tests/test_a.py": "import os, sys\n"
                "sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))\n\n"
                + PRE_EXISTING,
                "tests/lib/helper.py": "VALUE = 1\n",
                "tests/test_b.py": "import helper\n\n"
                "def test_b():\n    assert helper.VALUE == 1\n",
            },
            {"tests/lib/helper.py": "VALUE = 2\n"},
            id="a-sibling-puts-a-module-on-the-path",
        ),
        pytest.param(
            {
                "tests/test_a.py": "import os\nos.environ['MODE'] = 'ready'\n\n"
                + PRE_EXISTING,
                "tests/test_b.py": "import os\n\n"
                "def test_b():\n    assert os.environ.get('MODE') == 'ready'\n",
            },
            {
                "tests/test_b.py": "import os\n\n"
                "def test_b():\n    assert os.environ.get('MODE') == 'gone'\n"
            },
            id="a-sibling-sets-state",
        ),
        pytest.param(
            {
                "conftest.py": "import pytest\n\n"
                "@pytest.fixture(scope='session', autouse=True)\n"
                "def res():\n    yield\n    raise RuntimeError('teardown')\n",
                "tests/test_a.py": "def test_a():\n    assert True\n",
                "tests/test_b.py": "def test_b():\n    assert True\n",
            },
            {
                "tests/test_a.py": "def test_a():\n    assert False\n",
                "tests/test_b.py": "def test_b():\n    assert False\n",
            },
            id="a-session-teardown-error-goes-to-each-sessions-last-test",
        ),
    ],
)
def test_a_file_the_base_fails_only_alone_is_not_called_failing_on_base_too(
    tmp_path, at_base, on_feature
):
    """A file of a group the base passes beside the others and fails alone
    reads `new?`, never `failing on base too`."""
    repo = base_then_feature(tmp_path / "repo", FILES_ROW, at_base, on_feature)
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    gate = gate_module()
    for path in ("tests/test_a.py", "tests/test_b.py"):
        assert verdict_of(out.stdout, path) != gate.ON_BASE, out.stdout
    assert verdict_of(out.stdout, "tests/test_b.py").startswith(gate.NOT_MEASURED), (
        out.stdout
    )


BOX = (
    "import os, subprocess, sys\n"
    "args = ['--junitxml=box.xml' if a.startswith('--junitxml=') else a\n"
    "        for a in sys.argv[1:]]\n"
    "env = {'PATH': os.environ['PATH'], 'IN_BOX': '1'}\n"
    "sys.exit(subprocess.call([sys.executable, '-m', 'pytest', *args], env=env))\n"
)
TWO = (
    "import os\n\n"
    "def test_in_box():\n    assert os.environ.get('IN_BOX') == '{want}'\n\n"
    "def test_on_host():\n    assert os.environ.get('HOST_READY'), 'pre-existing'\n"
)


def test_a_runner_without_the_gates_environment_before_the_measured_one_costs_the_word(
    tmp_path,
):
    """A first runner that keeps its own environment and its own report (a
    container, emulated) named the file; the host runner after it fails
    another test of the file at the base. The proof pass sees one trailer,
    and the box's own outcome line is the second runner it must count."""
    py = sys.executable
    row = (
        f"{py} box.py -q -p no:cacheprovider -k test_in_box && "
        f"{FILES_ROW} -k test_on_host"
    )
    repo = base_then_feature(
        tmp_path / "repo",
        row,
        {"box.py": BOX, "tests/test_two.py": TWO.replace("{want}", "1")},
        {"tests/test_two.py": TWO.replace("{want}", "2")},
    )
    out = run_gate(repo, keep=tmp_path / "out")
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") != gate_module().ON_BASE, out.stdout
```

## Facts for the evidence ledger

- R2 (the proof pass) gains: an outcome line in the proof's output
  (`RAN_RE`) reads `MULTI_RUNNER`. NAME NOT IN TREE
- R3 (the groups) gains: a group of several that went file by file is
  compared by counts with its files' runs alone, and words earned alone fall
  back to the company reason where the group ran every test and failed
  fewer.
- R4 (rule 3) changes with the narrowed limit sentence and the company
  sentence below.
- Measured this round: pytest 8.1.1 and 8.3.5 collect only the file for
  `pytest tests tests/test_two.py`, and 9.1.1 collects all of `tests`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A file the base passes beside the other failing files and fails alone (sibling `sys.path`, sibling state, a session teardown error) reads `failing on base too`; a3aa139a gave `new` | `skills/verify/scripts/broad_gate.py:2291` | open | executed: layouts A, A2, B through three gates' `compare_at_base`; four regression cases red at cdb57895; regression against a3aa139a |
| 🔴 2 | A first runner without the gate's environment (container-style) is passed over, the host runner after it measures, and its proof sees one trailer: `failing on base too` where a3aa139a gave `new`; rule 3's "as they were before" is false for it | `skills/verify/scripts/broad_gate.py:2008` | open | executed: layout C (emulated box) through three gates; regression against a3aa139a |
| ⬜ 3 | Rule 3's `pytest -q tests` example reads `new?` only under pytest 9; 8.1–8.3 collect only the handed file and the word is measured | `templates/config.md:333` | open | executed: proof reader over 8.1.1, 8.3.5, 9.1.1 |
| ⬜ 4 | PR body says no exception outside S3–S5; phase 2 records two and this round adds more | PR #814 body | open | read; the orchestrator owns the body |
| ❓ | Two `failing on base too` gains outside the S3–S5 shape (warnings-only group; interrupted group's `test_two`) | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4752` | ❓ out of verified scope | each is true for the file alone and the first is the row's own truth; whether the acceptance rule admits them is the orchestrator's call against the owner's rule; the strict variant of fix 1 reverts both (measured: 3 failed, 498 passed) |
| 🟢 | The proof reader: one trailer, names, sum, errors, colour, deselection, `-n 2` | `skills/verify/scripts/broad_gate.py:1979` | confirmed | executed across pytest 8.1.1, 8.3.5, 9.1.1, 13 shapes each |
| 🟢 | The planted corpus leaks nothing and matches phase 2's table | `tests/test_the_seal_is_taken_once_by_the_sealer.py:5814` | confirmed | executed: 53 of 55 parameters, 64 file words, at a3aa139a, fb698f90, cdb57895 |
| 🟢 | A green run is unchanged; this repository's row hands pytest only the file | `skills/verify/scripts/broad_gate.py:3434` | confirmed | read: no hunk in `gate`; `.github/scripts/run_tests.py:644` uses `argv or ["tests"]`; S18 carried |

## Executed probes

| What was run | Result |
|---|---|
| Narrow module run in the clone at cdb57895, the five modules the prompt names | 716 passed, 1 skipped, exit 0 |
| `bin/evidence-check --strict .` in the clone at cdb57895 | exit 0 |
| Layouts A, A2, B, C plus two controls (normal; S3–S5 inner run under `-rN -s`) through a3aa139a, fb698f90, cdb57895 and the patched gate | A/A2 `test_b`, B `test_a`, C `test_two`: target `failing on base too`, a3aa139a `new`; patched gate `new?` for all four; controls unchanged across gates except S3–S5's accepted `new` → `failing on base too` |
| Planted corpus, 53 of 55 parameters (N3's symlink pair skipped), three gates | 64 file words; no target `failing on base too` where a3aa139a was stricter |
| Proof reader over real collect-only output, pytest 8.1.1 / 8.3.5 / 9.1.1 × 13 shapes | as expected everywhere; `-qqqq` → `MULTI_RUNNER`; error under `-rN` → beyond; `tests tests/test_two.py` proven under 8.x (pytest collected only the file) |
| Patched gate against the gate's three modules | 597 passed, 1 skipped |
| Strict variant of the patch (no `tests >=` guard) against two modules | 3 failed (the two ❓ gains, two params of one), 498 passed |
| The four regression cases above | red at cdb57895 (4 failed on the permissive word), green with the patch (4 passed) |
| Broad gate: the full suite, lint and typecheck after the rounds | not yet — not run by this round; the sealer's, once the rounds settle |

## Paste-ready fixes

### 🔴 1 and 🔴 2 — `skills/verify/scripts/broad_gate.py` (verified as one patch)

```diff
@@ -1929,6 +1929,28 @@
     "collected-at-base-{n}.txt), so the gate cannot tell which runner the "
     "failure is from. A row earns the measured word by running pytest once"
 )
+# Formatted with the number of the file's run alone. A file of a group of
+# several that the base fails alone, where the group's run at the base failed
+# fewer tests than its files fail one by one: some file fails alone and not
+# beside the others (a module another one puts on `sys.path`, state another
+# one sets, a session fixture's error pytest gives the last test of each
+# session), and a count does not say which.
+COMPANY = (
+    f"{NOT_MEASURED}: the base fails this file run alone, but the run of the "
+    "failing files together at the base failed fewer tests than they fail one "
+    "by one (kept as suite-at-base-<k>.txt and suite-at-base-<k>-{n}.txt), so "
+    "the failure alone may not be the base's failure in the row"
+)
+# pytest's outcome line, for a session that RAN tests: `1 passed in 0.01s`,
+# `== 1 failed, 2 passed in 0.12s ==`. Under the proof pass no session that
+# received `PYTEST_ADDOPTS` runs a test, so this line is a runner started
+# without the gate's environment (`tox`, `env -i`, a container), and the
+# trailer count cannot see it.
+RAN_RE = re.compile(
+    r"^=*[ ]*\d+ [a-z]+(?:, \d+ [a-z]+(?: [a-z]+)?)* in \d+(?:\.\d+)?s"
+    r"(?: \(\d+:\d\d:\d\d\))?[ ]*=*$",
+    re.M,
+)
 
 
 def report_counts(data):
@@ -2005,7 +2027,7 @@
     """
     plain = COLOUR_RE.sub("", text)
     trailers = list(COLLECTED_RE.finditer(plain))
-    if len(trailers) != 1:
+    if len(trailers) != 1 or RAN_RE.search(plain):
         return MULTI_RUNNER
     alone, selected, errors = trailers[0].groups()
     collected = int(alone or selected or 0)
@@ -2227,6 +2249,9 @@
         if len(others) == 1:
             work.append((others, None))
         verdicts, number, n = {}, {}, 0
+        # A group of several that went file by file, with its report's
+        # `(tests, failing)`, and each of its files' `(tests, failing)` alone.
+        together, alone_counts = None, {}
         for group, proving_at in work:
             if proving_at is not None:
                 (path,) = group
@@ -2288,9 +2313,11 @@
                 if tests and not failing and code == 0:
                     verdicts.update({f: NEW for f in group})
                 else:
+                    together = (group, tests, failing)
                     work += [([f], None) for f in group]
                 continue
             (path,) = group
+            alone_counts[path] = (tests, failing)
             if failing:
                 work.append((group, prefix))
             elif (code == 0 and tests) or (
@@ -2299,6 +2326,23 @@
                 verdicts[path] = NEW
             else:
                 verdicts[path] = NOT_ENDED.format(code=code, kept=f"{name}.txt")
+        # A run alone measures the file without the others, and the branch ran
+        # it beside them. Where the group ran every test its files hold alone
+        # and still failed fewer than they fail one by one, some failure alone
+        # is not the base's failure beside the others, and no count says
+        # whose: every word the group's files earned alone falls back to
+        # `new?`. A group that ran fewer tests (stopped, interrupted, handed a
+        # path it lacks) ran some file in no company, and says nothing.
+        if together is not None:
+            group, tests, failing = together
+            counts = [alone_counts.get(f) for f in group]
+            if None in counts or (
+                tests >= sum(t for t, _ in counts)
+                and failing < sum(x for _, x in counts)
+            ):
+                for f in group:
+                    if verdicts[f] == ON_BASE:
+                        verdicts[f] = COMPANY.format(n=number[f])
         return {f: verdicts[f] for f in files}
     finally:
         subprocess.run(
```

### 🔴 1 and 🔴 2 — `templates/config.md` rule 3 (the limit sentence and a company sentence)

```text
Replace:
  Two limits still read a word the gate did not measure. **A second runner the proof run does not reach, or reaches without the gate's environment** — one started by `tox`, `nox`, `env -i` or a container, one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq` — leaves the row read as one with a single runner, so a file a later runner named can read `failing on base too` from the measuring runner's directory.

With:
  A runner started without the gate's environment — by `tox`, `nox`, `env -i` or a container — runs its tests during the proof run, and the outcome line it prints counts as a second session, so the file reads `new?`, whichever runner comes first. A file the base fails alone, from a group of failing files that ran every test together at the base and failed fewer than they fail one by one, reads `new?` too: some file there fails alone and not beside the others, and no count says which. Two limits still read a word the gate did not measure. **A second runner the proof run does not reach, or that prints nothing it can read** — one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq`, one started without the gate's environment at `-qq` or quieter — leaves the row read as one with a single runner, so a file a later runner named can read `failing on base too` from the measuring runner's directory.
```

Needs a fix: yes — 🔴 1 (a file the base fails only alone reads failing on base too) and 🔴 2 (a first runner without the gate's environment hands the measurement to the next runner)
Loses a record or crashes: no

## Proof block

Files opened this round:
`skills/verify/scripts/broad_gate.py` (at cdb57895, lines 1776–2310 and the
`gate` call site, plus the hunk list), a3aa139a's and fb698f90's
`broad_gate.py` (via `git show`), `templates/config.md` (rule 3, via the
diff), `skills/verify/SKILL.md` (diff), `.github/scripts/run_tests.py`
(argument handling), `bin/test`, `seal/config.md` (`Broad gate` row),
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the helpers, S13,
the warnings case, the cannot-collect case, the planted corpus case),
`seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/`
`overview.md`, `phases/phase-1.md`, `phases/phase-2.md`, `spec.md`
(the frame, the scope), `seal/ledger/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure.md`,
`skills/code-review/scripts/round_record.py` (the verdict vocabulary), and
PR #814's body. Not opened: `plan.md`, `questions.md`, `phases/phase-3.md`,
`survivors.md`, `changelog.md`, and the first build's round records at
a82f8f8f. The corpus was reached through the planted case's own layouts,
not through those records.
