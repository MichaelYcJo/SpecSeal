#!/usr/bin/env python3
"""Close the current flow-measurement issue and open the next one.

Issue #109 part 3: the flow log's destination is a `flow-measurement`-labelled
GitHub issue (`skills/verify/SKILL.md`'s "Measure the segment, and feed the
flow log" section, phase 1 of this work item). Nothing closes that issue and
opens the next one on its own -- without this, the log silently stops growing
the day someone finally closes it by hand, and no session notices because the
skill's own lookup treats "no open issue" as a no-op rather than a failure.

This runs from the same workflow, the same trigger, and the same checkout as
`close_issues_on_release.py` (a push to `main` -- a release reaching the
default branch). At that point the release-preparation commit that moved
`.claude-plugin/plugin.json`'s version has already merged as part of the same
push, so the checked-out tree already carries the just-shipped version --
the fact this script's version arithmetic depends on
(`docs/branch-and-release.md` "Cutting a release").

  next_version("0.7.0") -> "0.8.0"     bump the minor, reset the patch
  next_version("0.7.3") -> "0.8.0"     a patch release still bumps the minor

That is a stated default, not a discovered rule: a day this repository ships
a patch release instead of a minor, the title this script writes will name
the wrong version. Nothing depends on the title being correct -- the
mechanism finds its issue by label and open state, never by parsing the
title -- so the cost of a wrong guess is a title a human can retitle by hand,
not a broken lookup (`plan.md` "Judgment recorded").

**The invariant is exactly one open `flow-measurement` issue at a time.**
Zero means the log already stopped and nobody reopened it; two or more means
something else wrote to this label outside this mechanism. Either way this
fails loudly rather than guessing which issue is current -- silently picking
one would make a wrong guess indistinguishable from a right one.

**One retry on a zero-open reading, not on a two-or-more reading.** Phase 1
of this work item measured `gh issue list --label flow-measurement --state
open` returning `[]` immediately after `gh issue edit ... --add-label
flow-measurement` on the very same issue, even though `gh issue view` in the
same breath showed the label applied and the issue open -- GitHub's search
index lagging the write, not a bug in either command. A release does not
write the label it is about to look for (the issue this script closes was
opened by the *previous* release, not by this run), so the race is unlikely
to reach this script in practice -- but a search-index lag can only ever
produce a reading that is short a result, never one with an extra issue in
it. So a zero reading gets one retry after a short sleep before it is trusted
as the real invariant violation; a two-or-more reading is never a lag
artifact and is never retried.

  roll_flow_measurement_issue.py     read REPO, GH_TOKEN from the
                                      environment (same as
                                      close_issues_on_release.py); close the
                                      one open flow-measurement issue and
                                      open the next

Exit codes: 0 done. Non-zero: the open-issue count was not exactly 1 (after
the retry), or a `gh` call failed.
"""

import json
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LABEL = "flow-measurement"
RETRY_DELAY_SECONDS = 5


def run(*args):
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"{' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def next_version(current):
    """`X.Y.Z` -> `X.(Y+1).0`. Pure -- no `gh`, no `git`, no filesystem."""
    major, minor, _patch = (int(part) for part in current.split("."))
    return f"{major}.{minor + 1}.0"


def read_version(root=ROOT):
    with open(
        os.path.join(root, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as f:
        return json.load(f)["version"]


def list_open_issues(repo):
    """The open `flow-measurement` issues, right now, as `gh` reports them."""
    out = run(
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--label",
        LABEL,
        "--state",
        "open",
        "--json",
        "number,title",
    )
    return json.loads(out)


def open_flow_measurement_issues(repo):
    """`list_open_issues`, with one retry when the first reading is empty.

    See the module docstring: an empty reading right after a label write can
    be the search index lagging rather than the true state, and a lag can
    only ever undercount. A reading of two or more is never retried -- it is
    never what a lag produces.
    """
    issues = list_open_issues(repo)
    if not issues:
        time.sleep(RETRY_DELAY_SECONDS)
        issues = list_open_issues(repo)
    return issues


def close_issue(repo, number):
    run(
        "gh",
        "issue",
        "close",
        str(number),
        "--repo",
        repo,
        "--comment",
        "Closed by the release that just reached `main` -- a new "
        "flow-measurement issue opens for the version this release ships "
        "next. `skills/verify/SKILL.md`'s \"Measure the segment, and feed "
        'the flow log" section has the reasoning.',
    )


def open_issue(repo, version):
    title = f"chore: flow measurement — {version}"
    run(
        "gh",
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        title,
        "--label",
        LABEL,
        "--body",
        "",
    )
    return title


def main():
    repo = os.environ["REPO"]
    next_v = next_version(read_version())

    issues = open_flow_measurement_issues(repo)
    if len(issues) != 1:
        sys.exit(
            f"expected exactly one open `{LABEL}` issue, found "
            f"{len(issues)}: {issues}. That invariant is what this script "
            "relies on to know which issue is current -- fix it by hand "
            "rather than let this guess."
        )

    number = issues[0]["number"]
    close_issue(repo, number)
    title = open_issue(repo, next_v)
    print(f"closed #{number}, opened {title!r}")


if __name__ == "__main__":
    main()
