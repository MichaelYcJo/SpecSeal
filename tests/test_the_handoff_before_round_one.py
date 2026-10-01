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

    # Phase 4 of #107 re-pointed the second half. The rule that a fact with
    # no coordinate and no label is an assertion nobody has opened is §5 of
    # the agent contract, which every agent receives at startup -- the smith
    # was one of two definitions stating it and the scribe stated it nowhere.
    # What stays in the definitions is the ROUTE: the section a prompt's
    # facts arrive under, which is what this case is about.
    assert "assertion nobody has opened" in flat(
        "skills", "agent-contract", "SKILL.md"
    ), (
        "the contract stopped saying what a fact with neither a coordinate "
        "nor a label is, so the route above leads to a section whose rule "
        "nothing states"
    )


# --- the interim home stops being one ---------------------------------------


def pointer_section(text):
    """The body of `## What every spawn prompt used to carry`, heading to the
    next `## `. Scoped rather than whole-file on purpose: the sentence this
    pins is also stated in `## Status`, so a document-wide search would stay
    green with the section itself gutted -- which is the one edit this case
    exists to catch."""
    match = re.search(
        r"^## What every spawn prompt used to carry$(.*?)(?=^## )",
        text,
        re.M | re.S,
    )
    assert match, (
        "the pointer section is gone or renamed. It replaced the interim home "
        "that carried the method half of every spawn prompt (#107 phase 5); a "
        "rename has to bring this case with it"
    )
    return " ".join(match.group(1).split())


def test_the_protocol_points_at_the_contract_instead_of_restating_it():
    """#107 phase 5. The section named itself an interim home and named the
    issue that would end it. It now points at the two files that carry those
    rules, and the sentence a prompt is actually governed by is what stands
    in its place.

    Both halves matter and only the second is unusual. A pointer that keeps
    the rules beside it is two answers in front of one reader, which is the
    duplication the move was made to end -- so the absence half is asserted
    as hard as the presence half."""
    section = pointer_section(read("docs", "review-handoff-protocol.md"))
    assert "a prompt carries what is specific to the round and nothing else" in (
        section.lower()
    ), (
        "the section stopped saying what a prompt is left holding, which is "
        "the one rule that stayed here when the rest moved"
    )
    assert "skills/agent-contract/SKILL.md" in section, (
        "the pointer names no contract, so a reader arriving for the rules "
        "leaves with neither them nor the path to them"
    )
    assert "agents/<name>.md" in section, (
        "the pointer names the shared half and not the per-agent half, which "
        "is half of the three-layer split"
    )


def test_the_protocol_no_longer_states_the_rules_it_points_at():
    """The restatement check, one phrase per list that used to sit here.

    Each is verbatim from what phase 5 removed, so a paste-back is red rather
    than invisible -- the same reasoning `test_a_moved_rule_leaves_its_
    definition.py` applies to the agent definitions, applied to the document
    those rules were moved OUT of."""
    protocol = flat("docs", "review-handoff-protocol.md")
    for phrase, whose in (
        ("never `cmd | tail; echo $?`", "the contract's §1"),
        ("enumerate the class, do not fix the coordinate", "the contract's §12"),
        ("Do not push, do not open a pull request", "the contract's §6"),
        ("make a `uv` venv", "`agents/warden.md`"),
        ("Mutation-test every unit added", "`agents/smith.md`"),
    ):
        assert phrase not in protocol, (
            f"the protocol states {whose} again: {phrase!r}. This document is "
            "a pointer at those rules now, and a copy beside the pointer is "
            "the state #107 opens with"
        )


