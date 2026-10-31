"""The censuses: rules every tracked file of a kind keeps, each judged one
file at a time (#942).

A module file runs every census over its own target: its last line is
`test_census = census_case(TARGET)`, from `tests/conftest.py`, so the run a
contributor makes of the module they touched judges that module too.
`tests/test_censuses.py` runs them once more over every tracked file no
module file declares as its `TARGET`, and holds each census's own cases.

Each census is `<name>(rel, root=None)` and returns one line per problem,
`<rel>:<line>: <name>: <what and the repair>`. REL is the file's path from
the repository root, written with `/`, and ROOT is this repository unless a
case hands another. A census reads the file at REL, and `floor_syntax` reads
`ruff.toml` beside it; a file outside a census's kind gets no line from it.

**An exemption is a comment line directly above the line it exempts**, of
the form `# exempt from <name>: <why>`, where <name> is the census's name
and <why> says what makes the line not the defect the census looks for. It
stands on a line of its own, among the comment lines directly above the
flagged line, because the formatter moves a comment that ends a long line
and splits the code around it. Above a line the census does not flag, the
comment excuses nothing, and the census refuses it, so an exemption leaves
the tree with the line it excused. No census keeps a list of exemptions.

This module imports nothing from `tests/conftest.py`:
`evals/scripts/noninferiority.py` loads it by path, without pytest, to mask
a record with `real_identifiers`' own readers.
"""

import ast
import fnmatch
import io
import os
import posixpath
import re
import tokenize

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXEMPTION = re.compile(r"^\s*#\s*exempt from ([a-z_]+):\s*\S")
COMMENT_LINE = re.compile(r"^\s*#")
SHIPPED = ("hooks/", "skills/", ".github/scripts/")


def _root(root):
    return ROOT if root is None else root


def _text(rel, root):
    """The file at REL as text with its line ends made LF, or None where it
    is not UTF-8 text."""
    try:
        with open(os.path.join(_root(root), rel), encoding="utf-8") as handle:
            return handle.read()
    except UnicodeDecodeError:
        return None


def _exempted(text, name):
    """`{exempted line: the comment line exempting it}` for every exemption
    from NAME in TEXT: a comment line among the comment lines directly above
    the line it exempts."""
    exempted, pending = {}, []
    lines = text.split("\n")
    for number, line in enumerate(lines, 1):
        if COMMENT_LINE.match(line):
            if name in EXEMPTION.findall(line):
                pending.append(number)
            continue
        for comment in pending:
            exempted[number] = comment
        pending = []
    for comment in pending:
        exempted[len(lines) + 1] = comment
    return exempted


def _held(name, rel, text, flagged):
    """The problem lines of census NAME over REL: each line FLAGGED,
    `{line: what}`, that no exemption from NAME stands above, and each
    exemption from NAME that stands above a line NAME does not flag."""
    exempted = _exempted(text, name)
    out = [
        f"{rel}:{number}: {name}: {flagged[number]}"
        for number in sorted(flagged)
        if number not in exempted
    ]
    out += [
        f"{rel}:{exempted[number]}: {name}: the exemption excuses nothing, "
        f"because {name} does not flag the line below it; remove the comment"
        for number in sorted(set(exempted) - set(flagged))
    ]
    if rel.endswith(".py"):
        out += [
            f"{rel}:{number}: {name}: the exemption ends a line, where the "
            "formatter moves it; put it on its own line above the line it exempts"
            for number in _trailing(text, name)
        ]
    return out


def _trailing(text, name):
    """The line numbers where an exemption from NAME ends a line of code.
    Python text only; text tokenize cannot read yields none."""
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, SyntaxError):
        return []
    return [
        token.start[0]
        for token in tokens
        if token.type == tokenize.COMMENT
        and token.line[: token.start[1]].strip()
        and name in EXEMPTION.findall(token.string)
    ]


def _python(rel, root, under=None):
    """REL's text where REL is a `.py` file, under one of UNDER when UNDER
    is given; None otherwise."""
    if not rel.endswith(".py") or (under and not rel.startswith(under)):
        return None
    return _text(rel, root)


