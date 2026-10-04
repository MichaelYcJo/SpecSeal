"""Every file the plugin reads or writes names its encoding (#741).

A file opened, read or written without `encoding=` takes the locale's
encoding. That is UTF-8 on macOS and on the ubuntu runner and cp1252 on
`windows-latest`, so the class is invisible everywhere except the one CI leg
nobody runs locally. #736 met it after review: a ledger row's ` · ` went out
as byte 0xB7 and came back as U+FFFD, 26 cases failed on Windows alone, and
two post-review commits repaired one branch's instances. Nothing held the next
branch to it. This module does, on every leg and on a contributor's machine.

**Why an AST walk and not ruff.** `PLW1514` is a preview rule, and it does
not see `read_text` / `write_text` called on a variable, which is most of
this class: measured 2026-10-04 on ruff 0.16.10, it reported
`Path("x").read_text()` and passed `p.read_text()` beside it. A regex over source text misses an `encoding=`
on a later line, and a reformat moves the blind spot. What the walk sees is
the table below, so **a call the walk does not know is a row to add to K1**,
not a row for `ALLOWED`.

**K1 -- the calls that take the locale's encoding when none is named.** The
standard library's half was found by construction (round 1 of #741, on
3.14): every public callable whose signature carries `encoding=None`, each
then read for whether `None` means the locale. It does not for
`TextIOWrapper.reconfigure` (keep the current one), `tarfile` (file names),
`urllib.parse`, the `xml` writers, `xml.etree.ElementInclude.default_loader`,
`xmlrpc`, `calendar` (each a fixed default), or `asyncio`'s subprocesses
(which refuse text). An opener with no
`encoding` parameter at all, like `os.popen`, is not in that construction
and is listed here by reading.

- builtin `open`, `io.open`, `codecs.open`, `os.fdopen`, in a text mode;
- `<expr>.open(...)` judged as `Path.open`, or as `zipfile.Path.open`,
  whose encoding comes one place earlier, on a `zipfile.Path`; except on
  `os`, `webbrowser`, `tarfile`, `shelve`, `dbm`, `dbm.dumb`, `wave`, PIL's
  `Image` and a `ZipFile(...)` or `TarFile(...)` built in the receiver
  itself, which open no text, and on a bare name no import binds; called on
  the class (`Path.open(p)`), every position moves one to the right;
- `<expr>.read_text(...)` and `<expr>.write_text(...)`, the same way;
- `subprocess.run` / `Popen` / `call` / `check_call` / `check_output` with
  `text=`, `universal_newlines=` or `errors=` and no `encoding`, the module
  resolved from the file's own imports;
- `subprocess.getoutput`, `subprocess.getstatusoutput`, `os.popen`;
- `tempfile.NamedTemporaryFile` / `TemporaryFile` / `SpooledTemporaryFile` in
  a literal text mode;
- `gzip`, `bz2`, `lzma` and `compression.*`'s `open` in a mode carrying `t`;
- `logging.FileHandler`, the file handlers of `logging.handlers`,
  `logging.basicConfig(filename=...)`, `logging.config.fileConfig`;
- `io.TextIOWrapper`, `fileinput.input` / `FileInput` / `hook_compressed`,
  `argparse.FileType`, `doctest.testfile` / `DocFileTest` / `DocFileSuite`,
  and the methods `.makefile()` and `.write_results_file()`.

**What no row can hold.** A static walk follows names, not values, so these
pass and no K1 row could catch them: a name rebound to an opener
(`f = open; f(p)`), a star import, `functools.partial(open, ...)`, an opener
passed by reference (`map(Path.read_text, ps)`), `getattr`, `__import__` and
a module loaded through `importlib`, `universal_newlines` given by position,
`configparser`'s `.read`, whose name is too common to match without types,
a file handler named in a string to `logging.config.dictConfig`, and a
handler subclass whose constructor calls `super().__init__(p)`. Write the
call plainly instead. The walk errs the other way too: a `ZipFile` or
`TarFile` bound to a name first (`with ZipFile(z) as zf: zf.open(n)`) is not
traced, so its `.open` is reported though it reads bytes.

**K2 -- what the walk cannot prove counts as unnamed:** a mode that is not a
literal, `encoding=None` written out, and a `*` or `**` splat on a K1 call
with no explicit `encoding`.

Any `encoding` but `None` passes: the check holds that an encoding is chosen,
not which one. The repair this repository writes is `encoding="utf-8"`.

The second half holds every hook entry point to opening its `__main__` block
with `console.to_utf8()`, which `hooks/console.py` says each one carries
rather than relying on `dispatch.py` having made the call. It is an assertion
on the AST and on ORDER, which is why it is not the source-text check
`tests/test_console_is_not_utf8.py`'s docstring refuses: moving the call
after `main()` fails it, and so does deleting it. Whether the call itself
works is held there, behaviourally.
"""

import ast
import inspect
import os