def test_the_smiths_definition_mandates_mutating_every_unit_it_added():
    """The rule the case above says is `agents/smith.md`'s is actually there.

    Measured 2026-09-03 at `dcdf4e4`, phase 6 of #107: it was not. Phase 4
    never moved *mutation-test every unit added, one at a time, before
    handing over* into the definition, and phase 5 removed the one place it
    had ever been written -- the protocol's interim list. So the case above
    went green over a rule that had left the repository altogether, and the
    work item built to stop rules going missing is what deleted it.

    That is the general lesson, and it is why this case sits here rather
    than in a module of its own: an absence check with no presence check
    beside it cannot tell a rule that MOVED from a rule that was DELETED.
    The other four rows of that table point at contract sections, which
    `test_the_agent_contract_holds_the_universal_rules.py` pins from the
    other side; this row pointed at a definition and nothing pinned it.

    Contract §15 is the neighbour, not this rule. It asks that a case be
    seen red on the day it is planted; this asks that every unit the branch
    added be broken before the branch leaves the implementer's hands. Both
    halves are asserted -- the act and its timing -- because a definition
    that kept only the act would read as §15 restated, which
    `test_a_moved_rule_leaves_its_definition.py` would then be right to
    refuse."""
    smith = flat("agents", "smith.md")
    # The whole clause, not its words one by one. Asserting `one at a time`
    # alone passed under the mutation that removed the cadence, because the
    # design gate two hundred lines up says asking questions `one at a time`
    # is a cost paid repeatedly -- an unrelated sentence holding the phrase
    # up. Measured while showing this case red, 2026-09-03.
    assert (
        "Mutation-test every unit you added, one at a time, before you hand "
        "over." in smith
    ), (
        "`agents/smith.md` does not mandate mutating what it added, on that "
        "cadence, at that moment. `spec.md` of work item 1788433011 puts the "
        "rule in the smith's own layer -- *only the agent that adds units "
        "can* -- and the protocol that used to carry it is a pointer now, so "
        "a definition without it leaves the rule stated nowhere at all. "
        "Units broken together cannot say which case caught which, and a "
        "mutation run after the handover is one the next reader takes on "
        "trust, which is why the cadence and the timing are in the assertion "
        "rather than beside it"
    )
    assert "watch one go red" in smith, (
        "the rule stopped asking for the observation that makes it a "
        "measurement. Breaking a unit and running the suite is not a "
        "mutation test until a case is seen to fail for it"
    )


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
    demand the work cannot meet — which is how rules stop being read.

    Re-pointed in phase 4 of #107. The rule and the caveat are §10's, which
    the smith receives at startup; what §10 sends back to the definition is
    the NUMBER, because a figure that measures a reviewer does not measure an
    implementer. So the caveat is asserted against the contract and the
    number against the definition, which is where each of them can go missing
    without the other noticing."""
    contract = flat("skills", "agent-contract", "SKILL.md")
    assert "An edit-test loop is serial" in contract, (
        "the contract stopped conceding what a serial loop cannot give, so "
        "the batching rule became a demand the work cannot meet"
    )
    assert "in that agent's definition" in contract, (
        "the contract stopped sending the numbers back to the definitions, "
        "and a figure with no home is one that measures the wrong agent"
    )
    smith = flat("agents", "smith.md")
    # U+2013 EN DASH, built rather than typed: the definition spells both
    # ranges with one, so a hyphen would match nothing, and a typed one is
    # what the linter reads as an ambiguous character.
    dash = chr(0x2013)
    assert f"1.08{dash}1.17" in smith
    assert f"1.29{dash}1.89" in smith
    assert "never obliged to fake a batch" in smith


def framer_opening(text):
    """The body of `agents/framer.md`'s `## How a frame opens`, heading to the
    next `## `. Scoped so a phrase elsewhere in the definition cannot hold one
    of the claims below up after the section itself lost it."""
    match = re.search(r"^## How a frame opens$(.*?)(?=^## )", text, re.M | re.S)
    assert match, (
        "`agents/framer.md` has no `## How a frame opens`. The opening was typed "
        "into spawn prompts from 0.12.3 and lived in no file (#640); a rename "
        "has to bring this case with it"
    )
    return " ".join(match.group(1).split())


def test_the_framers_definition_carries_its_opening():
    """#640, recommendation 1. A rule kept only in whoever last wrote a
    prompt goes missing without a trace (#107), and the framer's opening was
    exactly that: found by the 2026-09-28 sweep in no file at all.

    The three claims are asserted by phrase, and the prohibition the prompts
    carried is asserted ABSENT over the whole definition. Every framer that
    read 1.00-1.12 since 0.12.3 was told not to open with a parallel read
    burst; the 0.12.2 framers, never told, read 1.48-1.64. Writing that
    sentence into the file is the one edit that would fix the floor in place."""
    text = read("agents", "framer.md")
    section = framer_opening(text)
    assert text.index("## What you read, and how widely") < text.index(
        "## How a frame opens"
    ), "the opening sits before the reading it bounds"
    assert "skeleton `spec.md`" in section, "the early write went"
    assert "inside your first few calls" in section, (
        "the early write lost its moment, and a skeleton written at the end "
        "is what a watchdog loss leaves no trace of"
    )
    assert "about six reads or ranges" in section, "the bound on one call went"
    assert "never the whole reading list" in section, (
        "the bound says how large a call may be and not what it may not be, "
        "which is the opening burst #456's stalls are the evidence about"
    )
    assert "§10" in section, "the bound stopped citing the rule it applies"
    assert "read by range" in section and "sed -n" in section, (
        "the large-file half went, which is the third clause #478 recorded"
    )
    whole = " ".join(text.split()).lower()
    for prohibition in ("read burst", "not to open with", "do not open with"):
        assert prohibition not in whole, (
            f"`agents/framer.md` carries {prohibition!r}. The rewording bounds "
            "the opening and forbids nothing, because every reading taken "
            "under the prohibition sat at the floor"
        )


def test_the_framers_definition_carries_its_own_number():
    """§10 sends each kind's number back to that kind's definition, and the
    warden's (1.89) and the smith's (1.08-1.17) were there while the
    framer's was nowhere. The bar is 1.4, under the band it comes from."""
    section = framer_opening(read("agents", "framer.md"))
    dash = chr(0x2013)
    assert "1.4 tools per turn" in section, "the framer's bar went"
    assert f"1.46{dash}1.79" in section, (
        "the bar lost the band it was set under, and a number with nothing "
        "behind it reads as style advice"
    )
    assert "promises no saving" in section, (
        "the number reads as a forecast. `## Why the frame is not the "
        "builder's to draw` refuses one, and the bar is a lens"
    )


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
    # #640. A frame is a wide read of independent documents, so the framer
    # has a bar of its own, and the script's constant is cross-pinned to it
    # below rather than read from it.
    assert "| framing | tools per turn **≥ 1.4** |" in protocol, (
        "the framing bar went, and `--segments` grades framer rows against a "
        "number no policy states"
    )
    assert "never a refusal threshold" in protocol, (
        "the bar is a lens for rounds of ordinary size — a 23-call round "
        "read 1.64 doing everything right, and a gate failing it would "
        "punish the small honest round"
    )


def bars_section(text):
    """The body of `### After the run — the per-segment bars`, heading to the
    next heading of any level.

    Scoped rather than whole-file, for the reason `pointer_section` above is:
    the document names `session_cost.py` two sections up, so a document-wide
    search would stay green with this section saying nothing about the
    run-level table -- which is the one edit this case exists to catch."""
    match = re.search(
        r"^### After the run — the per-segment bars$(.*?)(?=^#{2,3} )",
        text,
        re.M | re.S,
    )
    assert match, (
        "the per-segment bars section is gone or renamed. It is where the "
        "orchestrator meets the meter's numbers, and a rename has to bring "
        "this case with it"
    )
    return " ".join(match.group(1).split())


def test_the_tying_paragraph_says_which_reading_applies_the_bars():
    """#640. The paragraph said the script cannot tell a reviewer's
    transcript from an edit-test loop, and for `--segments` that stopped
    being true: a row's kind is the `subagent_type` of the spawn it was
    joined to. The plain reading still cannot tell, which is why its
    advisory stays where it is and why the sentence is narrowed to it rather
    than removed."""
    section = bars_section(read("docs", "review-handoff-protocol.md"))
    assert "`--segments` applies the bars above by kind" in section, (
        "the paragraph does not say the page grades a row, so a reader meets "
        "a named row under a bar with no policy saying where it came from"
    )
    assert "`subagent_type`" in section, (
        "the paragraph says the page knows a row's kind and not how"
    )
    assert "a row with no kind is not graded" in section, (
        "the paragraph leaves an unnamed row's grade to be guessed"
    )
    assert (
        "the plain reading cannot tell a reviewer's transcript from an "
        "edit-test loop" in section
    ), (
        "the sentence about what the script cannot tell was dropped instead "
        "of narrowed, and it is still true of the plain reading"
    )


def test_the_bars_and_the_run_level_table_judge_different_things():
    """Two instruments over the same run, and a reader who meets only the
    bars has no way to know the second one exists.

    A bar reads one transcript against its own kind. The run-level table
    reads a whole run against the last run measured, which is a question no
    bar asks -- rounds, wall clock, commits and tokens together. The section
    that owns the bars is where that distinction has to be drawn, because it
    is the section an orchestrator opens holding a segment's numbers.

    The absence half is asserted as hard as the presence half. The table's
    rows are defined in `skills/verify/SKILL.md`, and a copy of them here
    would be a second thing to keep in step; and the table goes to the
    rolling log the measurement section already names, so a sentence that
    reads as a new home for a reading is the other way this paragraph can go
    wrong."""
    section = bars_section(read("docs", "review-handoff-protocol.md"))
    assert (
        "The bars judge a segment against its kind; the run-level table "
        "judges a run against the last run measured." in section
    ), (
        "the section does not say which instrument judges what, so a reader "
        "holding a segment's numbers meets one bar and no run"
    )
    assert "skills/verify/SKILL.md" in section, (
        "the section names no owner for the table, so a reader arriving for "
        "its rows leaves with neither them nor the path to them"
    )
    assert "Measure the segment, and feed the flow log" in section, (
        "the pointer names the file and not the section, which is a whole "
        "skill to search for one table"
    )
    assert "not a destination of its own" in section, (
        "the sentence reads as a third place a reading can go. The table "
        "joins the segment readings in the rolling log; naming it beside the "
        "bars must not invent a home for it"
    )
    assert "what the whole run cost" in section, (
        "the paragraph says the table asks another question and never says "
        "what it is, so a reader has the distinction and not the point of it"
    )
    for row in TABLE_ROWS:
        assert row not in section, (
            f"the section restates the table's rows ({row!r}). They are "
            "defined in `skills/verify/SKILL.md`, and a second copy is a "
            "second thing to keep in step"
        )
    # Round 2's finding 2. The labels above catch a paste-back OF THE TABLE;
    # what round 1's finding 8 actually removed was a lowercase gloss that
    # matches none of them. Replacing the sentence with it is already caught,
    # because `what the whole run cost` goes with it -- but ADDING it back
    # beside the sentence passed every case in this module. So the gloss is
    # refused by its own removed wording, the way
    # `test_the_protocol_no_longer_states_the_rules_it_points_at` refuses
    # what phase 5 removed.
    assert "rounds, wall clock, commits, findings and tokens" not in section, (
        "the lowercase gloss of the table's rows is back in the bars "
        "section. It is a second copy of the rows to keep in step, and being "
        "lowercase prose rather than the labels is what let it sit here "
        "through round 1 with nothing red"
    )


# One fragment per row of the table in `skills/verify/SKILL.md` §*Measure the
# segment, and feed the flow log*, taken verbatim. Refused in the bars section
# above and held to the owner below.
TABLE_ROWS = (
    "Rounds — finding and verifying",
    "Wall clock, routing commit to last record",
    "Commits, by kind",
    "Findings by severity",
    "Findings by `Location`",
    "Records' share of the diff",
    "Model turns",
    "Segments: count, minutes and tokens per kind",
    "Broad gate",
)


def test_the_refused_rows_are_the_owners_own():
    """The coupling that keeps the refusal above worth having: a row reworded
    in `skills/verify/SKILL.md` and not here leaves it guarding a string
    nobody would paste. The same one
    `tests/test_the_chain_section_has_one_shape.py` keeps over its own list.

    Round 1's finding 8 widened that refusal from three labels to nine, and
    round 2's finding 2 is that the widening does not reach what the finding
    was raised against. That prose glossed five rows in lowercase -- `rounds,
    wall clock, commits, findings and tokens` -- which shares no substring
    with any label. So the two halves need two different checks, and the
    gloss is refused by its own removed wording in the case above rather
    than by this list.

    Neither reaches a gloss somebody writes fresh, and no string can: the
    words are lowercase and generic, and `rounds` occurs four times in
    that section legitimately. That half is a reader's, and saying so is the
    point of writing it down -- a list that reads as though it closed the
    class is worse than one nobody expected to."""
    owner = read("skills", "verify", "SKILL.md")
    for row in TABLE_ROWS:
        assert row in owner, (
            f"{row!r} is no longer a row of the table in "
            "`skills/verify/SKILL.md`, so the refusal above guards a string "
            "nobody would paste. Re-take these from the owner's table"
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


def test_the_scripts_bars_are_the_protocols():
    """#640. The bars live in the protocol's table and, since `--segments`
    grades by kind, in `session_cost.py`'s `SEGMENT_BARS` too -- constants,
    because the script runs from the installed plugin in repositories with no
    such document. Two copies of a number is the six-month failure the plan
    names, so this reads both files and either moving alone turns it red.

    The implementing row is held too: the protocol says it is never judged
    on tools per turn, and the script's entry for it is the exemption."""
    script = read("skills", "verify", "scripts", "session_cost.py")
    protocol = read("docs", "review-handoff-protocol.md")
    for kind, segment in (("warden", "reviewing"), ("framer", "framing")):
        constant = re.search(rf'"{kind}": \("{segment}", ([\d.]+)\)', script)
        assert constant, f"`SEGMENT_BARS` lost its {kind} entry or its shape"
        row = re.search(
            rf"^\| {segment} \| tools per turn \*\*≥ ([\d.]+)\*\* \|", protocol, re.M
        )
        assert row, f"the protocol's bars table lost its {segment} row or its shape"
        assert constant.group(1) == row.group(1), (
            f"session_cost.py grades a {kind} row against {constant.group(1)} "
            f"and the protocol's {segment} bar is {row.group(1)} -- move both or "
            "neither"
        )
    assert '"smith": ("implementing", None)' in script, (
        "`SEGMENT_BARS` grades a smith row, and the protocol's implementing row "
        "says tools per turn never judges one"
    )
    assert re.search(r"^\| implementing \|.*never tools per turn", protocol, re.M)


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
