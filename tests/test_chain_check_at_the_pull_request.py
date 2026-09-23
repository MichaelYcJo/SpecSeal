"""The review chain is enforced at the pull request now, not at every commit.

The commit gate could never tell "routed to the chain, not reviewed yet" from
"nobody decided anything" — the two are byte-identical to it — so it asked
every time. Recording the answer lets it stay quiet, and the answer is only
allowed to make it quiet because the check MOVED rather than disappearing.
This is where it moved to.

Every case here builds a scratch repository with a real base branch and a real
HEAD, because the check is about what git can see between two refs. The
verdicts are read from the script's exit code, not from its prose.
"""

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

import pytest
from conftest import (
    committed_round_records_on_disk,
    load_hook_module,
    on_disk,
    symlink_or_skip,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py")

CHAIN = "through the review chain"
DIRECT = "straight to the PR"
ITEM = "seal/specs/1787700000-a-work-item"
# The eighth cutoff, as a literal rather than read from the script, so the
# boundary cases below are one second apart on a number this module states and
# `test_the_broad_gate_label_has_one_spelling_both_scripts_read` pins the
# script's own constant against it. Reading it from the script would make
# every case here agree with whatever the script says, including a typo.
GATE_FROM = 1788912166
# One level down, because `round-N` is the only member of the SDD set that is
# plural and unbounded. A record left at `ITEM` itself is a stray and fails.
ROUNDS = f"{ITEM}/rounds"
# The row's name as the arm quotes it back, for the cases that assert the arm
# said NOTHING. Every message this arm writes opens with it, so its absence is
# what tells a pass from a notice — and after round 1's 🟡 3 this arm has a
# state that prints at exit 0, which is why exit codes stopped being enough.
BROAD_GATE_ROW = "Broad gate"


def load_by_path(path, name):
    """The checker and the shared reader as MODULES, by absolute path.

    `conftest.load_hook_module` resolves against `hooks/`, and neither of these
    lives there. Used by the repository-wide case at the foot of this file,
    which asks one arm a question about the real tree rather than driving the
    whole script over a fixture.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def _build_chain_repo(d):
    d.mkdir()
    git(d, "init", "-q", "-b", "base")
    write(d, "f.py", "x = 1\n")
    commit(d, "base")
    git(d, "switch", "-qc", "feature")


@pytest.fixture(scope="session")
def _chain_repo_template(tmp_path_factory):
    d = tmp_path_factory.mktemp("chain-repo-template") / "repo"
    _build_chain_repo(d)
    return d


@pytest.fixture
def repo(tmp_path, _chain_repo_template):
    """A repository with a `base` branch and a feature branch checked out."""
    d = tmp_path / "repo"
    shutil.copytree(_chain_repo_template, d)
    return d


def declaration(review=CHAIN, branch="feature"):
    return (
        "# 1787700000-a-work-item — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {review} |\n"
        "| Destination | open the pull request |\n"
        f"| Branch | {branch} |\n"
    )


def record(
    sha,
    passed=False,
    verdict="fixed",
    finding="🔴 1",
    extra="",
    pr=None,
    checked_by="nobody — the run ended here",
    grounds="grounds",
):
    box = "x" if passed else " "
    # The `| PR |` row is optional, and `not yet opened` is what a review that
    # finished before its pull request writes there.
    pr_row = f"| PR | {pr} |\n" if pr is not None else ""
    # `Fixes checked by` is NOT optional, and the default is the one value
    # that is honest for a record with no later round beside it. Passing
    # `None` leaves the row out, which is a state of its own and has its own
    # cases in `test_the_last_rounds_fixes_are_checked.py`.
    who = f"| Fixes checked by | {checked_by} |\n" if checked_by is not None else ""
    return (
        "# round 1\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n{pr_row}{who}\n"
        f"- [{box}] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| {finding} | something | `f.py:1` | {verdict} | {grounds} |\n"
        f"{extra}"
    )


def run(repo, draft=None, payload=None, branch=None):
    """`draft=True/False` writes the event payload GitHub hands a workflow.

    `None` is the local run: no payload, so the check cannot see a pull
    request at all. That state is judged strictly on purpose — see
    `pull_request_state`.

    `payload` writes the file verbatim, for the shapes `draft=` cannot say: a
    payload that will not parse, one with no pull request in it, and one whose
    `draft` is the STRING `"false"`. `branch` sets `GITHUB_HEAD_REF`, which is
    where the branch comes from in a workflow because a pull-request checkout
    is a detached merge commit.
    """
    env = dict(os.environ)
    env.pop("GITHUB_EVENT_PATH", None)
    env.pop("GITHUB_HEAD_REF", None)
    if branch is not None:
        env["GITHUB_HEAD_REF"] = branch
    if payload is not None:
        path = repo / "event.json"
        path.write_text(payload, "utf-8")
        env["GITHUB_EVENT_PATH"] = str(path)
    elif draft is not None:
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


# --- the four declaration states --------------------------------------------


def test_a_chain_declaration_with_no_round_record_fails(repo):
    """S6. The round record is the pull request's only evidence — the local
    mark cannot travel here."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    code, out = run(repo)
    assert code == 1, out
    assert "holds no `round-N.md`" in out
    assert f"{ROUNDS}/" in out, (
        "the failure has to name the directory it looked in. A repository "
        "whose records are still one level up reads this as a review that "
        "never happened, and is told nothing about why"
    )


def test_a_draft_pull_request_has_not_had_its_rounds_yet(repo):
    """#296. The arm above used to fail the very sequence a document orders.

    `skills/code-review/orchestration.md` says the draft pull request opens at
    the end of the build, BEFORE round 1 — a reviewer needs a pull request to
    review. So the first thing that happens after the draft opens is this
    check running against a `rounds/` that is empty by design, and the session
    that obeyed the document got a red build for it.

    The record is still owed and the message says so. `ready_for_review` is in
    the workflow's trigger list, so pressing the button re-runs this and the
    arm applies — nothing that can reach `main` is exempt.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    code, out = run(repo, draft=True)
    assert code == 0, out
    assert "holds no `round-N.md`" in out, (
        "the state is printed rather than swallowed. A draft that is excused "
        "in silence reads exactly like a work item whose rounds are done"
    )
    assert "ready_for_review" in out, (
        "the notice has to name what re-arms the check, or a reader takes the "
        "exemption for a permanent one"
    )


def test_a_ready_pull_request_still_has_no_way_past_the_record(repo):
    """The other half of #296, stated as its own case.

    The arm's whole safety property is that the draft is a stage and not an
    escape. Pressing *Ready for review* is what this pins, with the message
    unchanged from before the draft path existed.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "holds no `round-N.md`" in out


# The four shapes of `unknown`, in ONE place because both arms that `strict`
# excuses are held to them and a second literal is how the two drift apart.
# `pull_request_state` has three answers, and `unknown` is judged as READY —
# otherwise `no pull-request context` becomes the quietest way past this check
# that exists. The string case is the one where a truthy read would have
# inverted the answer, and `"draft": "false"` inverting it is a defect this
# function has already had once.
#
# Round 1's 🟡 4: the gate arm carried two of the four, and the two it was
# missing are the two `phases/phase-1.md` calls dangerous. Both arms consume
# one `strict` today, which is what kept that from being a 🔴 — and the arms
# stopping to share it is exactly what this work item did to the other one.
UNKNOWN_SHAPES = [
    {},
    {"payload": "{not json"},
    {"payload": json.dumps({"repository": {}})},
    {"payload": json.dumps({"pull_request": {"draft": "true"}})},
]
UNKNOWN_IDS = ["no payload", "unparseable", "no pull request", "a string draft"]


@pytest.mark.parametrize("kwargs", UNKNOWN_SHAPES, ids=UNKNOWN_IDS)
def test_an_unknown_state_is_not_a_draft_at_this_arm_either(repo, kwargs):
    """The trap #296 opens, and the one thing that must not follow from it.

    `pull_request_state` has three answers, not two, and `unknown` is judged
    as READY — otherwise `no pull-request context` becomes the quietest way
    past this check that exists. The draft path above must inherit that
    direction rather than re-deciding it: a harness that stops writing
    `draft` into the payload would otherwise turn the fix for #296 into a way
    past the round record itself.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    code, out = run(repo, **kwargs)
    assert code == 1, out
    assert "holds no `round-N.md`" in out
    assert "judged as a ready pull request" in out, (
        "and it says which state it assumed. Passing — or failing — in "
        "silence is the one outcome `pull_request_state` rules out"
    )


def test_a_chain_declaration_with_a_record_passes(repo):
    """S7."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out


def test_a_pull_request_with_no_declaration_passes_with_a_notice(repo):
    """S8. Failing here would teach sessions not to declare, which voids the
    condition — the same reasoning `unverified_check.py` gives for not failing
    on an honest open row."""
    write(repo, "g.py", "y = 2\n")
    commit(repo, "no declaration")
    code, out = run(repo)
    assert code == 0, out
    assert "examined nothing" in out, (
        "the notice has to say what was NOT CHECKED. `no declaration found` "
        "describes the check's own state and reads as routine"
    )


def test_an_unreadable_declaration_fails(repo):
    """S9. A tolerant read reports `no declaration`, which is exactly what a
    branch that never declared looks like."""
    write(repo, f"{ITEM}/routing.md", "# routing\n\nwe are going to review it\n")
    commit(repo, "prose")
    code, out = run(repo)
    assert code == 1, out
    assert "not a readable declaration" in out


def test_a_direct_declaration_needs_no_round_record_and_is_printed(repo):
    """`ITEM` is below `DIRECT_GATE_FROM`, so the seal arm below prints for
    it. What this case pins is unchanged: the declaration is reported, and a
    direct answer is never failed for the absence of a round record."""
    write(repo, f"{ITEM}/routing.md", declaration(review=DIRECT))
    commit(repo, "declare direct")
    code, out = run(repo)
    assert code == 0, out
    assert DIRECT in out, "a decision nobody sees is not a record"
    assert "round-N.md" not in out, (
        "a direct declaration was asked for a round record, which is the one "
        "thing that answer turns off"
    )


# --- the frame a declaration says was drawn ---------------------------------
#
# A work item could declare `Planning | framer`, draw no frame, and reach the
# pull request with nothing noticing (#399). The key is a COMPARISON, not a
# derivation: nothing is re-judged and nothing is counted — `routing.md`
# carries the answer, written before the first edit by the party the routing
# batch asked.
#
# The cutoff is this work item's own id, measured rather than chosen
# (`questions.md` Q3): 11 declarations answer `Planning | framer` and 10 carry
# no mark because the mark did not exist.
FRAME_FROM = 1789518345
MARK = "Framed 2026-09-16 by framer, before the build."
PLACEHOLDER_MARK = "Framed <date> by <who>, before the build."
APPROVED = "Approved 2026-09-16 by the repository owner, when `smith` was spawned."
UNFILLED = "Approved <date> by <who>, when `smith` was spawned."


def framed_declaration(planning="framer", branch="feature"):
    return (
        "# a work item — routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {DIRECT} |\n"
        "| Destination | open the pull request |\n"
        f"| Planning | {planning} |\n"
        f"| Branch | {branch} |\n"
    )


def framed(repo, began, spec=MARK, plan=APPROVED, planning="framer", seal=True):
    """A framer-declared work item, with the frame `spec` and `plan` describe.

    `spec=None` writes no `spec.md`, `plan=None` writes no `plan.md`, and
    anything else is the FOOT of the file — which is where the mark lives and
    where the approval line is read from.

    `seal=True` writes the `broad-gate.md` the direct arm owes above this
    cutoff, so these cases fail on the frame and never on the seal.
    """
    item = f"seal/specs/{began}-a-framed-work-item"
    write(repo, f"{item}/routing.md", framed_declaration(planning))
    if spec is not None:
        write(repo, f"{item}/spec.md", f"# a spec\n\nProse about the work.\n\n{spec}\n")
    if plan is not None:
        write(repo, f"{item}/plan.md", f"# a plan\n\n{plan}\n\n## Phases\n\nProse.\n")
    first = commit(repo, "declare and frame")
    if seal:
        write(
            repo,
            f"{item}/broad-gate.md",
            f"# broad gate\n\n| Field | Value |\n|---|---|\n"
            f"| {BROAD_GATE_ROW} | {first} against base |\n",
        )
        commit(repo, "seal")
    return item


def test_a_declared_framer_with_no_spec_is_refused(repo):
    """S15. The reported failure, and it is the whole reason for the arm: a
    session took a change straight to `smith` with no frame, requests that had
    been passing started returning 422, and nothing in either tree said so."""
    item = framed(repo, FRAME_FROM, spec=None)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{item}/spec.md" in out, "the refusal does not name the file it wants"


def test_a_declared_framer_with_no_plan_is_refused(repo):
    """S15's other half. The plan is the design gate's artifact — approving it
    IS the gate — so its absence means the gate has no record anywhere."""
    item = framed(repo, FRAME_FROM, plan=None)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{item}/plan.md" in out, out


def test_a_spec_with_no_mark_is_refused(repo):
    """S16. A frame with no mark. The framer is the only party in the chain
    whose work left no evidence in the TREE — its other mark lives in the git
    dir, and a git dir does not travel here."""
    item = framed(repo, FRAME_FROM, spec="No mark at all.")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{item}/spec.md" in out and "Framed" in out, (
        "the refusal names neither the file nor the line it wants"
    )


def test_a_mark_that_is_only_QUOTED_does_not_count(repo):
    """The check that could not fail, caught before it shipped.

    Measured on this repository: the one `spec.md` a mark-shaped search
    matches today is the spec that DOCUMENTS the mark — it quotes the template
    line in a fenced block, names it in a table of who writes what, and states
    it again as an acceptance row. A search anywhere in the file reads all
    three as a framer having signed, so a spec ABOUT the mark passes for
    carrying one, and every later spec learns that quoting is enough.

    The foot of the file is the whole rule, and this is the case that holds
    it.
    """
    item = framed(
        repo,
        FRAME_FROM,
        spec=(
            "The framer's mark is one line at the foot of `spec.md`:\n\n"
            f"```\n{PLACEHOLDER_MARK}\n```\n\n"
            "## Open questions\n\nNone."
        ),
    )
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{item}/spec.md" in out, out
    assert "END with" in out, (
        "the refusal does not say WHERE the mark has to be, so the obvious "
        "repair is to quote it once more"
    )


