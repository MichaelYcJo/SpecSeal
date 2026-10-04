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
# What a run prints where an owed pact change could not be recorded: it plans
# its writes, records, and writes the ledger only after recording, so it wrote
# no ledger file (round 1, red 1; round 2, red 10 and yellow 11).
UNDONE = (
    "a pact change is owed and was not recorded, so this run wrote no ledger "
    "file: nothing was re-stamped"
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


def test_under_the_freeze_the_reread_row_is_never_written(repo):
    """Under `Ledger frozen from` the run plans a `Re-read ·` row for the
    `--into` fragment and in-place re-stamps of the fragments. Where the
    change cannot be recorded, neither is written: the fragment is as it
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


def test_a_fragment_the_run_would_create_is_never_created(repo):
    """Under the freeze with `--into` naming a fragment that does not exist
    yet, the run plans it for the `Re-read ·` row; where the change cannot
    be recorded, it is never created."""
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


def test_a_record_step_that_raises_writes_no_ledger(repo, monkeypatch, capsys):
    """The ledger is written after the record, so a record step that raises
    leaves the ledger as it was: nothing had been written yet."""
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


# --- round 2, red 10 and yellow 11: plan, record, then write ---------------

UNREADABLE = pytest.mark.skipif(
    os.name == "nt" or (hasattr(os, "geteuid") and os.geteuid() == 0),
    reason="a mode of 0 stops no read on Windows or as root",
)


@UNREADABLE
def test_a_ledger_that_will_not_read_survives_a_run_that_cannot_record(repo):
    """A sibling fragment that will not read stood in the run's scope; the
    old transaction read it as absent and its put-back removed it (round 2,
    red 10). A run that cannot record writes nothing, so it stays."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    other = cite(
        repo,
        [row("X1", "", "src/orders.py#evict@00000000")],
        where="seal/ledger/1790000000-other.md",
    )
    os.chmod(other, 0)
    try:
        move_serialize(repo)
        code, out = run(repo, "--checked", "2026-09-04")
        assert code == 1 and UNDONE in out, out
        assert os.path.lexists(other), out
        assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    finally:
        if os.path.lexists(other):
            os.chmod(other, 0o644)


