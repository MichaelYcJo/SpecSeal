#!/usr/bin/env python3
"""SessionStart: a pre-anchor ledger migrates itself, once per repo.

`claude plugin update` is the whole of what a user does. The grounds are the
repository's own stated philosophy: between two designs that catch the same
thing, the one that stops to ask a person is the more expensive — and
`--migrate` as a command a person must remember to run is that design. The
command stays for CI and for anyone who wants it by hand; this hook removes
the remembering.

**What licenses writing to a tree unasked.** The ledger is the plugin's own
artifact — the same ownership that lets `preset-setup` replace the CLAUDE.md
marker block without asking — and the operation is deterministic, idempotent,
all-or-nothing per row, and — in shared mode, where the root is committed —
fully visible in `git diff`, with the old text safe in git history. There the
notice ends "review the diff and commit" because the write is the beginning
of a review, not the end of one. A local root (#80) sits under the git
directory, where nothing is in a diff and the rewritten ledger is the only
copy; the same deterministic, all-or-nothing rewrite runs, and the notice
ends by naming what can be read instead: `evidence-check .`.

Boundaries, each pinned in `tests/test_the_ledger_migrates_itself.py`:

  - **never over uncommitted work** — a dirty ledger file is skipped with one
    line saying why, the marker is not stamped, and the ordinary check's
    OLD-FORMAT failure stays loud until a clean session start migrates
  - **once per repo** — an attempt stamps ~/.claude/specseal/ledger-migrated,
    so a repository whose unprovable rows persist is not re-nagged every
    morning; those rows keep failing the check, which is the backstop
  - **never at check time** — reading never rewrites; the plain checker stays
    pure and this hook is the one write moment
  - **silent when there is nothing to migrate** — the every-session scan
    measured at ~24 ms in-process on this repository's own ledgers, ~60 ms
    wall for the whole session-start group, against the checker's ~130 ms
    full run

Rows it cannot prove are left and named in the count, never guessed —
unchanged from `--migrate`, whose engine this calls.

What a change to a gate must carry (`CONTRIBUTING.md`), answered for a hook
that writes: failure direction — wrong-silent leaves the loud OLD-FORMAT
check failure, wrong-write is visible in `git diff` with the old text in git
history in shared mode, and in local mode is what `evidence-check .` reads
next, so both fail toward a person seeing it; prompt budget — zero
questions, one printed line once per repository; platform — pure Python plus
one `git status --porcelain`, no process inspection. Under `dispatch.py`'s
crash isolation a raising hook is skipped silently; here that loses one
migration attempt, and the OLD-FORMAT failure still speaks.
"""

import glob
import importlib.util
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import optin

STATE_DIR = os.path.join(os.path.expanduser("~"), ".claude", "specseal")
MARKER = os.path.join(STATE_DIR, "ledger-migrated")
CHECKER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "skills",
    "evidence-check",
    "scripts",
    "evidence_check.py",
)
# Two of the three live under the root `optin.home_at` resolves — under the
# git directory in local mode (#80) — and the pre-0.10 address stays under the
# repository root, a committed file at an old address.
HOME_GLOBS = ("ledger.md", "ledger/*.md")
ROOT_GLOBS = ("docs/**/_evidence.md",)


def checker():
    spec = importlib.util.spec_from_file_location("specseal_evidence", CHECKER)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    return ec


def ledgers(root, home=None):
    home = home or optin.home_at(root)
    patterns = [os.path.join(root, pat) for pat in ROOT_GLOBS]
    if home:
        patterns += [os.path.join(home, pat) for pat in HOME_GLOBS]
    return sorted({p for pat in patterns for p in glob.glob(pat, recursive=True)})


def attempted(root):
    try:
        with open(MARKER, encoding="utf-8") as f:
            return root in f.read().splitlines()
    except OSError:
        return False


def stamp(root):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(MARKER, "a", encoding="utf-8") as f:
            f.write(root + "\n")
    except OSError:
        pass


