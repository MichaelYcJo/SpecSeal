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
true at their SHA. `README.md` and `README.ko.md` move together in phase 3
of the work item, because the hygiene workflow warns when they do not; they
join `SCANNED` then.
"""

import os
import re
import subprocess

import pytest

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
    "`specs/` + `.specseal/` → `seal/`": "the checklist line for the move in docs/flow.md",
    "└── specs/<work-item-id>/": "the tree under `seal/` in the README, relative to it",
}


def tracked():
    out = subprocess.run(
        ["git", "ls-files", *SCANNED],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.split()
    return [rel for rel in out if rel.endswith(SUFFIXES) and rel not in DESIGN_RECORD]


def offenders(rel, text):
    """`(rel, line number, line)` for every live mention of an old root."""
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        if OLD_ROOT.search(line) and not any(k in line for k in KEEP):
            found.append((rel, number, line.strip()[:100]))
    return found


def test_no_shipped_document_names_the_old_roots():
    found = []
    for rel in tracked():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            found += offenders(rel, f.read())
    assert not found, "\n".join(
        [
            "the old roots are named as live paths — rewrite to seal/, or add the",
            "line's reason to KEEP:",
        ]
        + [f"  {rel}:{number}  {line}" for rel, number, line in found]
    )


def test_the_scan_covers_something():
    files = tracked()
    assert len(files) > 30, files
    assert "skills/implement/SKILL.md" in files
    assert ".github/workflows/hygiene.yml" in files


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
    corpus = ""
    for rel in tracked():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as f:
            corpus += f.read()
    unused = [k for k in KEEP if k not in corpus]
    assert not unused, f"KEEP entries no scanned file carries any more: {unused}"
