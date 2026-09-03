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


def record(sha, floor="no", new_units="none"):
    """A record that passes every check but the row each case is about.

    The verdict closes without a fix and `Fixes checked by` says so, so `Pass`
    beside `nobody` never fires; `Contract changes` is `none` for the same
    reason. `floor=None` and `new_units=None` leave the row out entirely,
    which is the state the grandfathering decides.
    """
    rows = "| Fixes checked by | no fixes to check |\n| Contract changes | none |\n"
    if new_units is not None:
        rows += f"| New units | {new_units} |\n"
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


def test_a_second_record_after_the_floor_fails(repo):
    """The run carrying on past its own stopping rule, which is the whole of
    what #110 measured: rounds 5, 6 and 7 of #81 came after a round that had
    already met the floor."""
    declared(
        repo,
        NEW_ITEM,
        lambda sha: record(sha, floor="no"),
        lambda sha: record(sha, floor="no"),
        lambda sha: record(sha, floor="no"),
    )
    code, out = run(repo)
    assert code == 1, out
    assert "at most one more" in out
    assert "deferred with a named answerer" in out and "issue" in out, (
        "the refusal has to name where the stopped round's other findings go, "
        "or the run is stopped at a wall"
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
    assert module.FLOOR_FROM == module.DEPTH_FROM, (
        "the floor and the depth shipped in one work item, so two different "
        "cutoffs mean one of them names an item that did not write its rule"
    )
    items = os.listdir(os.path.join(ROOT, "seal", "specs"))
    assert [d for d in items if d.startswith(f"{module.FLOOR_FROM}-")], (
        "the cutoffs name a work item whose directory is not in the tree, so "
        "the first records held to both rules are nobody's"
    )
