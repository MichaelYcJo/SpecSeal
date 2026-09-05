"""Each of #161's nine rules has one carrier that states it, and every other
carrier links to that one in a sentence that names it.

The last branch's count rule reached eight carriers, and rounds 7, 8 and 9
corrected them three at a time — a rule stated in eight places is eight
places to disagree. `spec.md` §Scope *In — the rules* of the work item that
added these lists the nine with one owner each:

  1  a record-located finding is a correction     docs/review-chain-spec.md
  2  a fix pass adds no mechanism                 skills/code-review/SKILL.md
  3  🟡 is a defect the release would ship; ⬜     skills/code-review/SKILL.md
  4  the reopening is one, then `capped`          docs/review-chain-spec.md
  5  a fix pass hands over a fix table            agents/smith.md
  6  the draft pull request before round 1        skills/code-review/SKILL.md
  7  a compacted session hands over the record    skills/code-review/SKILL.md
  8  the 0.8.x moratorium on fields               docs/review-chain-spec.md
  9  a hand-back's claim is re-run                skills/code-review/SKILL.md

Phase 4a wrote the three owners' files and phase 4b the five linking
carriers; the link tables below hold the links both phases' files carry, one
pin file rather than two. The four reach-backs are pinned beside the rules:
the sections that told the orchestrator to fill `Fixes checked by`, the fix
surface and `Ran by` by hand now name the subcommand that fills them, and
the linking carriers that said the orchestrator writes the record now name
the generator too — the sentences about the reviewed-HEAD mark, which the
orchestrator does write, are not among them.

Every sentence here was seen red with the sentence stashed (§15).
"""

import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SPEC = ("docs", "review-chain-spec.md")
SKILL = ("skills", "code-review", "SKILL.md")
TEMPLATE = ("templates", "sdd-round.md")
SMITH = ("agents", "smith.md")
PROTOCOL = ("docs", "review-handoff-protocol.md")
WARDEN = ("agents", "warden.md")
IMPLEMENT = ("skills", "implement", "SKILL.md")
FLOW = ("docs", "flow.md")
PHASE_TEMPLATE = ("templates", "sdd-phase.md")

# The directories the count rule was swept across.
TREE = ("docs", "skills", "agents", "templates")

REOPENING = "§*The reopening — one, and then the run is capped*"
NO_MECHANISM = (
    "`skills/code-review/SKILL.md` §*A fix pass adds the unit that pins it, "
    "and that unit ships unreviewed* owns that rule"
)
BEFORE_ROUND_ONE = (
    "`skills/code-review/SKILL.md` §*Orchestrator: the pull request opens "
    "before round 1, and a phase is re-run* owns"
)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(*parts).split())


# --- the rules: owner, the sentence, and the links that name the owner ------

# rule → (owner, the sentence the owner states, {link carrier: how it names
# the owner}). A link is one sentence and names the owner's file or the
# owner's subsection; it does not restate the rule.
RULES = {
    "1 a record-located finding is a correction": (
        SPEC,
        "A finding located in a record is a correction, not a round.",
        {
            SKILL: "`docs/review-chain-spec.md` §*The last round verifies* owns the rule",
            WARDEN: "`docs/review-chain-spec.md` §*The last round verifies* owns the rule",
        },
    ),
    "2 a fix pass adds no mechanism": (
        SKILL,
        "A fix pass may not add mechanism.",
        {SMITH: NO_MECHANISM, IMPLEMENT: NO_MECHANISM},
    ),
    "3 🟡 is a defect the release would ship": (
        SKILL,
        "a defect the release would ship",
        {WARDEN: "`skills/code-review/SKILL.md` §*Findings format* owns that line"},
    ),
    "4 the reopening is one": (
        SPEC,
        "at most one later record may close on a fix",
        {
            SKILL: f"`docs/review-chain-spec.md` {REOPENING} owns",
            TEMPLATE: f"`docs/review-chain-spec.md` {REOPENING} owns",
            PROTOCOL: f"`docs/review-chain-spec.md` {REOPENING} owns",
            WARDEN: f"`docs/review-chain-spec.md` {REOPENING} owns",
        },
    ),
    "5 a fix pass hands over a fix table": (
        SMITH,
        "hands over a fix table under `## Fixes`",
        {SKILL: "`agents/smith.md` owns that rule"},
    ),
    "6 the draft pull request opens before round 1": (
        SKILL,
        "The draft pull request opens at the end of the build, before round 1.",
        {
            PROTOCOL: f"opened when the build's last phase closes, because {BEFORE_ROUND_ONE}",
            FLOW: f"the draft pull request opens ({BEFORE_ROUND_ONE} when)",
        },
    ),
    "7 a compacted session hands the next round to a fresh one": (
        SKILL,
        "A session that has compacted hands the next round to a fresh one, and "
        "the generated record is the handoff.",
        {},
    ),
    "8 the moratorium": (
        SPEC,
        "no new parsed field in `round-N.md` and no new row the ledger must carry",
        {},
    ),
    "9 a hand-back's verification claim is a claim": (
        SKILL,
        "A hand-back's verification claim is a claim.",
        {
            PROTOCOL: f"{BEFORE_ROUND_ONE} the rule. Its grounds are one step from this document"
        },
    ),
}


