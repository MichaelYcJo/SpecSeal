"""Six words read more than one way across these documents.

Each was found at a coordinate where the reader cannot tell which meaning is
intended, and a rewrite that leaves the ambiguity is not a fix. So each word
gets ONE meaning and every coordinate is brought to it — a case per word,
asserting the pinned phrasing AND the absence of the loose one.

The absence half is what makes these cases worth having. A document can gain
the corrected sentence and keep the old one two paragraphs down, which is how
two answers ship at once.

`skills/code-review/SKILL.md` holds the second half of "the start" and of
"the cycle". It belongs to another branch and is deferred rather than
half-edited; the rows naming it are in this work item's overview.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    return " ".join(read(*parts).split())


# --- "the start" — the moment before the first edit of a work item ----------


def test_the_start_is_the_moment_before_the_first_edit():
    """Not the start of a round, and not the start of a session. A round does
    not restart it and a resumed session does not restart it."""
    for parts in (
        ("skills", "implement", "SKILL.md"),
        ("CLAUDE.md",),
        ("agents", "smith.md"),
    ):
        assert "before the first edit" in flat(*parts), "/".join(parts)


# --- "once" — every one of them states its grain ----------------------------


GRAINS = {
    "commit-review-gate": "once per session per repo",
    "review-skill-gate": "once per session per working tree",
    "worktree-guard": "once per session per repository per direction",
}


def test_every_once_in_the_readme_states_its_grain():
    """Four different grains were all spelled `once`. One session legitimately
    meets the worktree question twice, and the README read as a bug report."""
    en = flat("README.md")
    for grain in GRAINS.values():
        assert grain.lower() in en.lower(), grain
    assert "Fires once per session," not in en, (
        "a bare `once per session` cannot say which of four grains it means"
    )


def test_the_korean_readme_states_the_same_grains():
    ko = flat("README.ko.md")
    for grain in (
        "세션·레포당 한 번",
        "세션·작업트리당 한 번",
        "세션·레포·방향당 한 번",
    ):
        assert grain in ko, grain


def test_the_per_command_marker_says_per_command_in_both_readmes():
    """`[no-review]` waives ONE command. Spelled `once`, it read as once per
    session, which is a waiver nobody built."""
    assert "for **that one command**" in read("README.md")
    assert "**그 명령 하나만**" in read("README.ko.md")
    assert "skips the review gate once" not in read("README.md")


def test_the_worktree_spec_is_still_the_model():
    """It already stated its grain correctly, and the others were brought to
    it rather than the other way round."""
    spec = flat("docs", "worktree-guard-spec.md").lower()
    assert "once per session per direction" in spec


# --- "asks" — the model is instructed, the user gets buttons ----------------


def test_the_two_prompts_are_named_by_who_they_address():
    spec = flat("docs", "review-chain-spec.md")
    assert "instructs the model to put the choice up" in spec
    assert "putting two buttons to the user" in spec
    assert "A `deny` addresses the **model**" in spec
    assert "An `ask` addresses the **user**" in spec


# --- "the cycle" — the mark's unit, never the whole run ---------------------


def test_the_spec_separates_the_cycle_from_the_review_run():
    spec = flat("docs", "review-chain-spec.md")
    assert "A **cycle** is the mark's own unit" in spec
    assert "A **review run** is" in spec
    assert "## The review run has a bound, and an end" in read(
        "docs", "review-chain-spec.md"
    )
    assert "## The cycle has a bound" not in read("docs", "review-chain-spec.md"), (
        "the bound is on the review run; stated on the cycle it reads as a "
        "bound on commits"
    )


def test_the_smith_calls_the_whole_thing_a_review_run():
    smith = flat("agents", "smith.md")
    assert "the review run is bounded" in smith
    assert "the cycle is bounded" not in smith


# --- "needs no marker at all" — the one the change resolves -----------------


def test_the_row_that_could_not_be_true_is_corrected_not_reworded():
    """It was true only after the first review mark landed, and false for
    every commit before it — the defect in #52 stated as a sentence."""
    skill = read("skills", "implement", "SKILL.md")
    assert "| Through the review chain | it needs no marker at all" not in skill
    assert 'used to carry "no marker at all"' in skill, (
        "dropping the row leaves the next reader unable to tell it was wrong"
    )


# --- "the seal" — an instance names whose; the concept stays bare -----------

# The word reached three referents at once. `agents/warden.md` opened *You
# keep the seal* about `<git-dir>/specseal-reviewed`, `agents/sealer.md`
# opens *You take the seal* about the broad gate's stamp, and `README.md`
# said *the warden's audit of the seal* about a third thing again, the
# smith's proof block — two of them in files a reader opens together.
#
# The rule that resolves it is that more than one seal is CORRECT: every
# agent seals what it verified, and one of them is final. So the fix is not
# fewer seals, it is that a reference to an instance names whose.
SEAL_OWNER = ("skills", "verify", "SKILL.md")
SEAL_RULE = "## Every agent seals what it verified, and one of them is final"

