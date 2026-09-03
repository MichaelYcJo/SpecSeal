"""Every agent definition opens by naming the contract that binds it.

Phase 2 of #107. `skills/agent-contract/SKILL.md` holds the rules every agent
is bound by, and a contract nothing delivers is a contract that arrives for
whoever remembers it. The delivery is two facts in one file: the opening
paragraph names the contract, and the `skills:` frontmatter list is what the
harness actually preloads. Either one alone is silent — a paragraph naming a
skill nobody lists reaches no agent, and a listed skill the definition never
mentions is a rule set the definition does not admit it is under.

#107's stated reason for landing this before the framer and the sealer is
that a fifth agent should inherit the contract without anyone deciding to
give it one. So the check globs `agents/*.md` rather than naming the three
that exist: a fourth definition arriving without the line is red on the day
it lands, and that is the miss with no other symptom.

The pins are BODY sentences of the opening paragraph, matched inside that
paragraph and nowhere else. Scoping is not tidiness here. A contract line
that drifts to the bottom of a definition still satisfies a whole-file
search, while the agent reads it after the rules it was meant to precede;
and phase 1's first draft pinned eight headings, where a heading outliving
its rule passed.
"""

import glob
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

AGENTS = sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))

# The sentence as `spec.md` decided it, split into the four claims it makes.
# Identical in every definition so that a fourth agent's author copies it
# without thinking, which is what the identity case below holds it to.
PINS = (
    "The agent contract binds you, and you already have it",
    "so it arrived at startup, before your first tool call",
    "how to read an exit code, what you must not run, what you must not "
    "write, and how a probe is written",
    "This file adds only what is yours",
)

# A backtick-quoted token that could be a contract: a skill name or a path.
# `skills:` is not one of them — the colon is outside the character class,
# which is what keeps the name of the MECHANISM out of the answer.
TOKEN = re.compile(r"`([A-Za-z0-9][A-Za-z0-9._/-]*)`")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def frontmatter(text):
    return text.split("\n---\n", 1)[0]


def listed_skills(text):
    """The `skills:` entries the harness preloads, in order."""
    return re.findall(r"^  - (\S+)", frontmatter(text), re.M)


def opening_block(text):
    """Everything between the `# <name>` heading and the first `## ` heading."""
    body = text.split("\n---\n", 1)[1] if text.startswith("---\n") else text
    heading = re.search(r"^# \S.*$", body, re.M)
    assert heading, "no `# <name>` heading"
    rest = body[heading.end() :]
    following = re.search(r"^## ", rest, re.M)
    return rest[: following.start()] if following else rest


def contract_paragraph(text):
    """The FIRST paragraph under the `# <name>` heading, and only that.

    `spec.md`: the line stands immediately under the heading and before
    anything else. A paragraph that is merely somewhere in the file is not
    the thing that was decided."""
    return opening_block(text).strip("\n").split("\n\n", 1)[0]


def flat(text):
    return " ".join(text.split())


def missing_pins(text):
    """Every pin that is not inside the definition's contract paragraph."""
    paragraph = flat(contract_paragraph(text))
    return [phrase for phrase in PINS if phrase not in paragraph]


def named_contracts(text):
    """What the contract paragraph points at — skill names or paths."""
    return TOKEN.findall(contract_paragraph(text))


def resolves(token):
    """Whether the named contract is a file in this tree.

    A bare name is a skill, reached through the frontmatter; a token with a
    separator or a suffix is a path from the repository root. Both forms are
    resolved, because Q1 weighed both and a later answer could move it."""
    if "/" in token or token.endswith(".md"):
        return os.path.exists(os.path.join(ROOT, token))
    return os.path.exists(os.path.join(ROOT, "skills", token, "SKILL.md"))


def contract_path(token):
    if "/" in token or token.endswith(".md"):
        return os.path.join(ROOT, token)
    return os.path.join(ROOT, "skills", token, "SKILL.md")


