"""A markdown heading has one spelling, and a renderer holds it (#867).

`skills/verify/scripts/unverified_check.py#heading_level` is the one rule every
reader of a section asks: the checker's regions, the fold check's statements,
the chain check's `## Verdicts`, the survivor sweep's ledger headings, the
payload meter's sections and `unverified-check`'s `## Not verified`. Five of
them spelled it themselves until #867, two as `startswith("#")`, which read a
wrapped `#120)` line as a heading and ended a record's section above its rows.

What holds the rule here is `tests/commonmark_oracle.py`, which reads
markdown-it and nothing of this repository's: on every line a renderer shows,
`heading_level` answers what the parser's top-level ATX headings answer. Three
corpora, as `spec.md` S10 names them: the frame's shapes, a seeded generated
corpus, and every tracked `.md` file.

**One limit, stated rather than generated away.** A heading indented one to
three spaces under a list item is that item's content, and a rule that reads
one line cannot see the item above it. The generated corpus holds the shape;
the comparison skips such a line where a list item stands above it in the
document, counts how many it skipped, and the tracked-file case asserts the
tree holds none — the day one is written, it goes red here.

**Setext headings are not read**, and the last case says why: every setext
heading markdown-it finds in this repository is a front-matter line under its
`---` closer, which GitHub renders as a table and not as a heading.
"""

import importlib.util
import os
import random
import subprocess

import pytest
from commonmark_oracle import heading_lines, hidden_text, setext_lines

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _reader():
    path = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")
    spec = importlib.util.spec_from_file_location("uc_for_the_heading_rule", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uc = _reader()

LIST_ITEM = ("- ", "* ", "+ ", "1. ", "1) ")


def disagreements(lines):
    """`([(index, ours, theirs)], skipped)` over the lines of a document a
    renderer shows, skipping a line indented one to three spaces below a
    list item (the module's stated limit)."""
    text = "\n".join(lines)
    hidden = hidden_text(text)
    theirs = heading_lines(text)
    out, skipped, under_a_list = [], 0, False
    for index, line in enumerate(lines):
        if line.lstrip(" ").startswith(LIST_ITEM):
            under_a_list = True
        if index in hidden:
            continue
        ours = uc.heading_level(line)
        if ours != theirs.get(index):
            if (
                under_a_list
                and line[:1] == " "
                and len(line) - len(line.lstrip(" ")) <= 3
            ):
                skipped += 1
                continue
            out.append((index, ours, theirs.get(index)))
    return out, skipped


SHAPES = {
    "a heading": (["## B"], 2),
    "indented three spaces": (["   ## B"], 2),
    "indented four spaces": (["    ## B"], None),
    "a tab before the run": (["\t## B"], None),
    "an issue number at column 0": (["#84's line"], None),
    "a wrapped issue reference": (["text", "#120) was it"], None),
    "seven hashes": (["####### x"], None),
    "a run and a tab": (["#\tx"], 1),
    "a run alone": (["#"], 1),
    "a closing run": (["## B ##"], 2),
    "no space after the run": (["#hello"], None),
    "a heading in a block quote": (["> # q"], None),
    "a heading in a list item": (["- # item"], None),
    "a heading after a paragraph": (["text", "## B"], 2),
}


@pytest.mark.parametrize("name", sorted(SHAPES))
def test_the_frames_shapes(name):
    """S8's and S9's shapes: the rule's answer for the shape's last line, and
    markdown-it's, agree, and both are the level written beside it."""
    lines, level = SHAPES[name]
    assert uc.heading_level(lines[-1]) == level
    assert disagreements(lines) == ([], 0), name


SEED = 867
CORPUS_SIZE = 2000
ALPHABET = [
    "",
    "## B",
    "   ## B",
    "  ## B",
    " # x",
    "    ## B",
    "#120) x",
    "#84's",
    "####### x",
    "#",
    "#\tx",
    "\t# x",
    "## B ##",
    "x",
    "```",
    "~~~",
    "> # q",
    "- # item",
    "- item",
    "1. x",
    "<div>",
    "</div>",
    "---",
    "===",
    "* * *",
    "    code",
    "<!--",
    "-->",
    "| a | b |",
    "|---|---|",
]


def test_a_seeded_generated_corpus():
    """S10, the generated half: CORPUS_SIZE documents of one to twelve lines
    drawn from ALPHABET, the same ones on every run (SEED), so a red is
    reproducible. Measured while building it: 3,000 documents found
    disagreements only on the stated limit."""
    rng = random.Random(SEED)
    found, skipped = [], 0
    for _ in range(CORPUS_SIZE):
        lines = [rng.choice(ALPHABET) for _ in range(rng.randint(1, 12))]
        wrong, limit = disagreements(lines)
        skipped += limit
        found.extend((lines, w) for w in wrong)
    assert not found, found[:5]
    assert skipped, "the corpus no longer reaches the stated limit"


def tracked_markdown():
    listed = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "-z", "--", "*.md"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    return [path for path in listed.split("\0") if path]


def test_every_tracked_markdown_file():
    """S10, the tree's half: every line every tracked `.md` file shows is a
    heading by the rule exactly where markdown-it reads a top-level ATX
    heading, and no line reaches the stated limit."""
    wrong, skipped = [], 0
    for rel in tracked_markdown():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            text = f.read()
        found, limit = disagreements(text.replace("\r\n", "\n").split("\n"))
        skipped += limit
        wrong.extend((rel, index + 1, ours, theirs) for index, ours, theirs in found)
    assert not wrong, wrong[:10]
    assert skipped == 0, "a heading indented under a list item now stands in the tree"


def test_every_setext_heading_in_the_tree_is_a_front_matter_line():
    """S10's limit: a setext heading is not read by the rule, on the ground
    that the tree's every one is the last line of a front-matter block — the
    file opens with `---` and the heading's underline is the block's closer.
    The day one stands in a body, this goes red, and the rule is to gain
    setext with the oracle's answer as its ground."""
    seen = 0
    for rel in tracked_markdown():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            text = f.read()
        lines = text.replace("\r\n", "\n").split("\n")
        for index in setext_lines(text):
            seen += 1
            closer = next(
                (i for i in range(1, len(lines)) if lines[i].strip() == "---"), None
            )
            assert lines[0].strip() == "---" and closer is not None, (rel, index + 1)
            assert index < closer, (rel, index + 1)
    assert seen, "no setext heading is left to hold the limit to"
