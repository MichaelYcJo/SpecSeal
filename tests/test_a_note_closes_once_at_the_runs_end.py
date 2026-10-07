"""A note closes once, at the run's end (#837).

A ⬜ is the reviewer's mark for a finding that reads badly while the behaviour
and the fact stay right (`skills/code-review/SKILL.md` §*Findings format*).
Until #837 each one took a row in its own round's fix table, and a ⬜ closed
`fixed` commissioned a reader for a sentence: on #822's run the five ⬜ rows of
one record were its only fix words, and they spent the run's one reopening.

`skills/code-review/orchestration.md` §*A note closes once, at the run's end*
owns the rule. These cases hold the three places that make it so:
`chain_check.py` at the pull request, `round_record.py notes` at the run's
end, and `close` and `seal` around it. Every case drives a scratch
repository, and each was seen red against the code before the rule (§15) —
how is said in the case.
"""

import json
import os
import shutil
import subprocess
import sys

import pytest
from test_the_record_is_generated import (
    CHECK,
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
    reader_module,
    report,
    rows_of,
    write,
)

NOTE = "\N{WHITE LARGE SQUARE}"
VERDICT_HEADER = (
    "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
)
AT_THE_CUTOFF = "seal/specs/1791384154-an-item-under-the-rule"
BEFORE_THE_CUTOFF = "seal/specs/1791384153-an-item-before-the-rule"


@pytest.fixture
def scratch(tmp_path):
    d = tmp_path / "repo"
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")
    return d


def hand_record(target, verdicts, checker="no fixes to check", box="x", fof=None):
    """A record carrying only what the note arms read: the verdict table, the
    `Fixes checked by` row and, where a run is cut, `Fix of a fix`."""
    fof_row = f"| Fix of a fix | {fof} |\n" if fof else ""
    return (
        "# an item — review round\n\n| Field | Value |\n|---|---|\n"
        f"| Target SHA | {target} |\n| Fixes checked by | {checker} |\n{fof_row}\n"
        f"- [{box}] Pass\n\n## Verdicts\n\n{VERDICT_HEADER}{verdicts}\n"
    )


def committed(repo, item, records):
    """`records` ({n: text}) written under `item/rounds/` and committed;
    returns their repository-relative paths, lowest round first."""
    rels = []
    for n, text in sorted(records.items()):
        rel = f"{item}/rounds/round-{n}.md"
        write(repo, rel, text)
        rels.append(rel)
    commit(repo, "records")
    return rels


def arms(repo, rels, strict=True):
    chain, reader = check_module(), reader_module()
    return chain.carried_notes(reader, str(repo), rels, strict)


# --- the reader --------------------------------------------------------------


def test_note_rows_reads_the_marker_and_the_id_and_nothing_else():
    """The ⬜ in the `#` cell and digits after it make a note. A bare ⬜ names
    no finding, a 🟡 located in a record is the reviewer's 🟡, and a ⬜ written
    in another cell is a quote — none is a note. Seen red with
    `chain_check.note_rows` absent (AttributeError)."""
    chain = check_module()
    rows = [
        (10, [f"{NOTE} 3", "reads badly", "`seal/ledger.md`", "open", "read"]),
        (11, [f"{NOTE} 4", "reads badly", "`f.py:1`", "answered", "read"]),
        (12, [f"{NOTE}", "a bare note", "`f.py:1`", "open", "read"]),
        (13, ["\N{LARGE YELLOW CIRCLE} 5", "in a record", "`seal/x.md`", "open", ""]),
        (
            14,
            ["\N{LARGE GREEN CIRCLE}", f"quotes {NOTE} 2", "`f.py:1`", "verified", ""],
        ),
        (15, [f"{NOTE} 6", "closed", "`f.py:1`", "**fixed** `abc1234`", "read"]),
    ]
    assert chain.note_rows(rows, 3) == [(10, 3, True), (11, 4, False), (15, 6, False)]


def test_the_generator_reads_the_glyph_from_the_checker():
    """One spelling of the glyph: `round_record.py`'s `COMMISSIONS_NOTHING`
    is built from `chain_check.NOTE`, so the two cannot name different
    markers."""
    generator, chain = generator_module(), check_module()
    assert chain.NOTE == NOTE
    assert chain.NOTE in generator.COMMISSIONS_NOTHING


