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
import re
import sys
import unicodedata

import gfm_table_oracle as oracle
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


# --- #759: a pact row is read in one plain spelling -------------------------
#
# A `| Pact notify | always |` the table walk did not take was read as the
# default, and under `always` `evidence-check --reverify` re-stamped a moved
# row citing no clause with no record. The reader now takes a pact row in one
# spelling -- a walked row whose item is `Pact` or `Pact notify`, byte for
# byte -- and refuses every other line that names a pact (S1-S5 of work item
# 1791128260's `spec.md`). The corpus below is #784's generators, plus the
# spellings its round 4 found and never planted: every spelling any round of
# #784 found refuses here.

URL = "git@example.com:org/orders-api.git"
ORDERS = [(URL, "example.com/org/orders-api", "orders-api")]
CONFIG_TOP = "# config\n\n| Item | Value |\n|---|---|\n| Mode | shared |\n"
CONFIG = CONFIG_TOP + f"| Pact | {URL} |\n"
PLAIN = "| Pact notify | always |"
# The eight characters `str.splitlines` ends a line at and GFM does not.
SPLITLINES_ONLY = ["\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"]
# Every format character (Unicode category Cf).
FORMAT_CHARACTERS = [
    chr(c) for c in range(sys.maxunicode + 1) if unicodedata.category(chr(c)) == "Cf"
]


def refused(line, cell=False):
    """The sentence a line naming a pact is refused in, written here rather
    than asked of the reader, so the case pins what a person reads (S12).
    CELL is true where the line holds no `|` and is refused because the file
    holds an HTML table cell's tag (round 2 of PR #793, yellow 2)."""
    shown = "".join(
        f"<U+{ord(ch):04X}>"
        if (ch.isspace() and ch != " ") or unicodedata.category(ch) == "Cf"
        else ch
        for ch in line.strip()
    )
    return (
        f"`{shown}` names a pact and is not a `Pact` or `Pact notify` row in "
        "the one spelling read: write it as `| Pact | … |` or "
        "`| Pact notify | … |` inside the `| Item | Value |` table, or take it "
        "out of this file"
    ) + (
        "; this file holds an HTML table cell's tag, so a line with no `|` is "
        "refused too"
        if cell
        else ""
    )


# Delimiter rows by construction (round 2 of PR #793, yellow 1; round 3,
# yellow 1): the outer pipes each optional, one cell to three, a cell of one
# or three dashes with colons either side, padded with nothing or with each
# character Python calls whitespace that does not end a GFM line -- every
# one, so cmark-gfm, not a list, says which a delimiter row may hold. The
# plugin's GFM walker reads one as a delimiter row where `DELIMITER_ROW`
# matches and a pipe stands in it.
DELIMITERS = sorted(
    {
        left + "|".join([f"{pad}{cell}{pad}"] * cols) + right
        for left in ("", "|")
        for right in ("", "|")
        for cols in (1, 2, 3)
        for cell in ("-", "---", ":--", "--:", ":-:")
        for pad in (
            "",
            *(
                ch
                for ch in map(chr, range(sys.maxunicode + 1))
                if ch.isspace() and ch not in "\r\n"
            ),
        )
    }
)
WALKER_DELIMITERS = [
    d for d in DELIMITERS if config.DELIMITER_ROW.match(d) and "|" in d
]


