"""The guard judged the session's cwd, not the tree the command acts on.

`git -C <repo> switch <branch>` names its own repository. The guard resolved
the repository from the session's cwd instead and, when that cwd was not a repo
at all, stood it in for the tree root. With the cwd at a home directory the
containment test in `sessions_in_tree` then matched every Claude session on the
machine, and a single-stream switch was denied by sessions in unrelated
repositories.
"""

import json
import ntpath
import os
import subprocess

from conftest import load_hook_module

wg = load_hook_module("worktree-guard.py", "wg_tree")

ACTIVE = [(111, "/tree", 1.0, 0.5, "VS Code")]


def run(monkeypatch, capsys, command, cwd, sessions=([], [], True)):
    """Run the hook, returning (decision, reason, tree_it_judged)."""
    seen = {}

    def stub(top, own=""):
        seen["top"] = top
        return sessions

    monkeypatch.setattr(wg, "sessions_in_tree", stub)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": "me",
            "tool_input": {"command": command},
            "cwd": str(cwd),
        },
    )
    try:
        wg.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out.strip()
    decision = (
        "silent"
        if not out
        else json.loads(out)["hookSpecificOutput"]["permissionDecision"]
    )
    reason = (
        ""
        if not out
        else json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    )
    return decision, reason, seen.get("top")


# --- the parsing half -----------------------------------------------------


def test_parse_git_reports_the_chdir_it_used_to_only_skip():
    sub, args, chdirs = wg.parse_git(["git", "-C", "/srv/app", "switch", "topic"])
    assert (sub, args) == ("switch", ["topic"])
    assert chdirs == ["/srv/app"], "the value that decides WHICH repo was dropped"


def test_repeated_chdir_composes_like_git_does(tmp_path):
    base = str(tmp_path)
    assert wg.apply_chdir(base, ["a", "b"]) == os.path.join(base, "a", "b")
    absolute = "C:\\abs" if os.name == "nt" else "/abs"
    assert wg.apply_chdir(base, [absolute]) == os.path.normpath(absolute)
    assert wg.apply_chdir(base, []) == os.path.normpath(base)


def test_a_windows_path_survives_tokenizing():
    """POSIX-mode shlex eats `\\`, which is the Windows path separator.

    Run on every platform by asking for the Windows branch explicitly -- the
    failure it guards is invisible on the machines most sessions run on, and
    the value it destroys is the one that decides WHICH repository the command
    acts on. All three quoting forms are here because the fix doubles the
    backslashes before splitting, and single quotes are the form shlex does
    not unescape again.
    """
    for cmd, token in (
        (r"git -C C:\proj\repo switch topic", r"C:\proj\repo"),
        (r'git -C "C:\proj\repo" switch topic', r"C:\proj\repo"),
        (
            r"git -C 'C:\proj\repo' switch topic",
            "C:" + "\\" * 2 + "proj" + "\\" * 2 + "repo",
        ),
    ):
        segments, clean = wg.split_command(cmd, windows=True)
        assert clean, cmd
        _, _, chdirs = wg.parse_git(segments[0])
        assert chdirs == [token], cmd
        # Whatever the form, the path the guard acts on is the real one:
        # ntpath.normpath collapses the doubled separators (measured).
        assert ntpath.normpath(chdirs[0]) == r"C:\proj\repo", cmd


def test_posix_escaping_still_works():
    """The Windows branch is not the default; an escaped space is still one arg."""
    assert wg.split_command(r"git -C /a\ b switch topic", windows=False) == (
        [["git", "-C", "/a b", "switch", "topic"]],
        True,
    )


def test_an_untokenizable_segment_is_not_a_switch():
    """The splitter reports what it managed to read and says it gave up.
    `git switch "unclosed` yields a `switch` with no target, which is not a
    branch change."""
    segments, clean = wg.split_command('git switch "unclosed')
    assert clean is False
    assert wg.classify(segments[0], "") is None


def test_segment_cwd_leaves_a_non_git_segment_alone(tmp_path):
    assert wg.segment_cwd(["echo", "hello"], str(tmp_path)) == str(tmp_path)


def test_classify_follows_the_chdir_when_resolving_a_ref(repo, tmp_path):
    """`-C` decides which repo holds the branch name being checked out."""
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(repo), str(clone)], check=True)
    subprocess.run(
        ["git", "-C", str(clone), "branch", "-Dq", "feature/x"], capture_output=True
    )
    segments, _ = wg.split_command(f"git -C {clone} checkout feature/x")
    assert wg.classify(segments[0], str(outside)) == "switch", (
        "the ref lives in the -C repo; resolving it against the cwd finds nothing"
    )