# --- arm A: a note closed on a fix word ---------------------------------------

CLOSED_FIXED = f"| {NOTE} 2 | reads badly | `f.py:1` | **fixed** `abc1234` | read |\n"


@pytest.mark.parametrize(
    "item, refused",
    [(AT_THE_CUTOFF, True), (BEFORE_THE_CUTOFF, False)],
    ids=["at-the-cutoff", "one-second-before"],
)
def test_a_note_closed_fixed_is_an_error_from_the_cutoff_and_a_notice_before(
    scratch, item, refused
):
    """S7. A ⬜ closed `fixed` commissions a reader the note never owed. From
    `NOTES_FROM` on it fails; one second before it prints — the 35 rows the
    corpus closed that way before the rule print and never fail. Seen red with
    arm A deleted from `carried_notes`: neither list carried the line."""
    head = git(scratch, "rev-parse", "HEAD").stdout.strip()
    rels = committed(scratch, item, {1: hand_record(head, CLOSED_FIXED)})
    errors, notices = arms(scratch, rels)
    said = [m for _r, _l, m in (errors if refused else notices)]
    assert any(f"{NOTE} 2 closes on `fixed`" in m for m in said), (errors, notices)
    assert any("A note commissions nothing" in m for m in said), said
    assert any("§*A note closes once, at the run's end*" in m for m in said), said
    other = notices if refused else errors
    assert not [m for _r, _l, m in other if "closes on" in m], other
    if not refused:
        assert any("excused this and print instead" in m for m in said), said


def test_a_note_closed_answered_or_deferred_is_not_refused(scratch):
    """The three closings the rule names pass: `answered` with
    `corrected at <sha>`, `answered` with grounds, `deferred <home>`."""
    head = git(scratch, "rev-parse", "HEAD").stdout.strip()
    rows = (
        f"| {NOTE} 1 | a | `f.py:1` | answered | corrected at {head[:7]}; read |\n"
        f"| {NOTE} 2 | b | `f.py:1` | answered | it stands: the word is pinned |\n"
        f"| {NOTE} 3 | c | `f.py:1` | deferred #830 | #830 |\n"
    )
    rels = committed(scratch, AT_THE_CUTOFF, {1: hand_record(head, rows)})
    assert arms(scratch, rels) == ([], [])


# --- arm B: a note still open on a record of the run ---------------------------

OPEN_NOTE = f"| {NOTE} 3 | reads badly | `f.py:1` | open | read |\n"
ANSWERED = "| \N{LARGE YELLOW CIRCLE} 1 | a claim | `f.py:1` | answered | grounds |\n"


@pytest.mark.parametrize("strict", [True, False], ids=["ready", "draft"])
def test_an_open_note_on_an_earlier_record_fails_a_ready_pull_request(scratch, strict):
    """S7. The note is on round 1 and the last record is clean, which is the
    shape the check could not see before: `Pass` and the blocking walk read
    the last record alone. Ready, it is an error naming the note and
    `notes`; a draft prints the same and names what re-arms it. Seen red
    with arm B deleted: neither list carried the line."""
    head = git(scratch, "rev-parse", "HEAD").stdout.strip()
    rels = committed(
        scratch,
        BEFORE_THE_CUTOFF,
        {
            1: hand_record(head, ANSWERED + OPEN_NOTE, checker="round-2", box=" "),
            2: hand_record(head, ANSWERED),
        },
    )
    errors, notices = arms(scratch, rels, strict=strict)
    hit = errors if strict else notices
    said = [(r, m) for r, _l, m in hit if f"{NOTE} 3 is still open" in m]
    assert said and said[0][0] == rels[0], (errors, notices)
    assert "`round-record notes --item <dir> --fixes <table> --at <sha>`" in said[0][1]
    if strict:
        assert "A ready pull request over an open note" in said[0][1]
    else:
        assert "*Ready for review*" in said[0][1]
        assert not errors, errors


