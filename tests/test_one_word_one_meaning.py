"""Five words read more than one way across these documents.

Each was found at a coordinate where the reader cannot tell which meaning is
intended, and a rewrite that leaves the ambiguity is not a fix. So each word
gets ONE meaning and every coordinate is brought to it — a case per word,
asserting the pinned phrasing AND the absence of the loose one.

The absence half is what makes these cases worth having. A document can gain
the corrected sentence and keep the old one two paragraphs down, which is how
two answers ship at once.

`skills/code-review/SKILL.md` holds the second half of "the start" and of
"the cycle". It belongs to another branch and is deferred rather than
half-edited; the rows naming it are in this work item's overview.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    return " ".join(read(*parts).split())


# --- "the start" — the moment before the first edit of a work item ----------


def test_the_start_is_the_moment_before_the_first_edit():
    """Not the start of a round, and not the start of a session. A round does
    not restart it and a resumed session does not restart it."""
    for parts in (
        ("skills", "implement", "SKILL.md"),
        ("CLAUDE.md",),
        ("agents", "smith.md"),
    ):
        assert "before the first edit" in flat(*parts), "/".join(parts)


# --- "once" — every one of them states its grain ----------------------------


GRAINS = {
    "commit-review-gate": "once per session per repo",
    "review-skill-gate": "once per session per working tree",
    "worktree-guard": "once per session per repository per direction",
}


def test_every_once_in_the_readme_states_its_grain():
    """Four different grains were all spelled `once`. One session legitimately
    meets the worktree question twice, and the README read as a bug report."""
    en = flat("README.md")
    for grain in GRAINS.values():
        assert grain.lower() in en.lower(), grain
    assert "Fires once per session," not in en, (
        "a bare `once per session` cannot say which of four grains it means"
    )


def test_the_korean_readme_states_the_same_grains():
    ko = flat("README.ko.md")
    for grain in (
        "세션·레포당 한 번",
        "세션·작업트리당 한 번",
        "세션·레포·방향당 한 번",
    ):
        assert grain in ko, grain


def test_the_per_command_marker_says_per_command_in_both_readmes():
    """`[no-review]` waives ONE command. Spelled `once`, it read as once per
    session, which is a waiver nobody built."""
    assert "for **that one command**" in read("README.md")
    assert "**그 명령 하나만**" in read("README.ko.md")
    assert "skips the review gate once" not in read("README.md")


def test_the_worktree_spec_is_still_the_model():
    """It already stated its grain correctly, and the others were brought to
    it rather than the other way round."""
    spec = flat("docs", "worktree-guard-spec.md").lower()
    assert "once per session per direction" in spec


# --- "asks" — the model is instructed, the user gets buttons ----------------


def test_the_two_prompts_are_named_by_who_they_address():
    spec = flat("docs", "review-chain-spec.md")
    assert "instructs the model to put the choice up" in spec
    assert "putting two buttons to the user" in spec
    assert "A `deny` addresses the **model**" in spec
    assert "An `ask` addresses the **user**" in spec


# --- "the cycle" — the mark's unit, never the whole run ---------------------


def test_the_spec_separates_the_cycle_from_the_review_run():
    spec = flat("docs", "review-chain-spec.md")
    assert "A **cycle** is the mark's own unit" in spec
    assert "A **review run** is" in spec
    assert "## The review run has a bound, and an end" in read(
        "docs", "review-chain-spec.md"
    )
    assert "## The cycle has a bound" not in read("docs", "review-chain-spec.md"), (
        "the bound is on the review run; stated on the cycle it reads as a "
        "bound on commits"
    )


def test_the_smith_calls_the_whole_thing_a_review_run():
    smith = flat("agents", "smith.md")
    assert "the review run is bounded" in smith
    assert "the cycle is bounded" not in smith


# --- "needs no marker at all" — the one the change resolves -----------------


def test_the_row_that_could_not_be_true_is_corrected_not_reworded():
    """It was true only after the first review mark landed, and false for
    every commit before it — the defect in #52 stated as a sentence."""
    skill = read("skills", "implement", "SKILL.md")
    assert "| Through the review chain | it needs no marker at all" not in skill
    assert 'used to carry "no marker at all"' in skill, (
        "dropping the row leaves the next reader unable to tell it was wrong"
    )