@UNREADABLE
def test_an_into_that_will_not_read_is_refused_before_anything_is_written(repo):
    """`reverify_into` wrote its rows over an `--into` it could not read
    (#736's overwrite, round 2's red 10). It is refused at plan time, at
    exit 2, and nothing is written: not the record, not a ledger."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    other_rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    other = cite(repo, other_rows, where="seal/ledger/1790000000-other.md")
    frag = cite(
        repo,
        ["| F9 · kept | `src/orders.py#evict@00000000` | read | 2026-10-01 | |\n"],
    )
    os.chmod(frag, 0)
    try:
        move_serialize(repo)
        code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
        assert code == 2 and "will not read" in out, out
    finally:
        os.chmod(frag, 0o644)
    assert "F9 · kept" in frag.read_text(encoding="utf-8")
    assert other.read_text(encoding="utf-8") == "".join(other_rows), out
    assert not (repo / "seal" / "pact-changes").exists(), out


def test_a_run_killed_after_its_record_is_finished_by_the_next(repo, tmp_path):
    """The kill window. The record is written first and the ledger after, so
    a run killed between the two leaves the record holding the change and
    the ledger unstamped. The next run plans the same move, finds it is the
    record's last word already, records nothing twice, and re-stamps (round
    2, yellow 11). No handler is needed, because nothing is ever put back."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    new = move_serialize(repo)
    wrapper = tmp_path / "killed.py"
    wrapper.write_text(
        "import importlib.util, os, sys\n"
        f"spec = importlib.util.spec_from_file_location('ec', {SCRIPT!r})\n"
        "ec = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(ec)\n"
        "real = ec.record_pact_changes\n"
        "def recorded_then_killed(*a):\n"
        "    real(*a)\n"
        "    sys.stdout.flush()\n"
        "    os._exit(137)\n"
        "ec.record_pact_changes = recorded_then_killed\n"
        f"sys.argv = ['evidence_check.py', '--reverify', '--into', {FRAGMENT!r}, "
        f"'--checked', '2026-09-04', {str(repo)!r}]\n"
        "sys.exit(ec.main())\n",
        encoding="utf-8",
    )
    done = subprocess.run(
        [sys.executable, str(wrapper)],
        cwd=str(repo),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert done.returncode == 137, done.stdout + done.stderr
    assert ledger.read_text(encoding="utf-8") == "".join(rows)
    assert len(record_rows(repo)) == 1
    first = (repo / RECORD).read_bytes()
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert (repo / RECORD).read_bytes() == first, out
    assert f"src/orders.py#serialize@{new}" in ledger.read_text(encoding="utf-8")


def test_a_record_that_cannot_be_written_leaves_the_ledger(repo):
    """An OSError writing the record -- here `seal/pact-changes` is a file,
    so its directory cannot be made -- is a change not recorded: a `LEFT`
    line, exit 1, and no ledger file written."""
    (repo / "seal" / "pact-changes").write_text("not a directory", encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "could not be written" in out and UNDONE in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out


def test_a_change_relanded_after_its_revert_is_recorded(repo):
    """A→B, B→A, A→B: the third is a change the pact's repository has not
    seen since the revert, because the record's last word for the coordinate
    was the revert (round 2, yellow 12)."""
    a = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{a}")])
    b = move_serialize(repo)
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    (repo / "src" / "orders.py").write_text(SOURCE, encoding="utf-8")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-06")
    assert code == 0, out
    rows = record_rows(repo)
    assert len(rows) == 3, rows
    assert rows[-1].endswith(
        f"`src/orders.py#serialize@{a}` → `@{b}` | 2026-09-06 |"
    ), rows


@pytest.mark.parametrize(
    "rows",
    [
        (("Pact", PACT_URL), ("Pact notify", "allways")),
        (("Pact", "orders api"), ("Pact notify", "always")),
    ],
    ids=["a Pact notify that will not read", "a Pact row that will not read, always"],
)
def test_under_always_a_declaration_that_will_not_read_leaves_the_row(repo, rows):
    """A row citing no clause is owed under `always`, and a refused
    declaration cannot say `always` was not meant, so the row is unknown:
    exit 1, a `LEFT` line for a row with no clause, and no ledger file
    written (round 2, yellow 13)."""
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), *rows), encoding="utf-8"
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger_rows = [row("O1", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, ledger_rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "`Pact notify` may be `always`" in out, out
    assert UNDONE in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(ledger_rows), out


def test_a_valid_declaration_that_rules_always_out_still_records_nothing(repo):
    """The other side: a valid `when the pact is touched` rules `always`
    out, so a moved row citing no clause owes nothing and the run re-stamps
    at exit 0."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O1", "", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert f"@{new}" in ledger.read_text(encoding="utf-8"), out


def test_a_refused_declaration_that_still_rules_always_out_leaves_no_row_unknown(
    repo,
):
    """A `Pact` row that will not read beside a `Pact notify` that does and
    is not `always`: a moved row citing no clause is owed nothing under that
    notify, so it is not unknown, and the run re-stamps it at exit 0."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"),
            ("Pact", "orders api"),
            ("Pact notify", "when the pact is touched"),
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O1", "", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert f"@{new}" in ledger.read_text(encoding="utf-8"), out


def _minor_coordinate(repo):
    text = (repo / "src" / "orders.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/orders.py", "serialize", text)
    a, b = ec.minor_region("src/orders.py", text, places[0], '"return"')[0]
    h = ec.content_hash(ec.gfm_lines(text)[a - 1 : b])
    return f'src/orders.py#serialize>"return"@{h}'


def _leave(repo, how):
    if how == "the file is gone":
        (repo / "src" / "orders.py").unlink()
    else:
        (repo / "src" / "orders.py").write_text(
            SOURCE.replace("    return {'id': order.id}", "    pass"),
            encoding="utf-8",
        )


@pytest.mark.parametrize("how", ["the anchored statement is gone", "the file is gone"])
def test_a_coordinate_the_reread_leaves_is_recorded(repo, how):
    """A coordinate the re-read leaves because no one place holds it is
    recorded `BROKEN`, as a major-only one is; it was left at exit 0 with
    nothing recorded (round 2, yellow 14). A second run adds nothing."""
    coord = _minor_coordinate(repo)
    cite(repo, [row("O1", f"`{CLAUSE}`, ", coord)])
    _leave(repo, how)
    _code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `{coord}` BROKEN | 2026-09-04 |"
    ], out
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert len(record_rows(repo)) == 1


