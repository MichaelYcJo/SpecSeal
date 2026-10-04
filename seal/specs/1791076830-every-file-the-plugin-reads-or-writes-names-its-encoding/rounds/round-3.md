# 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding — review round 3

| Field | Value |
|---|---|
| Target SHA | 42db96397ce676dcfa551239bb6bd6ac5f647e48 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #757 |
| Broad gate | 1e443ea2 against e141980a |
| Fixes checked by | no fixes to check |
| Fix range | `42db96397ce676dcfa551239bb6bd6ac5f647e48..d74b92aa028b9e915d2c36c0ef3e6d7c544d2bda`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (`zipfile.Path.open` called on its class passes as named) and 🟡 2 (a local named after one of six modules has its `.open()` excused) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item `1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding` (#741, PR #757). This is the verifying round for round 2's fixes, over the range `de952182..7bfee70c`. Round 1 met the floor and round 2 was the one reopening, so this record ends the run whatever it finds. A finding left open takes the filing ladder and needs a `Who answers it`.

Open each fix and judge whether its round-2 verdict is closed:
- 🟡1: the `default_loader` branch is removed, and its text call is a `NAMED` row.
- ⬜2: `owner` again excuses a bare name that no import binds. `dbm.dumb` is a `NOT_A_FILE_OPENER` row, and the docstrings now say that only a constructor in the receiver slot is excused.
- ⬜3: a `zipfile.Path.open` row in `OPENERS`, with a branch in the `.open` path.
- ⬜4: the "What no row can hold" list.
- ⬜5: the record correction.

The fix pass added no unit. Its changes are rows on existing tables and edits inside the bodies of `judge` and `owner`. Watch the restored bare-name exclusion in particular. A name bound by something other than an import, such as a parameter or an assignment, should not excuse a real `open` that reads with the locale's encoding.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `zipfile.Path.open` sits in `OPENERS`, which the top of `judge` matches before the `.open` branch, so the class-called form is judged with no path shift and `zipfile.Path.open(q, "r")` passes as named | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:314` | deferred #762 | #762 — the run is capped: round 2 was its one reopening, and this record ends it; Executed: three unbound spellings return no site at the target and are reported at `de952182` and `839d19a9`; the line-765 `NAMED` case passes on `"r"` read as the encoding. Fix applied in the scratch clone: 122 passed, ruff clean. Who answers it: #741's branch, before PR #757 is marked ready; the walker's `judge` is a unit this work item created |
| 🟡 2 | The restored bare-name branch of `owner` excuses `.open()` on any local named `os`, `webbrowser`, `tarfile`, `shelve`, `dbm` or `wave`; before round 1 only the first two were; the docstring says any bare name | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:405` | deferred #762 | #762 — the run is capped: round 2 was its one reopening, and this record ends it; Executed: `wave`, `tarfile` and `shelve` locals holding a path return no site at the target and are reported at `839d19a9` and `de952182`. Read: `839d19a9`'s set held two names. Fix applied in the scratch clone: 122 passed. Who answers it: #741's branch, before PR #757 is marked ready; `owner` is a unit this work item created |
| ⬜ 3 | A `zipfile.Path` reached by `/`, `.joinpath` or a name is judged at `Path.open`'s positions, though the docstring says any `zipfile.Path` is judged as `zipfile.Path.open` | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:32` | deferred #762 | #762 — carried with the two yellows it sits beside; Executed at the target and with 🟡 1 and 🟡 2's fixes applied. An over-report, none in the tree. Who answers it: #741's branch, with 🟡 1's edit |
| ⬜ 4 | `dbm.gnu`, `dbm.ndbm` and `dbm.sqlite3` are reported though they open no text; the fix for round 2's finding 2 added `dbm.dumb` alone | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:134` | deferred #762 | #762 — carried with the two yellows it sits beside; Executed at the target for all three. An over-report, none in the tree. Who answers it: #741's branch, with 🟡 2's edit |
| ⬜ 5 | Correction: `spec.md`'s K1 row says `.open` on a bare name no import binds is excused, the same over-wide sentence as 🟡 2 | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/spec.md:86` | deferred #762 | #762 — `spec.md`'s K1 row and the module docstring are corrected together with 🟡 2's code, so the two never disagree; Read. Paperwork, so a correction. Who answers it: #741's branch, with 🟡 2's docstring edit |
| 🟢 | round 2's finding 1 is closed — `ElementInclude.default_loader` is no longer a K1 row and its text call is a `NAMED` case | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:24` | confirmed | Read: the loader's 3.12 source sets UTF-8 when `encoding` is falsy, and the branch is gone from `judge`. Executed: the text call returns no site at the target, and was reported at `de952182` |
| 🟢 | round 2's finding 2 is closed for what it named — the docstring says a `ZipFile` or `TarFile` built in the receiver, `dbm.dumb` is excused, and an unimported `os` is excused again | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:33` | confirmed | Executed: `dbm.dumb` by three import spellings and `def f(os)` return no site at the target. The fix reaches further than it says; that is this round's 🟡 2 and ⬜ 4 |
| 🟢 | round 2's finding 3 is closed for what it named — `zipfile.Path(z).open("r", "utf-8")` is not reported | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:191` | confirmed | Executed at the target, with the `from zipfile import Path` spelling as well. The unbound form the same row broke is this round's 🟡 1 |
| 🟢 | round 2's finding 4 is closed — *What no row can hold* names `dictConfig` and a handler subclass's `super().__init__` | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:57` | confirmed | Read |
| 🟢 | round 2's finding 5 is closed — the changelog counts two one-liners handed to a session, and `spec.md` names the CI step beside them | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:3` | confirmed | Read, with `spec.md:72` |

## Paste-ready fixes

```diff
--- a/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
+++ b/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
@@ def judge(call, bound):
     target = target_of(call.func, bound)
     func = call.func

-    if target in OPENERS:
+    # `zipfile.Path.open` is a method: called on its class it is judged in the
+    # `.open` branch below, where its path moves every position one right.
+    if target in OPENERS and target != "zipfile.Path.open":
         return judge_opener(call, target)
```
```diff
--- a/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
+++ b/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
@@ UNNAMED = {
+    "zipfile.Path open unbound, mode only": (
+        'import zipfile\nzipfile.Path.open(q, "r")',
+        "zipfile.Path.open()",
+    ),
     "zipfile.Path open is still judged": (
```
```diff
--- a/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
+++ b/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
@@ def owner(receiver, bound):
     if isinstance(receiver, ast.Call):
         return dotted(receiver.func, bound)
     if isinstance(receiver, ast.Name) and receiver.id not in bound:
-        return receiver.id
+        # Only the two modules excused before round 1; a local named after
+        # any other module is a value the walk cannot prove (K2).
+        return receiver.id if receiver.id in ("os", "webbrowser") else None
     return dotted(receiver, bound)
```
```diff
--- a/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
+++ b/tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py
@@ UNNAMED = {
+    "a local named after a module is judged": (
+        "wave = make(p)\nwave.open()",
+        "<expr>.open()",
+    ),
     "zipfile.Path open is still judged": (
```
```diff
-  `Image` and a `ZipFile(...)` or `TarFile(...)` built in the receiver
-  itself, which open no text, and on a bare name no import binds; called on
-  the class (`Path.open(p)`), every position moves one to the right;
+  `Image` and a `ZipFile(...)` or `TarFile(...)` built in the receiver
+  itself, which open no text, and on `os` or `webbrowser` where no import
+  binds the name; called on the class (`Path.open(p)`), every position moves
+  one to the right;
```
```diff
-    class a receiver call constructs (`zipfile.ZipFile(z)`), or a bare name no
-    import binds, read as itself (`os` taken as a parameter). An instance
-    bound to a name first (`with ZipFile(z) as zf`) is not traced."""
+    class a receiver call constructs (`zipfile.ZipFile(z)`), or `os` or
+    `webbrowser` where no import binds the name (`os` taken as a parameter).
+    Any other bare name no import binds is unproven, so it is None. An
+    instance bound to a name first (`with ZipFile(z) as zf`) is not traced."""
```
```diff
-- `<expr>.open(...)` judged as `Path.open`, or as `zipfile.Path.open`,
-  whose encoding comes one place earlier, on a `zipfile.Path`; except on
+- `<expr>.open(...)` judged as `Path.open`, or as `zipfile.Path.open`,
+  whose encoding comes one place earlier, on a `zipfile.Path(...)` built in
+  the receiver itself (one reached by `/`, `.joinpath` or a name is judged
+  as `Path.open`); except on
```
```diff
     "dbm.dumb",
+    "dbm.gnu",
+    "dbm.ndbm",
+    "dbm.sqlite3",
     "wave",
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the encoding module at the target, in the scratch clone, with `-p no:xdist` | 120 passed |
| A probe of 30 spellings through `unnamed_sites` at `839d19a9`, `de952182` and the target | at the target, 12 disagree with what the call reads: 6 missed (🟡 1 three, 🟡 2 three) and 6 over-reported, of which 3 are ⬜ 3 and 3 are ⬜ 4. The 🟡 1 and 🟡 2 shapes are reported at both earlier SHAs |
| The two new `UNNAMED` sources through `unnamed_sites` at the target | both return no site, which is the red the cases need |
| 🟡 1, 🟡 2 and ⬜ 4's fixes plus the two `UNNAMED` cases, applied in the scratch clone; then `bin/test` on the module, `uvx ruff check` and `uvx ruff format --check` on it | 122 passed; clean; clean |
| The same 30 spellings with those fixes applied | every one agrees except ⬜ 3's three over-reports, which the fixes do not touch |
| `bin/evidence-check .` at the target | 4401 ok · 0 drifted · 0 broken; records half 0 refused |
| The full suite | not yet. The sealer runs it once, after the rounds settle; nothing in this round ran it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:262` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:102` | round 1's 🟡 2 — fixed |
| round-1 | `skills/update/SKILL.md:45` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:16` | round 1's ⬜ 4 — fixed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:100` | round 1's ⬜ 5 — fixed |
| round-1 | `CONTRIBUTING.md:271` | round 1's ⬜ 6 — fixed |
| round-1 | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:18` | round 1's ⬜ 7 — answered |
| round-1 | `hooks/commit-review-gate.py:590` | round 1's 🟢 — confirmed |
| round-1 | `hooks/git/pre-commit.py:47` | round 1's 🟢 — confirmed |
| round-1 | `hooks/git/post-commit.py:24` | round 1's 🟢 — confirmed |
| round-1 | `hooks/git/reference-transaction.py:27` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:213` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_commit_gate_decides_at_the_commit.py:73` | round 1's ❓ — out of verified scope |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:330` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:32` | round 2's ⬜ 2 — fixed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:138` | round 2's ⬜ 3 — fixed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:49` | round 2's ⬜ 4 — fixed |
| round-2 | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:3` | round 2's ⬜ 5 — answered |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:376` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:142` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:153` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:23` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — `zipfile.Path.open` called on its class passes as named | not placed by this round; the orchestrator places it on the ladder. Candidate: rung 1, since `judge` is a unit this work item created | #741's branch, before PR #757 is marked ready |
| 🟡 2 — the bare-name branch of `owner` excuses six module spellings | not placed by this round; the orchestrator places it on the ladder. Candidate: rung 1, since `owner` is a unit this work item created | #741's branch, before PR #757 is marked ready |
