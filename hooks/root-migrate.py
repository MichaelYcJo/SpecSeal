#!/usr/bin/env python3
"""SessionStart: the old roots move into `seal/`, once per repository.

0.4.0 laid the plugin's tree out by lifetime under one root. `.specseal/` held
the ledger, the migration config and the follow-up list; `specs/<id>/` held a
work item's documents and its review records; both are `seal/` now, and the
opt-in is that root's presence (`docs/one-root-by-lifetime.md`, "What happens
to the existing directories at the switch"). Nothing reads the old names after
that release except this hook, so a repository still holding the old layout
gets silence from every gate until this runs. That silence is the fail
direction the design record keeps on purpose, and this hook is what ends it.

`hooks/ledger-migrate.py` is the model, and the same grounds license writing
to a tree unasked: the tree is the plugin's own, every step is a staged
`git mv` or a rewrite of a file git already tracks, and `git diff --cached`
shows the whole of it with the old text safe in history. The notice ends
"review the diff and commit" because the write is the beginning of a review.

The move, in order (`seal/specs/1788331011-…/spec.md`, "The move, in order"):

  1. `.specseal/map.md`   → `seal/ledger.md`
  2. `.specseal/map/`     → `seal/ledger/`
  3. `.specseal/README.md` → `seal/README.md`, then overwritten from
     `templates/seal-README.md` — the file is plugin-owned and its old text
     describes a layout that no longer exists
  4. every other entry under `.specseal/` → `seal/<same name>`
  5. each `specs/<id>/` whose name is `<unix seconds>-<slug>` → `seal/specs/<id>/`;
     anything else under `specs/` stays and is named, because `specs/` stops
     being SpecSeal's directory and a project may have had one first
  6. in every ledger, every anchor whose path starts with a moved prefix is
     rewritten to the new one; the hash after `@` is not touched, because it
     covers the cited content, which did not change
  7. the root is appended to `~/.claude/specseal/root-migrated`

Boundaries, each pinned in `tests/test_the_root_migrates_itself.py`:

  - **never over uncommitted work** — anything `git status --porcelain` reports
    under `.specseal/` or `specs/`, or a git that cannot answer, refuses the
    whole move with one line and stamps nothing
  - **only what git tracks** — the units come from `git ls-files`, so an
    ignored file under the old roots is not a unit and stays where it is;
    `.specseal/` may remain on disk holding nothing else
  - **once per repository** — a completed move stamps the marker, and so does
    a repository that has nothing old left and a root at EITHER place,
    `<repo>/seal/` or `<git-common-dir>/seal/`, so switching to an old branch
    later does not move it again — into a tree that local mode (#80) chose
    to keep clean, in the second case
  - **a stopped move resumes** — a step that fails stops the run, prints what
    moved and what did not, and stamps nothing; the next session start moves
    what remains and stamps only when nothing old is left
  - **a throwaway repository is left alone** — `.specseal/scratch` used to say
    so, and a repository still carrying it is not moved; the marker's
    successor is `.git/specseal-scratch`
  - **a symbolic link is refused, not half-moved** — git tracks a link as one
    blob, so a linked `.specseal/` or a linked `specs/` holding work items
    lists no units; either is refused with a line naming the by-hand
    section and nothing is stamped
  - **silent when there is nothing to do**
"""

# RIDER: this file is a reader of the OLD tree — `.specseal/` and a top-level
# `specs/` — and of nothing under `seal/specs/<id>/`. It can be deleted once
# no repository is left to migrate, and nothing else has to change when it
# goes; `hooks/dispatch.py`'s session-start group is the one place that names
# it. A comment rather than a docstring line on purpose: a docstring survives
# into the `.pyc`, and the rider test greps `hooks/` where a stale
# `__pycache__` then answers for a file. Verified 2026-09-02 at 2f51b8c.

import glob
import importlib.util
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import console
import optin

