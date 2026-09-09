#!/usr/bin/env python3
"""Enumerate a module's arms from its own syntax tree, and report the ones no
case kills.

#262. `hooks/review-history-guard.py` had its arms counted by hand — every
`ExceptHandler`, `If`, `While` and `IfExp`, each member of a boolean test and
of an except tuple separately — and then mutated one at a time to see which
ones any case would notice. Nine arms turned out to be watched by no case.

**Nine cases would close that list and not the class.** A written list of arms
rots the way #210's written list of reader passes rotted: the ticket's own
table says 33 arms where the module now has 31, because the file changed twice
after the count was taken. So the durable close is a checker that derives the
list, and `tests/test_chain_hooks.py`'s `reader_blanking_passes` is the same
idea in miniature — derive it instead of typing it.

WHAT AN ARM IS. #262's rule, extended by two shapes the rule predates:

  If / While / IfExp   each TOP-LEVEL member of the boolean test. `a and (b
                       or c)` is two arms, not four: the inner `BoolOp` is
                       one member of the outer one. Flattening recursively
                       gives `gh_segments` seven arms where the hand count
                       and this walk both give five
  ExceptHandler        each member of an except tuple separately; a bare
                       `except:` is one arm
  match_case           each alternative of the pattern (a `MatchOr`'s
                       patterns) plus each top-level member of the guard
  comprehension        each top-level member of each `if` guard

The last two are not in #262's rule, which was written before this module
needed them. They change no count here — `hooks/review-history-guard.py` has
neither shape — and they are the plan's named failure scenario answered in
advance: *a new arm shape the walk does not know, a `match` statement, a
comprehension guard.*

WHY AN UNKNOWN NODE TYPE IS A REFUSAL. A walk that skips a node type it does
not recognise is the failure of the thing it replaces, one level up: it
reports nine unwatched arms out of thirty-one while the module has
thirty-four, and the number it prints is as rotten as the number in the
ticket. So the classification below is **total over the grammar** — every AST
constructor is either an arm shape or a named non-arm with grounds — and a
node type in neither raises `UnknownNodeType`.

Totality is checked against `ast` itself rather than against this docstring:
`tests/test_arm_check.py` enumerates every constructor from the `ast` module's
own class tree and asserts this file covers all of them. A Python release that
adds a node type turns that case red instead of quietly narrowing the walk.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass

MODULE_SCOPE = "<module>"


class UnknownNodeType(Exception):
    """A node type that is neither an arm shape nor a named non-arm.

    Raised rather than skipped: see the module docstring. The message names
    the type and the line, because the repair is to classify it here.
    """


class NoMutationDefined(Exception):
    """An arm this walk enumerates and cannot mutate.

    Also a refusal rather than a skip. An arm silently left unmutated reports
    as unwatched forever, or as watched, depending on which way the silence
    falls — and either way nobody is told the checker did not try.
    """


# --------------------------------------------------------------------------
# The classification. Total over the grammar, by construction of the case
# that checks it.
# --------------------------------------------------------------------------

#: Node types that CARRY arms. The value is the reason, for the report.
ARM_SHAPES = {
    "If": "each top-level member of the boolean test",
    "While": "each top-level member of the boolean test",
    "IfExp": "each top-level member of the boolean test",
    "ExceptHandler": "each member of the except tuple; a bare except is one arm",
    "match_case": "each alternative of the pattern, plus the guard's members",
    "comprehension": "each top-level member of each `if` guard",
}

#: Node types that carry NO arm, grouped by the reason they carry none. The
#: groups exist so a reader can audit a hundred names without reading a
#: hundred lines — and so a new name lands in a group that already states
#: the grounds for excluding it.
NOT_ARMS = {
    "a boolean test is read THROUGH it, so counting it again double-counts": (
        # `cwd = payload.get("cwd", "") or "."` is a value, not a branch, and
        # counting BoolOp on its own is what would take `main` past 17.
        "BoolOp",
    ),
    "an operator, a comparison, or a load/store context — a leaf with no test": (
        "Add",
        "Sub",
        "Mult",
        "MatMult",
        "Div",
        "Mod",
        "Pow",
        "LShift",
        "RShift",
        "BitOr",
        "BitXor",
        "BitAnd",
        "FloorDiv",
        "Invert",
        "Not",
        "UAdd",
        "USub",
        "And",
        "Or",
        "Eq",
        "NotEq",
        "Lt",
        "LtE",
        "Gt",
        "GtE",
        "Is",
        "IsNot",
        "In",
        "NotIn",
        "Load",
        "Store",
        "Del",
    ),
    "an expression that computes a value and forks on nothing": (
        "Attribute",
        "Await",
        "BinOp",
        "Call",
        "Compare",
        "Constant",
        "Dict",
        "DictComp",
        "FormattedValue",
        "GeneratorExp",
        "JoinedStr",
        "Lambda",
        "List",
        "ListComp",
        "Name",
        "NamedExpr",
        "Set",
        "SetComp",
        "Slice",
        "Starred",
        "Subscript",
        "Tuple",
        "UnaryOp",
        "Yield",
        "YieldFrom",
        "arg",
        "arguments",
        "keyword",
    ),
    "a statement that runs unconditionally": (
        "AnnAssign",
        "Assign",
        "AugAssign",
        "Break",
        "Continue",
        "Delete",
        "Expr",
        "Global",
        "Import",
        "ImportFrom",
        "Nonlocal",
        "Pass",
        "Raise",
        "Return",
        "TypeAlias",
        "alias",
    ),
    "it forks on iteration or on entering a block, not on a boolean test": (
        # A `for`'s `orelse` runs unless something breaks, which is arguably
        # an arm. #262's rule does not count it and the 31 this walk is
        # checked against was measured without it: `is_closed`'s `for path in
        # records` is not among that function's four.
        "For",
        "AsyncFor",
        "With",
        "AsyncWith",
        "withitem",
    ),
    "a container whose arms are its children, counted there": (
        # `Try`/`TryStar` hold the handlers; `Match` holds the `match_case`s.
        # Counting the container too would double every one of them.
        "Try",
        "TryStar",
        "Match",
    ),
    "a match pattern read through its `match_case`": (
        # `MatchOr` is the alternation and IS read, by `match_case` above;
        # these are the shapes a single alternative can take.
        "MatchAs",
        "MatchClass",
        "MatchMapping",
        "MatchOr",
        "MatchSequence",
        "MatchSingleton",
        "MatchStar",
        "MatchValue",
    ),
    "a definition or a scope, not a branch": (
        "ClassDef",
        "FunctionDef",
        "AsyncFunctionDef",
        "ParamSpec",
        "TypeVar",
        "TypeVarTuple",
    ),
    "a parse root or a parser artefact, never a branch inside a module": (
        "Module",
        "Expression",
        "Interactive",
        "FunctionType",
        "TypeIgnore",
    ),
    "its test raises or continues rather than choosing a path, and #262's "
    "rule — which the measured 31 is counted under — does not count it": (
        # Stated rather than left implicit: an `assert` IS a test a mutation
        # could flip. Counting it would move every per-function number away
        # from the hand count this walk is checked against, so the exclusion
        # is declared here where it can be overturned, not omitted.
        "Assert",
    ),
    "a removed alias `ast.parse` never produces": (
        "AugLoad",
        "AugStore",
        "Bytes",
        "Ellipsis",
        "ExtSlice",
        "Index",
        "NameConstant",
        "Num",
        "Param",
        "Str",
        "Suite",
    ),
}

#: Flattened, for the walk.
NOT_ARM_NAMES = frozenset(n for names in NOT_ARMS.values() for n in names)

#: Every node type this file classifies. The case that checks totality
#: compares this against `ast`'s own class tree.
CLASSIFIED = frozenset(ARM_SHAPES) | NOT_ARM_NAMES


# --------------------------------------------------------------------------
# The enumeration
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Span:
    """Where a piece of source is, as `ast` gives it.

    `col_offset` is a UTF-8 BYTE offset, not a character index — see
    `_splice`, which is the only place that matters and the only place it is
    read.
    """

    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int


@dataclass(frozen=True)
class Arm:
    """One arm, with what it takes to find it again and to mutate it.

    Two spans, because the two mutation operators reach different amounts of
    text. `span` is the arm's own — enough to invert it in place. `group` is
    the whole decision it belongs to, the boolean test or the except tuple,
    and `group_without` is what that decision reads once this arm is taken
    out of it. Removing an arm cannot be done inside its own span: dropping a
    member of `a and b` has to rewrite `a and b`.
    """

    scope: str
    shape: str
    source: str
    note: str
    span: Span
    group: Span
    group_without: str

    @property
    def lineno(self) -> int:
        return self.span.lineno

    @property
    def where(self) -> str:
        return f"{self.scope}:{self.lineno}"

    def __str__(self) -> str:
        text = " ".join(self.source.split())
        if len(text) > 68:
            text = text[:65] + "..."
        return f"{self.where:28} {self.shape:14} {self.note:16} {text}"


def _refuse_unknown(tree: ast.AST, filename: str) -> None:
    """Every node type in the tree is classified, or this raises."""
    for node in ast.walk(tree):
        name = type(node).__name__
        if name not in CLASSIFIED:
            line = getattr(node, "lineno", "?")
            raise UnknownNodeType(
                f"{filename}:{line}: `{name}` is neither an arm shape nor a "
                f"named non-arm, so this walk cannot say whether it carries "
                f"an arm. Classify it in `ARM_SHAPES` or in `NOT_ARMS` — "
                f"skipping it is how the enumeration goes short while the "
                f"count it prints still looks right."
            )


def _members(test: ast.expr) -> list[ast.expr]:
    """The top-level members of a boolean test.

    Top-level, not flattened: `a and (b or c)` is two members. Flattening
    recursively gives `gh_segments` seven arms where the hand count gives
    five, so the rule and this walk would stop being comparable.
    """
    return list(test.values) if isinstance(test, ast.BoolOp) else [test]


def _span(node: ast.AST) -> Span:
    return Span(node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)


#: What a decision reads once its last remaining arm is taken out of it. An
#: `if` whose test is gone is a branch that never runs, which is what #262
#: means by *removing* an arm: "removing `not segs` makes the stray and
#: unreadable notices fire on every Bash call" — the guard's body stops
#: happening. The other reading, that the body always happens, is the same
#: edit seen from the other side; this one is the ticket's.
EMPTY_DECISION = "False"


def _group_of(
    members: list[ast.expr], joiner: str, node: ast.AST, source: str
) -> tuple[Span, list[str]]:
    """The whole decision's span, and what it reads without each member.

    Returned together because they are one fact: a member's removal is
    expressed as a rewrite of the group, never as an edit inside the member.
    """
    group = _span(node)
    texts = [ast.get_source_segment(source, m) or "" for m in members]
    withouts = []
    for index in range(len(members)):
        rest = [t for i, t in enumerate(texts) if i != index]
        withouts.append(joiner.join(rest) if rest else EMPTY_DECISION)
    return group, withouts


def _node_arms(node: ast.AST, scope: str, source: str) -> list[Arm]:
    """The arms one node carries, or [] when it carries none."""
    shape = type(node).__name__
    if shape not in ARM_SHAPES:
        return []

    # Each entry: the member node, its note, the group it is removed from,
    # and what that group reads without it.
    parts: list[tuple[ast.AST, str, Span, str]] = []

    def add_boolean(test: ast.expr, note: str) -> None:
        members = _members(test)
        joiner = (
            " and "
            if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.And)
            else " or "
        )
        group, withouts = _group_of(members, joiner, test, source)
        for member, without in zip(members, withouts):
            # **Parenthesised, and it is load-bearing for a wrapped test.**
            # The group's span covers the brackets the source used, so the
            # remainder replaces them too. `gh_segments`'s `while` test is
            # `i < len(toks) and (\n ... \n)`: dropping the index guard
            # leaves a two-line expression with nothing bracketing it, which
            # is a `SyntaxError`. Measured on the real module — that arm was
            # the one `remove` could not be asked of.
            parts.append((member, note, group, f"({without})"))

    if shape in ("If", "While", "IfExp"):
        add_boolean(node.test, "")
    elif shape == "ExceptHandler":
        if node.type is None:
            # No type to drop and none to aim elsewhere. Refused by `mutate`.
            parts.append((node, "bare except", _span(node), ""))
        elif isinstance(node.type, ast.Tuple):
            members = list(node.type.elts)
            group, withouts = _group_of(members, ", ", node.type, source)
            for member, without in zip(members, withouts):
                if without == EMPTY_DECISION:
                    # A tuple emptied of every type catches nothing that is
                    # raised, which is `NEVER_RAISED` spelled the long way.
                    without = NEVER_RAISED
                else:
                    # **Re-parenthesised, and it is not cosmetic.** An
                    # `ast.Tuple` in an except clause spans its own
                    # parentheses, so the remainder replaces them too --
                    # and `except OSError, ValueError:` has been a
                    # SyntaxError since Python 3. Unwrapped, every arm of a
                    # three-member handler would come back REFUSED rather
                    # than measured, and `reader` in
                    # `hooks/review-history-guard.py` is exactly that shape.
                    without = f"({without})"
                parts.append((member, "", group, without))
        else:
            parts.append((node.type, "", _span(node.type), NEVER_RAISED))
    elif shape == "match_case":
        pattern = node.pattern
        alts = pattern.patterns if isinstance(pattern, ast.MatchOr) else [pattern]
        for alt in alts:
            parts.append((alt, "pattern", _span(alt), ""))
        if node.guard is not None:
            add_boolean(node.guard, "guard")
    elif shape == "comprehension":
        for guard in node.ifs:
            add_boolean(guard, "guard")
    else:  # pragma: no cover - ARM_SHAPES and this dispatch are one unit
        raise UnknownNodeType(
            f"`{shape}` is listed in ARM_SHAPES and this dispatch does not "
            f"handle it, so its arms would be counted as zero"
        )

    total = len(parts)
    out = []
    for index, (member, note, group, without) in enumerate(parts, start=1):
        if total > 1:
            note = f"{note} {index}/{total}".strip()
        out.append(
            Arm(
                scope=scope,
                shape=shape,
                source=ast.get_source_segment(source, member) or "",
                note=note,
                span=_span(member),
                group=group,
                group_without=without,
            )
        )
    return out


def _scoped(node: ast.AST, scope: str):
    """Every node with the name of the function or class enclosing it."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            inner = child.name if scope == MODULE_SCOPE else f"{scope}.{child.name}"
            yield from _scoped(child, inner)
        else:
            yield scope, child
            yield from _scoped(child, scope)


