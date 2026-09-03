"""Issue #109 part 3: `.github/scripts/roll_flow_measurement_issue.py` closes
the currently-open `flow-measurement` issue and opens the next one, titled
with the version this release just shipped bumped to the next minor. It runs
as a second step in `close-issues-on-release.yml`, on the same trigger and
checkout `close_issues_on_release.py` already uses.

Following `tests/test_release_hygiene.py:225-355`'s `monkeypatch`-on-
`subprocess.run` pattern for that neighbouring script: `next_version` is a
pure function, tested directly with no `gh`/`git` calls; the exactly-one-open
invariant and the retry-once hardening (phase 1's own finding, in the new
module's docstring) are tested by monkeypatching the module's own `run`,
`list_open_issues`, `read_version`, and `time.sleep` -- never the real
network.
"""

import json
import os

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


def test_next_version_bumps_the_minor_and_resets_the_patch():
    m = _roller()
    assert m.next_version("0.7.0") == "0.8.0"
    assert m.next_version("0.7.3") == "0.8.0", (
        "a patch release still bumps the minor -- plan.md's stated default, "
        "not a discovered rule"
    )
    assert m.next_version("1.9.4") == "1.10.0", (
        "the minor is an integer, not a single digit -- string-slicing "
        "instead of parsing would break here"
    )


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
    m.open_issue = lambda repo, version: (
        created.append((repo, version)) or (f"chore: flow measurement — {version}")
    )
    os.environ["REPO"] = "example/repo"
    try:
        m.main()
    finally:
        del os.environ["REPO"]

    assert len(calls) == 2, "a one-open reading on retry must not retry again"
    assert closed == [("example/repo", 89)]
    assert created == [("example/repo", "0.8.0")]


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
    monkeypatch.setattr(m, "run", lambda *a: calls.append(a) or "")
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
    assert title == "chore: flow measurement — 0.8.0", (
        f"the new issue's title is {title!r}, not the next minor version"
    )
    assert "--label" in create_args
    assert create_args[create_args.index("--label") + 1] == "flow-measurement"
    assert "--body" in create_args
    assert create_args[create_args.index("--body") + 1] == "", (
        "the new issue's body must be empty"
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

    def fake_open_issue(repo, version):
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
        assert "0.8.0" in message, (
            f"the failure message must carry the recovery title (the next "
            f"version) so an operator can open the replacement issue by "
            f"hand: {message!r}"
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