def test_a_windows_cd_path_is_not_mistaken_for_an_expansion():
    """A `cd` argument is the same kind of value as a `-C` one and arrives the
    same way, so it goes through the same adapter.

    POSIX-mode shlex reads `\\` as an escape and the guard doubles the
    backslashes before splitting to hand them back. The reader must then not
    treat what comes out as a destination it cannot compute — the characters
    it refuses are the ones that name a value or a set of paths (`$`, a glob),
    and a path separator is neither.
    """
    for cmd in (
        r"cd C:\proj\repo && git switch topic",
        r'cd "C:\proj\repo" && git switch topic',
    ):
        items, clean = wg._tokenize_with_separators(cmd, windows=True)
        assert clean, cmd
        assert items[0][1][0] == "cd", cmd
        assert ntpath.normpath(items[0][1][1]) == r"C:\proj\repo", cmd
        walked = wg.walk_command(cmd, r"C:\start", windows=True)
        where = walked[1][1][0]
        assert not isinstance(where, wg.cmdline.Unresolved), cmd


# --- the decision half ----------------------------------------------------


def test_the_tree_judged_is_the_one_the_command_names(
    monkeypatch, capsys, repo, tmp_path
):
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    _, _, top = run(monkeypatch, capsys, f"git -C {repo} switch feature/x", outside)
    # One spelling on both sides: git answers with forward slashes on Windows.
    expected = {os.path.normpath(str(repo)), os.path.normpath(os.path.realpath(repo))}
    assert top in expected, f"judged {top!r}; the command acts on {str(repo)!r}"


def test_a_cwd_that_is_no_repo_is_not_a_tree(monkeypatch, capsys, tmp_path):
    """The measured false deny: cwd stood in for the tree root.

    Every session on the machine sits under a home directory, so `startswith`
    matched all of them and an active one denied the switch.
    """
    outside = tmp_path / "not-a-repo"
    outside.mkdir()
    decision, _, top = run(
        monkeypatch,
        capsys,
        "git switch feature/x",
        outside,
        sessions=(ACTIVE, [], True),
    )
    assert decision == "silent", (
        "with no repository there is nothing to keep two sessions out of"
    )
    assert top is None, "session detection ran against a directory that is not a tree"


def test_a_cd_moves_the_tree_the_guard_judges(monkeypatch, capsys, repo, tmp_path):
    """S10. The rider being discharged named both gates, and the parsing is
    shared: a session that walks to another repository and switches a branch
    there was judged against the tree it started in.

    That is the shape a session takes the moment this very guard refuses a
    `git switch` and tells the user to work in a separate worktree. The
    session stays where it was; the commands do not.
    """
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    _, _, top = run(monkeypatch, capsys, f"cd {repo} && git switch feature/x", outside)
    expected = {os.path.normpath(str(repo)), os.path.normpath(os.path.realpath(repo))}
    assert top in expected, f"judged {top!r}; the command switches in {str(repo)!r}"


def test_a_cd_moves_the_tree_even_when_the_session_sits_in_a_repository(
    monkeypatch, capsys, repo, tmp_path
):
    """S10 in the shape `spec.md` states it: "the session sits in `A`".

    The case above seats the session in a directory that is no repository, so
    the pre-fix failure there is `top is None` — the guard finding nothing at
    all. That does not distinguish "judged the wrong tree" from "judged
    nothing", and the wrong tree is the defect. Here the session sits in a
    real repository, so a guard that ignores the `cd` judges THAT one and the
    assertion has something to be wrong about.
    """
    other = tmp_path / "other"
    subprocess.run(["git", "init", "-q", str(other)], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(other),
            "-c",
            "user.email=e@example.com",
            "-c",
            "user.name=e",
            "commit",
            "-qm",
            "base",
            "--allow-empty",
        ],
        check=True,
        capture_output=True,
    )
    _, _, top = run(monkeypatch, capsys, f"cd {other} && git switch -c f", repo)
    expected = {os.path.normpath(str(other)), os.path.normpath(os.path.realpath(other))}
    assert top in expected, (
        f"judged {top!r}; the command switches in {str(other)!r}, and the "
        f"session's own repository is {str(repo)!r}"
    )


