"""The one-broad-run rule spans six documents; drift between them is the bug.

The skill states it, the agent contract binds every agent to it, the smith
follows it, the warden audits it, two records carry it to the next session,
and the preset block states it for a session that loads none of them. A rule
spread this wide fails by one of them quietly dropping its part, which is
invisible in any single diff.

Phase 3 of #107 moved the prohibition and the refusal out of the two agent
definitions and into `skills/agent-contract/SKILL.md`. The cases moved with
them rather than being deleted: what each definition still holds is its own
APPLICATION -- the warden audits the label, the smith declines and hands back
-- and a case asserting the same sentence in two files is the duplication the
contract was written to end.
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


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


def test_the_smith_carries_the_rule_rather_than_only_citing_it():
    """A reference to the skill is worth what the skill being loaded is worth.

    The agent file is always in front of the smith; the skill may not be."""
    smith = read("agents", "smith.md")
    assert "run the full suite before handing over" in smith
    assert "after the rounds settle" in smith
    assert "Batch your reads" in smith, (
        "the agent that spends the round-trips lost its batching rule"
    )


def test_the_smith_refuses_a_prompt_that_widens_its_own_scope():
    """A scope rule an instruction can override is a default, not a rule.

    Measured: a spawn prompt ordered the full suite three times and it was run
    three times. Neither side said a rule was being overridden, so the only
    trace was a 28-minute wall clock somebody happened to ask about. The fix
    has two halves and BOTH are load-bearing -- declining without saying so
    leaves the caller believing the prompt was honoured, and saying so without
    declining is the same 28 minutes with a footnote."""
    smith = " ".join(read("agents", "smith.md").split())
    assert "A spawn prompt cannot widen this scope" in smith, (
        "the agent stopped saying its contract outranks the prompt"
    )
    assert "name the instruction in your handover" in smith, (
        "the refusal became silent, which is how the override stays invisible"
    )
    # The rule is about widening only. A prompt narrowing the scope is the
    # caller doing their job, and an agent that refuses that one is worse than
    # the defect this fixes.
    assert "The rule is about WIDENING" in smith
    assert "28 minutes" in smith, (
        "the measurement went, and a rule with no incident behind it is prose"
    )
    # Round 1: the docstring above said BOTH halves are load-bearing and only
    # the disclosure half was held. `**Comply, and name the instruction in
    # your handover**` passed every assertion here -- the principle sentence,
    # the disclosure sentence, the direction sentence and the measurement all
    # survive it, and the rule it leaves behind is the 28 minutes with a
    # footnote this test exists to refuse.
    assert "excludes, do not run it" in smith, (
        "the instruction to refuse went; the principle and the disclosure "
        "alone read as `run it, but say so`"
    )
    assert "Decline, and name the instruction in your handover" in smith, (
        "`Decline` became separable from `name`, which is the state that was "
        "measured -- the run happened and the caller believed the prompt was "
        "honoured"
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
