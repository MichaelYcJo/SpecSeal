"""#450: a label this repository's documents specify exists on the tracker,
and stops existing on the issue it was spent on.

`size: now` was specified in 0.11.1 and never created. The work item that
wrote the section assigned creating it to a **person**, and a person has no
queue anything here can read — no open issue, no checklist row, no failing
check — so three releases were cut before the cost came due. The repair moves
the act to the workflow that already runs when `main` moves.

  A9   the reconcile step creates a missing label with the description the
       specifying document's own sentence gives, and says so
  A10  reconciling is idempotent: every label present, nothing written, exit 0
  A11  an issue carrying `size: now` that a shipped pull request claimed loses
       the label in the same act that closes it — and the issue closes even
       when that write fails
  A12  the document says when the judgment is made, what removes a spent
       label, and that no backlog sweep is owed

**Nothing here reaches GitHub.** The fake tracker is
`tests/test_a_merged_ticket_says_so_on_the_tracker.py`'s, for its stated
reason: it records every call as an argument tuple, in order, so a case can
assert about a write that did NOT happen. Three of these are exactly that.

**A11's second half is the one a green run hides.** An issue that closed and
kept a stale label is a wrong answer on a tracker; an issue left open because
a label write failed is a release that did not finish. So the failing-write
case asserts the close happened anyway, and the ordering case asserts the
close was made first rather than trusting that it was.

**Shown red before it was committed (§15).** Each case was run against the
script or document with the one behaviour it pins removed; the mutations and
what each case said were recorded in
phase 4 of work item `1790076050-the-release-tail-is-three-acts-no-document-names`,
whose rule `docs/branch-and-release.md` §*Cutting a release* now carries.
"""

import importlib.util
import json
import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, ".github", "scripts")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "close-issues-on-release.yml")
OWNER = "docs/issues-and-milestones.md"

REPO = "example/repo"
LABEL = "size: now"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(
        f"specseal_{name}_for_label_tests", os.path.join(SCRIPTS, filename)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def labels_module():
    return load("tracker_labels", "tracker_labels.py")


def closer_module():
    return load("close_issues_on_release", "close_issues_on_release.py")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def flat(rel):
    return " ".join(read(os.path.join(ROOT, rel)).split())


class Tracker:
    """A repository's issues, pull requests and labels, and every call made."""

    def __init__(self, issues=None, pulls=None, labels=(), refuse=()):
        self.issues = {n: list(v) for n, v in (issues or {}).items()}
        self.states = dict.fromkeys(self.issues, "open")
        self.pulls = dict(pulls or {})
        self.labels = set(labels)
        self.refuse = set(refuse)
        self.calls = []

    def api(self, repo, number):
        if number in self.pulls:
            return {"pull_request": {}, "body": self.pulls[number]}, True
        if number in self.issues:
            return {
                "labels": [{"name": name} for name in self.issues[number]],
                "state": self.states[number],
            }, True
        return None, False

    def run(self, *args):
        self.calls.append(args)
        if args[:3] == ("gh", "label", "list"):
            return json.dumps([{"name": name} for name in sorted(self.labels)])
        if args[:3] == ("gh", "label", "create"):
            self.labels.add(args[3])
            return ""
        if args[:3] == ("gh", "issue", "close"):
            self.states[int(args[3])] = "closed"
            return ""
        raise AssertionError(f"unexpected command: {args}")

    def edit(self, command, **kwargs):
        """Stands in for `subprocess.run` on the label removal alone."""
        self.calls.append(tuple(command))
        number = int(command[3])

        class Result:
            pass

        result = Result()
        if number in self.refuse:
            result.returncode, result.stderr = 1, "HTTP 502"
            return result
        if LABEL in self.issues.get(number, []):
            self.issues[number].remove(LABEL)
        result.returncode, result.stderr = 0, ""
        return result

    def writes(self):
        return [a for a in self.calls if a[:3] != ("gh", "label", "list")]


# --- A9 and A10: the label exists without anybody remembering ---------------


def test_a_missing_label_is_created_with_the_documents_own_sentence(
    monkeypatch, capsys
):
    """A9. The description is what a person reads on the tracker, so it is the
    specifying document's sentence rather than a summary of it — and it says
    when the label stops being the current answer, which is the half nothing
    else on the tracker can tell them."""
    mod = labels_module()
    tracker = Tracker(labels={"documentation", "release"})
    monkeypatch.setattr(mod.closer, "run", tracker.run)
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)

    assert mod.main(["--apply"]) == 0
    created = [a for a in tracker.calls if a[:3] == ("gh", "label", "create")]
    assert len(created) == 1, tracker.calls
    assert created[0][3] == LABEL
    description = created[0][created[0].index("--description") + 1]
    assert "before the next work item starts" in description, (
        "the description is not the document's own sentence about what the label means"
    )
    assert "removed when its release closes the issue" in description, (
        "the description does not say when the label stops being the current "
        "answer, which is the one thing a reader cannot get from the name"
    )
    assert LABEL in capsys.readouterr().out


