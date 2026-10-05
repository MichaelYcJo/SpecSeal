# 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict — review round 3

| Field | Value |
|---|---|
| Target SHA | 56c8eb0d371216a12e67f271c0541e004bd7a21a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #804 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `3a98dcf56814634ffcf52b9f489a54f71b46a808..3a98dcf56814634ffcf52b9f489a54f71b46a808`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a dotted-name placement is never read against the tree: an inherited test or a `--junit-prefix` row reopens P1 and Q1), 🟡 2 (a test file the row generates moves the rootdir to a vendored directory), 🟡 3 (rule 3, the docstring and the changelog promise `new?` for a file tracked under both runners' directories, which holds only where every failing file of its run is). |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round over round 2's fixes (562ab360..bf8669c2), and the last round this item gets: rounds 1–2's verdicts inherited and checked (P1–P7 and Q1–Q12 at the target, the base, 225af880 and 8662f9bf); the smith's measured divergence on P7 and its sentence; the tree reading judged by construction (rootdir and run-directory rules × tracked or untracked files × same-named packages and modules × submodules and sparse checkouts × unusual paths); the `file` prefix check against parametrized ids, nested classes and doctest items; a whole-item pass over every shape any round ran; the seal.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A dotted-name placement is never read against the tree. An inherited test, and every test under `--junit-prefix`, falls back to the offset rule, and P1's package and Q1's deeper module are placed on a module the base holds no test in. A regression against a3aa139a, introduced by 9639f2ff | `skills/verify/scripts/broad_gate.py:1952`, `skills/verify/scripts/broad_gate.py:2113-2116` | deferred #812 | #812 — the run is capped; fixed post-review on this branch, and #812 is what that fix closes; Executed R1, R1-ini, R2, R2b: `failing on base too` at 56c8eb0d, `new` at a3aa139a, `UNPLACED` at 8662f9bf and with the fix |
| 🟡 2 | The tree is the base's tracked files, so a test file the row generates is missing and a vendored directory holding every report path is taken for the rootdir. The root's failing test is placed on the handed file. A regression against a3aa139a, and rule 3 promises `new?` | `skills/verify/scripts/broad_gate.py:2357`, `skills/verify/scripts/broad_gate.py:2011-2029`, `templates/config.md:333` | deferred #812 | #812 — fixed with 🟡 1 post-review; Executed R3: `failing on base too` at 56c8eb0d, 225af880 and 8662f9bf, `new` at a3aa139a, `UNPLACED` with the fix |
| 🟡 3 | "A file the base tracks under both runners' directories reads `new?`" is false where another failing file of its run is tracked under the measured runner's directory only. The word is the base's; the sentence is new, in four places and a pin | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2329-2334`, `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/changelog.md` | deferred #812 | #812 — the sentence follows the post-review fix; Executed P7-mixed: `tests/test_y.py` `failing on base too` at all four SHAs |
| ⬜ 4 | The `UNPLACED` reason's parenthetical does not name a second directory that fits the run, which the tree reading added | `skills/verify/scripts/broad_gate.py:1897-1901` | deferred #812 | #812 — the reason text follows the post-review fix; Read; Q10b reads the reason while the report names the file's test |
| ⬜ 5 | `overview.md` §*Not done* says every pytest writes `file` and that an untracked test file makes the run read `new?`; the target drops `file` under `--junit-prefix`, and R3 reads `failing on base too` | `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/overview.md` | deferred #812 | #812 — the overview follows the post-review fix; A correction to this run's paperwork, not counted in Needs a fix |
| 🟢 | round 2's first finding is closed — Q1, Q3 and Q3b are not placed on the handed file, and Q10 and Q11 keep their words | `skills/verify/scripts/broad_gate.py:2003-2029`, `skills/verify/scripts/broad_gate.py:2099-2112` | confirmed | Executed Q1, Q3, Q3b `UNPLACED`; Q10, Q11 `failing on base too`; Q10b `UNPLACED` |
| 🟢 | round 2's second finding is closed — an inherited test is not placed on the defining file | `skills/verify/scripts/broad_gate.py:1945-1955` | confirmed | Executed Q4 `UNPLACED`, Q4b `new`, Q4c `failing on base too` |
| 🟢 | round 2's third finding is closed — the four uncounted runners are named in rule 3, the docstring and the changelog | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2321-2329` | confirmed | Read; Q8 executed, `UNPLACED` |
| 🟢 | round 2's fourth and fifth findings are closed — the fixture comments and the wrapper sentence | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4142`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:4275`, `templates/config.md:333` | confirmed | Read; Q12 executed, `NO_RUNNER` |
| 🟢 | The smith's measured divergence: P7 in #761's p1b layout reads `failing on base too`, as the base does | `templates/config.md:333` | confirmed | Executed P7-p1b at four SHAs; the sentence built on it is 🟡 3 |
| 🟢 | The `file` check holds for nested classes, parametrized ids, doctest modules and text files, dotted directories and collection errors | `skills/verify/scripts/broad_gate.py:1945-1955` | confirmed | Executed against real `xunit1` reports, and R5 end to end |
| 🟢 | A green run is unchanged | `skills/verify/scripts/broad_gate.py:3561-3564` | confirmed | Read; a green gate at the target executed |
| 🟢 | round 2's confirmed rows still hold — P3 `MULTI_RUNNER`, P5's cost, P4's reason, the counting change | `skills/verify/scripts/broad_gate.py:2402-2441` | confirmed | Executed P3, P4, P5, Q7, Qf, Qs2 |
| ❓ | Windows (backslash `file`, `cmd.exe` quoting, `shlex.quote` in `PYTEST_ADDOPTS`) and the `file` attribute on pytest 7 and 8 | `skills/verify/scripts/broad_gate.py:1870-1880` | ❓ out of verified scope | Read only, on macOS with pytest 9.1.1. CI's three-platform job answers Windows; the repository owner answers pytest 7 and 8 |

