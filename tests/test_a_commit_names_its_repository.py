"""An agent commits with its repository written out, and the rule says why.

Contract §17 is the written half of work item `1790644505` (#662, #665). The
gate half refuses, in an `automation` run, every commit it stops; this half is
what makes the refusal rare. Both were measured to be needed: in the
milestone-49 run three of the four stops that reached the person began
`cd <worktree> &&` and committed after a `;` or a new line, and the
orchestrator's loop over a variable met the gate in all three milestone runs.

A rule that ships only as prose has to be held by something, or the next
sweep removes it and nothing notices (`tests/test_edits_go_through_the_edit_
tool.py` records how §9 learned that). So each reason is pinned on its own,
the way §9's pair is, and the pairing sentence with them: one reason alone
reads as a style preference. The section points at §8 and §9 rather than
restating them, and `tests/test_a_moved_rule_leaves_its_definition.py` is
what refuses a copy.
"""

import os
import re

from conftest import load_hook_module

ROOT = os.path.join(os.path.dirname(__file__), "..")
CONTRACT = ("skills", "agent-contract", "SKILL.md")
ORCHESTRATION = ("skills", "implement", "orchestration.md")
HEADING = re.compile(r"^## §(\d+) (.+)$", re.M)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def section(number):
    text = read(*CONTRACT)
    heads = list(HEADING.finditer(text))
    for i, m in enumerate(heads):
        if int(m.group(1)) == number:
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            return m.group(2), " ".join(text[m.end() : end].split())
    return None, ""


def test_the_rule_is_the_last_section_and_names_the_shape():
    heading, body = section(17)
    numbers = [int(n) for n, _ in HEADING.findall(read(*CONTRACT))]
    assert numbers[-1] == 17, "§17 is not the last section"
    assert heading == "A commit names its repository in the command that makes it"
    assert "absolute path written out after `git -C`, in a command of its own" in body
    assert "join it to the commit with `&&` and nothing else" in body


def test_the_rule_pairs_its_two_reasons():
    _, body = section(17)
    assert "Two reasons, and they are two different facts about the gate" in body


def test_the_first_reason_is_where_the_shell_starts():
    """Without it, `cd W && x ; git commit` reads as a commit in W."""
    _, body = section(17)
    assert "your shell starts in the session's directory at every call" in body
    assert "where a failed `cd` leaves the shell" in body


def test_the_second_reason_is_what_the_gate_can_read():
    """Without it, a loop over `$d` reads as a path written out."""
    _, body = section(17)
    assert "the gate reads a command before the shell expands it" in body
    assert "a loop variable in the path names no directory at all" in body


def test_it_points_at_the_probe_and_edit_rules_rather_than_restating_them():
    _, body = section(17)
    assert "§8" in body and "§9" in body
    for copied in ("subprocess.run", "An edit must be able to fail"):
        assert copied not in body, f"§17 restates a neighbour: {copied!r}"


def test_the_orchestrator_commits_its_routing_files_the_same_way():
    """The loop over `$wt`, `$1` and `$d` was the orchestrator's, in all three
    milestone runs on disk."""
    text = " ".join(read(*ORCHESTRATION).split())
    assert "contract §17" in text
    assert "each work item's `routing.md` in a command of its own" in text


def test_the_contract_still_does_not_trip_the_commit_gate():
    """A session patching the contract meets the gate if its prose reads as a
    commit; §17 is the section most likely to, being about commits."""
    gate = load_hook_module("commit-review-gate.py", "crg_seventeen")
    assert not gate._hides_a_commit(read(*CONTRACT))
