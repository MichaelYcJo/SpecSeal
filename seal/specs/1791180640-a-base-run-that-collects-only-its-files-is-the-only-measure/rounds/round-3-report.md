# Round 3 report — 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure

| Field | Value |
|---|---|
| Target SHA | 95422c35 |
| Base | `release/v0.18.3` at a3aa139a |
| Fix range checked | `275cd1a0..d9ce4e1a` (code in d3095fea and 6b34713d) |
| Pull request | #814 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

## Summary

Round 2's 🔴 1 and 🟡 3 are closed. A group of several failing files now
reads `COMPANY` whatever any count says, and no file of it runs alone. Every
group layout rounds 1 and 2 built (A, A2, B, cancel, cancel2, outweigh,
flaky2) reads `COMPANY` for every file at 95422c35.

Round 2's 🟡 2 is closed for the layout round 2 built, but not for its
class (🟡 1 below). The proof decides "this session is the measuring
runner's" by the absence of a `<path>: <count>` line. A later runner that
collects no test at the base prints no such line either. The proof then
sees zero node ids against a trailer of zero and accepts the file. Two
shapes were executed: the later runner's directory holds no test at the
base, and the later runner deselects every test at the base. Both read
`failing on base too` at 95422c35, under pytest 8.1.2, 8.3.5 and 9.1.1.
a3aa139a read `new?` and `new`. **This is a regression against the base**,
and it is the only `failing on base too` I found at the target that
a3aa139a did not also give. A one-condition fix is fenced below. With it,
the narrow run passes except one unit parameter that pins the hole itself
(`everything-deselected`), which the fix flips.

Everything else I attacked holds: the node-id reader against row and ini
verbosity, xdist, conftest output and the three pytest versions; the routes
that never meet a group; a 15-layout corpus sample at both gates; and this
repository's own row.

## What this round was asked