def test_an_unfilled_mark_is_refused(repo):
    """A placeholder copied through reads to a person as a mark and says
    nothing, which is #151's shape on this line."""
    framed(repo, FRAME_FROM, spec=PLACEHOLDER_MARK)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "UNFILLED" in out, out


def test_a_mark_that_disagrees_with_the_declaration_is_refused(repo):
    """The declaration says `framer` and the mark says `the session`. Which of
    the two is true is not the check's to guess, so it refuses rather than
    picking one."""
    framed(repo, FRAME_FROM, spec="Framed 2026-09-16 by the session, before the build.")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "disagree" in out, out


def test_a_complete_frame_passes(repo):
    """The passing side, which the branch that adds this arm exercises on
    itself — this work item declares a framer and carries all three."""
    framed(repo, FRAME_FROM)
    code, out = run(repo, draft=False)
    assert code == 0, out


def test_the_session_drew_it_and_the_arm_makes_no_claim(repo):
    """Disclosure 4, asserted rather than only written down. A session that
    framed the work itself owes this arm nothing, so a `Planning | the
    session` work item with no `spec.md` at all is not this arm's business."""
    framed(repo, FRAME_FROM, spec=None, plan=None, planning="the session")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "spec.md" not in out, out


def test_an_unfilled_approval_line_is_reported_and_not_refused(repo):
    """S17, and it departs from #399's `Done when` on a measurement the ticket
    did not have: 61 of 71 `plan.md` files in this tree carry the unfilled
    placeholder. A refusal that fires on nearly every honest branch teaches
    people to write none."""
    framed(repo, FRAME_FROM, plan=UNFILLED)
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "approval line" in out and "placeholder" in out, (
        "the notice is missing, so the gap is not reported at all — which is "
        "the other way to satisfy exit 0"
    )


def test_a_framer_declaration_below_the_cutoff_prints_instead(repo):
    """S21's first half, and the retroactive red the measurement forecloses.

    10 of the 11 work items declaring `Planning | framer` carry no mark,
    because the mark did not exist. A release pull request carries every work
    item the release adds, so an arm with no cutoff refuses the next release
    into `main` for every one of them.
    """
    framed(repo, FRAME_FROM - 1, spec=None, seal=False)
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "spec.md" in out, "the notice does not say what was not checked"
    assert str(FRAME_FROM) in out, "the notice does not name the cutoff"


def test_the_same_state_above_the_cutoff_is_refused(repo):
    """S21's second half. One second apart, on a number this module states and
    the script states separately."""
    framed(repo, FRAME_FROM, spec=None)
    code, out = run(repo, draft=False)
    assert code == 1, out


def test_the_frame_arm_is_judged_on_a_draft_too(repo):
    """Every other arm here excuses a draft, and this one must not.

    A draft is excused where a review is still RUNNING — it has not reached
    its verdict yet. The frame is not still running: it is drawn before the
    first edit, so a draft with no `spec.md` is not early, it is a work item
    that declared a framer and then built without one.
    """
    framed(repo, FRAME_FROM, spec=None)
    code, out = run(repo, draft=True)
    assert code == 1, out


def test_the_arm_writes_down_what_it_cannot_see(repo):
    """S20. The disclosure is in the MODULE rather than in a ticket, because
    the reader it is for is whoever opens the arm.

    Each of the seven is asserted separately, so deleting one line is red.
    The third is the load-bearing one: the row and the mark are both the
    framer's writes, so a green run is not evidence that a framer ran — and
    this list is the only thing standing between that reading and a reader.

    `plan.md` and `spec.md` §S20 both say SIX. The spec lists seven bullets,
    and all seven are real, so the module carries seven and the count in the
    prose is what is wrong. Asserting the phrases rather than a number is what
    keeps this case from pinning the arithmetic instead of the disclosure.
    """
    text = _module("specseal_chain_check_for_the_frame_arm", CHECK).frame.__doc__
    assert "WHAT THIS ARM CANNOT SEE" in text
    for phrase in (
        "never wrote a `routing.md`",
        "Whether the frame is any good",
        "Whether the party named actually did it",
        "or an absent row",
        "The ladder's rung",
        "kept its `Automation` promise",
        "`no work item` exit",
    ):
        assert phrase in text, (
            f"the disclosure lost `{phrase}`. A reader who opens this arm has "
            "one place to learn what a green run does not mean"
        )


# --- the seal a direct declaration still owes -------------------------------
#
# `straight to the PR` turns off the REVIEWER and nothing else. The broad gate
# is the sealer's act, taken once after the rounds settle — and where no round
# runs, *after the rounds settle* is simply *at the end*. This arm was one
# `print` and a `continue`, so the one full-suite run the design turns on
# could be skipped entirely by answering a question about reviewing.
#
# The cutoff is its own, one work item later than `GATE_FROM`'s, and the
# measurement behind it is the same shape: 16 declarations in this repository
# answer `straight to the PR` and not one carries the file, because the file
# did not exist.
DIRECT_GATE_FROM = 1789518345
GATE_FILE = "broad-gate.md"


def direct_item(began, slug="a-direct-work-item"):
    return f"seal/specs/{began}-{slug}"


def direct(repo, began, gate=None):
    """A direct declaration, and a `broad-gate.md` when `gate` is given."""
    item = direct_item(began)
    write(repo, f"{item}/routing.md", declaration(review=DIRECT))
    first = commit(repo, "declare direct")
    if gate is not None:
        value = first if gate == "first" else gate
        write(
            repo,
            f"{item}/{GATE_FILE}",
            f"# broad gate\n\n| Field | Value |\n|---|---|\n"
            f"| {BROAD_GATE_ROW} | {value} against base |\n",
        )
        commit(repo, "seal")
    return item, first


def test_a_direct_declaration_with_no_seal_fails_a_ready_pull_request(repo):
    """S19's first half, and the silence this phase removes.

    Before this, the walk returned at the direct arm before it reached the
    broad-gate arm — so a work item could open a ready pull request having
    run nothing, and the check printed `nothing required`.
    """
    direct(repo, DIRECT_GATE_FROM)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert GATE_FILE in out, "the refusal does not name the file it wants"
    assert "sealer" in out, "the refusal names no way out"


def test_a_direct_declaration_with_a_seal_passes(repo):
    """S19's second half. The cell names a SHA the tree can see, so the run
    happened and the pull request is a request to merge something somebody
    ran the suite over."""
    direct(repo, DIRECT_GATE_FROM, gate="first")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert BROAD_GATE_ROW not in out, (
        "the arm spoke about a cell it had no complaint with; every message "
        "it writes opens with the row's name"
    )


def test_a_direct_declaration_whose_seal_never_ran_fails(repo):
    """The file existing is not the run happening. `not yet` is the honest
    mid-run value, and at a ready pull request it is the refusal — which is
    the same judgment the chain path's arm makes, reached through the same
    reader (`questions.md` Q4)."""
    direct(repo, DIRECT_GATE_FROM, gate="not yet")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert BROAD_GATE_ROW in out and "not yet" in out, out


def test_a_direct_declaration_below_the_cutoff_prints_instead(repo):
    """The retroactive red this cutoff forecloses.

    16 declarations in this repository answer `straight to the PR` and not
    one of them carries the file, because there was nowhere to write it. A
    release pull request carries every work item the release adds, so an arm
    with no cutoff refuses a release for work nobody could have sealed.
    """
    direct(repo, DIRECT_GATE_FROM - 1)
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert GATE_FILE in out, "the notice does not say what was not checked"
    assert str(DIRECT_GATE_FROM) in out, (
        "the notice does not name the cutoff, so a reader cannot tell why "
        "this one printed and the next one failed"
    )


def test_a_direct_declaration_with_no_seal_is_SILENT_on_a_draft(repo):
    """`strict` is false for a draft, and the reason is the chain path's: the
    broad gate runs at the end, so a draft with no seal is telling the truth.

    **Silence, not a notice**, and the old name said notice. `direct_seal`
    returns `[], []` when `strict` is false, which matches `broad_gate` and is
    right — but the case asserted exit 0 and nothing else, so it would have
    passed either way and its name would have gone on describing behaviour
    nobody had. The assertion is now on the silence itself.
    """
    item, _first = direct(repo, DIRECT_GATE_FROM)
    code, out = run(repo, draft=True)
    assert code == 0, out
    # The arm's informational PRINT names the file on every run — it says
    # where the cell would be read from — so the silence to assert is the
    # absence of the refusal's own words, not the absence of the filename.
    # Writing it the other way went red here, which is how the print's
    # unconditional half got found.
    for said in ("git carries no", "Spawn the `sealer`", BROAD_GATE_ROW):
        assert said not in out, (
            f"a draft was told `{said}` about a seal that is not due yet, "
            "which is the mid-run noise `strict` exists to keep out"
        )
    assert item in out, (
        "the declaration was not reported at all — silence about the SEAL is "
        "not silence about the work item"
    )


# --- the round record it finds ----------------------------------------------


def test_a_record_reviewing_a_commit_off_this_branch_fails(repo):
    """The target has to be an ancestor. A SHA from somewhere else is a review
    of something this pull request does not contain."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record("0" * 40))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "not an ancestor" in out


def test_a_record_with_no_target_sha_fails(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        "# round 1\n\n- [ ] Pass\n\n## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n|---|---|---|---|---|\n"
        "| 🟡 1 | x | `f.py:1` | answered | g |\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "which commit this round actually looked at" in out


def test_the_last_round_is_the_one_read(repo):
    """Earlier verdicts are not archived — every one needs an answer in the
    round that follows, so the last file is the state.

    Ordered numerically: `round-10.md` sorts before `round-2.md` as text.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    write(repo, f"{ROUNDS}/round-10.md", record(sha, passed=True, verdict="fixed"))
    commit(repo, "rounds")
    code, out = run(repo)
    assert code == 0, out
    assert "round-10.md" in out


# --- Pass against the verdict table -----------------------------------------


def test_a_checked_pass_beside_an_open_blocking_finding_fails(repo):
    """The state a checkbox alone would create. Both halves are in one file,
    so a machine can see the contradiction — and is made to."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "`Pass` is checked" in out


def test_a_blocking_finding_below_a_subheading_is_still_in_the_table(repo):
    """#505's class in the checker's own reader. `verdict_table` ended the
    `## Verdicts` section at the first line starting with `#`, so a `###`
    inserted by hand between the header and an open 🔴 row put that row
    outside the section: `open_blocking` saw no blocker, and a checked `Pass`
    beside it passed. The generator never writes a heading into a section,
    so only a hand-edited record reaches this — which is the record the
    checker exists for. A section ends at a heading of its own level or
    shallower, here as in `round_record.py`, and the survivor sweep over the
    generator's fix is what found this copy of the loop."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    text = record(sha, passed=True, verdict="open")
    separator = "|---|---|---|---|---|\n"
    assert text.count(separator) == 1, text
    text = text.replace(separator, separator + "\n### a label somebody added\n\n")
    write(repo, f"{ROUNDS}/round-1.md", text)
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "`Pass` is checked" in out


def test_an_unchecked_pass_fails_once_the_pull_request_is_ready(repo):
    """Reversed deliberately, and this docstring is the record of it.

    It used to read *an honest open finding is not what this fails for*, and
    that was written when nothing anywhere required `Pass` ever to be
    checked: a work item could declare the chain, run its rounds, leave every
    verdict open and open a pull request, and no gate in the repository had
    an opinion. `was it reviewed` was enforced and `did it pass` was not.

    The order is what settles it. In this design the chain runs BEFORE the
    pull request — smith, then warden, then the PR — so an unchecked `Pass`
    at the pull request means the chain was skipped or is still running.
    Neither is a state to open a ready pull request in. The escape is below:
    open it as a draft.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "`Pass` is not checked" in out


def test_an_unchecked_pass_passes_on_a_draft_pull_request(repo):
    """The escape hatch, and the only one. A review still running has
    somewhere to be: a draft pull request is not a request to merge."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, draft=True)
    assert code == 0, out
    assert "draft" in out


def test_a_run_that_cannot_see_a_pull_request_is_judged_as_a_ready_one(repo):
    """The unknown is judged strictly, and the reason is printed.

    Treating it as a draft would make `no pull-request context` the quietest
    way past this check that exists — quieter than `[no-review]`, which at
    least stays in the command. Passing in silence is the one outcome ruled
    out, so the verdict says which state it assumed and why."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "no pull-request event payload" in out


def test_a_checked_pass_beside_an_open_NON_blocking_finding_passes(repo):
    """🟡 does not block a merge, so it does not block a pass. The cap lets
    extra rounds only for 🔴, and this is the same line."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(sha, passed=True, verdict="open", finding="🟡 1"),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out


def test_a_verdict_word_it_does_not_recognise_counts_as_open(repo):
    """The direction has to be toward the finding still being open. A word
    this cannot read, counted as closed, is the tolerant read the whole file
    refuses."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="looked at"))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "looked at" in out


def test_a_record_with_no_pass_checkbox_fails(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        f"# round 1\n\n| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n\n"
        "## Verdicts\n\n| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n| 🟢 1 | x | `f.py:1` | fixed | g |\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "did it pass" in out


def test_an_unreadable_verdict_table_fails(repo):
    """Zero open findings and a table nobody can read are the same number.
    Only one of them means the review is done."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        f"# round 1\n\n| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n\n"
        "- [x] Pass\n\n## Verdicts\n\nwe found nothing worth writing down\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert "holds no table" in out


def test_a_blocking_finding_inside_a_fenced_block_is_not_a_finding(repo):
    """One reader, not two. A 🔴 inside a code fence or an HTML comment must
    not count here for exactly the reason it does not count in
    `unverified_check.py` — two readers of the same markdown drifted apart in
    four places across three rounds in this repository."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(sha, passed=True, verdict="fixed")
        + "\n```\n| 🔴 9 | quoted | `f.py:1` | open | from another round |\n```\n"
        + "<!-- | 🔴 8 | commented | `f.py:1` | open | a note | -->\n",
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out


# --- where a round record has to come from ----------------------------------


def test_an_uncommitted_round_record_is_not_evidence(repo):
    """The declaration comes from `git diff` and the records used to come
    from `os.listdir`, so two values built by two rules were compared. A file
    nobody committed cannot be a pull request's evidence — CI never sees it.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True))
    # deliberately not committed
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "holds no `round-N.md`" in out


