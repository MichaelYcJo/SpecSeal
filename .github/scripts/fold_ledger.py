#!/usr/bin/env python3
"""Fold each work item's ledger fragment into the release's own ledger file.

A work item writes its evidence rows to `seal/ledger/<work-item-id>.md` and
leaves `seal/ledger.md` alone, so two branches never queue at one file
(issue #46). Nothing ever folded the fragments back, so the directory gained
one file per work item forever and almost every pull request touched it
(issue #78). After the merge there is no branch left to queue, which is why
the rows fold rather than stay (`docs/one-root-by-lifetime.md`, "What happens
at a release", step 1).

**The layout** (#547). `seal/ledger.md` holds what is nobody's release: its
header, the coordinate notation and the rows from before the fragments
existed. A release's rows are `seal/releases/<X.Y.Z>.md`, one file per
release, and that file IS the section the fold used to append to the shared
file, byte for byte — first line `## X.Y.Z — <date>`, then each work item's
marker, `### <id>` heading and rows. Every reader of the ledger reads the
three addresses alike (`evidence_check.py#default_patterns`), so where a row
sits changes no row's status — the `ok` total counts a pair once per file,
so a move can change the count; the shared file stops growing, and a
re-stamp's diff lands in the file of the release the row belongs to. The
sections that were folded into `seal/ledger.md` before this layout move once,
at the release-preparation commit that ships it (`--split`, below).

This is the other half of that layout, the way `gather_changelog.py` is the
other half of the changelog fragments. Release preparation runs both, in the
same commit:

  fold_ledger.py --version 0.4.0            move the fragments into
                                            seal/releases/0.4.0.md
  fold_ledger.py --version 0.4.0 --dry-run  print the section, write nothing
  fold_ledger.py --check                    no fragment left, no open row,
                                            no release left in ledger.md,
                                            every release file named for the
                                            one version it heads once, no
                                            work item marked twice
  fold_ledger.py --split                    once: move every release section
                                            of ledger.md into its own file
  fold_ledger.py --split --dry-run          print what would move, write
                                            nothing

**The split runs once** (#547). `--split` cuts every `## X.Y.Z` section of
`seal/ledger.md` — from its heading to the next `## ` line or the end —
into `seal/releases/<X.Y.Z>.md` byte for byte, ending in one newline, and
leaves the header and the standing areas as `seal/ledger.md`. One kind of row
points INTO the shared file: an anchor `seal/ledger.md#"<locator>"@<hash>`
whose heading or line the split moves. Its content moves with the
file byte for byte, so the split rewrites the path to the release file and
keeps the hash — the class `hooks/root-migrate.py` rewrites for the root
move, and not a row whose content went (`CLAUDE.md`, *REMOVED, not
re-pointed*). The rewrite runs over the shared file, every release file and
every fragment, and reads a locator by the checker's own rule; an anchor
whose line or heading is in no section the split moved or kept, or stands in
more than one place so that only the row's hash could choose, is named and
left, for a person. The split refuses a version the ledger heads
twice (C's reader: joining two sections is a person's call), any target
that exists (a join is the fold's, and a file there before the split is a
state nobody planned), and a ledger with nothing to move.

**A second fold for one version joins its file** (#540). The release pull
request going red and a fragment landing after the preparation commit is the
ordinary shape, and the fold used to write a second `## X.Y.Z` heading for
it, below everything: `seal/ledger.md` headed `0.9.3` twice through the
seventeen ledger sections from `0.9.4` to `0.15.0` (eighteen tags after
`v0.9.3`; `0.13.2` folded no section). Where `seal/releases/X.Y.Z.md` already
exists, the new work items go at the end of it, the file keeps the first
fold's date over `--date` and over today, and `--dry-run` prints the heading
it joins. `--check` refuses a release file that heads a version twice, or one
not named for the version it heads, naming the lines — the same three answers
`gather_changelog.py` gives for `CHANGELOG.md` (#289). It also refuses a
`seal/ledger.md` that heads any release at all: after the split that is a fold
written to the old place or a split not run, and the refusal names `--split`
as the repair.

**A fold is a move, not a deletion.** Every table row of a fragment is copied
into the release file byte for byte, under a heading for the release and one
for the work item, and only then is the fragment removed. Nothing is written
until every fragment has been read, and nothing is removed until the release
file is on disk. `seal/ledger.md` is never written by a fold.

**A folded work item is marked, not matched.** Each section is written under
an HTML comment naming the work item, the same comment `gather_changelog.py`
writes in `CHANGELOG.md`. A fragment that turns up while its marker is already
in `ledger.md` or in any release file is refused rather than folded twice: the
same claim in the corpus twice, with no way to tell which is current, is
worse than a stop that names the work item and the file.

**A fragment's own leading marker line is dropped** (#553). `CLAUDE.md` says
a fragment needs no header, and twenty of them began with their own
`<!-- specs/<id> -->` line anyway; the fold wrote its marker in front and
copied the fragment whole, so each of the twenty stood twice in
`seal/ledger.md` and `--check` counted 118 work items over 98 folded
sections. `section()` drops a first line equal to the fragment's own marker,
the way `demote` drops its `# <id>` title, and `--check` refuses a marker
standing twice in `seal/ledger.md` or a release file, naming the file and
both lines. A marker quoted elsewhere in a fragment is text and is copied.

**The guard.** A sentence in a work item's `spec.md` that must outlive the
release has to have moved into a `docs/` policy or a ledger row before the
merge, and `seal/specs/<id>/evidence-todo.md` is where a reviewer lists the facts
still waiting for the ledger. So the fold refuses to run while any such file
in the tree has an open row, naming the file, and writes nothing (step 3 of
the same section). What an open row is:

  1. a file that does not exist has no open row;
  2. a line outside a table whose first word is `drained` closes the whole
     file, but only on a live line — one quoted in a fence, an HTML comment
     or a code span closes nothing;
  3. otherwise every table body row is open unless its first cell begins
     with a check mark (✅) — a header and its separator are not body rows,
     and a row inside a fenced block that closes is an example;
  4. a file with a header and no body row is not open.

The rule is `skills/verify/scripts/unverified_check.py#todo_open_rows`, which
this script loads rather than copies (#487), and whose docstring says why the
two halves read by opposite rules.

Every `seal/specs/*/evidence-todo.md` in the tree is read. The step runs on a
branch cut from the release branch, which holds merged work only, so "every
released work item" and "every work item present" are the same set.

**A new release is a new file**, where the changelog gather inserts at the
top of one file. A changelog is read newest-first; a ledger is read by area
and by coordinate. The checker (`evidence_check.py`) scans a ledger for
anchors and reads no headings, so nothing measures from where a row sits.

Exit codes: 0 done · 1 for nothing to fold, an open evidence-todo row, a
fragment whose marker is already in a ledger, a release file that does not
head the version it is named for, a fragment left at `--check`, a release
heading left in `seal/ledger.md` at `--check`, a release file headed twice or
misnamed at `--check`, a marker standing twice in any ledger at `--check`, a
`--split` refused (a version headed twice, a target that exists, nothing to
move), or a missing `seal/ledger.md`. Every one is a failure a release pull request
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
# what the tests and a person read; `ntpath.join` would print `seal\ledger`
# (round 1, 🔴 1). Disk paths are built from them through `under()`.
LEDGER = "seal/ledger.md"
FRAGMENTS = "seal/ledger"
RELEASES = "seal/releases"

HEADING_RE = re.compile(r"^(#{1,6})(\s)")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
VERSION_HEADING_RE = re.compile(r"^## (\d+\.\d+\.\d+)\b")
SEPARATOR_RE = re.compile(r"^\|(\s*:?-+:?\s*\|)+\s*$")
MARKER_LINE_RE = re.compile(r"^<!-- specs/\S+ -->$", re.M)


def under(root, rel):
    """The disk path of a `/`-joined repository-relative path."""
    return os.path.join(root, *rel.split("/"))


def release_path(version):
    """The `/`-joined path of one release's ledger file (#547)."""
    return f"{RELEASES}/{version}.md"