def test_reconciling_an_already_complete_tracker_writes_nothing(monkeypatch, capsys):
    """A10. A re-run of a push, a re-pushed release, a workflow re-run — all
    land here, and the no-op is by construction: the write happens only after
    a read says the name is absent."""
    mod = labels_module()
    tracker = Tracker(labels={label["name"] for label in mod.declared()})
    monkeypatch.setattr(mod.closer, "run", tracker.run)
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)

    assert mod.main(["--apply"]) == 0
    assert tracker.writes() == [], "it wrote to a tracker that needed nothing"
    assert "nothing to create" in capsys.readouterr().out


def test_check_reports_and_writes_nothing(monkeypatch, capsys):
    """`--check` is the arm a person types. It must not be the arm that acts,
    because then reading the state and changing it are one keystroke apart."""
    mod = labels_module()
    tracker = Tracker(labels=set())
    monkeypatch.setattr(mod.closer, "run", tracker.run)
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)

    assert mod.main(["--check"]) == 0
    assert tracker.writes() == []
    out = capsys.readouterr().out
    assert LABEL in out and "is missing" in out
    assert "--apply" in out, "the report does not name the arm that fixes it"


def test_every_declared_description_fits_the_trackers_cap():
    """#515. GitHub refuses a label description past its cap with a 422, and
    the refusal arrives in the workflow that runs after a release reaches
    `main` — where it skips the step behind it and nobody is looking. Held
    here, an over-long description is refused before the merge instead.

    The cap is read from the module that names it rather than written here,
    so the number has one source and a pointer to where it comes from."""
    mod = labels_module()
    limit = mod.signal.LABEL_DESCRIPTION_LIMIT
    too_long = [
        (label["name"], len(label["description"]))
        for label in mod.declared()
        if len(label["description"]) > limit
    ]
    assert not too_long, (
        f"the tracker refuses a label description past {limit} characters, "
        f"and these are longer: {too_long}"
    )


def test_every_declared_label_says_which_document_specifies_it():
    """A row here is a copy of a decision made somewhere else. A reader who
    cannot get back to the original has to take the copy's word for what the
    label means — which is how a label and its section drift apart."""
    mod = labels_module()
    assert mod.declared(), "nothing is declared, so the step reconciles nothing"
    for label in mod.declared():
        assert label["specified_by"].startswith(OWNER.split("/")[-1]) or label[
            "specified_by"
        ].startswith("docs/"), label
        document = label["specified_by"].split(" §")[0]
        assert os.path.exists(os.path.join(ROOT, document)), (
            f"{label['name']!r} cites {document}, which is not in the tree"
        )


def test_the_workflow_runs_the_apply_arm_and_needs_no_new_permission():
    """The whole argument for this shape: the job already fires when `main`
    moves and already holds `issues: write`, so the act costs no new trigger
    and no new scope. A step that needed either would be a different
    decision."""
    text = "\n".join(
        line
        for line in read(WORKFLOW).splitlines()
        if not line.lstrip().startswith("#")
    )
    assert "tracker_labels.py --apply" in text
    assert "issues: write" in text
    assert text.count("permissions:") == 1, (
        "the job grew a second permissions block, so the claim that this "
        "needed no new scope has stopped being checkable here"
    )


# --- A11: a spent label comes off with the issue ---------------------------