def arms(source: str, filename: str = "<source>") -> list[Arm]:
    """Every arm in `source`, in source order.

    Raises `UnknownNodeType` when the tree holds a node type this file does
    not classify — the refusal the module docstring argues for.
    """
    tree = ast.parse(source)
    _refuse_unknown(tree, filename)
    found = []
    for scope, node in _scoped(tree, MODULE_SCOPE):
        found.extend(_node_arms(node, scope, source))
    return sorted(found, key=lambda a: (a.span.lineno, a.span.col_offset))


def arms_of_file(path: str) -> list[Arm]:
    with open(path, encoding="utf-8") as f:
        return arms(f.read(), filename=path)


def counts(found: list[Arm]) -> dict[str, int]:
    """Arms per enclosing scope, in first-appearance order."""
    out: dict[str, int] = {}
    for arm in found:
        out[arm.scope] = out.get(arm.scope, 0) + 1
    return out


# --------------------------------------------------------------------------
# The mutation
# --------------------------------------------------------------------------


#: An exception class nothing raises, spelled as an expression so it needs no
#: name in the module under test.
NEVER_RAISED = 'type("_specseal_never_raised", (BaseException,), {})'


def _splice(source: str, span: Span, replacement: str) -> str:
    """`source` with the text at `span` replaced.

    `col_offset` is a UTF-8 BYTE offset, not a character index, so the slice
    is taken on the encoded line. A module with a non-ASCII comment above an
    arm is enough to part the two, and this repository's modules are full of
    them.
    """
    lines = source.splitlines(keepends=True)
    first, last = span.lineno - 1, span.end_lineno - 1
    head = lines[first].encode("utf-8")[: span.col_offset].decode("utf-8")
    tail = lines[last].encode("utf-8")[span.end_col_offset :].decode("utf-8")
    return (
        "".join(lines[:first]) + head + replacement + tail + "".join(lines[last + 1 :])
    )


