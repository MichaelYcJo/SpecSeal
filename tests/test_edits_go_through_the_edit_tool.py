"""The two agent files route file edits through the `Edit` tool, and say why.

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
"""

import os

from conftest import load_hook_module

ROOT = os.path.join(os.path.dirname(__file__), "..")
AGENTS = (("agents", "smith.md"), ("agents", "warden.md"))


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    """The file as one line, so an assertion is not pinning where it wraps."""
    return " ".join(read(*parts).split())


def test_both_agent_files_route_file_edits_through_the_edit_tool():
    """The instruction itself, in the two files a spawned agent reads."""
    for parts in AGENTS:
        text = flat(*parts)
        who = parts[-1]
        assert "`Edit` tool" in text, f"{who} stopped naming the tool"
        assert "two reasons that point the same way" in text, (
            f"{who} lost the pairing. One reason alone reads as a style "
            "preference, and the gate half is the one no other document says"
        )


def test_both_agent_files_name_the_second_reason():
    """Reason 1 is in `skills/implement/SKILL.md`; reason 2 is only here.

    The warden never loads `implement`, so for that file this is the only
    place either reason is stated at all.
    """
    for parts in AGENTS:
        text = flat(*parts)
        who = parts[-1]
        assert "no Bash command line exists" in text, (
            f"{who} lost reason 2 — that an edit made through the tool "
            "leaves the commit gate nothing to read"
        )
        assert "nothing to read" in text, f"{who} lost the consequence"


def test_both_agent_files_state_the_rule_the_gate_actually_applies():
    """Round 1's finding 1: the mechanism, not either example of it.

    The absence half matters more than usual here. The loose diagnosis is
    plausible and was believed by two readers, so a file can gain the rule
    and keep the wrong explanation beside it.
    """
    for parts in AGENTS:
        text = flat(*parts)
        who = parts[-1]
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


def test_both_agent_files_name_the_branch_that_has_no_commit_in_it():
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
    for parts in AGENTS:
        text = flat(*parts)
        who = parts[-1]
        assert "`eval`" in text, (
            f"{who} names only the command-word branch. A reader following "
            "it clears a patch that still stops the session"
        )
        assert "cannot expand" in text, (
            f"{who} lost the rule behind the example — an `eval` mentioned "
            "without saying WHY it counts reads as a special case"
        )


def test_neither_agent_file_claims_a_fact_about_the_reader_repository():
    """Round 1's finding 2.

    These files ship as a plugin and are read inside repositories that have
    no `hooks/commit-review-gate.py` at all. `This repository's are` is a
    claim about the READER's repository, and it is false there. The memo
    records the same reasoning for keeping the line coordinate out.
    """
    for parts in AGENTS:
        text = flat(*parts)
        who = parts[-1]
        for loose in (
            "This repository's are",
            "and this one's are",
            "the gate's own tests are where they cluster",
        ):
            assert loose not in text, (
                f"{who} asserts something about the repository it is read in: {loose!r}"
            )


def test_the_warden_file_does_not_itself_trip_the_commit_gate():
    """A patch to this file must not become the thing it warns about.

    `agents/warden.md` carries a `[no-review]` waiver example in its probe
    table, and that line alone is counted. The whole file is not, because the
    single quotes around the example are balanced by the rest of the
    document — and THAT is what an edit here can break.

    Measured while fixing round 1: adding one paragraph containing a single
    apostrophe (`the fragment's own quoting`) flipped the quote state for
    everything after it and pushed the waiver row into command position, so
    the whole file started tripping. `agents/smith.md` is deliberately not
    asserted here — it has tripped at its own waiver example since before
    this work, and pinning that would be pinning a defect as a requirement.
    """
    gate = load_hook_module("commit-review-gate.py", "crg_edit_tool")
    text = read("agents", "warden.md")
    assert not gate._hides_a_commit(text), (
        "agents/warden.md now reads as carrying a commit. An odd number of "
        "apostrophes in added prose flips the reader's quote state, which "
        "puts the `[no-review]` example in its probe table into command "
        "position — a session patching this file would meet the gate"
    )