This is the verifying round over round 2's fixes, `275cd1a0..d9ce4e1a`, and
the item's last round. The run is capped. The decisive property: `failing
on base too` may come only from a file run alone from the start, proven by
its own runner's node ids. Asked: enumerate every path to the word, attack
the node-id proof, attack the routes that never meet a group, re-run rounds
1–2's layouts and a corpus sample at the target and at a3aa139a, check that
the only remaining words are ones a3aa139a also gave, check rule 3 / the
`SKILL.md` bullet / the reasons / the changelog / `overview.md` against the
code, and check the seal.

## Enumeration: every path to `failing on base too` at 95422c35

Read at 95422c35. `ON_BASE` is assigned at one site,
`skills/verify/scripts/broad_gate.py:2347`, and only when `proof_refused`
returns None. A proof is queued at `:2368` only for a group of one file
whose report counts a failing test. Groups of one come from two places
only:

| Route to a run alone | Code | Meets a group | At a3aa139a |
|---|---|---|---|
| a candidate (the base's root tree lacks the path, e.g. every file of a `cd sub` row) | `:2282-2285`, `:2298` | never | run alone too |
| the one failing file the root carries | `:2299-2300` | never | a group of one |
| a file of a group of several | `:2360-2365` | — | judged by the group's run |

The third route now ends at `:2364` with `COMPANY` for every file and never
reaches `:2368`. So the decisive property comes down to `proof_refused`
(`:2052-2069`), which 🟡 1 is about.

## Findings — from execution

### 🟡 1 — a later runner that collects nothing at the base passes for the measuring runner

`skills/verify/scripts/broad_gate.py:2058-2069` (`proof_refused`).
**Regression against a3aa139a: yes.**

Round 2's fix made the proof require "the measuring runner's session" and
put that into code as "no `<path>: <count>` line, then every node id names
the file and their count equals the trailer". Nothing requires that at
least one node id be there. A session that collected zero tests prints no
listing line at all, so it satisfies every condition with zero node ids and
a trailer of `no tests collected`.

So round 2's 🟡 2 shape comes back whenever the visible runner collects
nothing at the base. The measuring runner's output still goes to a file.
Its run alone failed a test of another directory, and the proof accepts the
empty session of the runner after it.

Executed through the gate end to end (`run_gate`, so the branch's own
`FAILED` lines named the file), row
`python -m pytest -q -p no:cacheprovider tests/unit > unit.log; python -m pytest -q -p no:cacheprovider <second>`.
At the base, `tests/unit/test_u.py` holds a pre-existing failure. The branch
adds a failing test to `tests/integration/test_i.py`:

| Shape | `<second>` | At the base | a3aa139a | 95422c35 |
|---|---|---|---|---|
| swallow0 | `tests/integration` | `test_i.py` holds no test (a helper module) | `new?` (`NO_RUNNER`'s text) | **failing on base too** |
| swallow-desel | `-m slow tests/integration` | `test_i` is not marked `slow` | `new` | **failing on base too** |
| swallow (round 2's) | `tests/integration` | `test_i` passes | `new` | `MULTI_RUNNER` |

Both new shapes give the same words under pytest 8.1.2, 8.3.5 and 9.1.1.
The kept proof for swallow0 (`collected-at-base-1.txt`) holds the two
command lines, then one session: `collected 0 items` and `no tests
collected in 0.00s`, with no node id. The kept report of the run alone
(`suite-at-base-1-1.xml`) holds one failing testcase, `tests.unit.test_u`'s
`test_old`. The failure is another directory's, and the gate calls the
branch's new test inherited.

**Ordinary or contrived.** It needs the same row shape as round 2's 🟡 2,
a measuring runner whose output goes to a file. That is why it stays 🟡.
Given that row, it is the ordinary case rather than the rare one: a branch
that adds the first tests to a module, or marks a test into a selection the
base has none of. Rule 3 now says *"so where its output goes to a file and
the only session seen is a later runner's, the file reads `new?`"*, and the
changelog fragment repeats it. That sentence is false for both shapes.

**The fix.** The run alone failed the file. So, run the same way under
collection alone, the measuring runner either collected at least one test
of it (a node id) or failed to collect it (an `ERROR <path>` line, which
the proof already reads). A session with neither is not the measuring
runner's, and it reads `MULTI_RUNNER`. Executed in the clone with the fix
applied:

- swallow0, swallow-desel and swallow all read `MULTI_RUNNER`;
- the lone file, layout C and the normal shape are unchanged;
- a lone file the base cannot collect still proves under 8.1.2, 8.3.5 and
  9.1.1, plain and under `-n 2`, through its `ERROR tests/test_a.py` line;
- the narrow run passes, apart from
  `test_the_proof_needs_one_session_listing_the_file_alone[everything-deselected]`.
  That parameter pins the hole: a proof showing `no tests collected (2
  deselected)` is accepted. A measuring runner that just failed a test of
  the file selects that test again under the same arguments, so zero
  selected can only come from another runner. The fix flips that
  parameter to `MULTI_RUNNER`.

**What it does not close.** A silent measuring runner beside a later runner
that collects ≥1 test and prints node ids because its own command line sets
`verbosity_test_cases`. That needs the row to write that option itself.
Neither the ini nor `addopts` can do it, because `PYTEST_ADDOPTS` outranks
both (read from pytest's argument order, and executed for the ini's
`verbosity_test_cases` and an `addopts` of `-v`).

## Findings — from reading

### ⬜ 2 — the run's paperwork says no exception is left

`seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md`,
*Not done*: "After round 2's fix pass there is none" and "gives `failing on
base too` only where a3aa139a gave it too". `changelog.md` in the same
directory, under *Changed*: "a row whose measuring runner sends its output
to a file, so the only session the extra run shows is another runner's".
🟡 1 falsifies the first sentence at 95422c35. The changelog bullet and rule
3's sentence become true once 🟡 1's fix lands. This is a correction under
`seal/specs/`, so it is outside `Needs a fix`. The fenced text is below.

### ⬜ 3 — the `COMPANY` reason for a group whose run collected no test

`skills/verify/scripts/broad_gate.py:1953-1958`. A group of several files
that hold no test at the base (exit 5, a report with no testcase) reads
`COMPANY`. Its reason says the run "failed" and "does not say which of them
failed in it", but nothing failed in it. Executed (two-empty layout):
95422c35 gives `COMPANY` for both files, and a3aa139a gave `new?` for both.
So it is **not a regression**, and the word is not permissive. Rule 3's
"a base file with no test in it reads `new` too" is about a file run alone,
and this file does not run alone. A person who opens `suite-at-base-1.txt`
sees `no tests ran`, which the reason does not prepare them for. Giving
such a group `new` on exit 5 is safe (every path exists, so nothing
collected means the base has no test in any file). On exit 4 it is not,
because a `cd sub` path can be missing in one directory and present in
another. That makes it a design choice for the owner, not a fix this round
commissions.

## Round 2's verdicts, re-checked

- **🔴 1 (a count another file makes up): closed.** Executed: cancel,
  cancel2, outweigh and flaky2 read `COMPANY` for every file at 95422c35.
  At a3aa139a each gave `new` to the regressed `test_b` and `failing on base
  too` to the others. Read: the count comparison is gone (`:2360-2365`), and
  no file of a failed group reaches `:2368`.
- **🟡 2 (a measuring runner whose output never reaches the gate): closed
  for round 2's layout.** Executed: swallow reads `MULTI_RUNNER`. The
  class's remainder is 🟡 1.
- **🟡 3 (the `COMPANY` reason): closed.** Read: the reason no longer claims
  a count. ⬜ 3 is a narrower point on the new text.
- **⬜ 4 (routes that never meet a group): closed.** Read: rule 3 and the
  `compare_at_base` docstring name both routes. Executed: cdsub-cancel
  (both files candidates) and passing-sibling read `failing on base too` at
  both gates, as rule 3 says.
- **⬜ 5 (paperwork): closed as written.** ⬜ 2 is this round's remainder.

## What was checked and holds

- **The node-id reader across versions (executed).** Under
  `PYTEST_ADDOPTS` with the proof's options and `-o
  verbosity_test_cases=-1` after the file, pytest 8.1.2, 8.3.5 and 9.1.1
  each listed node ids for a file holding a plain test, two parametrized
  ids (`a b` and `c::d`) and a method in a class. That held under `-q`,
  `-v`, `-vv`, `-qq`, `-qqq`, an ini `verbosity_test_cases = 0`, an ini
  `addopts = -v -o verbosity_test_cases=0`, and `-n 2`. The proof read None
  in all 24. An option after the inserted one (a wrapper appending
  `-o verbosity_test_cases=-2`) turns the listing back to by-file and reads
  `MULTI_RUNNER`. That is stricter, never permissive.
- **Conftest and plugin lines shaped like node ids (executed).** A conftest
  printing `tests/test_a.py::…` at import (shown under `-s`) and a hook
  writing one to the terminal reporter (shown under `-q`) add ids. The
  count then exceeds the trailer, and the file reads `COLLECTED_BEYOND`.
  Such lines can only make the proof stricter, because they cannot remove a
  second trailer or a by-file line. Once 🟡 1's fix lands, they cannot
  stand in for a silent measuring runner either, unless a conftest prints
  exactly the failing file's path the trailer's number of times.
- **A non-pytest runner that echoes its arguments, and `set -x` (read).**
  The echoed line holds the path and `-o verbosity_test_cases=-1`, and no
  `::`. It matches neither `NODE_RE` nor `LISTED_RE`.
- **Two runners that both receive the `-o` (read).** Only a wrapper that
  forwards its arguments to two pytest processes does that. Both print a
  trailer, so the file reads `MULTI_RUNNER`. If one of them is silent, the
  visible one was handed the same file and arguments.
- **`--co` in the row (read).** A measuring runner with `--co` runs no test,
  so it never fails one and is never proven. Any other runner reads the
  variable and lists by file.
- **xdist (executed).** `-n 2` lists node ids from the controller in all
  three versions, a collection error included.
- **Windows-style paths (read).** pytest builds node ids with `/` on every
  platform, and the branch's `FAILED` line is a node id, so the path and
  the listing use one separator. A drive letter has one colon and never
  `::`. `run` reads in text mode, which turns `\r\n` into `\n`.
- **Routes that never meet a group (executed).** cdsub-cancel: test_b fails
  at the base only alone, and the row's own run would pass it. Both files
  are candidates and read `failing on base too` at 95422c35 and at
  a3aa139a. passing-sibling gives the same at both gates. Rule 3 names both
  routes, so the limit is named and is not a regression.
- **Rounds 1–2's layouts at both gates (executed, pytest 9.1.1):** A, A2, B,
  cancel, cancel2, outweigh and flaky2 read `COMPANY` for every file. C
  reads `MULTI_RUNNER`, swallow `MULTI_RUNNER`, lone `failing on base too`
  (a3aa139a the same), and normal `COMPANY` for both files (a3aa139a: on /
  `new`).
- **The corpus (executed, sampled).** 15 layouts of `REGRESSED` under each
  row they carry: P1, P3-sh, P7-both, P7-mixed, Q1, Q4, Q8, Qf-env, Qs2,
  R2b, R3, N1, N1-xdist, N1c and N7, 29 rows at both gates. Every target
  word equals the planted table's.
  - The only `failing on base too` at the target is N7 under the files-only
    row, and a3aa139a gives it too.
  - In the other direction, five files-only rows (P1, Q1, Q4, Qf-env, R2b)
    move from a3aa139a's `new?` to `new`. In each, the base passes the
    file.
  - The rest move to a form of `new?`.
- **Item 5, "the only `failing on base too` left is one a3aa139a also
  gave" (executed):** holds across every layout I built, except 🟡 1's two
  shapes.
- **Rule 3, `SKILL.md`, the reasons, the changelog and the overview against
  the code (read).** These match the code at 95422c35:
  - rule 3's group sentence and "Only a file that runs alone from the
    start";
  - the two routes;
  - the `COMPANY` and `MULTI_RUNNER` texts;
  - the *New?* bullet at `skills/verify/SKILL.md:509-511`;
  - the `compare_at_base` and `proof_refused` docstrings.

  The exceptions are rule 3's swallow sentence (🟡 1), the overview and the
  changelog bullet (⬜ 2), and the reason on the no-test route (⬜ 3).
- **The seal (read, plus this repository's row executed).** A green run
  never reaches `compare_at_base`. Its one call is at `:3507`, inside
  `if name == SUITE` and `if files`, and neither d3095fea nor 6b34713d has a
  hunk in `gate`. This repository's row (`uvx ruff check . && uvx ruff
  format --check . && bin/test -q`) went through 95422c35's
  `compare_at_base` in a second clone, over a base commit with ruff-clean
  failing files:
  - a lone pre-existing failing file reads `failing on base too`. Its proof
    holds the two ruff lines, one session at `-n auto`, the node id
    `tests/…::test_old` and `1 test collected`;
  - a group of two (one pre-existing, one passing at the base) reads
    `COMPANY` for both.
- **§2 audit (read).** `overview.md` labels the full suite, lint and
  typecheck `unverified` and names the sealer as the one who runs them. The
  round 2 record's `Broad gate` cell reads `not yet`, so the label is
  honest.

## Regression tests to plant

Destination: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, after
the case round 2 planted for its 🟡 2. In the clone at 95422c35, both
parameters are red on `assert 'failing on base too' == 'new? not mea…g
pytest once'` (2 failed). With the fix applied they are green. The
`everything-deselected` flip is in the same fenced fix. It is green at
95422c35 as it stands and red with the fix, which is the flip it records.

