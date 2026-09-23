#!/usr/bin/env python3
"""Gather each work item's changelog fragment into the released section.

Three branches ran in parallel on 2026-09-01 and touched 34 files between them.
They shared exactly one, and all three pairs shared the same one: `CHANGELOG.md`
(issue #46). Nothing else overlapped at all — so parallel work was never the
problem, appending to one three-line region was.

The conflict itself is cheap and arrives at the worst possible moment: after
the broad gate has run and before the pull request opens, where nothing may be
edited. Resolving it costs a second run of the whole broad gate.

So a change writes `seal/specs/<work-item-id>/changelog.md` and leaves `CHANGELOG.md`
alone. Two branches cannot collide, because no two work items share an id. This
script is the other half — release preparation runs it, and it concatenates the
fragments into `## X.Y.Z — <date>`.

  gather_changelog.py --version 0.2.0            write the released section
  gather_changelog.py --version 0.2.0 --dry-run  print it, write nothing
  gather_changelog.py --check                    every fragment reached the file

**A gathered fragment is marked, not matched.** Each entry is written under an
HTML comment naming the work item it came from, and `--check` looks for that
comment. Matching a fragment's text against the file instead would work once
and then break for good: any copy-edit to a released entry would make its
fragment read as ungathered forever. The marker also earns its place twice —
it is the only link from a released entry back to the work that produced it.

Markdown comments do not render, so a reader never sees them.

**`--check` judges by the markers, not only by the fragments.** A fragment
glob goes empty two ways: every fragment reached the file, and there are no
fragments left to reach it because `settle` retired the work items whole. The
second is the state every repository running this methodology ends up in, and
reporting it as *all gathered* is a pass over an empty set. So the check also
counts the markers `CHANGELOG.md` carries and prints both numbers, and a
corpus with neither a fragment nor a marker is refused rather than passed.

Exit codes: 0 done · 1 nothing to gather, a fragment is missing from the file,
or `--check` found neither a fragment nor a marker and so examined nothing.
All three are failures a release pull request should stop on.
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
# Markers on a line of their own, which is how `section()` writes them. The
# line anchor is what `fold_ledger.py#is_marked` already pays for: this file's
# own entries describe the convention, so a bare substring count reads the
# description as a gathered work item.
MARKER_LINE_RE = re.compile(r"^<!-- specs/\S+ -->$", re.M)


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


def ungathered(changelog_text, frags):
    return [(i, body) for i, body in frags if marker(i) not in changelog_text]


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


def existing_date(changelog_text, version):
    """The date the file already gives `version`, or None if it has no section.

    #289: a second gather for a version already in the file used to write a
    second heading, dated the day it ran, and one release shipped with its
    entries split across two sections that read as two releases with the same
    number. The date a section carries is the first gather's — the release
    date — and a repair gathered after the release pull request went red does
    not move it.
    """
    found = heading_re(version).search(changelog_text)
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
    lines = changelog_text.splitlines()
    heading = heading_re(version)
    at = next((n for n, line in enumerate(lines) if heading.match(line)), None)
    if at is not None:
        end = next(
            (n for n in range(at + 1, len(lines)) if lines[n].startswith("## ")),
            len(lines),
        )
        while end > at + 1 and not lines[end - 1].strip():
            end -= 1
        # `section()` writes the heading, a blank line, then the entries;
        # the heading is the file's already and the blank line is re-added.
        entries = block.splitlines()[2:]
        return "\n".join([*lines[:end], "", *entries, "", *lines[end:]]) + "\n"
    at = next((n for n, line in enumerate(lines) if line.startswith("## ")), None)
    if at is None:
        at = len(lines)
    return "\n".join(lines[:at] + block.splitlines() + [""] + lines[at:]) + "\n"


def main(argv=None):
    console.to_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", help="the version being released, e.g. 0.2.0")
    ap.add_argument("--date", help="release date (default: today, UTC)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="report fragments that are not in CHANGELOG.md and exit 1",
    )
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--root", default=ROOT, help="repository root (default: this one)")
    args = ap.parse_args(argv)

    if not args.check and not args.version:
        ap.error("pass --version to gather, or --check to verify")

    root = os.path.abspath(args.root)
    changelog = os.path.join(root, "CHANGELOG.md")
    with open(changelog, encoding="utf-8") as f:
        text = f.read()
    frags = fragments(root)
    missing = ungathered(text, frags)

    if args.check:
        if missing:
            print("changelog fragments that never reached CHANGELOG.md:")
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
        # one file over). The markers in the file are the record that survives
        # the directory, so they are what a folded corpus is judged by.
        marked = len(MARKER_LINE_RE.findall(text))
        if not frags and not marked:
            print(
                "nothing to check: no changelog fragment under seal/specs/ "
                "and no <!-- specs/<work-item-id> --> marker in CHANGELOG.md, "
                "so this examined nothing and `all gathered` would be a "
                "report about an empty set.\n"
                "A release gathers its fragments into the file, and the "
                "marker above each entry is what stays once the work item's "
                "directory is folded away."
            )
            return 1
        print(
            f"{len(frags)} changelog fragments, all gathered; "
            f"{marked} work items marked in CHANGELOG.md"
        )
        return 0

    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        ap.error(f"--version must be X.Y.Z, not {args.version!r}")

    if not missing:
        print(
            f"nothing to gather: all {len(frags)} fragments are already in "
            "CHANGELOG.md. A release with no entries is one nobody can read — "
            "check that the branches you meant to ship are merged"
        )
        return 1

    # The section's own date where it already exists — the release date is
    # the first gather's, and a later gather joins that section (#289).
    already = existing_date(text, args.version)
    date = (
        already or args.date or datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    )
    block = section(args.version, date, missing)
    if args.dry_run:
        if already:
            print("appending into the existing section:\n")
        print(block)
        return 0
    with open(changelog, "w", encoding="utf-8") as f:
        f.write(insert(text, block, args.version))
    print(
        f"gathered {len(missing)} fragments into ## {args.version} — {date}"
        + (" (appended into the existing section)" if already else "")
    )
    for work_item_id, _ in missing:
        print(f"  seal/specs/{work_item_id}/changelog.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
