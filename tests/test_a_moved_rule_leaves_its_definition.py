"""A rule moved into the contract does not stay behind in a definition too.

Q2 of #107 answered *full*: `skills/agent-contract/SKILL.md` is the single
home for every universal rule, and each `agents/*.md` keeps only its own
application. Phases 3 and 4 did the moving. Nothing checked that it was a
move.

Measured 2026-09-03 by the orchestrator, at `e51fd0b`: §9's body was pasted
back into `agents/warden.md` under a new heading, and `test_broad_gate_rule`,
`test_edits_go_through_the_edit_tool`, `test_every_agent_reads_the_contract`
and `test_the_agent_contract_holds_the_universal_rules` were all green -- 81
passed, exit 0. Every assertion in the two modules phases 1 and 2 wrote is a
presence check, and the only absence checks in the tree were about the
contract's own frontmatter. So the half of Q2 that says *the definition
keeps only its own application* had nothing behind it at all, and the tree
could drift straight back to the state #107 opens with, one paste at a time,
with a green suite the whole way.

## Where this draws the line

A definition MAY cite a section by its number and say what the rule means
for its own role, in its own words -- that is the application form, and
phases 3 and 4 kept several deliberately: the warden's audit of the
`unverified` label, its `❓ out of verified scope` field, the #36 cost of a
prompt landing during a round, its 1.89; the smith's 1.08-1.17, its
hand-back as the place both answers land, its own waiver example as the
patch §9's gate reads a commit out of. Every one of those is about one
agent, and none of them is the rule.

What a definition may NOT do is carry the contract's own sentences. So the
check is verbatim rather than semantic: a run of `WINDOW` consecutive words
from a section's body, whitespace-normalised, appearing inside an agent
definition.

Verbatim is the deliberate half. The failure that was measured is a paste,
and a check that tried to catch a paraphrase would have to decide when two
sentences say the same thing -- which no constant can hold, and which would
refuse the application prose this rule exists to permit. What it therefore
does not catch is a definition restating a universal rule in fresh words.
That is a reviewer's finding, and saying otherwise here would be the
counterfeit `CONTRIBUTING.md` refuses.

`WINDOW` comes from the tree rather than from taste. Measured across all
three definitions after phase 4, the longest run any KEPT application shares
with any section is 10 words (`agents/smith.md`'s `a bare word is a pathspec
and git rejects it`, which §8 and the design gate's waiver paragraph both
spell because both are about the same git fact; the warden's 9-word echo of
§6 is the next). The smallest run a REAL duplication produced, measured on
the same files before phase 4 removed them, is 25 words (§10), then 31 (§9),
37 (§16), 59 (§11) and 66 (§3). Fifteen sits between 10 and 25 with margin
on both sides, and both ends of that margin are printed by
`test_the_window_sits_between_what_was_measured`, so a later edit that
narrows the gap is red rather than silently mis-tuned.

The list of sections is derived from the contract, never typed here. A
hand-copied list is a second source that disagrees with the first, and this
repository has been bitten by exactly that -- `ROUND_RECORD_FIELDS` in
`tests/test_the_pull_request_language_is_the_repositorys.py` carries the
scar. A section added as §17 is checked on the day it lands, and so is a
fourth agent definition, because both come from a glob.
"""

import glob
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONTRACT = os.path.join(ROOT, "skills", "agent-contract", "SKILL.md")
AGENTS = sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))

HEADING = re.compile(r"^## §(\d+) (.+)$", re.M)

# A run of this many consecutive words is longer than any phrase two of these
# documents share by writing about the same mechanism, and shorter than the
# smallest copy phase 4 removed. Both bounds are measured; see the docstring
# and `test_the_window_sits_between_what_was_measured`.
WINDOW = 15

# What the two ends of that margin were, when the number was chosen. These are
# not the rule -- they are what makes the rule auditable, and the case below
# is what keeps them from becoming a story about a number nobody re-measured.
LONGEST_KEPT_APPLICATION = 10
SMALLEST_REAL_DUPLICATION = 25


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def flat(text):
    return " ".join(text.split())


def sections(text):
    """{number: body} for every `## §N` in the contract, heading excluded.

    The heading is left out on purpose: a heading is a label, and a
    definition that names the same subject in its own heading is doing the
    citing this file permits."""
    heads = list(HEADING.finditer(text))
    out = {}
    for index, match in enumerate(heads):
        end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
        out[int(match.group(1))] = text[match.end() : end]
    return out


SECTIONS = sections(read(CONTRACT))


def name(path):
    return os.path.relpath(path, ROOT)


def runs(body, window=WINDOW):
    """Every window of `window` consecutive words in a section body."""
    words = flat(body).split()
    return [" ".join(words[i : i + window]) for i in range(len(words) - window + 1)]


def copied(body, definition, window=WINDOW):
    """The runs of `body` that appear verbatim in `definition`."""
    haystack = flat(definition)
    return [run for run in runs(body, window) if run in haystack]


