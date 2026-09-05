"""The smith's fix table closes the record, and the fix surface is measured.

Phase 1 of #161 generated the record from the reviewer's report. This is the
other half: a fix pass hands over `| # | Verdict | Commit or grounds |` under
`## Fixes`, and `round_record.py close` applies it to the verdict cells,
measures `Contract changes` and `New units` from the fix range's diff, and
refuses a unit at depth 2 before any cell is written.

Every case here reads the record back through the same reader `chain_check`
uses. The cases were written before `close` existed and seen red (§15): the
refusals assert on the message the refusal prints, which an absent
subcommand's usage error does not carry.

The fixture repository is richer than phase 1's: `mod.py` holds a unit with
one in-tree caller and one test caller, and a unit called from tests alone,
because that is the diff `Contract changes` has to name.
"""

import re
import shutil
import subprocess
import sys

import pytest
from test_the_record_is_generated import (
    GENERATOR,
    ITEM,
    ROUNDS,
    check_module,
    commit,
    declared,
    env_without_a_pull_request,
    fields,
    generate,
    generator_module,
    git,
    read,
    reader_module,
    report,
    rows_of,
    write,
)
from test_the_record_is_generated import run_check as check_tree

MOD = (
    "def helper(a):\n"
    "    return a\n"
    "\n"
    "\n"
    "def only_tested(a):\n"
    "    return a\n"
    "\n"
    "\n"
    "def caller():\n"
    "    return helper(1)\n"
    "\n"
    "\n"
    "def my_only_tested():\n"
    "    return 0\n"
)
TEST_MOD = (
    "from mod import helper, only_tested\n"
    "\n"
    "\n"
    "def test_helper():\n"
    "    assert helper(1) == 1\n"
    "\n"
    "\n"
    "def test_only_tested():\n"
    "    assert only_tested(2) == 2\n"
)
# The same file with two signatures changed and nothing added.
MOD_CHANGED = MOD.replace("def helper(a):", "def helper(a, b=None):").replace(
    "def only_tested(a):", "def only_tested(a, *rest):"
)
# The same file with a unit and a constant added and nothing changed.
MOD_GROWN = MOD + "\n\ndef added_unit():\n    return 1\n\n\nADDED = 1\n"

OPEN_1 = "| 🔴 1 | helper drops b | `mod.py#helper` | open | executed |\n"
OPEN_2 = "| 🟡 2 | only_tested ignores rest | `mod.py:5` | open | read |\n"
OPEN_3 = "| 🟡 3 | a sentence reads badly | `README.md` | open | read |\n"
THREE = OPEN_1 + OPEN_2 + OPEN_3


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "mod.py", MOD)
    write(d, "tests/test_mod.py", TEST_MOD)
    write(d, "README.md", "# a fixture\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("closed-record-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def fix_table(*rows):
    generator = generator_module()
    return (
        f"{generator.FIXES}\n\n{generator.row(generator.FIXES_HEADER)}\n"
        f"{generator.separator(len(generator.FIXES_HEADER))}\n" + "".join(rows)
    )


def close(repo, n, fixes, rng, extra=()):
    """Run `round_record.py close`; return (exit code, output, record text)."""
    path = repo.parent / f"fixes-{n}.md"
    path.write_text(fixes, encoding="utf-8")
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "close",
            "--item",
            str(repo / ITEM),
            "--round",
            str(n),
            "--fixes",
            str(path),
            "--range",
            rng,
            "--baseline",
            "base",
            *extra,
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env_without_a_pull_request(),
    )
    record = (repo / ROUNDS / f"round-{n}.md").read_text(encoding="utf-8")
    return r.returncode, r.stdout + r.stderr, record


