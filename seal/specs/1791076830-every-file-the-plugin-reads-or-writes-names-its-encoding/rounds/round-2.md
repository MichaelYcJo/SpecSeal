# 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding — review round 2

| Field | Value |
|---|---|
| Target SHA | 4b6f727336d2166347565f5302bf8544bd4433fe |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #757 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the `ElementInclude.default_loader` row reports a call that reads UTF-8, and the docstring and spec call it a locale reader) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item `1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding` (#741, PR #757). It is the verifying round for round 1's fixes, range `839d19a9..16041459`, target `4b6f7273`.

Open each fix and judge whether each round-1 verdict is closed:
- 🟡1: unbound `Path` methods shift every argument position by one.
- 🟡2: the stdlib's text openers, enumerated by a probe over every public callable whose signature has `encoding=None` (58 found), now sit in five tables.
- 🟡3: three one-liners name UTF-8, the `.py`-only walk is stated as Out of scope, and the changelog is narrowed.
- ⬜4–⬜7.

The units the fixes created are a finding surface. They are all depth 1: `UNBOUND_RECEIVERS`, `BINARY_BY_DEFAULT`, `TEXT_ALWAYS`, `TEXT_UNLESS_BINARY`, `METHODS_TEXT_UNLESS_BINARY`, `dotted`, `mode_node`, `owner` and `judge_text`. `ALLOWED` is now empty.

Judge the smith's question: are the new K1 tables rows of the existing walker, or mechanism a fix pass may not add? Check the exclusions listed in the docstring (`TextIOWrapper.reconfigure`, `tarfile`, `urllib.parse`, the `xml` writers, `xmlrpc`, `calendar`, `asyncio`'s subprocesses) for one where `None` really means the locale.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `xml.etree.ElementInclude.default_loader` is a K1 row, but with no encoding it reads text as UTF-8, so the walker reports a UTF-8 call and the docstring and `spec.md` call it a locale reader | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:330` | open | Read: the function's source on 3.12, 3.13 and 3.14 sets UTF-8 when `encoding` is falsy. Executed: the text call is reported at the target and was not before the range. Fix applied in the scratch clone: 115 passed, ruff clean |
| ⬜ 2 | The docstring excuses `.open` on a `ZipFile` or `TarFile` instance, but only one built in the receiver is excused; `with ZipFile(z) as zf: zf.open(n)` and `dbm.dumb.open(p)` are still reported, and an unimported `os` lost its exclusion in this range | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:32` | open | Executed: the probe at the target and at `839d19a9`. None in the tree; the sentence is wider than the behaviour |
| ⬜ 3 | `zipfile.Path.open` takes its encoding at position 1, but it is judged with `Path.open`'s position 2, so `zipfile.Path(z).open("r", "utf-8")` is reported | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:138` | open | Read: the 3.14 source passes the first extra argument to `TextIOWrapper` as the encoding. Executed: reported at the target. An over-report, none in the tree |
| ⬜ 4 | *What no row can hold* omits `logging.config.dictConfig` with a handler class named in a string, and a handler subclass calling `super().__init__(p)`; both open the log in the locale's encoding | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:49` | open | Executed: both come back empty. None in the tree |
| ⬜ 5 | Correction: the changelog says three one-liners are handed to a session, but one is the CI workflow; `spec.md:72` says round 1 found three, but it found two | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:3` | open | Read. Paperwork, so a correction |
| 🟢 | round 1's finding 1 is closed — the unbound Path methods are judged with the path first | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:376` | confirmed | Executed: five unbound spellings reported at the target and missed at `839d19a9`; the named and binary forms are not reported |
| 🟢 | round 1's finding 2 is closed — the compressed openers, logging handlers, `fileinput`, `argparse`, `doctest` and `.makefile()` are rows, with correct positions | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:142` | confirmed | Executed: each reported at the target and missed before the range, with their binary and named forms passing. Read: every position against the 3.14 signatures. The one wrong row is finding 1 of this round |
| 🟢 | round 1's finding 3 is closed — the three shipped one-liners name UTF-8, and the walk's `.py` limit is stated | `skills/update/SKILL.md:45` | confirmed | Read; searched every tracked non-`.py` file for embedded Python that opens a file. These three are the only ones |
| 🟢 | round 1's notes 4, 5, 6 and 7 are closed | `CONTRIBUTING.md:271` | confirmed | Read and executed as above; what remains of note 5 is this round's ⬜ 2 |
| 🟢 | The new K1 tables are rows of the existing walker, not mechanism | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:153` | confirmed | Read: no new walk, checker or rule. The tables feed the existing `judge`, in the shape of its pre-run branches, through the extension point the docstring named before the run |
| 🟢 | No exclusion in the docstring is a call where `None` means the locale | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:23` | confirmed | Read: the seven in the 3.14 source. Executed: my own enumeration of callables whose `encoding` defaults to `None` (86) finds no other locale reader |

