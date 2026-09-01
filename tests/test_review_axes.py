"""The axes table is the review's coverage, so what it omits is invisible.

Eight axes each settled by reading one request end to end. A defect that needs
a second actor — a reservation mutated while an external call is in flight —
matched none of them, and an axis nobody listed leaves no trace: `❓ out of
verified scope` records that you looked and could not decide, not that nobody
looked. Two documents share this table; drift between them is the bug.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def test_the_table_asks_what_a_second_actor_does():
    axes = read("skills", "code-review", "SKILL.md")
    assert "| Concurrency & atomicity |" in axes, (
        "the axes table lost the only row that is not settled by reading one path"
    )
    for probe in ("between the read that decides", "retry executes twice"):
        assert probe in axes, f"the concurrency row lost `{probe}`"


def test_the_table_asks_the_security_questions():
    """Security was named in stage 2 and absent from the table, and the table
    is what makes an axis mandatory — an axis in prose leaves no `❓` when
    nobody walks it. Three of one round's four blocking findings had a
    stronger security frame than the one they were given, one of them a
    fail-open in a repository that keeps `test_gates_do_not_fail_open.py`
    for that class alone (issue #57)."""
    axes = read("skills", "code-review", "SKILL.md")
    assert "| Security |" in axes, "the axes table has no security row"
    for probe in ("fails open or closed", "crafted name, path, or payload"):
        assert probe in axes, f"the security row lost `{probe}`"
    # Round 1's 🟡 4: the prose groups Security with Concurrency as
    # not-settled-by-one-request-read and grounded only concurrency, so a
    # prose tightening could read the grouping as licensing a revert. The
    # ground is what makes the grouping earned rather than asserted.
    assert "nobody sends in good faith" in axes, (
        "the security paragraph lost the ground for its one-path exemption"
    )


def test_the_table_says_it_is_a_floor():
    """A fixed list is repeatable and blind in the same move.

    Without this the next unlisted axis — rounding, time zones, migration
    ordering — goes the way the concurrency one did."""
    axes = read("skills", "code-review", "SKILL.md")
    assert "### The table is a floor, not a ceiling" in axes
    assert "name this change's own axes before starting" in axes, (
        "nothing tells a round to add the axes this particular diff needs"
    )


def test_legacy_parity_still_points_at_that_table():
    """`legacy-parity` inherits the axes by reference, so one edit covers both.

    A copy would be two answers shipping at once."""
    assert "the same comparison axes" in read("skills", "legacy-parity", "SKILL.md")


def test_the_preset_block_carries_the_routing_decision():
    """The rule lived only in `implement`, which loads when the skill is invoked.

    A session that just commits never reads it and meets the gate at the commit
    instead — measured on a repository where <git-dir>/specseal-reviewed had
    never been written at all."""
    preset = read("CLAUDE.md").split("<!-- specseal:end -->")[0]
    assert "Routing, decided at the start" in preset
    assert "specs/<work-item-id>/routing.md" in preset
    assert "[no-review]" in preset and "[no-parity]" in preset


def test_the_handoff_protocol_inherits_no_verdict_anywhere():
    """Prose and the field table are read by different people.

    Whoever builds a tool fills the fields, so a row saying axes carry
    "without re-walking" outranks a corrected sentence twenty lines below it.
    The protocol had both at once."""
    protocol = read("docs", "review-handoff-protocol.md")
    for stale in ("inherit judged axes", "without re-walking"):
        assert stale not in protocol, f"verdict inheritance came back as `{stale}`"
    assert "The coordinates carry; the verdicts do not" in protocol, (
        "the round-N field table stopped saying what actually carries"
    )
    assert "hands over its coordinates, not its verdict" in protocol, (
        "the conformance rule stopped saying what actually carries"
    )


def test_implement_and_the_preset_block_do_not_drift():
    """Both state the same decision; only one of them is always loaded."""
    implement = " ".join(read("skills", "implement", "SKILL.md").split())
    preset = " ".join(read("CLAUDE.md").split("<!-- specseal:end -->")[0].split())
    for both in (
        "specs/<work-item-id>/routing.md",
        # The write is its own command. Both documents mandate it and the
        # commit gate's first prompt now names it as a way out, so all three
        # drift together or not at all -- and this is the one the gate cannot
        # check for itself, because a batched write leaves nothing on disk to
        # look at.
        "in a command of its own",
        "through the review chain",
        "straight to the PR",
        "open the pull request",
        "stop before the pull request",
        # The SHAPE of the asking, not just its vocabulary. Three independent
        # yes/no answers written as single-select options is eight
        # combinations and three interruptions; the rule against asking them
        # separately is worth nothing if only one document carries it, and
        # the preset block is the one a session that never loads the skill
        # reads.
        "one `multiSelect` question with three checkboxes",
        "What is checked is the answer",
        "each box is a row of",
        # The third axis. A document still saying two would send a session to
        # a template whose row it never asked about.
        "`the session`",
    ):
        assert both in implement, f"the skill lost `{both}`"
        assert both in preset, f"the preset block lost `{both}`"


def test_the_fix_pass_resumes_the_implementer():
    """A fix pass as a fresh spawn re-establishes what the implementing
    session already holds. Measured three times with no counterexample —
    282 calls / 45 minutes fresh (#33) against 30 / 3.9 (#29) and 26 / 5.2
    (the #57 chain) resumed — and an expectation with no number behind it
    reads as style advice (work item 1788277657, round 1's tests-todo)."""
    skill = read("skills", "code-review", "SKILL.md")
    assert "resuming the session that built the branch" in skill, (
        "the orchestrator sections lost the sentence saying how the fixing "
        "session is obtained"
    )
    assert "282 calls and 45 minutes" in skill, "the measurement went"
    assert "the fresh spawn is the only option left" in skill, (
        "the fallback for a session that no longer exists went"
    )