import pytest
from conftest import (
    build_tracked_tree,
    decline_if_shrunken,
    git_listing,
    load_hook_module,
    on_disk,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

REPAIR = 'name `encoding="utf-8"`, or classify the unit in `ALLOWED` with its grounds'

# Every unit that holds an unnamed K1 call on purpose, keyed by
# `<path>#<qualname>` (`<module>` at top level), with the grounds. A row
# covers every unnamed site in its unit. A row is a classification and not a
# permission: add one only where naming the encoding cannot serve, never to
# turn this module green.
ALLOWED = {}

# Hook entry points that do not open `__main__` with `console.to_utf8()`, by
# path, with the grounds.
ENTRY_POINTS_CLASSIFIED = {
    "hooks/dispatch.py": (
        "inline reconfigure loop; held by the three dispatch cases of "
        "tests/test_console_is_not_utf8.py"
    ),
}


# --- the walker ------------------------------------------------------------

SUBPROCESS_TEXT = {"run", "Popen", "call", "check_call", "check_output"}
# Calls that always read text: unnamed unless an `encoding` keyword is given,
# which `os.popen` has no parameter for and the other two gained in 3.11.
ALWAYS_UNNAMED = {"subprocess.getoutput", "subprocess.getstatusoutput", "os.popen"}
TEMPFILES = {
    # name: (the mode's position, the encoding's position)
    "NamedTemporaryFile": (0, 2),
    "TemporaryFile": (0, 2),
    "SpooledTemporaryFile": (1, 3),
}
# `.open` receivers that open no text file: a module, or a class whose
# instance's `.open` reads bytes (`zipfile.ZipFile(z).open(name)`).
NOT_A_FILE_OPENER = {
    "os",
    "webbrowser",
    "tarfile",
    "tarfile.TarFile",
    "zipfile.ZipFile",
    "shelve",
    "dbm",
    "dbm.dumb",
    "wave",
    "PIL.Image",
}
# Classes whose methods, called on the class, take the path first, so the
# encoding's position moves one to the right: `Path.read_text(p, "utf-8")`.
UNBOUND_RECEIVERS = {
    "pathlib.Path",
    "pathlib.PurePath",
    "pathlib.PosixPath",
    "pathlib.WindowsPath",
    "zipfile.Path",
}
# Openers that are binary unless the mode carries `t`: (the mode's position,
# the encoding's position or None where it is keyword-only).
BINARY_BY_DEFAULT = {
    "gzip.open": (1, 3),
    "bz2.open": (1, 3),
    "lzma.open": (1, None),
    "compression.gzip.open": (1, 3),
    "compression.bz2.open": (1, 3),
    "compression.lzma.open": (1, None),
    "compression.zstd.open": (1, None),
}
# Calls that open a text file whatever their mode, with the encoding's
# position (None where it is keyword-only or reached through `**kwargs`).
TEXT_ALWAYS = {
    "logging.FileHandler": 2,
    "logging.handlers.BaseRotatingHandler": 2,
    "logging.handlers.WatchedFileHandler": 2,
    "logging.handlers.RotatingFileHandler": 4,
    "logging.handlers.TimedRotatingFileHandler": 4,
    "logging.config.fileConfig": 3,
    "doctest.testfile": 11,
    "doctest.DocFileTest": 5,
    "doctest.DocFileSuite": None,
}
# Calls that open text unless a literal mode carries `b`, by the dotted name
# or, for a method, by its attribute: `(the mode's position, the encoding's)`.
TEXT_UNLESS_BINARY = {
    "fileinput.input": (None, None),
    "fileinput.FileInput": (None, None),
    "fileinput.hook_compressed": (1, None),
    "argparse.FileType": (0, 2),
}
METHODS_TEXT_UNLESS_BINARY = {"makefile": (0, None), "write_results_file": (None, 4)}
# The position of `mode` and of `encoding` in each function opener's
# signature. Functions only: `judge` matches this table by the call's dotted
# name before its `.open` branch, so a method's row here would be judged
# unshifted when the method is called on its class (#762).
OPENERS = {
    "builtins.open": (1, 3),
    "io.open": (1, 3),
    "codecs.open": (1, 2),
    # `fdopen(fd, mode, buffering, encoding)` is `open` with the fd in the
    # file's slot, so the positions are `open`'s.
    "os.fdopen": (1, 3),
}
# The same positions for an `.open` method, by what `owner` resolves its
# receiver to, `<expr>` for every receiver not listed. Read by the `.open`
# branch of `judge` alone, which moves them one to the right on the class.
OPEN_METHODS = {
    "<expr>": (0, 2),
    # `zipfile.Path.open(mode, *args)` hands `args[0]` to `TextIOWrapper` as
    # the encoding, one place earlier than `pathlib.Path.open`.
    "zipfile.Path": (0, 1),
}


def bindings(tree):
    """`{local name: dotted target}` for every import in the file.

    `import subprocess as sp` binds `sp` to `subprocess`; `from subprocess
    import run` binds `run` to `subprocess.run`. Collected over the whole
    file, so an import inside a function is seen too.
    """
    bound = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    bound[alias.asname] = alias.name
                else:
                    top = alias.name.split(".")[0]
                    bound[top] = top
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            for alias in node.names:
                bound[alias.asname or alias.name] = f"{node.module}.{alias.name}"
    return bound


def target_of(func, bound):
    """The dotted name a call's function resolves to, or None.

    A bare name resolves through the file's imports, and `open` unbound is the
    builtin. An attribute chain resolves its head the same way, so
    `logging.handlers.RotatingFileHandler` is seen whole.
    """
    if isinstance(func, ast.Name) and func.id not in bound:
        return "builtins.open" if func.id == "open" else None
    return dotted(func, bound)


def dotted(node, bound):
    """`a.b.c` with its head resolved through the file's imports, or None."""
    if isinstance(node, ast.Name):
        return bound.get(node.id)
    if isinstance(node, ast.Attribute):
        head = dotted(node.value, bound)
        return f"{head}.{node.attr}" if head else None
    return None


def keyword(call, name):
    for kw in call.keywords:
        if kw.arg == name:
            return kw
    return None


def splatted(call):
    """A `*` or `**` on the call, which could carry anything (K2)."""
    return any(kw.arg is None for kw in call.keywords) or any(
        isinstance(a, ast.Starred) for a in call.args
    )


def is_none(node):
    return isinstance(node, ast.Constant) and node.value is None


def names_encoding(call, position=None):
    """Whether the call names an encoding the walk can see: a keyword, or the
    positional argument at `position`, that is not `None`."""
    kw = keyword(call, "encoding")
    if kw is not None:
        return not is_none(kw.value)
    if position is not None and len(call.args) > position:
        arg = call.args[position]
        return not isinstance(arg, ast.Starred) and not is_none(arg)
    return False


def mode_of(call, position):
    """`"text"`, `"binary"` or `"unproven"` for the call's mode, with
    `"absent"` where none is given."""
    node = mode_node(call, position)
    if node is None:
        return "absent"
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return "binary" if "b" in node.value else "text"
    return "unproven"


def mode_node(call, position):
    """The node given as `mode`, by keyword or at `position` (None where the
    parameter is keyword-only), or None."""
    kw = keyword(call, "mode")
    if kw is not None:
        return kw.value
    if position is not None and len(call.args) > position:
        return call.args[position]
    return None


def judge_opener(call, opener, positions, shift=0):
    """The kind to report for a call to `opener`, whose mode and encoding sit
    at `positions`, or None if it names its encoding or opens in binary.
    `shift` is 1 where the call is a method called on its class, whose first
    argument is the path."""
    mode_at, encoding_at = (at + shift for at in positions)
    if names_encoding(call, encoding_at):
        return None
    mode = mode_of(call, mode_at)
    if mode == "binary":
        return None
    kind = opener.replace("builtins.", "") + "()"
    if mode == "unproven":
        return f"{kind}, mode not a literal"
    if splatted(call):
        return f"{kind}, splat"
    return kind


def judge(call, bound):
    """The kind of unnamed K1 call this is, or None."""
    target = target_of(call.func, bound)
    func = call.func

    if target in OPENERS:
        return judge_opener(call, target, OPENERS[target])
    if target in ALWAYS_UNNAMED:
        return None if names_encoding(call) else f"{target}()"
    if target in BINARY_BY_DEFAULT:
        mode_at, encoding_at = BINARY_BY_DEFAULT[target]
        if names_encoding(call, encoding_at):
            return None
        node = mode_node(call, mode_at)
        if node is None:
            return f"{target}(), splat" if splatted(call) else None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return f"{target}()" if "t" in node.value else None
        return f"{target}(), mode not a literal"
    if target in TEXT_ALWAYS:
        if names_encoding(call, TEXT_ALWAYS[target]):
            return None
        return f"{target}(), splat" if splatted(call) else f"{target}()"
    if target in TEXT_UNLESS_BINARY:
        return judge_text(call, f"{target}()", *TEXT_UNLESS_BINARY[target])
    if target == "logging.basicConfig":
        if names_encoding(call):
            return None
        if splatted(call):
            return "logging.basicConfig(), splat"
        return "logging.basicConfig(filename=)" if keyword(call, "filename") else None
    if target and target.startswith("subprocess."):
        name = target.split(".", 1)[1]
        if name not in SUBPROCESS_TEXT or names_encoding(call):
            return None
        if splatted(call):
            return f"{target}(), splat"
        for flag in ("text", "universal_newlines", "errors"):
            kw = keyword(call, flag)
            if kw is None:
                continue
            if flag != "errors" and (
                isinstance(kw.value, ast.Constant) and kw.value.value is False
            ):
                continue
            return f"{target}({flag}=)"
        return None
    if target and target.startswith("tempfile."):
        name = target.split(".", 1)[1]
        if name not in TEMPFILES:
            return None
        mode_at, encoding_at = TEMPFILES[name]
        if names_encoding(call, encoding_at):
            return None
        mode = mode_of(call, mode_at)
        if mode == "unproven":
            return f"{target}(), mode not a literal"
        if mode == "text":
            return f"{target}()"
        if splatted(call):
            return f"{target}(), splat"
        return None
    if target == "io.TextIOWrapper":
        return None if names_encoding(call, 1) else "io.TextIOWrapper()"

    if not isinstance(func, ast.Attribute):
        return None
    shift = 1 if dotted(func.value, bound) in UNBOUND_RECEIVERS else 0
    if func.attr == "open":
        made_by = owner(func.value, bound)
        if made_by in NOT_A_FILE_OPENER:
            return None
        made_by = made_by if made_by in OPEN_METHODS else "<expr>"
        return judge_opener(call, f"{made_by}.open", OPEN_METHODS[made_by], shift)
    if func.attr == "read_text":
        if names_encoding(call, shift):
            return None
        return ".read_text(), splat" if splatted(call) else ".read_text()"
    if func.attr == "write_text":
        if names_encoding(call, 1 + shift):
            return None
        return ".write_text(), splat" if splatted(call) else ".write_text()"
    if func.attr in METHODS_TEXT_UNLESS_BINARY:
        return judge_text(
            call, f".{func.attr}()", *METHODS_TEXT_UNLESS_BINARY[func.attr]
        )
    return None


def owner(receiver, bound):
    """What a `.open` is called on: the dotted name of a receiver, of the
    class a receiver call constructs (`zipfile.ZipFile(z)`), or a bare name no
    import binds, read as itself (`os` taken as a parameter). An instance
    bound to a name first (`with ZipFile(z) as zf`) is not traced."""
    if isinstance(receiver, ast.Call):
        return dotted(receiver.func, bound)
    if isinstance(receiver, ast.Name) and receiver.id not in bound:
        return receiver.id
    return dotted(receiver, bound)


def judge_text(call, kind, mode_at, encoding_at):
    """`kind` for a call that opens text unless a literal mode carries `b`,
    or None where it names its encoding or opens in binary."""
    if names_encoding(call, encoding_at):
        return None
    mode = mode_of(call, mode_at)
    if mode == "binary":
        return None
    if mode == "unproven":
        return f"{kind}, mode not a literal"
    return f"{kind}, splat" if splatted(call) else kind


class _Walk(ast.NodeVisitor):
    def __init__(self, bound):
        self.bound = bound
        self.stack = []
        self.found = []

    def _unit(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = visit_ClassDef = _unit

    def visit_Call(self, node):
        kind = judge(node, self.bound)
        if kind:
            qualname = ".".join(self.stack) or "<module>"
            self.found.append((node.lineno, kind, qualname))
        self.generic_visit(node)


def unnamed_sites(source, path="<source>"):
    """`[(line, kind, qualname)]` for every K1 call in `source` that names no
    encoding, in line order."""
    tree = ast.parse(source, filename=path)
    walk = _Walk(bindings(tree))
    walk.visit(tree)
    return sorted(walk.found)


# --- the corpus ------------------------------------------------------------


def tracked_python(root=ROOT):
    """`(every tracked `.py` on disk, the tracked paths that are not)`.

    Every tracked `.py` rather than a list of roots, so a fifth root is judged
    on arrival rather than when somebody remembers to extend a list. The
    tests are in it: a fixture written in the locale's encoding is read back
    wrong on the Windows leg, which is how #736 met this class.
    """
    out = git_listing(root, "ls-files", "*.py")
    listed = [rel for rel in out if rel]
    return on_disk(root, listed)


def sites_in(root=ROOT):
    """`({"<path>#<qualname>": [(line, kind)]}, missing)` over the corpus."""
    files, missing = tracked_python(root)
    assert files, "git ls-files found no python at all"
    units = {}
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8") as f:
            source = f.read()
        for line, kind, qualname in unnamed_sites(source, rel):
            units.setdefault(f"{rel}#{qualname}", []).append((line, kind))
    return units, missing


def unclassified(units, allowed):
    """Each unnamed site outside `allowed`, as `path:line (kind, unit)`."""
    out = []
    for unit, found in units.items():
        if unit in allowed:
            continue
        path, qualname = unit.split("#", 1)
        out += [
            (path, line, f"{path}:{line} ({kind}, {qualname})") for line, kind in found
        ]
    return [site for _, _, site in sorted(out)]


DECLINES_ALLOWED = "the liveness half of ALLOWED"


def classifications_of_nothing(units, missing, allowed):
    """The `allowed` units that hold no unnamed call any more, or
    `pytest.skip` when a file the tree deleted could be the reason."""
    gone = sorted(set(allowed) - set(units))
    if gone:
        decline_if_shrunken(missing, DECLINES_ALLOWED)
    return gone


def failure(sites):
    return (
        f"{len(sites)} call(s) read or write a file in the locale's encoding, "
        "which is cp1252 on the Windows leg: "
        + "; ".join(sites)
        + f". At each one, {REPAIR}."
    )


# --- the repository case ---------------------------------------------------


def test_every_file_the_plugin_reads_or_writes_names_its_encoding():
    """The class, enumerated by construction over every tracked `.py`."""
    units, missing = sites_in()
    sites = unclassified(units, ALLOWED)
    assert not sites, failure(sites)
    gone = classifications_of_nothing(units, missing, ALLOWED)
    assert not gone, (
        f"{gone} hold no unnamed call any more; drop the row rather than "
        "leaving a classification of nothing"
    )


def test_the_rule_is_where_a_contributor_reads_it():
    """`CONTRIBUTING.md`'s House rules names the rule and this module, the
    way *No real identifiers* names its own."""
    with open(os.path.join(ROOT, "CONTRIBUTING.md"), encoding="utf-8") as f:
        text = f.read()
    rules = text.split("\n## House rules\n", 1)[1].split("\n## ", 1)[0]
    flat = " ".join(rules.split())
    assert "**Every file read or written names its encoding.**" in flat, flat
    assert 'Name `encoding="utf-8"`.' in flat
    assert f"`tests/{os.path.basename(__file__)}`" in flat
    assert "opens its `__main__` with `console.to_utf8()`" in flat


def test_every_classification_carries_its_grounds():
    for table in (ALLOWED, ENTRY_POINTS_CLASSIFIED):
        empty = sorted(k for k, v in table.items() if not str(v).strip())
        assert not empty, f"{empty} are classified with no grounds"


def test_the_failure_names_the_site_and_the_repair():
    """A person reads this at a red Windows leg and acts on it (§14)."""
    message = failure(["hooks/x.py:3 (open(), main)"])
    assert "hooks/x.py:3 (open(), main)" in message, message
    assert (
        'At each one, name `encoding="utf-8"`, or classify the unit in '
        "`ALLOWED` with its grounds." in message
    ), message


# --- each K1 shape ---------------------------------------------------------

# `(source, kind)`: the source holds one unnamed call on its last line.
UNNAMED = {
    "builtin open": ("open(p)", "open()"),
    "builtin open, text mode": ('open(p, "w")', "open()"),
    "io.open": ("import io\nio.open(p)", "io.open()"),
    "codecs.open": ("import codecs\ncodecs.open(p)", "codecs.open()"),
    "os.fdopen": ('import os\nos.fdopen(fd, "w")', "os.fdopen()"),
    "Path.open": ("p.open()", "<expr>.open()"),
    "Path.open, text mode": ('p.open("w")', "<expr>.open()"),
    "read_text": ("p.read_text()", ".read_text()"),
    "write_text": ("p.write_text(s)", ".write_text()"),
    "subprocess.run text": (
        "import subprocess\nsubprocess.run(c, text=True)",
        "subprocess.run(text=)",
    ),
    "subprocess.Popen universal_newlines": (
        "import subprocess\nsubprocess.Popen(c, universal_newlines=1)",
        "subprocess.Popen(universal_newlines=)",
    ),
    "subprocess.check_output errors": (
        'import subprocess\nsubprocess.check_output(c, errors="replace")',
        "subprocess.check_output(errors=)",
    ),
    "subprocess.call text": (
        "import subprocess\nsubprocess.call(c, text=t)",
        "subprocess.call(text=)",
    ),
    "subprocess.check_call text": (
        "import subprocess\nsubprocess.check_call(c, text=True)",
        "subprocess.check_call(text=)",
    ),
    "subprocess.getoutput": (
        "import subprocess\nsubprocess.getoutput(c)",
        "subprocess.getoutput()",
    ),
    "subprocess.getstatusoutput": (
        "import subprocess\nsubprocess.getstatusoutput(c)",
        "subprocess.getstatusoutput()",
    ),
    "os.popen": ("import os\nos.popen(c)", "os.popen()"),
    "NamedTemporaryFile text": (
        'import tempfile\ntempfile.NamedTemporaryFile("w")',
        "tempfile.NamedTemporaryFile()",
    ),
    "TemporaryFile text": (
        'import tempfile\ntempfile.TemporaryFile(mode="w+")',
        "tempfile.TemporaryFile()",
    ),
    "SpooledTemporaryFile text": (
        'import tempfile\ntempfile.SpooledTemporaryFile(0, "w+")',
        "tempfile.SpooledTemporaryFile()",
    ),
    "TextIOWrapper": ("import io\nio.TextIOWrapper(b)", "io.TextIOWrapper()"),
    "fileinput": ("import fileinput\nfileinput.input(fs)", "fileinput.input()"),
    # Round 1 of #741: a method called on its class takes the path first.
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
    # Round 1 of #741: the standard library's other text openers, found by
    # every public callable whose signature carries `encoding=None`.
    "gzip.open text": ('import gzip\ngzip.open("x.gz", "rt")', "gzip.open()"),
    "bz2.open text, a b in the path": (
        'import bz2\nbz2.open("x.bz2", "rt")',
        "bz2.open()",
    ),
    "lzma.open text, imported by name": (
        'from lzma import open\nopen(p, "rt")',
        "lzma.open()",
    ),
    "compression.zstd.open text": (
        'from compression import zstd\nzstd.open(p, "rt")',
        "compression.zstd.open()",
    ),
    "logging.FileHandler": (
        "import logging\nlogging.FileHandler(p)",
        "logging.FileHandler()",
    ),
    "RotatingFileHandler": (
        "import logging.handlers\nlogging.handlers.RotatingFileHandler(p)",
        "logging.handlers.RotatingFileHandler()",
    ),
    "TimedRotatingFileHandler, imported by name": (
        "from logging.handlers import TimedRotatingFileHandler\nTimedRotatingFileHandler(p)",
        "logging.handlers.TimedRotatingFileHandler()",
    ),
    "WatchedFileHandler": (
        "import logging.handlers\nlogging.handlers.WatchedFileHandler(p)",
        "logging.handlers.WatchedFileHandler()",
    ),
    "logging.basicConfig with a file": (
        "import logging\nlogging.basicConfig(filename=p)",
        "logging.basicConfig(filename=)",
    ),
    "logging.config.fileConfig": (
        "import logging.config\nlogging.config.fileConfig(p)",
        "logging.config.fileConfig()",
    ),
    "fileinput.FileInput": (
        "import fileinput\nfileinput.FileInput(fs)",
        "fileinput.FileInput()",
    ),
    "fileinput.hook_compressed": (
        'import fileinput\nfileinput.hook_compressed(p, "r")',
        "fileinput.hook_compressed()",
    ),
    "argparse.FileType": (
        'import argparse\nargparse.FileType("w")',
        "argparse.FileType()",
    ),
    "doctest.testfile": ("import doctest\ndoctest.testfile(p)", "doctest.testfile()"),
    "doctest.DocFileSuite": (
        "import doctest\ndoctest.DocFileSuite(p)",
        "doctest.DocFileSuite()",
    ),
    "socket makefile": ("s.makefile()", ".makefile()"),
    "trace write_results_file": (
        "r.write_results_file(p, l, n, h)",
        ".write_results_file()",
    ),
    "zipfile.Path open is still judged": (
        "import zipfile\nzipfile.Path(z).open()",
        "zipfile.Path.open()",
    ),
    # #762: called on its class, `zipfile.Path.open` takes the path first, so
    # `"r"` is the mode and no encoding is named.
    "zipfile.Path open unbound, mode only": (
        'import zipfile\nzipfile.Path.open(q, "r")',
        "zipfile.Path.open()",
    ),
    "zipfile.Path open unbound, imported by name": (
        'from zipfile import Path\nPath.open(q, "r")',
        "zipfile.Path.open()",
    ),
    "zipfile.Path open unbound, aliased module": (
        'import zipfile as z\nz.Path.open(q, "r")',
        "zipfile.Path.open()",
    ),
}

# The same calls with the encoding named (by keyword, or positionally where
# the signature allows), or in a binary mode.
NAMED = {
    "builtin open, keyword": 'open(p, encoding="utf-8")',
    "builtin open, 4th positional": 'open(p, "r", -1, "utf-8")',
    "builtin open, binary": 'open(p, "rb")',
    "io.open, keyword": 'import io\nio.open(p, encoding="utf-8")',
    "codecs.open, 3rd positional": 'import codecs\ncodecs.open(p, "r", "utf-8")',
    "os.fdopen, binary": 'import os\nos.fdopen(fd, "wb")',
    "os.fdopen, keyword": 'import os\nos.fdopen(fd, "w", encoding="utf-8")',
    "Path.open, keyword": 'p.open(encoding="utf-8")',
    "Path.open, 3rd positional": 'p.open("r", -1, "utf-8")',
    "Path.open, binary": 'p.open("rb")',
    "read_text, keyword": 'p.read_text(encoding="utf-8")',
    "read_text, positional": 'p.read_text("utf-8")',
    "write_text, keyword": 'p.write_text(s, encoding="utf-8")',
    "write_text, positional": 'p.write_text(s, "utf-8")',
    "subprocess.run, encoding": (
        'import subprocess\nsubprocess.run(c, text=True, encoding="utf-8")'
    ),
    "subprocess.run, bytes": "import subprocess\nsubprocess.run(c, capture_output=True)",
    "subprocess.run, text=False": "import subprocess\nsubprocess.run(c, text=False)",
    "NamedTemporaryFile, default binary": "import tempfile\ntempfile.NamedTemporaryFile()",
    "NamedTemporaryFile, keyword": (
        'import tempfile\ntempfile.NamedTemporaryFile("w", encoding="utf-8")'
    ),
    "TextIOWrapper, positional": 'import io\nio.TextIOWrapper(b, "utf-8")',
    "fileinput, keyword": 'import fileinput\nfileinput.input(fs, encoding="utf-8")',
    "fileinput, binary": 'import fileinput\nfileinput.input(fs, mode="rb")',
    "os.open is not a file opener": "import os\nos.open(p, os.O_RDONLY)",
    "webbrowser.open is not a file opener": "import webbrowser\nwebbrowser.open(u)",
    "Path.read_text, unbound, positional": 'from pathlib import Path\nPath.read_text(p, "utf-8")',
    "Path.write_text, unbound, positional": (
        'from pathlib import Path\nPath.write_text(p, s, "utf-8")'
    ),
    "gzip.open, binary by default": "import gzip\ngzip.open(p)",
    "gzip.open text, keyword": 'import gzip\ngzip.open(p, "rt", encoding="utf-8")',
    "lzma.open text, keyword": 'import lzma\nlzma.open(p, "rt", encoding="utf-8")',
    "logging.FileHandler, positional": 'import logging\nlogging.FileHandler(p, "a", "utf-8")',
    "RotatingFileHandler, 5th positional": (
        'import logging.handlers\nlogging.handlers.RotatingFileHandler(p, "a", 0, 0, "utf-8")'
    ),
    "logging.basicConfig, no file": "import logging\nlogging.basicConfig(level=1)",
    "logging.basicConfig, file and encoding": (
        'import logging\nlogging.basicConfig(filename=p, encoding="utf-8")'
    ),
    "argparse.FileType, binary": 'import argparse\nargparse.FileType("rb")',
    "fileinput.FileInput, binary": 'import fileinput\nfileinput.FileInput(fs, mode="rb")',
    "socket makefile, binary": 's.makefile("rb")',
    "ElementInclude.default_loader, xml": (
        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "xml")'
    ),
    "getoutput, keyword": 'import subprocess\nsubprocess.getoutput(c, encoding="utf-8")',
    "tarfile.open is binary": "import tarfile\ntarfile.open(p)",
    "TarFile.open is binary": "import tarfile\ntarfile.TarFile.open(p)",
    "ZipFile(...).open is binary": "import zipfile\nzipfile.ZipFile(z).open(n)",
    "PIL Image.open is binary": "from PIL import Image\nImage.open(p)",
    "shelve.open is not a text file": "import shelve\nshelve.open(p)",
    "dbm.open is not a text file": "import dbm\ndbm.open(p)",
    "wave.open is binary": "import wave\nwave.open(p)",
    # Round 2 of #741.
    "ElementInclude.default_loader, text reads UTF-8 itself": (
        'from xml.etree import ElementInclude\nElementInclude.default_loader(h, "text")'
    ),
    "os.open on a name no import binds": "def f(os):\n    return os.open(p, 0)",
    "dbm.dumb.open is not a text file": "import dbm.dumb\ndbm.dumb.open(p)",
    "zipfile.Path open, 2nd positional": (
        'import zipfile\nzipfile.Path(z).open("r", "utf-8")'
    ),
    "zipfile.Path open unbound, 3rd positional": (
        'import zipfile\nzipfile.Path.open(q, "r", "utf-8")'
    ),
}


@pytest.mark.parametrize("shape", sorted(UNNAMED))
def test_each_unnamed_shape_is_reported(shape):
    source, kind = UNNAMED[shape]
    line = source.count("\n") + 1
    assert unnamed_sites(source) == [(line, kind, "<module>")]


@pytest.mark.parametrize("shape", sorted(NAMED))
def test_each_named_shape_is_not_reported(shape):
    assert unnamed_sites(NAMED[shape]) == []


def tables_matched_by_dotted_name():
    """`{name: table}` for every table `judge` tests `target in`, read from
    `judge`'s own source, so a table added there later is read here too."""
    tree = ast.parse(inspect.getsource(judge))
    names = {
        node.comparators[0].id
        for node in ast.walk(tree)
        if isinstance(node, ast.Compare)
        and isinstance(node.left, ast.Name)
        and node.left.id == "target"
        and isinstance(node.ops[0], ast.In)
        and isinstance(node.comparators[0], ast.Name)
    }
    return {name: globals()[name] for name in sorted(names)}


def methods_of_unbound_receivers(tables):
    """Each key of `tables` that is a method of a class in
    `UNBOUND_RECEIVERS`, as `TABLE['key']`."""
    return sorted(
        f"{name}[{key!r}]"
        for name, table in tables.items()
        for key in table
        if key.rsplit(".", 1)[0] in UNBOUND_RECEIVERS
    )


def test_no_method_is_matched_by_its_dotted_name():
    """#762: a method called on its class takes the path first, and only the
    `.open` branch of `judge` moves the positions for it. A method's row in a
    table `judge` matches by dotted name is reached there first, unshifted,
    so its path is read as the mode and its mode as the encoding."""
    tables = tables_matched_by_dotted_name()
    assert "OPENERS" in tables, tables
    # The row #762 moved out, so the check is shown to name one.
    moved = {"OPENERS": {"zipfile.Path.open": (0, 1), "io.open": (1, 3)}}
    assert methods_of_unbound_receivers(moved) == ["OPENERS['zipfile.Path.open']"]
    methods = methods_of_unbound_receivers(tables)
    assert not methods, (
        f"{methods} are methods of a class in UNBOUND_RECEIVERS, matched by "
        "their dotted name before the `.open` branch can shift them"
    )


# --- K2: what the walk cannot prove ----------------------------------------

UNPROVEN = {
    "a mode that is not a literal": ("open(p, m)", "open(), mode not a literal"),
    "encoding=None written out": ("open(p, encoding=None)", "open()"),
    "None in the encoding's position": ('open(p, "r", -1, None)', "open()"),
    "a ** splat": ("open(p, **kw)", "open(), splat"),
    "a * splat": ("open(*a)", "open(), splat"),
    "a ** splat on read_text": ("p.read_text(**kw)", ".read_text(), splat"),
    "a ** splat on subprocess": (
        "import subprocess\nsubprocess.run(c, **kw)",
        "subprocess.run(), splat",
    ),
    "a tempfile mode that is not a literal": (
        "import tempfile\ntempfile.TemporaryFile(m)",
        "tempfile.TemporaryFile(), mode not a literal",
    ),
    "a gzip mode that is not a literal": (
        "import gzip\ngzip.open(p, m)",
        "gzip.open(), mode not a literal",
    ),
}


@pytest.mark.parametrize("shape", sorted(UNPROVEN))
def test_what_the_walk_cannot_prove_counts_as_unnamed(shape):
    source, kind = UNPROVEN[shape]
    line = source.count("\n") + 1
    assert unnamed_sites(source) == [(line, kind, "<module>")]


# --- aliases ---------------------------------------------------------------


def test_an_aliased_module_is_resolved():
    source = "import subprocess as sp\nsp.run(c, text=True)\n"
    assert unnamed_sites(source) == [(2, "subprocess.run(text=)", "<module>")]


def test_a_function_imported_by_name_is_resolved():
    source = "from subprocess import run as r, check_output\n" + (
        "r(c, text=True)\ncheck_output(c, text=True)\n"
    )
    assert unnamed_sites(source) == [
        (2, "subprocess.run(text=)", "<module>"),
        (3, "subprocess.check_output(text=)", "<module>"),
    ]


def test_a_local_function_named_run_is_not_a_subprocess_call():
    source = (
        "def run(c, text):\n    return c\n\nrun(c, text=True)\nx.run(c, text=True)\n"
    )
    assert unnamed_sites(source) == []


def test_an_import_inside_a_function_is_seen():
    source = "def f():\n    from os import popen\n    return popen(c)\n"
    assert unnamed_sites(source) == [(3, "os.popen()", "f")]


def test_the_unit_is_the_enclosing_qualname():
    source = (
        "class C:\n"
        "    def m(self):\n"
        "        def inner():\n"
        "            return p.read_text()\n"
        "        return inner\n"
        "p.write_text(s)\n"
    )
    assert unnamed_sites(source) == [
        (4, ".read_text()", "C.m.inner"),
        (6, ".write_text()", "<module>"),
    ]


# --- the classification table's liveness half ------------------------------


def test_a_classification_of_nothing_is_reported(tmp_path):
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "hooks/a.py": "def f():\n    return p.read_text()\n",
            "hooks/b.py": 'def g():\n    return p.read_text(encoding="utf-8")\n',
        },
    )
    allowed = {"hooks/a.py#f": "grounds", "hooks/b.py#g": "grounds"}
    units, missing = sites_in(root)
    assert unclassified(units, allowed) == []
    assert classifications_of_nothing(units, missing, allowed) == ["hooks/b.py#g"]


