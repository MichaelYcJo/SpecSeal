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


def test_a_directory_at_the_record_path_is_refused_as_a_directory(repo):
    """The second member of ⬜ 6's class, in `close` rather than `report_path`.

    `not os.path.isfile(target)` is True for a directory as well as for a
    missing file, and `does not exist` about a path that has a directory at
    it sends the reader looking for something they already made. The fix
    that closed the report guard is owed here for the same cause (§12).

    Driven through `subprocess` rather than the `close` helper above: that
    helper reads the record back on its way out, which is exactly the read
    that cannot work when the record path is a directory.
    """
    declared(repo)
    (repo / ROUNDS / "round-1.md").mkdir(parents=True)
    fixes = repo.parent / "fixes-none.md"
    fixes.write_text(fix_table("| 1 | answered | none |\n"), encoding="utf-8")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "close",
            "--item",
            str(repo / ITEM),
            "--round",
            "1",
            "--fixes",
            str(fixes),
            "--range",
            f"{head}..{head}",
            "--baseline",
            "base",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env_without_a_pull_request(),
    )
    out = r.stdout + r.stderr
    assert r.returncode == 2, out
    assert "is a directory" in out, out
    assert "does not exist" not in out, (
        "the refusal still says the record is missing where a directory is"
    )
    # And it still says what `close` is for, which is how the reader learns
    # the directory is in the record's place rather than beside it.
    assert "`new` wrote" in out, out


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
    # Each of the three joins the reviewer's own grounds rather than
    # overwriting them (#391). `read` is what OPEN_2's reviewer wrote.
    assert two[4] == "the rest is never passed; read"
    assert three[3] == "deferred #12"
    assert three[4] == "#12; read"
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


def test_close_reads_back_the_record_it_writes(repo):
    """#182: `close` is the second writer, and its flag reaches the record
    the same way `new`'s does.

    `cell` refuses a `|` and a newline because either breaks the row. `<!--`
    breaks every reader below the row, and `close` writes the gate cell into
    the field table at the top of the record — so an opener there blanks the
    verdict table, the probes, the inherited coordinates and the Deferred
    section, in a file the pull-request check then reads.

    Executed at `0b99eb9` before this: the record rewritten, exit 1, and its
    `## Verdicts` resolving to 0 occurrences through the shared reader."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    before = (repo / ROUNDS / "round-1.md").read_text(encoding="utf-8")
    code, out, record = close(
        repo,
        1,
        fix_table(f"| 1 | fixed | {b[:7]} |\n"),
        f"{a}..{b}",
        extra=("--broad-gate", "abc1234 <!-- vs base"),
    )
    assert code == 2, out
    assert record == before, "a refusal writes nothing"
    assert "the record this would write" in out
    assert "never closed" in out
    assert "Broad gate" in out, "the coordinate names the row the value landed in"


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


def test_a_scope_marker_keeps_its_own_word(repo):
    """#353, measured twice in one run on #84. `❓ out of verified scope` is
    the reviewer looking and not judging — it carries no defect and
    commissions no fix. `close` counted it OPEN, refused to run until a fix
    row existed for it, and then wrote that row's word over the marker: round
    1's finding 15 of `1789081272-…` reads `answered` in the record where the
    report it was generated from reads the marker, and round 2 — the round
    that FOUND that — could only close its own copy as `deferred
    agents/sealer.md`, replacing the marker a second time in a different word.

    None of the three words is true of it. There is nothing for a closure word
    to change, so the row is not asked for one and keeps what the reviewer
    wrote.
    """
    marker = (
        "| 15 | the broad gate | `seal/config.md` "
        "| \N{BLACK QUESTION MARK ORNAMENT} out of verified scope "
        "| contract \N{SECTION SIGN}2 makes it one act with one owner |\n"
    )
    a = round_one(repo, verdicts=OPEN_1 + marker)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, record = close(
        repo, 1, fix_table("| 1 | answered | b is never passed |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "finding 15 of round 1 left with no row" not in out, out
    _one, fifteen = verdict_cells(record)
    assert fifteen[3] == "\N{BLACK QUESTION MARK ORNAMENT} out of verified scope", (
        fifteen,
        out,
    )
    assert fifteen[4] == "contract \N{SECTION SIGN}2 makes it one act with one owner"
    assert "- [x] Pass" in record, out


def test_a_fix_row_for_a_scope_marker_is_refused_as_already_closed(repo):
    """The other direction of the same rule. A fix pass that writes a row for
    the marker anyway is overwriting the reviewer's verdict with its own,
    which is the refusal `close` already carries for `withdrawn` and `not a
    defect` — and which is exactly what #84's orchestrator was forced to do."""
    marker = (
        "| 15 | the broad gate | `seal/config.md` "
        "| \N{BLACK QUESTION MARK ORNAMENT} out of verified scope | not run |\n"
    )
    a = round_one(repo, verdicts=OPEN_1 + marker)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, _ = close(
        repo,
        1,
        fix_table(f"| 1 | fixed | {b[:7]} |\n", "| 15 | answered | not run |\n"),
        f"{a}..{b}",
    )
    assert code == 2, out
    assert "already closed" in out, out


# --- `Fixes checked by` after a fix table applies (#273 part 1) -------------


def test_the_checker_cell_stops_saying_the_fixes_are_not_yet_written(repo):
    """#273 part 1. `new` lands the cell on `nobody — the fixes are not yet
    written`, which is true while the round runs. `close` then applies a fix
    table naming the commits, writes them into the record's own verdict
    cells — and left the cell alone, so the record said the fixes were not
    written beside the commits that wrote them.

    The record is what the next round and the pull request read. `nobody` is
    still the truth and the reason is not: nobody has opened them YET is a
    different statement from they do not exist yet, and only the second is
    false here.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _code, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    chain = check_module()
    cell = fields(record)[chain.CHECKED_BY]
    assert chain.NOT_YET not in cell, (cell, out)
    # Still `nobody — <why>`, which is the one value the ordering rule allows
    # at this moment: a checker has to be a LATER round, and none exists.
    assert cell.startswith(chain.NOBODY), cell
    assert cell.strip() != chain.NOBODY, "a bare `nobody` names nothing"


def test_a_table_with_no_fix_word_still_lands_on_no_fixes_to_check(repo):
    """The other branch, unchanged. A round that commissioned no fixes will
    never have any, so the cell is `no fixes to check` and not a reason about
    fixes nobody has opened."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# untouched\n")
    b = commit(repo, "nothing")
    code, out, record = close(
        repo, 1, fix_table("| 1 | answered | never passed |\n"), f"{a}..{b}"
    )
    chain = check_module()
    assert fields(record)[chain.CHECKED_BY] == chain.NO_FIXES, out
    assert code == 0, out


def test_neither_chain_check_arm_turns_red_on_the_new_reason(repo):
    """Q5, run as the question asked: one fixture record, both arms.

    The fix-surface arm refuses `none — the fixes are not yet written` in the
    SURFACE row beside a `Fixes checked by` naming a later round, and it reads
    the reason text — so the question was whether changing the reason in the
    checker row reaches it. It does not: the arm reads the surface row, and
    its gate is `CHECKER_RE`, which matches `round-N` and neither spelling of
    `nobody — <why>`. `checked_by` never reads the reason at all; it requires
    only that one exist.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _code, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    chain = check_module()
    # The surface arm: it fires on the row `close` measured, not on the cell
    # this phase rewrote, and `close` fills both surface rows from the diff.
    assert "still says the fixes are not yet written" not in out, out
    # The checker arm: the value is read and not refused for its wording.
    assert "naming the three values" not in out, out
    cell = fields(record)[chain.CHECKED_BY]
    assert not chain.says_not_yet(cell), cell


# --- what `close` preserves in the Grounds cell (#391) ----------------------


@pytest.mark.parametrize("word", ["fixed", "answered", "deferred"])
def test_no_verdict_word_discards_a_cell_it_was_not_asked_to_change(repo, word):
    """#391 names one row and the class is three wide (§12).

    The reviewer's grounds are the reason the finding was opened, and a fix
    pass is not asked to change them — it is asked what it did about the
    finding. `fixed` already joined the two with `;`. `answered` overwrote the
    cell with the fix table's third cell, and `deferred` overwrote it with the
    home, so the reviewer's own sentence survived exactly one of the three
    words and nothing said which.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    third = {
        "fixed": f"{b[:7]} — widened, b defaults to None",
        "answered": "b is never passed by any caller",
        "deferred": "#391",
    }[word]
    verdict = "deferred #391" if word == "deferred" else word
    _, out, record = close(
        repo, 1, fix_table(f"| 1 | {verdict} | {third} |\n"), f"{a}..{b}"
    )
    (one,) = verdict_cells(record)
    # `executed` is what OPEN_1's reviewer wrote in the Grounds cell.
    assert "executed" in one[4], (word, one, out)


