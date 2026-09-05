#!/usr/bin/env python3
"""round-record — write `rounds/round-N.md` from what is not prose.

Issue #161 measured the last branch of this repository: fifteen review rounds
and 22 h 47 min, of which 12.8 h sat in front of record commits, and half of
the 65 findings were located in a record rather than in code. The record is
nine parsed fields and four tables. Every one of them is derivable from
something a person did not type into a cell — the target from git, the
terminal lines and the three tables from the reviewer's report, the reach-back
from the record that came before — and the orchestrator was deriving all of
it by hand, one cell at a time, with the reviewer's report open and a fix
pass waiting.

So this writes the record. `new` takes the reviewer's report and the round
paragraph of the spawn prompt, and derives the rest:

  Target SHA          `--target`, which has to resolve
  Ran by              `--ran-by`
  PR                  `--pr`, else what `gh pr view` says, else `not yet opened`
  Broad gate          `--broad-gate`, else `not yet`
  Fixes checked by    `nobody — the fixes are not yet written` while a verdict
                      is open or closed on a fix; `no fixes to check` when
                      every verdict closed without one. The two values are
                      the landing states `templates/sdd-round.md` and
                      `chain_check.fix_surface` describe, and the second
                      exists because a record that commissions no fixes will
                      never have any — *not yet written* is false of it the
                      moment it is written
  Contract changes    `none — the fixes are not yet written`, or a bare `none`
  New units           in the same two states, for the same reason
  Needs a fix         what stands after the colon in the report's line
  Loses a record or   the same, for the second line; a report lacking either
  crashes             line is refused
  Pass                ticked when no verdict row is open
  the four sections   the round paragraph verbatim; the report's verdict,
                      probe and deferred tables row for row; every `Location`
                      cell of every earlier record, deduplicated

Then it sets the previous record's `Fixes checked by` to `round-N` — the one
reach-back the orchestrator forgot five times on the last branch — and runs
`chain_check.py --worktree` on the repository, so the record is judged before
it is committed rather than by CI afterwards.

`close` is the other end of the round. It takes the smith's fix table — one
row per finding under `## Fixes`, `| # | Verdict | Commit or grounds |`, the
verdict `fixed` with the commit, `answered` with the grounds, or `deferred
<home>` — and the range of fix commits, and derives the rest:

  the verdict cells    `**fixed** `<sha>`` with the grounds prefixed
                       `fixed at <sha>`, `answered` with the grounds, or
                       `deferred <home>` with the home; a commit has to
                       resolve and lie inside the range
  Contract changes     every top-level Python unit whose parameters or return
                       arities differ between the two ends of the range, each
                       with the enclosing unit of every `name(` in the tree,
                       `unit → site, site`; callers under `tests/` read
                       `pytest`, or `pytest only` when they are the whole reach
  New units            every top-level def, class and module-level constant
                       present at the end of the range and absent at its
                       start, `unit (depth 1)`; for a file the AST cannot read
                       the `+` diff lines are read for `def`, `class`,
                       `function`, `fn`, `func`, and a comment after the table
                       says which files were read that way
  Pass                 ticked when no verdict is open once the table applies
  Broad gate           `--broad-gate`, when given

A unit at depth 2 is refused before any of that is written: a `fixed`
finding whose `Location` sits inside a unit an earlier record's `New units`
names, in a file the range adds a unit to. The refusal names the unit, the
finding, the record, and the exit the rule gives. `Fixes checked by` is left
as it stands — `new` for the next round sets it — and the check runs the way
it runs for `new`.

**Every cell writer takes a structured value and refuses one it cannot
write.** A `|` or a newline in any cell, or a comma in `New units` or
`Contract changes`, is refused before anything touches the disk: the last
branch's 🔴 1 of round 2 was a semicolon inside a code span splitting a cell,
and its 🔴 1 of round 4 was prose inside a `New units` entry. Neither can be
written here, and there is no `--grounds` or `--note` flag for a session to
hide prose in. The generator carries none of the template's explanatory
comments into the record either: those are documentation, and a record is
read by checkers.

Nothing here commits. The generator writes files and runs the check; the
commit is the orchestrator's, made from a record it has read.

The constants this file matches against are `chain_check.py`'s wherever that
file has one — the headings, the field labels, the verdict vocabulary, the
`not yet written` reason — loaded from it rather than spelled again, so the
writer and the checker cannot drift about a string. What is defined here is
only what the checker never reads: the headings and headers of the two tables
it does not parse, and the honest starting values of the cells it does.

Exit codes: 0 and 1 are `chain_check`'s own, after the record is written ·
2 the input was unusable and nothing was written.
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHAIN = os.path.join(HERE, "chain_check.py")


def load(path, name):
    """Import a sibling script by path, or die — a missing checker is exit 2."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"round-record: cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


chain = load(CHAIN, "specseal_chain_check")

