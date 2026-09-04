"""A round record written after its own fixes, executed — what `chain_check.py`
refuses.

`templates/sdd-round.md` says a record is written *"right after it posts"*, and
until this work item nothing observed it. Issue #150 measured the orchestrator
stopping twice in a row, four minutes and two minutes after the fix commits
those records commissioned, and both times the reviewer's drafted replacement
text lived only in a report and the next segment rebuilt it from scratch.

**A record written late looks finished.** By the time it is committed the fixes
have landed, so its verdict cells read `fixed at <sha>` — which is exactly what
a correctly written record looks like after its own update pass. The two are
indistinguishable in the file, and distinguishable in git:

  the ADDING commit    descends from the fix  ->  written after the work it
                                                  commissioned
  the LAST commit      descends from the fix  ->  a correct record, updated in
                                                  place when the fixes landed

So the check reads the commit that ADDED the record, never the one that last
touched it. Refusing on the last commit would fail every well-written record,
and this file carries a case for that direction as well as for the defect.

Two more distinctions the cases pin, because each of them is a way to fail an
honest record:

  a fix the round did NOT commission — a verdict answering an earlier round's
  finding names a commit the round already reviewed, so it is an ancestor of
  this record's own `Target SHA` and says nothing about when the record was
  written

  a record this branch did not add — the adding commit is read in
  `<baseline>..HEAD`, so a record that arrived before the base makes no claim,
  the way a record the pull request does not touch already makes none

The grandfathering is the work item's own id, `ORDER_FROM`, the fifth cutoff of
the shape `STRICT_FROM`, `SURFACE_FROM`, `FLOOR_FROM`, `NEEDS_FROM` and
`RUNNER_FROM` already carry: a merged record has no honest repair — nobody can
commit it earlier now — and a check whose first production act is red on
history nobody can fix is a check people learn to skip.

Every case here was seen red at `fb52335`, before the check existed.
"""

import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")

# A work item begun before the cutoff: a late record prints.
OLD_ITEM = "seal/specs/1787700000-a-work-item"
# One begun after it: a late record fails. The two differ only in the second
# their names start with, which is the whole of what the grandfathering reads.
NEW_ITEM = "seal/specs/1799000000-a-later-work-item"

RUNNER = "specseal:warden on Opus 5 (1M context)"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_module():
    """`chain_check.py` itself, for the cutoff — typed here, the boundary
    case would pin a number instead of the boundary."""
    return _load("specseal_order_check_for_tests", CHECK)


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return handle.read()


def flat(*parts):
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
    d = tmp_path_factory.mktemp("record-order-template") / "repo"
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


def record(
    target,
    verdict="answered",
    checked_by="no fixes to check",
    severity="🟡",
    contract="none",
    units="none",
):
    """A record that passes every check but the one each case is about.

    `verdict` is the whole cell, so a case can write `**fixed** <sha>` or the
    `open` a record written on time carries before its fixes land. 🟡 rather
    than 🔴 so that an `open` verdict is not also an unanswered blocking
    finding, which is a different refusal.

    `contract` and `units` are the fix-surface cells, so a case can write the
    provisional `none — the fixes are not yet written` that every record now
    starts with.
    """
    return (
        "# a round\n\n"
        "| Field | Value |\n|---|---|\n"
        f"| Target SHA | {target} |\n"
        f"| Ran by | {RUNNER} |\n"
        f"| Fixes checked by | {checked_by} |\n"
        f"| Contract changes | {contract} |\n"
        f"| New units | {units} |\n"
        "| Needs a fix | no |\n"
        "| Loses a record or crashes | no |\n\n"
        "- [x] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| {severity} 1 | something | `f.py:1` | {verdict} | grounds |\n"
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


def touch(repo, text):
    """A commit that changes code — what a fix pass looks like to git."""
    write(repo, "f.py", text)
    return commit(repo, "fix")


def late_run(repo, item):
    """The defect, as a real run writes it: the fixes land, and only then is
    the record that commissioned them committed.

    Two records rather than one, because a verdict closed with a fix cannot
    say `no fixes to check` — the reader that refuses that pair is already
    shipped, and a fixture tripping it would test the wrong refusal.
    """
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    fix = touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict=f"**fixed** `{fix}`", checked_by="round-2"),
    )
    added = commit(repo, "round 1, written after its own fixes")
    write(repo, f"{item}/rounds/round-2.md", record(added))
    commit(repo, "round 2")
    return fix, added


# --- the refusal ------------------------------------------------------------


def test_a_record_added_after_its_own_fix_fails_after_the_cutoff(repo):
    """The refusal this half of the work item exists for."""
    fix, added = late_run(repo, NEW_ITEM)
    code, out = run(repo)
    assert code == 1, out
    assert "round-1.md" in out, out
    assert fix[:7] in out, "the failure does not name the commit it read"
    assert added[:7] in out, "the failure does not name the adding commit"


def test_the_failure_says_what_to_do_instead(repo):
    """A refusal that names no exit is a wall. The repair is a two-step
    habit, and it has to be in the message: commit the record with `open`
    cells, update it when the fixes land."""
    late_run(repo, NEW_ITEM)
    _code, out = run(repo)
    assert "open" in out and "update" in out, out