def test_a_symbolic_link_cannot_stand_in_for_the_last_round(repo):
    """The LAST round is the one whose verdict speaks, so anything that can
    add a name at the end decides which file is read.

    Reproduced before the fix: with a failing `round-2.md` committed, a
    tracked link `round-3.md` -> the clean `round-1.md` turned exit 1 into
    exit 0. The failing round was still sitting right there."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="fixed"))
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    commit(repo, "two rounds")
    symlink_or_skip("round-1.md", repo / ROUNDS / "round-3.md")
    commit(repo, "a link named round-3")
    assert (
        git(repo, "ls-tree", "HEAD", f"{ROUNDS}/round-3.md").stdout.split()[0]
        == "120000"
    ), "the link has to reach git as a link, or this case proves nothing"
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "round-2.md" in out


def test_a_declaration_already_in_the_base_is_still_checked(repo):
    """`changed_routing` reads what this pull request TOUCHED, so a pull
    request adding only round records to an item declared in an earlier one
    found nothing and printed `declared neither way` — a sentence about a
    tree holding the declaration right there.

    The branch is the key the commit gate already uses, and it is the key
    here too."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "work with no declaration in the diff")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "holds no `round-N.md`" in out
    assert "examined nothing" not in out


# --- S10 of the 0.4.0 root move: a declaration the pull request only moved --


OLD_ITEM = "specs/1780000000-released"


def move_into_seal(repo, *items):
    """The root move as `hooks/root-migrate.py` and this repository's own
    branch make it: a staged `git mv` of each work item under `seal/specs/`."""
    (repo / "seal" / "specs").mkdir(parents=True, exist_ok=True)
    for item in items:
        git(repo, "mv", item, f"seal/{item}")


def test_a_declaration_the_pull_request_only_renamed_is_not_judged(repo):
    """The root move renames every declaration in the repository, and each
    shows up in `git diff --name-only` under its new path exactly as an added
    one would. Judged, the move would put every released work item under
    review on the pull request that moved it — fifteen here — each needing
    its round records' Target SHA to resolve. A declaration the pull request
    only moved is not one it made."""
    write(repo, f"{OLD_ITEM}/routing.md", declaration(branch="released"))
    commit(repo, "a released work item, declared for a branch that is not this one")
    git(repo, "branch", "-f", "base", "HEAD")
    move_into_seal(repo, OLD_ITEM)
    commit(repo, "the root move")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "1780000000-released" not in out, out
    assert "examined nothing" in out, (
        "this branch declared nothing, and the notice says so"
    )


def test_the_branchs_own_declaration_is_still_judged_after_the_move(repo):
    """The set the check judges is what the pull request added or edited PLUS
    the declaration for this branch — so the move of this branch's own item
    does not hide it, and the fourteen it moved beside it stay out."""
    write(repo, "specs/1787700000-a-work-item/routing.md", declaration())
    write(repo, f"{OLD_ITEM}/routing.md", declaration(branch="released"))
    commit(repo, "two work items declared, one for this branch")
    git(repo, "branch", "-f", "base", "HEAD")
    move_into_seal(repo, "specs/1787700000-a-work-item", OLD_ITEM)
    commit(repo, "the root move")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert ITEM in out and "holds no `round-N.md`" in out, out
    assert "1780000000-released" not in out, out


def test_a_declaration_the_pull_request_renamed_and_edited_is_judged(repo):
    """Only an EXACT rename is a move. A declaration the pull request moved
    and then changed carries an edit of its own, and the edit is what the
    check exists to read."""
    write(repo, f"{OLD_ITEM}/routing.md", declaration(branch="released"))
    commit(repo, "a released work item")
    git(repo, "branch", "-f", "base", "HEAD")
    move_into_seal(repo, OLD_ITEM)
    moved = repo / "seal" / OLD_ITEM / "routing.md"
    moved.write_text(
        moved.read_text(encoding="utf-8") + "\nEdited on the way over.\n",
        encoding="utf-8",
    )
    commit(repo, "the root move, with an edit")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "1780000000-released" in out, out


def test_a_working_tree_edit_cannot_close_a_round_git_carries_as_open(repo):
    """The names came from `git ls-tree` and the CONTENT came from `open()`.

    Round 2 moved half of this and left the other half, so the check was still
    comparing two values built by two rules — it just did it one line later.
    A record committed with an open blocking finding, edited on disk to read
    `fixed` and not committed, turned exit 1 into exit 0. CI never sees that
    edit; a local run always can.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="open"))
    commit(repo, "round 1, blocking finding open")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="fixed"))
    # deliberately not committed
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "`Pass` is checked" in out


def test_a_clean_copy_in_the_working_tree_cannot_hide_a_committed_failure(repo):
    """The mirror of the symbolic-link case, and it ran the other way.

    There, git carried a link and the check had to see through it. Here git
    carries the failing `round-2.md` as an ordinary file and the WORKING TREE
    holds a link to the clean `round-1.md` in its place. `unique_by_target`
    resolved both worktree paths to one real file, folded the record git
    carries out of the list, and the failing round was never opened.

    The fold is gone rather than narrowed: with the content read from git, a
    worktree path is not what is being counted any more, and the mode filter
    already refuses a link git knows about.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="fixed"))
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    commit(repo, "two rounds, the second one failing")
    assert (
        git(repo, "ls-tree", "HEAD", f"{ROUNDS}/round-2.md").stdout.split()[0]
        == "100644"
    ), "git has to carry round-2 as a regular file, or this case proves nothing"
    (repo / ROUNDS / "round-2.md").unlink()
    symlink_or_skip("round-1.md", repo / ROUNDS / "round-2.md")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "round-2.md" in out


# --- what the event payload is allowed to say -------------------------------


def test_a_string_draft_is_not_a_draft(repo):
    """`pr["draft"]` read the value for its truthiness, and every non-empty
    string is true. A payload carrying `"draft": "false"` was therefore read
    as a draft, and a draft is excused the checked `Pass` — the one
    requirement this branch added, turned off by four characters."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, payload='{"pull_request": {"draft": "false"}}')
    assert code == 1, out
    assert "`Pass` is not checked" in out


def test_a_payload_that_will_not_parse_is_judged_ready_and_says_so(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, payload="{not json")
    assert code == 1, out
    assert "would not read" in out


def test_a_payload_naming_no_pull_request_is_judged_ready_and_says_so(repo):
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=False, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo, payload='{"repository": {"name": "x"}}')
    assert code == 1, out
    assert "names no pull request" in out


def test_a_branch_nobody_can_read_is_not_a_pull_request_that_declared_nothing(repo):
    """A detached HEAD with no `GITHUB_HEAD_REF` leaves no key to match a
    declaration by, and the notice said *this pull request declared neither
    way* — a sentence about a tree holding the declaration right there. The
    two states need different sentences: one is an author who declared
    nothing, the other is a run that could not look."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "work with no declaration in the diff")
    git(repo, "checkout", "-q", "--detach")
    code, out = run(repo, draft=False)
    # Still a pass: the same reasoning `unverified_check.py` gives for an
    # honest open row. What changes is the sentence, and the sentence is the
    # whole value of the row.
    assert code == 0, out
    assert "declared neither way" not in out, out
    assert "branch" in out and "could not be read" in out, out


def test_a_target_naming_two_commits_has_both_checked(repo):
    """`templates/sdd-round.md:12` says *both, if HEAD moved mid-review*, and
    `docs/review-handoff-protocol.md:84` repeats it. The check read the whole
    cell as one ref, so the documented two-SHA form could not resolve and no
    round record has ever been allowed to use it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, "h.py", "z = 3\n")
    second = commit(repo, "more work")
    body = record(sha, passed=True).replace(
        f"| Target SHA | {sha} |",
        f"| Target SHA | {sha} (reviewed); fixes landed at {second} |",
    )
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 0, out


def test_a_target_whose_second_commit_is_off_this_branch_fails(repo):
    """Both have to be ancestors, or the second SHA is a place to hide one."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    body = record(sha, passed=True).replace(
        f"| Target SHA | {sha} |",
        f"| Target SHA | {sha} (reviewed); fixes landed at deadbeef1234567 |",
    )
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "deadbeef1234567" in out


# --- the check itself has to be able to fail --------------------------------


def test_an_unresolvable_baseline_is_not_a_pass(repo):
    """A shallow checkout lands here, and passing it reports a check that
    never ran."""
    r = subprocess.run(
        [sys.executable, CHECK, "--baseline", "origin/nope", "--root", str(repo)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    assert r.returncode == 2, r.stdout + r.stderr
    assert "does not resolve" in r.stdout + r.stderr


# --- what a squash destroys, and what it must not excuse ---------------------
#
# `CONTRIBUTING.md` has feature branches squash into the release branch, and
# the commits a round reviewed are exactly what a squash discards. Requiring
# the target to be an ancestor of HEAD asserted a property the branching model
# destroys on purpose, and it failed on this repository's own release.
#
# Narrowing the requirement to records the pull request CHANGED does not reach
# it: a new work item's round records are added relative to `main`, so they are
# in every release pull request's diff. Measured before writing these — the
# release → `main` diff listed all five. So the requirement moved instead: an
# ancestor of HEAD, or of the branch the declaration names.


def squashed(repo, target_on_feature=True):
    """A release branch carrying `feature` as one squashed commit.

    Returns the SHA the round record names — a commit that exists on
    `feature` and, after the squash, nowhere in the release branch's history.
    """
    write(repo, f"{ITEM}/routing.md", declaration(branch="feature"))
    commit(repo, "declare")
    write(repo, "f.py", "x = 2\n")
    reviewed = commit(repo, "the work the round reviewed")
    write(repo, f"{ROUNDS}/round-1.md", record(reviewed, passed=True))
    commit(repo, "round 1")
    git(repo, "switch", "-qc", "release", "base")
    git(repo, "merge", "--squash", "-q", "feature")
    commit(repo, "squash feature into the release branch")
    if target_on_feature:
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "merge-base",
                "--is-ancestor",
                reviewed,
                "feature",
            ],
            check=True,
            capture_output=True,
        )
    return reviewed


def test_a_target_the_squash_discarded_passes_when_the_branch_still_has_it(repo):
    """#61. The record IS in this pull request's diff, and its target is not
    an ancestor of HEAD — both true, and the review really happened."""
    reviewed = squashed(repo)
    assert (
        subprocess.run(
            ["git", "-C", str(repo), "merge-base", "--is-ancestor", reviewed, "HEAD"]
        ).returncode
        != 0
    ), "the fixture did not actually squash the reviewed commit away"
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "must be reachable from HEAD or refs/heads/feature" in out


def test_a_target_the_squash_discarded_fails_once_nothing_carries_it(repo):
    """This used to pin the cost of reading the BRANCH: delete a feature
    branch before its release reaches `main` and that pull request goes red.
    It went red — a release pull request, six commits across five work
    items, five branches deleted by hand. The branch is no longer the only
    place looked at, so what is pinned here now is the remaining failure: a
    target nothing carries at all.

    The message is asserted because a red build whose cause is a checkout
    that never fetched `refs/pull/*/head` is unreadable without it, and that
    is a different repair from a lost commit."""
    squashed(repo)
    git(repo, "branch", "-qD", "feature")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "not an ancestor of HEAD" in out
    assert "refs/pull/*/head" in out, (
        "the failure has to name the fetch — the commit is usually still "
        "there, on a ref this clone never asked for"
    )


def test_a_merged_record_whose_commits_are_gone_is_not_re_examined(repo):
    """A record that arrived in an earlier merge is history. Its SHAs are
    expected to be gone, and asserting anything about them now re-fails a
    review that already passed at the pull request which added it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record("0" * 40, passed=True))
    commit(repo, "round 1")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "later work, touching neither the declaration nor the record")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "not changed by this pull request" in out
    assert "0000000" not in out, (
        "a SHA nothing resolves is the expected state for a merged record; "
        "naming it reads as a finding"
    )


def test_a_merged_record_is_still_read_for_everything_else(repo):
    """Only the reachability claim is dropped. A merged record that contradicts
    itself is still a contradiction, and the pull request can still fix it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record("0" * 40, passed=True, verdict="still looking"),
    )
    commit(repo, "round 1")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "later work")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "still looking" in out


def test_a_record_new_in_the_pull_request_naming_a_foreign_commit_still_fails(repo):
    """The teeth the relaxation must not remove. `other` is a real commit in
    this repository, reachable from a ref — and the declaration does not name
    that branch, so it is still a review of something this pull request does
    not carry."""
    git(repo, "switch", "-qc", "other", "base")
    write(repo, "h.py", "z = 3\n")
    foreign = commit(repo, "a commit on a branch nobody declared")
    git(repo, "switch", "-q", "feature")
    write(repo, f"{ITEM}/routing.md", declaration(branch="feature"))
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(foreign, passed=True))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert foreign[:7] in out
    assert "not an ancestor of HEAD or refs/heads/feature" in out


# --- a record left at the old location ---------------------------------------


def test_a_record_still_at_the_top_level_fails_naming_it_and_the_destination(repo):
    """S3, the CI half. Two substrings, not merely a non-zero exit.

    No fallback ships and nothing migrates a repository that updates the
    plugin, so a work item whose records stayed flat fails its pull request.
    That is only bearable because the failure says which file and where it
    goes; degraded to `holds no round-N.md` it says a review never happened,
    which is false and unactionable at once.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/round-1.md", record(sha, passed=True))
    commit(repo, "round 1, at the old location")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{ITEM}/round-1.md" in out, out
    assert f"{ITEM}/rounds/" in out, out


def test_a_stray_does_not_report_as_a_review_that_never_happened(repo):
    """The sentence that would replace the one above if the stray check were
    dropped. It is what every un-migrated repository would see.

    The positive half is asserted alongside the negative one deliberately.
    On its own, `not in out` also passes when the check says NOTHING, which
    is the second way this could go wrong and the quieter of the two.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/round-1.md", record(sha, passed=True))
    commit(repo, "round 1, at the old location")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{ITEM}/round-1.md" in out, out
    assert "holds no `round-N.md`" not in out, out
    # The command it prescribes has to run. `git mv` alone fails with
    # `destination directory does not exist`, and the slash-less retry that
    # follows renames the record to a FILE. Asserted on the RENDERED message
    # rather than the source, because a source check is defeated by degrading
    # the command to its own name.
    assert "mkdir" in out and "git mv" in out, out


