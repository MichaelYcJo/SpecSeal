"""#361: a release's size is a criterion, the count is a ceiling, and one
document states it.

The rule used to read *a release is sized in work items rather than in ticket
numbers, and three or four is the size*, which reads as a target. On
2026-09-11 a session read it as one twice — eighteen issues proposed for a move
out of the release milestones to bring them "down to size", and a two-item
release read as under the rule with room for a third. So the presence half and
the absence half are both pinned: a document can gain the corrected sentence
and keep the old one two paragraphs down, which is how two answers ship at
once.

**Every assertion reads the file with its wraps collapsed** — the presence and
absence cases through `flat()`, which flattens the whole file, and the sweep
through `hits()`, which flattens each line against the one after it so it can
still name a line number. The sentences here are hand-wrapped at 88 columns
(`test_docs_line_wrap.py`), so a phrase pinned as written on one line breaks
the moment a word is added earlier in the paragraph — and a phrase SEARCHED
for on one line is missed the moment its wrap falls inside it. Phase 1 of this
work item found the same thing from the other side: `spec.md` proposed
`git grep -n "three or four is the size"` as the absence check, and that
command exits 1 against the UNEDITED document, because the line wrapped
between `three` and `or four`. A check that passes before the change is no
check.

Round 1 of this work item found the sweep doing exactly that: five assertions
flattened and the two sweep units scanned line by line, so a restatement whose
wrap fell inside the phrase answered *no offender* in the check written to
catch it.

The sweep scans `.md` and `.py` alike and excludes only this module, **by
basename rather than by path**, so a copy of it anywhere in the scanned set is
excluded with it. Scanning one suffix would have been the cheaper way past the
self-match, and it would have left a comment in any other test module free to
state a second answer.
"""

import os
import re
import subprocess

ROOT = os.path.join(os.path.dirname(__file__), "..")

OWNER = "docs/issues-and-milestones.md"

# The wording the rule was brought to. `docs/review-chain-spec.md` states the
# review cap's ceiling in the same words, and the second assertion below keeps
# the two from drifting into two phrasings for one idea.
CEILING_MODEL = "docs/review-chain-spec.md"
SHARED_CEILING = "ceiling, not a target"

# The sentence that was replaced. Lower-cased on both sides, because the
# replacement opens a sentence with `Three`.
REPLACED = "three or four is the size"

SCANNED = (
    "docs",
    "skills",
    "agents",
    "templates",
    "tests",
    # `tests/test_one_word_one_meaning.py`, the module this sweep is modelled
    # on, reads this file for the same kind of claim, and it is where a rule
    # gets restated for a session that never opens `docs/`.
    "CLAUDE.md",
    "README.md",
    "README.ko.md",
    "CONTRIBUTING.md",
)
SUFFIXES = (".md", ".py")

# Every shape a second statement of a release's size could take, and the old
# wording literally. `seal/specs/` is outside `SCANNED` on purpose: an earlier
# work item's records state what was true at their own SHA and are not
# rewritten.
#
# **The verb is not the only form, which round 1 measured.** The first three
# alternatives all require `sized` or the replaced sentence verbatim, and three
# one-line restatements were measured escaping them: *a release's size is three
# or four work items*, *three or four work items is the size of a release*, and
# *the size of a release is three work items*. The noun forms below are what
# `questions.md` Q6's wider recipe already had — `release's size` and `is the
# size` — and the planted pattern had dropped both.
#
# `\bis\s+the\s+size\b` is the widest of them and the one that can misfire, on
# a sentence about the size of anything at all. Measured over the scanned set
# at the time it was added: no line matches it outside this module and the
# owner, both of which the sweep excludes. A legitimate match elsewhere is one
# judgement at the line the failure names, which is the cheaper direction than
# a sweep that reports nothing.
STATES_A_SIZE = re.compile(
    r"(?i)\brelease(?:'s)?\s+(?:is\s+|was\s+)?sized\b"
    r"|\bsized\s+in\s+work\s+items\b"
    r"|\bthree\s+or\s+four\s+is\s+the\s+size\b"
    r"|\brelease(?:'s)?\s+size\b"
    r"|\bsize\s+of\s+a\s+release\b"
    r"|\bis\s+the\s+size\b"
)

SELF = os.path.basename(__file__)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def flat(rel):
    """The file with every run of whitespace collapsed to one space.

    A hand-wrapped paragraph is one sentence to a reader and several lines to
    `in`. This is the reader `tests/test_one_word_one_meaning.py` already uses
    for the same reason.
    """
    return " ".join(read(rel).split())


def hits(lines):
    """Line numbers where `STATES_A_SIZE` matches, wrapped sentences included.

    A hand-wrapped sentence is split across exactly one line boundary, so a
    scan of single lines answers *no offender* for a statement a reader sees
    whole. Each line is therefore also searched joined to the one after it with
    the wrap collapsed — and only where that next line does not match on its
    own, so a sentence lying wholly in it is reported once, at its own line.
    """
    found = []
    for index, line in enumerate(lines):
        after = lines[index + 1] if index + 1 < len(lines) else ""
        if STATES_A_SIZE.search(line):
            found.append(index + 1)
        elif after and not STATES_A_SIZE.search(after):
            if STATES_A_SIZE.search(" ".join(f"{line} {after}".split())):
                found.append(index + 1)
    return found