def test_a_deferred_row_keeps_the_fix_passs_reasoning(repo):
    """#391 part 1, executed in its own report: rows 15 and 16 of
    `1788926756-…/rounds/round-2.md` both read `| #309 |` where the fix table
    carried a paragraph each.

    A deferred finding is the one verdict whose reasoning is the whole of its
    value — nothing else in the tree will explain why it left. That fix pass
    committed a separate fixes file so the prose survived somewhere, which is
    a file nothing reads, written because the file that IS read dropped it.
    """
    prose = (
        "the truncation is `round_record.py new`'s and predates this branch, "
        "so repairing it here would widen the range the surface was measured on"
    )
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# untouched\n")
    b = commit(repo, "nothing")
    code, out, record = close(
        repo, 1, fix_table(f"| 1 | deferred #391 | {prose} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    (one,) = verdict_cells(record)
    assert one[3] == "deferred #391", (one, out)
    assert prose in one[4], one
    assert one[4] != "#391", "the cell reduced to the home alone"


def test_a_fix_commit_carries_no_empty_code_span(repo):
    """#391 part 2, and the standing `# RIDER:` at `fix_table`'s `note` line.

    The commit is cut out of the middle of its own code span and both
    backticks are left standing, so `` `e7d3447` — widened `` lands as
    `fixed at e7d3447 — `` — widened`. Measured 2026-09-14 over the committed
    corpus: **210 rows** carry it, not the 103 the frame read.

    The repair is here and not in `chain.SEPARATORS`, which the rider says and
    which the case below holds: that constant is shared with the `deferred`
    home reader and with `chain_check`'s readers, and widening it would strip
    the backticks off a home deliberately written as a code span.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _code, out, record = close(
        repo,
        1,
        fix_table(f"| 1 | fixed | `{b[:7]}` — widened, b defaults to None |\n"),
        f"{a}..{b}",
    )
    # Not `code == 0`: a `fixed` verdict leaves `Pass` beside `nobody` on
    # the last record, which the check refuses for reasons of its own.
    assert "bare integer" not in out, out
    (one,) = verdict_cells(record)
    assert "``" not in one[4], (one, out)
    assert one[4].startswith(f"fixed at {b[:7]} — widened, b defaults to None"), one


def test_the_empty_span_repair_did_not_widen_the_shared_separators():
    """The direction the rider says the repair must not take. `chain.SEPARATORS`
    is read by the `deferred` home reader here and by `chain_check`'s own
    readers, so a backtick added to it would change what three callers strip.
    The repair is at the `note` line, and this is what says it stayed there.

    **Measured 2026-09-14, and the rider's stated consequence does not hold at
    this site.** It says widening the constant would strip the backticks off a
    home deliberately written as a code span — but `chain.EMPHASIS` is
    `[*_`]+` and `fix_table` applies it to the verdict cell one line before
    `SEPARATORS` is reached, so `` deferred `seal/follow-up.md` `` already
    arrives as `deferred seal/follow-up.md`. The rider is right about WHERE
    the repair goes and its reason is not the one it gives. Recorded rather
    than quietly corrected, because the other two callers are a real cost and
    nothing here measured them.
    """
    generator = generator_module()
    assert "`" not in generator.chain.SEPARATORS, (
        "the repair moved into the shared constant the rider reserves"
    )
    body = open(generator.__file__, encoding="utf-8").read()
    body = body.split("def fix_table", 1)[1].split("\ndef ", 1)[0]
    assert "sha.start()" in body, "the cut is still at the `note` line"


# --- what the fix pass's verdict vocabulary admits (#341, #321, #273) -------


def test_a_correction_closes_in_the_spelling_the_documents_give(repo):
    """#341's comment: `docs/review-chain-spec.md` prescribed `answered —
    corrected at <sha>` as ONE cell and `close` refuses it, while
    `agents/smith.md` prescribed the two-cell shape `close` accepts. The
    repository shipped both readings and a case asserted both sentences.

    The verdict cell is vocabulary and the grounds cell is free text, so the
    correcting commit goes in the grounds — which is also the only reading
    under which anything can find it: `chain_check` skips every row whose
    verdict is not a fix word before it looks for a commit.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# the record corrected\n")
    b = commit(repo, "the correction")
    code, out, record = close(
        repo, 1, fix_table(f"| 1 | answered | corrected at {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    (one,) = verdict_cells(record)
    assert one[3] == "answered", (one, out)
    assert one[4] == f"corrected at {b[:7]}; executed", one


def test_the_suffixed_verdict_cell_is_refused_naming_the_two_cell_shape(repo):
    """The spelling the spec prescribed until this release, and the message a
    reader met when they typed it. `fixed`/`answered` with anything after the
    word is one cell doing two cells' work, and the refusal used to list the
    three words without saying that the cell had begun with one of them —
    leaving the reader to work out which half of their row was wrong.

    `deferred <home>` is the one word that legitimately carries a suffix, and
    the case below holds that open.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# the record corrected\n")
    b = commit(repo, "the correction")
    code, out, _ = close(
        repo,
        1,
        fix_table(f"| 1 | answered \N{EM DASH} corrected at {b[:7]} | x |\n"),
        f"{a}..{b}",
    )
    assert code == 2, out
    assert "Commit or grounds" in out, out
    assert "answered" in out, out


@pytest.mark.parametrize("sep", [",", "\N{EM DASH}", ":", "-"])
def test_the_row_the_suffixed_refusal_prints_is_a_row_the_table_accepts(repo, sep):
    """Round 1's 🟡 3. `head` was computed by splitting the cell on the first
    `SEPARATORS` character found ANYWHERE in it, and `SEPARATORS` begins with a
    space — so any cell containing a space split there whatever followed the
    word. `answered, corrected at <sha>` printed the paste-ready row
    `| 1 | answered, | … |`, whose verdict `fix_table` refuses on the next run.

    The em-dash spelling worked by luck, because its separator happens to be
    the space that follows the word. This is the arm phase 2 added precisely so
    a reader who followed the old spec would be told what to write, and for the
    comma spelling it told them wrong.

    Asserted by pasting the row back rather than by reading the message: a
    message that advises a refused row is what the finding is about, and only
    running its advice can catch it.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# the record corrected\n")
    b = commit(repo, "the correction")
    code, out, _ = close(
        repo,
        1,
        fix_table(f"| 1 | answered{sep} corrected at {b[:7]} | x |\n"),
        f"{a}..{b}",
    )
    assert code == 2, out
    advised = re.search(r"write\s+`(\|[^`]+\|)`", out)
    assert advised, out
    row = advised.group(1)
    assert "answered |" in row, (row, out)
    code, out, record = close(repo, 1, fix_table(row + "\n"), f"{a}..{b}")
    assert code == 0, (row, out)
    (one,) = verdict_cells(record)
    assert one[3] == "answered", (one, row)
    assert f"corrected at {b[:7]}" in one[4], (one, row)


def test_a_deferred_row_whose_third_cell_begins_with_its_home_says_it_once(repo):
    """Round 1's 🟡 4. The guard against repeating the home was exact equality,
    so it caught `| N | deferred #12 | #12 |` and missed the shape immediately
    beside it — #391's own worked example. `| 1 | deferred #309 | #309 — the
    parity arm is out of scope |` landed as
    `#309 — #309 — the parity arm is out of scope; executed`.

    A smaller version of the same noise, in the cell #391 exists to make
    readable.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# untouched\n")
    b = commit(repo, "nothing")
    code, out, record = close(
        repo,
        1,
        fix_table("| 1 | deferred #309 | #309 — the parity arm is out of scope |\n"),
        f"{a}..{b}",
    )
    assert code == 0, out
    (one,) = verdict_cells(record)
    assert one[4].count("#309") == 1, (one, out)
    assert "the parity arm is out of scope" in one[4], one
    assert "executed" in one[4], "the reviewer's grounds"