def test_a_round_record_git_carries_as_a_file_is_named(repo):
    """`rounds` as a BLOB, the state the slash-less `git mv` retry produces.

    The filesystem reader learned this in round 1 and this one did not, so the
    same repository was told two different things about the same tree: the
    hook named the state, and the pull request said `holds no round-N.md` —
    which this file's own header calls true and indistinguishable from a work
    item that skipped its review. Worse here, because the `mkdir` that message
    then prescribes fails with `File exists`.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/rounds", record(sha, passed=True))
    commit(repo, "rounds as a file")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "is not a directory" in out, out
    assert "holds no `round-N.md`" not in out, out


def test_rounds_as_a_tracked_symlink_is_named_too(repo):
    """The same state, in the spelling git uses for a link.

    Round 2 added the FILE check here and built it on `tracked_files`, whose
    mode allow-list is `100644`/`100755`. Git carries a symbolic link as
    `120000`, so it fell straight through and the two readers went back to
    opposite answers for one tree — the exact state the function was added
    for. Not hypothetical: `tracked_files`'s own docstring records a tracked
    symbolic link turning exit 1 into exit 0 in this repository.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/real-round-1.md", record(sha, passed=True))
    symlink_or_skip("real-round-1.md", repo / ITEM / "rounds")
    commit(repo, "rounds as a symlink")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "is not a directory" in out, out
    assert "holds no `round-N.md`" not in out, out


def dir_link(repo, item):
    """`rounds` as a symlink to a DIRECTORY that holds a record.

    Round 4's fourth shape. The hook follows the link, reads the record and
    says nothing; the pull-request check sees `120000`, is not a tree, and
    fails telling the reader to `mkdir` a path that already exists. Three
    shapes were enumerated and the fourth split them again.
    """
    real = item / "real-rounds"
    real.mkdir()
    (real / "round-1.md").write_text("| Target SHA | `x` |\n", encoding="utf-8")
    symlink_or_skip("real-rounds", item / "rounds")


def test_the_two_readers_agree_on_every_shape_of_rounds(repo):
    """One tree, one answer. The hook and the pull-request check are separate
    implementations of `rounds_unreadable`, and every round so far has found
    them disagreeing on a shape one of them had not been taught.
    """
    guard = load_hook_module("routing.py", "routing_agree")
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    item = repo / ITEM

    def both(build):
        for stale in (item / "rounds",):
            if stale.is_symlink() or stale.is_file():
                stale.unlink()
            elif stale.is_dir():
                shutil.rmtree(stale)
        build()
        commit(repo, "shape")
        _, out = run(repo, draft=False)
        return guard.rounds_unreadable(str(item)), "is not a directory" in out

    write(repo, f"{ITEM}/real-round-1.md", record(sha, passed=True))
    commit(repo, "a record to point at")

    # The expected VALUE, not only that the two agree. Round 4 blinded both
    # implementations at once — `return False` in each — and this test stayed
    # green: a property test for "they answer alike" passes the state where
    # neither answers at all, which is the final form of the class it exists
    # to close.
    shapes = {
        "blob": (lambda: (item / "rounds").write_text("x", encoding="utf-8"), True),
        "symlink": (
            lambda: symlink_or_skip("real-round-1.md", item / "rounds"),
            True,
        ),
        "dir-symlink": (lambda: dir_link(repo, item), True),
        "tree": (
            lambda: (
                (item / "rounds").mkdir(),
                write(repo, f"{ITEM}/rounds/round-1.md", record(sha, passed=True)),
            ),
            False,
        ),
    }
    for name, (build, unreadable) in shapes.items():
        hook, check = both(build)
        assert hook == check == unreadable, (
            f"{name}: expected {unreadable}; the hook says {hook} and the "
            f"pull-request check says {check}"
        )


def test_a_stray_beside_a_real_record_still_has_its_pass_read(repo):
    """A stray must not become a way past the verdict check. Reporting it and
    then stopping would let a work item hide a failing round in `rounds/`
    behind one stale file at the top level."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ITEM}/round-1.md", record(sha, passed=True))
    write(repo, f"{ROUNDS}/round-2.md", record(sha, passed=True, verdict="open"))
    commit(repo, "one stray, one real")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"{ITEM}/round-1.md" in out, out
    assert "`Pass` is checked" in out, out


# --- round 1: what the reachability rule got wrong -----------------------------
#
# Every case below is a defect round 1 reached by execution, not by reading.


def test_a_work_item_id_git_quotes_keeps_its_reachability_check(repo):
    """`git diff --name-only` quotes and octal-escapes a path holding
    non-ASCII, a quote or a backslash under `core.quotePath`, which is on by
    default. `round_records` builds its paths from `ls-tree`, which never
    quotes. The two met in the per-record membership test, it failed, and the
    reachability requirement DISAPPEARED for a record new in the pull request —
    exit 1 before the diff condition existed, exit 0 after it. The line read
    `already merged`, which is what hid it."""
    item = "seal/specs/1780000000-caf\u00e9"
    write(repo, f"{item}/routing.md", declaration(branch="feature").replace(ITEM, item))
    commit(repo, "declare")
    write(repo, f"{item}/rounds/round-1.md", record("deadbeef1234567", passed=True))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "deadbeef1234567" in out
    assert "no claim made" not in out, (
        "a record this pull request just added must never be reported as "
        "one it did not touch"
    )


def test_the_ci_shape_is_the_remote_ref_with_no_local_branch(repo, tmp_path):
    """A pull-request checkout is a detached merge commit with no local
    branches, so `refs/remotes/origin/<branch>` is the ONLY candidate CI can
    take — and it was the one candidate no case ran."""
    bare = tmp_path / "origin.git"
    git(repo, "init", "-q", "--bare", str(bare))
    reviewed = squashed(repo)
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "origin", "feature")
    git(repo, "branch", "-qD", "feature")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "refs/remotes/origin/feature" in out
    assert reviewed[:7] not in out


def test_a_stale_remote_does_not_hide_the_local_branch_that_has_it(repo, tmp_path):
    """Taking the first candidate that resolves and stopping made a stale
    `origin/<branch>` shadow the local branch carrying the commit — and the
    failure advised restoring a branch that was sitting right there."""
    bare = tmp_path / "origin.git"
    git(repo, "init", "-q", "--bare", str(bare))
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "origin", "feature")  # origin/feature pinned here
    reviewed = squashed(repo)  # feature moves on; the remote does not
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert reviewed[:7] not in out


def test_a_tag_cannot_stand_in_for_the_branch_it_shares_a_name_with(repo):
    """`rev-parse <name>` follows git's disambiguation order, where
    `refs/tags/` beats `refs/heads/` — measured, with a `warning: refname is
    ambiguous` that `git()` discards. A tag carrying a commit nobody reviewed
    satisfied the check while the branch's own commits were invisible."""
    git(repo, "switch", "-qc", "unreviewed", "base")
    write(repo, "h.py", "z = 3\n")
    never_reviewed = commit(repo, "a commit no round ever looked at")
    git(repo, "switch", "-q", "feature")
    squashed(repo)
    git(repo, "tag", "feature", never_reviewed)  # same name as the branch
    write(repo, f"{ROUNDS}/round-1.md", record(never_reviewed, passed=True))
    commit(repo, "point the record at the tag's commit")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert never_reviewed[:7] in out


def test_a_branch_cell_naming_a_revision_expression_admits_nothing(repo):
    """The bare name accepted anything git parses as a revision, so a
    `| Branch | main |` cell admitted every commit on `main`. Fully qualified,
    `refs/heads/base~1` is not a ref and contributes no candidate."""
    write(repo, f"{ITEM}/routing.md", declaration(branch="base"))
    commit(repo, "declare against the base branch")
    write(repo, f"{ROUNDS}/round-1.md", record("0" * 40, passed=True))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "refs/heads/base" in out, out


def test_a_merged_record_still_needs_its_target_sha_row(repo):
    """Only the reachability claim is dropped for an untouched record.
    `check_round`'s docstring says the row itself is still required, and
    nothing pinned it."""
    write(repo, f"{ITEM}/routing.md", declaration())
    commit(repo, "declare")
    body = record("0" * 40, passed=True).replace(
        "| Target SHA | 0000000", "| Nope | 0000000"
    )
    write(repo, f"{ROUNDS}/round-1.md", body)
    commit(repo, "round 1 with no Target SHA row")
    git(repo, "branch", "-f", "base", "HEAD")
    write(repo, "g.py", "y = 2\n")
    commit(repo, "later work")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "which commit this round actually looked at" in out


# --- a reviewed commit outlives the branch it was on ------------------------


def reviewed_elsewhere(repo):
    """A commit that exists, is on no branch, and is not an ancestor of HEAD.

    Which is what every squashed review round's `Target SHA` becomes: the
    squash writes a new commit and the originals live on until whoever merged
    presses Delete branch.
    """
    git(repo, "switch", "-qc", "throwaway")
    write(repo, "g.py", "y = 1\n")
    commit(repo, "the commit the round reviewed")
    sha = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "switch", "-q", "feature")
    git(repo, "branch", "-qD", "throwaway")
    return sha


def declared_round(repo, sha, pr=None, branch="gone"):
    write(repo, f"{ITEM}/routing.md", declaration(branch=branch))
    commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, pr=pr, passed=True))
    commit(repo, "round 1")


def test_a_deleted_branch_is_what_this_used_to_fail_for(repo):
    """The control, and it is a real incident rather than a hypothetical.

    A release pull request went red naming six commits across five work
    items. `delete_branch_on_merge` is false in that repository, so nothing
    deleted the branches automatically — a paragraph asked people not to, and
    five were deleted anyway."""
    sha = reviewed_elsewhere(repo)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 1, out
    assert "not an ancestor" in out


def test_the_pull_head_that_carried_it_is_enough(repo):
    """And it needs nothing written in the record. `refs/pull/<N>/head` is
    GitHub's, a squash does not touch it and deleting the branch does not
    either."""
    sha = reviewed_elsewhere(repo)
    git(repo, "update-ref", "refs/remotes/pull/7/head", sha)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 0, out


def test_the_record_may_name_its_pull_request_and_then_the_ref_is_exact(repo):
    """The `| PR |` row was already in the template with nothing reading it.

    Where it names a number the check looks there, and a success cannot show
    that — the answer is the same either way. The FAILURE can: it names
    `refs/pull/7/head` instead of a namespace, so a reader is told which pull
    request was supposed to carry this and did not."""
    sha = reviewed_elsewhere(repo)
    # The row's number resolves, and it is not what carries the commit.
    git(repo, "update-ref", "refs/remotes/pull/7/head", "HEAD")
    declared_round(repo, sha, pr=7)
    code, out = run(repo)
    assert code == 1, out
    assert "refs/remotes/pull/7/head" in out, out


def test_a_pull_row_naming_a_ref_this_clone_lacks_is_left_out_of_the_message(repo):
    """The row is read for the message, so the message must not name a ref
    that is not here. `refs/pull/9/head` printed by a clone that never fetched
    the namespace reads as "that pull request does not carry it" when the true
    state is "this checkout never asked" — and those are different repairs.
    The fetch line covers the second one and says so."""
    sha = reviewed_elsewhere(repo)
    declared_round(repo, sha, pr=9)
    code, out = run(repo)
    assert code == 1, out
    assert "refs/remotes/pull/9/head" not in out, out
    assert "refs/pull/*/head" in out, out


def test_a_pull_row_naming_no_number_is_not_an_error(repo):
    """`not yet opened` is the honest value while the review runs, and the
    scan covers that case with nothing written at all."""
    sha = reviewed_elsewhere(repo)
    git(repo, "update-ref", "refs/remotes/pull/7/head", sha)
    declared_round(repo, sha, pr="not yet opened")
    code, out = run(repo)
    assert code == 0, out


def test_a_tag_carrying_the_commit_does_not_count(repo):
    """The narrowness is the point. `target_refs` records what resolving a
    bare name cost — `refs/tags/` beats `refs/heads/`, and a tag carrying a
    commit nobody reviewed satisfied the check. Accepting any ref that holds
    the SHA would re-open exactly that."""
    sha = reviewed_elsewhere(repo)
    git(repo, "tag", "reviewed", sha)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 1, out


def test_the_failure_says_which_fetch_is_missing(repo):
    """`refs/pull/*/head` is not in a default clone, so "not fetched" and "not
    there" are different repairs. A message that confuses them sends somebody
    to restore a branch that would not have helped."""
    sha = reviewed_elsewhere(repo)
    declared_round(repo, sha)
    code, out = run(repo)
    assert code == 1, out
    assert "refs/pull/*/head" in out, out


# --- the broad gate, which nothing read until #295 --------------------------
#
# `Broad gate` was written on every record and read by nothing:
# `grep -n broad chain_check.py` matched no line at all before this work item.
# So the one full-suite run the whole design turns on could be skipped, or
# spent before the round it was meant to seal, and every gate in the
# repository was silent about it.
#
# Every case here needs a record carrying all seven of the earlier cutoffs'
# rows, because `GATE_FROM` is later than every one of them: a work item held
# to this rule is held to those too. `gated_record` is that record, and the
# item id is what each case varies.


def gated_item(began, slug="a-work-item"):
    """A work item directory whose id decides which cutoffs reach it."""
    return f"seal/specs/{began}-{slug}"


def gated_record(sha, gate=None, passed=True, verdict="answered", rng=None):
    """A record that passes every other check, so the gate arm is what fails.

    `gate=None` leaves the `| Broad gate |` row out, which is a state of its
    own: the cell names no run, and it is indistinguishable from `not yet`
    for the one question this arm asks.

    `rng=None` leaves the `| Fix range |` row out the same way, which is the
    state every record written before that rule is in.
    """
    box = "x" if passed else " "
    gate_row = f"| Broad gate | {gate} |\n" if gate is not None else ""
    range_row = f"| Fix range | {rng} |\n" if rng is not None else ""
    return (
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {sha} |\n"
        f"{gate_row}{range_row}"
        "| Fixes checked by | no fixes to check |\n"
        "| Contract changes | none |\n"
        "| New units | none |\n"
        "| Ran by | specseal:warden on a model |\n"
        "| Needs a fix | no |\n"
        "| Loses a record or crashes | no |\n\n"
        f"- [{box}] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        f"| 🔴 1 | something | `f.py:1` | {verdict} | grounds |\n"
    )