# (id, text, the lines refused, the pacts read): #784's `STRAY_WAYS`, each a
# way the walk passes a pact row by.
STRAY_WAYS = [
    ("W1 above the header", PLAIN + "\n\n" + CONFIG, [PLAIN], ORDERS),
    (
        "W1 no header at all",
        f"| Pact | {URL} |\n{PLAIN}\n",
        [f"| Pact | {URL} |", PLAIN],
        [],
    ),
    (
        "W2 between the header and the first row",
        "| Item | Value |\n|---|---|\n | Pact notify | always |\n"
        f"| Mode | shared |\n| Pact | {URL} |\n",
        [" | Pact notify | always |"],
        ORDERS,
    ),
    ("W3 below a blank line", CONFIG + "\n" + PLAIN + "\n", [PLAIN], ORDERS),
    ("W4 prose", CONFIG + "Some prose.\n" + PLAIN + "\n", [PLAIN], ORDERS),
    ("W4 a heading", CONFIG + "## Notes\n" + PLAIN + "\n", [PLAIN], ORDERS),
    ("W4 a list item", CONFIG + "- a note\n" + PLAIN + "\n", [PLAIN], ORDERS),
    ("W4 a thematic break", CONFIG + "***\n" + PLAIN + "\n", [PLAIN], ORDERS),
    ("W4 an HTML block line", CONFIG + "<div>\n" + PLAIN + "\n", [PLAIN], ORDERS),
    (
        "W5 a second header",
        CONFIG + "| Item | Value |\n|---|---|\n" + PLAIN + "\n",
        [PLAIN],
        ORDERS,
    ),
    ("W6 a stray separator", CONFIG + "|---|---|\n" + PLAIN + "\n", [PLAIN], ORDERS),
    (
        "W7 a three-column header",
        CONFIG + "| A | B | C |\n" + PLAIN + "\n",
        [PLAIN],
        ORDERS,
    ),
    ("W8 indented", CONFIG + "  " + PLAIN + "\n", [PLAIN], ORDERS),
    ("W8 block-quoted", CONFIG + "> " + PLAIN + "\n", ["> " + PLAIN], ORDERS),
    ("W8 three cells", CONFIG + PLAIN + " x |\n", [PLAIN + " x |"], ORDERS),
    (
        "W8 no closing pipe",
        CONFIG + "| Pact notify | always\n",
        ["| Pact notify | always"],
        ORDERS,
    ),
    (
        "W8 an escaped pipe against the closing one",
        CONFIG + "| Pact notify | always\\|\n",
        ["| Pact notify | always\\|"],
        ORDERS,
    ),
    (
        "W10 a cut line",
        CONFIG + "\nprose\u2028" + PLAIN + "\n",
        ["prose\u2028" + PLAIN],
        ORDERS,
    ),
    (
        "W8 no leading pipe, directly under the table",
        CONFIG + "Pact notify | always |\n",
        ["Pact notify | always |"],
        ORDERS,
    ),
    (
        "W8 no leading pipe, punctuation before the item",
        CONFIG + "(Pact notify) | always |\n",
        ["(Pact notify) | always |"],
        ORDERS,
    ),
    *(
        (
            f"W8 no leading pipe, {mark!r} and U+{ord(space):04X} before the item",
            CONFIG + f"{mark}{space}Pact notify | always |\n",
            [f"{mark}{space}Pact notify | always |"],
            ORDERS,
        )
        for mark, space in (
            ("-", "\u00a0"),
            ("*", "\u00a0"),
            ("#", "\u00a0"),
            ("+", "\u00a0"),
            ("-", "\u2003"),
        )
    ),
    (
        "W8 no pipe at either end, directly under the table",
        CONFIG + "Pact notify | always\n",
        ["Pact notify | always"],
        ORDERS,
    ),
    # The pipe counts as written or decoded, as the word does.
    (
        "a pipe written as a reference",
        CONFIG + "Pact notify &#124; always\n",
        ["Pact notify &#124; always"],
        ORDERS,
    ),
    (
        "a fullwidth pipe",
        CONFIG + "Pact notify \uff5c always\n",
        ["Pact notify \uff5c always"],
        ORDERS,
    ),
    # Round 4 of PR #784, yellow 4: a row GFM keeps in the live table and the
    # walk does not take, with the item in a code span.
    *(
        (f"round 4, yellow 4: {why}", CONFIG + line + "\n", [line], ORDERS)
        for why, line in (
            ("no leading pipe", "`Pact notify` | always |"),
            ("no pipe at either end", "`Pact notify` | always"),
            ("no trailing pipe", "| `Pact notify` | always"),
            ("indented one space", " | `Pact notify` | always |"),
            ("a third cell", "| `Pact notify` | always | x |"),
        )
    ),
    # #784's S8, which it read: GFM's one line, which the reader cuts into
    # two pieces that are each a plain row. The line is refused whole.
    *(
        (
            f"one line of two plain rows, cut at U+{ord(ch):04X}",
            CONFIG_TOP + f"| Pact | {URL} |{ch}{PLAIN}\n",
            [f"| Pact | {URL} |{ch}{PLAIN}"],
            ORDERS,
        )
        for ch in SPLITLINES_ONLY
    ),
    # Round 1 of PR #793, yellow 2: an HTML table cell carries a value with
    # no pipe beside it, so a file holding one reads every line naming a
    # pact without the pipe condition.
    *(
        (f"an HTML table, {why}", CONFIG + "\n" + html, lines, ORDERS)
        for why, html, lines in (
            (
                "one line",
                "<table><tr><td>Pact notify</td><td>always</td></tr></table>\n",
                [("<table><tr><td>Pact notify</td><td>always</td></tr></table>", True)],
            ),
            (
                "a cell to a line",
                "<table>\n<tr>\n<td>Pact notify</td>\n<td>always</td>\n</tr>\n</table>\n",
                [("<td>Pact notify</td>", True)],
            ),
            (
                "the item on a line of its own",
                "<TABLE>\n<TR>\n<TD>\nPact notify\n</TD>\n<TD>always</TD>\n</TR>\n</TABLE>\n",
                [("Pact notify", True)],
            ),
        )
    ),
    # Round 2 of PR #793, yellow 2: the cause is named only on the line the
    # pipe condition alone would not refuse.
    (
        "an HTML table beside a piped line",
        CONFIG
        + "\n<table><tr><td>Pact notify</td><td>always</td></tr></table>\n\n"
        + PLAIN
        + "\n",
        [("<table><tr><td>Pact notify</td><td>always</td></tr></table>", True), PLAIN],
        ORDERS,
    ),
    # Round 1 of PR #793, yellow 3: a transposed table names the item in its
    # header and the value below it.
    *(
        (f"a transposed table, {why}", CONFIG + "\n" + table, [header], ORDERS)
        for why, header, table in (
            (
                "Pact first",
                "| Pact | Pact notify |",
                f"| Pact | Pact notify |\n|---|---|\n| {URL} | always |\n",
            ),
            (
                "another item first",
                "| Mode | Pact notify |",
                "| Mode | Pact notify |\n|---|---|\n| shared | always |\n",
            ),
        )
    ),
    # Round 2 of PR #793, yellow 1, and round 3, yellows 1 and 2: every table
    # cmark-gfm renders with `always` under a `Pact notify` header, over each
    # constructed delimiter row, behind each container -- none, a block
    # quote with and without its space, a block quote the header continues
    # lazily, a list item, three spaces, four spaces and a tab in. Its header
    # names a pact whether or not it holds a pipe, so it is refused, and a
    # copy with no `hooks/` is blind (S9 runs every row through it). Behind
    # a container the delimiter row is padded with spaces alone.
    *(
        (
            f"a table cmark-gfm renders, {where} over {d!r}",
            text,
            [first + head_line],
            ORDERS,
        )
        for d in DELIMITERS
        for where, before, first, rest in (
            ("at the margin", "", "", ""),
            ("in a block quote", "", "> ", "> "),
            ("in a block quote with no space", "", ">", ">"),
            ("continuing a block quote lazily", "> x\n", "", "> "),
            ("in a list item", "", "- ", "  "),
            ("three spaces in", "", "   ", "   "),
            ("four spaces in", "", "    ", "    "),
            ("a tab in", "", "\t", "\t"),
        )
        if where == "at the margin" or set(d) <= set("|-: ")
        for cols in [len(re.findall("-+", d))]
        for cells in [
            ("Mode", "Pact notify", "Note")[:cols] if cols > 1 else ("Pact notify",)
        ]
        for values in [("shared", "always", "x")[:cols] if cols > 1 else ("always",)]
        for head_line, body_line in [
            tuple(
                ("| " if d.startswith("|") else "")
                + " | ".join(row)
                + (" |" if d.endswith("|") else "")
                for row in (cells, values)
            )
        ]
        for text in [
            CONFIG
            + "\n"
            + before
            + first
            + head_line
            + "\n"
            + rest
            + d
            + "\n"
            + rest
            + body_line
            + "\n"
        ]
        if any(
            len(r) > cells.index("Pact notify")
            and r[cells.index("Pact notify")] == "always"
            for r in oracle.rows_under(text, cells) or []
        )
    ),
]


