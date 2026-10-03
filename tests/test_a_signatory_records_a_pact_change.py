"""A signatory records a pact change when its re-read moves code a clause binds (#647, C).

A signatory names the pact it signs in `seal/config.md` and cites clauses as
pact anchors in its ledger rows. When `evidence-check --reverify` moves the
hash of a row that cites a clause of a declared pact -- in place, or into a
`Re-read ·` row under the freeze -- or leaves a coordinate of one BROKEN, it
appends one row per ledger row to `seal/pact-changes/<work-item-id>.md` and
prints a `recorded` line. S7-S11 of the work item's `spec.md`.

Each case builds a temporary signatory: `src/orders.py`, a ledger row citing
`pact:orders-api/"## Order response shape / ### Fields"@1a2b3c4d` beside a
local coordinate, and a `Pact` row naming `git@example.com:org/orders-api.git`.
"""

import importlib.util
import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")
ITEM = "1791020000-a-field-is-added"
FRAGMENT = f"seal/ledger/{ITEM}.md"
RECORD = f"seal/pact-changes/{ITEM}.md"
PACT_URL = "git@example.com:org/orders-api.git"
CLAUSE = 'pact:orders-api/"## Order response shape / ### Fields"@1a2b3c4d'
OTHER = 'pact:billing/"## Invoices"@5e6f7a8b'
SOURCE = "def serialize(order):\n    return {'id': order.id}\n\n\ndef evict(key):\n    return key\n"


def load():
    spec = importlib.util.spec_from_file_location("ec_for_pact_changes", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = load()


def unit_hash(repo, rel, locator):
    text = (repo / rel).read_text(encoding="utf-8")
    places, _ = ec.resolve_unit(rel, locator, text)
    a, b = places[0]
    return ec.content_hash(ec.gfm_lines(text)[a - 1 : b])


def run(repo, *args):
    done = subprocess.run(
        [sys.executable, SCRIPT, "--reverify", *args, str(repo)],
        cwd=str(repo),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return done.returncode, done.stdout + done.stderr


def config_text(*rows):
    return "| Item | Value |\n|---|---|\n" + "".join(
        f"| {item} | {value} |\n" for item, value in rows
    )


def row(label, cites, coord):
    return f"| {label} · the field list | {cites}`{coord}` | read | 2026-10-01 | |\n"


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "orders-web"
    (d / "src").mkdir(parents=True)
    (d / "src" / "orders.py").write_text(SOURCE, encoding="utf-8")
    (d / "seal").mkdir()
    (d / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), ("Pact", PACT_URL)), encoding="utf-8"
    )
    return d


def cite(repo, rows, where=FRAGMENT):
    path = repo / where
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(rows), encoding="utf-8")
    return path


def move_serialize(repo):
    """Edit the code the clause binds, and return its new hash."""
    path = repo / "src" / "orders.py"
    path.write_text(
        SOURCE.replace("'id': order.id", "'id': order.id, 'tax': 0"), encoding="utf-8"
    )
    return unit_hash(repo, "src/orders.py", "serialize")


def record_rows(repo, where=RECORD):
    path = repo / where
    if not path.exists():
        return []
    return [
        ln
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.startswith("| ") and "---" not in ln and not ln.startswith("| Clause")
    ]


def test_s7_a_drifted_row_citing_a_clause_is_recorded(repo):
    """S7. The fragment row is re-stamped as before, and the record gains
    one row naming the clause, the row, the move and the date."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert f"src/orders.py#serialize@{new}" in ledger.read_text(encoding="utf-8")
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `src/orders.py#serialize@{old}` "
        f"→ `@{new}` | 2026-09-04 |"
    ]
    assert f"  recorded seal/pact-changes/{ITEM}.md:" in out, out
    assert f"a pact change for seal/ledger/{ITEM}.md:1" in out, out
    text = (repo / RECORD).read_text(encoding="utf-8")
    assert text.startswith(f"# Pact changes — {ITEM}\n"), text


def test_s7_the_ledger_is_written_exactly_as_before(repo, tmp_path):
    """The record is an addition to the act: the ledger bytes a run writes
    are the bytes the same run writes with no `Pact` row."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    with_pact = ledger.read_text(encoding="utf-8")
    cite(repo, rows)
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared")), encoding="utf-8"
    )
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert ledger.read_text(encoding="utf-8") == with_pact