def test_an_open_note_of_a_stopped_run_is_not_read_once_the_redesign_runs(scratch):
    """The current run is `runs_of`'s last. A note left open on a run that
    stopped at a `second` belongs to that run, which `notes` closes at the
    stop; the redesign's records are a run of their own."""
    head = git(scratch, "rev-parse", "HEAD").stdout.strip()
    rels = committed(
        scratch,
        BEFORE_THE_CUTOFF,
        {
            1: hand_record(head, OPEN_NOTE, box=" "),
            2: hand_record(head, ANSWERED, fof="first — `f.py:1`"),
            3: hand_record(head, ANSWERED, fof="second — `f.py:1`"),
            4: hand_record(head, ANSWERED),
        },
    )
    assert arms(scratch, rels) == ([], [])
    # And the same records with the redesign's round taken away: the stopped
    # run is the current one, and its open note is read.
    errors, _ = arms(scratch, rels[:3])
    assert any(f"{NOTE} 3 is still open" in m for _r, _l, m in errors), errors


# --- the arms are wired into `main` -------------------------------------------


def declared_at(repo, item):
    write(
        repo,
        f"{item}/routing.md",
        f"# {os.path.basename(item)} — routing\n\n| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n| Branch | feature |\n",
    )
    return commit(repo, "declare")


