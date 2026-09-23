"""#536: one issue the tracker refuses to close does not leave the rest open.

At the release before this change the closer ran when the release reached
`main`, closed the first issue in sorted order, and died on the second with
`gh issue close … failed: GraphQL: Something went wrong while executing your
query`. Four issues it had not reached yet stayed open, because `run` exits on
the first non-zero `gh` and the close loop called it once per issue. Run by
hand with the same inputs it died in the same place; `gh api -X PATCH
repos/<owner>/<repo>/issues/<n> -f state=closed` closed the issue at once.

  S1   a refusal on `gh issue close` takes the REST route — a PATCH and then
       the same comment posted through `gh api …/comments` — and the run
       exits 0 with every issue closed
  S2   a refusal on both routes is named with both errors, every other issue
       is still attempted and closed, the spent label still comes off each
       closed issue, and the exit is non-zero at the END
  S3   `tests/test_release_hygiene.py`'s AST case still counts one `gh issue
       close`, one `gh issue edit --remove-label` and no `gh issue comment`:
       the fallback's comment goes through `gh api`, on purpose

**Nothing here reaches GitHub.** The fake tracker below follows
`tests/test_a_declared_label_reaches_the_tracker.py`'s: every call is recorded
as an argument tuple, in order, so a case can assert about ORDER — that #3 was
attempted after #2 was refused — and not only about the end state.

**Shown red before it was committed (§15).** At `HEAD` before the fix, `run`
exits on the refused close, so S1 fails with #3 still open and S2 fails
because the exit arrives before #3 is attempted; both outputs are quoted in
phase 1's record of work item
`1790173209-the-release-tail-stops-at-the-first-issue-it-cannot-close`.
"""

import importlib.util
import os
import re

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS = os.path.join(ROOT, ".github", "scripts")

REPO = "example/repo"
LABEL = "size: now"
GRAPHQL_REFUSAL = "GraphQL: Something went wrong while executing your query"
REST_REFUSAL = "HTTP 502: Bad Gateway"