def test_s8_a_released_row_drifted_is_recorded_beside_its_reread(repo):
    """S8. Under `Ledger frozen from`, the released row takes a `Re-read ·`
    row in the fragment as before, and one pact change is recorded."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    released = cite(
        repo,
        [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")],
        where="seal/releases/0.1.0.md",
    )
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + released.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    cite(repo, [])
    new = move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert "Re-read · O1" in (repo / FRAGMENT).read_text(encoding="utf-8"), out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/releases/0.1.0.md · O1 | `src/orders.py#serialize@{old}` "
        f"→ `@{new}` | 2026-09-04 |"
    ], out


def git(repo, *args):
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def test_s9_a_declared_branch_names_the_record(repo):
    """S9, first half. In-place `--reverify` with no `--into`, on a branch a
    `routing.md` declares, records into that work item's file."""
    git(repo, "init", "-q", "-b", "feat/x")
    (repo / "seal" / "specs" / ITEM).mkdir(parents=True)
    (repo / "seal" / "specs" / ITEM / "routing.md").write_text(
        "| Axis | Answer |\n|---|---|\n| Review | straight to the PR |\n"
        "| Destination | open the pull request |\n| Branch | feat/x |\n",
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "commit",
        "-qm",
        "x",
    )
    new = move_serialize(repo)
    code, out = run(repo, "--checked", "2026-09-04")
    assert code == 0, out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `src/orders.py#serialize@{old}` "
        f"→ `@{new}` | 2026-09-04 |"
    ], out


