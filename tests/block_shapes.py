"""The shapes `seal/specs/1790645290-the-hooks-and-the-rider-check-read-
fences-and-comments-by-one-rule/spec.md` §*The shapes* names, as lines (#667).

Data and nothing else. Each shape is the document one row of that table is
about, and `RENDERER` is the frame's *Renderer* column turned into the lines
a CommonMark renderer hides, derived by reading the specification when the
frame was drawn. `tests/test_the_hooks_hide_what_a_renderer_hides.py` holds
the oracle to that column (the frame's Q2) and then holds every reader to the
oracle over these shapes and a generated corpus.

Most shapes are work item 1790635413's own test strings, taken verbatim at
`4edc5de6`, because each is a place a previous attempt at these readers was
wrong. The texts that hold an HTML comment opener build it by concatenation,
so that no line of this file begins with one: the rider check reads `.py`
files under `tests/` too.
"""

OPEN = "<" + "!--"
CLOSE = "-->"
RIDER = OPEN + " RIDER:"

# The characters `str.splitlines` ends a line at and CommonMark does not:
# CommonMark ends one at LF, CR and CRLF alone (#667 round 1, 🟡 1; #664's
# class). Spelled by code point, so no line of this file holds one.
BREAKS = {
    "LS": chr(0x2028),
    "PS": chr(0x2029),
    "NEL": chr(0x85),
    "FF": chr(0x0C),
    "VT": chr(0x0B),
    "FS": chr(0x1C),
    "GS": chr(0x1D),
    "RS": chr(0x1E),
}

CHAIN = "through the review chain"
DIRECT = "straight to the PR"

# `tests/test_routing_is_recorded.py#two_axis_text`, as lines.
TABLE = [
    "| Axis | Answer |",
    "|---|---|",
    f"| Review | {CHAIN} |",
    "| Destination | open the pull request |",
    "| Branch | feature/x |",
]

CONFIG = ["| Item | Value |", "|---|---|"]