## Paste-ready fixes

```diff
 then read for whether `None` means the locale. It does not for
 `TextIOWrapper.reconfigure` (keep the current one), `tarfile` (file names),
-`urllib.parse`, the `xml` writers, `xmlrpc`, `calendar` (each a fixed
-default), or `asyncio`'s subprocesses (which refuse text). An opener with no
+`urllib.parse`, the `xml` writers, `ElementInclude.default_loader` (UTF-8),
+`xmlrpc`, `calendar` (each a fixed default), or `asyncio`'s subprocesses
+(which refuse text). An opener with no
 `encoding` parameter at all, like `os.popen`, is not in that construction
```
```diff
   `argparse.FileType`, `doctest.testfile` / `DocFileTest` / `DocFileSuite`,
-  `xml.etree.ElementInclude.default_loader` unless it parses `"xml"`, and
-  the methods `.makefile()` and `.write_results_file()`.
+  and the methods `.makefile()` and `.write_results_file()`.
```
```diff
-    if target == "xml.etree.ElementInclude.default_loader":
-        kw = keyword(call, "parse")
-        parse = (
-            kw.value
-            if kw is not None
-            else (call.args[1] if len(call.args) > 1 else None)
-        )
-        if isinstance(parse, ast.Constant) and parse.value == "xml":
-            return None
-        return None if names_encoding(call, 2) else f"{target}()"
```
```diff
-    "ElementInclude.default_loader, text": (
-        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "text")',
-        "xml.etree.ElementInclude.default_loader()",
-    ),
```
```diff
-    "ElementInclude.default_loader, xml": (
-        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "xml")'
-    ),
+    # `default_loader` reads text as UTF-8 when `encoding` is None.
+    "ElementInclude.default_loader, text, is UTF-8": (
+        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "text")'
+    ),
```
```diff
 and `hook_compressed`, `argparse.FileType`, `doctest`'s file readers,
-`ElementInclude`'s text loader, and the `.makefile()` and
-`.write_results_file()` methods. The module docstring holds the whole table,
+and the `.makefile()` and `.write_results_file()` methods. The module
+docstring holds the whole table,
```
```diff
-  `tarfile`, `shelve`, `dbm`, `wave`, PIL's `Image` and a `ZipFile(...)` or
-  `TarFile(...)` instance, which open no text; called on the class
+  `tarfile`, `shelve`, `dbm`, `wave`, PIL's `Image`, and `ZipFile(z).open`
+  or `TarFile(t).open` written as one expression, which open no text (an
+  instance held in a name is still judged); called on the class
```
```diff
 a module loaded through `importlib`, `universal_newlines` given by position,
-and `configparser`'s `.read`, whose name is too common to match without
-types. Write the call plainly instead.
+`configparser`'s `.read`, whose name is too common to match without types,
+and a logging file handler made by `logging.config.dictConfig` or by a
+subclass's `super().__init__`. Write the call plainly instead.
```
```diff
-- Every Python file the plugin ships, and the three Python one-liners its
-  instructions hand a session, name the encoding they read and write in,
+- Every Python file the plugin ships, the two Python one-liners its
+  instructions hand a session, and the one its CI runs, name the encoding
+  they read and write in,
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the encoding module at the target, in the scratch clone | 116 passed |
| `uvx ruff check` and `uvx ruff format --check` on the module at the target | both clean |
| Spelling probe: 42 sources through `unnamed_sites` at the target | 32 agree; 10 disagree: 2 MISS (⬜ 4) and 8 FALSE+ (🟡 1, ⬜ 2, ⬜ 3, and `fileinput.input(..., openhook=hook_encoded(...))`, reported before and after the range) |
| The same 42 sources at `839d19a9` | 30 disagree; every round-1 shape is missed or over-reported there, the unimported-`os` case is not |
| Enumeration on 3.14 of public callables whose `encoding` defaults to `None` | 86 qualified names; each classified (see the exclusions section) |
| 🟡 1's fix applied in the scratch clone: the module, ruff check, ruff format | 115 passed; clean; clean |
| `bin/evidence-check .` at the target | 4401 ok · 0 drifted · 0 broken; records half 0 refused |
| `bin/survivor-check --range 839d19a9..16041459 --exempt` the work item's `survivors.md` | one survivor, excused by its row |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