#: The two ways an arm can be wrong, and they are not interchangeable.
#:
#: `invert` asks *would a case notice if this test were backwards*, and
#: `remove` asks *would a case notice if this arm were not here at all*.
#: Measured on `hooks/review-history-guard.py`: inversion kills 31 of 32 arms
#: and removal kills far fewer. **#262's table of unwatched arms is a REMOVAL
#: count** — every sentence in it is about taking something out ("removing
#: either opt-in half makes a globally installed plugin nag unrelated
#: repositories", "removing `not segs` makes the stray and unreadable notices
#: fire on every Bash call") — so a survivor count taken by inversion alone is
#: not the ticket's number and must not be compared with it.
#:
#: An arm is watched when ANY operator's mutation is noticed: that is the
#: question *does any case depend on this arm*. The per-operator counts are
#: reported beside it, because they answer narrower questions and the ticket's
#: nine is one of those answers.
OPERATORS = ("invert", "remove")


def mutate(source: str, arm: Arm, operator: str = "invert") -> str:
    """`source` with this one arm made wrong, one way.

    An arm with no mutation defined for the operator raises rather than coming
    back unchanged. An unmutated arm reported as `survived` reads as *no case
    watches this* when the truth is *this was never tried*.
    """
    if operator not in OPERATORS:
        raise NoMutationDefined(
            f"{operator!r} is not one of {OPERATORS}. A silently ignored "
            f"operator would report every arm as watched by whatever ran."
        )

    boolean = arm.shape in ("If", "While", "IfExp") or arm.note.startswith("guard")
    handler = arm.shape == "ExceptHandler" and arm.note != "bare except"

    if arm.note == "bare except":
        raise NoMutationDefined(
            f"{arm.where}: a bare `except:` catches everything, so there is "
            f"neither a type to aim elsewhere nor one to drop. Give it a type "
            f"or exempt it."
        )
    if not (boolean or handler):
        raise NoMutationDefined(
            f"{arm.where}: no mutation is defined for a `{arm.shape}` arm "
            f"({arm.note or 'no note'}). A match PATTERN is not an "
            f"expression, so neither inverting nor dropping it is available — "
            f"the repair is a mutation for that shape, not a skip."
        )

    if operator == "remove":
        # Rewritten at the GROUP, never inside the arm: dropping a member of
        # `a and b` has to rewrite `a and b`.
        mutated = _splice(source, arm.group, arm.group_without)
    elif boolean:
        if not arm.source:
            raise NoMutationDefined(
                f"{arm.where}: the arm's source segment could not be read, "
                f"so `not (...)` has nothing to wrap"
            )
        mutated = _splice(source, arm.span, f"not ({arm.source})")
    else:
        mutated = _splice(source, arm.span, NEVER_RAISED)
    ast.parse(mutated)  # a mutation that does not parse kills every arm
    return mutated


