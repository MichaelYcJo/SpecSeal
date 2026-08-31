"""Shared reader: which way did this work item say it was going?

The routing answer -- review chain or straight to the PR -- is given before the
first edit. Nothing used to receive it, so the commit gate re-derived it from
the absence of a review mark, and a mark only exists after a review passes.
Every commit of every round was stopped on its way to the reviewer the answer
had already named.

A declaration lives at `specs/<work-item-id>/routing.md` and is committed.
Committed is the load-bearing part: the check moves to the pull request, and CI
sees only what is in the tree. `<git-dir>/specseal-reviewed` cannot travel
there and never will.

Beside the work item rather than under `.specseal/`, because a work item begins
and ends in one directory and routing is its first fact. It also gives the work
below the SDD ladder somewhere to exist: those items write no `spec.md`, so
until now they left no trace anywhere, and they are most of what the gate sees.

Imported by the gate and by the hygiene check rather than copied into each --
the same reason `optin.py` gives for being a module: divergent copies is how
half of them keep the old answer.

Everything here fails toward "no declaration". A file that cannot be read is
not an answer somebody gave, so the gate goes back to asking. Silence would
make a corrupt file into the standing waiver `docs/review-chain-spec.md`
refuses to build.

The third axis, `Implementation`, is the one exception and it is not a
loophole. Nothing decides a commit on it -- see `parse()` for why an absent or
unreadable answer there reads as unanswered instead of taking the whole
declaration down with it.
"""

import os
import re
import subprocess

REVIEW = "Review"
DESTINATION = "Destination"
BRANCH = "Branch"
IMPLEMENTATION = "Implementation"

CHAIN = "through the review chain"
DIRECT = "straight to the PR"
REVIEW_ANSWERS = (CHAIN, DIRECT)

OPEN_PR = "open the pull request"
STOP_BEFORE_PR = "stop before the pull request"
DESTINATION_ANSWERS = (OPEN_PR, STOP_BEFORE_PR)

BY_SMITH = "smith"
BY_SESSION = "the session"
IMPLEMENTATION_ANSWERS = (BY_SMITH, BY_SESSION)

WORK_ITEMS = "specs"
FILENAME = "routing.md"


def table_rows(text):
    """Every two-cell markdown table row, as (label, value).

    Unknown labels are left in rather than filtered: a reader that drops what
    it does not recognise cannot gain a third axis later without the older
    readers silently ignoring it. The caller decides what it needs.
    """
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if set(cells[0]) <= set(":- "):  # the separator row
            continue
        rows.append((cells[0], cells[1]))
    return rows


def parse(text):
    """One declaration, or None when the text is not one.

    Strict on the two answer vocabularies and on the branch being named. A
    tolerant read here would turn prose that merely mentions the review chain
    into a waiver -- the same failure `has_marker` avoids by refusing to read a
    marker out of a commit message.

    `Implementation` is the third axis and it is read on DIFFERENT terms: it is
    optional, and an answer outside its vocabulary reads as unanswered rather
    than as "this file is not a declaration". Both halves of that are forced by
    what already exists. Every declaration written before the axis was added
    has no such row, and a required row would turn each of them back into an
    unanswered gate -- the review question would be asked again on branches
    whose answer is committed in the tree. The strict spelling below is
    deliberate for the first two, because a wrong answer there decides whether
    a reviewer sees the work. NOTHING reads this one yet -- the notice that
    would have is #26 -- so a wrong answer here is recorded and never
    contradicted. That is why the row is optional rather than lenient, and it
    is also the asymmetry to know about: a backticked or capitalised answer
    is rejected loudly in the first two, because the gate goes back to asking,
    and silently here. `templates/sdd-routing.md` is the only spelling a
    session should copy, and a test parses that file so it cannot drift.
    """
    found = dict(table_rows(text))
    review = found.get(REVIEW)
    destination = found.get(DESTINATION)
    branch = found.get(BRANCH)
    implementation = found.get(IMPLEMENTATION)
    if review not in REVIEW_ANSWERS:
        return None
    if destination not in DESTINATION_ANSWERS:
        return None
    if not branch:
        return None
    return {
        "review": review,
        "destination": destination,
        "branch": branch,
        # One value for "no row" and for "a row nobody can read". They must not
        # diverge: a reader that told them apart would have to decide what to
        # do about an unreadable one, and the only honest answer is the same
        # nothing it does for an absent one.
        "implementation": (
            implementation if implementation in IMPLEMENTATION_ANSWERS else None
        ),
    }


