#!/usr/bin/env python3
"""Fold each work item's ledger fragment into the gathered ledger.

A work item writes its evidence rows to `.specseal/map/<work-item-id>.md` and
leaves `.specseal/map.md` alone, so two branches never queue at one file
(issue #46). Nothing ever folded the fragments back, so the directory gained
one file per work item forever and almost every pull request touched it
(issue #78). After the merge there is no branch left to queue, which is why
the rows fold rather than stay (`docs/one-root-by-lifetime.md`, "What happens
at a release", step 1).

This is the other half of that layout, the way `gather_changelog.py` is the
other half of the changelog fragments. Release preparation runs both, in the
same commit:

  fold_ledger.py --version 0.4.0            move the fragments into map.md
  fold_ledger.py --version 0.4.0 --dry-run  print the section, write nothing
  fold_ledger.py --check                    no fragment left, no open row

**A fold is a move, not a deletion.** Every table row of a fragment is copied
into `map.md` byte for byte, under a heading for the release and one for the
work item, and only then is the fragment removed. Nothing is written until
every fragment has been read, and nothing is removed until the ledger has
been written.

**A folded work item is marked, not matched.** Each section is written under
an HTML comment naming the work item, the same comment `gather_changelog.py`
writes in `CHANGELOG.md`. A fragment that turns up while its marker is already
in `map.md` is refused rather than folded twice: the same claim in the file
twice, with no way to tell which is current, is worse than a stop that names
the work item.

**The guard.** A sentence in a work item's `spec.md` that must outlive the
release has to have moved into a `docs/` policy or a ledger row before the
merge, and `specs/<id>/evidence-todo.md` is where a reviewer lists the facts
still waiting for the ledger. So the fold refuses to run while any such file
in the tree has an open row, naming the file, and writes nothing (step 3 of
the same section). What an open row is:

  1. a file that does not exist has no open row;
  2. a line outside a table whose first word is `drained` closes the whole
     file, wherever it stands;
  3. otherwise every table body row is open unless its first cell begins
     with a check mark (✅) — a header and its separator are not body rows;
  4. a file with a header and no body row is not open.

Every `specs/*/evidence-todo.md` in the tree is read. The step runs on a
branch cut from the release branch, which holds merged work only, so "every
released work item" and "every work item present" are the same set.

**The section is appended**, where the changelog gather inserts at the top.
A changelog is read newest-first; a ledger is read by area and by coordinate,
and its top holds the notation a reader needs before any row. The checker
(`evidence_check.py`) scans a ledger for anchors and reads no headings, so
nothing measures from where a row sits.

Exit codes: 0 done · 1 for nothing to fold, an open evidence-todo row, a
fragment whose marker is already in the ledger, a fragment left at `--check`,
or a missing `.specseal/map.md`. Every one is a failure a release pull request
should stop on.
"""

import argparse
import datetime
import glob
import os
import re
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hooks")
)
import console

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# `/`-joined on every platform, because these are what the messages print and
# what the tests and a person read; `ntpath.join` would print `.specseal\map`
# (round 1, 🔴 1). Disk paths are built from them through `under()`.
LEDGER = ".specseal/map.md"
FRAGMENTS = ".specseal/map"

HEADING_RE = re.compile(r"^(#{1,6})(\s)")
SEPARATOR_RE = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
DRAINED_RE = re.compile(r"^[\s*_]*drained\b", re.IGNORECASE)
MARKER_LINE_RE = re.compile(r"^<!-- specs/\S+ -->$", re.M)


def under(root, rel):
    """The disk path of a `/`-joined repository-relative path."""
    return os.path.join(root, *rel.split("/"))


def marker(work_item_id):
    """The comment that says this work item's rows are in the ledger."""
    return f"<!-- specs/{work_item_id} -->"


def is_marked(ledger_text, work_item_id):
    """Whether the ledger carries this work item's marker on a line of its own.

    A substring test would read the marker's shape quoted in the ledger's own
    prose as a folded work item and refuse the fold, with advice that would
    have a person remove the only copy of the rows (round 1, 🟡 3). One
    line-anchored test serves the fold and `--check` alike.
    """
    return re.search(rf"^{re.escape(marker(work_item_id))}$", ledger_text, re.M)


def fragments(root):
    """[(work item id, text)] for every `.specseal/map/*.md`, in id order.

    The id is unix seconds, so sorting by it is chronological and stable: the
    same input always produces the same section, which is what makes a re-run
    comparable to the run before it. The text is returned whole, blank or
    not; `section()` decides what an empty one becomes.
    """
    out = []
    for path in glob.glob(os.path.join(under(root, FRAGMENTS), "*.md")):
        work_item_id = os.path.basename(path)[: -len(".md")]
        with open(path, encoding="utf-8") as f:
            out.append((work_item_id, f.read()))
    return sorted(out)


