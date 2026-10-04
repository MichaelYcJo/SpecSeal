# Round 2 report — 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding (#741)

| Field | Value |
|---|---|
| Round | 2, the verifying round for round 1's fixes |
| Target SHA | 4b6f7273 |
| Fix range read | `839d19a9..16041459` (six commits), plus `4b6f7273`, which edits `round-1.md` alone |
| Base | `release/v0.18.1` at e141980a |
| Reviewer | specseal:warden on claude-opus-5-5 |
| Where the probes ran | a `git clone --no-local` of the branch at the target, in the session scratchpad; deleted before handover |

## Summary

Every round-1 verdict is closed, and one of the rows the fix added is wrong.

- Round 1's three yellows are closed. The unbound Path methods are judged
  with the path first, the standard library's other text openers are rows,
  and the three shipped one-liners name UTF-8. Executed: a probe of 42
  spellings, run against the walker before and after the fixes, plus the
  module itself.
- **🟡 1.** The fix added `xml.etree.ElementInclude.default_loader` as a K1
  row. It is not one: when `encoding` is `None` it reads text as UTF-8, not
  in the locale's encoding. The walker now reports a call that already reads
  UTF-8, and the docstring and `spec.md` state a false fact about the
  standard library.
- Four ⬜ notes. Two say the `.open` receiver rule over-reports in ways the
  docstring does not mention. One says the *What no row can hold* list misses
  the two usual ways a logging file handler is built. One is a paperwork
  correction about the count of one-liners.

The smith's question has an answer. The new tables are rows of the existing
walker, not mechanism. The exclusions the docstring lists were each read in
the 3.14 source, and in none of them does `None` mean the locale.

Nothing found loses a record or crashes.

## Findings from reading and from execution

### 🟡 1 — `ElementInclude.default_loader` reads UTF-8 when no encoding is named, and the walker reports it

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:330`–`339`,
the docstring at `:46`, the case at `:680`, and
`seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/spec.md:100`.

The source of the function, read on 3.12, 3.13 and 3.14 alike
(`xml/etree/ElementInclude.py:87`):

```python
def default_loader(href, parse, encoding=None):
    if parse == "xml":
        with open(href, 'rb') as file:
            data = ElementTree.parse(file).getroot()
    else:
        if not encoding:
            encoding = 'UTF-8'
        with open(href, 'r', encoding=encoding) as file:
```

A text parse with no encoding is UTF-8. K1 is *the calls that take the
locale's encoding when none is named*, and the docstring says each callable
the construction found was *read for whether `None` means the locale*. This
one was misread.

Executed. The probe gives `ElementInclude.default_loader(h, "text")` to
`unnamed_sites` at the target, and it comes back as a site. Before the fix
range it came back empty.

Why it matters:

- **What it costs today.** A contributor who writes this call is told to
  name an encoding the call already uses. Naming it does no harm, so the
  cost to code is small.
- **What it costs the records.** The module docstring and `spec.md`'s
  inferred paragraph both present the call as one that reads in the
  locale's encoding. That is a false fact about the standard library,
  carried into the document the module calls its table.
- **Why this is 🟡 and not ⬜.** The behaviour and the stated fact are both
  wrong, so the line drawn in `code-review` puts it at 🟡.

The paste-ready fix removes the branch and the case. It adds the loader to
the docstring's sentence about fixed defaults and turns the text call into a
`NAMED` guard. I applied it in the scratch clone and ran it. The module
passed (115), and ruff check and ruff format passed. The guard is red
against the target walker: it is the probe's FALSE+ row for this call.

### ⬜ 2 — the docstring says a `ZipFile` instance is excused; only one built in the receiver is

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:31`–`32`
and `owner` at `:396`.

The docstring says `.open` is excused on *a `ZipFile(...)` or `TarFile(...)`
instance*. `owner` excuses the receiver only when it is the constructing call
itself, so the usual spelling is still reported (executed):

- `with zipfile.ZipFile(z) as zf: zf.open(n)` is reported as
  `<expr>.open(), mode not a literal`.
