"""`/specseal:config` — the door to `seal/config.md`.

Issue #105. Three rows exist and the only way to see them was to open a file
nobody has a reason to open. The skill is instructions rather than a program,
so what can be pinned is that the instructions are there and say what they
should — which is how #82 pinned `commit-pr-convention` and why those pins
have held.

The one thing worth stating twice: **the skill routes rather than
reimplements.** A row that moves files is `seal mode`'s work, and a second
implementation inside a skill is one nothing can mutation-test.
"""

import os

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")
SKILL = ("skills", "config", "SKILL.md")
BOOTSTRAP = ("skills", "implement", "SKILL.md")
TEMPLATE = ("templates", "config.md")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    return " ".join(read(*parts).split())


ROWS = ("Commit and pull request language", "Record language", "Mode")


@pytest.mark.parametrize("row", ROWS)
def test_the_skill_names_every_row_the_template_ships(row):
    """S1. A door that shows two of three rows is a door somebody has to go
    round anyway."""
    assert row in flat(*SKILL), f"the skill does not name `{row}`"
    assert row in flat(*TEMPLATE), f"the template no longer ships `{row}`"


def test_the_skill_shows_rows_that_are_absent():
    """S1, the half that is easy to drop. A row a repository never set is the
    most likely one somebody wants to change, and a file that shows only what
    is present hides exactly those."""
    text = flat(*SKILL)
    assert "absent" in text or "not carry" in text
    assert "default" in text


def test_the_mode_row_is_routed_and_not_read():
    """S2 and S3. `seal mode` is what the pull-request checks run, and a
    second reader of that row is a second answer."""
    text = flat(*SKILL)
    assert "seal mode" in text, "the skill does not name the command that owns the row"
    assert "second reader is a second answer" in text, (
        "the skill does not say why it routes rather than reading the row"
    )
    assert "mv " not in text, "the skill spells a move of its own"


def test_the_one_way_door_is_named_before_it_is_walked_through():
    """S5. Local mode exists for the repository whose tree must not carry
    these files, and shared is the direction that cannot be walked back."""
    text = flat(*SKILL)
    assert "point of no return" in text
    assert "before running the command" in text, (
        "the skill does not say WHEN to say it, so it can be said afterwards"
    )
    assert "git reset -- :/seal" in text, "the way back is not spelled"


def test_a_repository_with_no_root_is_not_opted_in_by_looking():
    """S6. The root's presence at one of two places is the opt-in. Creating
    the file here would opt somebody in from a command they ran to look."""
    text = flat(*SKILL)
    assert "has not been set up" in text or "not been set up" in text
    assert "Do not create the file" in text


def test_the_root_is_resolved_rather_than_spelled():
    """The two places, in that order — the rule every other reader follows."""
    text = flat(*SKILL)
    assert "<repo>/seal/config.md" in text
    assert "git rev-parse --git-common-dir" in text


def test_the_bootstrap_names_the_way_back_to_its_own_questions():
    """S7. A person who answers a question in a batch has no reason to expect
    a way back to it, so the batch has to say there is one."""
    assert "/specseal:config" in flat(*BOOTSTRAP), (
        "first setup asks three questions and names nothing that changes the "
        "answers later"
    )


def test_the_skill_refuses_to_grow_a_schema():
    """What it does not build, stated in the file so the next person adding a
    row does not add a setter with it."""
    text = flat(*SKILL)
    assert "does not define a schema" in text


@pytest.mark.parametrize("parts", [("README.md",), ("README.ko.md",)])
def test_both_readmes_list_it(parts):
    """A door nobody is told about is the file all over again."""
    assert "/specseal:config" in read(*parts), f"{parts[0]} does not list it"