SHAPES = {
    # --- the config reader ---------------------------------------------------
    "C1": [
        f"To park a row, open it with `{OPEN}`.",
        "",
        *CONFIG,
        "| Mode | shared |",
        "| Broad gate | bin/test -q |",
        "",
        f"and close it with `{CLOSE}`.",
    ],
    "C2": [
        f"{OPEN} a note, with an example:",
        "```",
        "an example",
        CLOSE,
        "",
        *CONFIG,
        "| Mode | shared |",
    ],
    "C3": [
        "# c",
        "",
        f"write {OPEN} to start a note.",
        "",
        "```",
        *CONFIG,
        "| Mode | local |",
        "| Broad gate | true |",
        "```",
        "",
        *CONFIG,
        "| Mode | shared |",
        "| Broad gate | bin/test |",
    ],
    "C4": [
        f"note {OPEN} stray",
        "",
        *CONFIG,
        "| Mode | shared |",
        "| Broad gate | bin/test -q |",
        "",
        "```",
        f"{OPEN} c {CLOSE}",
        "| Mode | local |",
        "```",
    ],
    "C5": [
        *CONFIG,
        f"{OPEN} the command before the move, kept for reference",
        "| Broad gate | old -q |",
        CLOSE,
        "| Mode | shared |",
        "| Broad gate | bin/test -q |",
    ],
    "C6": [
        "# Repository config",
        "",
        OPEN,
        *CONFIG,
        "| Mode | local |",
        "| Broad gate | old -q |",
        CLOSE,
        "",
        *CONFIG,
        "| Mode | shared |",
        "| Broad gate | bin/test -q |",
    ],
    "C8": [*CONFIG, OPEN, "| Broad gate | a | b |", CLOSE, "| Mode | shared |"],
    "C9a": [f"{OPEN} a note nobody closed", "", *CONFIG, "| Mode | shared |"],
    "C9b": [
        *CONFIG,
        f"{OPEN} open",
        "| Mode | shared |",
        "| Broad gate | bin/test -q |",
    ],
    "C10": [*CONFIG, OPEN, "| Mode | local |", CLOSE, "| Mode | local |"],
    "C11a": [
        *CONFIG,
        "| Mode | shared |",
        OPEN,
        "| Broad gate | bin/test -q |",
        CLOSE,
    ],
    "C11b": [
        *CONFIG,
        "| Mode | shared |",
        "",
        f"{OPEN} parked until the suite is green",
        "| Mode | local |",
        "| Broad gate | bin/test -q |",
        CLOSE,
    ],
    "C12": [
        "```",
        *CONFIG,
        "| Mode | local |",
        "```",
        "",
        *CONFIG,
        "| Mode | shared |",
    ],
    "C13": [f"a lone ` then {OPEN} x", "| a | b |", CLOSE, "| c | d |"],
    "C14": ["```", *CONFIG, "| Mode | shared |"],
    # --- the routing reader ---------------------------------------------------
    "R1": [
        *TABLE,
        "",
        "An example of the other answer:",
        "",
        "```markdown",
        f"| Review | {DIRECT} |",
        "| Branch | somebody-else |",
        "```",
    ],
    "R2": ["~~~", *TABLE, "~~~"],
    "R3": ["```", *TABLE],
    "R4": [f"{OPEN} a note, with an example:", "```", "an example", CLOSE, "", *TABLE],
    "R5": [*TABLE, "", f"{OPEN} the answer before:", f"| Review | {DIRECT} |", CLOSE],
    "R6": [
        *TABLE,
        "",
        f"A note: {OPEN} nobody closed this.",
        "",
        "```markdown",
        f"| Review | {DIRECT} |",
        "```",
    ],
    # R6 with no blank line between the note and the fence: a fence line
    # interrupts the paragraph the opener stands in, so the fence still opens.
    "R6b": [
        *TABLE,
        "",
        f"A note: {OPEN} nobody closed this.",
        "```markdown",
        f"| Review | {DIRECT} |",
        "```",
    ],
    "R7": [
        f"note {OPEN} stray",
        "",
        *TABLE,
        "",
        "```",
        f"{OPEN} c {CLOSE}",
        f"| Review | {DIRECT} |",
        "```",
    ],
    "R8": [
        *TABLE,
        "",
        f"{OPEN} nobody closed this",
        "",
        "```",
        f"| Review | {DIRECT} |",
        "```",
    ],
    "R9": [f"{OPEN} the table below is parked", *TABLE, CLOSE],
    # --- the rider check --------------------------------------------------------
    "K1": [
        "# doc",
        "",
        f"{RIDER} one",
        "```python",
        "snippet",
        f"Verified 2026-01-01 against x@abcdef12. {CLOSE}",
        "",
        "prose",
        "",
        f"{RIDER} two",
        f"Verified 2026-01-01 against y@abcdef12. {CLOSE}",
    ],
    "K2": [
        "# doc",
        "",
        f"A rider opens with `{OPEN}` and a marker.",
        "",
        "```markdown",
        f"{RIDER} quoted",
        f"Verified 2026-01-01 against q@abcdef12. {CLOSE}",
        "```",
        "",
        "prose",
        "",
        f"{RIDER} real",
        f"Verified 2026-01-01 against r@abcdef12. {CLOSE}",
    ],
    "K3": [
        "# doc",
        "",
        f"Write {OPEN} to open a note.",
        "",
        "```markdown",
        f"{RIDER} quoted",
        f"Verified 2026-01-01 against q@abcdef12. {CLOSE}",
        "```",
        "",
        "prose",
        "",
        f"{RIDER} real",
        f"Verified 2026-01-01 against r@abcdef12. {CLOSE}",
    ],
    "K4": [
        f"a lone ` then {OPEN} a note",
        "```",
        CLOSE,
        "",
        f"{RIDER} real",
        f"Verified 2026-01-01 against r@abcdef12. {CLOSE}",
    ],
    "K5": [
        "# X",
        "",
        "A rider looks like:",
        "",
        "```",
        f"{RIDER} the claim {CLOSE}",
        "```",
    ],
    "K7": [
        f"{RIDER} two",
        f"Verified 2026-01-01 against y@abcdef12. {CLOSE}",
        "",
        "```",
        f"{RIDER} quoted {CLOSE}",
        "```",
    ],
}

# C7 is C5 written with CRLF endings, as a reader that keeps its endings
# splits it.
SHAPES["C7"] = [line + "\r" for line in SHAPES["C5"]]


def span(first, last):
    return set(range(first, last + 1))


# The frame's *Renderer* column as hidden lines, derived by reading the
# CommonMark specification (§4.5 fences, §4.6 HTML blocks, §6.6 inline raw
# HTML) and GFM's table extension, before anything was parsed.
RENDERER = {
    "C1": set(),
    "C2": span(0, 3),
    "C3": span(4, 9),
    "C4": span(7, 10),
    "C5": span(2, 4),
    "C6": span(2, 7),
    "C7": span(2, 4),
    "C8": span(2, 4),
    "C9a": span(0, 4),
    "C9b": span(2, 4),
    "C10": span(2, 4),
    "C11a": span(3, 5),
    "C11b": span(4, 7),
    "C12": span(0, 4),
    "C13": {1, 2},
    "C14": span(0, 3),
    "R1": span(8, 11),
    "R2": span(0, 6),
    "R3": span(0, 5),
    "R4": span(0, 3),
    "R5": span(6, 8),
    "R6": span(8, 10),
    "R6b": span(7, 9),
    "R7": span(8, 11),
    "R8": span(6, 10),
    "R9": span(0, 6),
    "K1": span(2, 5) | span(9, 10),
    "K2": span(4, 7) | span(11, 12),
    "K3": span(4, 7) | span(11, 12),
    "K4": span(1, 5),
    "K5": span(4, 6),
    "K7": span(0, 1) | span(3, 5),
}
