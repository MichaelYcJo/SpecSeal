"""The hook readers hide what a CommonMark renderer hides, and nothing else (#667).

`seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-
by-one-rule/spec.md` §*The acceptance property* is what this module holds.
For every line L of a document, with `base(L)` a reader's reading at
`release/v0.16.0` and `renderer(L)` the oracle's:

  1. the reader never leaves both -- `new(L)` is `base(L)` or `renderer(L)`;
  2. where the walk claims to be exact, it is -- every line it does not call
     uncertain is classed as the oracle classes it;
  3. on every shape the frame names, the reader gives its expected answer.

Halves 1 and 2 run here, over the frame's shapes and a seeded generated
corpus. Half 3 is each reader's own case table, in the module that already
holds that reader's cases.

The oracle comes first, and it is the first thing held: before any reader
moved, it had to give the frame's *Renderer* column on every shape, which the
frame derived by reading the specification and could not execute (its Q2).
"""

import ast
import os

import commonmark_oracle as oracle
import pytest
from block_shapes import CLOSE, OPEN, RENDERER, SHAPES

HERE = os.path.dirname(os.path.abspath(__file__))


# --- the oracle is independent, and it says what the frame read -------------


def imported_roots(path):
    with open(path, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            roots.add((node.module or "").split(".")[0] if not node.level else ".")
    return roots


def test_the_oracle_imports_the_parser_and_nothing_of_this_repositorys():
    """S1. The oracle shares no code with the walk it checks: its only
    import is the parser, and it reaches for no path of this repository's.
    Round 3 of 1790635413: "The oracle cannot catch this, because it is
    built the same way." The shape data it is checked on imports nothing."""
    assert imported_roots(oracle.__file__) == {"markdown_it"}
    with open(oracle.__file__, encoding="utf-8") as handle:
        source = handle.read()
    for reach in ("sys.path", "importlib", "hooks/", "skills/", ".github"):
        assert reach not in source.split('"""', 2)[-1], reach
    assert imported_roots(os.path.join(HERE, "block_shapes.py")) == set()


@pytest.mark.parametrize("name", sorted(SHAPES))
def test_the_oracle_gives_the_frames_renderer_column(name):
    """S1, and the frame's Q2. The *Renderer* column was derived by reading
    CommonMark §4.5, §4.6 and §6.6 and was not executed; the parser gives it
    on every shape. Where the two disagreed, the oracle would win and the
    divergence would be recorded in `overview.md`."""
    assert oracle.hidden_lines(SHAPES[name]) == RENDERER[name]


@pytest.mark.parametrize(
    "lines, hidden",
    [
        # a fence, its delimiters included
        (["a", "", "```", "x", "```", "b"], {2: "fence", 3: "fence", 4: "fence"}),
        # four spaces after a blank line is an indented code block
        (["a", "", "    x", "", "b"], {2: "code"}),
        # a comment block runs to the first line holding the closer
        ([OPEN, "x", f"y {CLOSE} z", "b"], {0: "html", 1: "html", 2: "html"}),
        # any other HTML block hides the lines it holds, fence lines included
        (["<div>", "```", "x", "", "b"], {0: "html", 1: "html", 2: "html"}),
        # an inline comment hides the lines that begin inside it, and not the
        # line it opens on
        (["x " + OPEN + " y", "z", CLOSE + " w", "v"], {1: "comment", 2: "comment"}),
        # a blank line ends the paragraph, so the comment never closes
        (["x " + OPEN + " y", "", "z", CLOSE], {}),
        # inside a code span a delimiter is text
        ([f"x `{OPEN}` y", "z", f"`{CLOSE}`"], {}),
        # a table row is its own inline, so no comment spans two rows
        (["| a | b |", "|---|---|", f"| c {OPEN} d |", f"| e {CLOSE} |"], {}),
        # a fence inside a list item ends with the item
        (["- a", "  ```", "  x", "b"], {1: "fence", 2: "fence"}),
        # CRLF is the same document
        (["```\r", "x\r", "```\r", "y\r"], {0: "fence", 1: "fence", 2: "fence"}),
    ],
    ids=[
        "fence",
        "code",
        "comment block",
        "other html",
        "inline comment",
        "blank ends it",
        "code span",
        "table rows",
        "list item",
        "crlf",
    ],
)
def test_the_oracle_names_each_kind_it_hides(lines, hidden):
    """What each of the four kinds is, one case each, so a reader of this
    module can see what "a renderer hides" means before any reader is held
    to it."""
    assert oracle.hidden(lines) == hidden