def test_a_skipped_file_does_not_read_as_a_lost_classification(tmp_path):
    """A row whose file the working tree deleted would otherwise be reported
    as a classification of nothing, and the instruction that comes with that
    report is to DROP the row on evidence about a working tree."""
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "hooks/a.py": "def f():\n    return p.read_text()\n",
            "hooks/other.py": "nothing = 1\n",
        },
        deleted=["hooks/a.py"],
    )
    units, missing = sites_in(root)
    assert missing == ["hooks/a.py"], missing
    with pytest.raises(pytest.skip.Exception) as declined:
        classifications_of_nothing(units, missing, {"hooks/a.py#f": "grounds"})
    reason = str(declined.value)
    assert "hooks/a.py" in reason and DECLINES_ALLOWED in reason, reason


def test_the_walk_reaches_a_root_nobody_listed(tmp_path):
    """The corpus is every tracked `.py`, so a fifth root is judged on
    arrival."""
    root = build_tracked_tree(
        tmp_path / "r", {"evals/new.py": "p.write_text(s)\n", "notes.txt": "x\n"}
    )
    units, _ = sites_in(root)
    assert unclassified(units, {}) == ["evals/new.py:1 (.write_text(), <module>)"]


# --- the hook entry points -------------------------------------------------


def is_main_guard(node):
    if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
        return False
    test = node.test
    sides = [test.left, *test.comparators]
    return (
        len(test.ops) == 1
        and isinstance(test.ops[0], ast.Eq)
        and any(isinstance(s, ast.Name) and s.id == "__name__" for s in sides)
        and any(isinstance(s, ast.Constant) and s.value == "__main__" for s in sides)
    )