def test_the_unknown_finding_refusal_says_so_when_the_table_holds_no_id(repo):
    """Round 1's ⬜ 5. The parenthetical names the ids the verdict table does
    hold, so on an empty mapping it rendered as `(which has )` and the reader
    learned less than the sentence promised. Pre-existing — and the admission
    rule is what makes an empty mapping reachable from a well-formed report."""
    a = round_one(
        repo, verdicts="| carried | round 1's note | `mod.py` | verified | read |\n"
    )
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, _ = close(repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}")
    assert code == 2, out
    assert "(which has )" not in out, out
    assert "no numbered rows at all" in out, out


def test_a_deferred_verdict_still_carries_its_home_in_the_verdict_cell(repo):
    """The other side of the refusal above. `deferred <home>` is one word and
    a home in one cell by design — the home is what makes the deferral
    readable, and `verdict_of` hands back a bare `deferred` as OPEN."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# untouched\n")
    b = commit(repo, "nothing")
    code, out, record = close(
        repo, 1, fix_table("| 1 | deferred #391 | #391 |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    (one,) = verdict_cells(record)
    assert one[3] == "deferred #391", (one, out)


def test_a_repair_made_outside_the_tree_has_a_verdict(repo):
    """#321's comment. A finding repaired by a `gh issue edit` or an edit to a
    pull request body produces no commit in the branch, so `fixed` is unusable
    for it twice over: `fix_table` demands a commit in the third cell, and
    `close` then demands that commit resolve and lie inside `--range`.

    The repair still happened and the record has to say where it is. That is
    `answered`, with the repair named in the grounds — the same shape a
    correction takes, for the same reason: no code was written, so nobody is
    commissioned to read any.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# untouched by the repair\n")
    b = commit(repo, "nothing in the tree answers it")
    grounds = "repaired on the tracker: the body of #321 now names both halves"
    code, out, record = close(
        repo, 1, fix_table(f"| 1 | answered | {grounds} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    (one,) = verdict_cells(record)
    assert one[3] == "answered", (one, out)
    assert one[4] == f"{grounds}; executed", one


def test_fixed_on_a_repair_with_no_commit_is_refused_by_the_commit_it_needs(repo):
    """The direction that has to stay closed. `fixed` asserts a commit
    somebody can open, and a repair outside the tree has none — so the word
    is refused rather than quietly accepting a cell with no commit in it."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# untouched\n")
    b = commit(repo, "nothing")
    code, out, _ = close(
        repo, 1, fix_table("| 1 | fixed | repaired on the tracker |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "names no commit" in out, out


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
    # `--broad-gate` is passed because this case runs the check judged as
    # READY, and at a ready pull request `chain_check` reads that cell on the
    # last record (#295): a generated record says `not yet` until the one
    # full-suite run happens, and `not yet` there is a refusal of its own.
    # The value is `b`, the correction commit, because the broad gate runs
    # AFTER the fixes — a SHA the record's `Target SHA` descends from would
    # fail as the run spent before the round it was meant to seal.
    _, out, record = close(
        repo,
        1,
        fix_table(f"| 1 | answered | corrected at {b[:7]} |\n"),
        f"{a}..{b}",
        extra=("--broad-gate", f"{b[:7]} against base"),
    )
    chain = check_module()
    assert fields(record)["Fixes checked by"] == chain.NO_FIXES, out
    assert "- [x] Pass" in record
    cells = verdict_cells(record)[0]
    assert cells[3] == "answered", cells
    assert cells[4] == f"corrected at {b[:7]}; read", cells
    commit(repo, "round 1 closed")
    code, out = check_tree(repo)
    assert "judged as a ready pull request" in out, out
    assert code == 0, out


def test_close_does_not_overwrite_a_checker_cell_a_later_round_already_set(repo):
    """`close` corrects the landing value and nothing else.

    `Fixes checked by` naming a `round-N` is a later round's reading, set by
    the reach-back when that round's record was written. A `close` that
    rewrote the cell unconditionally would replace a fact — somebody read
    these fixes — with a weaker one, on any second application or on a record
    closed out of order.

    The cell is set by hand rather than by writing a second record, because
    the state this guards is *the cell already names a checker*, and how it
    came to say that is not what the guard reads. Found by mutation: dropping
    the comparison left every other case in this module green.
    """
    a = round_one(repo, verdicts=OPEN_1)
    path = repo / ROUNDS / "round-1.md"
    text = path.read_text(encoding="utf-8")
    chain = check_module()
    before = f"| {chain.CHECKED_BY} | {chain.NOBODY} \N{EM DASH} {chain.NOT_YET} |"
    assert before in text, text
    path.write_text(
        text.replace(before, f"| {chain.CHECKED_BY} | round-2 |"), encoding="utf-8"
    )
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _code, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert fields(record)[chain.CHECKED_BY] == "round-2", out


def test_a_table_with_a_fix_leaves_the_checker_cell_for_the_next_round(repo):
    """The other side of the derivation: one `fixed` row among deferrals means
    fixes exist that a later round owes a reading, so the cell carries the
    reason `close` writes for fixes nobody has opened — `nobody`, because a
    checker has to be a later round and none exists yet."""
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
    assert fields(text)["New units"] == "helper (depth 1)", (
        "the substitution missed, so round 1 names no unit and `depth_two` "
        "returns at its guard: the case this feeds would pass for a reason "
        "that has nothing to do with the finding (#407)"
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
        "`mod.py#other` and `#helper`",
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
        "fragment-after-path",
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


# #30's measured shape, in one file: two findings, each located inside a
# DIFFERENT unit that round 1's `New units` names, and each fix adding a unit
# of its own. The walk that compares the file cannot tell them apart; the walk
# that reads which commit added each unit can.
#
# The two parent units carry no underscore, and that is a fixture constraint
# rather than a preference: `units_named_earlier` runs each entry through
# `chain.EMPHASIS`, which is `[*_`]+`, so `only_tested` is read back as
# `onlytested` and matches no unit the AST names. That is a live defect of its
# own, outside this work item's six tickets, and it is written up in the
# stamped rider comment at `round_record.py#units_named_earlier` rather than
# repaired here. Spelled without the marker on purpose: `rider_check` reads
# any line carrying it as a rider of its own and asks this comment for a
# verification stamp it has no claim to make.
PAIR = "def alpha(a):\n    return a\n\n\ndef beta(a):\n    return a\n"
PAIR_FIXED = PAIR.replace("def alpha(a):", "def alpha(a, b=None):")
ALPHA_GUARD = "\n\ndef alpha_guard(b):\n    return b is not None\n"
BETA_GUARD = "\n\ndef beta_guard(b):\n    return b is not None\n"
TWO_INSIDE = (
    "| 🔴 1 | alpha guards nothing | `pair.py#alpha` | open | executed |\n"
    "| 🟡 2 | beta drops its rest | `pair.py#beta` | open | read |\n"
)


def two_findings_inside_two_earlier_units(repo):
    """Round 1 naming `alpha` and `beta`, then round 2 with a finding inside
    each. Returns round 2's commit, the start of the fix range."""
    declared(repo)
    write(repo, "pair.py", PAIR)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    commit(repo, "round 1")
    write(repo, "pair.py", PAIR_FIXED)
    commit(repo, "round 1's fix")
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=TWO_INSIDE))
    assert code in (0, 1), out
    first = repo / ROUNDS / "round-1.md"
    text = first.read_text(encoding="utf-8")
    text = re.sub(
        r"^\| New units \|.*$",
        "| New units | alpha (depth 1); beta (depth 1) |",
        text,
        flags=re.MULTILINE,
    )
    assert fields(text)["New units"] == "alpha (depth 1); beta (depth 1)", (
        "the substitution missed, so round 1 names no unit and `depth_two` "
        "returns at its guard (#407)"
    )
    first.write_text(text, encoding="utf-8")
    return commit(repo, "round 2")


