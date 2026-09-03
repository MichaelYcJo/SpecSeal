"""The one-broad-run rule spans six documents; drift between them is the bug.

The skill states it, the agent contract binds every agent to it, the smith
follows it, the warden audits it, two records carry it to the next session,
and the preset block states it for a session that loads none of them. A rule
spread this wide fails by one of them quietly dropping its part, which is
invisible in any single diff.

Phases 3 and 4 of #107 moved the prohibition and the refusal out of the two
agent definitions and into `skills/agent-contract/SKILL.md`. The cases moved
with them rather than being deleted: what each definition still holds is its
own APPLICATION -- the warden audits the label and has a named field for the
question, the smith puts both answers in a hand-back the caller can reply in
-- and a case asserting the same sentence in two files is the duplication the
contract was written to end. That duplication has its own module now,
`tests/test_a_moved_rule_leaves_its_definition.py`, because until phase 4
nothing in the tree noticed a moved rule being pasted back.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def flat(*parts):
    """The file as one line, so an assertion is not pinning where it wraps."""
    return " ".join(read(*parts).split())


# U+2013 EN DASH, built rather than typed. The definitions spell every ratio
# range with one, so a hyphen would match nothing; a typed one is what the
# linter reads as an ambiguous character.
DASH = chr(0x2013)


def test_verify_says_when_not_only_what():
    scope = read("skills", "verify", "SKILL.md")
    assert "## Scope" in scope, "verify lost the section that bounds the moment"
    for row in (
        "Each slice",
        "Phase boundary",
        "Handoff to review",
        "After the rounds settle",
    ):
        assert row in scope, f"the Scope table lost its `{row}` row"
    assert "against the base commit" in scope
    assert "Nothing edits between the broad seal and the PR" in scope


def test_the_broad_gate_section_states_its_own_timing():
    """The Scope table settles when the gate fires; the section did not repeat
    it, and a session that jumped to the section by its heading ran the whole
    suite before review. Two sessions did exactly that, 22 minutes between
    them, and both seals were void by the first review finding.

    The baseline is the same failure one step further in: it is reached for
    once an unexplained failure appears, not before one exists."""
    scope = read("skills", "verify", "SKILL.md")
    section = scope.split("## The broad gate")[1].split("\n## ")[0]
    flat = " ".join(section.split())  # re-wrapping a paragraph is not a regression
    assert "after the review rounds settle" in flat, (
        "the broad gate section stopped saying when it fires"
    )
    assert "Nothing broad runs at the handoff to review" in flat, (
        "the section stopped ruling out the run that review rounds void"
    )
    assert "once an unexplained failure appears" in flat, (
        "the baseline stopped naming the event that calls for it"
    )


def test_verify_prices_the_run_that_repeats():
    """Scope decides how often; it says nothing about what each run costs, and
    the narrow run is the one that multiplies."""
    scope = read("skills", "verify", "SKILL.md")
    assert "## The cost of the run you repeat" in scope
    assert "recipe in a comment" in scope  # line-wrapped in the source
    assert "Capture once, filter locally" in scope, (
        "re-running a check to see its output differently returns nothing new"
    )


def test_the_smith_carries_the_batching_rule_it_actually_spends():
    """Re-pointed in phase 4 of #107; it used to read the prohibition here.

    The old premise was that the agent file is always in front of the smith
    while the skill may not be. That premise stopped separating the two: the
    contract arrives through the same `skills:` frontmatter the definition
    does, so it is in front of the smith exactly as often. What is left for
    the definition is the half the contract sends BACK to it -- §10 says the
    numbers that judge each agent live in that agent's definition, because a
    figure that measures a reviewer does not measure an implementer.

    A number with no home is the failure here, not a rule with no copy. An
    edit-test loop that is judged by the reviewer's 1.8 bar is being asked
    for something a serial loop cannot give, which is how a rule stops being
    read at all."""
    smith = flat("agents", "smith.md")
    assert f"1.08{DASH}1.17" in smith, (
        "the implementer's own measured ratio went, and the only number left "
        "in the tree is the one that judges a reviewer"
    )
    assert f"1.29{DASH}1.89" in smith, (
        "the comparison went; a bare 1.08-1.17 reads as a target rather than "
        "as what a serial loop can give"
    )
    assert "§10" in smith, "the implementer can no longer reach the rule"


def test_the_smith_puts_both_answers_in_the_hand_back():
    """What stayed with the implementer when §2 and §3 moved.

    The rule is the contract's and is asserted against it below. This is the
    half that is nobody else's: WHERE the two answers land. The smith's
    handover is a conversation the caller can reply in, so the unverified
    suite and a declined instruction both go in as prose -- which is exactly
    why the warden, whose handover is a report, needed a named field for the
    same sentence and has one.

    Round 1 of the original rule found `Decline` separable from `name`: a
    refusal nobody is told about is the same 28 minutes with a footnote. The
    disclosure half is asserted here because the smith is where it is
    disclosed."""
    smith = flat("agents", "smith.md")
    assert "§2" in smith and "§3" in smith, (
        "the implementer can no longer reach the rules its hand-back answers"
    )
    assert "labeled `unverified`" in smith, (
        "the suite stopped going over labelled, and a suite that is simply "
        "not mentioned reads as a suite that passed"
    )
    assert "the orchestrator named as its answerer" in smith, (
        "the label lost its answerer, and a deferral to nobody is how "
        "`someone will look at it` becomes `nobody did`"
    )
    assert "what was asked, and which rule refused it" in smith, (
        "the declined instruction stopped being disclosed, which is how an "
        "override stays invisible"
    )
    assert "hand-back" in smith, (
        "the destination went. Without it §3's disclosure sentence has "
        "nowhere named to land, which is the gap the warden's field fills"
    )


def test_the_prohibition_itself_has_one_home_and_it_is_the_contract():
    """Phase 3 of #107 re-pointed this case; it used to read `agents/warden.md`.

    The prohibition was stated in two definitions in near-identical words and
    a third agent inherited neither, which is the duplication the contract
    exists to end. The rule moved; the case moved with it rather than being
    deleted, because a moved rule with no case is a rule that can be moved
    again into nothing."""
    contract = " ".join(read("skills", "agent-contract", "SKILL.md").split())
    assert "is the orchestrator's, run once, after the review rounds settle" in (
        contract
    ), "the contract stopped saying whose the broad gate is and when it fires"
    assert "Hand over with the suite labelled `unverified`" in contract, (
        "the label went, and a suite that is simply not mentioned reads as a "
        "suite that passed"
    )


def test_the_warden_audits_the_scope_of_a_seal():
    """What stayed with the reviewer: the audit, which is nobody else's.

    §2 says the reviewer does not run the suite. It does not say what the
    reviewer does INSTEAD, and that half is an application of the rule rather
    than the rule -- a seal is audited by the second person looking, and the
    warden is the only agent that is one."""
    warden = " ".join(read("agents", "warden.md").split())
    assert "whether that label is honest" in warden, (
        "the reviewer stopped being told to audit the label, so the only "
        "thing left is the prohibition and the seal goes unchecked"
    )
    assert "not whether the number is green" in warden, (
        "the audit lost the half that says what it is NOT -- a green number "
        "read as an honest label is the failure the audit exists to catch"
    )


def test_the_refusal_is_stated_once_and_names_both_directions():
    """Re-pointed in phase 3 from a per-agent loop over smith and warden.

    Round 2's finding stands and is now the contract's to hold: the rule
    reached a second file and the REFUSAL half did not follow it, so the
    principle and the disclosure alone read as `run it, but say so`. Both
    halves are asserted, plus the default for an instruction that cannot be
    classified -- a default nothing holds is the same as no default."""
    contract = " ".join(read("skills", "agent-contract", "SKILL.md").split())
    assert "do not run it" in contract, (
        "the refusal half went; the principle and the disclosure alone read "
        "as `run it, but say so`"
    )
    assert "Decline, and name the instruction in your handover" in contract, (
        "`Decline` became separable from `name`, which is the state that was "
        "measured -- the run happened and the caller believed the prompt was "
        "honoured"
    )
    assert "run nothing extra and ask in the handover" in contract, (
        "the contract lost the default for an instruction it cannot classify, "
        "so the rule above it decides nothing in the one case that needed "
        "deciding"
    )
    assert "rather than refusing outright" in contract


def test_the_reviewer_has_a_field_for_the_question_the_default_produces():
    """The reviewer needs somewhere for that question to LAND.

    Its handover is a report, not a conversation -- unlike the smith's, which
    returns through the chain -- so an unanswered axis would otherwise be
    sealed over by the orchestrator that reads the report. That is why this
    half stayed in `agents/warden.md` when the rule above it left."""
    warden = " ".join(read("agents", "warden.md").split())
    assert "out of verified scope" in warden, (
        "the reviewer asks a question with no field to ask it in, and a seal "
        "gets taken over an axis nobody decided"
    )
    assert "a report rather than a conversation" in warden, (
        "the reason the field exists went, and a field with no reason is the "
        "next one a rewrite drops"
    )


def test_the_broad_gate_state_survives_a_handoff():
    """A session joining at round 3 cannot see which commands were run."""
    assert "| Broad gate |" in read("docs", "review-handoff-protocol.md"), (
        "round-N.md lost the field that tells the next session whether the one "
        "broad run already happened"
    )
    assert "broad-gate state" in read("skills", "code-review", "SKILL.md"), (
        "the reference implementation stopped recording what the protocol wants"
    )
    assert "broad gate:" in read("skills", "verify", "SKILL.md"), (
        "the seal block stopped carrying the state the record needs"
    )


def test_the_seal_reports_what_the_checks_cost():
    """Nobody notices the runner eating the session from inside it."""
    assert "· cost:" in read("skills", "verify", "SKILL.md")


def test_the_preset_block_states_the_rule_the_loaded_files_assume():
    """Every other home for this rule loads on demand.

    An agent file needs the agent spawned and a skill needs the skill invoked.
    A session working this repo directly does neither, so the preset block --
    always in front of it -- is the only copy it will ever read."""
    preset = read("CLAUDE.md").split("<!-- specseal:end -->")[0]
    assert "<!-- specseal:start -->" in preset, "the preset markers moved"
    assert "Verification Scope" in preset, (
        "the always-loaded block lost the rule that bounds a broad run"
    )
    assert "Batch independent reads and runs" in preset, (
        "the always-loaded block lost the batching rule"
    )
