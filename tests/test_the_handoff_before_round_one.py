"""The step before round 1 had no protocol, and the orchestrator was blind.

Round N hands round N+1 its coordinates — `round-N.md`'s Inherited axes,
"the coordinates carry; the verdicts do not". Nothing equivalent existed for
the step before round 1: the orchestrator hands the implementer a spawn
prompt nobody's format constrains, and the one measured fact that travelled
as prose (a count standing in for a claim) cost a full review round before
anyone could check it. And while the implementer runs, the progress readout
it is already writing — `plan.md`'s Status column — is named by no document
the orchestrator reads, so "is 40 minutes normal" was answered by `git log`
twice on two consecutive work items.

Each case here was shown red before the prose it pins landed (#29).
"""

import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    return " ".join(read(*parts).split())


# --- the handoff before round 1 ---------------------------------------------


def test_the_protocol_carries_the_handoff_before_round_one():
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "The handoff before round 1" in protocol, (
        "the protocol hands state between rounds and says nothing about the "
        "handoff that starts the work"
    )
    assert "coordinates rather than prose" in protocol
    assert "executed / read / unverified" in protocol, (
        "the labels a handoff fact carries are verify's three, by name — a "
        "fact with none is an assertion nobody has opened"
    )
    assert "an aggregate is not a coordinate" in protocol, (
        "the measured failure went: a count travelled as if it were a "
        "checkable fact, and the claim it stood for was wrong"
    )
    assert "where to measure" in protocol, (
        "a claim that flips on measurement point needs the point, not just "
        "the place — two findings flipped on it in one work item"
    )


def test_the_draft_number_moved_for_the_new_section():
    protocol = read("docs", "review-handoff-protocol.md")
    assert "draft 0.6" in protocol or "Draft 0.6" in protocol, (
        "a changed layout or rule moves the draft"
    )


def test_the_implementer_documents_point_at_the_section():
    """A protocol section nobody is routed to is the same defect one layer
    up: the answer exists and the party needing it does not know it is
    there — which is how session_cost.py went unused for a day."""
    for parts in (("skills", "implement", "SKILL.md"), ("agents", "smith.md")):
        text = flat(*parts)
        assert "handoff before round 1" in text, "/".join(parts)
        assert "assertion nobody has opened" in text, "/".join(parts)


# --- progress observability -------------------------------------------------


def test_the_protocol_names_the_progress_channel_and_the_stall_signal():
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "Status column" in protocol, (
        "the readout the implementer already writes during the run has to be "
        "named where the orchestrator reads, or git log stays the only answer"
    )
    assert "time since it last advanced" in protocol, (
        "wall clock cannot separate a long run that is finishing from a "
        "short one that is wedged; the stall signal can"
    )
    assert "session_cost.py" in protocol, (
        "the meter existed through a full day of measurements nobody took, "
        "because nothing a session reads pointed at it"
    )


# --- the batching expectation in the contracts ------------------------------


def test_the_reviewers_contract_expects_batched_reads_and_probes():
    """Task shape dominates: a review reads independent things, and the one
    instructed round that batched (1.89 tools per turn) was the fastest
    round measured. The reviewer's contract is where the expectation pays."""
    warden = flat("agents", "warden.md")
    assert "Independent reads and probes go out together" in warden
    assert "1.89" in warden, (
        "the measurement went, and an expectation with no number behind it "
        "reads as style advice"
    )


def test_the_smiths_contract_does_not_demand_what_a_serial_loop_cannot_give():
    """The same rule lands on the smith with the caveat that keeps it
    honest: an edit-test loop is inherently serial (1.08-1.17 measured
    against 1.29-1.89 for review rounds), and a rule that ignores that is a
    demand the work cannot meet — which is how rules stop being read."""
    smith = flat("agents", "smith.md")
    assert "Independent reads and probes go out together" in smith
    assert "inherently serial" in smith
    assert "not forced to fake a batch" in smith


# --- the per-segment bars (work item 1788277657, round 1's tests-todo) ------


def test_the_protocol_names_a_bar_per_segment_kind():
    """One bar misread two of the three segment kinds: the ratio that judges
    a reviewer is the wrong question for an edit-test loop, and the meter's
    numbers had no written rule at all about what they mean."""
    protocol = flat("docs", "review-handoff-protocol.md")
    assert "tools per turn **≥ 1.8**" in protocol, "the reviewing bar went"
    assert "never tools per turn" in protocol, (
        "the implementing row must say which number does NOT judge it"
    )
    assert "`repeats = 0`" in protocol, "the implementing bar went"
    assert "| verifying | exempt |" in protocol
    assert "never a refusal threshold" in protocol, (
        "the bar is a lens for rounds of ordinary size — a 23-call round "
        "read 1.64 doing everything right, and a gate failing it would "
        "punish the small honest round"
    )


def test_the_title_and_the_status_section_agree_on_the_draft():
    """🔴 1 of the work item's round 1: the title moved to draft 0.8 while
    the Status section still opened with 0.7 — one document naming two
    current drafts, and Status is what a conformance reader opens. This
    case was planted against exactly that state and seen red."""
    text = read("docs", "review-handoff-protocol.md")
    title = re.search(r"^# Review Handoff Protocol — draft (\d+\.\d+)", text, re.M)
    status = re.search(r"^Draft (\d+\.\d+), extracted", text, re.M)
    assert title, "the title moved off its `draft N.N` pattern"
    assert status, "the Status opening moved off its `Draft N.N, extracted` pattern"
    assert title.group(1) == status.group(1), (
        f"the title says draft {title.group(1)} and the Status section says "
        f"{status.group(1)} — a draft bump rewrites both lines or neither"
    )


def test_the_advisory_and_the_tying_paragraph_name_one_value():
    """The bars (1.8) live in the protocol and the advisory in the script,
    tied by one sentence — the plan's own six-month failure scenario is the
    script's threshold moving while the sentence keeps the old value. This
    case reads both files, so that move turns it red."""
    script = read("skills", "verify", "scripts", "session_cost.py")
    threshold = re.search(r'data\["tools_per_turn"\] < ([\d.]+)', script)
    assert threshold, "the advisory threshold moved off its pattern in session_cost.py"
    protocol = flat("docs", "review-handoff-protocol.md")
    assert (
        f"batching advisory below {threshold.group(1)} and stays there" in protocol
    ), (
        "the protocol's tying paragraph names a different value than "
        f"session_cost.py's {threshold.group(1)} — update the sentence, "
        "or the reader meets 1.8 and the advisory as a contradiction"
    )