def test_a_late_record_only_prints_before_the_cutoff(repo):
    """A merged record has no honest repair — nobody can commit it earlier
    now — and a check whose first production act is red on history nobody
    can fix is a check people learn to skip."""
    late_run(repo, OLD_ITEM)
    code, out = run(repo)
    assert code == 0, out
    assert "round-1.md" in out, (
        "passing in silence would hide the state the check exists to surface"
    )
    assert "prints instead of failing" in out, out


def test_a_work_item_with_no_timestamp_prefix_is_grandfathered(repo):
    """`item_began` answers None for a work item named some other way, and
    None is below every cutoff — failing would fail a naming convention
    rather than a state anybody chose."""
    late_run(repo, "seal/specs/a-work-item-with-no-date")
    code, out = run(repo)
    assert code == 0, out
    assert "round-1.md" in out, out


def test_the_cutoff_is_the_work_items_own_second(repo):
    """The boundary, read off the module rather than typed — a literal here
    would pin the number and not the rule."""
    began = check_module().ORDER_FROM
    late_run(repo, f"seal/specs/{began}-the-item-that-added-the-rule")
    code, _out = run(repo)
    assert code == 1, (
        "the work item that ADDED the rule is the first one held to it, and "
        f"{began} is its own second — `>=`, not `>`"
    )


def test_the_cutoff_is_this_work_items_own_id():
    """The fifth cutoff takes the id of the work item that added it, like
    the four before it. A number typed from somewhere else grandfathers a
    stranger's records and holds none of its own."""
    module = check_module()
    assert module.ORDER_FROM == 1788501054
    assert module.ORDER_FROM > module.RUNNER_FROM, (
        "a cutoff added after `Ran by` cannot be earlier than it"
    )


# --- what must keep passing -------------------------------------------------


def test_a_record_updated_in_place_when_the_fixes_landed_passes(repo):
    """The direction that fails every well-written record if it is read
    wrong. A correct record is committed with `open` cells and updated to
    `fixed at <sha>` afterwards, so its LAST commit legitimately descends
    from the fix. The ADDING commit is the distinguishing one."""
    item = NEW_ITEM
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict="open", checked_by="round-2"),
    )
    added = commit(repo, "round 1, written right after it posted")
    fix = touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict=f"**fixed** `{fix}`", checked_by="round-2"),
    )
    updated = commit(repo, "round 1's verdicts, once the fixes landed")
    write(repo, f"{item}/rounds/round-2.md", record(updated))
    commit(repo, "round 2")
    code, out = run(repo)
    assert code == 0, out
    assert added not in out and "written after" not in out, (
        "the check read the commit that last TOUCHED the record, which every "
        "correct record has descending from its own fixes"
    )


def test_a_fix_this_round_did_not_commission_passes(repo):
    """A verdict answering an earlier round's finding names a commit this
    round already reviewed. It is an ancestor of this record's own
    `Target SHA`, so it says nothing about when the record was written — and
    reading it as a commissioned fix fails every second round of every run."""
    item = NEW_ITEM
    write(repo, f"{item}/routing.md", declaration(item))
    commit(repo, "declare")
    fix = touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(fix, verdict=f"**fixed** `{fix}`", checked_by="round-2"),
    )
    added = commit(repo, "round 1, reviewing the tree that already held the fix")
    write(repo, f"{item}/rounds/round-2.md", record(added))
    commit(repo, "round 2")
    code, out = run(repo)
    assert code == 0, out


def test_a_record_this_branch_did_not_add_makes_no_claim(repo):
    """The rebase answer, and the merged-record answer, in one rule: the
    adding commit is read in `<baseline>..HEAD`. A record that arrived before
    the base has no adding commit there, so nothing is claimed about it — the
    same `no claim` the reachability check already makes."""
    item = NEW_ITEM
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    fix = touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict=f"**fixed** `{fix}`", checked_by="round-2"),
    )
    added = commit(repo, "round 1, late — but on the base")
    write(repo, f"{item}/rounds/round-2.md", record(added))
    commit(repo, "round 2")
    git(repo, "branch", "-qf", "feature")
    git(repo, "switch", "-q", "feature")
    write(repo, "g.py", "y = 1\n")
    commit(repo, "the branch's own work")
    code, out = run(repo)
    assert code == 0, out


def test_a_record_added_before_the_base_and_updated_on_the_branch_passes(repo):
    """The case that separates *added* from *touched*, and the one the whole
    check rests on.

    A base that moves under a long-running branch takes the record's own
    adding commit out of `<baseline>..HEAD` and leaves the commit that
    updated its verdicts inside it — and that commit descends from the fix,
    because updating the verdicts is what a correct record does when the
    fixes land. Read as *any commit that touched the file*, this refuses a
    record that did everything right.

    **This case cannot be red at HEAD**: the behaviour it pins is already
    correct there. It is red only under the mutation that drops
    `--diff-filter=A`, which is how §15 was satisfied for it. Do not delete
    it as a case that never fails.

    **It was written when it was the ONLY case that mutation reached, and it
    is not any more.** Under the earliest add — the index round 1 inverted —
    a file added and then modified had the same oldest commit whether or not
    the flag was there, so this fixture's moving base was the only separator.
    Under the latest add the newest touching commit is the verdict update, so
    the ordinary updated-in-place case is red under the same mutation: round
    2 measured two cases red where round 1's battery saw one. Both are worth
    keeping, because they fail for different reasons — that one for a record
    updated on the branch, this one for a record whose add left the range.
    """
    item = NEW_ITEM
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict="open", checked_by="round-2"),
    )
    commit(repo, "round 1, written right after it posted")
    git(repo, "branch", "-qf", "feature")
    git(repo, "switch", "-q", "feature")
    fix = touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict=f"**fixed** `{fix}`", checked_by="round-2"),
    )
    updated = commit(repo, "round 1's verdicts, once the fixes landed")
    write(repo, f"{item}/rounds/round-2.md", record(updated))
    commit(repo, "round 2")
    code, out = run(repo)
    assert code == 0, out
    assert "was ADDED by" not in out, (
        "the commit that UPDATED the verdicts was read as the adding one, "
        "which refuses the record for doing exactly what a correct record does"
    )


