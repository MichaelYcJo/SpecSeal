"""A format this repository owns is read by one reader, and a copy is red on
arrival.

Issue #867, from #834's inventory: the ledger coordinate was spelled by four
regexes and a markdown heading by four rules, and the copies answered one file
differently. The build left each with one reader. What keeps it that way is
not a sentence in a docstring -- the copies were each written beside a
docstring pointing at the original -- but the two greps `spec.md` S12 names,
run over every shipped script, so the next copy fails here the day it lands.

Each exemption is named with what makes it not a copy. A new one is a
decision, written here with its reason, never a widened pattern.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHIPPED = ("hooks", "skills", os.path.join(".github", "scripts"))


def shipped_scripts():
    for top in SHIPPED:
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, top)):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for name in filenames:
                if name.endswith(".py"):
                    path = os.path.join(dirpath, name)
                    yield os.path.relpath(path, ROOT).replace(os.sep, "/"), path


# A regex fragment that reads a coordinate's hash: `@` and then six or more hex
# digits, optionally inside a named group.
HASH_AFTER_AT = re.compile(r"@(?:\(\?P<\w+>)?\[0-9a-f\]\{6")

# Where such a fragment is not a second grammar of the coordinate.
COORDINATE_EXEMPT = {
    # The one grammar, and the forms built from its pieces in the same file
    # (the pact anchor, the record of pact changes' `→ @<new>`).
    "skills/evidence-check/scripts/evidence_check.py": "the grammar itself",
    # A pact review's `Change` cell names a record as `<work-item-id>@<content
    # hash>`: an id, not a path and a locator, so it is no coordinate.
    "skills/evidence-check/scripts/pact_check.py": "CHANGE_RE, a record id",
}


def test_no_shipped_script_spells_the_coordinate_grammar_again():
    """S12 of #867, the coordinate's grep. `correction_check.py`,
    `settle.py` and `.github/scripts/rider_check.py` each kept a pattern
    ending `@[0-9a-f]{6,…}` and now read `evidence_check.py#ANCHOR_RE` or
    its pieces. Seen red against 5623d728, where it names those three."""
    found = []
    for rel, path in shipped_scripts():
        if rel in COORDINATE_EXEMPT:
            continue
        with open(path, encoding="utf-8") as f:
            for number, line in enumerate(f, 1):
                if HASH_AFTER_AT.search(line):
                    found.append(f"{rel}:{number}: {line.strip()}")
    assert not found, "a second grammar of the coordinate:\n" + "\n".join(found)


def test_every_coordinate_exemption_still_holds_the_fragment_it_excuses():
    """An exemption whose file no longer holds the fragment excuses nothing,
    and the next copy written there would pass unseen."""
    for rel in COORDINATE_EXEMPT:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            assert HASH_AFTER_AT.search(f.read()), rel
