#!/usr/bin/env python3
"""Say whether the plugin directory carries the version that just shipped.

Until 2026-09-16 everybody running this plugin had installed it themselves, so
a release that never reached them was one the owner could see was missing. A
directory listing removes that: the people it reaches are people the owner
cannot name, and `docs/release-checklist.md` §6 had no box that looked (#417).

**This reports. It never fails a release**, and that is the whole design
decision. The directories sync on somebody else's schedule -- measured, one of
the two went twenty-two days without a commit in #417 and twenty-eight by the
time this was written -- so a gate keyed to their state would go red for
something no branch caused, and a red nobody can act on is the interruption
`CLAUDE.md`'s first goal is against. The only non-zero exit here is a
malformed argument, which is the author's mistake rather than the
directories'.

Three facts per directory, which are the three the checklist box asks for:

  listed      is there an entry under this plugin's name
  pinned      which commit that entry names, where it names one
  reachable   whether that commit is an ancestor of `main` in this clone

**What it cannot answer is whether a submission was accepted**, and saying so
is part of the job. That is not readable from anywhere public. Neither is how
an update reaches a plugin that is already listed: the community mirror is
read-only and syncs from a pipeline nobody outside can see, and neither
README says whether a listed plugin's updates are picked up from its source
repository or have to be resubmitted. `questions.md` Q1 carries that as a
person's to find out, and the answer changes nothing here -- a stale pin gets
the same instruction under either one, because resubmitting an entry an
automatic sync would have caught up is unnecessary and never wrong.

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

# The two directory repositories, and the one form that submits to either.
# They live here rather than in a document because they are real
# organisations: `CLAUDE.md` §*no real identifiers in examples or fixtures*
# keeps them out of prose and fixtures, and the script that reads them is
# where a reader can check what was actually read.
DIRECTORIES = (
    ("official", "anthropics/claude-plugins-official"),
    ("community", "anthropics/claude-plugins-community"),
)
MANIFEST = ".claude-plugin/marketplace.json"
PORTAL = "clau.de/plugin-directory-submission"

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
    installed under it. Reading it means a rename shows up as *not listed*
    rather than as a check quietly grading the wrong name.
    """
    with open(
        os.path.join(root, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as handle:
        return json.load(handle)["name"]


def entry_for(text, name):
    """The directory entry named `name`, with the count of entries read.

    `(entry or None, how many, None)` -- or `(None, 0, why not)` where the
    payload cannot be read as a directory at all, which is the same kind of
    report as a failed fetch.
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
        text=True,
    )
    if known.returncode:
        return None
    resolved = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    if resolved.returncode:
        return None
    out = subprocess.run(
        ["git", "-C", root, "merge-base", "--is-ancestor", sha, ref],
        capture_output=True,
        text=True,
    )
    return out.returncode == 0


def line(label, repo, text, error, name, root, ref):
    """One directory's answer, as the lines the checklist box is read with."""
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
        return [
            f"{head} {name!r} is not listed, in {count} entries.",
            f"    Submit it through {PORTAL}. Nothing here can do that, and "
            "nothing here fails for it.",
        ]
    sha, url = pinned(entry)
    if sha is None:
        return [
            f"{head} listed, pinning no commit (source: {url or 'none'}).",
            "    Nothing to compare a release against.",
        ]
    reachable = is_ancestor(root, sha, ref)
    out = [f"{head} listed, pinning {sha[:12]} of {url or 'its own repository'}."]
    if reachable is None:
        out.append(
            f"    Whether {sha[:12]} is an ancestor of {ref} is unknown here — "
            f"this clone does not have that commit, or no {ref}. "
            "`git fetch origin` and run this again."
        )
    elif reachable:
        out.append(
            f"    Reachable from {ref}. Compare it against the commit this "
            "release tagged; where it is behind, the directory has not caught "
            f"up yet — resubmit through {PORTAL}."
        )
    else:
        out.append(
            f"    NOT reachable from {ref}. The directory pins a commit this "
            "repository's history does not contain, which is what a rewritten "
            "or squashed release branch leaves behind."
        )
    return out


def main(argv=None):
    console.to_utf8()
    parser = argparse.ArgumentParser(
        description="Report what the plugin directory carries for this plugin."
    )
    parser.add_argument("--root", default=ROOT, help="repository root (default: this)")
    parser.add_argument("--ref", default="main", help="the ref a pin is compared to")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    name = plugin_name(root)
    print(f"plugin {name!r}, against {args.ref}\n")
    for label, repo in DIRECTORIES:
        text, error = fetch(manifest_url(repo))
        for out in line(label, repo, text, error, name, root, args.ref):
            print(out)
        print()
    print(
        "Whether a submission has been ACCEPTED is readable from nowhere "
        "public, so no answer above is about that."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
