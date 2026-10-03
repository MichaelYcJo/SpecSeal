#!/usr/bin/env python3
"""Draw the release's seal as a PNG, attach it, and put it in the note (#718).

The 0.17.0 seal was drawn by hand: a script outside the tree read the cells
`seal_stamp.compose` builds, painted each the way `seal_stamp.block` describes
it, and the PNG was uploaded and edited into the note. This is that script,
in the tree and run by the tag push.

**One cell, one rectangle.** A cell of the letter is two halves and maybe a
character. `paint` turns each into rectangles and text in a `CELL_W` x
`CELL_H` pixel cell, each half `CELL_H // 2` tall, and `png` rasterises them.
So the PNG is the terminal form at a fixed pixel size: the same cells, the
same colours through xterm's 256-colour table (`rgb`), and transparent where
the terminal form paints nothing. `paint` is kept free of Pillow, so the case
that pins it against `block` runs on any interpreter, and Pillow is imported
inside `png` alone.

**Pillow is a test-and-release dependency, never a plugin one.** The gates
are stdlib-only (`CONTRIBUTING.md` §*Running the checks*), and nothing under
`hooks/` or `skills/` imports this file or Pillow. The version is pinned once,
in `.github/scripts/run_tests.py#PILLOW`.
"""

import functools
import importlib.util
import os
import re
import xml.etree.ElementTree as ElementTree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


# The tree's own modules are loaded when first asked for, not at import: a
# module that will not load is one more way for the seal to fail, and every
# way it fails has to end in today's note and an exit of 0 (`main`), which an
# import at the top of this file would end before `main` ran.
def module(name, *parts):
    """The tree's module at `ROOT/<parts>`, loaded once under `name`."""
    return _module(name, os.path.join(ROOT, *parts))


@functools.cache
def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def stamp():
    """`skills/verify/scripts/seal_stamp.py`, whose `compose`, `block` and
    `DEFAULT_SCALE` this draws with."""
    return module("specseal_seal_stamp", "skills", "verify", "scripts", "seal_stamp.py")


# One cell of the letter in pixels, and the size its characters are drawn
# at: the hand-drawn 0.17.0 seal's, which the owner saw on the release page.
CELL_W, CELL_H = 14, 28
FONT_SIZE = 22

# xterm's 256-colour table past the sixteen system colours: a 6x6x6 cube on
# these levels, then a ramp of 24 greys. The system colours are a terminal's
# own choice, and the sheet uses none of them.
CUBE_LEVELS = (0, 95, 135, 175, 215, 255)


