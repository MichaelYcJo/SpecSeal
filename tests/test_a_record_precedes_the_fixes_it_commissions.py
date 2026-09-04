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

import importlib.util
import json
import os
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


def record(target, verdict="answered", checked_by="no fixes to check", severity="🟡"):
    """A record that passes every check but the one each case is about.

    `verdict` is the whole cell, so a case can write `**fixed** <sha>` or the
    `open` a record written on time carries before its fixes land. 🟡 rather
    than 🔴 so that an `open` verdict is not also an unanswered blocking
    finding, which is a different refusal.
    """
    return (
        "# a round\n\n"
        "| Field | Value |\n|---|---|\n"
        f"| Target SHA | {target} |\n"
        f"| Ran by | {RUNNER} |\n"
        f"| Fixes checked by | {checked_by} |\n"
        "| Contract changes | none |\n"
        "| New units | none |\n"
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
    fixes land. Read as *the oldest commit that touched the file*, this
    refuses a record that did everything right.

    **This case cannot be red at HEAD**: the behaviour it pins is already
    correct there. It is red only under the mutation that drops
    `--diff-filter=A`, which is how §15 was satisfied for it — and that
    mutation SURVIVED every other case in this file, including the
    updated-in-place one, because a file that was added and then modified has
    the same oldest-touching commit either way. Do not delete this as a case
    that never fails.
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