- `zf = ZipFile(z); zf.open(n)` is reported the same way.
- `dbm.dumb.open(p)` is reported, because `dbm.dumb` is not `dbm`.

One more over-report is new in this range. The old receiver test fell back
to the bare name when nothing imported it: `bound.get(receiver.id,
receiver.id)`. `dotted` does not fall back, so `os.open(p, 0)` inside a
function that takes `os` as a parameter is now reported. Before the range it
was excused. The probe ran at both ends.

None of these is in the tree. Round 1's ⬜ 5 named the cost: the only answer
is an `ALLOWED` row, which covers the whole unit. The behaviour is acceptable
for a walk that has no types. The sentence is wider than the behaviour, and
that is what this note asks to change.

### ⬜ 3 — `zipfile.Path.open` takes its encoding one place earlier than `Path.open`

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:138`.

`zipfile.Path.open(mode='r', *args, pwd=None, **kwargs)` hands `args[0]` to
`io.TextIOWrapper` as the encoding (read, `zipfile/_path/__init__.py:334` on
3.14). So the encoding sits in position 1, while `Path.open` has it in
position 2. Executed: `zipfile.Path(z).open("r", "utf-8")` names its
encoding and is reported as `<expr>.open()`. The bound form behaved the same
way before the range. The range then added `zipfile.Path` to
`UNBOUND_RECEIVERS` and planted the case *zipfile.Path open is still judged*,
both of which treat it as `Path.open`. `read_text` agrees with pathlib, so
only `.open` differs. An over-report, and none is in the tree.

### ⬜ 4 — *What no row can hold* misses the two usual ways a logging file handler is made

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:49`–`55`.

Executed, and both come back empty:

- `logging.config.dictConfig({... "class": "logging.FileHandler", "filename": ...})`
  names the class in a string.
- A subclass of `logging.FileHandler` whose constructor calls
  `super().__init__(p)`.

Both open the log in the locale's encoding. Neither can be a row, for the
reason the paragraph already gives for `configparser`'s `.read`. The
paragraph reads as a complete list, and the next person reading it will
take these two as caught. None is in the tree (searched).

### ⬜ 5 — correction: the records count three one-liners a session is handed

`seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:3`–`4`
and `spec.md:72`.

The changelog says *the three Python one-liners its instructions hand a
session*. Two are in skills (`skills/update/SKILL.md:45`,
`skills/implement/orchestration.md:115`). The third is
`.github/workflows/hygiene.yml:81`, which CI runs and no session is handed.
`spec.md:72` says *the three instances round 1 of review found*, but round 1
found two and named the workflow line as not a defect. Both lines become
release-note or record text. This is paperwork, so it is a correction and is
not counted in `Needs a fix`.

### Round 1's findings, each answered

- **Round 1's 🟡 1, the unbound Path methods — closed.** `judge` computes a
  shift from the receiver at `:376`, and `read_text`, `write_text` and
  `.open` move every position by it. Executed: `Path.read_text(p)`,
  `pathlib.Path.write_text(p, s)`, `Path.open(p, "r", -1)`, the aliased
  `P.read_text(p)` and `zipfile.Path.read_text(zp)` are reported. The named
  and binary unbound forms are not. Before the range all five were missed.
- **Round 1's 🟡 2, the other standard-library openers — closed, apart from
  🟡 1 above.** Executed: the compressed openers in text mode (a `b` in the
  file name included), the logging handlers by attribute and by imported
  name, `encoding=None` written out, `basicConfig(filename=)`, `FileInput`,
  `hook_compressed`, `argparse.FileType`, `doctest.testfile`, and
  `.makefile()` are each reported. Their binary and named forms are not, and
  `subprocess.CompletedProcess.check_returncode(x)` is not mis-targeted by
  the deeper chain resolution. Read: every position in
  `BINARY_BY_DEFAULT`, `TEXT_ALWAYS`, `TEXT_UNLESS_BINARY` and
  `METHODS_TEXT_UNLESS_BINARY` against the 3.14 signatures. All are right.
