"""S15 of the 0.4.0 root move: no document, skill, agent, template or workflow
names `.specseal/` or a bare `specs/<…>/` as a live path.

A session follows the first path it reads. Every shipped text now says
`seal/`, and a stray `.specseal/map.md` in one skill is a second answer that
sends that session to write a file nothing reads — the silence every gate
gives the old layout is what makes the miss invisible.

Three kinds of mention keep the old name on purpose, and each is listed
below with its reason, so the allowlist cannot grow without one:

  - the design record and its Korean twin, which name both trees because
    the move is what they are about;
  - a marker or a retired key, which is read by a script or kept as
    history — the `<!-- specs/<id> -->` text in the changelog and the ledger,
    the `.specseal/handoff/PR-<n>/` directory that was never created;
  - a sentence about the migration itself, worded as past.

`hooks/root-migrate.py` reads the old names on purpose and is a `.py` file,
so it is outside the scanned suffixes; so are the round records, overviews
and plans of released work items under `seal/specs/`, which record what was
true at their SHA. `README.md` and `README.ko.md` moved together in phase 3
of the work item, because the hygiene workflow warns when they do not, and
their "coming up from 0.3.x" section is the one place a person is told how
the move happens and how to make it by hand — its lines are the third kind.
"""

import os
import re

import pytest
from conftest import build_tracked_tree, decline_if_shrunken, git_listing, on_disk

ROOT = os.path.join(os.path.dirname(__file__), "..")

# `.specseal/` anywhere; `specs/<` unless it is `seal/specs/<` or part of a
# longer path segment.
OLD_ROOT = re.compile(r"\.specseal/|(?<![\w/.])specs/<")

SCANNED = (
    ".github/workflows",
    "templates",
    "skills",
    "agents",
    "docs",
    "CONTRIBUTING.md",
    "CLAUDE.md",
    "SECURITY.md",
    "install.sh",
    "uninstall.sh",
    "seal/README.md",
    "README.md",
    "README.ko.md",
)
SUFFIXES = (".md", ".yml", ".sh")

# Whole files that name both trees because the move is their subject.
DESIGN_RECORD = {"docs/one-root-by-lifetime.md", "docs/one-root-by-lifetime.ko.md"}

# A line carrying one of these keeps the old name on purpose. Each entry is
# checked to still occur somewhere, so a reason cannot outlive its line.
KEEP = {
    ".specseal/handoff": "the retired handoff key, named where the reason it moved is kept",
    "<!-- specs/<work-item-id> -->": "the marker text in CHANGELOG.md and the ledger is unchanged (Q2)",
    "`.specseal/scratch`": "the predecessor of `.git/specseal-scratch`, named as past",
    "`.specseal/` or a top-level `specs/`": "the README saying what nothing reads any more",
    "└── specs/<work-item-id>/": "the tree under `seal/` in the README, relative to it",
    "└── specs/<작업항목-id>/": "the same tree in the Korean README",
    "(`.specseal/`, `specs/<id>/`)": "the READMEs naming the 0.3.x layout as what the move leaves",
    "git mv .specseal/": "the by-hand move in the READMEs' coming-up section",
    "git mv specs/<id>": "the by-hand move's last step, one work item at a time",
}


def tracked(root=ROOT):
    """`(the scanned files on disk, the scanned paths that are not)`.

    `root` is an argument so a case can build a repository with a
    tracked-and-deleted file and watch the guard work; `conftest.on_disk`
    carries why the second half is returned rather than dropped.
    """
    out = git_listing(root, "ls-files", *SCANNED)
    listed = [rel for rel in out if rel.endswith(SUFFIXES) and rel not in DESIGN_RECORD]
    return on_disk(root, listed)


def offenders(rel, text):
    """`(rel, line number, line)` for every live mention of an old root."""
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        if OLD_ROOT.search(line) and not any(k in line for k in KEEP):
            found.append((rel, number, line.strip()[:100]))
    return found


def offenders_under(root=ROOT):
    """Every live mention of an old root in the files `root` still has."""
    found = []
    files, _ = tracked(root)
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            found += offenders(rel, f.read())
    return found


def test_no_shipped_document_names_the_old_roots():
    found = offenders_under()
    assert not found, "\n".join(
        [
            "the old roots are named as live paths — rewrite to seal/, or add the",
            "line's reason to KEEP:",
        ]
        + [f"  {rel}:{number}  {line}" for rel, number, line in found]
    )


# The two paths the scan names to prove it reaches both ends of its own
# prefix list, and what a case declining over them says it is not judging.
COVERED = ("skills/implement/SKILL.md", ".github/workflows/hygiene.yml")
DECLINES_COVERAGE = "the named-coverage half of test_the_scan_covers_something"
DECLINES_KEEP = "the KEEP allowlist's liveness check"


def uncovered(files, missing):
    """The named paths the scan no longer covers, or `pytest.skip` when a
    skipped file is one of them.

    Q3's third case, found by reading the five modules rather than by either
    ticket. `skills/implement/SKILL.md` leaving the corpus through a `git mv`
    that has not been staged is exactly the state this work is about, and
    without this the case reports the scan as no longer covering a file that
    is merely somewhere else — a verdict about coverage taken from evidence
    about the working tree.

    **Conditional on every absent path being explained.** A named path absent
    for another reason is a real loss of coverage, and declining over a
    neighbour that is merely mid-edit would report it nowhere — the decline
    carrying a finding away with it, which is a worse failure than the one it
    was written against.
    """
    absent = [rel for rel in COVERED if rel not in files]
    unexplained = [rel for rel in absent if rel not in missing]
    if absent and not unexplained:
        decline_if_shrunken(sorted(set(absent) & set(missing)), DECLINES_COVERAGE)
    return unexplained


