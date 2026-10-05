# Round 2 report — 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict

Target SHA: 8662f9bf · Base: `release/v0.18.3` at a3aa139a · PR #804 (draft)
Ran by: specseal:warden on claude-opus-5-5

This is the verifying round over round 1's fixes (`3f90f333..78becaaf`, the
code in 93178ed8). Round 1 met the floor, so a fix this round commissions is
the work item's one reopening.

## Summary

Three of round 1's four findings are closed as recorded. P3 (`sh -c` before
the runner) now reads `MULTI_RUNNER`, P5's extra runs are stated in rule 3,
the changelog and the docstring, and P4's reason no longer calls a present
file missing.

Round 1's first finding is closed for the two layouts it ran and open for
its class. The class is "a name pytest's report gives that also fits
another file". This round ran three more members of it at the target, and
each gives `failing on base too` to a file the base does not fail. a3aa139a
gave `new` in all three.

- **Q1 — the shared-prefix rule is necessary, not sufficient.** When every
  test in the report sits under the same deeper directory, a same-named
  module there is placed at a positive offset that every test shares. P2
  without `tests/test_one.py` is enough. 🟡 1.
- **Q3 — a negative offset with pytest's rootdir at the run directory.**
  The handed `a/tests/test_two.py`, less its first directory, equals the
  failing `tests/test_two.py`. Rule 3 names only a rootdir below the run
  directory, and this rootdir is not below it. 🟡 1.
- **Q4b — the `xunit1` `file` attribute is where a test's function is
  defined, not the module that collected it.** A test class that inherits
  its tests from another test module fails at the base under the other
  module's path. The defining file then reads `failing on base too`,
  although every test it collects passes there. 225af880 read `new` here,
  so round 1's fix introduced this. The strict side (Q4c) is a file that
  the base fails through a test inherited from a helper module. It now
  reads `new`. 🟡 2.

The fix for 🟡 1 reads each report path against the files the base tracks.
That means the gate no longer guesses an offset. It also means the placement
step can no longer give `failing on base too` from another runner's
directory, so P7 and P3 with `-p no:junitxml` read `new?` as well. With
both fixes, the three gate modules give 499 passed, 1 skipped, and the four
regression cases below fail at the target and pass with the fix.

The counting change is sound for every shape this round ran. A pytest part
that is not a runner (`pytest --version`) is not counted. A preset
`PYTEST_ADDOPTS` and a keep path with spaces still count the `sh -c`
runner. The row's, environment's or ini's `junit_family` loses to the
gate's. The rule-3 list of uncounted shapes is incomplete, though: a
runner before the measured one whose own command line names `--junitxml`
is not counted (Q8, executed), and neither is one whose environment drops
`PYTEST_ADDOPTS` (constructed). 🟡 3.

A green run is unchanged: `compare_at_base` is still called only from the
failed-suite branch.

## Round 1's verdicts, answered

