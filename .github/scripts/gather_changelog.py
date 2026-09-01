#!/usr/bin/env python3
"""Gather each work item's changelog fragment into the released section.

Three branches ran in parallel on 2026-09-01 and touched 34 files between them.
They shared exactly one, and all three pairs shared the same one: `CHANGELOG.md`
(issue #46). Nothing else overlapped at all — so parallel work was never the
problem, appending to one three-line region was.

The conflict itself is cheap and arrives at the worst possible moment: after
the broad gate has run and before the pull request opens, where nothing may be
edited. Resolving it costs a second run of the whole broad gate.

So a change writes `specs/<work-item-id>/changelog.md` and leaves `CHANGELOG.md`
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

Exit codes: 0 done · 1 nothing to gather, or a fragment is missing from the
file. Both are failures a release pull request should stop on.
"""

import argparse
import datetime
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TITLE = "# Changelog"


def marker(work_item_id):
    """The comment that says this work item's entry is in the file."""
    return f"<!-- specs/{work_item_id} -->"


def fragments(root):
    """[(work item id, body)] for every `specs/*/changelog.md`, in id order.

    The id is unix seconds, so sorting by it is chronological and stable — the
    same input always produces the same section, which is what makes a re-run
    comparable to the run before it. An empty fragment is skipped rather than
    gathered as a blank entry.
    """
    out = []
    for path in glob.glob(os.path.join(root, "specs", "*", "changelog.md")):
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


def insert(changelog_text, block):
    """Above every dated section, below the file's title.

    A released section reads as newer than everything under it, so a new one
    landing anywhere but the top inverts the order the file is read in — which
    `tests/test_release_hygiene.py` has caught once already, from a rebase
    resolved the wrong way.
    """
    lines = changelog_text.splitlines()
    at = next((n for n, line in enumerate(lines) if line.startswith("## ")), None)
    if at is None:
        at = len(lines)
    return "\n".join(lines[:at] + block.splitlines() + [""] + lines[at:]) + "\n"


def main(argv=None):
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
                print(f"  specs/{work_item_id}/changelog.md")
            print(
                "\nRelease preparation gathers them:\n"
                "  python3 .github/scripts/gather_changelog.py --version X.Y.Z"
            )
            return 1
        print(f"{len(frags)} changelog fragments, all gathered")
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

    date = args.date or datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    block = section(args.version, date, missing)
    if args.dry_run:
        print(block)
        return 0
    with open(changelog, "w", encoding="utf-8") as f:
        f.write(insert(text, block))
    print(f"gathered {len(missing)} fragments into ## {args.version} — {date}")
    for work_item_id, _ in missing:
        print(f"  specs/{work_item_id}/changelog.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
