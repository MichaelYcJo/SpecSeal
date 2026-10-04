#!/usr/bin/env python3
"""Gather each work item's changelog fragment into the release's own file.

Three branches ran in parallel on 2026-09-01 and touched 34 files between them.
They shared exactly one, and all three pairs shared the same one: the changelog
(issue #46). Nothing else overlapped at all — so parallel work was never the
problem, appending to one three-line region was.

The conflict itself is cheap and arrives at the worst possible moment: after
the broad gate has run and before the pull request opens, where nothing may be
edited. Resolving it costs a second run of the whole broad gate.

So a change writes `seal/specs/<work-item-id>/changelog.md` and leaves the
released notes alone. Two branches cannot collide, because no two work items
share an id. This script is the other half — release preparation runs it, and
it concatenates the fragments into `## X.Y.Z — <date>`.

**Each release is a file of its own** (#728, `docs/the-record-layout.md` §F2):
`changelog/X.Y.Z.md`, which opens with that `## X.Y.Z — <date>` line, and
`CHANGELOG.md` is the index — one copy of each release's heading line, newest
first, with a link to its file under it. The gather writes the release's file
and, where the index has no heading for the version yet, puts one above every
older one. A reader who wants one release opens one file.

  gather_changelog.py --version 0.2.0            write the release's file
  gather_changelog.py --version 0.2.0 --dry-run  print it, write nothing
  gather_changelog.py --check                    every fragment reached a file

**A gathered fragment is marked, not matched.** Each entry is written under an
HTML comment naming the work item it came from, and `--check` looks for that
comment. Matching a fragment's text against the file instead would work once
and then break for good: any copy-edit to a released entry would make its
fragment read as ungathered forever. The marker also earns its place twice —
it is the only link from a released entry back to the work that produced it.

Markdown comments do not render, so a reader never sees them.

**A marker counts only on a live line** (#584). One quoted in a fenced
example, a commented-out draft or a code span is text about the convention,
and reading it as a gathered work item passes a release that never shipped
the entry. Every marker reader here — `ungathered` and `--check`'s count —
asks `live_markers`, which reads through `unverified_check.py#live_lines`,
the one function `docs/the-evidence-ledger.md` §*A marker counts only on a
live line* names. `survivor_check.py#gathered_fragments` reads this file's
markers through the same function, so the two cannot disagree about which
entries shipped.

**`--check` judges by the markers, not only by the fragments.** A fragment
glob goes empty two ways: every fragment reached the file, and there are no
fragments left to reach it because `settle` retired the work items whole. The
second is the state every repository running this methodology ends up in, and
reporting it as *all gathered* is a pass over an empty set. So the check also
counts the markers the release files under `changelog/` carry and prints both
numbers, and a corpus with neither a fragment nor a marker is refused rather
than passed. Each release file is read on its own, so a block one of them
leaves open hides nothing in another.

**A fragment carries no line starting `## `** (#586). The released section
ends at the next such line, for `insert` below and for
`publish_release_note.py#section_body`, so a fragment carrying one would ship
every entry after it under no version and cut the release note short. The
gather refuses, among the fragments it would write, before anything is
written or printed, naming the fragment, the line number and the line.

**A fragment closes what it opens** (#584, round 1's finding 1). The gather
writes a fragment verbatim with the next marker below it, so a fenced block or
an HTML comment it leaves open hides that marker and every older one from
`live_markers`: `--check` then calls a gathered entry missing, and the gather
it advises writes the entry twice. The gather refuses such a fragment, among
the ones it would write, before anything is written or printed, naming it.
It does not close the block for the author: that would ship text nobody
wrote, and a bare comment opener in prose was never meant to open anything.

Exit codes: 0 done · 1 nothing to gather, a fragment is missing from every
release file,
`--check` found neither a fragment nor a marker and so examined nothing, a
fragment carries a line starting `## `, or a fragment leaves a fenced block
or an HTML comment open. All five are failures a release pull request should
stop on.
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
TITLE = "# Changelog"
# The index, and the directory each release's own file lives in (#728).
INDEX = "CHANGELOG.md"
RELEASES = "changelog"
# A release file's name: the version and nothing else, so a README or a
# draft beside them is not read as a release.
RELEASE_FILE_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.md$")
# Markers on a line of their own, which is how `section()` writes them. The
# line anchor is what `fold_ledger.py#is_marked` already pays for: this file's
# own entries describe the convention, so a bare substring count reads the
# description as a gathered work item.
MARKER_LINE_RE = re.compile(r"^<!-- specs/\S+ -->$", re.M)

# The live-line rule is the shipped one, loaded by path the way
# `fold_ledger.py#load_reader` loads it (#487, #584). A reader that is moved
# or renamed stops the gather at load with a traceback, at the release, which
# is the loud direction.
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")


def load_reader(path=READER):
    """`unverified_check.py` as a module."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("specseal_unverified_reader", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reader = load_reader()