| Round 1 | Recorded | This round |
|---|---|---|
| Finding 1 (P1 package, P2 deeper module) | fixed `93178ed8` | P1 and P2 read `UNPLACED` at the target. The class is not closed: Q1 is P2 with no test outside the deeper directory, and Q3 is the same mistake in the other direction. Reopened as this round's 🟡 1 |
| Finding 2 (P3 `sh -c` before the runner, P7 and `-p no:junitxml` named) | fixed `93178ed8` | Closed for P3: `MULTI_RUNNER` naming parts 3 and 1, and `runners-at-base-1.xml` kept. The named list is incomplete (🟡 3) |
| Finding 3 (what the collection pass runs) | fixed `93178ed8` | Closed. P5 still runs A twice and B once, which is what rule 3, the changelog and the `compare_at_base` docstring now say |
| Finding 4 (`NOTHING_TOGETHER` reason, rule 3's empty-file sentence) | fixed `93178ed8` | Closed. P4 words are unchanged, the reason text says "or holds no test there", it is pinned, and rule 3 carries the root-carried half |

## What the account claimed, and what was checked

| Claim (where) | What the code does |
|---|---|
| "a test is placed by the path the `xunit1` report gives it, and a positive offset only where every test in the report shares it" closes the deeper-module shape (`overview.md` Not done) | Executed Q1: every test shares the deeper prefix, and the deeper module is placed on `tests/test_two.py` → `failing on base too` |
| "One shape stays open … pytest's rootdir below the directory the row runs pytest in" (`overview.md`, rule 3) | Q3b confirms the named shape. Q3 is a second open shape with the rootdir AT the run directory (the kept report names `tests/test_one.py` from the repository root), and it is named nowhere |
| `JUNIT_FAMILY`'s comment: "the `xunit1` family writes each test's file as a path from the rootdir" | It writes the file the test's function is defined in. Executed Q4b: `classname="tests.test_three.TestThree"` beside `file="tests/test_two.py"` |
| Rule 3: the collection pass counts a runner before the measured one through `PYTEST_ADDOPTS`, "but two shapes stay uncounted (#807)" | A runner whose own command line names `--junitxml` is a third, executed (Q8: `runners-at-base-1.txt` kept and no `.xml`, word `failing on base too`). One whose environment does not carry `PYTEST_ADDOPTS` is a fourth, constructed |
| The family option "changes nothing about the run" and wins over a row or ini that sets one | Executed Qf1, Qf2 and Qf3: `-o junit_family=xunit2` in the row, in `PYTEST_ADDOPTS`, and `junit_family = xunit2` in `pytest.ini` all lose to the gate's, and P1 still reads `UNPLACED`. It does not matter for the branch's own run, which the gate never changes |
| "this repository's own row runs its two `uvx ruff` prefixes once more" (changelog) | Read: `seal/config.md`'s row is `uvx ruff check . && uvx ruff format --check . && bin/test -q`, so the runner is prefix 3. Prefixes 1 and 2 run in the collection pass with nothing appended, which means `ruff check` twice and `ruff format --check` once, at the base, only on a failing gate. `.github/scripts/run_tests.py`'s `caller_decided` does not treat `-o` specially, and line 644 passes it on |
| A green run is unchanged (prompt) | Read: `skills/verify/scripts/broad_gate.py:3487-3491` calls `compare_at_base` only for the suite arm, only when it failed and named failing files |

## Findings from execution

### 🟡 1 — a same-named file is still placed on the handed file when every test shares its directory, or at a negative offset with the rootdir at the run directory

`skills/verify/scripts/broad_gate.py:2035-2058` (`report_words`, the
`shared` prefix) and `:1977-1983` (`offsets`, the exact branch). The exact
match accepts any suffix of the report's path as the handed file, at any
positive offset. It also accepts any shorter tail at a negative offset. The
only guard is that a positive offset must not exceed the leading components
every test shares. Two layouts pass that guard, each executed end to end
through the gate with the module's fixtures:

- **Q1.** At the base, `tests/test_two.py` holds no test, `tests/test_one.py`
  holds none either, and `tests/x/tests/test_two.py` fails. The report has
  one test, `file="tests/x/tests/test_two.py"`, so `shared` is 4 and the
  offset 2 passes. Words: target `failing on base too`, 225af880 the same,
  a3aa139a `new`.
- **Q3.** The row is `SUITE_ROW` plus ` a`. At the base,
  `a/tests/test_two.py` holds no test and `tests/test_two.py` fails.
  pytest's rootdir is the run directory (the kept report names
  `file="tests/test_one.py"`). `tests/test_two.py` equals the handed path
  less `a`, so it is placed at -1. Words: target `failing on base too`,
  a3aa139a `new`. This layout is not the limit rule 3 names, because the
  rootdir is not below the run directory.

**Why it matters.** `failing on base too` is the one word that lets a red
suite through, and in both layouts the base passes the handed file or holds
no test in it. A monorepo whose only tests sit in one package, or a row that
collects two sibling trees, is enough. The cause is that a path alone
cannot say which directory it is relative to. The gate has never known the
rootdir or the directory the row runs pytest in, and the offset rules guess
both.

**The fix reads the guess off the tree instead.** pytest's rootdir is a
directory under which every exact path in the report is a file the base
tracks. The directory the row runs pytest in is one under which every
handed file is, because pytest runs nothing otherwise. A placement counts
only where each is exactly one directory and the two name the same file.
Where the base tracks a second directory that fits either, the file reads
`UNPLACED`. This keeps every legitimate offset this round ran: Q10 (`cd sub`
with the ini file at the root), Q11 (the ini file in `sub`), and every case
of the three modules. It closes Q1 and Q3, and it also closes the rule-3
named limit (Q3b), P7, P3 with `-p no:junitxml`, and Q8. Each of those
gave `failing on base too` because the same path existed in both runners'
directories, and the tree now sees both. The one word it gives up is Q10b
(`cd sub`, with the root also tracking `tests/test_two.py`). It now reads
`new?`, which is the #761 layout, so that is the direction to give up.

### 🟡 2 — the `xunit1` path is the file a test is defined in, so an inherited test is placed on the file it inherits from

`skills/verify/scripts/broad_gate.py:1938-1946` (`report_cases`). pytest
writes `file` from the test's location, and a test's location is where its
function's source is. A test class that inherits its methods from a class in
another module reports the other module's path, while its `classname` names
the module that collected it. Executed:

