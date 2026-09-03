"""Issue #109 part 1: the instruction "measure every smith/warden segment and
log what it found" used to live only in a person's message
(`~/.claude/projects/.../memory/measure-every-segment-to-89.md`), retyped
every session and naming a hardcoded issue number that goes stale the moment
that issue closes. It moves into `skills/verify/SKILL.md`, between
`## Seal block` and `## Counterfeits (stop on sight)`, so a session does it
because the skill says so, and the destination becomes a
`flow-measurement`-labelled GitHub issue instead of a number.

This module pins three things a session reading that section needs: both
commands are named (`session_cost.py` and the `gh issue list --label
flow-measurement --state open` lookup), and the no-op case is stated
explicitly — most installed repositories never create the label, so the
common case is that this section does nothing, and the section has to say so
rather than leave a reader to infer it from silence.

`skills/verify/SKILL.md` carries no HTML comments anywhere in the file
(checked directly, not assumed) — so unlike
`tests/test_a_phase_hands_the_next_one_a_record.py`'s template pins, this
module does not need a comment-stripping reader; a plain substring check
already means "outside any comment", matching
`tests/test_review_axes.py`'s style for the same reason (the source here is
skill prose, not a template with placeholders).
"""

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(ROOT, "skills", "verify", "SKILL.md")

SECTION_HEADING = "## Measure the segment, and feed the flow log"


def read():
    with open(SKILL, encoding="utf-8") as f:
        return f.read()


def section_body():
    """Whitespace-collapsed, so a substring check does not break every time
    the prose re-wraps at a different column — the wording is what these
    tests pin, not which line a hyphen happens to fall on."""
    text = read()
    start = text.index(SECTION_HEADING)
    rest = text[start + len(SECTION_HEADING) :]
    next_heading = rest.index("\n## ")
    return " ".join(rest[:next_heading].split())


def test_skill_has_no_html_comments_at_all():
    """The premise the rest of this module leans on: with zero `<!--` in the
    whole file, a plain substring match already means "outside any HTML
    comment" — there is no comment for the section to hide inside."""
    assert "<!--" not in read(), (
        "skills/verify/SKILL.md now has HTML comments — this module's plain "
        "substring checks no longer prove the section sits outside them; "
        "switch to a comment-stripping reader like "
        "tests/test_a_phase_hands_the_next_one_a_record.py does"
    )


def test_the_section_exists_between_seal_block_and_counterfeits():
    text = read()
    seal_idx = text.index("## Seal block")
    section_idx = text.index(SECTION_HEADING)
    counterfeits_idx = text.index("## Counterfeits (stop on sight)")
    assert seal_idx < section_idx < counterfeits_idx, (
        "the flow-log section must sit between `## Seal block` and "
        "`## Counterfeits (stop on sight)` — that is the placement `plan.md` "
        "fixed for phase 1"
    )


def test_the_section_names_the_measure_step():
    body = section_body()
    assert "session_cost.py" in body, (
        "the section never names `session_cost.py` — a session reading it "
        "has no command to run against the segment's transcript"
    )


def test_the_section_names_the_lookup_command():
    body = section_body()
    assert "gh issue list --label flow-measurement --state open" in body, (
        "the section never names the exact lookup command — a session would "
        "have to guess how to find the destination issue rather than being "
        "told"
    )


def test_the_section_names_the_post_command():
    body = section_body()
    assert "gh issue comment" in body and "--body-file" in body, (
        "the section never names how to post the measurement — "
        "`gh issue comment <n> --body-file <file>`"
    )


def test_the_section_states_an_absent_label_is_a_no_op():
    body = section_body()
    assert "no-op" in body, (
        "the section must say explicitly that an absent "
        "`flow-measurement` issue makes this a no-op — silence here reads "
        "as an unhandled case, not as 'nothing to do', and most installed "
        "repositories will hit exactly this branch"
    )
    for phrase in ("nothing is posted", "nothing fails", "nothing asks"):
        assert phrase in body, f"the no-op sentence lost `{phrase}`"


def test_the_section_says_it_happens_without_asking():
    body = section_body()
    assert "never" in body and "question" in body, (
        "the section must say the post happens without asking — otherwise a "
        "session reading it may treat the destination issue as something "
        "requiring approval, reintroducing the prompt #109 exists to remove"
    )
