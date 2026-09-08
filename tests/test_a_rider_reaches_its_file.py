"""A deferral is either a rider or a schedulable item, and they live apart.

Thirteen rows sat in `.specseal/follow-up.md`. Classified by their answerer
column, most of them were not "someone should do this" at all — they were
*"if you open this file, do this too"*, which is worth exactly as much as its
chance of reaching the person who opens that file. A file nobody opens to find
out what to work on next has none.

So a rider goes to its coordinate as a `# RIDER:` comment, and
`grep -rn "RIDER:"` is the list. What stays in `follow-up.md` is the narrow
case issue #34 named in its own third checkbox: a schedulable item in a
repository with no tracker.

The failure this guards against is the file quietly refilling. A coordinate-
tied row written here is one nobody at that coordinate will ever see.
"""

import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOLLOW_UP = os.path.join(ROOT, "seal", "follow-up.md")

# A coordinate is `path/to/file.ext:123` — the shape a rider is written at.
COORDINATE = re.compile(r"[\w./-]+\.(?:py|md|json|yml|yaml|sh):\d+")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def rows(section):
    """Table rows under one `## ` heading of follow-up.md."""
    text = read(FOLLOW_UP)
    body = text.split(f"## {section}", 1)[1].split("\n## ", 1)[0]
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if set("".join(cells)) <= set(":- ") or cells[0] in ("Item", "Target"):
            continue
        out.append(cells)
    return out


def test_no_schedulable_row_carries_a_coordinate():
    """A row with a `file.py:120` in it is a rider filed where its reader is
    not. The rider list is `grep RIDER:`, and this section is not it."""
    offenders = [
        r
        for r in rows("Schedulable items with nowhere else to go")
        if COORDINATE.search(" ".join(r))
    ]
    assert not offenders, f"coordinate-tied rows in the schedulable list: {offenders}"


def test_the_header_says_what_belongs_and_what_does_not():
    text = read(FOLLOW_UP)
    assert "schedulable item in a repository with no tracker" in text
    assert "Anything tied to a coordinate" in text
    assert 'grep -rn "RIDER:"' in text


def test_the_header_stops_the_answerer_that_is_really_a_condition():
    """The file already forbade a deferral to nobody, and every one of its
    seventeen rows read `repository owner, next time X is opened` — a
    condition wearing a person's clothes. Issue #34 is that pair."""
    text = read(FOLLOW_UP)
    assert "no condition attached" in text
    assert "condition wearing a person's clothes" in text
    for row in rows("Schedulable items with nowhere else to go"):
        assert "next time" not in " ".join(row), row


def test_the_file_records_what_the_move_costs_and_that_it_can_be_overturned():
    """A judgment nobody can find is a judgment nobody can reverse."""
    text = read(FOLLOW_UP)
    assert "Nothing forces a rider to be deleted" in text
    assert "overturned" in text


def test_the_riders_exist_where_the_rows_said_they_would():
    """Every file a row said its rider went to.

    `hooks/worktree-guard.py` is held by `fix/the-guard-that-could-not-read`,
    and its four riders waited a round for that reason. They are planted now
    because the conflict they were avoiding does not exist: the file is the
    same blob at HEAD and at that branch's tip, so nothing there is being
    rewritten yet."""
    for rel in (
        "hooks/optin.py",
        "hooks/review-skill-gate.py",
        "hooks/review-history-guard.py",
        "hooks/cmdline.py",
        "hooks/dispatch.py",
        "hooks/worktree-guard.py",
        "templates/evidence-check.yml",
    ):
        assert "# RIDER:" in read(os.path.join(ROOT, rel)), rel


# Where riders are allowed to live. `templates` was missing, so the rider in
# `templates/evidence-check.yml` was never checked by anything at all —
# `follow-up.md` names it as planted and nothing here could see it. `tests`
# was missing for the same reason and one release longer, and it cost four
# riders unwatched: two carrying a measurement, one with no stamp in any form,
# and the one round 1's fix pass planted at `test_the_reopening_is_one.py`,
# whose own record then asserted the stamp names no commit of this branch as
# though a check had answered it. That is twice now that this list was the
# defect rather than the corpus, which is why `fix/239-a-stamp-names-content-
# not-a-commit` moves the walk to `.github/scripts/rider_check.py` over a
# sixth root as well. Whichever of the two lands second takes that version.
RIDER_ROOTS = ["hooks", "skills", "agents", "templates", "tests"]

# A rider opens a COMMENT. Matching the bare text reads an assertion ABOUT a
# rider as a rider — see `rider_stamps`.
MARKER = re.compile(r"^[ \t]*#+ *RIDER:", re.M)
# A stamp says what state the claim was read against, and there are two
# spellings of that on this release. `at <sha>` names a commit, and the
# release's merge rule destroys the commits it has to name (#239) — a feature
# branch squashes, so the stamp resolves to nothing for whoever reads it next.
# `against <anchor>@<hash>` names CONTENT, which is the ledger's own rule and
# what `fix/239-a-stamp-names-content-not-a-commit` migrates every stamp to.
#
# Both are accepted HERE and only one is verified here: this file checks that
# a stamp exists and that a commit-form stamp resolves, and the hash behind an
# anchor is #239's checker's to recompute. Accepting the anchor form is what
# lets a rider whose measurement commit was already squashed away carry a
# stamp at all — `test_the_records_can_be_carried_out_and_in.py`'s was taken
# at `3f8f846`, which is an ancestor of neither `HEAD` nor
# `origin/release/v0.9.1`, so no commit-form stamp for it can be written that
# resolves.
STAMP = re.compile(
    r"Verified \d{4}-\d{2}-\d{2}"
    r"(?: at (?P<sha>[0-9a-f]{7,40})\b"
    r"| against (?:\"(?:[^\"\n]|\\\")+\"|[A-Za-z_][A-Za-z0-9_.]*)@[0-9a-f]{6,12})"
)


