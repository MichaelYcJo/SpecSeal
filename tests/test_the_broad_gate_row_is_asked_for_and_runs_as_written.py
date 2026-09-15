"""The `Broad gate` row is asked for, and it runs as the command it reads as.

Two tickets about one row of `seal/config.md`, in causal order. Nothing ever
asks a person for it (#401), so the first repository to fill it in by hand
filled it in the way every command in every document here is written — wrapped
in backticks — and nothing looked at what was written (#402). A shell reads
that as command substitution: the checks run, their exit status is thrown
away, and their output is executed in their place. The measured pair is the
whole of why this exists — the same content exits 1 bare and exited 0 wrapped,
with the failure still on the screen.

`tests/test_the_seal_is_taken_once_by_the_sealer.py` holds the executed half:
the gate refusing each form over a fixture repository, and the forms that stay
allowed still sealing. What is pinned HERE is the text a person reads — what
`templates/config.md` promises about the row, the criterion for choosing a
value and its one owner, and the sentence that sends a session which meets the
refusal to a person instead of letting it choose.

Every case was executed against the documents as they stood at 0e676e6,
before any of them was edited, and every case failed; the output is in the
body of the commit that added it.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TEMPLATE = ("templates", "config.md")
CONFIG_SKILL = ("skills", "config", "SKILL.md")
ORCH = ("skills", "implement", "orchestration.md")
SEALER = ("agents", "sealer.md")
REVIEW_ORCH = ("skills", "code-review", "orchestration.md")

REFUSED_AND_ALLOWED = "### What is refused, and what stays allowed"


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(text):
    """Runs of whitespace folded to one space, so a phrase a hand-wrap splits
    across two lines still reads as the phrase.

    A block quote's `> ` goes with the wrap it marks: the criterion is a
    two-line quote, and folding without dropping the marker leaves `the exit
    code the > gate reads` — a phrase nobody wrote and nobody can assert.
    """
    unquoted = "\n".join(re.sub(r"^\s*>\s?", "", line) for line in text.splitlines())
    return re.sub(r"\s+", " ", unquoted)


def section(text, heading, level):
    """The text under HEADING up to the next heading of the same level."""
    assert heading in text, f"{heading!r} is not a heading any more"
    body = text.split(heading, 1)[1]
    return body.split("\n" + "#" * level + " ", 1)[0]


def broad_gate_section():
    return section(read(*TEMPLATE), "## Broad gate", 2)


def rows(text):
    return [line for line in text.splitlines() if line.startswith("| ")]


def table(text, header):
    """The rows of ONE table in a section — the one whose header row starts
    with HEADER — so a form moved from the refused list to the allowed one
    stops satisfying the case named for the list it left.

    Round 1's 🟡 6. `rows` returns every `| ` line under the heading, and both
    tables live under one heading, so it merged them: the pipe row could be
    moved into the refused table with every case still green, and the refused
    loop below could pair a form with another form's reason. That is the
    §14 artifact for this change asserting nothing about its own content, in a
    release whose whole subject is a check that could not fail.
    """
    assert header in text, f"{header!r} is not a table in this section"
    after = text.split(header, 1)[1]
    out = []
    for line in after.splitlines():
        if line.startswith("| "):
            out.append(line)
        elif out:
            break
    return out


def named(table_rows, form):
    """The one row of TABLE_ROWS whose FIRST cell names FORM, or None.

    The name cell and not the whole row. Matching anywhere in the row let a
    row be found by its own prose: renaming the pipe row's first cell left
    this green, because the cost cell says *and a pipe cannot reach this row
    at all* further along the same line. That is 🟡 6's weakness one level
    in, met while repairing 🟡 6.
    """
    for line in table_rows:
        cells = line.split(" | ")
        if form in flat(cells[0]):
            return line
    return None


# --- A7: the template says what is refused and what is not ------------------


def test_the_template_carries_both_lists_under_one_heading():
    """The lists are what a reviewer is pointed at when they want to argue
    with a form, so they live together rather than a paragraph apart."""
    assert REFUSED_AND_ALLOWED in read(*TEMPLATE)
    both = section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3)
    assert "| Refused |" in both, "no refused list"
    assert "| Stays legal |" in both, "no allowed list"


REFUSED = {
    "backticks": "discards its exit status",
    "`$(…)`": "the same semantics",
    "trailing `&`": "before any check has finished",
}


def test_each_refused_form_is_named_with_what_a_shell_does_with_it():
    """A list without the reason is an enumeration the next reader extends by
    analogy, which is how a narrow refusal becomes the general sanitiser #402
    steers away from.

    The reason is asserted IN the form's own row of the REFUSED table. The
    dictionary already holds the pairing, and a loop asking only whether both
    strings appear somewhere under the heading throws it away: round 1 swapped
    the backticks row's reason with the `$(…)` row's and 15 cases stayed
    green, leaving the backticks row explaining itself as *the same semantics
    in the spelling somebody who knows shell reaches for first*.
    """
    body = section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3)
    refused = table(body, "| Refused |")
    for form, because in REFUSED.items():
        row = named(refused, form)
        assert row, f"the refused list does not name {form}"
        assert because in flat(row), (
            f"{form} is listed with the wrong reason, or with none: {row!r}"
        )


def test_the_criterion_sits_beside_the_list_rather_than_only_the_list():
    """The defence against the list growing by analogy in six months: a form
    belongs in it only by breaking one of the two halves, and the halves are
    written where the list is."""
    body = flat(section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3))
    assert "must run as the command it reads as" in body
    assert "exit code the gate reads must be that command's" in body


def test_the_template_says_a_refused_value_is_refused_and_not_repaired():
    """#402 §*Not this*. Stripping makes a wrong value silently work, leaves
    the file still wrong, and teaches the next person that backticks were
    fine."""
    body = flat(section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3))
    assert "Nothing is stripped" in body
    assert "quietly repaired" in body
    assert "/specseal:config" in body, (
        "the section does not say where a person rewrites the row"
    )


ALLOWED = {
    "**inside** a longer line": "runs as the command it reads as",
    "quotes, redirection": "the repository's own claim about itself",
    "a pipe": "LAST status",
    # Round 1's 🟡 1. A backgrounding `&` breaks the criterion's second half
    # wherever it stands, and only the trailing form is refused — so the
    # mid-line form has to be in ONE of the two lists. It is here, with what
    # it costs, because telling it from a `2>&1` or a quoted `&` needs the
    # shell parser this list exists to avoid.
    "an `&` anywhere but at the end": "may still be running when the gate stamps",
}


def test_each_allowed_form_is_listed_with_what_it_costs():
    """What stays legal is a commitment rather than an omission, and a cost
    stated in the open is what keeps it from being re-litigated as a defect.

    Read from the ALLOWED table alone, and the cost from the form's own row:
    round 1 moved the pipe row into the refused table and both allowed-list
    cases stayed green, which made them assert only that certain characters
    appear somewhere under the heading.
    """
    body = section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3)
    legal = table(body, "| Stays legal |")
    for form, cost in ALLOWED.items():
        row = named(legal, form)
        assert row, f"the allowed list does not name {form}"
        assert cost in flat(row), (
            f"{form} is listed with the wrong cost, or with none: {row!r}"
        )


# No case asserts that the two lists partition the forms, and that is not an
# omission. `$(…)` belongs in both and must: the whole command wrapped in it
# is refused, and one INSIDE a longer line is legal, which is the distinction
# the section exists to draw. A partition case over the matching keys was
# written here and asserted exactly that falsehood; it went red on its first
# run and came out rather than being weakened into something that passes.
# What `table()` buys is the pairing above — a row's reason read from the
# row, in the list the row is in.


def test_the_allowed_list_says_a_pipe_cannot_reach_the_row_at_all():
    """Found by building phase 1 and executed 2026-09-15: a pipe is allowed by
    the criterion and unwritable in the row. `hooks/config.py#CONFIG_ROW`
    matches a cell as `[^|]*?`, so the value ends at the first `|` — bare and
    backslash-escaped alike — the line stops being a row of that table, and
    the gate reports the row as ABSENT.

    The spec's allowed list said a pipe stays legal and stopped there, which
    is true about the refusal and false about the row. A document that
    promises a form nobody can write is the shape this work item exists to
    end, so the promise carries the measurement with it.
    """
    body = section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3)
    pipe = named(table(body, "| Stays legal |"), "a pipe")
    assert pipe, "the allowed list has no pipe row"
    pipe = flat(pipe)
    assert "cannot reach this row at all" in pipe
    assert "ends at the first" in pipe
    assert "as absent" in pipe
    # Round 1's 🟡 2, measured: `config_rows` stops reading the table at the
    # first line that does not parse, so the pipe row takes every row BELOW it
    # as well — a `Record language` under it is invisible and falls back to
    # its default with no message anywhere. The cost cell said only that the
    # gate names a cause that is not the real one, which understates it.
    assert "takes every row below it" in pipe, (
        "the pipe's cost is stated as the row's alone, and it is not"
    )
    assert "falling back to its default" in pipe


# --- Round 1's 🟡 4: the removed design, where a reader opens first ---------
#
# Phase 5 changed `missing_row` so it no longer tells the reader what to write,
# and `phases/phase-5.md` recorded that the old sentence should survive
# nowhere. It survived outside the message, in the two places somebody meets
# BEFORE the message — the module's own header, and the template paragraph
# directly above the section this branch added. `agent-contract` §14 is the
# grounds: the documents that explain a changed behaviour change with it.

GATE_SCRIPT = ("skills", "verify", "scripts", "broad_gate.py")


def module_header():
    """The module docstring, which is the first thing anyone opening the file
    reads — bounded at its closing quotes, not the whole file."""
    text = read(*GATE_SCRIPT)
    opening = text.index('"""')
    return flat(text[opening : text.index('"""', opening + 3)])