def name(path):
    return os.path.relpath(path, ROOT)


# --- there is something to check -------------------------------------------


def test_the_glob_finds_the_definitions():
    """A glob that matches nothing passes every case parametrised on it."""
    assert len(AGENTS) >= 3, f"agents/*.md matched {len(AGENTS)} files"


# --- the line --------------------------------------------------------------


@pytest.mark.parametrize("path", AGENTS, ids=name)
def test_every_definition_opens_with_the_contract_line(path):
    absent = missing_pins(read(path))
    assert not absent, f"{name(path)}'s opening paragraph no longer says: {absent}"


@pytest.mark.parametrize("path", AGENTS, ids=name)
def test_the_contract_it_names_resolves_to_a_file_in_the_tree(path):
    named = named_contracts(read(path))
    assert len(named) == 1, (
        f"{name(path)}'s contract line names {named}; it names exactly one"
    )
    assert resolves(named[0]), (
        f"{name(path)} points at `{named[0]}`, which is not in this tree"
    )


@pytest.mark.parametrize("path", AGENTS, ids=name)
def test_the_file_it_names_is_a_contract(path):
    """Pointing the line at some other skill that happens to exist is the
    quieter half of the same miss: it resolves and delivers nothing."""
    named = named_contracts(read(path))[0]
    assert "## §1 " in read(contract_path(named)), (
        f"{name(path)} points at `{named}`, which carries no numbered sections"
    )


@pytest.mark.parametrize("path", AGENTS, ids=name)
def test_a_bare_name_is_delivered_by_the_frontmatter(path):
    """Q1 answered B′: the harness preloads what the `skills:` list holds.

    A definition that names the contract in prose but does not list it has
    written down an intention, not a delivery."""
    text = read(path)
    named = named_contracts(text)[0]
    if "/" in named:
        pytest.skip("named as a path, which the frontmatter does not deliver")
    assert named in listed_skills(text), (
        f"{name(path)} names `{named}` but its `skills:` list holds "
        f"{listed_skills(text)}"
    )


def test_the_line_is_identical_in_every_definition():
    """So the author of a fourth agent copies it without thinking."""
    paragraphs = {name(p): flat(contract_paragraph(read(p))) for p in AGENTS}
    assert len(set(paragraphs.values())) == 1, paragraphs


# --- the check can fail ----------------------------------------------------


FOURTH = """---
name: fourth
description: |
  A fourth agent, arriving with no contract line.
skills:
  - writing-style
---

# fourth

You do a fourth thing. This file says what it is.

## Role

- Something.
"""


def test_a_definition_with_no_contract_line_is_caught():
    assert missing_pins(FOURTH) == list(PINS)


def test_a_line_pointing_at_a_path_that_does_not_exist_is_caught():
    text = read(AGENTS[0])
    named = named_contracts(text)[0]
    broken = text.replace(f"`{named}`", "`docs/agent-contract.md`", 1)
    assert named_contracts(broken) == ["docs/agent-contract.md"]
    assert not resolves("docs/agent-contract.md")


def test_a_line_that_drifts_out_of_the_opening_is_caught():
    """The pin is scoped to the first paragraph, so a line that survives in
    the file while the definition opens without it is red."""
    text = read(AGENTS[0])
    paragraph = contract_paragraph(text)
    moved = text.replace(paragraph + "\n\n", "", 1).rstrip("\n") + "\n\n" + paragraph
    assert paragraph in moved, "the mutation deleted the line instead of moving it"
    assert missing_pins(moved) == list(PINS)


def test_a_name_dropped_from_the_frontmatter_is_caught():
    text = read(AGENTS[0])
    named = named_contracts(text)[0]
    stripped = re.sub(rf"^  - {re.escape(named)}\n", "", text, count=1, flags=re.M)
    assert stripped != text, "the frontmatter never listed it"
    assert named not in listed_skills(stripped)