- **Q4b, permissive.** `tests/test_two.py` defines a mixin `Shared` and
  `TestTwo(Shared)`, which passes. `tests/test_three.py` has
  `TestThree(Shared)` with a value that fails at the base. The branch fixes
  `test_three` and adds a failing test to `test_two`. The base report
  carries `classname="tests.test_three.TestThree" … file="tests/test_two.py"`,
  failing. Words: target `failing on base too`, 225af880 `new`, a3aa139a
  `new`. Round 1's fix introduced this.
- **Q4 (the mixin module collects no test of its own)**: target
  `failing on base too`, 225af880 `UNPLACED`, a3aa139a `new`.
- **Q4c, strict.** `tests/test_two.py` inherits a failing test from
  `tests/helpers.py`, and the branch adds a second failure. Target `new`;
  225af880 and a3aa139a `failing on base too`. A pre-existing failure is
  reported as one this work introduced.

**Why it matters.** Shared test base classes across test modules are an
ordinary pattern, and the permissive case needs nothing else. The fix keeps
`file` only where the test's dotted name also names that file. Otherwise
the test is placed by its dotted name, as 225af880 did. Q4b then reads
`new`, Q4 `UNPLACED` and Q4c `failing on base too`.

### 🟡 3 — rule 3 names two runners the collection pass cannot count, and the class has four

`templates/config.md:333` rule 3 ("but two shapes stay uncounted (#807)"),
`skills/verify/scripts/broad_gate.py:2258-2265` (`compare_at_base`
docstring), and the changelog's last bullet. A runner before the measured
one is counted only where it writes the report that the gate's
`PYTEST_ADDOPTS` asks for. Enumerated by what has to hold for that write:

- pytest's report plugin is loaded. Not with `-p no:junitxml`, which is named.
- The `--junitxml` that pytest keeps is the gate's. pytest reads the ini
  file's `addopts`, then `PYTEST_ADDOPTS`, then the command line, and the
  last one wins. A runner whose own command line names `--junitxml` writes
  there instead. Executed, Q8 (`sh -c '<SUITE_ROW> --junitxml=own.xml' &&
  cd sub && <SUITE_ROW>`): `runners-at-base-1.txt` kept, no `.xml`, word
  `failing on base too`; a3aa139a `new`. Not named.
- The process sees the gate's environment. A runner started by a tool that
  builds an environment of its own without `PYTEST_ADDOPTS` never gets the
  path. Constructed, not run. Not named.
- The runner is reached. A runner behind a part that fails, or behind `||`,
  is named.

**Why it matters.** Rule 3 is what a row's author reads to learn which rows
the gate cannot count, and it says two shapes where four exist. At the
target, Q8 gives the permissive word. With 🟡 1's fix the placement step
reads `new?` for it, and the sentence's "or `failing on base too`" stops
being true as well. So the paste-ready text below assumes 🟡 1's fix; without
that fix, keep "or `failing on base too`".

## Findings from reading