def test_the_module_header_names_both_refusals_and_neither_names_a_command():
    """The header's numbered list is where the command says what it does in
    order. It described the absent-row refusal as *the command names the row
    to write* — the removed behaviour — and did not mention the second
    refusal, this branch's headline change, at all."""
    header = module_header()
    assert "refused two ways" in header, (
        "the header still describes one refusal where the gate has two"
    )
    assert "wrapped in backticks or in `$(…)`, or ending in a single `&`" in header
    assert "names the row to write" not in header, (
        "the header asserts the behaviour phase 5 removed"
    )
    assert "Neither refusal names a command to write" in header


def test_the_paragraph_above_the_lists_no_longer_says_it_names_what_to_write():
    """*A refusal that names what to write is answered by the next person to
    read it* was half the stated reason for preferring a refusal to a prompt,
    and the refusal no longer does that. The paragraph sits inside the very
    section this branch rewrote."""
    section_text = flat(broad_gate_section())
    assert "names what to write is answered" not in section_text, (
        "the template still argues from the sentence the message dropped"
    )
    assert "names whose the row is and where it is answered" in section_text
    assert "#401" in section_text, (
        "the paragraph asserts the change without the report behind it"
    )


# --- A8: the criterion has one home, and rule 3 was folded into it ----------

CRITERION = "### Choosing a value — the criterion"

