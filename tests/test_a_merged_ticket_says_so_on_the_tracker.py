"""Issue #359, the signal half: a squash into `release/vX.Y.Z` puts
`merged: X.Y.Z` on the issues its pull requests answered.

Until it did, an issue's state was the only thing on the tracker that said
whether a ticket was done, and that state does not move until `main` moves --
once per release. So for the length of a release a finished work item and one
nobody has started read identically, which is what #359 is about.

Following `tests/test_release_hygiene.py`'s `monkeypatch`-on-the-module's-own-
`run` pattern and `tests/test_a_release_rolls_the_flow_measurement_issue.py`'s
fake tracker: the fixtures below replace `close_issues_on_release`'s `run`,
`arrived` and `_issue_api` -- never the real network.

Two of the three scenarios are about a write NOT happening, which is why the
fake tracker records every call rather than only the interesting ones: a case
that asserts a label was added cannot see a second, redundant add beside it.
"""

import importlib.util
import json
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, ".github", "scripts")
SCRIPT = os.path.join(SCRIPTS, "label_merged_on_release_branch.py")
WORKFLOW = os.path.join(
    ROOT, ".github", "workflows", "label-merged-on-release-branch.yml"
)

BRANCH = "release/v1.2.3"
VERSION = "1.2.3"
LABEL = "merged: 1.2.3"
REPO = "example/repo"


def signal():
    """The labelling script, imported so its readers can be monkeypatched.

    Importing it also loads `close_issues_on_release.py`, which is the point:
    a copy of those readers is exactly what this script exists not to have,
    and a test that stubbed them out could not see one arrive.
    """
    spec = importlib.util.spec_from_file_location(
        "specseal_label_merged_for_tests", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def workflow_settings():
    """The workflow with its comment lines removed.

    A setting that exists only in a comment is not a setting, which is
    `tests/test_ci_gives_the_checks_what_they_need.py`'s measured reason for
    the same helper: dropping a real `types:` line and keeping the comment
    above it left that file's checks green. It is also what lets the trigger
    below be read at all — this workflow carries a comment block between
    `on:` and `permissions:`, and a reader that stops at the first
    unindented line stops there.
    """
    return "\n".join(
        line
        for line in read(WORKFLOW).splitlines()
        if not line.lstrip().startswith("#")
    )


class Tracker:
    """A repository's issues, pull requests and labels, and every call made.

    `calls` holds the argument tuples exactly as the script passed them, in
    order, so an assertion can ask about ordering and about absence -- both of
    which a "was it labelled" check cannot see.
    """

    def __init__(self, issues=None, pulls=None, labels=()):
        self.issues = dict(issues or {})
        self.pulls = dict(pulls or {})
        self.labels = set(labels)
        self.calls = []

    def api(self, repo, number):
        if number in self.pulls:
            return {"pull_request": {}, "body": self.pulls[number]}, True
        if number in self.issues:
            return {
                "labels": [{"name": name} for name in self.issues[number]],
                "state": "open",
            }, True
        return None, False

    def run(self, *args):
        self.calls.append(args)
        if args[:3] == ("gh", "label", "list"):
            return json.dumps([{"name": name} for name in sorted(self.labels)])
        if args[:3] == ("gh", "label", "create"):
            self.labels.add(args[3])
            return ""
        if args[:3] == ("gh", "issue", "edit"):
            self.issues[int(args[3])].append(args[-1])
            return ""
        raise AssertionError(f"unexpected command: {args}")

    def writes(self):
        """The calls that change the tracker — everything but the read."""
        return [a for a in self.calls if a[:3] != ("gh", "label", "list")]


def wire(monkeypatch, module, tracker, subjects, branch=BRANCH, **env):
    monkeypatch.setattr(module.closer, "arrived", lambda before, after: subjects)
    monkeypatch.setattr(module.closer, "_issue_api", tracker.api)
    monkeypatch.setattr(module.closer, "run", tracker.run)
    monkeypatch.setenv("BRANCH", branch)
    monkeypatch.setenv("BEFORE", "a" * 40)
    monkeypatch.setenv("AFTER", "b" * 40)
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)


