# Round 3 report — 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding (#741)

| Field | Value |
|---|---|
| Round | 3, the verifying round for round 2's fixes; the record that follows the one reopening, so it ends the run |
| Target SHA | 42db9639 |
| Fix range read | `de952182..7bfee70c` (four commits), plus `42db9639`, which edits `round-2.md` alone |
| Base | `release/v0.18.1` at e141980a |
| Reviewer | specseal:warden on claude-opus-5-5 |
| Where the probes ran | a `git clone --no-local` of the branch at the target, in the session scratchpad; deleted before handover |

## Summary

Every round-2 verdict is closed for the instances it named. Two of the fixes
reach further than their commit message says, and both now let a call that
reads in the locale's encoding pass.

- Round 2's 🟡 1 is closed. The `default_loader` branch is gone, the text
  call is a `NAMED` row, and the loader is listed among the fixed defaults.
  Read: its source on 3.12 sets UTF-8 when `encoding` is falsy. Executed: the
  text call is not reported at the target.
- Round 2's ⬜ 2, ⬜ 3, ⬜ 4 and ⬜ 5 are closed for what they named.
- **🟡 1.** The new `zipfile.Path.open` row sits in `OPENERS`, which the top
  of `judge` matches by dotted name before the `.open` branch is reached. So
  `zipfile.Path.open(q, "r")`, called on the class, is judged without the
  path shift: `"r"` lands in the encoding's slot and counts as an encoding
  named. The call reads in the locale's encoding and is no longer reported.
  It was reported at `de952182` and at `839d19a9`. The `NAMED` case the fix
  added for the unbound form passes for this wrong reason.
- **🟡 2.** The restored bare-name exclusion in `owner` excuses every
  spelling in `NOT_A_FILE_OPENER`, not only `os`. A local named `wave`,
  `tarfile`, `shelve` or `dbm` that holds a path now has its `.open()`
  excused. Before round 1 only `os` and `webbrowser` were excused this way,
  so the commit's *as it was before round 1* is not what the code does. The
  docstring states it wider still: it says `.open` on any bare name no
  import binds is excused, which would include `p.open()`.
- Three ⬜ notes. Two are over-reports in the reach of round 2's ⬜ 2 and
  ⬜ 3 that the fixes did not enumerate. One is a paperwork correction to the
  same sentence in `spec.md`.

Nothing here loses a record or crashes. The walker is a test module, and
every finding is a call it judges wrongly.

## Findings

### 🟡 1 — `zipfile.Path.open` called on its class is judged without the path shift, and a locale read passes

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:314`

`judge` opens with `if target in OPENERS: return judge_opener(call, target)`.
`target` is the call's dotted name. Until this range no `OPENERS` key was a
method, so a method called on its class never matched there. It fell through
to the `.open` branch, where `UNBOUND_RECEIVERS` moves every position one to
the right.

The fix added `"zipfile.Path.open": (0, 1)` to `OPENERS`. Now
`zipfile.Path.open(q, "r")` resolves to that key at the top of `judge`. It is
judged at mode 0 and encoding 1 with no shift. `q` is read as the mode and
`"r"` as the encoding, and an encoding that is not `None` passes. The call
opens the member as text in the locale's encoding, so it reads cp1252 on the
Windows leg. This is the shape the module exists to report.

- Executed, at the target: `zipfile.Path.open(q, "r")`, `Path.open(q, "r")`
  after `from zipfile import Path`, and `z.Path.open(q, "r")` after
  `import zipfile as z` all come back with no site.
- Executed, at `de952182` and at `839d19a9`: all three are reported.
- The `NAMED` case `zipfile.Path open unbound, 3rd positional` (line 765)
  passes for the same wrong reason. Its `"r"` is taken as the encoding, and
  `"utf-8"` is never read. Deleting the `"utf-8"` from it still passes. This
  is the case §15 of the agent contract asks to see red. It cannot be red.
- `zipfile.Path.open(q)` is still reported, but with the kind
  `mode not a literal`, because `q` is read as the mode.

Why it matters: the row was added to stop an over-report, and it converts an
under-report the walk did not have into one it does. Nothing in the tree
calls `zipfile.Path.open` today, so the repository case stays green. The next
call written that way passes on every leg.

The fix: skip that one key at the top of `judge`. The `.open` branch already
resolves the owner, the shift and the `zipfile.Path.open` positions
correctly. Executed in the scratch clone: with the fix, all three unbound
spellings are reported, the named and binary forms are not, and the module
passes 122 cases.

The class, enumerated: the `OPENERS` keys are `builtins.open`, `io.open`,
`codecs.open`, `os.fdopen`, `<expr>.open` and `zipfile.Path.open`. Only the
last is a method that can be called on its class. `<expr>.open` is never a
dotted name. The other tables the top of `judge` matches
(`ALWAYS_UNNAMED`, `BINARY_BY_DEFAULT`, `TEXT_ALWAYS`, `TEXT_UNLESS_BINARY`)
hold functions and constructors only. So the class is this one key.

### 🟡 2 — a local named after one of six modules has its `.open()` excused

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:405`