def rider_stamps():
    """(file, sha) for every rider in the tree; `sha` is None for an anchor."""
    out = subprocess.run(
        # `__pycache__` excluded: a `.pyc` beside a script that carries a
        # rider matches too, and `grep` answers `Binary file … matches`,
        # which this then reads as a path. The roots held no rider inside a
        # compiled module until one landed in `skills/evidence-check/`, and
        # the failure is a `FileNotFoundError` naming grep's own sentence —
        # loud, and about nothing. Every walk in this repository skips it.
        ["grep", "-rn", "--exclude-dir=__pycache__", "RIDER:", *RIDER_ROOTS],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    assert out.strip(), "no riders found at all"
    found = []
    for rel in {line.split(":", 1)[0] for line in out.splitlines()}:
        block = read(os.path.join(ROOT, rel))
        # A rider OPENS a comment, so the split anchors on a line that starts
        # one. The marker inside a string literal is a case asserting that a
        # rider exists somewhere else, and splitting on the bare text read
        # each of those as a rider with no stamp. Three files carry one:
        # `tests/test_the_root_migrates_itself.py`, and this file twice — the
        # check's own corpus, the moment `tests` joined the roots.
        #
        # The marker itself is never spelled out in a comment anywhere in this
        # file, and that is deliberate rather than shy. #239's checker opens a
        # block at any comment line CONTAINING it, which is the looser of the
        # two readings, so prose about the convention would be a rider with no
        # stamp there while passing here — and the two have to agree while
        # both are in the tree.
        for chunk in MARKER.split(block)[1:]:
            head = chunk.split("\n\n", 1)[0]
            m = STAMP.search(head)
            assert m, f"{rel}: a rider with no verification stamp"
            found.append((rel, m.group("sha")))
    return found


def test_every_rider_carries_the_date_and_sha_it_was_verified_at():
    """A rider that outlives its fix is the cost of this arrangement. The
    stamp is the mitigation: a reader can tell how old the claim is without
    trusting it."""
    assert rider_stamps()


def is_shallow():
    """A shallow clone has no history to answer ancestry with."""
    r = subprocess.run(
        ["git", "-C", ROOT, "rev-parse", "--is-shallow-repository"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return r.stdout.strip() == "true"


def test_every_rider_stamp_names_a_commit_this_branch_can_reach():
    """The shape check above accepts `deadbeef`, and something worse than a
    made-up SHA got through it: three riders were stamped `714d6d2`, the
    pre-rebase version of a commit that is now `0ae5ed5`. The object survives
    in the worktree that wrote it, so `git log` answered locally and nothing
    looked wrong — and in a fresh clone it resolves to nothing.

    Whoever wants to know how stale a rider is opens the SHA first, so an
    unreachable stamp removes the only safeguard this arrangement has.

    A shallow clone fails here rather than skipping, and says why. `git clone
    --depth 1` leaves NO stamp resolvable, so a skip would turn the one
    checkout setting that voids this check into the setting that silences it
    — and that setting was the default in this repository's own `pytest` job
    until `tests/test_ci_gives_the_checks_what_they_need.py` pinned it.
    """
    assert not is_shallow(), (
        "this clone is shallow, so no stamp resolves and this check proves "
        "nothing. Fetch the full history (`fetch-depth: 0` in the workflow, "
        "`git fetch --unshallow` locally) rather than reading a pass into it"
    )
    stamps = rider_stamps()
    assert any(sha for _rel, sha in stamps), (
        "no rider carries a commit-form stamp, so this check reads as a pass "
        "over an empty corpus. Either the migration to content anchors is "
        "complete, in which case delete this case and let #239's checker own "
        "the rule, or the walk stopped seeing riders"
    )
    for rel, sha in stamps:
        if sha is None:
            # An anchor names content, so there is no commit to resolve. What
            # it claims is a hash, and recomputing that is #239's checker's
            # job rather than this one's.
            continue
        reachable = subprocess.run(
            ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
            cwd=ROOT,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        assert reachable.returncode == 0, (
            f"{rel}: rider stamped {sha}, which is not an ancestor of HEAD. "
            "A stamp nobody else can resolve is not a stamp"
        )


def test_a_held_file_is_named_with_the_branch_holding_it():
    """A rider that cannot be planted has to say what unblocks it, or it is a
    deferral to nobody."""
    for target in rows("Riders waiting on a file another branch holds"):
        assert "held by" in target[0], target[0]
        assert target[-1].strip() not in ("", "—"), f"no answerer: {target}"
