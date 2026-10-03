"""A signatory declares its pact (#647, step A).

Some work items commit in more than one repository, and those repositories
keep one contract together. The one copy of it is the PACT, `seal/pact.md` in
the repository that holds it, and every repository of such a work item is a
SIGNATORY. A signatory other than the pact's repository names the pact in its
own `seal/config.md`:

    | Pact | git@example.com:org/orders-api.git |
    | Pact notify | when the pact is touched |

The rows have one reader, `hooks/config.py#pact_declaration`, which both
`chain_check.py` (prints) and `pact_check.py` (refuses) ask. The cases below
are that reader's (S1-S3 of the work item's `spec.md`), and the routing
step's pinned sentences (S4).
"""

import os

from conftest import load_hook_module

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

config = load_hook_module("config.py", "config_for_the_pact")


def table(*rows):
    return "# config\n\n| Item | Value |\n|---|---|\n" + "".join(
        f"| {item} | {value} |\n" for item, value in rows
    )


def flat(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


# --- S1-S3: the rows and their reader ---------------------------------------


def test_one_pact_reads_normalised_with_the_default_notify():
    """S1. One URL and no `Pact notify`: the URL normalised, its name, and
    #647's recommended value."""
    pacts, notify, refusals = config.pact_declaration(
        table(("Mode", "shared"), ("Pact", "git@example.com:org/Orders-API.git"))
    )
    assert refusals == []
    assert pacts == [
        (
            "git@example.com:org/Orders-API.git",
            "example.com/org/orders-api",
            "orders-api",
        )
    ]
    assert notify == "when the pact is touched" == config.NOTIFY_DEFAULT


def test_two_pacts_come_back_in_order():
    """S2. `;` separates the pacts a signatory signs, and the order is the
    row's."""
    pacts, notify, refusals = config.pact_declaration(
        table(
            (
                "Pact",
                "https://example.com/org/orders-api ; git@example.com:org/billing.git",
            ),
            ("Pact notify", "Always"),
        )
    )
    assert refusals == []
    assert [name for _, _, name in pacts] == ["orders-api", "billing"]
    assert notify == "always"


def test_a_notify_value_outside_the_vocabulary_is_refused_naming_all_three():
    """S3, the reader half. The refusal names every value it would take."""
    pacts, notify, refusals = config.pact_declaration(
        table(
            ("Pact", "git@example.com:org/orders-api.git"), ("Pact notify", "sometimes")
        )
    )
    assert len(pacts) == 1
    assert notify is None
    assert refusals == [
        "`Pact notify | sometimes` is not one of `always`, "
        "`when the pact is touched`, `never`"
    ]


def test_no_row_and_an_empty_row_hold_no_pact_and_ignore_notify():
    """Absent means no pact is held elsewhere, and a `Pact notify` with no
    `Pact` is ignored rather than refused."""
    for text in (
        table(("Mode", "shared")),
        table(("Pact", "")),
        table(("Pact notify", "sometimes")),
        "no table here\n",
    ):
        assert config.pact_declaration(text) == ([], None, []), text


def test_a_row_that_will_not_parse_is_refused_and_never_read_as_absent():
    """Each way an entry fails is a sentence naming it, so a signatory that
    wrote a row is never read as one that wrote none."""
    cases = {
        "orders-api": "is not a remote URL",
        "git@example.com:org/a.git;;git@example.com:org/b.git": "holds an empty entry",
        "git@example.com:org/a.git git@example.com:org/b.git": "holds a space",
        "https://example.com/org/a+b": "which a pact anchor cannot name",
        "git@example.com:org/api.git;https://example.com/other/api": "both end in `api`",
        "git@example.com:org/api.git;https://example.com/org/api": "are one repository",
    }
    for value, said in cases.items():
        _, _, refusals = config.pact_declaration(table(("Pact", value)))
        assert len(refusals) == 1 and said in refusals[0], (value, refusals)
    _, _, refusals = config.pact_declaration(
        table(
            ("Pact", "git@example.com:org/a.git"), ("Pact", "git@example.com:org/b.git")
        )
    )
    assert refusals == [
        "`Pact` appears 2 times — list every pact in one row, separated by `;`"
    ]


def test_an_unreadable_config_is_no_declaration(tmp_path):
    """`declared_pacts` fails toward nothing declared, as every reader in
    `hooks/config.py` does."""
    assert config.declared_pacts(str(tmp_path / "missing")) == ([], None, [])
    home = tmp_path / "seal"
    home.mkdir()
    (home / "config.md").write_text(
        table(("Pact", "git@example.com:org/orders-api.git")), encoding="utf-8"
    )
    pacts, notify, _ = config.declared_pacts(str(home))
    assert [n for _, _, n in pacts] == [
        "orders-api"
    ] and notify == config.NOTIFY_DEFAULT


def test_seal_keeps_one_normaliser():
    """`seal.py` re-exports the reader's normaliser rather than keeping a
    second copy that could drift from the one the `Pact` rows go through."""
    seal = load_hook_module(
        os.path.join("..", "skills", "implement", "scripts", "seal.py"),
        "seal_for_the_pact",
    )
    assert seal.normalise_remote is seal.repo_config.normalise_remote


# --- the shipped rows -------------------------------------------------------


def test_the_template_and_the_config_skill_carry_both_rows_and_the_vocabulary():
    """`templates/config.md` documents both rows and keeps the notify words
    out of translation; `/specseal:config` shows both."""
    template = flat("templates", "config.md")
    skill = flat("skills", "config", "SKILL.md")
    for row in (config.PACT_ROW, config.PACT_NOTIFY_ROW):
        assert f"| `{row}` |" in template, row
        assert f"| `{row}` |" in skill, row
    start = template.index("## What no row governs")
    governs = template[start : template.index(" ## ", start + 1)]
    for value in config.NOTIFY_VALUES:
        assert f"`{value}`" in governs, value


# --- S4: the routing step across repositories -------------------------------

ORCHESTRATION = ("skills", "implement", "orchestration.md")


def test_the_routing_step_mints_one_id_and_declares_only_in_gated_repositories():
    """S4. The question is asked once, the id is minted once, and a
    repository with no root is named and left alone, because writing into it
    would opt it in."""
    text = flat(*ORCHESTRATION)
    start = text.index("### A work item that commits in more than one repository")
    section = text[start : text.index(" ## ", start)]
    for sentence in (
        "**One id, minted once, names the directory in every repository.** "
        "Take `date +%s` once, pick one slug, and use the resulting directory "
        "name in every repository.",
        "**Only a gated repository gets a declaration.**",
        "A repository with no root is not opted in by this step",
        "Name such a repository in the handback and write nothing into it.",
        "each in a command of its own, and commit each with that repository's "
        "absolute path written out after `git -C`",
        "A sentence is contract when another repository's code would be wrong "
        "if it changed.",
        "The pact's repository needs no row",
    ):
        assert sentence in section, sentence


# --- the pact's own table ---------------------------------------------------

PACT = (
    "# Pact\n\n<!-- | Signatory |\n|---|\n| git@example.com:org/quoted.git | -->\n\n"
    "| Signatory |\n|---|\n"
    "| git@example.com:org/orders-web.git |\n"
    "| https://example.com/other/orders-web |\n\n"
    "## Order response shape\n\nx\n"
)


def test_the_pact_lists_its_signatories_and_a_comment_is_not_the_table():
    """Two signatories may end in one segment, because nobody cites a
    signatory by name; a table in a comment block is not the table."""
    signatories, refusals = config.pact_signatories(PACT)
    assert refusals == []
    assert [n for _, n, _ in signatories] == [
        "example.com/org/orders-web",
        "example.com/other/orders-web",
    ]


def test_a_pact_with_no_table_or_an_unfilled_one_is_refused():
    """A pact nobody signs is not a pact, and the template's placeholder row
    is refused rather than read as a signatory."""
    assert config.pact_signatories("# Pact\n\n## A\n") == (
        [],
        ["holds no `| Signatory |` table, so it names no signatory"],
    )
    with open(os.path.join(ROOT, "templates", "pact.md"), encoding="utf-8") as h:
        signatories, refusals = config.pact_signatories(h.read())
    assert signatories == [] and len(refusals) == 1 and "holds a space" in refusals[0]
    _, refusals = config.pact_signatories("| Signatory |\n|---|\n\n## A\n")
    assert refusals == ["its `Signatory` table lists nobody"]