def wire_closer(monkeypatch, tracker, subjects):
    mod = closer_module()
    monkeypatch.setattr(mod, "arrived", lambda before, after: subjects)
    monkeypatch.setattr(mod, "_issue_api", tracker.api)
    monkeypatch.setattr(mod, "run", tracker.run)
    monkeypatch.setattr(mod.subprocess, "run", tracker.edit)
    monkeypatch.setenv("AFTER", "aaa")
    monkeypatch.setenv("BEFORE", "bbb")
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)
    return mod


def test_a_spent_label_comes_off_the_issue_the_release_closed(monkeypatch):
    """A11. The loop already knows exactly which issues shipped, which is the
    fact a person would otherwise reconstruct by hand."""
    tracker = Tracker(issues={7: [LABEL, "release"]}, pulls={100: "Closes #7"})
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    mod.main()
    assert tracker.states[7] == "closed"
    assert LABEL not in tracker.issues[7], "the spent label survived the close"
    assert "release" in tracker.issues[7], "it removed a label it was not asked to"


def test_the_close_comes_first_so_a_failed_label_write_cannot_cost_it(monkeypatch):
    """A11's second half, asserted on the ORDER rather than on the outcome.

    Both acts succeeding tells you nothing about which would survive the
    other failing. The close is what this script exists for; the label is
    bookkeeping about it.
    """
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"})
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    mod.main()
    closes = [
        i for i, a in enumerate(tracker.calls) if a[:3] == ("gh", "issue", "close")
    ]
    edits = [i for i, a in enumerate(tracker.calls) if "--remove-label" in a]
    assert closes and edits, tracker.calls
    assert closes[0] < edits[0], (
        "the label is removed before the issue is closed, so a failing label "
        "write takes the close with it"
    )


def test_the_issue_closes_even_when_the_label_write_fails(monkeypatch, capsys):
    """A11's stated direction: the issue closes either way."""
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"}, refuse={7})
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    mod.main()
    assert tracker.states[7] == "closed"
    out = capsys.readouterr().out
    assert "could not remove" in out and "closed either way" in out, (
        "a failed label write is silent, so a stale label looks like one "
        "nobody was supposed to remove"
    )


def test_an_issue_without_the_label_gets_no_label_call(monkeypatch):
    """Most issues do not carry it, and a write per issue to remove a label
    that is not there is a call per issue for nothing."""
    tracker = Tracker(issues={7: ["release"]}, pulls={100: "Closes #7"})
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    mod.main()
    assert not [a for a in tracker.calls if "--remove-label" in a], tracker.calls


def test_a_dry_run_writes_neither_the_close_nor_the_removal(monkeypatch, capsys):
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"})
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    monkeypatch.setenv("DRY_RUN", "1")
    mod.main()
    assert tracker.states[7] == "open"
    assert LABEL in tracker.issues[7]
    out = capsys.readouterr().out
    assert "would close #7" in out and f"would remove {LABEL!r} from #7" in out


# --- the already-closed issue, which no case reached (round 1, finding 1) ---
#
# Every A11 case above puts the issue in the `open` state, so all of them walk
# the branch that closes it. The loop's OTHER branch — an issue a previous run
# closed, or one closed by hand, still carrying a spent label — was reachable
# in production and by no case, and both of its defects lived there.


def test_an_already_closed_issue_reports_no_removal_that_failed(monkeypatch, capsys):
    """The job log is the only record of what a release did to the tracker.

    Unguarded, a refused write printed `could not remove …` and then
    `removed …` for the same issue in one log, with the tracker in the state
    the first line describes and the second denies — and the second is the
    line a reader takes away.
    """
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"}, refuse={7})
    tracker.states[7] = "closed"
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    mod.main()
    out = capsys.readouterr().out
    assert "could not remove" in out, "the failed write is not reported at all"
    assert f"removed {LABEL!r} from #7" not in out, (
        "the log says the label came off an issue it is still on"
    )
    assert LABEL in tracker.issues[7]


def test_an_already_closed_issue_reports_a_removal_that_worked(monkeypatch, capsys):
    """The other direction of the same branch, so the case above cannot be
    satisfied by never reporting anything."""
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"})
    tracker.states[7] = "closed"
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    mod.main()
    assert f"removed {LABEL!r} from #7" in capsys.readouterr().out
    assert LABEL not in tracker.issues[7], "the spent label survived"


