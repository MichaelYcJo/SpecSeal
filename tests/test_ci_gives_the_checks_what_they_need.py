"""Two workflow settings decide whether the checks below them mean anything.

Neither is visible from the checks themselves, and both failed silently.

**Checkout depth.** `actions/checkout@v4` fetches one commit unless told
otherwise. Two tests in this suite ask git whether a recorded SHA is an
ancestor of HEAD — the rider stamps and the ledger stamps — and at depth 1 no
SHA is, because no SHA is in the clone at all. Reproduced with
`git clone --depth 1`: `git cat-file -t <a stamped SHA>` answers *Not a valid object
name* and the rider test goes red on every matrix leg.

**Which pull-request events run.** `on: pull_request:` with no `types:` runs
on `opened`, `synchronize` and `reopened` — and on nothing else. A review that
has not finished opens its pull request as a DRAFT, which `chain_check.py`
excuses the checked `Pass` for. Pressing *Ready for review* adds no commit, so
`synchronize` never fires, the workflow never re-runs, and the green the draft
earned stays on that SHA through the merge. The one requirement this branch
added is voided by two clicks and no commit.

These are assertions about YAML, which is not this repository's usual shape
for a test. They are here because the alternative is a comment in the workflow
asking the next editor to remember.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")

# Events GitHub does NOT include by default and that this repository needs,
# because a draft is the documented way past `chain_check.py`'s `Pass`
# requirement (`docs/review-chain-spec.md` §`Pass` has to be checked).
DRAFT_EVENTS = ("ready_for_review", "converted_to_draft")


def strip_comments(text):
    """The workflow with its comment lines removed.

    A setting that exists only in a comment is not a setting. The comment
    above each `types:` list names both draft events, so a substring test on
    the raw trigger passes with the `types:` line itself deleted -- measured:
    dropping the real line and keeping the comment left both checks green,
    which is exactly the edit that reopens the defect they were written for.
    """
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )


def read(name):
    with open(os.path.join(WORKFLOWS, name), encoding="utf-8") as f:
        return strip_comments(f.read())


def workflows():
    return sorted(n for n in os.listdir(WORKFLOWS) if n.endswith((".yml", ".yaml")))


def jobs(text):
    """{job name: its block} — a two-space indent under `jobs:`.

    Hand-parsed rather than with PyYAML, which CI does not install: the
    workflow being read is the one that decides what CI installs, and it
    installs a test runner and a way to run it in parallel -- no parser.
    """
    body = text.split("\njobs:\n", 1)
    assert len(body) == 2, "no `jobs:` block"
    out, name, lines = {}, None, []
    for line in body[1].splitlines():
        m = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if m:
            if name:
                out[name] = "\n".join(lines)
            name, lines = m.group(1), []
            continue
        if name is not None:
            lines.append(line)
    if name:
        out[name] = "\n".join(lines)
    return out


def test_every_job_that_runs_pytest_has_the_whole_history():
    """A check that cannot resolve a SHA is not excused from resolving it."""
    offenders = []
    for name in workflows():
        for job, block in jobs(read(name)).items():
            if "pytest " not in block and "pytest\n" not in block:
                continue
            if "actions/checkout" not in block:
                continue
            if "fetch-depth: 0" not in block:
                offenders.append(f"{name}:{job}")
    assert not offenders, (
        f"jobs that run pytest on a shallow checkout: {offenders}. "
        "`tests/test_a_rider_reaches_its_file.py` and "
        "`tests/test_ledger_stamps_resolve.py` both ask git for ancestry, and "
        "at depth 1 every recorded SHA is missing rather than wrong"
    )


def test_a_pull_request_workflow_reruns_when_a_draft_becomes_ready():
    """Otherwise the draft excuse is permanent rather than temporary.

    `chain_check.py` lets a draft pull request open with an unchecked `Pass`
    because a review still running has to have somewhere to be. That excuse is
    meant to end when the pull request stops being a draft. Without these two
    event types it never does — no commit is needed to leave draft state, and
    no commit means no `synchronize`.
    """
    for name in workflows():
        text = read(name)
        if "\n  pull_request:" not in text:
            continue
        trigger = text.split("\n  pull_request:", 1)[1].split("\njobs:", 1)[0]
        for event in DRAFT_EVENTS:
            assert event in trigger, (
                f"{name}: `on.pull_request` does not list `{event}`. The "
                "default set is opened/synchronize/reopened, so leaving draft "
                "state re-runs nothing and the draft's green is what merges"
            )