def test_a_record_deleted_and_re_added_after_the_fix_is_judged_on_the_later_add(repo):
    """Round 1's 🟡 8. `--diff-filter=A` returns more than one commit exactly
    once — a delete-and-re-add — and that is the shape which makes a late
    record look early: a stub committed on time, removed, and the real record
    written after the fixes.

    The version anyone reads was authored at the LAST add, so that is the
    commit the refusal reads. Taking the first was the permissive direction
    and nothing held it: mutating `found[0]` to `found[-1]` left every other
    case in this file green, because a file added and then only modified has
    one add either way.

    What it costs, stated rather than hidden: a record accidentally deleted
    and restored after the fixes is refused, and the message names the
    restoring commit. The declared failure direction is *blocks more*, and
    the repair is visible in the failure.
    """
    item = NEW_ITEM
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict="open", checked_by="round-2"),
    )
    early = commit(repo, "round 1, a stub committed on time")
    (repo / item / "rounds" / "round-1.md").unlink()
    commit(repo, "round 1 removed")
    fix = touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict=f"**fixed** `{fix}`", checked_by="round-2"),
    )
    again = commit(repo, "round 1, written for real after the fixes")
    write(repo, f"{item}/rounds/round-2.md", record(again))
    commit(repo, "round 2")
    code, out = run(repo)
    assert code == 1, out
    assert again[:7] in out, (
        "the refusal read the FIRST add, which is the stub — a record whose "
        "content was written after the fixes passes on the strength of a "
        "commit that no longer holds any of it"
    )
    assert early[:7] not in out, out


def test_a_fix_sha_this_repository_cannot_see_makes_no_claim(repo):
    """After a squash or a rebase the commit a verdict names is gone, and a
    gone commit is `no claim` rather than a fault — the reading
    `resolves_to` already gives every other consumer.

    Stated rather than hidden: this is what makes a rebase unable to turn a
    passing record failing, and it is also why a rebase can turn a failing
    one passing. The safe direction is the one taken."""
    item = NEW_ITEM
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict="**fixed** `dead1234`", checked_by="round-2"),
    )
    added = commit(repo, "round 1")
    write(repo, f"{item}/rounds/round-2.md", record(added))
    commit(repo, "round 2")
    code, out = run(repo)
    assert code == 0, out


def test_a_verdict_that_closed_without_writing_anything_passes(repo):
    """`answered`, `withdrawn` and `not a defect` close a finding and produce
    no code, so there is no fix for a record to have been written after —
    whatever commit happens to sit in the cell."""
    item = NEW_ITEM
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    fix = touch(repo, "x = 2\n")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, verdict=f"answered, and see `{fix}`"),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out


# --- the fix surface the ordering rule made provisional ----------------------
#
# Round 2's 🟡 6, and the state is this branch's own doing. Before `ORDER_FROM`
# a record could be written after its fixes and its `Contract changes` / `New
# units` filled from the start; now the record is committed FIRST, so both
# rows begin at `none — the fixes are not yet written` and nothing required
# the second step. `says_none` accepts a reason, so a record that never got
# the reach-back reads exactly like one that did — which is this work item's
# own title, produced by this work item.
#
# The sibling cases for the rest of `fix_surface` are in
# `tests/test_the_fixes_name_their_surface.py`. These live here because the
# arm is keyed to `ORDER_FROM` and exists only because of the ordering rule.


def surface_run(repo, item, checked_by, contract="none", units="none"):
    """A two-record item whose FIRST record carries the fix-surface cells
    under test, with `Fixes checked by` saying whether a later round has
    opened its fixes."""
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        record(reviewed, checked_by=checked_by, contract=contract, units=units),
    )
    added = commit(repo, "round 1")
    write(repo, f"{item}/rounds/round-2.md", record(added))
    commit(repo, "round 2")
    return run(repo)


PENDING = "none — the fixes are not yet written"


def test_the_pending_spelling_is_the_one_the_template_prints():
    """The checker owns the phrase and the template shows it, so the two
    cannot drift. Read off the module rather than typed here — a literal
    would pin a string and not the tie between the two files."""
    not_yet = check_module().NOT_YET
    assert not_yet in flat("templates", "sdd-round.md"), (
        "the checker refuses a spelling the template never prints, so a "
        "session copying the template is refused for following it"
    )
    assert PENDING.endswith(not_yet), "this file's fixture drifted from the module"


def test_a_surface_still_pending_after_a_round_read_the_fixes_fails(repo):
    """The defect. `Fixes checked by` naming a round says a later round
    opened these fixes, so the fixes exist — and a cell two rows below still
    saying they are not yet written is false about a fact the same file
    states. The contradiction-inside-one-file shape `no fixes to check`
    beside a `fixed` verdict already takes."""
    code, out = surface_run(repo, NEW_ITEM, "round-2", units=PENDING)
    assert code == 1, out
    assert "New units" in out and "not yet written" in out, out
    assert "round-1.md" in out, out


