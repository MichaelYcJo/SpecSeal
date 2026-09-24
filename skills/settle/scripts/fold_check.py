#!/usr/bin/env python3
"""fold-check — hold a fold's two rules over the top level of `docs/`.

`skills/settle/SKILL.md` §2 gives a folded statement one shape and a document
a ceiling. Both checks lived in this plugin's own test suite, so a repository
that folds with `settle` had the rules and nothing that reads them (#566). This
is that reader, shipped.

  fold-check                     both checks, with the values seal/config.md states
  fold-check --shape-from ID     bind the shape from this work-item id on, this run
  fold-check --ceiling N         hold every document to N lines, this run
  fold-check --root DIR          a repository other than this one

**The shape.** Every statement whose marker group holds a work-item id at or
above the cutoff opens with a bold rule sentence and carries exactly one live
`Enforced by:` line, whose targets each resolve: a file inside the repository
and, with `::name`, a `def` or `class` in it. Or the line says
`nothing — <why>`, with a reason. Ids are epoch-prefixed, so the cutoff is a
comparison and needs no list of exemptions, and `--shape-from 0` binds every
statement there is.

**The ceiling.** Every top-level `docs/*.md` is at or under the ceiling, or is
listed over it with its fold markers frozen — how many, and which — until the
home it names splits it. The marker count is frozen and not the line count,
because a marker is the one thing only a fold adds.

**What it cannot read.** Presence, count and resolution are all it checks. It
cannot tell whether a target really enforces the rule, whether a statement is
true, or whether two statements contradict each other; those stay review's.

**It sets no value.** The plugin ships the reader and the repository states
the values, as three rows of `seal/config.md` read through
`hooks/config.py#config_rows`: `Fold shape from` (the cutoff),
`Document line ceiling`, and `Over the ceiling` (`none`, or `;`-separated
entries `<path> frozen at <n> markers <12-hex digest> until <home>`). An
absent row means *not declared*, as every optional row of that file does: the
check it governs is not run, and the output says so in one line rather than
refusing, because a repository that never folds has not asked for either. A
flag overrides its row for one run, which is how a retrofit lists every
statement still missing the shape without editing the config first.

Markers and live lines come from the fold's own reader,
`skills/verify/scripts/unverified_check.py#live_lines` and `#FOLD_MARKER`,
loaded rather than re-spelled: a marker this counted and the fold did not, or
the reverse, would be two answers about one document.

Exit codes: 0 nothing found, including the run where nothing is declared ·
1 at least one problem, each on a line of its own · 2 the root or a value was
unusable and nothing was checked, or the interpreter is below the floor.
"""

import argparse
import ast
import hashlib
import importlib.util
import os
import re
import sys

