"""A fix pass may add a unit. That unit's fix may not.

By construction a fix ships reviewed and the unit it added to pin it ships
unreviewed, in the same commit, so the next round's finding lands in the unit
rather than in the fix. Measured across four rounds of #82, three consecutive
rounds found their finding inside the previous round's fixes — round 1's
`configured_language` and templates check both reproduced the defect they
closed, round 2's widened glob went out of step with its corpus, and round 3's
`ROUND_RECORD_FIELDS` was a list hand-copied from the file it is checked
against.

The stopping floor (`tests/test_the_run_stops_at_the_last_finding.py`) is what
turns the bound from tidy into required: the rounds it removes are the rounds
that were reading those units, so shipping the floor alone cuts the eyes and
leaves the generation.

**The exit is pinned by position, not only by presence.** A rule that refuses
without naming where the refused work goes stops the chain at a wall, and the
two files that state the rule to a session state the exit before it. That
ordering is what `test_the_exit_is_stated_before_the_rule` reads, and it is why
the sections are sliced rather than searched whole: the same exit sentence
appears earlier in `skills/code-review/SKILL.md` under the floor, so a
whole-file search would be satisfied by a sentence that is not the one this
case is about.

`templates/sdd-round.md` is checked for presence only. It is a form to copy
rather than an argument to follow, and its own reading order — what the row
holds, then what is refused, then where the refusal goes — is the right one
for a template.
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SKILL = ("skills", "code-review", "SKILL.md")
SMITH = ("agents", "smith.md")
TEMPLATE = ("templates", "sdd-round.md")

RULE = "A fix pass may add a unit. That unit's fix may not."
EXIT = "deferred with a named answerer, or becomes an issue"
SHAPE = "unit (depth N)"

# The two files that state the rule to a session that is about to act on it.
# The template is a form, and is checked for presence alone.
STATES_THE_RULE = (SKILL, SMITH)

# Each file's rule section, bounded by text that was in the file BEFORE this
# rule landed, so the slice is defined by the document rather than by the
# sentence under test.
SECTION = {
    SKILL: ("### A fix pass adds the unit that pins it", "### Then say who checked"),
    SMITH: ("the way out is the verifying round above", "What is unresolved at that"),
}


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(*parts).split())


def section(parts):
    """The slice of the file that states the rule."""
    text = flat(*parts)
    opening, closing = SECTION[parts]
    assert opening in text, f"{'/'.join(parts)}: the section opening moved: {opening!r}"
    assert closing in text, f"{'/'.join(parts)}: the section closing moved: {closing!r}"
    start = text.index(opening)
    return text[start : text.index(closing, start)]


# --- the rule, in the three files -------------------------------------------


def test_all_three_files_state_the_rule():
    """#117's sentence, verbatim in each. It reached three files in three
    spellings on the first draft — a semicolon here, a lower-cased clause
    there — and a rule a reader has to recognise across paraphrases is a rule
    a checker cannot find at all."""
    for parts in (SKILL, SMITH, TEMPLATE):
        assert RULE in flat(*parts), (
            f"{'/'.join(parts)} does not state the depth bound, so a fix pass "
            "reading that file is told nothing about what it may create"
        )


def test_the_exit_is_named_in_the_section_that_states_the_rule():
    """Presence, in the slice rather than the file. `skills/code-review/
    SKILL.md` carries this same sentence under the floor as well, and a
    whole-file search would pass on that one while this section named no exit
    at all."""
    for parts in STATES_THE_RULE:
        assert EXIT in section(parts), (
            f"{'/'.join(parts)} refuses a second-level unit without naming "
            "where it goes instead, which stops the chain at a wall"
        )
    assert EXIT in flat(*TEMPLATE), (
        "templates/sdd-round.md describes the depth without saying what "
        "becomes of a unit the depth refuses"
    )


def test_the_exit_is_stated_before_the_rule():
    """The ordering `plan.md` calls the point rather than convenience.

    A session meets the refusal in the order the file is written, and one that
    meets it before the exit has to go looking for somewhere to put work it has
    just been told it may not do. Presence alone cannot see that, which is why
    this is a position case.
    """
    for parts in STATES_THE_RULE:
        text = section(parts)
        assert text.index(EXIT) < text.index(RULE), (
            f"{'/'.join(parts)} states the depth bound before it states the "
            "exit, so a session meets a refusal with nowhere to put the work"
        )


def test_the_section_slice_is_narrower_than_the_file():
    """`section()` is what keeps the case above honest, so it is pinned rather
    than trusted.

    Degrade it to the whole file and the `skills/code-review/SKILL.md` half of
    the ordering case passes on the floor's exit sentence — a different
    sentence, in a different section, that happens to sit before the rule. The
    case would then be green while saying nothing, which is the shape this
    repository calls a counterfeit seal.
    """
    for parts in STATES_THE_RULE:
        whole, sliced = flat(*parts), section(parts)
        assert sliced, f"{'/'.join(parts)}: the section sliced to nothing"
        assert sliced in whole, f"{'/'.join(parts)}: the slice is not of the file"
        assert len(sliced) < len(whole), (
            f"{'/'.join(parts)}: the section is the whole file, so every "
            "case reading it is answered by text from some other section"
        )
        assert SECTION[parts][1] not in sliced, (
            f"{'/'.join(parts)}: the slice runs past its own closing marker"
        )
    assert flat(*SKILL).count(EXIT) >= 2, (
        "the exit sentence appears once in `skills/code-review/SKILL.md`, so "
        "either the floor or the depth bound is now borrowing the other's, "
        "and one of the two sections refuses without an exit of its own"
    )


# --- the row that carries it ------------------------------------------------


def test_the_new_units_row_carries_the_depth():
    """The row named the units and nothing else, which is what let a
    second-level unit ship without anybody able to see that it was one."""
    row = next(
        line
        for line in read(*TEMPLATE).splitlines()
        if line.startswith("| New units |")
    )
    assert SHAPE in row, (
        f"the `New units` row does not carry the entry shape {SHAPE!r}, so the "
        f"depth has nowhere to be written: {row}"
    )
    assert "separated by `;`" in row, (
        "the row does not say how entries are separated, which is the one "
        "thing a session has to guess right for the row to be readable"
    )


def test_the_skills_fix_surface_table_names_the_depth():
    """🟡 4 of round 1. `skills/code-review/SKILL.md` says the depth once, in
    the section that argues for the rule, and again — differently — in the
    table a session actually opens to fill the cell in. The table said the
    row holds the units and nothing more, so a session following it writes a
    cell the checker refuses."""
    row = next(
        line for line in read(*SKILL).splitlines() if line.startswith("| `New units` |")
    )
    for needle in ("depth", "`;`"):
        assert needle in row, (
            f"the fix-surface table's `New units` row offers no `{needle}`, "
            f"so the file gives two answers about one cell: {row}"
        )


def test_the_template_shows_a_form_a_session_can_copy():
    """A shape described in a sentence and never shown is a shape every
    session spells differently."""
    text = flat(*TEMPLATE)
    assert (
        "| New units | configured_language (depth 1); mirror_to_refuse (depth 1) |"
        in text
    ), (
        "the comment below the field table does not show a filled-in `New "
        "units` cell, so the entry shape exists only as a description"
    )


def test_none_survives_the_depth():
    """`none` was an answer before the depth arrived, with or without a reason
    after it, and a row that now demands `(depth N)` of every entry must not
    have taken that away — `none — the fixes are not yet written` is the honest
    value while a round is still running."""
    text = flat(*TEMPLATE)
    assert "| New units | none |" in text, (
        "the depth swallowed the bare `none`, which is the value a round with "
        "no fixes yet has to be able to write"
    )
    assert "| New units | none — the fixes are not yet written |" in text, (
        "the depth swallowed `none` with a reason after it"
    )


def test_the_depth_did_not_become_a_row_of_its_own():
    """The absence half, and `plan.md`'s Alternatives table is its grounds: a
    single fix pass can answer a finding in code that predates the run and a
    finding inside an earlier unit at once, so one number for the round cannot
    be true of both."""
    text = flat(*TEMPLATE)
    assert "| Fix depth |" not in text, (
        "a per-round depth row is back in the template, and it cannot be "
        "answered honestly by a fix pass that did both kinds of fix"
    )
    assert "per entry rather than in a row of its own" in text, (
        "the template no longer records why the depth is per entry, which is "
        "the reasoning the next reader needs before proposing the row again"
    )