@pytest.mark.parametrize(
    "text, lines, pacts", [w[1:] for w in STRAY_WAYS], ids=[w[0] for w in STRAY_WAYS]
)
def test_s2_every_way_the_walk_passes_a_pact_row_by_is_refused(text, lines, pacts):
    """S2. Each way the table walk passes a pact row by: every line is
    refused, naming it, `notify` is None, and `pacts` is what the plain
    `Pact` row parsed."""
    assert config.pact_declaration(text) == (
        pacts,
        None,
        [refused(*x) if isinstance(x, tuple) else refused(x) for x in lines],
    )


# #784's generators of spellings of the item: emphasis, strikethrough, links,
# images, autolinks, raw HTML, code spans, escapes and references around it,
# and characters joining or splitting its words (`WRAPS` x items, `JOINS`,
# `SPLITS`). #784 held each to cmark-gfm; here every one names a pact, so
# every one refuses, including those GFM shows as another word.
WRAPS = {
    "emphasis": ["**{}**", "*{}*", "__{}__", "_{}_", "***{}***"],
    "strikethrough": ["~~{}~~", "~{}~"],
    "a link": [
        "[{}]()",
        "[{}](https://example.com/x)",
        '[{}](x "a)b")',
        "[{}](x 'a)b')",
        # Round 4 of PR #784, yellow 1.
        "[{}](it's)",
        '[{}](a"b)',
        "[{}](a(b(c)))",
        '[{}](x "a\\"b")',
        "[{}](a\\)b)",
        "[{}](<a)b>)",
    ],
    "an image": ["![{}]()", '![{}](x "t")', "![a [b] c](x){}"],
    "an autolink": [
        "<https://example.com/{}>",
        "<{}@example.com>",
        "<https://example.com>{}",
        "<a@example.com>{}",
    ],
    "raw HTML": [
        "<b>{}</b>",
        '<span title="a">{}</span>',
        '<span title="a>b">{}</span>',
        "<{}>",
        "<!-- a note -->{}",
        "<!-- {} -->",
        "<?x?>{}",
        "<![CDATA[]]>{}",
        "<![CDATA[{}]]>",
        "<![CDATA[a>b]]>{}",
        "<!X y>{}",
        "<!X 'a>b'>{}",
        # Round 4 of PR #784, yellow 2: an empty comment.
        "<!-->{}<!-- -->",
        "<!--->{}<!-- -->",
    ],
    "a code span": ["`{}`", "**`{}`**", "`{}`.", "{}`", "&#96;{}&#96;"],
    "a backslash escape": ["\\*{}\\*", "\\_{}\\_", "\\[{}\\]"],
    "entity-encoded punctuation": [
        "&ast;{}&ast;",
        "&lowbar;{}&lowbar;",
        "&#91;{}&#93;&#40;&#41;",
    ],
    "plain punctuation": ["({})"],
}
JOINS = [
    "&#32;",
    "&nbsp;",
    "&#x200B;",
    "&#8203;",
    "\u200b",
    "<b></b>",
    "<?x?>",
    "<![CDATA[]]>",
    "<!X y>",
    "* *",
    "_",
    "-",
    ".",
    "\\ ",
    "&ast;",
    "\u00a0",
    # Round 4 of PR #784, yellow 3: a legacy name with no `;`.
    "&",
    " &",
    "&nbsp ",
]
SPLITS = [
    "*Pact* *notify*",
    "**Pact** notify",
    "[Pact]() notify",
    "<i>Pact</i> notify",
    "Pact <i>notify</i>",
    "P&#97;ct notify",
    "P&#x61;ct notify",
    "`Pact` notify",
    "Pact `notify`",
    "Pact notify 2",
    "Pact 2 notify",
    "Pacts notify",
    "Pact notifyx",
]
MARKUP = sorted(
    {
        wrap.format(item)
        for wraps in WRAPS.values()
        for wrap in wraps
        for item in (
            "Pact notify",
            "Pact",
            "Pact notify 2",
            "Pact 2 notify",
            "Pacts notify",
            "Pact notifyx",
        )
    }
    | {f"Pact{j}notify" for j in JOINS}
    | set(SPLITS)
)
# Items the walk takes, each spelled another way: #784's S3 rows, its
# code-span rows, every format character at three places, and the markup.
OTHER_ITEMS = [
    "pact notify",
    "Pact  notify",
    "Pact\u00a0notify",
    "PACT",
    "Pact Notify",
    "Pact\\|notify",
    "Pact&#124;notify",
    "` Pact notify `",
    "`Pact  notify`",
    *(
        spelled
        for ch in FORMAT_CHARACTERS
        for spelled in (f"Pa{ch}ct notify", f"Pact{ch}notify", f"Pact notify{ch}")
    ),
    *MARKUP,
]


