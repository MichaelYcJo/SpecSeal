"""Each of #161's nine rules has one carrier that states it, and every other
carrier links to that one in a sentence that names it.

The last branch's count rule reached eight carriers, and rounds 7, 8 and 9
corrected them three at a time — a rule stated in eight places is eight
places to disagree. `spec.md` §Scope *In — the rules* of the work item that
added these lists the nine with one owner each:

  1  a record-located finding is a correction     docs/review-chain-spec.md
  2  a fix pass adds no mechanism                 code-review/orchestration.md
  3  🟡 is a defect the release would ship; ⬜     skills/code-review/SKILL.md
  4  the reopening is one, then `capped`          docs/review-chain-spec.md
  5  a fix pass hands over a fix table            agents/smith.md
  6  the draft pull request before round 1        code-review/orchestration.md
  7  a compacted session hands over the record    code-review/orchestration.md
  8  the 0.8.x moratorium on fields               docs/review-chain-spec.md
  9  a hand-back's claim is re-run                code-review/orchestration.md

Five of the nine used to be owned by `skills/code-review/SKILL.md`. #265 split
that file on the seam its own headings drew: the five sections it prefixed
`Orchestrator:` moved to `skills/code-review/orchestration.md`, so four of the
five rules above moved with their sections and rule 3 stayed with §*Findings
format*. The headings did not change, so every link sentence names the section
it always named and only the file it names moved.

Phase 4a wrote the three owners' files and phase 4b the five linking
carriers; the link tables below hold the links both phases' files carry, one
pin file rather than two. The four reach-backs are pinned beside the rules:
the sections that told the orchestrator to fill `Fixes checked by`, the fix
surface and `Ran by` by hand now name the subcommand that fills them, and
the linking carriers that said the orchestrator writes the record now name
the generator too — the sentences about the reviewed-HEAD mark, which the
orchestrator does write, are not among them.

A tenth rule joined from #30 rather than from #161, and it is here because
its shape is the table's exactly: one owner, two carriers whose sentences
must stay links rather than becoming restatements. It says which of the
seals a project accumulates is the final one -- the word reached three
referents at once, and the missing sentence was not *fewer seals* but
*one of them is final*.

Every sentence here was seen red with the sentence stashed (§15).
"""

import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SPEC = ("docs", "review-chain-spec.md")
SKILL = ("skills", "code-review", "SKILL.md")
# The orchestrator's half of the review skill (#265). The five sections the
# file prefixed `Orchestrator:` live here; the reviewer's half stays in SKILL.
ORCH = ("skills", "code-review", "orchestration.md")
TEMPLATE = ("templates", "sdd-round.md")
SMITH = ("agents", "smith.md")
PROTOCOL = ("docs", "review-handoff-protocol.md")
WARDEN = ("agents", "warden.md")
IMPLEMENT = ("skills", "implement", "SKILL.md")
# The orchestrator's half of the implement skill (#292). The order a ticket
# runs in landed here in #351, when the shared checklist that used to hold it
# was deleted -- beside the routing question its first step opens.
ORCH_IMPL = ("skills", "implement", "orchestration.md")
PHASE_TEMPLATE = ("templates", "sdd-phase.md")
VERIFY = ("skills", "verify", "SKILL.md")
SEALER = ("agents", "sealer.md")

# The directories the count rule was swept across.
TREE = ("docs", "skills", "agents", "templates")

