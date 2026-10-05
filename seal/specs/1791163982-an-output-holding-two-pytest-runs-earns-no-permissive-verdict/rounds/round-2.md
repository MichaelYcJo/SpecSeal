# 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict — review round 2

| Field | Value |
|---|---|
| Target SHA | 8662f9bf9c4f85a79304c9f5d89bd4e0ed6bc452 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #804 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `562ab360f45bb4ae7eb8e46d98417350e83b5872..bf8669c2f5c885a3bf88d231b75ee358538c668c`, 4 commits |
| Contract changes | report_words → round-1-report.md, round-1.md, round-2-report.md, round-2.md, compare_at_base, pytest |
| New units | joined (depth 1); directories_holding (depth 1); test_an_inherited_tests_file_is_kept_only_where_its_name_starts_with_it (depth 1); TREE_READINGS (depth 1); test_a_report_path_is_read_against_the_bases_tracked_files (depth 1); test_a_same_named_module_every_test_sits_beside_is_not_placed_on_the_file (depth 1); test_a_shorter_same_named_path_is_not_placed_on_the_file (depth 1); MIXIN (depth 1); test_a_test_another_module_inherits_is_not_placed_on_the_defining_file (depth 1); test_a_test_a_file_inherits_from_a_helper_is_placed_on_that_file (depth 1) |
| Needs a fix | yes — 🟡 1 (an exact placement still reaches a same-named file when every test shares its directory, or at a negative offset with the rootdir at the run directory), 🟡 2 (`file` is the defining file, so an inherited test is placed on the wrong module), 🟡 3 (rule 3 names two of the four runners the collection pass cannot count). |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round over round 1's fixes (3f90f333..78becaaf): round 1's probes P1–P7 re-run at the target, the base and 225af880; placement judged by construction over the tree-layout axis (rootdir placement, same-named modules or packages at other depths, configured rootdirs, xdist, an absent `file`, Windows separators); the collection pass's new prefixes against runners that already pass arguments, a preset `PYTEST_ADDOPTS` and quoted paths; rule 3, the SKILL.md bullet, the reasons and the changelog against the code; what changes for this repository's seal.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The exact placement still gives `failing on base too` to a file the base does not fail. A same-named module is placed at a positive offset when every test in the report sits under it (Q1), or at a negative offset while pytest's rootdir is the run directory (Q3). Round 1's first finding is closed for P1 and P2 only | `skills/verify/scripts/broad_gate.py:1977-1983`, `skills/verify/scripts/broad_gate.py:2035-2058` | **fixed** `9639f2ff` | fixed at 9639f2ff; Executed Q1 and Q3 at 8662f9bf (`failing on base too`) and a3aa139a (`new`). The tree-read fix gives `UNPLACED` for both, keeps Q10 and Q11, and runs the three gate modules 499 passed, 1 skipped |
| 🟡 2 | `report_cases` takes `file` as the test's module, but it is the file the test's function is defined in. An inherited test fails at the base under the parent's file (Q4b, permissive), and a file failing through a helper's test reads `new` (Q4c) | `skills/verify/scripts/broad_gate.py:1938-1946` | **fixed** `9639f2ff` | fixed at 9639f2ff; Executed Q4, Q4b and Q4c at the three SHAs. 225af880 read Q4b `new`, so the fix introduced it. With the name check, Q4b `new`, Q4 `UNPLACED` and Q4c `failing on base too` |
| 🟡 3 | Rule 3, the docstring and the changelog name two runners the collection pass cannot count, and the class has four. A runner before the measured one whose command line names `--junitxml` (Q8, executed) and one whose environment drops `PYTEST_ADDOPTS` (constructed) are missing | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2258-2265` | **fixed** `9639f2ff` | fixed at 9639f2ff; Executed Q8: `failing on base too` at 8662f9bf, `new` at a3aa139a, no `runners-at-base-1.xml` written |
| ⬜ 4 | Two test-module comments attach a rootdir of `tests` to the fixtures, whose rootdir is the repository root, and P2's offset is 2, not 1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4274`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:5229` | **fixed** `9639f2ff` | fixed at 9639f2ff; Executed: every kept fixture report names `file="tests/…"` |
| ⬜ 5 | Rule 3's "`--junitxml` included" does not cover the appended `-o junit_family=xunit1`, so a wrapper that forwards only known options reads `NO_RUNNER` | `templates/config.md:333` | **fixed** `9639f2ff` | fixed at 9639f2ff; Executed Q12: `NO_RUNNER` at 8662f9bf, `failing on base too` at 225af880 and a3aa139a. A safe direction |
| ⬜ 6 | `overview.md` Not done names one open placement shape; Q1, Q3 and Q4b are three more | `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/overview.md` | answered | corrected at 9639f2ff: `overview.md` §*Not done* says what is open after this pass; A correction to this run's paperwork, not counted in Needs a fix |
| 🟢 | round 1's second finding is closed for P3 — a runner that drops its arguments before the measured one is counted through `PYTEST_ADDOPTS` | `skills/verify/scripts/broad_gate.py:2330-2337` | confirmed | Executed P3 `sh -c`: `MULTI_RUNNER` (parts 3 and 1), `runners-at-base-1.xml` kept; 225af880 `failing on base too`, a3aa139a `new` |
| 🟢 | round 1's third finding is closed — what the collection pass runs is stated where a row's author reads it | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2243-2256`, `changelog.md` | confirmed | Executed P5: markers `AA` and `B` at 8662f9bf and 225af880, none at a3aa139a, which is what the three texts now say |
| 🟢 | round 1's fourth finding is closed — the `NOTHING_TOGETHER` reason and the rule-3 sentence for a file the root carries | `skills/verify/scripts/broad_gate.py:1899-1903`, `templates/config.md:333` | confirmed | Executed P4: `NOTHING_TOGETHER` and `UNPLACED`, unchanged; the reason is pinned in `test_the_unmeasured_word_says_so_and_every_reader_is_told_it` |
| 🟢 | The counting change turns no one-runner row into `MULTI_RUNNER`, survives a preset `PYTEST_ADDOPTS` and a keep path with spaces, and the family option wins over a row, environment or ini that sets one | `skills/verify/scripts/broad_gate.py:2298-2338` | confirmed | Executed Q7, Qs2, Qf1, Qf2 and Qf3; the twice-counted case by construction (Findings from reading) |
| 🟢 | A green run is unchanged, and this repository's row pays two `uvx ruff` prefixes once more only on a failing gate | `skills/verify/scripts/broad_gate.py:3487-3491`, `seal/config.md` | confirmed | Read |
| ❓ | Windows (backslash `file` paths, `cmd.exe` quoting of the family option, `shlex.quote` with backslashes in `PYTEST_ADDOPTS`) and the `file` attribute on pytest 7 and 8 | `skills/verify/scripts/broad_gate.py:1870-1877`, `skills/verify/scripts/broad_gate.py:2330-2337` | ❓ out of verified scope | Read only, on macOS with pytest 9.1.1. CI's three-platform test job answers Windows; the repository owner answers whether pytest 7 and 8 matter |

