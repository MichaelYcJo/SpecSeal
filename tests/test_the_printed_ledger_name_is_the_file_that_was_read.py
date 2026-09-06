"""The checker opened one file and printed the name of another.

Round 13 of work item `1788501054` closed the half that decides which file is
OPENED: `resolve_patterns` folds by inode and returns the spelling the pattern
gave, because `normpath` collapses `lnk/..` lexically and a normalised return
names a different file wherever `lnk` is a symlink. Round 14 found the printing
half still open — the issue listed four sites calling
`os.path.relpath(ledger, root)`, and `relpath` normalises exactly the way
`normpath` does. The run read `<root>/ledger.md`, exited 2 on its broken row,
and printed the header `x/ledger.md` over it. The exit code and the row were
right; the name a person reads and then goes to edit was a different file that
exists. That is issue #163, and `display_name` is the display side of
`resolve_patterns`' rule.

**The issue's four were not the class; there are five.** The fifth is `main`'s
`--ledger narrowed this run` loop, whose variable is `path` rather than
`ledger`, so a grep for `relpath(ledger` does not find it. Phase 2 enumerated
the class by data flow instead, and `test_no_ledger_path_reaches_relpath`
below is that enumeration kept as a case.

**Two kinds of case live here.** The unit's own, decomposed below (phase 1),
and the three at the end that read the checker's SOURCE to hold the class
(phase 2). The integration case over a real `--ledger` run is in
`tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`, beside the
symlink fixture it reuses.

**How the unit's cases were enumerated.** Not by listing what came to mind —
by decomposing the unit's input, which is two path strings and a path flavour:

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

import ast
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


def read_script():
    """The checker's own source, for the cases that hold the CLASS rather
    than the unit. Read as text on every call, so a case cannot be measuring
    a copy taken before its own edit."""
    with open(SCRIPT, encoding="utf-8") as handle:
        return handle.read()


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

    **The second assertion is what holds `altsep`, and nothing did until round
    1.** Dropping `flavour.altsep` from the separator set survived all 43
    cases, because the first assertion's `/` sits in the TAIL, which the unit
    slices rather than splits — the characters come back either way. Where it
    bites is a `/` inside the ROOT's own segments. An ABSOLUTE `--ledger`
    pattern is that input and it is reachable from the command line:
    `os.path.join` returns the second path unchanged when it is absolute, so
    `--ledger C:/proj/seal/ledger.md` under `root = os.path.abspath(".")` of
    `C:\\proj` arrives here exactly as spelled below. Without `altsep` the
    whole path is one segment, `1 <= 1` sends it back verbatim, and the header
    prints an absolute path where it should print `seal/ledger.md`.
    """
    assert shown(r"C:\proj\seal/ledger.md", r"C:\proj", flavour=ntpath) == (
        "seal/ledger.md"
    )
    assert shown("C:/proj/seal/ledger.md", r"C:\proj", flavour=ntpath) == (
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
    # The other direction, unpinned until round 1: case-folding the drive
    # survived all 43 cases. Windows treats `c:` and `C:` as one drive, so
    # folding them here is a defensible answer -- but it is not the answer
    # this unit gives, and the docstring says why: nothing on either side is
    # case-folded, resolved or normalised, because an answer derived that way
    # renames a file the operator did not name. Verbatim is longer and never
    # wrong, which is `plan.md`'s accepted alternative applied one more time.
    assert shown(r"C:\proj\seal\ledger.md", r"c:\proj", flavour=ntpath) == (
        r"C:\proj\seal\ledger.md"
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


# ------------------------------------------- the class, not the five sites


def carriers(text):
    """Every local name in `evidence_check.py` that can hold a ledger path.

    A ledger path enters that program at `resolve_patterns` and nowhere else,
    so the set is a fixed point over five rules: a name assigned from a
    `resolve_patterns` call carries one; a loop or comprehension variable over
    a carrier carries one; a function called with a carrier in argument
    position `i` gives its `i`th parameter one; a function that returns an
    expression mentioning a carrier gives its callers' assignment targets one;
    and a bare alias of a carrier, or a tuple of them, carries one.

    **It over-reaches in places, and that direction is the safe one.** The
    return rule marks `main`'s `findings` -- tuples whose first element is a
    coordinate -- and `resolve_patterns`' `key`, an inode pair; the alias rule
    marks every target of `a, b = ledger, root` rather than pairing them by
    position. None of those is a path, so each can raise a false alarm, and a
    false alarm costs a reader one minute.

    **What it does NOT claim is that a site cannot slip past it.** This
    docstring used to say the check could never let a real site through, and
    round 1 constructed six spellings that it did: an alias, a subscript, an
    inline wrapper, a tuple unpack, a bare `from os.path import relpath`, and
    `os.path.normpath`. All six are closed now and the seven arms of
    `test_the_refusal_above_can_actually_fail` hold them. A seventh spelling
    is always constructible -- a carrier reaching a rendering through a dict
    value, or through `getattr` -- so what these rules cover is the class of
    spelling somebody reaches for while editing, which is the class that
    produced issue #163. A guarantee is not on offer and was never measured.
    """
    tree = ast.parse(text)
    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    carried = {name: set() for name in funcs}
    hands_back = set()

    def names(node):
        return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}

    def bound(node):
        """Every name an assignment binds, tuple targets included.

        `main`'s own `migrated, left, unproven = migrate(...)` is that shape,
        and reading only top-level `ast.Name` targets skipped it -- so a
        carrier arriving through a tuple unpack was invisible (round 1).
        """
        return {
            sub.id
            for t in node.targets
            for sub in ast.walk(t)
            if isinstance(sub, ast.Name)
        }

    for fn in funcs.values():
        for n in ast.walk(fn):
            if not (isinstance(n, ast.Assign) and isinstance(n.value, ast.Call)):
                continue
            called = n.value.func
            if getattr(called, "id", None) == "resolve_patterns":
                carried[fn.name] |= bound(n)

    changed = True
    while changed:
        changed = False
        for fn in funcs.values():
            have = carried[fn.name]
            before = (len(have), len(hands_back))
            for n in ast.walk(fn):
                gens = []
                if isinstance(n, ast.For):
                    gens = [(n.target, n.iter)]
                elif isinstance(
                    n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
                ):
                    gens = [(g.target, g.iter) for g in n.generators]
                for target, over in gens:
                    if names(over) & have and isinstance(target, ast.Name):
                        have.add(target.id)
                if isinstance(n, ast.Assign):
                    if isinstance(n.value, ast.Call):
                        if getattr(n.value.func, "id", None) in hands_back:
                            have |= bound(n)
                    # A bare alias, or a tuple of them: `p = ledger`,
                    # `a, b = ledger, root`. Deliberately NOT every assignment
                    # mentioning a carrier -- round 1 measured that widening at
                    # fifteen extra names in `main` and six false alarms on the
                    # current source, where this one leaves the carrier sets
                    # byte-identical and closes the alias and tuple shapes.
                    values = (
                        n.value.elts if isinstance(n.value, ast.Tuple) else [n.value]
                    )
                    if any(isinstance(v, ast.Name) and v.id in have for v in values):
                        have |= bound(n)
                if isinstance(n, ast.Return) and n.value is not None:
                    if names(n.value) & have:
                        hands_back.add(fn.name)
                if isinstance(n, ast.Call):
                    callee = funcs.get(getattr(n.func, "id", None))
                    if callee is None:
                        continue
                    params = [a.arg for a in callee.args.args]
                    for i, arg in enumerate(n.args):
                        if i < len(params) and names(arg) & have:
                            if params[i] not in carried[callee.name]:
                                carried[callee.name].add(params[i])
                                changed = True
            if (len(have), len(hands_back)) != before:
                changed = True
    return carried


def relpath_on_a_ledger(text):
    """`(function, line, source)` for every parent-folding call on a ledger path.

    Three gates, each widened in round 1 after a measurement:

    - **Which call.** `relpath` AND `normpath`, matched on `os.path.relpath`
      and on a bare `relpath` alike -- reading only the attribute missed a
      `from os.path import relpath`, and reading only `relpath` missed the
      function that folds `..` by the same lexical rule and that round 13 of
      work item `1788501054` fought first.
    - **Which first argument.** Any carrier name ANYWHERE in it, rather than
      the whole argument being a carrier name. `relpath(ledgers[0], root)` and
      `relpath(os.path.join(ledger), root)` are the same defect wearing a
      subscript and a wrapper.

    `abspath` is deliberately absent though it folds `..` too, because
    `file_identity` calls it to build an inode fallback KEY that no person
    ever reads. Adding it would flag that line, and a check that cries wolf on
    the one correct use of a function is a check people learn to ignore.
    """
    carried = carriers(text)
    tree = ast.parse(text)
    found = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        have = carried.get(fn.name, set())
        for n in ast.walk(fn):
            if not isinstance(n, ast.Call) or not n.args:
                continue
            called = getattr(n.func, "attr", None) or getattr(n.func, "id", None)
            if called not in ("relpath", "normpath"):
                continue
            inside = {x.id for x in ast.walk(n.args[0]) if isinstance(x, ast.Name)}
            if inside & have:
                found.append((fn.name, n.lineno, ast.get_source_segment(text, n)))
    return found


def test_no_ledger_path_reaches_relpath():
    """The class, held by a property rather than by the five line numbers the
    issue happened to list.

    Without this the helper is a convention, and a convention is what this
    defect already was: `resolve_patterns` had carried the same rule for the
    file that is OPENED since round 13 of work item `1788501054`, said so in
    its docstring, and the printing half went on calling `relpath` for
    another two releases. What breaks in six months is a sixth site added by
    someone reaching for what the standard library offers.

    The check does not read line numbers or a list of names. It recomputes
    which locals can hold a ledger path -- the same data-flow enumeration
    phase 2 used to find the fifth site -- and refuses `relpath` and
    `normpath` on any of them. A site added tomorrow under a name nobody has
    thought of is in the set the moment a ledger path reaches it by one of the
    five propagation rules `carriers` lists.

    **That last clause is load-bearing and it used to be missing.** The
    sentence read *whatever it is called*, and round 1 constructed six
    spellings it did not catch. They are closed and pinned in
    `test_the_refusal_above_can_actually_fail`, and the honest statement of
    what this holds is there rather than here: the spellings somebody reaches
    for while editing, not every spelling that exists.

    Seen red first: `relpath_on_a_ledger` is run below over a copy of the
    source with one site put back, and that arm is what shows the detector
    can fail at all.
    """
    text = read_script()
    offenders = relpath_on_a_ledger(text)
    assert offenders == [], (
        "a ledger path is rendered by `os.path.relpath`, which folds `..` "
        "lexically and names a file that was not read (issue #163) — call "
        "`display_name(path, root)` instead:\n"
        + "\n".join(f"  {fn} L{ln}: {src}" for fn, ln, src in offenders)
    )


def test_the_refusal_above_can_actually_fail():
    """`verify`'s second condition — a check that cannot fail is a counterfeit
    seal — applied to the case above, which passes on an empty set and would
    pass just as quietly if the analysis had degraded to finding nothing.

    Two arms. The carrier set is asserted to hold the names the five real
    sites use, so an analysis that quietly returns nothing fails here; and the
    defect is put back into `main`'s per-ledger header in **seven spellings**,
    each of which the detector must name.

    **Seven rather than one, because round 1 measured that one proved almost
    nothing.** The first version of this arm put back the direct spelling
    alone, and six other ways of writing the same defect all went unreported:
    an alias (`name = ledger`), a subscript (`ledgers[0]`), an inline wrapper
    (`os.path.join(ledger)`), a tuple unpack — which `main`'s own
    `migrated, left, unproven = migrate(...)` makes reachable by an ordinary
    refactor — a bare `from os.path import relpath`, and `os.path.normpath`,
    which folds `..` by exactly the same lexical rule and is the function
    round 13 of work item `1788501054` fought in the first place.

    The shapes are the pin, not the count. A detector this one cannot evade is
    not on offer — a name reaching a rendering through a dict value or a
    `getattr` still passes — so what these seven hold is the class of spelling
    somebody reaches for while editing, which is the class that produced #163.
    """
    text = read_script()
    carried = carriers(text)
    for fn, name in (
        ("check_ledger", "ledger"),
        ("migrate", "ledger"),
        ("reverify", "ledger"),
        ("main", "ledger"),
        ("main", "missed"),
        ("main", "path"),
    ):
        assert name in carried.get(fn, set()), (
            f"the analysis lost `{name}` in `{fn}`, so it would not see a "
            "`relpath` put there"
        )

    header = 'print(f"\\n{display_name(ledger, root)}")'
    assert header in text, (
        "the header site was not found by its source text, so the arms below "
        "prove nothing — re-anchor them on the current spelling"
    )
    shapes = {
        "direct": 'print(f"\\n{os.path.relpath(ledger, root)}")',
        "alias": header
        + '\n        name = ledger\n        print(f"\\n{os.path.relpath(name, root)}")',
        "subscript": 'print(f"\\n{os.path.relpath(ledgers[0], root)}")',
        "inline wrapper": 'print(f"\\n{os.path.relpath(os.path.join(ledger), root)}")',
        "tuple unpack": header
        + '\n        a, b = ledger, root\n        print(f"\\n{os.path.relpath(a, b)}")',
        "bare import": 'print(f"\\n{relpath(ledger, root)}")',
        "normpath": 'print(f"\\n{os.path.normpath(ledger)}")',
    }
    for label, body in shapes.items():
        put_back = text.replace(header, body, 1)
        assert put_back != text, f"the {label} shape did not substitute"
        assert [fn for fn, _, _ in relpath_on_a_ledger(put_back)] == ["main"], (
            f"the defect was put back into `main`'s per-ledger header as a "
            f"{label} and the check did not name it"
        )


def test_the_scanned_source_path_is_not_a_ledger_and_keeps_its_relpath():
    """The judgement `spec.md` put out of scope, pinned so that a later
    session does not route it through `display_name` on the assumption that
    the two are interchangeable.

    `scan_candidates` renders a SCANNED SOURCE FILE, built by `os.walk` under
    `repo`, for the `(moved?)` hint on a broken row. Three things separate it
    from a ledger name. It carries no `..` to collapse, because `os.walk`
    composes it downward from the root it was given. It is compared against
    `rel`, a path spelled the way a ledger row spells one, so it must be
    normalised rather than preserved. And it appends
    `.replace(os.sep, "/")`, which `display_name` deliberately does not do --
    routing it through the helper would change what Windows prints for every
    such hint.

    So the detector must NOT reach it, and this pins that both ways: the site
    still calls `relpath`, and it is not in the class.
    """
    text = read_script()
    assert 'os.path.relpath(full, repo).replace(os.sep, "/")' in text, (
        "the scan-suggestion site changed shape; re-judge it against "
        "`spec.md`'s Out section rather than re-anchoring this case"
    )
    assert "scan_candidates" not in [fn for fn, _, _ in relpath_on_a_ledger(text)], (
        "the scanned-source path was classified as a ledger path — the "
        "class is *a ledger rendered for a person*, and this is not one"
    )