`owner` now returns a bare name no import binds as itself. `judge` then
checks it against `NOT_A_FILE_OPENER`. That set grew in round 1 from
`{"os", "webbrowser"}` to ten entries, and six of them are bare names: `os`,
`webbrowser`, `tarfile`, `shelve`, `dbm` and `wave`. A parameter, loop
variable or assignment with one of those names now has its `.open()`
excused, whatever it holds.

- Executed, at the target: `def f(wave): return wave.open()`,
  `for tarfile in d.glob("*"): tarfile.open()`, and
  `shelve = P(x); shelve.open("w")` come back with no site.
- Executed, at `839d19a9` (before round 1) and at `de952182`: all three are
  reported.
- Read: at `839d19a9`, `judge` read `bound.get(receiver.id, receiver.id)`
  against a set holding `os` and `webbrowser` only. The commit message of
  `347f2996` says the bare-name exclusion is excused again *as it was before
  round 1*. That holds for those two names and not for the other four.

The docstring states the rule wider than the code. Line 35 lists
*a bare name no import binds* among the receivers whose `.open` is excused.
Read as written, `def f(p): p.open()` would pass. It does not, and must not:
that is the most common shape in the class. Executed: `p.open()` on a
parameter and on an assignment is reported at the target.

Why it matters: the module's own K2 rule says what the walk cannot prove
counts as unnamed. A bare name with no import is a value the walk cannot
prove. The fix excuses it only where its spelling matches a module, which is
the case K2 was written for. The miss is narrow, and the shapes are unusual.
But it is a locale read the gate now passes and passed before, written into
the code by the fix pass, and the description given for it is not what the
code does.

The fix: keep the bare-name excuse for the two names that had it before
round 1, and judge any other bare name as `<expr>.open`. Executed in the
scratch clone: the module passes 122 cases, including the repository case.
Nothing in the tree depended on the wider excuse. The `NAMED` case for
`def f(os)` still passes.

### ⬜ 3 — a `zipfile.Path` reached by `/`, `.joinpath` or a name is judged at `Path.open`'s positions

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:32`

The docstring says `.open` is judged as `zipfile.Path.open` *on a
`zipfile.Path`*. `owner` finds that only where the receiver is the
constructor call itself. `(zipfile.Path(z) / "a").open("r", "utf-8")`,
`zipfile.Path(z).joinpath("a").open("r", "utf-8")` and a `zipfile.Path`
held in a name are still reported. Executed, at the target, with the fixes
above applied as well.

This is the over-report round 2's ⬜ 3 named, through the usual ways of
reaching a member. It is the same shape the fix already documented for a
`ZipFile` held in a name. It fails loud and nothing in the tree has it. The
docstring can say the walk does not trace it, as it says for `ZipFile`.

### ⬜ 4 — `dbm.gnu`, `dbm.ndbm` and `dbm.sqlite3` are still reported

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:134`

Round 2's ⬜ 2 named `dbm.dumb.open(p)`. The fix added `dbm.dumb` alone.
`import dbm.gnu` then `dbm.gnu.open(p)` resolves to `dbm.gnu`, which is not
in the set. The path is read as the mode, so the call is reported as
`<expr>.open(), mode not a literal`. Executed for `dbm.gnu`, `dbm.ndbm` and
`dbm.sqlite3` at the target. None of them opens text. `dbm.sqlite3` exists
from 3.13 on; the local 3.12 lists `dumb`, `gnu` and `ndbm`. An over-report,
and none is in the tree.