## Facts for the evidence ledger

- R2 (the proof): the measuring runner's session is shown by at least one
  node id or one `ERROR <path>` line naming the file, as well as by the
  absence of a by-file line. A session that collected nothing is another
  runner's. The row's R2 claim should gain that clause once the fix lands,
  re-stamping the `proof_refused` anchor.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A later runner that collects no test at the base (no test in its directory, or every test deselected) passes the proof for a silent measuring runner: zero node ids against a zero trailer, `failing on base too` where a3aa139a read `new?` / `new`; rule 3's swallow sentence is false for it | `skills/verify/scripts/broad_gate.py:2058` | open | executed: swallow0 and swallow-desel end to end under pytest 8.1.2, 8.3.5 and 9.1.1 at both gates; regression against a3aa139a; the fix executed with the narrow run; two cases red at 95422c35 |
| ⬜ 2 | `overview.md` says no exception to "no new permissive word" is left, and the changelog fragment's swallow bullet overstates the target | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md` | open | read; falsified by 🟡 1; a correction to the run's paperwork |
| ⬜ 3 | The `COMPANY` reason says the group's run "failed" where it collected no test (exit 5) | `skills/verify/scripts/broad_gate.py:1953` | open | executed: two-empty reads `COMPANY` at 95422c35 and `new?` at a3aa139a; not a regression, not permissive |
| 🟢 | round 2's blocking finding is closed — a count another file makes up no longer keeps the word | `skills/verify/scripts/broad_gate.py:2364` | confirmed | executed: cancel, cancel2, outweigh, flaky2 read `COMPANY` for every file; read: no file of a failed group reaches the proof |
| 🟢 | round 2's 🟡 2 is closed for its layout — swallow reads `MULTI_RUNNER` | `skills/verify/scripts/broad_gate.py:2058` | confirmed | executed at 95422c35; the class's remainder is 🟡 1 |
| 🟢 | round 2's 🟡 3 is closed — the `COMPANY` reason claims no count | `skills/verify/scripts/broad_gate.py:1953` | confirmed | read; ⬜ 3 is a narrower point |
| 🟢 | round 2's ⬜ 4 is closed — rule 3 names the two routes that never meet a group | `templates/config.md:333` | confirmed | read; executed: cdsub-cancel and passing-sibling as rule 3 says, equal at a3aa139a |
| 🟢 | round 2's ⬜ 5 is closed as written | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md` | confirmed | read; ⬜ 2 is this round's remainder |
| 🟢 | The node-id proof holds across pytest 8.1.2, 8.3.5, 9.1.1, row and ini verbosity, xdist and conftest output | `skills/verify/scripts/broad_gate.py:1886` | confirmed | executed: 24 proofs read None; extra node-id-shaped lines only make it stricter |
| 🟢 | The corpus sample leaks nothing, and the reverse-direction moves are to `new` where the base passes or to `new?` | `tests/test_the_seal_is_taken_once_by_the_sealer.py:5996` | confirmed | executed: 15 layouts, 29 rows at both gates |
| 🟢 | A green run is unchanged; this repository's row measures a lone failing file and reads `new?` for a group | `skills/verify/scripts/broad_gate.py:3507` | confirmed | read (no hunk in `gate`); executed (the row through `compare_at_base` in a clone) |