def live_markers(changelog_text):
    """The work item ids whose marker stands on a live line of its own, in
    file order (#584).

    Lines are split by the shared reader's `gfm_lines`, as
    `survivor_check.py#gathered_fragments` splits them, so the two readers of
    this file see the same lines -- and the lines GFM renders, so a marker
    standing after a U+2028 or a form feed on its line is not a line of its
    own to either of them (#664). Every other split of this file's text and
    of a fragment below reads the same function, for the same reason."""
    return [
        line[len("<!-- specs/") : -len(" -->")]
        for line, live in reader.live_lines(reader.gfm_lines(changelog_text))
        if live and MARKER_LINE_RE.match(line)
    ]


def marker(work_item_id):
    """The comment that says this work item's entry is in the file."""
    return f"<!-- specs/{work_item_id} -->"


def fragments(root):
    """[(work item id, body)] for every `seal/specs/*/changelog.md`, in id order.

    The id is unix seconds, so sorting by it is chronological and stable — the
    same input always produces the same section, which is what makes a re-run
    comparable to the run before it. An empty fragment is skipped rather than
    gathered as a blank entry.
    """
    out = []
    for path in glob.glob(os.path.join(root, "seal", "specs", "*", "changelog.md")):
        work_item_id = os.path.basename(os.path.dirname(path))
        with open(path, encoding="utf-8") as f:
            body = f.read().strip()
        if body:
            out.append((work_item_id, body))
    return sorted(out)


def release_path(root, version):
    """`changelog/<version>.md` under `root`, the file a release's notes are."""
    return os.path.join(root, RELEASES, f"{version}.md")


def release_files(root):
    """`[(version, path)]` for every `changelog/<X.Y.Z>.md`, newest first.

    Listed from the disk rather than from git: release preparation runs this
    before the new file is staged (`docs/release-checklist.md` §3)."""
    directory = os.path.join(root, RELEASES)
    if not os.path.isdir(directory):
        return []
    found = []
    for name in os.listdir(directory):
        parts = RELEASE_FILE_RE.match(name)
        if parts:
            number = tuple(int(n) for n in parts.groups())
            found.append((number, name[: -len(".md")], os.path.join(directory, name)))
    return [(version, path) for _, version, path in sorted(found, reverse=True)]


def released_markers(root):
    """The live markers of every release file, each file read on its own, so
    a block one file leaves open hides nothing in the next (#584's rule,
    applied per file)."""
    out = []
    for _, path in release_files(root):
        with open(path, encoding="utf-8") as f:
            out.extend(live_markers(f.read()))
    return out


def ungathered(marked, frags):
    """The fragments whose id is not among `marked`, the live markers
    `released_markers` read.

    It used to be a substring test, so a marker quoted in prose, a fence or a
    code span marked its fragment gathered (#584)."""
    gathered = set(marked)
    return [(i, body) for i, body in frags if i not in gathered]


def leaves_open(body):
    """Whether a marker written below BODY would stand on no live line: the
    fragment opens a fenced block or an HTML comment and never closes it
    (#584, round 1's finding 1).

    `section` writes the next fragment's marker below it after one blank
    line, and `insert` puts every older section's markers below that, so
    `ungathered` would call each of them missing and the gather `--check`
    then advises would write them twice. The probe is exactly that shape —
    the body, a blank line, a marker — asked of `live_lines` itself, so there
    is no second rule for what an open block is."""
    probe = [*reader.gfm_lines(body), "", marker("probe")]
    return not list(reader.live_lines(probe))[-1][1]


# What ends a released section for both of its readers: `insert` below and
# `publish_release_note.py#section_body`. Not a markdown heading rule — neither
# reader knows a fence or an indent — so this is exactly their predicate.
SECTION_LINE = "## "


def section_lines(root, work_item_id):
    """`[(1-based line number, line)]` for every line of the fragment on disk
    that starts `## `.

    #586: such a line ends the released section early for the gatherer and
    for the release note alike, so every entry after it ships under no
    version. The numbers are the file's own, read again rather than taken
    from `fragments`, whose body is stripped and so counts from the first
    line with text on it."""
    path = os.path.join(root, "seal", "specs", work_item_id, "changelog.md")
    with open(path, encoding="utf-8") as f:
        lines = reader.gfm_lines(f.read())
    return [
        (n, line) for n, line in enumerate(lines, 1) if line.startswith(SECTION_LINE)
    ]


def section(version, date, entries):
    """The released section, as it goes into the file."""
    blocks = [f"## {version} — {date}", ""]
    for work_item_id, body in entries:
        blocks.append(marker(work_item_id))
        blocks.append(body)
        blocks.append("")
    return "\n".join(blocks)


