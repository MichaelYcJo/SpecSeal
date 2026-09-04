"""The floor and the depth, executed — what `chain_check.py` refuses.

Phases 1 and 2 wrote both rules down. A rule no check reads is true only while
somebody is awake, which is the one question this work item was asked and
answered before its first edit: `CLAUDE.md`'s goal is verification that runs
unattended. These are the cases that make the two rows enforceable.

  Loses a record or crashes   absent (after the cutoff) fails; empty, or a
                              value that is neither `no` nor `yes — <what>`,
                              fails on ANY record. `no` with two or more later
                              round records fails — the run went past its own
                              stopping rule
  New units                   every entry carries the depth it was added at.
                              An entry without one fails; depth 2 or above
                              fails and the failure names where the unit goes
                              instead, because a refusal that names no exit
                              stops the chain at a wall

Both are grandfathered by the work item's own id — `FLOOR_FROM` and
`DEPTH_FROM`, the shape `STRICT_FROM` and `SURFACE_FROM` already carry and for
the reasoning recorded there: a merged record has no honest repair, and a check
whose first production act is red on history nobody can fix is a check people
learn to skip.

The sibling prose cases live in `tests/test_the_run_stops_at_the_last_finding.py`
(the floor, in the four files that state it) and
`tests/test_a_fix_pass_may_add_a_unit.py` (the depth, and its exit's position).
What is here is execution: a fixture repository, the checker run on it, and the
exit code read.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")

# A work item begun before every cutoff in this file: a missing row prints.
OLD_ITEM = "seal/specs/1787700000-a-work-item"
# One begun after all of them: a missing row fails. The two differ only in the
# second their names start with, which is the whole of what the
# grandfathering reads.
NEW_ITEM = "seal/specs/1799000000-a-later-work-item"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_module():
    """`chain_check.py` itself, for the two cutoffs — typed here, the boundary
    cases would pin a number instead of the boundary."""
    return _load("specseal_floor_check_for_tests", CHECK)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
    """The file as one line, so a pinned phrase survives re-wrapping."""
    return " ".join(read(*parts).split())


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(repo, message):
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.email=e@example.com",
        "-c",
        "user.name=e",
        "commit",
        "-qm",
        message,
    )
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def _build(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _template(tmp_path_factory):
    d = tmp_path_factory.mktemp("floor-and-depth-template") / "repo"
    _build(d)
    return d


@pytest.fixture
def repo(tmp_path, _template):
    d = tmp_path / "repo"
    shutil.copytree(_template, d)
    return d


def declaration(item):
    return (
        f"# {os.path.basename(item)} — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Branch | feature |\n"
    )


def record(sha, floor="no", new_units="none", needs="no"):
    """A record that passes every check but the row each case is about.

    The verdict closes without a fix and `Fixes checked by` says so, so `Pass`
    beside `nobody` never fires; `Contract changes` is `none` for the same
    reason. `floor=None`, `new_units=None` and `needs=None` leave the row out
    entirely, which is the state the grandfathering decides.

    `needs` defaults to `no` because the floor's run-length bound reads it:
    a round that reopened the run is where the count stops, so a fixture that
    left the row out would be testing the grandfathering rather than the
    bound.
    """
    rows = (
        "| Fixes checked by | no fixes to check |\n"
        "| Contract changes | none |\n"
        # `Ran by` for the reason `Contract changes` is here: `NEW_ITEM`
        # began after `chain_check.RUNNER_FROM`, so leaving it out would fail
        # every record in this file for a rule it does not pin.
        "| Ran by | specseal:warden on a model |\n"
    )
    if new_units is not None:
        rows += f"| New units | {new_units} |\n"
    if needs is not None:
        rows += f"| Needs a fix | {needs} |\n"
    if floor is not None:
        rows += f"| Loses a record or crashes | {floor} |\n"
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n{rows}\n"
        "- [x] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        "| 🟢 1 | something | `f.py:1` | answered | grounds |\n"
    )


def run(repo, draft=None):
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    if draft is not None:
        path = repo / "event.json"
        path.write_text(json.dumps({"pull_request": {"draft": draft}}), "utf-8")
        env["GITHUB_EVENT_PATH"] = str(path)
    r = subprocess.run(
        [sys.executable, CHECK, "--baseline", "base", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env=env,
    )
    return r.returncode, r.stdout + r.stderr


def declared(repo, item, *bodies):
    """The declaration, then one record per body, each in its own commit.

    Each record is handed the HEAD that existed before it, so round 2's
    `Target SHA` is a descendant of round 1's — what a real run looks like,
    since the fixes are what moved HEAD between the rounds.
    """
    write(repo, f"{item}/routing.md", declaration(item))
    sha = commit(repo, "declare")
    for number, body in enumerate(bodies, start=1):
        write(repo, f"{item}/rounds/round-{number}.md", body(sha))
        sha = commit(repo, f"round {number}")
    return sha


# --- the floor row is read on every record ----------------------------------


def test_a_record_without_the_floor_row_fails(repo):
    """The cap is a ceiling, and a record that does not answer the floor
    leaves the run with nothing under it — which is the state #81 spent three
    rounds in."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, floor=None))
    code, out = run(repo)
    assert code == 1, out
    assert "Loses a record or crashes" in out
    assert "floor" in out, (
        "the failure has to say what the row is FOR — the cap is a ceiling, "
        "and this row is the only thing under it"
    )


