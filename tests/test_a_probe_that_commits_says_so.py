"""Neither agent file said how to write a scratch-repo probe that commits.

Issue #82. A review agent spawned to run round 1 wrote its probes with shell
variables, two of them reached a user who was not driving the session as
permission prompts inside five minutes, and the agent was stopped to end them
— which cost the review round. The agent had been told to use literal paths in
its own prompt, and that prompt is written by a different session every time.

So the instruction lives in the agent files, where every future spawn of
either one reads it. Both carry it, because one agent knowing it is how this
reached a user in the first place.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
AGENTS = ("warden", "scribe")


def read(name):
    with open(os.path.join(ROOT, "agents", f"{name}.md"), encoding="utf-8") as f:
        return f.read()


def test_both_agents_carry_all_three_shapes():
    """S9. Three shapes avoid the prompt and a session needs all three: the
    one to prefer, the one for a single Bash command, and the waiver."""
    for name in AGENTS:
        text = read(name)
        assert 'subprocess.run(["git", "-C", d, "commit"' in text, (
            f"{name}: the shape that carries no Bash command line at all"
        )
        assert "git -C /abs/path/r1 commit" in text, (
            f"{name}: the written-out path, which is the Bash form"
        )
        assert ": '[no-review]';" in text, f"{name}: the waiver"


def test_both_agents_say_the_waiver_goes_in_front():
    """After `git commit` a bare word is a pathspec and git rejects the whole
    command, so a session told only the token writes one that cannot run."""
    for name in AGENTS:
        text = read(name)
        assert "pathspec" in text, f"{name}: nothing says why the token goes in front"


def test_both_agents_say_a_loop_variable_is_still_unreadable():
    """The reader fills in a name the command assigned itself and cannot fill
    a loop variable, so a session told only the first half writes
    `for n in 1 2; do git -C "$SB/r$n" …` and gets the prompt anyway."""
    for name in AGENTS:
        assert "loop variable" in read(name), (
            f"{name}: nothing says which names the reader still cannot fill"
        )


def test_both_agents_say_who_the_prompt_reaches():
    """Without the reason this reads as a style rule, and a session under
    pressure drops style rules first."""
    for name in AGENTS:
        text = read(name)
        assert "#36" in text, f"{name}: the incident is not cited"
        assert "keyboard" in text, f"{name}: nothing says the prompt reaches a person"
