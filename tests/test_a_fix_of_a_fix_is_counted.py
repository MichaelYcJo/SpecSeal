"""A fix of a fix is counted, and the second one stops the fix passes (#823).

In two 0.18.3 review chains a fix pass wrote code and the next round's finding
was a regression inside the code that fix pass had just written, twice in a
row, and nothing counted it. `round_record.py new` now reads where each open
finding lands: inside a top-level unit the previous record's `Fix range` added
or changed is a fix of a fix, and the record's `Fix of a fix` row says so.
The first in a run reads `first`; the second reads `second`, `new` prints the
stop, and no record after it is written until `spec.md`'s foot says the frame
was redrawn.

`skills/code-review/orchestration.md` §*A fix of a fix twice sends the work
item back to its framer* owns the rule. These are the generator's cases, S1 to
S7 of the work item's `spec.md`, each on a scratch repository driven through
`new` and `close` exactly as an orchestrator drives them. The gate's cases are
in `tests/test_the_chain_goes_back_to_its_framer.py`.
"""

import shutil

import pytest
from test_the_fixes_close_the_record import close, fix_table
from test_the_record_is_generated import (
    ITEM,
    ROUNDS,
    check_module,
    commit,
    declared,
    fields,
    generate,
    git,
    report,
    write,
)

# Two units and a module-level line. `u` spans lines 4-5 and `v` lines 8-9;
# line 1 is in no unit at all.
MOD = "import os\n\n\ndef u():\n    return 1\n\n\ndef v():\n    return os.sep\n"
# Round 1's fix: `u` changed, `v` only re-commented, and `w` added.
MOD_FIXED = (
    "import os\n"
    "\n"
    "\n"
    "def u():\n"
    "    return 10\n"
    "\n"
    "\n"
    "def v():\n"
    "    # the separator, as the platform spells it\n"
    "    return os.sep\n"
    "\n"
    "\n"
    "def w():\n"
    "    return 3\n"
)
# Round 2's fix: `u` changed again.
MOD_FIXED_AGAIN = MOD_FIXED.replace("return 10", "return 100")