## Paste-ready fixes

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ -2029,6 +2029,20 @@ def directories_holding(addresses, tree):
     return found


+def spelled(name, roots, tree):
+    """The one module the leading components of the dotted name `name` spell
+    as a file the base tracks under one of `roots`, split at `/`, or None
+    where they spell none or more than one (#789 round 3). A module and a
+    package of the same name are both tracked, which is the case a dotted
+    name alone could not tell apart."""
+    found = set()
+    for k in range(1, len(name) + 1):
+        address = (*name[: k - 1], f"{name[k - 1]}.py")
+        if any(joined(d, address) in tree for d in roots):
+            found.add(address)
+    return found.pop() if len(found) == 1 else None
+
+
 def report_words(text, files, code, stopped, alone=False, tree=None):
@@ -2099,8 +2113,20 @@ def report_words(text, files, code, stopped, alone=False, tree=None):
     if tree is not None:
         roots = directories_holding({a for a, _, e in cases if e}, tree)
         heres = directories_holding({paths[f][True] for f in files}, tree)
+        # A dotted name — an inherited test, or every test under a
+        # `--junit-prefix` — is read against the tree too: the one module it
+        # spells becomes its path, and one that spells none or more than one
+        # places nothing (#789 round 3).
+        cases = [
+            (address, failed, True)
+            if exact
+            else (spelled(address, roots, tree), failed, True)
+            for address, failed, exact in cases
+        ]
     for address, failed, exact in cases:
         hit = set()
+        if address is None:
+            continue
         for f in files:
             if exact and tree is not None:
                 tests = {joined(d, address) for d in roots}
@@ -2352,9 +2378,6 @@ def compare_at_base(root, base, command, files, keep):
             f for f in files if git(scratch, "cat-file", "-e", f"HEAD:{f}") is None
         ]
         others = [f for f in files if f not in candidates]
-        # The base's tracked paths, which a report's `file` is read against
-        # (`report_words`, #789 round 2's 🟡 1).
-        tree = frozenset((git(scratch, "ls-files", "-z") or "").split("\0")) - {""}
         # One group of every other file, kept as `suite-at-base-<k>.txt`, then
@@ -2413,6 +2436,13 @@ def compare_at_base(root, base, command, files, keep):
                         second = k
                         break
                     continue