def heading_re(version):
    """The `## X.Y.Z — <date>` line for one version, with the date captured."""
    return re.compile(rf"^## {re.escape(version)}\b(?: — (\S+))?.*$", re.M)


def section_heading(changelog_text, version):
    """The match for the `## <version>` line the file already has, or None.

    The one predicate for *is there a section*, asked by `main` before it
    builds the block and by `insert` when it places the entries. They used to
    ask two — `existing_date` for `main`, the heading pattern for `insert` —
    and a heading with no date answered them differently: the dry run printed
    a fresh heading while the write appended (round 1 of #536's work item).
    """
    return heading_re(version).search(changelog_text)


def existing_date(changelog_text, version):
    """The date the section already carries, or None where it has none.

    #289: a second gather for a version already in the file used to write a
    second heading, dated the day it ran, and one release shipped with its
    entries split across two sections that read as two releases with the same
    number. The date a section carries is the first gather's — the release
    date — and a repair gathered after the release pull request went red does
    not move it. This answers the date alone; whether the section exists is
    `section_heading`'s question.
    """
    found = section_heading(changelog_text, version)
    return found.group(1) if found else None


def insert(changelog_text, block, version):
    """Into the section `version` already has, or above every dated one.

    A released section reads as newer than everything under it, so a new one
    landing anywhere but the top inverts the order the file is read in — which
    `tests/test_release_hygiene.py` has caught once already, from a rebase
    resolved the wrong way.

    Where the file already heads `version`, `block`'s heading is dropped and
    its entries go at the end of that section, before the next `## `, in the
    order the fragments came: the section is one release however many gathers
    wrote it, and `publish_release_note.py#section_body` reads one section.
    `tests/test_release_hygiene.py` refuses a file that heads a version twice,
    so this arm is the one a red release pull request has to take.
    """
    lines = reader.gfm_lines(changelog_text)
    found = section_heading(changelog_text, version)
    if found is not None:
        # The heading's index in `lines`, counted with the split that made
        # them. Counting "\n" here while `lines` came from another split put
        # the entries above the heading wherever the two disagreed (#664).
        at = len(reader.gfm_lines(changelog_text[: found.start()]))
        end = next(
            (n for n in range(at + 1, len(lines)) if lines[n].startswith("## ")),
            len(lines),
        )
        while end > at + 1 and not lines[end - 1].strip():
            end -= 1
        # `section()` writes the heading, a blank line, then the entries;
        # the heading is the file's already and the blank line is re-added.
        # The tail's own blank lines go too, or the one re-added here joins
        # them: two before the next heading, and an extra at the end of the
        # file when the section was the last (round 1 of #536's work item).
        entries = reader.gfm_lines(block)[2:]
        tail = lines[end:]
        while tail and not tail[0].strip():
            tail.pop(0)
        joined = "\n".join([*lines[:end], "", *entries, "", *tail])
        return joined.rstrip("\n") + "\n"
    at = next((n for n, line in enumerate(lines) if line.startswith("## ")), None)
    if at is None:
        at = len(lines)
    return "\n".join(lines[:at] + reader.gfm_lines(block) + [""] + lines[at:]) + "\n"


def index_entry(heading, version):
    """One release's entry in `CHANGELOG.md`: the heading line its file opens
    with, a blank line, and the link to the file.

    The heading is kept here as well as in the file because the update skill
    an installed copy already carries checks an update landed by the first
    `## ` line of `CHANGELOG.md` (spec D2 of #728); the link is what a
    reader follows."""
    link = f"{RELEASES}/{version}.md"
    return f"{heading}\n\n[{link}]({link})"


def indexed(index_text, heading, version):
    """`index_text` with `version`'s entry above every older one, or as it is
    where the index already heads `version`.

    The entry goes above the first `## ` line, the way `insert` places a new
    section; an index with none yet takes it after its own text and one
    blank line."""
    if section_heading(index_text, version) is not None:
        return index_text
    lines = reader.gfm_lines(index_text)
    entry = reader.gfm_lines(index_entry(heading, version))
    at = next(
        (n for n, line in enumerate(lines) if line.startswith(SECTION_LINE)), None
    )
    if at is None:
        while lines and not lines[-1].strip():
            lines.pop()
        return "\n".join([*lines, "", *entry]) + "\n"
    return "\n".join([*lines[:at], *entry, "", *lines[at:]]) + "\n"