def tracked():
    out = subprocess.run(
        ["git", "ls-files", *SCANNED],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.split()
    return [
        rel for rel in out if rel.endswith(SUFFIXES) and os.path.basename(rel) != SELF
    ]


def test_the_rule_states_the_criterion_and_not_the_count():
    """The size is decided by what has to be in effect next, and a release of
    one work item is legitimate rather than under a target."""
    doc = flat(OWNER)
    assert (
        "A release is sized by what has to be in effect before the next work "
        "item starts, and not by a count." in doc
    ), f"{OWNER} no longer states the criterion"
    assert REPLACED not in doc.lower(), (
        f"{OWNER} still states the size as a count — the sentence that was "
        "read as a target twice on 2026-09-11"
    )


def test_the_count_survives_as_a_ceiling_in_the_wording_the_cap_already_uses():
    """Named as a ceiling, with what the ceiling is for, and in
    `docs/review-chain-spec.md`'s words rather than a second phrasing."""
    doc = flat(OWNER)
    assert f"Three or four is a {SHARED_CEILING}." in doc, (
        f"{OWNER} no longer names the count as a ceiling"
    )
    assert "it says nothing about when to stop under it" in doc, (
        "the ceiling is named without saying it is not a floor either"
    )
    assert SHARED_CEILING in flat(CEILING_MODEL), (
        f"{CEILING_MODEL} was the wording this rule was brought to, and it "
        "has moved — one idea is now spelled two ways"
    )


def test_the_two_releases_are_cited_without_a_version_number():
    """The evidence is what makes the rule a description rather than a
    proposal, and both releases are at or above the running version, so the
    citation is prose and the paragraph says why."""
    # Lower-cased on both sides: the first citation opens a sentence, so
    # pinning it as written would pin where the sentence break falls too.
    doc = flat(OWNER).lower()
    for citation in (
        "the release that shipped the framer",
        "the release that replaced the deleted checklist with a gate",
    ):
        assert citation in doc, f"{OWNER} no longer cites {citation!r}"
    assert "named rather than numbered on purpose" in doc, (
        "without this note a later author, for whom both numbers have become "
        "history, replaces the descriptions with numbers and is right to"
    )


def test_the_rule_says_what_it_does_not_change():
    """Three clauses in one place, so a reader does not have to assemble them
    from a milestone table and a label section."""
    doc = flat(OWNER)
    for clause in (
        "still the pool a release is cut from",
        "still the unscheduled pool",
        "nothing schedules from either",
    ):
        assert clause in doc, f"{OWNER} no longer says {clause!r}"


def test_the_label_is_two_states_and_nothing_reads_it():
    """`size: now` is where the sizing judgment stops being made again from
    scratch. A reader has to be able to apply it without asking, which takes
    the meaning, the absence, and the fact that no automation reads it."""
    doc = flat(OWNER)
    assert (
        "`size: now` says this ticket has to be in effect before the next "
        "work item starts." in doc
    ), f"{OWNER} no longer defines the label"
    assert "rides the next release that happens to carry it" in doc, (
        "the label's absence has no stated meaning, so a reader cannot apply "
        "it in two states"
    )
    assert "**Nothing reads this label**" in doc, (
        "a reader who thinks something schedules from the label reads a stale "
        "one as a blocked release"
    )


def test_one_document_states_a_releases_size():
    """The sweep, by construction rather than by reading. A second statement
    of a release's size is the failure #331 names: a judgement nobody records
    is made again from scratch by the next reader — and two recorded answers
    are worse than none."""
    offenders = []
    for rel in tracked():
        if rel == OWNER:
            continue
        lines = read(rel).splitlines()
        for number in hits(lines):
            offenders.append(f"{rel}:{number}: {lines[number - 1].strip()}")
    assert not offenders, (
        f"{OWNER} owns what a release's size is decided by. These state it "
        "too, so a reader can leave with either answer:\n  " + "\n  ".join(offenders)
    )


def test_the_sweep_can_fail():
    """The sweep's pattern is the whole of its value, and a pattern that
    matches nothing passes silently. So it is run against the owner as well:
    the owner MUST match, or the regex has stopped describing the sentence it
    is meant to find elsewhere. Through the same wrap-aware reader the sweep
    uses, so the control cannot pass on a reader the sweep does not have."""
    found = hits(read(OWNER).splitlines())
    assert found, (
        "the sweep's pattern no longer matches the document that states the "
        "rule, so it would answer 'no offender' for every file in the tree"
    )


# --- the sweep's reach, pinned rather than left to the green answer ----------

# **A sweep that answers *no offender* cannot pin its own reach.** No file in
# the tree carries any of the shapes below, so deleting the reach that finds
# them changes the sweep's answer not at all: round 2 measured each of round 1's
# three widenings reverting with this module still green. The two cases below
# are what stands between the reach and a later edit that trims it as unused.
#
# Kept as data rather than as prose, so the sentences round 1 measured escaping
# are the ones asserted.