def dirty(root, paths):
    """True when any ledger carries uncommitted changes — or git cannot say.

    Work in progress outranks the migration, and an unanswerable question is
    treated as work in progress: overwriting on a guess is the one direction
    this hook must never fail in.
    """
    # Forward slashes always: git pathspecs are slash-separated on every
    # platform, and a backslash pathspec on Windows would read as permanently
    # dirty — the migration never running, with a wrong reason printed
    # (round 4, ❓; the broad gate's windows leg gives the real answer).
    #
    # Only paths inside the tree are asked about. A local-mode ledger lives
    # under the git directory (#80), where nothing is ever committed, so
    # "uncommitted" has no meaning for it — and from a linked worktree its
    # path climbs out of the tree, which git refuses (`is outside
    # repository`, exit 128) and this function then read as dirty forever.
    #
    # A path with no relative spelling at all — on Windows, a root on another
    # drive than the tree, where `ntpath.relpath` raises `ValueError` — is
    # outside the tree by definition, and is skipped the same way rather
    # than raised out of `main()` at session start (round 1 of #80, 🔴 2).
    rels = []
    for p in paths:
        try:
            rel = os.path.relpath(p, root).replace(os.sep, "/")
        except ValueError:
            continue
        if rel.startswith("../") or rel.startswith(".git/"):
            continue
        rels.append(rel)
    if not rels:
        return False
    try:
        r = subprocess.run(
            ["git", "-C", root, "status", "--porcelain", "--", *rels],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return True
    return r.returncode != 0 or bool(r.stdout.strip())


def main():
    try:
        event = json.load(sys.stdin) or {}
        cwd = event.get("cwd")
    except (ValueError, AttributeError):
        return
    if not cwd or not os.path.isdir(cwd):
        return
    root = optin.repo_root(cwd)
    home = optin.home_at(root)
    if not root or not home:
        return

    found = ledgers(root, home)
    if not found:
        return
    ec = checker()
    if not any(ec.old_format_rows(ec.read(p) or "") for p in found):
        return
    if attempted(root):
        return  # once per repo; the OLD-FORMAT check failure is the backstop
    if dirty(root, found):
        print(
            json.dumps(
                {
                    "systemMessage": (
                        "specseal: the ledger has pre-anchor rows, but a "
                        "ledger file carries uncommitted changes — not "
                        "touching work in progress. Commit, then the next "
                        "session start migrates (or run "
                        "`evidence-check --migrate .` yourself)."
                    )
                }
            )
        )
        return

    migrated, left, unproven = ec.migrate(found, root)
    stamp(root)
    rows = f"{migrated} row{'' if migrated == 1 else 's'}"
    tail = f"; {len(left)} left, run `evidence-check .` to see them" if left else ""
    # The warning the CLI prints belongs here MORE, not less: this path runs
    # without anyone asking for it, and `stamp(root)` above means it is never
    # offered again (round 5, 🟡 E).
    warn = (
        f"; {unproven} rewritten without the since-the-stamp proof, resting on "
        "the current tree alone"
        if unproven
        else ""
    )
    # "Review the diff" is a shared-mode sentence: the root is committed, so
    # the rewrite is in a diff and the old text is in history. A local root
    # (#80) lives under the git directory, where nothing is in a diff and the
    # rewritten ledger is the only copy — so the line names what CAN be read
    # (round 1 of #80, 🟡 5). Local is "not the shared root", whichever
    # tree the session sits in: from a linked worktree the root is under the
    # main tree's common directory, which is not under this tree at all.
    shared = os.path.normcase(os.path.normpath(home)) == os.path.normcase(
        os.path.normpath(os.path.join(root, optin.HOME))
    )
    ending = (
        "review the diff and commit"
        if shared
        else "this root has no git history, so run `evidence-check .` to read "
        "the result"
    )
    print(
        json.dumps(
            {
                "systemMessage": (
                    f"specseal: ledger migrated to anchor format ({rows}{tail}"
                    f"{warn}) — {ending}"
                )
            }
        )
    )


if __name__ == "__main__":
    console.to_utf8()
    main()
