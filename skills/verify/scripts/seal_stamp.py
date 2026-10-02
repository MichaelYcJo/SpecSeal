#!/usr/bin/env python3
"""seal-stamp — the drawing the broad gate prints when it was earned.

Issue #30 §*What it prints*. A wax disc with a fleur-de-lis, and a parchment
panel beside it carrying what the gate read: the tree and its branch, the
base and its ref, the work item, the suite's counts, the ledger, the chain,
the rounds (`broad_gate.panel` owns the list). The disc is COMPUTED —
`hypot` for the bands, `sin` for the rope's twist — and only the lily is
authored, as a 29x32 counted-stitch chart held below as data. Four hand-typed
discs came before this one and every one was lopsided; a circle that is
calculated cannot be off centre, and resizing it is one number.

Two forms, one drawing. The block form is half-block characters in truecolour,
emitted only where the colour changes (a code per cell was 282 KB for one
seal). The letter twin is the same footprint as letters — `o O` rope, `l m`
wax, `G W y Y` the lily's golds, `.` the field — for a console that cannot
render half-blocks, and for `seal-stamp` on a pipe. The twin is chosen when
stdout is not a UTF-8 terminal, or on `--shape`. An agent's report carries
neither: since #400 the gate draws nothing on a pipe.

The stamp prints on success only. The failure form, `not_sealed`, is the words
`NOT SEALED`, the branch and the tree, the base's ref and its commit
(`sealed_names`), and the failing checks with their first lines — no drawing,
because a picture that says *sealed* beside a word that says *not* is read
picture first.

**A sealed run is drawn where a person sees it, and that is rarely where it
ran** (#400). The gate draws only on a terminal, and only over a written
cell. A recorded seal on a pipe — which is every sealer's run — writes the
panel's rows to a values file under the git common dir instead, keyed by the
Claude Code session, and
`hooks/sealer-stamp.py` draws each undrawn file once, at the end of that
session's turn. This module owns the file: `write_values`, `read_values`,
`pending` and `claim`. Drawing claims the file first, by renaming it to
`.drawn.json`, so a file is drawn once whoever draws it.

Usage:
  seal-stamp                      the stamp over sample rows, for a person
  seal-stamp --shape              the letter twin
  seal-stamp --scale 0.75         the chart shrunk; 0.75 is the floor
  seal-stamp --from <file>        a sealed run's values file, drawn once

The gate imports `stamp(rows, scale, shape)`, `not_sealed(tree, base,
failures, branch, ref)`, `sealed_names`, `pick_shape(stream)`,
`is_terminal(stream)` and `write_values`;
the hook imports `pending`, `read_values`, `claim` and `stamp`. The command
exists so a person can see the drawing without running a gate, and so a
values file no hook drew can still be drawn by hand.

Exit codes: 0 printed · 2 refused — a scale under the floor, an interpreter
under the floor, or a values file that is unreadable or drawn already;
nothing was written on 2.
"""

import argparse
import json
import math
import os
import re
import sys
import time

# --- the interpreter floor -----------------------------------------------
#
# Copied from `skills/code-review/scripts/round_record.py`, whose comment says
# this block is the spelling to copy. It sits after the imports, uses no syntax
# newer than the interpreter it means to catch, and precedes every other act
# at module level — the chart below is parsed by a call.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)
BELOW_FLOOR = (
    "seal-stamp: needs python {floor} or newer, and this is python {found} "
    "at {executable}.\n"
    "Nothing was read and nothing was written.\n"
    "`python3` is not always the newest interpreter installed -- macOS ships "
    "python 3.9 under that name -- so name one explicitly, `python{floor} "
    "<this script> ...`, or see CONTRIBUTING.md section 'Running the checks'."
)


def below_floor(version=None, executable=None):
    """The sentence for an interpreter under the floor, or None above it."""
    version = tuple(sys.version_info[:3]) if version is None else tuple(version)
    if version[:2] >= FLOOR:
        return None
    return BELOW_FLOOR.format(
        floor=FLOOR_TEXT,
        found=".".join(str(part) for part in version),
        executable=sys.executable if executable is None else executable,
    )


_refusal = below_floor()
if _refusal:
    sys.stderr.write(_refusal + "\n")
    raise SystemExit(2)


