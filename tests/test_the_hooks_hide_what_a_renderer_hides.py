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

# Spelled by its code point, so no line of this file carries the character
# itself for a reader to mistake for a space.
NBSP = chr(0xA0)


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


# --- the corpus: the frame's shapes, the old cases, and a generated set -----

# `tests/test_unverified_rows_close.py#FENCE_SHAPES`, the delimiter rule's own
# shapes, and 1790635413's `COMMENT_SHAPES` at `4edc5de6`: every line of each
# is a place a reading of fences or comments has had to be right.
COMMENT_SHAPES = [
    [OPEN, "| a | b |", CLOSE, "| c | d |"],
    [OPEN + " x", "| a | b |"],
    [OPEN + " one line " + CLOSE, "| a | b |"],
    ["| a |", OPEN, "| b |", CLOSE, OPEN, "| c |"],
    ["```", OPEN, "```", "| a |", CLOSE],
    [OPEN, "```", CLOSE, "```", "| a |"],
    [OPEN + "\r", "| a |\r", CLOSE + "\r", "| b |\r"],
    [f"text `{OPEN}` more", "| a |", f"`{CLOSE}`", "| b |"],
    [f"a note quoting `{OPEN}`", "```", "| a |", "```", "| b |"],
    [f"{OPEN} a note with `{CLOSE}` in it", "| a |", CLOSE, "| b |"],
    [f"a lone ` then {OPEN} x", "| a |", CLOSE, "| b |"],
    [f"{OPEN} a {CLOSE} {OPEN} b", "| x |", "c " + CLOSE, "| y |"],
    [OPEN, OPEN + " nested", CLOSE, "| a |", CLOSE],
    [OPEN, "| a |", f"{CLOSE} {OPEN}", "| b |"],
    ["<!-->", "| a |", CLOSE, "| b |"],
    ["a note " + OPEN + " never closed", "| a |", "```", "| b |", "```", "| c |"],
]

# Lines the generated documents are drawn from. Each is here because it is a
# delimiter, a container, or a context `hooks/blocks.py` calls uncertain, and
# a context the walk is ever made exact for has to be in this list first: the
# property is only as good as what the corpus can hold.
ALPHABET = [
    "",
    "text",
    "| a | b |",
    "|---|---|",
    "```",
    "````",
    "~~~",
    "```python",
    "``` `x`",
    "```\t",
    "   ```",
    "    ```",
    "\t```",
    OPEN,
    OPEN + " x",
    "x " + OPEN,
    "x " + OPEN + " y " + CLOSE,
    CLOSE,
    "x " + CLOSE,
    CLOSE + " x " + OPEN,
    OPEN + " a " + CLOSE,
    "<!-->",
    "<!---->",
    "   " + OPEN,
    "    " + OPEN,
    "`" + OPEN + "`",
    "`",
    "a lone ` then " + OPEN,
    "- item",
    "- ```",
    "- " + OPEN,
    "  ```",
    "  | a |",
    "1. ```",
    "> quote",
    "> ```",
    "> " + OPEN,
    "    code",
    # An indented code block inside a container, whose line starts with the
    # container's marker, and indentation counted with a tab in it.
    ">     code",
    "-     code",
    "1.     code",
    "  \tcode",
    "\tcode",
    "<div>",
    "</div>",
    "<br>",
    "<https://example.com>",
    "<pre>",
    "</pre>",
    "# heading",
    "---",
    "~~~~ x",
    # A no-break space: CommonMark counts neither it as a blank line nor it
    # after a closing run as a space, and Python's `str.strip` counts both.
    NBSP,
    "``` " + NBSP,
    "~~~" + NBSP,
    "text " + OPEN + " a " + CLOSE + " b " + OPEN,
    CLOSE + OPEN,
    OPEN + "--->",
    "`````",
    "```~",
    "~~~ ~",
    "<?php",
    "<!DOCTYPE html>",
    "<script>",
    "</script>",
    "* item",
    "10) ```",
    "> a " + OPEN,
    "| x " + OPEN + " |",
    "[ref]: <x>",
]

# The lines above that stand at the top level and start no block the walk
# does not follow. A document drawn from these alone is one the walk claims
# most of, which is where half 2 has something to check; a document drawn
# from the whole alphabet reaches the uncertain contexts too.
TOP_LEVEL = [
    line
    for line in ALPHABET
    if not line.startswith((" ", "\t", "-", "*", "1", ">"))
    and not (line.startswith("<") and not line.startswith(OPEN))
]

# The frame's Q7. Seeded, so a red is reproducible by its seed. Measured on
# 2026-09-29, one core, on the macOS machine phase 2 ran on: 20,000 documents
# of up to 24 lines took about 1.1 s for the oracle and the walk together,
# and 60 seeds of 20,000 found no disagreement (phase 2's record). 6,000 of up
# to 16 lines keeps each property case near a third of a second; raising
# CORPUS_SIZE is how a local run looks further.
SEED = 667
CORPUS_SIZE = 6000


def generated(size=CORPUS_SIZE, seed=SEED):
    """`size` documents of one to sixteen lines, the same ones on every run:
    half drawn from the top-level lines, half from the whole alphabet."""
    import random

    rng = random.Random(seed)
    docs = []
    for number in range(size):
        pool = TOP_LEVEL if number % 2 else ALPHABET
        lines = [rng.choice(pool) for _ in range(rng.randint(1, 16))]
        if rng.random() < 0.1:
            lines = [line + "\r" for line in lines]
        docs.append(lines)
    return docs


