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

Issue #136 adds a second destination and a second zero. Two issues collect
measurements in the same shape and one of them is deleted at every release, so
the section now says which reading goes to which — a segment's own numbers to
the rolling `flow-measurement` log, a reading that only means something across
versions to the durable `flow-baseline` one — and separates a repository that
never measured from one whose log stopped. The cases below pin both labels,
the rule that separates them, the `--state all` lookup that tells the two
zeroes apart, and the refusal that keeps a session from repairing the second.

They also pin what the section may NOT say. This file ships to repositories
that have neither this repository's `measurement` index label nor its
`log: measurement` milestone nor its durable issue number, so those three are
`.github/scripts/`'s to name and not the skill's —
`tests/test_the_release_check_watches_what_ships.py` is what classifies that
directory as staying home.
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


def test_the_section_names_the_durable_logs_label():
    body = section_body()
    assert "flow-baseline" in body, (
        "the section never names `flow-baseline`, so a reading that only "
        "means something across versions has nowhere to go but the rolling "
        "log — which is deleted when the version ships. That happened on "
        "2026-09-04 and is what #136 opened for"
    )


def test_the_section_says_what_separates_the_two_logs():
    """Naming both labels is not the same as saying which gets what. A session
    with two destinations and no rule picks by feel, which is the state before
    this section named either of them."""
    body = section_body()
    assert "span versions" in body, (
        "the section names the two logs but never says what separates them — "
        "a reading that spans versions is the one that must not go to the "
        "log that is discarded"
    )
    assert "discarded" in body, (
        "the section must say the rolling log is discarded at the release; "
        "that is the whole reason the durable one exists, and without it the "
        "split reads as an arbitrary filing convention"
    )


def test_the_section_separates_the_two_zeroes():
    body = section_body()
    assert "gh issue list --label flow-measurement --state all" in body, (
        "the section must name the `--state all` lookup. A repository that "
        "never measured and one whose log stopped both read zero open, and "
        "the first is a no-op while the second is a broken invariant — one "
        "call tells them apart"
    )


def test_a_session_names_the_stopped_log_rather_than_opening_one():
    """The obvious next step — if none is open, open one — is what breaks the
    invariant the release-time roll depends on."""
    body = section_body()
    assert "not a session's act" in body, (
        "the section must refuse outright: a session that finds the label "
        "with a history and nothing open names it and opens nothing"
    )
    assert "two or more" in body, (
        "the refusal must carry its reason — two sessions finishing segments "
        "at the same moment both read zero and both create, and the next "
        "release then fails on two or more. Without the reason the refusal "
        "reads as caution and the next reader talks themselves out of it"
    )


def test_the_shipped_skill_names_no_repository_specific_tracker_state():
    """This skill ships. `flow-measurement` and `flow-baseline` are the
    plugin's vocabulary and belong here; the `measurement` index label, the
    `log: measurement` milestone and the durable issue's number are this
    repository's own and belong in `.github/scripts/`, which
    `tests/test_the_release_check_watches_what_ships.py` classifies as staying
    home."""
    text = read()
    assert "log: measurement" not in text, (
        "the shipped skill names this repository's own milestone — an "
        "installed repository has no such milestone and cannot act on it"
    )
    assert "#51" not in text, (
        "the shipped skill hardcodes this repository's durable issue number. "
        "A number is what #109 removed from the rolling log's lookup for the "
        "same reason: it goes stale, and it means nothing anywhere else"
    )
    assert "`measurement`" not in section_body(), (
        "the section names the bare `measurement` index label, which exists "
        "in this repository only. The two labels a shipped skill may name are "
        "`flow-measurement` and `flow-baseline`"
    )