# --- the chart -----------------------------------------------------------
#
# 29 columns by 32 rows. `D` the lily's gold, `R` its highlight, `y` the
# band's shadow, `Y` the band's light, `.` the field. Traced outside the tree
# by hand against a counted-stitch pattern; this is the only copy.
ART = """
..............D..............
.............DDD.............
.............DRD.............
............DDDRD............
...........DDDDRRD...........
...........DDDDRRD...........
..........DDDDDRRDD..........
.........DDDDDDDRRDD.........
.........DDDDDDDRRDD.........
.........DDDDDDDRRDD.........
.........DDDDDDDRRDD.........
..........DDDDDRRDD..........
..DDDDD....DDDDRRD....DDDDD..
.DDDDDDDDD.DDDDRRD.DDDDDRRDD.
DDDDDDDDDDD.DDDRD.DDDDDDDDRRD
DDDDD...DDD.DDRDD.DDD...DDDRD
DDDD.....DDD.DDD.DDD.....DDRD
DDDD......DD.DDD.DD......DRDD
.DDDD..D...D.DDD.D...D..DDDD.
..DDDDD....yyyyYYY....DDDDD..
..........yyyyyyyyy..........
........D.yDyDDDyDy.D........
.......DD..DyDDDyD..DD.......
......DDD.DD.DDD.DD.DDD......
......DDDDDD.DDD.DDDDDD......
.......DDD..DDDDD..DDD.......
...........DDDDRDD...........
...........DDDDRRD...........
...........DDDDRDD...........
............DDRDD............
.............DDD.............
..............D..............
""".strip("\n").splitlines()

GOLD = {
    "D": (0xC8, 0x96, 0x1E),
    "R": (0xF7, 0xDC, 0x8A),
    "y": (0x8C, 0x63, 0x12),
    "Y": (0xE8, 0xB7, 0x3C),
}
ROPE_L, ROPE_D = (232, 226, 196), (168, 158, 122)
WAX_L, WAX_M, FIELD = (206, 46, 48), (168, 26, 30), (78, 12, 16)

# The letter for each colour. `None` is outside the disc.
KEY = {
    ROPE_L: "o",
    ROPE_D: "O",
    WAX_L: "l",
    WAX_M: "m",
    FIELD: ".",
    GOLD["D"]: "G",
    GOLD["R"]: "W",
    GOLD["y"]: "y",
    GOLD["Y"]: "Y",
    None: " ",
}

# #30 §*Size*: the chart compresses to 75 % with the lily still legible; at
# 60 % the band closes up and the foot becomes a blob, and at 50 % it reads as
# a cross. Above 1.0 nothing enlarges — the chart is one cell per stitch.
SCALE_FLOOR = 0.75
SCALE_CEILING = 1.0
# The scale both commands draw at unless told otherwise (#400 §*The size, and
# why it is 0.90*). Six scales were rendered in colour and looked at by the
# owner before the choice: at 0.90 the disc is 20 lines against the panel's
# 16, the darkest gold that crowds the lily's foot at 0.95 has cleared, the
# rope settles to two rows, and the highlight still runs the centre leaf.
# The trade was the lily's legibility against the two blocks lining up, and
# legibility won.
#
# 0.75 was the other candidate, passed over rather than missed: it is the only
# legal scale where the disc (17 lines) and the panel end within one line of
# each other, and it is the least detail of the band. Disc height moves in
# whole cells, so a scale is not a continuous dial.
DEFAULT_SCALE = 0.90

