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
    steers away from."""
    body = flat(section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3))
    for form, because in REFUSED.items():
        assert form in body, f"the refused list does not name {form}"
        assert because in body, f"{form} is listed with no reason"


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


ALLOWED = ["**inside** a longer line", "quotes, redirection", "a pipe"]


def test_each_allowed_form_is_listed_with_what_it_costs():
    """What stays legal is a commitment rather than an omission, and a cost
    stated in the open is what keeps it from being re-litigated as a defect."""
    body = section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3)
    legal = flat("\n".join(rows(body)))
    for form in ALLOWED:
        assert form in legal, f"the allowed list does not name {form}"
    assert "LAST status" in legal, "the pipe is listed without its cost"


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
    legal = flat("\n".join(rows(section(read(*TEMPLATE), REFUSED_AND_ALLOWED, 3))))
    assert "cannot reach this row at all" in legal
    assert "ends at the first" in legal
    assert "as absent" in legal


def test_the_config_skill_points_at_the_section_and_restates_no_form():
    """The door a person reaches later. It names the three forms so somebody
    reading it knows the refusal exists, and sends the reasoning to the one
    owner rather than carrying a second copy of it."""
    skill = flat(read(*CONFIG_SKILL))
    assert "What is refused, and what stays allowed" in skill, (
        "the config skill does not point at the section that decides this"
    )
    assert "would not run as the command it reads as" in skill
    assert "Nothing is stripped or repaired" in skill
    assert "must run as the command it reads as, and the exit code" not in skill, (
        "the config skill restates the criterion instead of pointing at it"
    )
