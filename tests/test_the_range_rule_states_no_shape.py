"""The sentences the review of #860 found false do not come back beside the
range rule.

`docs/the-record-layout.md` §*A range owns the commits that descend from its
start* owns one sentence: a range `a..b` owns exactly the commits `git log
--ancestry-path --no-merges a..b` lists. Three review rounds of #860 each
found a sentence beside it — an example phrased by merge shape or by time —
false in a shape its author had not built, and the run stopped at round 3 on
the second fix of a fix. The reframe moved every shape into
`tests/test_a_range_owns_what_git_lists_for_it.py` as a case, and this module
refuses, in the home's section and in every sentence that links the home,
the vocabulary those false examples used. Every carrier of the rule — the
docstrings of `own_commits`, `fragment_left_behind`, `fix_pass_units` and
`touched`, the orchestration and the round-record spec — reaches the list
through its linking sentence; the rest of a docstring is not read.

It is a word list and not a reader of meaning: a shape stated in other words
passes it, and a true sentence that needs a listed word is refused. What
keeps a shape out of the prose is the rule in the home and review; this
module keeps the sentences the rounds found from coming back.

`rule 17` of `tests/test_the_rules_have_one_owner.py` checks that each
carrier names the home; it held green through rounds 2 and 3 while four
carriers restated the rule by shape beside the link. Seen red with round 3's
🟡 2 sentence pasted back into the home.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOME = os.path.join(ROOT, "docs", "the-record-layout.md")
SECTION = "A range owns the commits that descend from its start"
LINK = f"§*{SECTION}*"
SCRIPTS = os.path.join(ROOT, "skills", "code-review", "scripts")

# The words rounds 1-3's false examples used (`questions.md` Q6 of work item
# 1791384160). The last alternative is round 1's sentence, which used none of
# the others: a guarantee that something descends from the start "never".
SHAPE_WORDS = re.compile(
    r"\b(?:sibling|topic|fork|back-merge|squash|made after|made before|"
    r"once the|and not before|descends? from \S+ never)",
    re.IGNORECASE,
)

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
        "the range rule's home uses a word the review's false examples used; "
        "a shape is a case of tests/test_a_range_owns_what_git_lists_for_it.py, "
        "never a sentence:\n" + "\n".join(found)
    )


def test_a_sentence_linking_the_home_uses_no_listed_word():
    found = [
        line
        for label, sentence in linking_sentences()
        for line in offenders(label, sentence)
    ]
    assert not found, (
        "a sentence linking the range rule's home uses a word the review's "
        "false examples used:\n" + "\n".join(found)
    )


def test_the_list_catches_the_sentences_the_rounds_found():
    """Each sentence a round found false, as it stood in the tree, trips the
    list."""
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