# The one heading and the one column the checker reads, by the checker's name.
VERDICTS = chain.VERDICTS
VERDICT_HEADER = ("#", "Finding", "Location", chain.VERDICT_COLUMN, "Grounds")
# The two tables the checker never parses, so their names live here. Their
# headers are what `agents/warden.md` §Report tells the reviewer to write,
# and `tests/test_the_record_is_generated.py` reads them from here and looks
# for them there — one constant, two carriers.
PROBES = "## Executed probes"
PROBE_HEADER = ("What was run", "Result")
DEFERRED = "## Deferred"
DEFERRED_HEADER = ("Finding", "Where it went", "Who answers it")
REPORT_TABLES = (
    (VERDICTS, VERDICT_HEADER),
    (PROBES, PROBE_HEADER),
    (DEFERRED, DEFERRED_HEADER),
)
# The two sections the generator fills from somewhere other than the report.
ASKED = "## What this round was asked"
INHERITED = "## Inherited coordinates"
INHERITED_HEADER = ("From", "Coordinate", "Why it is still worth opening")
# Field labels the checker has no constant for, because it never reads them.
BROAD_GATE = "Broad gate"
# The honest values while nothing has happened yet. `not yet opened` is what
# `chain_check.declared_pull_head` documents as the pre-pull-request value;
# `nothing to drain` is `templates/sdd-round.md`'s required answer for a
# Deferred section with no rows.
PR_NOT_YET = "not yet opened"
GATE_NOT_YET = "not yet"
NOTHING_TO_DRAIN = "nothing to drain"
# Built by codepoint for the reason `chain_check.SEPARATORS` gives: an em dash
# in a string literal is what ruff's RUF001 reads as a mistyped hyphen.
DASH = chr(0x2014)
# The landing values `ORDER_FROM` requires of a record committed before its
# fixes exist, spelled from the checker's own words.
PENDING_CHECKER = f"{chain.NOBODY} {DASH} {chain.NOT_YET}"
PENDING_SURFACE = f"{chain.NONE_WORD} {DASH} {chain.NOT_YET}"
# The rows a comma splits. `depth_problems` reads a comma inside a `New
# units` entry as a second unit, and `fix_surface`'s reach list is
# comma-separated, so a comma in either is structure and not punctuation.
COMMA_SPLIT_ROWS = (chain.NEW_UNITS, chain.CONTRACT)
# The two terminal lines of a reviewer's report, by the field they land in.
TERMINAL_LINES = (chain.NEEDS, chain.FLOOR)


class Refused(Exception):
    """An input this cannot turn into a record. Nothing is written."""


def escape(value):
    """A cell's text with its pipes escaped the way `split_row` unescapes."""
    return value.replace("|", "\\|")


def row(cells):
    """One markdown table row from already-checked cells."""
    return "| " + " | ".join(cells) + " |"


def separator(width):
    return "|" + "---|" * width


def cell(label, value):
    """`| label | value |`, or `Refused`.

    A `|` would split the row and a newline would end it, so neither can be
    written whatever the row. A comma is refused in the two rows the checker
    splits on it, and nowhere else — `Needs a fix` is prose and keeps its
    commas.
    """
    if not isinstance(value, str) or not value.strip():
        raise Refused(f"`{label}` needs a value and got {value!r}")
    for what, char in (("a pipe", "|"), ("a newline", "\n"), ("a newline", "\r")):
        if char in value:
            raise Refused(
                f"`{label}` cannot carry {what}: {value!r}. A row is one line "
                "and its cells are what stands between the pipes"
            )
    if label in COMMA_SPLIT_ROWS and "," in value:
        raise Refused(
            f"`{label}` cannot carry a comma: {value!r}. The checker splits "
            "that row on it, so a comma is a second entry and never punctuation"
        )
    return row((label, value))


def git(root, *args):
    r = subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    return r.stdout if r.returncode == 0 else None


