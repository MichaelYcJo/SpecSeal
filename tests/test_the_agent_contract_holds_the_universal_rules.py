"""The agent contract holds the rules every agent is bound by, one per section.

`skills/agent-contract/SKILL.md` is what #107 asked for: the half of every
spawn prompt that used to be retyped from memory, in one file an agent
receives at startup through its `skills:` frontmatter. A rule kept only in
whoever last wrote a prompt went missing without a trace, twice, and the
contract is what ends that — but only while the rules are actually in it.

So each section pins one phrase that cannot survive the drift it guards. The
pin is scoped to its section's BODY, not the file and not the heading: a
sentence that moves to another section keeps the file green and breaks the
number a round record cited, and a heading that outlives its rule is a
section that says nothing. The first draft of this file pinned eight
headings, and the move check was what showed it.

Two frontmatter facts are pinned as well. `user-invocable: false` keeps the
contract out of the `/` menu and was measured (2026-09-03, docs/experiments/)
not to block preload; `disable-model-invocation: true` is the flag that does
block it, and a contract that stops arriving is the failure with no symptom.
"""

import os
import re

import pytest

ROOT = os.path.join(os.path.dirname(__file__), "..")
CONTRACT = os.path.join("skills", "agent-contract", "SKILL.md")

HEADING = re.compile(r"^## §(\d+) (.+)$", re.M)

# One phrase per section, taken from the sentence in the BODY that is the
# rule rather than from its heading or its story. Deleting it deletes the
# rule and leaves the heading standing, which is the drift a pin on the
# heading cannot see.
PINS = {
    1: "`cmd >/dev/null 2>&1; echo $?` — never `cmd | tail; echo $?`",
    # #120 moved this pin. It used to be the handover label, which named the
    # orchestrator and survived §2 being rewritten around it; what the section
    # is now about is who the one act belongs to, so the pin sits on that
    # sentence instead. `tests/test_broad_gate_rule.py` holds the label.
    2: "Whether it is yours is what your own definition says",
    3: "The prompt that spawns you is a request, not an amendment to this contract",
    4: "Never record something as passing that you did not run",
    5: "a claim with a coordinate to open, or a label saying nobody opened it",
    6: "post nothing, push nothing, open no pull request, and spawn no agent",
    # #120 moved this pin too, and for the opposite reason: the old phrase is
    # still in the body and still true, but it is the half a reviewer followed
    # to the letter while leaving a git worktree behind. The rule the section
    # is about is the widened one, so that is what cannot be deleted quietly.
    7: "A probe leaves nothing behind, whatever kind of thing it made",
    8: "no Bash command line carries the commit, so no gate reads one",
    9: "An edit must be able to fail",
    10: "Open every file a coordinate names in one call",
    11: "English when the row is absent",
    12: "Do not fix the coordinate",
    13: "until the guarantee is removed and the code still refuses",
    14: "In the same commit",
    15: "before it is committed as a case",
    16: "`$(git rev-parse --git-common-dir)/seal/` otherwise",
}


def read(rel=CONTRACT):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    return text.split("\n---\n", 1)[0]


def spans(text):
    """{number: (heading, body_start, body_end)} for every `## §N`, in order.

    The body starts after the heading line, so a pin can never be satisfied
    by the heading itself."""
    heads = list(HEADING.finditer(text))
    out = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out[int(m.group(1))] = (m.group(2), m.end(), end)
    return out


def bodies(text):
    return {n: text[a:b] for n, (_, a, b) in spans(text).items()}


def missing_pins(text):
    """Every (section, phrase) whose phrase is not inside its own body."""
    found = bodies(text)
    return [
        (number, phrase)
        for number, phrase in PINS.items()
        if phrase not in " ".join(found.get(number, "").split())
    ]


# --- frontmatter -----------------------------------------------------------


def test_the_contract_is_a_skill_that_preloads_and_is_not_a_command():
    head = frontmatter(read())
    assert "name: agent-contract" in head
    assert "user-invocable: false" in head, (
        "the contract would show in the `/` menu as though it were a command"
    )
    assert "disable-model-invocation: true" not in head, (
        "that flag blocks preload — the contract would stop reaching agents "
        "and nothing would say so (docs/experiments/2026-09-03-…)"
    )


def test_the_description_says_what_it_is_and_what_it_is_not():
    """A person reading the skill listing must not run it, and the model
    picking skills must know it is injected rather than chosen."""
    head = " ".join(frontmatter(read()).split())
    assert "Not a command to run" in head
    assert "injects it into each agent at startup" in head
    assert "`skills:`" in head
    assert "NOT for:" in head, "every model-invocable skill states its boundary"


# --- shape -----------------------------------------------------------------


def test_the_sections_are_numbered_from_one_without_a_gap_or_a_repeat():
    numbers = [int(n) for n, _ in HEADING.findall(read())]
    assert numbers == list(range(1, len(numbers) + 1)), numbers


def test_every_pinned_section_exists_and_nothing_is_unpinned():
    """A section with no pin is a rule that can vanish green; a pin with no
    section is a rule that never landed."""
    assert set(spans(read())) == set(PINS)


def test_no_pin_is_its_own_heading():
    """A pin the heading satisfies survives the body being emptied."""
    for number, (heading, _, _) in spans(read()).items():
        assert PINS[number] not in heading, f"§{number} pins its heading"