def test_the_same_arm_reaches_contract_changes(repo):
    """Both rows or neither: `fix_surface` walks the two together and the
    argument for one is the argument for the other."""
    code, out = surface_run(repo, NEW_ITEM, "round-2", contract=PENDING)
    assert code == 1, out
    assert "Contract changes" in out and "not yet written" in out, out


def test_the_honest_mid_run_state_is_not_refused(repo):
    """**The direction that must keep passing**, and the one a careless
    refusal breaks: a record committed before its fixes, which is exactly
    what `ORDER_FROM` requires, says *not yet written* truthfully. Nothing
    has opened its fixes, `Fixes checked by` says `nobody`, and the cell is
    the honest value rather than an abandoned one."""
    code, out = surface_run(
        repo, NEW_ITEM, "nobody — this round's fixes are not written", units=PENDING
    )
    assert code == 0, out
    assert "still says the fixes are not yet written" not in out, (
        "the refusal fired on the state the ordering rule requires, which "
        "would refuse every correctly written record at the moment it lands"
    )


def test_a_bare_none_after_the_fixes_landed_passes(repo):
    """A fix pass may change no contract and add no unit — a deletion, a
    reworded message — so `none` after a round read the fixes is an answer
    and not an omission."""
    code, out = surface_run(repo, NEW_ITEM, "round-2")
    assert code == 0, out


def test_a_reason_the_checker_does_not_recognise_passes(repo):
    """The deliberate exception to this file's `blocks more` direction.

    A rule about which English sentences mean *not yet* is the enumeration
    over an unbounded domain the arrow's and the comma's limits decline, so
    an unrecognised reason is an answer. What is caught is the measured
    failure — the template's own words left standing.

    **The three cells after the first are the limit MEASURED rather than
    described** (round 3's 🟡 5). Each carries the template's words
    unchanged and each still escapes, because `says_none` tests the first
    character after `none` while `says_not_yet` strips `SEPARATORS` from
    both ends and then requires the constant to START what is left. The
    record said the escape was a rewording, and it is wider than that.

    The last of the three is also what holds the prefix rule (🟡 7).
    Substituting `NOT_YET in rest` for `startswith` turns it red; round 3
    found that mutation surviving all 164 cases with nothing here to kill
    it, which is round 1's 🟡 8 shape a third time.

    A distinct work item per spelling, because `surface_run` commits and a
    second call writing byte-identical files has nothing to commit. Each id
    is later than `ORDER_FROM`, which is the only thing about it that
    matters.
    """
    not_yet = check_module().NOT_YET
    spellings = (
        # An honest custom reason: what the `allow` direction exists for.
        "none — the fixes deleted a line",
        # A dash outside `SEPARATORS`. The leading space is what `says_none`
        # reads, and U+2015 survives the strip.
        f"none ― {not_yet}",
        # A doubled space INSIDE the phrase, which no widening of
        # `SEPARATORS` reaches.
        "none — " + not_yet.replace("the fixes", "the  fixes", 1),
        # Any clause in front of it.
        f"none — nothing yet, and {not_yet}",
    )
    for n, units in enumerate(spellings):
        code, out = surface_run(
            repo, f"seal/specs/179900000{n}-a-later-work-item", "round-2", units=units
        )
        assert code == 0, f"refused a cell it does not recognise, {units!r}:\n{out}"

    # Round 4's 🟡 3, as an assertion here rather than as a unit of its own:
    # the finding is INSIDE `says_not_yet`, which round 2's fix pass created,
    # so a new unit answering it would be depth 2. A bare `none` is what
    # `templates/sdd-round.md` prints, `says_none` answers True for it by
    # `s == NONE_WORD` with nothing after the word, and it reaches
    # `says_not_yet` with an empty `rest`. The docstring called both guards
    # duplicates that cannot change the answer; the `not rest` conjunct is
    # what keeps `rest[0]` from raising on the commonest cell there is.
    module = check_module()
    assert module.says_none("none") is True, (
        "the bare `none` route is what makes the separator guard load-bearing"
    )
    assert module.says_not_yet("none") is False, (
        "a bare `none` says nothing about whether the fixes exist yet"
    )
    for bare in ("none", "NONE", "`none`", "none.", "none;"):
        assert module.says_not_yet(bare) is False, (
            f"{bare!r} reached the separator guard with an empty tail and the "
            "guard did not hold — dropping `not rest` raises IndexError here"
        )

    # Round 4's 🟡 3 on the document side, in this same case for the same
    # reason: the corrected limit is a sentence a person reads and acts on
    # (§14), and a mutation battery reads a recorded limit as permission to
    # delete the line it describes.
    chain = flat("skills", "code-review", "scripts", "chain_check.py")
    assert "The separator guard does NOT" in chain, (
        "`says_not_yet` is back to calling both guards duplicates"
    )
    assert "prefix guard really is unreachable" in chain, (
        "the surviving half of the limit lost its statement"
    )