def folded(ledger_text, frags):
    """The fragments whose marker is already in the ledger, on its own line."""
    return [(i, text) for i, text in frags if is_marked(ledger_text, i)]


def demote(text, work_item_id):
    """The fragment's body as it goes under the work item's `###` heading.

    The fragment's own `# <id>` title is dropped, because the heading above
    the body already carries it; every other heading moves down two levels
    so a fragment's `## area` becomes `#### area` under the work item. Only
    heading lines outside tables and code fences are touched, and only their
    `#` prefix: every other line is copied byte for byte.

    Byte for byte means three things `str` methods do not (round 1, 🟡 5):
    lines are split on `\\n` alone, because `splitlines()` also breaks a row
    on U+2028; only newlines are stripped at either end, because `strip()`
    would take the last row's trailing whitespace; and a `#` line inside a
    code fence is text, not a heading.

    Two more from round 2 (🟡 4): blank lines above the title are skipped, so
    a title after one is still recognised rather than demoted into a second
    `### <id>`; and a fence is ``` or ~~~, closed by the next line that
    starts with the same three characters. That is looser than CommonMark,
    which closes only on a run at least as long as the opener with nothing
    after it; the rider below says what that misreads.
    """
    lines = text.strip("\n").split("\n")
    while lines and not lines[0].strip():
        lines = lines[1:]
    if lines and lines[0].strip() == f"# {work_item_id}":
        lines = lines[1:]
    out = []
    fence = None
    for line in lines:
        head = line.lstrip()
        if fence is None and (head.startswith("```") or head.startswith("~~~")):
            fence = head[:3]
        # RIDER: a ```python line, or a ``` line inside a ```` block, closes
        # the fence here and CommonMark says neither does — so a `#` line
        # after one is demoted where it should be copied. Round 3 of the work
        # item that wrote this measured it on probes and found no fence line
        # in any fragment or in map.md; a fold of today's ledger is untouched.
        # If a fragment ever quotes a fenced block, close on a run of the
        # same character at least as long as the opener with nothing after it
        # (`^(`{3,}|~{3,})(.*)$` and `len(run) >= len(fence) and not
        # rest.strip()`), and plant the case beside the tilde test.
        # Verified 2026-09-02 at 16c16c7.
        elif fence is not None and head.startswith(fence):
            fence = None
        m = None if fence else HEADING_RE.match(line)
        if m:
            line = "#" * min(len(m.group(1)) + 2, 6) + line[len(m.group(1)) :]
        out.append(line)
    return "\n".join(out).strip("\n")


def section(version, date, entries):
    """The release section, as it goes into the ledger.

    Returns the text and the ids of the fragments that were empty. An empty
    fragment gets no section — a marker with nothing under it would make
    `--check` say the work item's rows arrived when there were none — and is
    removed anyway, because a file holding nothing is not a row to preserve.
    """
    blocks = [f"## {version} — {date}", ""]
    empty = []
    for work_item_id, text in entries:
        body = demote(text, work_item_id)
        if not body.strip():
            empty.append(work_item_id)
            continue
        blocks.append(marker(work_item_id))
        blocks.append(f"### {work_item_id}")
        blocks.append("")
        blocks.append(body)
        blocks.append("")
    return "\n".join(blocks), empty


def append(ledger_text, block):
    """Below everything already in the ledger, separated by one blank line."""
    return ledger_text.rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n"


def open_rows(text):
    """Table body rows of an evidence-todo file that are still open.

    The rule, so a person can apply it by hand: a line outside a table whose
    first word is `drained` closes the whole file; otherwise every body row is
    open unless its first cell begins with ✅. A table is a run of lines
    starting with `|`; its first line is the header when the second is a
    separator, and neither is a body row.

    Split on `\\n` alone: `splitlines()` also breaks on U+2028, U+0085 and
    form feed, so a cell holding one of those followed by `drained` closed the
    file — the silent direction for a guard (round 1, 🟡 4).
    """
    lines = text.split("\n")
    rows = []
    n = 0
    while n < len(lines):
        line = lines[n]
        if not line.lstrip().startswith("|"):
            if DRAINED_RE.match(line):
                return []
            n += 1
            continue
        table = []
        while n < len(lines) and lines[n].lstrip().startswith("|"):
            table.append(lines[n])
            n += 1
        if len(table) >= 2 and SEPARATOR_RE.match(table[1].strip()):
            table = table[2:]
        for row in table:
            if SEPARATOR_RE.match(row.strip()):
                continue
            first = row.strip().strip("|").split("|", 1)[0].strip()
            if not first.startswith("✅"):
                rows.append(row)
    return rows