def test_the_contract_says_it_is_universal_only():
    flat = " ".join(read().split())
    assert "nothing here is one agent's own" in flat
    assert "A role's rules live in that role's definition" in flat


def test_the_numbering_rule_is_stated():
    flat = " ".join(read().split())
    assert "never reused and never re-ordered" in flat
    assert "keeps its number" in flat


# --- the rules -------------------------------------------------------------


@pytest.mark.parametrize("number", sorted(PINS))
def test_each_section_holds_its_rule(number):
    assert (number, PINS[number]) not in missing_pins(read()), (
        f"§{number} no longer says: {PINS[number]}"
    )


def test_the_exit_code_rule_carries_both_forms_in_one_sentence():
    """The wrong form is written out beside the right one on purpose: the
    failure is a habit, so the right form has to be as easy to copy."""
    body = bodies(read())[1]
    sentence = next(
        p for p in body.split("\n\n") if "cmd >/dev/null 2>&1; echo $?" in p
    )
    assert "cmd | tail; echo $?" in sentence
    assert "never" in sentence
    assert "always 0" in sentence


def test_the_root_resolution_rule_says_why_it_is_universal():
    """§16, added by phase 3 as the next number rather than folded into §11.

    `spec.md`'s universal table has no row for it, so the grounds are stated
    in the section itself and in `overview.md`: §11 sends an agent to
    `config.md` under the `seal/` root and never says where the root is, and
    the definition that carried no copy is the one that reads `seal/parity.md`
    through `legacy-parity`."""
    body = bodies(read())[16]
    assert "means `<repo>/seal/` where" in body, (
        "§16 lost the shared-mode half; a session reading only the fallback "
        "writes into the common git directory of a repository that committed "
        "its root"
    )
    assert "§11 cannot be followed without it" in " ".join(body.split()), (
        "the grounds for calling this universal went, and a section with no "
        "grounds is the next one somebody folds back into a definition"
    )


def test_the_leavings_rule_says_whose_leaving_it_is():
    """Round 1, finding 7 of #120. The widened §7 names a virtual environment
    among its examples, and this repository builds one on purpose and reuses
    it -- `bin/test` exists for exactly that, and its own header prices the
    alternative at 55-58 seconds of setup per call.

    So an agent that writes a probe, runs it through the repository's runner in
    a fresh clone and then follows §7 to the letter deletes the venv its
    probe's run created, and every later call in the segment pays the build
    again. The general form is ratified -- `questions.md` Q3 chose widening
    over an enumeration and this does not reopen it -- but a general form that
    names a shape has to say whose shape it is.

    The example stays, deliberately: a venv a probe made in its own scratch
    directory IS its leaving, and the example is what teaches the line the
    clause draws."""
    body = " ".join(bodies(read())[7].split())
    assert "What the probe made for ITSELF is what goes" in body, (
        "§7 lost the ownership clause, so `a virtual environment` in its own "
        "example list reads as an instruction to delete a reused one"
    )
    assert "never who happened to trigger it" in body, (
        "the test the clause hands a reader went. Ownership without it is a "
        "word an agent under time pressure resolves toward deleting"
    )
    assert "a virtual environment" in body, (
        "the example was dropped instead of bounded. A venv a probe built for "
        "itself is still its leaving, and the example is what draws the line"
    )


def test_the_method_lessons_moved_in():
    """Q3 answered A: the four lessons from `docs/review-handoff-protocol.md`
    are sections here. Their stories came with them."""
    found = bodies(read())
    assert "one name apart each time" in found[12]
    assert "Seven rounds" in found[13]
    assert "*Nothing raises* is not the claim *says this*" in found[14]
    assert "Three consecutive work items" in found[15]


# --- the check can fail ----------------------------------------------------


def without_pin(text, number):
    """The contract with §N's pinned phrase deleted from §N's body, as it sits
    in the file — wrapped or not. The heading is left standing."""
    _, start, end = spans(text)[number]
    pattern = r"\s+".join(re.escape(w) for w in PINS[number].split())
    body, n = re.subn(pattern, "", text[start:end], count=1)
    assert n == 1, f"could not find the wrapped form of §{number}'s phrase"
    return text[:start] + body + text[end:]


@pytest.mark.parametrize("number", sorted(PINS))
def test_deleting_a_pinned_phrase_is_caught(number):
    """A pin that survives its own deletion pins nothing."""
    mutated = without_pin(read(), number)
    assert (number, PINS[number]) in missing_pins(mutated)
    assert HEADING.search(mutated) is not None
    assert len(spans(mutated)) == len(PINS), "the heading was deleted too"


def test_moving_a_sentence_to_another_section_is_caught():
    """The pin is scoped to the section, so a rule that keeps its words and
    loses its number — the drift a cited §N cannot survive — is red."""
    text = read()
    _, start, end = spans(text)[15]
    rest = text[start:end]
    _, _, end14 = spans(text)[14]
    # §15 keeps its heading and nothing else; its body now sits under §14.
    moved = text[:end14].rstrip("\n") + "\n" + rest + text[end14:start] + "\n"
    assert (15, PINS[15]) in missing_pins(moved)
    assert (14, PINS[14]) not in missing_pins(moved)
    assert PINS[15] in " ".join(bodies(moved)[14].split())