@pytest.mark.parametrize("place", ["in the table", "below a blank line"])
@pytest.mark.parametrize("item", OTHER_ITEMS, ids=[ascii(i) for i in OTHER_ITEMS])
def test_s2_a_pact_item_spelled_another_way_is_refused(item, place):
    """S2. Each spelling of #784's generators, as a row inside the table
    under a `Pact` value and again below a blank line: refused, naming the
    line, with `notify` None. In the table the walk takes it under another
    item; below, the walk does not reach it."""
    row = f"| {item} | always |"
    text = CONFIG + ("" if place == "in the table" else "\n") + row + "\n"
    assert config.pact_declaration(text) == (ORDERS, None, [refused(row)])


@pytest.mark.parametrize(
    "ch", SPLITLINES_ONLY, ids=[f"U+{ord(c):04X}" for c in SPLITLINES_ONLY]
)
def test_s2_a_notify_row_a_splitlines_character_cuts_is_refused(ch):
    """S2, #784's W11. GFM shows one row, and the reader cuts it into two
    pieces neither of which is a row: the GFM line is read whole."""
    row = f"| Pact notify | {ch}always |"
    assert config.pact_declaration(CONFIG + row + "\n") == (
        ORDERS,
        None,
        [refused(row)],
    )


def test_s1_the_plain_spelling_is_read():
    """S1. A plain `Pact notify` row in the table is read, and the
    template's empty pair is no pact and no refusal."""
    assert config.pact_declaration(CONFIG + PLAIN + "\n") == (ORDERS, "always", [])
    assert config.pact_declaration(
        CONFIG_TOP + "| Pact |  |\n| Pact notify |  |\n"
    ) == ([], None, [])


