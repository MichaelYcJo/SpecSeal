# 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict — review round 1

| Field | Value |
|---|---|
| Target SHA | 225af880cea7c4645652add1cb2cb0e530805635 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #804 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (dotted-name placement gives `failing on base too` to a file with no test at the base), 🟡 2 (a runner that does not take the gate's arguments is passed over or not counted), 🟡 3 (rule 3 understates what the collection pass runs at the base), 🟡 4 (the `NOTHING_TOGETHER` reason and one rule-3 sentence are false for an existing module with no test). |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Spec compliance first against `spec.md` (the base's verdict read from a `--junitxml` report the gate-addressed pytest writes; the text readers retired with every 0.18.2 word assertion kept; the collection pass and `MULTI_RUNNER`; args-dropping parts read `new?`; what 0.18.2 built kept), then quality: the overview's divergences on their grounds; whether any verdict is still permissive, by construction over report shapes (pytest versions, xdist, import modes, doctest, rootdir placement, ids, collection errors, the option already given or refused, Windows paths); the collection pass's side effects and cost; what changes for this repository's seal.

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

## Paste-ready fixes

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
```
A test is placed on a file by the path pytest's report gives it (the gate adds `-o junit_family=xunit1`), at one offset between pytest's rootdir and the directory the row runs pytest in; a file named at two offsets, or at one not every test in the report shares, reads `new?`. Where pytest's rootdir sits below that directory, a same-named file a directory up that the row also collects can still be placed on a file the base holds no test in.
```
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
```
A part that does not hand the appended arguments on to pytest — a `sh -c '…'`, a `make` target, a wrapper that drops its arguments or refuses an option it does not know, a runner given `-p no:junitxml` — writes no report where the gate asked for one, so where no other part of the row runs pytest each file reads `new?`. Where another part does, the collection pass counts a runner before the one that wrote the report through `PYTEST_ADDOPTS`, but not one given `-p no:junitxml`, and not a runner after it that drops its arguments; such a row is read as one with a single runner, and a file can read `new` or `failing on base too` from the other runner's directory. Write such a part so it passes its arguments on, `--junitxml` included.
```
```
To count the runners, every other prefix runs once more at the base with ` --collect-only` added to `PYTEST_ADDOPTS`, kept as `runners-at-base-<j>.txt`: a prefix after the one whose report settled the walk with only its own `--junitxml` appended, and a prefix before it with nothing appended and its `--junitxml` carried in `PYTEST_ADDOPTS`. Only pytest honours `--collect-only`: every other part of those prefixes runs as written at the base, once for each prefix that holds it, and that includes a part after the runner that the branch's own run never reached because its suite failed first. This happens once per comparison and only on a failing gate; a row whose only part runs pytest pays nothing, and a part after the runner that writes outside the repository writes there at the base too.
```
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
```
so such a file the base holds with no test in it reads `new` too: the base cannot fail a test it does not have. A file the root carries runs with the others, and one with no test in it at the base reads `new?`
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Counting a later runner that drops its arguments (P7) and an earlier one given `-p no:junitxml`. Per-directory report paths (pytest expands `$PWD` in the `--junitxml` path) are one direction, and they would not reach `cmd.exe` | a new issue, if the owner wants these rows measured rather than named in rule 3 | the repository owner |
| A negative offset still accepts a same-named module a directory up (🟡 1's fix closes the positive offsets only) | rule 3's named limits, by 🟡 1's fix | the smith in the fix pass |
