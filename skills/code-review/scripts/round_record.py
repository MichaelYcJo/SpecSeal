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


def table_of(reader, raw, lines, heading, header, required):
    """The rows under `heading` as raw lines, header and separator first.

    The header has to be the record's own, cell for cell: a table whose
    columns differ is one the checker's column lookup reads differently, and
    copying it would put the difference in the record. Returns None when the
    section is absent and not required.
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
    out = [row(header), separator(len(header))]
    for i, cells in rows[1:]:
        if reader.is_separator([reader.visible(c) for c in cells]):
            continue
        out.append(raw[i].strip())
    return out


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


def new(args):
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
    args = ap.parse_args(argv)
    try:
        return new(args)
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