@pytest.mark.parametrize("how", ["the anchored statement is gone", "the file is gone"])
def test_under_the_freeze_a_coordinate_with_no_one_place_is_recorded(repo, how):
    """`reverify_into`'s *no one place to hash* is the same exit under the
    freeze: the released row is named and left, and its coordinate is
    recorded `BROKEN` through the same record step."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"), ("Pact", PACT_URL), ("Ledger frozen from", "0")
        ),
        encoding="utf-8",
    )
    coord = _minor_coordinate(repo)
    released = repo / "seal" / "releases" / "0.1.0.md"
    released.parent.mkdir(parents=True)
    released.write_text(
        "## 0.1.0 — 2026-01-01\n\n### 1000000001-x\n\n"
        + row("O1", f"`{CLAUSE}`, ", coord),
        encoding="utf-8",
    )
    cite(repo, [])
    _leave(repo, how)
    _code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    rows = record_rows(repo)
    assert len(rows) == 1 and rows[0].endswith("BROKEN | 2026-09-04 |"), out
    assert "seal/releases/0.1.0.md · O1" in rows[0], rows


# --- the writer's contract, W1-W10 of this work item's `spec.md` -------------


def _killed(repo, tmp_path, patch, *args):
    """Run `--reverify ARGS` in a child whose module PATCH rewires first, so
    a case can stop the run where a kill would; return its exit and output."""
    wrapper = tmp_path / "killed.py"
    wrapper.write_text(
        "import importlib.util, os, sys\n"
        f"spec = importlib.util.spec_from_file_location('ec', {SCRIPT!r})\n"
        "ec = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(ec)\n"
        + patch
        + f"sys.argv = ['evidence_check.py', '--reverify', *{list(args)!r}, "
        f"{str(repo)!r}]\n"
        "sys.exit(ec.main())\n",
        encoding="utf-8",
    )
    done = subprocess.run(
        [sys.executable, str(wrapper)],
        cwd=str(repo),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return done.returncode, done.stdout + done.stderr


def test_a_run_killed_before_its_record_has_written_nothing(repo, tmp_path):
    """W1, step 1. Killed as the record step begins, the run has planned
    every write and made none: no ledger file and no record changed."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = _killed(
        repo,
        tmp_path,
        "def killed(*a):\n    os._exit(137)\nec.record_pact_changes = killed\n",
        "--into",
        FRAGMENT,
        "--checked",
        "2026-09-04",
    )
    assert code == 137, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert not (repo / "seal" / "pact-changes").exists(), out


