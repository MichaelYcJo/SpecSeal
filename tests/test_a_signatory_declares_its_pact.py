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

import importlib.util
import os
import sys
import unicodedata

import pytest
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


@pytest.mark.parametrize("first", ["always", "when the pact is touched", "never"])
def test_a_notify_row_written_twice_has_no_value(first):
    """A `Pact notify` row written twice is refused and read as no value, as
    a value outside the vocabulary is: its first row is not the answer, so
    no caller can rule `always` in or out from it (#647 C and D, round 1 of
    PR #756, yellow 2)."""
    pacts, notify, refusals = config.pact_declaration(
        table(
            ("Pact", "git@example.com:org/orders-api.git"),
            ("Pact notify", first),
            ("Pact notify", "always"),
        )
    )
    assert len(pacts) == 1
    assert notify is None
    assert refusals == ["`Pact notify` appears 2 times — one value"]


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
    """`declared_pacts` is what `pact-check` reads a signatory's rows
    through. No file is no row; a file that is there and will not read is
    None, which the caller refuses, because a written row read as absent is
    the silence the reader exists to end."""
    assert config.declared_pacts(str(tmp_path / "missing")) == ([], None, [])
    home = tmp_path / "seal"
    (home / "config.md").mkdir(parents=True)
    assert config.declared_pacts(str(home)) is None
    (home / "config.md").rmdir()
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


# --- #759: a pact row the table walk does not reach is refused --------------
#
# `config_rows` ends the table at the first line that is not a row, a second
# header or a stray separator (#82), and a `Pact notify | always` row written
# past that point used to be read as the default. Under `always` a moved row
# citing no clause was then re-stamped unrecorded. The cases name each way the
# walk passes a pact row by (W1-W11 of the work item's `spec.md`), and each is
# refused with `notify` None.

URL = "git@example.com:org/orders-api.git"
CONFIG_TOP = "# config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n"
CONFIG = CONFIG_TOP + f"| Pact | {URL} |\n"
STRAY = "| Pact notify | always |"
# The eight characters `str.splitlines` ends a line at and GFM does not.
SPLITLINES_ONLY = ["\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"]
# Every format character (Unicode category Cf): GFM renders each as nothing,
# so a row spelled with one reads as the item it would be without it.
FORMAT_CHARACTERS = [
    chr(c) for c in range(sys.maxunicode + 1) if unicodedata.category(chr(c)) == "Cf"
]


def refused_as(line, item="Pact notify"):
    return (
        f"`{line}` is shaped as a `{item}` row and is not read as one, because "
        "it stands outside the `| Item | Value |` table, is not written as a "
        "two-cell row, spells the item another way, or holds a character that "
        "cuts the line. Write it as "
        f"`| {item} | … |` inside that table"
    )


def test_s1_a_notify_row_below_a_blank_line_is_refused():
    """S1, W3. The row #759 was opened about: written under a blank line that
    ended the table, it was read as the default."""
    assert config.pact_declaration(CONFIG + "\n" + STRAY + "\n") == (
        [(URL, "example.com/org/orders-api", "orders-api")],
        None,
        [refused_as(STRAY)],
    )


STRAY_WAYS = [
    ("W1 above the header", STRAY + "\n\n" + CONFIG, STRAY),
    (
        "W1 no header at all",
        f"| Pact | {URL} |\n{STRAY}\n",
        None,
    ),
    (
        "W2 between the header and the first row",
        "| Item | Value |\n|---|---|\n | Pact notify | always |\n"
        f"| Mode | shared |\n| Pact | {URL} |\n",
        "| Pact notify | always |",
    ),
    ("W4 prose", CONFIG + "Some prose.\n" + STRAY + "\n", STRAY),
    ("W4 a heading", CONFIG + "## Notes\n" + STRAY + "\n", STRAY),
    ("W4 a list item", CONFIG + "- a note\n" + STRAY + "\n", STRAY),
    ("W4 a thematic break", CONFIG + "***\n" + STRAY + "\n", STRAY),
    ("W4 an HTML block line", CONFIG + "<div>\n" + STRAY + "\n", STRAY),
    (
        "W5 a second header",
        CONFIG + "| Item | Value |\n|---|---|\n" + STRAY + "\n",
        STRAY,
    ),
    ("W6 a stray separator", CONFIG + "|---|---|\n" + STRAY + "\n", STRAY),
    ("W7 a three-column header", CONFIG + "| A | B | C |\n" + STRAY + "\n", STRAY),
    ("W8 indented", CONFIG + "  " + STRAY + "\n", STRAY),
    ("W8 block-quoted", CONFIG + "> " + STRAY + "\n", "> " + STRAY),
    ("W8 three cells", CONFIG + STRAY + " x |\n", STRAY + " x |"),
    (
        "W8 no closing pipe",
        CONFIG + "| Pact notify | always\n",
        "| Pact notify | always",
    ),
    (
        "W8 an escaped pipe against the closing one",
        CONFIG + "| Pact notify | always\\|\n",
        "| Pact notify | always\\|",
    ),
    ("W10 a cut line", CONFIG + "\nprose\u2028" + STRAY + "\n", STRAY),
    # Round 1 of PR #784, yellow 1: GFM needs no pipe at either end, so a
    # line directly under the table is one of its rows.
    (
        "W8 no leading pipe, directly under the table",
        CONFIG + "Pact notify | always |\n",
        "Pact notify | always |",
    ),
    (
        "W8 no pipe at either end, directly under the table",
        CONFIG + "Pact notify | always\n",
        "Pact notify | always",
    ),
]