def closer_module():
    spec = importlib.util.spec_from_file_location(
        "specseal_closer_for_refusal_tests",
        os.path.join(SCRIPTS, "close_issues_on_release.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Tracker:
    """Issues with labels and states, pull request bodies, and every call.

    `refuse_close` is the set of issue numbers `gh issue close` refuses, the
    way the tracker refused #515 — AFTER the comment landed, because
    `gh issue close --comment` posts the comment and then sends the close,
    and the refused issue at the previous release carried the workflow's
    comment (round 1, finding 1). `refuse_before_comment` is the other order,
    a refusal that left nothing on the issue. `refuse_rest` is the set the
    REST PATCH refuses too. Both routes record the comment they post, so a
    case can count what the issue ends up carrying.
    """

    def __init__(
        self, issues, pulls, refuse_close=(), refuse_rest=(), refuse_before_comment=()
    ):
        self.issues = {n: list(labels) for n, labels in issues.items()}
        self.states = dict.fromkeys(self.issues, "open")
        self.pulls = dict(pulls)
        self.refuse_close = set(refuse_close)
        self.refuse_rest = set(refuse_rest)
        self.refuse_before_comment = set(refuse_before_comment)
        self.comments = {n: [] for n in self.issues}
        self.calls = []

    def api(self, repo, number):
        if number in self.pulls:
            return {"pull_request": {}, "body": self.pulls[number]}, True
        if number in self.issues:
            return {
                "labels": [{"name": name} for name in self.issues[number]],
                "state": self.states[number],
                "comments": len(self.comments[number]),
            }, True
        return None, False

    def run(self, *args):
        """The exiting runner. Before the fix the close went through it, and
        a refusal here is what `run` does with one: `sys.exit`."""
        self.calls.append(args)
        if args[:3] == ("gh", "issue", "close"):
            ok, error = self.attempt(*args)
            self.calls.pop()
            if not ok:
                raise SystemExit(f"{' '.join(args)} failed: {error}")
            return ""
        raise AssertionError(f"unexpected command: {args}")

    def attempt(self, *args):
        """`(ok, stderr)` for a write, the shape the fixed closer reads."""
        self.calls.append(args)
        if args[:3] == ("gh", "issue", "close"):
            number = int(args[3])
            if number in self.refuse_before_comment:
                return False, GRAPHQL_REFUSAL
            # The comment lands first and the close is what gets refused:
            # the order the tracker showed (round 1, finding 1).
            self.comments[number].append(args[args.index("--comment") + 1])
            if number in self.refuse_close:
                return False, GRAPHQL_REFUSAL
            self.states[number] = "closed"
            return True, ""
        if args[:2] == ("gh", "api"):
            path = next(a for a in args if a.startswith(f"repos/{REPO}/issues/"))
            number = int(path.split("/")[4])
            field = next(a for a in args if "=" in a and not a.startswith("-"))
            if path.endswith("/comments"):
                assert field.startswith("body="), args
                self.comments[number].append(field[len("body=") :])
                return True, ""
            assert "-X" in args and args[args.index("-X") + 1] == "PATCH", args
            assert field == "state=closed", args
            if number in self.refuse_rest:
                return False, REST_REFUSAL
            self.states[number] = "closed"
            return True, ""
        raise AssertionError(f"unexpected command: {args}")

    def edit(self, command, **kwargs):
        """Stands in for `subprocess.run` on the label removal alone."""
        self.calls.append(tuple(command))
        assert command[:3] == ["gh", "issue", "edit"], command
        number = int(command[3])

        class Result:
            returncode, stderr = 0, ""

        if LABEL in self.issues.get(number, []):
            self.issues[number].remove(LABEL)
        return Result()

    def closes(self):
        """`(number, route)` for every close attempted, in order."""
        out = []
        for args in self.calls:
            if args[:3] == ("gh", "issue", "close"):
                out.append((int(args[3]), "gh issue close"))
            elif args[:2] == ("gh", "api") and "-X" in args:
                path = next(a for a in args if a.startswith("repos/"))
                out.append((int(path.split("/")[4]), "gh api PATCH"))
        return out


def wire(monkeypatch, tracker):
    mod = closer_module()
    monkeypatch.setattr(mod, "arrived", lambda before, after: ["feat: a thing (#100)"])
    monkeypatch.setattr(mod, "_issue_api", tracker.api)
    monkeypatch.setattr(mod, "run", tracker.run)
    # `raising=False` so the case is red for its own reason on the tree
    # before the fix, where no `attempt` exists and every close goes through
    # `run` — rather than red on this line.
    monkeypatch.setattr(mod, "attempt", tracker.attempt, raising=False)
    monkeypatch.setattr(mod.subprocess, "run", tracker.edit)
    monkeypatch.setenv("AFTER", "aaa")
    monkeypatch.setenv("BEFORE", "bbb")
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.delenv("DRY_RUN", raising=False)
    return mod


THREE = {1: [LABEL], 2: [LABEL], 3: [LABEL]}
CLAIMS = {100: "Closes #1\nCloses #2\nCloses #3"}


# --- S1: one route refuses, the other closes ---------------------------------


def test_a_refused_close_takes_the_rest_route_and_the_run_finishes(monkeypatch, capsys):
    """S1. The tracker refuses `gh issue close 2` the way it refused #515;
    the PATCH closes it, the comment follows through the API, and #3 —
    sorted after it — is closed as well. Exit 0: nothing is left for a
    person to repair."""
    tracker = Tracker(THREE, CLAIMS, refuse_close={2})
    mod = wire(monkeypatch, tracker)

    mod.main()

    assert tracker.states == {1: "closed", 2: "closed", 3: "closed"}, (
        f"a refusal on #2 left the tracker at {tracker.states}"
    )
    assert tracker.closes() == [
        (1, "gh issue close"),
        (2, "gh issue close"),
        (2, "gh api PATCH"),
        (3, "gh issue close"),
    ], tracker.calls
    out = capsys.readouterr().out
    assert "closed #2" in out and "REST" in out and GRAPHQL_REFUSAL in out, (
        f"the log does not say #2 took the fallback, or why: {out!r}"
    )


def test_the_fallback_posts_the_same_comment_the_first_route_carries(monkeypatch):
    """The comment is the last thing written on an issue people go on
    reading, and it says why a workflow closed it. An issue closed through
    the REST route ends up with the same sentence ONCE: `gh issue close
    --comment` posts the comment before the close it then fails, so the
    refused route usually left it already, and the fallback must not post it
    a second time. Measured on the tracker after the previous release: the
    issue that run could not close carried one identical comment per refused
    run (round 1, finding 1)."""
    tracker = Tracker(THREE, CLAIMS, refuse_close={2})
    mod = wire(monkeypatch, tracker)

    mod.main()

    assert len(tracker.comments[2]) == 1, (
        f"#2 carries {len(tracker.comments[2])} closing comments; the refused "
        f"route had already posted one"
    )
    assert tracker.comments[2] == tracker.comments[1], (
        f"the REST route's comment differs from the first route's:\n"
        f"{tracker.comments[2][0]!r}\n{tracker.comments[1][0]!r}"
    )
    assert "Closed by #100" in tracker.comments[2][0]


def test_a_refusal_before_the_comment_landed_still_gets_it_from_the_fallback(
    monkeypatch,
):
    """The other order: the comment mutation is what the tracker refused, so
    nothing is on the issue yet and the fallback has to say why it closed."""
    tracker = Tracker(THREE, CLAIMS, refuse_before_comment={2})
    mod = wire(monkeypatch, tracker)

    mod.main()

    assert tracker.states[2] == "closed"
    assert tracker.comments[2] == tracker.comments[1], tracker.comments


def test_a_tracker_that_does_not_count_comments_gets_the_comment_posted(
    monkeypatch,
):
    """Where the read cannot say whether the first route's comment landed,
    the fallback posts it: a duplicate is the smaller wrong answer than a
    close nobody explained."""

    class Uncounted(Tracker):
        def api(self, repo, number):
            data, exists = super().api(repo, number)
            if exists:
                data.pop("comments", None)
            return data, exists

    tracker = Uncounted(THREE, CLAIMS, refuse_close={2})
    mod = wire(monkeypatch, tracker)

    mod.main()

    assert tracker.states[2] == "closed"
    assert len(tracker.comments[2]) == 2, tracker.comments


def test_an_issue_closed_through_the_fallback_still_loses_its_spent_label(
    monkeypatch,
):
    """The label comes off after the close, whichever route closed it. A
    fallback that skipped the bookkeeping would leave #2 the one issue on
    the tracker still carrying a spent `size: now`."""
    tracker = Tracker(THREE, CLAIMS, refuse_close={2})
    mod = wire(monkeypatch, tracker)

    mod.main()

    assert all(LABEL not in tracker.issues[n] for n in (1, 2, 3)), tracker.issues


# --- S2: both routes refuse ---------------------------------------------------


def test_a_refusal_on_both_routes_is_named_at_the_end_and_the_rest_still_close(
    monkeypatch,
):
    """S2. #2 stays open — nothing this script can do closes it — and the run
    says so with both errors, AFTER attempting #3. The exit is non-zero so
    the job is red, and it is red at the end rather than at #2."""
    tracker = Tracker(THREE, CLAIMS, refuse_close={2}, refuse_rest={2})
    mod = wire(monkeypatch, tracker)

    with pytest.raises(SystemExit) as raised:
        mod.main()

    assert tracker.states == {1: "closed", 2: "open", 3: "closed"}, (
        f"#3 is sorted after the refused #2 and had to be closed anyway: "
        f"{tracker.states}"
    )
    assert tracker.closes() == [
        (1, "gh issue close"),
        (2, "gh issue close"),
        (2, "gh api PATCH"),
        (3, "gh issue close"),
    ], tracker.calls
    message = str(raised.value.code)
    assert raised.value.code, "the run exited 0 with an issue it could not close"
    assert "#2" in message and GRAPHQL_REFUSAL in message and REST_REFUSAL in message, (
        f"the exit names neither the issue nor both refusals: {message!r}"
    )
    # `\b`, because `#100` — the pull request every line names — holds `#1`.
    assert not re.search(r"#[13]\b", message), (
        f"the exit names an issue that closed: {message!r}"
    )


def test_the_spent_label_comes_off_what_closed_and_stays_on_what_did_not(
    monkeypatch,
):
    """The label is bookkeeping about a close that happened. Taking it off
    an issue still open would say the release finished with it."""
    tracker = Tracker(THREE, CLAIMS, refuse_close={2}, refuse_rest={2})
    mod = wire(monkeypatch, tracker)

    with pytest.raises(SystemExit):
        mod.main()

    assert LABEL not in tracker.issues[1] and LABEL not in tracker.issues[3]
    assert LABEL in tracker.issues[2], "the label came off an issue still open"


def test_the_exit_message_says_how_a_partial_close_is_repaired(monkeypatch):
    """A red job nobody can act on is a red job somebody re-learns. The
    message names the re-run — the same script, the same three inputs —
    because a re-run skips what is already closed and reaches the rest."""
    tracker = Tracker(THREE, CLAIMS, refuse_close={2}, refuse_rest={2})
    mod = wire(monkeypatch, tracker)

    with pytest.raises(SystemExit) as raised:
        mod.main()

    message = str(raised.value.code)
    for name in ("BEFORE", "AFTER", "REPO"):
        assert name in message, f"the exit does not name {name}: {message!r}"


# --- the runner under it all --------------------------------------------------


def test_attempt_answers_the_exit_code_and_the_error_rather_than_exiting(
    monkeypatch,
):
    """Every case above fakes `attempt`, so a mutation making it report every
    write as refused left all of them green. This one drives the real
    function against a fake `subprocess.run`, both ways round."""
    mod = closer_module()
    outcomes = iter([(0, ""), (1, "HTTP 502: Bad Gateway\n")])

    class Result:
        def __init__(self, returncode, stderr):
            self.returncode, self.stderr = returncode, stderr

    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **k: Result(*next(outcomes)))
    assert mod.attempt("gh", "issue", "close", "1") == (True, "")
    assert mod.attempt("gh", "issue", "close", "2") == (False, "HTTP 502: Bad Gateway")


# --- S3: the fallback adds no verb the AST case forbids -----------------------


def test_the_fallback_comments_through_the_api_and_not_through_issue_comment():
    """`gh issue comment` is on the forbidden list in
    `tests/test_release_hygiene.py`, because a script that can comment on an
    issue can comment on an unrelated one. The fallback's comment is the REST
    `…/issues/<n>/comments` endpoint, reached through `gh api` — the same
    two writes, one route over."""
    with open(
        os.path.join(SCRIPTS, "close_issues_on_release.py"), encoding="utf-8"
    ) as f:
        source = f.read()
    body = source.split('"""', 2)[2]
    assert "/comments" in body, "the fallback posts no comment at all"
    assert '"comment"' not in body.replace('"--comment"', ""), (
        "the fallback reaches `gh issue comment`, which the hygiene case forbids"
    )