def test_a_run_killed_between_two_ledger_files_is_finished_by_the_next(repo, tmp_path):
    """W2, inside step 3. The record is written, one ledger file is
    re-stamped and the other is not when the run dies. The next run finds
    both moves the record's last word, appends nothing, and re-stamps the
    file the first run did not reach."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    first = cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    second = cite(
        repo,
        [row("O2", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")],
        where="seal/ledger/1790000000-other.md",
    )
    new = move_serialize(repo)
    code, out = _killed(
        repo,
        tmp_path,
        "real = ec.write_atomic\n"
        "calls = []\n"
        "def write_then_die(path, text):\n"
        "    real(path, text)\n"
        "    calls.append(path)\n"
        "    if len(calls) == 2:\n"
        "        os._exit(137)\n"
        "ec.write_atomic = write_then_die\n",
        "--into",
        FRAGMENT,
        "--checked",
        "2026-09-04",
    )
    assert code == 137, out
    stamped = [f"@{new}" in p.read_text(encoding="utf-8") for p in (first, second)]
    assert sorted(stamped) == [False, True], out
    assert len(record_rows(repo)) == 2, out
    recorded = (repo / RECORD).read_bytes()
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert (repo / RECORD).read_bytes() == recorded, out
    for path in (first, second):
        assert f"@{new}" in path.read_text(encoding="utf-8"), out


def test_with_no_config_nothing_is_owed_and_every_row_is_restamped(repo):
    """W6's other arm. A `seal/config.md` that is not there declares no pact,
    so a moved row owes nothing, citing a clause or not: both are re-stamped,
    nothing is recorded, and the exit is 0."""
    (repo / "seal" / "config.md").unlink()
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(
        repo,
        [
            row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}"),
            row("O2", "", f"src/orders.py#serialize@{old}"),
        ],
    )
    new = move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert ledger.read_text(encoding="utf-8").count(f"@{new}") == 2, out
    assert not (repo / "seal" / "pact-changes").exists(), out


def _frozen_with_a_released_row(repo):
    """The freeze, a released row citing the clause, and an empty fragment:
    a run under `--into` plans one `Re-read ·` row and owes one change."""
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
    cite(repo, [row("F1", "", f"src/orders.py#serialize@{old}")])
    move_serialize(repo)


def test_a_run_that_writes_no_ledger_claims_no_write(repo):
    """W8. A run that cannot record writes no ledger file, so it prints no
    line saying it wrote one: no `wrote`, no `citing rows written`, no
    `re-verified`, and no per-row hash line. Its `LEFT` lines and the
    closing line are the whole account."""
    _frozen_with_a_released_row(repo)
    record = repo / RECORD
    record.parent.mkdir(parents=True)
    record.write_text("", encoding="utf-8")
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and UNDONE in out, out
    assert "  LEFT  " in out, out
    for claim in ("  wrote ", "citing row", "re-verified", " -> ", "dated "):
        assert claim not in out, (claim, out)


def test_a_line_that_says_a_write_happened_follows_the_record(repo):
    """W8, the other side. A run that writes prints each write line after
    the record step, because the write it names is made after the record."""
    _frozen_with_a_released_row(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    recorded = out.index("  recorded ")
    for claim in ("  wrote ", "1 citing row written", "1 row re-verified", " -> "):
        assert out.index(claim) > recorded, (claim, out)


def test_a_ledger_that_will_not_decode_is_left_byte_for_byte(repo):
    """W9. A lenient read put U+FFFD where a byte would not decode and the
    re-stamp wrote it back, destroying a byte the run never meant to touch.
    A file the run would write is read strictly: the fragment is named
    `ledger unreadable`, left byte for byte, and the exit is 1."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [])
    other = repo / "seal" / "ledger" / "1790000000-other.md"
    raw = (
        row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")
        .replace("| |\n", "| caf\xe9 |\n")
        .encode("latin-1")
    )
    other.write_bytes(raw)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert other.read_bytes() == raw, out
    assert "  LEFT  seal/ledger/1790000000-other.md  ledger unreadable" in out, out