+                # The base's files after this run, tracked or not, which a
+                # report's `file` is read against (`report_words`): a test
+                # file the row generated is one pytest named, so its rootdir
+                # is among the directories holding every report path (#789
+                # round 3).
+                listed = git(scratch, "ls-files", "-z", "--cached", "--others")
+                tree = frozenset((listed or "").split("\0")) - {""}
                 words = report_words(
```
```
A test is placed on a file by the path pytest's report gives it (the gate also appends `-o junit_family=xunit1`, which writes that path), read against the files in the base's worktree after the run, tracked or written by the run: pytest's rootdir is a directory under which every such path is a file, the directory the row runs pytest in is one under which every file the run was handed is, and the test is placed on the file only where each is one directory and the two name one file. Where a second directory fits either, the file reads `new?`. That path is the file a test's function is defined in, so a test a class inherits from another module, and every test of a run under `--junit-prefix`, is placed by its dotted name instead, read against the same files: the one module the name spells is its file, and a name that spells both a module and a package of the same name, or no file, places nothing.
```
```
  A file reads `failing on base too` only where the report places a failing
  or erroring test on that file and no other, by the file's path read
  against the files in the base's worktree after the run, tracked or written
  by the run. The gate also appends `-o junit_family=xunit1`, which makes
  pytest write each test's file as a path, so a package or a class named
  like a module is never taken for it. Where a same-named file the path
  could also name sits under another rootdir or another directory the row
  could run pytest in, the file reads `new?`. That path is where a test's
  function is defined, so a test a class inherits from another module, and
  every test under `--junit-prefix`, is placed by its dotted name instead,
  read against the same files: a name that spells both a module and a
  package of the same name places nothing.
```
```
such a row is read as one with a single runner: where the base tracks every failing file of a run under both runners' directories, each reads `new?`, and where it tracks any one of them under the first runner's directory only, every file of that run is measured there and can read `new` or `failing on base too` from the first runner's directory.
```
```
Such a row is read as one with a single runner: where the base tracks every failing file of a run under both runners' directories, each reads `new?`, and where it tracks any one of them under the measured runner's directory only, every file of that run is measured there, so each can read `new` or `failing on base too` from the wrong runner.
```
```
    Such a row is read as one with a single runner. Where the base tracks
    every failing file of a run under both runners' directories, each reads
    `new?`, because `report_words` reads the run directory off every handed
    file (#789 round 2); where it tracks any one of them under the measured
    runner's directory only, every file of that run is measured there, and
    can read `new` or `failing on base too` from the wrong runner, which is
    #761's p1b.
```
```
  In such a row, where the base tracks every failing file of a run under
  both runners' directories, each reads `new?`. Where it tracks any one of
  them under the measured runner's directory only, every file of that run
  is measured there, and can read `new` or `failing on base too` from the
  wrong runner.
```
```
UNPLACED = (
    f"{NOT_MEASURED}: pytest's report at the base does not place a test on "
    "this file alone (it names none of this file's tests, a failing test it "
    "names could be this file or another one, or a second directory of the "
    "base fits the run)"
)
```

## Executed probes

| What was run | Result |
|---|---|
| P1–P7 and Q1–Q12 end to end through the gate, in four `git clone --no-local` copies at 56c8eb0d holding the gate of 56c8eb0d, a3aa139a, 225af880 and 8662f9bf, on one probe file built on the module's helpers | All probe cases ran at each SHA (exit 0). The words are in the table below |
| This round's shapes R1–R6 and P7-mixed at the same four SHAs | The table below |
| A fifth copy with the fix below applied, every probe rerun | The last column of the table |
| The four regression cases and three tree rows below, at the target and with the fix | 5 failed at 56c8eb0d (each `'failing on base too' == UNPLACED`), 6 passed with the fix |
| `bin/test`'s five modules (`test_the_seal_is_taken_once_by_the_sealer.py`, `test_the_gate_hands_cmd_a_path_it_can_run.py`, `test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, `test_release_hygiene.py`, `test_a_record_states_what_the_tree_has.py`), run with the copy's venv and `-n 8` | 664 passed, 1 skipped (exit 0) at 56c8eb0d and the same with the fix |
| `report_cases` over real pytest 9.1.1 `xunit1` reports: nested classes, parametrized ids, doctests, `--junit-prefix`, a collection error, a test outside the rootdir | every case exact except `--junit-prefix` (all) and the outside test |
| `git ls-files` with a submodule, under a sparse checkout, and in a worktree added from it; `ls-files --cached --others` with an ignored file | gitlink only; every index entry; patterns inherited; ignored file listed |
| `uvx ruff check` and `uvx ruff format --check` on the target's two touched modules, and on the fixed gate | clean |
| The broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

```
probe / file                                56c8eb0d              a3aa139a              225af880              8662f9bf              with the fix
P1 tests/test_api.py                        UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
P2 tests/test_two.py                        UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
P3-nojunit tests/test_two.py                UNPLACED              new                   failing on base too   failing on base too   UNPLACED
P3-sh tests/test_two.py                     MULTI_RUNNER (3, 1)   new                   failing on base too   MULTI_RUNNER (3, 1)   MULTI_RUNNER (3, 1)
P4-files tests/test_two.py                  NOTHING_TOGETHER      NO_RUNNER             NOTHING_TOGETHER      NOTHING_TOGETHER      NOTHING_TOGETHER
P4-suite tests/test_two.py                  UNPLACED              new                   UNPLACED              UNPLACED              UNPLACED
P5 tests/test_two.py                        failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P5 marker (parts after the runner)          AAB                   (nothing)             AAB                   AAB                   AAB
P6 tests/test_two.py                        failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P7-both tests/test_x.py                     new                   new                   new                   new                   new
P7-both tests/test_y.py                     UNPLACED              failing on base too   failing on base too   failing on base too   UNPLACED
P7-both tests/test_z.py                     UNPLACED              new                   new                   new                   UNPLACED
P7-mixed tests/test_y.py                    failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P7-mixed tests/test_w.py                    new                   new                   new                   new                   new
P7-p1b tests/test_x.py                      new                   new                   new                   new                   new
P7-p1b tests/test_y.py                      failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
P7-p1b tests/test_z.py                      new                   new                   new                   new                   new
Q1 tests/test_two.py                        UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q2 sub/tests/test_two.py                    failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q3 a/tests/test_two.py                      UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q3b a/b/tests/test_two.py                   UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q4 tests/test_two.py                        UNPLACED              new                   UNPLACED              failing on base too   UNPLACED
Q4b tests/test_two.py                       new                   new                   new                   failing on base too   new
Q4c tests/test_two.py                       failing on base too   failing on base too   failing on base too   new                   failing on base too
Q5 tests/test_api.py (-n 2)                 UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Q7 tests/test_two.py                        failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q8 tests/test_two.py                        UNPLACED              new                   failing on base too   failing on base too   UNPLACED
Q10 tests/test_two.py                       failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q10b tests/test_two.py                      UNPLACED              failing on base too   failing on base too   failing on base too   UNPLACED
Q11 sub/tests/test_two.py                   failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
Q12 tests/test_two.py                       NO_RUNNER             failing on base too   failing on base too   NO_RUNNER             NO_RUNNER
Qf-row tests/test_api.py                    UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Qf-env tests/test_api.py                    UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Qf-ini tests/test_api.py                    UNPLACED              new                   failing on base too   UNPLACED              UNPLACED
Qs tests/test_two.py (-rN preset)           no comparison         no comparison         no comparison         no comparison         no comparison
Qs2 tests/test_two.py                       MULTI_RUNNER (3, 1)   new                   failing on base too   MULTI_RUNNER (3, 1)   MULTI_RUNNER (3, 1)
R1-prefix tests/test_api.py                 failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R1-prefix-ini tests/test_api.py             failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R2-inherited-package tests/test_api.py      failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R2b-inherited-deeper tests/test_two.py      failing on base too   new                   failing on base too   UNPLACED              UNPLACED
R3-generated vendor/tests/test_two.py       failing on base too   new                   failing on base too   failing on base too   UNPLACED
R4 tests/sp ace/test_sp.py                  not compared          not compared          not compared          not compared          not compared
R4 tests/test_é.py                          failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
R5 nested, parametrized, doctest            failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
R6 inherited and own failing test           failing on base too   failing on base too   failing on base too   failing on base too   failing on base too
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
| round-2 | `skills/verify/scripts/broad_gate.py:1977-1983`, `skills/verify/scripts/broad_gate.py:2035-2058` | round 2's 🟡 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:1938-1946` | round 2's 🟡 2 — fixed |
| round-2 | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2258-2265` | round 2's 🟡 3 — fixed |
| round-2 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4274`, `tests/test_the_seal_is_taken_once_by_the_sealer.py:5229` | round 2's ⬜ 4 — fixed |
| round-2 | `templates/config.md:333` | round 2's ⬜ 5 — fixed |
| round-2 | `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/overview.md` | round 2's ⬜ 6 — answered |
| round-2 | `skills/verify/scripts/broad_gate.py:2330-2337` | round 2's 🟢 — confirmed |
| round-2 | `templates/config.md:333`, `skills/verify/scripts/broad_gate.py:2243-2256`, `changelog.md` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:1899-1903`, `templates/config.md:333` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:2298-2338` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:3487-3491`, `seal/config.md` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:1870-1877`, `skills/verify/scripts/broad_gate.py:2330-2337` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A failing file whose path holds a space is never compared at the base: `FAILED_RE` stops at the space, at every SHA including a3aa139a. Strict, outside this change | #813 | the orchestrator, who files issues |
