"""File edits go through the `Edit` tool, and the rule says why.

Nothing pinned this prose when it landed. `grep -rn "nothing to read" tests/`
returned zero lines, so deleting both paragraphs left the suite green — and
those paragraphs are the whole of issue #34's fix, which changes no code. A
change that ships only as instructions has to be held by something, or the
next sweep through these files removes it and nothing notices.

Round 1 also found the first version diagnosing the wrong mechanism. It said
the gate trips because a repository's test fixtures are shell command
strings. Measured: a whole fixture file handed to `_hides_a_commit` is clean,
while `agents/smith.md` and `README.md` both TRIP on their own `[no-review]`
waiver examples. What the reader counts is a body segment whose command word
is `git` with the `commit` subcommand (`hooks/commit-review-gate.py:144-147`,
assembled in `commit_invocations` at `:262-286`). Two kinds of edit put such
a segment in a body: a partial patch to a file carrying shell commands as
test data, where the quoting of that fragment can leave a commit in command
position, and a patch to a document showing a waiver example verbatim.

So each case asserts the pinned phrasing AND the absence of the loose one,
following `tests/test_one_word_one_meaning.py:6`. A document can gain the
corrected sentence and keep the wrong one two paragraphs down, which is how
two answers ship at once.

Phases 3 and 4 of #107 re-pointed both halves. The rule is §9 of the agent
contract now, which every agent receives at startup, and each definition
keeps only its own application — for `agents/warden.md` that a probe script
and a scratch fixture are edits too, for `agents/smith.md` that it edits more
than anyone and its own waiver example is the shape the gate reads a commit
out of. So the four cases below assert one carrier, not three: a case
asserting the same sentence in two files is the duplication the contract was
written to end, and `tests/test_a_moved_rule_leaves_its_definition.py` is
what now refuses it.
"""

import os

from conftest import load_hook_module

ROOT = os.path.join(os.path.dirname(__file__), "..")
CONTRACT = ("skills", "agent-contract", "SKILL.md")
SMITH = ("agents", "smith.md")
CARRIERS = (CONTRACT,)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    """The file as one line, so an assertion is not pinning where it wraps."""
    return " ".join(read(*parts).split())


def test_the_rule_names_the_tool_and_pairs_its_two_reasons():
    """The instruction itself, in each file that states it."""
    for parts in CARRIERS:
        text = flat(*parts)
        who = "/".join(parts)
        assert "`Edit` tool" in text, f"{who} stopped naming the tool"
        # The whole clause, which phase 4 could tighten and phase 3 could
        # not. Two files stated the pairing in two spellings -- the contract's
        # `Two reasons point the same way` and the smith's `for two reasons
        # that point the same way` -- so the shared fragment was all either
        # could be pinned to, and a sentence that kept the fragment while
        # losing the count would have passed. One carrier means one spelling,
        # and the split is settled by there being nothing left to disagree
        # with rather than by choosing between them.
        assert "Two reasons point the same way" in text, (
            f"{who} lost the pairing. One reason alone reads as a style "
            "preference, and the gate half is the one no other document says"
        )


def test_the_rule_names_the_second_reason():
    """Reason 1 is in `skills/implement/SKILL.md`; reason 2 is only here.

    The warden never loads `implement`, so for every agent this is the only
    place either reason is stated at all — which is why it is a contract
    section rather than a paragraph in one definition.
    """
    for parts in CARRIERS:
        text = flat(*parts)
        who = "/".join(parts)
        assert "no Bash command line exists" in text, (
            f"{who} lost reason 2 — that an edit made through the tool "
            "leaves the commit gate nothing to read"
        )
        assert "nothing to read" in text, f"{who} lost the consequence"


def test_the_rule_states_what_the_gate_actually_applies():
    """Round 1's finding 1: the mechanism, not either example of it.

    The absence half matters more than usual here. The loose diagnosis is
    plausible and was believed by two readers, so a file can gain the rule
    and keep the wrong explanation beside it.
    """
    for parts in CARRIERS:
        text = flat(*parts)
        who = "/".join(parts)
        assert "command word is `git`" in text, (
            f"{who} stopped saying what the reader counts. Without the "
            "command-word rule, a reader cannot tell why a whole fixture "
            "file is clean and a fragment of one is not"
        )
        assert "command position" in text, (
            f"{who} lost the half that explains why only some fragments trip"
        )
        for loose in (
            "test fixtures are themselves shell command strings",
            "that reading finds a commit in a patch",
        ):
            assert loose not in text, (
                f"{who} still carries the refuted diagnosis: {loose!r}. "
                "A whole fixture file is clean; measured in round 1"
            )


