#!/usr/bin/env python3
"""A release cannot ship while its milestone claims work the release has not
got.

`docs/flow.md` used to carry this as a checklist bullet — *is everything in* —
and #351 deleted the file. This is the same question asked by the machine, at
the release pull request, which is the last moment anybody is looking.

Three sets of issue numbers, and naming them is what keeps a failure pointing
at the right party.

    M   open issues whose milestone is `release: X.Y.Z`
    D   issues the release branch actually carries: its commit subjects ->
        `(#N)` -> those pull request bodies -> closing keywords
    L   issues carrying the label `merged: X.Y.Z`

**D is the source of truth and L is a cache of it.** The signal
(`label_merged_on_release_branch.py`) writes L from D one push at a time; this
recomputes D in full from the release branch's own range. So the refusal is
`M \\ D` and never depends on a label write having succeeded — computing it as
`M \\ L` would give the same answer by transitivity and blame the wrong party,
since a release blocked by a failed label write is repaired by a person adding
a label by hand, which is the act this whole work item removes.

What it does in each direction, and every line says which direction it is
reporting:

    M \\ D   FAILS. The milestone claims an item the release does not carry
    L \\ D   FAILS. A label naming a release the issue is not in is always a
            hand-edit or a squash subject that lost its `(#N)`, and one
            command repairs it
    D \\ L   reports, passes. The signal missed one, and a release must not be
            held for a failure of the signal rather than of its contents
    D \\ M   reports, passes. An issue somebody closed by hand mid-release is
            in D and in no open milestone, which is ordinary tracker hygiene

It writes nothing anywhere. Exit 0 or 1, and a shape it cannot judge exits 0
with the reason printed.

Environment: `REPO`, `HEAD_BRANCH` (`github.head_ref`), and `BASE` for the
ref the range is measured from (default `origin/main`).
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, filename):
    path = os.path.join(HERE, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The signal holds the name mapping — branch -> version -> milestone -> label
# — and reaches the closer's readers through its own `closer`. Importing it
# runs nothing: it defines constants and functions at module level and
# guards its `main`.
signal = _load("label_merged_on_release_branch", "label_merged_on_release_branch.py")
closer = signal.closer


# --- reads ----------------------------------------------------------------


def merge_base(base, head="HEAD"):
    """Where this branch left `base`.

    `origin/main..HEAD` is the obvious spelling and it is wrong the moment
    `main` moves during a release's life, which a hotfix does
    (`docs/branch-and-release.md` has the hotfix row). What the release
    carries is what it accumulated since it was cut, and that is measured
    from the fork point.
    """
    return closer.run("git", "merge-base", base, head).strip()


def subjects_since(point, head="HEAD"):
    return closer.run("git", "log", "--format=%s", f"{point}..{head}").splitlines()


def issue_numbers(out):
    return {int(entry["number"]) for entry in json.loads(out)}


def milestone_titles(repo):
    """Every milestone this repository has, open or closed.

    Asked for separately because `gh issue list --milestone` answers a title
    nothing has with an empty list and exit 0 — measured. Without this read a
    mistyped or absent milestone would make the whole check pass while
    verifying nothing, which is the one direction a checker of claims must
    not fail in.
    """
    out = closer.run("gh", "api", f"repos/{repo}/milestones?state=all&per_page=100")
    return {entry["title"] for entry in json.loads(out)}


def open_in_milestone(repo, title):
    """M. `gh issue list` and not the REST `/issues` endpoint: REST counts a
    pull request as an issue and `gh issue list` does not — measured, and it
    matters because a pull request in the milestone could never carry
    `merged: X.Y.Z` and would block the release with nothing anyone could
    do about it."""
    return issue_numbers(
        closer.run(
            "gh",
            "issue",
            "list",
            "--repo",
            repo,
            "--milestone",
            title,
            "--state",
            "open",
            "--limit",
            "1000",
            "--json",
            "number",
        )
    )


def labelled(repo, name):
    """L, in every state. An issue closed by hand mid-release still carries
    the label the signal put on it, and dropping it here would report it as
    `D \\ L` — the signal blamed for a person's edit."""
    return issue_numbers(
        closer.run(
            "gh",
            "issue",
            "list",
            "--repo",
            repo,
            "--label",
            name,
            "--state",
            "all",
            "--limit",
            "1000",
            "--json",
            "number",
        )
    )


# --- the report ------------------------------------------------------------


def listed(numbers):
    return ", ".join(f"#{n}" for n in sorted(numbers)) or "none"


def judge(milestone_open, carried, labels, version):
    """(lines, failed). Pure, so every direction is a case rather than a run.

    Order is the reader's: what stops the release first, then what is only
    being reported, then the two sets the reader needs to check any of it.
    """
    lines, failed = [], False
    milestone, label = signal.milestone_title(version), signal.label_name(version)

    missing = milestone_open - carried
    if missing:
        failed = True
        lines.append(
            f"::error::M \\ D — the milestone {milestone!r} claims "
            f"{len(missing)} open issue(s) this release branch does not "
            f"carry: {listed(missing)}. Either the work is not in, or the "
            f"issues belong in another milestone"
        )

    stray = labels - carried
    if stray:
        failed = True
        lines.append(
            f"::error::L \\ D — {len(stray)} issue(s) carry {label!r} and are "
            f"not in this release: {listed(stray)}. A label naming a release "
            f"the issue is not in is a hand-edit or a squash subject that "
            f"lost its `(#N)`; `gh issue edit <n> --remove-label {label!r}` "
            f"repairs it"
        )

    unlabelled = carried - labels
    if unlabelled:
        lines.append(
            f"D \\ L — the signal missed {len(unlabelled)}: "
            f"{listed(unlabelled)}. Reported, not failed: a release is not "
            f"held for a failure of the signal rather than of its contents"
        )

    unclaimed = carried - milestone_open
    if unclaimed:
        lines.append(
            f"D \\ M — the release carries {len(unclaimed)} that no OPEN "
            f"issue in {milestone!r} claims: {listed(unclaimed)}. Reported, "
            f"not failed: an issue closed by hand mid-release looks exactly "
            f"like this"
        )

    lines.append(f"M (open in {milestone!r}): {listed(milestone_open)}")
    lines.append(f"D (carried by this release branch): {listed(carried)}")
    lines.append(f"L (carrying {label!r}): {listed(labels)}")
    return lines, failed


def main():
    head = os.environ.get("HEAD_BRANCH", "")
    version = signal.version_of(head)
    if version is None:
        # `docs/branch-and-release.md` lists a hotfix branch as the other
        # thing that reaches `main`, and a hotfix carries no release
        # milestone. Skipping is the answer rather than guessing a version.
        print(f"{head!r} is not a release/vX.Y.Z branch — nothing to judge")
        return 0

    repo = os.environ["REPO"]
    base = os.environ.get("BASE", "origin/main")
    milestone = signal.milestone_title(version)

    if milestone not in milestone_titles(repo):
        print(
            f"::warning::no milestone {milestone!r} exists — this run "
            f"verified NOTHING. `gh issue list --milestone` answers a title "
            f"nothing has with an empty list, so the check would otherwise "
            f"pass by measuring an empty set. Passing anyway: a release "
            f"nobody scheduled is a person's call, not this gate's"
        )
        return 0

    carried = set(signal.issues_in(repo, subjects_since(merge_base(base))))
    lines, failed = judge(
        open_in_milestone(repo, milestone),
        carried,
        labelled(repo, signal.label_name(version)),
        version,
    )
    for line in lines:
        print(line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