def round_one(repo, verdicts=THREE):
    """Round 1 generated and committed; returns the commit the range starts at."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=verdicts))
    assert code == 0, out
    return commit(repo, "round 1")


def verdict_cells(record):
    reader = reader_module()
    return [
        [reader.visible(c) for c in reader.split_row(line)]
        for line in rows_of(record, "## Verdicts")[2:]
    ]


# --- the fix table applied ---------------------------------------------------


def test_each_verdict_shape_is_written_and_read_back(repo):
    a = round_one(repo)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _, out, record = close(
        repo,
        1,
        fix_table(
            f"| 🔴 1 | fixed | {b[:7]} — widened, b defaults to None |\n",
            "| 2 | answered | the rest is never passed |\n",
            "| 3 | deferred #12 | #12 |\n",
        ),
        f"{a}..{b}",
    )
    chain = check_module()
    one, two, three = verdict_cells(record)
    assert one[3] == f"**fixed** `{b[:7]}`", (one, out)
    assert one[4] == f"fixed at {b[:7]} — widened, b defaults to None; executed"
    assert chain.verdict_of(one, 3) == "fixed"
    assert two[3] == "answered"
    assert two[4] == "the rest is never passed"
    assert three[3] == "deferred #12"
    assert three[4] == "#12"
    # Only the verdict and grounds cells moved.
    assert one[:3] == ["🔴 1", "helper drops b", "`mod.py#helper`"]
    assert three[:3] == ["🟡 3", "a sentence reads badly", "`README.md`"]


def test_pass_is_ticked_when_nothing_is_open_and_the_gate_is_the_flag(repo):
    """After the table every row is closed, so `Pass` is ticked -- and the
    check the generator runs then refuses `Pass` beside `nobody` on the last
    record, which is the state that makes the verifying round mandatory.
    The exit is the check's; the record stands."""
    a = round_one(repo)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, record = close(
        repo,
        1,
        fix_table(
            f"| 1 | fixed | {b[:7]} |\n",
            "| 2 | answered | the rest is never passed |\n",
            "| 3 | answered | prose; ⬜, fixed in passing |\n",
        ),
        f"{a}..{b}",
        extra=("--broad-gate", "abc1234 vs base"),
    )
    assert "- [x] Pass" in record, out
    cells = fields(record)
    assert cells["Broad gate"] == "abc1234 vs base"
    assert cells["Fixes checked by"].startswith("nobody"), "left as it stands"
    assert code == 1, out
    assert "chain-check:" in out
    assert "`Pass` is checked beside" in out


