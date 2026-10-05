# Round 1 report — 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict

Target SHA: 225af880 · Base: `release/v0.18.3` at a3aa139a · PR #804 (draft)
Ran by: specseal:warden on claude-opus-5-5

## Summary

The core of the frame holds. The base comparison reads its words off a JUnit
report that only the gate-addressed pytest writes. The text readers are gone
from the code, and every 0.18.2 end-to-end word assertion still passes. The
inner-run members 2 and 3 are closed by construction, and the module's own
cases show it.

The acceptance clause is what fails: "no shape in the class gives
`failing on base too` to a file the base did not fail where the row runs it".
This round built three shapes, each run end to end through the gate, where
225af880 gives that word to a file the base passes or holds no test in.
a3aa139a gave `new` in all three, so this change introduced them. They have two causes:

- **The reader places a test by matching names, and a name can match a file
  it is not.** The report's dotted `classname` cannot tell a module from a
  package of the same name (`tests.test_api.test_users` is placed on
  `tests/test_api.py` at offset 0). An offset is chosen per test rather
  than per run, so a same-named module deeper in the tree is placed on the
  appended file too. That second shape is the overview's *Not done*, and it is
  real. The offset-0 shape is not named anywhere. 🟡 1.
- **A runner that does not take the gate's appended arguments is never
  counted.** The walk passes over it to a later runner and measures there,
  in that runner's directory. The collection pass only looks after the
  settled prefix, so the row reads as having one runner. 🟡 2.

Two smaller findings sit beside these. The collection pass runs every part
after the runner for real at the base, and rule 3 calls that a "collection
run" (🟡 3). The `NOTHING_TOGETHER` reason and one rule-3 sentence state a
fact that is false for a module that exists at the base with no test in it
(🟡 4).

A tested fix for 🟡 1 and for the first half of 🟡 2 is under
*Paste-ready fixes*. With it applied in the review clone, the two gate
modules pass: 472 passed, 1 skipped. Each of P1, P2 and P3 (`sh -c`) goes from
`failing on base too` to `new?`. Two shapes stay open and need naming in
rule 3 rather than a fix this round: a later runner that drops its arguments
(P7), and an earlier one given `-p no:junitxml`.

## What the account claimed, and what was checked

| Claim (where) | What the code does |
|---|---|
| Only the process handed the gate's arguments writes the report (spec §intro, `compare_at_base` docstring) | True for every inner-run shape the module covers, and the end-to-end cases pass. One shape was read and not run: an inner `pytest.main()` called with no arguments reads `sys.argv` and writes to the same path. The outer process writes last at its own session end, so its report wins unless it dies first |
| The option overrides a `--junitxml` in the row (Scope 1) | Executed: P6 (`… tests --junitxml=own.xml`) reads `failing on base too` for a file the base fails |
| A part that drops its arguments reads `new?` (Scope 2, rule 3, changelog) | True only where no later part runs pytest. P3 shows the opposite (🟡 2) |
| A file reads `failing on base too` only where the report places a failing test on it and no other (rule 3, changelog) | `report_words` places by a name match, not by the file. P1 and P2 are counterexamples (🟡 1) |
| A row with more than one runner gives no measured word (Scope 4) | Only runners at prefixes after the settled one, and only those that take an appended argument, are counted (🟡 2) |
| The collection pass costs "one collection run per prefix after the runner" (rule 3, changelog) | Every non-pytest part in those prefixes runs as written, once per prefix that holds it (🟡 3, P5) |
| This repository's row pays no collection pass (S11) | Read and confirmed. `bin/test -q` is the row's last part, `.github/scripts/run_tests.py` line 644 passes its arguments to pytest unchanged, and no prefix follows the runner. With 🟡 2's fix applied, two prefixes before it run once more (two `uvx ruff` runs at the base, only on a failing gate) |
| The seal changes nothing for a green run (prompt) | Read: the call site at `skills/verify/scripts/broad_gate.py:3429` calls `compare_at_base` only when the suite arm failed and its output names failing files. On a failing run, only where the words come from changes |