# --- what one hook message may hold (#717) ---------------------------------
#
# The harness writes a `Stop` hook's `systemMessage` longer than this many
# characters to a file and shows the person a 2 KB preview of it, so a stamp
# past it is not seen. Counted as Python `str` length, not as bytes. Measured
# 2026-10-02 on Claude Code 2.1.287, with a `Stop` hook in a scratch project
# and one headless `claude -p` turn per size: 9,990 and 10,000 characters, and
# 9,990 `▀` (29,942 bytes), were shown with nothing written to the session's
# `tool-results/`; 10,001, 10,010 and 12,000 each left a
# `hook-<uuid>-<n>-systemMessage.txt` there. This project's own sessions had
# bracketed it before the probe: 9,919 shown, 10,090 persisted. The harness
# can move it, and the only sign is a preview on the owner's screen; the same
# hook at two sizes either side of this number is the whole probe again.
MESSAGE_LIMIT = 10000
# What the hook holds its WHOLE message under — every block, every label and
# the blank line between two blocks. The reserve is for what the hook cannot
# see: `hooks/dispatch.py#report` prepends the session's gate-failure report
# to this same message after the hook has printed. The longest report it can
# write, with each exception's text cut at its `MESSAGE_CAP`, is 533
# characters for one failed gate and 909 for two, separator included
# (measured 2026-10-02 over `dispatch.describe`); a third would pass the
# limit beside a stamp at the budget.
MESSAGE_RESERVE = 1000
MESSAGE_BUDGET = MESSAGE_LIMIT - MESSAGE_RESERVE
# The rungs a message over the budget steps down, after the file's own scale;
# past the last, every block is drawn with no disc (`fitted`). Each rung is
# inside `check_scale`'s band, so a step down cannot be refused.
SCALE_LADDER = (0.90, 0.80, 0.75)

SCALE_REFUSED = (
    "seal-stamp: scale {scale} is under the floor of {floor}; below it the "
    "lily is not legible (#30 measured 0.6 closing the band and 0.5 reading as "
    "a cross). Nothing was drawn."
)
# NaN is not under the floor and not above the ceiling; it is not on the line
# at all, and telling a reader it is "under the floor of 0.75" sends them to
# raise a number that will fail the same way.
SCALE_NOT_A_NUMBER = (
    "seal-stamp: scale {scale} is not a number, so it is neither inside the "
    "band {floor}-{ceiling} nor outside it. Nothing was drawn."
)
SCALE_TOO_LARGE = (
    "seal-stamp: scale {scale} is above {ceiling}; the chart is one cell per "
    "stitch and does not enlarge. Nothing was drawn."
)


def check_scale(scale):
    """The refusal for a scale outside the band, or None inside it."""
    # `not (floor <= scale <= ceiling)` rather than two `<`/`>` tests: NaN
    # compares False with everything, so the pair let it through and it
    # failed later inside `stamp` with `cannot convert float NaN to integer`
    # — after every check had run and the cell had been written, and
    # `broad_gate.main` catches `Refused` alone.
    if not (SCALE_FLOOR <= scale <= SCALE_CEILING):
        if scale != scale:  # NaN, and no comparison against it is true
            return SCALE_NOT_A_NUMBER.format(
                scale=scale, floor=SCALE_FLOOR, ceiling=SCALE_CEILING
            )
        if scale < SCALE_FLOOR:
            return SCALE_REFUSED.format(scale=scale, floor=SCALE_FLOOR)
        return SCALE_TOO_LARGE.format(scale=scale, ceiling=SCALE_CEILING)
    return None


def shrink(art, f):
    """The chart at a fraction of its size: each output cell takes the
    majority colour of the stitches it covers, and stays blank only when all
    of them are blank."""
    if f >= 1.0:
        return art
    h, w = len(art), len(art[0])
    nh, nw = max(1, round(h * f)), max(1, round(w * f))
    out = []
    for y in range(nh):
        row = []
        for x in range(nw):
            x0, x1 = int(x * w / nw), max(int(x * w / nw) + 1, int((x + 1) * w / nw))
            y0, y1 = int(y * h / nh), max(int(y * h / nh) + 1, int((y + 1) * h / nh))
            ink = [
                art[b][a]
                for b in range(y0, y1)
                for a in range(x0, x1)
                if b < h and a < w and art[b][a] != "."
            ]
            # `max(set(ink), …)` iterated a set of strings, whose order moves
            # with PYTHONHASHSEED, so a tie between two chart colours drew
            # differently from one process to the next (round 1's 🟡 6). This
            # module's argument is that a circle that is CALCULATED cannot be
            # off centre, and a calculated circle that is not reproducible
            # gives it back at every scale but 1.0. Highest count, then
            # earliest in the chart — both stable.
            row.append(
                max(dict.fromkeys(ink), key=lambda c: (ink.count(c), -ink.index(c)))
                if ink
                else "."
            )
        out.append("".join(row))
    return out