def test_a_closed_record_reads_back_through_the_next_round(repo):
    """Round 1 closed by `close`, committed, then round 2 generated as the
    verifying round: the reach-back names round 2 and the check exits 0 with
    the second record uncommitted. The two-record run of phase 1, with the
    hand edits replaced by the table."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert "- [x] Pass" in record, out
    sha2 = commit(repo, "round 1 closed")
    code, out, second = generate(
        repo,
        n=2,
        target=sha2,
        report_text=report(
            verdicts="| 🟢 1 | round 1's fix holds | `mod.py#helper` | answered | executed |\n",
            needs="no",
        ),
    )
    assert second is not None, out
    assert code == 0, out
    assert fields(record := (repo / ROUNDS / "round-1.md").read_text())[
        "Fixes checked by"
    ] == ("round-2")


def test_a_gate_cell_left_alone_stays_as_it_was(repo):
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert fields(record)["Broad gate"] == "not yet", out


# --- the four refusals -------------------------------------------------------


def refused(repo, fixes, rng, n=1):
    before = (repo / ROUNDS / f"round-{n}.md").read_text(encoding="utf-8")
    code, out, record = close(repo, n, fixes, rng)
    assert code == 2, out
    assert record == before, "a refusal writes nothing"
    return out


def test_a_row_whose_number_is_not_in_the_table_is_refused(repo):
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    out = refused(
        repo,
        fix_table(f"| 1 | fixed | {b[:7]} |\n", "| 9 | answered | no such finding |\n"),
        f"{a}..{b}",
    )
    assert "finding 9, not in" in out, out
    assert "(which has 1)" in out, out


def test_a_verdict_outside_the_three_is_refused(repo):
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    for word in ("maybe fixed", "withdrawn", "not a defect", "open"):
        out = refused(repo, fix_table(f"| 1 | {word} | {b[:7]} |\n"), f"{a}..{b}")
        assert word in out and "fixed" in out and "deferred" in out, out


def test_a_fixed_row_without_a_resolving_commit_inside_the_range_is_refused(repo):
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    out = refused(repo, fix_table("| 1 | fixed | the fix is in |\n"), f"{a}..{b}")
    assert "names no commit" in out, out
    out = refused(repo, fix_table("| 1 | fixed | 0000000 |\n"), f"{a}..{b}")
    assert "does not resolve" in out, out
    # A commit that exists and lies before the range: the round-1 commit.
    out = refused(repo, fix_table(f"| 1 | fixed | {a[:7]} |\n"), f"{a}..{b}")
    assert "outside" in out and a[:7] in out, out


def test_a_finding_left_with_no_row_is_refused(repo):
    a = round_one(repo)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    out = refused(repo, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}")
    assert "2" in out and "3" in out and "no row" in out, out


def test_a_table_of_only_deferrals_ticks_pass(repo):
    """A capped run's fix table: every row `deferred <home>`. Phase 2's
    hand-back said the box stayed unticked beside the word, for want of it
    in `CLOSED_WORDS`; phase 3 put it there, and `close` reads the tick
    through `chain_check` rather than through a list of its own."""
    a = round_one(repo)
    write(repo, "README.md", "# a fixture, untouched by any fix\n")
    b = commit(repo, "nothing that answers a finding")
    _, out, record = close(
        repo,
        1,
        fix_table(
            "| 1 | deferred #170 | #170 |\n",
            "| 2 | deferred #171 | #171 |\n",
            "| 3 | deferred seal/follow-up.md | seal/follow-up.md |\n",
        ),
        f"{a}..{b}",
    )
    assert "- [x] Pass" in record, out
    one, two, three = verdict_cells(record)
    assert [one[3], two[3], three[3]] == [
        "deferred #170",
        "deferred #171",
        "deferred seal/follow-up.md",
    ]
    chain = check_module()
    assert all(chain.verdict_of(c, 3) == chain.DEFERRED for c in (one, two, three))


def test_a_capped_runs_last_record_reads_no_fixes_to_check_and_the_check_exits_zero(
    repo,
):
    """`questions.md` A6 of #161. A table of only `deferred <home>` rows closes
    nothing on a fix word, so nobody will ever open fixes this record
    commissioned and no next round exists to set the cell -- `nobody -- the
    fixes are not yet written` is false the moment it is written, and the
    check refuses `Pass` beside it on the last record (phase 3 measured exit 1
    here). `close` derives `no fixes to check` the way `new` derives it for a
    report whose every verdict closed without a fix word, and the run has the
    legal end the spec gives a capped run."""
    a = round_one(repo)
    write(repo, "README.md", "# a fixture, untouched by any fix\n")
    b = commit(repo, "nothing that answers a finding")
    code, out, record = close(
        repo,
        1,
        fix_table(
            "| 1 | deferred #170 | #170 |\n",
            "| 2 | deferred #171 | #171 |\n",
            "| 3 | deferred seal/follow-up.md | seal/follow-up.md |\n",
        ),
        f"{a}..{b}",
    )
    cells = fields(record)
    chain = check_module()
    assert cells["Fixes checked by"] == chain.NO_FIXES, (cells, out)
    assert cells["Contract changes"] == chain.NONE_WORD, cells
    assert cells["New units"] == chain.NONE_WORD, cells
    assert "- [x] Pass" in record, out
    assert "`Pass` is checked beside" not in out, out
    assert code == 0, out
    assert chain.NO_FIXES in out, out


def test_a_correction_closed_answered_lands_on_no_fixes_to_check(repo):
    """Rule 1's fix word, generator side (round 1's 🟡 2 of #161's own
    chain): a ⬜ row located in a record closes `answered` with `corrected
    at <sha>`, which is no fix word, so the cell reads `no fixes to check`
    and the check judged as READY exits 0 -- where `fixed <sha>` on the same
    row leaves `nobody` beside a checked `Pass` and exits 1."""
    note = "| ⬜ 1 | F1 counts three where four are excused | `seal/ledger.md` | open | read |\n"
    a = round_one(repo, verdicts=note)
    write(repo, "README.md", "# the ledger row corrected\n")
    b = commit(repo, "the correction")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | answered | corrected at {b[:7]} |\n"), f"{a}..{b}"
    )
    chain = check_module()
    assert fields(record)["Fixes checked by"] == chain.NO_FIXES, out
    assert "- [x] Pass" in record
    cells = verdict_cells(record)[0]
    assert cells[3] == "answered" and cells[4] == f"corrected at {b[:7]}", cells
    commit(repo, "round 1 closed")
    code, out = check_tree(repo)
    assert "judged as a ready pull request" in out, out
    assert code == 0, out


def test_a_table_with_a_fix_leaves_the_checker_cell_for_the_next_round(repo):
    """The other side of the derivation: one `fixed` row among deferrals means
    fixes exist that a later round owes a reading, so the cell stays at the
    landing value and `new` for round N+1 is what sets it."""
    a = round_one(repo)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _, out, record = close(
        repo,
        1,
        fix_table(
            f"| 1 | fixed | {b[:7]} |\n",
            "| 2 | deferred #171 | #171 |\n",
            "| 3 | deferred seal/follow-up.md | seal/follow-up.md |\n",
        ),
        f"{a}..{b}",
    )
    cells = fields(record)
    chain = check_module()
    assert cells["Fixes checked by"].startswith(chain.NOBODY), (cells, out)
    assert "- [x] Pass" in record, out


def test_a_finding_the_report_already_closed_needs_no_row(repo):
    """The reviewer may close a finding in the report (`withdrawn`, `not a
    defect`); the fix table owes a row for every OPEN finding and no other."""
    closed = "| 🟢 4 | seen and withdrawn | `mod.py:9` | withdrawn | read |\n"
    a = round_one(repo, verdicts=OPEN_1 + closed)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert "- [x] Pass" in record, out
    assert verdict_cells(record)[1][3] == "withdrawn"


def test_a_row_for_a_finding_the_reviewer_closed_is_refused(repo):
    """Round 1's 🟡 3 of #161's own chain: a row for a finding the reviewer
    closed in the report would overwrite the reviewer's verdict with the
    smith's, so it is refused naming the finding, and nothing is written --
    the `withdrawn` cell stays, and the open one stays open."""
    closed = "| 🟢 4 | seen and withdrawn | `mod.py:9` | withdrawn | read |\n"
    a = round_one(repo, verdicts=OPEN_1 + closed)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    out = refused(
        repo,
        fix_table(f"| 1 | fixed | {b[:7]} |\n", f"| 4 | fixed | {b[:7]} |\n"),
        f"{a}..{b}",
    )
    assert "finding 4" in out, out
    assert "withdrawn" in out, out
    cells = verdict_cells(read_record(repo, 1))
    assert cells[0][3] == "open" and cells[1][3] == "withdrawn", cells


def read_record(repo, n):
    return (repo / ROUNDS / f"round-{n}.md").read_text(encoding="utf-8")


# --- the fix surface, measured -----------------------------------------------


def test_contract_changes_name_the_unit_and_its_reach(repo):
    """One signature with an in-tree caller and a test caller, one with test
    callers alone. The def line is not a site, `my_only_tested(` is not a
    call of `only_tested`; a caller under `tests/` collapses to `pytest`,
    and to `pytest only` when it is the whole reach."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    cells = fields(record)
    assert cells["Contract changes"] == (
        "helper → caller, pytest; only_tested → pytest only"
    ), out
    assert cells["New units"] == "none"
    # The rows were replaced in place: the field table still has the
    # template's labels, once each, in the template's order.
    template = read("templates", "sdd-round.md")
    template = re.findall(
        r"^\| ([^|]+?) \| <",
        template[: template.index("- [ ] Pass")],
        flags=re.MULTILINE,
    )
    labels = [
        line.split("|")[1].strip()
        for line in record[: record.index("] Pass")].splitlines()
        if line.startswith("| ") and not line.startswith("| Field |")
    ]
    assert labels == template, (labels, template)