@pytest.mark.parametrize(
    "text, line", [w[1:] for w in STRAY_WAYS], ids=[w[0] for w in STRAY_WAYS]
)
def test_s2_every_way_the_walk_passes_a_notify_row_by_is_refused(text, line):
    """S2. Each way `config_rows` passes a pact row by, with a `Pact` value
    standing: refused, naming the line, and `notify` None."""
    pacts, notify, refusals = config.pact_declaration(text)
    assert notify is None
    if line is None:
        # No table at all: both rows are strays, and `Pact` is refused too.
        assert pacts == []
        assert refusals == [
            refused_as(f"| Pact | {URL} |", "Pact"),
            refused_as(STRAY),
        ]
    else:
        assert [n for _, _, n in pacts] == ["orders-api"]
        assert refusals == [refused_as(line)]


@pytest.mark.parametrize(
    "row, shown",
    [
        ("| pact notify | always |", "| pact notify | always |"),
        ("| Pact  notify | always |", "| Pact  notify | always |"),
        ("| Pact\u00a0notify | always |", "| Pact<U+00A0>notify | always |"),
    ],
    ids=["another case", "a doubled space", "a no-break space"],
)
def test_s3_a_notify_row_spelled_another_way_is_refused(row, shown):
    """S3, W9. The walk takes the line as a row, under an item that is not
    `Pact notify`. The no-break space is shown as its code point, because the
    sentence naming the line would otherwise show nothing wrong with it."""
    assert config.pact_declaration(CONFIG + row + "\n")[1:] == (
        None,
        [refused_as(shown)],
    )


@pytest.mark.parametrize(
    "ch", SPLITLINES_ONLY, ids=[f"U+{ord(c):04X}" for c in SPLITLINES_ONLY]
)
def test_s4_a_notify_row_the_reader_cuts_in_two_is_refused(ch):
    """S4, W11. GFM renders one row, and the reader cuts it into two pieces
    neither of which is a row. Only GFM's cut sees it."""
    row = f"| Pact notify | {ch}always |"
    assert config.pact_declaration(CONFIG + row + "\n")[1:] == (
        None,
        [refused_as(f"| Pact notify | <U+{ord(ch):04X}>always |")],
    )


@pytest.mark.parametrize(
    "ch", FORMAT_CHARACTERS, ids=[f"U+{ord(c):04X}" for c in FORMAT_CHARACTERS]
)
def test_s3_a_notify_row_spelled_with_a_format_character_is_refused(ch):
    """S3, W9, round 1 of PR #784, yellow 2. A format character renders as
    nothing, so GFM shows `Pact notify` while the walk takes another item
    and `\\s` cannot cross it. Each is removed before the shape reads the
    line, and shown as its code point in the sentence naming it."""
    code = f"<U+{ord(ch):04X}>"
    for row, shown in (
        (f"| Pa{ch}ct notify | always |", f"| Pa{code}ct notify | always |"),
        (f"| Pact{ch}notify | always |", f"| Pact{code}notify | always |"),
        (f"| Pact notify{ch} | always |", f"| Pact notify{code} | always |"),
    ):
        assert config.pact_declaration(CONFIG + row + "\n")[1:] == (
            None,
            [refused_as(shown)],
        ), row


def test_s5_a_pact_row_below_the_table_is_refused_with_no_pact_in_it():
    """S5. A stray `Pact` row with none in the table: refused, and `pacts` is
    what the table parsed, which is nothing."""
    line = f"| Pact | {URL} |"
    assert config.pact_declaration(CONFIG_TOP + "\n" + line + "\n") == (
        [],
        None,
        [refused_as(line, "Pact")],
    )