def current_branch(cwd):
    """The checked-out branch, or "" when detached or unreadable.

    A detached HEAD matches no declaration, so the gate asks. That is the
    correct direction: nothing on a detached HEAD is the work item a branch
    was declared for.
    """
    try:
        out = subprocess.run(
            ["git", "-C", cwd or ".", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    name = out.stdout.strip() if out.returncode == 0 else ""
    return "" if name == "HEAD" else name


def declarations(root):
    """Every readable declaration under `root`, as (path, parsed) pairs.

    One per work-item directory. Nothing here reads the directory name: the id
    orders the directories and names the work, but which declaration APPLIES is
    settled by the branch it names, not by its position in a sort.
    """
    where = os.path.join(root, WORK_ITEMS)
    try:
        names = sorted(os.listdir(where))
    except OSError:
        return []
    out = []
    for name in names:
        path = os.path.join(where, name, FILENAME)
        try:
            with open(path, encoding="utf-8") as f:
                parsed = parse(f.read())
        except (OSError, UnicodeDecodeError):
            # `UnicodeDecodeError` is a `ValueError`, not an `OSError`, and it
            # is named rather than its parent: `parse()` is pure string work
            # today, so a `ValueError` reaching here later would be a defect in
            # it, and swallowing that as "no declaration" is how a gate goes
            # quiet for a reason nobody wrote down. A
            # declaration that is not valid UTF-8 used to raise out of
            # `declarations()` -> `commit-review-gate.py` -> `dispatch.py`'s
            # `except Exception: return ""`, which is no output, which the
            # harness reads as approval. The module docstring says everything
            # here fails toward "no declaration"; a file nobody can decode is
            # not an answer somebody gave, so it is skipped and the gate goes
            # back to asking. `chain_check.py` already catches both when it
            # reads the event payload -- the CI half was hardened and this one
            # was not.
            continue
        if parsed:
            out.append((path, parsed))
    return out


def for_branch(root, branch):
    """The one declaration that applies here, or None.

    Two declarations naming the same branch is not an answer, so it reads as
    none. Declarations accumulate over a repository's life and a branch-less
    match would let the first work item ever declared silence the gate for
    every commit after it.
    """
    if not root or not branch:
        return None
    matching = [d for _, d in declarations(root) if d["branch"] == branch]
    return matching[0] if len(matching) == 1 else None


def declared(cwd, root):
    """The routing answer in force for `cwd`, or None when there is not one."""
    return for_branch(root, current_branch(cwd))


def item_dir(root, branch):
    """The work-item directory the declaration for `branch` lives in, or "".

    This is what makes a review round writable before a pull request exists.
    The round records live one level down, in `rounds/`, so whatever resolves
    the declaration resolves them too, and the branch is the only key
    available at the moment a round closes.

    Two declarations naming one branch resolve to nothing here for the same
    reason they do in `for_branch`: not an answer.
    """
    if not root or not branch:
        return ""
    matching = [path for path, d in declarations(root) if d["branch"] == branch]
    return os.path.dirname(matching[0]) if len(matching) == 1 else ""


ROUND_RE = re.compile(r"round-(\d+)\.md")

# The subdirectory the records live in, under the work item.
ROUNDS_DIR = "rounds"


def round_number(name):
    """The N in `round-N.md`, or None when the name is not one.

    The one place the ordering rule lives. `skills/code-review/scripts/chain_check.py`
    calls this rather than writing the pattern again -- the two readers had
    two orders, this one by name and that one numerically, and the docstring
    of one called the other a defect. Nothing noticed, because
    `review-history-guard` reads every record rather than the last. At ten
    rounds they split, and the reader that takes the LAST record would take
    `round-9.md`.
    """
    m = ROUND_RE.fullmatch(os.path.basename(name))
    return int(m.group(1)) if m else None


def _ordered(where):
    """`round-N.md` under `where`, lowest round first, or [] when unreadable.

    Filtered BEFORE the sort, not after. Both callers below hand this a
    directory that holds other things -- the work item's own directory holds
    `routing.md` and the rest of the SDD set, and `rounds/` holds whatever a
    repository chooses to put beside its records -- and `sorted` comparing
    None against an int raises rather than ordering. Nothing here may assume
    a directory of records only.
    """
    try:
        names = os.listdir(where)
    except NotADirectoryError:
        # A `rounds` that is a FILE, not a directory. Round 1 reached it by
        # following this release's own migration command: `git mv
        # <item>/round-*.md <item>/rounds/` fails because `git mv` does not
        # create its destination, and dropping the trailing slash is what a
        # person tries next -- which succeeds for a single record and renames
        # it to a file called `rounds`. Both readers then said the work item
        # held no round record while git carried the review's whole text, and
        # a review reported as never having happened is the one direction this
        # module refuses. Raised so a caller says which of the two it is.
        raise
    except OSError:
        return []
    found = [(round_number(n), n) for n in names]
    return [
        os.path.join(where, n) for _, n in sorted(p for p in found if p[0] is not None)
    ]


def rounds(item):
    """Every round record in a work item's `rounds/`, lowest round first.

    Numerically, not by name, for the reason `round_number` gives.

    `rounds/` rather than the work-item directory itself, because `round-N`
    is the one member of the SDD set that is plural and unbounded: six
    records beside six other files was the worst case here, and the structure
    should say which member grows.

    The old flat location is NOT read, and `stray_rounds` exists so a caller
    can say so out loud. A permanent dual read would put two places to look in
    the reader four gates depend on, and an expiry nothing enforces is a
    comment -- so what replaces the fallback is a message naming the file and
    the destination.

    What stays different between the two readers is deliberate, and it is not
    the order: this one reads the working tree, because a hook fires before
    the commit and an uncommitted round record is exactly what it should see.
    The pull-request check reads what git carries, because CI sees nothing
    else -- an untracked file there is evidence nobody can open.
    """
    if not item:
        return []
    try:
        return _ordered(os.path.join(item, ROUNDS_DIR))
    except NotADirectoryError:
        # Caught here rather than raised at the gates. A hook that raises is
        # rendered as an allow by `hooks/dispatch.py`, so propagating this
        # would turn a nameable state into a silent one -- the opposite of
        # what `_ordered` refuses it for. `rounds_unreadable` is how a caller
        # asks which of the two happened.
        return []


def rounds_unreadable(item):
    """True when `rounds` exists beside the work item and is not a directory.

    Told apart from "no records" because the two need opposite answers: one
    is 28 of this repository's 35 work items and must stay quiet, the other
    is a review whose whole text git is still carrying while every reader
    reports that none happened.

    Reached by following this release's own migration command. `git mv
    <item>/round-*.md <item>/rounds/` fails -- `git mv` does not create its
    destination -- and dropping the trailing slash succeeds for a single
    record, renaming it to a file named `rounds`.
    """
    if not item:
        return False
    where = os.path.join(item, ROUNDS_DIR)
    if os.path.islink(where):
        # ANY link, including one that resolves to a directory holding
        # records. `os.path.exists` follows links, so the first version
        # returned False for a broken one; the second still followed a live
        # one into the directory and stayed quiet while the pull-request
        # check — which sees git's `120000` and calls it not-a-tree — failed
        # and told the reader to `mkdir` a path that already exists. The two
        # readers answer for what GIT carries, and git carries a link.
        # Round 4's fourth shape, after three were enumerated.
        return True
    if os.path.exists(where) and not os.path.isdir(where):
        return True
    if os.path.isdir(where):
        try:
            os.listdir(where)
        except OSError:
            # A directory nothing can list. `_ordered` returns [] for it, so
            # without this it reads as a work item that never ran a review.
            return True
    return False


def stray_rounds(item):
    """`round-N.md` left at the work item's own directory, lowest round first.

    These are records nothing reads. `rounds()` looks one level down and a
    reader that merely found nothing would report the same silence as a work
    item that never ran a review -- the state 28 of this repository's 35 work
    items are in, and the state that must stay quiet. The difference between
    "no review happened" and "the review is in a place nobody reads" is the
    whole reason this function is separate from the one above.
    """
    if not item:
        return []
    return _ordered(item)
