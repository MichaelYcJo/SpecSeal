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
import re
import shlex
import shutil
import subprocess

import pytest
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


def test_the_dirty_tree_row_reads_the_tree_the_switch_is_in(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1 of work item 1790550712, finding 1. The tracked-changes row
    asked `git status` in the session's own directory while every other row
    judged the tree the switch acts on. So a dirty repository reached by `git
    -C` or `cd` from elsewhere was silent, a clean clone switched from a dirty
    session tree was asked about the session tree's changes, and a dirty clone
    switched from a clean session tree was silent. Seen red at 77ad175 on all
    four."""
    outside = tmp_path / "outside"
    outside.mkdir()
    other = tmp_path / "other"
    subprocess.run(
        ["git", "clone", "-q", str(repo), str(other)], check=True, capture_output=True
    )
    (repo / "f.txt").write_text("changed on purpose\n")
    # A force-staged ignored path, which only the target tree's own
    # `check-ignore` can name: `phantom_entries` reads the same tree.
    (repo / ".gitignore").write_text("ign.txt\n")
    (repo / "ign.txt").write_text("x\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-f", "ign.txt"],
        check=True,
        capture_output=True,
    )
    for command in (
        f"git -C {repo} switch feature/x",
        f"cd {repo} && git switch feature/x",
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, outside)
        assert decision == "ask", (command, decision, reason)
        assert "f.txt" in reason, reason
        assert "gitignored path force-staged" in reason, reason
        # Round 2, finding 1: both commands in the note name the tree's root,
        # because the shell is not in that tree and porcelain paths are
        # relative to its root.
        hint = [x.strip() for x in reason.splitlines() if "restore --staged" in x]
        assert hint and hint[0].startswith("git -C "), hint
        assert os.path.samefile(shlex.split(hint[0])[2], repo), hint
        keep = re.search(r"`(git[^`]*) restore <path>`", reason)
        assert keep and keep.group(1).startswith("git -C "), reason
        assert os.path.samefile(shlex.split(keep.group(1))[2], repo), reason
    decision, reason, _ = run(
        monkeypatch, capsys, f"git -C {other} switch feature/x", repo
    )
    assert decision == "silent", (decision, reason)
    (repo / "f.txt").write_text("one\ntwo\nthree\n")
    subprocess.run(
        ["git", "-C", str(repo), "reset", "-q", "ign.txt"],
        check=True,
        capture_output=True,
    )
    (other / "f.txt").write_text("changed in the other clone\n")
    decision, reason, _ = run(
        monkeypatch, capsys, f"git -C {other} switch feature/x", repo
    )
    assert decision == "ask", (decision, reason)
    assert "f.txt" in reason, reason


def test_the_force_staged_check_reads_from_the_root_of_the_tree(
    monkeypatch, capsys, repo
):
    """Round 2 of work item 1790550712, finding 2. `git status --porcelain`
    names paths from the root of the tree, and `git check-ignore` reads a path
    from where it runs. Reached through a subdirectory, the check asked about
    `sub/ign.txt`, and an anchored pattern named nothing. The third cell, a
    session sitting in the subdirectory, missed it before this work item too."""
    (repo / "sub").mkdir()
    (repo / ".gitignore").write_text("/ign.txt\n")
    (repo / "ign.txt").write_text("x\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-f", "ign.txt"],
        check=True,
        capture_output=True,
    )
    for command, cwd in (
        (f"cd {repo / 'sub'} && git switch feature/x", repo),
        (f"git -C {repo / 'sub'} switch feature/x", repo),
        ("git switch feature/x", repo / "sub"),
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, cwd)
        assert decision == "ask", (command, decision, reason)
        assert "gitignored path force-staged" in reason, (command, reason)


# Round 2 of work item 1790550712, finding 1, as a class: every command a
# reason tells the person to run acts on the shell's repository unless it names
# another. Where the tree judged is not the shell's, each one carries `-C` and
# the tree's root; where it is, the text is what it always was.
PRINTED_COMMAND = re.compile(
    r"git(?P<at> -C \S+)? (fetch origin|switch -c <|switch <branch>|worktree add [^`]"
    r"|restore)"
)


def printed_commands(reason):
    return [m for m in PRINTED_COMMAND.finditer(reason)]


def test_every_printed_command_names_the_tree_it_is_about(
    monkeypatch, capsys, repo, tmp_path
):
    """From outside the judged tree, each row that hands the person a command
    names that tree: the switch ladder's ACTIVE deny and idle choice, and the
    creation ladder's single-stream deny and idle choice. From inside it, none
    of them carries `-C`. Seen red before the fix: every command printed from
    outside ran in the shell's own repository, or failed where the shell had
    none."""
    other = tmp_path / "other"
    subprocess.run(["git", "init", "-q", str(other)], check=True, capture_output=True)
    idle = [(222, "/tree", 400.0, 90.0, "Terminal")]
    rows = (
        ("switch", "ACTIVE", (ACTIVE, [], True)),
        ("switch", "idle", ([], idle, True)),
        ("worktree add ../wt f", "single", ([], [], True)),
        ("worktree add ../wt f", "idle", ([], idle, True)),
    )
    for n, (verb, state, sessions) in enumerate(rows):
        tail = "feature/x" if verb == "switch" else ""
        for shell in (other, repo):
            command = f"git -C {repo} {verb} {tail}".rstrip()
            monkeypatch.setattr(wg, "sessions_in_tree", lambda t, o="", s=sessions: s)
            monkeypatch.setattr(
                wg,
                "load_input",
                lambda command=command, shell=shell, n=n: {
                    "tool_name": "Bash",
                    "session_id": f"p{n}-{shell.name}",
                    "tool_input": {"command": command},
                    "cwd": str(shell),
                },
            )
            try:
                wg.main()
            except SystemExit:
                pass
            out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
            reason = out["permissionDecisionReason"]
            found = printed_commands(reason)
            assert found, (verb, state, reason)
            for m in found:
                if shell == repo:
                    assert m.group("at") is None, (verb, state, m.group(0))
                else:
                    assert m.group("at"), (verb, state, m.group(0))
                    assert os.path.samefile(shlex.split(m.group("at"))[1], repo), (
                        m.group(0)
                    )


def test_a_cd_behind_a_redirection_moves_the_tree_the_guard_judges(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of 1790660768. A redirection among a `cd`'s words is the
    shell's, and the switch runs in the tree the `cd` reached. The walk read
    it as an operand or as the program, and the guard judged the clean
    session tree instead of the dirty one the switch lands in -- silent at
    `86256492` and at #674's head. The consent writer filed the creation
    under the session's clone for the same reason."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    for command in (
        "cd w 2>/dev/null && git switch feature/x",
        "2>/dev/null cd w && git switch feature/x",
        "cd>/dev/null w && git switch feature/x",
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, session)
        assert decision == "ask", (command, decision, reason)
        assert "f.txt" in reason, (command, reason)
    acted = wg.worktree_consent.creation_directory(
        "2>/dev/null cd w && git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), acted


def test_a_chain_past_the_walks_cap_keeps_the_tree_the_base_judged(
    monkeypatch, capsys, repo, tmp_path
):
    """Q7 of 1790660768, in the guard. Nine `cd`s landed past their
    redirections carry the walk past `STATE_CAP`, and its collapse left one
    unresolved directory, which the guard reads as the session's own clean
    tree. `86256492`'s walk never reached the cap: every `cd nosuch` fails, so
    the switch runs in the dirty `w`, and that is the tree it judged."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    chain = "2>/dev/null cd nosuch; " * 9 + "cd w && "
    decision, reason, _ = run(
        monkeypatch, capsys, chain + "git switch feature/x", session
    )
    assert decision == "ask", (decision, reason)
    assert "f.txt" in reason, reason
    acted = wg.worktree_consent.creation_directory(
        chain + "git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), acted


def _dirty_nested_session(repo, tmp_path):
    """A clean session repository holding a dirty copy of `repo` at `w`."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    return session


def test_a_skipped_cd_past_the_walks_cap_keeps_the_tree_the_base_judged(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 3 of 1790660768, yellow 1. Past `STATE_CAP` the walk's thread
    collapses, and `cd <missing> ||` then gives it a readable directory on the
    branch the `||` skips. That directory put the walk in front of the base's
    thread, so the guard read the collapsed walk's unresolved directory as the
    session's clean tree, and the consent writer took the skipped branch.
    bash fails every `cd` after `cd w`, so the switch runs in the dirty `w`,
    which is the tree `86256492` judged."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    missing = tmp_path / "nosuch-either"
    chain = "cd w; " + "2>/dev/null cd nosuch; " * 9 + f"cd {missing} || "
    decision, reason, _ = run(
        monkeypatch, capsys, chain + "git switch feature/x", session
    )
    assert decision == "ask", (decision, reason)
    assert "f.txt" in reason, reason
    acted = wg.worktree_consent.creation_directory(
        chain + "git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), acted


# Every way a collapsed walk was measured to regain a readable directory only
# on the branch a `||` skips (#689). `{missing}` is never created and `{other}`
# is a repository of its own. The first four are where bash runs the switch in
# `w`; behind `cd {other} ||` bash runs nothing, and the tree judged is the one
# `86256492` judged.
SKIPPED_PAST_THE_CAP = {
    "behind a redirection the splitter cut": "2>&1 cd {missing} || ",
    "with a redirection after its operand": "cd {missing} 2>&1 || ",
    "landed past a redirection in front": "2>/dev/null cd {missing} || ",
    "into a repository the or-operator skips": "cd {other} || ",
}

# The chains that carry the walk past `STATE_CAP` in front of `cd {missing} ||`.
CAPPING_PREFIXES = {
    "nine failing cds after cd w &&": "cd w && " + "2>/dev/null cd nosuch; " * 9,
    "eight failing cds after cd w;": "cd w; " + "2>/dev/null cd nosuch; " * 8,
}


def _asks_in_w_and_files_under_w(monkeypatch, capsys, session, chain):
    decision, reason, _ = run(
        monkeypatch, capsys, chain + "git switch feature/x", session
    )
    assert decision == "ask", (chain, decision, reason)
    assert "f.txt" in reason, (chain, reason)
    acted = wg.worktree_consent.creation_directory(
        chain + "git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), (chain, acted)


@pytest.mark.parametrize("route", sorted(SKIPPED_PAST_THE_CAP))
def test_every_skipped_branch_past_the_walks_cap_keeps_the_tree_the_base_judged(
    monkeypatch, capsys, repo, tmp_path, route
):
    """#689, the class of round 3's yellow 1: each spelling of a `cd` that a
    collapsed walk lands on the branch the `||` skips. At `542f920b` each one
    led the base's thread, so the guard was silent on the dirty `w` and the
    consent writer filed the creation under the skipped target."""
    session = _dirty_nested_session(repo, tmp_path)
    other = tmp_path / "O"
    other.mkdir()
    subprocess.run(["git", "-C", str(other), "init", "-q"], check=True)
    regain = SKIPPED_PAST_THE_CAP[route].format(
        missing=tmp_path / "nosuch-either", other=other
    )
    chain = "cd w; " + "2>/dev/null cd nosuch; " * 9 + regain
    _asks_in_w_and_files_under_w(monkeypatch, capsys, session, chain)


@pytest.mark.parametrize("prefix", sorted(CAPPING_PREFIXES))
def test_a_skipped_cd_past_the_cap_keeps_the_base_tree_whatever_capped_the_walk(
    monkeypatch, capsys, repo, tmp_path, prefix
):
    """#689, round 3's yellow 1 behind the two other chains its report
    measured: `cd w &&` in front, and eight failing `cd`s where nine is the
    report's own case. Both were silent at `542f920b`."""
    session = _dirty_nested_session(repo, tmp_path)
    chain = CAPPING_PREFIXES[prefix] + f"cd {tmp_path / 'nosuch-either'} || "
    _asks_in_w_and_files_under_w(monkeypatch, capsys, session, chain)


@pytest.mark.parametrize("joined", ["&&", ";", "||"])
def test_a_subshell_behind_a_failing_cd_keeps_the_directory_the_base_named(
    tmp_path, joined
):
    """#689, the same cause with no cap reached. `2>/dev/null cd nosuch ||`
    lands `w/nosuch` on the branch the `||` skips, and the glued `(cd` after
    it is a construct the walk cannot name, so the walk's first directory was
    unresolved and its readable second was that skipped landing. Asking
    whether the walk named ANY readable directory put it first, and the
    creation was filed under `w/nosuch`. bash fails the `cd`, runs the
    subshell, and creates in `w`, which is what `86256492` named."""
    other = tmp_path / "O"
    command = (
        f"cd w; 2>/dev/null cd nosuch || (cd {other}) {joined} git worktree add ../wt"
    )
    acted = wg.worktree_consent.creation_directory(command, str(tmp_path))
    assert os.path.normpath(acted) == str(tmp_path / "w"), acted


def test_past_the_walks_cap_a_cd_landed_past_a_redirection_still_leads(
    monkeypatch, capsys, repo, tmp_path
):
    """#689. What the fix keeps: past `STATE_CAP` a `cd` read past its
    redirections (round 2 of 1790660768) still lands the running shell, so
    the walk's first directory is readable and the walk leads. bash switches
    in `O`, and the guard judges `O`. Putting the base's thread first from
    the walk's first collapse on -- round 3's proposed fix -- sent the guard
    to the dirty `w`, which `86256492` judged because it never read that
    `cd`, and filed `O`'s creation under `w`."""
    session = _dirty_nested_session(repo, tmp_path)
    other = tmp_path / "O"
    shutil.copytree(repo, other)
    chain = "cd w; " + "2>/dev/null cd nosuch; " * 9 + f"2>/dev/null cd {other} && "
    _, _, top = run(monkeypatch, capsys, chain + "git switch feature/x", session)
    assert top and os.path.samefile(top, other), top
    acted = wg.worktree_consent.creation_directory(
        chain + "git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, other), acted
