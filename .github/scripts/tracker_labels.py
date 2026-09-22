#!/usr/bin/env python3
"""Create the labels this repository's documents specify but the tracker lacks.

`docs/issues-and-milestones.md` has specified `size: now` since 0.11.1 -- two
states, the prefix argument, what its absence means -- and **the label was
never created**. Measured 2026-09-20 for #450 and again 2026-09-22:
`gh label list` does not list it and no issue has ever carried it. So a
section described a mechanism, and the paragraph arguing why the prefix and
not a bare `now` argued carefully about a label nobody could apply.

**Why it was nobody's, which is the half worth keeping.** The work item that
wrote the section ended its changelog entry with *creating the label and
applying it are the repository owner's, after this merges*. The act was
assigned to a **person**, and a person has no queue this repository can read
-- no open issue, no checklist row, no failing check. Three releases were cut
in between, and the cost came due at the fourth: six issue bodies re-read to
decide which had to be in effect next, which is exactly the reading the label
exists to make unnecessary.

The repair is not *remember harder* and not a ticket, which is the same act
one queue over. It is this: a label a document specifies is the same kind of
object as a label a release needs, and
`label_merged_on_release_branch.py` has been creating one of those from a
workflow all along, with the `issues: write` the job already holds. So the
declaration below is what a document specifies, and the workflow that runs
when `main` moves reconciles it.

**It never deletes and never re-colours.** The only write is
`gh label create`, and it happens only after a read says the name is absent
-- which makes a re-run a no-op by construction rather than by assuming what
GitHub does with a duplicate. A label deleted by hand comes back at the next
release rather than immediately, and that is the accepted cost of hanging
this off a trigger that already exists rather than inventing one.

**It is not a gate and must not become one.** A hygiene step failing a pull
request for a missing label was considered and rejected: it would be red on
the very branch that adds the label, because no agent in this repository's
chain may write to the tracker, and it would have to be added to
`broad_gate.py`'s partition as well. A step that performs the act costs
neither.

  tracker_labels.py --check   report what is missing, exit 0
  tracker_labels.py --apply   create what is missing

`DRY_RUN=1` makes `--apply` print what it would create and write nothing.

Environment: `REPO`, `GH_TOKEN`.
"""

import argparse
import importlib.util
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hooks")
)
import console

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Imported by path for the reason `label_merged_on_release_branch.py` gives:
# a test importing THIS module by path gets the same neighbours the workflow
# does. `existing_labels` reads the whole label list rather than asking for
# one name, because every name here carries a space and a colon and the
# one-label read would turn on how those are encoded in a URL path.
signal = _load("label_merged_on_release_branch", "label_merged_on_release_branch.py")
closer = signal.closer


# --- what the documents specify -------------------------------------------
#
# One row per label, and the row carries the document that specifies it.
# That last field is not decoration: this file is a copy of a decision made
# somewhere else, and a reader who cannot get back to the original has to
# take the copy's word for what the label means.
#
# The description is the document's OWN sentence, the way
# `label_merged_on_release_branch.py#label_description` derives one, and it
# says when the label stops being the current answer -- which is the half a
# person reading the tracker cannot otherwise know.
#
# The colour is `chain: capped`'s. That is this repository's other
# `<subject>: <state>` label and the shape `size: now`'s name was taken from
# -- the specifying section says so in as many words -- so two labels of one
# shape read as one shape on the tracker. `spec.md` §*Judgments* 11 expected
# the topic labels' family instead; they carry five different colours between
# them, so there was no one family colour to join, and `overview.md` records
# the divergence. Nothing turns on it either way.
LABELS = (
    {
        "name": "size: now",
        "color": "d4c5f9",
        "description": (
            "This ticket has to be in effect before the next work item "
            "starts; removed when the release carrying it closes the issue"
        ),
        "specified_by": (
            "docs/issues-and-milestones.md "
            "§A label answers what it is about, and survives the move"
        ),
    },
)


def declared():
    return LABELS


def missing(repo):
    """The declared labels the tracker does not have, in declared order."""
    present = signal.existing_labels(repo)
    return [label for label in declared() if label["name"] not in present]


def create(repo, label):
    closer.run(
        "gh",
        "label",
        "create",
        label["name"],
        "--repo",
        repo,
        "--description",
        label["description"],
        "--color",
        label["color"],
    )


def main(argv=None):
    # Every entry point carries this, because a hook or a script that raises
    # while printing dies with stdout empty and an empty stdout is how a gate
    # says "nothing to see here" (`hooks/console.py`). The arm at risk is
    # `--check`, which is the one a person types: under cp949, cp932, cp936
    # or a bare `LC_ALL=C` the em dash below raises `UnicodeEncodeError` and
    # the process dies. The workflow's runner is UTF-8, so `--apply` was
    # never the exposed one. Round 1, finding 3.
    console.to_utf8()
    parser = argparse.ArgumentParser(
        description="Reconcile the tracker's labels with what the documents specify."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check", action="store_true", help="report what is missing, exit 0"
    )
    group.add_argument("--apply", action="store_true", help="create what is missing")
    args = parser.parse_args(argv)

    repo = os.environ["REPO"]
    dry = os.environ.get("DRY_RUN", "").strip() not in ("", "0", "false", "no")
    if dry:
        print("DRY_RUN — nothing will be written")

    absent = missing(repo)
    if not absent:
        print(f"all {len(declared())} declared labels exist — nothing to create")
        return 0

    for label in absent:
        print(f"{label['name']!r} is missing, specified by {label['specified_by']}")
        if args.check or dry:
            continue
        create(repo, label)
        print(f"created {label['name']!r}: {label['description']}")
    if args.check:
        print(
            "\nThe workflow that runs when `main` moves creates these:\n"
            "  python3 .github/scripts/tracker_labels.py --apply"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
