"""Every reader of markdown or record text ends a line where GFM does (#664).

`str.splitlines` ends a line at LF, CR and CRLF, and also at U+2028, U+2029,
NEL, a form feed, VT and `\\x1c`-`\\x1e`. GFM, `ast` and git end one at the
first three alone. So below one of those eight a reader that split with
`splitlines` read lines no renderer shows: a table row cut in two, a marker or
a heading that stands mid-line read as a line of its own, a line number one
off the one `grep -n` prints, and, where the reader wrote the text back, the
character turned into a line break.

One splitter, `skills/verify/scripts/unverified_check.py#gfm_lines`, is what
every such reader now reads, and two readers of one text split it alike. The
scenarios are `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/
spec.md`'s, numbered as it numbers them, and each was seen red at `2e392d46`
before it was committed.

Every one of the eight is built from its code point, never typed: an escape
typed into an editing tool can come back as the character itself, and a file
holding one is exactly what these cases are about.
"""

import importlib.util
import os
import shutil
import sys

import pytest
from test_the_record_is_generated import (
    commit,
    declared,
    generate,
    generator_module,
    git,
    report,
    write,
)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
READER = os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py")
CHECKER = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")
ARM_CHECK = os.path.join(ROOT, "skills", "verify", "scripts", "arm_check.py")
FOLD_CHECK = os.path.join(ROOT, "skills", "settle", "scripts", "fold_check.py")

# Every character `str.splitlines` ends a line at and GFM does not.
SPLITLINES_ONLY = [chr(c) for c in (0x0B, 0x0C, 0x1C, 0x1D, 0x1E, 0x85, 0x2028, 0x2029)]
LS = chr(0x2028)
FF = chr(0x0C)
BY_CODE_POINT = {"ids": lambda c: f"U+{ord(c):04X}"}


def _load(name, path):
    """A script by path, registered under NAME first: `arm_check.py` defines
    dataclasses, which look their own module up in `sys.modules`."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


reader = _load("specseal_reader_for_gfm_lines", READER)


# --- S17: one splitter, and its copies agree ---------------------------------


def texts():
    """Every shape the copies could part on: each line end GFM has, each of
    the eight mid-line and at a line end, no trailing newline, and nothing."""
    out = ["", "a", "a\n", "a\n\n", "\n", "a\nb", "a\r\nb\r\n", "a\rb\r", "a\r\n\r\n"]
    for char in SPLITLINES_ONLY:
        out += [f"a{char}b\n", f"a{char}\nb", f"{char}", f"a\n{char}\n\nc{char}"]
    return out


def test_the_readers_splitter_ends_a_line_at_lf_cr_and_crlf_alone():
    for char in SPLITLINES_ONLY:
        assert reader.gfm_lines(f"a{char}b\nc") == [f"a{char}b", "c"], repr(char)
    assert reader.gfm_lines("a\r\nb\rc\nd") == ["a", "b", "c", "d"]
    assert reader.gfm_lines("a\r\nb\n", keepends=True) == ["a\r\n", "b\n"]


def test_the_splitter_is_splitlines_on_a_text_without_the_eight():
    for text in [t for t in texts() if not any(c in t for c in SPLITLINES_ONLY)]:
        assert reader.gfm_lines(text) == text.splitlines(), repr(text)
        assert reader.gfm_lines(text, True) == text.splitlines(True), repr(text)


def test_every_copy_of_the_splitter_is_the_readers():
    """S17. The checker keeps its own copy because `evidence-ci` runs it alone
    in a user's `tools/`, and `arm_check._lines` splits Python source where
    `ast` does, ends kept. All three are one rule, held equal here."""
    checker = _load("specseal_checker_for_gfm_lines", CHECKER)
    arm_check = _load("specseal_arm_check_for_gfm_lines", ARM_CHECK)
    for text in texts():
        want = reader.gfm_lines(text)
        assert checker.gfm_lines(text) == want, repr(text)
        kept = reader.gfm_lines(text, keepends=True)
        assert checker.gfm_lines(text, keepends=True) == kept, repr(text)
        assert arm_check._lines(text) == kept, repr(text)
    assert reader.GFM_LINE_RE.pattern == checker.GFM_LINE_RE.pattern


def test_fold_check_keeps_no_copy_of_its_own():
    """The copy `fold_check.py` held while the reader was being rewritten on
    another branch is gone, and the ceiling counts with the reader's."""
    fold_check = _load("specseal_fold_check_for_gfm_lines", FOLD_CHECK)
    assert not hasattr(fold_check, "gfm_lines")
    assert not hasattr(fold_check, "GFM_LINE_RE")