REOPENING = "§*The reopening — one, and then the run is capped*"
NO_MECHANISM = (
    "`skills/code-review/orchestration.md` §*A fix pass adds the unit that "
    "pins it, and that unit ships unreviewed* owns that rule"
)
ONE_SEAL_IS_FINAL = (
    "`skills/verify/SKILL.md` §*Every agent seals what it verified, and "
    "one of them is final* owns that rule"
)
BEFORE_ROUND_ONE = (
    "`skills/code-review/orchestration.md` §*Orchestrator: the pull request "
    "opens before round 1, and a phase is re-run* owns"
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
            ORCH: "`docs/review-chain-spec.md` §*The last round verifies* owns the rule",
            WARDEN: "`docs/review-chain-spec.md` §*The last round verifies* owns the rule",
        },
    ),
    "2 a fix pass adds no mechanism": (
        ORCH,
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
            ORCH: f"`docs/review-chain-spec.md` {REOPENING} owns",
            TEMPLATE: f"`docs/review-chain-spec.md` {REOPENING} owns",
            PROTOCOL: f"`docs/review-chain-spec.md` {REOPENING} owns",
            WARDEN: f"`docs/review-chain-spec.md` {REOPENING} owns",
        },
    ),
    "5 a fix pass hands over a fix table": (
        SMITH,
        "hands over a fix table under `## Fixes`",
        {ORCH: "`agents/smith.md` owns that rule"},
    ),
    "6 the draft pull request opens before round 1": (
        ORCH,
        "The draft pull request opens at the end of the build, before round 1.",
        {
            PROTOCOL: f"opened when the build's last phase closes, because {BEFORE_ROUND_ONE}",
            ORCH_IMPL: f"the draft pull request opens ({BEFORE_ROUND_ONE} when)",
        },
    ),
    "7 a compacted session hands the next round to a fresh one": (
        ORCH,
        "A session that has compacted hands the next round to a fresh one, and "
        "the generated record is the handoff.",
        {},
    ),
    "8 the moratorium": (
        SPEC,
        "no new parsed field in `round-N.md` and no new row the ledger must carry",
        {},
    ),
    "10 every agent seals what it verified, and one seal is final": (
        VERIFY,
        "Every agent seals what it verified, and the one seal over the whole "
        "project is the sealer's.",
        {SEALER: ONE_SEAL_IS_FINAL, WARDEN: ONE_SEAL_IS_FINAL},
    ),
    "9 a hand-back's verification claim is a claim": (
        ORCH,
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
    refuse.

    **Counted across both halves of the skill, not in one file.** #265 moved
    both places into `orchestration.md`, and a count taken in that file alone
    would go green again the day a copy moves back to `SKILL.md` — which is
    the two-answers-in-one-document shape the count exists to refuse. The sum
    is what the case was written to mean.
    """
    halves = flat(*SKILL) + " " + flat(*ORCH)
    assert halves.count(REOPENING) == 2, (
        f"the skill names the reopening subsection {halves.count(REOPENING)} "
        "times across its two halves, where its two former copies of the "
        "exception stood"
    )
    assert "`chain: capped`" in halves
    assert "`deferred #N`" in halves


# --- rule 1's fix word, and rule 6's red leg ---------------------------------


def test_a_correction_row_closes_answered_and_never_fixed():
    """Round 1's 🟡 2 of #161's own chain: `fixed <sha>` on a correction
    row leaves `nobody — the fixes are not yet written` beside a checked
    `Pass`, and the check refuses that pair on the last record — a reader
    commissioned for a row rule 1 says owes none. The owner states the
    word, and the smith's fix-table paragraph names the owner."""
    assert ("such a row closes `answered — corrected at <sha>`, never `fixed`") in flat(
        *SPEC
    )
    smith = flat(*SMITH)
    assert (
        "closes `answered` with `corrected at <sha>` as its grounds, never `fixed`"
        in smith
    )
    assert "§*The last round verifies* owns the rule" in smith


def test_the_release_leg_is_no_longer_red_until_round_ones_record_commits():
    """Round 1's ⬜ 8 asked the owner to say that window was expected, and
    #296 closed the window instead.

    The sentence this case used to require — *the `release` leg is red from
    the draft's opening until round 1's record commits*, and *that is the
    window's expected state, not a failure to chase* — was true, and was the
    defect. This file orders the draft pull request opened before round 1,
    because a reviewer needs a pull request to review, so the arm counting
    round records was red for obedience to the document beside it. A check
    like that is one people learn to route around.

    The owner now says the window is closed, and BOTH halves are asserted:
    the state prints on a draft rather than failing, and the record is still
    owed. Requiring only the first would go green over a document that had
    quietly turned the draft into a permanent exemption.
    """
    assert "That window used to be red and is not any more" in flat(*ORCH)
    assert "on a draft the missing record prints and the run exits 0" in flat(*ORCH)
    assert "Nothing that can reach `main` is exempt" in flat(*ORCH)


def test_the_release_leg_is_red_again_until_the_verifying_rounds_record_commits():
    """Round 2's ⬜ 12: the leg has a second red window, from `close`
    ticking `Pass` until the verifying round's record commits, and the
    ⬜ 8 sentence named one. The owner names both.

    Asserted through the sentence's LAST WORD since round 1's ⬜ 5 of work
    item 1788912166. It ended `expected too` — the `too` pointing at the
    first red window — and #296 closed that window, so the word was dropped.
    Dropping it is right and it is an EDIT, which is what the phase record
    that called it a restoration got wrong. The clause stopped at `record
    commits` here, so nothing was watching the half where the word lived.
    """
    assert (
        "It is red once more from `close` ticking `Pass` until the verifying "
        "round's record commits, for the reason the check prints — `Pass` "
        "beside `nobody` on the last record — and that window is expected."
    ) in flat(*ORCH)


def test_the_generator_carries_the_fenced_blocks_under_the_probes_table():
    """Round 2's 🟡 10: the spec's generator paragraph said a fenced block
    under the report's probes table stays in the report, and the rule
    beside it says the row owes the block in the record. The paragraph
    now says the generator carries the blocks, and nothing else of the
    section."""
    assert "together with every fenced block under that table" in flat(*SPEC)


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
    text = flat(*ORCH)
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
    that replaced it names the generator.

    The absence is read across both halves and the presence in the half that
    holds the sections (#265): an absence checked in one file is satisfied by
    the sentence coming back in the other.
    """
    both = flat(*SKILL) + " " + flat(*ORCH)
    assert "The habit that makes all of it moot" not in both
    assert "What makes all of it moot is the generator" in flat(*ORCH)


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
                    # `/`-joined on every platform: the callers look a key
                    # up as `"/".join(SPEC)`, and `relpath` joins with `\`
                    # on Windows (PR #168's red leg).
                    found[os.path.relpath(path, ROOT).replace(os.sep, "/")] = count
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
    for carrier in (ORCH, TEMPLATE):
        text = flat(*carrier)
        assert found.get("/".join(carrier)) == 1, found
        after = text[text.index(AT_MOST_ONE_MORE) :]
        assert REOPENING in after[:600], (
            f"{'/'.join(carrier)} carries the count rule's sentence without "
            "the owner's subsection in the same breath"
        )
    # SKILL keeps its place in the absence half: #265 moved the phrase to
    # ORCH, and the half it left must not grow a copy of the exception.
    for carrier in (SPEC, SKILL, ORCH, TEMPLATE):
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


def test_the_occurrence_keys_are_slash_joined_whatever_the_separator(monkeypatch):
    """PR #168's Windows leg, run 33962446559: `os.path.relpath` joins with
    the platform separator and the two cases above look a key up as a
    `/`-joined tuple, so both failed there and nowhere else. The separator
    is monkeypatched here so the case is red on every platform against a
    key built from `relpath` alone."""
    real = os.path.relpath
    monkeypatch.setattr(os, "sep", "\\")
    monkeypatch.setattr(
        os.path, "relpath", lambda path, start: real(path, start).replace("/", "\\")
    )
    found = occurrences("Rounds are capped at **three**")
    assert found == {"/".join(SPEC): 1}, found


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


def test_the_order_opens_the_draft_between_the_build_and_the_rounds():
    """`skills/implement/orchestration.md` §*Orchestrator: the order inside a
    ticket* is what a session reads to know what comes after the smith; a
    pull request listed last there is the dozen-rounds-on-one-platform shape
    the owner's section measured.

    The section lived in the shared checklist until #351 deleted it. The
    case moved rather than going with it, because what it pins is an ordering
    claim about the chain and not a fact about the checklist."""
    text = flat(*ORCH_IMPL)
    step = text[text.index("2. spec · plan") : text.index("3. The pull request body")]
    assert "smith → the draft pull request opens (" in step
    assert ") → warden rounds → sealer → the pull request is marked ready." in step
    assert step.index("the draft pull request opens") < step.index("warden rounds")


def test_the_order_no_longer_defers_the_framer_to_a_ticket():
    """The other half of S11 of #84. Step 2 read `spec · plan (framer, once
    #84 exists; the session until then)` -- a step written before the agent
    it names, carrying its own escape clause for the interval.

    The interval closed when `agents/framer.md` landed, and a clause saying
    the session frames the work `until then` is now an instruction to do the
    thing this work item exists to stop. It reads as current, because nothing
    in the sentence says which side of the arrival a reader is on."""
    step = flat(*ORCH_IMPL)
    step = step[step.index("2. spec · plan") : step.index("3. The pull request body")]
    assert "framer" in step, "step 2 stopped naming who draws the frame"
    for gone in ("once #84 exists", "the session until then"):
        assert gone not in step, (
            f"step 2 still carries `{gone}`. The framer ships, so the interval "
            "that clause covered is over and the escape reads as the rule"
        )


# carrier → the sentence that names the generator where the orchestrator's
# hand used to be named.
GENERATOR_NAMED = {
    PROTOCOL: "The record is written by `round_record.py new` from the reviewer's report",
    WARDEN: (
        "`round_record.py new` writes `round-N.md` from your report once the "
        "orchestrator has verified your findings"
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