# Documents a wider generated run found the walk or the oracle wrong on while
# phase 2 was built, each reduced to the lines that matter, and kept so the
# next run meets them whatever the seed draws.
FOUND = [
    # a blank line between two indented lines is inside the code block
    ["    code", "", "    more"],
    # a list item whose content is an indented code block
    ["-     code"],
    # a line of only a no-break space is paragraph text, which the parser's
    # own `str.strip` drops from the top of the inline source
    [NBSP, "x " + OPEN, "x " + CLOSE],
    # a no-break space after a closing run: CommonMark does not close there
    ["```", "x", "``` " + NBSP, "y", "```", "z"],
]

CORPUS = (
    [SHAPES[name] for name in sorted(SHAPES)]
    + [list(lines) for lines in COMMENT_SHAPES]
    + FOUND
    + generated()
)


def load_hook(filename):
    from conftest import load_hook_module

    return load_hook_module(filename, "specseal_" + filename[:-3] + "_for_the_oracle")


blocks = load_hook("blocks.py")


def disagreements(lines):
    """Lines the walk calls exact and classes otherwise than the oracle."""
    found = blocks.walk(lines)
    renderer = oracle.hidden_lines(lines)
    return [
        (index, found.kinds[index], index in renderer)
        for index in range(len(lines))
        if not found.uncertain[index]
        and (found.kinds[index] != blocks.LIVE) != (index in renderer)
    ]


def test_where_the_walk_claims_to_be_exact_it_is():
    """Half 2, S2. On every line `hooks/blocks.py` does not call uncertain,
    over the shapes, the old cases and the generated corpus, the walk hides
    a line exactly where the oracle hides it. Without this half a reader that
    did nothing would pass half 1."""
    wrong = [(lines, bad) for lines in CORPUS if (bad := disagreements(lines))]
    assert not wrong, f"{len(wrong)} documents, the first: {wrong[0]}"


def test_the_walk_is_exact_somewhere():
    """The half above is empty if everything is uncertain. On the frame's
    shapes the walk claims every line but where a construct never closes or
    a mid-line opener leaves a paragraph open, and it hides the constructs the
    renderer hides."""
    for name in ("C2", "C5", "C6", "R1", "R2", "R4", "R5", "R9", "K1", "K5", "K7"):
        found = blocks.walk(SHAPES[name])
        assert not any(found.uncertain), name
        assert set(found.hidden()) == RENDERER[name], name
    claimed = sum(
        1 for lines in CORPUS for flag in blocks.walk(lines).uncertain if not flag
    )
    total = sum(len(lines) for lines in CORPUS)
    assert claimed > total // 3, (claimed, total)


# --- half 1: each reader never leaves both readings -------------------------


def shared_rule():
    """`skills/verify/scripts/unverified_check.py`, which states the fence
    delimiter rule the config reader's base reading was held to."""
    import importlib.util

    path = os.path.join(
        HERE, "..", "skills", "verify", "scripts", "unverified_check.py"
    )
    spec = importlib.util.spec_from_file_location("specseal_uc_for_the_oracle", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uc = shared_rule()


def config_base(lines):
    """What `hooks/config.py` hid at `release/v0.16.0`: every line inside a
    fenced block by the shared delimiter rule, a block nobody closed running
    to the end. `tests/test_unverified_rows_close.py#test_the_fence_rule_
    agrees_with_the_config_reader` held that reader to exactly this."""
    out = set()
    for first, last in uc.fence_spans(lines):
        out.update(range(first, len(lines) if last is None else last + 1))
    return out


def leaves_both(new, base, renderer, count):
    """The lines where a reader's answer is neither its base answer nor the
    renderer's: hidden where both show it, or shown where both hide it."""
    return [
        index
        for index in range(count)
        if (index in new) != (index in base) and (index in new) != (index in renderer)
    ]


config = load_hook("config.py")


def test_the_config_reader_never_leaves_both_readings():
    """Half 1, S4. On every line of every document, `hooks/config.py` hides
    the line where its base reading hid it or where a renderer hides it, and
    nowhere else: a line it newly hides was never a live row, and a line it
    newly shows was never fenced or commented out."""
    wrong = []
    for lines in CORPUS:
        new = {index for index in range(len(lines))} - {
            index for index, _line in config.unfenced(lines)
        }
        bad = leaves_both(
            new, config_base(lines), oracle.hidden_lines(lines), len(lines)
        )
        if bad:
            wrong.append((lines, bad))
    assert not wrong, f"{len(wrong)} documents, the first: {wrong[0]}"


routing = load_hook("routing.py")


def test_the_routing_reader_never_leaves_both_readings():
    """Half 1, S9. `hooks/routing.py#table_rows` read every line at
    `release/v0.16.0`, so its base hides nothing, and every line it skips now
    has to be one a renderer hides: a row it stops reading was never a live
    answer."""
    wrong = []
    for lines in CORPUS:
        new = set(range(len(lines))) - {index for index, _line in routing.shown(lines)}
        bad = leaves_both(new, set(), oracle.hidden_lines(lines), len(lines))
        if bad:
            wrong.append((lines, bad))
    assert not wrong, f"{len(wrong)} documents, the first: {wrong[0]}"


def test_the_routing_reader_hides_something():
    """The half above is empty for a reader that skips nothing, which is
    what it was. On the shapes that park or quote a table it skips the
    renderer's lines."""
    for name in ("R1", "R2", "R5", "R9"):
        lines = SHAPES[name]
        skipped = set(range(len(lines))) - {i for i, _ in routing.shown(lines)}
        assert skipped == RENDERER[name], name
