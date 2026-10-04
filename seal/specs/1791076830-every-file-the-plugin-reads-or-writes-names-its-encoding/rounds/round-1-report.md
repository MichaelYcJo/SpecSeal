# Round 1 report — 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding (#741)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 9e1759d5 |
| Base | `release/v0.18.1` at e141980a |
| Reviewer | specseal:warden on claude-opus-5-5 |
| Where the probes ran | a `git clone --no-local` of the branch at the target, in the session scratchpad; deleted before handover |

## Summary

Spec compliance holds for what the frame wrote down. The walker implements
every K1 row and every K2 shape the spec lists, the alias half resolves both
import forms, both liveness halves work, the entry-point half is an order
assertion, and every one of the 29 product edits keeps its failure
direction. The three cases this work planted for product behaviour (S7, S8,
S9) each went red when I undid their unit.

What fails is the class itself, enumerated the way the ask said to: every
text-opening API in the standard library, crossed with every way to spell the
call. Three findings come from that.

- **🟡 1.** K1's own Path rows are misjudged when the method is called on its
  class: `Path.read_text(p)` and `Path.write_text(p, s)` pass, because the
  walker reads the path as the encoding.
- **🟡 2.** K1 leaves out standard-library calls that open text in the
  locale's encoding (gzip/bz2/lzma in text mode, the logging file handlers,
  `fileinput.FileInput`). One of them, `bz2.open("x.bz2", "rt")`, passes
  because the receiver rule reads the file name as the mode.
- **🟡 3.** Two shipped Markdown files tell a session to run Python that
  opens a file with no encoding. The walker's corpus is `.py` only, so the
  changelog's *every file the plugin reads* is wider than what is held.

Four ⬜ notes follow. Nothing found loses a record or crashes.

## Findings from reading and from execution

### 🟡 1 — `Path.read_text(p)` is read as naming its encoding

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:262`–`276`.
The attribute branch of `judge` judges `.read_text` by position 0 and
`.write_text` by position 1, and `.open` through `judge_opener` with Path's
positions. That holds for a bound call, `p.read_text()`. When the method is
called on its class, the path is the first argument, so every position moves
one to the right.

- `from pathlib import Path; Path.read_text(p)`: position 0 is `p`, which is
  not `None`, so the walker says the encoding is named.
- `Path.write_text(p, s)`: position 1 is the text, so the same thing happens.
- `Path.open(p, "r", -1)`: position 2 is the buffering value `-1`.

Executed: all three come back empty from `unnamed_sites` at the target (the
walker-miss probe below). The tree holds none of them today. The spelling is
an ordinary one, though (`sorted(paths, key=Path.read_text)` and its
neighbours), and it is a K1 row's own shape, which is exactly what the module
says it holds.

Why it matters: a branch that writes this passes the module on every leg and
reads cp1252 on Windows, which is the late discovery this work item exists to
end.

### 🟡 2 — standard-library text openers outside K1

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:102`.
The walker-miss probe enumerated the standard library's text openers against
the walker at the target. These take the locale's encoding when none is named,
and K1 has no row for them:

| Call | What the walker does at the target |
|---|---|
| `gzip.open(name, "rt")`, `bz2.open(…, "rt")`, `lzma.open(…, "rt")` | judged by the receiver rule as `Path.open`, with the file name in the mode's slot. So `bz2.open("x.bz2", "rt")` and `lzma.open("b.xz", "rt")` **pass**, because the name contains a `b`. `from gzip import open; open(p, "rt")` passes, because `gzip.open` is in no table and the call is a bare name |
| `logging.FileHandler(p)`, `logging.handlers.RotatingFileHandler(p)`, `TimedRotatingFileHandler`, `WatchedFileHandler`, `logging.basicConfig(filename=p)` | pass. `target_of` also resolves only one level of attribute, so `logging.handlers.X` resolves to nothing |
| `fileinput.FileInput(fs)` | passes; K1 names `fileinput.input` alone |
| `configparser.ConfigParser().read(p)` | passes. An attribute named `read` is too common to match without types, so the fix below leaves it out and ⬜ 4 asks the docstring to name it |