def test_the_rule_names_the_branch_that_has_no_commit_in_it():
    """Round 2's finding 1: the command-word rule is one branch of two.

    A segment the reader cannot expand counts the same way, so `eval "$CMD"`
    stops the session with no `git` anywhere in the body
    (`hooks/commit-review-gate.py:148-150`, resolved by
    `_eval_hides_a_commit` at `:176-188` against `EXPANDS` at
    `hooks/cmdline.py:678`). Measured: `eval "$CMD"` TRIPS, `eval $(cat f)`
    TRIPS, `eval "echo hello"` is clean because it holds no expansion
    character.

    Stating only the first branch is worse than stating neither. A session
    that reads it searches its patch for a commit, finds none, proceeds, and
    meets the prompt anyway — which is the failure this work item exists to
    remove, arriving through the fix for it.
    """
    for parts in CARRIERS:
        text = flat(*parts)
        who = "/".join(parts)
        assert "`eval`" in text, (
            f"{who} names only the command-word branch. A reader following "
            "it clears a patch that still stops the session"
        )
        assert "reduces to without running the shell" in text or (
            "cannot expand" in text
        ), (
            f"{who} lost the rule behind the example — an `eval` mentioned "
            "without saying WHY it counts reads as a special case"
        )


def test_no_carrier_claims_a_fact_about_the_reader_repository():
    """Round 1's finding 2.

    These files ship as a plugin and are read inside repositories that have
    no `hooks/commit-review-gate.py` at all. `This repository's are` is a
    claim about the READER's repository, and it is false there. The memo
    records the same reasoning for keeping the line coordinate out.
    """
    for parts in (*CARRIERS, SMITH, ("agents", "warden.md")):
        text = flat(*parts)
        who = "/".join(parts)
        for loose in (
            "This repository's are",
            "and this one's are",
            "the gate's own tests are where they cluster",
        ):
            assert loose not in text, (
                f"{who} asserts something about the repository it is read in: {loose!r}"
            )


def test_the_reviewer_keeps_the_half_that_makes_the_rule_its_own():
    """What stayed in `agents/warden.md` when §9 took the rest.

    A reviewer edits less than an implementer and would read a rule about
    edits as somebody else's. Its paragraph is the one that names what its
    own edits are — a probe script, a scratch fixture, a file patched to see
    whether a finding reproduces — and without it the contract's §9 arrives
    at an agent that does not think it is addressed.
    """
    warden = flat("agents", "warden.md")
    assert "§9" in warden, "the reviewer can no longer reach the rule"
    assert "scratch fixture" in warden, (
        "the reviewer stopped being told which of its own acts are edits"
    )


def test_the_implementer_keeps_the_half_that_makes_the_rule_its_own():
    """What stayed in `agents/smith.md` when §9 took the rest.

    The reviewer's half answers *are my acts edits at all*. The smith never
    had that doubt — it is the agent that edits — so its half is the other
    end of the same reason: which of the documents in front of it is the one
    the gate reads a commit out of. Its own routing paragraph is that
    document, and the RIDER beside it is why the example stays.
    """
    smith = flat(*SMITH)
    assert "§9" in smith, "the implementer can no longer reach the rule"
    assert "waiver" in smith and "RIDER" in smith, (
        "the smith stopped being told that its own waiver example is the "
        "patch the gate reads a commit out of, which is the one instance of "
        "§9 that is nobody else's"
    )


def test_the_contract_file_does_not_itself_trip_the_commit_gate():
    """A patch to the file carrying the waiver example must not become the
    thing it warns about.

    Re-pointed in phase 3 of #107. `agents/warden.md` used to carry the
    `[no-review]` example in its probe table and was asserted here; §8 of the
    contract carries it now. The hazard did NOT come with it unchanged, and
    saying it had would have been a case that cannot fail — measured while
    re-pointing: the warden's apostrophe mutation (`the fragment's own
    quoting`, which flipped its quote state and pushed its table row into
    command position) leaves the contract clean at 21 apostrophes, whether
    the paragraph goes above §1 or above §8.

    What differs is the example itself. The warden's table row spelled the
    waiver AND the command it waives on one line, so a quote flip had a
    `git commit` to promote. §8 writes the token without a command after it,
    so today there is nothing to promote. That is the state this case holds:
    the realistic edit is a future one completing the example, and it trips
    immediately. `agents/smith.md` is deliberately not asserted — it has
    tripped at its own waiver example since before this work, and pinning
    that would be pinning a defect as a requirement.
    """
    gate = load_hook_module("commit-review-gate.py", "crg_edit_tool")
    text = read(*CONTRACT)
    assert ": '[no-review]';" in text, (
        "the example this case exists to guard is gone; the case would pass "
        "on a file that no longer carries the hazard"
    )
    assert not gate._hides_a_commit(text), (
        "the agent contract now reads as carrying a commit. An odd number of "
        "apostrophes in added prose flips the reader's quote state, which "
        "puts the `[no-review]` example in §8 into command position — a "
        "session patching this file would meet the gate"
    )


def test_the_reviewer_file_still_does_not_trip_the_gate():
    """The warden lost the waiver example with §8, and must stay clean."""
    gate = load_hook_module("commit-review-gate.py", "crg_edit_tool")
    assert not gate._hides_a_commit(read("agents", "warden.md"))