def build(scale=1.0, margin=0.74):
    """`(w, h, px)` — the disc's width and height in cells, and a function
    from a cell to its colour, `None` outside the disc.

    The radius is the chart's reach from its centre over `margin`, so the lily
    fills the field and the bands are drawn around it: rope from 0.90, wax in
    two reds from 0.78, the field and the chart inside. The rope's twist is a
    sine over the angle, so it alternates light and dark around the ring.
    `h` is even, because the block form prints two cells per line."""
    refusal = check_scale(scale)
    if refusal:
        raise ValueError(refusal)
    art = shrink(ART, scale)
    fh, fw = len(art), len(art[0])
    cx, cy = (fw - 1) / 2, (fh - 1) / 2
    reach = max(
        math.hypot(x - cx, y - cy)
        for y in range(fh)
        for x in range(fw)
        if art[y][x] != "."
    )
    r0 = reach / margin
    w = int(r0 * 2) + 2
    h = w + (w % 2)
    ox, oy = w / 2, h / 2

    def px(x, y):
        # Sampled at the cell's centre. Sampled at its corner, the disc sat
        # half a cell right and half a cell down of the grid's centre — the
        # top rope row came out six cells wider than the bottom one — which is
        # the lopsidedness a computed circle is supposed to make impossible.
        dx, dy = x + 0.5 - ox, y + 0.5 - oy
        r = math.hypot(dx, dy) / r0
        if r > 1.00:
            return None
        if r > 0.90:
            twist = math.sin(math.atan2(dy, dx) * 30 + r * 8)
            return ROPE_L if twist > 0 else ROPE_D
        if r > 0.84:
            return WAX_L
        if r > 0.78:
            return WAX_M
        # `floor`, not `int`: `int` truncates toward zero, so the cell just
        # outside the chart's top-left would read stitch 0 a second time.
        fx, fy = math.floor(dx + fw / 2), math.floor(dy + fh / 2)
        if 0 <= fy < fh and 0 <= fx < fw and art[fy][fx] in GOLD:
            return GOLD[art[fy][fx]]
        return FIELD

    return w, h, px


# --- the two row writers -------------------------------------------------
#
# Both walk the same cells — row `y` on top, `y + 1` below — so the two forms
# have one footprint: a cell is blank in the twin exactly where the block form
# prints a space.


def sgr(ground, rgb):
    """A truecolour sequence: `ground` 38 for the foreground, 48 for the
    background."""
    r, g, b = rgb
    return f"\x1b[{ground};2;{r};{g};{b}m"


def colour_row(px, w, y):
    """One line of the block form, emitting a colour only where it changes.

    A cell whose top half is outside the disc is a lower half-block in the
    bottom colour; one whose bottom half is outside is an upper half-block;
    one inside on both halves is an upper half-block with the bottom colour
    as its background. The line ends with a reset, so nothing bleeds into the
    panel beside it."""
    out, fg, bg = [], None, None
    for x in range(w):
        top, bot = px(x, y), px(x, y + 1)
        if top is None and bot is None:
            if fg or bg:
                out.append("\x1b[0m")
                fg = bg = None
            out.append(" ")
            continue
        if top is None:
            want_fg, want_bg, ch = bot, None, "▄"
        elif bot is None:
            want_fg, want_bg, ch = top, None, "▀"
        else:
            want_fg, want_bg, ch = top, bot, "▀"
        if want_fg != fg:
            out.append(sgr(38, want_fg))
            fg = want_fg
        if want_bg != bg:
            out.append("\x1b[49m" if want_bg is None else sgr(48, want_bg))
            bg = want_bg
        out.append(ch)
    return "".join(out) + "\x1b[0m"


def letter_row(px, w, y):
    """One line of the letter twin over the same two cell rows: the top cell's
    letter, or the bottom cell's where only the bottom is inside the disc."""
    out = []
    for x in range(w):
        top, bot = px(x, y), px(x, y + 1)
        out.append(KEY[top if top is not None else bot])
    return "".join(out)


# --- the panel -----------------------------------------------------------

PANEL_WIDTH = 36


def letter(rows, width=PANEL_WIDTH):
    """A parchment panel carrying the stamp's numbers, set beside the disc.

    `rows` is a list of `(label, value)` pairs with `None` for a blank line,
    so what the stamp reports is data the gate fills rather than a string it
    formats. A pair whose label is `""` is a continuation: its value lands in
    the value column under the row above it. A value longer than the panel is
    cut at the frame, which is why `broad_gate.fit` elides before it does."""
    inner = width - 2
    out = ["." + "-" * inner + ".", "|" + " " * inner + "|"]
    for row in rows:
        if row is None:
            out.append("|" + " " * inner + "|")
            continue
        label, value = row
        out.append("|" + f"  {label:<8} {value}".ljust(inner)[:inner] + "|")
    out.append("|" + " " * inner + "|")
    out.append("'" + "-" * inner + "'")
    return out