def version_key(name):
    """Sort key: releases in version order, anything else after, by name."""
    return (
        (0, tuple(int(n) for n in name.split(".")))
        if VERSION_RE.match(name)
        else (1, name)
    )


def release_files(root):
    """`[(name, path, text)]` for every `seal/releases/*.md`, in version order.

    The name is the file's, read off the file name and not off its heading:
    `--check` is what holds the two together, and a reader that trusted the
    heading would file a misnamed release under the wrong version silently.
    """
    out = []
    for disk in glob.glob(os.path.join(under(root, RELEASES), "*.md")):
        name = os.path.basename(disk)[: -len(".md")]
        with open(disk, encoding="utf-8") as f:
            out.append((name, release_path(name), f.read()))
    return sorted(out, key=lambda entry: version_key(entry[0]))


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
    """[(work item id, text)] for every `seal/ledger/*.md`, in id order.

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


def folded(ledgers, frags):
    """`[(work item id, text, ledger path)]` for every fragment whose marker
    already stands, on a line of its own, in one of `ledgers` — `[(path,
    text)]`: `seal/ledger.md` and every release file (#547). The path is
    what the refusal names, because a person comparing by hand has to know
    which file to open."""
    out = []
    for work_item_id, text in frags:
        for path, ledger_text in ledgers:
            if is_marked(ledger_text, work_item_id):
                out.append((work_item_id, text, path))
                break
    return out


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
        # Verified 2026-09-08 against demote@8f967708.
        elif fence is not None and head.startswith(fence):
            fence = None
        m = None if fence else HEADING_RE.match(line)
        if m:
            line = "#" * min(len(m.group(1)) + 2, 6) + line[len(m.group(1)) :]
        out.append(line)
    return "\n".join(out).strip("\n")


def own_marker_dropped(text, work_item_id):
    """The fragment without a first line that is its own marker (#553).

    Blank lines above it are skipped the way `demote` skips them above the
    title, and only the FIRST non-blank line is asked: a marker quoted later
    in the fragment is the fragment's text. The blank lines under a dropped
    marker go with it, or the section would open on a blank.
    """
    lines = text.split("\n")
    at = 0
    while at < len(lines) and not lines[at].strip():
        at += 1
    if at < len(lines) and lines[at].strip() == marker(work_item_id):
        at += 1
        while at < len(lines) and not lines[at].strip():
            at += 1
        return "\n".join(lines[at:])
    return text


def doubled_markers(ledgers):
    """`[(work item id, [(path, line number)])]` for every work item whose
    marker stands on a line of its own more than once across `ledgers` —
    `[(path, text)]`, the shared file and every release file (#553).

    Across the corpus rather than per file, because both shapes are one
    defect: a work item marked twice in one file (the fragment that began
    with its own marker) and one marked in two files (a fold to the old
    place after the split) both make the count say one work item is two.
    `tests/test_release_hygiene.py#duplicated_markers` is the same reader
    over the real tree on every pull request.
    """
    where = {}
    for path, text in ledgers:
        for number, line in enumerate(text.split("\n"), 1):
            found = MARKER_LINE_RE.match(line)
            if found:
                where.setdefault(
                    found.group(0)[len("<!-- specs/") : -len(" -->")], []
                ).append((path, number))
    return [(work_item_id, at) for work_item_id, at in where.items() if len(at) > 1]


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
        body = demote(own_marker_dropped(text, work_item_id), work_item_id)
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


def section_heading(ledger_text, version):
    """The match for the `## <version>` line the ledger already has, or None.

    The one predicate for *is there a section*, asked by `main` for the date
    and the heading it prints and by `insert` when it places the work items
    — `gather_changelog.py#section_heading`, name for name, so a reader of
    one script knows the other. Group 1 is the date the heading carries, or
    None where it carries none.
    """
    return re.compile(rf"^## {re.escape(version)}\b(?: — (\S+))?.*$", re.M).search(
        ledger_text
    )


def insert(ledger_text, block, version):
    """Into the section `version` already heads, or below everything (#540).

    Where the ledger already heads `version`, `block`'s heading is dropped
    and its work items go at the end of that section, before the next `## `,
    with one blank line each side: the section is one release however many
    folds wrote it, and `--check` refuses a file that heads a version twice,
    so this arm is the one a red release pull request has to take. The
    section is normally the last `## ` in the file, and the walk to the next
    heading is what keeps an area appended later from breaking the join.

    Lines are split on `\\n` alone, as `demote` splits them: `splitlines()`
    also breaks a row on U+2028, and a row the first fold moved byte for
    byte would leave the second fold as two lines.
    """
    found = section_heading(ledger_text, version)
    if found is None:
        return append(ledger_text, block)
    lines = ledger_text.split("\n")
    at = ledger_text.count("\n", 0, found.start())
    end = next(
        (n for n in range(at + 1, len(lines)) if lines[n].startswith("## ")),
        len(lines),
    )
    while end > at + 1 and not lines[end - 1].strip():
        end -= 1
    # `section()` writes the heading, a blank line, then the work items; the
    # heading is the file's already and the blank line is re-added. The
    # tail's own blank lines go too, or the one re-added here joins them.
    entries = block.rstrip("\n").split("\n")[2:]
    tail = lines[end:]
    while tail and not tail[0].strip():
        tail.pop(0)
    joined = "\n".join([*lines[:end], "", *entries, "", *tail])
    return joined.rstrip("\n") + "\n"


def version_headings(text):
    """`[(version, [line numbers])]` for every version a `## ` line heads.

    The one reader of `## X.Y.Z` lines (#547, Q3). `--check` asks it of
    `seal/ledger.md`, where any answer is a release left in the shared file,
    and of each release file, where the answer has to be the file's own
    version once; `--split` asks it for the sections to move.
    """
    lines = {}
    for number, line in enumerate(text.split("\n"), 1):
        found = VERSION_HEADING_RE.match(line)
        if found:
            lines.setdefault(found.group(1), []).append(number)
    return list(lines.items())


def doubled_versions(text):
    """`[(version, [line numbers])]` for every version `## ` heads twice.

    `tests/test_release_hygiene.py#duplicated_version_headings` is the same
    reader over the real tree on every pull request; this one is `--check`'s,
    at the release, and is spelled here because a script cannot import a
    test. `version_headings` filtered (#547).
    """
    return [(version, at) for version, at in version_headings(text) if len(at) > 1]


def misnamed(name, text):
    """Why a release file is not the one version its name says, or None.

    A release file heads exactly the version it is named for, once: the name
    is what the fold and every reader key on, and the heading is what a
    person reads. Two spellings of one fact, held together here.
    """
    headed = version_headings(text)
    if not VERSION_RE.match(name):
        return "is not named X.Y.Z"
    if not headed:
        return "heads no version"
    if len(headed) > 1 or len(headed[0][1]) > 1:
        lines = ", ".join(str(n) for _, at in headed for n in at)
        versions = ", ".join(v for v, _ in headed)
        return f"heads {versions} at lines {lines} — one release, one file"
    version, at = headed[0]
    if version != name:
        return f"heads {version} at line {at[0]}"
    return None


# An anchor whose path is exactly `seal/ledger.md`, with a quoted locator and
# the `@hash` every coordinate carries (`evidence_check.py#ANCHOR_RE`). The
# look-behind keeps `x/seal/ledger.md` — some other file — out; the
# look-ahead keeps a backticked mention with no hash out, and makes the
# locator backtrack over an escaped `\"` rather than stop at its backslash.
SELF_ANCHOR_RE = re.compile(
    r'(?<![A-Za-z0-9_.@/-])seal/ledger\.md#"((?:[^"\n]|\\")+)"'
    r'(?=(?:>"(?:[^"\n]|\\")+")?@[0-9a-f]{6,12})'
)
HEADING_SEP = " / "  # `evidence_check.py#HEADING_SEP`


def release_sections(text):
    """`[(version, start, end)]`, 0-based `[start, end)` line ranges of every
    `## X.Y.Z` section: from its heading to the next `## ` line or the end."""
    lines = text.split("\n")
    out = []
    for n, line in enumerate(lines):
        found = VERSION_HEADING_RE.match(line)
        if found:
            end = next(
                (k for k in range(n + 1, len(lines)) if lines[k].startswith("## ")),
                len(lines),
            )
            out.append((found.group(1), n, end))
    return out


def body_rows(lines):
    """Table body rows: `| ` lines that are not a header over a separator."""
    rows = 0
    for n, line in enumerate(lines):
        if not line.startswith("| "):
            continue
        following = lines[n + 1].strip() if n + 1 < len(lines) else ""
        if not SEPARATOR_RE.match(following):
            rows += 1
    return rows


def rewrite_self_anchors(text, moved, kept):
    """`(text, rewritten, left)` — every `seal/ledger.md#"<locator>"@<hash>`
    whose target is in `moved` (`{line: version}`) points at that release's
    file, hash untouched. The target is read by the checker's rule
    (`evidence_check.py#resolve_unit`): the first part of a heading path when
    that part is a heading, the one whole line otherwise. An anchor whose
    line or heading is in no section the split moved or kept is `left`: the
    split cannot say where it points, so a person does. `split` leaves a
    line out of both maps when it stands in more than one place, so such an
    anchor is `left` too. `rewritten` is
    `[(old, new, line)]`, the line of that anchor's own occurrence — a
    rewrite adds no newline, so a line in `text` is the same line after."""
    rewritten, left = [], []

    def one(match):
        body = match.group(1).replace('\\"', '"').replace("\\|", "|")
        parts = [p for p in body.split(HEADING_SEP) if p.strip()]
        if parts and HEADING_RE.match(parts[0].strip()):
            first = " ".join(parts[0].split())
        else:
            first = " ".join(body.split())
        version = moved.get(first)
        if version is None:
            if first not in kept:
                left.append(match.group(0))
            return match.group(0)
        new = f'{release_path(version)}#"{match.group(1)}"'
        line = text.count("\n", 0, match.start()) + 1
        rewritten.append((match.group(0), new, line))
        return new

    return SELF_ANCHOR_RE.sub(one, text), rewritten, left


def split(root, text, dry_run):
    """`--split`. Returns the exit code; prints what moved or would."""
    doubled = doubled_versions(text)
    if doubled:
        print(f"{LEDGER} heads a version twice — one release, one file:")
        for version, at in doubled:
            print(f"  {version}  at lines {', '.join(str(n) for n in at)}")
        print(
            "\nMove the later heading's work items under the first heading and "
            f"delete the later one, then split.\nnothing split: {LEDGER} is untouched"
        )
        return 1
    sections = release_sections(text)
    if not sections:
        print(f"nothing to split: {LEDGER} heads no release")
        return 1
    present = [
        release_path(v)
        for v, _, _ in sections
        if os.path.exists(under(root, release_path(v)))
    ]
    if present:
        print("release files that already exist — the split writes new files only:")
        for path in present:
            print(f"  {path}  exists")
        print(
            "\nA release file before the split is a state nobody planned; compare "
            f"it with its section by hand.\nnothing split: {LEDGER} is untouched"
        )
        return 1

    lines = text.split("\n")
    inside = set()
    moved = {}
    files = {}
    for version, start, end in sections:
        inside.update(range(start, end))
        body = lines[start:end]
        files[release_path(version)] = "\n".join(body).rstrip("\n") + "\n"
        # Every non-blank line, not headings only: a line anchor into a
        # moved section moves with it exactly as a heading does.
        for line in body:
            key = " ".join(line.split())
            if key:
                moved[key] = None if key in moved else version
    twice = {k for k, v in moved.items() if v is None}
    moved = {k: v for k, v in moved.items() if v is not None}
    rest = [line for n, line in enumerate(lines) if n not in inside]
    kept = {" ".join(line.split()) for line in rest if line.strip()}
    # A line that stands in more than one place is several places to the
    # checker, and the row's own hash picks between them
    # (`evidence_check.py#check_text`). The split reads no hash, so an anchor
    # to such a line is named for a person rather than moved or kept by guess.
    both = (kept & moved.keys()) | (kept & twice)
    moved = {k: v for k, v in moved.items() if k not in both}
    kept -= both
    files[LEDGER] = "\n".join(rest).rstrip("\n") + "\n"
    # Every other ledger an anchor can stand in: release files from before,
    # and fragments. The split's own files are rewritten with them.
    for _, path, body in release_files(root):
        files.setdefault(path, body)
    for work_item_id, body in fragments(root):
        files[f"{FRAGMENTS}/{work_item_id}.md"] = body
    rewrites, lefts = [], []
    for path in list(files):
        new, rewritten, left = rewrite_self_anchors(files[path], moved, kept)
        if new != files[path]:
            files[path] = new
        for old, fresh, number in rewritten:
            rewrites.append((path, number, old, fresh.split("#", 1)[0]))
        lefts += [(path, anchor) for anchor in left]

    verb = "would move" if dry_run else "moved"
    print(f"{verb} {len(sections)} release sections out of {LEDGER}:")
    for version, start, end in sections:
        last = end
        while last > start + 1 and not lines[last - 1].strip():
            last -= 1
        rows = body_rows(lines[start:end])
        print(
            f"  {version}  lines {start + 1}-{last}  -> {release_path(version)}  "
            f"({rows} row{'' if rows == 1 else 's'})"
        )
    verb = "would rewrite" if dry_run else "rewrote"
    print(
        f"{verb} {len(rewrites)} anchor{'' if len(rewrites) == 1 else 's'} into a moved section:"
    )
    for path, number, old, target in rewrites:
        print(f"  {path}:{number}  {old} -> {target}")
    if lefts:
        print(
            "anchors into seal/ledger.md the split could not place — open them by hand:"
        )
        for path, anchor in lefts:
            print(f"  {path}  {anchor}")
    if dry_run:
        print("nothing written")
        return 0
    # The release files first and the shared file last: an interruption
    # leaves every row in the shared file still, and the next split refuses
    # on the files it already wrote rather than losing a section.
    os.makedirs(under(root, RELEASES), exist_ok=True)
    for path, body in sorted(files.items(), key=lambda item: item[0] == LEDGER):
        with open(under(root, path), "w", encoding="utf-8") as f:
            f.write(body)
    return 0


# The open-rows rule is the shipped one, loaded by path the way
# `.github/scripts/rider_check.py` loads the shipped checker (#487). This file
# used to keep a copy on the ground that release automation may not depend on
# a shipped script, and nothing held the two in step; `rider_check.py` had
# already taken that direction. A reader that is moved or renamed stops the
# fold at load with a traceback, at the release, which is the loud direction.
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")


def load_reader(path=READER):
    """`unverified_check.py` as a module."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_unverified_reader", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# `unverified_check.py#todo_open_rows`, the one rule, under the name this
# script's callers and cases already use.
open_rows = load_reader().todo_open_rows


def open_items(root):
    """[(relative path, open row count)] for every evidence-todo file with one."""
    out = []
    for path in sorted(
        glob.glob(os.path.join(under(root, "seal/specs"), "*", "evidence-todo.md"))
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
        help="report fragments left in seal/ledger/, open evidence-todo "
        "rows, a release left in seal/ledger.md, a release file not "
        "named for the one version it heads once and a marker standing "
        "twice, and exit 1",
    )
    ap.add_argument(
        "--split",
        action="store_true",
        help="once: move every release section of seal/ledger.md into "
        "seal/releases/<X.Y.Z>.md and rewrite the anchors into them",
    )
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--root", default=ROOT, help="repository root (default: this one)")
    args = ap.parse_args(argv)

    if sum(bool(a) for a in (args.check, args.version, args.split)) != 1:
        ap.error("pass one of --version to fold, --check to verify, --split to move")

    root = os.path.abspath(args.root)
    ledger = under(root, LEDGER)
    if not os.path.isfile(ledger):
        print(f"{LEDGER} is not there — not a ledger root, nothing folded")
        return 1
    with open(ledger, encoding="utf-8") as f:
        text = f.read()
    if args.split:
        return split(root, text, args.dry_run)
    releases = release_files(root)
    ledgers = [(LEDGER, text), *[(path, body) for _, path, body in releases]]
    frags = fragments(root)
    already = folded(ledgers, frags)
    items = open_items(root)

    if args.check:
        bad = False
        if frags:
            bad = True
            print(f"ledger fragments that never folded into {RELEASES}/:")
            marked = {i: path for i, _, path in already}
            for work_item_id, _ in frags:
                line = f"  {FRAGMENTS}/{work_item_id}.md"
                if work_item_id in marked:
                    line += f"  (its marker is already in {marked[work_item_id]} — compare by hand)"
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
        headed = version_headings(text)
        if headed:
            # A release's rows are its own file (#547). A section standing
            # in the shared file is a fold written to the old place, or the
            # one-time split not run; either way the repair is the split.
            bad = True
            if frags or items:
                print()
            print(
                f"{LEDGER} still heads a release — a release's rows live in "
                f"{RELEASES}/<X.Y.Z>.md:"
            )
            for version, at in headed:
                for number in at:
                    print(f"  {version}  at line {number}")
            print(
                "\nRun once, at the release-preparation commit "
                "(its --dry-run first):\n"
                "  python3 .github/scripts/fold_ledger.py --split"
            )
        wrong = [(path, misnamed(name, body)) for name, path, body in releases]
        wrong = [(path, why) for path, why in wrong if why]
        if wrong:
            # A second fold for one version joins its file now (#540); a
            # heading standing twice is a fold from before, or a hand edit,
            # and a file not named for what it heads is one nothing reads
            # under the right version.
            bad = True
            if frags or items or headed:
                print()
            print("release files that are not the one version their name says:")
            for path, why in wrong:
                print(f"  {path}  {why}")
            print(
                "\nA release file heads exactly the version it is named for, "
                "once: rename it, or move a later heading's work items under "
                "the first and delete the later one"
            )
        twice = doubled_markers(ledgers)
        if twice:
            # A fragment that began with its own marker line used to be
            # folded with it (#553); a marker standing twice now is a fold
            # from before, or a hand edit.
            bad = True
            if frags or items or headed or wrong:
                print()
            print("a marker stands twice — one work item, one marker:")
            for work_item_id, at in twice:
                places = ", ".join(f"{path}:{n}" for path, n in at)
                print(f"  {work_item_id}  at {places}")
            print(
                "\nKeep the marker above the work item's `### ` heading; delete "
                "the other line and the blank line under it"
            )
        if bad:
            return 1
        # Markers on a line of their own. The ledger's own header quotes the
        # marker's shape inline, and a bare substring count read that as a
        # work item (measured: 7 where 6 had been folded).
        marked = sum(len(MARKER_LINE_RE.findall(body)) for _, body in ledgers)
        files = len(releases)
        print(
            f"no ledger fragment left in {FRAGMENTS}/; "
            f"{marked} work items marked across {LEDGER} and "
            f"{files} release file{'' if files == 1 else 's'}; "
            "no open evidence-todo row"
        )
        return 0

    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        ap.error(f"--version must be X.Y.Z, not {args.version!r}")

    target = release_path(args.version)
    disk = under(root, target)
    existing = None
    if os.path.isfile(disk):
        with open(disk, encoding="utf-8") as f:
            existing = f.read()

    if items:
        report_open(items)
        print(f"\nnothing folded: {RELEASES}/ and {FRAGMENTS}/ are untouched")
        return 1

    if already:
        print("fragments whose marker is already in a ledger:")
        for work_item_id, _, path in already:
            print(f"  {FRAGMENTS}/{work_item_id}.md  (in {path})")
        print(
            "\nFolding one twice would put the same rows in the corpus twice. "
            "Compare the fragment against its folded section by hand, then "
            f"remove the fragment.\nnothing folded: {RELEASES}/ is untouched"
        )
        return 1

    if existing is not None and section_heading(existing, args.version) is None:
        # A file at the release's path that does not head the release is a
        # tree a person should look at; joining it would put the rows under
        # a heading nobody looks for. `--check` refuses the same file.
        print(
            f"{target} exists and does not head {args.version} — a release "
            "file is the section it is named for, first line "
            f"`## {args.version} — <date>`.\nnothing folded: {RELEASES}/ and "
            f"{FRAGMENTS}/ are untouched"
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
    # The heading a reader sees is the file's own where the file exists —
    # dated or not — and the block's only where this run writes one. The
    # date a joined file keeps is the first fold's, because `insert` drops
    # the block's heading and this line prints the file's (#540); a `date`
    # override here was measured dead by mutation and is not kept.
    found = section_heading(existing, args.version) if existing else None
    heading = found.group(0) if found else block.split("\n")[0]
    if args.dry_run:
        if found:
            print("appending into the existing file:\n")
        print("\n".join([heading, *block.split("\n")[1:]]))
        for work_item_id in empty:
            print(f"(empty, would be removed) {FRAGMENTS}/{work_item_id}.md")
        return 0

    if len(empty) < len(frags):
        # A new release is a new file; a second fold for one release joins
        # its file through C's `insert`, whose walk to the next `## ` reaches
        # EOF because the file is the section (#547). `seal/ledger.md` is
        # never written here.
        written = insert(existing, block, args.version) if found else block
        os.makedirs(under(root, RELEASES), exist_ok=True)
        with open(disk, "w", encoding="utf-8") as f:
            f.write(written.rstrip("\n") + "\n")
    # Removed only after the release file is on disk, so a failed write
    # leaves every fragment where it was.
    for work_item_id, _ in frags:
        os.remove(under(root, f"{FRAGMENTS}/{work_item_id}.md"))
    try:
        os.rmdir(under(root, FRAGMENTS))
    except OSError:
        pass  # something else is in it, or it is already gone; both are fine
    moved = len(frags) - len(empty)
    print(
        f"folded {moved} fragments into {target} under {heading}"
        + (" (appended into the existing file)" if found else "")
    )
    for work_item_id, _ in frags:
        note = "  (empty, removed)" if work_item_id in empty else ""
        print(f"  {FRAGMENTS}/{work_item_id}.md{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