@pytest.mark.parametrize("line", [f"| Pact | {URL} |", PLAIN])
def test_s3_a_pact_line_with_no_pact_in_the_table_is_refused(line):
    """S3. No plain `Pact` row, and a line naming a pact below the table:
    refused all the same. Telling a mangled `Pact` line from a mangled
    notify line would need the item read through markup."""
    assert config.pact_declaration(CONFIG_TOP + "\n" + line + "\n") == (
        [],
        None,
        [refused(line)],
    )


def test_s3_a_plain_notify_row_with_no_pact_is_still_ignored():
    """S3. A plain `Pact notify` row in the table with no `Pact` row is
    ignored, as before #759."""
    assert config.pact_declaration(CONFIG_TOP + PLAIN + "\n") == ([], None, [])


# (below `CONFIG`, the notify read): lines that name no pact in another
# spelling, each read as the table says.
SILENT = [
    ("| Broad gate | bin/test -k pact |\n", config.NOTIFY_DEFAULT),
    ("\nThe impact | compact of this.\n", config.NOTIFY_DEFAULT),
    ("\n<!-- this repository signs the orders pact -->\n", config.NOTIFY_DEFAULT),
    ("\nThis repository signs the orders pact: always.\n", config.NOTIFY_DEFAULT),
    ("|\u00a0Pact notify\u00a0| always |\n", "always"),
    # Round 3 of PR #793: a run of dashes alone under a line is a setext
    # underline, not a delimiter row, so a heading naming a pact is prose.
    ("\nThis repository signs the orders pact\n---\n", config.NOTIFY_DEFAULT),
]


@pytest.mark.parametrize(
    "below, notify",
    SILENT,
    ids=[
        "a walked row's value",
        "impact and compact with a pipe",
        "a comment with no pipe",
        "prose with no pipe",
        "a no-break space beside a pipe",
        "a setext heading naming a pact",
    ],
)
def test_s4_a_line_that_is_not_a_pact_row_in_another_spelling_is_silent(below, notify):
    """S4. A walked row's value is not read, a letter before the `p` keeps
    `impact` and `compact` silent, a line with no pipe carries no value, and
    a no-break space beside a pipe is the walk's own whitespace."""
    assert config.pact_declaration(CONFIG + below) == (ORDERS, notify, [])


def _broad_gate_block():
    """The prose `skills/config/SKILL.md` step 3 tells a session to copy
    below the live table: `templates/config.md` from `## Broad gate` down to
    `### What is refused, and what stays allowed`."""
    with open(os.path.join(ROOT, "templates", "config.md"), encoding="utf-8") as f:
        text = f.read()
    start = text.index("## Broad gate\n")
    return text[start : text.index("### What is refused, and what stays allowed")]