# --- the name mapping ------------------------------------------------------


def test_the_branch_name_decides_the_version_the_milestone_and_the_label():
    """One fact spelled four ways, and nothing checked the chain before.

    `docs/issues-and-milestones.md` and `docs/release-checklist.md` both write
    parts of it out in prose; the gate and the signal both have to agree with
    it and with each other, and a mismatch between `release: X.Y.Z` and
    `merged: X.Y.Z` is a release blocked on a milestone nothing can satisfy.
    """
    m = signal()
    assert m.version_of("release/v1.2.3") == "1.2.3"
    assert m.milestone_title("1.2.3") == "release: 1.2.3"
    assert m.label_name("1.2.3") == "merged: 1.2.3"
    assert "release/v1.2.3" in m.label_description("1.2.3"), (
        "the label's description does not name the branch it records, so a "
        "person reading it on the tracker cannot tell which release it means"
    )


@pytest.mark.parametrize(
    "branch",
    ["main", "feat/a-thing", "release/next", "release/v1.2", "", "release/v1.2.3.4"],
)
def test_a_branch_that_is_not_a_release_names_no_version(branch):
    """A shape it cannot name a version for is skipped, never guessed.

    The workflow triggers on `release/*`, so `release/next` reaches this and a
    version read out of it would be invented. `docs/branch-and-release.md`
    names only `release/vX.Y.Z`.
    """
    assert signal().version_of(branch) is None


def test_a_non_release_branch_writes_nothing_at_all(monkeypatch):
    """The skip is at entry: no range read, no API call, no write."""
    m = signal()
    tracker = Tracker(issues={88: []}, pulls={100: "Closes #88"})
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"], branch="release/next")
    m.main()
    assert tracker.calls == [], (
        "a branch with no version in its name still reached the tracker"
    )


# --- S1: a squash labels what it closes ------------------------------------


def test_it_labels_the_issue_the_keyword_named_and_nothing_else(monkeypatch):
    """S1. Swapping the key and the value in `wanted` would label the pull
    requests instead of the issues, and no string check can see that."""
    m = signal()
    tracker = Tracker(
        issues={88: [], 92: []},
        pulls={100: "Closes #88", 101: "Part of #92"},
        labels={LABEL},
    )
    wire(
        monkeypatch,
        m,
        tracker,
        ["feat: a thing (#100)", "docs: another (#101)"],
    )
    m.main()
    assert tracker.issues[88] == [LABEL]
    assert tracker.issues[92] == [], (
        "`Part of #92` is not a closing keyword, and #92 was labelled anyway"
    )
    assert tracker.writes() == [
        ("gh", "issue", "edit", "88", "--repo", REPO, "--add-label", LABEL)
    ]


def test_a_keyword_inside_a_fence_labels_nothing(monkeypatch):
    """The readers are the closer's, so a quoted example is not a claim here
    either. A body quoting `docs/branch-and-release.md`'s fenced example would
    otherwise label the issue that document names, and bodies here quote the
    documents routinely."""
    m = signal()
    tracker = Tracker(issues={88: []}, pulls={100: "```\nCloses #88\n```"})
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"])
    m.main()
    assert tracker.writes() == [], "a fenced keyword was read as a claim"


def test_a_number_that_names_no_pull_request_is_skipped(monkeypatch):
    """`fix: the thing (#61)` is a number a person typed to name an issue.
    Failing on it would fail a push for a commit message."""
    m = signal()
    tracker = Tracker(issues={61: [], 88: []}, pulls={100: "Closes #88"})
    wire(monkeypatch, m, tracker, ["fix: a thing (#61)", "feat: b (#100)"])
    m.main()
    assert tracker.issues[61] == [], "an issue number in a subject was labelled"
    assert tracker.issues[88] == [LABEL]