# --- encoding (#741, #762) ---------------------------------------------------
#
# A file opened, read or written without `encoding=` takes the locale's
# encoding: UTF-8 on macOS and on the ubuntu runner, cp1252 on
# `windows-latest`, so the class is invisible everywhere except the one leg
# nobody runs locally. #736 met it after review: a ledger row's middle dot
# went out as byte 0xB7 and came back as U+FFFD, and 26 cases failed on
# Windows alone.
#
# Why an AST walk and not ruff: `PLW1514` is a preview rule, and it does not
# see `read_text` / `write_text` called on a variable, which is most of this
# class (measured 2026-10-04 on ruff 0.16.10). A regex over source text
# misses an `encoding=` on a later line. What the walk sees is the tables
# below, so a call the walk does not know is a row to add to K1.
#
# K1, the calls that take the locale's encoding when none is named. The
# standard library's half was found by construction (round 1 of #741, on
# 3.14): every public callable whose signature carries `encoding=None`, each
# then read for whether `None` means the locale. It does not for
# `TextIOWrapper.reconfigure` (keep the current one), `tarfile` (file names),
# `urllib.parse`, the `xml` writers, `xml.etree.ElementInclude.default_loader`,
# `xmlrpc`, `calendar` (each a fixed default), or `asyncio`'s subprocesses
# (which refuse text). An opener with no `encoding` parameter at all, like
# `os.popen`, is not in that construction and is listed here by reading.
#
# - builtin `open`, `io.open`, `codecs.open`, `os.fdopen`, in a text mode;
# - `<expr>.open(...)` judged as `Path.open`, except where the receiver, or
#   the class a call in the receiver builds, resolves through the file's
#   imports to a module or class in NOT_A_FILE_OPENER, and `zipfile.Path`,
#   `importlib.resources`' readers and `pipes.Template` by OPEN_METHODS. A
#   receiver no import binds is excused under no spelling, so `os.open(p, 0)`
#   on a parameter named `os` is judged. Called on the class
#   (`Path.open(p)`), every position moves one to the right;
# - `<expr>.read_text(...)` and `<expr>.write_text(...)`, the same way;
# - `subprocess.run` / `Popen` / `call` / `check_call` / `check_output` with
#   `text=`, `universal_newlines=` or `errors=` and no `encoding`;
# - `subprocess.getoutput`, `subprocess.getstatusoutput`, `os.popen`;
# - `tempfile.NamedTemporaryFile` / `TemporaryFile` / `SpooledTemporaryFile`
#   in a literal text mode;
# - `gzip`, `bz2`, `lzma` and `compression.*`'s `open` in a mode carrying `t`;
# - `logging.FileHandler`, the file handlers of `logging.handlers`,
#   `logging.basicConfig(filename=...)`, `logging.config.fileConfig`;
# - `io.TextIOWrapper`, `fileinput.input` / `FileInput` / `hook_compressed`,
#   `argparse.FileType`, `doctest.testfile` / `DocFileTest` / `DocFileSuite`,
#   and the methods `.makefile()` and `.write_results_file()`.
#
# What no row can hold: a static walk follows names, not values, so a name
# rebound to an opener (`f = open; f(p)`), a star import,
# `functools.partial(open, ...)`, an opener passed by reference, `getattr`,
# `__import__`, a module loaded through `importlib`, `universal_newlines`
# given by position, `configparser`'s `.read`, a handler named in a string to
# `logging.config.dictConfig`, a handler subclass's `super().__init__(p)`, and
# a name an import binds that anything else in the file also binds all pass.
# Write the call plainly instead. The walk errs the other way too: a `ZipFile`
# bound to a name first (`with ZipFile(z) as zf: zf.open(n)`) is not traced,
# so its `.open` is reported though it reads bytes.
#
# K2, what the walk cannot prove counts as unnamed: a mode that is not a
# literal, `encoding=None` written out, and a `*` or `**` splat on a K1 call
# with no explicit `encoding`. Any `encoding` but `None` passes: the census
# holds that an encoding is chosen, not which one.

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
# `.open` receivers whose `open` takes no locale encoding, matched against
# what `owner` resolves them to through the file's imports. A module whose
# `open` opens no text file, or reads the encoding the file itself declares
# (`tokenize`); or a class whose `.open` reads bytes, called on the class or
# built in the receiver (`zipfile.ZipFile(z).open(name)`). The modules are
# every standard-library module with a module-level `open` that no other
# table holds (#762). Each module that
# imports on macOS was found by importing it on 3.12 to 3.14. Each one that
# does not was read in its documentation instead: `dbm.gnu`, `nt` and
# `ossaudiodev` carry an `open`, and `nis`, `spwd`, `msilib`, `msvcrt`,
# `winreg`, `winsound` and the Windows-only submodules
# `asyncio.windows_events`, `asyncio.windows_utils`, `encodings.mbcs`,
# `encodings.oem` and `multiprocessing.popen_spawn_win32` carry none.
NOT_A_FILE_OPENER = {
    "os",
    "webbrowser",
    "tarfile",
    "tarfile.TarFile",
    "zipfile.ZipFile",
    "shelve",
    "dbm",
    "dbm.dumb",
    "dbm.gnu",
    "dbm.ndbm",
    "dbm.sqlite3",
    "wave",
    "aifc",
    "sunau",
    "tokenize",
    "posix",
    "nt",
    # 3.12 on Linux and FreeBSD, removed in 3.13: an audio device.
    "ossaudiodev",
}
# Classes whose methods, called on the class, take the path first, so the
# encoding's position moves one to the right: `Path.read_text(p, "utf-8")`.
#
# How the list was settled (#762, review rounds 1 and 2). On 3.12, 3.13 and
# 3.14, every public class reachable from every importable public module and
# submodule was listed with each `open`, `read_text` or `write_text` it has,
# defined in its own body or inherited through its MRO. A class counts under
# its home module, an `__all__` re-export, or a module `__getattr__` alias;
# a name a module merely imported for itself (`json.tool.Path`,
# `compileall.Path`, `importlib.metadata.SimplePath`) is left out. These are
# the classes whose method, called on the class, reads text in the locale,
# itself or by handing `encoding=None` on to the receiver's `open`:
# `Traversable.read_text`, which `ResourceHandle` and `ResourceContainer`
# inherit, does that. Left out: methods that open no text file (`imaplib`,
# `telnetlib`, `tkinter.tix`, `urllib.request`, `webbrowser`, `ZipFile`,
# `TarFile`), that read a fixed encoding (`importlib.metadata`), that raise
# (`MultiplexedPath`), and protocol stubs. The modules that do not import on
# macOS were read in CPython's 3.12 source and hold no such class.
UNBOUND_RECEIVERS = {
    "pathlib.Path",
    "pathlib.PurePath",
    "pathlib.PosixPath",
    "pathlib.WindowsPath",
    "zipfile.Path",
    "importlib.resources.abc.Traversable",
    # The same class on 3.12 and 3.13, through `importlib.abc.__getattr__`.
    "importlib.abc.Traversable",
    "importlib.resources.simple.ResourceHandle",
    "importlib.resources.simple.ResourceContainer",
    # `importlib.simple` re-exports both in its `__all__`.
    "importlib.simple.ResourceHandle",
    "importlib.simple.ResourceContainer",
    # 3.12 only, removed in 3.13.
    "pipes.Template",
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
# signature. Functions only: `judge_call` matches this table by the call's
# dotted name before its `.open` branch, so a method's row here would be
# judged unshifted when the method is called on its class (#762).
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
# branch of `judge_call` alone, which moves them one to the right on the
# class.
OPEN_METHODS = {
    "<expr>": (0, 2),
    # `zipfile.Path.open(mode, *args)` hands `args[0]` to `TextIOWrapper` as
    # the encoding, one place earlier than `pathlib.Path.open`.
    "zipfile.Path": (0, 1),
    # `open(mode='r', *args)` the same way: `Traversable`'s is abstract,
    # `ResourceHandle`'s wraps the stream in `TextIOWrapper(stream, *args)`,
    # and `ResourceContainer`'s raises. Each is listed so that a class in
    # UNBOUND_RECEIVERS for its `read_text` keeps its encoding slot for `open`.
    "importlib.resources.abc.Traversable": (0, 1),
    "importlib.abc.Traversable": (0, 1),
    "importlib.resources.simple.ResourceHandle": (0, 1),
    "importlib.resources.simple.ResourceContainer": (0, 1),
    "importlib.simple.ResourceHandle": (0, 1),
    "importlib.simple.ResourceContainer": (0, 1),
    # `Template.open(file, rw)` takes no encoding: slot 2 lies past its last
    # parameter, so no position can name one, and a keyword is a TypeError.
    "pipes.Template": (1, 2),
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


def judge_call(call, bound):
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
    """What a `.open` is called on: the dotted name of a receiver, or of the
    class a receiver call constructs (`zipfile.ZipFile(z)`), resolved through
    the file's imports; None where no import binds the name. A name no import
    binds is None whatever it is spelled, because the walk cannot prove that
    a parameter named `os` is the module (K2). An instance bound to a name
    first (`with ZipFile(z) as zf`) is not traced."""
    if isinstance(receiver, ast.Call):
        return dotted(receiver.func, bound)
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
        kind = judge_call(node, self.bound)
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


def encoding(rel, root=None):
    """Every file the plugin reads or writes names its encoding: each K1 call
    in a tracked `.py` names one, the tests' fixtures included, since a
    fixture written in the locale's encoding is read back wrong on Windows.
    `CONTRIBUTING.md` *House rules* states the rule."""
    text = _python(rel, root)
    if text is None:
        return []
    flagged = {}
    for line, kind, qualname in unnamed_sites(text, rel):
        flagged.setdefault(
            line,
            f"{kind} in {qualname} reads or writes in the locale's encoding, "
            'which is cp1252 on the Windows leg; name `encoding="utf-8"`, or '
            "put `# exempt from encoding: <why>` on its own line above it",
        )
    return _held("encoding", rel, text, flagged)


# --- entry_point --------------------------------------------------------------


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


def entry_point(rel, root=None):
    """Every hook entry point opens its `__main__` block with
    `console.to_utf8()`, which `hooks/lib/console.py` says each one carries
    rather than relying on `dispatch.py` having made the call. The census
    reads the order: the call after `main()` is refused as its absence is.
    Whether the call works is `tests/hooks/test_console.py`'s and, for the
    dispatcher's own loop, `tests/hooks/test_dispatch.py`'s."""
    text = _python(rel, root, ("hooks/",))
    if text is None:
        return []
    flagged = {
        node.lineno: (
            "the `__main__` block does not open with `console.to_utf8()`, so "
            "a hook that raises while printing dies with stdout empty; make "
            "the call the block's first statement, or put "
            "`# exempt from entry_point: <why>` on its own line above it"
        )
        for node in ast.parse(text, rel).body
        if is_main_guard(node) and not opens_with_to_utf8(node)
    }
    return _held("entry_point", rel, text, flagged)


# --- splitlines (S19 of work item F, #667) ------------------------------------


def splitlines(rel, root=None):
    """No shipped reader splits a document's lines with `.splitlines(`,
    which also ends a line at the eight separators GFM does not. A reader
    of markdown or record text reads `hooks/lib/blocks.py#gfm_lines`, and a call
    over any other text, git's output or a tool's, carries its exemption
    above the line that names `splitlines`."""
    text = _python(rel, root, SHIPPED)
    if text is None:
        return []
    calls = [
        node.func.end_lineno
        for node in ast.walk(ast.parse(text, rel))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "splitlines"
    ]
    flagged = {
        line: (
            "`.splitlines(` ends a line where GFM does not; a reader of "
            "markdown or record text reads `hooks/lib/blocks.py#gfm_lines`, and a "
            "call over any other text puts "
            "`# exempt from splitlines: <what it splits>` on its own line above it"
        )
        for line in calls
    }
    # An exemption names one call, so a second call on its line would pass
    # under it; the old census counted calls per unit for the same reason.
    doubled = sorted({line for line in calls if calls.count(line) > 1})
    return _held("splitlines", rel, text, flagged) + [
        f"{rel}:{line}: splitlines: two calls on one line, and an exemption "
        "names one; put each call on a line of its own"
        for line in doubled
    ]


# --- heading_rule (#867) --------------------------------------------------------
#
# A format this repository owns is read by one reader. A markdown heading was
# read by four rules, and the copies answered one file differently. Each copy
# had been written beside a docstring pointing at the original, so what holds
# the one reader is a census over every shipped script.

# A code line that reads a markdown heading by a rule of its own: a counted
# `#` run in a pattern, `#{1,6}`, `#{2,3}` or any `#{<digit>`, or a
# `startswith` of `#` asked of a line.
HEADING_SPELLING = re.compile(r'#\{\d|startswith\(\(?"#')


def code_lines(text):
    """`(line number, line)` for every line of TEXT that is code: not inside
    a docstring, and not a whole-line comment."""
    prose = set()
    for node in ast.walk(ast.parse(text)):
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            prose.update(range(node.lineno, node.end_lineno + 1))
    for number, line in enumerate(text.split("\n"), 1):
        if number not in prose and not line.lstrip().startswith("#"):
            yield number, line


def heading_rule(rel, root=None):
    """No shipped script spells the markdown heading rule again: a reader of
    a document's sections asks
    `skills/verify/scripts/unverified_check.py#heading_level`. A docstring
    and a whole-line comment are prose about the rule and are not read."""
    text = _python(rel, root, SHIPPED)
    if text is None:
        return []
    flagged = {
        number: (
            "a second spelling of the heading rule; a reader of a document's "
            "sections asks `skills/verify/scripts/unverified_check.py"
            "#heading_level`"
        )
        for number, line in code_lines(text)
        if HEADING_SPELLING.search(line)
    }
    return _held("heading_rule", rel, text, flagged)


# --- floor_syntax ---------------------------------------------------------------
#
# What runs before any floor is checked (a hook, a git hook, the launcher,
# `bin/test`'s runner, and every module one of them loads) runs on whatever
# `python3` starts it, 3.9 on a stock macOS. `ruff.toml` lints that set at
# the version its `per-file-target-version` names, so B905 and UP017 do not
# ask it for `zip`'s `strict=` or `datetime.UTC`.
# `tests/hooks/test_launch.py` derives the set
# and holds the table to it; this census holds each file the table names to
# its version.

# The two constructs ruff pushes toward at the floor, and the version each
# needs: B905 asks every `zip` for `strict=`, and UP017 spells `timezone.utc`
# as `datetime.UTC`. A syntax newer than the version is `ast`'s to refuse.
NEWER = {"`zip(..., strict=...)`": (3, 10), "`datetime.UTC`": (3, 11)}


def newer_than(text, version):
    """`[(line, construct)]` in a module's text that a `python3` at
    `version` cannot run: a syntax `ast` refuses at that version, or one of
    `NEWER`'s constructs where it needs a later one."""
    try:
        tree = ast.parse(text, feature_version=version)
    except SyntaxError as error:
        return [(error.lineno, f"syntax: {error.msg}")]
    found = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "zip"
            and any(k.arg == "strict" for k in node.keywords)
        ):
            found.append((node.lineno, "`zip(..., strict=...)`"))
        elif (
            isinstance(node, ast.Attribute)
            and node.attr == "UTC"
            and isinstance(node.value, ast.Name)
            and node.value.id == "datetime"
        ) or (
            isinstance(node, ast.ImportFrom)
            and node.module == "datetime"
            and any(a.name == "UTC" for a in node.names)
        ):
            found.append((node.lineno, "`datetime.UTC`"))
    return [(line, what) for line, what in found if NEWER[what] > tuple(version)]


def ruff_targets(path):
    """`{pattern: (major, minor)}`, the `per-file-target-version` of the
    `ruff.toml` at `path`, or `{}` where there is no such file."""
    import tomllib

    if not os.path.isfile(path):
        return {}
    with open(path, "rb") as handle:
        table = tomllib.load(handle).get("per-file-target-version", {})
    return {p: (int(v[2]), int(v[3:])) for p, v in table.items()}


def matches(pattern, rel):
    """Whether ruff's glob `pattern` names `rel`. Its `*` crosses a `/`, as
    ruff's does: `"hooks/*.py"` lints `hooks/git/pre-commit.py` too. Ruff
    also matches the pattern against the file's name, so one with no `/`,
    `"seal_stamp.py"`, names that file in any directory; a name holds no `/`
    for a pattern's `/` to match."""
    return any(fnmatch.fnmatchcase(p, pattern) for p in (rel, posixpath.basename(rel)))


def floor_syntax(rel, root=None):
    """A file `ruff.toml`'s `per-file-target-version` names holds nothing a
    `python3` at that version cannot run."""
    text = _python(rel, root)
    if text is None:
        return []
    targets = ruff_targets(os.path.join(_root(root), "ruff.toml"))
    versions = [v for pattern, v in targets.items() if matches(pattern, rel)]
    if not versions:
        return []
    floor = min(versions)
    flagged = {}
    for line, what in newer_than(text, floor):
        flagged.setdefault(
            line,
            f"{what} needs a python3 newer than {floor[0]}.{floor[1]}, the "
            "version ruff.toml lints this file at, and it runs before any "
            "floor is checked",
        )
    return _held("floor_syntax", rel, text, flagged)


# --- section_sign (#1005) -------------------------------------------------------

SIGN = "\N{SECTION SIGN}"
# The records of a moment keep what they said when they were written, and
# `evals/behaviour/`'s cases are generated from records.
RECORDS = ("seal/threads/", "evals/behaviour/")


def section_sign(rel, root=None):
    """No living file writes the section sign: a reader can take it for
    syntax, so a living file cites in words, in the shape
    `skills/writing-style/SKILL.md` states. A fixture that needs the sign
    builds it from its name, `\\N{SECTION SIGN}`. A file that is not UTF-8
    text is not read."""
    if rel.startswith(RECORDS):
        return []
    text = _text(rel, root)
    if text is None:
        return []
    flagged = {
        number: (
            "a living file writes the section sign. Cite a contract rule as "
            "`contract rule <N>`, and another file's section by its path and "
            "its heading text in italics"
        )
        for number, line in enumerate(text.split("\n"), 1)
        if SIGN in line
    }
    return _held("section_sign", rel, text, flagged)


# --- real_identifiers -------------------------------------------------------------
#
# Both incidents that required a history rewrite entered through the same two
# doors: a real domain used as a test fixture, and real machine paths carried
# along inside copied config. The census is class-based (domains, user
# paths), not a blocklist of names: a blocklist of sensitive words cannot
# itself live in a public repository, and its completeness is what fails.

FIXTURE_DOMAIN = "example.com"  # the designated fixture domain
ALLOWED_DOMAINS = (
    FIXTURE_DOMAIN,
    "github.com",
    "arxiv.org",
    "claude.com",  # official docs this plugin is built against
    "w3.org",  # the SVG namespace, which every SVG file must declare to open
)
# A host allowed bare, or under the paths named for it, and nowhere else. The
# developer portal sits under /directory on the product's own address, and it
# is the one page where the directory's state is readable, to a person (#858).
# The rest of that host carries people's own conversations, shares and
# artifacts, and an address at it is somebody's mail, so neither is allowed.
ALLOWED_UNDER_PATHS = {"claude" + ".ai": ("/directory",)}
ALLOWED_USER_PATH = "/Users/x/"  # the designated fixture user

DOMAIN_RE = re.compile(r"\b[a-z0-9][a-z0-9.-]*\.(?:com|io|net|org|ai|dev)\b")
# Built from two halves, so the pattern does not hold a user path itself.
USER_PATH_RE = re.compile("/" + r"Users/[^\s\"'`)/]+/?")
# A projects directory spells the path its session started in with dashes:
# `-Users-<name>-<repo>`, or `-Users-<name>` alone for a session started in
# the home directory. So a user path reaches a record that way too. Built
# from two halves, like USER_PATH_RE. The name is read as word characters
# and dots up to the first character that is neither. A name holding a dash,
# or a dot the slug spells as one, is read by its first part, and refused
# unless that part is the fixture user's. A placeholder such as `<name>` or
# a pattern such as `[A-Za-z]` is no name.
SLUG_USER_RE = re.compile("-" + r"Users-([\w.]+)")
NOT_TEXT = (".gif", ".png", ".jpg")


def refused_domains(line):
    """The match of every domain in `line` outside the allowlist, in order.

    `evals/scripts/noninferiority.py#masked` reads a kept round record by
    this function, so the record a committed side holds is masked by the
    census that reads it."""
    refused = []
    for m in DOMAIN_RE.finditer(line):
        d = m.group(0)
        if d in ALLOWED_UNDER_PATHS:
            rest = line[m.end() :]
            mail = m.start() > 0 and line[m.start() - 1] == "@"
            if not mail and (
                not rest.startswith("/") or rest.startswith(ALLOWED_UNDER_PATHS[d])
            ):
                continue
        elif any(d == a or d.endswith("." + a) for a in ALLOWED_DOMAINS):
            continue
        refused.append(m)
    return refused


def refused_user_paths(line):
    """The match of every user path in `line` outside the fixture one, in
    order, written with slashes or as a projects directory's dashed slug;
    `refused_domains` says who else reads it."""
    return [
        m
        for m in USER_PATH_RE.finditer(line)
        if not m.group(0).startswith(ALLOWED_USER_PATH)
    ] + [m for m in SLUG_USER_RE.finditer(line) if m.group(1) != "x"]


def real_identifiers(rel, root=None):
    """No tracked text names a real domain or a real user path: fixtures and
    examples use `example.com` and `/Users/x/`, and a domain joins
    `ALLOWED_DOMAINS` by a deliberate edit, never to make a test pass."""
    if rel.endswith(NOT_TEXT):
        return []
    with open(
        os.path.join(_root(root), rel), encoding="utf-8", errors="replace"
    ) as handle:
        text = handle.read()
    flagged = {}
    for number, line in enumerate(text.split("\n"), 1):
        said = [
            f"{m.group(0)} is a real-looking domain, and fixtures and examples "
            "use example.com"
            for m in refused_domains(line)
        ] + [
            f"{m.group(0)} is a real user path, and fixtures use /Users/x/"
            for m in refused_user_paths(line)
        ]
        if said:
            flagged[number] = "; ".join(said)
    return _held("real_identifiers", rel, text, flagged)


# --- old_names (#1051) ----------------------------------------------------------
#
# The plugin was renamed AgenticSeal in one release: its prefix, its agents,
# its record layout and its command line each have one spelling, #1051's
# mapping, and a living file that writes the old one names a thing that no
# longer exists. The census reads every tracked text file outside the records
# below, so a name the sweep missed, or one a later edit brings back, is a
# line with its coordinate.
#
# Each alternative is one old name, or one family of them. The pattern is
# built from halves, so this file does not write the names it refuses.
_OLD = "spec" + "seal"
OLD_NAME = re.compile(
    "|".join(
        (
            # The brand, the plugin's old `name` and prefix, every identifier
            # and variable spelt after it, and the old trailer key.
            _OLD,
            # The tagline the one sentence replaced.
            "specs, " + "sealed",
            # The agents now named crafter, proofer and tracer.
            r"\b(?:" + "smi" + "th|war" + "den|scr" + r"ibe)\b",
            # A work item's directory, now `seal/threads/<id>/`.
            "seal/" + r"specs\b",
            # The frame's design and the closing memo, now `frame/design.md`
            # and `gaps.md`; a file named for its subject, such as
            # `graders/shape-writes-spec.md`, is not the record.
            r"(?<![\w-])(?:" + "sp" + "ec|over" + r"view)\.md\b",
            # The broad run's record, now `trail/gate.md`, and the command
            # now `seal gate`; `docs/the-broad-gate.md` names the act.
            r"(?<!the-)broad" + "-gate",
            # The hand-offs, now under a thread's `trail/`.
            r"(?<!trail/)\b(?:pha" + "ses|rou" + "nds)/",
            # The commands `seal <subcommand>` replaced.
            r"\b(?:session-" + "cost|mutation-" + "check|unverified-" + "check"
            r"|arm-" + "check|deferral-" + "check|fold-" + "check|pact-" + "check"
            r"|payload-" + "meter|seal-" + "stamp|test-" + r"layout)\b",
        )
    ),
    re.IGNORECASE,
)
# The old spellings a living file keeps on purpose, each for a reader that
# still meets it, and each taken out of a line before OLD_NAME reads it.
KEPT_OLD_NAMES = (
    # The trailer key a commit made before the rename carries, which
    # `chain_check.py` no longer reads. It is still spelt by the case in
    # `tests/skills/test_chain_check.py#Test_routing_trailers` that pins the
    # key as unread.
    "Spec" + "Seal-Routing",
    # The `renames` entry of `.claude-plugin/marketplace.json`, which carries
    # the plugin's old name to its new one and is append-only.
    f'"{_OLD}": "agentic"',
    # The 0.3.x directory, which `docs/one-root-by-lifetime.md` names as one
    # no code of the plugin opens, and which the cases pinning it as unread
    # spell.
    f".{_OLD}",
)
# A released work item's record cited at the commit that holds it, as
# `<commit>:<path>`, the form `git show` opens as written: the settle removed
# the directory and nothing rewrites history, so the old path is the only one
# any commit holds. Taken out of a line before OLD_NAME
# reads it, whole, so the record names inside the path pass with it.
HISTORY_PATH = re.compile(
    r"(?<![\w/:])[0-9a-f]{7,40}:"
    + "seal/"
    + r"specs/[0-9]{10}-[a-z0-9-]+(?:/[\w.-]+)*/?"
)
# The records of a moment, which keep the names they were written under. A
# thread is read against the commits it names until the settle after its
# release removes it, and the thread that renames a name quotes the name it
# renames. The truths measured on recorded eval runs name the trees those
# runs read. `.test_durations` is the cache the test runner rewrites.
OLD_NAME_RECORDS = (
    "seal/threads/",
    "evals/scripts/recurred_truths.json",
    ".test_durations",
)
# A replayed or seeded eval case holds a run at a recorded commit, so its
# bytes are the record (`evals/README.md`).
RECORDED_CASE = re.compile(r"^evals/behaviour/[^/]+/(?:replay|seeded)-")
# The replay and seeded cases' generators read round records in both layouts
# a release has kept them in, the one before 0.23.0 that every committed case
# was cut from among them, spelt once and exempted at
# `evals/scripts/replay_targets.py#LAYOUTS`, and their cases build records in
# both.
KEPT_FILES = (
    "tests/evals/test_replay_targets.py",
    "tests/evals/test_seed_defects.py",
)


def old_names(rel, root=None):
    """No living file writes a name the rename to AgenticSeal replaced:
    the brand, the old prefix and identifiers, the old agents, the old
    record layout, the old commands and the tagline. A spelling kept on
    purpose is in KEPT_OLD_NAMES, a record or a file of KEPT_FILES is passed over
    whole, a released work item's record passes only cited at a commit
    (HISTORY_PATH), and any other line that keeps an old name carries its
    exemption. A file that is not UTF-8 text is not read."""
    if rel.startswith(OLD_NAME_RECORDS + KEPT_FILES) or RECORDED_CASE.match(rel):
        return []
    text = _text(rel, root)
    if text is None:
        return []
    flagged = {}
    for number, line in enumerate(text.split("\n"), 1):
        for kept in KEPT_OLD_NAMES:
            line = line.replace(kept, "")
        line = HISTORY_PATH.sub("", line)
        found = OLD_NAME.search(line)
        if found:
            flagged[number] = (
                f"`{found.group(0)}` is a name the rename to AgenticSeal "
                "replaced; write the new one from #1051's mapping, or put "
                "`# exempt from old_names: <why>` on its own line above a "
                "line that keeps it on purpose"
            )
    return _held("old_names", rel, text, flagged)


# --- vacated_paths (#1060) ------------------------------------------------------
#
# #1060 moves files one directory down: a module of `hooks/` into
# `hooks/lib/`, a template into `templates/records/` or `templates/setup/`, a
# test file into an area of `tests/`. The path the file stood at one level up
# is then a path no file holds, and a living line that spells it sends its
# reader to nothing. The census derives those spellings from the files that
# stand in each subdirectory on disk, so it keeps no list of old paths and
# refuses nothing until a file has moved.

# Each subdirectory a move fills, with the directory one level up whose
# spelling it vacates. `tests/e2e/` is not an area: its files never stood at
# the top of `tests/`.
TEST_AREAS = ("hooks", "skills", "github", "evals", "behaviour", "text")
VACATING = (
    ("hooks/lib/", "hooks/"),
    ("templates/records/", "templates/"),
    ("templates/setup/", "templates/"),
    *((f"tests/{area}/", "tests/") for area in TEST_AREAS),
)
# A path cited at a commit, `<commit>:<path>`, the form `git show` opens as
# written; the old path is the one that commit holds. Taken out of a line
# before the census reads it.
COMMIT_PATH = re.compile(r"(?<![\w/:])[0-9a-f]{7,40}:[\w./-]+")


def vacated(root=None):
    """`{old path: new path}` for every file standing directly in a
    subdirectory `VACATING` names whose path one level up no file holds."""
    found = {}
    for sub, up in VACATING:
        directory = os.path.join(_root(root), *sub.split("/"))
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if not os.path.isfile(os.path.join(directory, name)):
                continue
            if not os.path.exists(os.path.join(_root(root), *up.split("/"), name)):
                found.setdefault(up + name, sub + name)
    return found


def vacated_paths(rel, root=None):
    """No living file spells a path a move one directory down vacated:
    `hooks/<name>` once the file stands at `hooks/lib/<name>`, and the same
    for `templates/` and `tests/`. A spelling counts as a word, at the start
    of a path or after a shell variable such as `$CLAUDE_PLUGIN_ROOT/`, and
    not inside a longer path. The records and the recorded cases `old_names`
    passes are passed over whole, a path cited at a commit passes, and any
    other line that keeps an old path carries its exemption. A file that is
    not UTF-8 text is not read."""
    if rel.startswith(OLD_NAME_RECORDS) or RECORDED_CASE.match(rel):
        return []
    moved = vacated(root)
    if not moved:
        return []
    text = _text(rel, root)
    if text is None:
        return []
    spelling = re.compile(
        r"(?<![\w./}$-])(?:\$\{?\w+\}?/)?("
        + "|".join(re.escape(old) for old in sorted(moved, key=len, reverse=True))
        + r")(?![\w/-]|\.\w)"
    )
    flagged = {}
    for number, line in enumerate(text.split("\n"), 1):
        found = spelling.search(COMMIT_PATH.sub("", line))
        if found:
            old = found.group(1)
            flagged[number] = (
                f"`{old}` is a path no file holds since the file moved to "
                f"`{moved[old]}`; write the path the file stands at, or put "
                "`# exempt from vacated_paths: <why>` on its own line above a "
                "line that keeps it on purpose"
            )
    return _held("vacated_paths", rel, text, flagged)


CENSUSES = (
    encoding,
    entry_point,
    splitlines,
    heading_rule,
    floor_syntax,
    section_sign,
    real_identifiers,
    old_names,
    vacated_paths,
)


def judge(rel, root=None):
    """Every census's lines over the file at REL, census by census in the
    order `CENSUSES` holds them."""
    return [line for census in CENSUSES for line in census(rel, root)]
