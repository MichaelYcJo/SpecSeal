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

import ast
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


# A code line that reads a markdown heading by a rule of its own: a counted
# `#` run in a pattern, `#{1,6}`, `#{2,3}` or any `#{<digit>`, or
# `startswith("#` asked of a line. A docstring and a whole-line comment are
# prose about the rule and are not read. It read `#{1,6}` alone until round
# 1 of #867 (🟡 6), and `unverified_check.py`'s `^#{2,3}\s` passed it.
HEADING_SPELLING = re.compile(r'#\{\d|startswith\(\(?"#')

# Where such a line is not a second spelling of the heading rule, each by
# (file, a piece of the line) and why.
HEADING_EXEMPT = {
    (
        "skills/evidence-check/scripts/evidence_check.py",
        "GITHUB_HEADING_RE",
    ): "the slugger: which `#slug` links resolve, not a section's end (spec Out)",
    (
        "hooks/config.py",
        "ATX_HEADING",
    ): "the GFM table walker's table-end rule, held to cmark-gfm (spec Out)",
    (
        "skills/code-review/scripts/round_record.py",
        r"|\#{1,6}(?=\s|$)",
    ): "where a hand-wrapped paragraph ends, pinned pairwise (spec Out)",
    (
        "skills/code-review/scripts/survivor_check.py",
        r"\#{1,6}(?=\s|$)",
    ): "where a hand-wrapped paragraph ends, pinned pairwise (spec Out)",
    (
        ".github/scripts/issue_claims_check.py",
        r"|\#{1,6}(?=\s|$)",
    ): "where a hand-wrapped paragraph ends, pinned pairwise (spec Out)",
    (
        ".github/scripts/fold_ledger.py",
        "HEADING_RE = re.compile",
    ): "the fold's demotion of a fragment's headings, which rewrites bytes; "
    "left by #867 and named in its overview",
    (
        "skills/settle/scripts/settle.py",
        'if line.startswith("## "):',
    ): "the fold's own `## X.Y.Z` section line, an owned format (spec Out)",
    (
        ".github/scripts/gather_changelog.py",
        'lines[n].startswith("## ")),',
    ): "the gathered changelog's own `## X.Y.Z` line, an owned format (spec Out)",
    (
        ".github/scripts/gather_changelog.py",
        'line.startswith("## ")), None)',
    ): "the gathered changelog's own `## X.Y.Z` line, an owned format (spec Out)",
    (
        ".github/scripts/fold_ledger.py",
        'lines[n].startswith("## ") and n not in fenced',
    ): "the fold's own `## X.Y.Z` section line, an owned format (spec Out)",
    (
        "skills/verify/scripts/deferral_check.py",
        'rest.startswith("#")',
    ): "a YAML comment in a workflow's `on:` key",
    (
        "skills/verify/scripts/deferral_check.py",
        'follow.lstrip().startswith("#")',
    ): "a YAML comment in a workflow's `on:` block",
    (
        "skills/verify/scripts/deferral_check.py",
        'stripped.startswith("#")',
    ): "a YAML or shell comment in a workflow's run lines",
    (
        ".github/scripts/rider_check.py",
        'stripped.startswith("#") and',
    ): "a Python or shell comment, where a rider lives",
    (
        ".github/scripts/rider_check.py",
        'lines[j + 1].lstrip().startswith("#")',
    ): "a Python or shell comment, where a rider lives",
}


def code_lines(path):
    """(line number, line) for every line of the script at PATH that is
    code: not inside a docstring, and not a whole-line comment."""
    with open(path, encoding="utf-8") as f:
        source = f.read()
    prose = set()
    for node in ast.walk(ast.parse(source)):
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            prose.update(range(node.lineno, node.end_lineno + 1))
    for number, line in enumerate(source.split("\n"), 1):
        if number not in prose and not line.lstrip().startswith("#"):
            yield number, line


def heading_spellings():
    for rel, path in shipped_scripts():
        for number, line in code_lines(path):
            if HEADING_SPELLING.search(line):
                yield rel, number, line.strip()


def exempt(rel, line):
    return any(rel == where and piece in line for where, piece in HEADING_EXEMPT)


def test_no_shipped_script_spells_the_heading_rule_again():
    """S12 of #867, the heading's grep. Five readers spelled a markdown
    heading themselves; each now asks `unverified_check.py#heading_level`.
    Every other code line that spells one is named in HEADING_EXEMPT with
    why it is not a reader of a document's sections. Seen red against
    5623d728's readers."""
    found = [
        f"{rel}:{number}: {line}"
        for rel, number, line in heading_spellings()
        if not exempt(rel, line)
    ]
    assert not found, "a second spelling of the heading rule:\n" + "\n".join(found)


def test_every_heading_exemption_still_matches_a_line():
    """An exemption that matches nothing excuses nothing."""
    seen = {
        (where, piece)
        for rel, _number, line in heading_spellings()
        for where, piece in HEADING_EXEMPT
        if rel == where and piece in line
    }
    assert seen == set(HEADING_EXEMPT), set(HEADING_EXEMPT) - seen