def test_records_predating_the_floor_print_rather_than_fail(repo):
    """The grandfathering, which is what keeps every merged record in this
    repository green. A record written before the rule has no honest repair:
    the round it describes is over."""
    declared(repo, OLD_ITEM, lambda sha: record(sha, floor=None))
    code, out = run(repo)
    assert code == 0, out
    assert "Loses a record or crashes" in out, (
        "passing in silence would hide the state the row exists to surface"
    )


def test_a_work_item_begun_at_the_floor_cutoff_is_held_to_the_rule(repo):
    """`>=`, and the item on the boundary is the one that wrote the rule —
    read from the module so a moved cutoff moves this case with it."""
    began = check_module().FLOOR_FROM
    declared(
        repo,
        f"seal/specs/{began}-the-item-that-wrote-the-rule",
        lambda sha: record(sha, floor=None),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "Loses a record or crashes" in out


def test_a_work_item_with_no_timestamp_prefix_is_grandfathered(repo):
    """No date to compare — failing would fail a naming convention."""
    declared(
        repo,
        "seal/specs/a-work-item-with-no-date",
        lambda sha: record(sha, floor=None),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_no_prefix_item_is_excused_all_four_refusals_not_only_the_absent_row(repo):
    """🟡 7 of round 1. `item_began` answers None for a work item named some
    other way, and None is below every cutoff — so the depth, the run-length
    bound and the missing rows are all excused, permanently and for every
    record. That follows from the recorded reasoning and is not disputed; a
    reader of the two tables in `docs/review-chain-spec.md` had no way to
    learn it, which the prose case below now pins.
    """
    declared(
        repo,
        "seal/specs/a-work-item-with-no-date",
        lambda sha: record(sha, floor="no", new_units="`helper`, `another`"),
        lambda sha: record(sha, floor="no"),
        lambda sha: record(sha, floor="no"),
    )
    code, out = run(repo)
    assert code == 0, out
    assert "at most one more" in out and "depth" in out, (
        "both states have to print — a no-prefix item that passes in silence "
        "is a work item nothing will ever say anything about"
    )


def test_a_draft_pull_request_is_not_excused_the_floor(repo):
    """The `Pass` excuse does not reach here, exactly as it does not reach the
    fix-surface rows: a round that has run has an answer, so a missing row is
    missing at every stage of a run."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, floor=None))
    code, out = run(repo, draft=True)
    assert code == 1, out
    assert "Loses a record or crashes" in out


# --- what the floor cell may say --------------------------------------------


def test_no_is_an_answer(repo):
    declared(repo, NEW_ITEM, lambda sha: record(sha, floor="no"))
    code, out = run(repo)
    assert code == 0, out


def test_yes_with_what_is_an_answer(repo):
    """Backticks and an em dash are how every document shows the value."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="`yes` — the export drops a record"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_an_empty_floor_cell_fails_on_any_record(repo):
    """Unlike the absent row, an empty one is always the author's to fill —
    the split `fix_surface` already makes, so the grandfathering does not
    reach it."""
    declared(repo, OLD_ITEM, lambda sha: record(sha, floor=""))
    code, out = run(repo)
    assert code == 1, out
    assert "empty" in out


def test_a_value_outside_the_vocabulary_fails_on_any_record(repo):
    """`CLOSED_WORDS` takes this direction for a verdict cell and this row
    takes it too: a word the check cannot read is never the reassuring
    reading. `probably not` would otherwise stop a run."""
    declared(repo, OLD_ITEM, lambda sha: record(sha, floor="probably not"))
    code, out = run(repo)
    assert code == 1, out
    assert "neither answer" in out


def test_yes_without_what_fails(repo):
    """The same refusal `nobody` takes for a reason it does not give: without
    it the cell records that something was found and not what."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, floor="yes"))
    code, out = run(repo)
    assert code == 1, out
    assert "does not say what" in out


def test_yes_with_a_separator_and_nothing_after_fails(repo):
    """`yes —` is the half-written cell, and it is the one that survives a
    reason read loosely: the value is not the bare word, so an equality test
    passes it, and what follows the separator is empty. Found by mutation —
    replacing the reason with a constant left every other case green."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, floor="yes —"))
    code, out = run(repo)
    assert code == 1, out
    assert "does not say what" in out


def test_a_word_that_merely_starts_with_no_is_not_a_no(repo):
    """The separator boundary `says_none` and `nobody_reason` both use.
    `nothing anybody can see` reads as a `no` to a prefix match, and it is a
    sentence rather than an answer."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="nothing anybody can see"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "neither answer" in out


# --- a record that met the floor is followed by at most one more -------------


def test_one_record_may_follow_a_record_that_met_the_floor(repo):
    """The verifying round, which the floor has to leave standing. Refusing it
    would refuse the round that ends a run honestly."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="no"),
        lambda sha: record(sha, floor="no"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_three_quiet_rounds_after_the_floor_are_still_refused(repo):
    """The run carrying on past its own stopping rule, which is the whole of
    what #110 measured: rounds 5, 6 and 7 of #81 came after a round that had
    already met the floor. None of the three reopened the run.

    **This pin changed at round 1 of this work item, deliberately.** It used
    to be `test_a_second_record_after_the_floor_fails` and it refused ANY two
    later records, which refused the only legal end to a run whose verifying
    round produces fixes. What it pins now is narrower and is the #81 shape
    itself: two later records, neither of which says the run reopened. The
    case below is the sequence the old pin forbade.
    """
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="no", needs="no"),
        lambda sha: record(sha, floor="no", needs="no"),
        lambda sha: record(sha, floor="no", needs="no"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "at most one more" in out
    assert "deferred with a named answerer" in out and "issue" in out, (
        "the refusal has to name where the stopped round's other findings go, "
        "or the run is stopped at a wall"
    )


def test_the_verifying_round_may_reopen_the_run_and_its_fixes_get_a_reader(repo):
    """🔴 1 of round 1, and the sequence the documents require.

    Round 1 meets the floor. The verifying round reads its fixes and opens
    something — `skills/code-review/SKILL.md` says a verifying round that
    opens something IS a finding round — so ITS fixes need a reader in turn,
    and that reader is a third record. Counting later records blindly made
    that sequence unwritable, which is the wall this branch exists not to
    build.

    The count stops at the first later record whose `Needs a fix` says the
    run reopened, because everything after that record answers to it rather
    than to the round that met the floor.
    """
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="no", needs="yes — three 🔴"),
        lambda sha: record(sha, floor="no", needs="yes — one, inside the fixes"),
        lambda sha: record(sha, floor="no", needs="no"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_reopening_further_down_does_not_excuse_the_two_before_it(repo):
    """The count stops at the FIRST reopening, not at any reopening. Two
    quiet rounds followed by a third that reopens is still the run going on
    past its floor — the reopening cannot reach back and license the rounds
    that preceded it."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="no", needs="no"),
        lambda sha: record(sha, floor="no", needs="no"),
        lambda sha: record(sha, floor="no", needs="yes — something late"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "at most one more" in out


def fixed_record(sha, verdict, checker):
    """`record()` with the one thing it cannot say: a verdict cell that
    closed on a fix, and the `Fixes checked by` that goes with it.

    `record()` hard-codes `answered` and `no fixes to check`, which is the
    shape every other case in this file needs. The floor's second stop
    condition is about the other shape — a record whose reviewer answered
    `no` and whose table nonetheless says `**fixed**`, because the
    orchestrator fixed what the reviewer said could be answered with grounds.
    """
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n"
        f"| Fixes checked by | {checker} |\n"
        "| Contract changes | none |\n"
        "| Ran by | specseal:warden on a model |\n"
        "| New units | none |\n"
        "| Needs a fix | no |\n"
        "| Loses a record or crashes | no |\n\n"
        "- [ ] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| 🟡 1 | a count that ships | `seal/ledger/x.md:4` | {verdict} | grounds |\n"
    )


def test_a_round_that_fixed_over_a_no_is_where_the_count_stops(repo):
    """Round 7's 🔴 1 of this work item, and the sequence that had no legal
    spelling.

    Round 1 meets the floor. Round 2 is its verifying round; the reviewer
    answers `Needs a fix: no`, judging its one 🟡 answerable with grounds. The
    orchestrator fixes it anyway — the finding was a false count that
    `fold_ledger.py` ships into the shared ledger — commits the fix, and sets
    the verdict to `**fixed**`. Those fixes owe a reader, so round 3 reads
    them and opens nothing.

    Before this case the walk read only `Needs a fix`, which is the REVIEWER's
    answer to what it opened; round 2 says `no`, so round 3 counted as a
    second uncounted record after the floor and `round-1.md` was refused.
    Ending at round 2 was refused both ways too — `no fixes to check` beside a
    `fixed` verdict, `nobody` beside a ticked `Pass`. The record already
    carries the missing fact in its verdict column, and the walk now reads it.
    """
    write(repo, f"{NEW_ITEM}/routing.md", declaration(NEW_ITEM))
    base = commit(repo, "declare")
    write(repo, f"{NEW_ITEM}/rounds/round-1.md", record(base, floor="no", needs="no"))
    one = commit(repo, "round 1")
    # The record is ADDED before its fix exists, with the verdict open --
    # the ordering rule refuses the other sequence.
    write(
        repo,
        f"{NEW_ITEM}/rounds/round-2.md",
        fixed_record(one, "open", "nobody — the fixes are not yet written"),
    )
    commit(repo, "round 2, its verdict open")
    write(repo, "note.md", "the count, corrected\n")
    fix = commit(
        repo, "the orchestrator fixes what the reviewer said could be answered"
    )
    write(
        repo,
        f"{NEW_ITEM}/rounds/round-2.md",
        fixed_record(one, f"**fixed** `{fix}`", "round-3"),
    )
    two = commit(repo, "round 2, its verdict filled")
    write(repo, f"{NEW_ITEM}/rounds/round-3.md", record(two, floor="no", needs="no"))
    commit(repo, "round 3, the reader")
    code, out = run(repo)
    assert code == 0, out


def test_wrote_fixes_reads_the_verdicts_and_not_the_needs_a_fix_row():
    """The predicate the walk's second stop rests on, pinned directly: a
    table of `answered` is not a fix, a table with one `fixed` is, and the
    `Needs a fix` row is not consulted either way. The first half is what
    keeps `test_three_quiet_rounds_after_the_floor_are_still_refused` red —
    three quiet rounds write nothing, so nothing stops the count."""
    check = check_module()
    reader = check.load(check.READER, "specseal_unverified_reader")
    answered = fixed_record("abc1234", "answered", "no fixes to check")
    fixed = fixed_record("abc1234", "**fixed** `abc1234`", "round-3")
    assert not check.closed_with_a_fix(reader, reader.readable(answered), "r.md")
    assert check.closed_with_a_fix(reader, reader.readable(fixed), "r.md")


def test_an_unreadable_needs_a_fix_does_not_stop_the_count(repo):
    """A row the checker cannot read must never be the thing that quiets a
    refusal — the declared failure direction is *blocks more*.

    Found by mutation: making `run_reopened` answer True for an unreadable
    row killed no case. It is only reachable where the unreadable row is
    itself refused, so the exit code alone cannot see it; what disappears is
    the run-past-the-floor message, and a reader who fixed the one error
    printed would never learn the run had gone past its floor.
    """
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="no", needs="no"),
        lambda sha: record(sha, floor="no", needs="probably"),
        lambda sha: record(sha, floor="no", needs="no"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "neither answer" in out, "the unreadable row is refused on its own"
    assert "at most one more" in out, (
        "the count treated a row it cannot read as a reopening, so the run "
        "that went past its floor was reported by nothing"
    )


def test_a_later_record_with_no_needs_a_fix_row_does_not_stop_the_count(repo):
    """The sibling of the unreadable-cell case, one state further out. An
    ABSENT row answers None the same way an unreadable one does, and None
    counts as NOT reopening — otherwise leaving the row out would be the way
    to buy extra rounds, which is the direction `plan.md` forbids."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="no", needs="no"),
        lambda sha: record(sha, floor="no", needs=None),
        lambda sha: record(sha, floor="no", needs="no"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "no readable" in out, "the absent row is refused on its own"
    assert "at most one more" in out, (
        "the count treated a row that is not there as a reopening, so the "
        "run that went past its floor was reported by nothing"
    )


def test_a_record_that_found_something_may_be_followed_by_more(repo):
    """`yes` leaves the cap to decide, so three rounds after it are the cap
    working rather than the floor being ignored."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="yes — the export drops a record"),
        lambda sha: record(sha, floor="yes — it still does"),
        lambda sha: record(sha, floor="no"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_the_last_record_meeting_the_floor_is_never_the_failure(repo):
    """A run that stopped at its floor has one record after it and no more —
    and the record that met it is the second-to-last, never the last. A check
    counting the wrong end would fail every correctly stopped run."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="yes — the export drops a record"),
        lambda sha: record(sha, floor="no"),
        lambda sha: record(sha, floor="no"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_a_run_past_the_floor_prints_for_an_item_begun_before_it(repo):
    """The grandfathering reaches this one too, and it is not the
    present-and-malformed case: the repair is a round that was never spawned,
    which nobody can write now."""
    declared(
        repo,
        OLD_ITEM,
        lambda sha: record(sha, floor="no"),
        lambda sha: record(sha, floor="no"),
        lambda sha: record(sha, floor="no"),
    )
    code, out = run(repo)
    assert code == 0, out
    assert "at most one more" in out


# --- `Needs a fix` is now a row a check reads -------------------------------


def test_a_record_without_the_needs_a_fix_row_fails(repo):
    """The bound above rests on this row, so a record that leaves it out
    leaves the bound resting on nothing. Before round 1 the row was read by
    no check at all — `grep -rn "Needs a fix"` over the checkers returned
    nothing — and `templates/sdd-round.md` said so of itself."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, needs=None))
    code, out = run(repo)
    assert code == 1, out
    assert "Needs a fix" in out
    assert "reopened" in out, (
        "the failure has to say what the row is FOR — it is what lets the "
        "floor's bound tell a verifying round from a run that ran on"
    )


def test_an_unreadable_needs_a_fix_fails_after_the_cutoff(repo):
    declared(repo, NEW_ITEM, lambda sha: record(sha, needs="probably"))
    code, out = run(repo)
    assert code == 1, out
    assert "neither answer" in out


def test_an_empty_needs_a_fix_cell_gets_the_sentence_an_empty_cell_gets(repo):
    """Round 2's 🟡 3. It printed ``is ``, which is neither answer`` — empty
    backticks, and a value quoted where there is none.

    The floor row two functions away has said *a row that says nothing
    answers nothing* since it shipped, and these two rows read the same
    vocabulary. Two answers to one state at two qualities is the drift this
    file closes everywhere else, and this is a line a person reads and acts
    on."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, needs=""))
    code, out = run(repo)
    assert code == 1, out
    assert "`Needs a fix` is empty" in out
    assert "answers nothing" in out
    assert "is ``," not in out, (
        "the empty cell is still quoted as though it held a value, which is "
        "the message the finding is about"
    )


@pytest.mark.parametrize("value", (None, "probably", ""))
def test_the_whole_needs_a_fix_row_is_grandfathered_not_only_its_absence(repo, value):
    """This row is grandfathered differently from the floor and the fix
    surface, and the difference is the point.

    Those two arrived with their checks, so a row present on a later record
    was written by an author who knew one would read it, and malformed meant
    careless. `Needs a fix` has existed since draft 0.5 with no check on it,
    so a value written before round 1 of this work item was never held to a
    vocabulary. Refusing those would fail records for a rule that did not
    exist when they were written, which is the grandfathering's whole reason.
    """
    declared(repo, OLD_ITEM, lambda sha: record(sha, needs=value))
    code, out = run(repo)
    assert code == 0, out
    assert "Needs a fix" in out, (
        "passing in silence would hide the state the row is read for"
    )


def test_a_work_item_begun_at_the_needs_cutoff_is_held_to_the_rule(repo):
    began = check_module().NEEDS_FROM
    declared(
        repo,
        f"seal/specs/{began}-the-item-that-wrote-the-rule",
        lambda sha: record(sha, needs=None),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "Needs a fix" in out


def test_needs_a_fix_takes_a_reason_after_either_answer(repo):
    """Every one of the 77 records in this repository spells it one of these
    two ways, and a check that refused a reason after `no` would refuse
    `no — the two this round opened are a comment and a docstring`, which is
    a real record."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, needs="`no` — both were answered with grounds"),
    )
    code, out = run(repo)
    assert code == 0, out


# --- every `New units` entry carries its depth ------------------------------


def test_a_unit_without_its_depth_fails(repo):
    """The row named the units and nothing else, which is what let a
    second-level unit ship with nobody able to see that it was one."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, new_units="`helper`"))
    code, out = run(repo)
    assert code == 1, out
    assert "`helper`" in out, "the failure has to name the entry"
    assert "unit (depth 1)" in out, (
        "the failure has to show the shape, or the author guesses it"
    )


def test_a_unit_at_depth_one_passes(repo):
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units="`helper` (depth 1)"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_the_form_the_template_shows_passes(repo):
    """Copied from `templates/sdd-round.md`'s filled-in cell. A template whose
    own example the check refuses is a record every session writes wrong."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(
            sha,
            new_units="configured_language (depth 1); mirror_to_refuse (depth 1)",
        ),
    )
    code, out = run(repo)
    assert code == 0, out


@pytest.mark.parametrize("value", ("none", "none — the fixes are not yet written"))
def test_none_survives_the_depth(repo, value):
    """`none` was an answer before the depth arrived and stays one, with or
    without a reason. The template case of the same name pins the row; this
    one pins the check."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, new_units=value))
    code, out = run(repo)
    assert code == 0, out


@pytest.mark.parametrize("depth", ("2", "3"))
def test_a_unit_below_the_first_level_fails_and_names_the_exit(repo, depth):
    """A fix pass may add a unit; that unit's fix may not. The exit is half of
    the refusal — phase 2 shipped before phase 3 so that this message would
    have somewhere to point."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units=f"`pin_the_pin` (depth {depth})"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "`pin_the_pin`" in out, "the failure has to name the entry"
    assert "deferred with a named answerer" in out and "issue" in out, (
        "a refusal that does not name where the refused work goes stops the "
        "chain at a wall"
    )


def test_a_depth_below_one_is_not_a_depth(repo):
    """`(depth 0)` parses and names no level the rule defines. Read
    permissively it is under the bound and passes, which is the tolerant read
    every other vocabulary in this file refuses."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units="`helper` (depth 0)"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "depth 1" in out


def test_a_digit_in_the_unit_name_is_not_a_depth(repo):
    """`sha256_of` carries a number and no depth, and a check that looks for
    a number rather than for the marked form reads it as depth 256 — which is
    over the bound, so the tolerant read here fails in the WRONG direction as
    well. Found by mutation: degrading the pattern to `(\\d+)` left every
    other case green, because no fixture had a digit in a unit name."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, new_units="`sha256_of`"))
    code, out = run(repo)
    assert code == 1, out
    assert "without the depth" in out, (
        "the entry has no depth, so the failure is the missing one and never "
        "a level read out of the name"
    )


def test_a_comma_separated_list_under_one_depth_is_refused(repo):
    """🟡 5 of round 1. `;` is the separator, so a comma list is ONE entry to
    the walk and one `(depth 1)` at its end covers every name in it.

    The comma form is not hypothetical: it is the spelling `New units` used
    before this branch, and `tests/test_the_fixes_name_their_surface.py` had
    a fixture written that way that this branch had to migrate.
    """
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units="`a`, `b` (depth 1)"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "one depth per unit" in out, (
        "the failure has to say the separator is `;`, or the author writes "
        "the same cell again"
    )


def test_two_depth_markers_in_one_entry_are_refused(repo):
    """The walk took the first marker and stopped, so a doubled marker
    declared whichever depth came first."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units="helper (depth 1) (depth 2)"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "one depth per unit" in out


def test_a_comma_inside_a_reason_after_none_is_not_a_list(repo):
    """`none, nothing added` is a `none` with a reason and never reaches the
    walk — `says_none` short-circuits first. The comma refusal must not take
    the value the sibling file already pins as an answer."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units="none, nothing added"),
    )
    code, out = run(repo)
    assert code == 0, out


@pytest.mark.parametrize("cell", ("`NONE` (depth 2)", "none (depth 2)"))
def test_a_unit_named_none_carrying_a_depth_is_a_unit(repo, cell):
    """Round 2's 🟡 2, and the other half of round 1's 🟡 6.

    `EMPHASIS` strips the backticks and `.lower()` strips the case, so
    `` `NONE` `` is the word `none`; the space before the marker is a
    separator, so the whole cell parsed as *none, with a reason* and the
    depth walk was never reached. A unit really named `NONE`, declared at a
    depth the rule refuses, passed.

    The guard is narrow on purpose: only a parenthesised `(depth N)` takes a
    cell out of `none`. A reason that merely says the word — `none — the
    depth was not recorded` — is still an answer, and the case below holds
    that.
    """
    declared(repo, NEW_ITEM, lambda sha: record(sha, new_units=cell))
    code, out = run(repo)
    assert code == 1, out
    assert "deferred with a named answerer" in out, (
        "the cell names a unit at depth 2 and was read as naming no units, "
        "so the refusal that should have fired did not"
    )


def test_a_reason_that_merely_says_the_word_depth_is_still_none(repo):
    """The absence half of the guard above: it keys on the parenthesised
    marker, not on the word, so an ordinary reason is untouched."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units="none — the depth was not recorded"),
    )
    code, out = run(repo)
    assert code == 0, out


def test_none_with_a_trailing_semicolon_is_still_none(repo):
    """🟡 6 of round 1, and the refusal's own instruction produced it: `none;`
    was refused as separators-with-nothing-between, and the message says to
    write the units or `none` with the entry shape — which a session read as
    `none (depth 1)`, a cell the check then reads as NO units at all."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, new_units="none;"))
    code, out = run(repo)
    assert code == 0, out


# The mirror of the arrow limit `fix_surface` records for `Contract changes`.
# The comma is found by substring ANYWHERE in the entry outside the depth
# marker — round 2's 🟡 9 found the sentence naming only a unit name, while a
# comma in a reason is refused too.
COMMA_LIMIT = "a comma anywhere in the entry outside the depth marker"
# The separator's own limit, which round 2's 🔴 1 hit before either of the
# other two could apply. `;` splits both rows before anything looks at code
# spans, so an entry describing the character splits itself.
SPLIT_LIMIT = "a literal semicolon inside a code span splits the entry"


@pytest.mark.parametrize(
    "cell", ("`get(a, b)` (depth 1)", "`helper` (depth 1) — adds a, b")
)
def test_the_recorded_limit_a_comma_outside_the_depth_marker(repo, cell):
    """The limit, executed, in both places a comma can sit: inside the unit
    name and inside the reason after it. Round 2's 🟡 9 is the second — the
    code refused it and the recorded sentence named only the first.

    If this case ever fails, the limit was closed — delete the sentence the
    case below pins."""
    declared(repo, NEW_ITEM, lambda sha: record(sha, new_units=cell))
    code, out = run(repo)
    assert code == 1, out
    assert "one depth per unit" in out


@pytest.mark.parametrize("limit", (COMMA_LIMIT, SPLIT_LIMIT))
def test_the_recorded_limits_are_recorded_where_the_rule_lives(limit):
    """A recorded limit that is recorded nowhere is a closed finding. The
    arrow's is stated in the checker and in the document that carries its
    refusals, and these two go in the same two places.

    `SPLIT_LIMIT` is the class round 2's 🔴 1 belongs to and the reason it is
    here: the branch recorded the arrow's limit and the comma's and said
    nothing about the separator that runs before both, so the record naming
    the fix surface was cut in half by the row it was describing."""
    for parts in (SPEC, CHECKER):
        assert limit in flat(*parts), "/".join(parts)


def test_one_entry_without_a_depth_fails_among_good_ones(repo):
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, new_units="`a` (depth 1); `b`"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "`b`" in out, "the failure has to name the entry"


def test_records_predating_the_depth_print_rather_than_fail(repo):
    """A work item begun after `SURFACE_FROM` and before `DEPTH_FROM` owes the
    `New units` row and not the depth in it. Its records were written when the
    row named units alone, and re-deriving a depth for fixes nobody re-read
    fabricates the answer."""
    began = check_module().DEPTH_FROM - 1
    declared(
        repo,
        f"seal/specs/{began}-an-item-between-the-two-cutoffs",
        lambda sha: record(sha, new_units="`helper`, `another`"),
    )
    code, out = run(repo)
    assert code == 0, out
    assert "depth" in out, (
        "passing in silence would hide the state the depth exists to surface"
    )


def test_a_work_item_begun_at_the_depth_cutoff_is_held_to_the_rule(repo):
    """`>=` again, and the item on this boundary is also the one that wrote
    the rule."""
    began = check_module().DEPTH_FROM
    declared(
        repo,
        f"seal/specs/{began}-the-item-that-wrote-the-rule",
        lambda sha: record(sha, new_units="`helper`"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "depth" in out


def test_a_second_level_unit_prints_for_an_item_begun_before_the_rule(repo):
    """The unit shipped, the round is over, and the repair — deferring it or
    opening an issue — was a decision available only while the run was
    running."""
    declared(
        repo,
        OLD_ITEM,
        lambda sha: record(sha, new_units="`pin_the_pin` (depth 2)"),
    )
    code, out = run(repo)
    assert code == 0, out
    assert "deferred with a named answerer" in out


# --- what the check does is written down where the check lives --------------

SPEC = ("docs", "review-chain-spec.md")
CHECKER = ("skills", "code-review", "scripts", "chain_check.py")


@pytest.mark.parametrize("cutoff", ("FLOOR_FROM", "DEPTH_FROM"))
def test_the_document_says_why_older_records_are_excused(cutoff):
    """A cutoff with no reason beside it reads as a leftover constant, and
    deleting one turns a release pull request red on merged history. The
    sibling case for `SURFACE_FROM` is the precedent, and it is in
    `tests/test_the_fixes_name_their_surface.py`."""
    for parts in (SPEC, CHECKER):
        assert cutoff in flat(*parts), (
            f"{'/'.join(parts)} does not name `{cutoff}`, so a reader who "
            "meets a record printing instead of failing cannot find out why"
        )
    spec = flat(*SPEC)
    assert "print" in spec and "grandfather" in spec


# Each new subsection of `docs/review-chain-spec.md`, bounded by the heading
# that follows it, so a claim about one table cannot be answered by the other.
SUBSECTIONS = {
    "the floor": (
        "##### The floor — `Loses a record or crashes`",
        "##### `Needs a fix` — the row the bound",
    ),
    "needs a fix": (
        "##### `Needs a fix` — the row the bound",
        "##### The depth in `New units`",
    ),
    "the depth": ("##### The depth in `New units`", "Which declaration applies"),
}


@pytest.mark.parametrize("which", sorted(SUBSECTIONS))
def test_each_table_says_a_no_prefix_work_item_is_excused(which):
    """🟡 7 of round 1. `item_began` answers None for a work item named some
    other way, and None is below every cutoff — so all four refusals are
    excused for it, permanently. The fix-surface table has said so since it
    shipped; these two said it of nothing.

    Sliced rather than searched whole, for the reason
    `test_the_exit_is_stated_before_the_rule` slices: one table carrying the
    sentence would answer a whole-file search for both.
    """
    text = flat(*SPEC)
    opening, closing = SUBSECTIONS[which]
    assert opening in text, f"the subsection opening moved: {opening!r}"
    assert closing in text, f"the subsection closing moved: {closing!r}"
    table = text[text.index(opening) : text.index(closing, text.index(opening))]
    assert "no timestamp prefix" in table, (
        f"{which}'s table never says a work item named some other way is "
        "excused, so a reader learns it only by running the checker"
    )


def test_the_document_states_what_each_refusal_does():
    """The gate's verdict is what a person reads and acts on, so the two
    tables that say which shapes fail and which print are part of the change
    rather than a description of it."""
    spec = flat(*SPEC)
    for phrase in (
        "with two or more later round records",
        "an entry at depth 2 or above",
        "deferred with a named answerer, or an issue",
    ):
        assert phrase in spec, (
            f"`docs/review-chain-spec.md` does not say what the check makes "
            f"of {phrase!r}, which leaves the refusal readable only in the "
            "failure it prints"
        )


def test_the_module_docstring_names_what_the_checker_refuses():
    """🟡 8 of round 1. The docstring is the checker's own inventory of what
    a record owes, and a reader who opened it to find out learned neither
    rule — `Loses a record or crashes` first appeared 130 lines below it, as
    a constant."""
    text = flat(*CHECKER)
    opening = text.index('"""')
    head = text[opening : text.index('"""', opening + 3)]
    for phrase in ("Loses a record or crashes", "depth", "Needs a fix"):
        assert phrase in head, (
            f"the module docstring does not name {phrase!r}, so the file's "
            "own summary of what it refuses is missing a refusal it makes"
        )


# The claim each file used to make about `Needs a fix`, beside the sentence
# that replaced it. The pair is phase 2's lesson: an absence is trivially
# satisfied by a file that was never opened, so the present half is what
# makes the absent half evidence.
NO_CHECK_READS = {
    ("templates", "sdd-round.md"): (
        "No check reads this row.",
        "read by `chain_check.py`",
    ),
    ("skills", "code-review", "SKILL.md"): (
        "No check reads the row;",
        "read by `chain_check.py`",
    ),
}


@pytest.mark.parametrize("parts", sorted(NO_CHECK_READS))
def test_no_document_still_says_the_row_is_read_by_nothing(parts):
    """It was true when it was written and round 1's repair made it false.
    A file that keeps the old sentence beside the new one ships two answers,
    and this row's own history is why that matters: the sentence is what a
    reader consults before deciding the cell can hold anything."""
    gone, stands = NO_CHECK_READS[parts]
    text = flat(*parts)
    assert stands in text, (
        f"{'/'.join(parts)} does not say the row is read, so the absence "
        "below is a search that found nothing rather than a file that says "
        "nothing"
    )
    assert gone not in text, (
        f"{'/'.join(parts)} still tells a reader no check reads `Needs a "
        "fix`, beside a bound that now rests on it"
    )


# --- the two cutoffs are this work item's own id ----------------------------


def test_the_two_cutoffs_are_the_id_of_the_item_that_wrote_them():
    """The whole of what "a fresh install creates every work item after it"
    rests on, and the convention `STRICT_FROM` and `SURFACE_FROM` set.

    No number is typed here. The claim is that both cutoffs are ONE work
    item's id and that the work item is in the tree — a constant with a digit
    wrong names a directory nobody has, and one copied from another rule's
    cutoff excuses the very records that were written to be held.
    """
    module = check_module()
    assert module.FLOOR_FROM == module.DEPTH_FROM == module.NEEDS_FROM, (
        "the floor, the depth and `Needs a fix` shipped in one work item, so "
        "two different cutoffs mean one of them names an item that did not "
        "write its rule. `NEEDS_FROM` may never be LATER than `FLOOR_FROM` "
        "for a second reason: between the two, the floor's run-length bound "
        "would rest on a row no record was required to carry"
    )
    items = os.listdir(os.path.join(ROOT, "seal", "specs"))
    assert [d for d in items if d.startswith(f"{module.FLOOR_FROM}-")], (
        "the cutoffs name a work item whose directory is not in the tree, so "
        "the first records held to both rules are nobody's"
    )
