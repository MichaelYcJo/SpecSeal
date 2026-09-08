"""The reviewer's report reaches the record as a file, not as a retyped copy.

`round_record.py new` took `--report <path>`, a file, and the reviewer's
report was not one. The warden returns it as its final message and the
orchestrator is told not to open the agent transcript, so the report existed
in two places and neither was a file -- and the orchestrator typed it into
one. Four rounds of one work item in another repository, four retypings;
0.9.0's own #190 · #207 run retyped rounds 2 and 3 by hand. A retyped verdict
row carries retyped coordinates, re-review inheritance carries the paraphrase
into the next round, and `Fixes checked by` then names a round whose report
is not the report the reviewer wrote (#228).

Two halves of the repair, and these cases pin both:

  the reviewer   writes the report to `<item>/rounds/round-N-report.md` and
                 returns the path (`agents/warden.md` §Report)
  the generator  reads that path when `--report` is absent, derived from
                 `--item` and `--round` -- the same pair `round-N.md` is
                 derived from, so the two names cannot be spelled apart

Every case here was seen red first (§15): the three generator cases against
`--report required=True`, where the run exits 2 on argparse before it reaches
anything this module asserts, and the two document cases with the sentence
they pin deleted. The report-is-not-a-record case was seen red by widening
`hooks/routing.py`'s `ROUND_RE` to match the report's own name.
"""

import os
import subprocess
import sys

import pytest
from test_the_record_is_generated import (
    ASKED,
    GENERATOR,
    ITEM,
    RAN_BY,
    ROUNDS,
    _build,
    declared,
    env_without_a_pull_request,
    generator_module,
    git,
    read,
    report,
    write,
)

# The reviewer's own artifact, beside the record it becomes. Spelled here
# rather than imported so a rename of the constant cannot quietly rename the
# convention two documents and one agent state in prose.
REPORT_NAME = "round-{n}-report.md"

WARDEN = ("agents", "warden.md")
SKILL = ("skills", "code-review", "SKILL.md")
PROTOCOL = ("docs", "review-handoff-protocol.md")

