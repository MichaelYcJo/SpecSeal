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

**The issue this opens carries a body, and finds the durable log by label.**
A rolling log opened with `--body ""` is born with no path back to the one it
replaced and no statement of what it is for, which is the state every log
before this change was in (#136). The body names the issue just closed, says
the log closes when this version ships, and points at the durable ledger --
the issue carrying `flow-baseline`, looked up the same way the rolling one is
and never by number. Where a repository has no such issue that clause is left
out rather than the roll failing: a durable ledger is a thing a repository may
not have, and a release is not the place to insist on one.

**The index label and the milestone are best-effort, and a failure to set
either is written into the body of the issue this just created.** `gh issue
create` resolves labels and milestones before it creates anything, so a
milestone somebody renamed or deleted fails the whole call -- and a milestone
is repository state, not code. The invariant this script protects is the
one-open rule, which neither argument touches, so a release does not stop for
them. The create is attempted with both, then with the index label alone, then
with neither, and each fallback carries into the body what the attempt above
it could not set. The body is where that goes because it is the one artifact
a person opens; a line in a workflow log is not read (#136).

**A failed attempt re-reads the open-issue list before it retries.** A `gh
issue create` that fails after the mutation lands would, on retry, open a
second issue -- the exactly-one-open invariant broken from the other side, by
the script that exists to keep it. So a failure is followed by the lookup, and
a reading that is no longer empty ends the ladder with the issue that landed.
The last rung uses `run` rather than `try_run`, so a create that fails all the
way down still exits loudly into the recovery message below.

**The index label and the milestone are this repository's own names, and they
belong here rather than in the skill.** `skills/verify/SKILL.md` ships to
repositories that have neither, so it names `flow-measurement` and
`flow-baseline` and stops there. `.github/` stays home
(`tests/test_the_release_check_watches_what_ships.py`), which is what lets
this file name `measurement` and `log: measurement`.

**The close and the open are not one transaction.** `main` closes the old
issue first and only then opens the next one, so a `gh issue create` failure
after a successful close leaves the flow-measurement log with zero open
issues -- the same state the exactly-one-open invariant above exists to
catch, except now self-inflicted rather than found on the next run. The
failure message names both facts: which issue was already closed, and the
title a human should open by hand to restore the invariant before the next
release runs. Ordering the close first is a stated trade-off, not an
oversight it would be better to fix by making the open ordered first: opening
before closing would leave two open issues rather than zero on any of this
script's own failures after the create, which is the exact reading the
retry-once hardening above treats as never a lag artifact and always the
invariant broken -- closing first turns every failure mode into a state the
existing zero-issue recovery already tells the operator how to fix by hand.

Exit codes: 0 done. Non-zero: the open-issue count was not exactly 1 (after
the retry), a `gh` call failed, or the close succeeded and the open then
failed (message names the closed issue and the recovery title).
"""

import json
import os
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LABEL = "flow-measurement"
BASELINE_LABEL = "flow-baseline"
INDEX_LABEL = "measurement"
INDEX_MILESTONE = "log: measurement"
RETRY_DELAY_SECONDS = 5

MILESTONE_NOTE = (
    f"The `{INDEX_MILESTONE}` milestone could not be set on this issue -- it "
    f"has been renamed, deleted, or is not resolvable from the release "
    f"workflow. Set it by hand if it still exists. Nothing automated reads a "
    f"milestone (`docs/issues-and-milestones.md`), so this costs a person a "
    f'wrong answer to "what is in this version" and costs no check anything.'
)

BASELINE_AMBIGUOUS_NOTE = (
    f"More than one open `{BASELINE_LABEL}` issue, so this one points at no "
    f"durable ledger. That label carries the same exactly-one-open invariant "
    f"the rolling log does, and naming a broken invariant is what this does "
    f"instead of picking whichever the search listed first."
)

INDEX_NOTE = (
    f"The `{INDEX_LABEL}` index label could not be applied either. Add it by "
    f"hand so this issue turns up beside the durable ledger when the whole "
    f"concern is queried by label."
)


def run(*args):
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"{' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def try_run(*args):
    """`run` without the exit -- `None` where the call failed.

    For the parts of this script whose failure must not stop a release: the
    durable ledger's lookup, and the best-effort arguments to the create. None
    of them touches the exactly-one-open invariant, which is the thing worth
    failing a release over.
    """
    out = subprocess.run(args, capture_output=True, text=True)
    return None if out.returncode else out.stdout


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


def find_baseline_issue(repo):
    """The durable measurement ledger, by label: `(number, note)`.

    Best-effort in every direction: a repository that never created
    `flow-baseline` has no durable ledger, a `gh` failure here is not worth a
    release, and either way the body simply leaves the clause out. The lookup
    is the rolling log's own shape -- a label, never a number -- because a
    number goes stale the moment its issue closes, which is what `#109`
    removed from the rolling log's lookup for the same reason.

    **The note separates two silences.** No durable ledger is the ordinary
    case and says nothing, because a note about it would appear on every
    rolling log every repository ever opens. Two or more open is that label's
    invariant broken, and it answers `None` with a note rather than taking
    the first: `skills/verify/SKILL.md` gives both labels the same
    exactly-one-open rule and says a broken invariant is named rather than
    guessed at, and a body carrying one of two numbers looks exactly like a
    body carrying the only one.
    """
    out = try_run(
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--label",
        BASELINE_LABEL,
        "--state",
        "open",
        "--json",
        "number",
    )
    if not out:
        return None, None
    try:
        issues = json.loads(out)
    except ValueError:
        return None, None
    if len(issues) > 1:
        return None, BASELINE_AMBIGUOUS_NOTE
    return (issues[0]["number"], None) if issues else (None, None)


def issue_body(version, closed_number, baseline_number, notes=()):
    """What the rolling log says about itself on the day it is opened.

    `notes` are what the create could not set -- see the module docstring.
    They go in the body rather than in the workflow log because the issue is
    the artifact a person opens.
    """
    ledger = (
        f"Baselines and the observations that span versions live in "
        f"#{baseline_number}; this"
        if baseline_number is not None
        else "This"
    )
    opening = (
        f"Rolls from #{closed_number}. {ledger} issue takes one comment per "
        f"segment and is closed when {version} ships."
    )
    return "\n\n".join([opening, *notes])


def create_args(repo, title, body, extras):
    return (
        "gh",
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        title,
        "--label",
        LABEL,
        *extras,
        "--body",
        body,
    )


def landed_create(repo, closed_number):
    """An open `flow-measurement` issue that is not the one `main` just closed.

    The ladder's guard. `closed_number` is excluded because the reading can
    still carry it: `gh issue list` lagging a write is what this module's
    docstring records, and a lag behind a *close* is a reading with an extra
    issue in it rather than one short a result. The empty reading gets the
    same one retry `open_flow_measurement_issues` gives it, and for the same
    reason -- a lag behind the create sends the ladder on to open a second.
    """
    for attempt in (0, 1):
        if attempt:
            time.sleep(RETRY_DELAY_SECONDS)
        landed = [i for i in list_open_issues(repo) if i["number"] != closed_number]
        if landed:
            return True
    return False


def open_issue(repo, version, closed_number):
    title = f"chore: flow measurement — {version}"
    baseline, baseline_note = find_baseline_issue(repo)
    ledger_notes = (baseline_note,) if baseline_note else ()

    # Most to least. Each rung drops the argument the rung above it could not
    # set and says so in the body; only `LABEL` is on every rung, because that
    # is the one the exactly-one-open invariant is read through.
    for extras, notes in (
        (("--label", INDEX_LABEL, "--milestone", INDEX_MILESTONE), ()),
        (("--label", INDEX_LABEL), (MILESTONE_NOTE,)),
    ):
        body = issue_body(version, closed_number, baseline, (*notes, *ledger_notes))
        if try_run(*create_args(repo, title, body, extras)) is not None:
            return title
        if landed_create(repo, closed_number):
            # The call reported failure and an issue that is not the one just
            # closed is open, so the create landed and the failure arrived
            # after it. Retrying here opens a second one.
            return title

    body = issue_body(
        version, closed_number, baseline, (MILESTONE_NOTE, INDEX_NOTE, *ledger_notes)
    )
    run(*create_args(repo, title, body, ()))
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
    try:
        title = open_issue(repo, next_v, number)
    except SystemExit as exc:
        sys.exit(
            f"closed #{number}, but opening the next issue failed: {exc}. "
            f"Check the `{LABEL}` label before opening anything: a create "
            f"that failed may still have landed. Where none is open, open "
            f"one by hand (label `{LABEL}`, title `chore: flow measurement — "
            f"{next_v}`) before the next release runs."
        )
    print(f"closed #{number}, opened {title!r}")


if __name__ == "__main__":
    main()
