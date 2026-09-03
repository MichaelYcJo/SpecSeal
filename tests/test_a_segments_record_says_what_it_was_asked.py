"""Neither a round record nor a build phase said what it was ASKED to do,
only what it found. #81 is the measured cost on the review side: round 1 of
the work item it names was the cheapest round measured — 7.6 minutes, 29
tool calls, one 🔴 and four 🟡 — because its spawn prompt named eight
specific things to try to break, in order. That fact survives today only in
a transcript.

Phase 3 of the "a phase hands the next one a record" work item adds the
round-side half of the fix: `## What this round was asked` in
`templates/sdd-round.md`, mirroring the `## What this phase was asked`
section `templates/sdd-phase.md` already ships
(`test_a_phase_hands_the_next_one_a_record.py`). This module pins:

  the section        exists outside HTML comments, as a placeholder rather
                     than a filled claim, placed after the field table's
                     comment and before `## Verdicts`
  the measured story  the section's own comment names #81 and the numbers
                     that made round 1 the cheapest round measured
  the copy instruction `skills/code-review/SKILL.md` tells the orchestrator
                     to copy the round-specific spawn content in, right
                     after posting — beside "A round record starts from
                     `templates/sdd-round.md`"
  cross-file consistency  the round-side and phase-side headings and copy
                     instructions follow one shared skeleton rather than
                     two conventions for the same behavioral guarantee —
                     mindful that `templates/sdd-round.md`'s and
                     `templates/sdd-phase.md`'s own self-referencing path
                     comments are bracketed (`round-<N>.md`,
                     `phase-<N>.md`) while every file that only POINTS AT
                     either record uses the bracket-free form, a split
                     phase 2 already found deliberate and not an
                     inconsistency to flatten

The placeholder check reads through the same `strip_comments` `chain_check.py`
itself loads for `round-N.md` (`skills/verify/scripts/unverified_check.py`),
the same reader phase 1's module used for `templates/sdd-phase.md` — a
second implementation here would be free to drift from what actually reads
these records.
"""

import importlib.util
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROUND_TEMPLATE = os.path.join(ROOT, "templates", "sdd-round.md")
PHASE_TEMPLATE = os.path.join(ROOT, "templates", "sdd-phase.md")
REVIEW_SKILL = os.path.join(ROOT, "skills", "code-review", "SKILL.md")
IMPLEMENT_SKILL = os.path.join(ROOT, "skills", "implement", "SKILL.md")

ROUND_HEADING = "## What this round was asked"
PHASE_HEADING = "## What this phase was asked"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def flat(path):
    """Whitespace-collapsed text, for pinning a multi-word phrase that this
    repository's own line wrap is free to break across lines — the same
    normalization `test_the_fixes_name_their_surface.py`'s `flat()` uses.
    Structural checks (heading order, section boundaries) still read the raw
    text, where a real line break is part of what is being checked."""
    return " ".join(read(path).split())