def opens_with_to_utf8(guard):
    first = guard.body[0]
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Call)
        and isinstance(first.value.func, ast.Attribute)
        and first.value.func.attr == "to_utf8"
        and isinstance(first.value.func.value, ast.Name)
        and first.value.func.value.id == "console"
        and not first.value.args
        and not first.value.keywords
    )


def entry_point_verdict(source, path="<source>"):
    """None for a file with no module-level `__main__` block, else whether its
    first statement is `console.to_utf8()`."""
    tree = ast.parse(source, filename=path)
    guards = [n for n in tree.body if is_main_guard(n)]
    if not guards:
        return None
    return all(opens_with_to_utf8(g) for g in guards)


def entry_points(root=ROOT):
    """`({hook entry point: opens with the call}, missing)`."""
    out = git_listing(root, "ls-files", "hooks/*.py")
    files, missing = on_disk(root, [rel for rel in out if rel])
    verdicts = {}
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8") as f:
            verdict = entry_point_verdict(f.read(), rel)
        if verdict is not None:
            verdicts[rel] = verdict
    return verdicts, missing


DECLINES_ENTRY_POINTS = "the liveness half of ENTRY_POINTS_CLASSIFIED"


def lacking_and_gone(verdicts, missing, classified):
    """`(entry points lacking the call and not classified, classified paths
    that are no longer an entry point lacking it)`, or `pytest.skip` when a
    file the tree deleted could be why a classified path looks gone."""
    lacking = sorted(p for p, ok in verdicts.items() if not ok and p not in classified)
    gone = sorted(p for p in classified if verdicts.get(p) is not False)
    if gone:
        decline_if_shrunken(missing, DECLINES_ENTRY_POINTS)
    return lacking, gone