def test_a_forgotten_checker_cell_leaves_the_arm_nothing_to_key_on(repo):
    """Round 3's 🟡 1. The arm reads `Fixes checked by`, so the session that
    forgets the reach-back ENTIRELY — all three cells left where the template
    put them — is reached by nothing in `fix_surface` at all.

    That direction is forced rather than chosen: `nobody — <why>` beside a
    pending row is the state `ORDER_FROM` requires at the moment a record
    lands, and refusing it would refuse every correctly written record. What
    covers the state instead is `Fixes checked by`'s own notice, printed on
    every record, which is what this asserts is still there. The limit is
    written where a reader meets the refusal rather than closed, because
    closing it means keying the arm on a second source of truth.
    """
    code, out = surface_run(
        repo,
        NEW_ITEM,
        "nobody — this round's fixes are not yet written",
        contract=PENDING,
        units=PENDING,
    )
    assert code == 0, out
    assert "still says the fixes are not yet written" not in out, (
        "the arm fired on the state the ordering rule requires"
    )
    assert "opened by nobody" in out, (
        "nothing at all reports a record that forgot all three cells:\n" + out
    )
    for where in (
        ("docs", "review-chain-spec.md"),
        ("templates", "sdd-round.md"),
        ("skills", "code-review", "SKILL.md"),
    ):
        assert "the session that filled" in flat(*where), (
            f"{'/'.join(where)} describes the refusal without its limit, so a "
            "reader meets the rule and not what it does not reach"
        )


def test_the_terminal_value_is_in_the_specs_table_with_what_it_costs(repo):
    """Round 3's 🟡 3. `Fixes checked by` has three legal values and the
    spec's table for the pending arm enumerated two of them, omitting the one
    the TERMINAL record of every run carries.

    Not a hole in the checker — the run's legal ending is not refused, which
    this runs. What was missing is that the pair is WRONG rather than merely
    unrefused: a round commissioning no fixes will never have any, so *not
    yet written* beside it is false the moment it is written, and nothing
    said so anywhere. Whether to refuse it is `questions.md` Q4's sibling and
    is the repository owner's.
    """
    code, out = surface_run(repo, NEW_ITEM, "no fixes to check", units=PENDING)
    assert code == 0, out
    assert "still says the fixes are not yet written" not in out, out
    spec = flat("docs", "review-chain-spec.md")
    assert "`Fixes checked by` reads `no fixes to check`" in spec, (
        "the spec's table still enumerates two of the three legal values"
    )
    assert "will never have any" in spec, (
        "the table says the value passes and not why that is a limit"
    )


def test_the_declared_limit_names_what_escapes_with_the_words_unchanged():
    """Round 3's 🟡 5, on the document side. `docs/review-chain-spec.md`, the
    ledger row and the changelog fragment all declared the escape as **a
    rewording**, and three spellings escape with the template's words
    untouched. The case above runs them; this is the claim about them.

    **Pinned in all FIVE copies, and it used to pin three of them** (round
    4's 🟡 6). `phases/phase-7.md`'s own removal table names five places the
    rewording claim was written into, and this loop covered the spec, the
    ledger fragment and the changelog — leaving `chain_check.py#says_not_yet`
    and `overview.md` free to keep saying what was measured false. A case
    written to close *a correction reaches one copy and not the rest* was
    itself an instance of it.

    The measurement is one fact written into five places, so counting the
    copies is part of the claim: if a sixth copy is added, it is added here
    too.
    """
    item = "1788501054-a-check-reports-clean-while-something-is-missing"
    copies = (
        ("docs", "review-chain-spec.md"),
        ("skills", "code-review", "scripts", "chain_check.py"),
        ("seal", "ledger", f"{item}.md"),
        ("seal", "specs", item, "changelog.md"),
        ("seal", "specs", item, "overview.md"),
    )
    assert len(copies) == 5, "the removal table in phase-7.md names five copies"
    for where in copies:
        text = flat(*where)
        assert "wider than a rewording" in text, (
            f"{'/'.join(where)} still declares the escape as a rewording"
        )
        assert "doubled space" in text and "clause" in text, (
            f"{'/'.join(where)} names fewer than the three spellings measured"
        )


FIELD_ROW = re.compile(r"^\| ([A-Z][^|]*?) \| (.*) \|$")


def _field_cells(sha, rel):
    """The record's field table as it stood at `sha`, `{label: value}`."""
    text = git(ROOT, "--no-pager", "show", f"{sha}:{rel}").stdout
    cells = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        m = FIELD_ROW.match(line)
        if m and m.group(1).strip() != "Field":
            cells[m.group(1).strip()] = m.group(2).strip()
    return cells


CORRECTION_MARKER = "CORRECTED IN PLACE"


def _correction_traces(rel):
    """What the record's trailing comment records as corrected in place.

    Only the text AFTER `CORRECTED IN PLACE` counts. A cell name mentioned
    loosely elsewhere in the comment is not a trace, and every one of these
    records names its own cells in its ordinary reasoning — keying on the
    bare name would let a deleted trace pass.
    """
    text = read(*rel.split("/"))
    body = text.split("- [ ] Pass", 1)[-1].split("-->", 1)[0]
    if CORRECTION_MARKER not in body:
        return ""
    return " ".join(body.split(CORRECTION_MARKER, 1)[1].split())


