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
# What a run prints after putting the ledger back because an owed pact change
# could not be recorded (round 1, red 1).
UNDONE = (
    "a pact change is owed and was not recorded, so every ledger file this run "
    "wrote is back as it was: nothing was re-stamped"
)
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
    """S9, second half. No `--into` and no declaration: nothing is recorded,
    and so nothing is re-stamped either -- the drift is what records the
    change on the run the `LEFT` line names (round 1, red 1) -- a `LEFT` line
    names both ways to name a work item, and the exit is 1."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--checked", "2026-09-04")
    assert code == 1, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert not (repo / "seal" / "pact-changes").exists()
    assert (
        f"  LEFT  seal/ledger/{ITEM}.md:1  {CLAUSE} — a pact change is owed and no "
        "work item names its record: name the work item with `--into "
        "seal/ledger/<work-item-id>.md`, or run it on a branch a "
        "`seal/specs/<work-item-id>/routing.md` declares — no pact change was "
        "recorded and nothing was re-stamped"
    ) in out, out
    assert UNDONE in out, out


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
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert (
        f"  LEFT  seal/pact-changes/{ITEM}.md  the record has a row at line 3 whose "
        "`Checked` is `soon`, not a date written YYYY-MM-DD — no pact change was "
        "recorded and nothing was re-stamped"
    ) in out, out


def test_a_vendored_copy_says_it_recorded_nothing(repo, tmp_path):
    """Q15. A copy with no `hooks/` beside it cannot read the `Pact` row: it
    names each row citing a pact, records nothing, re-stamps nothing (round
    1, red 1), and the exit is 1."""
    vendored = tmp_path / "tools" / "evidence_check.py"
    vendored.parent.mkdir()
    vendored.write_text(open(SCRIPT, encoding="utf-8").read(), encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
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
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert not (repo / "seal" / "pact-changes").exists()
    assert (
        f"  LEFT  seal/ledger/{ITEM}.md:1  cites a pact clause, and this copy of "
        "evidence_check.py has no hooks/ beside it to read the `Pact` row with — no "
        "pact change was recorded and nothing was re-stamped"
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


# --- round 1, red 1: a change that cannot be recorded re-stamps nothing -----


def test_a_change_left_is_recorded_by_the_remedy_it_names(repo):
    """The run that cannot name a work item re-stamps nothing, so the drift
    is still there for the run its `LEFT` line names, and that run records
    the change. Before the fix it found nothing moved and exited 0."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    new = move_serialize(repo)
    code, out = run(repo, "--checked", "2026-09-04")
    assert code == 1 and "nothing was re-stamped" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `src/orders.py#serialize@{old}` "
        f"→ `@{new}` | 2026-09-04 |"
    ], out


@pytest.mark.parametrize(
    "config_bytes, said",
    [
        (
            b"| Item | Value |\n|---|---|\n| Pact | orders api |\n",
            "the `Pact` rows will not read: `orders api` holds a space",
        ),
        (
            b"| Item | Value |\n|---|---|\n| Pact | git@example.com:org/orders-api.git |"
            b"\n| Note | caf\xe9 |\n",
            "the `Pact` rows will not read: seal/config.md could not be read",
        ),
    ],
    ids=["a Pact row that will not parse", "a config that is not UTF-8"],
)
def test_a_pact_row_that_will_not_read_leaves_the_row(repo, config_bytes, said):
    """The silent path: the `Pact` rows will not read, so nothing could say
    whether the drifted row cites a declared pact. It was exit 0 with the
    ledger re-stamped and no line at all; it is a refusal now."""
    (repo / "seal" / "config.md").write_bytes(config_bytes)
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert said in out and "nothing was re-stamped" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out


@pytest.mark.parametrize("shape", ["an empty file", "a directory"])
def test_a_record_that_will_not_read_or_parse_leaves_the_ledger(repo, shape):
    """The record path's other two exits: an empty record (no table to
    parse) and one that will not read. Each re-stamps nothing."""
    record = repo / RECORD
    record.parent.mkdir(parents=True)
    if shape == "an empty file":
        record.write_text("", encoding="utf-8")
    else:
        record.mkdir()
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert "no pact change was recorded and nothing was re-stamped" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert UNDONE in out, out


