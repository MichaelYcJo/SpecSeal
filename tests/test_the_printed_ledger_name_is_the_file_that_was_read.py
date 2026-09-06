"""The checker opened one file and printed the name of another.

Round 13 of work item `1788501054` closed the half that decides which file is
OPENED: `resolve_patterns` folds by inode and returns the spelling the pattern
gave, because `normpath` collapses `lnk/..` lexically and a normalised return
names a different file wherever `lnk` is a symlink. Round 14 found the printing
half still open — four sites calling `os.path.relpath(ledger, root)`, and
`relpath` normalises exactly the way `normpath` does. The run read
`<root>/ledger.md`, exited 2 on its broken row, and printed the header
`x/ledger.md` over it. The exit code and the row were right; the name a person
reads and then goes to edit was a different file that exists. That is issue
#163, and `display_name` is the display side of `resolve_patterns`' rule.

**What is here is the unit alone** (phase 1). The call sites, the integration
case over a real `--ledger` run, and the source-reading case that refuses a
future `relpath` on a ledger path are phase 2's.

**How these cases were enumerated.** Not by listing what came to mind — by
decomposing the unit's input, which is two path strings and a path flavour:

  A  the lexical relation between `path` and `root`, which is what the rule
     branches on: all of root's segments match with something left · all match
     with nothing left · a segment differs partway · a segment differs at the
     first position · root has no segments at all · root matches as a
     CHARACTER prefix but not a SEGMENT one · the anchors differ though the
     segments agree · the drives differ
  B  what the surviving part of `path` holds, by segment kind: ordinary · `.`
     · `..` · `..` reached through a symlink that exists on disk
  C  how `root` is spelled: absolute · `.` · with a trailing separator · one
     separator alone
  D  the separator style, by flavour: POSIX `/` · Windows `\\` · Windows mixed,
     which is what `os.path.join(root, "seal/ledger.md")` produces there

The Windows arms pass `ntpath` rather than skipping off Windows, because a
case that never runs where the platform differs is a defence resting on a
guarantee nobody removed (`agent-contract` §13).

**Every case here was seen red first**, and against which stand-in is stated
per case: `relpath` in the same position for the collapse cases, and the
verbatim-always alternative `plan.md` rejected for the cases that pin what an
ordinary run already prints. Both stand-ins live in
`test_tmp_*` form and are named in `phases/phase-1.md`.
"""

import importlib.util
import ntpath
import os
import posixpath

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "evidence-check", "scripts", "evidence_check.py")