def test_s6_a_stray_notify_row_with_no_pact_anywhere_is_ignored():
    """S6. A notify row with no `Pact` value is ignored wherever it stands,
    as it is inside the table: refusing it would leave every moved row in a
    repository that holds no pact (round 2 of PR #756, yellow 2)."""
    for text in (
        CONFIG_TOP + "\n" + STRAY + "\n",
        CONFIG_TOP + "| Pact |  |\n\n" + STRAY + "\n",
        CONFIG_TOP + "Pact notify | always |\n",
    ):
        assert config.pact_declaration(text) == ([], None, []), text


@pytest.mark.parametrize(
    "below",
    [
        "\n```\n" + STRAY + "\n```\n",
        "\n<!--\n" + STRAY + "\n-->\n",
        "\n- " + STRAY + "\n",
        "\n| Pact notify |  |\n",
        "\n| Pact |  |\n",
    ],
    ids=["a closed fence", "a closed comment", "a list item", "empty", "empty pact"],
)
def test_s7_a_pact_row_that_is_not_a_stray_is_not_refused(below):
    """S7. An example in a closed fence or comment, a list item, and an empty
    value are not rows anybody wrote as live ones; the table reads as today."""
    pacts, notify, refusals = config.pact_declaration(CONFIG + below)
    assert refusals == []
    assert notify == config.NOTIFY_DEFAULT
    assert [n for _, _, n in pacts] == ["orders-api"]


@pytest.mark.parametrize(
    "ch", SPLITLINES_ONLY, ids=[f"U+{ord(c):04X}" for c in SPLITLINES_ONLY]
)
def test_s8_a_line_whose_pieces_the_reader_reads_is_read_as_today(ch):
    """S8. GFM's cut sees one line, and the reader reads both of its pieces
    as rows. A row the reader read on either cut is never refused."""
    text = CONFIG_TOP + f"| Pact | {URL} |{ch}{STRAY}\n"
    pacts, notify, refusals = config.pact_declaration(text)
    assert (notify, refusals) == ("always", [])
    assert [n for _, _, n in pacts] == ["orders-api"]


def test_the_shipped_configs_hold_no_stray_pact_row():
    """The template ships empty `Pact` rows inside its example table and
    shaped ones in its prose; neither it nor this repository's own config is
    refused (questions.md Q2)."""
    for parts in (("templates", "config.md"), ("seal", "config.md")):
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
            assert config.pact_declaration(handle.read())[2] == [], parts


def test_s14_the_reader_and_the_vendored_copy_share_one_grammar():
    """S14. A copy with no `hooks/` looks for the same rows with
    `evidence_check.py#NOTIFY_ROW_SHAPE`; the two are one grammar."""
    path = os.path.join(
        ROOT, "skills", "evidence-check", "scripts", "evidence_check.py"
    )
    spec = importlib.util.spec_from_file_location("ec_for_the_pact_shape", path)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    ours, theirs = config.PACT_ROW_SHAPE, ec.NOTIFY_ROW_SHAPE
    assert (ours.pattern, ours.flags) == (theirs.pattern, theirs.flags)
    # The line each reads the shape through is one rule too (round 1 of PR
    # #784, yellow 2): every format character removed, nothing else.
    for ch in [*FORMAT_CHARACTERS, "\u00a0", "\u2028"]:
        line = f"{ch}| Pa{ch}ct notify{ch} | x |"
        assert config.shape_line(line) == ec.shape_line(line), hex(ord(ch))


def test_config_rows_is_the_indexed_walk_without_its_places():
    """`config_rows` returns what it returned before the walk kept indices:
    the index is the place in `text.splitlines()` each row came from."""
    text = CONFIG + "| Pact notify | always |\n\n| Broad gate | x |\n"
    indexed = config.indexed_config_rows(text)
    lines = text.splitlines()
    assert [(i, v) for _, i, v in indexed] == config.config_rows(text)
    assert all(lines[n].startswith(f"| {item} |") for n, item, _ in indexed)
    assert [item for _, item, _ in indexed] == ["Mode", "Pact", "Pact notify"]


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