## Paste-ready fixes

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
```
A test is placed on a file by the path pytest's report gives it (the gate also appends `-o junit_family=xunit1`, which writes that path), read against the files the base tracks: pytest's rootdir is a directory under which every such path is a tracked file, the directory the row runs pytest in is one under which every file the run was handed is, and the test is placed on the file only where each is one directory and the two name one file. Where the base tracks a second directory that fits either, the file reads `new?`.
```
```
  A file reads `failing on base too` only where the report places a failing
  or erroring test on that file and no other, by the file's path read against
  the files the base tracks. The gate also appends `-o junit_family=xunit1`,
  which makes pytest write each test's file as a path, so a package or a class
  named like a module is never taken for it. Where the base tracks a
  same-named file the path could also name, from another rootdir or another
  directory the row could run pytest in, the file reads `new?`.
```
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
```
That path is the file a test's function is defined in, so a test a class inherits from another module is placed by its dotted name instead, which cannot tell a module from a package of the same name.
```
```
Where another part does, the collection pass counts a runner before the one that wrote the report through `PYTEST_ADDOPTS`, which counts it only where it writes the report that variable asks for. Four shapes stay uncounted (#807): a runner given `-p no:junitxml`, which refuses the option from either source; one whose own command line names `--junitxml`, which wins over `PYTEST_ADDOPTS`; one started in an environment that does not carry `PYTEST_ADDOPTS`; and a runner after the one that wrote the report inside a part that drops its arguments. Such a row is read as one with a single runner, and a file can read `new` from the other runner's directory, or `new?` where the base tracks it in both.
```
```
    Nor does it count a runner given `-p no:junitxml`, which refuses the
    option from either source, one whose own command line names
    `--junitxml`, which wins over the environment, one started in an
    environment without `PYTEST_ADDOPTS`, or a later runner inside a part
    that drops its arguments (#807).
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:1932-2023` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2277-2316`, `templates/config.md` rule 3 | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2262-2316`, `templates/config.md` rule 3, `changelog.md` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:1886-1890`, `templates/config.md` rule 3 | round 1's 🟡 4 — fixed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py` S1–S5 cases | round 1's 🟢 — confirmed |
| round-1 | `overview.md` §*Where spec and implementation diverged* | round 1's 🟢 — confirmed |
| round-1 | `seal/config.md` row, `.github/scripts/run_tests.py:644` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:1906-1938` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #807's body lists two uncounted runners. It should also list a runner before the measured one whose command line names `--junitxml` (Q8), and one whose environment drops `PYTEST_ADDOPTS` | #807, as an edit to its list | the orchestrator, who files and edits issues |