# Files that instruct somebody, swept below. A record of what was true when
# it was written is not brought to a new wording, so `seal/` is not here.
SEAL_SWEPT = (
    ("agents", "sealer.md"),
    ("agents", "warden.md"),
    ("agents", "smith.md"),
    ("skills", "verify", "SKILL.md"),
    ("skills", "code-review", "orchestration.md"),
    ("skills", "code-review", "SKILL.md"),
    ("skills", "implement", "SKILL.md"),
    ("templates", "config.md"),
    ("docs", "review-chain-spec.md"),
    ("docs", "review-handoff-protocol.md"),
    ("CONTRIBUTING.md",),
    ("README.md",),
    # Added by round 1's 🟡 10, which found a FOURTH referent here — the
    # evidence ledger called `the seal itself`. The list was closed where
    # somebody had looked, which is the same shape as that round's 🟡 7 and
    # 🟡 8. The three below are what a sweep of the shipped tree turned up
    # once the list stopped being the boundary of the search.
    ("docs", "one-root-by-lifetime.md"),
    ("skills", "verify", "scripts", "seal_stamp.py"),
    ("skills", "code-review", "scripts", "round_record.py"),
)

# The two places that DISCUSS the word rather than use it: the rule's own
# section quotes the loose shape in order to forbid it, and the naming table
# quotes `"the seal"` as the product's vocabulary. Both are excluded by the
# sweep below, and each exclusion names the span it removes rather than the
# file, so a bare instance elsewhere in either file is still caught.
SEAL_VOCABULARY = ("docs", "one-root-by-lifetime.md")
SEAL_VOCABULARY_SPAN = "## Naming"

# What may follow a bare `the seal`: the concept, its formats, and the one
# sentence that names the referent in the same clause. Everything else is an
# instance with nobody's name on it.
SEAL_BARE_IS_THE_CONCEPT = (
    " Test",  # the Seal Test
    " block",  # the seal block
    "'s `cost` row",  # a field of that block
    " is a different mark and a different agent's",  # the warden's link
)


def test_the_owner_states_that_one_seal_is_final():
    """The rule the three referents were missing. It is stated once, by the
    file that holds the Seal Test and the seal block, and the two agent
    definitions link to it rather than restating it —
    `tests/test_the_rules_have_one_owner.py` is what holds that pairing."""
    owner = flat(*SEAL_OWNER)
    assert (
        "Every agent seals what it verified, and the one seal over the whole "
        "project is the sealer's."
    ) in owner
    assert "every reference to an INSTANCE names whose" in owner
    assert "The concept and its formats stay bare" in owner


def test_the_two_definitions_name_what_they_actually_keep():
    """`agents/warden.md` kept `<git-dir>/specseal-reviewed`, which is the
    mark that a review happened, and called it the seal. The rest of that
    paragraph is unchanged — a record and not a barrier, waivable without
    one, worth whatever is put behind it."""
    warden = flat("agents", "warden.md")
    assert "You keep the review mark" in warden
    assert "You keep the seal:" not in warden, (
        "the opening claims a word the sealer's definition claims two files "
        "over, and a reader opens them together"
    )
    assert "the commit gate can be waived without one" in warden, (
        "the rewrite took the paragraph's meaning with the word"
    )
    sealer = flat("agents", "sealer.md")
    assert "You take the last seal" in sealer
    assert "You take the seal." not in sealer


def test_the_readme_says_whose_seal_the_warden_audits():
    """The shape to look for: a sentence naming one party and leaving the
    audited seal anonymous. The answer there is the smith's proof block,
    three bullets from one describing the `Broad gate` cell — so a reader of
    that list met the word twice on one screen meaning two things."""
    readme = flat("README.md")
    assert "the warden's audit of the smith's seal" in readme
    assert "the warden's audit of the seal," not in readme


def test_no_instructing_document_leaves_an_instance_anonymous():
    """The absence half, swept rather than listed.

    A document can gain the corrected sentence and keep the old one two
    paragraphs down, and a rule about a word that appears this often cannot
    be held by naming the coordinates a reader happened to find. So every
    bare `the seal` in a file that instructs somebody has to be the concept
    or one of its formats; anything else names an instance and has to say
    whose.

    The owner's own rule section is excluded, and that exclusion is the
    reason this sweep is possible at all: that section quotes the loose
    shape in order to forbid it, which is the one place the bare phrase is
    doing its job."""
    for parts in SEAL_SWEPT:
        # Flattened, so a suffix that happens to straddle a line wrap is
        # still read as the phrase it is.
        text = flat(*parts)
        if parts == SEAL_OWNER:
            head, _, rest = text.partition(SEAL_RULE)
            text = head + rest.partition(" ## ")[2]
        if parts == SEAL_VOCABULARY:
            head, _, rest = text.partition(SEAL_VOCABULARY_SPAN)
            text = head + rest.partition(" ## ")[2]
        lowered = text.lower()
        start = 0
        while (hit := lowered.find("the seal", start)) != -1:
            start = hit + 1
            after = text[hit + len("the seal") :]
            if after[:1].isalpha():  # the sealer, the sealed tree
                continue
            assert after.startswith(SEAL_BARE_IS_THE_CONCEPT), (
                f"{'/'.join(parts)} says `the seal` and leaves the instance "
                f"anonymous: ...{' '.join(text[hit - 60 : hit + 60].split())}..."
            )