@pytest.mark.parametrize("rule", sorted(RULES))
def test_the_owner_states_the_rule(rule):
    owner, sentence, _ = RULES[rule]
    assert sentence in flat(*owner), (
        f"{'/'.join(owner)} no longer states rule {rule!r}, and it is the one "
        "carrier that does"
    )


@pytest.mark.parametrize("rule", sorted(r for r in RULES if RULES[r][2]))
def test_every_link_names_the_owner(rule):
    owner, _, links = RULES[rule]
    for carrier, names_the_owner in links.items():
        assert carrier != owner, f"{rule!r}: the owner is listed as its own link"
        assert names_the_owner in flat(*carrier), (
            f"{'/'.join(carrier)} carries rule {rule!r} without naming "
            f"{'/'.join(owner)} as its owner, which is a second statement of "
            "the rule rather than a link to the one that owns it"
        )


# --- rule 3's other half: ⬜ exists beside 🟡 ------------------------------


def test_a_note_severity_exists_and_needs_a_fix_does_not_count_it():
    """Half of the last branch's 53 🟡 were true sentences about prose, and
    each cost a fix pass and a reader. Without a fourth line the reviewer has
    no spelling for *reads badly and ships nothing wrong*."""
    skill = flat(*SKILL)
    assert "⬜ note" in skill, "the findings format has no ⬜ line"
    assert "never counted by Needs a fix" in skill
    assert "`Needs a fix` counts 🔴 and 🟡 only" in skill


# --- rule 4's link in the skill, twice, and the exit in both -----------------


def test_the_skill_links_the_reopening_from_both_places_it_used_to_state_it():
    """The skill carried the exception twice — under the verifying round and
    under the floor — and each copy now links rather than restates. Counted,
    because one copy left restating is the disagreement this file exists to
    refuse."""
    skill = flat(*SKILL)
    assert skill.count(REOPENING) == 2, (
        f"the skill names the reopening subsection {skill.count(REOPENING)} "
        "times where its two former copies of the exception stood"
    )
    assert "`chain: capped`" in skill
    assert "`deferred #N`" in skill


# --- rule 1 says what the count was --------------------------------------------


def test_the_owner_of_rule_one_carries_the_count():
    """The rule is the reading of a number, and the number is in the owner:
    33 of 65 findings located in records, records 55 % of the diff."""
    spec = flat(*SPEC)
    assert "33 of its 65 findings were located in records" in spec
    assert "55 % of the diff" in spec
    assert "`Needs a fix` does not count it" in spec


# --- the reach-backs are the generator's ------------------------------------

# The section that used to tell the orchestrator to fill a cell by hand, and
# the sentence that now names the subcommand.
REACH_BACKS = {
    "Fixes checked by": (
        "### Then say who checked them, in the record",
        "`round_record.py new --item <dir> --round N …` sets it",
    ),
    "the fix surface": (
        "### And name the fix surface, in the same record",
        "`round_record.py close --range <a>..<b>` derives both from the fix range",
    ),
    "Ran by": (
        "### And say what ran the round",
        '`round_record.py new` writes it from `--ran-by "<agent> on <model>"`',
    ),
    "the record before the fixes": (
        "### And commit the record before commissioning the fixes",
        "`round_record.py new` writes `round-N.md` when the round posts",
    ),
}