def gated(repo, began, gate=None, target="first", **kwargs):
    """Three commits, a declaration, and a record. Returns the run's args.

    `target` picks which commit the record says it reviewed, and that is the
    whole comparison this arm makes:

      `first`   the record reviewed c1 and the gate ran at c2 — after it
      `second`  the record reviewed c2 and the gate ran at c1 — BEFORE it,
                which is the run spent before the round it was meant to seal
    """
    item = gated_item(began)
    write(repo, f"{item}/routing.md", declaration())
    first = commit(repo, "declare")
    write(repo, "another.py", "z = 3\n")
    second = commit(repo, "a commit the round could have reviewed")
    named = first if target == "first" else second
    resolved = {"first": first, "second": second}.get(gate, gate)
    write(
        repo,
        f"{item}/rounds/round-1.md",
        gated_record(named, gate=resolved, **kwargs),
    )
    commit(repo, "round 1")
    return first, second


def test_a_broad_gate_that_never_ran_fails_a_ready_pull_request(repo):
    """#295's first half. `not yet` is the run that never happened.

    The cell was written on every record and read by nothing, so a work item
    could open a ready pull request having never run the one full-suite pass
    the design turns on — and no gate in the repository had an opinion.
    """
    gated(repo, GATE_FROM, gate="not yet")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "Broad gate" in out, "the failure names the row it read"
    assert "not yet" in out, (
        "and quotes the cell back. A refusal that does not say what it read "
        "sends somebody to look for a different cell"
    )
    assert "sealer" in out and "broad-gate" in out, (
        "#30: the refusal tells a reader to run the pass by hand, where the "
        "route is now a spawn. A message naming no agent is where the act "
        "goes back to whoever is reading it"
    )


def test_a_not_yet_carrying_its_reason_is_still_a_run_that_never_happened(repo):
    """The spelling records in this tree actually use.

    Every `not yet` cell written so far carries a reason after a separator —
    `not yet — a 🔴 was open`, `not yet — round 5 verifies these fixes`. An
    arm matching the bare two words would have passed every one of them, and
    the cell means the same thing with the reason as without it.
    """
    gated(repo, GATE_FROM, gate="not yet — a 🔴 was open")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "Broad gate" in out


def test_a_broad_gate_row_that_is_absent_names_no_run_either(repo):
    """An absent row is the same state as `not yet`, and must read that way.

    `round_record.py new` writes this row on every record it generates, with
    `not yet` when nothing has run — so above the cutoff an absent row cannot
    arise honestly. Reading it as "nothing to check" would make deleting one
    line the way past the whole arm.

    That last reason was false when this case was written, and round 1's 🔴 2
    is where it was measured: a cell holding one word this arm cannot parse
    was a notice, so `skipped` was a shorter way past than deleting the row.
    `test_a_one_word_cell_is_not_a_way_past_the_arm` is what closed the
    shorter way, and it is what makes this case's own grounds true.
    """
    gated(repo, GATE_FROM, gate=None)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "Broad gate" in out


def test_a_broad_gate_spent_before_the_round_it_was_meant_to_seal_fails(repo):
    """#295's second half, and the more expensive of the two.

    A run taken before the round finished is worse than no run at all,
    because the record claims one happened. `CLAUDE.md` §*Verification Scope*
    is the rule it breaks: a broad run with an edit after it was spent, not
    banked — and the round's own fixes are edits after it by definition.
    """
    first, second = gated(repo, GATE_FROM, gate="first", target="second")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert first[:7] in out and second[:7] in out, (
        "both SHAs, or the reader cannot tell which run was spent and which "
        "commit it failed to cover"
    )
    # Round 1's 🟡 8. This arm prints three fatal refusals; #30 re-pointed
    # two of them to the sealer's spawn and left this one telling the reader
    # to take the run by hand — in the same function, reached by the same
    # person at the same moment. The enumeration was one short, in the one
    # function the branch had opened.
    assert "sealer" in out and "broad-gate --base" in out, (
        "the premature refusal names no agent and no command, so the reader "
        f"is told to take the run themselves:\n{out}"
    )


def test_a_broad_gate_taken_after_the_rounds_settled_passes(repo):
    """The state the whole arm exists to let through, and it passes SILENTLY.

    The silence is asserted because the exit code alone does not hold this
    case: round 1's 🟡 3 added a reported state, and a mutation removing the
    at-or-after pass left this case green — the honest shape fell through to
    *different line of history*, which is a notice at exit 0. So the gate
    ran after the round, the arm said it had no idea, and nothing was red.
    """
    gated(repo, GATE_FROM, gate="second", target="first")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert BROAD_GATE_ROW not in out, (
        "the arm printed something about a gate run that is exactly right. "
        f"The passing shape has nothing to say\n{out}"
    )


def test_a_broad_gate_at_the_very_commit_the_round_reviewed_passes(repo):
    """Equal is not premature, and `--is-ancestor` says a commit is its own.

    So the comparison cannot be ancestry alone: `merge-base --is-ancestor X X`
    exits 0, and an arm resting on it would fail the exactly-correct case —
    the round reviewed a commit and the gate ran at that commit.

    Silent for the reason the case above is: exit 0 beside a notice is a
    state this arm now has, so a pass has to be told from a shrug.
    """
    gated(repo, GATE_FROM, gate="first", target="first")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert BROAD_GATE_ROW not in out, (
        f"the exactly-correct case was reported rather than passed\n{out}"
    )


def test_a_draft_may_still_have_no_broad_gate_run(repo):
    """The rounds are allowed to still be running.

    This is the third thing `strict` excuses, and the reason is the one the
    other two have: the broad gate runs once, AFTER the rounds settle, so a
    draft whose cell reads `not yet` is telling the truth.
    """
    gated(repo, GATE_FROM, gate="not yet")
    code, out = run(repo, draft=True)
    assert code == 0, out


@pytest.mark.parametrize("kwargs", UNKNOWN_SHAPES, ids=UNKNOWN_IDS)
def test_an_unknown_state_is_held_to_the_broad_gate_too(repo, kwargs):
    """The same trap #296 opens, at the arm that would pay for it.

    If `unknown` were read as a draft, then `no pull-request context` would
    excuse the record's existence AND the broad gate AND the checked `Pass`
    all at once — which is the whole check. All four shapes, from the list
    above: the two this arm was missing are the string draft and the payload
    naming no pull request, which are the two the build's own record calls
    dangerous.
    """
    gated(repo, GATE_FROM, gate="not yet")
    code, out = run(repo, **kwargs)
    assert code == 1, out
    assert "Broad gate" in out


def test_a_work_item_one_second_below_the_cutoff_is_not_failed_for_it(repo):
    """The eighth cutoff, and why it is not optional.

    Every round record ever written defaults to `Broad gate: not yet`, so an
    arm reading the cell without a cutoff fails every work item in flight —
    including one whose rounds were running while this was built. The
    reasoning is `chain_check.py`'s own, at `STRICT_FROM`: a check whose first
    production act is red on history nobody can fix is a check people learn
    to skip.
    """
    gated(repo, GATE_FROM - 1, gate="not yet")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "Broad gate" in out, (
        "excused is not the same as unread. The state prints, the way every "
        "other cutoff in this file prints for a record it excuses"
    )


def test_a_work_item_at_the_cutoff_is_held_to_it(repo):
    """`>=`, the way the seven before it are keyed.

    Each of those constants is the id of the work item that ADDED its rule,
    so the first records held to a rule are the ones written under it. This
    case and the one above it are one second apart and are the whole boundary.
    """
    gated(repo, GATE_FROM, gate="not yet")
    code, out = run(repo, draft=False)
    assert code == 1, out


def test_a_work_item_whose_id_is_not_a_date_is_grandfathered(repo):
    """A repository that names its work items some other way has no date to
    compare, and failing it would be failing it for a naming convention."""
    item = "seal/specs/a-work-item-with-no-date"
    write(repo, f"{item}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{item}/rounds/round-1.md", gated_record(sha, gate="not yet"))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 0, out


def test_a_broad_gate_cell_nobody_can_parse_is_reported_below_the_cutoff(repo):
    """`questions.md` assumption 3, bounded by the cutoff it rests on.

    Nothing validates this cell where it is WRITTEN — that is Q4, and it is
    the owner's — so records written before `GATE_FROM` hold free text, and a
    real one in this tree reads `due after this record — see the row below`.
    Failing THOSE would be the retroactive red the cutoff exists to avoid,
    arriving through the reader instead of through the date.

    This case used to run AT the cutoff, which pinned the leniency at the one
    id where the arm is meant to apply — round 1's 🔴 2. Its real subject is a
    record from below the cutoff, which is where it now runs; the case beneath
    it is the other half.
    """
    gated(repo, GATE_FROM - 1, gate="due after this record — see the row below")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "Broad gate" in out, (
        "reported, which is the half that is not optional. A cell nobody can "
        "parse and a cell nobody wrote must not look the same"
    )


@pytest.mark.parametrize(
    "cell", ["pending", "skipped", "n/a", "TBD", "not run", "-", "due later"]
)
def test_a_one_word_cell_is_not_a_way_past_the_arm(repo, cell):
    """Round 1's 🔴 2. Above the cutoff, a cell with no SHA in it is a choice.

    An absent row fails and `not yet` fails, so leaving every OTHER word a
    notice made writing one the cheapest way past this arm there is — cheaper
    than deleting the row, which is the edit the absent-row judgment was taken
    to close. `skipped` is not an exotic value: it is the word a session that
    skipped the run would write.

    Above the cutoff there is no free-text history to grandfather.
    `round_record.py new` writes this row on every record it generates, and
    `seal` and `close --broad-gate` are the only things that change the value
    (#30 added the first), so a cell this arm cannot parse above `GATE_FROM`
    is a cell somebody chose. Below it the tail of the same function still
    grandfathers, which is the case above.
    """
    gated(repo, GATE_FROM, gate=cell)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "Broad gate" in out and cell in out, (
        "and it quotes the cell back, so nobody goes looking for a different row"
    )
    assert "sealer" in out and "close --broad-gate" in out, (
        "#30: this arm's message names one route where there are two, and the "
        "one it named is the exception rather than the ordinary path"
    )


def test_a_gate_sha_on_a_divergent_line_makes_no_claim_and_says_so(repo):
    """Round 1's 🟡 3. The arm asked one question — is the gate an ancestor of
    the target — which is the PREMATURE direction, so everything that is
    neither equal to the target nor descended from it passed, and passed in
    silence. That is quieter than the notice an unresolvable SHA already gets:
    the arm said nothing about the case it could check and something about the
    case it could not.

    `spec.md` names three shapes — `not yet`, premature, at-or-after — and a
    commit on a line the branch never descended from is none of them.
    """
    item = gated_item(GATE_FROM)
    write(repo, f"{item}/routing.md", declaration())
    first = commit(repo, "declare")
    git(repo, "checkout", "-q", "-b", "side", first)
    write(repo, "side.py", "s = 1\n")
    side = commit(repo, "a commit on a line the branch never descended from")
    git(repo, "checkout", "-q", "feature")
    write(repo, "another.py", "z = 3\n")
    second = commit(repo, "the commit the round reviewed")
    write(repo, f"{item}/rounds/round-1.md", gated_record(second, gate=side))
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "different line of history" in out, (
        "a resolvable gate SHA the arm cannot relate to the target must not "
        f"be quieter than one it cannot resolve at all\n{out}"
    )


def test_a_gate_sha_this_repository_cannot_see_makes_no_claim(repo):
    """A squash discards the commits a round reviewed, and the gate ran at one
    of them. `resolves_to` returning None is the ordinary state after a merge,
    not a fault — the same "no claim" `check_round` already makes for a record
    the pull request does not touch."""
    gated(repo, GATE_FROM, gate="9f9f9f9")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "9f9f9f9" in out, "and it says which SHA it could not resolve"


def test_the_broad_gate_label_has_one_spelling_both_scripts_read():
    """The cell's name and its sentinel moved to the reader that now needs
    them, and the writer imports them from there.

    Two copies of `Broad gate` would drift the moment either script renamed
    the row, and the failure would be silent in the direction that matters:
    the writer would keep writing a row the reader no longer finds, which
    this arm reads as *no run was named*.
    """
    chain = _module(
        "specseal_chain_check_labels",
        os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py"),
    )
    record_mod = _module(
        "specseal_round_record_labels",
        os.path.join(ROOT, "skills", "code-review", "scripts", "round_record.py"),
    )
    assert chain.BROAD_GATE == "Broad gate"
    assert chain.GATE_NOT_YET == "not yet"
    assert chain.GATE_FROM == GATE_FROM, (
        "the cutoff this module's boundary cases are written around. They sit "
        "one second either side of it, which measures nothing if the number "
        "is read from the thing under test"
    )
    assert record_mod.BROAD_GATE == chain.BROAD_GATE
    assert record_mod.GATE_NOT_YET == chain.GATE_NOT_YET

    # The values agreeing proves nothing — two copies of a literal agree
    # until one of them is edited, which is the whole failure. What is
    # asserted is that there is ONE spelling: the reader defines it and the
    # writer names the reader. An `is` comparison cannot say this either,
    # because the two scripts load `chain_check.py` as separate module
    # objects and `"Broad gate"` is not an identifier, so it is not interned.
    reader_src = open(
        os.path.join(ROOT, "skills", "code-review", "scripts", "chain_check.py"),
        encoding="utf-8",
    ).read()
    writer_src = open(
        os.path.join(ROOT, "skills", "code-review", "scripts", "round_record.py"),
        encoding="utf-8",
    ).read()
    assert reader_src.count('"Broad gate"') == 1, (
        "the label is defined once, in the script that reads it"
    )
    assert '"Broad gate"' not in writer_src, (
        "and the script that WRITES the row takes the label from the reader. "
        "Rename it here alone and `round_record.py` keeps writing a row "
        "`chain_check.py` no longer finds, which that arm reads as `no run "
        "was named` — a silent pass where the state is unknown"
    )
    assert "BROAD_GATE = chain.BROAD_GATE" in writer_src
    assert "GATE_NOT_YET = chain.GATE_NOT_YET" in writer_src