HOOKS = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(os.path.expanduser("~"), ".claude", "specseal")
MARKER = os.path.join(STATE_DIR, "root-migrated")
TEMPLATE = os.path.join(HOOKS, "..", "templates", "seal-README.md")
CHECKER = os.path.join(
    HOOKS, "..", "skills", "evidence-check", "scripts", "evidence_check.py"
)

OLD_HOME = ".specseal"
OLD_ITEMS = "specs"
OLD_SCRATCH = "scratch"
NEW = optin.HOME
# The shape `date +%s` and a slug produce. `specs/` may hold other things in
# a project that had the directory before the plugin arrived; those stay.
ITEM_RE = re.compile(r"^[0-9]{9,10}-[A-Za-z0-9._-]+$")
# Longest first, so `.specseal/map.md` is not read as `.specseal/` + `map.md`.
PREFIXES = (
    (".specseal/map.md", f"{NEW}/ledger.md"),
    (".specseal/map/", f"{NEW}/ledger/"),
    (".specseal/", f"{NEW}/"),
    ("specs/", f"{NEW}/specs/"),
)
LEDGER_GLOBS = (f"{NEW}/ledger.md", f"{NEW}/ledger/*.md", "docs/**/_evidence.md")


class MoveError(Exception):
    """A unit that did not move. `resumable` says whether the next session
    start can pick it up unaided; a destination already holding the file, or
    a `seal` that is a file, needs a person first, and the line says so
    instead of promising a continuation that never comes."""

    def __init__(self, path, error, resumable=True):
        super().__init__(f"{path}: {error}")
        self.path = path
        self.error = error
        self.resumable = resumable


def checker():
    spec = importlib.util.spec_from_file_location("specseal_evidence", CHECKER)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    return ec


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


def under(root, rel):
    """The disk path of a `/`-joined repository-relative path."""
    return os.path.join(root, *rel.split("/"))