@pytest.mark.parametrize("which", sorted(REACH_BACKS))
def test_the_section_names_the_subcommand_that_fills_the_cell(which):
    """Five reach-backs forgotten five times on the last branch. The
    sections keep the rule and its grounds and no longer ask a session to
    remember the step; the subcommand is named where the instruction was."""
    heading, sentence = REACH_BACKS[which]
    text = flat(*SKILL)
    assert heading in text, f"the section for {which!r} moved: {heading!r}"
    start = text.index(heading)
    end = text.find(" ### ", start + len(heading))
    section = text[start : end if end > 0 else None]
    assert sentence in section, (
        f"the {which!r} section no longer names the subcommand that fills "
        "the cell, so the reach-back is a habit to remember again"
    )


def test_the_skill_no_longer_calls_the_reach_back_a_habit():
    """The absence half, beside the presence above: the sentence that told
    the orchestrator the cells were a pass to remember is gone, and the one
    that replaced it names the generator."""
    text = flat(*SKILL)
    assert "The habit that makes all of it moot" not in text
    assert "What makes all of it moot is the generator" in text


def test_the_template_says_the_record_is_generated():
    """A template a session copies by hand is the record-writing this work
    removes. The top comment says which subcommand writes and which closes,
    and that the comments are documentation a generated record does not
    carry."""
    template = flat(*TEMPLATE)
    assert "It is GENERATED: `round_record.py new` writes it" in template
    assert "`round_record.py close` applies the implementer's fix table" in template
    assert "a generated record does not carry them" in template
    assert "the generator commits nothing" in template


def test_the_template_offers_deferred_with_a_home():
    """The verdict vocabulary comment is where a reader learns what closes a
    finding; a word the checker accepts and the template omits is a word
    nobody writes."""
    template = flat(*TEMPLATE)
    assert "`deferred <home>` closes a finding handed to the tracker" in template
    assert "A bare `deferred`, nothing after it, stays OPEN" in template


def test_the_spec_says_the_record_is_written_by_the_generator():
    """*A declaration, and why no check reads it* was written when the
    orchestrator typed the probes table; it now describes what `new` copies
    from the reviewer's report."""
    spec = flat(*SPEC)
    assert "The record is written by `round_record.py` now" in spec
    assert "copies the reviewer's `Executed probes` table row for row" in spec


# --- the count rule's phrases: the owner and the links, and nothing else ---


def occurrences(phrase):
    """{relative path: count} over every Markdown file in the swept tree."""
    found = {}
    for top in TREE:
        for dirpath, _, names in os.walk(os.path.join(ROOT, top)):
            for name in sorted(names):
                if not name.endswith(".md"):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8") as handle:
                    count = " ".join(handle.read().split()).count(phrase)
                if count:
                    found[os.path.relpath(path, ROOT)] = count
    return found


AT_MOST_ONE_MORE = "at most one more round record"
UNLESS = "Unless th"

# What the tree holds after phase 4a. Phase 4b sweeps the five linking
# carriers and may only lower these; a phase that raises one has written a
# ninth carrier of the count rule.
AT_MOST_ONE_MORE_CEILING = 4
UNLESS_CEILING = 0


def test_the_count_rules_sentence_is_the_owners_and_its_links():
    """`docs/review-chain-spec.md` states *at most one more round record*
    and owns it; the skill and the template carry the phrase in a sentence
    that names the owner's subsection, and nothing they carry says *unless*
    — the exception is the owner's to state, bounded to one."""
    found = occurrences(AT_MOST_ONE_MORE)
    assert found.get("/".join(SPEC)) == 1, found
    for carrier in (SKILL, TEMPLATE):
        text = flat(*carrier)
        assert found.get("/".join(carrier)) == 1, found
        after = text[text.index(AT_MOST_ONE_MORE) :]
        assert REOPENING in after[:600], (
            f"{'/'.join(carrier)} carries the count rule's sentence without "
            "the owner's subsection in the same breath"
        )
    for carrier in (SPEC, SKILL, TEMPLATE):
        assert UNLESS not in flat(*carrier), (
            f"{'/'.join(carrier)} still states the exception as an *unless*, "
            "which is the unbounded reading"
        )
    assert sum(found.values()) <= AT_MOST_ONE_MORE_CEILING, found
    assert sum(occurrences(UNLESS).values()) <= UNLESS_CEILING, occurrences(UNLESS)