def test_a_depth_two_refusal_names_the_finding_whose_fix_added_the_unit(repo):
    """#333, and S11. `inside = [n for r, n in added if r == f]` compared the
    FILE, so every unit added to that file was attributed to whichever fix row
    the walk reached first. The refusal fired correctly on #30 and named the
    wrong finding and the wrong enclosing unit — worse than firing wrongly,
    because the reader is sent to a row that did not add the unit.

    Two commits, one per finding, so each unit has an adder the range can
    resolve. Red against the file-level walk, which pairs both units with the
    same row.
    """
    a = two_findings_inside_two_earlier_units(repo)
    write(repo, "pair.py", PAIR_FIXED + ALPHA_GUARD)
    b1 = commit(repo, "round 2's fix for 1")
    write(repo, "pair.py", PAIR_FIXED + ALPHA_GUARD + BETA_GUARD)
    b2 = commit(repo, "round 2's fix for 2")
    out = refused(
        repo,
        fix_table(f"| 1 | fixed | {b1[:7]} |\n| 2 | fixed | {b2[:7]} |\n"),
        f"{a}..{b2}",
        n=2,
    )
    assert "depth 2" in out, out
    # Each unit paired with the finding whose commit added it, and with that
    # finding's own enclosing unit — the two halves the file-level walk got
    # wrong together.
    for name, finding, parent in (
        ("alpha_guard", "🔴 1", "alpha"),
        ("beta_guard", "🟡 2", "beta"),
    ):
        line = next(ln for ln in out.splitlines() if f"`{name}` in pair.py" in ln)
        assert finding in line, f"`{name}` is attributed to the wrong row:\n{out}"
        assert f"inside `{parent}`" in line, (
            f"`{name}` is named inside the wrong parent unit:\n{out}"
        )
    assert "FILE-LEVEL" not in out, (
        "the range resolves an adder for each unit, so nothing should fall back"
    )
    assert "deferred with a named answerer, or becomes an issue" in out


def test_a_depth_two_refusal_it_cannot_attribute_says_so_and_names_every_candidate(
    repo,
):
    """#333's other half, and S12. One commit answers both findings, so no
    unit resolves to a single row at any cost — `measure` compares two ends
    and a commit is one of them.

    It still refuses. `docs/review-chain-spec.md` takes that direction for
    every verdict the checker cannot read, and `CONTRIBUTING.md` supplies the
    asymmetry: a wrong deny costs a prompt, and a wrong allow here ships a
    depth-2 unit that is read by nobody. What changes is the MESSAGE — a
    per-file answer is structurally unable to state what the record is
    required to state per entry, so it says the attribution is file-level and
    names every candidate instead of asserting one.
    """
    a = two_findings_inside_two_earlier_units(repo)
    write(repo, "pair.py", PAIR_FIXED + ALPHA_GUARD + BETA_GUARD)
    b = commit(repo, "one commit answering both findings")
    out = refused(
        repo,
        fix_table(f"| 1 | fixed | {b[:7]} |\n| 2 | fixed | {b[:7]} |\n"),
        f"{a}..{b}",
        n=2,
    )
    assert "depth 2" in out, out
    assert "FILE-LEVEL" in out, out
    assert "the range does not resolve which fix added it" in out, out
    for finding, parent in (("🔴 1", "alpha"), ("🟡 2", "beta")):
        assert finding in out and f"inside `{parent}`" in out, out
    assert "deferred with a named answerer, or becomes an issue" in out


# Round 1's 🟡 3, one earlier unit instead of two: round 1 names `alpha` only,
# so finding 2 — inside `beta` — is not a candidate, and it is finding 2's
# commit that adds the unit.
PAIR_BOTH_FIXED = PAIR_FIXED.replace("def beta(a):", "def beta(a, *rest):")
ONE_INSIDE_ONE_OUTSIDE = (
    "| 🔴 1 | alpha guards nothing | `pair.py#alpha` | open | executed |\n"
    "| 🟡 2 | beta drops its rest | `pair.py#beta` | open | read |\n"
)


def one_finding_inside_one_earlier_unit(repo):
    """Round 1 naming `alpha` alone, then round 2 with a finding inside it and
    a second finding inside `beta`, which no earlier record names. Returns
    round 2's commit, the start of the fix range."""
    declared(repo)
    write(repo, "pair.py", PAIR)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, _ = generate(
        repo, n=2, report_text=report(verdicts=ONE_INSIDE_ONE_OUTSIDE)
    )
    assert code in (0, 1), out
    first = repo / ROUNDS / "round-1.md"
    text = first.read_text(encoding="utf-8")
    text = re.sub(
        r"^\| New units \|.*$",
        "| New units | alpha (depth 1) |",
        text,
        flags=re.MULTILINE,
    )
    assert fields(text)["New units"] == "alpha (depth 1)", (
        "the substitution missed, so round 1 names no unit and `depth_two` "
        "returns at its guard (#407)"
    )
    first.write_text(text, encoding="utf-8")
    return commit(repo, "round 2")


def test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one(repo):
    """Round 1's 🟡 3, and #333's quiet direction. `beta_guard` is added by
    finding 2's commit, and finding 2 sits inside no unit an earlier record
    names — so the unit is at depth 1 and the rule has nothing to say about
    it. The walk took the file-level fallback anyway, because the resolved
    adder is not one of the candidate rows, and then printed *the range does
    not resolve which fix added it* about a range that just had.

    Red against the tree before the fix: exit 2, FILE-LEVEL, and that
    sentence — which `docs/review-chain-spec.md` reserves for a range that
    resolved nothing.
    """
    a = one_finding_inside_one_earlier_unit(repo)
    write(repo, "pair.py", PAIR_FIXED)
    c1 = commit(repo, "finding 1's fix, adding nothing")
    write(repo, "pair.py", PAIR_BOTH_FIXED + BETA_GUARD)
    c2 = commit(repo, "finding 2's fix, adding the unit")
    _code, out, record = close(
        repo,
        2,
        fix_table(f"| 1 | fixed | {c1[:7]} |\n| 2 | fixed | {c2[:7]} |\n"),
        f"{a}..{c2}",
    )
    assert "depth 2" not in out, out
    assert "FILE-LEVEL" not in out, out
    # The positive assertion beside the two negatives (#407). Both of them
    # hold when `depth_two` returns at its own guard -- round 1 naming no unit
    # at all -- which is a state that has nothing to do with the finding this
    # case is named for. This is false in exactly that state.
    #
    # **It is a duplicate of the fixture's own guard and cannot fire ahead of
    # it** (round 1's ⬜ 4). `one_finding_inside_one_earlier_unit` asserts the
    # same equality on the same cell and nothing between the two writes it, so
    # in the defect state #407 names the fixture fires first and this is never
    # reached. What actually closed the vacuity is the fixture guard; this is
    # a second reader of the same fact, kept because it states inside the case
    # what the case depends on. Nothing in `close`'s output can discriminate
    # the two states -- `New units | beta_guard (depth 1)` is written from
    # `measure` and `added` whether or not the walk ran -- so there is no
    # assertion that would be both positive and independent.
    assert fields(read(repo / ROUNDS / "round-1.md"))["New units"] == (
        "alpha (depth 1)"
    ), (
        "round 1 names no unit, so `depth_two` returned at its guard and the "
        "two negatives above hold for a reason other than the judgment"
    )
    # The exit code is `chain_check`'s verdict on a fixture whose round 1 has
    # no fix surface and whose round 2 no later round has read — a different
    # question with its own cases, and the same reason
    # `test_the_reach_forward_says_nothing_where_the_next_round_does_not_exist`
    # asserts the line rather than the code. What this pins is that `close`
    # refused nothing and wrote the unit at depth 1.
    assert "round-record: closed" in out, out
    assert "no cell was written" not in out, out
    assert fields(record)["New units"] == "beta_guard (depth 1)", record


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
    skill = read("skills", "code-review", "orchestration.md")
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