def pull_request_cell(root, given, which=shutil.which, run=subprocess.run):
    """The `PR` cell: the flag, else `gh`'s answer, else `not yet opened`.

    `gh pr view --json number,url` on the current branch. The number goes
    first so `chain_check.PR_RE` finds it before the digits in the URL.
    `which` and `run` are parameters so a case can stand in for a `gh` that
    answers without a remote to ask.
    """
    if given is not None:
        return given
    if which("gh") is None:
        return PR_NOT_YET
    try:
        r = run(
            ["gh", "pr", "view", "--json", "number,url"],
            cwd=root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return PR_NOT_YET
    if r.returncode != 0:
        return PR_NOT_YET
    try:
        answer = json.loads(r.stdout)
        number, url = int(answer["number"]), str(answer["url"])
    except (ValueError, KeyError, TypeError):
        return PR_NOT_YET
    return f"#{number} {DASH} {url}"


def pull_request_is_ready(root, which=shutil.which, run=subprocess.run):
    """True only when `gh` says the branch's pull request is not a draft.

    `chain_check` judges an unchecked `Pass` as a failure on a READY pull
    request and as the honest state of a running review on a draft. A record
    being generated is a review still running, so the check is told `draft`
    unless the platform says otherwise — and the platform is asked, not the
    session.
    """
    if which("gh") is None:
        return False
    try:
        r = run(
            ["gh", "pr", "view", "--json", "isDraft"],
            cwd=root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        return r.returncode == 0 and json.loads(r.stdout).get("isDraft") is False
    except (OSError, subprocess.SubprocessError, ValueError, AttributeError):
        return False


def default_baseline(root):
    """The upstream of the current branch, else `origin/main`."""
    upstream = git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    return upstream.strip() if upstream and upstream.strip() else "origin/main"


def read_text(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as exc:
        raise Refused(f"cannot read the {what} at {path}: {exc}") from exc


def section_body(reader, lines, heading):
    """(start, [(index, line)]) for the one section under `heading`, or None.

    `lines` are already `readable`, so a heading inside a comment or a fence
    is not a section, and indices are the raw file's.
    """
    starts = reader.sections(lines, heading)
    if not starts:
        return None
    if len(starts) > 1:
        raise Refused(f"the report has {len(starts)} `{heading}` sections")
    body = []
    for i in range(starts[0] + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        body.append((i, lines[i]))
    return starts[0], body


def table_body(reader, lines, heading, header, required):
    """[(index, cells)] for the body rows under `heading`, or None.

    The header has to be the record's own, cell for cell: a table whose
    columns differ is one the checker's column lookup reads differently, and
    copying it would put the difference in the record. Returns None when the
    section is absent and not required. Indices are the raw file's, so a
    caller can copy the raw line or replace it.
    """
    found = section_body(reader, lines, heading)
    if found is None:
        if required:
            raise Refused(
                f"the report has no `{heading}` section — the generator copies "
                "that table into the record, and a report without it says "
                "nothing about what the round found"
            )
        return None
    _start, body = found
    rows = [(i, reader.split_row(ln)) for i, ln in body if ln.strip()]
    rows = [(i, cells) for i, cells in rows if cells is not None]
    if not rows:
        if required:
            raise Refused(f"`{heading}` holds no table")
        return None
    seen = tuple(reader.visible(c) for c in rows[0][1])
    if seen != header:
        raise Refused(
            f"`{heading}` has the header {row(seen)!r}; the record's is "
            f"{row(header)!r}, and the generator copies only a table in the "
            "record's own columns"
        )
    return [
        (i, cells)
        for i, cells in rows[1:]
        if not reader.is_separator([reader.visible(c) for c in cells])
    ]


def table_of(reader, raw, lines, heading, header, required):
    """The rows under `heading` as raw lines, header and separator first."""
    body = table_body(reader, lines, heading, header, required)
    if body is None:
        return None
    return [row(header), separator(len(header))] + [raw[i].strip() for i, _ in body]


def terminal_value(reader, lines, label):
    """What stands after the colon in the report's `<label>: …` line."""
    pattern = re.compile(r"^\s*" + re.escape(label) + r"\s*:\s*(.*?)\s*$")
    found = [m.group(1) for ln in lines for m in [pattern.match(ln)] if m]
    if len(found) != 1:
        raise Refused(
            f"the report has {len(found)} `{label}:` lines and the record "
            "needs exactly one — the row is copied from what stands after "
            "the colon"
        )
    value = reader.visible(found[0])
    word, _ = chain.yes_or_no(value)
    if word is None:
        raise Refused(
            f"`{label}: {value}` is not `{chain.FLOOR_NO}` or "
            f"`{chain.FLOOR_YES} {DASH} <what>`, which is the vocabulary the "
            "checker reads the row in"
        )
    return value


def verdict_words(reader, rows):
    """The normalized verdict of each body row of a copied verdict table."""
    col = VERDICT_HEADER.index(chain.VERDICT_COLUMN)
    words = []
    for line in rows[2:]:
        cells = reader.split_row(line)
        seen = [reader.visible(c) for c in cells]
        if len(seen) <= col:
            raise Refused(f"a verdict row has {len(seen)} cells: {line!r}")
        words.append(chain.verdict_of(seen, col))
    return words


def earlier_records(routing, rounds, n):
    """[(K, path)] for every `round-K.md` on disk with K < n, lowest first."""
    try:
        names = os.listdir(rounds)
    except OSError:
        return []
    found = []
    for name in names:
        k = routing.round_number(name)
        path = os.path.join(rounds, name)
        if k is not None and k < n and os.path.isfile(path):
            found.append((k, path))
    return sorted(found)


def inherited_rows(reader, earlier):
    """One row per `Location` cell of every earlier record, first seen wins.

    `Why` names the round, the finding and its verdict word, so the next
    round knows what it is reopening; coordinates carry, conclusions do not.
    """
    location = VERDICT_HEADER.index("Location")
    number = VERDICT_HEADER.index("#")
    seen, out = set(), []
    for k, path in earlier:
        text = read_text(path, f"earlier record round-{k}.md")
        lines = reader.readable(text)
        rows = table_of(
            reader, text.splitlines(), lines, VERDICTS, VERDICT_HEADER, True
        )
        for word, line in zip(verdict_words(reader, rows), rows[2:], strict=True):
            cells = [reader.visible(c) for c in reader.split_row(line)]
            coordinate = cells[location]
            if not coordinate or coordinate in seen:
                continue
            seen.add(coordinate)
            out.append(
                row(
                    (
                        f"round-{k}",
                        escape(coordinate),
                        escape(f"round {k}'s {cells[number]} {DASH} {word}"),
                    )
                )
            )
    return out


def reach_back(reader, path, n):
    """Set round N-1's `Fixes checked by` to `round-N`, touching nothing else.

    Refused when the cell is absent or outside the checker's vocabulary — a
    cell nobody can read is not one to overwrite silently — and when it
    already names a different later round, because that is a true fact about
    which round read those fixes and this would be replacing it with a guess.
    """
    text = read_text(path, f"earlier record round-{n - 1}.md")
    raw = text.splitlines()
    lines = reader.readable(text)
    hits = [
        i
        for i, ln in enumerate(lines)
        for cells in [reader.split_row(ln)]
        if cells and len(cells) >= 2 and cells[0].strip() == chain.CHECKED_BY
    ]
    if len(hits) != 1:
        raise Refused(
            f"{path} has {len(hits)} `| {chain.CHECKED_BY} | … |` rows, and the "
            "reach-back needs exactly one to set"
        )
    i = hits[0]
    value = reader.visible(reader.split_row(lines[i])[1]).strip("`").rstrip(".")
    mine = f"round-{n}"
    if chain.CHECKER_RE.match(value.lower()):
        named = value.lower().removesuffix(".md")
        if named != mine:
            raise Refused(
                f"{path}'s `{chain.CHECKED_BY}` already names `{value}`, and "
                f"this is {mine}. A record that says which round read its "
                "fixes is not overwritten with a different one"
            )
    elif value.lower() != chain.NO_FIXES and chain.nobody_reason(value.lower()) is None:
        raise Refused(
            f"{path}'s `{chain.CHECKED_BY}` reads `{value}`, which is outside "
            f"the vocabulary — `round-N`, `{chain.NO_FIXES}`, or "
            f"`{chain.NOBODY} {DASH} <why>`. Correct it before the reach-back "
            "overwrites it"
        )
    raw[i] = cell(chain.CHECKED_BY, mine)
    ending = "\n" if text.endswith("\n") else ""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(raw) + ending)


def build(reader, routing, args, root, item, rounds):
    """The record's text, and the reach-back to make once it is written."""
    if not reader.resolves(root, args.target):
        raise Refused(
            f"--target {args.target} does not resolve in {root} — a record "
            "naming a commit nobody can open names nothing"
        )
    report = read_text(args.report, "report")
    raw = report.splitlines()
    lines = reader.readable(report)
    asked = read_text(args.asked, "round paragraph").strip()
    if not asked:
        raise Refused(
            f"the round paragraph at {args.asked} is empty — `{ASKED}` is the "
            "durable home of what this round was told to attack (#119)"
        )

    verdicts = table_of(reader, raw, lines, VERDICTS, VERDICT_HEADER, True)
    probes = table_of(reader, raw, lines, PROBES, PROBE_HEADER, False) or [
        row(PROBE_HEADER),
        separator(len(PROBE_HEADER)),
    ]
    deferred = table_of(reader, raw, lines, DEFERRED, DEFERRED_HEADER, False)
    if deferred is None:
        deferred = [row(DEFERRED_HEADER), separator(len(DEFERRED_HEADER)), ""]
        deferred.append(NOTHING_TO_DRAIN)
    needs = terminal_value(reader, lines, chain.NEEDS)
    floor = terminal_value(reader, lines, chain.FLOOR)

    words = verdict_words(reader, verdicts)
    open_rows = [w for w in words if w not in chain.CLOSED_WORDS]
    fixed_rows = [w for w in words if w in chain.FIX_WORDS]
    if open_rows or fixed_rows:
        checker, surface = PENDING_CHECKER, PENDING_SURFACE
    else:
        checker, surface = chain.NO_FIXES, chain.NONE_WORD

    earlier = earlier_records(routing, rounds, args.round)
    if args.round > 1 and not any(k == args.round - 1 for k, _ in earlier):
        raise Refused(
            f"round {args.round} needs round-{args.round - 1}.md beside it in "
            f"{rounds}, and it is not there — the reach-back has nothing to set"
        )

    fields = [
        row(("Field", "Value")),
        separator(2),
        cell(chain.TARGET, args.target),
        cell(chain.RAN_BY, args.ran_by),
        cell(chain.PR_FIELD, pull_request_cell(root, args.pr)),
        cell(BROAD_GATE, args.broad_gate if args.broad_gate else GATE_NOT_YET),
        cell(chain.CHECKED_BY, checker),
        cell(chain.CONTRACT, surface),
        cell(chain.NEW_UNITS, surface),
        cell(chain.NEEDS, needs),
        cell(chain.FLOOR, floor),
    ]
    box = "x" if not open_rows else " "
    inherited = [row(INHERITED_HEADER), separator(len(INHERITED_HEADER))]
    inherited += inherited_rows(reader, earlier)

    parts = [
        f"# {os.path.basename(item)} {DASH} review round {args.round}",
        "",
        *fields,
        "",
        f"- [{box}] Pass",
        "",
        ASKED,
        "",
        asked,
        "",
        VERDICTS,
        "",
        *verdicts,
        "",
        PROBES,
        "",
        *probes,
        "",
        INHERITED,
        "",
        *inherited,
        "",
        DEFERRED,
        "",
        *deferred,
    ]
    previous = next((p for k, p in earlier if k == args.round - 1), None)
    return "\n".join(parts) + "\n", previous


def run_check(root, baseline):
    """`chain_check --worktree` on the repository, printed, its code returned.

    The check reads the pull request's state from the event payload GitHub
    writes, and outside a workflow it has none and judges as READY — where an
    unchecked `Pass` fails. A record being generated is a review still
    running, so the check is told `draft` unless `gh` says the pull request
    is already ready, in which case it is judged as CI will judge it.
    """
    env_was = os.environ.get("GITHUB_EVENT_PATH")
    payload = None
    if not pull_request_is_ready(root):
        fd, payload = tempfile.mkstemp(suffix=".json", prefix="round-record-")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"pull_request": {"draft": True}}, f)
        os.environ["GITHUB_EVENT_PATH"] = payload
    try:
        return chain.main(["--worktree", "--baseline", baseline, "--root", root])
    finally:
        if payload is not None:
            if env_was is None:
                os.environ.pop("GITHUB_EVENT_PATH", None)
            else:
                os.environ["GITHUB_EVENT_PATH"] = env_was
            try:
                os.unlink(payload)
            except OSError:
                pass


def where(args):
    """(reader, routing, root, item, rounds) for `--item`, or `Refused`."""
    reader = load(chain.READER, "specseal_unverified_reader")
    routing = load(chain.ROUTING, "specseal_routing")
    item = os.path.abspath(args.item)
    root = args.root or reader.repo_root(item)
    if root is None or not os.path.isdir(item):
        raise Refused(f"--item {args.item} is not a directory inside a git repository")
    root = os.path.abspath(root)
    if args.round < 1:
        raise Refused(f"--round {args.round} — rounds are numbered from 1")
    rounds = os.path.join(item, routing.ROUNDS_DIR)
    return reader, routing, root, item, rounds


def new(args):
    reader, routing, root, item, rounds = where(args)
    target = os.path.join(rounds, f"round-{args.round}.md")
    if os.path.lexists(target):
        raise Refused(
            f"{target} already exists. A record is written once and corrected "
            "in place — this does not overwrite one"
        )

    text, previous = build(reader, routing, args, root, item, rounds)
    if previous is not None:
        reach_back(reader, previous, args.round)
    os.makedirs(rounds, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"round-record: wrote {os.path.relpath(target, root)}")
    if previous is not None:
        print(
            f"round-record: set `{chain.CHECKED_BY}` of "
            f"{os.path.relpath(previous, root)} to round-{args.round}"
        )
    return run_check(root, args.baseline or default_baseline(root))


# --- close: the fix table applied, the fix surface measured ------------------

# The smith's fix-pass handover: one row per finding of the round it answers,
# under this heading, in these columns. `agents/smith.md` and
# `skills/implement/SKILL.md` §5 tell the smith to write it, and
# `tests/test_the_fixes_close_the_record.py` reads both from here — one
# constant, three carriers.
FIXES = "## Fixes"
FIXES_HEADER = ("#", "Verdict", "Commit or grounds")
# The three verdicts a fix pass may hand over, all the checker's own closing
# words. `deferred <home>` closes on the home after it and a bare `deferred`
# stays OPEN (`questions.md` A4) -- `close` writes the word with the home, so
# a `Pass` ticked over a table of deferrals is the capped run's legal end.
FIXED, ANSWERED, DEFERRED_WORD = "fixed", "answered", chain.DEFERRED
assert {FIXED, ANSWERED, DEFERRED_WORD} <= chain.CLOSED_WORDS, (
    "a fix verdict the checker cannot close"
)
FIXED_AT = "fixed at"
# The reach grammar `fix_surface` reads, `unit → site, site`, in the checker's
# first spelling of the arrow. The comma between sites is the writer's own and
# never an input's, which is what lets `cell` keep refusing one in this row.
ARROW = chain.ARROWS[0]
PYTEST_ONLY = "pytest only"
PYTEST = "pytest"
NO_SITE = "no call site found"
TESTS_DIR = "tests"
# The columns of the verdict table, by the record's header.
NUMBER_COL = VERDICT_HEADER.index("#")
LOCATION_COL = VERDICT_HEADER.index("Location")
VERDICT_COL = VERDICT_HEADER.index(chain.VERDICT_COLUMN)
GROUNDS_COL = VERDICT_HEADER.index("Grounds")
# `questions.md` A1: a file the AST cannot read — not Python, or Python that
# does not parse at one end of the range — gives up its added definitions by
# a `+` diff line starting with one of five keywords and a name. The record
# says which files were read that way, in a comment the checkers blank.
HEURISTIC_RE = re.compile(r"^\+\s*(?:def|class|function|fn|func)\s+([A-Za-z_]\w*)")
HEURISTIC_NOTE = "read by the diff-line heuristic and not by the AST"
# The shapes a `Location` cell names a unit in: `path#unit`, `path#unit@hash`,
# `path:line`, and a backticked identifier on its own.
LOCATION_UNIT_RE = re.compile(r"([\w./-]+\.py)#([A-Za-z_]\w*)")
LOCATION_LINE_RE = re.compile(r"([\w./-]+\.py):(\d+)")
IDENTIFIER_RE = re.compile(r"`([A-Za-z_]\w*)`")
NUMBER_RE = re.compile(r"\d+")
DEPTH_EXIT = "deferred with a named answerer, or becomes an issue"


def part(label, text):
    """One name inside a surface entry — a unit or a site — or `Refused`.

    The writer joins names into `unit → site, site` and `unit (depth N)`, so
    the separators are its own: a name carrying one would read as two names,
    and `cell`'s refusal of a comma in these rows is what this keeps true.
    """
    text = text.strip()
    if not text:
        raise Refused(f"`{label}` needs a name and got {text!r}")
    for what, char in (
        ("a pipe", "|"),
        ("a newline", "\n"),
        ("a newline", "\r"),
        ("a comma", ","),
        ("a semicolon", ";"),
    ):
        if char in text:
            raise Refused(
                f"`{label}` cannot carry {what} inside a name: {text!r}. The "
                "separators of that row are the writer's, never a name's"
            )
    return text


def contract_entry(unit, sites):
    """`unit → site, site`, every name checked."""
    label = chain.CONTRACT
    return f"{part(label, unit)} {ARROW} " + ", ".join(part(label, s) for s in sites)


def units_entry(unit, depth):
    """`unit (depth N)`, the name checked."""
    return f"{part(chain.NEW_UNITS, unit)} ({chain.DEPTH_WORD} {depth})"


def surface_cell(label, entries):
    """The row for one surface list: `none` when empty, else `;`-joined.

    `row` rather than `cell`, because the joined value carries the writer's
    own commas and `cell` refuses one in these rows on purpose — every name
    in `entries` has been through `part`, which is the check `cell` would
    have made on the whole.
    """
    if not entries:
        return cell(label, chain.NONE_WORD)
    return row((label, "; ".join(entries)))


def parse_range(root, value):
    """(a, b) as full commits from `<a>..<b>`, or `Refused`."""
    a, dots, b = value.partition("..")
    a, b = a.strip(), b.strip()
    if not dots or not a or not b or b.startswith("."):
        raise Refused(f"--range {value!r} is not `<a>..<b>`")
    out = []
    for ref in (a, b):
        full = chain.resolves_to(root, ref)
        if full is None:
            raise Refused(f"--range names `{ref}`, which does not resolve in {root}")
        out.append(full)
    return out[0], out[1]


def touched(root, a, b):
    """The paths the range changes, as they stand at `b`; deletions left out.

    A rename is one path — the new one — so a renamed file's units read as
    new when nothing at `a` carries that path, which is the honest reading
    of a comparison that opens both ends by path.
    """
    out = git(root, "diff", "--name-status", "-M", a, b)
    if out is None:
        raise Refused(f"git diff {a[:7]}..{b[:7]} failed in {root}")
    paths = []
    for line in out.splitlines():
        cells = line.split("\t")
        if len(cells) < 2 or not cells[0] or cells[0][0] == "D":
            continue
        paths.append(cells[-1])
    return paths


def parse_module(text):
    """`ast.Module`, or None for text that is not Python."""
    if text is None:
        return None
    try:
        return ast.parse(text)
    except (SyntaxError, ValueError):
        return None


def signature(args):
    """A unit's parameters: names in order, whether each has a default, and
    the `*args` / `**kwargs` names — what a call site can be wrong about."""
    positional = args.posonlyargs + args.args
    padding = [False] * (len(positional) - len(args.defaults))
    defaults = padding + [True] * len(args.defaults)
    return (
        tuple((arg.arg, has) for arg, has in zip(positional, defaults, strict=True)),
        args.vararg.arg if args.vararg else None,
        tuple(
            (arg.arg, default is not None)
            for arg, default in zip(args.kwonlyargs, args.kw_defaults, strict=True)
        ),
        args.kwarg.arg if args.kwarg else None,
    )


def return_arities(node):
    """The set of arities the unit's own `return` statements have — 0 for a
    bare `return`, n for a tuple of n elements, 1 for anything else. A
    nested def, class or lambda is somebody else's returns."""
    found, stack = set(), list(node.body)
    while stack:
        n = stack.pop()
        if isinstance(
            n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        if isinstance(n, ast.Return):
            if n.value is None:
                found.add(0)
            elif isinstance(n.value, ast.Tuple):
                found.add(len(n.value.elts))
            else:
                found.add(1)
        stack.extend(ast.iter_child_nodes(n))
    return frozenset(found)


def top_units(module):
    """{name: (contract, first line, last line)} for every top-level def,
    class and constant, in source order.

    The contract is what `Contract changes` compares: a function's
    parameters and return arities, a class's `__init__` parameters, and
    nothing for a constant — a changed value is not a changed contract. A
    constant is an assignment to a bare name at module level.
    """
    out = {}
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            contract = (signature(node.args), return_arities(node))
            out[node.name] = (contract, node.lineno, node.end_lineno)
        elif isinstance(node, ast.ClassDef):
            init = next(
                (
                    n
                    for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and n.name == "__init__"
                ),
                None,
            )
            contract = (signature(init.args) if init else None, None)
            out[node.name] = (contract, node.lineno, node.end_lineno)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = (None, node.lineno, node.end_lineno)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.value is not None:
                out[node.target.id] = (None, node.lineno, node.end_lineno)
    return out


def enclosing_unit(units, line):
    """The top-level unit whose lines hold `line`, or None at module level."""
    for name, (_, first, last) in units.items():
        if first <= line <= (last or first):
            return name
    return None


def measure(reader, root, a, b, paths):
    """(changed, added, heuristic, at_a, at_b) over the range.

    `changed` and `added` are `[(path, unit)]` — a contract that differs
    between the two ends, and a unit present at `b` and absent at `a`, in
    file order. `heuristic` names the files whose units came from the diff
    lines rather than the AST. `at_a` and `at_b` are the parsed units per
    path, for the depth walk and the call-site walk.
    """
    changed, added, heuristic, at_a, at_b = [], [], [], {}, {}
    for rel in paths:
        before_text = reader.show(root, a, rel)
        after_text = reader.show(root, b, rel)
        before = parse_module(before_text) if rel.endswith(".py") else None
        after = parse_module(after_text) if rel.endswith(".py") else None
        by_ast = after is not None and (before_text is None or before is not None)
        if by_ast:
            old = top_units(before) if before is not None else {}
            new_units = top_units(after)
            at_a[rel], at_b[rel] = old, new_units
            for name, (contract, _, _) in new_units.items():
                if name not in old:
                    added.append((rel, name))
                elif contract is not None and contract != old[name][0]:
                    changed.append((rel, name))
            continue
        heuristic.append(rel)
        for line in (git(root, "diff", a, b, "--", rel) or "").splitlines():
            m = HEURISTIC_RE.match(line)
            if m:
                added.append((rel, m.group(1)))
    return changed, added, heuristic, at_a, at_b


def under_tests(path):
    return TESTS_DIR in path.split("/")[:-1]


def call_sites(reader, root, b, rel, name, at_b):
    """The reach of one changed unit at `b`: the enclosing top-level unit of
    every `name(` in the tracked files, the unit's own def line excluded,
    the file's basename for a call at module level or outside Python.

    Callers under `tests/` collapse to `pytest`, and to `pytest only` when
    they are the whole reach; a unit nobody calls reads `no call site
    found`, because `fix_surface` refuses a unit listed without a reach
    and an empty reach would be the tolerant read it refuses.
    """
    out = git(root, "grep", "-n", "-F", "-e", f"{name}(", b) or ""
    word = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"\(")
    named, tested = [], False
    for line in out.splitlines():
        try:
            _ref, path, number, text = line.split(":", 3)
            number = int(number)
        except ValueError:
            continue
        if not word.search(text):
            continue
        if path.endswith(".py"):
            if path not in at_b:
                module = parse_module(reader.show(root, b, path))
                at_b[path] = top_units(module) if module is not None else {}
            units = at_b[path]
            site = enclosing_unit(units, number)
            if path == rel and site == name and number == units[name][1]:
                continue
            site = site or os.path.basename(path)
        else:
            site = os.path.basename(path)
        if under_tests(path):
            tested = True
        elif site not in named:
            named.append(site)
    if not named:
        return [PYTEST_ONLY] if tested else [NO_SITE]
    return named + ([PYTEST] if tested else [])


def fix_table(reader, path):
    """{finding number: (word, value, note)} from the smith's `## Fixes`.

    `value` is the commit for `fixed`, the grounds for `answered`, the home
    for `deferred`; `note` is what stood beside the commit, if anything.
    Refused: a row whose `#` names no number or names one twice, a verdict
    outside the three, a `fixed` whose third cell names no commit, an
    `answered` with no grounds, a `deferred` with no home.
    """
    text = read_text(path, "fix table")
    raw, lines = text.splitlines(), reader.readable(text)
    out = {}
    for i, cells in table_body(reader, lines, FIXES, FIXES_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        if len(seen) < len(FIXES_HEADER):
            raise Refused(f"a fix row has {len(seen)} cells: {raw[i].strip()!r}")
        m = NUMBER_RE.search(seen[0])
        if not m:
            raise Refused(f"a fix row's `#` names no finding: {seen[0]!r}")
        number = int(m.group())
        if number in out:
            raise Refused(f"the fix table has two rows for finding {number}")
        verdict = chain.EMPHASIS.sub("", seen[1]).strip().rstrip(".").strip()
        word, third = verdict.lower(), seen[2].strip()
        if word == FIXED:
            sha = chain.SHA_RE.search(third)
            if not sha:
                raise Refused(
                    f"finding {number} is `{FIXED}` and its third cell names no "
                    f"commit: {third!r}. A fix is a commit somebody can open"
                )
            note = (third[: sha.start()] + third[sha.end() :]).strip(chain.SEPARATORS)
            out[number] = (FIXED, sha.group(), note)
        elif word == ANSWERED:
            if not third:
                raise Refused(
                    f"finding {number} is `{ANSWERED}` with no grounds in its "
                    "third cell. An answer nobody can argue with is not one"
                )
            out[number] = (ANSWERED, third, "")
        elif word == DEFERRED_WORD or (
            word.startswith(DEFERRED_WORD)
            and word[len(DEFERRED_WORD)] in chain.SEPARATORS
        ):
            home = verdict[len(DEFERRED_WORD) :].strip(chain.SEPARATORS) or third
            if not home:
                raise Refused(
                    f"finding {number} is `{DEFERRED_WORD}` with no home. Write "
                    f"`{DEFERRED_WORD} #N` or `{DEFERRED_WORD} <path>` — a "
                    "deferral to nowhere is how *someone will look at it* "
                    "becomes nobody did"
                )
            out[number] = (DEFERRED_WORD, home, "")
        else:
            raise Refused(
                f"finding {number}'s verdict `{seen[1]}` is none of `{FIXED}`, "
                f"`{ANSWERED}`, `{DEFERRED_WORD} <home>` — the three a fix pass "
                "may hand over. A reviewer's words (`withdrawn`, `not a "
                "defect`) are the reviewer's to write"
            )
    return out


def verdict_rows(reader, lines):
    """{finding number: (index, cells)} for round N's verdict table."""
    out = {}
    for i, cells in table_body(reader, lines, VERDICTS, VERDICT_HEADER, True):
        seen = [reader.visible(c) for c in cells]
        m = NUMBER_RE.search(seen[NUMBER_COL]) if len(seen) > NUMBER_COL else None
        if not m:
            raise Refused(f"a verdict row's `#` names no number: {lines[i].strip()!r}")
        number = int(m.group())
        if number in out:
            raise Refused(f"the record has two verdict rows numbered {number}")
        out[number] = (i, cells)
    return out


def units_named_earlier(reader, earlier):
    """{unit: K} for every entry of every earlier record's `New units` row,
    the lowest round first, in the entry grammar the checker reads."""
    named = {}
    for k, path in earlier:
        text = read_text(path, f"earlier record round-{k}.md")
        value = chain.field(
            chain.table_rows(reader, reader.readable(text)), chain.NEW_UNITS
        )
        if value is None or chain.says_none(reader.visible(value)):
            continue
        for entry in reader.visible(value).split(";"):
            entry = chain.DEPTH_RE.sub("", entry)
            for arrow in chain.ARROWS:
                entry = entry.split(arrow)[0]
            name = chain.EMPHASIS.sub("", entry).strip()
            if name and name not in named:
                named[name] = k
    return named


def location_units(reader, root, a, text):
    """[(path or None, unit)] the `Location` cell of a finding names.

    A `path:line` is resolved to the top-level unit holding that line at
    `a`, the tree the fix started from. A bare identifier names a unit and
    no file, and the caller finds the file.
    """
    visible = reader.visible(text)
    out = []
    for m in LOCATION_UNIT_RE.finditer(visible):
        out.append((m.group(1), m.group(2)))
    for m in LOCATION_LINE_RE.finditer(visible):
        module = parse_module(reader.show(root, a, m.group(1)))
        unit = enclosing_unit(top_units(module), int(m.group(2))) if module else None
        if unit:
            out.append((m.group(1), unit))
    for m in IDENTIFIER_RE.finditer(visible):
        out.append((None, m.group(1)))
    return out


def depth_two(reader, root, a, rows, fixes, added, at_a, earlier):
    """`Refused` when a `fixed` finding sits inside a unit an earlier record's
    `New units` names and the range adds a unit in that finding's file.

    That is depth 2 — a unit added by the fix of a finding inside a unit an
    earlier fix pass created — and the rule refuses it at the keyboard,
    naming the unit, the finding, the record whose row names the parent,
    and the exit. Nothing has been written when this raises.
    """
    named = units_named_earlier(reader, earlier)
    if not named or not added:
        return
    for number, (word, _, _) in fixes.items():
        if word != FIXED:
            continue
        _i, cells = rows[number]
        location = cells[LOCATION_COL] if len(cells) > LOCATION_COL else ""
        for rel, unit in location_units(reader, root, a, location):
            if unit not in named:
                continue
            files = [rel] if rel else [f for f, units in at_a.items() if unit in units]
            for f in files:
                inside = [n for r, n in added if r == f]
                if not inside:
                    continue
                raise Refused(
                    f"{', '.join(f'`{n}`' for n in inside)} in {f} would be at "
                    f"depth 2: added by the fix of {reader.visible(cells[NUMBER_COL])}, "
                    f"whose Location `{reader.visible(location)}` is inside "
                    f"`{unit}`, a unit round-{named[unit]}.md's `{chain.NEW_UNITS}` "
                    "names. A fix pass may add a unit; that unit's fix may not, "
                    "because the fix is read by the round that follows and the "
                    "unit it added is read by nobody. The unit is "
                    f"{DEPTH_EXIT}; no cell was written"
                )


def field_index(reader, lines, label):
    """The index of the one `| label | … |` row, or `Refused`."""
    hits = [
        i
        for i, ln in enumerate(lines)
        for cells in [reader.split_row(ln)]
        if cells and len(cells) >= 2 and cells[0].strip() == label
    ]
    if len(hits) != 1:
        raise Refused(
            f"the record has {len(hits)} `| {label} | … |` rows and needs one"
        )
    return hits[0]


def close(args):
    """Apply the fix table, measure the surface, tick `Pass`, run the check.

    Every refusal comes before the write: the table is parsed, every `fixed`
    commit resolved and placed inside the range, the range measured and the
    depth walked, and only then is the record rewritten in one pass.
    """
    reader, routing, root, _item, rounds = where(args)
    target = os.path.join(rounds, f"round-{args.round}.md")
    if not os.path.isfile(target):
        raise Refused(f"{target} does not exist — `close` fills a record `new` wrote")
    a, b = parse_range(root, args.range)
    fixes = fix_table(reader, args.fixes)

    text = read_text(target, f"record round-{args.round}.md")
    raw, lines = text.splitlines(), reader.readable(text)
    rows = verdict_rows(reader, lines)
    unknown = sorted(n for n in fixes if n not in rows)
    if unknown:
        raise Refused(
            f"the fix table names finding{'s' if len(unknown) > 1 else ''} "
            f"{', '.join(map(str, unknown))}, not in round {args.round}'s verdict "
            f"table (which has {', '.join(map(str, sorted(rows)))})"
        )
    open_now = [
        n
        for n, (_i, cells) in rows.items()
        if chain.verdict_of([reader.visible(c) for c in cells], VERDICT_COL)
        not in chain.CLOSED_WORDS
    ]
    missing = [n for n in open_now if n not in fixes]
    if missing:
        raise Refused(
            f"finding{'s' if len(missing) > 1 else ''} {', '.join(map(str, missing))} "
            f"of round {args.round} left with no row in the fix table. Every open "
            f"finding takes a row — `{FIXED}`, `{ANSWERED}`, or "
            f"`{DEFERRED_WORD} <home>` — or the record stays open"
        )
    for number, (word, value, _note) in fixes.items():
        if word != FIXED:
            continue
        full = chain.resolves_to(root, value)
        if full is None:
            raise Refused(
                f"finding {number}'s commit `{value}` does not resolve in {root}"
            )
        if not chain.is_ancestor(root, full, b) or chain.is_ancestor(root, full, a):
            raise Refused(
                f"finding {number}'s commit `{value}` lies outside --range "
                f"{a[:7]}..{b[:7]}. A fix the range does not hold is a fix the "
                "surface below was not measured on"
            )

    paths = touched(root, a, b)
    changed, added, heuristic, at_a, at_b = measure(reader, root, a, b, paths)
    earlier = earlier_records(routing, rounds, args.round)
    depth_two(reader, root, a, rows, fixes, added, at_a, earlier)

    contract = surface_cell(
        chain.CONTRACT,
        [
            contract_entry(n, call_sites(reader, root, b, r, n, at_b))
            for r, n in changed
        ],
    )
    units = surface_cell(chain.NEW_UNITS, [units_entry(n, 1) for _r, n in added])
    gate = cell(BROAD_GATE, args.broad_gate) if args.broad_gate else None

    # Nothing above touched `raw`; everything below does, indices first and
    # the one insertion last.
    for number, (word, value, note) in fixes.items():
        i, _cells = rows[number]
        cells = reader.split_row(raw[i])
        while len(cells) <= GROUNDS_COL:
            cells.append("")
        old = cells[GROUNDS_COL].strip()
        if word == FIXED:
            cells[VERDICT_COL] = f"**{FIXED}** `{value}`"
            grounds = f"{FIXED_AT} {value}" + (f" {DASH} {note}" if note else "")
            cells[GROUNDS_COL] = grounds + (f"; {old}" if old else "")
        elif word == ANSWERED:
            cells[VERDICT_COL], cells[GROUNDS_COL] = ANSWERED, value
        else:
            cells[VERDICT_COL], cells[GROUNDS_COL] = f"{DEFERRED_WORD} {value}", value
        raw[i] = row([escape(c) for c in cells])
    words = [
        chain.verdict_of(
            [reader.visible(c) for c in reader.split_row(raw[i])], VERDICT_COL
        )
        for i, _ in rows.values()
    ]
    still_open = [w for w in words if w not in chain.CLOSED_WORDS]
    boxes = [i for i, ln in enumerate(lines) if chain.PASS_RE.match(ln)]
    if len(boxes) != 1:
        raise Refused(f"the record has {len(boxes)} `Pass` boxes and needs one")
    raw[boxes[0]] = f"- [{' ' if still_open else 'x'}] Pass"
    raw[field_index(reader, lines, chain.CONTRACT)] = contract
    last = field_index(reader, lines, chain.NEW_UNITS)
    raw[last] = units
    if gate is not None:
        raw[field_index(reader, lines, BROAD_GATE)] = gate
    if heuristic:
        while last + 1 < len(raw) and reader.split_row(raw[last + 1]) is not None:
            last += 1
        raw.insert(
            last + 1,
            f"<!-- {chain.NEW_UNITS}: {', '.join(heuristic)} {HEURISTIC_NOTE} -->",
        )

    ending = "\n" if text.endswith("\n") else ""
    with open(target, "w", encoding="utf-8") as f:
        f.write("\n".join(raw) + ending)
    counts = {
        w: sum(1 for word, _, _ in fixes.values() if word == w)
        for w in (FIXED, ANSWERED, DEFERRED_WORD)
    }
    print(
        f"round-record: closed {os.path.relpath(target, root)} {DASH} "
        + ", ".join(f"{n} {w}" for w, n in counts.items())
        + f"; {contract.strip('| ')}; {units.strip('| ')}"
    )
    return run_check(root, args.baseline or default_baseline(root))


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="round-record",
        description="Write a review round's record from the reviewer's report.",
    )
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("new", help="write rounds/round-N.md")
    p.add_argument("--item", required=True, help="the work item directory")
    p.add_argument("--round", required=True, type=int, metavar="N")
    p.add_argument("--target", required=True, help="the commit this round reviewed")
    p.add_argument("--report", required=True, help="the reviewer's report, a file")
    p.add_argument("--asked", required=True, help="the round paragraph, a file")
    p.add_argument("--ran-by", required=True, help="`<agent> on <model>`")
    p.add_argument("--broad-gate", default=None, help="the Broad gate cell")
    p.add_argument("--pr", default=None, help="the PR cell")
    p.add_argument("--root", default=None, help="the repository (default: the item's)")
    p.add_argument(
        "--baseline",
        default=None,
        help="the base for chain_check (default: the upstream, else origin/main)",
    )
    c = sub.add_parser("close", help="apply the fix table to rounds/round-N.md")
    c.add_argument("--item", required=True, help="the work item directory")
    c.add_argument("--round", required=True, type=int, metavar="N")
    c.add_argument(
        "--fixes", required=True, help=f"the smith's `{FIXES}` table, a file"
    )
    c.add_argument("--range", required=True, metavar="A..B", help="the fix commits")
    c.add_argument("--broad-gate", default=None, help="the Broad gate cell")
    c.add_argument("--root", default=None, help="the repository (default: the item's)")
    c.add_argument(
        "--baseline",
        default=None,
        help="the base for chain_check (default: the upstream, else origin/main)",
    )
    args = ap.parse_args(argv)
    try:
        return close(args) if args.command == "close" else new(args)
    except Refused as exc:
        print(f"round-record: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