def git(root, *args):
    return subprocess.run(
        ["git", "-C", root, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


def dirty(root):
    """True when anything under the old roots is uncommitted — or git cannot
    say. Work in progress outranks the move, and an unanswerable question is
    treated as work in progress: moving on a guess is the one direction this
    hook must never fail in.

    One shape is not work in progress: a staged rename or deletion with a
    clean worktree (`R ` and `D ` in porcelain's two columns). That is what
    a stopped run of this hook leaves behind, and a resume has to see past
    its own earlier steps or a stopped move can never finish. Anything with
    a worktree change, anything untracked, and anything staged as an
    addition or a modification still refuses.

    A `git ls-files` that cannot answer is the same case: `entries()` then
    lists the directory, which is the listing 🔴 1 replaced, so the move is
    refused here before that listing can move anything.
    """
    if tracked_names(root, OLD_HOME) is None or tracked_names(root, OLD_ITEMS) is None:
        return True
    try:
        r = git(root, "status", "--porcelain", "--", OLD_HOME, OLD_ITEMS)
    except (OSError, subprocess.SubprocessError):
        return True
    if r.returncode != 0:
        return True
    for line in r.stdout.splitlines():
        if len(line) < 2:
            continue
        x, y = line[0], line[1]
        if y != " " or x not in "RD":
            return True
    return False


def tracked_names(root, rel):
    """The top-level names git tracks under `rel`, sorted — or None when git
    cannot say.

    Every step of the move is a `git mv`, so a unit is what git tracks. An
    ignored file directly under `.specseal/` (`.DS_Store` is macOS's default)
    passes `dirty()`, which reads porcelain, and then stops `git mv` for good:
    every session start met the same unit, and the tree stayed half-moved
    with `seal/` present and `routing.md` still at the old path. Listing the
    directory was the defect; git's own list is the fix.
    """
    try:
        r = git(root, "ls-files", "-z", "--", rel)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    prefix = rel + "/"
    names = set()
    for path in r.stdout.split("\0"):
        if path.startswith(prefix):
            head = path[len(prefix) :].split("/", 1)[0]
            if head:
                names.add(head)
    return sorted(names)


def entries(root, rel):
    """What is under `rel` as units: git's list, or the directory listing when
    git cannot answer — `dirty()` reads as dirty then, so nothing moves."""
    names = tracked_names(root, rel)
    if names is not None:
        return names
    try:
        return sorted(os.listdir(under(root, rel)))
    except OSError:
        return []


def old_items(root):
    """(SpecSeal work items under `specs/`, everything else on disk there).

    The first list is what moves and comes from git; the second is what the
    printed line names as left behind and comes from the directory, because
    what stays on disk is what a person will see there.
    """
    items = [
        n
        for n in entries(root, OLD_ITEMS)
        if ITEM_RE.match(n) and os.path.isdir(under(root, f"{OLD_ITEMS}/{n}"))
    ]
    try:
        names = sorted(os.listdir(under(root, OLD_ITEMS)))
    except OSError:
        names = []
    return items, [n for n in names if n not in items]


def moves(root):
    """The units still to move, in the spec's order, as (kind, src, dst).

    Computed from what git tracks as it stands, which is what makes a stopped
    move resume: a unit that already moved is not there to be listed.
    """
    units = []
    names = entries(root, OLD_HOME)
    if "map.md" in names:
        units.append(("ledger", f"{OLD_HOME}/map.md", f"{NEW}/ledger.md"))
    if "map" in names:
        units.append(("ledger-dir", f"{OLD_HOME}/map", f"{NEW}/ledger"))
    if "README.md" in names:
        units.append(("readme", f"{OLD_HOME}/README.md", f"{NEW}/README.md"))
    for name in names:
        if name in ("map.md", "map", "README.md"):
            continue
        units.append(("other", f"{OLD_HOME}/{name}", f"{NEW}/{name}"))
    items, _ = old_items(root)
    for name in items:
        units.append(("item", f"{OLD_ITEMS}/{name}", f"{NEW}/specs/{name}"))
    return units


def git_mv(root, src, dst):
    """One staged rename. `git mv` does not create its destination's parent,
    and a `seal` that is a file makes creating it fail — inside the `try`,
    because an exception out of here is silence under the dispatcher."""
    parent = os.path.dirname(under(root, dst))
    try:
        os.makedirs(parent, exist_ok=True)
    except OSError as exc:
        raise MoveError(
            src, f"cannot create {os.path.dirname(dst)}/: {exc}", resumable=False
        ) from exc
    try:
        r = git(root, "mv", src, dst)
    except (OSError, subprocess.SubprocessError) as exc:
        raise MoveError(src, str(exc)) from exc
    if r.returncode != 0:
        raise MoveError(src, (r.stderr or r.stdout).strip() or f"exit {r.returncode}")


def taken(src, dst):
    """The error for a destination that already holds a file: `git mv` would
    say `destination exists` and the plain tail would promise a continuation
    that never comes, because the state does not change by itself."""
    return MoveError(
        src,
        f"{dst} already exists — keep one by hand: git rm {src} if {dst} is "
        f"the newer, or git rm {dst} to let the move bring the old one over",
        resumable=False,
    )


def move(root, src, dst):
    """`src` to `dst`, whole when nothing is at `dst` yet.

    When `dst` already exists — the state a stopped run leaves — a directory
    is moved file by file, because `git mv dir existing-dir` would put it
    INSIDE the destination. A file already at its destination is the person's
    to settle (a merge of a branch bootstrapped on the new layout leaves
    exactly that), and is named rather than tried. The empty directories left
    behind are removed.
    """
    if not os.path.isdir(under(root, src)):
        if os.path.exists(under(root, dst)):
            raise taken(src, dst)
        git_mv(root, src, dst)
        return
    if not os.path.exists(under(root, dst)):
        git_mv(root, src, dst)
        return
    r = git(root, "ls-files", "-z", "--", src)
    if r.returncode != 0:
        raise MoveError(src, (r.stderr or "").strip() or "git ls-files failed")
    for rel in [p for p in r.stdout.split("\0") if p]:
        target = dst + rel[len(src) :]
        if os.path.exists(under(root, target)):
            raise taken(rel, target)
        git_mv(root, rel, target)
    for here, dirs, files in os.walk(under(root, src), topdown=False):
        if not dirs and not files:
            try:
                os.rmdir(here)
            except OSError:
                pass


def rewrite_readme(root, dst):
    """Step 3's second half: the moved README becomes the new template's text.

    A template that cannot be read leaves the moved file as it was — a README
    describing the old layout is the state Q5 weighed, and it beats stopping
    the move for a file that is not the move.
    """
    try:
        with open(TEMPLATE, encoding="utf-8") as f:
            text = f.read()
        with open(under(root, dst), "w", encoding="utf-8") as f:
            f.write(text)
    except OSError:
        return
    git(root, "add", "--", dst)


def run_moves(root, units):
    """(units moved, the error that stopped the run or None)."""
    done = 0
    for kind, src, dst in units:
        try:
            move(root, src, dst)
            if kind == "readme":
                rewrite_readme(root, dst)
        except MoveError as exc:
            return done, exc
        done += 1
    for old in (OLD_HOME, OLD_ITEMS):
        try:
            os.rmdir(under(root, old))
        except OSError:
            pass  # something else is in it, or it is already gone
    return done, None


def ledgers(root):
    return sorted(
        {
            p
            for pat in LEDGER_GLOBS
            for p in glob.glob(os.path.join(root, pat), recursive=True)
        }
    )


def repoint_path(path):
    """The path after the move — unchanged when nothing moved it. An entry
    under `specs/` that is not a work item stays where it is (step 5), so a
    row citing it has to stay too, or the row breaks."""
    for old, new in PREFIXES:
        if path.startswith(old):
            if old == f"{OLD_ITEMS}/":
                head = path[len(old) :].split("/", 1)[0]
                if not ITEM_RE.match(head):
                    return path
            return new + path[len(old) :]
    return path


def repoint(root):
    """Step 6. Every anchor under a moved prefix follows it; the hash stays.

    The checker's own `ANCHOR_RE` finds the coordinates, so the rewrite reads
    exactly what the check reads and nothing in prose. The count is of lines
    changed — rows — not of anchors, since a row may cite two.
    """
    ec = checker()
    rows = 0
    for ledger in ledgers(root):
        text = ec.read(ledger)
        if text is None:
            continue

        def follow(m):
            path = m.group("path")
            new = repoint_path(path)
            return m.group(0) if new == path else new + m.group(0)[len(path) :]

        new_text = ec.ANCHOR_RE.sub(follow, text)
        if new_text == text:
            continue
        # The same line count on both sides: only a path changed, never a
        # newline, so a mismatch here would be a defect in `follow`.
        rows += sum(
            1
            for a, b in zip(text.split("\n"), new_text.split("\n"), strict=True)
            if a != b
        )
        with open(ledger, "w", encoding="utf-8") as f:
            f.write(new_text)
        git(root, "add", "--", os.path.relpath(ledger, root).replace(os.sep, "/"))
    return rows


def has_root(root):
    """True when `seal/` is a directory at either place the root can be."""
    if os.path.isdir(under(root, NEW)):
        return True
    common = optin.git_common_dir(root)
    return bool(common) and os.path.isdir(os.path.join(common, NEW))


def say(message):
    print(json.dumps({"systemMessage": message}))


def main():
    try:
        event = json.load(sys.stdin) or {}
        cwd = event.get("cwd")
    except (ValueError, AttributeError):
        return
    if not cwd or not os.path.isdir(cwd):
        return
    # NOT `optin.opted_in`: the old layout is exactly what does not opt in any
    # more, and a hook gated on the new signal would never meet what it moves.
    root = optin.repo_root(cwd)
    if not root:
        return
    if os.path.islink(under(root, OLD_HOME)):
        # Git tracks the link as one blob, so the home lists no units: the
        # work items would move, the marker would be stamped, and
        # `seal/ledger.md` would never appear. Refused before anything else,
        # every session start, until the link is gone.
        say(
            f"specseal: {OLD_HOME}/ is a symbolic link, which git tracks as the "
            "link and not as its files — not moving it. Move by hand (README, "
            '"Coming up from 0.3.x") and remove the link.'
        )
        return

    units = moves(root)
    if not units:
        # Nothing old left. Stamped so that checking out a branch that still
        # carries the old layout later finds the once-per-repository rule
        # already answered, rather than a move staged onto that branch.
        #
        # Either place, read directly rather than through `optin.home_at`,
        # so the scratch marker does not hide the root from this rule. A
        # local-mode repository (#80) keeps the root under the git directory
        # and was never stamped by the tree-only test: it re-listed the old
        # names at every session start, and an old branch checked out later
        # was moved INTO the tree the person chose to keep clean.
        if not attempted(root) and has_root(root):
            stamp(root)
        return
    if attempted(root):
        return  # once per repository; the silent gates are the backstop (Q8)
    if os.path.exists(under(root, f"{OLD_HOME}/{OLD_SCRATCH}")):
        say(
            "specseal: .specseal/scratch says this repository is throwaway — "
            "not migrating it. Delete the file if it is not."
        )
        return
    if os.path.islink(under(root, OLD_ITEMS)) and any(
        ITEM_RE.match(n) and os.path.isdir(under(root, f"{OLD_ITEMS}/{n}"))
        for n in old_items(root)[1]
    ):
        # The same blob on the other root. Git lists no work items behind
        # the link, so the home would move, the items would be named as
        # "not tracked" and left, their rows re-pointed to a `seal/specs/`
        # that never appears, and the marker stamped over a broken ledger.
        # After the unit and marker checks, so a migrated repository stays
        # silent; a linked `specs/` holding no work items is not SpecSeal's
        # name and is not refused.
        say(
            f"specseal: {OLD_ITEMS}/ is a symbolic link holding work items, which "
            "git tracks as the link and not as its files — not moving it. Move by "
            'hand (README, "Coming up from 0.3.x") and remove the link.'
        )
        return
    if dirty(root):
        say(
            "specseal: .specseal/ and specs/ are the old layout, but they carry "
            "uncommitted changes — not touching work in progress. Commit, then "
            f"the next session start moves them into {NEW}/."
        )
        return

    done, error = run_moves(root, units)
    if error is not None:
        tail = (
            "The next session start continues."
            if error.resumable
            else "Settle that by hand, then the next session start continues."
        )
        say(
            f"specseal: moved {done} of {len(units)} into {NEW}/ and stopped at "
            f"{error.path}: {error.error}. {tail}"
        )
        return
    try:
        rows = repoint(root)
    except OSError as exc:
        # Every unit has moved and the rows still say the old paths. Not
        # stamped: the checker reports them BROKEN loudly, and the next start
        # finds nothing old and stamps then.
        say(
            f"specseal: moved everything into {NEW}/ but could not re-point the "
            f"ledger: {exc}. Run `evidence-check --reverify .`"
        )
        return
    stamp(root)

    had_home = any(kind != "item" for kind, _, _ in units)
    items = sum(1 for kind, _, _ in units if kind == "item")
    what = " and ".join(
        part
        for part in (
            f"{OLD_HOME}/" if had_home else "",
            f"{items} work item{'' if items == 1 else 's'}" if items else "",
        )
        if part
    )
    _, left = old_items(root)
    tail = (
        f"; left {', '.join(f'{OLD_ITEMS}/{n}' for n in left)} where it is "
        "(not tracked as a SpecSeal work item)"
        if left
        else ""
    )
    say(
        f"specseal: moved {what} into {NEW}/ ({rows} ledger row"
        f"{'' if rows == 1 else 's'} re-pointed{tail}) — review the diff and commit"
    )


if __name__ == "__main__":
    console.to_utf8()
    main()
