#!/usr/bin/env python3
"""Publish the GitHub Release for the tag that was just pushed.

Publishing a release note was a habit and nothing else. `docs/release-checklist.md`
walked to the tag and stopped, no workflow did it, and **three consecutive
releases shipped without one** -- measured on 2026-09-13 while cutting a
release, by the run that would have made it four (#386). The tag beside it
gets done every time, because `hooks/version-check.py` reads it and an
untagged release is one no installed session is ever told about. The note had
no reader in the tree at all, so nothing noticed its absence.

So this reads the tag instead of asking anybody to remember. It runs when a
`v*` tag is pushed, which is the release's last manual act and the moment
`docs/branch-and-release.md` says stays a person's.

**The body is the `CHANGELOG.md` section the preparation commit gathered.**
By the time the tag exists that section is written, reviewed and on `main`:
`gather_changelog.py --version X.Y.Z` wrote it and the hygiene workflow ran
`--check` over it at the release pull request. Nothing here composes prose.

**The title comes from the tagged commit's message**, which carries the
`release: X.Y.Z -- <symptoms>` line `docs/release-checklist.md` §5
prescribes. Three other sources were measured and rejected: the merge
commit's *subject* is GitHub's `Merge pull request #N from <owner>/...` line
and not the title at all; the `## X.Y.Z -- <date>` changelog heading carries
a date and no prose, so a title taken from it drops the symptom line every
existing release carries; and the twenty-three hand-written release names
reproduce neither the pull request titles nor the changelog headings, so
nothing can reproduce them. §5's line is the only written-down source, and so
the only one anything can read.

Three things it deliberately does not do.

**It never republishes.** A release already at the tag is left exactly as it
is -- printed and exited 0 -- so a re-pushed tag and a re-run job change
nothing. The note may have been edited by hand after it was published, and
overwriting that is the one way this could destroy something a person wrote.

**It does not fail a release for a missing title line.** Nothing holds that
convention -- `gather_changelog.py --check` holds the changelog section and
no check holds the commit subject -- so a missing line falls back to the tag
name and says in the job log which branch it took. A wrong title is visible
on the releases page and fixable in one edit; a failed job at the tag is a
release that stops after `main` has already moved.

**It does fail for a missing changelog section**, which is the opposite
direction on purpose. That is the release shipping unexplained, and the body
is the whole of what this publishes.

**It thanks every outside contributor, by handle, under the body** (#572).
An outside contribution carries no work item and so no changelog fragment,
so a release that carried one credited it only when somebody remembered to
write a sentence about it. So the set is read, not remembered: the pull
requests merged into `release/vX.Y.Z`, less the repository owner's and any
bot's, one line per person naming each pull request. A release with no such
pull request gets no section, and reads exactly as it did before. It adds no
way to fail: a `gh` call that cannot list the pull requests publishes the
note without the section and says so in the job log, because a missing
credit is fixable in one edit and a failed job at the tag is not.

`DRY_RUN=1` prints what it would create and writes nothing, for the reason
`close_issues_on_release.py`'s docstring gives: a tool whose only mode has
side effects gets run for its output sooner or later, and the first person to
do it is whoever wrote it.

Environment: `TAG` (`github.ref_name`), `REPO`, `GH_TOKEN`.

Exit codes: 0 published, or already published, or a dry run -- 1 the tag is
not `vX.Y.Z`, or `CHANGELOG.md` carries no section for it.
"""

import json
import os
import re
import subprocess
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hooks")
)
import console

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CHANGELOG = "CHANGELOG.md"

# `vX.Y.Z`. Anything else under `v*` -- `v1.2`, `vnext`, a typo -- is a shape
# this cannot name a version for, and it says so rather than guessing one.
# `label_merged_on_release_branch.py#version_of` refuses a branch name the
# same way and for the same reason.
TAG_RE = re.compile(r"^v(\d+\.\d+\.\d+)$")


# The title line `docs/release-checklist.md` §5 prescribes for the release
# pull request, which is what the merge commit's body carries.
#
# **The symptoms are required, not optional.** `release: 0.12.3` with nothing
# after it was measured in this repository's own history, and reading a title
# out of it yields the version alone -- which is the tag name with the `v`
# removed, so the two branches would differ by one character and the log line
# saying which was taken would be telling a reader nothing. A line with no
# symptoms is not the prescribed line, so it takes the fallback and says so.
def title_line_re(version):
    return re.compile(
        r"^release:\s*" + re.escape(version) + r"\s+—\s*(\S.*?)\s*$", re.M
    )


# The heading `gather_changelog.py#section` writes, with its date left open.
# The two are held against each other by
# `tests/test_a_release_publishes_its_note.py#test_the_reader_reads_what_the_gatherer_writes`
# rather than by this comment: that script has no section READER to import --
# it writes sections and finds the first `## ` line to insert above -- so what
# is owed is a case proving this pattern reads that writer's output, not a
# second hand-checked copy of the format.
def section_heading_re(version):
    return re.compile(r"^## " + re.escape(version) + r"\b.*$", re.M)


def run(*args):
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"{' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def version_of(tag):
    """`X.Y.Z` for a `vX.Y.Z` tag, or None for any other name."""
    found = TAG_RE.match((tag or "").strip())
    return found.group(1) if found else None