THREE_RULES = [
    "red repository-wide for reasons unrelated to any branch",
    "A command that **fixes** the tree",
    "The suite runner comes first",
]


def test_the_template_carries_all_three_rules_of_the_criterion():
    """#401's second half. The row is the one value only a person can write
    and nobody had written down how to choose it: the session that met the
    refusal derived these three under pressure, and two of them existed in no
    document at all."""
    body = flat(section(read(*TEMPLATE), CRITERION, 3))
    for rule in THREE_RULES:
        assert rule in body, f"the criterion does not carry {rule!r}"


def test_each_rule_is_carried_with_the_reason_it_is_a_rule():
    """A rule with no reason is one the next reader drops when it is
    inconvenient, and two of these three were dropped by being written
    nowhere."""
    body = flat(section(read(*TEMPLATE), CRITERION, 3))
    assert "block every future work item" in body, "rule 1 has no reason"
    assert "can only come back green" in body, "rule 2 has no reason"
    assert "before the row's first `&&`" in body, "rule 3 has no reason"


def test_rule_three_was_folded_rather_than_copied_into_a_third_place():
    """It stood in `templates/config.md` and in `skills/config/SKILL.md`
    before this work. Writing the criterion without folding would have made
    three copies of the one rule that was already written down —
    `tests/test_the_rules_have_one_owner.py` is the standing check, and this
    case is the fold itself."""
    skill = flat(read(*CONFIG_SKILL))
    assert "put the suite runner first" not in skill, (
        "the config skill still states rule 3 beside the criterion that owns it"
    )
    assert "re-runs\n  what stands before the first" not in read(*CONFIG_SKILL)
    template_body = read(*TEMPLATE)
    assert template_body.count("The suite runner comes first") == 1


def test_the_config_skill_sends_the_criterion_to_its_owner_by_name():
    """A link is one sentence naming the owner, and it does not restate the
    rule (the shape `tests/test_the_rules_have_one_owner.py` holds every
    linking carrier to)."""
    skill = flat(read(*CONFIG_SKILL))
    assert CRITERION.lstrip("# ") in skill, (
        "the config skill does not name the section that owns the criterion"
    )
    assert "red repository-wide" not in skill, (
        "the config skill restates a rule instead of pointing at it"
    )