def strip_ansi(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def beside(left, right, gap=3, pad_left=2):
    """Two blocks side by side, the shorter one centred against the taller.
    Widths are measured with colour codes removed."""
    lw = max(len(strip_ansi(line)) for line in left) if left else 0
    top = max(0, (len(left) - len(right)) // 2)
    rows = max(len(left), len(right) + top)
    out = []
    for i in range(rows):
        line = left[i] if i < len(left) else ""
        pad = lw - len(strip_ansi(line))
        r = right[i - top] if 0 <= i - top < len(right) else ""
        out.append(" " * pad_left + line + " " * (pad + gap) + r)
    return out


# --- what the gate calls -------------------------------------------------


def stamp(rows, scale=1.0, shape=False):
    """The lines of the stamp: the disc at `scale`, the panel of `rows`
    beside it. `shape` picks the letter twin. Raises `ValueError` with the
    refusal sentence for a scale outside the band. `scale` None is the
    panel with no disc, the last rung `fitted` steps down to (#717)."""
    if scale is None:
        return letter(rows)
    w, h, px = build(scale)
    writer = letter_row if shape else colour_row
    disc = [writer(px, w, y) for y in range(0, h, 2)]
    return beside(disc, letter(rows))


def fitted(blocks, budget=MESSAGE_BUDGET):
    """The message the `Stop` hook prints for `blocks`, held under `budget`
    (#717). `blocks` is `(label, rows, scale)` per values file, oldest first;
    each is its label and then its block form, and two are joined by a blank
    line.

    One rung for the whole message, the highest at which every block fits
    together: the files' own scales first, then each of `SCALE_LADDER` —
    never above a file's own scale — and last every block with no disc.
    Two stamps in one message are two stamps at one scale. The last rung is
    returned whatever its size, because nothing comes after it: a panel
    with no disc is about 40 characters a row, and its width is bounded by
    `broad_gate.PANEL_VALUE_WIDTH`, so only a record deferring to far more
    homes than any work item has had could pass the budget there.
    `budget` is a parameter so a case can drive every rung."""

    def message(rung):
        return "\n\n".join(
            "\n".join(
                [
                    label,
                    *stamp(
                        rows,
                        None if rung is None else min(scale, rung),
                        shape=False,
                    ),
                ]
            )
            for label, rows, scale in blocks
        )

    for rung in (SCALE_CEILING, *SCALE_LADDER):
        drawn = message(rung)
        if len(drawn) <= budget:
            return drawn
    return message(None)


# A ref spelled as a commit: what `--base <sha>` resolves to (`sealed_names`).
HEX_REF = re.compile(r"[0-9a-fA-F]{4,40}")


def sealed_names(tree, base, branch=None, ref=None):
    """`<branch> @ <tree> against <ref> @ <base>` — what a `SEALED` line, a
    `NOT SEALED` line and a drawn stamp's label say was sealed (#666).

    A head naming two commits named neither the branch nor the base's ref,
    so a reader matched a stamp to its work by hash alone. One composer for
    the three lines, because two spellings of one sentence drift.

    Two collapses, and each leaves a part out rather than printing it twice:

      - `branch` None — a detached HEAD has no branch, so the tree prints
        alone, with no stray `@`
      - `ref` None, or a ref that is the commit itself — a bare SHA given as
        `--base` resolves to itself, and `1e2bed9 @ 1e2bed9` says one thing
        twice. Read as a ref spelled in hex with either hash a prefix of the
        other, because the caller may have typed forty characters where the
        gate prints eight, and a branch named `b` is not the commit `b1e2…`

    `ref` is the RESOLVED ref (`broad_gate.Base.ref`), the one CI reads, not
    the spelling the caller typed: #423's repair was that a reader can tell
    `origin/<base>` from a local ref a week behind it."""
    named = f"{branch} @ {tree}" if branch else f"{tree}"
    against = f"{base}" if ref_is_commit(ref, base) else f"{ref} @ {base}"
    return f"{named} against {against}"


def ref_is_commit(ref, base):
    """True where `ref` names nothing the commit `base` does not: no ref at
    all, or a ref spelled in hex that `base` begins, or that begins with
    `base`. The one reading of *the ref is the commit*, asked by
    `sealed_names` for the lines and by `broad_gate.panel` for the row under
    `base`, so the two cannot disagree about when a ref is worth printing."""
    base, ref = str(base), ("" if ref is None else str(ref))
    if not ref:
        return True
    return bool(HEX_REF.fullmatch(ref)) and (
        base.startswith(ref) or ref.startswith(base)
    )


def not_sealed(tree, base, failures, branch=None, ref=None):
    """The failure form, as lines: `NOT SEALED <branch> @ <tree> against
    <ref> @ <base>` (`sealed_names`), then each failing check's name with its
    first lines under it. No drawing.

    `failures` is a list of `(name, lines)` — the check that failed and the
    first lines of what it printed, as the gate kept them. `branch` and `ref`
    None leave their half out, which is the line a caller that names neither
    has always got."""
    out = [f"NOT SEALED   {sealed_names(tree, base, branch, ref)}", ""]
    # The widest name present, not a literal 8: `survivors` is nine
    # characters, so that one check's first line sat a column out from every
    # other check's.
    pad = max([len(name) for name, _ in failures] + [8])
    for name, lines in failures:
        lines = list(lines) or ["(no output)"]
        out.append(f"  {name:<{pad}} {lines[0]}")
        out.extend(f"  {'':<{pad}} {line}" for line in lines[1:])
    return out


def pick_shape(stream):
    """True when `stream` gets the letter twin: anything that is not a UTF-8
    terminal. A console on another codepage draws UTF-8 half-blocks as
    mojibake, and a pipe has no terminal to draw colour on, so `seal-stamp`
    on one prints the twin; the gate asks `is_terminal` first and draws
    nothing on a pipe at all (#400). Asked BEFORE the stream is reconfigured to UTF-8 — after
    that call every stream answers `utf-8`, and a cp949 console would get the
    blocks it cannot draw."""
    encoding = (getattr(stream, "encoding", None) or "").lower().replace("-", "")
    if encoding != "utf8":
        return True
    return not is_terminal(stream)


def is_terminal(stream):
    """True when `stream` is a terminal, whatever its encoding.

    The other half of what `pick_shape` used to fold into one answer, split
    out because the gate asks two different questions (#400): whether to
    draw at all — only a terminal has a person in front of it — and, where
    it draws, which form. A cp949 terminal is a terminal that gets letters,
    and a UTF-8 pipe is not a terminal. Asked with `pick_shape`, before the
    streams are reconfigured, so both answers describe the stream as the
    process found it."""
    isatty = getattr(stream, "isatty", None)
    try:
        return bool(isatty and isatty())
    except (ValueError, OSError):
        return False


# --- a sealed run's values, drawn by somebody else -----------------------
#
# The gate's stdout on a sealer's run is a pipe into a report nobody sees
# unfolded (#400), so it writes the run's panel here and a `Stop` hook in the
# session that spawned the sealer draws it. The directory is under the git
# COMMON dir because the sealer's root and that session's cwd are different
# worktrees of one clone, and the common dir is the one place both resolve
# alike. It is keyed by session so that a concurrent session of the same
# clone does not draw, and take, a stamp that is not its own.

VALUES_DIR = "specseal-stamp"
# The key of a run no Claude Code session was found for. No hook reads it;
# `seal-stamp --from` is how such a file is drawn.
NO_SESSION = "none"
PENDING = ".json"
DRAWN = ".drawn.json"

VALUES_UNREADABLE = "seal-stamp: {path} cannot be read ({why}). Nothing was drawn."
VALUES_MALFORMED = (
    "seal-stamp: {path} is not a values file the broad gate wrote: {why}. "
    "Nothing was drawn."
)
VALUES_DRAWN = (
    "seal-stamp: {path} was drawn already, and a sealed run's values are drawn "
    "once. Nothing was drawn; the values stay in {drawn}."
)


def session_key(session):
    """The directory name for `session`: the id's last path part, or
    `NO_SESSION` where there is none. The id names a directory, so a
    separator in a malformed one must not become a path escape."""
    name = os.path.basename(str(session or "").strip())
    return name if name and name not in (".", "..") else NO_SESSION


def values_dir(common, session):
    """Where the runs of `session` wait to be drawn."""
    return os.path.join(common, VALUES_DIR, session_key(session))


def drawn_path(path):
    """The name `path` takes once it has been claimed."""
    stem = path[: -len(PENDING)] if path.endswith(PENDING) else path
    return stem + DRAWN


def write_values(common, session, values, now=None):
    """Write one run's `values` for `session`; returns the file's path.

    Written to a hidden temporary name and renamed into place, so a hook
    listing the directory never reads half a file. The name leads with the
    time in nanoseconds, so a name sort is oldest first. Raises `OSError`
    where the directory cannot be made or the file cannot be written."""
    directory = values_dir(common, session)
    os.makedirs(directory, exist_ok=True)
    moment = time.time_ns() if now is None else now
    name = f"{moment}-{os.path.basename(str(values.get('tree') or 'tree'))}"
    path = os.path.join(directory, name + PENDING)
    temporary = os.path.join(directory, f".{name}.tmp")
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(values, handle)
    os.replace(temporary, path)
    return path


def read_values(path):
    """A values file as the gate wrote it, with each row a `(label, value)`
    pair or None. Raises `ValueError` with the refusal sentence for a file
    that cannot be read or is not in that shape — which covers a scale the
    band refuses too, because `stamp` checks it again when it draws."""
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except OSError as exc:
        raise ValueError(
            VALUES_UNREADABLE.format(path=path, why=exc.strerror or exc)
        ) from exc
    except ValueError as exc:
        raise ValueError(
            VALUES_MALFORMED.format(path=path, why="it is not JSON")
        ) from exc
    if not isinstance(data, dict):
        raise ValueError(VALUES_MALFORMED.format(path=path, why="it is not an object"))
    rows = data.get("rows")
    shaped = isinstance(rows, list) and all(
        row is None
        or (
            isinstance(row, list)
            and len(row) == 2
            and all(isinstance(cell, str) for cell in row)
        )
        for row in rows
    )
    if not shaped:
        raise ValueError(
            VALUES_MALFORMED.format(
                path=path, why="`rows` is not a list of label and value pairs"
            )
        )
    scale = data.get("scale")
    if isinstance(scale, bool) or not isinstance(scale, (int, float)):
        raise ValueError(
            VALUES_MALFORMED.format(path=path, why="`scale` is not a number")
        )
    return {**data, "rows": [None if row is None else tuple(row) for row in rows]}


def pending(directory):
    """The undrawn values files in `directory`, oldest first; empty where
    the directory does not exist."""
    try:
        names = os.listdir(directory)
    except OSError:
        return []
    return sorted(
        os.path.join(directory, name)
        for name in names
        if name.endswith(PENDING)
        and not name.endswith(DRAWN)
        and not name.startswith(".")
    )


def claim(path):
    """Mark `path` drawn by renaming it; the new path, or None where it was
    not there to rename — somebody else claimed it first.

    Called BEFORE anything is printed. Two drawers racing for one file both
    reach `os.replace` and only one finds it, so the file is drawn at most
    once; a crash between the rename and the print loses that one drawing
    rather than repeating it."""
    target = drawn_path(path)
    try:
        os.replace(path, target)
    except OSError:
        return None
    return target


def label(values):
    """The line said above a drawn stamp: what was sealed, and for which
    work item. The harness shows a hook message's first line as a dim label,
    so this is the line that must not be blank.

    A file carrying `branch` — written by a gate that has #666, `null` on a
    detached HEAD — gets the `SEALED` line's own names (`sealed_names`) and
    then ` · #<pr>` where the record named a pull request (#666). **A file
    without the key draws the label it always drew**, `SEALED <tree> against
    <base> · <item>`: the file is written by the gate the TREE ships and read
    by the hook the INSTALLED plugin ships, so a file from an older gate may
    still be pending when a newer hook draws it."""
    item = values.get("item")
    where = f" · {os.path.basename(os.path.normpath(item))}" if item else ""
    if "branch" not in values:
        return f"SEALED {values.get('tree')} against {values.get('base')}{where}"
    pr = values.get("pr")
    names = sealed_names(
        values.get("tree"), values.get("base"), values.get("branch"), values.get("from")
    )
    return f"SEALED {names}{f' · {pr}' if pr else ''}{where}"


# --- a person's command --------------------------------------------------

# Neutral values in the panel's shape, so `seal-stamp` shows a person what the
# gate will print without a gate having run — every row `broad_gate.panel`
# can return, the conditional ones included, in its order. It read `lint
# clean` from #400 to #666, which the real panel's own comment refuses as a
# counterfeit, because nothing held the two lists together; a case in
# `tests/test_the_seal_is_taken_once_by_the_sealer.py` holds the labels
# against `panel`'s now.
SAMPLE_ROWS = [
    ("SEALED", ""),
    None,
    ("tree", "c46fd2d"),
    ("", "feat/12-a-branch"),
    ("base", "1e2bed9"),
    ("", "origin/release/next"),
    ("item", "#34 . 1799000000"),
    ("gate", "tree 1.2.3"),
    None,
    ("suite", "768 passed, 1 skipped"),
    ("", "exit 0"),
    ("ledger", "187 ok"),
    ("", "0 drifted . 0 broken"),
    ("chain", "exit 0"),
    None,
    ("workflow", "4 of 9 not answered"),
    None,
    ("rounds", "3 . capped"),
    ("", "2 deferred -> #56"),
]


def main(argv=None, console_wants_letters=None):
    """`console_wants_letters` is `pick_shape` asked of stdout as the process
    found it. `__main__` asks before it reconfigures the streams, because
    `reconfigure` changes the one object `sys.stdout` and `sys.__stdout__`
    both name; a direct call may leave it to be asked here."""
    parser = argparse.ArgumentParser(
        prog="seal-stamp",
        description="Print the sealer's seal — the disc the broad gate stamps.",
    )
    parser.add_argument(
        "--shape", action="store_true", help="the letter twin, whatever the console"
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=None,
        help=f"the chart's scale; {SCALE_FLOOR} is the floor, {SCALE_CEILING} the "
        f"size, {DEFAULT_SCALE} the default, and a values file's own scale with "
        "--from",
    )
    parser.add_argument(
        "--from",
        dest="values",
        default=None,
        metavar="FILE",
        help="draw a sealed run's values file, once, instead of the sample",
    )
    args = parser.parse_args(argv)
    if console_wants_letters is None:
        console_wants_letters = pick_shape(sys.stdout)
    shape = args.shape or console_wants_letters
    try:
        if args.values is None:
            scale = DEFAULT_SCALE if args.scale is None else args.scale
            lines = stamp(SAMPLE_ROWS, scale=scale, shape=shape)
        else:
            lines = drawn_from(args.values, args.scale, shape)
    except ValueError as refused:
        sys.stderr.write(str(refused) + "\n")
        return 2
    sys.stdout.write("\n" + "\n".join(lines) + "\n\n")
    return 0


def drawn_from(path, scale, shape):
    """The lines for the values file at `path`, which is claimed before they
    are returned. `scale` None takes the file's own. Raises `ValueError`
    with a refusal for a file drawn already, unreadable, or out of shape —
    and every refusal comes before the claim, so a file refused for its
    content is still there to be drawn once it is repaired."""
    if path.endswith(DRAWN) or (
        not os.path.exists(path) and os.path.exists(drawn_path(path))
    ):
        # The drawn file's own name, where that is what was given:
        # `drawn_path` of it is `X.drawn.drawn.json`, which does not exist,
        # and this is the sentence a person recovers the values from (round
        # 1's 🟡 3).
        drawn = path if path.endswith(DRAWN) else drawn_path(path)
        raise ValueError(VALUES_DRAWN.format(path=path, drawn=drawn))
    values = read_values(path)
    lines = stamp(values["rows"], values["scale"] if scale is None else scale, shape)
    if claim(path) is None:
        raise ValueError(VALUES_DRAWN.format(path=path, drawn=drawn_path(path)))
    return lines


if __name__ == "__main__":
    # Which form, asked of stdout as the process found it. It has to come
    # before the loop below: `reconfigure` puts the stream into UTF-8, and a
    # cp949 console asked afterwards would be handed the blocks it cannot draw.
    _letters = pick_shape(sys.stdout)
    # A console that cannot encode what this prints kills it with stdout
    # empty. `hooks/console.py` owns the reasoning and the three decisions
    # behind these lines.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main(console_wants_letters=_letters))