def section_body(text, version):
    """The released section's body for `version`, or None if there is none.

    From the line after the `## X.Y.Z -- <date>` heading to the line before
    the next `## ` heading, stripped. The heading itself is left out: it
    carries the date, which GitHub already shows beside the release.
    """
    found = section_heading_re(version).search(text)
    if not found:
        return None
    rest = text[found.end() :]
    after = re.search(r"^## ", rest, re.M)
    body = rest[: after.start()] if after else rest
    return body.strip()


def title_from(message, version, tag):
    """`(the release title, where it came from)`.

    The second element is what the job log prints. A title a reader cannot
    trace to a source is one nobody can correct at the right end.
    """
    found = title_line_re(version).search(message or "")
    if found:
        return f"{version} — {found.group(1)}", "the tagged commit's `release:` line"
    return tag, "the tag name — the tagged commit carries no `release:` line"


def commit_message(tag):
    """The message of the commit `tag` names.

    `%B` is the raw body, so the `release:` line reaches this whether it sits
    in the subject or below it. In this repository it is below: the tagged
    commit is the release merge, whose subject GitHub writes as
    `Merge pull request #N from <owner>/release/vX.Y.Z`.
    """
    return run("git", "log", "-1", "--format=%B", tag)


def release_exists(repo, tag):
    """Whether a GitHub Release already sits at `tag`.

    A 404 here is the answer rather than a failure -- the usual case is that
    no release exists yet, which is the whole reason this job runs. Anything
    else still stops the run, because a token without the scope to read
    releases would otherwise be read as "none exists" and publish a second.
    """
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/releases/tags/{tag}"],
        capture_output=True,
        text=True,
    )
    if out.returncode:
        if "Not Found" in out.stderr or "404" in out.stderr:
            return False
        sys.exit(f"gh api releases/tags/{tag} failed: {out.stderr.strip()}")
    return True


THANKS_HEADING = "### 🙌 Thanks to"


def merged_pulls(repo, version):
    """The pull requests merged into `release/v<version>`, or None.

    Each is `{"number", "title", "author": {"login", "is_bot"}}` as
    `gh pr list --json` prints it. None means the list could not be read, and
    the caller publishes without a credit rather than failing the tag's job.
    """
    out = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--base",
            f"release/v{version}",
            "--state",
            "merged",
            "--limit",
            "500",
            "--json",
            "number,title,author",
        ],
        capture_output=True,
        text=True,
    )
    if out.returncode:
        print(f"gh pr list failed, so the note carries no credit: {out.stderr.strip()}")
        return None
    try:
        return json.loads(out.stdout)
    except ValueError:
        print(
            "gh pr list printed something that is not JSON, so the note carries no credit"
        )
        return None


def thanks_section(pulls, owner):
    """`### 🙌 Thanks to` and one line per outside contributor, or "".

    Outside means neither `owner` -- the repository's, read from `REPO` and
    never written down here -- nor a bot, whether `gh` marks it one or its
    login carries the `[bot]` suffix. A person with several pull requests gets
    one line naming them all, oldest first; the lines are ordered by the
    contributor's first pull request, so the order is the release's own.
    """
    by_login = {}
    for pull in sorted(pulls or (), key=lambda p: p["number"]):
        author = pull.get("author") or {}
        login = author.get("login") or ""
        if not login or login.lower() == owner.lower():
            continue
        if author.get("is_bot") or login.endswith("[bot]") or login.startswith("app/"):
            continue
        by_login.setdefault(login, []).append(pull)
    if not by_login:
        return ""
    lines = [THANKS_HEADING, ""]
    for login, mine in by_login.items():
        named = "; ".join(f"{p['title'].strip()} (#{p['number']})" for p in mine)
        lines.append(f"- **@{login}** — {named}")
    return "\n".join(lines)


def create(repo, tag, title, body):
    run(
        "gh",
        "release",
        "create",
        tag,
        "--repo",
        repo,
        "--title",
        title,
        "--notes",
        body,
    )


def main(argv=None):
    console.to_utf8()
    tag = os.environ["TAG"].strip()
    repo = os.environ["REPO"]
    dry = os.environ.get("DRY_RUN", "").strip() not in ("", "0", "false", "no")
    if dry:
        print("DRY_RUN — nothing will be written")

    version = version_of(tag)
    if version is None:
        print(
            f"{tag!r} is not a vX.Y.Z tag, so there is no changelog section "
            "to name. Nothing published."
        )
        return 1

    path = os.path.join(ROOT, CHANGELOG)
    with open(path, encoding="utf-8") as handle:
        body = section_body(handle.read(), version)
    if body is None:
        print(
            f"{tag} was pushed and {CHANGELOG} carries no `## {version}` "
            "section, so this release would be published with no notes at "
            "all.\n"
            "Release preparation gathers the fragments into that section:\n"
            "  python3 .github/scripts/gather_changelog.py --version "
            f"{version}"
        )
        return 1

    if release_exists(repo, tag):
        print(
            f"a release already exists at {tag} — leaving it. Nothing here "
            "overwrites a note, because one may have been edited by hand "
            "after it was published"
        )
        return 0

    title, source = title_from(commit_message(tag), version, tag)
    print(f"title {title!r}, from {source}")
    pulls = merged_pulls(repo, version)
    thanks = thanks_section(pulls, repo.split("/")[0])
    if thanks:
        body = f"{body}\n\n{thanks}"
        print(thanks)
    elif pulls is not None:
        print("no outside contribution in this release, so no Thanks to section")
    if dry:
        print(f"would create the release at {tag} with {len(body)} characters of notes")
        return 0
    create(repo, tag, title, body)
    print(f"published the release at {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
