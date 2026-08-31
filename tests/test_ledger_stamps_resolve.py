"""A ledger row's Checked SHA is its drift baseline, so it has to resolve.

`.specseal/map.md:21-23` states what the column means: *the date AND the commit
SHA it was read at, and drift for that row is measured from there.* When that
SHA does not resolve, `evidence_check.row_baseline` returns None and the row
falls back to the header baseline — silently. Nothing prints, nothing fails,
and the row goes on being counted.

That is worse than a broken coordinate, because the fallback can be QUIETER
than the truth. One row here cited `hooks/worktree-guard.py:247` at a branch-only commit
and read DRIFTED in the worktree that wrote it. In a fresh clone — which is
all CI ever gets — that commit does not exist, the row fell back to the header
baseline, and the drift disappeared from the report. The visible drift that
was being deliberately preserved was not visible anywhere except one laptop.

Where the dead SHAs come from is worth writing down, because it will happen
again: a rebase during the work rewrote every commit this branch had made, and
the rows kept naming the pre-rebase objects. Those objects survive in the
worktree that wrote them and nowhere else. `CONTRIBUTING.md:133-135` makes it
permanent — feature branches squash back into the release branch, so a
branch-only SHA is unresolvable to everyone the moment the branch merges.

This is the ledger's half of `tests/test_a_rider_reaches_its_file.py`, which
holds the same rule for rider stamps.
"""

import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEDGER = os.path.join(ROOT, ".specseal", "map.md")

# `2026-08-26 eb4c255`, or the same inside backticks. Read off the whole row
# rather than off a `|`-split cell on purpose: a cell here holds
# `` `|| [ $? -eq 1 ]` ``, and splitting on the pipe puts the Checked column
# at a different index for that row alone. A reader that mislocates one column
# is how the row went unchecked in the first place.
STAMP = re.compile(r"\b\d{4}-\d{2}-\d{2}\s+`?([0-9a-f]{7,40})`?")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def git(*args):
    return subprocess.run(
        ["git", "-C", ROOT, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).returncode


def is_shallow():
    """A shallow clone cannot answer any of this, and must not pass quietly."""
    r = subprocess.run(
        ["git", "-C", ROOT, "rev-parse", "--is-shallow-repository"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout.strip() == "true"


SHALLOW = (
    "this clone is shallow, so no stamp can be resolved and this check "
    "proves nothing. Fetch the full history (`fetch-depth: 0` in the "
    "workflow, `git fetch --unshallow` locally) rather than reading a pass "
    "into it"
)


def stamps():
    """(line number, sha) for every Checked stamp the ledger writes."""
    found = []
    for n, line in enumerate(read(LEDGER).splitlines(), 1):
        if not line.strip().startswith("|"):
            continue
        for m in STAMP.finditer(line):
            found.append((n, m.group(1)))
    assert found, "no Checked stamps found at all — this check reads nothing"
    return found


def test_every_checked_stamp_names_a_commit_that_exists():
    assert not is_shallow(), SHALLOW
    missing = [
        (n, sha)
        for n, sha in stamps()
        if git("cat-file", "-e", f"{sha}^{{commit}}") != 0
    ]
    assert not missing, (
        f".specseal/map.md stamps that resolve to no object: {missing}. "
        "A drift baseline nobody can resolve falls back to the header "
        "without saying so"
    )


def test_every_checked_stamp_is_reachable_from_this_branch():
    """Existing is not enough. An orphaned object still answers `cat-file`
    in the worktree that wrote it, which is exactly why nobody noticed: the
    rows were re-read locally, the SHAs resolved locally, and the ledger was
    already lying to every other checkout."""
    assert not is_shallow(), SHALLOW
    unreachable = [
        (n, sha)
        for n, sha in stamps()
        if git("cat-file", "-e", f"{sha}^{{commit}}") == 0
        and git("merge-base", "--is-ancestor", sha, "HEAD") != 0
    ]
    assert not unreachable, (
        f".specseal/map.md stamps that no ref can reach: {unreachable}. "
        "The object survives in the worktree that wrote it and nowhere else "
        "— a rebase or a squash is what puts a row here"
    )


def test_the_baseline_reader_picks_the_sha_the_row_wrote():
    """The stamp and the reader have to agree on which SHA is the baseline.

    `evidence_check.row_baseline` takes the FIRST resolvable SHA-shaped word
    in the row after coordinates are stripped, scanning the whole line rather
    than the Checked cell. A hex-looking word earlier in the Clause or Grounds
    column would therefore become the row's baseline, and the stamp the author
    wrote would never be read at all — with nothing anywhere reporting the
    substitution.
    """
    assert not is_shallow(), SHALLOW
    import importlib.util

    path = os.path.join(
        ROOT, "skills", "evidence-check", "scripts", "evidence_check.py"
    )
    spec = importlib.util.spec_from_file_location("specseal_evidence_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    text = read(LEDGER)
    cache = {}
    wrong = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip().startswith("|"):
            continue
        m = STAMP.search(line)
        if not m:
            continue
        # A position anywhere inside the row is enough: `row_baseline` widens
        # to the whole line itself.
        pos = text.index(line) + m.start(1)
        picked = mod.row_baseline(text, pos, ROOT, cache)
        if picked != m.group(1):
            wrong.append((n, m.group(1), picked))
    assert not wrong, (
        f"(line, stamp written, baseline actually read): {wrong}. The row's "
        "drift is being measured from a commit nobody wrote there"
    )