- **Round 1's 🟡 3, the shipped one-liners — closed.** All three name UTF-8.
  Searched for the class: every tracked file outside `.py` and `seal/` for
  `python3 -c` / `python3 -` carrying `open(`, `read_text`, `write_text` or
  `text=True`, and shipped Markdown for any `open(` without an encoding.
  These three are the only ones. The Out-of-scope row in `spec.md` and the
  `CONTRIBUTING.md` sentence say the walk stops at `.py`.
- **Round 1's ⬜ 4 — closed.** The docstring now has a *What no row can hold*
  paragraph. ⬜ 4 above adds two spellings to it.
- **Round 1's ⬜ 5 — closed for the forms it named.** `tarfile.open(p)`,
  `tarfile.TarFile.open(p)` and `zipfile.ZipFile(z).open(n)` are no longer
  reported (executed). ⬜ 2 above covers what is still reported.
- **Round 1's ⬜ 6 — closed.** `CONTRIBUTING.md:270`–`274` now says the first
  half covers every tracked `.py` and the second covers `hooks/`. The module's
  pinning case is green.
- **Round 1's ⬜ 7 — closed.** The changelog, phase 1, the overview and the
  ledger fragment each carry the backslash-u escape text again (`grep -c`, one
  line per file).

### The smith's question: rows, or mechanism?

Rows. `skills/code-review/orchestration.md` §*A fix pass adds the unit that
pins it* forbids a fix pass *a rule, a checker, a template section, a walk*.
None was added here:

- The walk is the one that existed. `_Walk`, the corpus and the allowance
  check are unchanged.
- The four new tables are data that the existing `judge` consults. Each
  branch that reads one has the same shape as branches that predate the run:
  the tempfile branch, the `TextIOWrapper` branch, the old `fileinput`
  branch.
- The module's own docstring named this as its extension point before the
  run: *a call the walk does not know is a row to add to K1*.
- `dotted` and the shift widen how the existing walk resolves a name and a
  position. They are not a second resolver.

The one branch with a shape of its own is the `default_loader` branch, and
🟡 1 removes it.

### The exclusions, checked for one where `None` means the locale

None of them takes the locale. Read in the 3.14 source:

| Exclusion | What `None` means |
|---|---|
| `TextIOWrapper.reconfigure` | keep the current encoding |
| `tarfile` | the module's `ENCODING`, used for member names and not for file content |
| `urllib.parse.quote` and its family | UTF-8 |
| the `xml` writers (`ElementTree.write`, `tostring`, the `minidom` methods) | `us-ascii`, or a returned `str` |
| `xmlrpc` | `encoding or 'utf-8'` |
| `calendar.HTMLCalendar.formatyearpage` | `sys.getdefaultencoding()`, which is UTF-8 |
| `asyncio`'s two event-loop subprocess methods | a `ValueError`: *encoding must be None* |

I also ran my own enumeration on 3.14: every public callable, class method
included, whose `encoding` parameter defaults to `None`. It found 86
qualified names, with constructors and aliases counted apart. Each one is a
K1 row, a `.read_text` method the attribute rule already catches
(`importlib.resources`' and `importlib.metadata`'s), `configparser`'s
`.read` (in the no-row paragraph), one of the exclusions above, or
`default_loader` (🟡 1). Two more names came from `pathlib`'s new private
`types` module, and they are not public API.

## The claims of the account, checked

| The account claimed | What I found |
|---|---|
| The K1 standard-library half was *found by construction* and each name *read for whether `None` means the locale* | The construction reproduces (86 qualified names on 3.14). One name was misread: `default_loader` (🟡 1) |
| The docstring's exclusions take a fixed default or refuse text | Holds for all seven (table above) |
| *A `ZipFile(...)` or `TarFile(...)` instance* opens no text and is excused | Only an instance built in the receiver itself is excused (⬜ 2) |
| *The three Python one-liners its instructions hand a session* | Two are handed to a session, and one is CI (⬜ 5) |
| `ALLOWED` is empty because the receiver rule no longer reports PIL's `Image` | Holds. The module is green with no row, and `survivor-check` over the range excuses the one released survivor through `survivors.md` |

## Regression tests to plant