@pytest.mark.parametrize(
    "parts, sentence",
    [
        (
            ("docs", "the-pact.md"),
            "**A `Pact` or `Pact notify` row the table's reader does not reach "
            "is refused, never read as the default.**",
        ),
        (
            ("docs", "the-pact.md"),
            "A `Pact` row there always refuses. A `Pact notify` row there "
            "refuses only where a `Pact` value stands, because one with no pact "
            "is ignored wherever it is written.",
        ),
        (
            ("docs", "the-pact.md"),
            "It looks for both rows on every line, as `str.splitlines` and as "
            "GFM cut the file, so it leaves a row wherever the plugin's reader "
            "refuses a notify row it does not reach.",
        ),
        (
            ("templates", "config.md"),
            "**So is a `Pact` or `Pact notify` row written where the table's "
            "reader does not reach it**, never read as the default",
        ),
        (
            ("templates", "config.md"),
            "Write both rows inside the one `| Item | Value |` table.",
        ),
    ],
    ids=[
        "the pact: the rule",
        "the pact: which row refuses",
        "the pact: the vendored copy",
        "template: the rule",
        "template: the remedy",
    ],
)
def test_s16_the_documents_say_a_stray_pact_row_is_refused(parts, sentence):
    """S16 of #759. Each sentence a person reads about the stray rule is
    pinned whole; the refusal's own text is pinned by S1 above."""
    assert sentence in flat(*parts), sentence


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
    assert refusals == ["has a `Signatory` table that lists nobody"]
    # A header GFM renders no table under is that refusal alone: it names
    # no table, so it cannot be one that lists nobody.
    assert config.pact_signatories("| Signatory |\n\n## A\n") == (
        [],
        [
            "has a `| Signatory |` header with no delimiter row under it, so "
            "GFM renders no table there"
        ],
    )


@pytest.mark.parametrize(
    "row",
    [
        "| https://example.com/org/orders-mobile",
        "| https://example.com/org/orders-mobile | the app |",
    ],
    ids=["no closing pipe", "two cells"],
)
def test_a_signatory_row_the_walk_cannot_read_is_refused(row):
    """A table line the walk cannot read ends it, and the signatories below
    it would go unread; the line is refused rather than passed in silence."""
    text = (
        "# Pact\n\n| Signatory |\n|---|\n| https://example.com/org/orders-web |\n"
        + row
        + "\n\n## A\n\nx\n"
    )
    signatories, refusals = config.pact_signatories(text)
    assert [s[2] for s in signatories] == ["orders-web"]
    assert refusals == [
        f"has a `Signatory` table that stops at `{row}`, which is not a one-cell "
        "row written `| … |` — every signatory below it would go unread"
    ], refusals


# --- every way GFM ends or breaks the `Signatory` table (round 2 of #647) ---
#
# A table is a header row, a delimiter row of the same width, then body rows,
# and it is broken by a blank line or by the start of another block. Each way
# is either read as GFM reads it, or refused; none drops a signatory while the
# table reads as complete. These cases pin the SENTENCES the pact prints. That
# the walk reads what GFM renders is not held here but by
# `tests/test_one_table_walker_reads_what_gfm_renders.py`, over a corpus
# enumerated from the block kinds and judged by cmark-gfm itself: a list like
# this one, written by the walk's own author, is what round 3 of #735 found
# short by an autolink.

WEB = "https://example.com/org/orders-web"
MOBILE = "https://example.com/org/orders-mobile"
HEAD = f"# Pact\n\n| Signatory |\n|---|\n| {WEB} |\n"
CLAUSE = "\n## Order response shape\n\nx\n"
ENDS_ABOVE = (
    f"has a `Signatory` table that ends above `| {MOBILE} |`, a row the walk "
    "never reaches — it and every signatory below it would go unread"
)


def stops_at(line, why="which is not a one-cell row written `| … |`"):
    return (
        f"has a `Signatory` table that stops at `{line}`, {why} — every "
        "signatory below it would go unread"
    )