def test_a_claimed_number_that_names_nothing_is_skipped(monkeypatch):
    """A typo in a merged body is input, not a failure — and the run has to
    reach the issues sorted after it."""
    m = signal()
    tracker = Tracker(issues={88: []}, pulls={100: "closes #9999, closes #88"})
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"])
    m.main()
    assert tracker.issues[88] == [LABEL], (
        "a number naming nothing stopped the run before the real issue"
    )


# --- S2: the label is created when it is absent -----------------------------


def test_the_label_is_created_before_it_is_added(monkeypatch):
    """S2. Ordering, because an add against a label that does not exist fails
    — and a case that only asserts both calls happened cannot see the order
    they happened in."""
    m = signal()
    tracker = Tracker(issues={88: []}, pulls={100: "Closes #88"}, labels=set())
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"])
    m.main()
    writes = tracker.writes()
    assert [a[:3] for a in writes] == [
        ("gh", "label", "create"),
        ("gh", "issue", "edit"),
    ], f"the label was not created before it was added: {writes}"
    assert writes[0][3] == LABEL
    assert "--description" in writes[0], (
        "the label is created with no description, so the tracker shows a "
        "bare name where a person has to work out what it means"
    )


def test_an_existing_label_is_not_created_again(monkeypatch):
    """S2's other half. `gh label create` on a name that exists is an error,
    so this is the difference between a green run and a red one on every
    release after the first push."""
    m = signal()
    tracker = Tracker(issues={88: []}, pulls={100: "Closes #88"}, labels={LABEL})
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"])
    m.main()
    assert [a[:3] for a in tracker.writes()] == [("gh", "issue", "edit")]


def test_the_label_is_read_before_it_is_created(monkeypatch):
    """The read is what makes the case above true of the real tracker rather
    than of this fixture: without it the script would be assuming the label's
    absence instead of checking it."""
    m = signal()
    tracker = Tracker(issues={88: []}, pulls={100: "Closes #88"}, labels=set())
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"])
    m.main()
    assert tracker.calls[0][:3] == ("gh", "label", "list"), (
        f"the first tracker call was {tracker.calls[0]}, not the label read"
    )


# --- S3: re-running changes nothing ----------------------------------------


def test_an_issue_that_already_carries_the_label_is_left_alone(monkeypatch):
    """S3, and the reason it is a case rather than an assumption.

    Whether adding a label an issue already has errors or is a no-op was never
    measured here (`questions.md` Q6). Reading first means the answer is not
    load-bearing: the path is never reached. A future edit that drops the read
    and adds unconditionally turns this red.
    """
    m = signal()
    tracker = Tracker(
        issues={88: [LABEL, "documentation"]},
        pulls={100: "Closes #88"},
        labels={LABEL},
    )
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"])
    m.main()
    assert tracker.writes() == [], "the same push labelled #88 a second time"
    assert tracker.issues[88] == [LABEL, "documentation"]


def test_a_push_with_no_claimed_issue_writes_nothing(monkeypatch):
    """Including no label creation. A release branch that moves for a commit
    claiming nothing must not leave a label behind for a version it has not
    yet shipped anything of."""
    m = signal()
    tracker = Tracker(pulls={100: "Part of #92"}, labels=set())
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"])
    m.main()
    assert tracker.calls == []


# --- DRY_RUN ---------------------------------------------------------------


def test_dry_run_reads_and_writes_nothing(monkeypatch):
    """The neighbouring script grew this flag because it was run by hand for
    its output and closed a real issue. The same hand reaches this one."""
    m = signal()
    tracker = Tracker(issues={88: []}, pulls={100: "Closes #88"}, labels=set())
    wire(monkeypatch, m, tracker, ["feat: a thing (#100)"], DRY_RUN="1")
    m.main()
    assert tracker.writes() == [], "DRY_RUN wrote to the tracker"
    assert tracker.issues[88] == []