def test_s9_with_no_work_item_nothing_is_recorded_and_the_row_is_left(repo):
    """S9, second half. No `--into` and no declaration: the row is
    re-stamped as before, nothing is recorded, a `LEFT` line names both
    ways to name a work item, and the exit is 1."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    code, out = run(repo, "--checked", "2026-09-04")
    assert code == 1, out
    assert f"@{new}" in ledger.read_text(encoding="utf-8")
    assert not (repo / "seal" / "pact-changes").exists()
    assert (
        f"  LEFT  seal/ledger/{ITEM}.md:1  {CLAUSE} — a pact change is owed and no "
        "work item names its record: name the work item with `--into "
        "seal/ledger/<work-item-id>.md`, or run it on a branch a "
        "`seal/specs/<work-item-id>/routing.md` declares"
    ) in out, out


@pytest.mark.parametrize(
    "notify, cites, want",
    [
        ("never", f"`{CLAUSE}`, ", None),
        ("always", "", "—"),
        ("when the pact is touched", f"`{OTHER}`, ", None),
        ("always", f"`{OTHER}`, ", "—"),
    ],
    ids=[
        "never",
        "always, no clause",
        "an undeclared pact",
        "always, an undeclared pact",
    ],
)
def test_s10_notify_decides_what_is_recorded(repo, notify, cites, want):
    """S10. `never` records nothing; `always` also records a drifted row
    citing no clause, with `—`; a pact anchor naming an undeclared pact is
    no clause of this pact."""
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), ("Pact", PACT_URL), ("Pact notify", notify)),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", cites, f"src/orders.py#serialize@{old}")])
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    rows = record_rows(repo)
    if want is None:
        assert rows == [], out
    else:
        assert len(rows) == 1 and rows[0].startswith(f"| {want} | "), rows


def test_s11_a_broken_coordinate_is_recorded_and_the_row_left(repo):
    """S11, first half. A coordinate no one place holds is recorded as
    `BROKEN`, and the row is left as today."""
    old = unit_hash(repo, "src/orders.py", "evict")
    rows = [row("O2", f"`{CLAUSE}`, ", f"src/orders.py#evict@{old}")]
    ledger = cite(repo, rows)
    (repo / "src" / "orders.py").write_text(
        SOURCE.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O2 | `src/orders.py#evict@{old}` "
        "BROKEN | 2026-09-04 |"
    ], out


def test_s11_a_second_run_records_nothing_twice(repo):
    """S11, second half. The BROKEN coordinate is still there on the next
    day's run, and the record is not appended to again."""
    old = unit_hash(repo, "src/orders.py", "evict")
    cite(repo, [row("O2", f"`{CLAUSE}`, ", f"src/orders.py#evict@{old}")])
    (repo / "src" / "orders.py").write_text(
        SOURCE.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    first = (repo / RECORD).read_text(encoding="utf-8")
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert code == 0, out
    assert (repo / RECORD).read_text(encoding="utf-8") == first, out
    assert "recorded" not in out, out


def test_a_record_that_will_not_parse_is_left_and_named(repo):
    """The record is written by this command alone; one that will not parse
    is named, nothing is appended to it, and the exit is 1."""
    record = repo / RECORD
    record.parent.mkdir(parents=True)
    record.write_text(
        "| Clause | Row | Code | Checked |\n|---|---|---|---|\n| a | b | c | soon |\n",
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert (
        f"  LEFT  seal/pact-changes/{ITEM}.md  the record has a row at line 3 whose "
        "`Checked` is `soon`, not a date written YYYY-MM-DD — nothing recorded"
    ) in out, out


def test_a_vendored_copy_says_it_recorded_nothing(repo, tmp_path):
    """Q15. A copy with no `hooks/` beside it cannot read the `Pact` row: it
    re-stamps as today, names each row citing a pact, records nothing, and
    the exit is 1."""
    vendored = tmp_path / "tools" / "evidence_check.py"
    vendored.parent.mkdir()
    vendored.write_text(open(SCRIPT, encoding="utf-8").read(), encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    done = subprocess.run(
        [
            sys.executable,
            str(vendored),
            "--reverify",
            "--checked",
            "2026-09-04",
            str(repo),
        ],
        cwd=str(repo),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    out = done.stdout + done.stderr
    assert done.returncode == 1, out
    assert f"@{new}" in ledger.read_text(encoding="utf-8")
    assert not (repo / "seal" / "pact-changes").exists()
    assert (
        f"  LEFT  seal/ledger/{ITEM}.md:1  cites a pact clause, and this copy of "
        "evidence_check.py has no hooks/ beside it to read the `Pact` row with — no "
        "pact change was recorded"
    ) in out, out


def test_a_row_left_whole_moved_nothing_and_records_nothing(repo):
    """A row with no date cell is left whole under `--checked`, hash
    included, so no hash moved and nothing is owed."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    line = f"| O1 · the field list | `{CLAUSE}`, `src/orders.py#serialize@{old}` | read |\n"
    ledger = cite(repo, [line])
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert ledger.read_text(encoding="utf-8") == line, out
    assert code == 1 and "its hash moved and the row has no date cell" in out, out
    assert not (repo / "seal" / "pact-changes").exists(), out


def test_a_coordinate_naming_two_places_is_recorded_broken(repo):
    """A coordinate whose unit now names two places, neither holding the
    recorded content, is left and recorded `BROKEN`."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    (repo / "src" / "orders.py").write_text(
        "def serialize(a):\n    return 1\n\n\ndef serialize(b):\n    return 2\n",
        encoding="utf-8",
    )
    _code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `src/orders.py#serialize@{old}` "
        "BROKEN | 2026-09-04 |"
    ], out


def test_a_released_coordinate_broken_is_recorded(repo):
    """Under the freeze, a released row's coordinate a re-read cannot clear
    is named for a `Corrected ·` row as before, and recorded `BROKEN`."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "evict")
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + row("O2", f"`{CLAUSE}`, ", f"src/orders.py#evict@{old}"),
        encoding="utf-8",
    )
    cite(repo, [])
    (repo / "src" / "orders.py").write_text(
        SOURCE.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "a re-read cannot clear it" in out, out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/releases/0.1.0.md · O2 | `src/orders.py#evict@{old}` "
        "BROKEN | 2026-09-04 |"
    ], out