def open_items(root):
    """[(relative path, open row count)] for every evidence-todo file with one."""
    out = []
    for path in sorted(
        glob.glob(os.path.join(under(root, "specs"), "*", "evidence-todo.md"))
    ):
        with open(path, encoding="utf-8") as f:
            rows = open_rows(f.read())
        if rows:
            out.append((os.path.relpath(path, root).replace(os.sep, "/"), len(rows)))
    return out


def report_open(items):
    print("evidence-todo rows still open — a fact that never reached the ledger:")
    for rel, count in items:
        print(f"  {rel}  ({count} open row{'' if count == 1 else 's'})")
    print(
        "\nMerge each fact into the work item's ledger fragment and write "
        "`drained` above or below the table, or mark each merged row with ✅"
    )


def main(argv=None):
    console.to_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", help="the version being released, e.g. 0.4.0")
    ap.add_argument("--date", help="release date (default: today, UTC)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="report fragments left in .specseal/map/ and open evidence-todo "
        "rows, and exit 1",
    )
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--root", default=ROOT, help="repository root (default: this one)")
    args = ap.parse_args(argv)

    if not args.check and not args.version:
        ap.error("pass --version to fold, or --check to verify")

    root = os.path.abspath(args.root)
    ledger = under(root, LEDGER)
    if not os.path.isfile(ledger):
        print(f"{LEDGER} is not there — nothing to fold into")
        return 1
    with open(ledger, encoding="utf-8") as f:
        text = f.read()
    frags = fragments(root)
    already = folded(text, frags)
    items = open_items(root)

    if args.check:
        bad = False
        if frags:
            bad = True
            print(f"ledger fragments that never folded into {LEDGER}:")
            for work_item_id, _ in frags:
                line = f"  {FRAGMENTS}/{work_item_id}.md"
                if is_marked(text, work_item_id):
                    line += "  (its marker is already in the ledger — compare by hand)"
                print(line)
            print(
                "\nRelease preparation folds them:\n"
                "  python3 .github/scripts/fold_ledger.py --version X.Y.Z"
            )
        if items:
            bad = True
            if frags:
                print()
            report_open(items)
        if bad:
            return 1
        # Markers on a line of their own. The ledger's own header quotes the
        # marker's shape inline, and a bare substring count read that as a
        # work item (measured: 7 where 6 had been folded).
        marked = len(MARKER_LINE_RE.findall(text))
        print(
            f"no ledger fragment left in {FRAGMENTS}/; "
            f"{marked} work items marked in {LEDGER}; no open evidence-todo row"
        )
        return 0

    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        ap.error(f"--version must be X.Y.Z, not {args.version!r}")

    if items:
        report_open(items)
        print(f"\nnothing folded: {LEDGER} and {FRAGMENTS}/ are untouched")
        return 1

    if already:
        print(f"fragments whose marker is already in {LEDGER}:")
        for work_item_id, _ in already:
            print(f"  {FRAGMENTS}/{work_item_id}.md")
        print(
            "\nFolding one twice would put the same rows in the file twice. "
            "Compare the fragment against its folded section by hand, then "
            f"remove the fragment.\nnothing folded: {LEDGER} is untouched"
        )
        return 1

    if not frags:
        print(
            f"nothing to fold: {FRAGMENTS}/ holds no fragment. A release whose "
            "work items wrote no evidence rows is unusual — check that the "
            "branches you meant to ship are merged"
        )
        return 1

    date = args.date or datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    block, empty = section(args.version, date, frags)
    if args.dry_run:
        print(block)
        for work_item_id in empty:
            print(f"(empty, would be removed) {FRAGMENTS}/{work_item_id}.md")
        return 0

    if len(empty) < len(frags):
        with open(ledger, "w", encoding="utf-8") as f:
            f.write(append(text, block))
    # Removed only after the ledger is on disk, so a failed write leaves every
    # fragment where it was.
    for work_item_id, _ in frags:
        os.remove(under(root, f"{FRAGMENTS}/{work_item_id}.md"))
    try:
        os.rmdir(under(root, FRAGMENTS))
    except OSError:
        pass  # something else is in it, or it is already gone; both are fine
    moved = len(frags) - len(empty)
    print(f"folded {moved} fragments into {LEDGER} under ## {args.version} — {date}")
    for work_item_id, _ in frags:
        note = "  (empty, removed)" if work_item_id in empty else ""
        print(f"  {FRAGMENTS}/{work_item_id}.md{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