def test_a_cd_to_no_repository_leaves_the_guard_judging_its_own_tree(
    monkeypatch, capsys, repo, tmp_path
):
    """A regression this work introduced: the parent denied, the fix that followed was silent.

    A `cd` whose destination reads cleanly but holds no repository sent the
    guard to `if not top: sys.exit(0)`. With `;` the failing `cd` does not
    stop what follows — it runs in the session's own tree, which is exactly
    the tree another session may be sitting in.

    The commit gate STOPS on a target like this and this guard falls back
    instead, because the two protect different things: a commit nobody judged
    is a commit nobody reviewed, while going silent here leaves a shared tree
    unguarded. A `-C` keeps today's silence — git itself refuses that one, and
    the case below pins it.
    """
    plain = tmp_path / "plain"
    plain.mkdir()
    for command in (
        f"cd {plain} ; git switch feature/x",
        f"cd {plain} && git switch feature/x",
        "cd /no/such/dir ; git switch feature/x",
    ):
        decision, _, top = run(
            monkeypatch, capsys, command, repo, sessions=(ACTIVE, [], True)
        )
        assert decision == "deny", command
        expected = {
            os.path.normpath(str(repo)),
            os.path.normpath(os.path.realpath(repo)),
        }
        assert top in expected, command


def test_a_relative_chdir_option_composes_onto_the_cd_destination(
    monkeypatch, capsys, repo, tmp_path
):
    """`cd ~/projects && git -C myrepo switch main` — the ordinary shape.

    The fallback for a destination holding no repository ran BEFORE the
    segment's own `-C` was applied, so it threw the destination away and
    composed the relative `-C` onto the session directory instead. A real
    target repository became a path that does not exist, and the guard exited
    at `if not top`.

    The order is what fixes it: compose first, and only fall back when the
    composed directory holds no repository either. The parent directory here
    is deliberately NOT a repository, which is what makes the fallback fire.
    """
    outer = tmp_path / "outer"
    inner = outer / "myrepo"
    inner.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(inner)], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(inner),
            "-c",
            "user.email=e@example.com",
            "-c",
            "user.name=e",
            "commit",
            "-qm",
            "base",
            "--allow-empty",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(inner), "branch", "other"], check=True, capture_output=True
    )

    _, _, top = run(
        monkeypatch, capsys, f"cd {outer} && git -C myrepo switch other", repo
    )
    expected = {os.path.normpath(str(inner)), os.path.normpath(os.path.realpath(inner))}
    assert top in expected, (
        f"judged {top!r}; the switch happens in {str(inner)!r}, which the "
        f"relative -C names from the cd destination"
    )


def test_a_subshell_checkout_resolves_the_branch_it_names(repo, tmp_path):
    """The residual round 1 left: a closing parenthesis rides on the BRANCH.

    `(git checkout feature/x)` asks about a branch called `feature/x)`, which
    resolves to nothing, so the guard classified it as no branch change at
    all. The retry happens only AFTER the name as written fails to resolve, so
    a branch that genuinely ends in a parenthesis still answers first.
    """
    segments, _ = wg.split_command("(git checkout feature/x)")
    assert wg.classify(segments[0], str(repo)) == "switch"

    subprocess.run(["git", "-C", str(repo), "branch", "odd)"], capture_output=True)
    segments, _ = wg.split_command("git checkout odd)")
    assert wg.classify(segments[0], str(repo)) == "switch", (
        "a branch whose name really ends in a parenthesis has to answer first"
    )


def test_a_branch_ending_in_a_parenthesis_answers_inside_a_subshell_too(repo):
    """Round 2 stripped every trailing parenthesis at once, so the property it
    was asked for held only outside a subshell.

    With a branch really called `weird)`, `git checkout weird)` classified and
    `(git checkout weird))` went silent — one parenthesis too many was taken
    off and the ref lookup missed. They are peeled one at a time now, so the
    longest name that resolves answers first.
    """
    subprocess.run(["git", "-C", str(repo), "branch", "weird)"], capture_output=True)
    for command in ("git checkout weird)", "(git checkout weird))"):
        segments, _ = wg.split_command(command)
        assert wg.classify(segments[0], str(repo)) == "switch", command


def test_a_file_restore_inside_a_subshell_stays_silent(repo):
    """The other side of peeling: restoring a file is not a branch change, in
    any of the three shapes."""
    for command in (
        "(git checkout README.md)",
        "(git checkout -- README.md)",
        "(git checkout .)",
    ):
        segments, _ = wg.split_command(command)
        assert wg.classify(segments[0], str(repo)) is None, command


