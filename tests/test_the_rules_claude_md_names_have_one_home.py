"""The rules `CLAUDE.md` names have one home each, and `CLAUDE.md` links (#730).

#715 gave the ledger and fragment rules one home each and left the rest of
`CLAUDE.md` alone. Three more of its rows restated a rule another file holds,
and one of those copies had already gone false: the merge table there said a
`# RIDER:` stamp names a commit, where its home had said the reverse since
work item `1788826000`, and it had lost two of the home's six rows. Nothing
pinned that copy, so nothing went red. A fourth restatement sat at the foot of
the goal section, beside the link to the rule it restated.

So each rule now has one home, which states it, and `CLAUDE.md` keeps a row
that names the home's path and section, says when the rule applies, and gives
the act in one sentence of its own words:

  the merge method per direction   docs/branch-and-release.md
  no real identifiers              CONTRIBUTING.md
  the commit cadence               skills/implement/SKILL.md, step 2
  the question batch               skills/implement/SKILL.md, step 1

A needle is a sentence only the home writes and the link row does not need.
No carrier may contain one, the home aside. The carriers are the files
`seal/specs/1791076836-every-rule-claude-md-restates-has-one-home/spec.md`
names in its Scope 1-4 and D1, and the release checklist its O3 names.

What this does not hold: the act sentence in a `CLAUDE.md` row is the rule in
other words, and a later change to the rule's values (a seventh merge
direction, a second fixture domain) has to reach the row as well. Only the
home's sentences are pinned here, so a stale value in a row is a reviewer's
finding. That is spec D2's stated cost, and it is narrower than a whole table
drifting unseen.

This is the shape `tests/test_the_ledger_rules_have_one_home.py` set, in a
module of its own because that one is named for the ledger rules.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BRANCHES = "docs/branch-and-release.md"
CONTRIBUTING = "CONTRIBUTING.md"
IMPLEMENT = "skills/implement/SKILL.md"

# rule: (home, section heading, needles only the home writes)
RULES = {
    "merge": (
        BRANCHES,
        "Work accumulates on a release branch",
        (
            "| a feature branch | `release/vX.Y.Z` | **squash** | *Squash and merge* |",
            "Pick the other one and something downstream stops resolving, so "
            "this table is the whole rule and the paragraphs below are why.",
            "A hotfix was squashed in once, and it cost nothing only because no "
            "rider stamp and no round record named its commits",
        ),
    ),
    "identifiers": (
        CONTRIBUTING,
        "House rules",
        (
            "extend its allowlist deliberately, never to make a test pass.",
            "both incidents that forced a rewrite of this repository's history "
            "entered exactly this way",
        ),
    ),
    "cadence": (
        IMPLEMENT,
        "2. Implement, and feed evidence back where you verified it",
        (
            "What an intermediate commit costs is a property of the repository "
            "rather than a fact about committing",
            "*Commit as you go* alone does not settle the cadence.",
        ),
    ),
    "batch": (
        IMPLEMENT,
        "1. Read the spec before the code",
        (
            "Asking one at a time is the same failure spread out: three "
            "interruptions cost three waits.",
            "**A question you can answer is not a question.**",
        ),
    ),
}

# The files that must name a home's path and section, and for which rules.
# `CLAUDE.md` is loaded into every session; the four code comments cited it
# for the identifiers rule until this work pointed them at the home.
LINKED = {
    "CLAUDE.md": ("merge", "identifiers", "cadence", "batch"),
    ".github/scripts/plugin_directory_check.py": ("identifiers",),
    "tests/test_the_plugin_directory_answers_the_box.py": ("identifiers",),
    "tests/test_a_workflow_is_read_the_one_way.py": ("identifiers",),
    "tests/test_the_gate_asks_the_range_ci_will_ask.py": ("identifiers",),
    # The fifth citation, spelled `no-real-identifiers`, which the enumerating
    # grep's `real identifier` did not match (round 1). Round 1's fix pass
    # re-enumerated every `CLAUDE.md` mention against all four rules' words,
    # hyphenated, spaced or quoted, and found no other.
    "agents/warden.md": ("identifiers",),
}

# Every file in the class. A home is a carrier of the other rules, so a rule's
# own home is skipped when that rule's needles are looked for.
CARRIERS = (
    "CLAUDE.md",
    CONTRIBUTING,
    BRANCHES,
    IMPLEMENT,
    "docs/release-checklist.md",
    "templates/claude-md-block.md",
    ".github/scripts/plugin_directory_check.py",
    "tests/test_the_plugin_directory_answers_the_box.py",
    "tests/test_a_workflow_is_read_the_one_way.py",
    "tests/test_the_gate_asks_the_range_ci_will_ask.py",
    "agents/warden.md",
)


def flat(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return " ".join(f.read().split())


def section(rel, heading):
    """The text under the heading in REL, at any level, flattened.

    It runs to the next heading of the same level or above, so a `###`
    section keeps its own `####` children and stops at its sibling."""
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        text = f.read()
    heads = list(re.finditer(r"(?m)^(#{2,6}) (.+?)\s*$", text))
    found = [h for h in heads if h.group(2) == heading]
    assert len(found) == 1, f"{rel} has no single heading `{heading}`"
    start, level = found[0], len(found[0].group(1))
    end = len(text)
    for h in heads:
        if h.start() > start.start() and len(h.group(1)) <= level:
            end = h.start()
            break
    return " ".join(text[start.end() : end].split())


def restated(texts):
    """(carrier, needle) for every needle a carrier other than its home holds.

    TEXTS maps a carrier to its flattened text, so a case can hand in a copy."""
    return [
        (rel, needle)
        for home, _, needles in RULES.values()
        for rel, text in texts.items()
        if rel != home
        for needle in needles
        if " ".join(needle.split()) in text
    ]


def unlinked(texts):
    """(file, rule) for every rule a linked file does not name the home of."""
    missing = []
    for rel, rules in LINKED.items():
        text = texts[rel]
        for rule in rules:
            home, heading, _ = RULES[rule]
            if home not in text or heading not in text:
                missing.append((rel, rule))
    return missing


def tree():
    return {rel: flat(rel) for rel in sorted(set(CARRIERS) | set(LINKED))}


def test_each_home_states_its_rule_under_its_section():
    for rule, (home, heading, needles) in RULES.items():
        body = section(home, heading)
        missing = [n for n in needles if " ".join(n.split()) not in body]
        assert not missing, f"{home} §{heading} does not state {rule}: {missing}"


def test_no_carrier_restates_a_home():
    found = restated(tree())
    assert not found, (
        f"a carrier states a home's own sentence: {found}. Link to the home "
        "instead, per `docs/the-record-layout.md`: a rule written in two "
        "files is two rules after the first edit to either"
    )


def test_every_linked_file_names_each_home_and_section():
    """A link is the home's path and its section's name, in the file."""
    missing = unlinked(tree())
    assert not missing, (
        f"these files do not name the home of a rule they carry: {missing}"
    )


def test_a_restored_copy_is_named():
    """The check can fail: the old merge table's row put back is named."""
    texts = tree()
    texts["CLAUDE.md"] += " " + RULES["merge"][2][0]
    assert ("CLAUDE.md", RULES["merge"][2][0]) in restated(texts)


def test_a_removed_link_is_named():
    """The other half can fail too: a row that drops its home's path is named,
    and so is one that keeps the path and drops the section."""
    texts = tree()
    texts["CLAUDE.md"] = texts["CLAUDE.md"].replace(CONTRIBUTING, "the guide")
    assert ("CLAUDE.md", "identifiers") in unlinked(texts)
    texts = tree()
    texts["CLAUDE.md"] = texts["CLAUDE.md"].replace("§*House rules*", "")
    assert ("CLAUDE.md", "identifiers") in unlinked(texts)


def test_a_section_stops_at_its_sibling():
    """*Under its section* means that section: step 1 of `implement` does not
    run on into step 2, so a needle moved between them is caught."""
    first = section(IMPLEMENT, RULES["batch"][1])
    for needle in RULES["cadence"][2]:
        assert " ".join(needle.split()) not in first