def test_a_changed_return_arity_is_a_contract_change(repo):
    a = round_one(repo, verdicts=OPEN_1)
    write(
        repo,
        "mod.py",
        MOD.replace("def helper(a):\n    return a", "def helper(a):\n    return a, a"),
    )
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert fields(record)["Contract changes"] == "helper → caller, pytest", out


def test_new_units_name_the_def_and_the_constant_at_depth_one(repo):
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_GROWN)
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    cells = fields(record)
    assert cells["New units"] == "added_unit (depth 1); ADDED (depth 1)", out
    assert cells["Contract changes"] == "none"
    chain = check_module()
    assert chain.depth_problems(cells["New units"]) == ([], [], [], [])


def test_a_file_the_ast_cannot_read_is_read_by_heuristic_and_says_so(repo):
    """A1: a `+` diff line starting with `def`, `class`, `function`, `fn` or
    `func` and a name is an added unit, and the record says which files
    were read that way -- in a comment after the table, never in the cell."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    write(
        repo,
        "lib.js",
        "function widget() {}\nclass Gadget {}\nconst arrow = () => 1;\n",
    )
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    cells = fields(record)
    assert cells["New units"] == "widget (depth 1); Gadget (depth 1)", out
    assert "<!--" not in cells["New units"]
    lines = record.splitlines()
    note = [i for i, ln in enumerate(lines) if ln.startswith("<!--") and "lib.js" in ln]
    assert len(note) == 1, record
    assert lines[note[0] - 1].startswith("| "), "the note follows the field table"
    assert not lines[note[0] + 1].strip(), "and stands on a line of its own"
    assert "heuristic" in lines[note[0]]


def test_prose_is_neither_ast_nor_heuristic(repo):
    """Round 1's 🟡 5 of #161's own chain: a Markdown line beginning `class
    of` or `def` is prose, and the heuristic read it as a definition and
    named every document the range touched as read that way. A prose suffix
    -- `.md`, `.markdown`, `.txt`, `.rst` -- is skipped whole: no entry, and
    no comment naming the file."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    write(
        repo,
        "NOTES.md",
        "# notes\n\nclass of defect the release would ship\ndef the word here\n",
    )
    write(repo, "notes.txt", "function words\n")
    write(repo, "notes.rst", "fn words\n")
    write(repo, "notes.markdown", "func words\n")
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert fields(record)["New units"] == check_module().NONE_WORD, out
    for name in ("NOTES.md", "notes.txt", "notes.rst", "notes.markdown"):
        assert name not in record, (name, record)
    assert not [ln for ln in record.splitlines() if ln.startswith("<!--")], record


