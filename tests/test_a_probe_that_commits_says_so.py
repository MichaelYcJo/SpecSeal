"""Neither agent file said how to write a scratch-repo probe that commits.

Issue #82. A review agent spawned to run round 1 wrote its probes with shell
variables, two of them reached a user who was not driving the session as
permission prompts inside five minutes, and the agent was stopped to end them
— which cost the review round. The agent had been told to use literal paths in
its own prompt, and that prompt is written by a different session every time.

So the instruction lives where every future spawn reads it. Until phase 3 of
#107 that meant both agent files, because one agent knowing it is how this
reached a user in the first place — and two files carrying it in near-identical
words is how a third agent inherited neither. It is now §8 of the agent
contract, which every agent receives at startup, so the cases below are
re-pointed there rather than deleted: a rule that moves with no case behind it
is a rule that can move again into nothing.

The smith is why this is worth a section rather than a third copy. It writes
probes too, and no file ever told it any of this.
"""

import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
CONTRACT = os.path.join("skills", "agent-contract", "SKILL.md")
HEADING = re.compile(r"^## §(\d+) ", re.M)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def section(number):
    """§N's body, so a shape that drifts into another section is not a pass.

    The whole file would let §8 be emptied while the words survive under §9,
    which breaks the number a spawn prompt cites and nothing would say so."""
    text = read(CONTRACT)
    heads = list(HEADING.finditer(text))
    for i, m in enumerate(heads):
        if int(m.group(1)) != number:
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        return " ".join(text[m.end() : end].split())
    raise AssertionError(f"the contract has no §{number}")


def test_the_contract_carries_all_three_shapes():
    """S9. Three shapes avoid the prompt and a session needs all three: the
    one to prefer, the one for a single Bash command, and the waiver."""
    body = section(8)
    assert 'subprocess.run(["git", "-C", d, "commit"' in body, (
        "the shape that carries no Bash command line at all"
    )
    assert "git -C /abs/path/r1" in body, "the written-out path, which is the Bash form"
    assert ": '[no-review]';" in body, "the waiver"


def test_the_contract_says_the_waiver_goes_in_front():
    """After `git commit` a bare word is a pathspec and git rejects the whole
    command, so a session told only the token writes one that cannot run."""
    assert "pathspec" in section(8), "nothing says why the token goes in front"


def test_the_contract_says_a_loop_variable_is_still_unreadable():
    """The reader fills in a name the command assigned itself and cannot fill
    a loop variable, so a session told only the first half writes
    `for n in 1 2; do git -C "$SB/r$n" …` and gets the prompt anyway."""
    assert "loop variable" in section(8), (
        "nothing says which names the reader still cannot fill"
    )


def test_the_contract_says_who_the_prompt_reaches():
    """Without the reason this reads as a style rule, and a session under
    pressure drops style rules first."""
    body = section(8)
    assert "#36" in body, "the incident is not cited"
    assert "keyboard" in body, "nothing says the prompt reaches a person"


def test_the_reviewer_still_says_why_the_rule_reaches_its_own_edits():
    """What stayed in `agents/warden.md` is the application, not the shapes.

    The warden edits less than the smith and would read a rule about probes
    that commit as somebody else's. Its own paragraph is what says a scratch
    fixture and a patched file are edits too, and it is the one place the #36
    cost is stated for a round that is running rather than for work."""
    warden = " ".join(read("agents", "warden.md").split())
    assert "#36" in warden, "the reviewer's own copy of the incident went"
    assert "not driving the session" in warden, (
        "the reviewer stopped being told who the prompt reaches during a "
        "round, which is the half that makes the rule its own"
    )
    assert "§8" in warden, (
        "the pointer went, so the shapes are reachable only by an agent that "
        "already knows to look for them"
    )


def test_the_fact_finder_points_at_the_rule_it_no_longer_restates():
    """`agents/scribe.md` step 4 carried the three shapes verbatim. It now
    says what reading settles for an original, and points at §7 and §8."""
    scribe = " ".join(read("agents", "scribe.md").split())
    assert "§8" in scribe, "the fact-finder can no longer reach the shapes"
    assert "read, not probed" in scribe, (
        "the scribe's own half — what an original settles by reading — went "
        "with the shapes it used to sit beside"
    )
