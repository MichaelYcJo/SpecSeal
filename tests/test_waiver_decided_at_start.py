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
import re

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


def checkbox_tables(text):
    """Every table of boxes in `text`, as a list of its body rows.

    Found by the header naming a box rather than by position, because the
    question's shape is what changes and a reader looking for `| Checkbox |`
    exactly once is a reader that finds nothing the day it becomes two
    questions. What stays true across every shape is that a table of boxes
    has a column named for one.
    """
    lines = text.splitlines()
    tables = []
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        header = [c.strip() for c in line.strip("|").split("|")]
        if not any(c in ("Checkbox", "Box") for c in header):
            continue
        rows = []
        for body in lines[i + 2 :]:
            if not body.startswith("|"):
                break
            rows.append(body)
        tables.append(rows)
    return tables


def test_the_skill_asks_the_whole_question_in_the_first_batch():
    """The count moved twice and each time a stale copy survived the edit.

    It was `two axes`, then `three axes`, and now it is neither: the question
    is two questions in one call, and the boxes number four. What this case
    pins is the SHAPE — the one call, the four answers a box can write, and
    the moment — plus the absence of every count the shape has outgrown.

    The absence half is the half that would have caught this edit. The three
    stale `three axes` copies were green under the old presence-only
    assertion, because the string it required was the stale copy itself: the
    orchestrator's own summary line, `skills/implement/SKILL.md`'s pointer
    sentence and `agents/smith.md`'s phase 2. A count asserted by presence
    passes on the copy that should have moved.
    """
    skill = flat(read(*ORCH))
    assert "two questions" in skill, (
        "the section stopped naming its own shape, so a session reads a "
        "question whose number of questions is nowhere stated"
    )
    assert "ONE `AskUserQuestion` call" in skill, (
        "the one-call sentence went, and two questions in two calls is two "
        "waits — which is the whole thing the batch rule forbids"
    )
    for stale in ("two axes", "three axes", "three checkboxes"):
        assert stale not in skill + flat(read(*SKILL)), (
            f"`{stale}` survived the rewrite; a count the shape outgrew reads "
            "as the shape"
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
    # `agents/smith.md` used to state the same axis in prose, because it used
    # to ask the question. It does not any more — the act is the framer's, and
    # the vocabulary travels with the act. Asserting the answers here again
    # would put the moved rule back in the definition it left, which is what
    # `tests/test_a_moved_rule_leaves_its_definition.py` exists to refuse.
    smith = flat(read("agents", "smith.md"))
    assert "implementation (smith · the session" not in smith, (
        "the routing vocabulary is back in `agents/smith.md`, whose phase 2 "
        "no longer asks the question it belongs to"
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


def test_the_template_PARSES_into_the_FOURTH_axis_it_ships():
    """The fourth axis's vocabulary is read out of the template, never retyped.

    `hooks/routing.py`'s `parse()` docstring promises that
    `templates/sdd-routing.md` is the only spelling a session should copy and
    that a test parses the file so the two cannot drift. This is that test for
    the `Planning` row: every constant the parser accepts is substituted into
    the template's own row and parsed back, so a row labelled `Planner` or a
    vocabulary that moved in one file only is red here rather than silent in
    every work item that copies the file.

    Shipped as a placeholder for the reason the third axis is: nothing
    contradicts a wrong answer in either, so copy-and-never-revisit has to land
    on "not answered".
    """
    import sys

    sys.path.insert(0, os.path.join(ROOT, "hooks"))
    import routing

    template = read("templates", "sdd-routing.md")
    parsed = routing.parse(template)
    assert parsed is not None, "the template no longer parses as a declaration"
    assert parsed["planning"] is None, (
        "the template pre-answers the fourth axis, which makes the commonest "
        "mistake produce a WRONG record instead of no record"
    )
    assert "| Planning | <framer, or: the session> |" in template, (
        "the placeholder TEXT is the half a person reads, and a blank cell or "
        "`TBD` parses identically while reading as answered"
    )

    rows = [ln for ln in template.splitlines() if ln.startswith("| Planning |")]
    assert len(rows) == 1, "the template has no single `Planning` row"
    for answer in routing.PLANNING_ANSWERS:
        filled = template.replace(rows[0], f"| Planning | {answer} |")
        assert routing.parse(filled)["planning"] == answer, (
            f"the template's row does not accept `{answer}`, so a session "
            "filling it in as instructed still records nothing"
        )
    # The vocabulary is READ OUT of the template and compared, rather than
    # each constant being looked for inside it. Substituting the constants
    # into the row above is self-consistent by construction -- rename
    # `BY_FRAMER` and the substitution renames with it -- so on its own it
    # cannot see the two files drift apart. This direction can: the answers
    # the comment offers a person have to BE the answers the parser accepts.
    import re

    stated = re.search(r"Planning — `([^`]+)` or `([^`]+)`\.", template)
    assert stated, (
        "the comment no longer states the fourth axis's two answers, so the "
        "only thing a person reads is the placeholder"
    )
    assert tuple(stated.groups()) == routing.PLANNING_ANSWERS, (
        f"the template offers {stated.groups()} and the parser accepts "
        f"{routing.PLANNING_ANSWERS}; a session filling the row in as "
        "instructed would record nothing"
    )

    # The row inherits the third axis's terms rather than restating them, so
    # the comment has to SEND a reader there. Without this the row ships with
    # no account of why an absent answer is not a defect.
    tpl = flat(template)
    assert "on exactly the terms the `Implementation` row" in tpl, (
        "the fourth axis stopped pointing at the row whose terms it borrows, "
        "so its own optionality is unexplained"
    )


def test_the_template_PARSES_into_the_TWO_NEWEST_rows_it_ships():
    """The fifth and sixth rows, on the terms the third and fourth have.

    `Automation` is a property of the run and `Answer pressed` is which of
    question 1's options was pressed. Both are read out of the template and
    parsed back, so a row labelled `Automated` or a vocabulary that moved in
    one file only is red here rather than silent in every work item that
    copies the file.

    Shipped as placeholders, and for this pair the reason is sharper than for
    the two above. An absent `Automation` row means nobody was ever asked; a
    pre-answered one means a question nobody put reads as a promise somebody
    made. That is #151's shape, which is the thing the row exists to end.
    """
    import sys

    sys.path.insert(0, os.path.join(ROOT, "hooks"))
    import routing

    template = read("templates", "sdd-routing.md")
    parsed = routing.parse(template)
    assert parsed is not None, "the template no longer parses as a declaration"
    for key in ("automation", "pressed"):
        assert parsed[key] is None, (
            f"the template pre-answers `{key}`, which makes the commonest "
            "mistake produce a WRONG record instead of no record"
        )
    for label, answers in (
        (routing.AUTOMATION, routing.AUTOMATION_ANSWERS),
        (routing.ANSWER_PRESSED, routing.ANSWER_PRESSED_ANSWERS),
    ):
        rows = [ln for ln in template.splitlines() if ln.startswith(f"| {label} |")]
        assert len(rows) == 1, f"the template has no single `{label}` row"
        assert rows[0].split("|")[2].strip().startswith("<"), (
            f"the `{label}` row stopped shipping a placeholder a person reads"
        )
        key = "automation" if label == routing.AUTOMATION else "pressed"
        for answer in answers:
            filled = template.replace(rows[0], f"| {label} | {answer} |")
            assert routing.parse(filled)[key] == answer, (
                f"the template's `{label}` row does not accept `{answer}`, so "
                "a session filling it in as instructed still records nothing"
            )
        # The vocabulary READ OUT of the comment, the direction that can see
        # the two files drift. Substituting the constants is self-consistent
        # by construction; what the person reads has to BE what the parser
        # takes.
        stated = re.search(rf"{label} — `([^`]+)` or `([^`]+)`\.", template)
        assert stated, f"the comment no longer states `{label}`'s two answers"
        assert tuple(stated.groups()) == answers, (
            f"the template offers {stated.groups()} for `{label}` and the "
            f"parser accepts {answers}"
        )


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def labelled_table(text, first_column, second_column):
    """The body rows of the table whose header is exactly those two columns.

    Question 1 is `| Order | Label | Description |` and question 2 is
    `| Order | Box | Checked | Not checked |`, so the pair names one of them
    without either being found by position in the file.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        header = cells(line)
        if header[:2] != [first_column, second_column]:
            continue
        rows = []
        for body in lines[i + 2 :]:
            if not body.startswith("|"):
                break
            rows.append(cells(body))
        return rows
    raise AssertionError(f"no table headed `| {first_column} | {second_column} |`")


def test_the_question_is_two_questions_in_one_call():
    """S1. One batch before the first edit is one WAIT, not one question.

    Two `AskUserQuestion` calls is two waits and the batch rule is broken by
    the second one, whatever either call contains. So the two tables have to
    be there AND the sentence that they go in one call.
    """
    skill = read(*ORCH)
    assert len(labelled_table(skill, "Order", "Label")) == 3, (
        "question 1 does not offer exactly three options"
    )
    assert len(labelled_table(skill, "Order", "Box")) == 4, (
        "question 2 does not offer exactly four boxes"
    )
    # ONE spelling, shared with `templates/claude-md-block.md` and its
    # generated copy, because `tests/test_review_axes.py` pairs the two
    # documents on this exact phrase — two spellings of one decision is
    # the drift that pair exists to catch.
    assert "two questions in ONE `AskUserQuestion` call" in flat(skill)


def test_the_boxes_are_in_the_stated_order():
    """S5. The first box is a property of the run; the three below name
    parties, in the order they run.

    Asserted as an ORDER rather than as a membership, because the defect it
    guards against is positional: a reader meeting four boxes of apparently
    the same kind reads the first as a fourth party to switch on. Swap the
    first two rows and the boxes are all still present.
    """
    rows = labelled_table(read(*ORCH), "Order", "Box")
    boxes = [r[1] for r in rows]
    assert "run end to end" in boxes[0], (
        f"the property-of-the-run box is at position {boxes.index(next(b for b in boxes if 'run end to end' in b)) + 1}, "
        "not first. The order is the specification: a party box read first "
        "makes the run's own property look like a fifth party"
    )
    for i, party in enumerate(("smith", "warden", "pull request"), start=1):
        assert party in boxes[i], (
            f"box {i + 1} is `{boxes[i]}`; the three party boxes follow the "
            "run's property in the order they run"
        )
    assert "the order is the specification" in flat(read(*ORCH)).lower(), (
        "nothing says the order is load-bearing, so the next edit reorders it"
    )


def test_every_box_states_what_UNCHECKED_means():
    """S6. The half a label cannot say, and the half the measured instance
    got wrong — the owner read `straight to the PR` as *call no agents at
    all*, where it turns off `warden` alone.

    Each phrase is asserted in the box it belongs to rather than anywhere in
    the file, because a document can carry all four words in prose two
    sections down while the box a person reads at the moment of answering
    carries none of them.
    """
    rows = labelled_table(read(*ORCH), "Order", "Box")
    unchecked = {r[1]: r[3] for r in rows}
    wanted = {
        "run end to end": "may be asked",
        "smith": "this session writes the code",
        "warden": "nothing reviews",
        "pull request": "stop before",
    }
    for box, phrase in wanted.items():
        found = [v for k, v in unchecked.items() if box in k]
        assert found, f"no box named for `{box}`"
        assert phrase in found[0], (
            f"the `{box}` box's unchecked half does not say `{phrase}`; a "
            "person answering reads the label and this cell and nothing else"
        )


def test_the_exit_names_what_does_not_run_rather_than_where_it_ends():
    """S4. The rule the measured instance produced: a label must name what it
    turns off, not where it ends.

    So the exit's label carries no destination, and its description names the
    five things that do not happen. `straight to the PR` is the counter-example
    and it stays in the tree — as the `Review` row's value, which is machine
    vocabulary 16 committed declarations carry. What moved is the LABEL.
    """
    rows = labelled_table(read(*ORCH), "Order", "Label")
    exits = [r for r in rows if "no work item" in r[1]]
    assert exits, "question 1 has no exit option labelled `no work item`"
    label, description = exits[0][1], exits[0][2]
    for destination in ("the PR", "pull request"):
        assert destination not in label, (
            f"the exit's label names a destination (`{label}`), which is the "
            "defect the measured instance is an instance of"
        )
    for noun in ("no frame", "no review", "no seal", "no `routing.md`", "[no-review]"):
        assert noun in description, (
            f"the exit's description does not name `{noun}`, so a person "
            "pressing it cannot see what they are turning off"
        )
    assert rows[-1][1] == label, (
        "the exit is not last. It is one click and the least-verified path, "
        "so it sits where a reader's eye lands last"
    )


def test_the_ceiling_is_stated_beside_the_shape():
    """S7. The next person meets the constraint instead of discovering it.

    All three halves: the cap, where the room came from, and that a fifth
    breaks the shape. The third is the one that matters — a cap stated
    without it reads as a limit somebody could raise.
    """
    skill = flat(read(*ORCH))
    assert "at most four options per question" in skill, "the cap is unstated"
    assert "taking the framer and the sealer out of the question" in skill, (
        "nothing says where the room for the fourth box came from, so the "
        "next person reads two empty slots"
    )
    assert "a fifth box breaks this shape" in skill, (
        "the cap reads as a limit somebody could raise"
    )


def test_the_preset_and_the_boxes_are_told_apart_in_the_file():
    """S2 and S3 at the document. Both write the same party rows; the row
    that says which answer was pressed is the only difference.

    Without that row the preset buys nothing — a chosen answer goes back to
    being indistinguishable from a question nobody read, which is #151.
    """
    skill = flat(read(*ORCH))
    for derivation in (
        "`Answer pressed` = `automation`",
        "`Answer pressed` =\n`per axis`",
    ):
        assert flat(derivation) in skill, (
            f"the section does not say the preset writes {flat(derivation)}, "
            "so a session has the row and no rule for filling it"
        )
    assert "same bytes" in skill, (
        "the section states the row without the reason, so the next edit "
        "reads it as bookkeeping and drops it"
    )
    rows = [ln for ln in read(*ORCH).splitlines() if ln.startswith("| Automation |")]
    assert len(rows) == 1, (
        f"the section has {len(rows)} `Automation` rows; the declaration has one"
    )
    assert "yes · no" in rows[0], "the row lost its vocabulary"
    assert "OPTIONAL" in rows[0], "the row stopped saying an absent answer is fine"


FRAMER = ("agents", "framer.md")


def test_the_framer_asks_nobody_and_writes_no_declaration():
    """S10, after round 1 reversed WHERE the act lands.

    **A subagent in this harness has no `AskUserQuestion` and no equivalent.**
    Measured from two agents independently — `warden` during round 1 and
    `smith` during its fix pass — each of which, like the framer, declares no
    `tools:` key and inherits the full set: the tool is not in the list and
    `ToolSearch` for it returns `No matching deferred tools found`. So the
    build's first answer told an agent to call a tool it does not have, which
    is the class this repository keeps finding.

    #419's finding survives intact: the acts are not `smith`'s. What was wrong
    is only where they were sent. They go to the SESSION that spawns the work,
    which has the tool and is already the party that spawns, approves and
    reads back.

    Asserted as an absence AND a presence. The absence alone would pass on a
    definition that says nothing at all about routing, which is the state that
    lets a framer write a declaration from a guess — a recorded answer nobody
    gave, which is #151's shape arriving through the door this work opened.
    """
    framer = flat(read(*FRAMER))
    assert "You have no interactive phase" in framer, (
        "the framer's definition no longer says it asks nobody, so the next "
        "reader restores an interactive phase the harness cannot give it"
    )
    assert "has no `AskUserQuestion`" in framer, (
        "the reason went. Without it the instruction reads as a preference "
        "somebody can reverse, and the measurement is what makes it not one"
    )
    assert "`routing.md` is not one of them" in framer, (
        "`routing.md` is back among the framer's writes, and a framer that "
        "cannot ask can only write it from a guess"
    )
    assert "a thing to report,\nnever a thing to write" in read(*FRAMER), (
        "the framer meeting a missing declaration has no instruction, so the "
        "obvious repair is the one that records an answer nobody gave"
    )
    for claimed in (
        "The routing question is in that batch, and it is yours to ask",
        "Yours is the one interactive phase",
    ):
        assert claimed not in framer, (
            f"`{claimed}` is back in `agents/framer.md`, which hands a "
            "subagent an act the harness gives it no tool for"
        )


def test_no_agent_definition_tells_an_agent_to_ask_a_person():
    """The class behind 🟡 4, pinned by the one name that was measured.

    An agent definition instructing an agent to call a tool it cannot reach is
    exactly what went undetected here: the build moved the routing batch to
    `agents/framer.md`, every case stayed green, and nothing in the tree could
    see that the instruction was unperformable.

    **This is one name, not a vocabulary.** A sweep over `agents/*.md` for
    every tool an agent cannot reach needs a list of what each agent has, kept
    in step with the harness — that is mechanism, which a fix pass may not add
    (`skills/code-review/orchestration.md` §*A fix pass adds the unit that
    pins it*), and it is handed over as a ticket instead. What this case holds
    is the measured instance and the glob: a fourth agent definition added
    tomorrow is checked on the day it lands.
    """
    import glob

    definitions = sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))
    assert len(definitions) >= 3, f"agents/*.md matched {len(definitions)} files"
    for path in definitions:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        name = os.path.relpath(path, ROOT)
        for line in text.splitlines():
            if "AskUserQuestion" not in line:
                continue
            # Naming the tool to say it is ABSENT is the whole repair, so the
            # sentence that does it has to be allowed. What is refused is an
            # instruction to use it.
            # ONE spelling across every definition, deliberately. A marker
            # list that grows a phrase per file is a list that stops being a
            # check, so a definition saying the tool is absent says it this
            # way — and the case is what keeps the four sentences in step.
            assert "no `AskUserQuestion`" in line, (
                f"{name} names `AskUserQuestion` outside the sentence that "
                "says an agent does not have it. No agent this plugin spawns "
                "can reach that tool, so an instruction to use it is an "
                "instruction nothing can carry out"
            )


def test_the_framers_acts_are_gather_judge_plan():
    """S11. Judging was in none of the four acts, and both framers spawned in
    the release that found this judged anyway, because the spawn prompt asked.

    A definition that describes collecting and not deciding rewards a framer
    for stopping people. The act is named, and the grounds requirement rides
    with it — a judgment whose grounds nobody can open is not reviewable.
    """
    framer = flat(read(*FRAMER))
    assert "Gather, judge, plan" in framer, (
        "the three acts went. `judge` is the one that was missing, and its "
        "absence is what made deciding well an unrewarded act"
    )
    assert "A reader and a writer" not in framer, (
        "the old persona survived beside the new one, so a framer reads "
        "whichever it reaches first"
    )
    assert "grounds written where a reviewer can open them" in framer, (
        "judging arrived without the requirement that makes it checkable"
    )


def test_questions_md_is_the_residue_and_every_row_says_why():
    """S11's second half. What changes is not that `questions.md` goes, but
    what belongs in it: the residue after judging, never a collection.

    The reason cell is what makes the difference visible. Without it a row a
    framer never tried to answer and a row the tree genuinely cannot answer
    are the same row, and both cost a person the same interruption.
    """
    framer = flat(read(*FRAMER))
    assert "is the residue, not a collection" in framer
    assert "owes a reason the tree could not answer it" in framer, (
        "a row may again arrive with no account of why judging did not settle "
        "it, which is the collection this act replaced"
    )


def test_the_framer_leaves_a_mark_in_the_tree():
    """S12. Measured at the frame: 0 of 84 work items carry any mark in
    `spec.md`, and the definition asked for none.

    `smith` leaves a mark and `warden` writes round records, so the framer was
    the only party in the chain whose work left no evidence that it happened —
    only a claim in a row somebody typed. The existing framer mark is in the
    repository's git dir, and a git dir does not travel, so the check at the
    pull request cannot read it.

    Both ends are asserted: the definition that tells a framer to write it and
    the template a session copies. Either alone ships a mark nobody writes or
    a line nobody was told to fill in.
    """
    line = "Framed <date> by <who>, before the build."
    template = read("templates", "sdd-spec.md")
    assert line in template, (
        "`templates/sdd-spec.md` ships no mark, so every spec copied from it "
        "is a frame with no evidence it was framed"
    )
    assert template.rstrip().endswith(line), (
        "the mark is not at the foot of the file; the check reads the same "
        "shape `routing.md` and `plan.md` already end with"
    )
    framer = flat(read(*FRAMER))
    assert line in framer, (
        "the framer is not told to write the mark, so the template's line "
        "survives into the committed spec as a placeholder"
    )
    assert "a git dir does not travel" in framer, (
        "the mark arrives with no account of why the existing one does not do, "
        "which is the first thing an editor will ask"
    )


def test_the_planning_row_is_a_record_and_not_a_checkbox():
    """#88, cited rather than re-argued: the question grows only where a
    decision is genuinely a person's, and `agents/framer.md`'s `## When you
    run` says the SDD ladder decides this one.

    Both halves are asserted, because either alone passes over the state that
    matters. The row has to be IN the orchestrator's routing section — an axis
    nobody documents is a template row a session meets with no account of it —
    and it must not appear among the boxes.

    **Renamed and rewritten from
    `test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox`, which named
    `Planning` by POSITION and counted the boxes.** Both spellings stopped
    being about `Planning` the moment a row was added: the declaration's
    fourth row is not `Planning` any more, and the question's box count is
    four because one of the new rows genuinely IS a person's decision — which
    is what #88's rule permits rather than what it forbids. The rule was
    always about this row and never about a number, so the assertions are
    over the row's NAME. A count here would have gone red at the next phase
    for a change the rule allows, and a reader would have read that red as
    the rule being broken.
    """
    skill = read(*ORCH)
    rows = [ln for ln in skill.splitlines() if ln.startswith("| Planning |")]
    assert len(rows) == 1, (
        f"the routing section has {len(rows)} `Planning` rows; the declaration "
        "has exactly one"
    )
    assert "framer · the session" in rows[0], (
        "the row lost the vocabulary, so a session reads an axis with no answers"
    )
    assert "OPTIONAL" in rows[0], "the row stopped saying an absent answer is fine"

    for boxes in checkbox_tables(skill):
        assert not any("framer" in b or "Planning" in b for b in boxes), (
            "the `Planning` axis reached a checkbox table, which is the one "
            "place #88 says it must not be"
        )
    assert "#88" in skill, (
        "the section asserts the rule without citing where it is stated, so a "
        "reader who disagrees has nothing to open"
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


def test_the_smith_carries_its_own_half_and_not_the_questions():
    """The agent file is always in front of the smith; the skill may not be.

    **What its own half IS moved, which is why this case is rewritten rather
    than deleted.** It used to carry the routing question's whole vocabulary,
    because it used to ask it — three axes, the four answers, the path it
    wrote them to. That act is the framer's now, and a definition that keeps
    the words of an act it no longer performs is a session's instruction to
    perform it.

    What stays is what a smith still does with the answer somebody else
    wrote: run to the pull request without coming back, and name an answerer
    for anything it could not close.
    """
    smith = flat(read("agents", "smith.md"))
    assert "run to the pull request" in smith
    assert "answerer" in smith, (
        "a deferral with nobody named is how a follow-up becomes nobody's"
    )
    for count in ("three axes", "two axes", "three checkboxes"):
        assert count not in smith, (
            f"`{count}` is back in `agents/smith.md`, which is the routing "
            "question in the definition of the party that does not ask it"
        )


def test_the_preset_block_carries_it_too():
    """`CLAUDE.md` is the one file a session in this repository always has.

    So it is the copy that matters most, and round 1 measured it as the copy
    nothing held: the block kept its old three-checkbox paragraph and 176
    cases stayed green, `claude_block.py --check` included — that command
    compares the template with its generated copy and neither with the
    question. Most of what this work item distributes IS this paragraph.

    Asserted at BOTH ends, template and generated copy, and the absence half
    is the half that would have caught it. This is the same defect the build
    repaired one file over — a presence assertion on a count passing on the
    copy that should have moved — landing on the copy a session always has.
    """
    for parts in (("templates", "claude-md-block.md"), ("CLAUDE.md",)):
        text = flat(read(*parts))
        where = "/".join(parts)
        assert "seal/specs/<work-item-id>/routing.md" in text, where
        for answer in AXES:
            assert answer in text, f"{where} lost the answer `{answer}`"
        assert "two questions in ONE `AskUserQuestion` call" in text, (
            f"{where} still asks the old question, and the block is what a "
            "session in an opted-in repository always has in front of it"
        )
        for stale in ("two axes", "three axes", "three checkboxes"):
            assert stale not in text, (
                f"`{stale}` survived in {where}, so every session reads the "
                "shape the rest of the repository stopped describing"
            )


def test_the_template_ships_the_vocabulary_the_parser_accepts():
    """A template offering words the reader rejects produces a declaration
    that reads as none, which is what a branch that never declared looks
    like."""
    tpl = read("templates", "sdd-routing.md")
    routing = read("hooks", "routing.py")
    for answer in AXES:
        assert answer in tpl, f"the template lost `{answer}`"
        assert f'"{answer}"' in routing, f"the parser does not accept `{answer}`"
