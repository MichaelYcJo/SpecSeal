"""A finding id is a bare integer, and the refusal says so and quotes the row.

#227, observed on 0.8.3. A reviewer numbered a round's findings `R2-1` …
`R2-8` — the round in the id, so a finding stays unambiguous when three
rounds are read side by side. `NUMBER_RE.search` takes the FIRST digit run,
so every one of the eight collapsed toward `2` and both `new` and `close`
refused with

    round-record: the fix table has two rows for finding 2
    round-record: the record has two verdict rows numbered 2

which reports a duplicate that is not visibly one: the table holds a single
`R2-1` and a single `R2-2`. The first read is that the table is malformed,
not that the ids are. And with eight rows and no coordinates, finding the
pair is a manual scan.

The second-order cost is why it is worth a checker rather than a convention.
The reviewer and the fixer are separate agents, and the fixer copies the
reviewer's numbering into the fix table — so a numbering the reviewer chose
surfaces as a refusal at the orchestrator, one hop from either agent that
could have avoided it.

**The corpus is what chose the refusal over accepting a prefix.** Every
committed `round-N.md` in this repository was run through the module's own
`table_body` path under both rules before the format was fixed: of 130
records that parse, 82 pass under both, 46 already refuse today, and 2 pass
today only by miscounting — `r3 🟡 2` keys as finding **3**, out of the `3`
in `r3`, and `🟢 round 2's finding (🟡 4)` keys as **2** where the cell names
4. `test_the_committed_records_only_lose_a_miscount` is that measurement,
kept as a case rather than as a paragraph.

Every case here was seen red against the unfixed generator: the refusals
assert on the format the message has to name, which the old duplicate
message does not carry, and the two-row refusals assert on both cells, of
which the old message quotes neither.
"""

import os
import re
import shutil
import subprocess
import time

