"""The range rule's home and its carriers state no merge shape and no time.

`docs/the-record-layout.md` §*A range owns the commits that descend from its
start* owns one sentence: a range `a..b` owns exactly the commits `git log
--ancestry-path --no-merges a..b` lists. Three review rounds of #860 each
found a sentence beside it — an example phrased by merge shape or by time —
false in a shape its author had not built, and the run stopped at round 3 on
the second fix of a fix. The reframe moved every shape into
`tests/test_a_range_owns_what_git_lists_for_it.py` as a case, and this module
keeps the shapes out of the prose: the home's section, the docstrings of the
four units that read a range, and every sentence that links the home may not
use the vocabulary those false examples used.

`rule 17` of `tests/test_the_rules_have_one_owner.py` checks that each
carrier names the home; it held green through rounds 2 and 3 while four
carriers restated the rule by shape beside the link. This checks what it
does not. Seen red with round 3's 🟡 2 sentence pasted back into the home.
"""

import ast
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOME = os.path.join(ROOT, "docs", "the-record-layout.md")
SECTION = "A range owns the commits that descend from its start"
LINK = f"§*{SECTION}*"
SCRIPTS = os.path.join(ROOT, "skills", "code-review", "scripts")

# The words rounds 1-3's false examples used (`questions.md` Q6 of work item
# 1791384160). Each names a branch's shape or a commit's time, which the
# owner sentence does not read; a sentence needing one is stating a shape.
# The last alternative is round 1's sentence, which used none of the words:
# a guarantee that something descends from the start "never" is a claim
# derived from the owner sentence, true only of the shapes its author built.
SHAPE_WORDS = re.compile(
    r"\b(?:sibling|topic|fork|back-merge|squash|made after|made before|"
    r"once the|and not before|descends? from \S+ never)",
    re.IGNORECASE,
)

# The units whose docstrings read a range, by file.
DOCSTRINGS = {
    "chain_check.py": ("own_commits", "fragment_left_behind"),
    "round_record.py": ("fix_pass_units", "touched"),
}

# Files whose sentences link the home: each such sentence is held to the list.
LINKERS = (
    os.path.join(ROOT, "skills", "code-review", "orchestration.md"),
    os.path.join(ROOT, "docs", "round-record-spec.md"),
    os.path.join(SCRIPTS, "chain_check.py"),
    os.path.join(SCRIPTS, "round_record.py"),
)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def flat(text):
    return " ".join(text.split())


def home_section():
    text = read(HOME)
    start = text.index(f"\n## {SECTION}\n")
    end = text.find("\n## ", start + 1)
    return text[start : end if end != -1 else len(text)]


def docstrings():
    for name, units in DOCSTRINGS.items():
        module = ast.parse(read(os.path.join(SCRIPTS, name)))
        found = {
            node.name: ast.get_docstring(node) or ""
            for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name in units
        }
        assert set(found) == set(units), (name, sorted(found))
        for unit in units:
            yield f"{name}#{unit}", found[unit]


def linking_sentences():
    for path in LINKERS:
        text = flat(read(path))
        at = text.find(LINK)
        assert at != -1, f"{os.path.relpath(path, ROOT)} no longer links the home"
        while at != -1:
            start = text.rfind(". ", 0, at) + 1
            end = text.find(". ", at)
            yield (
                os.path.relpath(path, ROOT),
                text[start : end if end != -1 else len(text)],
            )
            at = text.find(LINK, at + 1)


def offenders(label, text):
    return [
        f"{label}: `{m.group(0)}` in {flat(text)[max(0, m.start() - 60) : m.end() + 60]!r}"
        for m in SHAPE_WORDS.finditer(flat(text))
    ]


def test_the_home_states_no_shape_and_no_time():
    found = offenders("docs/the-record-layout.md", home_section())
    assert not found, (
        "the range rule's home states a merge shape or a time; a shape is a "
        "case of tests/test_a_range_owns_what_git_lists_for_it.py, never a "
        "sentence:\n" + "\n".join(found)
    )


@pytest.mark.parametrize(
    "label, text", list(docstrings()), ids=[label for label, _ in docstrings()]
)
def test_a_reader_of_a_range_defines_no_shape(label, text):
    found = offenders(label, text)
    assert not found, (
        "a docstring of a unit that reads a range states a merge shape or a "
        f"time; it names the home instead ({LINK}):\n" + "\n".join(found)
    )


def test_a_sentence_linking_the_home_states_no_shape():
    found = [
        line
        for label, sentence in linking_sentences()
        for line in offenders(label, sentence)
    ]
    assert not found, (
        "a sentence linking the range rule's home restates it by shape:\n"
        + "\n".join(found)
    )


def test_the_list_catches_the_sentences_the_rounds_found():
    """The list is not a guess: each sentence a round found false, as it
    stood in the tree, trips it."""
    found_false = (
        # round 1's 🟡 2
        "A commit that a merge brought in reaches `b` only through the merge "
        "and descends from `a` never",
        # round 2's 🟡 1
        "an own commit on a topic forked before `a` descends from it never",
        # round 3's 🟡 2
        "a sibling's commit made after the base merged `a` is; and an own fix "
        "on a topic forked before `a` is owned once that topic has merged "
        "`a`, and not before",
    )
    missed = [s for s in found_false if not SHAPE_WORDS.search(s)]
    assert not missed, missed