## Executed probes

| What was run | Result |
|---|---|
| The narrow module run (the five modules the prompt names, plus a probe module holding the two cases below) in the clone at 95422c35 | 730 passed, 1 skipped, 2 failed — the two probe cases, each on `failing on base too` |
| The same with 🟡 1's fix applied in the clone | 731 passed, 1 skipped, 1 failed — the `everything-deselected` parameter, which the fix flips |
| `bin/evidence-check --strict .` | not run by this round; the orchestrator reports exit 0 at the fix head |
| Rounds 1–2's layouts (A, A2, B, C, cancel, cancel2, outweigh, flaky2, swallow) and normal / lone through the gate of a3aa139a and 95422c35, pytest 9.1.1 | 95422c35: every group file `COMPANY`; C and swallow `MULTI_RUNNER`; lone on. a3aa139a: on / `new` splits, C and swallow `new` |
| swallow0 and swallow-desel through both gates under pytest 8.1.2, 8.3.5 and 9.1.1 | a3aa139a `new?` and `new`; 95422c35 `failing on base too` in all six |
| cdsub-cancel, passing-sibling, two-empty through both gates | cdsub-cancel and passing-sibling: on at both; two-empty: a3aa139a `new?`, 95422c35 `COMPANY` |
| The proof reader on real output: 8 verbosity and ini variants × 3 pytest versions, a collection error × 3 versions × plain and `-n 2`, two conftest variants | 24 + 6 proven; conftest lines → `COLLECTED_BEYOND` |
| Corpus sample: 15 `REGRESSED` layouts, each under the rows it carries, at both gates | 29 rows; target words equal the table; the only target on is N7-files, also on at a3aa139a |
| This repository's row through 95422c35's `compare_at_base` in a second clone | lone: `failing on base too`, proof one session with the node id; group of two: `COMPANY` ×2 |
| Broad gate: the full suite, lint and typecheck after the rounds | not yet — not run by this round; the sealer's, once the rounds settle |