def test_every_hook_entry_point_opens_with_to_utf8():
    verdicts, missing = entry_points()
    assert verdicts, "git ls-files found no hook entry point at all"
    lacking, gone = lacking_and_gone(verdicts, missing, ENTRY_POINTS_CLASSIFIED)
    assert not lacking, (
        f"{lacking} do not open `if __name__ == '__main__':` with "
        "`console.to_utf8()`. A hook that raises while printing dies with "
        "stdout empty, which is how a hook says nothing applies. Make the "
        "call the block's first statement, as hooks/console.py says"
    )
    assert not gone, (
        f"{gone} are classified and are no longer an entry point lacking the "
        "call; drop the row"
    )


def test_an_entry_point_classification_of_nothing_is_reported(tmp_path):
    guard = 'if __name__ == "__main__":\n'
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "hooks/bare.py": guard + "    main()\n",
            "hooks/fixed.py": guard + "    console.to_utf8()\n    main()\n",
            "hooks/sub/deep.py": guard + "    main()\n",
            "hooks/module.py": "x = 1\n",
        },
    )
    verdicts, missing = entry_points(root)
    assert verdicts == {
        "hooks/bare.py": False,
        "hooks/fixed.py": True,
        "hooks/sub/deep.py": False,
    }, verdicts
    classified = {"hooks/bare.py": "grounds", "hooks/fixed.py": "grounds"}
    lacking, gone = lacking_and_gone(verdicts, missing, classified)
    assert lacking == ["hooks/sub/deep.py"] and gone == ["hooks/fixed.py"]