### ⬜ 5 — correction: `spec.md`'s K1 row carries the same over-wide sentence as 🟡 2

`seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/spec.md:86`

The row lists *a bare name no import binds* among the receivers excused,
in the same words as the docstring line 🟡 2 names. Paperwork, so a
correction. It moves with 🟡 2's docstring edit.

## Regression tests to plant

All in `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`.
Each was seen red: its source was run through the walker at the target and
came back with no site, or with a site where none belongs.

- `UNNAMED`: `zipfile.Path.open(q, "r")` on the class, kind
  `zipfile.Path.open()` (🟡 1). No site at the target.
- `UNNAMED`: a module-level `wave = make(p)` then `wave.open()`, kind
  `<expr>.open()` (🟡 2). No site at the target.
- `NAMED`: `dbm.gnu.open(p)` and `dbm.ndbm.open(p)` after their imports
  (⬜ 4). Reported at the target.

The `NAMED` case at line 765 should change, so that the encoding it names is
the one read. With 🟡 1's fix in place it passes for the right reason as it
stands, since the shift then puts `"utf-8"` in the encoding's slot.

## Facts for the evidence ledger

- E1's `judge` stamp was moved to `13184adc` in `7bfee70c`. Its *Executed*
  cell says each K1 row was mutated once through `bin/mutation-check`. That
  run predates the `zipfile.Path.open` row and the bare-name branch, and the
  re-stamp did not re-run it. Both fixes above change `judge` and `owner`
  again, so E1's stamp moves a second time where they land.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `zipfile.Path.open` sits in `OPENERS`, which the top of `judge` matches before the `.open` branch, so the class-called form is judged with no path shift and `zipfile.Path.open(q, "r")` passes as named | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:314` | open | Executed: three unbound spellings return no site at the target and are reported at `de952182` and `839d19a9`; the line-765 `NAMED` case passes on `"r"` read as the encoding. Fix applied in the scratch clone: 122 passed, ruff clean. Who answers it: #741's branch, before PR #757 is marked ready; the walker's `judge` is a unit this work item created |
| 🟡 2 | The restored bare-name branch of `owner` excuses `.open()` on any local named `os`, `webbrowser`, `tarfile`, `shelve`, `dbm` or `wave`; before round 1 only the first two were; the docstring says any bare name | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:405` | open | Executed: `wave`, `tarfile` and `shelve` locals holding a path return no site at the target and are reported at `839d19a9` and `de952182`. Read: `839d19a9`'s set held two names. Fix applied in the scratch clone: 122 passed. Who answers it: #741's branch, before PR #757 is marked ready; `owner` is a unit this work item created |
| ⬜ 3 | A `zipfile.Path` reached by `/`, `.joinpath` or a name is judged at `Path.open`'s positions, though the docstring says any `zipfile.Path` is judged as `zipfile.Path.open` | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:32` | open | Executed at the target and with 🟡 1 and 🟡 2's fixes applied. An over-report, none in the tree. Who answers it: #741's branch, with 🟡 1's edit |
| ⬜ 4 | `dbm.gnu`, `dbm.ndbm` and `dbm.sqlite3` are reported though they open no text; the fix for round 2's finding 2 added `dbm.dumb` alone | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:134` | open | Executed at the target for all three. An over-report, none in the tree. Who answers it: #741's branch, with 🟡 2's edit |
| ⬜ 5 | Correction: `spec.md`'s K1 row says `.open` on a bare name no import binds is excused, the same over-wide sentence as 🟡 2 | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/spec.md:86` | open | Read. Paperwork, so a correction. Who answers it: #741's branch, with 🟡 2's docstring edit |
| 🟢 | round 2's finding 1 is closed — `ElementInclude.default_loader` is no longer a K1 row and its text call is a `NAMED` case | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:24` | confirmed | Read: the loader's 3.12 source sets UTF-8 when `encoding` is falsy, and the branch is gone from `judge`. Executed: the text call returns no site at the target, and was reported at `de952182` |
| 🟢 | round 2's finding 2 is closed for what it named — the docstring says a `ZipFile` or `TarFile` built in the receiver, `dbm.dumb` is excused, and an unimported `os` is excused again | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:33` | confirmed | Executed: `dbm.dumb` by three import spellings and `def f(os)` return no site at the target. The fix reaches further than it says; that is this round's 🟡 2 and ⬜ 4 |
| 🟢 | round 2's finding 3 is closed for what it named — `zipfile.Path(z).open("r", "utf-8")` is not reported | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:191` | confirmed | Executed at the target, with the `from zipfile import Path` spelling as well. The unbound form the same row broke is this round's 🟡 1 |
| 🟢 | round 2's finding 4 is closed — *What no row can hold* names `dictConfig` and a handler subclass's `super().__init__` | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:57` | confirmed | Read |
| 🟢 | round 2's finding 5 is closed — the changelog counts two one-liners handed to a session, and `spec.md` names the CI step beside them | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:3` | confirmed | Read, with `spec.md:72` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — `zipfile.Path.open` called on its class passes as named | not placed by this round; the orchestrator places it on the ladder. Candidate: rung 1, since `judge` is a unit this work item created | #741's branch, before PR #757 is marked ready |
| 🟡 2 — the bare-name branch of `owner` excuses six module spellings | not placed by this round; the orchestrator places it on the ladder. Candidate: rung 1, since `owner` is a unit this work item created | #741's branch, before PR #757 is marked ready |