ROUND_1 = "| 🔴 1 | u returns the wrong value | `mod.py:5` | open | executed |\n"


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    write(d, "mod.py", MOD)
    write(d, "README.md", "# a fixture\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("fix-of-a-fix-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def finding(location, n=1, mark="🟡", verdict="open"):
    return f"| {mark} {n} | a regression | {location} | {verdict} | read |\n"


def round_report(*rows):
    return report(verdicts="".join(rows), needs="yes — a regression")


def a_round(repo, n, *rows):
    """Round `n` generated from a report holding `rows`, and committed.
    Returns (exit, output, record, the commit the record landed in)."""
    code, out, text = generate(repo, n=n, report_text=round_report(*rows))
    head = commit(repo, f"round {n}") if text is not None else None
    return code, out, text, head


def fixed(repo, n, start, mod, numbers):
    """Round `n`'s fix pass: `mod.py` rewritten, committed, and `close` run
    over `start..fix` with every finding in `numbers` fixed there."""
    write(repo, "mod.py", mod)
    fix = commit(repo, f"fix round {n}")
    rows = [f"| {k} | fixed | {fix[:7]} |\n" for k in numbers]
    code, out, _record = close(repo, n, fix_table(*rows), f"{start[:8]}..{fix[:8]}")
    assert code != 2, out
    return commit(repo, f"close round {n}")


def deferred_to_the_frame(repo, n, start, numbers):
    """Round `n` closed on `deferred the frame` over a range of no commits —
    what the stop writes in place of a fix pass."""
    rows = [f"| {k} | deferred the frame | the frame |\n" for k in numbers]
    code, out, record = close(repo, n, fix_table(*rows), f"{start[:8]}..{start[:8]}")
    assert code != 2, out
    commit(repo, f"close round {n}")
    return record


def two_rounds(repo, second_location):
    """Round 1 opens a finding in `u`, its fix changes `u`, adds `w` and
    re-comments `v`, and round 2 opens one finding at `second_location`."""
    declared(repo)
    code, out, _text, a = a_round(repo, 1, ROUND_1)
    assert code != 2, out
    fixed(repo, 1, a, MOD_FIXED, [1])
    return a_round(repo, 2, finding(second_location))


def row(text):
    return fields(text)["Fix of a fix"]


# --- S1, the quiet record ---------------------------------------------------


def test_round_one_reads_no(repo):
    """S1's base: a first round has no previous fix pass to land in."""
    declared(repo)
    code, out, text, _ = a_round(repo, 1, ROUND_1)
    assert code != 2, out
    assert row(text) == "no"


def test_a_finding_outside_the_units_the_fixes_wrote_reads_no(repo):
    """S1. Round 1's fixes changed `u` and added `w`; a finding in `f.py`
    lands in neither."""
    code, out, text, _ = two_rounds(repo, "`f.py:1`")
    assert code != 2, out
    assert row(text) == "no"


# --- S2, the first landing --------------------------------------------------


def test_a_finding_inside_a_unit_the_fixes_changed_reads_first(repo):
    """S2. The row names the finding, the unit and the record whose fixes
    changed it, and nothing about a stop is printed."""
    code, out, text, _ = two_rounds(repo, "`mod.py:5`")
    assert code != 2, out
    assert row(text) == "first — 🟡 1 at mod.py#u, a unit round-1's fixes changed"
    assert "the fix passes stop here" not in out, out


@pytest.mark.parametrize(
    "location",
    ["`mod.py#u`", "`mod.py::u`", "`u`", "`u()`"],
)
def test_every_location_shape_the_depth_walk_reads_lands(repo, location):
    """The readings `location_units` already makes, all four of them: a
    `Location` the depth walk can place is one this reading places too."""
    code, out, text, _ = two_rounds(repo, location)
    assert code != 2, out
    assert row(text).startswith("first — 🟡 1 at mod.py#u"), (row(text), out)


# --- S3, the second landing stops -------------------------------------------


def three_rounds(repo):
    """Round 2 lands in `u`, its fix changes `u` again, round 3 lands again."""
    code, out, _text, b = two_rounds(repo, "`mod.py:5`")
    assert code != 2, out
    fixed(repo, 2, b, MOD_FIXED_AGAIN, [1])
    return a_round(repo, 3, finding("`mod.py:5`"))


def test_the_second_landing_in_a_run_reads_second_and_prints_the_stop(repo):
    """S3. `second`, the stop sentence in the row, and the stop line printed
    naming the finding, the unit, the record whose fixes wrote it, and the
    exit -- read by the orchestrator deciding whether to spawn a fix pass, so
    every half of it is pinned (§14)."""
    code, out, text, _ = three_rounds(repo)
    assert code != 2, out
    assert row(text) == (
        "second — 🟡 1 at mod.py#u, a unit round-2's fixes changed; "
        "the fix passes stop here and the work item goes back to its framer"
    )
    line = next(
        (ln for ln in out.splitlines() if "the fix passes stop here" in ln), None
    )
    assert line is not None, out
    assert line.startswith("round-record: the fix passes stop here — "), line
    for part in (
        "🟡 1 at mod.py#u, a unit round-2's fixes changed",
        "round-2.md's fixes wrote the unit",
        "Do not commission a fix pass",
        check_module().REFRAME_EXIT,
    ):
        assert part in line, (part, line)


def test_a_quiet_record_between_the_two_does_not_restart_the_count(repo):
    """A run counts every record from its start, not only the previous one:
    round 2 `first`, round 3 quiet, round 4 lands again — `second`."""
    code, out, _text, b = two_rounds(repo, "`mod.py:5`")
    assert code != 2, out
    fixed(repo, 2, b, MOD_FIXED_AGAIN, [1])
    code, out, text, c = a_round(repo, 3, finding("`f.py:1`"))
    assert row(text) == "no", out
    write(repo, "f.py", "x = 2\n")
    fixed(repo, 3, c, MOD_FIXED_AGAIN.replace("return 3", "return 30"), [1])
    code, out, text, _ = a_round(repo, 4, finding("`mod.py#w`"))
    assert row(text).startswith("second — 🟡 1 at mod.py#w"), (row(text), out)


# --- S4, a landing in a new unit --------------------------------------------


def test_a_finding_inside_a_unit_the_fixes_added_says_added(repo):
    """S4. `w` is absent before round 1's fix and present after it."""
    code, out, text, _ = two_rounds(repo, "`mod.py#w`")
    assert code != 2, out
    assert row(text) == "first — 🟡 1 at mod.py#w, a unit round-1's fixes added"


# --- S5, what does not land -------------------------------------------------


@pytest.mark.parametrize(
    "location",
    [
        # A prose file the fix pass never touched, and one it did not parse.
        "`README.md`",
        # A module-level line, in no unit.
        "`mod.py:1`",
        # A unit the range only re-commented: its AST is equal at both ends.
        "`mod.py#v`",
        # A path this tree does not carry.
        "`nowhere.py:3`",
        # Round 1's 🟡 1: a prose file whose sentence names the unit the fixes
        # changed, and one naming the unit they added.
        "`README.md:1`, which describes `u`",
        "`README.md`, the sentence about `w()`",
        # The same beside a `.py` file the range did not touch.
        "`f.py:1`, called from `u`",
    ],
)
def test_a_location_that_lands_in_no_written_unit_reads_no(repo, location):
    code, out, text, _ = two_rounds(repo, location)
    assert code != 2, out
    assert row(text) == "no", (location, row(text))


def test_a_bare_name_two_files_of_the_range_carry_does_not_land(repo):
    """Round 1's 🟡 1, its other half: a bare name lands only where it
    resolves to one file of the range. Here round 1's fix changes `u` in
    `mod.py` and adds another `u` in `other.py`."""
    declared(repo)
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    write(repo, "other.py", "def u():\n    return 0\n")
    fixed(repo, 1, a, MOD_FIXED, [1])
    code, out, text, _ = a_round(repo, 2, finding("`u`"))
    assert code != 2, out
    assert row(text) == "no", row(text)


def test_a_bare_name_a_touched_file_carries_unchanged_does_not_land(repo):
    """Round 2's 🟡 1: `other.py` is touched by round 1's fix and carries a
    `u` the fix left alone, so a bare `u` names either file. The count is of
    every touched file defining the name at the target, changed or not."""
    declared(repo)
    write(repo, "other.py", "def u():\n    return 0\n\n\ndef z():\n    return 1\n")
    commit(repo, "other.py")
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    write(repo, "other.py", "def u():\n    return 0\n\n\ndef z():\n    return 2\n")
    fixed(repo, 1, a, MOD_FIXED, [1])
    code, out, text, _ = a_round(repo, 2, finding("`u`"))
    assert code != 2, out
    assert row(text) == "no", row(text)


TRACKED_FILES = ("bin/tool", "bin/tool.cmd", "Makefile", "hooks/x.html")


@pytest.mark.parametrize(
    "location",
    [
        # An extensionless tracked file, as `bin/` wrappers are.
        "`bin/tool`, which calls `u`",
        # A `.cmd` wrapper.
        "`bin/tool.cmd`, which calls `u`",
        # A tracked file with no directory and no extension.
        "`Makefile`, the target that runs `u`",
        # An extension no list carried.
        "`hooks/x.html`, which names `u`",
        # A tracked path with `:line`, and one written outside a code span.
        "`bin/tool:2`, which calls `u`",
        "bin/tool, which calls `u`",
    ],
)
def test_a_name_beside_a_tracked_file_of_any_kind_does_not_land(repo, location):
    """Round 2's 🟡 2, and the class: whether a cell names a file is asked of
    the tree, not guessed from an extension. Every one of these is tracked,
    so the cell is about that file and its backticked name is prose."""
    for rel in TRACKED_FILES:
        write(repo, rel, "u\nu\n")
    commit(repo, "the files the cells name")
    code, out, text, _ = two_rounds(repo, location)
    assert code != 2, out
    assert row(text) == "no", (location, row(text))


def test_a_name_beside_a_tracked_py_file_lands_only_through_it(repo):
    """The other half of the tracked-path test: a cell naming `mod.py` by a
    line lands there, and a tracked non-Python file named in the same cell
    does not move it."""
    for rel in TRACKED_FILES:
        write(repo, rel, "u\nu\n")
    commit(repo, "the files the cells name")
    code, out, text, _ = two_rounds(repo, "`mod.py:5`, called from `bin/tool`")
    assert code != 2, out
    assert row(text).startswith("first — 🟡 1 at mod.py#u"), row(text)


def test_a_finding_the_report_already_closed_does_not_land(repo):
    """Only the rows `close` will demand a fix-table row for: a verdict the
    reviewer closed in the report is no fix pass's to answer."""
    declared(repo)
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    fixed(repo, 1, a, MOD_FIXED, [1])
    code, out, text, _ = a_round(
        repo,
        2,
        finding("`f.py:1`", n=1),
        finding("`mod.py:5`", n=2, verdict="withdrawn"),
    )
    assert code != 2, out
    assert row(text) == "no"


@pytest.mark.parametrize("mark", ["⬜", "🟢", "❓"])
def test_a_finding_whose_severity_commissions_nothing_does_not_land(repo, mark):
    """A ⬜ is fixed in passing or not at all, and 🟢 and ❓ commission
    nothing: a row carrying one is open in the table and still owes no fix,
    so it is no fix of a fix however it sits inside `u`."""
    declared(repo)
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    fixed(repo, 1, a, MOD_FIXED, [1])
    code, out, text, _ = a_round(repo, 2, finding("`mod.py:5`", mark=mark))
    assert code != 2, out
    assert row(text) == "no", (mark, row(text))


def test_a_previous_record_that_commissioned_nothing_lands_nowhere(repo):
    """Round 1 opened nothing, so `close` never ran and its `Fix range` still
    reads `none`: there is no range for anything to land in."""
    declared(repo)
    _code, _out, text, _a = a_round(repo, 1, finding("`mod.py:5`", verdict="withdrawn"))
    assert fields(text)["Fix range"] == "none", text
    code, out, text, _ = a_round(repo, 2, finding("`mod.py:5`"))
    assert code != 2, out
    assert text is not None, out
    assert row(text) == "no"


def test_a_fix_range_of_no_commits_lands_nowhere(repo):
    declared(repo)
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    deferred_to_the_frame(repo, 1, a, [1])
    code, out, text, _ = a_round(repo, 2, finding("`mod.py:5`"))
    assert code != 2, out
    assert row(text) == "no"


# --- S6, the unresolvable range ---------------------------------------------


def foreign_range(repo):
    """Round 1 closed, then its `Fix range` rewritten to commits this tree
    does not carry."""
    declared(repo)
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    fixed(repo, 1, a, MOD_FIXED, [1])
    path = repo / ROUNDS / "round-1.md"
    text = path.read_text(encoding="utf-8")
    lines = [
        "| Fix range | `deadbeef..cafebabe`, 2 commits |"
        if ln.startswith("| Fix range |")
        else ln
        for ln in text.splitlines()
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    commit(repo, "a range from somewhere else")


def test_a_fix_range_this_tree_does_not_carry_is_refused(repo):
    """S6. `new` counts from the previous range, and it runs where `close`
    ran; ends this tree cannot resolve mean the wrong tree."""
    foreign_range(repo)
    code, out, text = generate(repo, n=2, report_text=round_report(finding("`u`")))
    assert code == 2, out
    assert text is None, "a refused record was written"
    assert "`deadbeef..cafebabe`" in out, out
    assert "the wrong tree to count in" in out, out


def test_a_foreign_range_with_no_open_row_reads_no(repo):
    """Round 1's ⬜ 3. With nothing open, nothing lands whatever the range
    holds, so a range this tree cannot resolve decides nothing and refuses
    nothing."""
    foreign_range(repo)
    code, out, text = generate(
        repo, n=2, report_text=round_report(finding("`u`", verdict="withdrawn"))
    )
    assert code != 2, out
    assert text is not None, out
    assert row(text) == "no"


# --- S7, no record after the stop without a reframe -------------------------


def stopped(repo, touched=False):
    """Round 3 reads `second` and closes on `deferred the frame`. `touched`
    puts a commit changing `u` inside that close's range, which no correct
    stop writes and which the record after it must still not count."""
    _code, out, text, c = three_rounds(repo)
    assert row(text).startswith("second"), (row(text), out)
    if not touched:
        deferred_to_the_frame(repo, 3, c, [1])
        return
    write(repo, "mod.py", MOD_FIXED_AGAIN.replace("return 100", "return 1000"))
    end = commit(repo, "a change inside the stop's range")
    rows = "| 1 | deferred the frame | the frame |\n"
    code, out, _record = close(repo, 3, fix_table(rows), f"{c[:8]}..{end[:8]}")
    assert code != 2, out
    commit(repo, "close round 3")


FRAMED = "Framed 2026-10-06 by framer, before the build.\n"
REFRAMED = "Reframed 2026-10-07 by framer, after round 3.\n"


def test_a_record_after_an_unreframed_second_is_refused(repo):
    stopped(repo)
    write(repo, f"{ITEM}/spec.md", "# a spec\n\n" + FRAMED)
    commit(repo, "the frame")
    code, out, text = generate(repo, n=4, report_text=round_report(finding("`u`")))
    assert code == 2, out
    assert text is None, "a record after an unreframed `second` was written"
    for part in (
        "round-3.md reads `second`",
        "`Reframed <date> by <who>, after round 3.`",
        "Nothing was written",
    ):
        assert part in out, (part, out)


def test_a_reframe_naming_another_round_does_not_permit_the_record(repo):
    stopped(repo)
    write(
        repo,
        f"{ITEM}/spec.md",
        "# a spec\n\n" + FRAMED + REFRAMED.replace("round 3", "round 2"),
    )
    commit(repo, "the frame, reframed after the wrong round")
    code, out, text = generate(repo, n=4, report_text=round_report(finding("`u`")))
    assert code == 2, out
    assert text is None


def test_an_orphan_second_is_no_stop_to_the_generator(repo):
    """Round 1's ⬜ 2, the generator's half: a `second` written by hand with
    no landing before it in its run cuts nothing, as the gate's `runs_of`
    cuts nothing there, so the next record needs no reframe."""
    declared(repo)
    _code, _out, _text, a = a_round(repo, 1, ROUND_1)
    fixed(repo, 1, a, MOD_FIXED, [1])
    a_round(repo, 2, finding("`f.py:1`"))
    path = repo / ROUNDS / "round-2.md"
    text = path.read_text(encoding="utf-8").replace(
        "| Fix of a fix | no |",
        "| Fix of a fix | second — 🟡 1 at f.py#x, a unit round-1's fixes "
        "changed; the fix passes stop here and the work item goes back to its "
        "framer |",
    )
    path.write_text(text, encoding="utf-8")
    commit(repo, "a second nobody counted")
    code, out, text = generate(repo, n=3, report_text=round_report(finding("`f.py:1`")))
    assert code != 2, out
    assert text is not None, out


def test_the_depth_restarts_at_a_stop(repo):
    """Round 1's ❓, decided by the orchestrator: a redesign is a new run, so
    a unit the stopped run's fixes added (`w`, round 1) does not make a unit
    the redesign's fix adds depth 2. Round 4's finding sits in `w`, and its
    fix adds `helper` to the same file; the depth walk reads the current run
    only, so `close` writes the record."""
    stopped(repo)
    write(repo, f"{ITEM}/spec.md", "# a spec\n\n" + FRAMED + REFRAMED)
    commit(repo, "the frame, redrawn")
    code, out, _text, d = a_round(repo, 4, finding("`mod.py#w`"))
    assert code != 2, out
    grown = (
        MOD_FIXED_AGAIN.replace("return 3", "return helper()")
        + "\n\ndef helper():\n    return 3\n"
    )
    fixed(repo, 4, d, grown, [1])
    record = (repo / ROUNDS / "round-4.md").read_text(encoding="utf-8")
    assert "helper (depth 1)" in fields(record)["New units"], record


@pytest.mark.parametrize("touched", [False, True])
def test_a_reframed_record_is_written_and_starts_the_count_at_no(repo, touched):
    """S7's other arm: with the line, the record is written, and a finding in
    `u` — the unit round 2's fixes wrote — reads `no`, because round 3 wrote
    no fixes for it to land in. `touched` is the same with a code commit in
    the stop's range: a `second` is the end of its run whatever its range
    holds, so the redesign's first record starts the count at `no`."""
    stopped(repo, touched)
    write(repo, f"{ITEM}/spec.md", "# a spec\n\n" + FRAMED + REFRAMED)
    commit(repo, "the frame, redrawn")
    code, out, text = generate(repo, n=4, report_text=round_report(finding("`u`")))
    assert code != 2, out
    assert text is not None, out
    assert row(text) == "no"
    assert "the fix passes stop here" not in out, out
    # `questions.md` Q3: the reach-back leaves the stopped record's
    # `no fixes to check` standing. It commissioned no fixes, so `round-4`
    # there would claim this round read fixes round 3 never wrote.
    stopped_record = (repo / ROUNDS / "round-3.md").read_text(encoding="utf-8")
    assert fields(stopped_record)["Fixes checked by"] == "no fixes to check"
    assert "left `Fixes checked by` of round-3.md at `no fixes to check`" in out, out


def test_fix_of_a_fix_count_reads_the_three_values_and_nothing_else():
    """The one reader of the row, shared by the gate and the generator."""
    count = check_module().fix_of_a_fix_count
    assert count("no") == 0
    assert count("`no`") == 0
    assert count("first — 🟡 1 at a.py#some_unit, a unit round-1's fixes changed") == 1
    assert count("second — 🟡 1 at a.py#u, …; the fix passes stop here") == 2
    for bad in ("", "first", "second", "first —", "third — x", "firstly — x", "yes"):
        assert count(bad) is None, bad
