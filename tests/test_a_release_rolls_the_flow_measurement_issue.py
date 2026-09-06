"""Issue #109 part 3: `.github/scripts/roll_flow_measurement_issue.py` closes
the currently-open `flow-measurement` issue and opens the next one, titled
after the version this release just shipped. It runs as a second step in
`close-issues-on-release.yml`, on the same trigger and checkout
`close_issues_on_release.py` already uses.

Issue #155 gave it a condition. The roll fires when a new version has shipped
since the open log opened, not on every push to `main`, and the title states
the version it rolled FROM rather than a guess at the version it is for --
`log_title` and `rolled_from` are pure and read the same constant. The cases
for that half are at the bottom of this file, under their own heading.

Following `tests/test_release_hygiene.py:225-355`'s `monkeypatch`-on-
`subprocess.run` pattern for that neighbouring script: the exactly-one-open
invariant and the retry-once hardening (phase 1's own finding, in the
module's docstring) are tested by monkeypatching the module's own `run`,
`list_open_issues`, `read_version`, and `time.sleep` -- never the real
network.

Every fixture below carries `chore: flow measurement — 0.7.0` as the open
log's title, which is the OLD convention: it names no version the roll can
read, so it is always due and every case here reaches the roll it is about.
That is deliberate rather than left over -- it is also the migration path,
exercised by every case in the file.
"""