@dataclass(frozen=True)
class Verdict:
    """One arm's result, across every operator that could be applied to it.

    `by_operator` maps an operator to `True` when its mutation was noticed.
    An operator with no mutation for this arm is absent from it rather than
    recorded as unnoticed — the distinction between *no case watches this*
    and *this was never tried* is the whole reason `refused` exists.

    `not_applicable` is where that operator goes instead, with the reason.
    It is a separate field rather than nothing, because an arm ANOTHER
    operator could be applied to is not refused as a whole, and its
    un-asked operator was invisible until this field existed: the real
    module reported `remove 31 asked` against 32 arms and never said which
    arm was missing or why.
    """

    arm: Arm
    by_operator: dict[str, bool]
    not_applicable: dict[str, str]

    @property
    def killed(self) -> bool:
        """Watched at all: some case noticed some way of being wrong."""
        return any(self.by_operator.values())

    @property
    def detail(self) -> str:
        return " · ".join(
            f"{name} {'killed' if hit else 'survived'}"
            for name, hit in self.by_operator.items()
        )


def clear_bytecode_cache(path: str) -> list[str]:
    """Remove any cached bytecode for `path`. Returns what it removed.

    **This is not housekeeping; without it the run reports verdicts for the
    wrong mutation.** CPython validates a `.pyc` against the source's mtime
    and SIZE, and two mutations of the same arm shape are routinely the same
    number of bytes — `not (host == "example.com")` and `not (flag)` both add
    six characters. Written inside the same mtime granularity, the second
    mutation loads the FIRST one's bytecode.

    Measured while building this: a fixture whose second arm no case reaches
    came back `killed`, with the traceback pointing at an assertion the
    unmutated module satisfies. It is the same family as the defect the hash
    compare in `restore` exists for — a verdict recorded against a module
    that was never the one on disk — and no hash catches it, because the file
    on disk was right and the interpreter did not read it.

    The subprocess also runs with `PYTHONDONTWRITEBYTECODE`, so the loop
    writes no new cache to poison the next arm. Both halves are needed: this
    one clears what was there before the run, that one stops the run creating
    more.
    """
    stem = os.path.splitext(os.path.basename(path))[0]
    absolute = os.path.abspath(path)
    roots = [os.path.join(os.path.dirname(absolute), "__pycache__")]
    prefix = getattr(sys, "pycache_prefix", None) or os.environ.get(
        "PYTHONPYCACHEPREFIX"
    )
    if prefix:
        # `sys.pycache_prefix` mirrors the absolute source tree under itself.
        drive, tail = os.path.splitdrive(os.path.dirname(absolute))
        roots.append(os.path.join(prefix, tail.lstrip(os.sep).lstrip("/")))
    removed = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in os.listdir(root):
            if name.startswith(stem + ".") and name.endswith(".pyc"):
                os.remove(os.path.join(root, name))
                removed.append(os.path.join(root, name))
    return removed