# --- what the script is allowed to do at all --------------------------------


def test_the_script_only_ever_creates_a_label_and_adds_one():
    """Fold the source before matching: the arguments go one per line, so a
    forbidden-substring list over the raw text forbids nothing.

    `close_issues_on_release.py` has the same case for the same reason — what
    makes a re-run and a force-push safe to reason about is that the set of
    writes is small enough to enumerate.
    """
    folded = " ".join(read(SCRIPT).split())
    assert '"gh", "label", "create",' in folded, "the script stopped creating"
    assert '"--add-label",' in folded, "the script stopped adding"
    for forbidden in ("close", "reopen", "delete", "comment", "transfer"):
        assert f'"gh", "issue", "{forbidden}"' not in folded, (
            f"the script gained `issue {forbidden}`. Closing an issue at the "
            "release-branch merge closes it for something nobody has received"
        )
    assert '"gh", "label", "delete"' not in folded, (
        "the script gained `label delete`, which removes the label from every "
        "issue that carried it and falsifies the record it was created to "
        "leave"
    )


def test_the_readers_come_from_the_closer_rather_than_a_second_copy():
    """Two readers of the same pull request body drifted apart here before.

    `FENCE` and `SPAN` carry a `# RIDER:` stamp and an open decision (#266)
    about widening them; a second copy of that treatment would answer that
    decision by accident, in a file whose author never read the rider.
    """
    source = read(SCRIPT)
    assert "close_issues_on_release.py" in source, "the closer is not imported"
    for own in ("CLOSING = re.compile", "FENCE = re.compile", "SPAN = re.compile"):
        assert own not in source, f"the script wrote its own {own.split()[0]}"
    m = signal()
    assert m.closer.keywords_in("see `Closes #54` in the doc") == [], (
        "the imported reader is not the one that ignores a code span"
    )


# --- the workflow -----------------------------------------------------------


def test_the_token_is_the_smallest_that_can_add_a_label():
    """Read the block as a mapping, not as text: a substring search for
    `contents: write` passes `contents:  write`, which is one value to YAML.

    Its sibling `close-issues-on-release.yml` has the same case. This token is
    handed a pull request body somebody else wrote, and the only thing that
    keeps that from mattering is how little it can do.
    """
    workflow = workflow_settings()
    block = re.search(r"^permissions:\n((?:  [\w-]+:.*\n)+)", workflow, re.M)
    assert block, "the workflow states no permissions block, so it inherits all"
    granted = dict(re.findall(r"^  ([\w-]+):\s*(\S+)\s*$", block.group(1), re.M))
    assert granted == {"contents": "read", "issues": "write"}, (
        f"the token's scopes changed: {granted}. Its only writes are a label "
        "create and a label add"
    )


def test_the_trigger_is_a_push_to_a_release_branch_and_nothing_else():
    """A trigger an untrusted pull request can fire hands it this token.

    The sibling workflow's case says the same of `push: [main]`; a release
    branch is pushed to by a squash merge, which needs write access to the
    repository.
    """
    workflow = workflow_settings()
    on = re.search(r"^on:\n((?:  .*\n|\n)*?)^\w", workflow, re.M)
    assert on and re.findall(r"^  ([\w_]+):", on.group(1), re.M) == ["push"], (
        "the workflow gained a second trigger"
    )
    assert re.search(r"^\s*branches:\s*\['release/\*'\]\s*$", workflow, re.M), (
        "the push trigger no longer names `release/*` alone"
    )


def test_the_checkout_has_the_range_the_script_reads():
    """`arrived()` reads `git log before..after`. At depth 1 neither end of
    that range is in the clone, and the run reads the tip alone — which is the
    fallback that dropped three of four pull requests when it fired."""
    assert "fetch-depth: 0" in read(WORKFLOW)