def test_a_cell_corrected_after_the_record_landed_says_so_in_the_record():
    """Round 4's 🟡 7, as the class rather than the coordinate.

    `round-1.md`'s `Fixes checked by` was changed from `nobody — …` to
    `round-2` two rounds late, with no trace in the record — so a reader of
    that file cannot tell the reach-back was ever missing. Enumerating the
    class over git found two more in-place corrections and the round had
    named one of them.

    What this refuses is narrow on purpose: a cell that went from one
    ASSERTED value to a DIFFERENT asserted value. Filling a row that started
    `none — the fixes are not yet written`, or a `Fixes checked by` that
    started `nobody — <why>`, is the reach-back the ordering rule requires and
    the record announces of itself — not a correction, and not listed.

    The trace lives in the trailing HTML comment because three of these rows
    are parsed and a marker inside them changes what the checker reads. That
    is not a style preference: prose appended to `Fixes checked by` silences
    its arm, and a sentence added to `New units` is read as another entry,
    which made this repository's own suite red for a commit.

    Depth 1. The finding is in a record's cell and the fix is a template
    paragraph plus three record comments; no unit any fix pass on this run
    created is involved, so this is not a unit answering a finding inside
    one.
    """
    check = check_module()
    records = sorted(
        glob.glob(
            os.path.join(ROOT, "seal", "specs", "*", "rounds", "round-*.md"),
        )
    )
    assert records, "no round records found — the glob or the layout moved"

    untraced = []
    changes = 0
    for path in records:
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        shas = git(
            ROOT, "--no-pager", "log", "--format=%H", "--reverse", "--", rel
        ).stdout.split()
        if len(shas) < 2:
            continue
        comment = _correction_traces(rel)
        previous = _field_cells(shas[0], rel)
        for sha in shas[1:]:
            current = _field_cells(sha, rel)
            for label, value in current.items():
                was = previous.get(label)
                if was is None or was == value:
                    continue
                changes += 1
                # A pending row being filled is the reach-back, not a
                # correction. Both spellings of pending are excluded.
                if check.says_none(was) or check.nobody_reason(was) is not None:
                    continue
                if label not in comment:
                    untraced.append(f"{rel}: `{label}` corrected at {sha[:7]}")
            previous = current

    # A walk that reads no cell finds no correction and passes, which is the
    # counterfeit-seal shape: this repository's own records are edited after
    # they land — every one of them fills its two fix-surface rows — so a run
    # that sees zero changes is a broken reader, not a clean history.
    assert changes, (
        "the walk compared no field cells at all. `_field_cells` or the "
        "record layout moved, and with it every correction this case exists "
        "to catch"
    )

    assert not untraced, (
        "a field cell was corrected in place and the record does not say so. "
        "`templates/sdd-round.md` puts the trace in the trailing HTML comment "
        f"under `{CORRECTION_MARKER}` — naming the cell, what it said, what "
        "it says now and which round found it — because the cells themselves "
        "are parsed:\n  " + "\n  ".join(untraced)
    )


def test_the_template_puts_the_correction_trace_where_no_checker_reads_it():
    """The rule above, in the file that produces a record.

    A rule applied to four records and written nowhere is the shape
    `agent-contract`'s own preamble names: it goes missing without a trace.
    """
    template = flat("templates", "sdd-round.md")
    assert (
        "CORRECTED after this file is committed leaves its trace in the" in template
    ), "the template no longer says where a correction's trace goes"
    assert "never inside the cell" in template, (
        "the template no longer says the cell is the wrong place"
    )
    assert CORRECTION_MARKER in template, (
        "the template no longer names the one spelling a trace opens with, "
        "so a cell name mentioned loosely would read as a trace"
    )
    assert "made this repository's own suite red" in template, (
        "the template states the rule without the measurement behind it, "
        "which is what a reader needs to not treat it as a style preference"
    )


def test_the_pending_surface_only_prints_before_the_cutoff(repo):
    """The state became structural with `ORDER_FROM`, so records of earlier
    work items print. A merged record has no honest repair: nobody can
    recover now what a fix pass added months ago."""
    code, out = surface_run(repo, OLD_ITEM, "round-2", units=PENDING)
    assert code == 0, out
    assert "not yet written" in out, (
        "passing in silence would hide the state the arm exists to surface"
    )
    assert "prints instead of failing" in out, out


def test_a_work_item_between_the_two_cutoffs_owes_the_rows_and_not_this_arm(repo):
    """The boundary that decides WHICH cutoff this arm takes, and nothing
    held it: every other case here sits below both cutoffs or above both, so
    keying the arm to `SURFACE_FROM` left them all green.

    A work item begun between the two owes the rows — `SURFACE_FROM` has
    required them since it landed — and does not owe this arm, because its
    records were written when a record could be committed after its fixes and
    both rows filled from the start. That is the same split `DEPTH_FROM`
    already makes inside `New units`.
    """
    module = check_module()
    between = (module.SURFACE_FROM + module.ORDER_FROM) // 2
    assert module.SURFACE_FROM < between < module.ORDER_FROM
    code, out = surface_run(
        repo, f"seal/specs/{between}-a-work-item-between", "round-2", units=PENDING
    )
    assert code == 0, (
        "a work item that predates the ordering rule is refused for a state "
        "the ordering rule created"
    )
    assert "prints instead of failing" in out, out


def test_the_pending_surface_cutoff_is_this_work_items_own_second(repo):
    """Keyed to `ORDER_FROM` rather than `SURFACE_FROM`: the rows have been
    required since the earlier cutoff, and only the ordering rule made them
    start out provisional."""
    began = check_module().ORDER_FROM
    item = f"seal/specs/{began}-the-item-that-added-the-rule"
    code, _out = surface_run(repo, item, "round-2", units=PENDING)
    assert code == 1, (
        "the work item that ADDED the ordering rule is the first one held to "
        f"this arm, and {began} is its own second"
    )