def test_the_same_name_added_in_two_files_is_one_entry(repo):
    """Round 1's ⬜ 7: `New units` listed a name twice when two files added
    it. One entry, in first-seen order."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_GROWN)
    write(repo, "other.py", "def added_unit():\n    return 2\n")
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert fields(record)["New units"] == "added_unit (depth 1); ADDED (depth 1)", out


def test_a_surface_writer_refuses_a_separator_inside_a_name():
    generator = generator_module()
    with pytest.raises(generator.Refused):
        generator.contract_entry("get", ["a, b"])
    with pytest.raises(generator.Refused):
        generator.units_entry("a;b", 1)
    with pytest.raises(generator.Refused):
        generator.contract_entry("get", ["a | b"])
    assert generator.contract_entry("get", ["a", "b"]) == "get → a, b"
    assert generator.units_entry("get", 1) == "get (depth 1)"


# --- depth 2 is refused before any cell is written ----------------------------


GUARD = "\n\ndef helper_guard(b):\n    return b is not None\n"


def two_rounds(repo, location, path="mod.py", others=()):
    """Round 1 whose `New units` names `helper`, its fix in `path`, and
    round 2 locating a finding at `location`; returns round 2's commit, the
    start of the fix range. `others` are files committed before round 1."""
    declared(repo)
    for rel, text in others:
        write(repo, rel, text)
    if path != "mod.py":
        write(repo, path, MOD)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    commit(repo, "round 1")
    write(repo, path, MOD_CHANGED)
    commit(repo, "round 1's fix")
    finding = f"| 🔴 1 | helper guards nothing | {location} | open | executed |\n"
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=finding))
    assert code in (0, 1), out
    first = repo / ROUNDS / "round-1.md"
    text = first.read_text(encoding="utf-8")
    text = re.sub(
        r"^\| New units \|.*$",
        "| New units | helper (depth 1) |",
        text,
        flags=re.MULTILINE,
    )
    first.write_text(text, encoding="utf-8")
    return commit(repo, "round 2")


@pytest.mark.parametrize(
    "location",
    [
        "`mod.py#helper`",
        "`mod.py:2`",
        "`helper`",
        "`mod.py#helper@deadbee`",
        "`./mod.py#helper`",
        "`helper()`",
        "helper",
        "`mod.py::helper`",
        "`mod.py:2`, and the guard at `README.md`",
    ],
    ids=[
        "path-unit",
        "path-line",
        "identifier",
        "path-unit-hash",
        "dot-slash",
        "identifier-call",
        "bare",
        "double-colon",
        "prose-around-path-line",
    ],
)
def test_a_unit_added_beside_a_finding_inside_an_earlier_units_is_refused(
    repo, location
):
    """Round 1's `New units` names `helper`; round 2's finding sits inside
    `helper`; the fix adds `helper_guard` in the same file. That is depth 2,
    and it is refused naming the unit, the finding, and the record whose
    row names the parent -- with the exit the rule gives.

    The last five forms are the ones round 1 of #161's own chain found
    escaping (🟡 4): each closed with `helper_guard (depth 1)` until the
    Location's path was resolved against the tree and `()` and `::`
    were read. A bare name is resolved against every file the range
    touched, at the range's start, that holds a unit of that name."""
    a = two_rounds(repo, location)
    write(repo, "mod.py", MOD_CHANGED + GUARD)
    b = commit(repo, "round 2's fix")
    out = refused(repo, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}", n=2)
    assert "helper_guard" in out, out
    assert "🔴 1" in out
    assert "round-1.md" in out
    assert "depth 2" in out
    assert "deferred with a named answerer, or becomes an issue" in out


