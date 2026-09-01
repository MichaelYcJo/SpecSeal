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
all-or-nothing per row, and fully visible in `git diff`, with the old text
safe in git history. The notice ends "review the diff and commit" because the
write is the beginning of a review, not the end of one.

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
history, so both fail toward a person seeing it; prompt budget — zero
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
LEDGER_GLOBS = (".specseal/map.md", ".specseal/map/*.md", "docs/**/_evidence.md")


def checker():
    spec = importlib.util.spec_from_file_location("specseal_evidence", CHECKER)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    return ec


def ledgers(root):
    return sorted(
        {
            p
            for pat in LEDGER_GLOBS
            for p in glob.glob(os.path.join(root, pat), recursive=True)
        }
    )


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
    rels = [os.path.relpath(p, root) for p in paths]
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
    if not cwd or not os.path.isdir(cwd) or not optin.opted_in(cwd):
        return
    root = optin.repo_root(cwd)
    if not root:
        return

    found = ledgers(root)
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
                        "specseal: the ledger has pre-anchor rows, but "
                        ".specseal/ carries uncommitted changes — not "
                        "touching work in progress. Commit, then the next "
                        "session start migrates (or run "
                        "`evidence-check --migrate .` yourself)."
                    )
                }
            )
        )
        return

    migrated, left = ec.migrate(found, root)
    stamp(root)
    rows = f"{migrated} row{'' if migrated == 1 else 's'}"
    tail = f"; {len(left)} left, run `evidence-check .` to see them" if left else ""
    print(
        json.dumps(
            {
                "systemMessage": (
                    f"specseal: ledger migrated to anchor format ({rows}{tail})"
                    " — review the diff and commit"
                )
            }
        )
    )


if __name__ == "__main__":
    console.to_utf8()
    main()