def refusal_bullet():
    """The config skill's paragraph about the refusal, bounded at the blank
    line — not the file. Round 1's 🟡 8: the clause naming the three forms
    could be deleted with 15 cases green, because every assertion matched a
    sentence on one side of it or the other."""
    skill = read(*CONFIG_SKILL)
    opening = "**The `Broad gate` row is looked at before it is run**"
    assert opening in skill, "the refusal paragraph is gone from the config skill"
    return flat(skill[skill.index(opening) :].split("\n\n", 1)[0])


def test_the_config_skill_points_at_the_section_and_restates_no_form():
    """The door a person reaches later. It names the three forms so somebody
    reading it knows the refusal exists, and sends the reasoning to the one
    owner rather than carrying a second copy of it."""
    skill = flat(read(*CONFIG_SKILL))
    assert "What is refused, and what stays allowed" in skill, (
        "the config skill does not point at the section that decides this"
    )
    assert "must run as the command it reads as, and the exit code" not in skill, (
        "the config skill restates the criterion instead of pointing at it"
    )
    bullet = refusal_bullet()
    assert "would not run as the command it reads as" in bullet
    assert "Nothing is stripped or repaired" in bullet
    # The docstring's own claim, asserted. It said the paragraph names the
    # three forms and nothing checked that it did.
    for form in ("backticks", "`$(…)`", "trailing `&`"):
        assert form in bullet, (
            f"the config skill does not name {form}, so somebody reading it "
            "does not learn that the refusal exists"
        )


# --- A10: a session that meets the refusal brings it to a person ------------
#
# #401's third Done-when, and the one the ticket says a sentence already
# failed: *a session that meets the refusal anyway is told to bring it to a
# person rather than to choose — and something checks that, since a sentence
# is what failed here.* The something is this section and the executed case
# beside it in `tests/test_the_seal_is_taken_once_by_the_sealer.py`.


def missing_row_text():
    """The refusal itself, built by the module rather than quoted from it."""
    import importlib.util

    path = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")
    spec = importlib.util.spec_from_file_location("specseal_broad_gate_text", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return flat(module.missing_row("/seal"))


def test_the_absent_row_refusal_no_longer_tells_the_reader_to_write_one():
    """The only reader standing in front of this message is a session, so
    *write the repository's own broad command into it* asked the one party
    that may not. It printed the row to type, too."""
    said = missing_row_text()
    assert "Write the repository's own broad command" not in said
    assert "<the full suite, the repository-wide lint, the typecheck>" not in said
    assert "not this session's to do" in said


def test_the_absent_row_refusal_says_whose_the_row_is_and_where_it_is_answered():
    """Naming the door is what keeps *not this session's* from reading as a
    dead end — which is how a refusal with no route becomes a session filling
    the row in anyway."""
    said = missing_row_text()
    assert "a row is a thing a person wrote" in said
    assert "/specseal:config" in said
    assert "Choosing a value — the criterion" in said
    assert "Nothing ran" in said


def test_the_sealer_is_told_the_row_refusal_is_a_persons_and_not_its_own():
    """`agents/sealer.md` already said the sealer judges nothing. What it did
    not say is what to do with the one refusal that has an obvious action
    attached, which is the refusal #401 watched a session take."""
    sealer = flat(read(*SEALER))
    assert "goes back to a person, and never to you" in sealer
    assert "/specseal:config" in sealer
    assert "seal your own choice" in sealer
    # The bullet on its own, not the file. Asserted against the whole file
    # this passed while the bullet said nothing, because the paragraph below
    # carries the same phrase -- which is the counterfeit `agent-contract`
    # §15 exists to catch, met while catching it.
    bullet = read(*SEALER).split("- **Exit 2, refused, and nothing ran**", 1)[1]
    bullet = flat(bullet.split("\n\n", 1)[0])
    assert "would not run as the command it reads as" in bullet, (
        "the exit-2 bullet names only the absent row, not the refused one"
    )


def test_the_review_orchestrator_stops_the_run_rather_than_filling_the_row_in():
    """The other party in the room when the refusal lands. The sealer reports
    it; whoever spawned the sealer is the one holding a draft pull request and
    a reason to get past it."""
    orchestrator = flat(read(*REVIEW_ORCH))
    assert "A refusal about the `Broad gate` row goes to a person" in orchestrator
    assert "leave the pull request as a draft until they have" in orchestrator
    assert "/specseal:config" in orchestrator
    assert "#401" in orchestrator, (
        "the instruction is asserted without the measurement behind it"
    )
