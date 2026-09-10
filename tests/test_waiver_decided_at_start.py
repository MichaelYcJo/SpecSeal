"""Where the work is going is decided in the first minute, and written down.

The rule spans four documents — the skill states it, the smith follows it, the
chain spec says what the gate does with it, and the template is what gets
written. A rule spread across four files fails by one of them quietly dropping
its part, which no single diff shows.

The rule: how a work item is routed has **three axes**, all asked in the same
batch before the first edit, and the answer goes into
`seal/specs/<work-item-id>/routing.md` rather than being re-derived at every
commit.

`Implementation` is the third and it is read on looser terms — optional, and
an unreadable answer means "not answered" rather than "not a declaration".
That looseness is why the count is asserted here rather than left implied: a
document still saying two is not wrong about anything the gate does, so
nothing else would catch it, and a session reading it would meet a template
row its question never asked about.

The second axis is not decoration. Opening a pull request is an outward-facing
act, and asked at the end it IS a mid-round prompt — the thing this release
removes. And the answer had to be recorded rather than inferred, because
"routed to the chain, not reviewed yet" and "nobody decided anything" were
byte-identical to the gate: one row of the old table said work routed to the
chain "needs no marker at all", which was true only after the first review
mark landed and false for every commit before it.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")

AXES = (
    "through the review chain",
    "straight to the PR",
    "open the pull request",
    "stop before the pull request",
    # The third axis. Its answers are `smith` and `the session`; only the
    # second is pinned, because `smith` appears in these documents for a dozen
    # unrelated reasons -- it is the name of the agent one of them IS -- and
    # would pass on any of them.
    "the session",
)


# The routing section — the axes, the checkbox, the file, the four
# combinations, the wake/quiet table — is `implement`'s orchestrator half
# since #292: the session that asks reads `orchestration.md`, and no smith
# spawn preloads it. The per-command waiver stays in `SKILL.md`, because
# the implementer is who types the command.
ORCH = ("skills", "implement", "orchestration.md")
SKILL = ("skills", "implement", "SKILL.md")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(text):
    """Rewrapped prose and table cells compare the same way collapsed.

    A literal with a newline in it was asserting the column width once.
    """
    return " ".join(text.split())


def test_the_skill_asks_every_axis_in_the_first_batch():
    skill = flat(read(*ORCH))
    assert "three axes" in skill, (
        "the skill still names two, so a session asks two and the template offers three"
    )
    assert "two axes" not in skill + flat(read(*SKILL)), (
        "the old count survived beside the new one"
    )
    for answer in AXES:
        assert answer in skill, f"the skill lost the answer `{answer}`"
    assert "before the first edit" in skill


def test_every_document_shows_the_third_axis_ROW_not_only_the_count():
    """Round 1, M1: the count said three, the table showed two, nothing red.

    The tuple above cannot carry this one. `the session` occurs nine times in
    `skills/implement/SKILL.md` and only two of them are about the axis, so
    deleting the axis row leaves eight matches standing -- which is the exact
    reason `smith` was left out of that tuple, applied to the answer that WAS
    put in it."""
    rows = [
        ln for ln in read(*ORCH).splitlines() if ln.startswith("| Implementation |")
    ]
    assert len(rows) == 1, (
        f"the axes table has {len(rows)} `Implementation` rows; the count "
        "beside it promises exactly one"
    )
    assert "smith · the session" in rows[0], (
        "the row lost the vocabulary, so a session reads a third axis with no answers"
    )
    # The agent file states the same axis in prose rather than a table, so it
    # is pinned on its own terms.
    smith = flat(read("agents", "smith.md"))
    assert "implementation (smith · the session" in smith, (
        "the agent stopped naming the third axis's answers"
    )


def test_the_optional_row_ships_the_criterion_that_decides_it():
    """#120: the row asked `smith` · `the session` and never said how to
    answer, so it was answered by habit — and #263 is where that habit was
    measured against the same class of change done in the parent session.

    The other two axes need no criterion: a wrong answer in either is
    contradicted at the next commit, because the gate stops recognising the
    file and goes back to asking. This one is contradicted by nothing, which
    is why the guidance has to travel with the row rather than sit in a skill
    a session may not have loaded.

    Written as a criterion and NOT as a default, which is the half a check can
    hold: a sentence naming one answer as what to do absent a reason makes the
    other the exception, and the row is optional precisely so that neither
    reads as the silent one. `test_the_template_PARSES_into_the_three_answers
    _it_ships` below holds the placeholder itself unanswered."""
    tpl = " ".join(read("templates", "sdd-routing.md").split())
    assert "FINDING OUT or WRITING DOWN" in tpl, (
        "the criterion went. The row is back to being answered by habit, "
        "which is the state #263 measured"
    )
    assert "is a STEP to send to `scribe`" in tpl, (
        "the criterion names no destination for discovery, so the axis it "
        "draws collapses back into `smith` or nothing"
    )
    # Round 1, finding 8. The criterion named three destinations for a row
    # that accepts two values -- `hooks/routing.py`'s IMPLEMENTATION_ANSWERS
    # is `smith` and `the session` -- and never said what to TYPE. A session
    # whose work is finding-out had two readings and the wrong one is
    # permitted by the same comment: line 27 says to delete the row rather
    # than invent a third answer. Deleting it there loses an answer that
    # exists. This row is the one axis nothing contradicts, so a session that
    # guesses gets no correction from anywhere.
    assert "That is a step and not an answer to this row" in tpl, (
        "the criterion routes discovery to `scribe` and stops, so a session "
        "reading it has a destination and no value to write in the row"
    )
    assert "still answers `the session`" in tpl, (
        "the comment stopped saying what to type for a discovery work item, "
        "which is the half `questions.md` Q4 did not have to answer"
    )
    assert "never deleted because the work is discovery" in tpl, (
        "the wrong recovery is permitted again: `Delete the row rather than "
        "inventing a third answer` reads as licence to delete a row whose "
        "answer exists, and the result is a record that says `not answered`"
    )
    assert "REPLACEABILITY, not cost" in tpl, (
        "the axis the last clause sits on went. Without it the threshold "
        "reads as a cost question, which is the one thing #263 says it is not"
    )
    assert "a number nobody has" in tpl, (
        "the threshold stopped saying it is unmeasured. An invented number "
        "here is a default wearing a criterion's clothes"
    )


def test_the_template_PARSES_into_the_three_answers_it_ships():
    """Round 1, M4: `| Implementor | Smith the agent |` shipped green.

    Every check on this file compared strings the test itself supplied, so
    the one reader that decides whether a declaration means anything --
    `parse()` -- had never been pointed at the template a session copies. A
    corrupt third row costs nothing at the gate, which is exactly why nothing
    else would ever report it."""
    import sys

    sys.path.insert(0, os.path.join(ROOT, "hooks"))
    import routing

    template = read("templates", "sdd-routing.md")
    parsed = routing.parse(template)
    assert parsed is not None, "the template no longer parses as a declaration"
    assert parsed["review"] == routing.CHAIN
    assert parsed["destination"] == routing.OPEN_PR

    # Shipped as a PLACEHOLDER, unlike the other two, and that is the whole
    # point: a wrong answer in the first two is caught at the next commit
    # because the gate stops recognising the file, and a wrong answer here is
    # never contradicted by anything. So copy-and-never-revisit has to land on
    # "not answered" rather than on a confident `smith` nobody performed.
    assert parsed["implementation"] is None, (
        "the template pre-answers the one axis nothing checks, which makes "
        "the commonest mistake produce a WRONG record instead of no record"
    )
    # Round 2: `is None` is satisfied by an empty cell and by `TBD`, and both
    # were green. `parse()` cannot tell them apart -- all three are outside
    # the vocabulary -- but a PERSON can, and the person is who the
    # placeholder is for. An empty cell reads as "nothing to fill in"; `TBD`
    # reads as an answer somebody will get to. Only the shipped text says
    # what the two choices are.
    assert "| Implementation | <smith, or: the session> |" in template, (
        "the placeholder TEXT is the half a person reads, and a blank cell "
        "or `TBD` parses identically while reading as answered"
    )

    # The label, which the placeholder cannot exercise. Substituting each
    # documented answer must yield that answer -- `| Implementor | … |` or a
    # backticked value reads as unanswered forever, silently, in every work
    # item that copies this file.
    rows = [ln for ln in template.splitlines() if ln.startswith("| Implementation |")]
    assert len(rows) == 1, "the template has no single `Implementation` row"
    for answer in routing.IMPLEMENTATION_ANSWERS:
        filled = template.replace(rows[0], f"| Implementation | {answer} |")
        assert routing.parse(filled)["implementation"] == answer, (
            f"the template's row does not accept `{answer}`, so a session "
            "filling it in as instructed still records nothing"
        )


def test_no_committed_declaration_still_carries_a_template_placeholder():
    """Round 2: nothing reads the third axis, so nothing reports a work item
    that copied the template and never filled the row in.

    The `Branch` row is the contrast that shows this is a real gap rather
    than a tidy one: leaving ITS placeholder produces a branch name nothing
    matches, `for_branch` finds no declaration, and the gate asks again at
    the next commit. The third axis has no such reader, so the placeholder
    would sit in the record forever, reading to a person as an answer."""
    import glob

    for path in sorted(
        glob.glob(os.path.join(ROOT, "seal", "specs", "*", "routing.md"))
    ):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if not line.startswith("|"):
                    continue
                label, _, value = line.strip().strip("|").partition("|")
                assert not value.strip().startswith("<"), (
                    f"{os.path.relpath(path, ROOT)} still carries the "
                    f"template placeholder for `{label.strip()}`"
                )


def test_the_skill_states_all_four_combinations():
    """Four rows, because two of them are the ones that surprise people: a
    chain declaration that never opens a pull request is checked by nothing."""
    skill = read(*ORCH)
    rows = [
        ln
        for ln in skill.splitlines()
        if ln.startswith("| chain") or ln.startswith("| direct")
    ]
    assert len(rows) == 4, f"expected four combinations, found {len(rows)}"
    assert any("nothing runs" in r for r in rows), (
        "the combination nothing checks has to be the one stated outright"
    )


def test_the_skill_names_where_the_answer_is_written():
    skill = flat(read(*ORCH))
    assert "seal/specs/<work-item-id>/routing.md" in skill
    assert "templates/sdd-routing.md" in skill
    assert "Committed" in skill or "committed" in skill


def test_the_skill_keeps_the_token_as_a_per_command_waiver():
    """The two are independent, and coupling them would ask for one answer
    twice — then stop a session for not repeating itself."""
    skill = flat(read("skills", "implement", "SKILL.md"))
    assert "waives **one command**" in skill
    assert "routes **a work item**" in skill


def test_the_row_that_said_no_marker_at_all_is_gone():
    """It is the defect stated as a sentence, and rewording it would have left
    the same claim in place."""
    skill = read(*ORCH)
    assert 'used to carry "no marker at all"' in skill, (
        "the skill dropped the correction rather than making it — the next "
        "reader cannot tell the old row was wrong"
    )
    for text in (skill, read(*SKILL)):
        assert "| Through the review chain | it needs no marker at all" not in text


def test_the_skill_refuses_a_standing_waiver_and_says_why_this_is_not_one():
    """The cheap way to stop the interruptions is to switch the gate off for a
    session, and it is the one way that costs the gate its reason to exist."""
    skill = flat(read(*ORCH))
    assert "What must not happen instead is a standing waiver" in skill
    assert "moves the check rather than removing it" in skill, (
        "without this the declaration reads as exactly the switch the sentence "
        "above it forbids"
    )
    spec = flat(read("docs", "review-chain-spec.md"))
    assert "no standing waiver" in spec
    assert "per command" in spec


def test_the_gate_has_no_path_from_an_unreadable_declaration_to_silence():
    spec = flat(read("docs", "review-chain-spec.md"))
    assert "resolves to *no declaration*" in spec
    assert "therefore to **asking**" in spec, (
        "a fail-open here is a gate that a corrupt file switches off"
    )


def test_the_session_runs_to_the_pull_request():
    skill = read("skills", "implement", "SKILL.md")
    assert "the session runs to the pull request" in skill
    for destination in ("questions.md", "seal/follow-up.md", "Not done"):
        assert destination in skill, (
            f"the skill lost `{destination}` as somewhere a late finding goes"
        )
    assert "would a different\nanswer change what you build" in skill, (
        "the test separating a question from a row is the operative part"
    )


def test_the_smith_carries_both_halves_rather_than_only_citing_them():
    """The agent file is always in front of the smith; the skill may not be."""
    smith = flat(read("agents", "smith.md"))
    assert "three axes" in smith and "two axes" not in smith
    for answer in AXES:
        assert answer in smith, f"the smith lost the answer `{answer}`"
    assert "seal/specs/<work-item-id>/routing.md" in smith
    assert "run to the pull request" in smith
    assert "answerer" in smith, (
        "a deferral with nobody named is how a follow-up becomes nobody's"
    )


def test_the_preset_block_carries_it_too():
    """`CLAUDE.md` is the one file a session in this repository always has."""
    preset = flat(read("CLAUDE.md"))
    assert "seal/specs/<work-item-id>/routing.md" in preset
    for answer in AXES:
        assert answer in preset, f"the preset block lost `{answer}`"


def test_the_template_ships_the_vocabulary_the_parser_accepts():
    """A template offering words the reader rejects produces a declaration
    that reads as none, which is what a branch that never declared looks
    like."""
    tpl = read("templates", "sdd-routing.md")
    routing = read("hooks", "routing.py")
    for answer in AXES:
        assert answer in tpl, f"the template lost `{answer}`"
        assert f'"{answer}"' in routing, f"the parser does not accept `{answer}`"