def test_the_retry_token_survives_a_closing_parenthesis(repo):
    """A consent read that the judgment read can reach past.

    The judgment read strips a subshell opener, so a creation command inside
    parentheses now classifies — and `has_token` did not strip anything, so
    the token written at the end of that command carried the closing
    parenthesis and matched nothing. Creation is the one verdict in this guard
    with no `ask` behind it, which makes an unreadable token an inescapable
    loop rather than an extra prompt.
    """
    inside = "(git worktree add ../wt f [worktree-ok])"
    assert wg.has_token(inside, "[worktree-ok]")
    assert wg.has_token("git switch x [shared-tree-ok])", "[shared-tree-ok]")
    assert not wg.has_token("echo nothing here", "[worktree-ok]")


def test_the_repository_lookup_cannot_hang_the_gate(repo):
    """A shape check, and labelled as one: no unresponsive mount was mounted.

    `repo_paths` shells out to git once per candidate directory, and the
    reader can hand it several. The same species of call in `hooks/optin.py`
    carries `timeout=5` for a reason recorded there. A hook that never returns
    is a hook that never decides.
    """
    import inspect

    source = inspect.getsource(wg.repo_paths)
    assert "timeout=" in source, (
        "the git lookup has no timeout, so an unresponsive path hangs the hook"
    )


def test_a_chdir_option_to_no_repository_stays_silent(monkeypatch, capsys, repo):
    """The other half of the case above, so the fallback cannot widen quietly.

    `git -C <nowhere> switch` fails in git before it touches any tree, so
    there is nothing to protect and the guard says nothing — its answer at
    before this change and the one it keeps.
    """
    decision, _, _ = run(
        monkeypatch,
        capsys,
        "git -C /no/such/dir switch feature/x",
        repo,
        sessions=(ACTIVE, [], True),
    )
    assert decision == "silent"


def test_a_cd_the_guard_cannot_read_leaves_it_judging_its_own_tree(
    monkeypatch, capsys, repo, tmp_path
):
    """The commit gate stops on a destination it cannot compute, because a
    silent commit is one nobody reviewed. This guard has no such answer to
    give: what it protects is a tree two sessions would share, and with the
    destination unknown the session's own tree is the one still known to be
    shared. Going silent there would be a fail-open, so it keeps today's
    answer rather than acquiring a second stop.
    """
    decision, _, top = run(
        monkeypatch,
        capsys,
        'cd "$WT" && git switch feature/x',
        repo,
        sessions=(ACTIVE, [], True),
    )
    expected = {os.path.normpath(str(repo)), os.path.normpath(os.path.realpath(repo))}
    assert top in expected
    assert decision == "deny"


def test_an_active_session_in_the_named_tree_still_denies(
    monkeypatch, capsys, repo, tmp_path
):
    """The fix must not cost the guard its actual job."""
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    decision, reason, _ = run(
        monkeypatch,
        capsys,
        f"git -C {repo} switch feature/x",
        outside,
        sessions=(ACTIVE, [], True),
    )
    assert decision == "deny"
    assert "VS Code" in reason


# --- the commit gate's other answer ---------------------------------------


def test_the_commit_gate_says_what_declining_does(tmp_path):
    """A hook returns allow/deny/ask; declining renders as a bare No.

    The reason string is the only place that can give the decline a
    destination, and `implement` §1 rejects a question whose no leads nowhere.
    """
    from conftest import run_hook

    repo = tmp_path / "repo"
    (repo / "seal").mkdir(parents=True)
    git = lambda *a: subprocess.run(
        ["git", "-C", str(repo), *a], capture_output=True, check=True
    )
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / "f.py").write_text("x = 1\n")
    git("add", "-A")
    git("-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "base")
    (repo / "f.py").write_text("x = 2\n")
    git("add", "-A")

    out = run_hook(
        "commit-review-gate.py",
        {
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'change'"},
            "cwd": str(repo),
        },
    )
    d = json.loads(out)["hookSpecificOutput"]
    assert d["permissionDecision"] == "ask"
    reason = d["permissionDecisionReason"]
    assert "Approving is the waiver" in reason
    assert "Declining cancels the commit" in reason, (
        "the decline branch has no text of its own, so it reads as a dead end"
    )
    assert "[no-review]" in reason and "review chain" in reason, (
        "both continuations have to be named, or the prompt is a yes/no"
    )