TABLE_ENDS = [
    ("a blank line, then a row", HEAD + f"\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    (
        "a line with no pipe",
        HEAD + f"{MOBILE}\n" + CLAUSE,
        f"has a `Signatory` table that continues with `{MOBILE}`, a line with "
        "no pipe that GFM reads as one of its rows — write it as `| … |`",
    ),
    ("a heading", HEAD + f"## A clause\n\n| {MOBILE} |\n", None),
    ("a fence", HEAD + f"```\nx\n```\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("an HTML comment", HEAD + f"<!-- a note -->\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("a block quote", HEAD + f"> a note\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("a list item", HEAD + f"- a note\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("the end of the file", HEAD, None),
    # Round 3 of #735 (🟡 18): an autolink is a row to GFM, not an HTML
    # block, and a thematic break ends the table rather than being a row.
    (
        "an autolink row",
        HEAD + f"<{MOBILE}>\n" + CLAUSE,
        f"has a `Signatory` table that continues with `<{MOBILE}>`, a line with "
        "no pipe that GFM reads as one of its rows — write it as `| … |`",
    ),
    ("an HTML block", HEAD + f"<div>\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("an ordered list item", HEAD + f"1. a note\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("a thematic break", HEAD + f"***\n| {MOBILE} |\n" + CLAUSE, ENDS_ABOVE),
    ("a thematic break, then a clause", HEAD + "---\n" + CLAUSE, None),
    # ⬜ 22: indented as GFM permits, read rather than refused.
    (
        "an indented header, delimiter and row",
        f"# Pact\n\n   | Signatory |\n  |---|\n | {WEB} |\n" + CLAUSE,
        None,
    ),
    (
        "a row four columns in",
        HEAD + f"    | {MOBILE} |\n" + CLAUSE,
        f"has a `Signatory` table that ends above `| {MOBILE} |`, a row the walk "
        "never reaches — it and every signatory below it would go unread",
    ),
    (
        "a header GFM reads into a list item",
        f"# Pact\n\n- a note\n| Signatory |\n|---|\n| {WEB} |\n" + CLAUSE,
        "has a `| Signatory |` header directly under `- a note`, and GFM "
        "renders a table under a line only in some of the shapes that line "
        "can take — leave a blank line above the header",
    ),
    (
        "no delimiter row",
        f"# Pact\n\n| Signatory |\n| {WEB} |\n" + CLAUSE,
        "has a `| Signatory |` header with no delimiter row under it, so GFM "
        "renders no table there",
    ),
    (
        "a comment between the header and its delimiter",
        f"# Pact\n\n| Signatory |\n<!-- a note -->\n|---|\n| {WEB} |\n" + CLAUSE,
        "has a `| Signatory |` header with no delimiter row under it, so GFM "
        "renders no table there",
    ),
    (
        "a delimiter row of the wrong width",
        f"# Pact\n\n| Signatory |\n|---|---|\n| {WEB} |\n" + CLAUSE,
        "has a `| Signatory |` header over a delimiter row of 2 cells, so GFM "
        "renders no table there",
    ),
    (
        "a delimiter row out of place",
        HEAD + f"|---|\n| {MOBILE} |\n" + CLAUSE,
        stops_at("|---|", "a delimiter row out of place"),
    ),
    ("too few cells", HEAD + "|  |\n" + CLAUSE, "an empty row"),
    (
        "too many cells",
        HEAD + f"| {MOBILE} | the app |\n" + CLAUSE,
        stops_at(f"| {MOBILE} | the app |"),
    ),
    ("no closing pipe", HEAD + f"| {MOBILE}\n" + CLAUSE, stops_at(f"| {MOBILE}")),
    ("no opening pipe", HEAD + f"{MOBILE} |\n" + CLAUSE, stops_at(f"{MOBILE} |")),
]


@pytest.mark.parametrize(
    "text, said", [c[1:] for c in TABLE_ENDS], ids=[c[0] for c in TABLE_ENDS]
)
def test_every_way_the_table_ends_is_read_or_refused(text, said):
    signatories, refusals = config.pact_signatories(text)
    if said is None:
        assert refusals == [], refusals
        assert [s[1] for s in signatories] == ["example.com/org/orders-web"]
    else:
        assert any(said in r for r in refusals), refusals


ENTRY = "has a `Signatory` entry that will not read: "


@pytest.mark.parametrize(
    "row, sentence",
    [
        ("|  |", ENTRY + "an empty row"),
        (
            "| https://example.com/org/orders web |",
            ENTRY + "`https://example.com/org/orders web` holds a space — one "
            "remote URL per entry",
        ),
        (
            "| orders-mobile |",
            ENTRY + "`orders-mobile` is not a remote URL — it reduces to no host "
            "and path, so no repository can be found by it",
        ),
        (
            "| git@example.com:org/orders-web.git |",
            ENTRY + "`git@example.com:org/orders-web.git` and "
            "`https://example.com/org/orders-web` are one repository",
        ),
    ],
    ids=["empty", "a space", "not a url", "one repository"],
)
def test_every_entry_refusal_reads_after_the_pact(row, sentence):
    """Both callers print a table refusal after "the pact "; each sentence
    an entry can raise is pinned whole (round 2 of #647, white 14)."""
    text = HEAD + row + "\n" + CLAUSE
    _, refusals = config.pact_signatories(text)
    assert refusals == [sentence], refusals
    assert ("the pact " + sentence).count("the pact the") == 0