def keep_entries_not_in_use(root=ROOT):
    """The `KEEP` entries no scanned file carries, or `pytest.skip` when a
    skipped file could be the one carrying an entry.

    The decline is conditional on there being a finding at all, which is what
    keeps a mid-edit tree from turning this check off: a skip can only ever
    make an entry LOOK unused, never used, so a run that finds every entry
    still in place has reached the right verdict whatever it skipped.
    """
    corpus = ""
    files, missing = tracked(root)
    for rel in files:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
            corpus += f.read()
    unused = [k for k in KEEP if k not in corpus]
    if unused:
        decline_if_shrunken(missing, DECLINES_KEEP)
    return unused


def test_the_scan_covers_something():
    files, missing = tracked()
    # The floor survives a skip on purpose: a corpus that still clears it has
    # proved the scan is not reading nothing, whatever else the tree is
    # missing — and that is the half which stops a sweep passing on an empty
    # read, so it is the wrong half to turn off on a shrunken corpus.
    assert len(files) > 30, files
    absent = uncovered(files, missing)
    assert not absent, f"the scan no longer covers {absent}"


@pytest.mark.parametrize(
    "line",
    [
        "rows go in `.specseal/map/<work-item-id>.md`",
        "the gate reads `specs/<work-item-id>/routing.md`",
        "<!-- specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT",
        "opt-in: `.specseal/` at the repo root",
    ],
)
def test_the_check_can_fail(line):
    assert offenders("x.md", line) == [("x.md", 1, line)]


@pytest.mark.parametrize(
    "line",
    [
        "rows go in `seal/ledger/<work-item-id>.md`",
        "the gate reads `seal/specs/<work-item-id>/routing.md`",
        "one `###` section marked with `<!-- specs/<work-item-id> -->`",
        "the file `.git/specseal-scratch`",
    ],
)
def test_the_new_root_and_the_kept_forms_pass(line):
    assert offenders("x.md", line) == []


def test_every_keep_entry_is_still_in_use():
    """An allowlist line nothing matches is a reason with no line under it —
    delete it rather than let the list say the old name is still somewhere."""
    unused = keep_entries_not_in_use()
    assert not unused, f"KEEP entries no scanned file carries any more: {unused}"


def test_the_scan_survives_a_tracked_file_the_tree_deleted(tmp_path):
    """The same defect as #432, one module over: this sweep walks its own
    `git ls-files` and opens every path, so a fold that leaves a tracked path
    with nothing behind it ends the walk before any document is judged."""
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "docs/live.md": "rows go in `.specseal/map/<work-item-id>.md`\n",
            "docs/folded.md": "the fragment the fold removes\n",
        },
        deleted=["docs/folded.md"],
    )
    files, missing = tracked(root)
    assert missing == ["docs/folded.md"], missing
    assert files == ["docs/live.md"], files
    assert offenders_under(root) == [
        ("docs/live.md", 1, "rows go in `.specseal/map/<work-item-id>.md`")
    ]


def test_a_skipped_file_does_not_read_as_a_dead_keep_entry(tmp_path):
    """The inverse direction, which neither ticket names.

    To this case a file the working tree deleted and an allowlist entry
    nobody carries any more are the same evidence, so a bare skip buys it a
    false alarm on an ordinary mid-edit tree. It declines and names the path
    instead.
    """
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "docs/carrier.md": "\n".join(KEEP) + "\n",
            "docs/other.md": "nothing kept here\n",
        },
        deleted=["docs/carrier.md"],
    )
    with pytest.raises(pytest.skip.Exception) as declined:
        keep_entries_not_in_use(root)
    reason = str(declined.value)
    assert "docs/carrier.md" in reason, reason
    assert DECLINES_KEEP in reason, reason
    assert "not judging" in reason, reason


def test_a_present_carrier_still_proves_the_entries_alive(tmp_path):
    """The decline is conditional on a finding, so a tree that is merely
    mid-edit does not turn the check off."""
    root = build_tracked_tree(
        tmp_path / "r",
        {
            "docs/carrier.md": "\n".join(KEEP) + "\n",
            "docs/folded.md": "the fragment the fold removes\n",
        },
        deleted=["docs/folded.md"],
    )
    assert keep_entries_not_in_use(root) == []


def test_a_skipped_file_does_not_read_as_lost_coverage():
    """Q3's third case. A named path that is missing from disk is not a path
    the scan has stopped covering."""
    with pytest.raises(pytest.skip.Exception) as declined:
        uncovered(files=[], missing=list(COVERED))
    reason = str(declined.value)
    assert all(rel in reason for rel in COVERED), reason
    assert DECLINES_COVERAGE in reason, reason
    # A named path absent for any other reason is a finding, not a skip.
    assert uncovered(files=[], missing=[]) == list(COVERED)


def test_a_real_loss_of_coverage_survives_a_neighbour_being_mid_edit():
    """The decline must not carry a finding away with it.

    One named path merely off disk and the other genuinely gone from the
    corpus: the first is explained by the working tree and the second is not,
    so the case has to report the second rather than decline over the first.
    """
    try:
        found = uncovered(files=[], missing=[COVERED[0]])
    except pytest.skip.Exception as declined:
        raise AssertionError(
            "a named path that genuinely left the corpus was carried away by a "
            f"decline over its neighbour: {declined}"
        ) from None
    assert found == [COVERED[1]], found