def test_s4_the_configs_this_plugin_writes_or_copies_are_silent():
    """S4. This repository's own `seal/config.md`, the stub `seal mode`
    writes, and that stub with the copied `## Broad gate` block below it --
    with and without the pact rows `orchestration.md` writes into the table
    -- give no refusal. Each is read from the tree, not retyped."""
    seal = load_hook_module(
        os.path.join("..", "skills", "implement", "scripts", "seal.py"),
        "seal_for_the_silent_set",
    )
    with open(os.path.join(ROOT, "seal", "config.md"), encoding="utf-8") as f:
        assert config.pact_declaration(f.read()) == ([], None, [])
    stub = seal.NEW_CONFIG.format(item="Mode", value="shared")
    block = _broad_gate_block()
    assert "Broad gate" in block and "pact" not in block.lower()
    assert config.pact_declaration(stub) == ([], None, [])
    assert config.pact_declaration(stub + "\n" + block) == ([], None, [])
    signed = stub + f"| Pact | {URL} |\n| Pact notify | when the pact is touched |\n"
    assert config.pact_declaration(signed + "\n" + block) == (
        ORDERS,
        config.NOTIFY_TOUCHED,
        [],
    )
    # Round 1 of PR #793, yellow 1: `skills/commit-pr-convention/SKILL.md`
    # tells a session to copy `templates/config.md` whole, so the template is
    # a config too: no pact and no refusal to either reader, and `always`
    # once its two rows are filled.
    with open(os.path.join(ROOT, "templates", "config.md"), encoding="utf-8") as f:
        template = f.read()
    assert config.pact_declaration(template) == ([], None, [])
    assert ec.notify_may_be_always(template) is False
    filled = template.replace("| Pact |  |\n", f"| Pact | {URL} |\n", 1).replace(
        "| Pact notify |  |\n", "| Pact notify | always |\n", 1
    )
    assert config.pact_declaration(filled) == (ORDERS, config.NOTIFY_ALWAYS, [])
    assert ec.notify_may_be_always(filled) is True


@pytest.mark.parametrize(
    "below",
    ["\n```\n" + PLAIN + "\n```\n", "\n<!--\n" + PLAIN + "\n-->\n"],
    ids=["a closed fence", "a closed comment"],
)
def test_s5_a_plain_row_in_a_fence_or_a_comment_is_refused_and_not_read(below):
    """S5. Fences and comments are read through: an example there refuses,
    and the walk still does not read it, so `notify` is None, not
    `always`."""
    assert config.pact_declaration(CONFIG + below) == (ORDERS, None, [refused(PLAIN)])


def test_a_refusal_comes_after_a_doubled_pact_and_before_the_entries():
    """Data: one refusal per refused line, in file order, after the
    doubled-`Pact` refusal and before the entry refusals."""
    text = (
        CONFIG_TOP
        + "| Pact | orders-api |\n| Pact | git@example.com:org/b.git |\n"
        + "\n"
        + PLAIN
        + "\n**Pact**: x |\n"
    )
    _pacts, notify, refusals = config.pact_declaration(text)
    assert notify is None
    assert refusals[0].startswith("`Pact` appears 2 times")
    assert refusals[1:3] == [refused(PLAIN), refused("**Pact**: x |")]
    assert "is not a remote URL" in refusals[3] and len(refusals) == 4


def test_config_rows_is_the_indexed_walk_without_its_places():
    """`config_rows` returns what it returned before the walk kept indices:
    the index is the place in `text.splitlines()` each row came from."""
    text = CONFIG + PLAIN + "\n\n| Broad gate | x |\n"
    indexed = config.indexed_config_rows(text)
    lines = text.splitlines()
    assert [(i, v) for _, i, v in indexed] == config.config_rows(text)
    assert all(lines[n].startswith(f"| {item} |") for n, item, _ in indexed)
    assert [item for _, item, _ in indexed] == ["Mode", "Pact", "Pact notify"]


def _vendored_checker():
    path = os.path.join(
        ROOT, "skills", "evidence-check", "scripts", "evidence_check.py"
    )
    spec = importlib.util.spec_from_file_location("ec_for_one_spelling", path)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    return ec


ec = _vendored_checker()
# Every S2 text: the ways the walk passes a row by, the cut rows, and each
# other spelling of the item in the table and below a blank line.
S2_TEXTS = [
    *(text for _id, text, _lines, _pacts in STRAY_WAYS),
    *(CONFIG + f"| Pact notify | {ch}always |\n" for ch in SPLITLINES_ONLY),
    *(
        CONFIG + gap + f"| {item} | always |\n"
        for item in OTHER_ITEMS
        for gap in ("", "\n")
    ),
]


def test_s9_the_vendored_copy_cannot_rule_always_out_on_any_s2_text():
    """S9 (a). A copy with no `hooks/` leaves a moved row citing no clause
    wherever `Pact notify` may be `always`. Over every S2 text, under a
    `Pact` value, its decision says it may, so each leaves the row where the
    plugin refuses. `tests/test_a_signatory_records_a_pact_change.py` runs a
    sample of them end to end."""
    missed = [t for t in S2_TEXTS if not ec.notify_may_be_always(t)]
    assert missed == [], missed[:5]


