"""The ledger and fragment rules have one home each, and the rest link (#715).

A rule written in two files is one rule today and two after the first edit to
either, and the quiet copy is the one a reader acts on. `CLAUDE.md` and
`CONTRIBUTING.md` used to carry the same sentences about ledger corrections,
and the two disagreed once: one forbade editing the file at all while the
other forbade appending to it, which left a branch with no reading that
permits the only correct act. Their pin then held the two copies against each
other, which kept them equal and kept them both.

So each rule now has one home, which states it, and every other carrier names
that home's path and section and states none of it:

  the re-read and the correction   docs/the-evidence-ledger.md
  the conflict rule                docs/the-evidence-ledger.md
  the coordinate rules             docs/the-evidence-ledger.md
  the fragment rule                docs/the-record-layout.md

A needle is a sentence only the home writes. The carriers are the class
`seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-
never-changes/spec.md` §*The classes, enumerated* lists, taken by the same
instrument: every file that names `--reverify` or states where a ledger row
stands, outside the records, the releases and the changelog.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LEDGER = "docs/the-evidence-ledger.md"
LAYOUT = "docs/the-record-layout.md"

# rule: (home, section heading, needles only the home writes)
RULES = {
    "re-read": (
        LEDGER,
        "A released row is read again in the branch's fragment",
        (
            "A re-read or a correction is a citing row in the branch's own fragment.",
            "The checker reads a released row together with the rows that read it, "
            "as one family:",
            "Without the row, a released row is kept true where it stands.",
        ),
    ),
    "conflict": (
        LEDGER,
        "A correction a merge dropped",
        (
            "resolve it hunk by hunk and read both sides.",
            "Hunk by hunk has two halves, and only the notes are a union.",
        ),
    ),
    "coordinate": (
        LEDGER,
        "A row is a content anchor, and it names no commit",
        (
            "That removes a whole chain rather than one rule from it.",
            "A stale minor anchor widens to its unit and says re-read,",
        ),
    ),
    "fragment": (
        LAYOUT,
        "A change writes fragments, never a shared file",
        (
            "an entry under `CHANGELOG.md`'s `## Unreleased`",
            "No two work items share an id, so no two branches share a file.",
        ),
    ),
}

# The two files a session or a contributor reads first, and the rules each
# carries; each names the home's path and section for every one of them.
LINKED = {
    "CLAUDE.md": ("re-read", "conflict", "coordinate", "fragment"),
    "CONTRIBUTING.md": ("re-read", "conflict", "fragment"),
}

# The rest of the class, from `spec.md` §*The classes, enumerated*. They may
# describe their own act; they state none of a home's needles.
CARRIERS = (
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "docs/release-checklist.md",
    "docs/branch-and-release.md",
    "skills/implement/SKILL.md",
    "skills/settle/SKILL.md",
    "skills/evidence-check/SKILL.md",
    "skills/code-review/orchestration.md",
    "seal/README.md",
    "seal/ledger.md",
    ".github/scripts/fold_ledger.py",
    "skills/evidence-check/scripts/correction_check.py",
    "hooks/evidence-advisor.py",
    "skills/settle/scripts/settle.py",
)


def flat(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return " ".join(f.read().split())


def section(rel, heading):
    """The text under `## heading` in REL, to the next `## `, flattened."""
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        text = f.read()
    parts = re.split(r"(?m)^## ", text)
    found = [p for p in parts if p.startswith(heading + "\n")]
    assert len(found) == 1, f"{rel} has no single `## {heading}`"
    return " ".join(found[0].split())


def stated_in_carriers(needles):
    return [
        (rel, needle)
        for rel in CARRIERS
        for needle in needles
        if " ".join(needle.split()) in flat(rel)
    ]


def test_each_home_states_its_rule_under_its_section():
    for rule, (home, heading, needles) in RULES.items():
        body = section(home, heading)
        missing = [n for n in needles if " ".join(n.split()) not in body]
        assert not missing, f"{home} §{heading} does not state {rule}: {missing}"


def test_no_carrier_restates_a_home():
    found = []
    for _, (_, _, needles) in RULES.items():
        found += stated_in_carriers(needles)
    assert not found, found


def test_the_two_first_reads_link_each_rule_to_its_home():
    """A link is the home's path and its section's name, in the carrier."""
    missing = []
    for rel, rules in LINKED.items():
        text = flat(rel)
        for rule in rules:
            home, heading, _ = RULES[rule]
            if home not in text or heading not in text:
                missing.append((rel, rule, home, heading))
    assert not missing, missing


def test_a_restored_copy_is_named(tmp_path, monkeypatch):
    """The check can fail: one needle put back into `CLAUDE.md` is named."""
    copy = tmp_path / "CLAUDE.md"
    with open(os.path.join(ROOT, "CLAUDE.md"), encoding="utf-8") as f:
        copy.write_text(
            f.read() + "\nHunk by hunk has two halves, and only the notes are a "
            "union.\n",
            encoding="utf-8",
        )
    real_flat = flat

    def patched(rel):
        if rel == "CLAUDE.md":
            return " ".join(copy.read_text(encoding="utf-8").split())
        return real_flat(rel)

    monkeypatch.setitem(globals(), "flat", patched)
    found = stated_in_carriers(RULES["conflict"][2])
    assert ("CLAUDE.md", RULES["conflict"][2][1]) in found