def test_under_the_freeze_the_reread_row_is_taken_back_too(repo):
    """Under `Ledger frozen from` the run writes a `Re-read ·` row into the
    `--into` fragment, and re-stamps fragments in place. Where the change
    cannot be recorded, both writes are taken back: the fragment is as it
    was, byte for byte, and so is every other ledger file."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}"),
        encoding="utf-8",
    )
    fragment_rows = [row("F1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    fragment = cite(repo, fragment_rows)
    record = repo / RECORD
    record.parent.mkdir(parents=True)
    record.write_text("", encoding="utf-8")
    before = released.read_bytes()
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert fragment.read_text(encoding="utf-8") == "".join(fragment_rows), out
    assert released.read_bytes() == before, out
    assert UNDONE in out, out


def test_a_fragment_the_run_created_is_removed_again(repo):
    """Under the freeze with `--into` naming a fragment that does not exist
    yet, the run creates it for the `Re-read ·` row; where the change cannot
    be recorded, it is removed again rather than left holding a re-read."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}"),
        encoding="utf-8",
    )
    record = repo / RECORD
    record.parent.mkdir(parents=True)
    record.write_text("", encoding="utf-8")
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert not (repo / FRAGMENT).exists(), out


def test_a_run_that_dies_part_way_puts_the_ledger_back(repo, monkeypatch, capsys):
    """Transactional means a crash too: the re-stamp is written, the record
    step raises, and the ledger is what it was."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)

    def boom(*_args):
        raise RuntimeError("the record step died")

    monkeypatch.setattr(ec, "record_pact_changes", boom)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "evidence_check.py",
            "--reverify",
            "--into",
            FRAGMENT,
            "--checked",
            "2026-09-04",
            str(repo),
        ],
    )
    monkeypatch.chdir(repo)
    with pytest.raises(RuntimeError):
        ec.main()
    assert ledger.read_text(encoding="utf-8") == "".join(rows)


# --- round 1, yellow 2: a second identical run records nothing new ----------


def test_a_broken_coordinate_beside_a_moved_one_is_recorded_once(repo):
    """Run 1 records the move and the BROKEN together; run 2 has only the
    BROKEN left, which was recorded already."""
    s = unit_hash(repo, "src/orders.py", "serialize")
    e = unit_hash(repo, "src/orders.py", "evict")
    cite(
        repo,
        [
            f"| O1 · x | `{CLAUSE}`, `src/orders.py#serialize@{s}`, "
            f"`src/orders.py#evict@{e}` | read | 2026-10-01 | |\n"
        ],
    )
    src = SOURCE.replace("'id': order.id", "'id': order.id, 'tax': 0")
    (repo / "src" / "orders.py").write_text(
        src.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    first = (repo / RECORD).read_text(encoding="utf-8")
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert code == 0, out
    assert (repo / RECORD).read_text(encoding="utf-8") == first, out


def test_a_coordinate_holding_an_escaped_pipe_is_recorded_once(repo):
    """A coordinate and a label holding `\\|`: the record is compared in the
    form its reader reads a cell, so the second run finds them held."""
    doc = repo / "docs" / "x.md"
    doc.parent.mkdir()
    doc.write_text("# T\n\n## A | B\n\ntext one\n", encoding="utf-8")
    h = unit_hash(repo, "docs/x.md", '"## A \\| B"')
    cite(
        repo,
        [
            f'| O1 \\| x · y | `{CLAUSE}`, `docs/x.md#"## A \\| B"@{h}` '
            "| read | 2026-10-01 | |\n"
        ],
    )
    doc.write_text("# T\n", encoding="utf-8")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert len(record_rows(repo)) == 1


REPOSITORY_PIPED = (
    ("templates/sdd-phase.md", '"\\| Field \\| Value \\|"'),
    ("templates/sdd-round.md", '"\\| Field \\| Value \\|"'),
    (
        "templates/sdd-round.md",
        '"# <work-item-id> — review round <N>">"\\| Target SHA \\| <the commit '
        'this round actually reviewed — both, if HEAD moved mid-review> \\|"',
    ),
)


def test_this_repositorys_own_piped_coordinates_are_recorded_once(repo):
    """The three coordinates holding `\\|` that stand in this repository's
    own ledger, cited beside a clause in a signatory holding the same two
    templates, then the templates edited under them: each is recorded once,
    and a second and third run add nothing."""
    for rel in {r for r, _ in REPOSITORY_PIPED}:
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
            target.write_text(handle.read(), encoding="utf-8")
    rows = []
    for n, (rel, locator) in enumerate(REPOSITORY_PIPED, 1):
        text = (repo / rel).read_text(encoding="utf-8")
        m = ec.ANCHOR_RE.search(f"{rel}#{locator}@00000000")
        assert m, locator
        place, claim = m.group("locator"), m.group("claim")
        places, _ = ec.resolve_unit(rel, place, text)
        region = places[0]
        if claim:
            region = ec.minor_region(rel, text, region, claim)[0]
        digest = ec.content_hash(ec.gfm_lines(text)[region[0] - 1 : region[1]])
        rows.append(
            f"| P{n} \\| piped · t | `{CLAUSE}`, `{rel}#{locator}@{digest}` "
            "| read | 2026-10-01 | |\n"
        )
    cite(repo, rows)
    for rel in {r for r, _ in REPOSITORY_PIPED}:
        path = repo / rel
        path.write_text(
            path.read_text(encoding="utf-8")
            .replace("| Field | Value |", "| Field | Value | Note |")
            .replace("moved mid-review> |", "moved mid-review> | read |"),
            encoding="utf-8",
        )
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    first = (repo / RECORD).read_text(encoding="utf-8")
    assert len(record_rows(repo)) == len(REPOSITORY_PIPED), first
    for day in ("2026-09-05", "2026-09-06"):
        code, out = run(repo, "--into", FRAGMENT, "--checked", day)
        assert code == 0, out
        assert (repo / RECORD).read_text(encoding="utf-8") == first, out


def _fixture(repo, shape):
    """Write one signatory ledger and move its code, for the property case."""
    s = unit_hash(repo, "src/orders.py", "serialize")
    e = unit_hash(repo, "src/orders.py", "evict")
    two = f'`{CLAUSE}`, `pact:orders-api/"## Errors"@5e6f7a8b`, '
    rows = {
        "a move": [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{s}")],
        "a BROKEN": [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#evict@{e}")],
        "a move beside a BROKEN": [
            f"| O1 · x | `{CLAUSE}`, `src/orders.py#serialize@{s}`, "
            f"`src/orders.py#evict@{e}` | read | 2026-10-01 | |\n"
        ],
        "two rows": [
            row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{s}"),
            row("O2", f"`{CLAUSE}`, ", f"src/orders.py#evict@{e}"),
        ],
        "two clauses": [row("O1", two, f"src/orders.py#serialize@{s}")],
        "a piped label": [row("O1 \\| a", f"`{CLAUSE}`, ", f"src/orders.py#evict@{e}")],
        "no clause, always": [row("O1", "", f"src/orders.py#serialize@{s}")],
    }[shape]
    if shape == "no clause, always":
        (repo / "seal" / "config.md").write_text(
            config_text(
                ("Mode", "shared"), ("Pact", PACT_URL), ("Pact notify", "always")
            ),
            encoding="utf-8",
        )
    cite(repo, rows)
    src = SOURCE.replace("'id': order.id", "'id': order.id, 'tax': 0")
    (repo / "src" / "orders.py").write_text(
        src.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )


@pytest.mark.parametrize(
    "shape",
    [
        "a move",
        "a BROKEN",
        "a move beside a BROKEN",
        "two rows",
        "two clauses",
        "a piped label",
        "no clause, always",
    ],
)
def test_a_second_identical_run_leaves_the_record_byte_identical(repo, shape):
    """The property `spec.md` item 5 states: running it twice records
    nothing twice. On each fixture the record after the second run is the
    record after the first, byte for byte."""
    _fixture(repo, shape)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0 and "recorded" in out, out
    first = (repo / RECORD).read_bytes()
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert code == 0, out
    assert (repo / RECORD).read_bytes() == first, out


def test_one_change_cited_by_two_rows_of_one_label_is_recorded_once(repo):
    """Two ledger rows of one label citing the same clause and coordinate
    are one change: the first run records it once, not once per row."""
    s = unit_hash(repo, "src/orders.py", "serialize")
    cite(
        repo,
        [
            row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{s}"),
            row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{s}"),
        ],
    )
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert len(record_rows(repo)) == 1, record_rows(repo)
