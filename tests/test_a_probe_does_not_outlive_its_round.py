"""Two rules that cost a session before anyone wrote them down.

A probe is throwaway, so the ways it can go wrong are never reviewed and
never regress-tested. Both of these were paid for once at full price:
sixty-eight minutes inside one hung shell chain, and a round's uncommitted
fixes deleted by the loop that was verifying them. Neither is about
git or about shells; both are about a temporary thing being written with
less care than the code it checks.

Nothing else pins either sentence, and a rule nothing pins is one a rewrite
drops without noticing — which is how the same review chain lost four
document claims one round apart.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def test_the_probe_rules_say_a_fixture_chain_is_and():
    skill = read("skills", "code-review", "SKILL.md")
    assert "A fixture chain is `&&`, never `|`" in skill, (
        "the probe rules lost the sequencing rule; a `|` between two commands "
        "feeds one to the other instead of ordering them, and the chain waits "
        "on stdin forever"
    )
    assert "waiting on stdin" in skill, (
        "the rule kept its instruction and lost its reason, which is the half "
        "a reader needs to recognise the shape in their own command"
    )


def test_the_probe_rules_ask_for_a_timeout_somebody_chose():
    skill = read("skills", "code-review", "SKILL.md")
    assert "a timeout" in skill and "rather than one you assumed" in skill, (
        "nothing tells a probe that can run long to carry a bound; the hang "
        "that cost the session exceeded the tool's own maximum"
    )


def test_smith_commits_before_it_mutates():
    smith = read("agents", "smith.md")
    assert "Commit before you mutate" in smith, (
        "the mutation-loop rule is gone; a loop reverting with "
        "`git checkout --` restores HEAD and takes uncommitted fixes with it"
    )
    assert "restore from your own copy" in smith, (
        "the rule kept the commit half and lost the restore half, and the "
        "restore half is the one that deleted a round's work"
    )