- `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`,
  `NAMED`: `ElementInclude.default_loader(h, "text")` as the UTF-8 guard,
  from 🟡 1's fix. Seen red against the target walker (the probe's FALSE+
  row).

## Facts for the evidence ledger

- E1's anchor on `judge` moves when 🟡 1's fix lands. Re-read it then.

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

## Paste-ready fixes

### 🟡 1 — remove the `default_loader` row

In `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`,
the docstring's exclusion sentence and K1 list:

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

In `judge`, delete the branch:

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

In `UNNAMED`, delete the case:

```diff
-    "ElementInclude.default_loader, text": (
-        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "text")',
-        "xml.etree.ElementInclude.default_loader()",
-    ),
```

In `NAMED`, replace the `xml` guard with the text one, which is red against
the walker at the target:

```diff
-    "ElementInclude.default_loader, xml": (
-        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "xml")'
-    ),
+    # `default_loader` reads text as UTF-8 when `encoding` is None.
+    "ElementInclude.default_loader, text, is UTF-8": (
+        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "text")'
+    ),
```

In `spec.md`'s inferred paragraph:

```diff
 and `hook_compressed`, `argparse.FileType`, `doctest`'s file readers,
-`ElementInclude`'s text loader, and the `.makefile()` and
-`.write_results_file()` methods. The module docstring holds the whole table,
+and the `.makefile()` and `.write_results_file()` methods. The module
+docstring holds the whole table,
```

### ⬜ 2 — the docstring's receiver sentence

```diff
-  `tarfile`, `shelve`, `dbm`, `wave`, PIL's `Image` and a `ZipFile(...)` or
-  `TarFile(...)` instance, which open no text; called on the class
+  `tarfile`, `shelve`, `dbm`, `wave`, PIL's `Image`, and `ZipFile(z).open`
+  or `TarFile(t).open` written as one expression, which open no text (an
+  instance held in a name is still judged); called on the class
```

### ⬜ 4 — two more spellings no row can hold

```diff
 a module loaded through `importlib`, `universal_newlines` given by position,
-and `configparser`'s `.read`, whose name is too common to match without
-types. Write the call plainly instead.
+`configparser`'s `.read`, whose name is too common to match without types,
+and a logging file handler made by `logging.config.dictConfig` or by a
+subclass's `super().__init__`. Write the call plainly instead.
```

### ⬜ 5 — the count of one-liners

`changelog.md`:

```diff
-- Every Python file the plugin ships, and the three Python one-liners its
-  instructions hand a session, name the encoding they read and write in,
+- Every Python file the plugin ships, the two Python one-liners its
+  instructions hand a session, and the one its CI runs, name the encoding
+  they read and write in,
```

`spec.md:72`: *The three instances round 1 of review found* becomes *The
two instances round 1 of review found, and the workflow line it named
beside them,*.

Needs a fix: yes — 🟡 1 (the `ElementInclude.default_loader` row reports a call that reads UTF-8, and the docstring and spec call it a locale reader)

Loses a record or crashes: no

## Proof — files opened

- `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/`:
  `rounds/round-1.md`, `rounds/round-1-report.md`, the fix range's diff of
  `spec.md`, `changelog.md`, `overview.md`, `phases/phase-1.md`,
  `survivors.md`
- the fix range's diff of
  `seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md`
- `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`:
  the docstring, the tables, `bindings` through `judge_text`, and the case
  tables around the new rows; the whole fix-range diff
- `CONTRIBUTING.md:262`–`275`, `skills/update/SKILL.md:45`,
  `skills/implement/orchestration.md:115`, `.github/workflows/hygiene.yml:80`–`81`
- `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins
  it*, `agents/smith.md:320`–`365`
- standard library, 3.14: `xml/etree/ElementInclude.py`, `doctest.py`,
  `calendar.py`, `http/cookiejar.py`, `zipfile/_path/__init__.py`,
  `tarfile.py`, `urllib/parse.py`, `xmlrpc/client.py`,
  `xml/etree/ElementTree.py`, `asyncio/base_events.py`, `_pyio.py`,
  `fileinput.py`; 3.12 and 3.13: `xml/etree/ElementInclude.py`