def test_a_record_that_will_not_decode_is_left_byte_for_byte(repo):
    """W9, the record. Rewriting a record read leniently changes its content
    hash, so a pact review that took it reads `NOT TAKEN` again for nothing.
    One that will not decode is left byte for byte, the run is a change not
    recorded, and no ledger file is written."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0 and len(record_rows(repo)) == 1, out
    record = repo / RECORD
    raw = record.read_bytes().replace(b"(#647)", b"(#647 \xff)")
    assert raw != record.read_bytes()
    record.write_bytes(raw)
    stamped = ledger.read_text(encoding="utf-8")
    (repo / "src" / "orders.py").write_text(SOURCE, encoding="utf-8")
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert code == 1 and UNDONE in out, out
    assert record.read_bytes() == raw, out
    assert ledger.read_text(encoding="utf-8") == stamped, out
    assert (
        f"  LEFT  seal/pact-changes/{ITEM}.md  the record could not be read — "
        "no pact change was recorded and nothing was re-stamped"
    ) in out, out


@UNREADABLE
def test_a_ledger_step_three_cannot_write_is_named_and_the_rest_written(repo):
    """W10. The record is written, then one ledger file cannot be replaced:
    its directory refuses. That file is named on a `LEFT` line with the
    cause, the other ledger is written, nothing is a traceback, and the exit
    is 1. The record already holds both moves, so once the directory takes
    writes again the next run re-stamps the file and records nothing."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    (repo / "docs").mkdir()
    shared = repo / "docs" / "ledger.md"
    shared.write_text(
        row("S1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}"), encoding="utf-8"
    )
    fragment = cite(
        repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    )
    new = move_serialize(repo)
    both = ("--ledger", "docs/ledger.md", "--ledger", FRAGMENT)
    folder = repo / "seal" / "ledger"
    os.chmod(folder, 0o555)
    try:
        code, out = run(repo, *both, "--into", FRAGMENT, "--checked", "2026-09-04")
    finally:
        os.chmod(folder, 0o755)
    assert code == 1 and "Traceback" not in out, out
    assert f"@{new}" in shared.read_text(encoding="utf-8"), out
    assert f"@{old}" in fragment.read_text(encoding="utf-8"), out
    assert (
        f"  LEFT  seal/ledger/{ITEM}.md  could not be written (Permission denied) "
        "— it is as it was, and the next run plans its writes again"
    ) in out, out
    assert out.count(" -> ") == 1 and "1 row re-verified" in out, out
    assert len(record_rows(repo)) == 2, out
    recorded = (repo / RECORD).read_bytes()
    code, out = run(repo, *both, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert (repo / RECORD).read_bytes() == recorded, out
    assert f"@{new}" in fragment.read_text(encoding="utf-8"), out


@pytest.mark.parametrize(
    "doc, sentence",
    [
        (
            "docs/the-pact.md",
            "**A line saying the run wrote a ledger file prints only once that "
            "file is written, so a run that writes none claims none.**",
        ),
        (
            "docs/the-pact.md",
            "**The record-first order holds against the process dying, and not "
            "against the machine losing power.**",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "**A line saying a ledger was written prints after it was.**",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "The order holds against the process dying, not against a power "
            "loss: nothing is `fsync`ed",
        ),
    ],
    ids=[
        "the pact: W8-W10",
        "the pact: the power-loss limit",
        "skill: W8-W10",
        "skill: the limit",
    ],
)
def test_the_documents_say_what_the_writer_does(doc, sentence):
    """W8-W10 and the stated limit are things a person reads before running
    `--reverify`, so each sentence is pinned where it stands (§14)."""
    with open(os.path.join(ROOT, doc), encoding="utf-8") as handle:
        text = " ".join(handle.read().split())
    assert sentence in text, (doc, sentence)


@UNREADABLE
def test_an_into_step_three_cannot_write_claims_no_row_written(repo):
    """W8 and W10 under the freeze. The record is written, then `--into`
    cannot be replaced: no `wrote` line names a row in it, the count says
    none was written, and the file is named on a `LEFT` line."""
    _frozen_with_a_released_row(repo)
    folder = repo / "seal" / "ledger"
    before = (repo / FRAGMENT).read_bytes()
    os.chmod(folder, 0o555)
    try:
        code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    finally:
        os.chmod(folder, 0o755)
    assert code == 1 and "Traceback" not in out, out
    assert (repo / FRAGMENT).read_bytes() == before, out
    assert len(record_rows(repo)) == 1, out
    assert "  wrote " not in out and "0 citing rows written" in out, out
    assert f"  LEFT  seal/ledger/{ITEM}.md  could not be written" in out, out