# --- what the failure reads like --------------------------------------------


def test_one_commit_named_two_ways_is_one_failure(repo):
    """A record naming the same fix abbreviated in one cell and in full in
    another is one late record, not two — the grouping key is the RESOLVED
    commit. It is the same mechanism that keeps a record with seven closed
    verdicts from printing seven copies of one paragraph, which is what the
    real record measured for #150 does.
    """
    item = NEW_ITEM
    write(repo, f"{item}/routing.md", declaration(item))
    reviewed = commit(repo, "declare")
    fix = touch(repo, "x = 2\n")
    body = record(reviewed, verdict=f"**fixed** `{fix}`", checked_by="round-2")
    body += f"| 🟡 2 | another | `f.py:1` | **fixed** `{fix[:7]}` | grounds |\n"
    write(repo, f"{item}/rounds/round-1.md", body)
    added = commit(repo, "round 1, written after its own fixes")
    write(repo, f"{item}/rounds/round-2.md", record(added))
    commit(repo, "round 2")
    code, out = run(repo)
    assert code == 1, out
    assert out.count("was ADDED by") == 1, (
        "one commit named two ways produced two failures — the reader is "
        f"asked to scroll past a repeated paragraph:\n{out}"
    )
    assert "🟡 1" in out and "🟡 2" in out, (
        "the single failure has to name every row that carries the commit, "
        "or collapsing them loses the detail"
    )


# --- every record, not only the last ----------------------------------------


def test_the_check_reads_every_record_not_only_the_last(repo):
    """Ordering is a fact about one round's own record, and every round has
    one. A check reading the last record alone answers it for one round —
    and the last record is the one LEAST likely to be late, because nothing
    follows it to commission anything.

    The fixture's own shape is asserted rather than assumed: with one record
    the case is not testing `every record` at all, because one record is also
    the last one. `chain_check.py` prints the count it found, so the shape is
    readable from the output.
    """
    _fix, _added = late_run(repo, NEW_ITEM)
    code, out = run(repo)
    assert "2 round record(s)" in out, (
        "the fixture did not write the records the case needs, so it is not "
        "testing `every record` at all"
    )
    assert code == 1, out
    assert "rounds/round-1.md" in out, (
        "the late record is round 1, not the last one, and the failure does "
        "not name it — the check is reading the last record alone"
    )
    assert "rounds/round-2.md" not in out, (
        "the honest record is named too, so the failure does not say which "
        "record was written late"
    )


# --- the documents ----------------------------------------------------------


def test_the_spec_carries_the_subsection():
    """Every refusal `chain_check.py` makes at the pull request has a
    subsection in `docs/review-chain-spec.md` saying what it costs. A fifth
    cutoff owes one, and round 2 of the last work item found that copying a
    neighbouring table row is how a false claim travels."""
    spec = flat("docs", "review-chain-spec.md")
    assert "When the record was written" in spec, (
        "the new refusal has no subsection beside the seven it joins"
    )
    assert "ORDER_FROM" in spec, "the subsection names no cutoff constant"
    assert "the ADDING commit" in spec or "the **adding** commit" in spec, (
        "the subsection does not say which commit is read, which is the "
        "whole distinction between the defect and a correct record"
    )


def test_the_spec_states_what_a_rebase_does_to_this():
    """The refusal reads a commit relationship, and a rebase rewrites those.
    Whichever way it is settled, it is settled in writing — an unstated
    caveat is one the next person rediscovers by being failed."""
    spec = flat("docs", "review-chain-spec.md")
    assert "rebase" in spec, "the six-month failure scenario is not written down"


def test_the_review_skill_tells_the_orchestrator_when_to_commit_it():
    """The refusal is the floor; this is the habit that clears it. The
    orchestrator writes the record, so the instruction belongs where the
    orchestrator reads — and the cheapest way to satisfy the check is the
    one that pays anyway: commission the fix pass from the committed record
    rather than from a report in a session that ends."""
    skill = flat("skills", "code-review", "SKILL.md")
    assert "And commit the record before commissioning the fixes" in skill
    assert "ORDER_FROM" in skill, (
        "the skill describes the habit and never names the check that "
        "enforces it, so a reader cannot tell a convention from a gate"
    )


def test_a_fixed_verdict_naming_no_commit_passes(repo):
    """Round 1's 🟡 7, executed. A record whose cells read `| fixed |` with no
    commit in them is invisible to the refusal however late it was committed.

    The two halves are run against **the same late record**, differing only in
    whether the verdict cell carries the SHA — which is what makes this a
    measurement of the reach rather than an exit code that could come from
    anywhere. With the commit: refused. Without it: passes.
    """
    item = NEW_ITEM

    def late(verdict):
        git(repo, "checkout", "-q", "-B", "feature", "base")
        write(repo, f"{item}/routing.md", declaration(item))
        reviewed = commit(repo, "declare")
        fix = touch(repo, "x = 2\n")
        write(
            repo,
            f"{item}/rounds/round-1.md",
            record(reviewed, verdict=verdict(fix), checked_by="round-2"),
        )
        added = commit(repo, "round 1, written after its own fixes")
        write(repo, f"{item}/rounds/round-2.md", record(added))
        commit(repo, "round 2")
        return run(repo)

    named_code, named_out = late(lambda fix: f"**fixed** `{fix}`")
    assert named_code == 1, named_out
    assert "was ADDED by" in named_out, named_out

    bare_code, bare_out = late(lambda _fix: "**fixed** — round-2 read it")
    assert bare_code == 0, bare_out
    assert "was ADDED by" not in bare_out, (
        "the same late record, and the only difference is the commit in the "
        "cell — so this is the reach's limit and not a second defect"
    )


