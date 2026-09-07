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

import re
import shutil
import subprocess

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
    commit,
    generator_module,
    reader_module,
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


# --- the id the reviewer picks ----------------------------------------------


def test_a_round_prefixed_verdict_id_is_refused_naming_the_format(repo):
    """#227's own numbering, in the verdict table `new` copied from the report."""
    a = round_one(
        repo,
        verdicts=(
            "| 🔴 R2-1 | helper drops b | `mod.py#helper` | open | executed |\n"
            "| 🟡 R2-2 | only_tested ignores rest | `mod.py:5` | open | read |\n"
        ),
    )
    b = a_fix(repo)
    code, out, _ = close(
        repo, 1, fix_table(f"| R2-1 | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    # The format, named. The old message named a duplicate instead.
    assert "bare integer" in out, out
    # The row, quoted. The old message quoted nothing.
    assert "R2-1" in out, out
    assert "two verdict rows" not in out, "the duplicate that was not one"


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
    a = round_one(
        repo,
        verdicts=(
            "| 🔴 1a | one | `mod.py#helper` | open | read |\n" if on_record else OPEN_1
        ),
    )
    b = a_fix(repo)
    bad_id = "1a" if not on_record else "1"
    code, out, _ = close(
        repo, 1, fix_table(f"| {bad_id} | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    want = generator.RECORD_LABEL if on_record else generator.FIX_TABLE_LABEL
    other = generator.FIX_TABLE_LABEL if on_record else generator.RECORD_LABEL
    assert code == 2, out
    assert want in out, out
    assert other not in out, out


@pytest.mark.parametrize(
    "bad",
    ["R2-1", "1-1", "1b", "A2", "N1", "A", "carried", "round 2's finding (🟡 4)"],
)
def test_every_shape_the_corpus_holds_is_refused_by_name(repo, bad):
    """The eight shapes committed records actually carry in that column.
    Each is refused, and each refusal quotes the cell it refused — with
    eight rows and no coordinate, the ticket's complaint was the scan."""
    a = round_one(
        repo, verdicts=f"| 🔴 {bad} | one | `mod.py#helper` | open | read |\n"
    )
    b = a_fix(repo)
    code, out, _ = close(
        repo, 1, fix_table(f"| {bad} | fixed | {b[:7]} |\n"), f"{a}..{b}"
    )
    assert code == 2, out
    assert "bare integer" in out, out
    # The whole row, not just the cell — a bare `A` would match anything.
    assert f"| {bad} | fixed |" in out, out


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


# --- the duplicate that really is one ---------------------------------------


def test_a_duplicate_verdict_id_quotes_both_rows(repo):
    """When two rows really do carry the same id, the refusal names both.
    Naming one is the manual scan the ticket paid for."""
    a = round_one(
        repo,
        verdicts=(
            "| 🔴 3 | the first three | `mod.py#helper` | open | executed |\n"
            "| 🟡 3 | the second three | `mod.py:5` | open | read |\n"
        ),
    )
    b = a_fix(repo)
    code, out, _ = close(repo, 1, fix_table(f"| 3 | fixed | {b[:7]} |\n"), f"{a}..{b}")
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
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files", "seal/specs/*/rounds/round-*.md"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.split()
    return out


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