# --- the real records, which no test and no local run ever read -------------


def _module(name, path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# A record's path, spelled once and matched whole. Git's pathspec globbing
# lets `*` cross a slash, so `seal/specs/*/rounds/round-*.md` handed to git is
# wider than it looks; the listing is taken over `seal/specs` and narrowed
# here, where `fullmatch` means what the pattern says.
RECORD_PATH_RE = re.compile(r"seal/specs/[^/]+/rounds/round-[^/]*\.md")


def _real_records(root=ROOT):
    """Every `seal/specs/*/rounds/round-*.md` git carries at HEAD.

    From `git ls-tree HEAD` rather than `git ls-files`, because the
    per-record readers below take their content from `git show HEAD:<rel>`.
    `ls-files` reads the INDEX, so a record staged and not committed was
    listed here and then had no content at HEAD — `read_record` answers
    `None`, every per-record check returns `([], [])`, and the walk reported
    nothing about a record it had just listed. Listed-and-skipped is silent,
    which is worse than not listed at all: the case stayed green over a
    record nobody checked (#142).

    `root` is a parameter so the lister itself has a case
    (`test_the_real_records_lister_reads_head_and_not_the_index`); every
    caller in this repository's own walk leaves it at `ROOT`.
    """
    out = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "ls-tree",
            "-r",
            "-z",
            "--name-only",
            "HEAD",
            "--",
            "seal/specs",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    ).stdout
    return sorted(p for p in out.split("\0") if RECORD_PATH_RE.fullmatch(p))


def _the_walk_found_every_committed_record(records, what, root=ROOT):
    """The population guard for a sweep of this repository's own records.

    It replaces `assert len(records) > 200` at the two sweeps below. The
    floor was answering the right question — *did the walk read anything* —
    with a literal that stops being true the moment the corpus shrinks, and
    `settle --retire` shrank it from 263 records to 7 in one commit. A floor
    lowered to fit is a comment (`skills/settle/SKILL.md` §3), so the
    question is asked against the tree instead.

    **Two independent routes to the same population.** The sweeps build
    `records` by walking `seal/specs/` on disk; this compares that against
    `_real_records()`, which is `git ls-tree HEAD`. Neither can go quiet
    without the other noticing, and the comparison says nothing about how
    many records there are — it holds at 263 and at 7.

    **`on_disk` before the comparison, for the reason it exists.** A record
    git carries at HEAD and the working tree has deleted is listed with
    nothing behind it (#432, #282), and that is the ordinary state at step 3
    of `docs/release-checklist.md`. Comparing the raw listing against a walk
    of the disk would report every such path as a record the walk missed,
    which is a fact about the release sequence rather than about the sweep.

    **The walk may hold MORE than the listing.** A record written and not yet
    committed is on disk and not at HEAD, which is the ordinary state of a
    review round mid-flight. So the assertion is that the walk covers the
    committed corpus, not that the two sets are equal.

    **`assert listed` stood here, and it was a floor of one.** It asked
    whether the listing found anything, which is the right question with an
    answer the fold turns false: after a complete fold nothing is committed
    under `seal/specs/` and the listing is empty because the corpus is. The
    question is asked of the tree instead —
    `conftest.committed_round_records_on_disk`, a walk of the disk and a
    `git cat-file` per file, has to find nothing the listing lacks — so a
    listing that goes quiet over records that exist is named, and one that is
    empty over an empty corpus is correct (#517, `skills/settle/SKILL.md` §3).
    """
    listed, _missing = on_disk(
        root,
        [
            p
            for p in _real_records(root)
            if re.fullmatch(r"round-\d+\.md", os.path.basename(p))
        ],
    )
    unlisted = sorted(set(committed_round_records_on_disk(root)) - set(listed))
    assert not unlisted, (
        f"{len(unlisted)} record(s) git carries at HEAD are not in the listing "
        f"{what} is checked against, so it reads less than is there: "
        f"{unlisted[:3]}"
    )
    # git names a path with `/` on every platform and a walk joins with
    # `os.sep`, so the comparison is made on one spelling. The doubled-grounds
    # sweep passed its paths unnormalised and this reported all 15 committed
    # records as missed on windows alone.
    walked = {rel.replace(os.sep, "/") for rel in records}
    unwalked = sorted(set(listed) - walked)
    assert not unwalked, (
        f"{len(unwalked)} committed record(s) the tree still has did not "
        f"reach {what}: {unwalked[:3]}"
    )


def test_the_walk_guard_names_what_either_route_missed(repo, monkeypatch):
    """The guard the two sweeps and the per-record walk share, over a corpus
    this case builds — the property the real tree can no longer be relied on
    to exercise once a fold empties it (#517, `skills/settle/SKILL.md` §3).

    Both directions: a walk that missed a committed record, and a listing
    that went quiet over a record git carries. An empty corpus is neither."""
    rel = f"{ROUNDS}/round-1.md"
    write(repo, rel, "# round 1\n")
    commit(repo, "a committed record")
    _the_walk_found_every_committed_record([rel], "the case", root=str(repo))
    with pytest.raises(AssertionError, match="did not reach"):
        _the_walk_found_every_committed_record([], "the case", root=str(repo))
    module = sys.modules[__name__]
    monkeypatch.setattr(module, "_real_records", lambda root=ROOT: [])
    with pytest.raises(AssertionError, match="not in the listing"):
        _the_walk_found_every_committed_record([rel], "the case", root=str(repo))


def _numbered(routing, records):
    """The RECORDS among `records`, by name.

    `round-*.md` is the shape of four files, not one: the review chain writes
    `round-N-report.md`, `round-N-asked.md` and `round-N-fixes.md` beside the
    record. `routing.round_number` answers `None` for those, and it is the one
    place the naming rule lives (`docs/review-handoff-protocol.md` §Layout).
    Two `None`s in one work item also used to make the sort below raise
    `TypeError` rather than fail an assertion; `chain_check.py#round_records`
    already drops them on the same test, and this is the reader that did not.
    """
    return [r for r in records if routing.round_number(os.path.basename(r)) is not None]


def _record_walk(chain, reader, routing, root, records):
    """The per-record checks, over `records`, as a list of failures.

    Extracted so that the positive control below runs THE SAME loop over a
    record known to be refused. An assertion that reads this list cannot tell
    an empty list from a loop that never collected anything, which is what
    left both `failures.extend` calls replaceable by `pass` with the module
    still green (#142).
    """
    by_item = {}
    for rel in records:
        by_item.setdefault(rel.rsplit("/rounds/", 1)[0], []).append(rel)

    failures = []
    for rels in by_item.values():
        ordered = sorted(rels, key=lambda r: routing.round_number(os.path.basename(r)))
        for index, rel in enumerate(ordered):
            errors, _ = chain.fix_surface(reader, root, rel)
            failures.extend(errors)
            errors, _ = chain.stopping_floor(reader, root, rel, ordered[index + 1 :])
            failures.extend(errors)
    return failures


def test_the_real_records_lister_reads_head_and_not_the_index(repo):
    """#142. The lister's docstring said HEAD and the command said the index.

    The two disagree for exactly one file: a record `git add`-ed and not
    committed. `ls-files` lists it, `read_record` finds nothing for it at
    HEAD, and every per-record check returns `([], [])` — so the record was
    listed, skipped, and reported on by nothing.
    """
    write(repo, f"{ROUNDS}/round-1.md", "# round 1\n")
    commit(repo, "a committed record")
    write(repo, f"{ROUNDS}/round-2.md", "# round 2\n")
    git(repo, "add", f"{ROUNDS}/round-2.md")

    listed = _real_records(repo)
    assert f"{ROUNDS}/round-1.md" in listed, listed
    assert f"{ROUNDS}/round-2.md" not in listed, (
        "a staged, uncommitted record is listed. The per-record readers take "
        "their content from HEAD, where it has none, so it is listed and then "
        "silently skipped"
    )


def test_the_walk_over_the_real_records_can_fail(repo):
    """The positive control #142 asks for, through the same call path.

    The case below asserts that a walk over this repository's own records
    collects no failures. Nothing said the walk collects anything at all:
    replacing both `failures.extend(errors)` calls with `pass` left it green,
    and so would a filter that quietly matched no records.

    So: one record whose `New units` cell is empty and whose floor row is
    empty. The first is refused by `fix_surface` on any record, the second by
    `stopping_floor` on any record — neither is grandfathered, because a
    present-and-malformed row is always the author's to fix. Both halves of
    the walk are therefore asserted on, and stubbing EITHER `extend` turns
    this red.
    """
    chain = _module("chain_check_for_the_positive_control", CHECK)
    reader = _module("reader_for_the_positive_control", chain.READER)
    routing = _module("routing_for_the_positive_control", chain.ROUTING)

    sha = git(repo, "rev-parse", "HEAD").stdout.strip()
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        "# round 1\n\n"
        "| Field | Value |\n|---|---|\n"
        f"| Target SHA | {sha} |\n"
        "| Fixes checked by | nobody — the run ended here |\n"
        "| New units |  |\n"
        f"| {chain.FLOOR} |  |\n\n"
        "- [ ] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        "| 🔴 1 | something | `f.py:1` | fixed | grounds |\n",
    )
    commit(repo, "a record the checks refuse")

    records = _numbered(routing, _real_records(repo))
    assert records == [f"{ROUNDS}/round-1.md"], records

    failures = _record_walk(chain, reader, routing, repo, records)
    messages = [message for _rel, _line, message in failures]
    assert any("`New units` is empty" in m for m in messages), messages
    assert any(f"`{chain.FLOOR}` is empty" in m for m in messages), messages


def test_this_repositorys_own_round_records_pass_the_per_record_checks():
    """Round 2's 🔴 1: `round-1.md`'s own `Contract changes` cell was refused
    by the checker the record was describing, and it was committed.

    Nothing looked. The suite builds fixture repositories and never reads the
    real records; a local `chain_check` run reaches them only through a
    routing declaration the branch happens to touch; CI reaches them at the
    pull request, which is after the commit that broke it. So the first
    reader of a record this repository writes was the pull request it was
    written for.

    This is that reader, one step earlier. It calls the per-record functions
    themselves rather than the whole script, because the script's other
    verdicts — an unchecked `Pass` while a run is still going, a `Target SHA`
    that has to be reachable — are true of a branch mid-review and would make
    this red for a state that is correct.

    Notices are not asserted on: an older work item printing what it is
    grandfathered out of is the design, and the assertion is that nothing
    here FAILS.
    """
    chain = _module("chain_check_for_real_records", CHECK)
    reader = _module("reader_for_real_records", chain.READER)
    routing = _module("routing_for_real_records", chain.ROUTING)

    records = _numbered(routing, _real_records())
    # `assert records` stood here: a floor of one, red once a fold empties the
    # corpus. The question it asked — did the glob or the layout move — is
    # asked of the tree instead, at any size (#517).
    unlisted = sorted(set(committed_round_records_on_disk(ROOT)) - set(records))
    assert not unlisted, (
        f"records git carries at HEAD are not in the walk — the glob or the "
        f"layout moved: {unlisted[:3]}"
    )

    failures = _record_walk(chain, reader, routing, ROOT, records)

    assert not failures, "this repository's own records are refused:\n" + "\n".join(
        f"  {rel}: {message}" for rel, _, message in failures
    )


# --- one sentence named two severities for one row (#408) --------------------
#
# `open_blocking` asked `BLOCKING in "".join(seen)`, which is every cell of the
# row. Naming what an earlier round found is exactly what a carried-forward
# closure is for, so a 🟢 row whose Grounds quote an earlier 🔴 was announced
# as a blocking finding in a sentence that then printed `🟢` as the row.

QUOTES_AN_EARLIER_BLOCKER = (
    "| 🟢 | round 1's 🔴 2, re-read | `f.py:2` | {verdict} | "
    "round 1 opened this as 🔴 2 and its fix closed it |\n"
)
BLOCKING_SENTENCE = "a blocking finding that is not fixed, answered or withdrawn"
# What the second arm says instead, and the phrase every case below finds its
# line by. It names the MARKER, which is half of what selected the row --
# `BLOCKING in "".join(seen)` is a 🔴 in any cell but the first, and that is
# not always an earlier round's finding quoted in the Grounds (round 2's ⬜ 3).
QUOTED_SENTENCE = "carries a blocking marker"