# --- a pipe the smith wrote survives the close -------------------------------
#
# #189's last paragraph: the same question applies to `close`'s fix table,
# which takes free text in `Commit or grounds`. `new` escaping the report is
# half of it; a grounds cell the smith writes goes through this one.


def test_a_pipe_in_the_fix_tables_third_cell_reaches_the_record(repo):
    """`answered` puts the smith's third cell straight into `Grounds`. A `|`
    in it used to split the fix row before it was ever read, so the grounds
    the record carried stopped at the pipe."""
    a = round_one(repo)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    grounds = "the guard reads flags |= NEW, so the bit is set"
    code, out, record = close(
        repo,
        1,
        fix_table(
            f"| 1 | fixed | {b[:7]} |\n",
            f"| 2 | answered | {grounds} |\n",
            "| 3 | deferred #12 | #12 |\n",
        ),
        f"{a}..{b}",
    )
    assert code in (0, 1), out
    _one, two, _three = verdict_cells(record)
    assert two[4] == f"{grounds}; read", record


def test_a_pipe_the_record_already_carries_survives_close(repo):
    """The row `new` wrote is re-serialised by `close`, so an escaped pipe
    has to make the round trip once more without doubling its backslash or
    splitting the row."""
    grounds = "the augmented assignment reads a |= b"
    a = round_one(
        repo,
        verdicts=(
            f"| 🔴 1 | helper drops b | `mod.py#helper` | open | {grounds} |\n"
            + OPEN_2
            + OPEN_3
        ),
    )
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, record = close(
        repo,
        1,
        fix_table(
            f"| 1 | fixed | {b[:7]} |\n",
            "| 2 | answered | the rest is never passed |\n",
            "| 3 | deferred #12 | #12 |\n",
        ),
        f"{a}..{b}",
    )
    assert code in (0, 1), out
    one, _two, _three = verdict_cells(record)
    assert len(one) == 5, record
    assert one[4] == f"fixed at {b[:7]}; {grounds}"


def test_a_raw_pipe_the_record_already_carries_survives_close(repo):
    """Round 1's 🟡 5. `close` re-reads a verdict row out of the record it is
    about to rewrite, and that row may carry a BARE `|`: every record written
    before this branch escaped nothing, and a record is a file a person
    edits. Seven such rows stand in this repository's own committed records.

    `reader.split_row` puts the tail in a sixth cell, so the grounds stop at
    the pipe and the row outgrows its header. The two cases added with the
    change could not see it — one goes through `fix_table`, the other through
    an already-escaped pipe both readings agree about — and reverting both
    `close` sites left the module green."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=THREE))
    assert code == 0, out
    path = repo / ROUNDS / "round-1.md"
    grounds = "the augmented assignment reads a |= b"
    text = path.read_text(encoding="utf-8")
    assert "| open | executed |" in text
    path.write_text(
        text.replace("| open | executed |", f"| open | {grounds} |", 1),
        encoding="utf-8",
    )
    a = commit(repo, "round 1")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, record = close(
        repo,
        1,
        fix_table(
            f"| 1 | fixed | {b[:7]} |\n",
            "| 2 | answered | the rest is never passed |\n",
            "| 3 | deferred #12 | #12 |\n",
        ),
        f"{a}..{b}",
    )
    assert code in (0, 1), out
    one, _two, _three = verdict_cells(record)
    assert len(one) == 5, record
    assert one[4] == f"fixed at {b[:7]}; {grounds}"


def test_a_span_pipe_in_a_closed_row_does_not_leave_pass_unchecked(repo):
    """The other of `close`'s two reads of a verdict row, and it decides the
    `Pass` box rather than a Grounds cell.

    After the fix table is applied, `close` re-derives every row's verdict to
    decide whether anything is still open. That read walks rows the fix table
    never touched — including a finding the reviewer already closed — and a
    record written before this branch escaped nothing. Read by the plain
    splitter, a `|` inside a code span in the Finding cell shifts the row and
    the Location stands where the verdict word should be, so a closed finding
    counts as open and the run's own record goes out with `Pass` unchecked.

    The Grounds case beside this one cannot see it: it exercises the rewrite
    loop, which only visits rows the fix table names."""
    declared(repo)
    closed = "| 🟢 2 | round 0's finding | `mod.py:1` | answered | read |\n"
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1 + closed))
    assert code == 0, out
    path = repo / ROUNDS / "round-1.md"
    text = path.read_text(encoding="utf-8")
    assert "round 0's finding" in text
    path.write_text(
        text.replace("round 0's finding", "the cell reads `a | b`", 1),
        encoding="utf-8",
    )
    a = commit(repo, "round 1")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code in (0, 1), out
    assert "- [x] Pass" in record, record


# --- the reach forward: round N's words carried into round N+1's rows ---------


ROUND_TWO = "| 🟡 1 | the guard needs a case | `mod.py#only_tested` | open | read |\n"


def two_records(repo):
    """Round 1 and round 2 both generated and committed, in the order the
    chain writes them: a record lands BEFORE the fixes it commissions, so
    round 2's `## Inherited coordinates` carries round 1's findings at the
    word the reviewer wrote. Returns round 2's commit."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=ROUND_TWO))
    assert code in (0, 1), out
    return commit(repo, "round 2")