# **The interpreter floor, copied from
# `skills/code-review/scripts/round_record.py#below_floor`**, which is written
# to be copied and says so, by way of `skills/settle/scripts/settle.py`. Two
# things about its shape are load-bearing, and they are the reason it is
# copied rather than imported. It sits after the imports and not after
# `import sys`, because ruff's E402 is selected and every shipped script is
# measured to compile under 3.9, so no import above it can fail first. And it
# uses no syntax newer than the oldest interpreter it means to catch — no
# walrus, no f-string — since a guard that cannot parse is the traceback it
# exists to replace.
#
# `tests/test_a_script_says_which_interpreter_it_needs.py` pins this number
# to the runner's and to `ruff.toml`'s.
FLOOR = (3, 12)
FLOOR_TEXT = ".".join(str(part) for part in FLOOR)
BELOW_FLOOR = (
    "fold-check: needs python {floor} or newer, and this is python {found} "
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

HERE = os.path.dirname(os.path.abspath(__file__))
READER = os.path.join(HERE, "..", "..", "verify", "scripts", "unverified_check.py")
CONFIG_READER = os.path.join(HERE, "..", "..", "..", "hooks", "config.py")
OPTIN = os.path.join(HERE, "..", "..", "..", "hooks", "optin.py")

DOCS = "docs"
CONFIG = "config.md"

# The three `seal/config.md` rows this reads. Each is optional, and an absent
# one means *not declared*, which is what every optional row in
# `templates/config.md` means: the check it governs is not run, and the
# output says so in one line.
SHAPE_ROW = "Fold shape from"
CEILING_ROW = "Document line ceiling"
OVER_ROW = "Over the ceiling"
NONE_LISTED = "none"

# One `Over the ceiling` entry, as a person writes it. The digest is printed
# by this command when the count or the ids disagree, so nobody computes it
# by hand.
OVER_ENTRY = re.compile(
    r"^(?P<path>\S+) frozen at (?P<count>[0-9]+) markers (?P<digest>[0-9a-f]{12}) "
    r"until (?P<home>\S+)$"
)
WHOLE = re.compile(r"[0-9]+")
OVER_SHAPE = "<path> frozen at <n> markers <12-hex digest> until <home>"

HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
BOLD_OPENING = re.compile(r"^\*{2,3}[^*\s]")
ENFORCED = "Enforced by: "
NOTHING = "nothing — "


def load(path, name):
    """Import a sibling script by path, or refuse with a sentence."""
    if not os.path.isfile(path):
        raise SystemExit(
            f"fold-check: cannot read {path}, and it is where the fold's "
            "markers are read from. This command ships beside it under "
            "`skills/`; a copy of one script taken on its own is not a plugin."
        )
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"fold-check: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_loaded = {}


def reader():
    """`unverified_check.py`, loaded once on first use."""
    if "reader" not in _loaded:
        _loaded["reader"] = load(READER, "specseal_unverified_reader_for_folds")
    return _loaded["reader"]


# --- the shape -------------------------------------------------------------


def numbered_statements(text):
    """`[(marker ids, [(1-based line number, live line)])]`, in document order.

    Consecutive marker lines are one group. A statement runs from its markers
    to the next marker, the next heading or the end of the file."""
    uc = reader()
    found = []
    current = None
    previous_was_marker = False
    for number, (line, live) in enumerate(uc.live_lines(text.splitlines()), 1):
        if not live:
            previous_was_marker = False
            continue
        ids = uc.FOLD_MARKER.findall(line)
        if ids:
            if previous_was_marker:
                current[0].extend(ids)
            else:
                current = (list(ids), [])
                found.append(current)
            previous_was_marker = True
            continue
        previous_was_marker = False
        if HEADING.match(line):
            current = None
            continue
        if current is not None:
            current[1].append((number, line))
    return found


def statements(text):
    """`[(marker ids, the statement's live lines)]`, in document order."""
    return [
        (ids, [line for _number, line in lines])
        for ids, lines in numbered_statements(text)
    ]


def names_targets(value):
    """Whether an `Enforced by:` value is read as targets rather than as
    `nothing — <why>`. The shape check and `enforced_lines` both ask this, so
    the lines a wrap limit skips are exactly the lines read as paths."""
    return not value.startswith(NOTHING.strip())


def enforced_lines(text):
    """The 1-based numbers of the lines this reader reads as a statement's
    `Enforced by:` line with targets, whatever the cutoff.

    A line of paths cannot be wrapped without ceasing to be one line, which
    is what the shape counts, so a wrap limit asks this which lines to skip.
    A `nothing — <why>` line is not among them: its reason is prose."""
    return [
        number
        for _ids, lines in numbered_statements(text)
        for number, line in lines
        if line.startswith(ENFORCED) and names_targets(line[len(ENFORCED) :].strip())
    ]


def bound(ids, cutoff):
    """Whether any id in the group is at or above the cutoff."""
    for work_item in ids:
        prefix = work_item.split("-", 1)[0]
        if prefix.isdigit() and int(prefix) >= cutoff:
            return True
    return False


def target_problem(root, target):
    """Why `target` does not resolve under `root`, or None when it does."""
    target = target.strip().strip("`")
    if not target:
        return "an empty target"
    path, _, name = target.partition("::")
    # Both sides through `realpath`, so a symlink inside the root that opens
    # a file outside it is outside, and a root reached through one is itself.
    base = os.path.realpath(root)
    full = os.path.realpath(os.path.join(base, *path.split("/")))
    if os.path.commonpath([full, base]) != base:
        return f"{path} is not a path inside the repository"
    if not os.path.exists(full):
        return f"{path} does not exist"
    if not os.path.isfile(full):
        return f"{path} is not a file in the repository"
    if not name:
        return None
    if not path.endswith(".py"):
        return f"{target}: `::name` needs a Python file"
    with open(full, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    kinds = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    if any(isinstance(n, kinds) and n.name == name for n in ast.walk(tree)):
        return None
    return f"{target}: no def or class named {name} in {path}"


def shape_problems(root, name, text, cutoff):
    """What is wrong with the shape of each bound statement in `text`."""
    problems = []
    for ids, lines in statements(text):
        if not bound(ids, cutoff):
            continue
        where = f"{name}: the statement under {ids}"
        body = [line for line in lines if line.strip()]
        if not body or not BOLD_OPENING.match(body[0]):
            problems.append(f"{where} does not open with a bold rule sentence")
        enforced = [line for line in lines if line.startswith(ENFORCED)]
        if len(enforced) != 1:
            problems.append(
                f"{where} carries {len(enforced)} `Enforced by:` lines, not one"
            )
            continue
        value = enforced[0][len(ENFORCED) :].strip()
        if not names_targets(value):
            if not value[len(NOTHING.strip()) :].strip():
                problems.append(f"{where} says `nothing` and gives no reason")
            continue
        for target in value.split(","):
            problem = target_problem(root, target)
            if problem:
                problems.append(f"{where}: {problem}")
    return problems


# --- the ceiling -----------------------------------------------------------


def markers(text):
    """How many fold markers the fold itself would read in `text`."""
    uc = reader()
    return sum(
        len(uc.FOLD_MARKER.findall(line))
        for line, live in uc.live_lines(text.splitlines())
        if live
    )


def marker_digest(text):
    """The first 12 hex digits of a SHA-256 over the sorted live marker ids."""
    uc = reader()
    ids = sorted(
        found
        for line, live in uc.live_lines(text.splitlines())
        if live
        for found in uc.FOLD_MARKER.findall(line)
    )
    return hashlib.sha256("\n".join(ids).encode()).hexdigest()[:12]


def documents(root):
    """Every top-level `docs/*.md`, repo-relative with `/`, in name order."""
    top = os.path.join(root, DOCS)
    return [
        f"{DOCS}/{name}"
        for name in sorted(os.listdir(top))
        if name.endswith(".md") and os.path.isfile(os.path.join(top, name))
    ]


def read(root, rel):
    with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as f:
        return f.read()


def ceiling_problems(root, ceiling, over, digests=None):
    """Every way the tree at `root` breaks the ceiling or its listing.

    `over` maps a listed document to `(frozen marker count, home)`, and
    `digests` maps it to the `marker_digest` its markers are frozen at."""
    problems = []
    names = documents(root)
    for rel in sorted(set(over) - set(names)):
        problems.append(f"{rel} is listed over the ceiling and does not exist")
    for rel in names:
        text = read(root, rel)
        lines = len(text.splitlines())
        if rel not in over:
            if lines > ceiling:
                problems.append(
                    f"{rel} is {lines} lines, over the ceiling of {ceiling}. "
                    "Split it along its own headings, or place the rule in the "
                    "document for its own sub-subject"
                )
            continue
        frozen, home = over[rel]
        if lines <= ceiling:
            problems.append(
                f"{rel} is {lines} lines, no longer over the ceiling of "
                f"{ceiling}. Remove its entry; {home} was its home"
            )
        found = markers(text)
        now = marker_digest(text)
        if found != frozen:
            problems.append(
                f"{rel} carries {found} fold markers and is frozen at {frozen} "
                f"until {home} splits it. A new fold goes to the document for "
                "the rule's own sub-subject; a removed marker lowers the frozen "
                "count, so the room it made is not refilled, and sets the "
                f"entry's digest in the `{OVER_ROW}` row to {now}, the file's "
                "marker_digest() now, in the same commit"
            )
            continue
        want = (digests or {}).get(rel)
        if want is not None and now != want:
            problems.append(
                f"{rel} carries {frozen} fold markers, but not the ones frozen "
                f"until {home} splits it: their ids no longer match the entry's "
                f"digest in the `{OVER_ROW}` row. If a fold added a statement "
                "here and removed another, the new rule goes to the document "
                "for its own sub-subject. If a marker was removed on purpose, "
                f"set the entry's digest to {now}, the file's marker_digest() "
                "now, in the commit that lowered the count"
            )
    return problems


# --- the rows --------------------------------------------------------------


class Unusable(Exception):
    """A row whose value will not parse (exit 2, nothing checked)."""


def seal_home(root):
    """The `seal/` root of the repository at `root`, or "" where it has none.

    Through the one resolver, `hooks/optin.py#home_at`, loaded by path the
    way `settle.py#main` loads it: `<root>/seal/`, else the common git
    directory's `seal/`, and "" for a repository that opted out."""
    optin = load(OPTIN, "specseal_optin_for_folds")
    return optin.home_at(root)


def config_rows(home):
    """Every `| Item | Value |` row of `<home>/config.md`, through the one
    table reader, `hooks/config.py#config_rows`. No root, no file or a file
    that will not read is no row at all, as every reader of it fails."""
    if not home:
        return []
    try:
        with open(os.path.join(home, CONFIG), encoding="utf-8") as f:
            text = f.read()
    except (OSError, ValueError):
        return []
    return load(CONFIG_READER, "specseal_config_for_folds").config_rows(text)


def row_value(rows, item):
    """The row's value, or None where it is absent or empty."""
    for name, value in rows:
        if name == item:
            return value or None
    return None


def parse_over(value):
    """`(over, digests)` from an `Over the ceiling` value, or `Unusable`."""
    over, digests = {}, {}
    if value is None or value.lower() == NONE_LISTED:
        return over, digests
    for entry in value.split(";"):
        match = OVER_ENTRY.match(entry.strip())
        if not match:
            raise Unusable(
                f"the `{OVER_ROW}` row holds `{entry.strip()}`, which is not "
                f"`{NONE_LISTED}` and not an entry `{OVER_SHAPE}`"
            )
        over[match["path"]] = (int(match["count"]), match["home"])
        digests[match["path"]] = match["digest"]
    return over, digests


def declared(home):
    """`(cutoff, ceiling, over, digests)` as the root's `config.md` states
    them, None for a row that is absent, or `Unusable` naming the row."""
    rows = config_rows(home)
    cutoff = row_value(rows, SHAPE_ROW)
    if cutoff is not None:
        if not WHOLE.fullmatch(cutoff):
            raise Unusable(
                f"the `{SHAPE_ROW}` row holds `{cutoff}`, which is not a "
                "work-item id's epoch prefix (a whole number; `0` binds every "
                "statement)"
            )
        cutoff = int(cutoff)
    ceiling = row_value(rows, CEILING_ROW)
    if ceiling is not None:
        if not WHOLE.fullmatch(ceiling) or int(ceiling) < 1:
            raise Unusable(
                f"the `{CEILING_ROW}` row holds `{ceiling}`, which is not a "
                "positive whole number of lines"
            )
        ceiling = int(ceiling)
    over, digests = parse_over(row_value(rows, OVER_ROW))
    return cutoff, ceiling, over, digests


# --- the command -----------------------------------------------------------


def positive(text):
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError(f"{text} is not a positive integer")
    return value


def not_negative(text):
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError(f"{text} is not a work-item id prefix")
    return value


def plural(count, word):
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def run(root, values, where, out):
    """Both checks over `root`, the lines they print, and the problems.

    `where` names what the values were read from, for the line that says a
    check was not run because nothing declared its value."""
    cutoff, ceiling, over, digests = values
    names = documents(root)
    problems = []
    if cutoff is None:
        out.write(
            f"fold-check: `{SHAPE_ROW}` is not declared in {where}, so the "
            "shape was not checked\n"
        )
    else:
        groups = bound_groups = 0
        for rel in names:
            text = read(root, rel)
            found = statements(text)
            groups += len(found)
            bound_groups += sum(1 for ids, _ in found if bound(ids, cutoff))
            problems += shape_problems(root, rel, text, cutoff)
        out.write(
            f"fold-check: read {plural(groups, 'statement')} in "
            f"{plural(len(names), 'document')} under {DOCS}/; the cutoff "
            f"{cutoff} binds {bound_groups}\n"
        )
    if ceiling is None:
        out.write(
            f"fold-check: `{CEILING_ROW}` is not declared in {where}, so no "
            "document's length was checked\n"
        )
    else:
        problems += ceiling_problems(root, ceiling, over, digests)
        out.write(
            f"fold-check: held {plural(len(names), 'document')} under {DOCS}/ "
            f"to {ceiling} lines, {len(over)} listed over it\n"
        )
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="fold-check",
        description="Hold the fold's statement shape and document ceiling "
        "over the top level of docs/, with the values seal/config.md states.",
    )
    ap.add_argument("--root", help="the repository to read (default: cwd)")
    ap.add_argument(
        "--shape-from",
        type=not_negative,
        metavar="ID",
        help=f"bind the shape from this work-item id prefix on, for this run "
        f"only, over the `{SHAPE_ROW}` row; 0 binds every statement",
    )
    ap.add_argument(
        "--ceiling",
        type=positive,
        metavar="N",
        help=f"hold every top-level docs/*.md to N lines, for this run only, "
        f"over the `{CEILING_ROW}` row",
    )
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root or os.getcwd())
    if not os.path.isdir(root):
        sys.stderr.write(
            f"fold-check: {root} is not a directory — nothing was checked\n"
        )
        return 2
    home = seal_home(root)
    where = (
        os.path.join(home, CONFIG)
        if home
        else f"{root}, which has no seal/ root at either place"
    )
    try:
        cutoff, ceiling, over, digests = declared(home)
    except Unusable as refused:
        sys.stderr.write(f"fold-check: in {where}, {refused} — nothing was checked\n")
        return 2
    if args.shape_from is not None:
        cutoff = args.shape_from
    if args.ceiling is not None:
        ceiling = args.ceiling
    if cutoff is None and ceiling is None:
        sys.stdout.write(
            f"fold-check: neither `{SHAPE_ROW}` nor `{CEILING_ROW}` is declared "
            f"in {where}, so nothing was checked\n"
        )
        return 0
    if not os.path.isdir(os.path.join(root, DOCS)):
        sys.stderr.write(
            f"fold-check: {root} has no {DOCS}/ directory — nothing was checked\n"
        )
        return 2
    problems = run(root, (cutoff, ceiling, over, digests), where, sys.stdout)
    for problem in problems:
        sys.stdout.write(problem + "\n")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