def confirmation(repo, verdict):
    """A last record whose only 🔴 is one a 🟢 row QUOTES, at `verdict`."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(
            sha,
            passed=True,
            verdict="fixed",
            finding="🟢 1",
            extra=QUOTES_AN_EARLIER_BLOCKER.format(verdict=verdict),
        ),
    )
    commit(repo, "round 1")
    return run(repo)


def test_a_confirmation_quoting_an_earlier_blocker_is_not_called_a_blocking_finding(
    repo,
):
    """A7. The row is still refused — two things put it here, its quote of an
    earlier 🔴 and a verdict that closes nothing, and either is a way out.
    What must not happen is the refusal calling it a 🔴 row, because the
    reader then goes looking for a blocking finding that belongs to a round
    that is over.

    Red against the whole-row join: the refusal reads *this 🔴 row reads
    `verified` — a blocking finding…* about a row whose `#` cell is 🟢.
    """
    code, out = confirmation(repo, "verified")
    assert code == 1, out
    assert BLOCKING_SENTENCE not in out, (
        "a row whose `#` cell reads 🟢 is announced as a blocking finding",
        out,
    )
    assert QUOTED_SENTENCE in out, out
    (line,) = [ln for ln in out.splitlines() if QUOTED_SENTENCE in ln]
    assert "\N{LARGE RED CIRCLE}" not in line, (
        "the arm for a row that only QUOTES a 🔴 still names one",
        line,
    )


def test_an_unrecognised_verdict_is_refused_by_its_own_name(repo):
    """A8, and §14: the sentence a reader is stopped by. It has to name the
    verdict word, because that is one of the two things that can change, and
    the words that would close the row, because the reader who is stopped is
    the one choosing the replacement.

    **And it has to name the quote**, which is the other half of what put the
    row here (round 1's 🟡 1). A message that names one way out while
    asserting a general rule about the other is #408's own complaint moved
    one cell over.
    """
    code, out = confirmation(repo, "verified")
    assert code == 1, out
    assert QUOTED_SENTENCE in out, out
    (line,) = [ln for ln in out.splitlines() if QUOTED_SENTENCE in ln]
    assert "`verified`" in line, line
    for word in ("`fixed`", "`answered`", "`withdrawn`", "`not a defect`"):
        assert word in line, (word, line)
    assert "drop the marker" in line, line
    assert "leave `Pass` unchecked" in line, line
    assert "outside the vocabulary" not in line, (
        "the arm still says the word is outside a vocabulary this file does "
        "not enforce one row over",
        line,
    )
    # Round 2's ⬜ 4: the same proposition, one clause later and in other
    # words. `open` is the word `agents/warden.md` prescribes, so calling it
    # unrecognised is what dropping `outside the vocabulary` was for.
    assert "unrecognised verdict" not in line, (
        "the arm still calls the author's own prescribed word unrecognised",
        line,
    )


def test_a_row_the_vocabulary_closes_is_silent_even_while_it_quotes_a_blocker(repo):
    """The other direction. The same row with `answered` in its verdict cell
    says nothing at all: the quote and a non-closing verdict are BOTH needed
    to select a row, so closing the verdict is enough to let it through.

    The docstring here used to read *the quote is not what selects a row, and
    it never was*, which is false and is half of round 1's 🟡 1 — the
    selection is `BLOCKING in "".join(seen)` and the quote is what satisfies
    it. `test_a_row_reading_open_is_not_told_its_word_is_unrecognised` below
    holds the other half.
    """
    code, out = confirmation(repo, "answered")
    assert code == 0, out
    assert QUOTED_SENTENCE not in out, out
    assert BLOCKING_SENTENCE not in out, out


def test_a_row_that_carries_a_blocker_keeps_the_blocking_sentence(repo):
    """§14's other half. The 🔴 arm is unchanged, and the split is what makes
    that worth pinning: a repair that moved every row to the new sentence
    would lose the one complaint that is about the finding rather than about
    the word.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(repo, f"{ROUNDS}/round-1.md", record(sha, passed=True, verdict="open"))
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    (line,) = [ln for ln in out.splitlines() if BLOCKING_SENTENCE in ln]
    assert "\N{LARGE RED CIRCLE} row reads `open`" in line, line
    assert QUOTED_SENTENCE not in line, line


# --- the word `open` is not an unrecognised verdict (round 1's 🟡 1) ---------
#
# The split #408 added is keyed on the `#` cell while the SELECTION is still a
# 🔴 anywhere in the row, so the second arm fires on rows it was not naming.
# `open` is the word `agents/warden.md` prescribes, and the first arm prints it
# back as `this 🔴 row reads `open``.

OPEN_ROW_QUOTING_A_BLOCKER = (
    "| 🟡 3 | the guard needs a case | `f.py:3` | open | "
    "round 1 opened this as 🔴 2 and the fix closed it |\n"
)


def test_a_row_reading_open_is_not_told_its_word_is_unrecognised(repo):
    """`open` is the word `agents/warden.md` prescribes for a finding a round
    opened, and the first arm of this same function prints it back as
    `` this 🔴 row reads `open` ``. The second arm must not tell the author
    the word is outside any vocabulary — what selected this row is the quote.

    The fixture is `test_a_checked_pass_beside_an_open_NON_blocking_finding_passes`'s
    row with one thing added: the quote of an earlier round's 🔴 that a
    verifying round is asked to write. That alone flips the row from pass to
    refusal, which is why the refusal has to name it.

    Red against the arm as written: *…reads `open`, which is outside the
    vocabulary…* on a row whose `#` cell reads 🟡.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(
            sha,
            passed=True,
            verdict="fixed",
            finding="🟢 1",
            extra=OPEN_ROW_QUOTING_A_BLOCKER,
        ),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert QUOTED_SENTENCE in out, out
    (line,) = [ln for ln in out.splitlines() if QUOTED_SENTENCE in ln]
    assert "outside the vocabulary" not in line, (
        "`open` is told it is outside a vocabulary, and the first arm of the "
        "same function prints the same word back as a blocking finding",
        line,
    )
    assert "`open`" in line, line
    assert "drop the marker" in line, line
    assert "unrecognised" not in line, line
    assert "\N{LARGE RED CIRCLE}" not in line, line


def test_the_same_open_row_without_the_quote_is_a_pass(repo):
    """The control, and it is what makes the case above about the quote. The
    identical 🟡 row with an ordinary Grounds cell is not refused at all —
    `test_a_checked_pass_beside_an_open_NON_blocking_finding_passes` pins that
    for the one-row record, and this pins it beside a second row so the two
    differ in the quote and nothing else.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(
            sha,
            passed=True,
            verdict="fixed",
            finding="🟢 1",
            extra=OPEN_ROW_QUOTING_A_BLOCKER.replace(
                "round 1 opened this as 🔴 2 and the fix closed it", "read only"
            ),
        ),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out
    assert QUOTED_SENTENCE not in out, out
    assert BLOCKING_SENTENCE not in out, out


# --- a Grounds cell closed twice (#427, the read half) -----------------------

DOUBLED_SENTENCE = "carries `fixed at`"


def test_a_grounds_cell_closed_twice_is_named(repo):
    """#427's read half. `close` refusing the second write stops the NEXT one
    and leaves every one already committed unreadable, and the ticket says so:
    a repair that only stops the second write has closed the instance and not
    the class.

    What makes it worth a checker at all is that the duplication is invisible.
    The record still parses, every other arm here is silent, and the original
    was caught only by reading a committed file against two earlier commits.
    """
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(
            sha,
            passed=True,
            verdict="fixed",
            grounds="fixed at 1575d77; fixed at 1575d77; executed",
        ),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    # The file, the finding, and the repeated text — a reader who cannot find
    # the cell cannot restore it.
    assert f"{ROUNDS}/round-1.md" in out, out
    assert DOUBLED_SENTENCE in out, out
    assert "🔴 1" in out, out
    assert "1575d77" in out, out
    # §14's second half: what to do instead, which is the half a reword drops.
    assert "Restore it" in out, out
    assert "round-record close" in out, out


def test_a_grounds_cell_closed_once_is_not_named(repo):
    """The control. One prefix is what a correct close writes, and the arm has
    to be silent about it or every record in every tree fails."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(sha, passed=True, verdict="fixed", grounds="fixed at 1575d77; executed"),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 0, out
    assert DOUBLED_SENTENCE not in out, out


def test_a_second_close_prefix_naming_another_commit_is_still_two(repo):
    """The shape, not the repetition of one string. Two closes with different
    commits leave two prefixes naming different SHAs, and a check that
    compared the halves to each other would pass exactly the record whose two
    closes were furthest apart."""
    write(repo, f"{ITEM}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{ROUNDS}/round-1.md",
        record(
            sha,
            passed=True,
            verdict="fixed",
            grounds="fixed at 64f36ee; fixed at 1575d77; executed",
        ),
    )
    commit(repo, "round 1")
    code, out = run(repo)
    assert code == 1, out
    assert DOUBLED_SENTENCE in out, out
    assert "64f36ee" in out and "1575d77" in out, out


def test_the_records_in_this_repository_carry_no_doubled_grounds():
    """This repository's own records at exit 0, which is a DISCLOSURE.

    Measured 2026-09-17 at the branch tip: 229 `round-N.md` files, 227 with a
    readable verdict table, 3331 `Grounds` cells, and zero carrying two
    prefixes. The one record that was corrupted this way had it repaired by
    hand before this arm existed. So a green run here says nothing was found,
    never that this arm found something — and the three cases above are what
    give it a subject.

    The population is asserted along with the verdict. A walk that silently
    read nothing would also be green, and green over an empty corpus is the
    shape of a check that cannot fail.
    """
    check = load_by_path(CHECK, "specseal_chain_check_for_doubled")
    reader = load_by_path(
        os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py"),
        "specseal_reader_for_doubled",
    )
    check.WORKTREE = True
    records = [
        os.path.relpath(os.path.join(d, name), ROOT)
        for d, _dirs, names in os.walk(os.path.join(ROOT, "seal", "specs"))
        for name in names
        if re.fullmatch(r"round-\d+\.md", name)
    ]
    _the_walk_found_every_committed_record(records, "the doubled-grounds sweep")
    named = []
    for rel in sorted(records):
        errors, _notices = check.doubled_grounds(reader, ROOT, rel.replace(os.sep, "/"))
        named.extend(errors)
    assert not named, f"records carrying a doubled close prefix: {named}"


# --- the fix range is read against the tree (#344) ---------------------------

# The tenth cutoff, as a literal for the reason the others here are: reading it
# from the script would make every case below agree with whatever the script
# says, including a typo.
RANGE_FROM = 1789621028
RANGE_ROW = "Fix range"


def ranged(repo, began, rng, **kwargs):
    """A declaration and a record whose `Fix range` row is what varies.

    Returns the two commits the range can be written over, so a case can state
    a range the tree holds and a range it does not.
    """
    item = gated_item(began, slug="a-ranged-item")
    write(repo, f"{item}/routing.md", declaration())
    first = commit(repo, "declare")
    write(repo, "another.py", "z = 3\n")
    second = commit(repo, "one commit between the ends")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        gated_record(
            first, gate=f"{first} against base", rng=rng(first, second), **kwargs
        ),
    )
    commit(repo, "round 1")
    return first, second


def test_a_fix_range_the_tree_contradicts_is_named(repo):
    """#344's core. A record states a range, the tree holds a different one,
    and until now nothing compared them — `evidence-check` does exactly this
    job for the ledger over content anchors, and the records were left out.

    The count is the half that catches a row nobody can re-derive. Its ends
    still resolve; what moved is how many commits lie between them.
    """
    ranged(repo, RANGE_FROM, lambda a, b: f"`{a}..{b}`, 7 commits")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert RANGE_ROW in out, out
    assert "says 7 commits" in out, out
    assert "the tree holds 1" in out, out
    # §14's second half: what to do about it, and which of the two halves to
    # suspect. A refusal that names only the mismatch sends somebody to edit
    # the number, which is the wrong repair when the ends are what moved.
    assert "git log --oneline" in out, out
    assert "what to correct rather than the number" in out, out


def test_a_fix_range_the_tree_confirms_passes(repo):
    """The control. The identical record with the count the tree actually
    holds is not refused at all, so the case above is about the comparison."""
    ranged(repo, RANGE_FROM, lambda a, b: f"`{a}..{b}`, 1 commit")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert RANGE_ROW not in out, out


def test_a_fix_range_this_repository_cannot_see_prints(repo):
    """The squash. A feature branch squashes into its release branch and the
    squash keeps none of the branch's own commits, so a merged record's fix
    commits are ordinarily invisible. Failing there would fail every record at
    the moment its work shipped, for something the record did not do wrong.
    """
    ranged(repo, RANGE_FROM, lambda a, b: f"`{'0' * 40}..{'1' * 40}`, 3 commits")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert RANGE_ROW in out, "the state is reported even though it is not failed"
    assert "squash" in out, out


def test_a_fix_range_that_states_no_readable_range_is_named(repo):
    """A present cell nobody can parse is always the author's to fix, which is
    the line `fix_surface` already draws between a malformed row and an absent
    one. `HEAD` written into the cell by hand is the shape this catches after
    the generator's own refusal has been bypassed."""
    ranged(repo, RANGE_FROM, lambda a, b: f"`{a}..HEAD`, four commits")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert RANGE_ROW in out, out
    assert "does not state a range this can read" in out, out
    assert "names that move" in out, out


def test_a_fix_range_saying_none_is_not_read_against_anything(repo):
    """A round that commissioned no fixes has no range, and this is the value
    the row starts at — a record is committed before its fixes exist."""
    ranged(repo, RANGE_FROM, lambda a, b: "none — the fixes are not yet written")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert RANGE_ROW not in out, out


PENDING_RANGE = "none — the fixes are not yet written"


def read_by_a_later_round(repo, began, checked_by):
    """Two records; the FIRST carries `Fix range` at the value `new` writes
    before the fixes exist, beside a `Fixes checked by` of `checked_by`.

    The second record exists so that `round-2` is a checker the repository
    can confirm; it is the last record and carries its own seal.
    """
    item = gated_item(began, slug="a-ranged-item")
    write(repo, f"{item}/routing.md", declaration())
    first = commit(repo, "declare")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        "# a round\n\n"
        f"| Field | Value |\n|---|---|\n| Target SHA | {first} |\n"
        "| Broad gate | not yet |\n"
        f"| Fix range | {PENDING_RANGE} |\n"
        f"| Fixes checked by | {checked_by} |\n"
        "| Contract changes | none |\n"
        "| New units | none |\n"
        "| Ran by | specseal:warden on a model |\n"
        "| Needs a fix | no |\n"
        "| Loses a record or crashes | no |\n\n"
        "- [x] Pass\n\n"
        "## Verdicts\n\n"
        "| # | Finding | Location | Verdict | Grounds |\n"
        "|---|---|---|---|---|\n"
        "| 🟡 1 | something | `f.py:1` | answered | grounds |\n",
    )
    second = commit(repo, "round 1")
    write(
        repo,
        f"{item}/rounds/round-2.md",
        gated_record(second, gate=f"{second} against base", rng="none"),
    )
    commit(repo, "round 2")
    return run(repo, draft=False)


def test_a_fix_range_still_pending_after_a_round_read_the_fixes_fails(repo):
    """A6 of #436. `Fixes checked by` naming `round-2` says a later round
    opened this record's fixes, so they exist — and `Fix range` two rows up
    still saying they are not yet written is false about a fact the same
    file states. `fix_surface` refuses exactly that on its own two rows;
    this row took the same pending value from the same line of `build` and
    was never read back for whether anybody replaced it."""
    code, out = read_by_a_later_round(repo, RANGE_FROM, "round-2")
    assert code == 1, out
    assert RANGE_ROW in out and "not yet written" in out, out
    assert "round-1.md" in out, out
    assert "round-2" in out, "the refusal names the checker that contradicts the cell"