def test_the_occurrence_count_can_fail():
    """A sweep that finds nothing is indistinguishable from one that read
    nothing, so the walker is shown finding a phrase the owner is known to
    carry."""
    assert occurrences("Rounds are capped at **three**") == {"/".join(SPEC): 1}


# --- phase 4b: the linking carriers ------------------------------------------

RE_RUN_HEADING = "### After a phase — the hand-back's claim is re-run"


def test_the_protocol_re_runs_a_closed_phase_under_its_own_heading():
    """Rule 9 reaches the protocol as a subsection of its own, between the
    one about watching a running implementer and the one about the bars
    after a run, and the subsection names the owner rather than restating
    the rule's grounds."""
    text = flat(*PROTOCOL)
    before = text.index("### While the implementer runs")
    after = text.index("### After the run — the per-segment bars")
    assert before < text.index(RE_RUN_HEADING) < after, (
        "the re-run subsection is not where a reader watching a phase close "
        "would look for it"
    )
    section = text[text.index(RE_RUN_HEADING) : after]
    assert "runs the closed phase's suite and the lint of its changed files" in section
    assert "the broad gate still runs once" in section
    assert (
        RULES["9 a hand-back's verification claim is a claim"][2][PROTOCOL] in section
    )


def test_the_flow_opens_the_draft_between_the_build_and_the_rounds():
    """`docs/flow.md`'s order inside a ticket is what a session reads to
    know what comes after the smith; a pull request listed last there is the
    dozen-rounds-on-one-platform shape the owner's section measured."""
    text = flat(*FLOW)
    step = text[text.index("2. spec · plan") : text.index("3. The pull request body")]
    assert "smith → the draft pull request opens (" in step
    assert ") → warden rounds → sealer → the pull request is marked ready." in step
    assert step.index("the draft pull request opens") < step.index("warden rounds")


# carrier → the sentence that names the generator where the orchestrator's
# hand used to be named.
GENERATOR_NAMED = {
    PROTOCOL: "The record is written by `round_record.py new` from the reviewer's report",
    WARDEN: (
        "`round_record.py new` writes the record from this report once the "
        "orchestrator has verified its findings"
    ),
    SMITH: "`round_record.py new` sets it on the previous record when the next round posts",
    IMPLEMENT: "`round_record.py new`, run by the review orchestrator; `close` applies the fix table",
    PHASE_TEMPLATE: "runs `round_record.py new`, which writes that file",
}


@pytest.mark.parametrize("carrier", sorted(GENERATOR_NAMED))
def test_the_linking_carrier_names_the_generator(carrier):
    """Five carriers said the orchestrator writes the record, and the
    orchestrator writes the round paragraph of the spawn prompt and nothing
    else in it. What the orchestrator does write — the reviewed-HEAD mark —
    keeps its sentence, and no case here reads it."""
    assert GENERATOR_NAMED[carrier] in flat(*carrier), (
        f"{'/'.join(carrier)} no longer names `round_record.py new` where it "
        "used to name the orchestrator's hand"
    )


def test_the_warden_hands_both_terminal_lines_to_the_generator():
    """The reviewer's two terminal lines are copied into the record by `new`,
    and the report used to say the orchestrator copied them — a sentence
    that reads as an instruction to type a cell."""
    warden = flat(*WARDEN)
    assert "`round_record.py new` copies it into the row of the same name" in warden
    assert "copied into the row of the same name by the same subcommand" in warden
    # The report's own copy of the sentence, distinct from the §6 bullet's: a
    # pin on the shared prefix stayed green when one of the two was stashed.
    assert (
        "`round_record.py new` writes the record from this report, so the "
        "headers are what it parses"
    ) in warden
    assert "the orchestrator copies it into the row" not in warden
    assert "the orchestrator owns the records" not in flat(*SMITH)
