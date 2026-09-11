"""Issue #359, the gate half: a release pull request is refused while its
milestone claims an open issue the release branch does not carry.

`docs/flow.md` carried this as a checklist bullet — *is everything in* — and
#351 deleted the file. Nothing replaced it, and nothing had ever checked it:
`docs/issues-and-milestones.md` says a milestone answers *what is in 1.2.3*,
and until this gate a wrong one cost a person a wrong answer and cost no
automation anything.

Three sets, and every case below is about which of the four directions between
them stops a release and which only gets reported:

    M   open issues whose milestone is `release: X.Y.Z`
    D   what the release branch carries, read out of its own commit subjects
    L   what carries the label `merged: X.Y.Z`

`judge()` is pure, so the four directions are cases rather than runs. What
needs the fake tracker is the wiring above it — which command each set is read
with, and the range D is read over.
"""

import importlib.util
import json
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, ".github", "scripts", "release_completeness_check.py")
HYGIENE = os.path.join(ROOT, ".github", "workflows", "hygiene.yml")

VERSION = "1.2.3"
BRANCH = "release/v1.2.3"
MILESTONE = "release: 1.2.3"
LABEL = "merged: 1.2.3"
REPO = "example/repo"


def gate():
    spec = importlib.util.spec_from_file_location(
        "specseal_release_completeness_for_tests", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def verdict(milestone_open, carried, labels):
    lines, failed = gate().judge(
        set(milestone_open), set(carried), set(labels), VERSION
    )
    return "\n".join(lines), failed


# --- S4: the milestone claims what the release does not carry ---------------


def test_an_open_issue_the_release_does_not_carry_refuses_it():
    """S4. The whole reason the gate exists, and the direction that fails.

    The release this gate ships in met exactly this on the day it was
    written: its milestone held nine open issues and the branch carried two.
    """
    out, failed = verdict(milestone_open={88, 92, 99}, carried={88}, labels={88})
    assert failed, "a milestone claiming two absent issues let the release through"
    assert "M \\ D" in out, "the refusal does not name the direction it is about"
    assert "#92" in out and "#99" in out, f"the refusal names no issue: {out}"
    assert "::error::" in out, "the refusal is not annotated as an error"


def test_a_pull_request_body_with_no_closing_keyword_refuses_the_release():
    """S8. `docs/issues-and-milestones.md` says a missing `Closes #N` "costs
    an issue that stays open forever"; this is the first thing that reports
    it, and it reports it as the milestone claiming an item that is not in.

    The issue is in M because a person scheduled it, and out of D because the
    body never said so — which is the same shape as work that has not been
    built, and correctly so: nothing in the tree can tell them apart.
    """
    out, failed = verdict(milestone_open={88}, carried=set(), labels=set())
    assert failed
    assert "#88" in out and "M \\ D" in out


def test_the_refusal_says_what_to_do_about_it():
    """A refusal is read by whoever is stopped by it, and the half that says
    what to do is the half that has to survive a reword."""
    out, _ = verdict(milestone_open={88, 92}, carried={88}, labels={88})
    assert "another milestone" in out, (
        "the refusal does not offer moving the issue, so a reader meeting it "
        "mid-release has only 'build it now' on the table"
    )


# --- S5: a true milestone passes --------------------------------------------


def test_a_milestone_the_release_satisfies_passes_and_prints_both_sets():
    """S5. Printing them is not decoration: the reader who has just been told
    nothing is wrong is the reader who has to be able to check that."""
    out, failed = verdict(milestone_open={88, 92}, carried={88, 92}, labels={88, 92})
    assert not failed
    assert "::error::" not in out
    assert re.search(r"^M \(open in .*\): #88, #92$", out, re.M), out
    assert re.search(r"^D \(carried by this release branch\): #88, #92$", out, re.M)
    assert re.search(r"^L \(carrying .*\): #88, #92$", out, re.M)


def test_nothing_anywhere_is_not_a_failure():
    """A release branch with no claimed issue at all — the first push of a
    freshly cut branch. Empty sets agree with each other."""
    out, failed = verdict(milestone_open=set(), carried=set(), labels=set())
    assert not failed
    assert "none" in out


# --- S6: a label disagreement names its direction ---------------------------


def test_a_label_naming_a_release_the_issue_is_not_in_fails():
    """S6, the failing direction, and `questions.md` Q1's answer (c).

    `L \\ D` is always a hand-edit or a squash subject that lost its `(#N)`,
    and one command repairs it — which is why this half fails where the other
    reports.
    """
    out, failed = verdict(milestone_open={88}, carried={88}, labels={88, 77})
    assert failed, "a label on an issue this release does not carry passed"
    assert "L \\ D" in out, "the finding does not name which direction it is"
    assert "#77" in out
    assert "--remove-label" in out, (
        "the finding does not name the one command that repairs it"
    )
    assert "#88" not in out.split("L \\ D")[1].split("\n")[0], (
        "the correctly-labelled issue is named in the refusal"
    )


def test_the_signal_having_missed_one_reports_and_passes():
    """S6, the passing direction. A release held for the signal's outage is a
    release paying for something that does not change what ships — and the
    remedy would be a person adding a label by hand, which is the act this
    work item exists to remove."""
    out, failed = verdict(milestone_open={88, 92}, carried={88, 92}, labels={88})
    assert not failed, "the release was held because a label write had not landed"
    assert "D \\ L" in out and "#92" in out
    assert "::error::" not in out


def test_an_issue_closed_by_hand_mid_release_reports_and_passes():
    """`D \\ M`. It is in D because the release carries it and in no OPEN
    milestone because somebody closed it, and a gate that went red for that
    would go red for ordinary tracker hygiene."""
    out, failed = verdict(milestone_open=set(), carried={88}, labels={88})
    assert not failed
    assert "D \\ M" in out and "#88" in out


def test_both_failing_directions_are_reported_together():
    """A run that stopped at the first refusal would send a release
    preparation round the loop twice."""
    out, failed = verdict(milestone_open={88, 99}, carried={88}, labels={88, 77})
    assert failed
    assert "M \\ D" in out and "#99" in out
    assert "L \\ D" in out and "#77" in out


# --- S7: what the gate cannot judge ----------------------------------------


@pytest.mark.parametrize(
    "head",
    ["hotfix/v1.2.4", "fix/88-a-thing", "main", "release/next", "release/v1.2", ""],
)
def test_a_head_that_is_not_a_release_branch_is_skipped_with_a_reason(
    monkeypatch, capsys, head
):
    """S7. `docs/branch-and-release.md` lists a hotfix branch as the other
    thing that reaches `main`, and a hotfix carries no release milestone.
    Guessing a version out of the name is the one thing that must not
    happen."""
    m = gate()
    monkeypatch.setattr(m.closer, "run", lambda *a: pytest.fail(f"the gate ran {a}"))
    monkeypatch.setenv("HEAD_BRANCH", head)
    monkeypatch.setenv("REPO", REPO)
    assert m.main() == 0
    assert "nothing to judge" in capsys.readouterr().out


def test_a_milestone_that_does_not_exist_says_it_verified_nothing(monkeypatch, capsys):
    """Measured on the real tracker: `gh issue list --milestone` answers a
    title nothing has with `[]` and exit 0. So without a separate existence
    read, a mistyped or absent milestone makes this whole check pass while
    measuring an empty set — a check that cannot fail.

    It still passes, because a release nobody scheduled is a person's call
    rather than this gate's, and the `D \\ M` direction was rejected for the
    same reason. What it must not be is silent.
    """
    m = gate()
    monkeypatch.setattr(m, "milestone_titles", lambda repo: {"release: 9.9.9"})
    monkeypatch.setattr(
        m, "open_in_milestone", lambda *a: pytest.fail("the empty set was measured")
    )
    monkeypatch.setenv("HEAD_BRANCH", BRANCH)
    monkeypatch.setenv("REPO", REPO)
    assert m.main() == 0
    out = capsys.readouterr().out
    assert "verified NOTHING" in out, out
    assert MILESTONE in out


# --- the wiring above `judge` ----------------------------------------------


class Tracker:
    """Every `closer.run` the gate makes, and a canned answer for each."""

    def __init__(self, milestones=(MILESTONE,), m=(), label=(), subjects=()):
        self.milestones = list(milestones)
        self.m = list(m)
        self.label = list(label)
        self.subjects = list(subjects)
        self.calls = []

    def run(self, *args):
        self.calls.append(args)
        if args[:2] == ("git", "merge-base"):
            return "f" * 40 + "\n"
        if args[:2] == ("git", "log"):
            return "\n".join(self.subjects) + "\n"
        if args[:2] == ("gh", "api"):
            return json.dumps([{"title": t} for t in self.milestones])
        if args[:3] == ("gh", "issue", "list"):
            which = self.label if "--label" in args else self.m
            return json.dumps([{"number": n} for n in which])
        raise AssertionError(f"unexpected command: {args}")

    def call_with(self, *needles):
        for args in self.calls:
            if all(n in args for n in needles):
                return args
        raise AssertionError(f"no call carrying {needles}: {self.calls}")


def wire(monkeypatch, m, tracker, pulls):
    monkeypatch.setattr(m.closer, "run", tracker.run)
    monkeypatch.setattr(
        m.closer,
        "_issue_api",
        lambda repo, n: (
            ({"pull_request": {}, "body": pulls[n]}, True)
            if n in pulls
            else (None, False)
        ),
    )
    monkeypatch.setenv("HEAD_BRANCH", BRANCH)
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("BASE", raising=False)


def test_the_range_is_measured_from_where_the_branch_left_main(monkeypatch):
    """`questions.md` Q8. `origin/main..HEAD` is the obvious spelling and it
    is wrong the moment a hotfix moves `main` during a release's life; what
    the release carries is what it accumulated since it was cut."""
    m = gate()
    tracker = Tracker(m=[88], label=[88], subjects=["feat: a thing (#100)"])
    wire(monkeypatch, m, tracker, {100: "Closes #88"})
    assert m.main() == 0
    assert tracker.call_with("merge-base") == (
        "git",
        "merge-base",
        "origin/main",
        "HEAD",
    )
    log = tracker.call_with("git", "log")
    assert log[-1] == "f" * 40 + "..HEAD", (
        f"D was read over {log[-1]!r}, not over the fork point"
    )


def test_the_base_the_range_starts_from_is_configurable(monkeypatch):
    """CI passes `origin/<base_ref>`, and a session checking a release by
    hand has a different remote name for it."""
    m = gate()
    tracker = Tracker(subjects=[])
    wire(monkeypatch, m, tracker, {})
    monkeypatch.setenv("BASE", "upstream/main")
    assert m.main() == 0
    assert tracker.call_with("merge-base")[2] == "upstream/main"


def test_M_is_read_with_gh_issue_list_and_not_the_rest_endpoint(monkeypatch):
    """Measured: REST `/issues` counts a pull request as an issue and
    `gh issue list` does not. A pull request carrying the milestone could
    never carry `merged: X.Y.Z`, so it would sit in `M \\ D` and block the
    release forever with nothing anybody could do about it."""
    m = gate()
    tracker = Tracker(m=[88], label=[88], subjects=["feat: a thing (#100)"])
    wire(monkeypatch, m, tracker, {100: "Closes #88"})
    assert m.main() == 0
    call = tracker.call_with("--milestone")
    assert call[:3] == ("gh", "issue", "list"), call
    assert "--state" in call and call[call.index("--state") + 1] == "open"


def test_L_is_read_in_every_state(monkeypatch):
    """An issue closed by hand mid-release still carries the label the signal
    put on it. Reading only the open ones would report it as `D \\ L` — the
    signal blamed for a person's edit."""
    m = gate()
    tracker = Tracker(m=[], label=[88], subjects=["feat: a thing (#100)"])
    wire(monkeypatch, m, tracker, {100: "Closes #88"})
    assert m.main() == 0
    call = tracker.call_with("--label")
    assert call[call.index("--label") + 1] == LABEL
    assert call[call.index("--state") + 1] == "all"


def test_D_comes_from_the_same_readers_the_signal_writes_it_with(monkeypatch):
    """The gate recomputes D rather than trusting L, and it has to recompute
    it the same way — a second reader of a pull request body is how the label
    and the refusal come to disagree about a fenced example."""
    m = gate()
    tracker = Tracker(
        m=[88],
        label=[88],
        subjects=["feat: a thing (#100)", "docs: quoted (#101)"],
    )
    wire(monkeypatch, m, tracker, {100: "Closes #88", 101: "```\nCloses #92\n```"})
    assert m.main() == 0
    source = read(SCRIPT)
    assert "signal.issues_in(" in source, "the gate derives D some other way"
    for own in ("CLOSING = re.compile", "MERGED_PR = re.compile"):
        assert own not in source, f"the gate wrote its own {own.split()[0]}"


def test_the_gate_writes_nothing(monkeypatch):
    """Its whole job is to judge. A gate that can write is a gate whose red
    can be made green by the thing that went red."""
    folded = " ".join(read(SCRIPT).split())
    for forbidden in ("edit", "close", "create", "delete", "comment", "reopen"):
        assert f'"gh", "issue", "{forbidden}"' not in folded, f"issue {forbidden}"
        assert f'"gh", "label", "{forbidden}"' not in folded, f"label {forbidden}"


# --- the step in hygiene.yml ------------------------------------------------


def hygiene_step():
    """The gate's step, from `- name:` to the next one at the same indent."""
    text = read(HYGIENE)
    start = text.index("- name: the milestone this release claims")
    rest = text[start + 1 :]
    end = rest.find("\n      - name:")
    return rest[: end if end != -1 else len(rest)]


def test_the_gate_runs_only_for_a_release_pull_request():
    """It is the fifth release-only step in this file. A feature pull request
    carries no milestone of its own and the release branch it targets is not
    finished, so running it there is noise at best."""
    step = hygiene_step()
    assert 'github.base_ref }}" != "main" ]' in step, (
        "the step is missing the base guard the other release-only steps use"
    )
    assert "release_completeness_check.py" in step


def test_the_head_shape_reaches_the_script_rather_than_the_guard():
    """A hotfix branch merging into `main` is the other shape that gets here,
    and what it does about that is a case (S7) rather than a shell condition
    nothing can test."""
    step = hygiene_step()
    assert "HEAD_BRANCH: ${{ github.head_ref }}" in step, (
        "the head branch does not reach the script, so the skip it is "
        "supposed to make is unreachable"
    )


def test_the_job_asks_for_a_token_that_can_read_issues():
    """`hygiene.yml` declared no `permissions:` block and used no `gh` before
    this step, so it ran on whatever an enterprise, organisation or repository
    default happened to be. The gate writes nothing, so the block is
    read-only in both scopes — narrower than any default, and stated rather
    than inherited."""
    text = "\n".join(
        line for line in read(HYGIENE).splitlines() if not line.lstrip().startswith("#")
    )
    block = re.search(r"^permissions:\n((?:  [\w-]+:.*\n)+)", text, re.M)
    assert block, "hygiene.yml states no permissions block, so it inherits a default"
    granted = dict(re.findall(r"^  ([\w-]+):\s*(\S+)\s*$", block.group(1), re.M))
    assert granted == {"contents": "read", "issues": "read"}, (
        f"the token's scopes changed: {granted}. Every step in this job reads "
        "and none of them writes"
    )
    assert "GH_TOKEN: ${{ github.token }}" in hygiene_step(), (
        "the step does not pass a token, so `gh` falls back to whatever the "
        "runner happens to have"
    )