None of these is in the tree today (searched, read). The spec presents K1 as
*the class, enumerated by construction*, and `CONTRIBUTING.md` tells a
contributor the module enforces the rule over every tracked `.py`. A logging
handler added next month would not be seen, and would write cp1252 on the
Windows leg.

The paste-ready fix below was applied in the scratch clone and run:
the module passed (87, the 72 existing cases plus 15 new ones), ruff check and
ruff format passed, and the repository case stayed green, so widening
`target_of` to resolve attribute chains moved no verdict in the tree. The ten
new unnamed shapes and `gzip.open(p)`'s binary default are each red against
the walker at the target (the probe's MISS and FALSE+ rows). The other four
new named shapes pass there too, so they guard the new rules against
over-reporting and were not seen red. The fix also removes the receiver
rule's false positive on `gzip.open(p)`.

### 🟡 3 — shipped Markdown tells a session to open a file with no encoding

`skills/update/SKILL.md:45` and `skills/implement/orchestration.md:115`.
Both hand a session a `python3 -c` one-liner that calls `json.load(open(…))`
with no encoding. The update skill's call reads the installer's
installed_plugins.json, which records the plugin's install path. That path
is under the user's home directory, and a home directory can hold non-ASCII.
On a Windows interpreter whose code page is cp949 or cp1252, the UTF-8 file
is decoded in that code page. It either raises or produces a path that does
not exist, and the update check then greps the wrong place. Read, not
executed: no Windows interpreter was available.

Neither line is in the walker's corpus, which is `git ls-files '*.py'` (D2),
and the spec's Out of scope says nothing about Python embedded in Markdown.
The changelog fragment says *every file the plugin reads or writes names its
encoding*. That sentence goes into the release note, and these two lines
contradict it. `.github/workflows/hygiene.yml:81` has the same shape, but it
runs on `ubuntu-latest` only, so it is not a defect there.

The fix names the encoding in both lines. Holding the class there (a walk
over fenced `python3 -c` bodies) is a wider change. If the smith prefers to
answer with grounds, the honest form is an Out-of-scope row in `spec.md`
plus a changelog sentence narrowed to *every Python file*.

### ⬜ 4 — spellings no table row can hold, and a docstring that says every miss is a row

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:16`.
The docstring says *a spelling the walk misses is a row to add to K1*. The
probe found ten spellings that no table row can catch, because a static walk
cannot follow them:

- `f = open; f(p)`, and `sp = subprocess; sp.run(c, text=True)`
- `from subprocess import *`
- `functools.partial(open, mode="w")(p)`
- `map(Path.read_text, ps)`, a reference rather than a call
- `getattr(subprocess, "run")(…)`, `__import__("subprocess").run(…)` and
  a module loaded through `importlib` and then called
- `universal_newlines` passed to `Popen` by position
- `configparser`'s `read`, from 🟡 2

None is in the tree. The behaviour is acceptable for a static check. What
reads wrong is the sentence, which tells the next person that each miss is a
row to add. One sentence naming these limits would stop that.

### ⬜ 5 — the receiver rule over-reports a binary `.open`, and the cost is a whole-unit allowance

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:100`.
`tarfile.open(p)` and `zipfile.ZipFile(z).open(name)` are reported as
`<expr>.open(), mode not a literal`, because the rule judges every receiver
except `os` and `webbrowser` as `Path.open` (executed, the probe's FALSE+
rows). Neither has a text mode. The only answer the module offers is an
`ALLOWED` row, and D4 keys a row by unit. So one binary call allowance hides
every real unnamed call added to the same function later. `Image.open` is
the case already in the table. Adding `tarfile`, `shelve`, `dbm` and `wave`
to `NOT_A_FILE_OPENER`, and the compressed openers to their own table (🟡 2's
fix), keeps the table short. It is not a defect today.

### ⬜ 6 — `CONTRIBUTING.md` says both halves cover every tracked `.py`

`CONTRIBUTING.md:271`: *enforces both over every tracked `.py`*. The
entry-point half walks `hooks/` alone, by design (spec Out of scope). The
behaviour is right and the sentence is wider. *Enforces both, the first over
every tracked `.py` and the second over `hooks/`* says what is held. The
phrase the pinning case asserts is a different one, so this edit leaves it
green.

### ⬜ 7 — correction: the records lost the escape they describe

`seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:18`,
and the same sentence in `phases/phase-1.md:31`, `overview.md:22`, and the
ledger fragment's E3 row. Each says the refusal arrived *with each `—` and
`…` spelled `—` and `…`*. The escape spellings themselves, a backslash, `u`
and the four hex digits (`u2014`, `u2026`), were written as the characters
they stand for, so the sentence now says nothing. I read the bytes with
`cat -v`, and the files carry no `u2014`. The test docstring at
`tests/test_the_commit_gate_decides_at_the_commit.py:839` has it right. The
changelog line becomes a release-note line. This is paperwork, so it is
reported as a correction and is not counted in `Needs a fix`.

### Confirmations, each from my own reading or run

- **The 29 product edits keep their failure direction.** Read at the target:
  - Nine are `open(path, "w").close()` empty markers.
  - Two are writes that cannot fail to encode. `hooks/session-lease.py:119`
    writes `json.dump`'s ASCII. `hooks/version-check.py:96` writes an
    integer.
  - One read gained `errors="replace"`: `read_mark`, whose handler catches
    `OSError` alone.
  - Three reads sit in handlers that already catch `UnicodeDecodeError`.
    `hooks/version-check.py:74` catches `ValueError`.
    `hooks/worktree-guard.py:1229` and `:1294` catch `Exception`, and those
    two read lease files that `session-lease.py` writes as ASCII JSON.
  - The 14 `.github/scripts/` sites go from strict-in-the-locale to strict
    UTF-8. They are not gates, and the workflows run them on a UTF-8 runner.
    `encoding=` alone puts `subprocess` in text mode, so dropping `text=True`
    changes nothing else.
- **S7, S8 and S9 go red when their unit is undone.** Executed through
  `bin/mutation-check` in the scratch clone:
  - Dropping `errors="replace"` from `read_mark` turned
    `test_a_mark_that_is_not_utf8_reads_as_text_rather_than_raising` red.
  - Deleting the call from `hooks/git/pre-commit.py` turned
    `test_the_refusal_reaches_an_ascii_console_as_written` red.
  - Moving the call after `main()` in `hooks/git/post-commit.py` turned
    `test_every_hook_entry_point_opens_with_to_utf8` red.
- **The smith's question: post-commit's stdout under an ASCII console.**
  Before this work, `PYTHONIOENCODING=ascii` gave stdout `strict` errors. I
  wrote an em dash to it and it raised `UnicodeEncodeError` (executed).
  After `console.to_utf8()`, the same write goes out as UTF-8 with `replace`
  (executed). The raise was real but narrow:
  - The notice line is ASCII except the work item's path, so only a
    non-ASCII item directory could reach it.
  - `notify` marks `already_told` (`hooks/implementer-notice.py:163`) before
    it returns the line, so the raise lost the notice for the whole session.
  - post-commit's exit status does not affect the commit.

  The call closes it. S7 holds the call's presence, and no case builds the
  notice under an ASCII console. That is D5's chosen trade, and I do not
  reopen it.
- **The reference-transaction hook now decodes stdin as UTF-8 with
  `replace`.** Read: `_commit_lines` uses a refname only for a prefix test and
  an equality with `HEAD`. A refname holding non-UTF-8 bytes used to crash
  the hook under a UTF-8 locale, and that crash refused the update. Now the
  gate judges the update. That is the direction `CONTRIBUTING.md`'s *a gate
  that crashes should let the work through* asks for, and the gate still
  judges every commit.
- **Every K1 row and K2 shape the spec lists is seen.** Executed: the
  walker-miss probe's `ok` rows, plus the module's own cases at the target.
  The corpus is `git ls-files '*.py'`, and no tracked file outside `.py`
  carries a Python shebang (searched).
- **The records check is clean.** `bin/evidence-check .` at the target
  reported 4362 ok, 0 drifted, 0 broken (executed).

### The claims of the account, checked

| The account claimed | What I found |
|---|---|
| M1: 29 product sites, equal to the census | The diff touches 15 sites under `hooks/` in 11 files and 14 under `.github/scripts/` in 5. Counted from the diff |
| *Every unit was mutated once, and every one went red* | Three re-run by me (above), all red. The rest is carried as the smith's claim, not re-established |
| *The enumeration of the class by construction* (spec) | Holds for the K1 table as written. The table itself is short of the class (🟡 1, 🟡 2) |
| Overview, *Not verified*: post-commit stdout keeps strict errors under an ASCII console | True before this work and closed by it (above) |

## Regression tests to plant

- `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`,
  in `UNNAMED` and `NAMED`: the 15 shapes in the fixes for 🟡 1 and 🟡 2. Ten
  unnamed shapes and `gzip.open(p)` were seen red at the target (probe MISS
  and FALSE+ rows). The other four named shapes are guards and pass there.

## Facts for the evidence ledger

- E1's claim cell should name what K1 now covers, once 🟡 2 lands: the
  compressed openers, the logging file handlers, `fileinput.FileInput`, and
  the unbound Path methods.
- E3's evidence cell spells the escapes the way ⬜ 7 describes. It should
  read as backslash-u sequences.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `Path.read_text(p)`, `Path.write_text(p, s)` and `Path.open(p, "r", -1)`, called on the class, pass the walker: the path is read in the encoding's slot | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:262` | open | Executed: the three return no site at the target. A K1 row's own shape, so the module's claim to hold K1 fails |
| 🟡 2 | K1 omits standard-library text openers: gzip/bz2/lzma in text mode (and `bz2.open("x.bz2", "rt")` passes because the name has a `b`), the logging file handlers and `basicConfig(filename=)`, `fileinput.FileInput` | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:102` | open | Executed: the walker-miss probe at the target. Fix applied in the scratch clone: 87 passed, ruff clean, the repository case still green |
| 🟡 3 | Two shipped Markdown one-liners open a file with no encoding, outside the `.py` corpus; the changelog says every file the plugin reads names its encoding | `skills/update/SKILL.md:45` | open | Read. The update one reads the installer's record of a path under the user's home; on a cp949 or cp1252 interpreter that is decoded wrong. `skills/implement/orchestration.md:115` is the second |
| ⬜ 4 | The docstring says every missed spelling is a K1 row; ten spellings found cannot be rows (rebinding, star import, `partial`, a reference passed to `map`, `getattr`, `__import__`, a module loaded through `importlib`, positional `universal_newlines`, `configparser`'s `read`) | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:16` | open | Executed: the probe's MISS rows. None in the tree. The sentence misleads, not the behaviour |
| ⬜ 5 | The receiver rule reports `tarfile.open(p)` and `zipfile.ZipFile(z).open(name)`, which are binary, so the answer is a whole-unit allowance that hides later real sites in that unit | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:100` | open | Executed: the probe's FALSE+ rows |
| ⬜ 6 | `CONTRIBUTING.md` says both halves cover every tracked `.py`; the entry-point half covers `hooks/` | `CONTRIBUTING.md:271` | open | Read; the spec scopes that half to hooks on purpose |
| ⬜ 7 | Correction: the changelog fragment, phase-1, overview and ledger E3 say each em dash and ellipsis was *spelled* as itself; the escape text was lost | `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/changelog.md:18` | open | Read the bytes with `cat -v`; no `u2014` in any of the three files. Paperwork, so a correction |
| 🟢 | The 29 product edits keep their failure direction | `hooks/commit-review-gate.py:590` | confirmed | Read per site: 9 empty markers, 2 ASCII-only writes, `read_mark` with `errors="replace"`, 3 reads in handlers catching `ValueError` or `Exception`, 14 non-gate scripts strict before and after |
| 🟢 | S7, S8 and S9 each go red when their unit is undone | `hooks/git/pre-commit.py:47` | confirmed | Executed: three mutations through `bin/mutation-check`, each red |
| 🟢 | The smith's question: post-commit's stdout raised under an ASCII console before this work, and the call closes it | `hooks/git/post-commit.py:24` | confirmed | Executed: the stdout write raised before `to_utf8` and went out as UTF-8 after. Read: `notify` marks before it returns, so the raise lost the notice for the session |
| 🟢 | The reference-transaction hook's stdin, now UTF-8 with `replace`, changes no verdict a refname reaches | `hooks/git/reference-transaction.py:27` | confirmed | Read: refnames meet only a prefix test and an equality; a crash that used to refuse now becomes a judgement |
| 🟢 | Every K1 row and K2 shape the spec lists is seen, both alias forms resolve, both liveness halves report and decline | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:213` | confirmed | Executed: module green at the target, probe `ok` rows |
| ❓ | The 19 converted test `subprocess` sites decode their child as UTF-8; each child (git, the hook entry points, payload-meter) writes UTF-8, but on a cp1252 interpreter that is unrun | `tests/test_the_commit_gate_decides_at_the_commit.py:73` | ❓ out of verified scope | Read: the children enumerated by AST from the diff. Answered by the pull request's `windows-latest` CI leg |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the new module and `tests/test_console_is_not_utf8.py`, at the target, in the scratch clone | 82 passed |
| Walker-miss probe: 37 spellings (the standard library's text openers crossed with alias, rebinding, star import, unbound, partial, reference, dynamic and positional forms) through the target's `unnamed_sites` | 12 `ok`; 21 MISS (the unbound Path methods, `bz2.open`/`lzma.open` text, `from gzip import open`, the logging handlers and `basicConfig`, `fileinput.FileInput`, `configparser`, and the ten dynamic spellings); 4 FALSE+ (`gzip.open(p)`, `tarfile.open(p)`, `ZipFile(z).open(name)`, a local `def open`) |
| Child-decoding probe: every `subprocess` call in the diff that names `encoding`, with its child command | 19 test sites; the children are git, bash or the claude shim running hook entry points, `dispatch.py`, payload-meter, the mutation-check wrapper (skipped on Windows) and a bare interpreter |
| `bin/mutation-check` ×3: `errors="replace"` out of `read_mark`; the call out of `hooks/git/pre-commit.py`; the call after `main()` in `hooks/git/post-commit.py` | red, red, red; the clone restored clean each time |
| `PYTHONIOENCODING=ascii PYTHONUTF8=0`, an em dash written to stdout, without and with `console.to_utf8()` | without: `ascii strict`, `UnicodeEncodeError`; with: `utf-8 replace`, the UTF-8 bytes |
| `bin/evidence-check .` at the target | 4362 ok · 0 drifted · 0 broken; records half 0 refused |
| The fix for 🟡 1 and 🟡 2 applied in the scratch clone: the module, `uvx ruff check`, `uvx ruff format --check` | 87 passed; all checks passed; already formatted. The probe's remaining MISS rows are the ten of ⬜ 4 |
| The full suite | not yet. The sealer runs it once, after the rounds settle; nothing in this round ran it |

## Paste-ready fixes

### 🟡 1 — the unbound Path methods

In `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`,
after `OPENERS`:

```python
# Classes whose methods, called on the class, take the path first, so the
# encoding's position moves one to the right: `Path.read_text(p, "utf-8")`.
UNBOUND_RECEIVERS = {
    "pathlib.Path",
    "pathlib.PurePath",
    "pathlib.PosixPath",
    "pathlib.WindowsPath",
    "zipfile.Path",
}


def dotted(node, bound):
    """`a.b.c` with its head resolved through the file's imports, or None."""
    if isinstance(node, ast.Name):
        return bound.get(node.id)
    if isinstance(node, ast.Attribute):
        head = dotted(node.value, bound)
        return f"{head}.{node.attr}" if head else None
    return None
```

`target_of` resolves any attribute chain, and `judge_opener` takes the shift:

```diff
         return "builtins.open" if func.id == "open" else None
-    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
-        receiver = bound.get(func.value.id)
-        if receiver:
-            return f"{receiver}.{func.attr}"
-    return None
+    return dotted(func, bound)
```

```diff
-def judge_opener(call, opener):
+def judge_opener(call, opener, shift=0):
     """The kind to report for an opener call, or None if it names its
-    encoding or opens in binary."""
-    mode_at, encoding_at = OPENERS[opener]
+    encoding or opens in binary. `shift` is 1 where the call is a method
+    called on its class, whose first argument is the path."""
+    mode_at, encoding_at = (at + shift for at in OPENERS[opener])
```

In `judge`'s attribute branch:

```diff
     if not isinstance(func, ast.Attribute):
         return None
+    shift = 1 if dotted(func.value, bound) in UNBOUND_RECEIVERS else 0
     if func.attr == "open":
@@
-        return judge_opener(call, "<expr>.open")
+        return judge_opener(call, "<expr>.open", shift)
     if func.attr == "read_text":
-        if names_encoding(call, 0):
+        if names_encoding(call, shift):
             return None
@@
     if func.attr == "write_text":
-        if names_encoding(call, 1):
+        if names_encoding(call, 1 + shift):
             return None
```

The cases, in `UNNAMED` and `NAMED`:

```python
    "Path.read_text, unbound": (
        "from pathlib import Path\nPath.read_text(p)",
        ".read_text()",
    ),
    "pathlib.Path.write_text, unbound": (
        "import pathlib\npathlib.Path.write_text(p, s)",
        ".write_text()",
    ),
    "Path.open, unbound": (
        'from pathlib import Path\nPath.open(p, "r", -1)',
        "<expr>.open()",
    ),
```

```python
    "Path.read_text, unbound, positional": (
        'from pathlib import Path\nPath.read_text(p, "utf-8")'
    ),
```

The docstring's K1 list gains, under the `read_text` bullet: *called on the
instance or on the class (`Path.read_text(p)`), the path then first*.

### 🟡 2 — the standard library's other text openers

This uses the `dotted` from 🟡 1's fix. After `OPENERS` (and after 🟡 1's
table):

```python
# Module-level openers that are binary unless the mode carries `t`:
# (mode position, encoding position or None where it is keyword-only).
BINARY_BY_DEFAULT = {"gzip.open": (1, 3), "bz2.open": (1, 3), "lzma.open": (1, None)}
# Calls that always open their file in text mode, with the encoding's
# position (None where it is keyword-only).
TEXT_ALWAYS = {
    "logging.FileHandler": 2,
    "logging.handlers.WatchedFileHandler": 2,
    "logging.handlers.RotatingFileHandler": 4,
    "logging.handlers.TimedRotatingFileHandler": 4,
    "fileinput.FileInput": None,
}
```

In `judge`, after the `fileinput.input` branch and before the attribute
branch:

```python
    if target in BINARY_BY_DEFAULT:
        mode_at, encoding_at = BINARY_BY_DEFAULT[target]
        if names_encoding(call, encoding_at):
            return None
        kw = keyword(call, "mode")
        node = kw.value if kw is not None else None
        if node is None and len(call.args) > mode_at:
            node = call.args[mode_at]
        if node is None:
            return f"{target}(), splat" if splatted(call) else None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return f"{target}()" if "t" in node.value else None
        return f"{target}(), mode not a literal"
    if target in TEXT_ALWAYS:
        if names_encoding(call, TEXT_ALWAYS[target]):
            return None
        return f"{target}(), splat" if splatted(call) else f"{target}()"
    if target == "logging.basicConfig":
        if names_encoding(call):
            return None
        if splatted(call):
            return "logging.basicConfig(), splat"
        return "logging.basicConfig(filename=)" if keyword(call, "filename") else None
```

The cases, in `UNNAMED`:

```python
    "gzip.open text": ('import gzip\ngzip.open("x.gz", "rt")', "gzip.open()"),
    "bz2.open text, a b in the path": (
        'import bz2\nbz2.open("x.bz2", "rt")',
        "bz2.open()",
    ),
    "lzma.open text, imported by name": (
        'from lzma import open\nopen(p, "rt")',
        "lzma.open()",
    ),
    "logging.FileHandler": (
        "import logging\nlogging.FileHandler(p)",
        "logging.FileHandler()",
    ),
    "RotatingFileHandler": (
        "import logging.handlers\nlogging.handlers.RotatingFileHandler(p)",
        "logging.handlers.RotatingFileHandler()",
    ),
    "logging.basicConfig with a file": (
        "import logging\nlogging.basicConfig(filename=p)",
        "logging.basicConfig(filename=)",
    ),
    "fileinput.FileInput": (
        "import fileinput\nfileinput.FileInput(fs)",
        "fileinput.FileInput()",
    ),
```

and in `NAMED`:

```python
    "gzip.open, binary by default": "import gzip\ngzip.open(p)",
    "gzip.open text, keyword": 'import gzip\ngzip.open(p, "rt", encoding="utf-8")',
    "logging.FileHandler, positional": 'import logging\nlogging.FileHandler(p, "a", "utf-8")',
    "logging.basicConfig, no file": "import logging\nlogging.basicConfig(level=1)",
```

The docstring's K1 list gains a bullet:

```text
- `gzip.open`, `bz2.open`, `lzma.open` in a mode carrying `t`;
  `logging.FileHandler` and the three file handlers of `logging.handlers`,
  `logging.basicConfig(filename=...)`, and `fileinput.FileInput`;
```

and `spec.md`'s K1 table gains the same rows, since it is the document the
module calls its table.

### 🟡 3 — the two Markdown one-liners

`skills/update/SKILL.md:45`:

```bash
p=$(python3 -c "import json,os;d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'),encoding='utf-8'));print(d['plugins']['specseal@specseal'][0]['installPath'])")
```

`skills/implement/orchestration.md:115`:

```bash
     python3 -c 'import json, os; print("v" + json.load(open(os.path.join(os.environ["CLAUDE_PLUGIN_ROOT"], ".claude-plugin", "plugin.json"), encoding="utf-8"))["version"])'
```

Needs a fix: yes — 🟡 1 (the unbound Path methods pass the walker), 🟡 2 (K1 omits the standard library's other text openers), 🟡 3 (two shipped Markdown one-liners open a file with no encoding)

Loses a record or crashes: no

## Proof — files opened

- `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/`:
  `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`,
  `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`
- `seal/ledger/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding.md`
  (rows E1–E5 and a sample of the re-read rows)
- `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`
  (whole)
- `tests/test_the_commit_gate_decides_at_the_commit.py` (the S8 case and the
  `g` helper)
- `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`
  (the wrapper case)
- `hooks/console.py`, `hooks/commitgate.py` (the three hook functions),
  `hooks/git/post-commit.py`, `hooks/git/reference-transaction.py`,
  `hooks/implementer-notice.py` (`notify`, `line`), `hooks/version-check.py`
  (`running`, `due`), `hooks/session-lease.py` (`main`),
  `hooks/worktree-guard.py` (the two lease reads)
- the diff from the base for `hooks/`, `.github/scripts/` and
  `CONTRIBUTING.md`
- `skills/update/SKILL.md`, `skills/implement/orchestration.md:115`,
  `.github/workflows/hygiene.yml:70`–`85`, `bin/test`, `bin/mutation-check`
