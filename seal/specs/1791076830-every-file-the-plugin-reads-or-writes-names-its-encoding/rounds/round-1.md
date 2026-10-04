# 1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding — review round 1

| Field | Value |
|---|---|
| Target SHA | 9e1759d515dd3c5c7bd99e33a5da52c56445a954 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #757 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the unbound Path methods pass the walker), 🟡 2 (K1 omits the standard library's other text openers), 🟡 3 (two shipped Markdown one-liners open a file with no encoding) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item `1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding` (#741, PR #757), target `9e1759d5` against `release/v0.18.1` at `e141980a`. Spec compliance comes first: the walker's class (K1–K4: every call that can open text without naming an encoding, a mode it cannot prove, `encoding=None`, a `*`/`**` splat, and the alias `subprocess` is imported under), the allowlist with its liveness half, the entry-point half, and D7 (a hook read must not newly raise, because a raise inside a hook lets the command through). Quality comes second. Enumerate the walker's misses by construction: every text-opening API in the standard library, crossed with every way to spell the call. Check that each of the 29 product edits keeps its failure direction. The orchestrator verified the 44 changed test modules (2325 passed, 79 skipped) and ruff on the 64 changed Python files at the target. The smith left one question for this round: under an ASCII console, `hooks/git/post-commit.py`'s stdout keeps strict errors.

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

## Paste-ready fixes

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
```python
    "gzip.open, binary by default": "import gzip\ngzip.open(p)",
    "gzip.open text, keyword": 'import gzip\ngzip.open(p, "rt", encoding="utf-8")',
    "logging.FileHandler, positional": 'import logging\nlogging.FileHandler(p, "a", "utf-8")',
    "logging.basicConfig, no file": "import logging\nlogging.basicConfig(level=1)",
```
```text
- `gzip.open`, `bz2.open`, `lzma.open` in a mode carrying `t`;
  `logging.FileHandler` and the three file handlers of `logging.handlers`,
  `logging.basicConfig(filename=...)`, and `fileinput.FileInput`;
```
```bash
p=$(python3 -c "import json,os;d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'),encoding='utf-8'));print(d['plugins']['specseal@specseal'][0]['installPath'])")
```
```bash
     python3 -c 'import json, os; print("v" + json.load(open(os.path.join(os.environ["CLAUDE_PLUGIN_ROOT"], ".claude-plugin", "plugin.json"), encoding="utf-8"))["version"])'
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