def inherited(repo, n=2):
    """{coordinate: why} for round N's `## Inherited coordinates` rows."""
    text = read(repo / ROUNDS / f"round-{n}.md")
    out = {}
    for line in rows_of(text, "## Inherited coordinates")[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3:
            out[cells[1]] = cells[2]
    return out


def test_two_records_committed_together_do_not_contradict_each_other(repo):
    """#342, and S8. `new --round 2` writes the inherited rows from round 1's
    verdict cells, which read `open` at that moment because a record is
    committed BEFORE the fixes it commissions. `close --round 1` then wrote
    the words into round 1 and nothing carried them forward, so the two
    records stated the same finding as open and as fixed.

    Red against the tree before this: the `Why` cell stays at `open` while
    round 1's own verdict cell reads `**fixed**`.
    """
    a = two_records(repo)
    assert inherited(repo)["`mod.py#helper`"].endswith("open"), (
        "the fixture is not the state this is about"
    )
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    code, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "**fixed**" in fields_row(record, "🔴 1"), record
    why = inherited(repo)["`mod.py#helper`"]
    assert why == f"round 1's 🔴 1 {chr(0x2014)} fixed", why
    # Printed the way the fix surface is, so an orchestrator reading stdout
    # sees the second file was written.
    assert "Inherited coordinates of round-2.md | 1 row filled" in out, out


def fields_row(record, number):
    """The verdict row whose `#` cell reads `number`."""
    for line in rows_of(record, "## Verdicts")[2:]:
        if line.strip("|").split("|")[0].strip() == number:
            return line
    raise AssertionError(f"no verdict row numbered {number!r}:\n{record}")


def test_the_reach_forward_says_nothing_where_the_next_round_does_not_exist(repo):
    """Every ordinary run: the fix pass comes first and the verifying round is
    spawned after it. A reach that refused here would stop the run it is meant
    to keep truthful."""
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    _code, out, _record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    # The exit code is `chain_check`'s verdict on a one-record run whose fixes
    # no later round has read, which is a different question and has its own
    # cases. What this pins is that `close` wrote its record and the reach
    # said nothing.
    assert "round-record: closed" in out, out
    assert "no cell was written" not in out, out
    assert "Inherited coordinates" not in out, out


def test_the_reach_forward_refuses_a_next_record_with_no_inherited_table(repo):
    """It refuses rather than guesses. A record whose `## Inherited
    coordinates` cannot be read is one whose `Why` cells will go on saying
    what round 1 said before its fixes, and there is no honest place to put
    the words."""
    a = two_records(repo)
    path = repo / ROUNDS / "round-2.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("## Inherited coordinates", "## Coordinates inherited"),
        encoding="utf-8",
    )
    b = commit(repo, "the section renamed by hand")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    before = (repo / ROUNDS / "round-1.md").read_text(encoding="utf-8")
    code, out, _record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "no readable `## Inherited coordinates` table" in out, out
    assert "no cell was written" in out, out
    assert (repo / ROUNDS / "round-1.md").read_text(encoding="utf-8") == before, (
        "round 1 was written under a refusal"
    )


def test_the_reach_forward_refuses_a_coordinate_the_verdict_table_lacks(repo):
    """The other refusal: a row inherited from round 1 whose coordinate round
    1's verdict table does not hold. The reach sets a `Why` cell from the row
    it names, and there is no row to name — so it declines rather than
    picking one."""
    a = two_records(repo)
    path = repo / ROUNDS / "round-2.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("| round-1 | `mod.py#helper` |", "| round-1 | `mod.py#absent` |"),
        encoding="utf-8",
    )
    commit(repo, "the coordinate edited by hand")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    code, out, _record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "`mod.py#absent`" in out and "holds no row with that `Location`" in out, out
    assert "no cell was written" in out, out


# --- the two shapes the reach refused although `new` wrote them ---------------


CONFIRMATION = "| 🟢 | round 0's finding, re-read | `README.md` | verified | read |\n"


def test_a_row_that_commissions_nothing_does_not_stop_the_reach(repo):
    """Round 1's 🔴 1. `inherited_rows` writes a row per `Location` cell of
    EVERY verdict row; `close` keyed its map from the numbered ones. A round
    carrying a confirmation — the shape `agents/warden.md` asks for, and 25 of
    the committed corpus — then could not be closed at all: `close` exited 2
    against a coordinate that was already correct.

    Red against the tree before the fix: exit 2, `README.md` named as a
    coordinate round 1's verdict table holds no row for.
    """
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1 + CONFIRMATION))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=ROUND_TWO))
    assert code in (0, 1), out
    a = commit(repo, "round 2")
    assert inherited(repo)["`README.md`"].endswith("verified"), (
        "the fixture is not the state this is about"
    )
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    code, out, _ = close(repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}")
    assert code == 0, out
    why = inherited(repo)
    # The numbered row carries its new word, and the row that commissions
    # nothing carries the word it already had rather than stopping the reach.
    assert why["`mod.py#helper`"] == f"round 1's 🔴 1 {chr(0x2014)} fixed", why
    assert why["`README.md`"] == f"round 1's 🟢 {chr(0x2014)} verified", why


def test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused(repo):
    """Round 1's 🔴 2. `inherited_rows` is first-seen-wins ACROSS rounds, so a
    round 2 finding at a coordinate round 1 already carried is written into
    round 3's section under `round-1` and under no other round. `close --round
    2` read a section with nothing from round 2 in it as a malformed record
    and refused.

    A re-review round looking again where the round before it looked is the
    ordinary shape, so this fired on the case the section is most useful for.
    Red against the tree before the fix: exit 2, *names no row from round-2*.
    """
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    a1 = commit(repo, "round 1")
    write(repo, "mod.py", MOD_CHANGED)
    b1 = commit(repo, "round 1's fix")
    code, out, _ = close(
        repo, 1, fix_table(f"| 1 | fixed | {b1[:7]} |\n"), f"{a1}..{b1}"
    )
    assert "no cell was written" not in out, out
    commit(repo, "round 1 closed")
    code, out, _ = generate(
        repo,
        n=2,
        report_text=report(
            verdicts="| 🟡 1 | helper still drops b | `mod.py#helper` | open | read |\n"
        ),
    )
    assert code in (0, 1), out
    commit(repo, "round 2")
    code, out, _ = generate(
        repo,
        n=3,
        report_text=report(
            verdicts="| 🟡 1 | a third look | `mod.py:5` | open | read |\n"
        ),
    )
    assert code in (0, 1), out
    a = commit(repo, "round 3")
    assert "round-2" not in "".join(
        rows_of(read(repo / ROUNDS / "round-3.md"), "## Inherited coordinates")
    ), "the fixture is not the state this is about"
    write(repo, "mod.py", MOD_CHANGED + "\n\ndef extra():\n    return 1\n")
    b = commit(repo, "round 2's fix")
    code, out, _ = close(
        repo, 2, fix_table("| 1 | answered | grounds |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "no cell was written" not in out, out
    assert "Inherited coordinates" not in out, out


# --- one coordinate, two verdict rows: both sides take the same row ----------
#
# #404. `inherited_rows` skips a `Location` it has already emitted and the map
# `close` hands the reach assigned into a plain dict, so one repeat resolved to
# the first row on one side and to the last on the other.


SAME_COORDINATE = (
    "| 🟢 | helper re-read after round 0 | `mod.py#helper` | verified | read |\n"
)
THREE_AT_ONE_COORDINATE = (
    SAME_COORDINATE
    + OPEN_1
    + "| ⬜ | round 0's record corrected | `mod.py#helper` | withdrawn | read |\n"
)


def test_the_reach_takes_the_row_the_inherited_table_attributed_it_to(repo):
    """A1. Round 1 carries `🔴 1 … open` and, below it, an unnumbered
    confirmation at the SAME coordinate. Round 2's section attributes that
    coordinate to the first of the two, so the reach has to write the first
    row's verdict into it.

    Red against the plain assignment: the `Why` cell reads
    `round 1's 🟢 — verified` — round 1 saying `**fixed**` for finding 1 while
    round 2 says that coordinate was verified by a row that commissioned
    nothing, which is #342's disease arriving through the repair for it.
    """
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1 + SAME_COORDINATE))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=ROUND_TWO))
    assert code in (0, 1), out
    a = commit(repo, "round 2")
    assert inherited(repo)["`mod.py#helper`"] == f"round 1's 🔴 1 {chr(0x2014)} open", (
        "the fixture is not the state this is about: the section has to "
        "attribute the repeated coordinate to round 1's first row"
    )
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    code, out, record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "**fixed**" in fields_row(record, "🔴 1"), record
    why = inherited(repo)["`mod.py#helper`"]
    assert why == f"round 1's 🔴 1 {chr(0x2014)} fixed", why