def main(argv=None):
    console.to_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", help="the version being released, e.g. 0.2.0")
    ap.add_argument("--date", help="release date (default: today, UTC)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="report fragments that are in no changelog/<X.Y.Z>.md and exit 1",
    )
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--root", default=ROOT, help="repository root (default: this one)")
    args = ap.parse_args(argv)

    if not args.check and not args.version:
        ap.error("pass --version to gather, or --check to verify")

    root = os.path.abspath(args.root)
    frags = fragments(root)
    marked = released_markers(root)
    missing = ungathered(marked, frags)

    if args.check:
        if missing:
            print(f"changelog fragments that never reached a file under {RELEASES}/:")
            for work_item_id, _ in missing:
                print(f"  seal/specs/{work_item_id}/changelog.md")
            print(
                "\nRelease preparation gathers them:\n"
                "  python3 .github/scripts/gather_changelog.py --version X.Y.Z"
            )
            return 1
        # What the check read, not only what it did not find. `ungathered`
        # measures the fragments on disk, and after `settle` retires a
        # released work item its directory is gone with its fragment — so an
        # empty glob used to print "all gathered" having examined nothing,
        # which reads as success and is the one direction a checker of claims
        # must not fail in (`unverified_check.py`'s own docstring argues it
        # one file over). The markers in the release files are the record that
        # survives the directory, so they are what a folded corpus is judged by.
        if not frags and not marked:
            print(
                "nothing to check: no changelog fragment under seal/specs/ "
                f"and no <!-- specs/<work-item-id> --> marker in any "
                f"{RELEASES}/<X.Y.Z>.md, so this examined nothing and "
                "`all gathered` would be a report about an empty set.\n"
                "A release gathers its fragments into its own file, and the "
                "marker above each entry is what stays once the work item's "
                "directory is folded away."
            )
            return 1
        print(
            f"{len(frags)} changelog fragments, all gathered; "
            f"{len(marked)} work items marked in {RELEASES}/"
        )
        return 0

    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        ap.error(f"--version must be X.Y.Z, not {args.version!r}")

    if not missing:
        print(
            f"nothing to gather: all {len(frags)} fragments are already in "
            f"{RELEASES}/. A release with no entries is one nobody can read — "
            "check that the branches you meant to ship are merged"
        )
        return 1

    # #586: refused before anything is written or printed, among the
    # fragments this run would gather only. One already in the file cannot be
    # un-shipped by refusing the release, and refusing over it would leave no
    # remedy but editing prose that has shipped.
    headed = [
        (work_item_id, n, line)
        for work_item_id, _ in missing
        for n, line in section_lines(root, work_item_id)
    ]
    if headed:
        print(
            "changelog fragments carrying a line that starts `## `, which "
            "ends the released section for this gather and for the release "
            "note alike, so every entry after it would ship under no version:"
        )
        for work_item_id, n, line in headed:
            print(f"  seal/specs/{work_item_id}/changelog.md:{n}: {line}")
        print(
            "\nDemote each to `###` or lower in a pull request into the release "
            "branch, then gather again. Nothing was written."
        )
        return 1

    # #584, phase 9: refused on the same terms as #586 above, and after it.
    unclosed = [work_item_id for work_item_id, body in missing if leaves_open(body)]
    if unclosed:
        print(
            "changelog fragments that open a fenced block or an HTML comment "
            "and never close it, so every marker written below them would "
            "read as not gathered and --check would ask for a second gather:"
        )
        for work_item_id in unclosed:
            print(f"  seal/specs/{work_item_id}/changelog.md")
        print(
            "\nClose it in the fragment in a pull request into the release "
            "branch, then gather again. Nothing was written."
        )
        return 1

    # The section's own date where it already exists — the release date is
    # the first gather's, and a later gather joins that section (#289). The
    # index's heading answers where the file does not exist yet.
    path = release_path(root, args.version)
    shown = os.path.relpath(path, root).replace(os.sep, "/")
    text = ""
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            text = f.read()
    index_path = os.path.join(root, INDEX)
    with open(index_path, encoding="utf-8") as f:
        index = f.read()
    found = section_heading(text, args.version)
    date = (
        existing_date(text, args.version)
        or existing_date(index, args.version)
        or args.date
        or datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    )
    block = section(args.version, date, missing)
    # The heading a reader sees is the file's own where the section exists
    # — dated or not — and the block's only where this run writes one.
    heading = found.group(0) if found else reader.gfm_lines(block)[0]
    if args.dry_run:
        print(f"into {shown}:")
        if found:
            print("appending into the existing section:\n")
        print("\n".join([heading, *reader.gfm_lines(block)[1:]]))
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(insert(text, block, args.version) if text.strip() else block)
    new_index = indexed(index, heading, args.version)
    if new_index != index:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_index)
    print(
        f"gathered {len(missing)} fragments into {shown}, {heading}"
        + (" (appended into the existing section)" if found else "")
    )
    for work_item_id, _ in missing:
        print(f"  seal/specs/{work_item_id}/changelog.md")
    if new_index != index:
        print(f"{INDEX} now heads its index with {heading}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