def reader_module():
    """`unverified_check.py`'s `strip_comments` — the same reader
    `chain_check.py` loads for `rounds/round-N.md`."""
    spec = importlib.util.spec_from_file_location(
        "specseal_round_reader_for_tests",
        os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stripped_lines(path):
    return reader_module().strip_comments(read(path).splitlines())


def section_body(lines, heading):
    """The non-blank lines between `heading` and the next `## ` heading (or
    end of file), from lines already run through `strip_comments`."""
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    assert start is not None, f"heading not found outside comments: {heading}"
    body = []
    for line in lines[start:]:
        if line.strip().startswith("## "):
            break
        if line.strip():
            body.append(line)
    return body


# --- the round section exists, placed correctly, and ships a placeholder ----


def test_the_round_section_exists_outside_comments():
    lines = stripped_lines(ROUND_TEMPLATE)
    present = {line.strip() for line in lines}
    assert ROUND_HEADING in present, (
        f"`{ROUND_HEADING}` is missing outside HTML comments — a heading "
        "only a comment carries is a heading a copied file does not have"
    )


def test_the_round_section_is_between_the_field_table_and_verdicts():
    raw = read(ROUND_TEMPLATE)
    pass_idx = raw.index("- [ ] Pass")
    asked_idx = raw.index(ROUND_HEADING)
    verdicts_idx = raw.index("## Verdicts")
    assert pass_idx < asked_idx < verdicts_idx, (
        "`## What this round was asked` must sit after the field table's "
        "closing HTML comment and before `## Verdicts`"
    )


def test_the_round_section_ships_a_placeholder():
    lines = stripped_lines(ROUND_TEMPLATE)
    body = section_body(lines, ROUND_HEADING)
    assert body, f"`{ROUND_HEADING}` has no content outside comments"
    text = " ".join(line.strip() for line in body)
    assert text.startswith("<") and text.endswith(">"), (
        f"`{ROUND_HEADING}` ships `{text}` — a template must offer a "
        "placeholder, not a filled-in claim"
    )


def test_the_round_sections_comment_names_81_and_the_measured_numbers():
    raw = read(ROUND_TEMPLATE)
    asked_idx = raw.index(ROUND_HEADING)
    verdicts_idx = raw.index("## Verdicts")
    section = " ".join(raw[asked_idx:verdicts_idx].split())
    assert "#81" in section, (
        "the new section's own comment does not name #81 — the measured gap it answers"
    )
    for probe in ("7.6", "29", "cheapest round"):
        assert probe in section, (
            f"the section's comment lost `{probe}` — the measured reason "
            "#81's round 1 was cheap, and the fact this section exists to "
            "keep from surviving only in a transcript"
        )


# --- the skill carries the copy instruction ----------------------------------


def test_skill_carries_the_copy_instruction():
    skill = read(REVIEW_SKILL)
    assert ROUND_HEADING.lstrip("# ").strip() in skill or ROUND_HEADING in skill, (
        "skills/code-review/SKILL.md never names the section the copied "
        "content lands in"
    )
    assert "boilerplate" in skill, (
        "skills/code-review/SKILL.md does not say that the copied content "
        "excludes the boilerplate `agent-contract` and `agents/warden.md` "
        "already carry"
    )
    assert "agent-contract" in skill and "agents/warden.md" in skill
    assert "right after posting" in skill, (
        "skills/code-review/SKILL.md does not say WHEN to copy the content "
        "in — the same moment the other three cross-session files are "
        "written"
    )


def test_the_copy_instruction_sits_beside_the_round_record_starts_from_line():
    skill = read(REVIEW_SKILL)
    anchor = "A round record starts from `templates/sdd-round.md`"
    assert anchor in skill, "the anchor sentence itself moved or was reworded"
    anchor_idx = skill.index(anchor)
    copy_idx = skill.index("What goes into `round-N.md`")
    # "beside" — within the same subsection, not pages away. The next
    # heading after the anchor bounds how far "beside" can stretch.
    next_heading_idx = skill.index("\n## ", anchor_idx)
    assert anchor_idx < copy_idx < next_heading_idx, (
        "the copy instruction is not beside the "
        "`A round record starts from templates/sdd-round.md` sentence"
    )


# --- cross-file consistency: one skeleton, not two conventions --------------
#
# The heading text cannot be identical — "round" and "phase" name different
# segments — so what has to match is the SKELETON: `## What this <segment>
# was asked`, with the same three words on either side of the segment name.
# Flattening the two into byte-identical text is the wrong fix here: phase 2
# already found that `templates/sdd-phase.md`'s own self-reference is
# bracketed (`phase-<N>.md`) while `templates/sdd-plan.md`/`agents/smith.md`/
# `skills/implement/SKILL.md` point at it bracket-free (`phase-N.md`), and
# that split is deliberate, matching `templates/sdd-round.md`'s own
# bracketed self-reference. This test checks the headings and the copy
# instructions share one convention; it does not force the two templates'
# own path comments to spell themselves alike, because they already don't
# and phase 2 recorded why.


SKELETON_RE = re.compile(r"^## What this (\w+) was asked$", re.MULTILINE)


def test_the_heading_skeleton_matches_across_round_and_phase():
    # Reads the actual file content through the skeleton pattern rather than
    # comparing the two hardcoded constants above to each other — a
    # constant-to-constant comparison can never go red against a real wording
    # change in either template.
    round_match = SKELETON_RE.search(read(ROUND_TEMPLATE))
    phase_match = SKELETON_RE.search(read(PHASE_TEMPLATE))
    assert round_match, (
        "templates/sdd-round.md has no heading matching "
        "`## What this <segment> was asked`"
    )
    assert phase_match, (
        "templates/sdd-phase.md has no heading matching "
        "`## What this <segment> was asked`"
    )
    assert round_match.group(1) == "round", round_match.group(0)
    assert phase_match.group(1) == "phase", phase_match.group(0)


def test_the_copy_instructions_share_one_skeleton():
    review_skill = flat(REVIEW_SKILL)
    implement_skill = flat(IMPLEMENT_SKILL)
    # The phase-side instruction (skills/implement/SKILL.md, phase 2):
    # "What goes into `phases/phase-N.md`'s `## What this phase was asked`
    # section is the phase-specific content of the spawn or task that
    # started it — never the boilerplate the contract, this skill, and
    # `agents/smith.md` already carry".
    assert (
        "What goes into `phases/phase-N.md`'s `## What this phase was asked`"
        in implement_skill
    ), "the phase-side copy instruction moved or was reworded"
    assert (
        "What goes into `round-N.md`'s `## What this round was asked`" in review_skill
    ), "the round-side copy instruction does not open the same way"
    # Both instructions must state the same three things, in the same
    # vocabulary: WHAT is copied (the segment-specific content), what it
    # EXCLUDES (the boilerplate its own contract/skill/agent already
    # carry), and WHEN (a specific moment, not "eventually").
    for skill_text, segment in ((implement_skill, "phase"), (review_skill, "round")):
        assert f"{segment}-specific content" in skill_text, (
            f"the {segment}-side instruction does not name what is copied "
            f"as `{segment}-specific content`"
        )
        assert "never the boilerplate" in skill_text, (
            f"the {segment}-side instruction does not use the shared "
            "`never the boilerplate ... already carry` framing"
        )
        assert "already carry" in skill_text


def test_the_round_and_phase_records_do_not_diverge_on_which_file_moves():
    # Both instructions must name the concrete template AND the concrete
    # agent/skill boilerplate they exclude, so a reader of either can find
    # the other half of the pair without guessing.
    review_skill = read(REVIEW_SKILL)
    implement_skill = read(IMPLEMENT_SKILL)
    assert "agents/warden.md" in review_skill
    assert "agents/smith.md" in implement_skill
    assert "agent-contract" in review_skill
    assert "the contract" in implement_skill