def test_a_repeated_coordinate_resolves_to_one_row_on_both_sides(repo):
    """A2. Three verdict rows at one `Location`, the numbered one in the
    middle, so neither side can agree by accident with a one-row table or by
    the numbered row happening to sit first.

    What is pinned is not WHICH row wins — it is that the writer of round 2's
    section and the map `close` hands the reach name the same `#` cell. The
    picking is not the defect; the disagreement is.

    Red against the plain assignment: the section names `🟢` and the reach
    overwrites the cell with `round 1's ⬜ — withdrawn`, the last row.
    """
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=THREE_AT_ONE_COORDINATE))
    assert code == 0, out
    commit(repo, "round 1")
    code, out, _ = generate(repo, n=2, report_text=report(verdicts=ROUND_TWO))
    assert code in (0, 1), out
    a = commit(repo, "round 2")
    before = inherited(repo)["`mod.py#helper`"]
    assert before == f"round 1's 🟢 {chr(0x2014)} verified", (
        f"the fixture is not the state this is about: {before!r}"
    )
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    code, out, _record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    after = inherited(repo)["`mod.py#helper`"]
    assert after.split(chr(0x2014))[0] == before.split(chr(0x2014))[0], (
        f"the two sides name different rows of one record: {before!r} then {after!r}"
    )
    assert after == f"round 1's 🟢 {chr(0x2014)} verified", after


# --- the second cause of an empty fill: the section lost its rows ------------
#
# #405. `filled == 0` was answered with unconditional silence, and it has two
# causes: the re-review round above, and a `## Inherited coordinates` table
# edited or truncated after `new` wrote it. The other two refusals both miss
# the second -- a table with no rows is readable, and it inherits no
# coordinate for round N's verdict table to lack.


def strip_inherited_rows(repo, n=2):
    """Delete every body row of round N's `## Inherited coordinates`, leaving
    the heading, the header and the separator. Returns what was deleted."""
    path = repo / ROUNDS / f"round-{n}.md"
    text = path.read_text(encoding="utf-8")
    head, rest = text.split("## Inherited coordinates", 1)
    body, tail = rest.split("\n## ", 1)
    gone = [ln for ln in body.splitlines() if ln.startswith("| round-")]
    assert gone, f"round-{n}.md has no inherited body row to delete:\n{text}"
    kept = [ln for ln in body.splitlines() if not ln.startswith("| round-")]
    path.write_text(
        head + "## Inherited coordinates" + "\n".join(kept) + "\n## " + tail,
        encoding="utf-8",
    )
    return gone