## Paste-ready fixes

### 🟡 1 — the proof needs the measuring runner to show the file

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ def proof_refused(text, path):  (docstring)
       - **the measuring runner's session**: no `<path>: <count>` line, which
         only a runner that took its listing from the variable prints, so the
-        one session seen is the one handed `OWN_LISTING` (#789 round 2);
-        otherwise `MULTI_RUNNER`;
+        one session seen is the one handed `OWN_LISTING` (#789 round 2), and
+        at least one node id or `ERROR` line naming `path`: the run alone
+        failed the file, so its runner collected a test of it or could not
+        collect it, and a session showing neither -- one that collected
+        nothing -- is another runner's (#789 round 3); otherwise
+        `MULTI_RUNNER`;
@@ def proof_refused(text, path):  (body, after the error checks)
     errors = int(errors or 0)
     if errors > 1 or (errors == 1 and not named):
         return COLLECTED_BEYOND
+    # The run alone failed the file, so the measuring runner collected a
+    # test of it or failed to collect it. A session showing neither is
+    # another runner's, the measuring one having printed nothing the gate
+    # sees (#789 round 3).
+    if not ids and not named:
+        return MULTI_RUNNER
     return None
```

```diff
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ the proof reader's parameters (test_the_proof_needs_one_session_listing_the_file_alone)
+    # #789 round 3's 🟡 1: a measuring runner that just failed a test of
+    # the file selects it again under the same arguments, so a session
+    # that selected nothing is another runner's.
     pytest.param(
         "collecting ... collected 2 items / 2 deselected / 0 selected\n\n"
         "================== no tests collected (2 deselected) in 0.01s "
         "==================\n",
         "tests/test_two.py",
-        None,
+        "MULTI_RUNNER",
         id="everything-deselected",
     ),
@@ after test_a_measuring_runner_whose_output_the_gate_never_sees_earns_no_word
+@pytest.mark.parametrize(
+    "second, at_base, on_feature",
+    [
+        pytest.param(
+            "tests/integration",
+            {"tests/integration/test_i.py": "HELPER = 1\n"},
+            {
+                "tests/integration/test_i.py": "HELPER = 1\n\n\n"
+                "def test_i():\n    assert False\n"
+            },
+            id="the-next-runner-collects-no-test-at-the-base",
+        ),
+        pytest.param(
+            "-m slow tests/integration",
+            {
+                "pytest.ini": "[pytest]\nmarkers =\n    slow: a slow test\n",
+                "tests/integration/test_i.py": "def test_i():\n    assert True\n",
+            },
+            {
+                "tests/integration/test_i.py": "import pytest\n\n\n"
+                "@pytest.mark.slow\ndef test_i():\n    assert False\n"
+            },
+            id="the-next-runner-deselects-every-test-at-the-base",
+        ),
+    ],
+)
+def test_a_silent_measuring_runner_beside_an_empty_session_earns_no_word(
+    tmp_path, second, at_base, on_feature
+):
+    """#789 round 3's 🟡 1. The runner that measures sends its output to a
+    file, and the runner after it collects nothing at the base, so it
+    prints no line listed by file and no node id: zero ids against a
+    trailer of zero is not the measuring runner's session."""
+    row = f"{FILES_ROW} tests/unit > unit.log; {FILES_ROW} {second}"
+    repo = base_then_feature(
+        tmp_path / "repo",
+        row,
+        {"tests/unit/test_u.py": PRE_EXISTING, **at_base},
+        on_feature,
+    )
+    out = run_gate(repo, keep=tmp_path / "out")
+    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
+    gate = gate_module()
+    path = "tests/integration/test_i.py"
+    assert verdict_of(out.stdout, path) == gate.MULTI_RUNNER.format(n=1), out.stdout
```

```text
templates/config.md, rule 3 — replace:
  so where its output goes to a file and the only session seen is a later runner's, the file reads `new?`.
With:
  so where its output goes to a file and the only session seen is a later runner's, one that collected nothing at the base included, the file reads `new?`.

tests/test_the_seal_is_taken_once_by_the_sealer.py, the rule 3 sentences — replace the pinned
  "goes to a file and the only session seen is a later runner's, the file "
  "reads `new?`."
With:
  "goes to a file and the only session seen is a later runner's, one that "
  "collected nothing at the base included, the file reads `new?`."
```

### ⬜ 2 — the run's paperwork (a correction)

```text
overview.md, Not done — replace:
  After round 2's fix pass there is none.
With:
  After round 2's fix pass round 3 found one more, a regression against a3aa139a: a silent measuring runner beside a later runner that collects nothing at the base (no test in its directory, or every test deselected) passed the proof with zero node ids. <closed at <fix commit> by requiring a node id or an ERROR line naming the file | named in rule 3 as a limit>.

overview.md, the table row "The session the proof reads" — append to Chosen:
  , and at least one node id or `ERROR` line naming the file (round 3)

changelog.md, Changed — replace:
  - a row whose measuring runner sends its output to a file, so the only
    session the extra run shows is another runner's.
With:
  - a row whose measuring runner sends its output to a file, so the only
    session the extra run shows is another runner's, one that collected
    nothing at the base included.
```

Needs a fix: yes — 🟡 1 (a later runner that collects nothing at the base passes the proof for a silent measuring runner; a regression against a3aa139a)
Loses a record or crashes: no

## Proof block

Opened and read at 95422c35:
`skills/verify/scripts/broad_gate.py` (lines 1840-2410, 3490-3530, and the
`ON_BASE` and `compare_at_base` sites), a3aa139a's `compare_at_base` (the
body), `skills/verify/SKILL.md` (488-520), `templates/config.md` rule 3
(the diff over the fix range), `bin/test`, `.github/scripts/run_tests.py`
(`main`), `tests/test_the_seal_is_taken_once_by_the_sealer.py` (690-960,
3962-4030, 4189-4211, 5393-5600, 5996-6260), and this work item's
`overview.md`, `changelog.md`, `rounds/round-2.md`, `rounds/round-2-report.md`
(1-380), `rounds/round-1-report.md` (75-175), and the R2 row of its ledger
fragment. Every probe ran in a clone under the scratchpad and was removed
with it.
