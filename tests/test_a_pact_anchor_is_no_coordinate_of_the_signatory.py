"""A pact anchor is invisible to the signatory's own evidence check (#647, B).

A signatory cites a clause of a pact held in another repository as

    pact:<name>/"<heading path>"@<hash>

in its spec's Grounding and in a ledger row's `Clause` cell, beside its own
code coordinate in `Code grounds`. `pact-check` at the pact's repository
grades it. The signatory's own `evidence-check` must read past it: a pact
anchor read as a coordinate would be `BROKEN` (no such file here), and a
clause heading holding `v1.2:3` read by `OLD_COORD_RE` would be `OLD-FORMAT`
at exit 2.

`ANCHOR_RE` cannot match inside one by construction, and the readers that
blank `ANCHOR_RE` before reading with another pattern blank pact anchors
first: `old_format_rows`, `malformed_rows` and `migrate` (S7 of the work
item's `spec.md`).
"""

import importlib.util
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def load():
    spec = importlib.util.spec_from_file_location("ec_for_pact_anchors", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = load()

# Every shape a clause heading can take that the grammar has to carry: a
# nested path, an escaped pipe and quote, a `#` inside the text, a version
# carrying `:` and digits, a dotted and an underscored name.
PACT_ANCHORS = (
    'pact:orders-api/"## Order response shape"@1a2b3c4d',
    'pact:orders-api/"## Order response shape / ### Fields"@1a2b3c4d',
    'pact:orders.api/"## v1.2:3 shape"@1a2b3c4d',
    'pact:orders_api/"## A \\| B / ### \\"quoted\\""@abcdef12',
    'pact:x/"## C# clients"@abcdef1234',
)

SERVICE = "def handler(x):\n    return x + 1\n"
LEDGER_HEADER = (
    "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    "|---|---|---|---|---|\n"
)


@pytest.mark.parametrize("anchor", PACT_ANCHORS)
def test_no_coordinate_pattern_matches_inside_a_pact_anchor(anchor):
    """The grammar: the pact pattern takes the whole anchor, and
    `ANCHOR_RE` finds nothing in it, in a cell or alone."""
    assert ec.PACT_ANCHOR_RE.fullmatch(anchor), anchor
    for text in (anchor, f"| {anchor} |", f"see `{anchor}`, cited"):
        assert ec.ANCHOR_RE.search(text) is None, text


def test_a_word_ending_in_pact_is_not_an_anchor():
    """`compact:` is a word, and the look-behind keeps it one."""
    assert ec.PACT_ANCHOR_RE.search('compact:x/"## A"@1a2b3c4d') is None


def signatory(tmp_path, clause_cell, grounds_extra=""):
    """A signatory tree: one Python unit and a ledger row citing it, with
    CLAUSE_CELL as the row's `Clause` and GROUNDS_EXTRA after its local
    coordinate in `Code grounds`."""
    root = tmp_path / "signatory"
    (root / "src").mkdir(parents=True)
    (root / "seal").mkdir()
    (root / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    regions, _ = ec.resolve_unit("src/service.py", "handler", SERVICE)
    start, end = regions[0]
    digest = ec.content_hash(ec.gfm_lines(SERVICE)[start - 1 : end])
    grounds = f"`src/service.py#handler@{digest}`" + grounds_extra
    ledger = root / "seal" / "ledger.md"
    ledger.write_text(
        LEDGER_HEADER
        + f"| {clause_cell} | {grounds} | **Executed** | 2026-10-03 | |\n",
        encoding="utf-8",
    )
    return root, ledger


def test_a_pact_anchor_in_the_clause_cell_leaves_the_local_coordinate_alone(
    tmp_path,
):
    """S7. The signatory's check reports its own coordinate and nothing
    for the pact anchor: no OLD-FORMAT for `v1.2:3`, no BROKEN, no
    EXTERNAL, and exit 0."""
    clause = (
        'P1 · built against `pact:orders-api/"## v1.2:3 shape / ### Fields"@1a2b3c4d`'
    )
    root, ledger = signatory(tmp_path, clause)
    findings = ec.check_ledger(str(ledger), str(root), {})
    assert [f[0] for f in findings] == ["OK"], findings
    done = subprocess.run(
        [sys.executable, SCRIPT, "--strict", "."],
        cwd=str(root),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    out = done.stdout + done.stderr
    assert done.returncode == 0, out
    for word in ("OLD-FORMAT  ", "BROKEN  ", "EXTERNAL  ", "MALFORMED  "):
        assert word not in out, out


def test_a_pact_anchor_beside_the_local_coordinate_is_not_malformed(tmp_path):
    """A pact anchor written into `Code grounds` beside the code coordinate
    is not a coordinate the ledger failed to write."""
    root, ledger = signatory(
        tmp_path,
        "P2 · the field list",
        ', `pact:orders-api/"## v1.2:3 shape / ### Fields"@1a2b3c4d`',
    )
    findings = ec.check_ledger(str(ledger), str(root), {})
    assert [f[0] for f in findings] == ["OK"], findings


def test_migrate_leaves_a_pact_anchor_alone(tmp_path):
    """`--migrate` reads the line after blanking coordinates; a pact
    clause's `v1.2:3` is not a row to migrate, so nothing is left behind
    and the file is untouched."""
    clause = 'P3 · `pact:orders-api/"## v1.2:3 shape"@1a2b3c4d`'
    root, ledger = signatory(tmp_path, clause)
    before = ledger.read_text(encoding="utf-8")
    assert ec.old_format_rows(before) == []
    assert ec.migrate([str(ledger)], str(root)) == (0, [], 0)
    assert ledger.read_text(encoding="utf-8") == before


# --- the pact in the layout --------------------------------------------------

TREE_LINE = ("├", "└", "│")


def tree_drawings():
    """Every tracked text file with a tree line naming `parity.md`, found
    the way the work item enumerated them, so a drawing added later is held
    too. The work item's own records and the changelog quote trees and are
    not drawings."""
    out = subprocess.run(
        ["git", "-C", ROOT, "grep", "-l", "-E", "(├|└|│).*parity\\.md", "--"],
        capture_output=True,
        encoding="utf-8",
    ).stdout.split()
    return sorted(
        p for p in out if not p.startswith("seal/specs/") and p != "CHANGELOG.md"
    )


def test_every_layout_tree_that_draws_parity_draws_the_pact():
    """`seal/pact.md` is a permanent file of the root, held in the pact's
    repository only, so every drawing of the root lists it beside
    `parity.md`."""
    drawings = tree_drawings()
    assert len(drawings) >= 7, drawings
    for rel in drawings:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
            lines = handle.read().splitlines()
        trees = [ln for ln in lines if ln.lstrip().startswith(TREE_LINE)]
        assert any("pact.md" in ln for ln in trees), rel