## Paste-ready fixes

### 🟡 1

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

### 🟡 2

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

The docstring at line 35, and the same words in `spec.md:86` (⬜ 5):

```diff
-  `Image` and a `ZipFile(...)` or `TarFile(...)` built in the receiver
-  itself, which open no text, and on a bare name no import binds; called on
-  the class (`Path.open(p)`), every position moves one to the right;
+  `Image` and a `ZipFile(...)` or `TarFile(...)` built in the receiver
+  itself, which open no text, and on `os` or `webbrowser` where no import
+  binds the name; called on the class (`Path.open(p)`), every position moves
+  one to the right;
```

The `owner` docstring:

```diff
-    class a receiver call constructs (`zipfile.ZipFile(z)`), or a bare name no
-    import binds, read as itself (`os` taken as a parameter). An instance
-    bound to a name first (`with ZipFile(z) as zf`) is not traced."""
+    class a receiver call constructs (`zipfile.ZipFile(z)`), or `os` or
+    `webbrowser` where no import binds the name (`os` taken as a parameter).
+    Any other bare name no import binds is unproven, so it is None. An
+    instance bound to a name first (`with ZipFile(z) as zf`) is not traced."""
```

### ⬜ 3

```diff
-- `<expr>.open(...)` judged as `Path.open`, or as `zipfile.Path.open`,
-  whose encoding comes one place earlier, on a `zipfile.Path`; except on
+- `<expr>.open(...)` judged as `Path.open`, or as `zipfile.Path.open`,
+  whose encoding comes one place earlier, on a `zipfile.Path(...)` built in
+  the receiver itself (one reached by `/`, `.joinpath` or a name is judged
+  as `Path.open`); except on
```

### ⬜ 4

```diff
     "dbm.dumb",
+    "dbm.gnu",
+    "dbm.ndbm",
+    "dbm.sqlite3",
     "wave",
```

Needs a fix: yes — 🟡 1 (`zipfile.Path.open` called on its class passes as named) and 🟡 2 (a local named after one of six modules has its `.open()` excused)
Loses a record or crashes: no

## Proof block

Files opened this round:

- `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` at the target, lines 1–560 and 563–800, and the same file at `839d19a9` and `de952182` through `git show`
- `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/rounds/round-2.md` and `round-2-report.md`
- `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/spec.md` lines 69–100, through the range diff and directly at line 86
- `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md`
- `seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md`, the E1 row, through the range diff
- `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped*, §*The reopening — one, and then the run is capped* and §*Where a leftover goes — the ladder, and why a new issue is not the default*
- `bin/test`
- the standard library's `zipfile.Path.open` and `xml.etree.ElementInclude.default_loader` sources on 3.12