def test_a_deleted_entry_point_declines_rather_than_drops_its_row(tmp_path):
    root = build_tracked_tree(
        tmp_path / "r",
        {"hooks/bare.py": 'if __name__ == "__main__":\n    main()\n'},
        deleted=["hooks/bare.py"],
    )
    verdicts, missing = entry_points(root)
    assert verdicts == {} and missing == ["hooks/bare.py"]
    with pytest.raises(pytest.skip.Exception) as declined:
        lacking_and_gone(verdicts, missing, {"hooks/bare.py": "grounds"})
    assert DECLINES_ENTRY_POINTS in str(declined.value)


def test_the_call_after_main_is_reported():
    source = (
        "import console\n\n"
        "def main():\n    return 0\n\n"
        "if __name__ == '__main__':\n    main()\n    console.to_utf8()\n"
    )
    assert entry_point_verdict(source) is False


def test_the_call_first_is_accepted_and_a_module_is_not_an_entry_point():
    head = "import console, sys\n\n"
    assert (
        entry_point_verdict(
            head
            + 'if __name__ == "__main__":\n    console.to_utf8()\n    sys.exit(0)\n'
        )
        is True
    )
    assert entry_point_verdict(head + "def f():\n    return 0\n") is None


# --- a converted read inside a hook does not newly raise -------------------


def test_a_mark_that_is_not_utf8_reads_as_text_rather_than_raising(tmp_path):
    """#741's D7, at the one hook read whose handler catches `OSError` alone.

    On a cp1252 machine the unnamed read never raised, because cp1252 decodes
    almost any byte; strict UTF-8 raises `UnicodeDecodeError`. Inside a hook
    that raise reaches `dispatch.py`'s `except Exception`, which is an allow,
    so naming the encoding must not be what turns a stray byte into a pass."""
    crg = load_hook_module("commit-review-gate.py", "crg_for_the_encoding_case")
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "specseal-reviewed").write_bytes(b"\xffabc\n")
    got = crg.read_mark(str(tmp_path), ".git", "specseal-reviewed")
    assert got == "�abc", repr(got)