def test_s9_the_vendored_copy_reads_the_silent_set_as_the_table_says():
    """S9 (b). Where the plugin reads no refusal, the copy is blind exactly
    where the table's notify is `always`: a plain row of each, both carrying
    a value. A plain notify row with no `Pact` value, the template's empty
    pair, and this repository's own config re-stamp."""
    for below, notify in SILENT:
        assert ec.notify_may_be_always(CONFIG + below) == (notify == "always"), below
    assert ec.notify_may_be_always(CONFIG_TOP + PLAIN + "\n") is False
    assert (
        ec.notify_may_be_always(CONFIG_TOP + "| Pact |  |\n| Pact notify |  |\n")
        is False
    )
    assert ec.notify_may_be_always(None) is True
    # Round 2 of PR #793, yellow 1: the copy reads a line as a table's header
    # wherever the plugin's walker reads the line under it as a delimiter
    # row. Round 3 widened the copy to what cmark-gfm renders, held in
    # `STRAY_WAYS`, so here it is at least the walker, not exactly.
    for d in WALKER_DELIMITERS:
        text = CONFIG + f"\n| Mode | Pact notify |\n{d}\n| shared | always |\n"
        assert ec.notify_may_be_always(text) is True, repr(d)
    with open(os.path.join(ROOT, "seal", "config.md"), encoding="utf-8") as f:
        assert ec.notify_may_be_always(f.read()) is False


@pytest.mark.parametrize(
    "ch", SPLITLINES_ONLY, ids=[f"U+{ord(c):04X}" for c in SPLITLINES_ONLY]
)
def test_s9_a_pact_row_a_splitlines_character_cuts_is_no_plain_row(ch):
    """S9. A `Pact` row with a `str.splitlines`-only character in its value
    is one GFM line the walk never took, so the reader refuses it with no
    notify row anywhere, and the vendored copy, which judges a line by its
    row shape, does not count it as a plain row: it leaves the moved row
    where the plugin does, though the shape alone would read a plain row."""
    line = f"| Pact | {ch}{URL} |"
    assert config.pact_declaration(CONFIG_TOP + line + "\n") == (
        [],
        None,
        [refused(line)],
    )
    assert ec.CONFIG_ROW_RE.match(line) is not None
    assert ec.notify_may_be_always(CONFIG_TOP + line + "\n") is True


def test_s10_the_reader_and_the_vendored_copy_read_one_word():
    """S10. A copy with no `hooks/` names a pact by the same word and the
    same predicate as the plugin's reader: the patterns are equal, and the
    two predicates answer alike on every S2 and S4 line, piped or not."""
    assert (config.PACT_WORD.pattern, config.PACT_WORD.flags) == (
        ec.PACT_WORD.pattern,
        ec.PACT_WORD.flags,
    )
    assert (config.HTML_CELL.pattern, config.HTML_CELL.flags) == (
        ec.HTML_CELL.pattern,
        ec.HTML_CELL.flags,
    )
    assert config.UNDER_A_HEADER.pattern == ec.UNDER_A_HEADER.pattern
    lines = {line for text in S2_TEXTS for line in text.splitlines()}
    lines |= {line for below, _ in SILENT for line in (CONFIG + below).splitlines()}
    lines |= set(OTHER_ITEMS)
    for line in sorted(lines):
        for piped in (True, False):
            assert config.names_a_pact(line, piped) == ec.names_a_pact(line, piped), (
                line,
                piped,
            )


# A letter between the word's letters, or a look-alike letter.
BLIND_SIDE = [
    "P<b></b>act notify",
    "[P](x)act notify",
    "P&zz;act notify",
    "P\u0430ct notify",
    # Round 1 of PR #793, white 6: a look-alike from its own script.
    "\u1d18\u1d00\u1d04\u1d1b notify",
]


@pytest.mark.parametrize("gap", ["", "\n"], ids=["in the table", "below it"])
@pytest.mark.parametrize("item", BLIND_SIDE, ids=ascii)
def test_the_blind_side_is_read_as_no_line(item, gap):
    """Q1's default, stated in `docs/the-pact.md` §*What this does not see*:
    a spelling that puts a letter between the word's letters, or spells it
    with a look-alike letter, names no pact to either reader,
    so the table's notify is read. A change to Q1's answer turns this red."""
    text = CONFIG + gap + f"| {item} | always |\n"
    assert config.pact_declaration(text) == (ORDERS, config.NOTIFY_DEFAULT, [])
    assert ec.notify_may_be_always(text) is False