def test_a_basename_resolves_to_the_one_tracked_file_that_ends_in_it(repo):
    """Records name `chain_check.py#fix_surface` for a file three directories
    down, and the walk compared that basename with the diff's full path and
    never matched. The one tracked path ending in `/inner.py` is the file."""
    a = two_rounds(repo, "`inner.py#helper`", path="pkg/inner.py")
    write(repo, "pkg/inner.py", MOD_CHANGED + GUARD)
    b = commit(repo, "round 2's fix")
    out = refused(repo, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}", n=2)
    assert "helper_guard" in out and "pkg/inner.py" in out, out
    assert "depth 2" in out


def test_a_same_named_unit_in_another_file_is_not_refused(repo):
    """The other direction: round 1's `helper` is `mod.py`'s. A finding
    located at `other.py#helper`, where `other.py` holds no `helper` at the
    range's start, is not inside that unit, so a unit the fix adds in
    `other.py` is depth 1 -- the walk used to refuse it on the name alone."""
    a = two_rounds(
        repo,
        "`other.py#helper`",
        others=[("other.py", "def unrelated():\n    return 0\n")],
    )
    write(repo, "other.py", "def unrelated():\n    return 0\n" + GUARD)
    b = commit(repo, "round 2's fix")
    _, out, record = close(
        repo, 2, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert fields(record)["New units"] == "helper_guard (depth 1)", out


def test_the_same_range_is_depth_one_when_no_earlier_row_names_the_parent(repo):
    """The contrast: the identical fix, with round 1's `New units` left at
    `none`, lands at depth 1."""
    a = round_one(repo, verdicts=OPEN_1)
    write(
        repo,
        "mod.py",
        MOD_CHANGED + "\n\ndef helper_guard(b):\n    return b is not None\n",
    )
    b = commit(repo, "fix")
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert fields(record)["New units"] == "helper_guard (depth 1)", out


# --- the two agents hand over the table and write no phase record ------------


def test_the_smith_hands_over_the_fix_table_and_writes_no_phase_record():
    generator = generator_module()
    smith = read("agents", "smith.md")
    assert generator.FIXES in smith
    assert generator.row(generator.FIXES_HEADER) in smith
    assert "writes no `phases/phase-N.md`" in smith, (
        "agents/smith.md does not say a fix pass writes no phase record"
    )
    assert "round_record.py close" in smith, (
        "agents/smith.md does not say the depth is measured by `close`"
    )
    assert "depth is measured rather than declared" in smith, (
        "agents/smith.md still has the smith declare the depth in the hand-back"
    )
    flat = " ".join(smith.split())
    assert "one row per OPEN finding of the round it answers" in flat
    assert "refuses a row for a finding the reviewer already closed" in flat, (
        "agents/smith.md does not say a row for a closed finding is refused"
    )


def test_the_review_skill_says_close_writes_the_capped_ends_checker_cell():
    """§14: the cell `close` now writes is a value a person reads, so the
    skill's `Fixes checked by` section says which subcommand writes it and
    when, beside the sentence that gives `new` the reach-back."""
    chain = check_module()
    skill = read("skills", "code-review", "SKILL.md")
    section = skill[
        skill.index("### Then say who checked them") : skill.index(
            "### And name the fix surface"
        )
    ]
    flat = " ".join(section.split())
    assert f"`round_record.py close` writes `{chain.NO_FIXES}`" in flat, (
        "skills/code-review/SKILL.md does not say `close` writes the capped "
        "end's checker cell"
    )
    assert "has no next round to set the cell" in flat


def test_the_implement_skill_says_the_same_in_section_five():
    generator = generator_module()
    skill = read("skills", "implement", "SKILL.md")
    five = skill[skill.index("### 5. Incorporate review") : skill.index("### 6. Close")]
    assert generator.FIXES in five
    assert generator.row(generator.FIXES_HEADER) in five
    assert "writes no `phases/phase-N.md`" in five, (
        "skills/implement/SKILL.md §5 does not say a fix pass writes no phase record"
    )
    flat = " ".join(five.split())
    assert "one row per OPEN finding of the round it answers" in flat
    assert (
        "the reviewer closed in the report takes no row, and `close` refuses one"
        in flat
    )
