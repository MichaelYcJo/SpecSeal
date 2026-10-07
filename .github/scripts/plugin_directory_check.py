#!/usr/bin/env python3
"""Say what the two marketplace files hold for this plugin -- and that the
directory was not read.

Until 2026-09-16 everybody running this plugin had installed it themselves, so
a release that never reached them was one the owner could see was missing. A
listing in the directory -- the catalog people browse inside Claude -- removes
that: the people it reaches are people the owner cannot name, and
`docs/release-checklist.md` §6 had no box that looked (#417).

**The directory itself is not read here, because no script can read it.**
Measured 2026-10-07: three of its pages answered HTTP 403 with a challenge
page, to a plain client and to one carrying a browser user agent, and the
documentation's index names no API for it (#858). What a script can read is
the two marketplace files below, the public `.claude-plugin/marketplace.json`
files: the community one calls itself a read-only mirror synced nightly from
the review pipeline, and the official one takes outside plugins through the
same submission. They are outputs of that pipeline and not the directory, so
an absent entry in them says nothing about whether the plugin is published
there. This used to print *not listed* and send the reader to submit, about a
catalog it never read, on the day the owner's Console page showed the plugin
published. The run now ends by saying the directory was not read and naming
the page a person opens instead.

**Three facts from the documentation, read 2026-10-07**, which are why that
closing names two pages and sends nobody to resubmit:

  - a plugin submitted at the developer portal takes new versions on its
    own: a merge to the tracked branch is scanned and published, and nothing
    is resubmitted;
  - a listing made through the earlier Console form takes no new version
    until a person moves it to the portal;
  - *Published* is the only installable status, and *Not live yet* is a
    status of its own -- marked published, with nothing listed yet.

**This reports. It never fails a release**, and that is the whole design
decision. The marketplace files sync on somebody else's schedule -- measured,
one of the two went twenty-two days without a commit in #417 and twenty-eight
by the time this was first written -- so a gate keyed to their state would go
red for something no branch caused, and a red nobody can act on is the
interruption `CLAUDE.md`'s first goal is against. The only non-zero exit here
is a malformed argument, which is the author's mistake rather than the
files'.

Three facts per marketplace file, which are the three the checklist box asks
for:

  entry       is there an entry under this plugin's name, and over how many
  pinned      which commit that entry names, where it names one
  reachable   whether that commit is an ancestor of `main` in this clone

**Four entry shapes, not one.** Measured 2026-09-22 over both files: of
official's 310 entries, 157 carry `source` as an object with `url` and `sha`,
96 add `path` and `ref`, 5 add `path` alone, and **52 carry `source` as a
plain string** -- `./plugins/<name>`, the in-repository shape, with no url and
no sha to read at all. Community's 2,282 split the same way and add 3 entries
with a `url` and a `ref` and no `sha`. So a reader that assumed
`entry["source"]["sha"]` would raise on the 57 entries that have no such
thing, and it is a listing of somebody else's file: the shapes in it are not
this repository's to hold steady.

**It reads over HTTPS through `api.github.com`** rather than a raw-content
host. `tests/test_no_real_identifiers.py` allows `github.com` and every
subdomain of it, and is silent on the host GitHub serves raw file bodies
from; extending that allowlist to read a file the documented API already
serves would spend the repository's own rule for nothing -- and the sweep
refuses the host's NAME in the tree, so a comment explaining the choice by
spelling it out is itself the violation. No credentials are needed for a
public
file. `.claude-plugin/marketplace.json` is the path -- measured, the root
`marketplace.json` both the ticket and `spec.md` name is 404 in both
repositories.

  plugin_directory_check.py             read both, report
  plugin_directory_check.py --root DIR  read the plugin name and git from DIR
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "hooks")
)
import console

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# The two repositories holding the marketplace files, and the two pages a
# person opens for the directory's own answer. They live here rather than in a
# document because they are real organisations' addresses: `CONTRIBUTING.md`
# §*House rules*, *No real identifiers*, keeps them out of prose and fixtures,
# and the script that reads or names them is where a reader can check what was
# actually read and what was not.
MARKETPLACES = (
    ("official", "anthropics/claude-plugins-official"),
    ("community", "anthropics/claude-plugins-community"),
)
MANIFEST = ".claude-plugin/marketplace.json"
# The developer portal, where a portal listing's status and live version are.
SUBMISSIONS_PAGE = "https://claude.ai/directory/manage"
# The earlier submission form's page, where a Console listing is.
CONSOLE_PAGE = "https://platform.claude.com/plugins/submissions"

TIMEOUT = 20


def manifest_url(repo):
    """The documented API path to a public file, on an allowed host."""
    return f"https://api.github.com/repos/{repo}/contents/{MANIFEST}"


def fetch(url):
    """`(the text, None)`, or `(None, why not)`.

    A failed read is a report rather than a failure, for the reason at the top
    of this file: the thing that failed is somebody else's server, and a
    release that stops for it stops for nothing anyone here can fix.
    """
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github.raw"}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.read().decode("utf-8"), None
    except urllib.error.HTTPError as error:
        return None, f"HTTP {error.code}"
    except Exception as error:
        return None, f"{type(error).__name__}: {error}"


def plugin_name(root):
    """This plugin's name, from its own manifest rather than a literal.

    A literal here would be a second place the name is written down, and the
    name is the thing that cannot change any more -- users have the plugin
    installed under it. Reading it means a rename shows up as *not an entry*
    rather than as a check quietly grading the wrong name.
    """
    with open(
        os.path.join(root, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as handle:
        return json.load(handle)["name"]


def entry_for(text, name):
    """The marketplace file's entry named `name`, with the count of entries read.

    `(entry or None, how many, None)` -- or `(None, 0, why not)` where the
    payload cannot be read as a marketplace file at all, which is the same
    kind of report as a failed fetch.
    """
    try:
        payload = json.loads(text)
    except ValueError as error:
        return None, 0, f"not JSON: {error}"
    entries = payload.get("plugins") if isinstance(payload, dict) else payload
    if not isinstance(entries, list):
        return None, 0, "no `plugins` list"
    for entry in entries:
        if isinstance(entry, dict) and entry.get("name") == name:
            return entry, len(entries), None
    return None, len(entries), None


def pinned(entry):
    """`(the commit this entry pins, the repository it points at)`.

    Either may be None. A `source` that is a plain string is the
    in-repository shape and pins nothing; an object may carry `url` without
    `sha`, which three community entries do.
    """
    source = entry.get("source")
    if not isinstance(source, dict):
        return None, source if isinstance(source, str) else None
    return source.get("sha"), source.get("url")


def is_ancestor(root, sha, ref):
    """Whether `sha` is an ancestor of `ref` here — or None if it cannot say.

    A commit the clone does not have is not a commit that is unreachable, and
    reporting the two as one would turn a shallow or unfetched checkout into
    a stale-pin warning. So the third answer exists and is printed as itself.
    """
    known = subprocess.run(
        ["git", "-C", root, "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True,
        encoding="utf-8",
    )
    if known.returncode:
        return None
    resolved = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        capture_output=True,
        encoding="utf-8",
    )
    if resolved.returncode:
        return None
    out = subprocess.run(
        ["git", "-C", root, "merge-base", "--is-ancestor", sha, ref],
        capture_output=True,
        encoding="utf-8",
    )
    return out.returncode == 0


def line(label, repo, text, error, name, root, ref):
    """One marketplace file's answer, as the lines the checklist box is read
    with.

    An absent entry is one line and the whole answer: which file, over how
    many entries. It names no act, because the file is not the directory and
    nothing here read the directory (#858).
    """
    head = f"{label} ({repo}):"
    if error:
        return [
            f"{head} could not be read — {error}.",
            "    Not a release problem and not a reason to stop: this reads "
            "somebody else's repository.",
        ]
    entry, count, unreadable = entry_for(text, name)
    if unreadable:
        return [f"{head} could not be read — {unreadable}."]
    if entry is None:
        return [f"{head} {name!r} is not an entry in this file ({count} entries)."]
    sha, url = pinned(entry)
    if sha is None:
        return [
            f"{head} an entry, pinning no commit (source: {url or 'none'}).",
            "    Nothing to compare a release against.",
        ]
    reachable = is_ancestor(root, sha, ref)
    out = [f"{head} an entry, pinning {sha[:12]} of {url or 'its own repository'}."]
    if reachable is None:
        out.append(
            f"    Whether {sha[:12]} is an ancestor of {ref} is unknown here — "
            f"this clone does not have that commit, or no {ref}. "
            "`git fetch origin` and run this again."
        )
    elif reachable:
        out.append(
            f"    Reachable from {ref}. Compare it against the commit this "
            "release tagged; where it is behind, this file has not caught up "
            "yet, and nothing here moves it."
        )
    else:
        out.append(
            f"    NOT reachable from {ref}. This file pins a commit this "
            "repository's history does not contain, which is what a rewritten "
            "or squashed release branch leaves behind."
        )
    return out


def closing():
    """What the run did not read, and the page a person opens instead.

    The directory answers a challenge page to any script (measured 2026-10-07,
    #858), so its state is not among what this run says. Which page answers
    *is it published, and at which version* depends on the kind of listing,
    and the run cannot see the kind either, so it names both.
    """
    return [
        "The directory -- the catalog people browse inside Claude -- was not "
        "read: no script can reach it, so nothing above says whether this "
        "plugin is published there.",
        "A person opens the page for the kind of listing it has:",
        f"    a portal listing:  the portal's Submissions page, {SUBMISSIONS_PAGE}"
        " -- its status, and the version that is live",
        f"    a Console listing: the Console page, {CONSOLE_PAGE}",
        "A portal listing takes new versions from its tracked branch on its "
        "own; a Console listing takes none until it is moved to the portal.",
    ]


def main(argv=None):
    console.to_utf8()
    parser = argparse.ArgumentParser(
        description="Report what the two marketplace files hold for this plugin."
    )
    parser.add_argument("--root", default=ROOT, help="repository root (default: this)")
    parser.add_argument("--ref", default="main", help="the ref a pin is compared to")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    name = plugin_name(root)
    print(f"plugin {name!r}, against {args.ref}\n")
    for label, repo in MARKETPLACES:
        text, error = fetch(manifest_url(repo))
        for out in line(label, repo, text, error, name, root, args.ref):
            print(out)
        print()
    for out in closing():
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