- **⬜ 4 — two comments in the test module state a rootdir the fixtures do
  not have.** `tests/test_the_seal_is_taken_once_by_the_sealer.py:4274`
  ("The fixtures' shape with a path: the rootdir is `tests`, offset -1") and
  `:5229` (P2's case: "at offset 1 from the rootdir `tests`"). Every kept
  report from the fixtures this round names `file="tests/…"` and
  `classname="tests.…"`, so the rootdir is the repository root, and P2's
  offset is 2. The unit row's input is still a valid shape, a row whose
  rootdir is `tests`. Only the sentence attaching it to the fixtures is
  wrong.
- **⬜ 5 — "`--junitxml` included" is no longer enough for a wrapper.**
  Rule 3's last sentence tells a row's author to pass the arguments on,
  "`--junitxml` included". A wrapper that forwards the files and
  `--junitxml` but rejects other options now reads `NO_RUNNER`, because the
  gate also appends `-o junit_family=xunit1`. Executed (Q12, an `argparse`
  wrapper): target `NO_RUNNER`, 225af880 and a3aa139a
  `failing on base too`. The direction is safe, which is why this is ⬜.
- **⬜ 6 — `overview.md` §*Not done* says one placement shape stays open.**
  Q1, Q3 and Q4b are three more at the target. This is a correction to this
  work item's paperwork. Its text follows whichever of 🟡 1 and 🟡 2 lands.
- **Counting, by construction.** A prefix before the settled one cannot end
  in a runner that takes the appended arguments, because that prefix would
  have written the report and settled first. The pytest parts the new
  branch can reach are droppers, refusers, unreached parts and parts that
  write no session report. Q7 executed the last kind (`pytest --version`
  first): no `.xml`, one runner, word unchanged. Each prefix holding a
  dropper writes its own report, and `second` records only the first one.
  So a runner is never counted twice into a different word, and no
  one-runner row this round could build turns into `MULTI_RUNNER`.
- **`shlex.quote` in `PYTEST_ADDOPTS`.** pytest splits that variable with
  POSIX `shlex.split`. Single quotes keep a Windows backslash and a space
  literal, so the quoting is right on both platforms. Spaces were executed
  (Qs2, keep directory `o u t`, `MULTI_RUNNER`). Backslashes were read and
  not run.
- **Outside this change, noted only.** With `--rootdir=sub` or
  `-c sub/pytest.ini` (Q2), pytest's own `FAILED` line names
  `sub/test_two.py`, which does not exist. The gate reads it `new` at all
  three SHAs. With `-rN` preset in the environment (Qs), the branch run
  prints no `FAILED` line, and nothing is compared at all three SHAs. Both
  are on the branch side, which this change did not touch, and neither is
  permissive.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The exact placement still gives `failing on base too` to a file the base does not fail. A same-named module is placed at a positive offset when every test in the report sits under it (Q1), or at a negative offset while pytest's rootdir is the run directory (Q3). Round 1's first finding is closed for P1 and P2 only | `skills/verify/scripts/broad_gate.py:1977-1983`, `skills/verify/scripts/broad_gate.py:2035-2058` | open | Executed Q1 and Q3 at 8662f9bf (`failing on base too`) and a3aa139a (`new`). The tree-read fix gives `UNPLACED` for both, keeps Q10 and Q11, and runs the three gate modules 499 passed, 1 skipped |
| 🟡 2 | `report_cases` takes `file` as the test's module, but it is the file the test's function is defined in. An inherited test fails at the base under the parent's file (Q4b, permissive), and a file failing through a helper's test reads `new` (Q4c) | `skills/verify/scripts/broad_gate.py:1938-1946` | open | Executed Q4, Q4b and Q4c at the three SHAs. 225af880 read Q4b `new`, so the fix introduced it. With the name check, Q4b `new`, Q4 `UNPLACED` and Q4c `failing on base too` |
| 🟡 3 | Rule 3, the docstring and the changelog name two runners the collection pass cannot count, and the class has four. A runner before the measured one whose command line names `--junitxml` (Q8, executed) and one whose environment drops `PYTEST_ADDOPTS` (constructed) are missing | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2258-2265` | open | Executed Q8: `failing on base too` at 8662f9bf, `new` at a3aa139a, no `runners-at-base-1.xml` written |
| ⬜ 4 | Two test-module comments attach a rootdir of `tests` to the fixtures, whose rootdir is the repository root, and P2's offset is 2, not 1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4274`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:5229` | open | Executed: every kept fixture report names `file="tests/…"` |
| ⬜ 5 | Rule 3's "`--junitxml` included" does not cover the appended `-o junit_family=xunit1`, so a wrapper that forwards only known options reads `NO_RUNNER` | `templates/config.md:333` | open | Executed Q12: `NO_RUNNER` at 8662f9bf, `failing on base too` at 225af880 and a3aa139a. A safe direction |
| ⬜ 6 | `overview.md` Not done names one open placement shape; Q1, Q3 and Q4b are three more | `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/overview.md` | open | A correction to this run's paperwork, not counted in Needs a fix |
| 🟢 | round 1's second finding is closed for P3 — a runner that drops its arguments before the measured one is counted through `PYTEST_ADDOPTS` | `skills/verify/scripts/broad_gate.py:2330-2337` | confirmed | Executed P3 `sh -c`: `MULTI_RUNNER` (parts 3 and 1), `runners-at-base-1.xml` kept; 225af880 `failing on base too`, a3aa139a `new` |
| 🟢 | round 1's third finding is closed — what the collection pass runs is stated where a row's author reads it | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2243-2256`, `changelog.md` | confirmed | Executed P5: markers `AA` and `B` at 8662f9bf and 225af880, none at a3aa139a, which is what the three texts now say |
| 🟢 | round 1's fourth finding is closed — the `NOTHING_TOGETHER` reason and the rule-3 sentence for a file the root carries | `skills/verify/scripts/broad_gate.py:1899-1903`, `templates/config.md:333` | confirmed | Executed P4: `NOTHING_TOGETHER` and `UNPLACED`, unchanged; the reason is pinned in `test_the_unmeasured_word_says_so_and_every_reader_is_told_it` |
| 🟢 | The counting change turns no one-runner row into `MULTI_RUNNER`, survives a preset `PYTEST_ADDOPTS` and a keep path with spaces, and the family option wins over a row, environment or ini that sets one | `skills/verify/scripts/broad_gate.py:2298-2338` | confirmed | Executed Q7, Qs2, Qf1, Qf2 and Qf3; the twice-counted case by construction (Findings from reading) |
| 🟢 | A green run is unchanged, and this repository's row pays two `uvx ruff` prefixes once more only on a failing gate | `skills/verify/scripts/broad_gate.py:3487-3491`, `seal/config.md` | confirmed | Read |
| ❓ | Windows (backslash `file` paths, `cmd.exe` quoting of the family option, `shlex.quote` with backslashes in `PYTEST_ADDOPTS`) and the `file` attribute on pytest 7 and 8 | `skills/verify/scripts/broad_gate.py:1870-1877`, `skills/verify/scripts/broad_gate.py:2330-2337` | ❓ out of verified scope | Read only, on macOS with pytest 9.1.1. CI's three-platform test job answers Windows; the repository owner answers whether pytest 7 and 8 matter |

## Executed probes

| What was run | Result |
|---|---|
| P1–P7 end to end through the gate at 8662f9bf, at a3aa139a and at 225af880 (each version's `broad_gate.py` swapped into one review clone at 8662f9bf; one probe file built on the module's helpers) | The words-per-probe table below. All 29 probe cases ran at each SHA (exit 0) |
| This round's shapes Q1–Q12 at the same three SHAs | The second table below |
| The candidate fix (🟡 1 and 🟡 2's blocks) applied in the clone, every probe rerun | The last column of both tables |
| `bin/test -q tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_gate_hands_cmd_a_path_it_can_run.py tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` with the fix applied | 499 passed, 1 skipped (exit 0) |
| The four regression cases below, at 8662f9bf and with the fix | 4 failed at 8662f9bf (`'failing on base too' == UNPLACED` twice, `'failing on base too' == 'new'`, `'new' == 'failing on base too'`), 4 passed with the fix |
| Mutation check of the fix: the name check removed, then the tree removed | 2 failed each, the inherited pair and the placement pair respectively |
| `uvx ruff check` and `uvx ruff format --check` on the fixed `broad_gate.py` | both clean |
| The broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

```
words per probe            8662f9bf             a3aa139a             225af880             with this round's fix
P1 offset-0 package        UNPLACED             new                  failing on base too  UNPLACED
P2 deeper module           UNPLACED             new                  failing on base too  UNPLACED
P3 sh -c then runner       MULTI_RUNNER (3, 1)  new                  failing on base too  MULTI_RUNNER (3, 1)
P3 -p no:junitxml then run failing on base too  new                  failing on base too  UNPLACED
P4 empty module, files row NOTHING_TOGETHER     NO_RUNNER            NOTHING_TOGETHER     NOTHING_TOGETHER
P4 empty module, SUITE_ROW UNPLACED             new                  UNPLACED             UNPLACED
P5 parts after the runner  ran A twice, B once  ran neither          ran A twice, B once  ran A twice, B once
P6 row's own --junitxml    failing on base too  failing on base too  failing on base too  failing on base too
P7 runner then sh -c       failing on base too  failing on base too  failing on base too  UNPLACED
```

```
this round's shapes                         8662f9bf             a3aa139a             225af880             with the fix
Q1  deeper module, every test shares it     failing on base too  new                  failing on base too  UNPLACED
Q3  -1 offset, rootdir at the run dir       failing on base too  new                  failing on base too  UNPLACED
Q3b -2 offset, rootdir below (named limit)  failing on base too  new                  failing on base too  UNPLACED
Q4  inherited test, mixin collects none     failing on base too  new                  UNPLACED             UNPLACED
Q4b inherited test, own test passes         failing on base too  new                  new                  new
Q4c file fails through a helper's test      new                  failing on base too  failing on base too  failing on base too
Q5  P1 under -n 2                           UNPLACED             new                  failing on base too  UNPLACED
Q7  pytest --version before the runner      failing on base too  failing on base too  failing on base too  failing on base too
Q8  dropper with its own --junitxml first   failing on base too  new                  failing on base too  UNPLACED
Q10 cd sub, ini at the root                 failing on base too  failing on base too  failing on base too  failing on base too
Q10b the same, root also tracks the file    failing on base too  failing on base too  failing on base too  UNPLACED
Q11 ini in sub, row at the root             failing on base too  failing on base too  failing on base too  failing on base too
Q12 wrapper knows --junitxml, not -o        NO_RUNNER            failing on base too  failing on base too  NO_RUNNER
Qf  junit_family=xunit2 in row, env, ini    UNPLACED (P1)        new                  failing on base too  UNPLACED
Qs2 preset PYTEST_ADDOPTS, keep "o u t"     MULTI_RUNNER (3, 1)  new                  failing on base too  MULTI_RUNNER (3, 1)
Q2  --rootdir=sub / -c sub/pytest.ini       sub/test_two.py new on every SHA: pytest's own FAILED name, branch side
Qs  -rN preset in the environment           no comparison on every SHA: no FAILED line on the branch
```

The words Q10, Q11 and P6 give at the target are right. Q7 and Q8 kept
`runners-at-base-1.txt` with no `.xml`, and P3 `sh -c` and Qs2 kept
`runners-at-base-1.xml`.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #807's body lists two uncounted runners. It should also list a runner before the measured one whose command line names `--junitxml` (Q8), and one whose environment drops `PYTEST_ADDOPTS` | #807, as an edit to its list | the orchestrator, who files and edits issues |

## Paste-ready fixes

### 🟡 1 — read a report path against the base's tracked files

Tested in the review clone together with 🟡 2's block: the three gate
modules 499 passed, 1 skipped, and `ruff check` and `ruff format --check`
are clean.

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ import ntpath
 import ntpath
 import os
+import posixpath
 import re
@@ def holds(address, part):  (after 🟡 2's `holds`)
+def joined(directory, address):
+    """`address` under `directory`, both split at `/`, as one normalised
+    path, or None where it climbs out of the tree."""
+    path = posixpath.normpath("/".join((*directory, *address)))
+    return None if path.startswith("..") else path
+
+
+def directories_holding(addresses, tree):
+    """Every directory of `tree` (the base's tracked paths) under which
+    each of `addresses` names a tracked file. Empty where none does, or
+    where every address climbs out of the directory it is read from."""
+    plain = [a for a in addresses if ".." not in a]
+    if not plain:
+        return set()
+    n = len(plain[0])
+    found = set()
+    for path in tree:
+        parts = tuple(path.split("/"))
+        if parts[len(parts) - n :] == plain[0] and len(parts) >= n:
+            directory = parts[: len(parts) - n]
+            if all(joined(directory, a) in tree for a in addresses):
+                found.add(directory)
+    return found
@@
-def report_words(text, files, code, stopped, alone=False):
+def report_words(text, files, code, stopped, alone=False, tree=None):
@@ def report_words(text, files, code, stopped, alone=False):
     named = {f: set() for f in files}
     unshared = set()
     places = []
+    if tree is not None:
+        # Where a path can be read against the base's tree, the rootdir is
+        # a directory under which every such test's file exists, and the
+        # directory the row runs pytest in one under which every handed
+        # file does (pytest ran nothing otherwise). A placement is the
+        # run's only where one of each is possible and they name one file.
+        roots = directories_holding([a for a, _, e in cases if e], tree)
+        heres = directories_holding([paths[f][True] for f in files], tree)
     for address, failed, exact in cases:
         hit = set()
         for f in files:
-            found = offsets(paths[f][exact], address, exact)
-            if any(shift > shared for shift in found):
-                unshared.add(f)
+            if exact and tree is not None:
+                tests = {joined(d, address) for d in roots} - {None}
+                here = {joined(c, paths[f][True]) for c in heres} - {None}
+                if not tests & here:
+                    continue
+                if len(tests) > 1 or tests != here:
+                    unshared.add(f)
+                found = offsets(paths[f][True], address, True) or {None}
+            else:
+                found = offsets(paths[f][exact], address, exact)
+                if any(shift > shared for shift in found):
+                    unshared.add(f)
             if found:
@@ def compare_at_base(root, base, command, files, keep):
         others = [f for f in files if f not in candidates]
+        # The base's tracked paths, which a report's `file` is read against
+        # (`report_words`).
+        tree = frozenset((git(scratch, "ls-files", "-z") or "").split("\0")) - {""}
@@
                     alone=bool(alone),
+                    tree=tree,
                 )
```

The rule-3 sentences "A test is placed on a file by the path pytest's report
gives it … reads `new?`. Where pytest's rootdir sits below that directory, …
a file the base holds no test in." become the following. The same text
replaces the two strings pinned in
`test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`.

```
A test is placed on a file by the path pytest's report gives it (the gate also appends `-o junit_family=xunit1`, which writes that path), read against the files the base tracks: pytest's rootdir is a directory under which every such path is a tracked file, the directory the row runs pytest in is one under which every file the run was handed is, and the test is placed on the file only where each is one directory and the two name one file. Where the base tracks a second directory that fits either, the file reads `new?`.
```

The changelog's sentences from "by the file's path and at the run's one
offset" to "shares the directories in front of it." become:

```
  A file reads `failing on base too` only where the report places a failing
  or erroring test on that file and no other, by the file's path read against
  the files the base tracks. The gate also appends `-o junit_family=xunit1`,
  which makes pytest write each test's file as a path, so a package or a class
  named like a module is never taken for it. Where the base tracks a
  same-named file the path could also name, from another rootdir or another
  directory the row could run pytest in, the file reads `new?`.
```

The `report_words` docstring's first `UNPLACED` bullet gains: "or, read
against the base's tracked paths (`tree`), where a second rootdir or a
second directory the row could run pytest in fits the test or the file".

### 🟡 2 — keep a report's `file` only where the dotted name names it too

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ def report_cases(text):
     cases = []
     for case in root.iter("testcase"):
         failed = case.find("failure") is not None or case.find("error") is not None
+        name = tuple((case.get("classname") or case.get("name") or "").split("."))
         where = (case.get("file") or "").replace("\\", "/")
-        if where:
+        # `file` is where the test's function is DEFINED, and the dotted
+        # name is the module that collected it: a test a class inherits
+        # from another module names that other module's file. Only a file
+        # the dotted name also names is the test's own.
+        if where and holds(name, dotted(where)):
             cases.append((tuple(where.split("/")), failed, True))
             continue
-        where = case.get("classname") or case.get("name") or ""
-        cases.append((tuple(where.split(".")), failed, False))
+        cases.append((name, failed, False))
     return cases
 
 
+def holds(address, part):
+    """Whether `part` sits in `address` at a component boundary."""
+    n = len(part)
+    return any(address[i : i + n] == part for i in range(len(address) - n + 1))
```

`JUNIT_FAMILY`'s comment ("writes each test's file as a path from the
rootdir") gains "— the file the test's function is defined in, which
`report_cases` keeps only where the test's dotted name names it too". Rule 3
gains, after 🟡 1's sentence:

```
That path is the file a test's function is defined in, so a test a class inherits from another module is placed by its dotted name instead, which cannot tell a module from a package of the same name.
```

### 🟡 3 — name the four runners the collection pass cannot count

Rule 3's sentence from "Where another part does, the collection pass counts"
to "from the other runner's directory." becomes the following. It assumes
🟡 1's fix; without it, keep "or `failing on base too`".

```
Where another part does, the collection pass counts a runner before the one that wrote the report through `PYTEST_ADDOPTS`, which counts it only where it writes the report that variable asks for. Four shapes stay uncounted (#807): a runner given `-p no:junitxml`, which refuses the option from either source; one whose own command line names `--junitxml`, which wins over `PYTEST_ADDOPTS`; one started in an environment that does not carry `PYTEST_ADDOPTS`; and a runner after the one that wrote the report inside a part that drops its arguments. Such a row is read as one with a single runner, and a file can read `new` from the other runner's directory, or `new?` where the base tracks it in both.
```

The `compare_at_base` docstring's "Nor does it count a runner given `-p
no:junitxml`, which refuses the option from either source, or a later runner
inside a part that drops its arguments (#807)." becomes:

```
    Nor does it count a runner given `-p no:junitxml`, which refuses the
    option from either source, one whose own command line names
    `--junitxml`, which wins over the environment, one started in an
    environment without `PYTEST_ADDOPTS`, or a later runner inside a part
    that drops its arguments (#807).
```

The changelog's last bullet ends "…, a runner given `-p no:junitxml`, a
runner whose own command line names `--junitxml`, one started without
`PYTEST_ADDOPTS`, and a later runner inside a part that drops its arguments
(#807)." The rule-3 pin in
`test_the_solo_runs_cost_and_limits_are_told_where_the_row_is_written`
takes the new text.

## Regression tests to plant

Destination: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside
the round 1 cases (they use its `base_then_feature`, `run_gate`, `verdict_of`
and `gate_module`). Each was run as written: red at 8662f9bf with the words
in *Executed probes*, green with both fixes. Removing the name check turns
the last two red. Removing the tree turns the first two red.

```python
MIXIN = (
    "class Shared:\n"
    "    value = 1\n\n"
    "    def test_shared(self):\n"
    "        assert self.value == 1, 'planted'\n"
)


def test_a_same_named_module_every_test_sits_beside_is_not_placed_on_the_file(
    tmp_path,
):
    """#789 round 2's 🟡 1 (Q1). Every test the base's report names sits
    under `tests/x/tests`, so the offset 2 is shared by all of them, and
    `tests/x/tests/test_two.py`'s failure was placed on `tests/test_two.py`,
    which holds no test at the base."""
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW,
        {
            "tests/test_one.py": "X = 1\n",
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
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().UNPLACED, (
        out.stdout
    )


def test_a_shorter_same_named_path_is_not_placed_on_the_file(tmp_path):
    """#789 round 2's 🟡 1 (Q3). pytest's rootdir is the directory the row
    runs in, and the failing `tests/test_two.py` equals the handed
    `a/tests/test_two.py` less its first directory, so it was placed there
    at offset -1."""
    repo = base_then_feature(
        tmp_path / "repo",
        f"{SUITE_ROW} a",
        {
            "a/__init__.py": "",
            "a/tests/__init__.py": "",
            "a/tests/test_two.py": "X = 1\n",
            "tests/test_two.py": FAILING_TEST,
        },
        {"a/tests/test_two.py": FAILING_TWO, "tests/test_two.py": PASSING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "a/tests/test_two.py") == gate_module().UNPLACED, (
        out.stdout
    )


def test_a_test_another_module_inherits_is_not_placed_on_the_defining_file(tmp_path):
    """#789 round 2's 🟡 2 (Q4b). `xunit1` writes the file a test's function
    is defined in: `tests/test_three.py`'s inherited test failed at the base
    under `file="tests/test_two.py"` and gave that file `failing on base
    too`, though every test it collects passes there."""
    three = "from test_two import Shared\n\n\nclass TestThree(Shared):\n    value = {}\n"
    own = MIXIN + "\n\nclass TestTwo(Shared):\n    value = 1\n"
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW,
        {"tests/test_two.py": own, "tests/test_three.py": three.format(2)},
        {
            "tests/test_two.py": own + "\n\n" + FAILING_TWO,
            "tests/test_three.py": three.format(1),
        },
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().NEW, out.stdout


def test_a_test_a_file_inherits_from_a_helper_is_placed_on_that_file(tmp_path):
    """#789 round 2's 🟡 2 (Q4c), the strict side: the base fails
    `tests/test_two.py` through a test it inherits from `tests/helpers.py`,
    and `xunit1` names the helper, so the file read `new`."""
    helpers = (
        "class Base:\n    v = 1\n\n    def test_inherited(self):\n"
        "        assert self.v == 1, 'planted'\n"
    )
    two = "from helpers import Base\n\n\nclass TestTwo(Base):\n    v = 2\n\n\ndef test_ok():\n    pass\n"
    repo = base_then_feature(
        tmp_path / "repo",
        SUITE_ROW,
        {"tests/helpers.py": helpers, "tests/test_two.py": two},
        {"tests/test_two.py": two + "\n\n" + FAILING_TWO},
    )
    out = run_gate(repo)
    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
    assert verdict_of(out.stdout, "tests/test_two.py") == gate_module().ON_BASE, (
        out.stdout
    )
```

Q8 is not planted as a passing case. With 🟡 1's fix it reads `UNPLACED`,
which a case can pin. Whether to pin it is the fix pass's choice, since
🟡 3's fix is a sentence.

## Facts for the evidence ledger

- pytest 9.1.1's `xunit1` `file` attribute is the path of the source file a
  test's function is defined in, relative to the rootdir. For an inherited
  test method it names the parent class's module, while `classname` names
  the collecting module (executed, Q4b's kept report).
- With no ini file, pytest 9.1.1's rootdir for the module's fixtures is the
  directory the row runs in, not `tests` (executed: every fixture report
  names `tests/…`).
- pytest reads `--junitxml` from the ini file's `addopts`, then
  `PYTEST_ADDOPTS`, then the command line, and the last one wins (executed
  for the command line over `PYTEST_ADDOPTS`, Q8; the ini order was read).

Needs a fix: yes — 🟡 1 (an exact placement still reaches a same-named file
when every test shares its directory, or at a negative offset with the
rootdir at the run directory), 🟡 2 (`file` is the defining file, so an
inherited test is placed on the wrong module), 🟡 3 (rule 3 names two of the
four runners the collection pass cannot count).

Loses a record or crashes: no

This round leaves three findings needing a fix, so the broad gate has not come due.

## Proof block

Opened this round: `rounds/round-1-report.md`, `rounds/round-1.md`,
`survivors.md`, `changelog.md`, and the 225af880..8662f9bf diffs of
`overview.md` and `spec.md`, all in this work item's directory.
`skills/verify/scripts/broad_gate.py`: the 225af880..8662f9bf diff, and
lines 356-366, 1860-2420 and 3470-3500 at 8662f9bf. The a3aa139a..8662f9bf
diff of `skills/verify/SKILL.md`. The 225af880..8662f9bf diff of
`templates/config.md`. In `tests/test_the_seal_is_taken_once_by_the_sealer.py`:
the 225af880..8662f9bf diff and lines 685-800, 876-910, 3950-4010, 4268-4276
and 5225-5232. `.github/scripts/run_tests.py` lines 366-410 and 644.
`bin/test`. `seal/config.md`'s `Broad gate` row. Issue #807.

Executed: the probes and module runs in *Executed probes*, in a
`git clone --no-local` of the worktree at 8662f9bf under this session's
scratchpad. The probe file, the clone, its virtual environment and every
output are deleted.

Unverified: the full suite, lint and typecheck, which the sealer answers.
Windows, and pytest 7 and 8 (the ❓ row).