def test_a_dry_run_over_an_already_closed_issue_names_the_label_too(
    monkeypatch, capsys
):
    """A preview silent about half the act is the failure `DRY_RUN` exists to
    prevent — by this script's own stated reason for having the arm. The
    open-issue path said `would remove`; this one said nothing, so a person
    reading a dry run concluded the label was out of scope."""
    tracker = Tracker(issues={7: [LABEL]}, pulls={100: "Closes #7"})
    tracker.states[7] = "closed"
    mod = wire_closer(monkeypatch, tracker, ["feat: a thing (#100)"])
    monkeypatch.setenv("DRY_RUN", "1")
    mod.main()
    out = capsys.readouterr().out
    assert f"would remove {LABEL!r} from #7" in out
    assert LABEL in tracker.issues[7], "a dry run wrote to the tracker"
    assert not [a for a in tracker.calls if "--remove-label" in a], tracker.calls


def test_every_report_of_the_removal_goes_through_one_place():
    """§12: the defect was one copy of three being unguarded, so what is owed
    is that a fourth copy cannot be written. Both branches of the loop call
    `spend_label`, and the two lines a reader sees are inside it."""
    source = read(os.path.join(SCRIPTS, "close_issues_on_release.py"))
    body = source.split('"""', 2)[2]
    assert body.count("would remove") == 1, (
        "the dry-run line is written in more than one place again"
    )
    assert body.count("removed {SPENT_ON_CLOSE!r}") == 1, (
        "the success line is written in more than one place again"
    )
    # Call sites, not occurrences: `def drop_label(repo, …)` is the third
    # match of a bare substring count and is not a caller. Measured — the
    # first spelling of this assertion counted the definition and went red
    # against the repaired file.
    calls = [
        line
        for line in body.splitlines()
        if "drop_label(" in line and not line.lstrip().startswith("def ")
    ]
    assert len(calls) == 1, (
        "a call site reaches `drop_label` without going through "
        f"`spend_label`, which is where the report is guarded on the "
        f"write: {calls}"
    )


def test_the_label_reader_has_one_source():
    """Two scripts read an issue's labels and there is one reader. A second
    copy is what `label_merged_on_release_branch.py`'s own docstring says it
    exists not to have, and it had one until this work item gave the second
    caller a reason to share."""
    signal = load("label_merged", "label_merged_on_release_branch.py")
    assert hasattr(signal.closer, "issue_labels"), (
        "the reader is no longer on the module that owns the 404-tolerant "
        "read it is built on"
    )
    # The CALL, not the word. The sibling's docstring says in prose that it
    # used to unpack `closer._issue_api` here and now delegates, and a check
    # on the bare name counts that sentence as the defect — which would make
    # explaining the history the thing that fails.
    source = read(os.path.join(SCRIPTS, "label_merged_on_release_branch.py"))
    assert "_issue_api(" not in source, (
        "the sibling unpacks the private read again instead of delegating, "
        "which is the copied reader coming back"
    )


# --- A12: the document says the three things it never said ------------------


@pytest.mark.parametrize(
    ("clause", "what_it_answers"),
    [
        pytest.param(
            "The judgment is made at filing, and again when an issue moves milestone.",
            "when somebody decides it",
            id="when the judgment is made",
        ),
        pytest.param(
            "removes `size: now` from each issue it closes when the release "
            "reaches `main`",
            "what removes a spent one",
            id="what removes a spent label",
        ),
        pytest.param(
            "No sweep of the standing backlog is owed, and none should be done.",
            "whether the open backlog gets one",
            id="no sweep is owed",
        ),
    ],
)
def test_the_document_answers_what_it_left_open(clause, what_it_answers):
    """A12. Each of the three was a gap #450 named, and each is the kind a
    reader fills in for themselves — differently each time — when the document
    does not."""
    assert clause in flat(OWNER), (
        f"{OWNER} no longer says {what_it_answers}: {clause!r} is gone"
    )


def test_the_no_sweep_rule_carries_its_reason():
    """A rule with no reason is one the next reader overturns by having a
    different intuition, and the obvious first move after creating a label is
    to apply it everywhere."""
    doc = flat(OWNER)
    assert "a sweep is the batch, performed once, by the very party the label" in doc