# A row that could only have come from one of the two reports below, so a
# case can say WHICH file was read rather than that reading succeeded.
CONVENTIONAL_ROW = (
    "| 🔴 1 | the conventional report was read | `f.py:1` | open | executed |\n"
)
FLAGGED_ROW = "| 🔴 1 | the flagged report was read | `f.py:1` | open | executed |\n"


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("reviewers-report-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    import shutil

    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def leave_report(repo, n, text):
    """Write the report where the reviewer leaves it, and return the path."""
    rel = f"{ROUNDS}/{REPORT_NAME.format(n=n)}"
    write(repo, rel, text)
    return repo / rel


def run_new(repo, n=1, report_flag=None, target=None, asked=ASKED):
    """`round_record.py new`, with `--report` only when one is given.

    The default arm is the whole point: passing the flag is what the
    orchestrator used to do with a retyped file, and a case that always
    passes it can never see the default fire.
    """
    asked_path = repo.parent / f"asked-{n}.md"
    asked_path.write_text(asked, encoding="utf-8")
    target = target or git(repo, "rev-parse", "HEAD").stdout.strip()
    argv = [
        sys.executable,
        GENERATOR,
        "new",
        "--item",
        str(repo / ITEM),
        "--round",
        str(n),
        "--target",
        target,
        "--asked",
        str(asked_path),
        "--ran-by",
        RAN_BY,
        "--baseline",
        "base",
    ]
    if report_flag is not None:
        argv += ["--report", str(report_flag)]
    r = subprocess.run(
        argv,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        env=env_without_a_pull_request(),
    )
    path = repo / ROUNDS / f"round-{n}.md"
    text = path.read_text(encoding="utf-8") if path.exists() else None
    return r.returncode, r.stdout + r.stderr, text


def test_the_default_reads_the_report_the_reviewer_left(repo):
    """No `--report`, and the record still carries the reviewer's own rows.

    This is the retyping removed: the file the generator reads is the file
    the reviewer wrote, and nothing passed through a person in between.
    """
    declared(repo)
    leave_report(repo, 1, report(verdicts=CONVENTIONAL_ROW))
    code, out, text = run_new(repo)
    assert code == 0, out
    assert text is not None, out
    assert "the conventional report was read" in text


def test_the_flag_still_wins_over_the_conventional_path(repo):
    """`--report` names a report written somewhere else, and it is read.

    Two callers need it and both are real: a round whose report predates the
    convention, and a round that ran more than one reviewer, where the
    orchestrator hands each its own path rather than letting the second
    overwrite the first. Both reports exist here, so the assertion is about
    which one was chosen and not about one of them being missing.
    """
    declared(repo)
    leave_report(repo, 1, report(verdicts=CONVENTIONAL_ROW))
    elsewhere = repo.parent / "somewhere-else.md"
    elsewhere.write_text(report(verdicts=FLAGGED_ROW), encoding="utf-8")
    code, out, text = run_new(repo, report_flag=elsewhere)
    assert code == 0, out
    assert "the flagged report was read" in text
    assert "the conventional report was read" not in text


def test_the_absence_names_the_path_and_the_convention(repo):
    """Neither the flag nor a file, and the refusal says both.

    The path alone reads as a mistyped argument, which is the one thing it
    cannot be: nobody typed it. So the message has to carry where the
    reviewer was told to leave the report as well as where the generator
    looked.
    """
    declared(repo)
    code, out, text = run_new(repo)
    assert code == 2, out
    assert text is None, "a record was written from a report that is not there"
    assert REPORT_NAME.format(n=1) in out, out
    assert "warden.md" in out, out
    assert "--report" in out, out


def test_a_directory_at_the_report_path_is_refused_as_a_directory(repo):
    """`isfile` is False for two states, and the message named only one.

    A reviewer that made the directory instead of the file read `no report at
    <path>` about a path with something at it — the one reading this guard
    exists to rule out, because nobody typed the path and *nothing is there*
    is therefore not a typo the reader can go and find. Both leads still
    carry the convention: the path, the document that fills it, and the flag
    that names one written elsewhere.
    """
    declared(repo)
    (repo / ROUNDS / REPORT_NAME.format(n=1)).mkdir(parents=True)
    code, out, text = run_new(repo)
    assert code == 2, out
    assert text is None, "a record was written from a directory"
    assert "is a directory" in out, out
    assert "no report at" not in out, (
        "the refusal still says nothing is at a path that has a directory at it"
    )
    # The tail the absence carries too — a lead that drops it leaves the
    # reviewer knowing what is wrong and not what to do.
    assert REPORT_NAME.format(n=1) in out, out
    assert "warden.md" in out, out
    assert "--report" in out, out


def test_a_report_beside_a_record_is_not_a_record(repo):
    """`rounds/` now holds a second file per round, and only one is a record.

    Every reader of that directory selects by name through
    `routing.round_number`. Three did not. Two raised `TypeError` rather than
    failing an assertion (`tests/test_the_reopening_is_one.py`,
    `tests/test_chain_check_at_the_pull_request.py`); the third counted
    fifty-three non-records into a corpus of records and said nothing at all
    (`tests/test_a_finding_id_is_a_bare_integer.py`, round 1 🟡 1). The
    round-2 run is the executed half: its reach-back walks `rounds/` with
    round 1's record and round 1's report both sitting in it.
    """
    generator = generator_module()
    routing = generator.load(generator.chain.ROUTING, "routing_for_report_names")
    assert routing.round_number("round-1.md") == 1
    assert routing.round_number(REPORT_NAME.format(n=1)) is None
    assert routing.round_number(REPORT_NAME.format(n=12)) is None

    declared(repo)
    leave_report(repo, 1, report(verdicts=CONVENTIONAL_ROW))
    code, out, _ = run_new(repo)
    assert code == 0, out
    assert (repo / ROUNDS / REPORT_NAME.format(n=1)).exists()

    leave_report(repo, 2, report(verdicts=FLAGGED_ROW))
    code, out, text = run_new(repo, n=2)
    # Not the exit code. `new` runs `chain_check` after it writes, and on a
    # scratch repository mid-review that check has true things to say which
    # have nothing to do with this case -- two records at one target SHA, and
    # round 1's fix-surface cells still in their starting state. What this
    # case is about happens before the check runs.
    assert text is not None, out
    assert "round-2.md" in out, out
    # The reach-back walked `rounds/` with the report sitting in it and found
    # round 1's record. A report read as a record would have made two `None`
    # round numbers in one directory, which is the `TypeError` on the sort
    # that the two tests named above were written for.
    assert "set `Fixes checked by` of round-1.md to round-2" in out, out
    # And the inheritance carried round 1's coordinate, not the report's.
    assert "`f.py:1`" in text


def test_the_warden_is_told_where_to_leave_the_report():
    """§14: the instruction a reviewer reads and acts on is pinned.

    The generator's default is worth nothing if the file is not there, and
    the only thing that puts it there is this sentence.
    """
    warden = read(*WARDEN)
    assert "rounds/round-<n>-report.md" in warden, (
        "agents/warden.md no longer tells the reviewer where to write its "
        "report, so `round_record.py new`'s default reads a path nothing fills"
    )
    assert "return that path" in warden or "returns that path" in warden


def test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file():
    """§14: the cost this convention added, stated where the reviewer reads it.

    The report used to be chat text, and nothing in the tree scanned chat
    text. Committed beside the record it is a tracked file, so two
    repository-wide readers reach it: the no-real-identifiers rule over every
    tracked file, and the evidence checker over every `.md` under a live work
    item. Neither reader is new. What is new is that a reviewer's prose is
    their input, and the round that found this had to be told so by nothing.

    The contract walks the reviewer into the first of them — §8 says to write
    the clone's absolute path out, which is exactly the string the identifier
    rule refuses. Both refusals land at the pull request, after the round has
    ended and where nobody can ask the reviewer what it meant, so the warning
    is worth nothing without the edit that answers it. Every escape is
    pinned for that reason: the fixture user path, the evidence checker's own
    per-line exemption marker, the rule that the marker never goes inside a
    fence (round 2, 🟡 7 -- the block's first version illustrated it there,
    which is the one region the checker never reads), and the identifier
    rule's second half, the domain arm.
    """
    warden = read(*WARDEN)
    assert "## Report" in warden
    section = warden.split("## Report", 1)[1]
    for needle, why in (
        (
            "tracked content",
            "nothing tells the reviewer its report becomes a file the tree's "
            "own readers scan",
        ),
        (
            "test_no_real_identifiers.py",
            "the identifier rule is not named, so the reviewer cannot tell "
            "which red build its absolute paths caused",
        ),
        (
            "/Users/x/",
            "the identifier rule is named with no way through it — a warning "
            "that leaves the reviewer a red build and no edit to make",
        ),
        (
            "NAME NOT IN TREE",
            "the evidence checker's exemption marker is not named, so a "
            "paste-ready fix proposing a new symbol has no legal spelling",
        ),
        (
            "marking one up corrupts it",
            "the fence rule is gone, and the block is back to the state "
            "round 2 found: an exemption marker illustrated inside the one "
            "region the checker reads as a quotation, where nothing reads it "
            "and the smith pastes it into the fix",
        ),
        (
            "second arm",
            "the identifier rule's second half is unstated, so a reviewer "
            "quoting a host meets the domain arm of the same module with no "
            "warning and no way through",
        ),
    ):
        assert needle in section, f"agents/warden.md §Report: {why}"


def test_the_record_and_the_report_are_told_apart(repo):
    """The distinction the change turns on, in the documents that state it.

    Both sentences used to read as one prohibition -- the reviewer writes
    nothing under the work item -- which is why the missing half of the
    convention read as forbidden rather than as absent. The record stays the
    orchestrator's; the report is the reviewer's own artifact.
    """
    warden = read(*WARDEN)
    skill = read(*SKILL)
    for text, where in ((warden, WARDEN), (skill, SKILL)):
        assert "round-N-report.md" in text or "round-<n>-report.md" in text, (
            f"{'/'.join(where)} does not name the report, so nothing there "
            "distinguishes it from the record"
        )
    # The record's owner is unchanged, and saying so is what keeps the new
    # permission from being read as a general one.
    assert "round_record.py new` writes the record" in warden

    protocol = read(*PROTOCOL)
    assert "round-N.md" in protocol
    # `rounds/` holds more than records, and a reader that takes directory
    # membership for record-ness is the failure two of this repository's own
    # tests exist because of.
    assert "by name" in protocol, (
        "docs/review-handoff-protocol.md §Layout no longer says a record is "
        "selected by name; its diagram then reads as the whole of what "
        "`rounds/` holds, which it is not"
    )


def test_the_generator_documents_the_default_in_its_own_help():
    """`--help` is where an orchestrator looks, and it names the path.

    A default nobody can see is a default nobody uses, and this one exists
    to stop a person typing a path at all.
    """
    r = subprocess.run(
        [sys.executable, GENERATOR, "new", "--help"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    flat = " ".join(r.stdout.split())
    assert "round-<N>-report.md" in flat, flat
    assert os.path.join("rounds") in flat or "rounds/" in flat, flat