# --- S1, S2: the record generator reads and writes the character back ----------


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("gfm-lines-record-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def test_a_reports_quoted_character_survives_into_its_record(repo):
    """S1, the instance #664 names: `rounds/round-1.md` of work item
    `1790635414` holds a line break where its report held U+2028, inside a
    quoted test. `new` copies the report's lines out of `raw`, and `raw` was
    split with `splitlines` and joined back with LF."""
    declared(repo)
    quoted = f"```python\nassert 'alpha{LS}beta' in text\n```\n"
    code, out, text = generate(repo, report_text=report(fixes=quoted))
    assert code == 0, out
    assert f"alpha{LS}beta" in text
    assert "alpha\nbeta" not in text


def test_a_fix_row_with_a_line_separator_in_a_cell_is_one_row(tmp_path):
    """S2. A row cut at the separator read its grounds as the half before it,
    and the half after was no row at all."""
    generator = generator_module()
    fixes = tmp_path / "fixes.md"
    fixes.write_text(
        f"{generator.FIXES}\n\n{generator.row(generator.FIXES_HEADER)}\n"
        f"{generator.separator(len(generator.FIXES_HEADER))}\n"
        f"| 1 | answered | the grounds, alpha{LS}beta |\n",
        encoding="utf-8",
    )
    got = generator.fix_table(generator.load(READER, "specseal_reader_s2"), fixes)
    assert got == {1: ("answered", f"the grounds, alpha{LS}beta", "")}


# --- S3, S4: a marker GFM does not show as its own line excuses nothing -----


MARKED = f"# A policy\n\nprose{LS}<!-- specs/1700000000-a -->\n\n**A rule.**\n"


def test_a_marker_after_a_separator_is_not_a_fold(tmp_path):
    """S3. The marker is line-anchored, and GFM renders it mid-line, so no
    fold wrote it there. Read as a fold, it excused the removal of a
    directory nothing absorbed."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "x.md").write_text(MARKED, encoding="utf-8")
    assert reader.folded_items(str(tmp_path)) == set()


def test_the_ceiling_and_the_fold_agree_about_that_marker():
    """S4. `fold-check` counts what the fold reads, so it counts no marker
    there either: the frozen count, the digest and the statements."""
    fold_check = _load("specseal_fold_check_s4", FOLD_CHECK)
    assert fold_check.markers(MARKED) == 0
    assert fold_check.marker_digest(MARKED) == fold_check.marker_digest("")
    assert fold_check.numbered_statements(MARKED) == []


@pytest.mark.parametrize("char", SPLITLINES_ONLY, **BY_CODE_POINT)
def test_no_one_of_the_eight_makes_a_marker_a_line(tmp_path, char):
    text = MARKED.replace(LS, char)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "x.md").write_text(text, encoding="utf-8")
    assert reader.folded_items(str(tmp_path)) == set(), repr(char)


# --- S5-S8: the changelog readers and their partner ---------------------------


GATHER = os.path.join(ROOT, ".github", "scripts", "gather_changelog.py")
SURVIVOR = os.path.join(ROOT, "skills", "code-review", "scripts", "survivor_check.py")


def test_gathering_below_a_separator_lands_in_the_section_and_keeps_it():
    """S5. `insert` found the section by counting LF and then indexed a list
    `splitlines` had made, so a U+2028 above the section put the new entries
    above its heading, and the file was written back with a line break where
    the character stood."""
    gather = _load("specseal_gather_s5", GATHER)
    text = (
        "# Changelog\n\n"
        f"Intro alpha{LS}beta.\n\n"
        "## 1.1.0 — 2026-01-02\n\n"
        "<!-- specs/1-a -->\nentry a\n\n"
        "## 1.0.0 — 2026-01-01\n\nold\n"
    )
    block = gather.section("1.1.0", "2026-01-03", [("2-b", f"entry{FF}b")])
    assert gather.insert(text, block, "1.1.0") == (
        "# Changelog\n\n"
        f"Intro alpha{LS}beta.\n\n"
        "## 1.1.0 — 2026-01-02\n\n"
        "<!-- specs/1-a -->\nentry a\n\n"
        f"<!-- specs/2-b -->\nentry{FF}b\n\n"
        "## 1.0.0 — 2026-01-01\n\nold\n"
    )
    fresh = gather.section("1.2.0", "2026-01-03", [("2-b", f"entry{FF}b")])
    assert gather.insert(text, fresh, "1.2.0") == (
        "# Changelog\n\n"
        f"Intro alpha{LS}beta.\n\n"
        f"## 1.2.0 — 2026-01-03\n\n<!-- specs/2-b -->\nentry{FF}b\n\n"
        "## 1.1.0 — 2026-01-02\n\n"
        "<!-- specs/1-a -->\nentry a\n\n"
        "## 1.0.0 — 2026-01-01\n\nold\n"
    )


def test_the_sections_index_is_counted_on_the_list_it_indexes():
    """`insert` indexes `gfm_lines(text)`, and the heading's index is counted
    with the same split. A text read through `open()` never holds a lone CR,
    so counting LF agrees on every file `main` reads; handed one directly,
    the two counts part and the entries land above the heading."""
    gather = _load("specseal_gather_index", GATHER)
    text = "# Changelog\n\nIntro\rmore.\n\n## 1.1.0 — 2026-01-02\n\nentry a\n"
    block = gather.section("1.1.0", "2026-01-03", [("2-b", "entry b")])
    assert gather.insert(text, block, "1.1.0") == (
        "# Changelog\n\nIntro\nmore.\n\n## 1.1.0 — 2026-01-02\n\n"
        "entry a\n\n<!-- specs/2-b -->\nentry b\n"
    )


def fragment_tree(tmp_path, body):
    """A repository root holding one changelog fragment and a changelog."""
    item = tmp_path / "seal" / "specs" / "2-b"
    item.mkdir(parents=True)
    (item / "changelog.md").write_text(body, encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 1.0.0 — 2026-01-01\n\nold\n", encoding="utf-8"
    )
    return tmp_path


def test_the_dry_run_prints_a_fragments_character_as_it_stands(tmp_path, capsys):
    gather = _load("specseal_gather_dry_run", GATHER)
    root = fragment_tree(tmp_path, f"entry{LS}b\n")
    argv = ["--version", "1.1.0", "--date", "2026-01-02", "--dry-run"]
    assert gather.main([*argv, "--root", str(root)]) == 0
    assert f"entry{LS}b" in capsys.readouterr().out


def test_a_fence_after_a_separator_opens_nothing_in_a_fragment():
    """`leaves_open` asks `live_lines` whether a marker written below the
    body would be live. A fence run after a U+2028 is mid-line to GFM, so it
    opens nothing, and the fragment is not refused for one."""
    gather = _load("specseal_gather_leaves_open", GATHER)
    assert gather.leaves_open(f"an entry{LS}```\n") is False


def test_a_section_line_is_a_line_that_starts_one(tmp_path):
    """`section_lines` names every fragment line starting `## `, by the
    number `grep -n` prints. One after a form feed mid-line starts none."""
    gather = _load("specseal_gather_section_lines", GATHER)
    root = fragment_tree(tmp_path, f"entry{FF}## not a heading\n\n## one\n")
    assert gather.section_lines(str(root), "2-b") == [(3, "## one")]


def test_the_gatherer_and_the_sweep_read_one_marker_alike(monkeypatch):
    """S6. A marker after a U+2028 on its line is not a line of its own to
    GFM, so neither reader of `CHANGELOG.md` may call the fragment gathered.
    The sweep's side is the one that excuses a fragment, and it was red."""
    gather = _load("specseal_gather_s6", GATHER)
    survivor = _load("specseal_survivor_s6", SURVIVOR)
    text = f"# Changelog\n\n## 1.0.0 — 2026-01-01\n\nold{LS}<!-- specs/1-a -->\n"
    monkeypatch.setattr(
        survivor, "read_blobs", lambda root, rev, paths: {survivor.CHANGELOG: text}
    )
    assert survivor.gathered_fragments("unused", "HEAD") == set()
    assert gather.live_markers(text) == []


def test_the_sweep_loads_its_reader_once_per_path(tmp_path):
    """`segments` asks the reader for its splitter once per file of the
    corpus, so the reader is loaded once -- and once per path, so a reader
    that is not where `READER` now points is still refused."""
    survivor = _load("specseal_survivor_cache", SURVIVOR)
    assert survivor.reader() is survivor.reader()
    survivor.READER = str(tmp_path / "gone" / "unverified_check.py")
    with pytest.raises(survivor.Refused, match="which says what a retirement is"):
        survivor.reader()


def test_a_sentences_line_number_is_the_files():
    """S7. The number is the one `grep -n` prints, and the one
    `python_prose` and `released_lines` keep."""
    survivor = _load("specseal_survivor_s7", SURVIVOR)
    text = f"# A title\n\nalpha{FF}beta.\n\nThe sentence stands here.\n"
    found = [n for n, raw in survivor.segments(text) if "sentence" in raw]
    assert found == [5]


def test_a_ledger_row_holding_a_separator_is_one_row_at_both_ends(monkeypatch):
    """S8. A row with no id, whose second anchor sits after a U+2028 in its
    notes, corrected in place to drop the anchor that left the code. Cut at
    the separator, the row lost the anchor that still resolves, so nothing at
    `b` could be seen citing it, and the correction was reported as a
    removal."""
    survivor = _load("specseal_survivor_s8", SURVIVOR)
    module = {
        "a": "def helper(w):\n    return w\n\n\ndef other(w):\n    return w\n",
        "b": "def other(w):\n    return w\n",
    }
    monkeypatch.setattr(
        survivor,
        "read_blobs",
        lambda root, rev, paths: {p: module[rev] for p in paths if p == "pkg/mod.py"},
    )
    head = "| Clause | Code grounds | Verified behavior | Checked | Notes |\n"
    head += "|---|---|---|---|---|\n"
    before = head + (
        "| a claim with no id | `pkg/mod.py#helper@0123abcd` | read | 2026-01-01 "
        f"| see{LS}also `pkg/mod.py#other@0123abcd` |\n"
    )
    # At `b` too the anchor that still resolves stands after the separator
    # alone, so each end's split is asked on its own.
    after = head + (
        "| a claim with no id, corrected | the notes cite it | read "
        f"| 2026-01-02 | see{LS}also `pkg/mod.py#other@0123abcd` |\n"
    )
    ledger = "seal/ledger.md"
    removed = survivor.removed_ledger_rows(
        "unused", "a", "b", {ledger: before}, {ledger: after}
    )
    assert removed == set()