The divergences in `overview.md`, each judged on its own grounds:

- **A file the report names no test of reads `UNPLACED`.** Accepted. A file
  can read `new` only where its own tests appear in the report, which is
  the safe direction. S5's words hold.
- **One file named at two offsets reads `UNPLACED`.** Accepted. 🟡 1's fix
  keeps the unit row green.
- **The reader's fifth argument, `alone`.** Accepted on S5's grounds. A
  one-file group that counts no test could be measured as `new`, but
  0.18.2 pinned it as `new?`, and that is the conservative direction. Its
  reason text is 🟡 4.
- **S6 built on a passing base.** Accepted. With the base passing, both rows
  read `new` at a3aa139a, which is the red the case needs.
- **Three assertions moved from `NO_RUNNER` to `NOTHING_TOGETHER`.** These
  are in `test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd`
  and in two places of the warnings-only case. Accepted. Spec Scope 5
  orders this move, and the word stays `new?`.

Not opened this round: `plan.md`, `questions.md`, `phases/`, `routing.md`,
`survivors.md` and the ledger fragment. The phase records' claims were not
carried. Each claim above was checked against the code instead.

## Findings from execution

### 🟡 1 — a failing test is placed on a file by a name that can belong to another file

`skills/verify/scripts/broad_gate.py:1932-1959` (`report_cases`, `offsets`)
and `:1995-2023` (`report_words`). Each test's address is its dotted
`classname` split at the dots, and `offsets` accepts it wherever the appended
path's components appear in it. Two shapes follow, both executed through the
gate with `SUITE_ROW` (a row that collects all of `tests`):

- **P1, offset 0, not named anywhere.** At the base, `tests/test_api.py`
  holds no test and `tests/test_api/test_users.py` fails. The branch adds a
  failing test to `tests/test_api.py` and fixes `test_users`. The report's NAME NOT IN TREE
  `tests.test_api.test_users` is placed on `tests/test_api.py` at offset 0,
  so the result is `failing on base too`. a3aa139a read `new`, from the
  exact `FAILED tests/test_api/test_users.py::` path.
- **P2, the overview's *Not done*.** At the base, `tests/test_two.py` holds
  no test and `tests/x/tests/test_two.py` (a package) fails. The address
  `tests.x.tests.test_two` is placed on `tests/test_two.py` at offset 2, so
  the result is `failing on base too`. a3aa139a read `new`. The shape is
  real.

**Why it matters.** `failing on base too` is the one word that lets a red
suite through without blocking. This work exists to stop that word being
earned by something other than the file. The overview says closing the
nonzero-offset shape "needs the rootdir off a report". That is not the only
way. A run has one offset, so a placement at a positive offset has to be
shared by every test the report names. P2's `tests.test_one` does not start
with `tests.x`, which rules that placement out. The offset-0 shape needs the
file rather than the class path. pytest writes it when given
`-o junit_family=xunit1` (`_pytest/junitxml.py`, `record_testreport`, NAME NOT IN TREE
`"file": testreport.location[0]`), and the option changes nothing about the
run. NAME NOT IN TREE

**What stays open after the fix.** A negative offset (pytest's rootdir below
the directory the row runs in) still accepts a same-named module a directory
up. It is constructed, not run, and needs naming in rule 3.

So this is a defect to fix, not a limit to state: the class is "names that
cannot be told apart", and this reader added a member of it.

### 🟡 2 — a runner that does not take the gate's arguments is passed over, and the next runner measures the file in the wrong directory

`skills/verify/scripts/broad_gate.py:2277-2316` (`compare_at_base`, the walk
and the collection pass).