def longest_shared(body, definition):
    """The longest run of `body`'s words that appears in `definition`.

    Reported rather than asserted on, so a failure says how much was copied
    and a measurement case can print the margin."""
    haystack = flat(definition)
    words = flat(body).split()
    best = 0
    for start in range(len(words)):
        end = start
        while end < len(words) and " ".join(words[start : end + 1]) in haystack:
            end += 1
        best = max(best, end - start)
    return best


# --- there is something to check -------------------------------------------


def test_the_globs_find_the_definitions_and_the_sections():
    """A glob that matches nothing passes every case parametrised on it, and
    both of these are globs."""
    assert len(AGENTS) >= 3, f"agents/*.md matched {len(AGENTS)} files"
    assert len(SECTIONS) >= 16, f"the contract has {len(SECTIONS)} numbered sections"


# --- the move was a move ----------------------------------------------------


@pytest.mark.parametrize("number", sorted(SECTIONS))
@pytest.mark.parametrize("path", AGENTS, ids=name)
def test_no_definition_carries_a_sections_own_sentences(path, number):
    """One case per section per definition, so a failure names both.

    Both axes are derived: a §17 added tomorrow and a fourth agent added
    tomorrow are each checked on the day they land, which is the miss with no
    other symptom."""
    duplicated = copied(SECTIONS[number], read(path))
    assert not duplicated, (
        f"{name(path)} carries §{number}'s own words: {duplicated[0]!r}. "
        f"A definition may cite §{number} and say what it means for its role, "
        "in its own words; carrying the contract's sentences is the "
        "duplication the contract was written to end, and it is invisible in "
        "a diff that only adds"
    )


def test_the_window_sits_between_what_was_measured():
    """The number is a measurement, so it is checked against the tree.

    Two ways this goes wrong quietly. A kept application grows until it
    shares more than `WINDOW` words with a section, and the case above starts
    refusing the prose it exists to permit. Or `WINDOW` is raised past what a
    real copy produces, and the case passes on a paste. Both are edits
    somebody makes for a good local reason, and neither shows up anywhere
    else."""
    widest = max(
        (
            (longest_shared(body, read(path)), name(path), number)
            for number, body in SECTIONS.items()
            for path in AGENTS
        ),
    )
    assert widest[0] < WINDOW, (
        f"{widest[1]} now shares {widest[0]} words with §{widest[2]}, which "
        f"is at or over the {WINDOW}-word window. Either that application "
        "prose has drifted into a copy, or it needs rewording -- do not "
        "raise the window, which is what makes the copy invisible"
    )
    assert widest[0] <= LONGEST_KEPT_APPLICATION, (
        f"the longest kept application is now {widest[0]} words "
        f"({widest[1]}, §{widest[2]}), where {LONGEST_KEPT_APPLICATION} was "
        "measured at phase 4. The margin under the window is shrinking; "
        "re-measure both ends before this case is the one that fails"
    )
    assert WINDOW < SMALLEST_REAL_DUPLICATION, (
        "the window is at or over the smallest duplication ever measured, so "
        "a real copy can now pass"
    )


# --- the check can fail -----------------------------------------------------


def paste_back(definition, number):
    """A definition with §N's body pasted back in under a new heading.

    This is the orchestrator's mutation of 2026-09-03, in the module rather
    than in a transcript: it is the exact edit a session makes when it
    decides a definition ought to state the rule too."""
    return definition.rstrip("\n") + (
        f"\n\n## The rule §{number} states\n\n{SECTIONS[number].strip()}\n"
    )


@pytest.mark.parametrize("number", sorted(SECTIONS))
@pytest.mark.parametrize("path", AGENTS, ids=name)
def test_pasting_a_section_body_back_into_a_definition_is_caught(path, number):
    """Every section, in every definition -- the mutation was run against one
    pair, and a case that only held that pair would be pinning the
    experiment rather than the rule."""
    mutated = paste_back(read(path), number)
    assert copied(SECTIONS[number], mutated), (
        f"§{number} pasted whole into {name(path)} is not caught, so that "
        "section's body holds no run of "
        f"{WINDOW} words -- it is too short for this check to see"
    )


def test_a_citation_is_not_a_copy():
    """The other direction, which matters more than it looks.

    A check that flagged the application forms would be worse than no check:
    the definitions would be rewritten to satisfy it, and what they would
    lose is the half that is actually theirs. So the kept applications are
    named here and asserted clean."""
    kept = {
        ("agents", "warden.md"): (
            "§9 applies to you although you edit less than the smith does",
            "whether that label is honest",
            "out of verified scope",
            "1.89",
        ),
        ("agents", "smith.md"): (
            "1.08–1.17",
            "hand-back",
            "§10's number for you",
        ),
    }
    for parts, phrases in kept.items():
        definition = read(os.path.join(ROOT, *parts))
        haystack = flat(definition)
        for phrase in phrases:
            assert phrase in haystack, (
                f"{'/'.join(parts)} lost its own application: {phrase!r}"
            )
        for number, body in SECTIONS.items():
            assert not copied(body, definition), (
                f"{'/'.join(parts)}'s application prose reads as a copy of §{number}"
            )
