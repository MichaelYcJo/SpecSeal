"""A ledger row with more cells than its table's header is named `OVERFLOW`.

An unescaped `|` inside a cell splits the row, and the text after it lands in
the next column: a claim runs into its grounds, a date into its notes, and
whatever falls past the last column is in no column at all. Until #585 only
this repository's own test refused such a row, so a repository that installs
the plugin could hold one, and any marker written in the overflow cell, with
no reader seeing it.

The arm is `evidence_check.py#overflow_rows`, and it reads through the same
walk the `MALFORMED` arm reads, `ledger_table_rows`. A row under no header --
every fragment row, by rule -- is counted against `LEDGER_COLUMNS`, the five
columns `templates/ledger.md` declares. The grading is `MALFORMED`'s: exit 1
on a lenient run, exit 2 under `--strict`.

Only MORE cells are named. A short row hides nothing: GitHub renders every
cell of it, and the rule, the issue and the owner's answer all say *more*.

No fixture here runs git: the checker calls git for nothing outside
`--migrate`.
"""

import ntpath
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")
BROAD_GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")
TEMPLATE = os.path.join(ROOT, "templates", "ledger.md")


def load(path, name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ec = load(SCRIPT, "ec_overflow")

SERVICE = "def handler(x):\n    return x + 1\n"
HEADER = "| Clause | Code grounds | Verified behavior | Checked | Notes |\n|---|---|---|---|---|\n"
# The #562 shape: a shell pipe quoted in a Verified-behavior cell. Six cells.
SPLIT = "| a | `{c}` | ran `cat f | grep -c x` | 2026-01-01 | n |\n"
# The same text escaped. Five cells.
ESCAPED = "| b | `{c}` | ran `cat f \\| grep -c x` | 2026-01-01 | n |\n"


def good():
    """`src/service.py#handler` at the content `SERVICE` holds."""
    places = ec.resolve("src/service.py", "handler", SERVICE)
    a, b = places[0]
    return f"src/service.py#handler@{ec.content_hash(SERVICE.splitlines()[a - 1 : b])}"


def run(args, cwd, script=SCRIPT):
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


@pytest.fixture
def repo(tmp_path):
    d = tmp_path / "proj"
    (d / "src").mkdir(parents=True)
    (d / "seal" / "ledger").mkdir(parents=True)
    (d / "src" / "service.py").write_text(SERVICE, encoding="utf-8")
    return d


def fragment(repo, body):
    path = repo / "seal" / "ledger" / "f.md"
    path.write_text(body, encoding="utf-8")
    return path


def named(text):
    """`[(line, detail)]` for every row the arm names in TEXT."""
    out = []
    for status, coord, detail in ec.overflow_rows(text):
        assert status == "OVERFLOW", status
        m = re.fullmatch(r"line (\d+)", coord)
        assert m, f"the coordinate names no line: {coord!r}"
        out.append((int(m.group(1)), detail))
    return out


def lines(text):
    return [n for n, _ in named(text)]


# --- A1 · a split row is named, with the grading MALFORMED has --------------


def test_a_split_row_is_named_with_its_line_its_counts_and_the_remedy(repo):
    """A1. Seen red against the checker at `11e3104c`: exit 0, no finding."""
    c = good()
    fragment(repo, "# frag\n\n" + HEADER + SPLIT.format(c=c) + ESCAPED.format(c=c))
    r = run(["."], repo)
    assert r.returncode == 1, r.stdout + r.stderr
    row = [ln for ln in r.stdout.splitlines() if ln.lstrip().startswith("OVERFLOW")]
    assert row == [
        "  OVERFLOW line 5  6 cells under a 5-cell header — a `|` inside a "
        "cell splits the row; write it as `\\|`"
    ], r.stdout
    assert "· 1 overflow" in r.stdout, r.stdout
    assert "OVERFLOW" in r.stdout.rstrip().splitlines()[-1], "the notice"
    r = run(["--strict", "."], repo)
    assert r.returncode == 2, r.stdout + r.stderr
    assert "OVERFLOW line 5" in r.stdout, r.stdout


# --- A2 · a row under no header is counted against the ledger row ----------


def test_a_header_less_row_is_counted_against_the_ledger_rows_columns():
    """A2, the #501 shape. A fragment has no header by rule, and the fold
    copies it into its release file as it stands."""
    body = SPLIT.format(c="x.py#f@00000000") + ESCAPED.format(c="x.py#f@00000000")
    assert lines(body) == [1]
    ((_, detail),) = named(body)
    assert detail == (
        "6 cells and no header above it, so counted against the 5 columns of "
        "a ledger row — a `|` inside a cell splits the row; write it as `\\|`, "
        "or give a table that is not ledger rows a header of its own"
    ), detail


def test_a_table_with_its_own_header_keeps_its_own_width():
    """A2. A two-column table keeps two, and the fragment row after the blank
    line under it is counted against the ledger row again."""
    beside = "| Item | Value |\n|---|---|\n| a | b |\n\n" + SPLIT.format(
        c="x.py#f@00000000"
    )
    assert lines(beside) == [5]
    assert lines("| Item | Value |\n|---|---|\n| a | b | c |\n") == [3]
    assert (
        "under a 2-cell header" in named("| A | B |\n|---|---|\n| a | b | c |\n")[0][1]
    )


def test_a_header_less_row_is_named_in_the_run(repo):
    """A2 through the command, not only the function."""
    fragment(repo, SPLIT.format(c=good()))
    r = run(["."], repo)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "OVERFLOW line 1  6 cells and no header above it" in r.stdout, r.stdout


# --- A3 · the reading is the shared one -------------------------------------

WIDE = "| a | b | c | d | e | f |\n"


@pytest.mark.parametrize(
    "shape, body",
    [
        ("closed backtick fence", "```\n" + WIDE + "```\n"),
        ("closed tilde fence", "~~~\n" + WIDE + "~~~\n"),
        ("indented closed fence", "   ```\n" + WIDE + "   ```\n"),
        ("longer closer", "```\n" + WIDE + "`````\n"),
    ],
)
def test_a_row_in_a_closed_fence_is_an_example(shape, body):
    """A3. Only a block that closes is a quotation (#444)."""
    assert lines(body) == [], shape


@pytest.mark.parametrize(
    "shape, body, line",
    [
        ("unclosed fence", "```\n" + WIDE, 2),
        ("html comment", "<!--\n" + WIDE + "-->\n", 2),
        ("indented row", "  " + WIDE, 1),
        ("fence of another char", "```\n" + WIDE + "~~~\n", 2),
    ],
)
def test_a_row_the_shared_reader_calls_live_is_read(shape, body, line):
    """A3. An unclosed fence runs to the end of the file, and reading nothing
    from there on is the silent direction; a commented-out row is a claim
    somebody parked."""
    assert lines(body) == [line], shape


@pytest.mark.parametrize(
    "row",
    [
        "| a | b \\| c | d | e | f |\n",
        "| a | b | c | d | e \\|\n",
        "| a | `b \\| c` | d | e | f |\n",
        "| a | b | c | d | e\n",
    ],
)
def test_an_escaped_pipe_and_a_missing_closer_count_exactly(row):
    """A3. `\\|` is inside the cell, and a row ending in `\\|` with no closing
    pipe is not one cell short, which is how this repository's own case
    counted it before #585."""
    assert lines(row) == [], row
    assert lines(row.replace("| a |", "| a | z |", 1)) == [1], row


# --- A4 · a short row is not refused ----------------------------------------


def test_a_row_with_fewer_cells_than_its_header_is_not_named():
    """A4. Nothing is hidden in a short row."""
    assert lines(HEADER + "| a | b |\n") == []
    assert lines("| a | b |\n") == []


# --- A5 · a vendored copy refuses the same row -----------------------------


def test_a_vendored_copy_names_the_same_row(repo, tmp_path):
    """A5. The copy `evidence-ci` puts alone in `tools/` has no shared reader
    and no template beside it, which is why the width is a constant."""
    tools = tmp_path / "elsewhere" / "tools"
    tools.mkdir(parents=True)
    copy = tools / "evidence_check.py"
    copy.write_bytes(open(SCRIPT, "rb").read())
    c = good()
    fragment(repo, "# frag\n\n" + HEADER + SPLIT.format(c=c) + "\n" + SPLIT.format(c=c))
    plugin = run(["--strict", "."], repo)
    vendored = run(["--strict", "."], repo, script=copy)
    assert vendored.returncode == 2, vendored.stdout + vendored.stderr
    rows = [ln for ln in vendored.stdout.splitlines() if "OVERFLOW line" in ln]
    assert len(rows) == 2, vendored.stdout
    assert rows == [ln for ln in plugin.stdout.splitlines() if "OVERFLOW line" in ln]


# --- A6 · the columns are the template's -----------------------------------


def test_the_ledger_rows_columns_are_the_templates():
    """A6. Held here and not read at run time, because the vendored copy has
    no template beside it. A column added to the template goes red here, and
    the constant moves in the same change."""
    with open(TEMPLATE, encoding="utf-8") as f:
        headers = [ec.cell_rule()(ln) for ln in f if ln.startswith("| Clause |")]
    assert len(headers) == 1, headers
    assert tuple(headers[0]) == ec.LEDGER_COLUMNS, (headers[0], ec.LEDGER_COLUMNS)
    assert ec.LEDGER_COLUMNS.index(ec.CODE_GROUNDS) == 1


# --- the walk the two arms share -------------------------------------------


def test_the_walk_yields_body_rows_with_their_header():
    """`ledger_table_rows` is the one table walk, and the interface work item
    C (#387) builds on: `(line, header cells or None, cells)`, rule and header
    rows never yielded, line numbers into the text as given."""
    text = "intro\n\n| A | B |\n|---|---|\n| a | b |\n\n| x | y |\n"
    assert list(ec.ledger_table_rows(text)) == [
        (5, ["A", "B"], ["a", "b"]),
        (7, None, ["x", "y"]),
    ]


# --- A8 · the totals say it at zero ----------------------------------------


def test_a_clean_ledger_says_zero_overflow_on_both_lines(repo):
    """A8. Last on the line, so the text every reader matches today is
    unchanged, and `broad_gate.py#LEDGER_RE` still reads the total."""
    fragment(repo, "# frag\n\n" + HEADER + ESCAPED.format(c=good()))
    r = run(["."], repo)
    assert r.returncode == 0, r.stdout + r.stderr
    tail = "0 old-format · 0 malformed · 0 overflow"
    per_ledger = [ln for ln in r.stdout.splitlines() if ln.startswith("  1 ok")]
    total = [ln for ln in r.stdout.splitlines() if ln.startswith("total:")]
    assert per_ledger and per_ledger[0].endswith(tail), r.stdout
    assert total and total[0].endswith(tail), r.stdout
    gate = load(BROAD_GATE, "bg_overflow")
    assert gate.LEDGER_RE.search(total[0]), total[0]


# --- a line ends where GFM ends one (round 1, 🟡 1) --------------------------
#
# GFM ends a line at LF, CR and CRLF only. `str.splitlines` also ends one at
# U+2028, NEL, a form feed and five others, so every walk in the checker that
# reads markdown lines for a table or a fence cut a line GFM keeps whole.
# One case per walk.

NOT_A_LINE_END = ["\u2028", "\x85", "\x0c"]


@pytest.mark.parametrize("ch", NOT_A_LINE_END)
def test_a_character_gfm_does_not_end_a_line_at_does_not_cut_a_row(ch):
    """`ledger_table_rows`. Cut there, a split after the cut went unnamed and
    every later row was one line off and read as under no header."""
    c = "x.py#f@00000000"
    hidden = f"| a | `{c}` | ran `a | b` more{ch}text | 2026-01-01 | n |\n"
    assert lines(HEADER + hidden) == [3]
    before = f"| a | `{c}` | b{ch}c | 2026-01-01 | n |\n"
    text = HEADER + before + SPLIT.format(c=c)
    assert lines(text) == [4]
    assert "under a 5-cell header" in named(text)[0][1]


@pytest.mark.parametrize("ch", NOT_A_LINE_END)
def test_a_character_gfm_does_not_end_a_line_at_does_not_open_a_fence(ch):
    """`unquoted`. A fence run after such a character is not at the start of
    a line to GFM, so the row after it is live."""
    assert lines(f"intro{ch}```\n{WIDE}```\n") == [2]


@pytest.mark.parametrize("ch", NOT_A_LINE_END)
def test_an_old_coordinate_after_such_a_character_is_still_offered(ch):
    """`old_format_rows`. The rest of the row after the cut did not start with
    a pipe, so an old coordinate there was not offered for migration."""
    found = ec.old_format_rows(f"| a | x{ch}`src/a.py:1-2` |\n")
    assert [coord for _, coord, _ in found] == ["src/a.py:1-2"], found


@pytest.mark.parametrize("ch", NOT_A_LINE_END)
def test_migrate_reads_the_fence_where_gfm_reads_it(repo, ch):
    """`migrate`. It read fences on its own cut, so a row GFM shows live was
    left as a fenced example and never migrated."""
    path = fragment(repo, f"intro{ch}```\n| POL | old `src/service.py:1-2` |\n```\n")
    run(["--migrate", "."], repo)
    assert "`src/service.py#handler@" in path.read_text(encoding="utf-8")


@pytest.mark.parametrize("ch", NOT_A_LINE_END)
def test_a_record_line_after_such_a_fence_run_is_read(tmp_path, ch):
    """`check_records`. A record is read a line at a time with fences
    skipped, so a false fence there hid a name the tree does not have."""
    h = tmp_path / "seal"
    d = h / "specs" / "1780000000-live"
    d.mkdir(parents=True)
    (h / "ledger").mkdir()
    (h / "ledger" / "1780000000-live.md").write_text("", encoding="utf-8")
    (d / "overview.md").write_text(
        f"# r\n\nintro{ch}```\nthe alias `gone_helper` has one call site\n```\n",
        encoding="utf-8",
    )
    findings, _read, _stamps = ec.check_records(str(tmp_path), str(h))
    assert [(s, c.rsplit("/", 1)[-1]) for s, c, _ in findings] == [
        ("NOT-IN-TREE", "overview.md:4")
    ], findings


# --- A9 · `--reverify` does not go quiet -----------------------------------


def test_reverify_names_an_overflowing_row_and_leaves_it(repo):
    """A9. Every row the check names gets a line back from `--reverify`.
    Seen red against `11e3104c`: `0 rows re-verified`, exit 0, no line."""
    path = fragment(repo, "# frag\n\n" + HEADER + SPLIT.format(c=good()))
    before = path.read_text(encoding="utf-8")
    r = run(["--reverify", "."], repo)
    assert r.returncode == 1, r.stdout + r.stderr
    assert (
        "  LEFT  seal/ledger/f.md line 5  OVERFLOW — 6 cells under a 5-cell "
        "header" in r.stdout.replace(os.sep, "/")
    ), r.stdout
    assert path.read_text(encoding="utf-8") == before


def test_reverify_names_an_overflowing_row_with_forward_slashes(
    repo, monkeypatch, capsys
):
    """The `LEFT` line's `<ledger> line <n>` is a coordinate the run built,
    so it takes `built_name`'s `/`, as `reverify`'s dated and named rows do.
    Windows' `glob` spells the ledger `seal\\ledger\\f.md`; the case above
    folds `os.sep` before it compares, so it could not see that. Simulated
    from a POSIX machine: the display spelling is Windows', and
    `built_name` reads `ntpath` (`agent-contract` §13)."""
    path = fragment(repo, "# frag\n\n" + HEADER + SPLIT.format(c=good()))
    shown = ec.display_name
    monkeypatch.setattr(
        ec,
        "display_name",
        lambda p, root, flavour=os.path: shown(p, root).replace("/", "\\"),
    )
    monkeypatch.setattr(ec.built_name, "__defaults__", (ntpath,))
    assert ec.reverify([str(path)], str(repo), {}, None) == 1
    out = capsys.readouterr().out
    assert "  LEFT  seal/ledger/f.md line 5  OVERFLOW — " in out, out


# --- A13 · a new ledger is clean -------------------------------------------


def test_the_template_copied_as_a_ledger_is_clean(repo):
    """A13. A repository's first ledger is this file, and it must not open
    with a finding."""
    with open(TEMPLATE, encoding="utf-8") as f:
        (repo / "seal" / "ledger.md").write_text(f.read(), encoding="utf-8")
    assert ec.overflow_rows((repo / "seal" / "ledger.md").read_text("utf-8")) == []
    r = run(["--ledger", "seal/ledger.md", "."], repo)
    assert "OVERFLOW" not in r.stdout, r.stdout
    assert "0 overflow" in r.stdout, r.stdout