def test_the_spec_and_the_template_state_the_reach_and_ask_for_the_commit():
    """The limit above is a fact a reader has to be able to find, and the
    template is where the person writing the cell meets it. Round 1 counted
    the cells; this keeps both halves of the answer in the tree."""
    spec = flat("docs", "review-chain-spec.md")
    assert "the refusal's reach is the commit a cell happens to carry" in spec, (
        "the reach's limit is not stated, so the six pass states read as an "
        "enumeration rather than as a bound"
    )
    assert "a convention rather than a guarantee" in spec, (
        "without this the table reads as though a passing record was shown "
        "to have been written on time"
    )
    template = flat("templates", "sdd-round.md")
    assert "A `fixed` verdict names the commit that fixed it" in template, (
        "the reach depends on a commit nobody is asked for"
    )
    assert "215 name a commit" in template and "215 name a commit" in spec, (
        "the measurement that decides this is in neither place, so the next "
        "reader cannot tell an edge case from the commonest one"
    )


def test_every_description_of_which_add_is_read_says_the_latest():
    """Round 2's 🟡 4 and 🟡 5. Round 1 inverted the index and left three
    descriptions of the old rule standing — the function's own summary line,
    the case docstring, and the spec's table row — one of them false by
    measurement rather than merely stale.

    A reader skimming a function reads its summary, and this is the function
    round 1 found undefended, so the summary is the copy that matters most.
    """
    source = flat("skills", "code-review", "scripts", "chain_check.py")
    assert "The LATEST commit on THIS BRANCH that added" in source, (
        "the summary line still states the rule the inversion replaced, "
        "twenty-six lines above the body that contradicts it"
    )
    assert "first added `rel`" not in source

    # Built from pieces rather than written out, because this case reads the
    # file it lives in: spelled as a literal, the needle would be satisfied
    # by this very line and the case would pass whatever the docstring says.
    # That is the shape `seal/ledger.md` records as a case green against its
    # own mutation, met from the inside.
    stale = "oldest commit " + "that touched"
    for parts in (
        ("docs", "review-chain-spec.md"),
        ("tests", "test_a_record_precedes_the_fixes_it_commissions.py"),
    ):
        assert stale not in flat(*parts), "/".join(parts)


def test_the_docstring_says_what_the_flag_now_protects():
    """The flag's reach changed with the index and only the ledger row said
    so. Under the earliest add, dropping `--diff-filter=A` was separable by a
    base that moves under a long branch; under the latest add it refuses
    every correctly updated record, because the newest commit that touched a
    record is its verdict update. Two cases red for one mutation, where round
    1's battery saw one."""
    source = flat("skills", "code-review", "scripts", "chain_check.py")
    assert "it now protects the ORDINARY record rather than a rare one" in source
    assert "two cases red for that one mutation" in source


def test_the_spec_points_at_the_row_it_means():
    """Round 2's 🟡 9. The bound sentence exists so a reader can find the
    limit themselves, so a pointer that counts to the wrong row is the whole
    of it — neither the third row nor the third pass row is the no-commit
    one."""
    spec = flat("docs", "review-chain-spec.md")
    assert "the bolded row above" in spec, (
        "the sentence still counts rows, and no third row is the one it means"
    )
    assert "the third style above" not in spec


def test_the_spec_carries_the_delete_and_re_add_state():
    """The one shape producing more than one add is a state the table never
    enumerated, and it is the shape that makes a late record look early."""
    spec = flat("docs", "review-chain-spec.md")
    assert "a record DELETED and re-added on the branch" in spec
    assert "judged on the **latest** add" in spec


def test_the_spec_answers_whether_carrying_is_checkable():
    """#150's own comment asks the narrower question beside the ordering one
    — whether a record can be made to carry the artifact it says it verified
    — and asks for it to be *stated whether it is checkable before assuming
    it is*. Answered either way is the requirement; this is the answer being
    in the file rather than in a session."""
    spec = flat("docs", "review-chain-spec.md")
    assert "What the record carries" in spec, (
        "the narrower question is left assumed, which is what its own "
        "comment asks not to happen"
    )
    assert "unbounded domain" in spec, (
        "the answer names no reason, so a later reader reads it as an "
        "omission rather than as a decision"
    )
    assert "a declaration" in spec, (
        "what is not checkable has to be named as a declaration, the shape "
        "`New units`' depth and `Ran by`'s provenance already take"
    )


def test_the_template_says_what_a_probe_row_owes():
    """The rule the answer above leaves behind: a probe row whose subject was
    a proposed replacement carries the replacement, not a sentence about
    it."""
    template = flat("templates", "sdd-round.md")
    assert "never a sentence about it" in template
    assert "reproducible from its own text" in template, (
        "the rule arrives with no reason, and a rule about writing more is "
        "the first one a tired session drops"
    )


def test_the_template_says_what_the_check_does():
    """The row's own comment is where a session copying the template meets
    the rule. `templates/sdd-round.md` said the record is written right after
    the round posts and nothing said anyone would look."""
    template = flat("templates", "sdd-round.md")
    assert "written after the work it commissioned" in template, (
        "the template's timing sentence is still an instruction nobody reads "
        "as enforceable"
    )