def test_a_fix_range_still_pending_prints_for_a_work_item_begun_before_the_row(
    repo,
):
    """One second before `RANGE_FROM`, the same pair prints and does not fail
    — the row's own grandfathering, and no cutoff of its own. The row has
    carried the pending value from birth since it shipped, so `ORDER_FROM`
    would excuse nothing this does not."""
    code, out = read_by_a_later_round(repo, RANGE_FROM - 1, "round-2")
    assert code == 0, out
    assert RANGE_ROW in out and "not yet written" in out, "the state is reported"
    assert str(RANGE_FROM) in out, "and the cutoff is named"


def test_a_fix_range_pending_beside_nobody_is_the_honest_mid_run_state(repo):
    """The direction that must keep passing: nothing has opened the fixes,
    `Fixes checked by` says so, and the pending value is the truth rather than
    an abandoned cell. `no fixes to check` beside the same value is the case
    two above, and stays untouched too."""
    code, out = read_by_a_later_round(
        repo, RANGE_FROM, "nobody — this round's fixes are not written"
    )
    assert code == 0, out
    assert "still says the fixes are not yet written" not in out, out


def test_an_empty_fix_range_row_is_named(repo):
    """A row that says nothing answers nothing, on any record."""
    ranged(repo, RANGE_FROM, lambda a, b: " ")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert RANGE_ROW in out, out
    assert "says nothing answers nothing" in out, out


def test_a_missing_fix_range_row_fails_a_work_item_begun_after_the_cutoff(repo):
    """The row is owed from the work item that added it onward, which is the
    shape all nine cutoffs above it carry."""
    item = gated_item(RANGE_FROM, slug="a-ranged-item")
    write(repo, f"{item}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        gated_record(sha, gate=f"{sha} against base"),
    )
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert f"no `| {RANGE_ROW} | … |` row" in out, out
    assert "HEAD` is not a commit" in out, out


def test_a_missing_fix_range_row_prints_for_a_work_item_begun_before_it(repo):
    """One second earlier, and the same record prints instead of failing. A
    merged record cannot state a range it never measured, and a check whose
    first production act is red on history nobody can repair is a check people
    learn to skip."""
    item = gated_item(RANGE_FROM - 1, slug="a-ranged-item")
    write(repo, f"{item}/routing.md", declaration())
    sha = commit(repo, "declare")
    write(
        repo,
        f"{item}/rounds/round-1.md",
        gated_record(sha, gate=f"{sha} against base"),
    )
    commit(repo, "round 1")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert f"no `| {RANGE_ROW} | … |` row" in out, "the state is still reported"
    assert str(RANGE_FROM) in out, "and the cutoff is named, so the reason is readable"


def test_the_records_in_this_repository_are_not_failed_by_the_new_row(repo):
    """Every record already in this tree, read by the new arm.

    The row did not exist when any of them was written, so what this pins is
    the grandfathering: each one PRINTS and none of them fails. A cutoff set
    one work item too early would turn every shipped record red at the next
    pull request, which is the failure mode `plan.md` named for this phase
    before it was built.

    The population is asserted beside the verdict. A walk that read nothing
    would also report no failures, and that is the shape of a check that
    cannot fail.
    """
    check = load_by_path(CHECK, "specseal_chain_check_for_ranges")
    reader = load_by_path(
        os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py"),
        "specseal_reader_for_ranges",
    )
    check.WORKTREE = True
    records = [
        os.path.relpath(os.path.join(d, name), ROOT).replace(os.sep, "/")
        for d, _dirs, names in os.walk(os.path.join(ROOT, "seal", "specs"))
        for name in names
        if re.fullmatch(r"round-\d+\.md", name)
    ]
    _the_walk_found_every_committed_record(records, "the fix-range sweep")
    failed, printed_without_a_row, carrying = [], 0, []
    for rel in sorted(records):
        errors, notices = check.fix_range(reader, ROOT, rel)
        failed.extend(errors)
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            carries = f"| {check.FIX_RANGE} |" in f.read()
        if carries:
            carrying.append(rel)
        else:
            printed_without_a_row += len(notices)
    assert not failed, f"records the new row would fail: {failed[:5]}"
    # The population, split the way the tree is actually split. Until this
    # work item's own round 1 there was no record carrying the row at all and
    # this read `printed == len(records)`; the first record to carry one made
    # that false, which is the case being right rather than the tree being
    # wrong. What has to hold is that a record WITHOUT the row is printed and
    # never failed, and that the two groups account for every record — a walk
    # that quietly read nothing would report no failures too.
    #
    # The notices are counted over that group ALONE, never as a subtraction
    # from the whole. A record that HAS the row prints whenever its ends stop
    # resolving, which `fix_range`'s own docstring calls "the ordinary state
    # of a merged record and not a fault in it" — and the squash that merges
    # this branch makes it the state of the one record carrying the row. A
    # subtraction asserts that such a record prints nothing, which is the
    # opposite of what this module documents (round 2's 🔴 1).
    # `assert carrying` stood here and the fold took its subject away. Every
    # one of the 34 records carrying the row belonged to a work item the
    # retirement removed, because the row is younger than every work item
    # kept — so the assertion is not weakened here, it is MOVED to
    # `test_a_record_carrying_the_row_is_read_and_one_without_it_prints`
    # below, where the two-way split is exercised over a record this case
    # builds. What stays here is the real-corpus half the fold cannot empty:
    # no shipped record is failed by the row, and every record without one
    # prints rather than going quiet.
    assert printed_without_a_row == len(records) - len(carrying), (
        f"{printed_without_a_row} notices over {len(records) - len(carrying)} "
        "records with no row: a record that predates the row has to print, "
        "not go quiet"
    )


# --- a declaration the pull request RETIRED (#497) ---------------------------


def retired_item(repo, item, marker=True):
    """A declared, reviewed work item that this branch then folds away.

    The shape `settle --retire` leaves: the declaration is on the base branch,
    the branch removes the whole directory, and `docs/` carries the marker
    saying a policy document absorbed the spec first.

    **It writes a `spec.md`**, because the marker arm is about a work item
    that stated a rule. Without one, the directory is the rule arm's (#517
    D3) — no `spec.md` and nothing open at the merge base is retired with no
    marker — and `marker=False` would stop being a deletion at all.
    """
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration())
    write(repo, f"{item}/spec.md", "# a spec\n\nA rule that still governs.\n")
    write(repo, f"{item}/rounds/round-1.md", "# round 1\n")
    commit(repo, "a work item, declared and reviewed")
    git(repo, "switch", "-q", "feature")
    git(repo, "merge", "-q", "base")
    shutil.rmtree(repo / item)
    if marker:
        write(
            repo,
            "docs/a-policy.md",
            f"# a policy\n\nA rule that still governs.\n\n"
            f"<!-- specs/{os.path.basename(item)} -->\nThe folded sentence.\n",
        )
    commit(repo, "fold and retire")


def test_a_declaration_this_branch_retired_is_not_one_it_made(repo):
    """#497's first fold put 88 retired declarations in one diff and this
    check failed all 88.

    A `routing.md` that `settle --retire` removed is in the diff as a
    deletion and absent at HEAD, which is what the refusal below reads — but
    the work item it declared was reviewed at its own pull request, long
    before this branch existed. That is the judgment `changed_routing`
    already makes for a rename, arriving for the other way a declaration
    leaves a diff.

    The marker is the only thing that can tell the two apart, because a fold
    and a plain deletion both leave the file absent here.
    """
    retired_item(repo, "seal/specs/1788000000-a-folded-item")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "retired:" in out, out
    assert "1788000000-a-folded-item" in out, out
    assert "its own pull request" in out, out
    assert "does not carry this file at HEAD" not in out, (
        "a retired declaration is still being refused as a missing one"
    )


def test_a_deleted_declaration_with_no_marker_is_still_refused(repo):
    """The half that keeps the refusal's teeth.

    A directory removed with nothing absorbing it is not a fold, and it is
    exactly what the original refusal was written for. If this passed, the
    arm above would be excusing every deletion rather than a retirement.
    """
    retired_item(repo, "seal/specs/1788000000-a-deleted-item", marker=False)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "does not carry this file at HEAD" in out, out
    assert "retired:" not in out, out


CLOSED_MEMO = (
    "# a moment — overview\n\n## Not verified\n\n"
    "| Item | Who must answer |\n|---|---|\n"
    "| ✅ a claim | run on 2026-01-01 |\n"
)
OPEN_MEMO = (
    "# a moment — overview\n\n## Not verified\n\n"
    "| Item | Who must answer |\n|---|---|\n"
    "| a claim nobody ran | the repository owner |\n"
)


def moment_item(repo, item, memo=CLOSED_MEMO, spec=False):
    """A declared work item below the SDD ladder that this branch removes
    with no marker — the rule arm's shape (#517 D3)."""
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration())
    write(repo, f"{item}/overview.md", memo)
    if spec:
        write(repo, f"{item}/spec.md", "# a spec\n\nA rule.\n")
    commit(repo, "a moment, declared")
    git(repo, "switch", "-q", "feature")
    git(repo, "merge", "-q", "base")
    shutil.rmtree(repo / item)
    commit(repo, "retire by the rule")


def test_a_declaration_the_rule_arm_retired_is_not_one_it_made(repo):
    """A7. `settle --retire` removes a released directory that held no
    `spec.md` and nothing open, and writes no marker — so the marker arm above
    refused it as a missing declaration. Asked of the merge base, through the
    one predicate the other readers ask."""
    moment_item(repo, "seal/specs/1788000000-a-release-entry")
    code, out = run(repo, draft=False)
    assert code == 0, out
    assert "retired:" in out and "by the rule" in out, out
    assert "1788000000-a-release-entry" in out, out
    assert "does not carry this file at HEAD" not in out, out


def test_a_spec_at_the_merge_base_is_still_a_missing_declaration(repo):
    moment_item(repo, "seal/specs/1788000000-a-deleted-spec", spec=True)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "does not carry this file at HEAD" in out, out


def test_a_spec_deleted_by_an_earlier_merge_is_not_a_rule_retirement(repo):
    """Round 1's finding 3. The merge base held no `spec.md` because an
    earlier pull request had deleted it, and that one passed every reader
    too. D3 is about a work item that WROTE no spec, which history answers
    and one tree does not."""
    item = "seal/specs/1788000000-a-spec-dropped-earlier"
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration())
    write(repo, f"{item}/overview.md", CLOSED_MEMO)
    write(repo, f"{item}/spec.md", "# a spec\n\nA rule nobody folded.\n")
    commit(repo, "a work item that stated a rule")
    (repo / item / "spec.md").unlink()
    commit(repo, "an earlier pull request drops the spec")
    git(repo, "switch", "-q", "feature")
    git(repo, "merge", "-q", "base")
    shutil.rmtree(repo / item)
    commit(repo, "the directory, removed with no marker")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "does not carry this file at HEAD" in out, out
    assert "by the rule" not in out, out


def test_an_open_row_at_the_merge_base_is_still_a_missing_declaration(repo):
    moment_item(repo, "seal/specs/1788000000-an-open-moment", memo=OPEN_MEMO)
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "does not carry this file at HEAD" in out, out


def test_a_declaration_removed_from_a_directory_that_stays_is_refused(repo):
    """A retirement removes the directory. A spec-less directory that stays
    with only its `routing.md` gone is a declaration deleted, whatever the
    merge base held."""
    item = "seal/specs/1788000000-a-kept-moment"
    git(repo, "switch", "-q", "base")
    write(repo, f"{item}/routing.md", declaration())
    write(repo, f"{item}/overview.md", CLOSED_MEMO)
    commit(repo, "a moment, declared")
    git(repo, "switch", "-q", "feature")
    git(repo, "merge", "-q", "base")
    (repo / item / "routing.md").unlink()
    commit(repo, "remove the declaration only")
    code, out = run(repo, draft=False)
    assert code == 1, out
    assert "does not carry this file at HEAD" in out, out


def test_a_record_carrying_the_row_is_read_and_one_without_it_prints(repo):
    """The two-way split, over records this case builds rather than over
    whatever the repository happens to hold.

    `assert carrying` used to sit in the sweep above and assert that the real
    corpus had a specimen of each kind, so that the subtraction beside it was
    comparing two non-empty groups. The `Fix range` row is younger than every
    work item the fold keeps, so all 34 of its carriers left in one commit and
    the assertion had no subject at all. Re-pointed here, where both kinds
    exist because this case writes them, the split is pinned for good instead
    of for as long as a carrier happens to survive.

    The item with no row is begun a second BEFORE the cutoff. A record owing
    the row and not carrying it is failed rather than printed, which is a
    different case (`test_a_missing_fix_range_row_fails_a_work_item_begun_
    after_the_cutoff`); what this one needs is the grandfathered state, where
    a record with no row prints and is not refused.
    """
    check = load_by_path(CHECK, "specseal_chain_check_for_the_split")
    reader = load_by_path(
        os.path.join(ROOT, "skills", "verify", "scripts", "unverified_check.py"),
        "specseal_reader_for_the_split",
    )
    check.WORKTREE = True
    first, _second = ranged(repo, RANGE_FROM, lambda a, b: f"`{a}..{b}`, 1 commit")
    older = gated_item(RANGE_FROM - 1, slug="an-item-with-no-row")
    write(repo, f"{older}/routing.md", declaration())
    write(
        repo,
        f"{older}/rounds/round-1.md",
        gated_record(first, gate=f"{first} against base"),
    )
    commit(repo, "a record from before the row existed")

    records = sorted(
        os.path.relpath(os.path.join(d, name), str(repo)).replace(os.sep, "/")
        for d, _dirs, names in os.walk(os.path.join(str(repo), "seal", "specs"))
        for name in names
        if re.fullmatch(r"round-\d+\.md", name)
    )
    failed, printed_without_a_row, carrying = [], 0, []
    for rel in records:
        errors, notices = check.fix_range(reader, str(repo), rel)
        failed.extend(errors)
        with open(os.path.join(str(repo), rel), encoding="utf-8") as f:
            carries = f"| {check.FIX_RANGE} |" in f.read()
        if carries:
            carrying.append(rel)
        else:
            printed_without_a_row += len(notices)

    assert len(records) == 2, records
    assert not failed, failed
    assert len(carrying) == 1, (
        "the walk found no record carrying the row, so the group the "
        f"subtraction below excludes is empty: {records}"
    )
    assert printed_without_a_row == len(records) - len(carrying), (
        f"{printed_without_a_row} notices over one record with no row: a "
        "record that predates the row has to print, not go quiet"
    )