- **P3, row `sh -c '{SUITE_ROW}' && cd sub && {SUITE_ROW}`.** The root's
  `tests/test_two.py` passes at the base, and `sub/tests/test_two.py` fails
  there. The branch fails the root file. Prefix 1 drops the files and writes
  no report. Prefix 3 runs the `sub` runner with `tests/test_two.py`
  appended, which is `sub`'s failing file, so the root file reads
  `failing on base too`. The collection pass starts after prefix 3 and finds
  nothing. a3aa139a read `new` (from the first runner's summary).
- **P3, the same with `{SUITE_ROW} -p no:junitxml` as the first part.** Same
  word, same mechanism. That runner refuses the option only when it is
  handed one.
- **P7, a later runner, row `{SUITE_ROW} && sh -c 'cd sub && {SUITE_ROW}'`,
  in #761's p1b layout.** The collection pass appends `--junitxml` to the
  `sh -c`, which drops it, so the row reads as one runner. `tests/test_y.py`,
  which the branch fails only in `sub`, reads `failing on base too` from the
  root's file. a3aa139a gave the same word (it is the original p1b), so
  this one is not a regression. It is still a member-1 instance that rule 3
  now says reads `new?`.

**Why it matters.** Scope 2 and Scope 4 are the two promises rule 3 and the
changelog now make to a row's author, and both are false for these rows. The
first part of the fix is cheap, because a runner that drops its arguments
still reads `PYTEST_ADDOPTS`. For the prefixes before the settled one, the
collection pass can carry `--junitxml` there and append nothing. With that
applied, P3 (`sh -c`) reads `MULTI_RUNNER` naming parts 3 and 1. The
`-p no:junitxml` variant and P7 stay open: the first refuses the option from
either source, and in the second the measured runner would also write a path
carried in `PYTEST_ADDOPTS`. Both need naming in rule 3.

### 🟡 3 — the collection pass runs every non-pytest part after the runner, for real, at the base

`compare_at_base` (`:2262-2275`) runs each prefix after the runner with
`--collect-only` in `PYTEST_ADDOPTS`. Only pytest honours that, so every other
part of the prefix runs as written. P5 shows it with the row
`{SUITE_ROW} && python -c "<append A>" && python -c "<append B>"` and a
failing base test. The branch's own run never reached A or B, because the
suite failed and `&&` stopped. At the base the gate ran A twice and B once.
a3aa139a ran neither.

**Why it matters.** Rule 3 is where a row's author learns what the
comparison costs, and it says "one collection run per prefix after the
runner". A part after the runner that ignores extra arguments (a script, a
coverage upload, a docs build) now runs at the base. It runs once for each
prefix that holds it, and only on a failing gate, where the row itself
skipped it. Writes inside the scratch worktree go away when the worktree is
removed. Anything that writes outside it, or over the network, does not.

### 🟡 4 — the `NOTHING_TOGETHER` reason calls a file missing that is present and holds no test

`skills/verify/scripts/broad_gate.py:1886-1890` and `templates/config.md`
rule 3. P4 used a row that collects only the appended files, with an
existing `tests/test_two.py` that holds no test at the base and a failing
test added on the branch. The result was `NOTHING_TOGETHER`, which says "a
file the run was handed is missing where the row runs pytest". The file is
not missing. With `SUITE_ROW` the same base reads `UNPLACED`, where a3aa139a
read `new`.

Both words are `new?`, the conservative direction. What is wrong is the
sentence a person acts on: it sends them looking for a missing file. Rule 3's
"so a base file with no test in it reads `new` too" now holds only for a
file the root lacks.

## Findings from reading

- **Report shapes enumerated** (read, unless marked executed):
  - The naming comes from `mangle_test_address`. It is the same for
    parametrized and class-nested ids and for doctest items (`docs.x.txt`).
    `--import-mode=importlib` does not change node ids.
  - Under xdist the controller writes the report. This was executed by the
    module's `UNDER` cases.
  - A collection error carries `name` with an empty `classname`. Under
    `--junit-prefix` that `classname` is the prefix, so the error is
    unplaced. That reads `new?`, which is safe.
  - `-p no:junitxml` is a usage error (executed, S6). `--junitxml` in the row
    is overridden (executed, P6). In `addopts` or `PYTEST_ADDOPTS` it comes
    before the command line, so the gate's value wins.
  - A runner that rejects the option reads `NO_RUNNER`.
  - pytest 7 and 8 write the `testsuites` root, and a bare `testsuite` is
    accepted. This was not run on 7 or 8.
  - On Windows, pytest's node ids use `/`, and 🟡 1's fix normalises the
    `file` separator. Not run.