import json
import os

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _roller():
    """The rollover script, imported so its functions can be monkeypatched
    and its regex/format strings read directly -- the same reason
    `tests/test_release_hygiene.py`'s own `_closer()` imports rather than
    shells out."""
    import importlib.util

    path = os.path.join(ROOT, ".github", "scripts", "roll_flow_measurement_issue.py")
    spec = importlib.util.spec_from_file_location("roll_flow_measurement_issue", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_zero_open_issues_after_the_retry_fails_loudly(monkeypatch):
    """Phase 1 measured the lookup returning `[]` right after a label write,
    then correctly finding the issue seconds later. The retry exists so a
    lag artifact does not masquerade as the real zero -- but a *second*
    empty reading is the real zero, and that still fails loudly rather than
    guessing."""
    m = _roller()
    calls = []
    monkeypatch.setattr(m, "list_open_issues", lambda repo: calls.append(repo) or [])
    slept = []
    monkeypatch.setattr(m.time, "sleep", lambda s: slept.append(s))
    monkeypatch.setattr(m, "read_version", lambda: "0.7.0")
    monkeypatch.setenv("REPO", "example/repo")

    raised = False
    try:
        m.main()
    except SystemExit as exc:
        raised = True
        assert "found 0" in str(exc), f"the exit message lost the count: {exc}"
    assert raised, "zero open issues, even after a retry, must exit loudly"
    assert len(calls) == 2, (
        f"expected one retry (two lookups total), got {len(calls)} -- the "
        "retry-once hardening stopped retrying, or started retrying more "
        "than once"
    )
    assert slept == [m.RETRY_DELAY_SECONDS], (
        "the retry must sleep before the second lookup, using the module's "
        "own delay constant"
    )


def test_one_open_issue_after_the_retry_succeeds():
    """The retry's whole point: a first reading of zero is not necessarily
    the real state, and a second reading of one must be trusted rather than
    treated as a second violation."""
    m = _roller()
    readings = [[], [{"number": 89, "title": "chore: flow measurement — 0.7.0"}]]
    calls = []

    def fake_list(repo):
        calls.append(repo)
        return readings.pop(0)

    closed = []
    created = []
    slept = []
    m.list_open_issues = fake_list
    m.time.sleep = lambda s: slept.append(s)
    m.read_version = lambda: "0.7.0"
    m.close_issue = lambda repo, number: closed.append((repo, number))
    m.open_issue = lambda repo, shipped, closed_number: (
        created.append((repo, shipped, closed_number))
        or (f"chore: flow measurement — after {shipped}")
    )
    os.environ["REPO"] = "example/repo"
    try:
        m.main()
    finally:
        del os.environ["REPO"]

    assert len(calls) == 2, "a one-open reading on retry must not retry again"
    assert closed == [("example/repo", 89)]
    assert created == [("example/repo", "0.7.0", 89)], (
        "two things reach `open_issue` and `main` is the only caller that "
        "knows either: the version this tree ships, which is what the new "
        "title states, and the number just closed, which is what the new "
        "body rolls from"
    )


def test_two_open_issues_fails_loudly_without_retrying(monkeypatch):
    """A reading of two or more is never what a search-index lag produces --
    a lag can only undercount -- so it must not get the retry's benefit of
    the doubt."""
    m = _roller()
    calls = []
    monkeypatch.setattr(
        m,
        "list_open_issues",
        lambda repo: (
            calls.append(repo)
            or [{"number": 1, "title": "a"}, {"number": 2, "title": "b"}]
        ),
    )
    slept = []
    monkeypatch.setattr(m.time, "sleep", lambda s: slept.append(s))
    monkeypatch.setattr(m, "read_version", lambda: "0.7.0")
    monkeypatch.setenv("REPO", "example/repo")

    raised = False
    try:
        m.main()
    except SystemExit as exc:
        raised = True
        assert "found 2" in str(exc)
    assert raised, "two open issues must exit loudly rather than pick one"
    assert len(calls) == 1, "two open issues must not trigger the retry"
    assert slept == [], "two open issues must not sleep at all"


def test_one_open_issue_closes_it_and_opens_the_next(monkeypatch):
    """The full round trip, with `run` itself mocked (matching
    `tests/test_release_hygiene.py`'s pattern for `close_issues_on_release.py`)
    so the exact `gh` arguments are visible -- the same reason that file's
    `test_it_closes_the_issue_the_keyword_named_and_nothing_else` mocks `run`
    rather than a higher-level function."""
    m = _roller()
    calls = []

    def fake_try_run(*args):
        """The durable ledger's lookup answers with an issue; every other
        best-effort call succeeds and returns nothing readable, which is what
        `gh issue create` returns anyway."""
        calls.append(args)
        if args[:3] == ("gh", "issue", "list"):
            return json.dumps([{"number": 51}])
        return ""

    monkeypatch.setattr(m, "run", lambda *a: calls.append(a) or "")
    monkeypatch.setattr(m, "try_run", fake_try_run)
    monkeypatch.setattr(
        m,
        "list_open_issues",
        lambda repo: [{"number": 89, "title": "chore: flow measurement — 0.7.0"}],
    )
    monkeypatch.setattr(m, "read_version", lambda: "0.7.0")
    monkeypatch.setenv("REPO", "example/repo")

    m.main()

    close_calls = [a for a in calls if a[:3] == ("gh", "issue", "close")]
    create_calls = [a for a in calls if a[:3] == ("gh", "issue", "create")]
    assert close_calls and close_calls[0][3] == "89", (
        f"expected `gh issue close 89 ...`, got {calls}"
    )
    assert create_calls, f"no `gh issue create` call was made: {calls}"
    create_args = create_calls[0]
    assert "--title" in create_args
    title = create_args[create_args.index("--title") + 1]
    assert title == "chore: flow measurement — after 0.7.0", (
        f"the new issue's title must name the version this tree ships, which "
        f"is the version the log it opens rolls from: {title!r}"
    )
    assert "--label" in create_args
    assert create_args[create_args.index("--label") + 1] == "flow-measurement"
    labels = [create_args[i + 1] for i, a in enumerate(create_args) if a == "--label"]
    assert labels == ["flow-measurement", "measurement"], (
        f"the create must carry the lookup key and this repository's index "
        f"label, in that order -- the first is what the roll and the skill "
        f"find the log by, the second is what puts it beside the durable "
        f"ledger: {labels}"
    )
    assert "--milestone" in create_args, (
        f"the create must ask for the `log: measurement` milestone: {create_args}"
    )
    assert create_args[create_args.index("--milestone") + 1] == "log: measurement"
    assert "--body" in create_args
    body = create_args[create_args.index("--body") + 1]
    assert "#89" in body, (
        f"the new issue's body must name the issue it rolls from, so a "
        f"reader of the 0.9.0 log has a path back to the 0.8.0 one: {body!r}"
    )
    assert "#51" in body, (
        f"the new issue's body must name the durable ledger, found by the "
        f"`flow-baseline` label rather than hardcoded: {body!r}"
    )
    assert "since 0.7.0 shipped" in body, (
        f"the body must say what stretch of work this log covers, in the "
        f"same terms as its title: {body!r}"
    )
    assert "closed by the release that ships the next version" in body, (
        f"the new issue's body must say when it closes -- it is a rolling "
        f"log, and nothing on the issue itself says so. It cannot name that "
        f"version, which is the whole of #155: {body!r}"
    )


def _ladder_harness(m, monkeypatch, create_results, readings, baseline="[]"):
    """Drive `main` with the create call answering from `create_results` and
    the open-issue lookup from `readings`.

    `create_results` is one entry per create attempt: a string for a call that
    succeeded, `None` for one that reported failure. `readings` is what
    `list_open_issues` answers, in order -- the first is `main`'s own lookup,
    and each later one is a read `landed_create` takes. `baseline` is what the
    durable ledger's own lookup answers with.

    Returns `(creates, slept)` -- the `gh issue create` argument tuples that
    were made, and the delays that were waited. The second exists because the
    guard's retry is worth nothing without its sleep: an immediate second read
    hits the same lagged index, and a mutation removing the sleep left every
    case in this module green until it was added.
    """
    creates = []
    slept = []

    def fake_try_run(*args):
        if args[:3] == ("gh", "issue", "create"):
            creates.append(args)
            return create_results.pop(0)
        return baseline

    monkeypatch.setattr(m, "try_run", fake_try_run)
    monkeypatch.setattr(
        m, "list_open_issues", lambda repo: readings.pop(0) if readings else []
    )
    monkeypatch.setattr(m, "close_issue", lambda repo, number: None)
    monkeypatch.setattr(m, "read_version", lambda: "0.7.0")
    monkeypatch.setattr(m.time, "sleep", lambda s: slept.append(s))
    monkeypatch.setenv("REPO", "example/repo")
    return creates, slept


OPEN_ONE = [{"number": 89, "title": "chore: flow measurement — 0.7.0"}]


def test_a_milestone_that_cannot_be_set_does_not_fail_the_release(monkeypatch):
    """`gh issue create --milestone` fails outright on a name it cannot
    resolve, and a milestone is repository state -- it gets renamed and
    deleted. The invariant this script protects is the one-open rule, which no
    milestone touches, so the release does not stop for it."""
    m = _roller()
    creates, _ = _ladder_harness(m, monkeypatch, [None, ""], [list(OPEN_ONE), []])
    monkeypatch.setattr(m, "run", lambda *a: pytest.fail(f"fell through to run: {a}"))

    m.main()

    assert len(creates) == 2, f"expected one fallback attempt: {creates}"
    assert "--milestone" not in creates[1], (
        f"the fallback must drop the milestone -- retrying with the argument "
        f"that failed is not a fallback: {creates[1]}"
    )
    assert "measurement" in creates[1], (
        f"the fallback must keep the index label; only the milestone failed: "
        f"{creates[1]}"
    )
    body = creates[1][creates[1].index("--body") + 1]
    assert "log: measurement" in body and "could not be set" in body, (
        f"the issue's own body must say the milestone could not be set. It is "
        f"the one artifact a person opens; a line in a workflow log is not "
        f"read: {body!r}"
    )


def test_both_best_effort_arguments_failing_still_opens_the_issue(monkeypatch):
    m = _roller()
    creates, _ = _ladder_harness(m, monkeypatch, [None, None], [list(OPEN_ONE), [], []])
    monkeypatch.setattr(m, "run", lambda *a: creates.append(a) or "")

    m.main()

    assert len(creates) == 3, f"expected two fallbacks then the plain create: {creates}"
    final = creates[2]
    assert "--milestone" not in final and final.count("--label") == 1, (
        f"the last attempt carries the lookup key alone -- that is the one "
        f"argument the invariant depends on: {final}"
    )
    body = final[final.index("--body") + 1]
    assert "log: measurement" in body and "`measurement` index label" in body, (
        f"the body must name both things that could not be set, not just the "
        f"last one tried: {body!r}"
    )


def test_a_create_that_landed_despite_a_failed_call_is_not_retried(monkeypatch):
    """The hazard the ladder introduces. A `gh issue create` that fails after
    the mutation lands would, on retry, open a second issue -- the
    exactly-one-open invariant broken from the other side, by the script that
    exists to keep it."""
    m = _roller()
    landed = [{"number": 90, "title": "chore: flow measurement — 0.8.0"}]
    creates, _ = _ladder_harness(m, monkeypatch, [None], [list(OPEN_ONE), landed])
    monkeypatch.setattr(m, "run", lambda *a: pytest.fail(f"fell through to run: {a}"))

    m.main()

    assert len(creates) == 1, (
        f"a failed attempt whose issue is nonetheless open must end the "
        f"ladder; retrying opens a second one: {creates}"
    )


def test_the_issue_main_just_closed_does_not_count_as_the_create_landing(monkeypatch):
    """The guard asks whether a failed create landed anyway. `gh issue list`
    lagging the close that ran seconds earlier answers with the issue `main`
    has already closed, and reading that as the new log ends the release with
    no rolling issue open and the workflow green."""
    m = _roller()
    creates, _ = _ladder_harness(
        m, monkeypatch, [None, ""], [list(OPEN_ONE), list(OPEN_ONE), list(OPEN_ONE)]
    )
    monkeypatch.setattr(m, "run", lambda *a: pytest.fail(f"fell through to run: {a}"))

    m.main()

    assert len(creates) == 2, (
        f"the reading still carries #89, the issue `main` closed before the "
        f"ladder started -- only an issue that is not that one is evidence "
        f"the create landed: {creates}"
    )


def test_the_landed_create_guard_retries_an_empty_reading(monkeypatch):
    """The mirror of the case above, and the reason the guard cannot be one
    lookup. A create that landed followed by a stale empty reading sends the
    ladder down a rung and opens a second issue -- the lag this file already
    retries for in `open_flow_measurement_issues`."""
    m = _roller()
    landed = [{"number": 90, "title": "chore: flow measurement — 0.8.0"}]
    creates, slept = _ladder_harness(
        m, monkeypatch, [None, ""], [list(OPEN_ONE), [], landed]
    )
    monkeypatch.setattr(m, "run", lambda *a: pytest.fail(f"fell through to run: {a}"))

    m.main()

    assert len(creates) == 1, (
        f"the first reading was empty and the second found the issue the "
        f"create had already opened -- an empty reading gets the one retry "
        f"this module gives every other empty reading: {creates}"
    )
    assert slept == [m.RETRY_DELAY_SECONDS], (
        f"the retry must sleep before the second reading, using the module's "
        f"own delay constant. An immediate second read hits the same lagged "
        f"index, so a retry without the sleep is one lookup wearing two "
        f"names -- and removing the sleep left every case here green until "
        f"this line: {slept}"
    )


def test_the_recovery_message_does_not_promise_the_log_is_empty(monkeypatch):
    """`list_open_issues` exits on a `gh` failure, so a lookup that stumbles
    mid-ladder raises `SystemExit` into `main`'s handler. By then the first
    rung's create may already have landed, and an operator told the log has
    zero open issues opens the second one."""
    m = _roller()
    monkeypatch.setattr(
        m, "list_open_issues", lambda repo: [{"number": 89, "title": "x"}]
    )
    monkeypatch.setattr(m, "read_version", lambda: "0.7.0")
    monkeypatch.setattr(m, "close_issue", lambda repo, number: None)

    def fake_open_issue(repo, version, closed_number):
        raise SystemExit("gh issue list failed: some network error")

    monkeypatch.setattr(m, "open_issue", fake_open_issue)
    monkeypatch.setenv("REPO", "example/repo")

    with pytest.raises(SystemExit) as exc:
        m.main()
    message = str(exc.value)
    assert "may still have landed" in message, (
        f"the recovery message must say the create may have landed, because "
        f"`main` cannot know: the failure can arrive from a lookup taken "
        f"after a create that worked: {message!r}"
    )
    assert "zero open issues" not in message, (
        f"the message asserts a state it cannot observe. Somebody following "
        f"it opens the second issue and the next release fails on "
        f"two-or-more: {message!r}"
    )


def test_every_attempt_failing_still_exits_loudly(monkeypatch):
    """The ladder tolerates the two best-effort arguments, never the create.
    A create that fails all the way down is the zero-open state the module
    docstring's recovery message exists for."""
    m = _roller()
    _ladder_harness(m, monkeypatch, [None, None], [list(OPEN_ONE)])

    def fatal(*args):
        raise SystemExit("gh issue create failed: some network error")

    monkeypatch.setattr(m, "run", fatal)

    with pytest.raises(SystemExit) as exc:
        m.main()
    message = str(exc.value)
    assert "89" in message and m.log_title("0.7.0") in message, (
        f"the recovery message must survive the ladder -- it names the "
        f"already-closed issue and the title to open by hand, and that title "
        f"comes from the same constant the roll writes: {message!r}"
    )
    assert m.LABEL in message, (
        f"the recovery message must name the label the recovery issue "
        f"needs: {message!r}"
    )


def test_the_body_drops_the_ledger_clause_where_no_durable_log_exists():
    """A durable ledger is a thing a repository may not have. The clause goes
    rather than the roll failing, and rather than the body carrying the word
    an unguarded f-string would put there."""
    m = _roller()
    body = m.issue_body("0.8.0", 89, None)
    assert "#89" in body, f"the body still rolls from the closed issue: {body!r}"
    assert "since 0.8.0 shipped" in body, (
        f"the body still says what stretch of work it covers: {body!r}"
    )
    assert "live in #" not in body, (
        f"the body points at a durable ledger that does not exist: {body!r}"
    )
    assert "None" not in body, (
        f"the body carries the absent ledger as a word -- `#None` is what an "
        f"unguarded f-string writes, and it reads as an issue link: {body!r}"
    )


def test_the_durable_logs_lookup_answers_none_rather_than_failing(monkeypatch):
    """Three ways for the lookup to come back with nothing, and none of them
    may reach a release: the `gh` call failed, the label exists with nothing
    open, and the output is not JSON at all. All three are silent -- most
    repositories have no durable ledger, and that is not a fault to report."""
    m = _roller()
    for answer in (None, "[]", "not json"):
        monkeypatch.setattr(m, "try_run", lambda *a, _r=answer: _r)
        number, note = m.find_baseline_issue("example/repo")
        assert number is None, (
            f"a lookup answering {answer!r} must be `None`, not an exception "
            f"and not a truthy value the body would interpolate"
        )
        assert note is None, (
            f"a repository with no durable ledger is the ordinary case, and "
            f"a note about it would appear on every rolling log: {note!r}"
        )
    monkeypatch.setattr(m, "try_run", lambda *a: json.dumps([{"number": 51}]))
    assert m.find_baseline_issue("example/repo") == (51, None)


def test_two_open_durable_logs_are_named_rather_than_guessed_between(monkeypatch):
    """The rolling log's invariant and the durable one's are the same
    sentence in `skills/verify/SKILL.md`, and that section says a broken
    invariant is named rather than guessed at. Taking the first of two is the
    guess -- and it is silent, because a body carrying one of two numbers
    looks exactly like a body carrying the only one."""
    m = _roller()
    monkeypatch.setattr(
        m, "try_run", lambda *a: json.dumps([{"number": 51}, {"number": 77}])
    )
    number, note = m.find_baseline_issue("example/repo")
    assert number is None, (
        f"two open `flow-baseline` issues is that invariant broken, and the "
        f"body must not point at one of them as though it were the ledger: "
        f"{number}"
    )
    assert note and "flow-baseline" in note, (
        f"omitting the clause with no note says the repository has no durable "
        f"ledger, which is a different fact from having two: {note!r}"
    )


def test_the_ambiguous_ledger_note_reaches_the_issue_it_is_about(monkeypatch):
    """The other half, and the one a mutation found. `find_baseline_issue`
    answering with a note buys nothing if `open_issue` drops it: setting the
    note aside left every case in this module green, because none of them
    drove a two-open reading through to a created issue's body."""
    m = _roller()
    two_open = json.dumps([{"number": 51}, {"number": 77}])
    creates, _ = _ladder_harness(
        m, monkeypatch, [""], [list(OPEN_ONE)], baseline=two_open
    )
    monkeypatch.setattr(m, "run", lambda *a: pytest.fail(f"fell through to run: {a}"))

    m.main()

    assert len(creates) == 1
    body = creates[0][creates[0].index("--body") + 1]
    assert "flow-baseline" in body and "picking whichever" in body, (
        f"the note never reached the body, so the issue says nothing about "
        f"the ledger and looks exactly like one opened in a repository that "
        f"has none: {body!r}"
    )
    assert "live in #" not in body, (
        f"the body points at a ledger anyway, which is the guess the note "
        f"exists instead of: {body!r}"
    )


def test_close_succeeds_but_open_fails_names_both_in_the_message(monkeypatch):
    """`main` closes the old issue, then opens the next one -- not one
    transaction. Warden round 1 on `0d59003` found that a `gh issue create`
    failure after a successful close left the failure message naming only
    the failed create call, with nothing saying the old issue was already
    closed -- an operator debugging a red release-workflow step had to
    separately check whether the old issue was still open or already closed.
    This pins that the recovery message names both: the closed issue's
    number, and the title to open by hand to restore the invariant."""
    m = _roller()
    monkeypatch.setattr(
        m, "list_open_issues", lambda repo: [{"number": 89, "title": "x"}]
    )
    monkeypatch.setattr(m, "read_version", lambda: "0.7.0")
    closed = []
    monkeypatch.setattr(
        m, "close_issue", lambda repo, number: closed.append((repo, number))
    )

    def fake_open_issue(repo, version, closed_number):
        raise SystemExit("gh issue create failed: some network error")

    monkeypatch.setattr(m, "open_issue", fake_open_issue)
    monkeypatch.setenv("REPO", "example/repo")

    raised = False
    try:
        m.main()
    except SystemExit as exc:
        raised = True
        message = str(exc)
        assert "89" in message, (
            f"the failure message must name the already-closed issue's "
            f"number, so an operator does not have to separately check "
            f"whether it is still open: {message!r}"
        )
        assert m.log_title("0.7.0") in message, (
            f"the failure message must carry the recovery title so an "
            f"operator can open the replacement issue by hand, and it must "
            f"be the title the roll itself writes rather than a second "
            f"spelling of it: {message!r}"
        )
        assert m.LABEL in message, (
            f"the failure message must name the label the recovery issue "
            f"needs: {message!r}"
        )
    assert raised, (
        "an open_issue failure after a successful close must still exit loudly"
    )
    assert closed == [("example/repo", 89)], (
        "close_issue must still have run before the open failed"
    )


def test_read_version_reads_plugin_json(tmp_path):
    """`read_version` is a filesystem read, not a `gh`/`git` call -- covered
    directly rather than mocked, the same way `tests/test_release_hygiene.py`'s
    own `version()` helper reads `plugin.json` straight."""
    m = _roller()
    plugin_dir = tmp_path / ".claude-plugin"
    plugin_dir.mkdir()
    (plugin_dir / "plugin.json").write_text(
        json.dumps({"version": "9.9.9"}), encoding="utf-8"
    )
    assert m.read_version(root=str(tmp_path)) == "9.9.9", (
        "read_version must read the given root, not the real repository's "
        "own plugin.json — a version distinct from this repo's own is used "
        "on purpose so an ignored `root` parameter cannot pass by coincidence"
    )


# --- The condition, and the title the condition reads back (#155) -----------
#
# Until #155 the roll had no condition at all: every push to `main` closed the
# open log and opened one named `next_version(read_version())`. At the 0.8.1
# release that closed #166, opened for `0.9.0` and holding 0.8.1's own
# measurements, and opened #172 with the identical title. The cases below pin
# the two halves the work item settled -- the log is named after the version
# it rolled FROM, and a run that shipped no new version closes nothing.


def _roll_harness(m, monkeypatch, title, shipped, number=89):
    """Drive `main` with one open log titled `title`, against a tree that
    ships `shipped`, and record what was closed and what was created.

    The condition is the only thing under test here, so every `gh` call below
    it succeeds on the first rung -- the create ladder has its own cases
    above, and `run` is wired to fail the case if anything falls through to
    it. Returns `(closed, creates)`.
    """
    closed = []
    creates = []

    def fake_try_run(*args):
        if args[:3] == ("gh", "issue", "create"):
            creates.append(args)
            return ""
        return "[]"

    monkeypatch.setattr(m, "try_run", fake_try_run)
    monkeypatch.setattr(
        m, "list_open_issues", lambda repo: [{"number": number, "title": title}]
    )
    monkeypatch.setattr(m, "close_issue", lambda repo, n: closed.append((repo, n)))
    monkeypatch.setattr(m, "read_version", lambda: shipped)
    monkeypatch.setattr(m, "run", lambda *a: pytest.fail(f"fell through to run: {a}"))
    monkeypatch.setenv("REPO", "example/repo")
    return closed, creates


def _created_title(creates):
    args = creates[0]
    return args[args.index("--title") + 1]


def test_a_push_that_shipped_no_new_version_rolls_nothing(monkeypatch):
    """The half that bites. This workflow fires on every push to `main`, not
    on every release, and even between releases the same push can be replayed
    by a re-run. Where the open log already names the version in the tree,
    nothing has shipped since it opened and there is nothing to roll: the run
    exits 0 having closed nothing and opened nothing."""
    m = _roller()
    closed, creates = _roll_harness(
        m, monkeypatch, "chore: flow measurement — after 0.7.0", "0.7.0"
    )

    m.main()

    assert closed == [], (
        f"the open log is the log for the work since 0.7.0 shipped and 0.7.0 "
        f"is still what this tree ships, so closing it throws away a log "
        f"nothing has replaced: {closed}"
    )
    assert creates == [], (
        f"a second log opened here is the 0.8.1 incident exactly -- two open "
        f"issues where the invariant allows one: {creates}"
    )


def test_a_new_version_since_the_log_opened_rolls_it(monkeypatch):
    """The other half. The new title names the version this tree ships, which
    is the one thing the release moment makes certain -- not the next one,
    which `docs/branch-and-release.md` says is not known until the end."""
    m = _roller()
    closed, creates = _roll_harness(
        m, monkeypatch, "chore: flow measurement — after 0.7.0", "0.8.0"
    )

    m.main()

    assert closed == [("example/repo", 89)], (
        f"0.8.0 shipped after the open log opened, so that log is complete "
        f"and the release closes it: {closed}"
    )
    assert len(creates) == 1, f"expected exactly one create: {creates}"
    assert _created_title(creates) == "chore: flow measurement — after 0.8.0", (
        f"the title must name the version in the tree. Naming a computed "
        f"successor is the guess #155 removed: {_created_title(creates)!r}"
    )


def test_the_title_the_roll_writes_is_the_title_the_next_roll_reads(monkeypatch):
    """Writer and reader are one constant, and this is what holds them
    together. A wording change on the title alone -- a colon for the em dash,
    `since` for `after` -- leaves every other case here green and stops the
    condition reading its own output, after which every later release rolls a
    log that was not due and the invariant breaks from the other side."""
    m = _roller()
    _, creates = _roll_harness(
        m, monkeypatch, "chore: flow measurement — after 0.7.0", "0.8.0"
    )
    m.main()
    written = _created_title(creates)

    closed, again = _roll_harness(m, monkeypatch, written, "0.8.0", number=90)
    m.main()

    assert closed == [] and again == [], (
        f"the roll wrote {written!r} and then did not recognise it as the log "
        f"for the version it had just written it for: closed {closed}, "
        f"created {again}"
    )


def test_a_title_written_before_this_change_is_always_due(monkeypatch):
    """What the old titles mean, made executable. `chore: flow measurement —
    0.9.0` names a version that had not shipped, so it cannot answer "has
    anything shipped since this log opened" -- and the marker this change
    writes, ` — after `, appears in no title written before it. Such a log is
    due whatever the tree ships, which is what retires the old convention at
    the first release after this change rather than by hand.

    The second half is the one that matters. A condition that only asked
    whether the two versions differ would read `0.9.0` against a tree
    shipping `0.9.0` as *nothing due* and leave that log open forever, with
    the workflow green -- the prediction coming true is exactly when the old
    convention would trap the new one."""
    m = _roller()
    old = "chore: flow measurement — 0.9.0"

    _, creates = _roll_harness(m, monkeypatch, old, "0.8.2")
    m.main()
    assert _created_title(creates) == "chore: flow measurement — after 0.8.2", (
        f"a patch release must roll a log named by the old convention: "
        f"{_created_title(creates)!r}"
    )

    closed, met = _roll_harness(m, monkeypatch, old, "0.9.0", number=90)
    m.main()
    assert closed == [("example/repo", 90)], (
        f"the predicted version shipping is not the same fact as the log "
        f"naming the version it rolled from, and reading it as one stalls "
        f"that log for good: {closed}"
    )
    assert _created_title(met) == "chore: flow measurement — after 0.9.0", (
        f"the replacement is named the new way whatever the old one said: "
        f"{_created_title(met)!r}"
    )


def test_a_title_the_roll_cannot_read_is_due_rather_than_silent(monkeypatch):
    """The direction the design is chosen in. Reading the title is what makes
    a title editable-by-accident, and the two ways to answer an unreadable one
    are not symmetric: *not due* stops the log forever with the workflow
    green, and *due* costs one roll that was not owed. This is the only case
    that pins which way it falls."""
    m = _roller()
    closed, creates = _roll_harness(m, monkeypatch, "chore: measurement log", "0.8.0")

    m.main()

    assert closed == [("example/repo", 89)] and len(creates) == 1, (
        f"a title this script cannot read as its own must roll rather than "
        f"go quiet -- silence here is the failure class #155 is about: "
        f"closed {closed}, created {creates}"
    )


def test_the_nothing_due_line_names_the_log_and_the_version(monkeypatch, capsys):
    """A reader of the workflow log must be able to tell *rolled* from
    *nothing due* without opening GitHub. The job is green either way, so the
    printed line is the only thing that separates a roll that was not owed
    from a mechanism that has quietly stopped."""
    m = _roller()
    _roll_harness(m, monkeypatch, "chore: flow measurement — after 0.7.0", "0.7.0")

    m.main()

    out = capsys.readouterr().out
    assert "nothing due" in out, (
        f"the line must say nothing was due, in those words -- a silent exit "
        f"0 and a stalled mechanism read identically in a workflow log: {out!r}"
    )
    assert "#89" in out and "0.7.0" in out, (
        f"the line must name the log it left alone and the version this tree "
        f"ships, which is the pair a reader checks: {out!r}"
    )


def test_the_rolled_line_names_the_issue_closed_and_the_title_opened(
    monkeypatch, capsys
):
    """The other half of the same requirement."""
    m = _roller()
    _roll_harness(m, monkeypatch, "chore: flow measurement — after 0.7.0", "0.8.0")

    m.main()

    out = capsys.readouterr().out
    assert "rolled" in out, (
        f"the two outcomes must be distinguishable by the first word of the "
        f"line rather than by reading it to the end: {out!r}"
    )
    assert "#89" in out and "after 0.8.0" in out, (
        f"the line must name the issue closed and the title opened: {out!r}"
    )
