#!/usr/bin/env python3
"""Label the issues a squash into `release/vX.Y.Z` just answered.

Between a work item squashing into `release/vX.Y.Z` and the release reaching
`main`, a finished ticket is indistinguishable from one nobody has started:
an issue's state does not move until `main` moves, and `main` moves once per
release. A person reading the milestone mid-release cannot tell the two
apart, and the checklist line that used to tell them apart went with the file
it lived in (#351, #359).

So this runs when a release branch moves. It reads the pull request numbers
out of the commit subjects that arrived, fetches those pull request bodies,
and puts `merged: X.Y.Z` on every issue their closing keywords name. The
version comes from the branch name.

**Nothing here parses anything new.** `MERGED_PR`, `keywords_in`,
`pull_request_body` and `arrived` all come from
`close_issues_on_release.py`, which is the module that already reads exactly
these three things and whose `FENCE`/`SPAN` treatment of a quoted keyword is
the behaviour a second reader would have to reproduce. Importing it runs
nothing: its `main` is guarded.

Four things it deliberately does not do.

**It does not close anything.** An issue closed at the release-branch merge
is closed for something nobody has received yet.
`close_issues_on_release.py` keeps the close, when `main` moves, and this
adds no second closer.

**It never removes a label and never comments.** The only two writes are
`gh label create` and `gh issue edit --add-label`.

**It writes nothing it has not read first.** The label is created only after
a read says it is absent, and added to an issue only after a read says that
issue does not carry it. That is not tidiness -- it is what makes a re-run of
a push, or a re-push, a no-op *by construction* rather than by assuming what
GitHub does with a duplicate label. Nobody here has run that assumption
(`questions.md` Q6), and this way nobody has to.

**A `(#N)` that names no pull request is skipped, not fatal**, and so is a
number naming no issue at all -- both for the reasons
`close_issues_on_release.py` gives, on the same readers.

`DRY_RUN=1` prints what it would write and writes nothing, for the reason
that script's docstring gives: a tool whose only mode has side effects gets
run for its output sooner or later.

Environment: `BRANCH` (`github.ref_name`), `BEFORE`, `AFTER`, `REPO`.
"""

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The branch a release accumulates on. Anything else under `release/*` --
# `release/next`, a typo -- is a shape this cannot name a version for, and it
# says so and exits 0 rather than guessing one.
RELEASE_BRANCH = re.compile(r"^release/v(\d+\.\d+\.\d+)$")


def _load(name, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Imported by path rather than by `import close_issues_on_release`, so that a
# test importing THIS module by path gets the same neighbour the workflow
# does. `sys.path[0]` is this directory only when the script is the entry
# point.
closer = _load("close_issues_on_release", "close_issues_on_release.py")


# --- the name mapping -----------------------------------------------------
#
# branch `release/vX.Y.Z` -> version `X.Y.Z` -> milestone `release: X.Y.Z`
# -> label `merged: X.Y.Z`. Four spellings of one fact, and until these
# functions existed the chain was written out by hand at each end. They live
# here, in the first of the two scripts to exist, and
# `release_completeness_check.py` imports them: one source, the way both
# scripts take their readers from one source.


def version_of(branch):
    """`X.Y.Z` for a release branch, or None for any other name."""
    found = RELEASE_BRANCH.match((branch or "").strip())
    return found.group(1) if found else None


def milestone_title(version):
    return f"release: {version}"


def label_name(version):
    return f"merged: {version}"


def label_description(version):
    """What the label says on the tracker, where a person reads it.

    It has to say WHEN the label stops being the current answer, because the
    labels accumulate -- one per release, never removed, since deleting a
    label deletes it from every issue that carried it and falsifies the
    record it was created to leave.
    """
    return (
        f"Squash-merged into release/v{version}; closes when the release reaches main"
    )


# --- reads ----------------------------------------------------------------


def issue_labels(repo, number):
    """(label names, exists) for an issue, or ([], False) if there is none.

    `_issue_api` is the 404-tolerant read `close_issues_on_release.py` wrote
    for exactly this -- a number that names nothing arrives here from a
    hand-written `(#N)` and from a typo in a merged body, and neither is a
    reason to fail a push. Reaching for the private name is deliberate: the
    public wrappers beside it return a state and a body, and a second read of
    my own would be the copied reader this script exists not to have.
    """
    data, exists = closer._issue_api(repo, number)
    if not exists:
        return [], False
    return [entry.get("name") for entry in data.get("labels") or []], True


def existing_labels(repo):
    """Every label name the repository has.

    The whole list rather than `GET /labels/{name}`, because the name carries
    a space and a colon and the one-label read would turn on how they are
    encoded in a path -- a detail nothing else here depends on.
    """
    out = closer.run(
        "gh", "label", "list", "--repo", repo, "--limit", "1000", "--json", "name"
    )
    return {entry["name"] for entry in json.loads(out)}


# --- writes ---------------------------------------------------------------


def create_label(repo, version):
    closer.run(
        "gh",
        "label",
        "create",
        label_name(version),
        "--repo",
        repo,
        "--description",
        label_description(version),
        # The green the first one was created with by hand, so a label this
        # writes and a label somebody wrote before it look the same.
        "--color",
        "0E8A16",
    )


def add_label(repo, number, version):
    closer.run(
        "gh",
        "issue",
        "edit",
        str(number),
        "--repo",
        repo,
        "--add-label",
        label_name(version),
    )


# --- the run --------------------------------------------------------------


def issues_in(repo, subjects):
    """{issue number: the pull request that claimed it}, in arrival order."""
    wanted = {}
    for subject in subjects:
        found = closer.MERGED_PR.search(subject.strip())
        if not found:
            continue
        number = int(found.group(1))
        body = closer.pull_request_body(repo, number)
        if body is None:
            print(f"#{number} is not a pull request — a hand-written number")
            continue
        for issue in closer.keywords_in(body):
            wanted.setdefault(int(issue), number)
    return wanted


def main():
    branch = os.environ.get("BRANCH", "")
    version = version_of(branch)
    if version is None:
        print(f"{branch!r} is not a release/vX.Y.Z branch — nothing to label")
        return
    before, after = os.environ.get("BEFORE", ""), os.environ["AFTER"]
    repo = os.environ["REPO"]
    dry = os.environ.get("DRY_RUN", "").strip() not in ("", "0", "false", "no")
    if dry:
        print("DRY_RUN — nothing will be written")

    label = label_name(version)
    wanted = issues_in(repo, closer.arrived(before, after))
    if not wanted:
        print("no closing keyword in any of them — nothing to label")
        return

    if label in existing_labels(repo):
        print(f"label {label!r} exists")
    elif dry:
        print(f"would create label {label!r}")
    else:
        create_label(repo, version)
        print(f"created label {label!r}")

    for issue, source in sorted(wanted.items()):
        carried, exists = issue_labels(repo, issue)
        if not exists:
            print(f"#{issue} does not exist (named by #{source}) — skipping")
            continue
        if label in carried:
            print(f"#{issue} already carries {label!r} — leaving it")
            continue
        if dry:
            print(f"would label #{issue} {label!r}, named by #{source}")
            continue
        add_label(repo, issue, version)
        print(f"labelled #{issue} {label!r}, named by #{source}")


if __name__ == "__main__":
    sys.exit(main())