def checker_module():
    spec = importlib.util.spec_from_file_location("specseal_ec_display", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ec = checker_module()


def shown(path, root, **kw):
    """One indirection, so a red run can put another rendering in this
    position without editing a case. Looked up on the module at call time."""
    return ec.display_name(path, root, **kw)


# ---------------------------------------------------------------- A1, B, C, D


def test_an_ordinary_ledger_name_loses_the_roots_own_segments():
    """A1, ordinary segments, an absolute root, POSIX — the shape every run
    takes, since `main` does `root = os.path.abspath(args.root)` and both
    ledger sources are then joined under it. Red against verbatim-always,
    which prints the whole absolute path.
    """
    assert shown("/tmp/proj/seal/ledger.md", "/tmp/proj", flavour=posixpath) == (
        "seal/ledger.md"
    )


def test_a_dot_root_still_renders_the_short_name():
    """A1 with C-dot. `default_patterns(".")` joins under `./seal`, so the
    spelling a direct in-process caller renders is `./seal/ledger.md` and it
    has to keep reading `seal/ledger.md`. Red against verbatim-always.

    The second assertion is the A4 arm of the same root — a bare relative
    spelling shares no leading segment with `.`, so it comes back verbatim,
    and verbatim is already the right name. It is an assertion rather than a
    case of its own because no candidate rendering here answers it
    differently, and a case that cannot go red is not a case (§15).
    """
    assert shown("./seal/ledger.md", ".", flavour=posixpath) == "seal/ledger.md"
    assert shown("seal/ledger.md", ".", flavour=posixpath) == "seal/ledger.md"


def test_the_defaults_render_the_names_they_have_always_rendered():
    """The acceptance row *an ordinary name is unchanged*, taken through the
    program's own pattern builder rather than through a hand-typed string, so
    a change to `default_patterns` reaches this case. Red against
    verbatim-always, which prints three absolute paths.
    """
    root = os.path.abspath(os.sep + os.path.join("tmp", "specseal-display-probe"))
    names = [shown(p, root) for p in ec.default_patterns(root)]
    assert names == [
        os.path.join("seal", "ledger.md"),
        os.path.join("seal", "ledger", "*.md"),
        os.path.join("docs", "**", "_evidence.md"),
    ], names


def test_a_trailing_separator_on_the_root_changes_nothing():
    """C-trailing. A root spelled with the separator the caller happened to
    leave on has the same segments, so it strips the same way. Red against
    verbatim-always.
    """
    assert shown("/tmp/proj/seal/ledger.md", "/tmp/proj/", flavour=posixpath) == (
        "seal/ledger.md"
    )


def test_a_root_of_one_separator_leaves_the_whole_tail():
    """A5 — root with no segments at all. Nothing is stripped but the anchor.
    Red against verbatim-always, which keeps the leading separator.
    """
    assert shown("/seal/ledger.md", "/", flavour=posixpath) == "seal/ledger.md"


# ------------------------------------------------------------ B — `..` and `.`


def test_a_parent_segment_is_never_folded_away():
    """B-`..` — the defect itself, as a string. `relpath` answers
    `x/ledger.md` here, which is issue #163's own example. Red against
    `relpath`.
    """
    assert (
        shown("/tmp/proj/x/lnk/../ledger.md", "/tmp/proj", flavour=posixpath)
        == "x/lnk/../ledger.md"
    )


def test_a_dot_segment_is_left_where_the_caller_put_it():
    """B-`.` — the rule is literal and has one branch, so a `.` segment
    survives too. Folding it would need a normalisation pass, and the pass
    that folds `.` is the one that folds `..`. Printing what the operator
    typed is never wrong. Red against `relpath`, which drops it.
    """
    assert (
        shown("/tmp/proj/./seal/ledger.md", "/tmp/proj", flavour=posixpath)
        == "./seal/ledger.md"
    )


@pytest.mark.skipif(os.name == "nt", reason="Win32 folds `..` before the filesystem")
def test_the_name_over_a_symlink_opens_the_file_that_was_read(tmp_path):
    """B — `..` reached through a symlink that exists on disk, which is what
    makes this a wrong FILE rather than a longer string.

    The fixture is issue #163's: `x/lnk -> y`, with a ledger at the root and a
    decoy at `x/ledger.md`. POSIX resolves `lnk` before it meets the `..`, so
    the pattern names `<root>/ledger.md`; `relpath` folds lexically and names
    `x/ledger.md`, which exists and holds something else. The case asserts
    both halves — that the rendered name reopens the file the pattern named,
    and that `relpath`'s answer reopens the decoy. Red against `relpath` on
    the first assertion.

    Skipped on Windows rather than branched, because there the premise is
    gone: Win32 collapses `..` before the filesystem is consulted, so the two
    renderings name one file and there is nothing to tell apart. That is round
    14's 🔴 1, one work item over.
    """
    root = str(tmp_path)
    (tmp_path / "y").mkdir()
    (tmp_path / "x").mkdir()
    (tmp_path / "x" / "lnk").symlink_to(tmp_path / "y")
    (tmp_path / "ledger.md").write_text("the file the pattern names\n")
    (tmp_path / "x" / "ledger.md").write_text("the decoy relpath names\n")

    pattern = os.path.join(root, "x", "lnk", "..", "ledger.md")
    (opened,) = ec.resolve_patterns([pattern])

    name = shown(opened, root)
    assert os.path.realpath(os.path.join(root, name)) == os.path.realpath(opened)
    assert (
        open(os.path.join(root, name), encoding="utf-8").read().startswith("the file")
    )

    collapsed = os.path.relpath(opened, root)
    assert os.path.realpath(os.path.join(root, collapsed)) != os.path.realpath(opened)


# ------------------------------------------------- A2, A3, A4, A6, A7 — a miss


def test_the_root_itself_has_no_name_under_itself():
    """A2 — every segment matches and nothing is left. `relpath` answers `.`,
    which names a directory rather than a ledger. Red against `relpath`.
    """
    assert shown("/tmp/proj", "/tmp/proj", flavour=posixpath) == "/tmp/proj"


def test_a_path_outside_the_root_keeps_its_own_spelling():
    """A4 — the first segment already differs. `relpath` climbs out with
    `../../elsewhere/...`, a name whose meaning depends on where the reader
    stands. Red against `relpath`.
    """
    assert (
        shown("/elsewhere/seal/ledger.md", "/tmp/proj", flavour=posixpath)
        == "/elsewhere/seal/ledger.md"
    )


def test_a_sibling_whose_name_extends_the_roots_is_not_under_it():
    """A6 — `/a/project` starts with the characters of `/a/proj` and is not
    under it. A `str.startswith` strip answers `ect/seal/ledger.md`, which is
    not a path at all; `relpath` answers `../project/seal/ledger.md`. Red
    against both.
    """
    assert (
        shown("/a/project/seal/ledger.md", "/a/proj", flavour=posixpath)
        == "/a/project/seal/ledger.md"
    )


def test_a_relative_path_is_not_under_an_absolute_root():
    """A7 — the segments agree and the anchors do not. `relpath` resolves the
    relative side against the process's current directory, so its answer
    changes with where the checker was invoked from; this one does not. Red
    against `relpath`.
    """
    assert (
        shown("tmp/proj/seal/ledger.md", "/tmp/proj", flavour=posixpath)
        == "tmp/proj/seal/ledger.md"
    )


def test_a_local_mode_home_outside_the_tree_prints_absolute():
    """The judgement the handoff asked to be written down. `seal_home` can
    answer `<git-common-dir>/seal`, and from a LINKED worktree that directory
    sits outside the worktree root — `optin.git_common_dir` normalises git's
    answer against the root, so it is absolute and outside.

    A4 covers it, and the consequence is the one `plan.md`'s accepted
    alternative accepts: the header prints the absolute path. Longer than
    `relpath`'s `../main/.git/seal/ledger.md`, and it names the file that was
    read from any directory. Red against `relpath`.
    """
    assert (
        shown("/clone/main/.git/seal/ledger.md", "/clone/wt", flavour=posixpath)
        == "/clone/main/.git/seal/ledger.md"
    )


# ------------------------------------------------------ D — separators, drives


def test_windows_separators_are_segments_too():
    """D-Windows. Run through `ntpath` from any platform, so the assertion is
    not waiting on a CI leg. Red against verbatim-always.
    """
    assert shown(r"C:\proj\seal\ledger.md", r"C:\proj", flavour=ntpath) == (
        r"seal\ledger.md"
    )


def test_a_windows_pattern_typed_with_forward_slashes_keeps_them():
    """D-mixed — what `os.path.join(root, "seal/ledger.md")` actually produces
    on Windows, which is how a `--ledger` argument arrives. Both characters
    are separators there, and the surviving substring keeps the spelling the
    caller used. Red against verbatim-always.
    """
    assert shown(r"C:\proj\seal/ledger.md", r"C:\proj", flavour=ntpath) == (
        "seal/ledger.md"
    )


def test_a_windows_parent_segment_is_never_folded_away():
    """D-Windows with B-`..`. `ntpath.relpath` folds it to `x\\ledger.md`. Win32
    would fold it at the filesystem too, so no file is misnamed there — but
    the unit's rule is one rule, and a renderer that folds on one platform and
    not the other is two. Red against `relpath`.
    """
    assert (
        shown(r"C:\proj\x\lnk\..\ledger.md", r"C:\proj", flavour=ntpath)
        == r"x\lnk\..\ledger.md"
    )


def test_a_path_on_another_drive_keeps_its_own_spelling():
    """A8 — `ntpath.relpath` does not answer this one at all: it raises
    `ValueError` when the two paths are on different drives, so the site that
    called it would traceback instead of printing a name. Red against
    `relpath`, which fails the case by raising.
    """
    assert shown(r"D:\proj\seal\ledger.md", r"C:\proj", flavour=ntpath) == (
        r"D:\proj\seal\ledger.md"
    )


def test_a_backslash_is_an_ordinary_character_on_posix():
    """D — the converse of the Windows arms, and what pins the separator set
    to the FLAVOUR rather than to a literal. A POSIX file may be named
    `a\\b.md`.

    **Two assertions, because the separator set is consulted in two places
    and only the second one can catch a literal.** In the surviving TAIL a
    hardcoded `\\` is invisible: the unit slices the original substring rather
    than rejoining segments, so splitting `a\\b.md` in two and then slicing
    from the first of them returns the same characters either way. The
    mutation that hardcodes the set survived this case alone, which is how the
    second assertion was found rather than recalled.

    Where it is not invisible is at the boundary the root ends on.
    `/tmp/proj\\seal` is one segment on POSIX — a file named `proj\\seal`
    under `/tmp` — so `/tmp/proj\\seal/ledger.md` is NOT under `/tmp/proj` and
    prints verbatim. A renderer with `\\` in its set reads three segments
    there, matches the root, and answers `seal/ledger.md`: a name under a root
    the file is not under, which is issue #163's own failure shape one
    character over.

    Red against verbatim-always on the first assertion, and red against both
    `relpath` and the hardcoded set on the second.
    """
    assert shown("/tmp/proj/a\\b.md", "/tmp/proj", flavour=posixpath) == "a\\b.md"
    assert (
        shown("/tmp/proj\\seal/ledger.md", "/tmp/proj", flavour=posixpath)
        == "/tmp/proj\\seal/ledger.md"
    )