- **Output redirected to a file with `-x` under xdist.** The stop is read
  only from the text, so it is lost when the output goes to a file. A file
  partly run before another worker's failure stopped the session can then
  read `new`. That is the strict direction, constructed and not run, and
  left as a note.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A failing test is placed on an appended file by a dotted-name match that also fits another module: a package of the same name at offset 0 (P1), or a same-named module deeper in the tree (P2, the overview's *Not done*). Either gives `failing on base too` to a file with no test at the base, where a3aa139a gave `new` | `skills/verify/scripts/broad_gate.py:1932-2023` | open | Executed P1 and P2 at 225af880 (`failing on base too`) and a3aa139a (`new`). A fix closing both was run in the review clone: two gate modules 472 passed, 1 skipped |
| 🟡 2 | A runner that drops or refuses the gate's appended arguments is passed over. A runner before the settled prefix sends the file to a later runner's directory (P3, a regression from `new`), and one after it is not counted by the collection pass (P7, the original p1b). Both give `failing on base too`, against Scope 2, Scope 4 and rule 3 | `skills/verify/scripts/broad_gate.py:2277-2316`, `templates/config.md` rule 3 | open | Executed P3 for both variants and P7. The fix (`PYTEST_ADDOPTS` for prefixes before the settled one) turns P3 `sh -c` into `MULTI_RUNNER`. The `-p no:junitxml` variant and P7 stay open and are to be named |
| 🟡 3 | The collection pass runs every non-pytest part after the runner as written, at the base, once per prefix that holds it, including parts the branch's run never reached. Rule 3 and the changelog call it "one collection run per prefix" | `skills/verify/scripts/broad_gate.py:2262-2316`, `templates/config.md` rule 3, `changelog.md` | open | Executed P5: markers `AA` and `B` at 225af880, empty at a3aa139a |
| 🟡 4 | `NOTHING_TOGETHER` says a handed file is missing when it exists with no test in it, and rule 3's "a base file with no test in it reads `new` too" no longer holds for a file the root carries | `skills/verify/scripts/broad_gate.py:1886-1890`, `templates/config.md` rule 3 | open | Executed P4: `NOTHING_TOGETHER` (files-only row), `UNPLACED` (`SUITE_ROW`). a3aa139a gave `NO_RUNNER` and `new` |
| 🟢 | The inner-run members 2 and 3 (stderr under `-s`, `-rN` and `-rP`, `-qq`) are read off the report, and the 0.18.2 word assertions are kept | `tests/test_the_seal_is_taken_once_by_the_sealer.py` S1–S5 cases | confirmed | Two-module run in the clone (472 passed with the fix, which changes no case's words). Orchestrator's run at the target: 703 passed |
| 🟢 | The overview's divergences: `UNPLACED` for an unnamed file, two offsets, `alone`, S6's passing base, three `NO_RUNNER` assertions moved to `NOTHING_TOGETHER` | `overview.md` §*Where spec and implementation diverged* | confirmed | Each is judged in *What the account claimed*; Scope 5 orders the move |
| 🟢 | This repository's row: no collection pass, and the runner receives the report option | `seal/config.md` row, `.github/scripts/run_tests.py:644` | confirmed | Read. The runner is the last part, and arguments pass through unchanged |
| ❓ | Report shapes on pytest 7 and 8, and on Windows (`cmd.exe` quoting of the option, and `file` separators once 🟡 1's fix lands) | `skills/verify/scripts/broad_gate.py:1906-1938` | ❓ out of verified scope | Read only. CI's three-platform test job answers Windows. Nothing in this repository runs pytest 7 or 8, so the repository owner decides whether it matters |

## Executed probes

| What was run | Result |
|---|---|
| P1–P6 end to end through the gate at 225af880 (one probe file in the review clone, built on the module's `base_then_feature` and `run_gate`) | P1 `failing on base too`, P2 `failing on base too`, P3 `sh -c` and `-p no:junitxml` both `failing on base too`, P5 markers `AA`/`B`, P4 `NOTHING_TOGETHER` / `UNPLACED`, P6 `failing on base too` (right) |
| The same probes with a3aa139a's `broad_gate.py` in place | P1 `new`, P2 `new`, P3 `new` and `new`, P5 markers empty, P4 `NO_RUNNER` / `new`, P6 `failing on base too` |
| P7 (later runner that drops its arguments) at the fix state; the fix does not touch prefixes after the runner | `failing on base too` |
| 🟡 1 and 🟡 2's fix applied in the clone, the probes rerun | P1 `UNPLACED`, P2 `UNPLACED`, P3 `sh -c` `MULTI_RUNNER` (parts 3 and 1), P3 `-p no:junitxml` still `failing on base too` |
| `bin/test -q tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_gate_hands_cmd_a_path_it_can_run.py` with the fix applied | 472 passed, 1 skipped (exit 0). The shell-site case still counts one `run` call |
| The broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

```
words per probe            225af880             a3aa139a         with the fix
P1 offset-0 package        failing on base too  new              UNPLACED
P2 nonzero offset          failing on base too  new              UNPLACED
P3 sh -c then runner       failing on base too  new              MULTI_RUNNER
P3 -p no:junitxml then run failing on base too  new              failing on base too
P7 runner then sh -c       failing on base too  (p1b, same)      failing on base too
P5 parts after the runner  ran A twice, B once  ran neither      ran A twice, B once
P4 empty module, files row NOTHING_TOGETHER     NO_RUNNER        NOTHING_TOGETHER
P4 empty module, SUITE_ROW UNPLACED             new              UNPLACED
P6 row's own --junitxml    failing on base too  failing on base too
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Counting a later runner that drops its arguments (P7) and an earlier one given `-p no:junitxml`. Per-directory report paths (pytest expands `$PWD` in the `--junitxml` path) are one direction, and they would not reach `cmd.exe` | a new issue, if the owner wants these rows measured rather than named in rule 3 | the repository owner |
| A negative offset still accepts a same-named module a directory up (🟡 1's fix closes the positive offsets only) | rule 3's named limits, by 🟡 1's fix | the smith in the fix pass |

## Paste-ready fixes

### 🟡 1 — place a test by its file, at one offset per run

Tested in the review clone together with 🟡 2's block; the existing unit
rows (`two-files`, `two-offsets`) keep their words.

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ JUNIT_REPORT
 JUNIT_REPORT = "--junitxml={path}"
+# The report family that writes each test's file as a path (`report_cases`).
+JUNIT_FAMILY = "-o junit_family=xunit1"
@@ def report_cases(text):
     cases = []
     for case in root.iter("testcase"):
-        where = case.get("classname") or case.get("name") or ""
         failed = case.find("failure") is not None or case.find("error") is not None
-        cases.append((tuple(where.split(".")), failed))
+        # `-o junit_family=xunit1` (JUNIT_FAMILY) writes the test's file as
+        # a path, which no class or module name can be mistaken for.
+        where = (case.get("file") or "").replace("\\", "/")
+        if where:
+            cases.append((tuple(where.split("/")), failed, True))
+            continue
+        where = case.get("classname") or case.get("name") or ""
+        cases.append((tuple(where.split(".")), failed, False))
     return cases
@@
-def offsets(path, address):
+def offsets(path, address, exact=False):
@@
     found = set()
     n = len(path)
+    if exact:
+        if len(address) >= n and address[len(address) - n :] == path:
+            found.add(len(address) - n)
+        for shift in range(1, n):
+            if address == path[shift:]:
+                found.add(-shift)
+        return found
     for shift in range(len(address) - n + 1):
@@ def report_words(text, files, code, stopped, alone=False):
-    paths = {f: dotted(f) for f in files}
+    paths = {f: (tuple(f.split("/")), dotted(f)) for f in files}
     named = {f: set() for f in files}
     places = []
-    for address, failed in cases:
+    unshared = set()
+
+    # One run has one rootdir and one directory pytest runs in, so a
+    # placement at a positive offset says every test the report names sits
+    # under the same leading directories. Where one does not, the test may
+    # be another file the row collected, and the file reads `UNPLACED`.
+    def shared(address, shift):
+        return all(other[:shift] == address[:shift] for other, _, _ in cases)
+
+    for address, failed, exact in cases:
         hit = set()
         for f in files:
-            found = offsets(paths[f], address)
+            found = offsets(paths[f][0 if exact else 1], address, exact)
+            if any(shift > 0 and not shared(address, shift) for shift in found):
+                unshared.add(f)
             if found:
@@
     for f in files:
-        if len(named[f]) > 1:
+        if len(named[f]) > 1 or f in unshared:
             words[f] = UNPLACED
@@ def compare_at_base(root, base, command, files, keep):
-                    f"{prefix} {appended}{quote(JUNIT_REPORT.format(path=report))}",
+                    f"{prefix} {appended}{quote(JUNIT_REPORT.format(path=report))} {JUNIT_FAMILY}",
```

The rule-3 sentence that names what stays open, added after "…and a file
whose tests the report names with none failing reads `new`.":

```
A test is placed on a file by the path pytest's report gives it (the gate adds `-o junit_family=xunit1`), at one offset between pytest's rootdir and the directory the row runs pytest in; a file named at two offsets, or at one not every test in the report shares, reads `new?`. Where pytest's rootdir sits below that directory, a same-named file a directory up that the row also collects can still be placed on a file the base holds no test in.
```

The `report_words` docstring's first bullet gains "or at an offset not every
test in the report shares", and the changelog's "places a failing or erroring
test on that file and no other" gains "by the file's path, at the run's one
offset".

### 🟡 2 — count a runner before the settled prefix through `PYTEST_ADDOPTS`, and name what stays uncounted

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ def compare_at_base(root, base, command, files, keep):
             for k, prefix in enumerate(prefixes, 1):
-                if k <= first:
+                if k == first or (not collecting and k <= first):
                     continue
@@
                 appended = "" if collecting else " ".join(quote(f) for f in group) + " "
-                tried = run(
-                    name,
-                    f"{prefix} {appended}{quote(JUNIT_REPORT.format(path=report))}",
-                    scratch,
-                    keep,
-                    shell=True,
-                    env=collecting_env if collecting else None,
-                )
+                line = f"{prefix} {appended}{quote(JUNIT_REPORT.format(path=report))} {JUNIT_FAMILY}"
+                env = collecting_env if collecting else None
+                if collecting and k < first:
+                    # A runner before the one that settled the walk is one
+                    # that dropped or refused what was appended to it. It
+                    # still reads PYTEST_ADDOPTS, so the report's path goes
+                    # there, and nothing is appended.
+                    line = prefix
+                    env = dict(collecting_env)
+                    env["PYTEST_ADDOPTS"] += " " + shlex.quote(
+                        JUNIT_REPORT.format(path=report)
+                    )
+                tried = run(name, line, scratch, keep, shell=True, env=env)
```

Rule 3: replace "A part that does not hand the appended arguments on to
pytest — … — writes no report where the gate asked for one, so each file
reads `new?` where it used to read `new` for a file it never ran." with:

```
A part that does not hand the appended arguments on to pytest — a `sh -c '…'`, a `make` target, a wrapper that drops its arguments or refuses an option it does not know, a runner given `-p no:junitxml` — writes no report where the gate asked for one, so where no other part of the row runs pytest each file reads `new?`. Where another part does, the collection pass counts a runner before the one that wrote the report through `PYTEST_ADDOPTS`, but not one given `-p no:junitxml`, and not a runner after it that drops its arguments; such a row is read as one with a single runner, and a file can read `new` or `failing on base too` from the other runner's directory. Write such a part so it passes its arguments on, `--junitxml` included.
```

The changelog's second bullet takes the same qualification ("where no other
part of the row runs pytest").

### 🟡 3 — say what the collection pass runs

Rule 3: replace "To count the runners, each prefix after the one whose report
settled the walk runs once more … so a row whose runner is its last part never
pays it." with (it already folds in 🟡 2's prefixes before the runner):

```
To count the runners, every other prefix runs once more at the base with ` --collect-only` added to `PYTEST_ADDOPTS`, kept as `runners-at-base-<j>.txt`: a prefix after the one whose report settled the walk with only its own `--junitxml` appended, and a prefix before it with nothing appended and its `--junitxml` carried in `PYTEST_ADDOPTS`. Only pytest honours `--collect-only`: every other part of those prefixes runs as written at the base, once for each prefix that holds it, and that includes a part after the runner that the branch's own run never reached because its suite failed first. This happens once per comparison and only on a failing gate; a row whose only part runs pytest pays nothing, and a part after the runner that writes outside the repository writes there at the base too.
```

The changelog's "That is one collection run per later part" becomes "Each part
of those prefixes that is not pytest runs as written at the base, once for
each prefix that holds it".

### 🟡 4 — the reason states both causes

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@
 NOTHING_TOGETHER = (
     f"{NOT_MEASURED}: pytest's report at the base counts no test, so a file "
-    "the run was handed is missing where the row runs pytest, and a run that "
-    "is not of one file alone does not say which"
+    "the run was handed is missing where the row runs pytest or holds no test "
+    "there, and a run that is not of one new file alone does not say which"
 )
```

The same text replaces the pin in
`test_the_unmeasured_word_says_so_and_every_reader_is_told_it`. In rule 3,
"so a base file with no test in it reads `new` too: the base cannot fail a
test it does not have" becomes:

```
so such a file the base holds with no test in it reads `new` too: the base cannot fail a test it does not have. A file the root carries runs with the others, and one with no test in it at the base reads `new?`
```

## Regression tests to plant

Destination: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside
the S6–S8 cases. Each was red at 225af880 (`failing on base too`) and green
with the fix above, run in the review clone. `-p no:junitxml` before a runner
and P7 are not planted as passing cases; they are the named limits.

```python
def test_a_package_named_like_the_file_is_not_placed_on_it(tmp_path):
    """#789 round 1's 🟡 1 (P1). The report's `tests.test_api.test_users`
    used to be placed on `tests/test_api.py`, which holds no test at the
    base, and gave it `failing on base too`."""
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW,
        {
            "tests/test_api.py": "X = 1\n",
            "tests/test_api/test_users.py": FAILING_TEST.replace("test_two", "test_u"),
        },
        {
            "tests/test_api.py": FAILING_TWO,
            "tests/test_api/test_users.py": PASSING_TEST.replace("test_one", "test_u"),
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_api.py") == gate_module().UNPLACED, out.stdout


def test_a_same_named_module_deeper_in_the_tree_is_not_placed_on_the_file(tmp_path):
    """#789 round 1's 🟡 1 (P2, the overview's Not done). `tests.x.tests.test_two`
    matched `tests/test_two.py` at offset 2, which `tests.test_one` does not
    share."""
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW,
        {
            "tests/test_two.py": "X = 1\n",
            "tests/x/__init__.py": "",
            "tests/x/tests/__init__.py": "",
            "tests/x/tests/test_two.py": FAILING_TEST.replace("test_two", "test_deep"),
        },
        {
            "tests/test_two.py": FAILING_TWO,
            "tests/x/tests/test_two.py": PASSING_TEST.replace("test_one", "test_deep"),
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().UNPLACED, out.stdout


def test_a_runner_that_drops_its_arguments_before_another_is_counted(tmp_path):
    """#789 round 1's 🟡 2 (P3). The `sh -c` runner wrote no report, the walk
    went on to the runner in `sub`, and the root's file read `failing on base
    too` from `sub`'s same-named file."""
    posix_row_shell_or_skip()
    repo = base_then_feature(
        tmp_path / "repo",
        f"sh -c '{SUITE_ROW}' && cd sub && {SUITE_ROW}",
        {"tests/test_two.py": PASSING_TWO, "sub/tests/test_two.py": FAILING_TEST},
        {"tests/test_two.py": FAILING_TWO, "sub/tests/test_two.py": PASSING_TWO},
    )
    keep = tmp_path / "out"
    out = run_gate(repo, keep=keep)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    expected = gate_module().MULTI_RUNNER.format(first=3, second=1)
    assert verdict_of(out.stdout, "tests/test_two.py") == expected, out.stdout
    assert (keep / "runners-at-base-1.xml").is_file()
```

Unit rows for `REPORTS` need `junit()` to take a `file` attribute: one row
whose `file` is `tests/test_api/test_users.py` (failing), appended
`["tests/test_api.py"]`, which gives `UNPLACED`. One row in dotted form with
`tests.x.tests.test_two` failing beside `tests.test_one` passing, appended
`["tests/test_two.py"]`, which gives `UNPLACED`. Mutation check: drop the
`unshared` test and the second row turns `ON_BASE`. Drop the `file` branch
and the first row turns `ON_BASE`.

## Facts for the evidence ledger

- pytest 9.1.1 writes a test's file as a path in its JUnit report only under
  the `xunit1` family: `_pytest/junitxml.py`, `record_testreport`, the NAME NOT IN TREE
  `"file": testreport.location[0]` attribute, which is filtered out for
  `xunit2`, the default. The path is relative to the rootdir.
- `record_testreport` puts `--junit-prefix` in front of every `classname`, NAME NOT IN TREE
  and so in front of a collection error's empty one.
- `.github/scripts/run_tests.py` line 644 hands its arguments to pytest
  unchanged, so this repository's `bin/test -q` receives the gate's
  `--junitxml`.

Needs a fix: yes — 🟡 1 (dotted-name placement gives `failing on base too` to a file with no test at the base), 🟡 2 (a runner that does not take the gate's arguments is passed over or not counted), 🟡 3 (rule 3 understates what the collection pass runs at the base), 🟡 4 (the `NOTHING_TOGETHER` reason and one rule-3 sentence are false for an existing module with no test).
Loses a record or crashes: no

The broad gate has not come due: this round leaves four findings open.

## Proof block

Opened this round: `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/spec.md`,
`overview.md` and `changelog.md` in the same directory;
`skills/verify/scripts/broad_gate.py` (the diff a3aa139a..225af880, and lines
1906–2064, 2220–2330 and 3410–3440 at 225af880); the diffs of
`skills/verify/SKILL.md`, `templates/config.md`, `tests/test_release_hygiene.py`
and `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`;
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (lines 685–797, 876–910,
3952–4010, 4150–4340, 4547–4553, 4940–5110, and the diff's word assertions);
`bin/test`; `.github/scripts/run_tests.py` (lines 1–80 and the lines naming
`argv`); `seal/config.md` (the `Broad gate` row); `_pytest/junitxml.py` of
pytest 9.1.1 (lines 110–150 and 445–462).

Executed: the probes and module runs in *Executed probes*, in a
`git clone --no-local` of the worktree at 225af880. The probe file, the clone
and its virtual environment are deleted.

Unverified: the full suite, lint and typecheck, which the sealer answers.
Windows and pytest 7 and 8 report shapes (❓ row above).