import pytest
from test_the_fixes_close_the_record import (
    MOD_CHANGED,
    OPEN_1,
    _build,
    close,
    fix_table,
    round_one,
)
from test_the_record_is_generated import (
    ROOT,
    ROUNDS,
    commit,
    declared,
    generate,
    generator_module,
    reader_module,
    report,
    write,
)


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("bare-id-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def a_fix(repo):
    """A range whose end changes two signatures, so `close` has work to do."""
    write(repo, "mod.py", MOD_CHANGED)
    return commit(repo, "fix")


def hand_edited(repo, before, after):
    """Round 1's record, its `#` cell replaced the way a hand-edit would.

    `new` refuses a malformed id at the report now, so a hand-edit is the one
    remaining way one reaches `close` — and `close` still has to refuse it.
    The two halves are the same rule read at two moments, which is what this
    whole work item is about: a record the generator did not write is exactly
    what the second reading exists to hold.
    """
    path = repo / ROUNDS / "round-1.md"
    text = path.read_text(encoding="utf-8")
    assert before in text, f"the record does not carry {before!r}"
    path.write_text(text.replace(before, after), encoding="utf-8")


def a_report(repo, verdicts):
    """`new` over a report carrying `verdicts`; returns (code, output)."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=verdicts))
    return code, out


# --- the id the reviewer picks ----------------------------------------------


def test_a_round_prefixed_verdict_id_is_refused_naming_the_format(repo):
    """#227's own numbering, in the verdict table. It is refused at `new`
    now — where the reviewer who chose it is — rather than two commands
    later at `close`."""
    code, out = a_report(
        repo,
        "| 🔴 R2-1 | helper drops b | `f.py:1` | open | executed |\n"
        "| 🟡 R2-2 | only_tested ignores rest | `f.py:1` | open | read |\n",
    )
    assert code == 2, out
    # The format, named. The old message named a duplicate instead.
    assert "bare integer" in out, out
    # The rows, quoted. The old message quoted neither.
    assert "R2-1" in out and "R2-2" in out, out
    assert "two verdict rows" not in out, "the duplicate that was not one"


def test_a_hand_edited_record_still_meets_the_rule_at_close(repo):
    """`new` refusing does not retire the reading at `close`. A record is a
    file somebody can open and edit, and `close` keys every row of it."""
    a = round_one(repo, verdicts=OPEN_1)
    hand_edited(repo, "| 🔴 1 |", "| 🔴 R2-1 |")
    b = a_fix(repo)
    code, out, _ = close(repo, 1, fix_table(f"| 1 | fixed | {b[:7]} |\n"), f"{a}..{b}")
    assert code == 2, out
    assert "bare integer" in out, out
    assert "R2-1" in out, out


def test_a_round_prefixed_fix_table_id_is_refused_naming_the_format(repo):
    """The fixer copies the reviewer's numbering, so the same id arrives one
    file over. The refusal has to name the format there too — that table is
    what the smith writes and what `close` reads first."""
    a = round_one(repo, verdicts=OPEN_1)
    b = a_fix(repo)
    code, out, _ = close(
        repo, 1, fix_table(f"| R2-1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "bare integer" in out, out
    assert "R2-1" in out, out
    assert "two rows for finding" not in out, out


@pytest.mark.parametrize("carries_it", ["record", "fixes"])
def test_the_refusal_names_the_table_it_read(repo, carries_it):
    """A message that names the format and not the file sends the reader to
    the wrong one of the two tables — they are written by different agents,
    and the fixer's copy is refused for what the reviewer chose."""
    generator = generator_module()
    on_record = carries_it == "record"
    if on_record:
        code, out = a_report(repo, "| 🔴 1a | one | `f.py:1` | open | read |\n")
    else:
        a = round_one(repo, verdicts=OPEN_1)
        b = a_fix(repo)
        code, out, _ = close(
            repo, 1, fix_table(f"| 1a | fixed | {b[:7]} |\n"), f"{a}..{b}"
        )
    want = generator.RECORD_LABEL if on_record else generator.FIX_TABLE_LABEL
    other = generator.FIX_TABLE_LABEL if on_record else generator.RECORD_LABEL
    assert code == 2, out
    assert want in out, out
    assert other not in out, out


@pytest.mark.parametrize(
    "bad", ["R2-1", "1-1", "1b", "A2", "N1", "round 2's finding (🟡 4)"]
)
def test_every_shape_the_corpus_holds_is_refused_by_name(repo, bad):
    """The shapes committed records carry in that column that were REACHING
    for an id and missed. Each is refused, and each refusal quotes the cell —
    with eight rows and no coordinate, the ticket's complaint was the scan.

    `A` and `carried` left this list when #321 landed: they carry no digit and
    no severity that owes an answer, so nothing asks them for a closure. The
    case below is their half. A bare `A` is admitted only because it carries
    no marker — `🔴 A` and `🟡 A` are refused, which is the 44-row shape the
    corpus actually holds.
    """
    a = round_one(repo, verdicts=OPEN_1)
    b = a_fix(repo)
    code, out, _ = close(
        repo, 1, fix_table(f"| {bad} | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "bare integer" in out, out
    # The whole row, not just the cell — a bare `A` would match anything.
    assert f"| {bad} | fixed |" in out, out


@pytest.mark.parametrize("none", ["A", "carried", "✅", "🟢 fix-surface", "—"])
def test_every_no_digit_shape_the_corpus_holds_is_admitted(repo, none):
    """The other half of the corpus, and the one #321 is about. A cell with no
    digit in it was never reaching for an id, so refusing it asked a reviewer
    to number a row that commissions nothing — and the record then reads as a
    round with twice the findings it had."""
    a = round_one(
        repo, verdicts=OPEN_1 + f"| {none} | verified | `mod.py` | verified | read |\n"
    )
    b = a_fix(repo)
    code, out, record = close(
        repo, 1, fix_table("| 1 | answered | b is never passed |\n"), f"{a}..{b}"
    )
    assert code == 0, out
    assert "bare integer" not in out, out
    assert f"| {none} | verified |" in record, record


@pytest.mark.parametrize("owed", ["🔴 A", "🟡 A", "🔴", "🟡 fix-surface"])
def test_a_no_digit_cell_whose_severity_owes_an_answer_is_refused(repo, owed):
    """Round 1's 🔴 1. The three-way read admitted a row on the strength of its
    `#` cell alone, and never consulted the cell that says whether anything is
    owed. So `| 🟡 A | … | open | … |` came through `new` at exit 0, silently,
    and the record was written with `- [x] Pass` beside an open finding in its
    own verdict table — the two halves of one generator disagreeing about one
    row, reproduced inside this work item's own fix.

    Nothing downstream caught it: `chain_check.open_blocking` reads only rows
    carrying 🔴. The 🔴 shape did refuse, but on `new`'s own check of the
    record it had just written, pointing at the Verdict column where nothing
    is wrong.

    The severity marker is what already means *somebody owes this an answer* —
    🔴 blocks merge and 🟡 needs grounds — so it is what this rule reads. A
    vocabulary test of the verdict cannot serve in its place: a confirmation row
    reads `verified`, which is in no vocabulary and therefore OPEN, so it would
    trade one refusal for another. Reading the single word `open` is a separate
    arm and composes with this one —
    `test_a_row_that_commissions_nothing_cannot_read_open` below.
    """
    code, out = a_report(repo, f"| {owed} | one | `f.py:1` | open | read |\n")
    assert code == 2, out
    assert "owes an answer" in out, out
    assert owed in out, out
    assert "- [x] Pass" not in out, "a record was written"


def test_an_empty_hash_cell_is_refused(repo):
    """The other half of 🔴 1's reproduction, which the finding's own
    paste-ready fix does not reach (§12 — the fix is owed to the class).

    A blank `#` cell carries no severity, so a rule reading the marker admits
    it; and the round measured `| | … | open | read |` coming through `new` at
    exit 0 with `Pass` ticked, exactly as the 🟡 did. A blank is not `carried`
    or `🟢 fix-surface` — it says nothing at all, which is what a reviewer who
    forgot the id writes.

    Free against the corpus: of the 51 no-digit cells in the committed
    records, **zero** are blank, so no record that reads correctly today is
    refused by this.
    """
    code, out = a_report(repo, "|  | one | `f.py:1` | open | read |\n")
    assert code == 2, out
    assert "bare integer" in out or "owes an answer" in out, out


@pytest.mark.parametrize(
    "cell",
    [
        "\N{LARGE GREEN CIRCLE} fix-surface",
        "carried",
        "\N{WHITE LARGE SQUARE}",
        "\N{BLACK QUESTION MARK ORNAMENT}",
        "A",
        "\N{EM DASH}",
    ],
)
def test_a_row_that_commissions_nothing_cannot_read_open(repo, cell):
    """Round 2's 🟡 7, and round 1's 🔴 1 one cell over.

    The severity arm reads the `#` cell, and the row says it is open in the
    column beside it. So every shape the rule admits came through `new` at exit
    0, silently, with `Pass` ticked over a row its own table calls open — the
    same record asserting a review passed while its own verdict table says
    otherwise. Three of these six carry no severity marker at all, so the
    residual the documents stated did not describe them even as prose.

    **This composes with the marker check rather than replacing it.** The
    grounds for not reading the verdict were that a confirmation reads
    `verified`, which is in no vocabulary and therefore OPEN — true of
    replacing the marker check, false of composing with it. What is read here
    is the literal word `open`, which is unambiguous.

    Free against the corpus: of the 25 admitted no-digit cells in the committed
    records, the verdicts are `fixed`, `answered`, `truthful`, `record only`
    and their kin — not one reads `open`.
    """
    code, out = a_report(repo, f"| {cell} | one | `f.py:1` | open | read |\n")
    assert code == 2, out
    # The Verdict column named, not just the word `open` — the refusal this
    # replaced already said "ticked over an open finding", so asserting the
    # bare word would have passed against the defect.
    assert "`Verdict` cell reads `open`" in out, out
    assert cell in out, out
    assert "- [x] Pass" not in out, "a record was written"


def test_a_row_failing_both_arms_is_named_once(repo):
    """`| 🔴 A | … | open | … |` fails the severity arm and the verdict arm at
    once. Both append to the same list, so without a guard the row is quoted
    twice and the message counts two rows where the table holds one — which is
    the #303 complaint (a message you cannot trust the shape of) arriving from
    the fix for it. Found by mutation: dropping the guard left every other case
    in this module green.
    """
    code, out = a_report(repo, "| 🔴 A | one | `f.py:1` | open | read |\n")
    assert code == 2, out
    assert "has 1 row " in out, out
    assert out.count("| 🔴 A | one |") == 1, out


def test_a_numbered_short_row_is_refused_rather_than_raising(repo):
    """Round 3's 🔴 1, and the member round 2's bounds guard did not reach.

    A digit in the `#` cell KEYS the row, so it passes `verdict_rows` and every
    caller then indexes `VERDICT_COL` on it: `new` at the `words` comprehension,
    `close` at `open_now`, at the `already` message and at the write pass. Round
    2's guard sits inside `verdict_rows` and covers only the row that is not
    keyed.

    Worse than a defect, this is a regression: on `release/v0.11.4` `new`
    computed `Pass` through `verdict_words`, which raises `a verdict row has N
    cells` — a refusal naming the row. Round 2's repair replaced that path and
    carried no width check with it.

    `fix_table` has refused the same shape since it was written, and zero of the
    committed verdict rows are short, so matching its shape costs nothing.
    """
    code, out = a_report(repo, "| 1 | one |\n")
    assert code == 2, out
    assert "Traceback" not in out and "IndexError" not in out, out
    assert "2 cells" in out and "no `Verdict` cell" in out, out
    assert "- [x] Pass" not in out, "a record was written"


def test_a_row_missing_only_its_grounds_is_still_written_short(repo):
    """The bound is `VERDICT_COL`, not the header width, and this is why.

    Round 3's paste-ready code for finding 1 refused any row narrower than the
    header. That reaches a four-cell row — one with a Verdict cell and no
    Grounds — which nothing indexes past and which
    `test_a_short_row_with_a_comment_pipe_is_not_padded_into_a_full_one`
    deliberately admits, so the record shows the column the reviewer left out
    rather than inventing one. The wider test turns that case red.

    Refusing exactly what crashes leaves the older decision standing, and the
    corpus is silent either way: zero committed verdict rows are short at all.
    """
    code, out = a_report(repo, "| 1 | one | `f.py:1` | open |\n")
    assert "Traceback" not in out and "IndexError" not in out, out
    assert "no `Verdict` cell" not in out, out
    # The row IS refused, by the verdict arm — it reads `open` with a `#` cell
    # that keys it, so `Pass` is decided on it. What matters here is which
    # refusal it meets: not the width one.
    assert code in (0, 2), out


@pytest.mark.parametrize(
    "verdict",
    ["open", "open — deferred", "open, comment only", "**open** — still"],
)
def test_every_spelling_of_open_the_records_hold_is_refused(repo, verdict):
    """Round 3's 🟡 2. `agents/warden.md`, `templates/sdd-round.md` and
    `skills/code-review/SKILL.md` all say a row whose Verdict cell *reads*
    `open` is refused, and the arm tested equality.

    Measured over every committed record: 127 verdict cells begin `open` and
    **9 of them continue** — `open — deferred`, `open, comment only` and seven
    more — so the equality reached 118 of 127 while the documents described all
    of them. A head match ended by `chain.SEPARATORS`, the boundary
    `verdict_of` already uses for its own vocabulary, reaches all 127 and newly
    refuses **0** of the 25 admitted no-digit rows.

    The grounds for not running a VOCABULARY test are untouched and were
    re-measured: 15 of those 25 carry a verdict outside `CLOSED_WORDS`, so
    *anything not closed* would refuse them. What never followed from those
    grounds is equality.
    """
    code, out = a_report(repo, f"| carried | one | `f.py:1` | {verdict} | read |\n")
    assert code == 2, out
    assert "`Verdict` cell reads `open`" in out, out


@pytest.mark.parametrize("verdict", ["opened in round 2", "openly carried"])
def test_a_word_that_merely_begins_with_open_is_not_the_open_verdict(repo, verdict):
    """The boundary is what makes `says_open` match a WORD rather than a
    prefix of one — the same distinction `verdict_of` states for its own
    vocabulary, where without it `not a defect` would swallow `not a defective
    reading`.

    Found by mutation: dropping the separator test left every other case in
    this module green, because no case fed it a longer word.
    """
    _code, out = a_report(repo, f"| carried | one | `f.py:1` | {verdict} | read |\n")
    assert "`Verdict` cell reads `open`" not in out, out


def test_a_row_too_short_to_have_a_verdict_cell_does_not_crash(repo):
    """The guard finding 7's repair needs. `table_body` returns as many cells
    as the row has, and `verdict_rows` only checks that the `#` cell exists —
    so reading the Verdict column off a two-cell row indexes past the end.

    `Loses a record or crashes` is its own gate, so a repair that trades a
    silent pass for a traceback is not a repair.
    """
    code, out = a_report(repo, "| carried | one |\n")
    assert "Traceback" not in out, out
    assert "IndexError" not in out, out
    # The exit code is not the assertion: a two-cell row is malformed for
    # other reasons and `run_check` may refuse the record it produces. What
    # this pins is that the generator refuses or accepts it deliberately
    # rather than dying inside the verdict read.
    assert code != 3, out


@pytest.mark.parametrize("marker", ["🔴", "🟡", "🟢", "⬜", "❓", "✅"])
def test_a_severity_marker_still_leads_the_cell(repo, marker):
    """Every marker the corpus puts in front of the number, still read. The
    rule is about what follows the marker, and a rule that took the marker
    with it would refuse every record ever written."""
    a = round_one(
        repo, verdicts=f"| {marker} 1 | one | `mod.py#helper` | open | read |\n"
    )
    b = a_fix(repo)
    code, out, record = close(
        repo, 1, fix_table(f"| {marker} 1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert "bare integer" not in out, out
    assert f"**fixed** `{b[:7]}`" in record, (code, out)


@pytest.mark.parametrize("wrapped", ["**1**", "`1`", "*1*", "**🔴 1**"])
def test_an_emphasised_id_is_the_same_id(repo, wrapped):
    """Markdown emphasis around the id is emphasis, not part of the id.

    A record already writes `**fixed**` in the next column, so a session
    bolding the `#` cell to match is the obvious thing to do — and a rule
    that read the asterisks as *not digits* would refuse it. Found by
    mutation: dropping the strip left every other case green.
    """
    a = round_one(
        repo, verdicts=f"| {wrapped} | one | `mod.py#helper` | open | read |\n"
    )
    b = a_fix(repo)
    _, out, record = close(
        repo, 1, fix_table(f"| {wrapped} | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert "bare integer" not in out, out
    assert f"**fixed** `{b[:7]}`" in record, out


def test_a_number_with_no_marker_at_all_is_read(repo):
    a = round_one(repo, verdicts="| 12 | one | `mod.py#helper` | open | read |\n")
    b = a_fix(repo)
    _, out, record = close(
        repo, 1, fix_table(f"| 12 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert f"**fixed** `{b[:7]}`" in record, out


def test_a_long_punctuation_cell_is_refused_without_hanging():
    """The refusal is the deliverable, so it has to arrive.

    Round 1's finding 3. `[^\\w\\s]+` inside the `*` group let a run of
    punctuation be split into groups in exponentially many ways, and a cell
    ending in a non-digit made the engine try all of them before failing:
    0.18 s at 22 characters, 2.9 s at 26, 11.4 s at 28, doubling per
    character. What a person saw was `close` or `new` producing nothing and
    never returning — worse than the confusing message #227 opened for, on
    the tool that gates every record.
    """
    generator = generator_module()
    start = time.monotonic()
    assert generator.FINDING_ID_RE.match("!" * 4000 + "x") is None
    assert time.monotonic() - start < 1.0, "the pattern is backtracking"


# --- the duplicate that really is one ---------------------------------------


def test_a_duplicate_verdict_id_quotes_both_rows(repo):
    """When two rows really do carry the same id, the refusal names both.
    Naming one is the manual scan the ticket paid for."""
    code, out = a_report(
        repo,
        "| 🔴 3 | the first three | `f.py:1` | open | executed |\n"
        "| 🟡 3 | the second three | `f.py:1` | open | read |\n",
    )
    assert code == 2, out
    assert "the first three" in out and "the second three" in out, out


def test_a_duplicate_fix_row_quotes_both_rows(repo):
    a = round_one(repo, verdicts=OPEN_1)
    b = a_fix(repo)
    code, out, _ = close(
        repo,
        1,
        fix_table(f"| 1 | fixed | {b[:7]} |\n", "| 1 | answered | said twice |\n"),
        f"{a}..{b}",
    )
    assert code == 2, out
    assert out.count("| 1 |") >= 2 or "said twice" in out, out


# --- the corpus this rule was measured against ------------------------------


def old_key(cell):
    """What the unfixed generator read out of a `#` cell: the FIRST digit run."""
    m = re.search(r"\d+", cell)
    return int(m.group()) if m else None


def last_run(cell):
    """What a person reads out of the same cell: the LAST digit run."""
    runs = re.findall(r"\d+", cell)
    return int(runs[-1]) if runs else None


def committed_records():
    """`seal/specs/*/rounds/round-*.md` git carries — the RECORDS among them.

    `round-*.md` is git's pathspec and git has no way to say "and then a
    number", so it also returns the three files the review chain writes beside
    a record, one per round: `round-N-report.md`, `round-N-asked.md`,
    `round-N-fixes.md`. Measured at a50431b: 204 paths, of which 151 are
    records and **53 are not** — 20 reports, 20 asked, 13 fix tables. Twenty
    of those 53 parse as a verdict table under this module's own header, so
    the corpus below was judging twenty reports as records; the other 33 fell
    out as unparseable and hid the defect rather than reporting it.

    A record is selected by name (`docs/review-handoff-protocol.md` §Layout),
    and `routing.round_number` is the one place that rule lives. This was the
    third reader in the tree to take directory membership for record-ness,
    and the quietest: the other two raised `TypeError` on sorting two `None`s,
    while this one said nothing at all (#228, round 1 🟡 1).
    """
    generator = generator_module()
    routing = generator.load(generator.chain.ROUTING, "routing_for_the_id_corpus")
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "seal/specs/*/rounds/round-*.md"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return [p for p in out if routing.round_number(os.path.basename(p)) is not None]


def test_the_corpus_is_records_only():
    """Not one of the three siblings `rounds/` holds reaches the corpus.

    The assertion below measures a population, so what is IN that population
    decides what it says. A report parses as a verdict table — it carries the
    same `## Verdicts` heading under the same header, because the record is
    written from it — so a report in the corpus is not an inert extra path,
    it is a counted member with cells of its own. Twenty of them were counted
    at a50431b.

    Named by suffix rather than by asking `round_number` again: this case has
    to fail when the filter is removed, and re-running the filter's own rule
    over its own output cannot.
    """
    paths = committed_records()
    assert paths, "the corpus is empty; the filter takes everything"
    strays = [
        p
        for p in paths
        if any(
            os.path.basename(p).endswith(t)
            for t in ("-report.md", "-asked.md", "-fixes.md")
        )
    ]
    assert not strays, (
        f"{len(strays)} of {len(paths)} corpus paths are not records: "
        f"{strays[:3]}. `rounds/` holds three files per round beside the "
        "record, and a record is selected by name, never by directory "
        "membership (`docs/review-handoff-protocol.md` §Layout)"
    )


def id_cells(generator, reader, path):
    """The `#` cells of one record's verdict table, or None if it does not parse."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        body = generator.table_body(
            reader,
            reader.readable(text),
            generator.VERDICTS,
            generator.VERDICT_HEADER,
            True,
        )
        return [reader.visible(cells[0]).strip() for _i, cells in body]
    except Exception:
        return None


def test_the_committed_records_only_lose_a_miscount():
    """No record that the old rule reads CORRECTLY is refused by the new one.

    The invariant rather than the count, because the count moves as records
    land. A record the old rule accepts and the new one refuses has to be one
    whose accepted key is not the number its own cell names — the first digit
    run and the last one disagree. That is the whole of what this branch
    takes away, and it takes away a wrong answer.
    """
    generator, reader = generator_module(), reader_module()
    paths = committed_records()
    assert len(paths) > 100, f"the corpus is {len(paths)} records; the case is vacuous"
    parsed = teeth = 0
    for path in paths:
        cells = id_cells(generator, reader, f"{ROOT}/{path}")
        if cells is None:
            continue
        parsed += 1
        old, seen = {}, None
        for c in cells:
            k = old_key(c)
            if k is None or k in old:
                seen = "refused"
                break
            old[k] = c
        refused_now = [c for c in cells if not generator.FINDING_ID_RE.match(c)]
        if refused_now:
            teeth += 1
        if seen == "refused" or not refused_now:
            continue
        for c in refused_now:
            assert old_key(c) != last_run(c), (
                f"{path}: `{c}` reads correctly today and the new rule refuses it"
            )
    assert parsed > 100, parsed
    assert teeth, "the rule refuses nothing in the corpus, so it has no teeth"


def test_the_rule_is_one_constant_both_tables_read():
    """One pattern, so the two tables cannot drift into different formats.
    The reviewer writes one and the fixer copies it; a rule that held only on
    the record would refuse the copy for a reason the original passed."""
    generator = generator_module()
    source = open(generator.__file__, encoding="utf-8").read()
    assert source.count("def finding_number") == 1
    assert source.count("FINDING_ID_RE.match") == 1, (
        "the pattern is matched in `finding_number` and nowhere else — a "
        "second match site is where the two tables drift apart"
    )
    body = source.split("def finding_number", 1)[1].split("\ndef ", 1)[0]
    assert "FINDING_ID_RE.match" in body, "the one match site is not that one"
    assert source.count("finding_number(") == 3, (
        "one definition and the two calls — `fix_table` and `verdict_rows`"
    )
    assert "NUMBER_RE" not in source, (
        "the first-digit-run search is what #227 reported; it has no callers left"
    )


# --- a row that commissions nothing (#321, #341, #353) ----------------------

# Six shapes with no digit and no severity that owes an answer, so none of
# them commissions anything: a confirmation the round verified, a fix-surface
# re-derivation, an earlier round's closure carried forward, a bare dash, and
# a scope marker. Measured 2026-09-14 over the 207 committed records that
# parse: 51 rows carry a `#` cell with no digit — but 44 of those are a marker
# and a single letter, which is a finding id in the wrong alphabet and is
# refused. Seven are this shape. `✅` and a bare dash occur zero times in a
# committed record; the 21 bare dashes are in reviewers' REPORTS.
CONFIRMED = (
    "| \N{WHITE HEAVY CHECK MARK} | the pipe escape still renders "
    "| `mod.py#helper` | verified | read |\n"
    "| \N{WHITE HEAVY CHECK MARK} | the reach-back still sets round 1 "
    "| `mod.py#caller` | verified | read |\n"
    "| \N{LARGE GREEN CIRCLE} fix-surface | both rows re-derived | `mod.py` "
    "| verified | executed |\n"
    "| carried | round 1's \N{LARGE YELLOW CIRCLE} 4, not re-opened "
    "| `README.md` | verified | read |\n"
    "| \N{EM DASH} | the corpus count re-measured | `mod.py:5` | verified "
    "| executed |\n"
    "| \N{BLACK QUESTION MARK ORNAMENT} | nothing else was in scope | `mod.py` "
    "| verified | read |\n"
)


def test_six_rows_with_no_id_stand_beside_one_finding_and_commission_nothing(repo):
    """#321's answer 2. A round that verified six things and opened one used
    to have to number all seven, which reads back as a seven-finding round.

    The row is copied, never keyed, and never asked for a closure — so the fix
    table carries one row and `close` exits 0 with the six standing as the
    reviewer wrote them.
    """
    a = round_one(repo, verdicts=OPEN_1 + CONFIRMED)
    b = a_fix(repo)
    code, out, record = close(
        repo,
        1,
        fix_table("| 1 | answered | b is never passed |\n"),
        f"{a}..{b}",
    )
    assert code == 0, out
    assert "left with no row in the fix table" not in out, out
    for line in CONFIRMED.strip().splitlines():
        assert line.strip() in record, (line, record)
    assert "- [x] Pass" in record, out


def test_a_row_with_no_id_does_not_decide_pass(repo):
    """The six rows read `verified`, which is in no vocabulary. Counted as
    verdicts they would each be OPEN and `Pass` could never be ticked — so
    admitting the row and then reading its verdict word would trade one
    refusal for another."""
    a = round_one(repo, verdicts=OPEN_1 + CONFIRMED)
    b = a_fix(repo)
    _, out, record = close(
        repo, 1, fix_table("| 1 | answered | the rest is never passed |\n"), f"{a}..{b}"
    )
    assert "- [x] Pass" in record, out


def test_a_fix_table_row_with_no_id_is_refused(repo):
    """The verdict table admits an id-less row and the fix table cannot: a fix
    row with no id references no finding, and `close` would have nothing to
    apply it to. The two tables are the same rule read in opposite directions
    — one names a row that commissions nothing, the other is the commission."""
    a = round_one(repo, verdicts=OPEN_1)
    b = a_fix(repo)
    code, out, _ = close(
        repo, 1, fix_table(f"| \N{EM DASH} | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "bare integer" in out, out


def test_an_earlier_rounds_number_in_the_hash_cell_is_still_refused(repo):
    """The round and the number belong in the Finding cell, which is prose.
    Put into the `#` cell they are digits, and digits there are an id: `round
    2's 1` keyed as finding **2** under the old reader — colliding with this
    round's own 2 — and is refused by name under the new one. The refusal says
    where the row's own spelling is, which is the half a reviewer meets."""
    code, out = a_report(
        repo,
        "| 🟢 round 2's 1 | the parser row | `f.py:1` | answered | closed in 2 |\n",
    )
    assert code == 2, out
    assert "carries no id at all" in out, out


def test_an_earlier_rounds_closure_does_not_collide_with_this_rounds_findings(repo):
    """#341's body. A round 3 report closing round 2's findings 1 and 2 while
    opening its own 1 and 2 used to produce a duplicate-id refusal out of a
    table holding four distinct rows. The closures carry no id, so nothing
    collides and the four rows are distinguishable in the record."""
    a = round_one(
        repo,
        verdicts=(
            OPEN_1
            + "| \N{LARGE YELLOW CIRCLE} 2 | only_tested ignores rest | `mod.py:5` "
            "| open | read |\n"
            "| \N{LARGE GREEN CIRCLE} | round 2's finding 1, re-read "
            "| `mod.py#helper` | answered | closed in round 2 |\n"
            "| \N{LARGE GREEN CIRCLE} | round 2's finding 2, re-read "
            "| `mod.py#caller` | answered | closed in round 2 |\n"
        ),
    )
    b = a_fix(repo)
    code, out, record = close(
        repo,
        1,
        fix_table(
            "| 1 | answered | b is never passed |\n",
            "| 2 | answered | rest is never passed |\n",
        ),
        f"{a}..{b}",
    )
    assert code == 0, out
    assert "two verdict rows" not in out, out
    assert "round 2's finding 1, re-read" in record, record
    assert "round 2's finding 2, re-read" in record, record


def test_one_refusal_names_every_malformed_row(repo):
    """#303, merged into #321: five offending rows and a message naming one,
    at two round trips per repair. The refusal is the deliverable, so it
    carries the whole set."""

    declared(repo)
    rows = "".join(
        f"| R2-{n} | finding {n} | `f.py:1` | open | read |\n" for n in range(1, 6)
    )
    code, out, _ = generate(repo, report_text=report(verdicts=rows))
    assert code == 2, out
    for n in range(1, 6):
        assert f"R2-{n}" in out, (n, out)
    assert out.count("bare integer") == 1, out


def test_a_malformed_id_is_refused_at_new_where_the_author_is(repo):
    """#321's answer 1, kept for the rows that DO carry an id. `new` copied a
    `#` cell through `copied_row` validating nothing, so a numbering the
    reviewer chose surfaced two commands later at `close`. It is refused where
    the report is, and `close` still refuses it for a record written by hand."""

    declared(repo)
    code, out, _ = generate(
        repo, report_text=report(verdicts="| R2-1 | one | `f.py:1` | open | read |\n")
    )
    assert code == 2, out
    assert "bare integer" in out, out
    assert "R2-1" in out, out


# --- what a person reads ----------------------------------------------------


def test_the_documents_say_where_the_reviewer_picks_the_number():
    """The ticket's own last line: if bare integers are the contract, say so
    where reviewers pick numbers, not only at the point of refusal."""
    for rel in (
        "skills/code-review/SKILL.md",
        "docs/review-chain-spec.md",
        "templates/sdd-round.md",
    ):
        with open(f"{ROOT}/{rel}", encoding="utf-8") as f:
            text = " ".join(f.read().split())
        assert "bare integer" in text, rel


def test_the_documents_say_that_a_row_commissioning_nothing_takes_no_id():
    """§14: the refusal moved, so the sentence a reviewer reads moves with it
    in the same commit. A rule stated only at the point of refusal reaches a
    report that is already written — which is why #321's answer 3 was rejected
    as a mechanism and kept as this obligation."""
    for rel in (
        "skills/code-review/SKILL.md",
        "docs/review-chain-spec.md",
        "templates/sdd-round.md",
    ):
        with open(f"{ROOT}/{rel}", encoding="utf-8") as f:
            text = " ".join(f.read().split())
        assert "commissions nothing" in text, rel
        # The direction it fails in, where the reviewer picks the number.
        assert "no id" in text, rel
    with open(f"{ROOT}/agents/warden.md", encoding="utf-8") as f:
        warden = " ".join(f.read().split())
    assert "commissions nothing" in warden, "the agent that writes the marker"