def rgb(colour):
    """`colour` as an `(r, g, b)` triple: a triple as it is, and a
    256-colour code through xterm's cube and grey ramp. Raises `ValueError`
    for 0-15, whose values a terminal chooses."""
    if isinstance(colour, tuple):
        return colour
    if 16 <= colour <= 231:
        n = colour - 16
        return (CUBE_LEVELS[n // 36], CUBE_LEVELS[n // 6 % 6], CUBE_LEVELS[n % 6])
    if 232 <= colour <= 255:
        grey = 8 + 10 * (colour - 232)
        return (grey, grey, grey)
    raise ValueError(f"no fixed colour for 256-colour code {colour}")


def size(letter):
    """The PNG's `(width, height)` in pixels for `letter`'s cells."""
    width = max((len(line) for line in letter.cells), default=0)
    return width * CELL_W, len(letter.cells) * CELL_H


def paint(letter):
    """`letter`'s cells as drawing operations, in the order they are laid.

    Each is `("rect", x0, y0, x1, y1, rgb)` with the corners inclusive, or
    `("text", cx, cy, character, rgb, bold)` centred on the cell. A cell
    takes its background over the whole cell, then the half its half-block
    colours, or its character; a cell `block` paints nothing gets nothing,
    which is what leaves it transparent. The title line, the letter's
    second, is bold, the way `compose` inks it in `TITLE`."""
    ops, half = [], CELL_H // 2
    for y, line in enumerate(letter.cells):
        for x, cell in enumerate(line):
            char, fg, bg = stamp().block(cell)
            x0, y0 = x * CELL_W, y * CELL_H
            x1, y1 = x0 + CELL_W - 1, y0 + CELL_H - 1
            if bg is not None:
                ops.append(("rect", x0, y0, x1, y1, rgb(bg)))
            if char == "▀":
                ops.append(("rect", x0, y0, x1, y0 + half - 1, rgb(fg)))
            elif char == "▄":
                ops.append(("rect", x0, y0 + half, x1, y1, rgb(fg)))
            elif char != " ":
                ops.append(("text", x0 + CELL_W // 2, y0 + half, char, rgb(fg), y == 1))
    return ops


# The faces `font` tries, in order, as `(name, regular, bold, regular index,
# bold index)`: DejaVu Sans Mono where a Linux runner has it, Menlo on macOS,
# Consolas on Windows. The hand-drawn seal used Menlo, which is macOS-only,
# which is why this is a chain rather than a path.
FACES = (
    (
        "DejaVu Sans Mono",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        0,
        0,
    ),
    (
        "Menlo",
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Menlo.ttc",
        0,
        1,
    ),
    (
        "Consolas",
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\consolab.ttf",
        0,
        0,
    ),
)


def font(image_font):
    """`(regular, bold, name)`: the first face in `FACES` that loads at
    `FONT_SIZE`, its bold where one loads and its regular where not, else
    Pillow's own default at that size. `image_font` is `PIL.ImageFont`,
    handed in so this module imports Pillow in `png` alone. `name` is what
    the log prints, because a runner's font is a fact nobody wrote down
    (`questions.md` Q11)."""
    for name, regular, bold, at, bold_at in FACES:
        try:
            face = image_font.truetype(regular, FONT_SIZE, index=at)
        except OSError:
            continue
        try:
            heavy = image_font.truetype(bold, FONT_SIZE, index=bold_at)
        except OSError:
            heavy = face
        return face, heavy, name
    face = image_font.load_default(size=FONT_SIZE)
    return face, face, "Pillow's default"


def png(ops, dimensions, path):
    """Write `ops` as an RGBA PNG of `dimensions` at `path`, transparent
    where nothing is laid, and answer the name of the font it drew with."""
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGBA", dimensions, (0, 0, 0, 0))
    pen = ImageDraw.Draw(image)
    regular, bold, name = font(ImageFont)
    for op in ops:
        if op[0] == "rect":
            _, x0, y0, x1, y1, colour = op
            pen.rectangle([x0, y0, x1, y1], fill=colour)
        else:
            _, cx, cy, char, colour, heavy = op
            face = bold if heavy else regular
            pen.text((cx, cy), char, fill=colour, font=face, anchor="mm")
    image.save(path, format="PNG")
    return name


# --- the rows ------------------------------------------------------------
#
# A release's panel is a fixed set of rows, held here as one constant: the
# owner's 0.17.0 seal is the drawing, and a label the code composed from free
# text could grow past `seal_stamp.letter`'s eight-wide label column. That
# column is `{label:<8}`, not the longest label: `deferred` is exactly eight,
# which is the only reason the column looked set by it.
LABELS = ("SEALED", "tag", "PRs", "issues", "suite", "items", "capped", "deferred")
# The widest value the panel carries before the frame would cut it,
# `skills/verify/scripts/broad_gate.py#PANEL_VALUE_WIDTH`. Held here rather
# than imported, because that module is the whole gate; a case holds the two
# to one number.
PANEL_VALUE_WIDTH = 23
# What a row says when the source it is read from could not be read: the row
# stays, because a dropped row reads as none and a 0 reads as a count
# (`questions.md` Q8).
NOT_READ = "not read"
# The label the review chain puts on a pull request whose run ended at the
# round cap (`docs/review-chain-spec.md`).
CAPPED_LABEL = "chain: capped"


def plural(count, word):
    return f"{count} {word}{'' if count == 1 else 's'}"


def release_rows(version, sha, pulls_n, issues_n, suite, chain):
    """The panel's rows for a release, `(label, value)` with `""` for a
    continuation, in `LABELS`' order.

    `suite` is `(passed, skipped)`; `chain` is `chain_counts`' four, each a
    number or None for not read. A suite value wider than
    `PANEL_VALUE_WIDTH` moves `S skipped` to a continuation row under
    `P passed` (`questions.md` Q6): only the suite can overflow, a five-digit
    count and a three-digit skip being 25. The items row needs both its
    numbers and the capped row both of its own, so either missing says
    `not read`."""
    items, rounds, capped, deferred = chain
    passed, skipped = suite
    rows = [
        ("SEALED", f"v{version}"),
        ("tag", sha[:8]),
        ("", "main"),
        ("PRs", f"{pulls_n} merged"),
        ("issues", f"{issues_n} closed"),
    ]
    whole = f"{passed} passed, {skipped} skipped"
    if len(whole) <= PANEL_VALUE_WIDTH:
        rows.append(("suite", whole))
    else:
        rows += [("suite", f"{passed} passed"), ("", f"{skipped} skipped")]
    rows += [
        (
            "items",
            NOT_READ
            if items is None or rounds is None
            else f"{items} . {plural(rounds, 'round')}",
        ),
        (
            "capped",
            NOT_READ if capped is None or items is None else f"{capped} of {items}",
        ),
        ("deferred", NOT_READ if deferred is None else plural(deferred, "issue")),
    ]
    return rows


def alt_text(rows):
    """One sentence carrying every value of `rows`, in the shape of the alt
    text written by hand for 0.17.0's seal, for a reader whose browser does
    not draw the image. A `]` or a line break would end the Markdown image
    early, so neither is let through."""
    by = {}
    for label, value in rows:
        if label:
            by[label] = [value]
            last = label
        else:
            by[last].append(value)
    sealed, tag = by["SEALED"][0], by["tag"]
    first = f"The {sealed.removeprefix('v')} release seal: SEALED {sealed} at {tag[0]}"
    suite = [part.strip() for value in by["suite"] for part in value.split(",")]
    parts = [
        first + "".join(f" on {more}" for more in tag[1:]),
        plural(int(by["PRs"][0].split()[0]), "pull request") + " merged",
        plural(int(by["issues"][0].split()[0]), "issue") + " closed",
        "the suite at " + " and ".join(suite),
    ]
    items, capped, deferred = by["items"][0], by["capped"][0], by["deferred"][0]
    if items == NOT_READ:
        parts.append("work items not read")
    else:
        count, rounds = items.split(" . ")
        rounds = rounds.replace("round", "review round")
        parts.append(f"{plural(int(count), 'work item')} over {rounds}")
    if capped == NOT_READ:
        parts.append("capped not read")
    else:
        parts.append(f"{capped.split()[0]} of them capped")
    parts.append(
        "deferred not read" if deferred == NOT_READ else f"{deferred} deferred"
    )
    return re.sub(r"[\]\[\r\n]+", " ", ", ".join(parts))


# --- the sources ---------------------------------------------------------


def suite_counts(path):
    """`(passed, skipped)` from the JUnit XML pytest wrote at `path`.

    JUnit is pytest's documented output format, where a log is not: each
    `testsuite` element carries `tests`, `failures`, `errors` and `skipped`,
    and passed is the first less the other three, summed over every suite.
    Raises `OSError` for a file that is not there and `ValueError` for one
    that does not parse, holds no suite, carries a count that is not a
    number, or counts a failure or an error -- a `SEALED` above a red suite
    would be false, and a file nobody can read is never a zero."""
    try:
        root = ElementTree.parse(path).getroot()
    except ElementTree.ParseError as problem:
        raise ValueError(f"{path} is not JUnit XML: {problem}") from problem
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    if not suites:
        raise ValueError(f"{path} holds no testsuite")
    total = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for suite in suites:
        for key in total:
            try:
                total[key] += int(suite.get(key, ""))
            except ValueError as problem:
                raise ValueError(
                    f"{path}: a testsuite's {key} is {suite.get(key)!r}"
                ) from problem
    if total["failures"] or total["errors"]:
        raise ValueError(
            f"the suite at the tag did not pass: {total['failures']} failed and "
            f"{total['errors']} errors"
        )
    passed = total["tests"] - total["failures"] - total["errors"] - total["skipped"]
    return passed, total["skipped"]


def readers():
    """`(routing, chain_check, the markdown reader)`: the modules the review
    chain's own gates read round records with, so the counts here are the
    ones a gate would read and a change to where records live has to move
    these readers first."""
    return (
        module("specseal_routing", "hooks", "routing.py"),
        module(
            "specseal_chain_check", "skills", "code-review", "scripts", "chain_check.py"
        ),
        module(
            "specseal_unverified_reader",
            "skills",
            "verify",
            "scripts",
            "unverified_check.py",
        ),
    )


def labels_of(pull):
    return {
        (label.get("name") if isinstance(label, dict) else str(label)) or ""
        for label in pull.get("labels") or ()
    }


def chain_counts(root, pulls):
    """`(items, rounds, capped, deferred)` for the release's pull requests,
    each a number or None for not read, with the log saying why.

    `capped` counts the pull requests labelled `CAPPED_LABEL`. A pull request
    is a work item where exactly one `routing.md` under `root` names its head
    branch (`hooks/routing.py#item_dir`), and its rounds are
    `hooks/routing.py#rounds`. `deferred` is the number of distinct issues
    named in a Verdicts cell whose verdict is `deferred`, read with
    `chain_check.verdict_table` and `#verdict_of`; a home that is a file
    names no issue. A round record whose verdict table cannot be read leaves
    `deferred` None -- an incomplete count is a wrong number -- and a reader
    that will not load leaves all three tree counts None."""
    capped = sum(1 for pull in pulls if CAPPED_LABEL in labels_of(pull))
    try:
        routing, chain, reader = readers()
    except Exception as problem:
        print(
            f"the chain rows are not read: the round-record readers did not load ({problem})"
        )
        return None, None, capped, None
    items, rounds, deferred, unread = 0, 0, set(), []
    for pull in pulls:
        item = routing.item_dir(root, pull.get("headRefName") or "")
        if not item:
            continue
        items += 1
        if routing.rounds_unreadable(item):
            unread.append(os.path.join(item, routing.ROUNDS_DIR))
        records = routing.rounds(item)
        rounds += len(records)
        for path in records:
            try:
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
            except (OSError, UnicodeDecodeError):
                unread.append(path)
                continue
            rows, col, _header, _errors = chain.verdict_table(
                reader, reader.readable(text), path
            )
            if col < 0:
                unread.append(path)
                continue
            for _line, seen in rows:
                if chain.verdict_of(seen, col) == chain.DEFERRED:
                    deferred.update(int(n) for n in re.findall(r"#(\d+)", seen[col]))
    if unread:
        print(
            "the deferred row is not read: no verdict table could be read in "
            + ", ".join(os.path.relpath(p, root) for p in unread)
        )
        return items, rounds, capped, None
    return items, rounds, capped, len(deferred)