def restore(path: str, original: bytes, original_sha: str) -> None:
    """Put `original` back and prove it landed, or stop the run.

    A function of its own so the failure path is reachable by a case. The
    defect it exists for is the one four fix passes met by hand in a day: a
    mutation recorded as killed that had never been applied, because the
    pattern missed by two spaces of indentation and nothing compared the
    bytes afterwards. Every verdict taken after a failed restore is measured
    against a mutated module, so this raises rather than warning.
    """
    with open(path, "wb") as f:
        f.write(original)
    with open(path, "rb") as f:
        back = hashlib.sha256(f.read()).hexdigest()
    if back != original_sha:
        raise RuntimeError(
            f"{path} was not restored: {back} != {original_sha}. Every "
            f"verdict after this point would be measured against a mutated "
            f"module, so the run stops here."
        )


def run_arms(
    path: str,
    tests: list[str],
    *,
    only: str | None = None,
    cwd: str | None = None,
    operators: tuple[str, ...] = OPERATORS,
    echo=lambda _msg: None,
) -> tuple[list[Verdict], list[tuple[Arm, str]]]:
    """Mutate each arm of `path` in turn and ask whether `tests` notices.

    Every operator in `operators` is applied to every arm that has a mutation
    for it, because the two ask different questions and #262's own count is
    an answer to only one of them — `OPERATORS` holds the measurement.

    The module is restored from bytes held here and sha256-compared after
    every mutation, never with `git checkout`. Four fix passes ran this by
    hand on one day and the one that skipped the hash check recorded a
    mutation as killed while never having applied it — the pattern had missed
    by two spaces of indentation.
    """
    with open(path, "rb") as f:
        original = f.read()
    original_sha = hashlib.sha256(original).hexdigest()
    source = original.decode("utf-8")
    found = arms(source, filename=path)
    if only:
        found = [a for a in found if a.scope == only]

    # Nothing this loop runs may leave a `.pyc` behind for the next arm to
    # load instead of the mutation it was handed. `clear_bytecode_cache`
    # explains what that costs.
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    verdicts: list[Verdict] = []
    refused: list[tuple[Arm, str]] = []
    try:
        for arm in found:
            by_operator: dict[str, bool] = {}
            not_applicable: dict[str, str] = {}
            for operator in operators:
                try:
                    mutated = mutate(source, arm, operator)
                except (NoMutationDefined, SyntaxError) as exc:
                    not_applicable[operator] = f"{type(exc).__name__}: {exc}"
                    continue
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(mutated)
                clear_bytecode_cache(path)
                try:
                    run = subprocess.run(
                        tests, cwd=cwd, capture_output=True, text=True, env=env
                    )
                    by_operator[operator] = run.returncode != 0
                finally:
                    restore(path, original, original_sha)
                    clear_bytecode_cache(path)
            if not by_operator:
                # No operator had a mutation for this arm. Refused, never
                # reported as a survivor: `survived` would read as "no case
                # watches this" when the truth is "this was never tried".
                refused.append(
                    (arm, " | ".join(f"{k}: {v}" for k, v in not_applicable.items()))
                )
                echo(f"  refused  {arm}")
                continue
            verdict = Verdict(arm, by_operator, not_applicable)
            verdicts.append(verdict)
            echo(
                f"  {'killed ' if verdict.killed else 'SURVIVED'} {arm}"
                f"  ({verdict.detail})"
            )
    finally:
        # An arm no case kills, and reported rather than removed -- which is
        # the verdict this whole module exists to produce, applied to itself.
        # The per-arm restore above already leaves the module clean, so
        # `test_the_module_is_restored_byte_for_byte_after_the_run` goes red
        # only when BOTH are gone (measured). What only this one covers is an
        # exception escaping between the write and the inner `try` -- a
        # `clear_bytecode_cache` that raises on a permissions error, say --
        # where the module would otherwise be left mutated on disk.
        restore(path, original, original_sha)
    return verdicts, refused


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _report(path, verdicts, refused, counted, echo):
    echo("")
    echo(f"{path} — {sum(counted.values())} arms")
    for scope, n in counted.items():
        echo(f"  {scope:24} {n}")

    if not verdicts and not refused:
        return 0

    survivors = [v for v in verdicts if not v.killed]
    echo("")
    echo(
        f"{len(verdicts)} arms mutated · {len(verdicts) - len(survivors)} killed "
        f"· {len(survivors)} watched by no case"
    )

    # Per operator, beside the combined verdict and never instead of it. The
    # two answer different questions and #262's table of unwatched arms is an
    # answer to `remove` alone, so a reader comparing this run with the
    # ticket needs that row rather than the total.
    applied = [op for op in OPERATORS if any(op in v.by_operator for v in verdicts)]
    for operator in applied:
        asked = [v for v in verdicts if operator in v.by_operator]
        lived = [v for v in asked if not v.by_operator[operator]]
        echo(
            f"  {operator:8} {len(asked)} asked · {len(asked) - len(lived)} killed "
            f"· {len(lived)} survived"
        )
    if len(applied) > 1:
        echo(
            "  An arm counts watched when ANY operator's mutation is noticed. `invert`"
        )
        echo(
            "  asks whether a case would notice this test being backwards and `remove`"
        )
        echo(
            "  whether one would notice the arm being absent — #262's own unwatched-arm"
        )
        echo("  table is a `remove` count, so compare it with that row.")

    # An operator that could not be asked of an arm ANOTHER operator handled.
    # Named, because `remove 31 asked` against 32 arms said nothing about
    # which arm was missing, and a per-operator count read against #262's
    # table has to say what its own denominator was.
    skipped = [
        (v.arm, op, why) for v in verdicts for op, why in v.not_applicable.items()
    ]
    if skipped:
        echo("")
        echo(
            f"{len(skipped)} operator/arm pairs not asked — the arm was "
            f"measured by another operator, so it is not refused, but this "
            f"operator's count excludes it:"
        )
        for arm, operator, why in skipped:
            echo(f"  {operator:8} {arm}")
            echo(f"      {why}")

    if refused:
        echo("")
        echo(f"{len(refused)} arms refused — enumerated and not mutated:")
        for arm, why in refused:
            echo(f"  {arm}")
            echo(f"      {why}")
    if survivors:
        echo("")
        echo("Watched by no case — a report, not a list of defects. An arm")
        echo("that cannot be constructed, or whose removal preserves")
        echo("behaviour, belongs here and is not a gap:")
        for v in survivors:
            echo(f"  {v.arm}")
    return len(survivors)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="arm-check",
        description=(
            "Enumerate a module's arms from its own syntax tree and report "
            "the ones no case kills."
        ),
    )
    parser.add_argument("module", help="the module whose arms to enumerate")
    parser.add_argument(
        "--tests",
        help=(
            "the command that decides whether an arm is watched, e.g. "
            '--tests "bin/test tests/test_chain_hooks.py -q". Omitted, the '
            "arms are listed and nothing is mutated."
        ),
    )
    parser.add_argument("--only", help="restrict to one enclosing scope, by name")
    parser.add_argument("--cwd", default=None, help="working directory for --tests")
    args = parser.parse_args(argv)

    def echo(msg):
        print(msg, flush=True)

    if not args.tests:
        found = arms_of_file(args.module)
        if args.only:
            found = [a for a in found if a.scope == args.only]
        for arm in found:
            echo(f"  {arm}")
        _report(args.module, [], [], counts(found), echo)
        return 0

    verdicts, refused = run_arms(
        args.module,
        shlex.split(args.tests),
        only=args.only,
        cwd=args.cwd or os.getcwd(),
        echo=echo,
    )
    found = [v.arm for v in verdicts] + [a for a, _ in refused]
    _report(args.module, verdicts, refused, counts(found), echo)
    # Report-only: exit 0 whether or not an arm survived. `questions.md` Q1 is
    # the owner's, and the two other answers -- non-zero on any survivor, or
    # non-zero above a recorded baseline -- both need the first run's number
    # to exist before they can be set. This is that run.
    return 0


if __name__ == "__main__":
    sys.exit(main())