@pytest.mark.parametrize(
    "parts, sentence",
    [
        (
            ("docs", "the-pact.md"),
            "**A pact row is read in one spelling, and every other line of "
            "`seal/config.md` that names a pact is refused.**",
        ),
        (
            ("docs", "the-pact.md"),
            "On a row of the table only the item is read, so a value that mentions "
            "a pact is never refused.",
        ),
        (
            ("docs", "the-pact.md"),
            "An example kept in a fence or a comment is refused too, because "
            "telling it from a live row would mean modelling GFM; delete it.",
        ),
        (
            ("docs", "the-pact.md"),
            "A line with no `|` has no value cell, so the pact can be named in prose.",
        ),
        (
            ("docs", "the-pact.md"),
            "**A pact line with a letter written between the word's letters, or "
            "with a look-alike letter, from another script or its own, is read as "
            "no line at all.**",
        ),
        (
            ("docs", "the-pact.md"),
            "So does `P\u0430ct` spelled with a Cyrillic `\u0430`, U+0430, and "
            "`\u1d18\u1d00\u1d04\u1d1b` in Latin small capitals, which NFKC does not fold.",
        ),
        (
            ("docs", "the-pact.md"),
            "as written or with its character references decoded and its "
            "compatibility letters folded (NFKC), so a fullwidth or mathematical "
            "`Pact` names one and `impact` names none.",
        ),
        (
            ("docs", "the-pact.md"),
            "In a file that holds an HTML table cell's tag, `<td>` or `<th>`, "
            "anywhere, a code span, a fence or a comment included, a line naming a "
            "pact is refused with or without a `|`, because such a cell carries a "
            "value with no pipe beside it; take the tag out to name the pact in "
            "prose again.",
        ),
        (
            ("docs", "the-pact.md"),
            "YAML front matter is not read either: github.com shows it as a table, "
            "cmark-gfm does not, and a line of it naming a pact is refused only "
            "where it holds a `|`.",
        ),
        (
            ("templates", "config.md"),
            "**Both rows are read only where the table above holds them, spelled "
            "exactly `Pact` and `Pact notify`.**",
        ),
        (
            ("templates", "config.md"),
            "Written anywhere but the table above, or spelled any other way, it is "
            "refused, not absent",
        ),
        (
            ("templates", "config.md"),
            "A sentence with no pipe in it may name the pact freely, which is why "
            "this section is written without one: this file can be copied whole.",
        ),
        (
            ("templates", "config.md"),
            "A file that also holds an HTML table cell's tag, a `td` or `th` opened "
            "with a `<`, anywhere, a comment or a code span included, refuses such a "
            "sentence too, so keep that tag out of this file.",
        ),
        (
            ("docs", "the-pact.md"),
            "A line standing directly over a table's delimiter row is that table's "
            "header, and a one-column table needs no pipe anywhere, so such a line "
            "naming a pact is refused with or without a `|`, inside a block quote "
            "or a list item too.",
        ),
        (
            ("templates", "config.md"),
            "So does a line of dashes and colons directly under the sentence, which "
            "makes it a one-column table's header.",
        ),
    ],
    ids=[
        "the pact: the rule",
        "the pact: a walked row's item alone",
        "the pact: an example refuses",
        "the pact: no pipe",
        "the pact: the blind side",
        "the pact: a look-alike letter",
        "the pact: the NFKC fold, round 1 of PR #793",
        "the pact: an HTML table cell, round 1 of PR #793",
        "the pact: YAML front matter, round 1 of PR #793",
        "template: the rule",
        "template: the Absent cell",
        "template: no pipe",
        "template: an HTML table cell's tag, round 2 of PR #793",
        "the pact: a table's header, round 3 of PR #793",
        "template: a table's header, round 3 of PR #793",
    ],
)
def test_s12_the_documents_say_a_pact_row_is_read_in_one_spelling(parts, sentence):
    """S12 of #759. Each sentence a person reads about the one spelling is
    pinned whole; the refusal's own text is pinned by `refused` above."""
    assert sentence in flat(*parts), sentence


# --- the shipped rows -------------------------------------------------------


def test_the_template_and_the_config_skill_carry_both_rows_and_the_vocabulary():
    """`templates/config.md` documents both rows and keeps the notify words
    out of translation; `/specseal:config` shows both."""
    template = flat("templates", "config.md")
    skill = flat("skills", "config", "SKILL.md")
    for row in (config.PACT_ROW, config.PACT_NOTIFY_ROW):
        assert f"**`{row}`**" in template, row
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
