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
import subprocess
import sys

import pytest
from test_the_record_is_generated import (
    CHECK,
    check_module,
    commit,
    git,
    reader_module,
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
    from test_the_record_is_generated import generator_module

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


def declared(repo, item):
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
    head = declared(scratch, AT_THE_CUTOFF)
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