def run_main(repo, draft):
    env = dict(os.environ)
    env.pop("GITHUB_HEAD_REF", None)
    env.pop("GITHUB_EVENT_PATH", None)
    # The annotation form, so a line says whether it is an error or a notice;
    # a plain line is `path:line  message` for both.
    env["GITHUB_ACTIONS"] = "true"
    if draft:
        payload = repo.parent / "event.json"
        payload.write_text(json.dumps({"pull_request": {"draft": True}}), "utf-8")
        env["GITHUB_EVENT_PATH"] = str(payload)
    r = subprocess.run(
        [sys.executable, CHECK, "--baseline", "base", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


@pytest.mark.parametrize("draft", [False, True], ids=["ready", "draft"])
def test_chain_check_reports_an_open_note_once_per_work_item(scratch, draft):
    """The arms run from `main`, once per work item, after the per-record
    walk: an error line at a ready pull request and a notice line on a
    draft, each naming the record that holds the note. Seen red with the
    call removed from `main`: no line carried the note."""
    head = declared_at(scratch, AT_THE_CUTOFF)
    committed(
        scratch,
        AT_THE_CUTOFF,
        {
            1: hand_record(head, ANSWERED + OPEN_NOTE, checker="round-2", box=" "),
            2: hand_record(head, ANSWERED),
        },
    )
    _code, out = run_main(scratch, draft)
    level = "notice" if draft else "error"
    lines = [ln for ln in out.splitlines() if f"{NOTE} 3 is still open" in ln]
    assert len(lines) == 1, out
    assert lines[0].startswith(f"::{level} ") and "round-1.md" in lines[0], lines


# --- `notes`: the run's notes, closed once at its end ---------------------------
#
# The records here are written by `round_record.py new` from reviewers'
# reports, so a cell `notes` reads is a cell the generator wrote.

NOTE_ONE = f"| {NOTE} 1 | a sentence reads badly | `README.md` | open | read |\n"
NOTE_TWO = f"| {NOTE} 1 | another sentence | `docs/x.md` | open | read |\n"
YELLOW_ANSWERED = (
    "| \N{LARGE YELLOW CIRCLE} 2 | a claim | `f.py:1` | answered | grounds |\n"
)
RED_OPEN = "| \N{LARGE RED CIRCLE} 2 | a defect | `f.py:1` | open | executed |\n"


def _build_repo(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    write(d, "README.md", "# a fixture\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("notes-template") / "repo"
    _build_repo(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def round_n(repo, n, verdicts, needs="no", floor="no"):
    """Round N written by `new` from a report and committed; returns the
    record's text."""
    code, out, text = generate(
        repo, n, report_text=report(verdicts=verdicts, needs=needs, floor=floor)
    )
    assert code in (0, 1), out
    assert text is not None, out
    commit(repo, f"round {n}")
    return text


def two_rounds_with_a_note_each(repo):
    """Round 1 holds ⬜ 1 open beside a 🟡 the reviewer answered, round 2
    holds its own ⬜ 1 open: the same id on two records of one run, and the
    run ended at round 2, which reads `no fixes to check`. Returns the
    correction commit, made after the last review."""
    declared(repo)
    round_n(repo, 1, NOTE_ONE + YELLOW_ANSWERED)
    round_n(repo, 2, NOTE_TWO)
    write(repo, "README.md", "# a fixture, the sentence reworded\n")
    return commit(repo, "the notes' corrections")


def notes_table(*rows):
    return (
        "## Fixes\n\n| Round | # | Verdict | Commit or grounds |\n|---|---|---|---|\n"
        + "".join(rows)
    )


def run_notes(repo, table, at=None, extra=()):
    path = repo.parent / "notes.md"
    path.write_text(table, encoding="utf-8")
    r = subprocess.run(
        [
            sys.executable,
            GENERATOR,
            "notes",
            "--item",
            str(repo / ITEM),
            "--fixes",
            str(path),
            *(["--at", at] if at else []),
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
    return r.returncode, r.stdout + r.stderr


def record(repo, n):
    return (repo / ROUNDS / f"round-{n}.md").read_text(encoding="utf-8")


def cells_of(text):
    reader = reader_module()
    return [
        [reader.visible(c) for c in reader.split_row(line)]
        for line in rows_of(text, "## Verdicts")[2:]
    ]


BOTH_ROWS = (
    "| round-1 | 1 | corrected | the sentence reworded |\n",
    "| round-2 | 1 | answered | it stands: the word is pinned by a case |\n",
)


def test_notes_closes_every_note_of_the_run_once(repo):
    """S4. Two notes sharing an id, on two records, closed in one pass at one
    commit: round 1's reads `answered | corrected at <sha> — <note>; <the
    reviewer's grounds>`, round 2's `answered | <grounds>; <the reviewer's>`,
    `Pass` is ticked on both, round 2's `Why` cell for round 1's note stops
    saying `open`, and the chain check exits 0. Seen red with `notes`
    absent: argparse refused the subcommand."""
    at = two_rounds_with_a_note_each(repo)
    before_one, before_two = record(repo, 1), record(repo, 2)
    chain = check_module()
    assert fields(before_one)[chain.CHECKED_BY] == chain.NO_FIXES, before_one
    assert fields(before_two)[chain.CHECKED_BY] == chain.NO_FIXES, before_two
    assert "- [ ] Pass" in before_one and "- [ ] Pass" in before_two
    assert f"round 1's {NOTE} 1 \N{EM DASH} open" in before_two
    code, out = run_notes(repo, notes_table(*BOTH_ROWS), at=at)
    assert code == 0, out
    one, two = record(repo, 1), record(repo, 2)
    assert cells_of(one)[0][3:] == [
        "answered",
        f"corrected at {at[:8]} \N{EM DASH} the sentence reworded; read",
    ], one
    assert cells_of(one)[1][3] == "answered", "a row the table did not name moved"
    assert cells_of(two)[0][3:] == [
        "answered",
        "it stands: the word is pinned by a case; read",
    ], two
    assert "- [x] Pass" in one and "- [x] Pass" in two
    assert f"round 1's {NOTE} 1 \N{EM DASH} answered" in two, two
    assert f"round 1's {NOTE} 1 \N{EM DASH} open" not in two
    assert "closed 2 notes of the run ending at round-2.md" in out, out


def test_a_note_with_no_row_is_named_and_nothing_is_written(repo):
    """S4, the second case: every open note of the run takes a row, and the
    one without is named by record and id."""
    at = two_rounds_with_a_note_each(repo)
    before = record(repo, 1), record(repo, 2)
    code, out = run_notes(repo, notes_table(BOTH_ROWS[0]), at=at)
    assert code == 2, out
    assert f"round-2.md's {NOTE} 1 is open and the notes table has no row" in out
    assert (record(repo, 1), record(repo, 2)) == before


def test_fixed_on_a_note_is_refused_with_the_rule(repo):
    """S4, the third case: `fixed` is refused naming the rule and its owner,
    because a note commissions no reader and `fixed` commissions one (§14
    pins the sentence)."""
    at = two_rounds_with_a_note_each(repo)
    code, out = run_notes(
        repo,
        notes_table(f"| round-1 | 1 | fixed | {at[:7]} |\n", BOTH_ROWS[1]),
        at=at,
    )
    assert code == 2, out
    assert "round-1's note 1 is `fixed`, and a note never closes on a fix word" in out
    assert "§*A note closes once, at the run's end*" in out, out


def test_a_row_for_a_finding_that_is_not_a_note_is_refused(repo):
    """A 🔴 or 🟡 closes in its round's fix table through `close`; a notes
    table naming one is refused, and so is a row for a note already closed."""
    at = two_rounds_with_a_note_each(repo)
    code, out = run_notes(
        repo,
        notes_table(*BOTH_ROWS, "| round-1 | 2 | answered | grounds |\n"),
        at=at,
    )
    assert code == 2, out
    assert "round-1's finding 2, which is not a" in out, out


def test_notes_refuses_before_the_run_has_ended(repo):
    """S3. Round 1 holds an open 🔴, so its `Fixes checked by` reads `nobody
    — the fixes are not yet written` and the run has not ended: `notes`
    refuses, saying what the last record reads. Seen red with the run's-end
    test removed: the note closed under a run still running."""
    declared(repo)
    round_n(repo, 1, NOTE_ONE + RED_OPEN, needs="yes \N{EM DASH} 2")
    before = record(repo, 1)
    code, out = run_notes(repo, notes_table("| round-1 | 1 | answered | it stands |\n"))
    assert code == 2, out
    assert "round-1.md is the last record of the run" in out, out
    assert "so the run has not ended" in out and "nobody" in out, out
    assert record(repo, 1) == before


@pytest.mark.parametrize("where", ["the-last-target", "off-the-branch"])
def test_at_is_a_commit_after_the_last_review_on_the_branch(repo, where):
    """S5. `--at` naming the run's last `Target SHA` (or an ancestor of it)
    is a correction the last round already read, and one HEAD does not
    descend from is a commit the branch does not carry; both are refused
    before anything is written."""
    two_rounds_with_a_note_each(repo)
    if where == "the-last-target":
        at = fields(record(repo, 2))["Target SHA"]
        said = "or an ancestor of it"
    else:
        git(repo, "switch", "-qc", "elsewhere", "base")
        write(repo, "g.py", "y = 1\n")
        at = commit(repo, "elsewhere")
        git(repo, "switch", "-q", "feature")
        said = "is not an ancestor of HEAD"
    before = record(repo, 1), record(repo, 2)
    code, out = run_notes(repo, notes_table(*BOTH_ROWS), at=at)
    assert code == 2, out
    assert said in out, out
    assert (record(repo, 1), record(repo, 2)) == before


def test_corrected_without_at_is_refused(repo):
    """`corrected` writes the commit into the grounds, and the commit is
    `--at`'s; a table carrying one with no `--at` is refused."""
    two_rounds_with_a_note_each(repo)
    code, out = run_notes(repo, notes_table(*BOTH_ROWS))
    assert code == 2, out
    assert "a row reads `corrected` and --at names no commit" in out, out


def test_a_bare_id_with_no_round_is_refused_naming_the_round_column(repo):
    """The notes table is the fix table with a `Round` column in front,
    because an id restarts at every round; the fix table's own header is
    refused naming the notes table's."""
    at = two_rounds_with_a_note_each(repo)
    table = (
        "## Fixes\n\n| # | Verdict | Commit or grounds |\n|---|---|---|\n"
        "| 1 | answered | it stands |\n"
    )
    code, out = run_notes(repo, table, at=at)
    assert code == 2, out
    assert "| Round | # | Verdict | Commit or grounds |" in out, out


def test_the_seal_waits_for_the_notes(repo):
    """S6. Round 1 holds an open note and round 2, the last record, is clean:
    `Pass` ticked and `no fixes to check`. `seal` used to read the last
    record alone and wrote the cell; it refuses now, naming `round-1.md`'s
    ⬜ 1 and `notes`, and `seal --check` refuses the same way. Seen red with
    the refusal removed: exit 0 and the cell written."""
    declared(repo)
    round_n(repo, 1, NOTE_ONE + YELLOW_ANSWERED)
    round_n(repo, 2, YELLOW_ANSWERED)
    assert "- [x] Pass" in record(repo, 2)
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    for extra in ((), ("--check",)):
        before = record(repo, 2)
        r = subprocess.run(
            [
                sys.executable,
                GENERATOR,
                "seal",
                "--item",
                str(repo / ITEM),
                "--broad-gate",
                f"{head[:8]} against base",
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
        out = r.stdout + r.stderr
        assert r.returncode == 2, out
        assert f"1 note of the run is still open: round-1.md's {NOTE} 1" in out, out
        assert "round-record notes --item <dir> --fixes <table> --at <sha>" in out
        assert "no cell was written" in out
        assert record(repo, 2) == before


def test_a_stopped_run_closes_its_notes_at_the_second(repo):
    """S9. The last record reads `Fix of a fix | second` and `no fixes to
    check`: `notes` runs there, before the framer is spawned, closes the
    stopped run's note, and says nothing about a `Reframed` line. The run is
    the one the LAST record joined, which `current_run` alone answers empty
    for. Seen red with `run_of_last` returning `current_run(found)`: no
    record to close."""
    declared(repo)
    # The floor is `yes` until the stop, so the floor's walk does not refuse
    # a run that carried on: a stopped run is one that kept finding things.
    crashes = "yes \N{EM DASH} the record is lost"
    round_n(repo, 1, NOTE_ONE + YELLOW_ANSWERED, floor=crashes)
    round_n(repo, 2, YELLOW_ANSWERED, floor=crashes)
    round_n(repo, 3, YELLOW_ANSWERED)
    for n, value in (
        (2, "first \N{EM DASH} `f.py:1`"),
        (3, "second \N{EM DASH} `f.py:1`"),
    ):
        path = repo / ROUNDS / f"round-{n}.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("| Fix of a fix | no |", f"| Fix of a fix | {value} |"),
            encoding="utf-8",
        )
    commit(repo, "the run stopped at round 3")
    generator, reader = generator_module(), reader_module()
    routing = generator.load(generator.chain.ROUTING, "specseal_routing_for_notes")
    found = generator.earlier_records(routing, str(repo / ROUNDS), sys.maxsize)
    assert [k for k, _p in generator.current_run(reader, found)[0]] == []
    assert [k for k, _p in generator.run_of_last(reader, found)] == [1, 2, 3]
    code, out = run_notes(repo, notes_table("| round-1 | 1 | answered | it stands |\n"))
    assert code == 0, out
    assert "Reframed" not in out, out
    assert "closed 1 note of the run ending at round-3.md" in out, out
    assert cells_of(record(repo, 1))[0][3] == "answered"
    # Round 1's coordinate sits under round 1 in EVERY later record's
    # inherited table, so both owe the new word, not round 2's alone.
    for later in (2, 3):
        assert f"round 1's {NOTE} 1 \N{EM DASH} answered" in record(repo, later)


def test_a_note_reopened_by_hand_over_its_closing_is_refused(repo):
    """`close`'s guard, in `notes`: a ⬜ whose `Verdict` cell was set back to
    `open` while its `Grounds` cell still carries the closing would carry the
    closing twice, and a record that says a thing twice still parses."""
    at = two_rounds_with_a_note_each(repo)
    code, out = run_notes(repo, notes_table(*BOTH_ROWS), at=at)
    assert code == 0, out
    path = repo / ROUNDS / "round-1.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace(
            f"| {NOTE} 1 | a sentence reads badly | `README.md` | answered |",
            f"| {NOTE} 1 | a sentence reads badly | `README.md` | open |",
        ),
        encoding="utf-8",
    )
    before = path.read_text(encoding="utf-8")
    assert before != text, "the fixture did not reopen the row"
    code, out = run_notes(repo, notes_table(BOTH_ROWS[0]), at=at)
    assert code == 2, out
    assert "already carries a closing" in out, out
    assert path.read_text(encoding="utf-8") == before
