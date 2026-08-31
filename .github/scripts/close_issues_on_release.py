#!/usr/bin/env python3
"""Close the issues a release's pull requests said they close.

A closing keyword is read by GitHub only for a pull request whose base is the
default branch. Everything here merges into `release/vX.Y.Z` first, so every
keyword a feature pull request writes is inert -- measured on #37, #38 and
#39, all merged, none fired. The answer existed; nothing acted on it.

This runs when `main` moves. It reads the pull request numbers out of the
commit subjects that arrived, fetches each of those pull request bodies, and
closes what their keywords name.

Three things it deliberately does not do.

**It does not parse the release pull request's own body.** That would be the
same manual step one layer up -- somebody assembling a list, and forgetting.
The keywords are already written, one per feature pull request, by the session
that knew which issue it was answering.

**It never reopens and never comments on an unrelated issue.** The only write
is a close, and a close of an issue already closed is skipped rather than
repeated, so a re-run or a force-push changes nothing.

**A `(#N)` that names no pull request is skipped, not fatal.** People write
that form by hand to name the issue a commit fixes; measured here on a `(#N)`
that names an issue. Everything else still fails loudly.

**It fails loudly.** A closing keyword nobody acted on is the defect this
exists for; a run that swallows its own error would be that defect wearing a
green check.

`DRY_RUN=1` prints what it would close and writes nothing. It exists because
of an incident rather than for tidiness: this script was run by hand against
a real commit range to check its output, and it closed a real issue -- the one
this work item had deliberately left open so the release could be seen closing
it. A tool whose only mode has side effects gets run for its output sooner or
later, and the first person to do it is whoever wrote it.
"""

import json
import os
import re
import subprocess
import sys

# GitHub's own set. Each has to appear immediately before its number -- the
# documentation asks for full syntax for each issue and sanctions no shorter
# form, so `Closes #1, #2` is not read as two here either.
KEYWORDS = (
    "close",
    "closes",
    "closed",
    "fix",
    "fixes",
    "fixed",
    "resolve",
    "resolves",
    "resolved",
)
CLOSING = re.compile(r"\b(?:" + "|".join(KEYWORDS) + r")\s+#(\d+)\b", re.IGNORECASE)
# `feat: … (#100)` -- what a squash merge puts in the subject.
MERGED_PR = re.compile(r"\(#(\d+)\)\s*$")

# GitHub creates no reference from a closing keyword inside a code fence or a
# code span, and neither does this. `docs/branch-and-release.md` carries
# `Closes #88` in a fenced block as the example to copy, so a pull request
# body quoting the document would otherwise close the issue the document
# names -- and this repository's bodies quote its documents routinely.
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
SPAN = re.compile(r"`[^`\n]*`")


def keywords_in(body):
    """Closing keywords GitHub itself would read: prose only."""
    return CLOSING.findall(SPAN.sub(" ", FENCE.sub(" ", body)))


def run(*args):
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"{' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def gh_json(path):
    return json.loads(run("gh", "api", path))


def _issue_api(repo, number):
    """(state_json, exists). A 404 here is input, not a failure.

    A number that names nothing reaches this from two directions: a `(#N)` a
    person typed in a commit subject, and a typo in a merged pull request
    body. Neither is a reason to fail a release -- and a run that died halfway
    would leave the issues after it in the sorted order open, with a re-run
    dying in the same place.
    """
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/issues/{number}"],
        capture_output=True,
        text=True,
    )
    if out.returncode:
        if "Not Found" in out.stderr or "404" in out.stderr:
            return None, False
        sys.exit(f"gh api issues/{number} failed: {out.stderr.strip()}")
    return json.loads(out.stdout), True


def issue_state(repo, number):
    """`open`, `closed`, or None when no such issue exists."""
    data, exists = _issue_api(repo, number)
    return data.get("state") if exists else None


def pull_request_body(repo, number):
    """The body of pull request `number`, or None if it is not one.

    `(#N)` at the end of a subject is what a squash merge writes, and it is
    ALSO something a person writes by hand to name the issue a commit fixes.
    Measured on this repository: `fix: a Target SHA the squash discarded …
    (#61)` names an issue rather than a pull request, and asking
    `repos/…/pulls/61` for it returns 404. A run that treated that as an error
    would fail the whole release for a number somebody typed in a commit
    message.

    So a 404 here is expected input rather than a failure, and it is told
    apart from a real one: anything other than "not found" still stops the
    run. `/issues/N` answers for both kinds and carries a `pull_request` key
    only for a pull request, so one call settles it.
    """
    data, exists = _issue_api(repo, number)
    if not exists or data.get("pull_request") is None:
        return None
    return data.get("body") or ""


def arrived(before, after):
    """Commit subjects new to `main` in this push.

    `before` is all zeroes for a branch's first push. A force-push is NOT
    that case -- it sends the SHA it displaced, and if the runner's clone
    cannot reach it the range fails and the run stops, which is the right
    direction and not the fallback. The fallback reads the tip alone and says
    so, because it drops every pull request behind it: measured, a release
    push whose four pull requests name three issues collects one.
    """
    if not before or set(before) == {"0"}:
        print(
            "WARNING: no `before` commit — reading only the tip. Any pull "
            "request behind it in this push is not seen."
        )
        return run("git", "log", "-1", "--format=%s", after).splitlines()
    return run("git", "log", "--format=%s", f"{before}..{after}").splitlines()


def main():
    before, after = os.environ.get("BEFORE", ""), os.environ["AFTER"]
    repo = os.environ["REPO"]
    dry = os.environ.get("DRY_RUN", "").strip() not in ("", "0", "false", "no")
    if dry:
        print("DRY_RUN — nothing will be written")

    prs = []
    for subject in arrived(before, after):
        found = MERGED_PR.search(subject.strip())
        if found:
            prs.append(int(found.group(1)))
    print(f"pull requests in this push: {prs or 'none'}")

    wanted = {}
    for number in prs:
        body = pull_request_body(repo, number)
        if body is None:
            print(f"#{number} is not a pull request — a hand-written number")
            continue
        for issue in keywords_in(body):
            wanted.setdefault(int(issue), number)
    if not wanted:
        print("no closing keyword in any of them — nothing to close")
        return

    for issue, source in sorted(wanted.items()):
        state = issue_state(repo, issue)
        if state is None:
            print(f"#{issue} does not exist (named by #{source}) — skipping")
            continue
        if state == "closed":
            print(f"#{issue} already closed (named by #{source}) — leaving it")
            continue
        if dry:
            print(f"would close #{issue}, named by #{source}")
            continue
        run(
            "gh",
            "issue",
            "close",
            str(issue),
            "--repo",
            repo,
            "--comment",
            f"Closed by #{source}, which shipped in the release that just "
            f"reached `main`.\n\nIts body carried the keyword; GitHub does not "
            f"read one on a pull request whose base is not the default branch, "
            f"so this workflow acts on it instead. "
            f"`docs/branch-and-release.md` has the reasoning.",
        )
        print(f"closed #{issue}, named by #{source}")


if __name__ == "__main__":
    main()