def test_a_truncated_inherited_table_is_refused_naming_what_it_no_longer_holds(repo):
    """A4. Round 2 generated normally, then every body row of its
    `## Inherited coordinates` deleted. `close --round 1` used to exit 0 and
    say nothing about the reach, so the truncation reached the pull request
    with the `Why` cells gone.

    Red against the unconditional silence: exit 0 and no mention of the
    coordinate. The refusal names the coordinates the table no longer
    accounts for rather than stating a rule, so a reader can tell a
    truncation from a generator that stopped emitting a row.
    """
    a = two_records(repo)
    gone = strip_inherited_rows(repo)
    assert any("`mod.py#helper`" in ln for ln in gone), gone
    commit(repo, "the section truncated by hand")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "the fix")
    before = {
        n: (repo / ROUNDS / f"round-{n}.md").read_text(encoding="utf-8") for n in (1, 2)
    }
    code, out, _record = close(
        repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "`mod.py#helper`" in out, out
    assert "does not account for" in out, out
    # §14: the sentence a person is stopped by. The last clause is what lets a
    # reader tell this state from the re-review round below it, which is the
    # reading the removed refusal got wrong and the reason it was removed.
    assert "regenerate the section, or put the rows back" in out, out
    assert "already claimed is NOT this state" in out, out
    assert "no cell was written" in out, out
    for n, text in before.items():
        assert (repo / ROUNDS / f"round-{n}.md").read_text(encoding="utf-8") == text, (
            f"round-{n}.md was written under a refusal"
        )


def test_a_section_that_accounts_for_the_coordinates_under_an_earlier_round_is_silent(
    repo,
):
    """A3's mechanism, stated as the accounting rather than as the count. The
    round-3 section of the re-review case names no `round-2` row and still
    holds round 2's one coordinate, under `round-1`. That is what the
    accounting reads, and it is why the narrowing does not reach the shape
    the silence exists for.
    """
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=OPEN_1))
    assert code == 0, out
    a1 = commit(repo, "round 1")
    write(repo, "mod.py", MOD_CHANGED)
    b1 = commit(repo, "round 1's fix")
    code, out, _ = close(
        repo, 1, fix_table(f"| 1 | fixed | {b1[:7]} |\n"), f"{a1}..{b1}"
    )
    assert "no cell was written" not in out, out
    commit(repo, "round 1 closed")
    code, out, _ = generate(
        repo,
        n=2,
        report_text=report(
            verdicts="| 🟡 1 | helper still drops b | `mod.py#helper` | open | read |\n"
        ),
    )
    assert code in (0, 1), out
    commit(repo, "round 2")
    code, out, _ = generate(
        repo,
        n=3,
        report_text=report(
            verdicts="| 🟡 1 | a third look | `mod.py:5` | open | read |\n"
        ),
    )
    assert code in (0, 1), out
    a = commit(repo, "round 3")
    third = read(repo / ROUNDS / "round-3.md")
    rows = rows_of(third, "## Inherited coordinates")[2:]
    assert "round-2" not in "".join(rows), "the fixture is not the state this is about"
    assert any("`mod.py#helper`" in ln for ln in rows), (
        "round 2's coordinate has to be in the section under round-1, or the "
        f"accounting is not what this case exercises:\n{third}"
    )
    write(repo, "mod.py", MOD_CHANGED + "\n\ndef extra():\n    return 1\n")
    b = commit(repo, "round 2's fix")
    code, out, _ = close(
        repo, 2, fix_table("| 1 | answered | grounds |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "does not account for" not in out, out
    assert "no cell was written" not in out, out


# --- the stray period the cut leaves behind, at both sites -------------------
#
# #414. `chain.SEPARATORS` is six characters wide and holds no period, so a span
# cut out of a cell that opens `` `6233b769`. `` leaves the stop behind.
# Nine cells were repaired BY HAND once and the next record the generator wrote
# carried the rendering again -- §12 as a measurement rather than a rule.


def test_a_fix_note_carries_no_stray_period(repo):
    """A6. The third cell opens with the commit's own code span and a full
    stop. The rendered Grounds cell has to read `fixed at <sha> — <note>`
    with one separator between the dash and the note.

    The whole cell is asserted rather than the absence of a period, so the
    case cannot pass on a cell the fixture failed to build. Red against the
    un-widened strip: `fixed at <sha> — . <note>`.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    _code, out, record = close(
        repo,
        1,
        fix_table(f"| 1 | fixed | `{b[:7]}`. `helper` takes b now |\n"),
        f"{a}..{b}",
    )
    assert "bare integer" not in out, out
    (one,) = verdict_cells(record)
    assert one[4] == f"fixed at {b[:7]} \N{EM DASH} `helper` takes b now; executed", (
        one,
        out,
    )


def test_a_deferred_note_carries_no_stray_period(repo):
    """The second member of the same class, and the one #414's report did not
    name. `rest = third[len(home):]` is the same shape as the commit span's
    cut — a span the generator chose, taken off the front of a cell somebody
    wrote — so `| 1 | deferred #309 | #309. the parity arm … |` rendered
    `#309 — . the parity arm …`.

    Red against the un-widened strip at that line, which the fix-table note's
    own widening does not reach.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "README.md", "# untouched\n")
    b = commit(repo, "nothing")
    code, out, record = close(
        repo,
        1,
        fix_table("| 1 | deferred #309 | #309. the parity arm is out of scope |\n"),
        f"{a}..{b}",
    )
    assert code == 0, out
    (one,) = verdict_cells(record)
    assert one[4] == ("#309 \N{EM DASH} the parity arm is out of scope; executed"), (
        one,
        out,
    )


def test_the_stray_period_repair_did_not_widen_the_shared_separators():
    """#414's chosen direction, held where the empty-span repair's is. Five
    readers share `chain.SEPARATORS`: a period in it would be stripped from a
    `deferred` home, from `chain_check`'s own cell readers and from a
    `nobody — <why>` reason, where a trailing period is part of a sentence
    rather than decoration. The widening is at the two call sites that cut a
    span out of a cell, and this is what says it stayed there.
    """
    generator = generator_module()
    assert "." not in generator.chain.SEPARATORS, (
        "the period moved into the shared constant the call sites reserve"
    )
    body = open(generator.__file__, encoding="utf-8").read()
    body = body.split("def fix_table", 1)[1].split("\ndef ", 1)[0]
    assert body.count('chain.SEPARATORS + "."') == 2, (
        "the two cuts that take a span off a cell are what carry the period"
    )


# --- re-closing a corrected record does not double its grounds (#427) --------


def reopen_verdicts(repo, n):
    """#427's own path: the `Verdict` cells go back to `open` and `Grounds` is
    left exactly as `close` wrote it.

    That is the repair a person makes after a stalled fix pass writes its own
    verdicts into a record where the reviewer's report still says `open` —
    restore the verdicts, re-run `close`, let the generator write them from
    the fix table. The `Grounds` cell is not restored because nothing tells
    the repair's author that `close` prefixes it.
    """
    generator = generator_module()
    path = repo / ROUNDS / f"round-{n}.md"
    text = path.read_text(encoding="utf-8")
    head, marker, rest = text.partition(generator.VERDICTS)
    assert marker, f"no {generator.VERDICTS} heading in the record"
    out, seen, done = [], 0, False
    for line in rest.splitlines(keepends=True):
        # The verdict table only. The record carries later tables of its own
        # and a walk that runs on reaches them.
        if line.startswith("##"):
            done = True
        if (
            not done
            and line.lstrip().startswith("|")
            and set(line.strip()) - set("|-: ")
        ):
            seen += 1
            if seen > 1:
                cells = line.split("|")
                assert len(cells) > generator.VERDICT_COL + 1, line
                cells[generator.VERDICT_COL + 1] = f" {generator.OPEN_WORD} "
                line = "|".join(cells)
        out.append(line)
    assert seen > 1, "no verdict rows were reopened"
    path.write_text(head + marker + "".join(out), encoding="utf-8")
    return path


@pytest.mark.parametrize("word", ["fixed", "answered", "deferred"])
def test_re_closing_a_half_restored_record_is_refused_for_every_word(repo, word):
    """#427 names `fixed` and all three words reach the join (§12).

    `close` prefixes the `Grounds` cell rather than replacing it, on purpose:
    the reviewer's sentence and the fix pass's are by different authors. What
    it did not check is whether its OWN prefix is already there — so closing
    the same finding twice wrote the grounds twice, the record still parsed,
    `chain_check` was silent, and the only way it was caught was reading the
    committed file against two earlier commits.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    third = {
        "fixed": f"{b[:7]} — widened, b defaults to None",
        "answered": "b is never passed by any caller",
        "deferred": "#427",
    }[word]
    verdict = "deferred #427" if word == "deferred" else word
    table = fix_table(f"| 1 | {verdict} | {third} |\n")
    # 0 or 1: a green `close` still exits 1 on the chain-check notice about
    # `Pass` beside `Fixes checked by: nobody`, which is unrelated and is what
    # #427's own reproduction reported. The refusal below is exit 2.
    code, out, _first = close(repo, 1, table, f"{a}..{b}")
    assert code in (0, 1), out
    reopen_verdicts(repo, 1)
    before = (repo / ROUNDS / "round-1.md").read_text(encoding="utf-8")

    code, out, after = close(repo, 1, table, f"{a}..{b}")
    assert code == 2, out
    # §14: what is wrong, and what to do instead. Both halves, because the
    # second is the one that survives a reword badly.
    assert "already carries a close prefix" in out, out
    assert "finding 1" in out, out
    assert "Restore the `Grounds` cell" in out, out
    # Nothing reached disk. `write_record` runs after the loop this raises in,
    # so a refusal here leaves the half-restored record exactly as it stood —
    # which is what makes the message's instruction possible to follow.
    assert after == before, "the refusal wrote to the record anyway"


def test_the_close_prefix_is_caught_when_the_commit_changed(repo):
    """The arm the same-table comparison cannot reach.

    A fix pass that amends its commit between two closes writes a DIFFERENT
    prefix the second time, so the cell no longer begins with the text this
    run would write and a text comparison sees nothing. The cell still carries
    a close prefix, which is the thing that must not be doubled — so the guard
    reads the SHAPE as well, and that shape is the one `chain_check` reads
    when it names a record already carrying two.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, _ = close(repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}")
    assert code in (0, 1), out
    write(repo, "README.md", "# amended\n")
    c = commit(repo, "the fix, amended")
    reopen_verdicts(repo, 1)
    before = (repo / ROUNDS / "round-1.md").read_text(encoding="utf-8")

    code, out, after = close(
        repo, 1, fix_table(f"| 1 | fixed | {c[:7]} |\n"), f"{a}..{c}"
    )
    assert code == 2, out
    assert "already carries a close prefix" in out, out
    assert after == before, "the refusal wrote to the record anyway"


def test_the_documented_repair_still_closes(repo):
    """The direction that has to stay OPEN, and `questions.md` Q4's risk.

    Correcting a record and re-closing it is the documented way out of a
    record written wrong, and #427 refuses a fix that forbids it. So the
    guard must fire on the HALF-restored record and not on the fully restored
    one: restore the `Grounds` cell to the reviewer's sentence as well, and
    `close` writes the row exactly as it did the first time.
    """
    a = round_one(repo, verdicts=OPEN_1)
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    table = fix_table(f"| 1 | fixed | {b[:7]} |\n")
    code, out, first = close(repo, 1, table, f"{a}..{b}")
    assert code in (0, 1), out
    (one,) = verdict_cells(first)
    assert one[4] == f"fixed at {b[:7]}; executed", one

    # The WHOLE repair: the verdict back to `open` and the grounds back to
    # what the reviewer wrote.
    path = reopen_verdicts(repo, 1)
    text = path.read_text(encoding="utf-8")
    assert f"fixed at {b[:7]}; executed" in text
    path.write_text(
        text.replace(f"fixed at {b[:7]}; executed", "executed"), encoding="utf-8"
    )

    code, out, again = close(repo, 1, table, f"{a}..{b}")
    assert code in (0, 1), out
    (one,) = verdict_cells(again)
    assert one[4] == f"fixed at {b[:7]}; executed", (one, out)


def test_the_generator_and_the_checker_spell_the_close_prefix_once(repo):
    """Two parties read this prefix now, so there is one spelling of it.

    The generator writes it and `chain_check` names a cell carrying two. A
    second literal in either file is how a writer and a reader drift apart
    about what they are both looking at.
    """
    generator, checker = generator_module(), check_module()
    assert generator.FIXED_AT == checker.CLOSE_PREFIX, (
        "the generator's prefix is no longer the checker's constant"
    )
    # Identity is not available: the two modules are loaded separately here, so
    # equal strings are not the same object. What the rule is actually about is
    # a SECOND literal, so that is what is counted -- the generator's constant
    # is an alias now, and the phrase may stand in its prose and nowhere else.
    body = open(generator.__file__, encoding="utf-8").read()
    literals = re.findall('"' + checker.CLOSE_PREFIX + '"', body)
    assert not literals, "the generator spells the close prefix itself again: " + str(
        literals
    )
    assert checker.CLOSE_PREFIX_RE.match(f"{checker.CLOSE_PREFIX} 64f36eee")
    assert not checker.CLOSE_PREFIX_RE.match("executed, and the caller agrees")
