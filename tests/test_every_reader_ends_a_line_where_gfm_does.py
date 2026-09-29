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
