"""The guard judged the session's cwd, not the tree the command acts on.

`git -C <repo> switch <branch>` names its own repository. The guard resolved
the repository from the session's cwd instead and, when that cwd was not a repo
at all, stood it in for the tree root. With the cwd at a home directory the
containment test in `sessions_in_tree` then matched every Claude session on the
machine, and a single-stream switch was denied by sessions in unrelated
repositories.
"""

import importlib.util
import json
import ntpath
import os
import re
import shlex
import shutil
import subprocess
import sys

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
    (repo / "f.py").write_text("x = 1\n", encoding="utf-8")
    git("add", "-A")
    git("-c", "user.email=e@example.com", "-c", "user.name=e", "commit", "-qm", "base")
    (repo / "f.py").write_text("x = 2\n", encoding="utf-8")
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
    (repo / "f.txt").write_text("changed on purpose\n", encoding="utf-8")
    # A force-staged ignored path, which only the target tree's own
    # `check-ignore` can name: `phantom_entries` reads the same tree.
    (repo / ".gitignore").write_text("ign.txt\n", encoding="utf-8")
    (repo / "ign.txt").write_text("x\n", encoding="utf-8")
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
    (repo / "f.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(repo), "reset", "-q", "ign.txt"],
        check=True,
        capture_output=True,
    )
    (other / "f.txt").write_text("changed in the other clone\n", encoding="utf-8")
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
    (repo / ".gitignore").write_text("/ign.txt\n", encoding="utf-8")
    (repo / "ign.txt").write_text("x\n", encoding="utf-8")
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


def test_a_cd_behind_a_redirection_leaves_the_guard_on_the_tree_the_base_judged(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of 1790660768 made the guard judge the tree a `cd` behind a
    redirection reaches, and #689 took that back: the guard and the consent
    writer read through `hooks/cmdline_base.py`, which is `86256492`'s reader,
    and that reader does not land these `cd`s. So the guard judges the clean
    session tree and is silent, and the consent writer files the creation
    under the session's clone, while bash runs both in the dirty `w`. That is
    the containment's accepted cost, recorded in #689's spec. The commit gate
    still lands each `cd` (`test_no_shape_the_base_stops_reads_silent.py`).

    Changed by #689 rather than deleted. It asserted `ask` naming `f.txt`,
    and the consent writer filing under `w`; at the containment it failed on
    the first command with `silent`, the answer `86256492` gives."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n", encoding="utf-8")
    for command in (
        "cd w 2>/dev/null && git switch feature/x",
        "2>/dev/null cd w && git switch feature/x",
        "cd>/dev/null w && git switch feature/x",
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, session)
        assert decision == "silent", (command, decision, reason)
    acted = wg.worktree_consent.creation_directory(
        "2>/dev/null cd w && git worktree add ../wt", str(session)
    )
    assert os.path.normpath(acted) == str(session), acted


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
    (session / "w" / "f.txt").write_text("changed on purpose\n", encoding="utf-8")
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


# --- #689: the guard and the consent writer read the base's directories ---
#
# Each chain below is one where the order of the walk's two threads decided
# the tree, and every attempt to order them was met by another chain (#689).
# The guard and the consent writer now read through `hooks/cmdline_base.py`,
# `86256492`'s reader frozen, so each judges the tree `86256492` judged,
# which is the dirty `w` bash runs the command in. `{missing}` is never
# created and `{other}` is a clean repository of its own.
BASE_TREE_CHAINS = {
    # Round 3 of #689's report: past `STATE_CAP` the walk collapses, and the
    # `cd {missing} ||` gives it a readable directory on the branch the `||`
    # skips, which led the base's thread.
    "the round-3 chain past the cap": "cd w; "
    + "2>/dev/null cd nosuch; " * 9
    + "cd {missing} || ",
    # PR #690's residuals. A `cd` landed past its redirection into a directory
    # that does not exist led, so the guard found no repository there and
    # fell back to the clean session tree.
    "a landing into a missing directory, then a semicolon": "cd w; "
    "2>/dev/null cd {missing}; ",
    "a glued landing into nothing, then one into a repository": "cd w; "
    "cd>/dev/null {missing} && 2>/dev/null cd {other}\n",
}


def _a_dirty_w_under_a_clean_session(repo, tmp_path):
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n", encoding="utf-8")
    shutil.copytree(repo, session / "clean")
    other = tmp_path / "O"
    shutil.copytree(repo, other)
    return session, other


@pytest.mark.parametrize("name", sorted(BASE_TREE_CHAINS))
def test_the_guard_judges_the_tree_the_base_judged_whatever_the_walk_leads(
    monkeypatch, capsys, repo, tmp_path, name
):
    """#689. At `542f920b` each chain was silent: the walk's directory led the
    base's, and it was either a directory the `||` skips or one the `cd`
    never reached. `86256492` asked about the dirty `w`, and so does this."""
    session, other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    chain = BASE_TREE_CHAINS[name].format(
        missing=tmp_path / "nosuch-either", other=other
    )
    decision, reason, top = run(
        monkeypatch, capsys, chain + "git switch feature/x", session
    )
    assert decision == "ask", (name, decision, reason)
    assert "f.txt" in reason, (name, reason)
    assert top and os.path.samefile(top, session / "w"), (name, top)


@pytest.mark.parametrize("name", sorted(BASE_TREE_CHAINS))
def test_the_consent_writer_files_where_the_base_filed_whatever_the_walk_leads(
    repo, tmp_path, name
):
    """#689, the consent twin. At `542f920b` the writer filed each creation
    under the walk's first directory, the skipped or unreached one; bash
    creates from `w`, and `86256492` filed it there."""
    session, other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    chain = BASE_TREE_CHAINS[name].format(
        missing=tmp_path / "nosuch-either", other=other
    )
    acted = wg.worktree_consent.creation_directory(
        chain + "git worktree add ../wt", str(session)
    )
    assert os.path.normpath(acted) == str(session / "w"), (name, acted)


def test_a_segment_only_the_reading_past_redirections_finds_is_not_git_to_the_guard(
    monkeypatch, capsys, repo, tmp_path
):
    """#689. `2>/dev/null nice -n 5 git switch` is git only to the reading
    past redirections (#674). The guard reads through `86256492`'s frozen
    reader, which finds no git there, so it judges no tree, while bash
    switches `w`. That is the accepted cost of reading as the base read, the
    same one a `cd` behind a redirection pays.

    Changed by round 1 of 1790745049 rather than deleted. It asserted `ask`
    about `w`, which the build's `base_directories` gave by placing the
    segment where the wider reading unplaced it; `86256492` gives `silent`.

    Changed again by phase 4 of 1790993140 (#678's guard half). The frozen
    reader still judges no tree (`top` stays None), and the guard now puts the
    switch it could not read to the person instead of passing it silently."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, top = run(
        monkeypatch,
        capsys,
        "cd w && 2>/dev/null nice -n 5 git switch feature/x",
        session,
    )
    assert decision == "ask", (decision, reason)
    assert top is None, top


# A segment only #674's reading reads as git, in FRONT of one `86256492` read
# (round 1 of 1790745049, red 1). The guard takes the first segment of each
# kind, so while it read with #674's `parse_git` the wider segment took the
# place of the one the base judged. An ACTIVE session sits in any tree the
# stub is asked about, so `top` is what tells the two apart.
WIDER_FIRST = (
    "2>/dev/null git switch feature/x; cd w && git switch feature/x",
    "git 2>/dev/null switch feature/x; cd w && git switch feature/x",
    "nocorrect git switch feature/x; cd w && git switch feature/x",
    "repeat 1 git switch feature/x; cd w && git switch feature/x",
    "cd clean && 2>/dev/null git switch feature/x; cd ../w && git switch feature/x",
)


@pytest.mark.parametrize("command", WIDER_FIRST)
def test_a_segment_the_base_reads_no_git_in_does_not_take_the_first_slot(
    monkeypatch, capsys, repo, tmp_path, command
):
    """Round 1 of 1790745049, red 1. bash switches `w`, and `86256492` denied
    each command over the session active in `w`. At `4bc94f05` the first
    segment took the slot and the guard judged the session's own tree."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    active = [(111, str(session / "w"), 1.0, 0.5, "VS Code")]
    decision, reason, top = run(
        monkeypatch, capsys, command, session, sessions=(active, [], True)
    )
    assert decision == "deny", (command, decision, reason)
    assert top and os.path.samefile(top, session / "w"), (command, top)


def test_the_consent_writer_files_the_creation_the_base_filed_behind_a_wider_one(
    repo, tmp_path
):
    """Round 1 of 1790745049, red 1, the consent twin. `86256492` filed under
    `w`; at `4bc94f05` the first creation, which it did not read as git, was
    filed under the session's clone."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    acted = wg.worktree_consent.creation_directory(
        "2>/dev/null git worktree add ../wt-a; cd w && git worktree add ../wt-b",
        str(session),
    )
    assert os.path.normpath(acted) == str(session / "w"), acted


# zsh's precommand words and short loop in front of git (round 1 of
# 1790745049, yellow 2). #674's `command_word` reads them as runners, so the
# build read each as git with an unresolved directory; `86256492` read none of
# them as git.
ZSH_PREFIXED = (
    "cd w && repeat 2 git {verb}",
    "cd w && for i (1) git {verb}",
    "cd w && noglob git {verb}",
    "cd w && nocorrect git {verb}",
    # Round 2 of 1790745049, white 3: `542f920b`'s guard read `foreach` too.
    "cd w && foreach i (1) git {verb}; end",
)


@pytest.mark.parametrize("shape", ZSH_PREFIXED)
def test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer(
    monkeypatch, capsys, repo, tmp_path, shape
):
    """Round 1 of 1790745049, yellow 2. The guard does not judge the tree,
    and the consent writer files nothing, as at `86256492`. At `4bc94f05` the
    guard judged the session's tree and denied, and the writer filed the
    creation under the session's clone.

    Changed by phase 4 of 1790993140 (#678's guard half): it asserted
    `silent` over the ACTIVE session; the guard now asks about the switch it
    could not read, without judging any tree. The writer's half is unchanged."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    active = [(111, str(session / "w"), 1.0, 0.5, "VS Code")]
    decision, reason, _ = run(
        monkeypatch,
        capsys,
        shape.format(verb="switch feature/x"),
        session,
        sessions=(active, [], True),
    )
    assert decision == "ask", (shape, decision, reason)
    acted = wg.worktree_consent.creation_directory(
        shape.format(verb="worktree add ../wt"), str(session)
    )
    assert acted == "", (shape, acted)


# --- #686 and #678's guard half, decided by a count ------------------------
#
# Both were built in phase 2 of work item 1790993140 and counted in phase 3
# over the recorded runs; phase 4 wired or removed each by that count, under
# the owner's rule of 2026-10-03. #686's ask fired on 9 recorded pairs and was
# removed, so its fallback is a known limit. #678's fired on none and is wired.

SWITCH = "git switch feature/x"

# #686's seven: a `cd` the frozen walk cannot follow, or follows confidently
# to the wrong place, before the switch. bash switches the dirty `w`; the
# guard judges the clean session tree and says nothing.
UNPLACED = {
    "builtin cd": f"builtin cd w && {SWITCH}",
    "command cd": f"command cd w && {SWITCH}",
    "time cd": f"time cd w && {SWITCH}",
    "pushd": f"pushd w && {SWITCH}",
    "noglob cd": f"noglob cd w && {SWITCH}",
    "cd to an unset variable": f'cd "$W" && {SWITCH}',
    "2>&1 cd": f"2>&1 cd w && {SWITCH}",
}


@pytest.mark.parametrize("name", sorted(UNPLACED))
def test_a_switch_tree_the_guard_cannot_place_is_judged_as_its_own(
    monkeypatch, capsys, repo, tmp_path, name
):
    """`docs/worktree-guard-spec.md` §*Known limits*: asking here would have
    stopped 9 of the 27,351 recorded command and directory pairs, so the
    fallback stays (phase 3 of work item 1790993140). Seen red against a
    mutant whose last silent exit asks."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, _ = run(monkeypatch, capsys, UNPLACED[name], session)
    assert decision == "silent", (name, decision, reason)


WIDER_ONLY = {
    "git 2>&1 worktree add": ("cd w && git 2>&1 worktree add ../wt b", "creation"),
    "--config-env, a creation": (
        "git --config-env k=v worktree add ../wt b",
        "creation",
    ),
    "2>/dev/null nice -n 5 git switch": (
        f"cd w && 2>/dev/null nice -n 5 {SWITCH}",
        "switch",
    ),
    "--config-env, a switch": ("git --config-env k=v switch x", "switch"),
    # Round 2 of 1790993140: a redirection glued to the subcommand's end.
    # bash runs each (executed by the round); the frozen parser reads
    # `switch>/dev/null` as no subcommand, and only the cut view reads the
    # kind. Silent at `f1629706`, where the cut view was compared with the
    # frozen parser.
    "a redirection glued to switch": (
        "cd w && git switch>/dev/null feature/x",
        "switch",
    ),
    "a redirection glued to checkout": (
        "cd w && git checkout>/dev/null -b y",
        "switch",
    ),
    "a redirection glued to add": (
        "cd w && git worktree add>/dev/null ../wt b",
        "creation",
    ),
    # #737. The splitter cuts `&>` at `&`, and only the merged view holds the
    # switch; bash runs each (executed). A mutant comparing the merged view
    # with itself is silent on both.
    "&> between switch and its name": (
        "cd w && git switch &>/dev/null feature/x",
        "switch",
    ),
    "&> between checkout and its name": (
        "cd w && git checkout &>/dev/null feature/x",
        "switch",
    ),
    # #737. bash runs it as a creation (executed); silent at `2b1dcb1f`,
    # where `2>/dev/null` was read as `worktree`'s first positional.
    "a redirection between worktree and add": (
        "cd w && git worktree 2>/dev/null add ../wt b",
        "creation",
    ),
    **{
        f"zsh: {shape.split('&& ')[1]}": (
            shape.format(verb="switch feature/x"),
            "switch",
        )
        for shape in ZSH_PREFIXED
    },
}


@pytest.mark.parametrize("name", sorted(WIDER_ONLY))
def test_candidate_c_finds_what_only_the_wider_reading_finds(tmp_path, name):
    command, kind = WIDER_ONLY[name]
    assert wg.wider_only_kinds(command, str(tmp_path)) == {kind}, name


@pytest.mark.parametrize("command", [*WIDER_FIRST, SWITCH, "git worktree add ../wt b"])
def test_candidate_c_reports_nothing_the_frozen_reading_found(tmp_path, command):
    assert wg.wider_only_kinds(command, str(tmp_path)) == set(), command


@pytest.mark.parametrize("name", sorted(WIDER_ONLY))
def test_what_only_the_wider_reading_finds_is_put_to_the_person(
    monkeypatch, capsys, repo, tmp_path, name
):
    """#678's guard half, wired. Each was silent at `233f0455`, and seen red
    against a mutant whose silent exits skip the question."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    command, kind = WIDER_ONLY[name]
    decision, reason, top = run(monkeypatch, capsys, command, session)
    assert decision == "ask", (name, decision, reason)
    assert "does not read" in reason, reason
    assert ("switches a branch" in reason) == (kind == "switch"), reason
    assert ("creates a worktree" in reason) == (kind == "creation"), reason
    assert top is None, top


@pytest.mark.parametrize(
    "name", sorted(k for k, (_c, kind) in WIDER_ONLY.items() if kind == "creation")
)
def test_a_creation_only_the_wider_reading_finds_is_silent_under_consent(
    monkeypatch, capsys, repo, tmp_path, name
):
    """`questions.md` D10: consent is read first, as for every creation."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    assert wg.worktree_consent.record(str(session), "me")
    decision, reason, _ = run(monkeypatch, capsys, WIDER_ONLY[name][0], session)
    assert decision == "silent", (name, decision, reason)


def test_the_question_names_both_kinds_and_says_it_in_korean(
    monkeypatch, capsys, repo, tmp_path
):
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    command = "2>/dev/null git switch x; git 2>&1 worktree add ../wt b"
    _, reason, _ = run(monkeypatch, capsys, command, session)
    assert "switches a branch and creates a worktree" in reason, reason
    monkeypatch.setattr(wg, "LANG", "ko")
    _, reason, _ = run(monkeypatch, capsys, command, session)
    assert "브랜치 전환·worktree 생성은 이 guard 가 읽지 않는 모양" in reason, reason


@pytest.mark.parametrize(
    "first", ["git checkout README.md && ", "git checkout nosuch; "]
)
def test_a_restore_before_a_hidden_switch_does_not_silence_the_question(
    monkeypatch, capsys, repo, tmp_path, first
):
    """Round 1 of 1790993140, yellow 3. `classify` reads `git checkout
    README.md`, and a checkout of no ref, as no switch, so the frozen loop
    judged no switch, and the switch behind the redirection is still put to
    the person. Silent at `07a3dc7f`, where the restore's words alone took the
    switch kind out."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    command = f"{first}cd w && 2>/dev/null {SWITCH}"
    decision, reason, top = run(monkeypatch, capsys, command, session)
    assert decision == "ask", (decision, reason)
    assert "switches a branch" in reason, reason
    assert top is None, top


@pytest.mark.parametrize(
    "command",
    [
        "cd w && git checkout . &>/dev/null",
        "cd w && git checkout .&>/dev/null",
        "cd w && git checkout -q &>/dev/null",
        "cd w && git switch --detach &>/dev/null",
        "cd w && git switch --detach>/dev/null",
        "cd w && git checkout>/dev/null .",
    ],
)
def test_a_redirection_word_is_not_read_as_a_branch_name(
    monkeypatch, capsys, repo, tmp_path, command
):
    """#737. A cut or merged view carries a redirection word its segments do
    not, and `switch_kind` reads any word as a name, so each of these asked
    *switches a branch* at `2b1dcb1f`. bash runs each as a restore or a
    detach (executed), and `233f0455` asked none of them."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, _ = run(monkeypatch, capsys, command, session)
    assert decision == "silent", (command, decision, reason)


def _redirections():
    """Every redirection `hooks/cmdline.py`'s `_REDIRECTION` names, as (operator,
    target) pairs, each operator once bare and, where it is not `&`-led, with
    a number and with bash 4.1's `{fd}` in front. Derived from the pattern, so
    an operator the reader learns is a new case the day it is added."""
    pattern = wg.wide._REDIRECTION.pattern
    assert pattern.endswith(")"), pattern
    operators = pattern[pattern.rindex("(?:") + 3 : -1]
    pairs = []
    for op in (o.replace("\\", "") for o in re.split(r"(?<!\\)\|", operators)):
        target = {"<<<": "word", "<<": "EOF", "<<-": "EOF"}.get(op, "/dev/null")
        if op.endswith("&"):
            target = "1"
        fds = [""] if op.startswith("&") else ["", "2", "{fd}"]
        pairs += [(fd + op, target) for fd in fds]
    return pairs


def test_the_redirections_are_read_from_the_reader():
    """The generator below is only as wide as this list."""
    ops = {op for op, _target in _redirections()}
    assert {"&>", "&>>", ">&", "<&", "2>", "{fd}>", "<<<", ">|", ">!"} <= ops, ops
    assert len(ops) == 2 + 12 * 3, sorted(ops)


RESTORES = (
    "checkout .",
    "checkout -- README.md",
    "checkout -q",
    "switch --detach",
    "worktree list",
)


def _placed(verb):
    """`git <verb>` with every redirection `_redirections` gives, at every
    position, glued to the word before it and spaced, its target glued and
    spaced -- as `(command, at, glued, operator)`, where `at` is the index of
    the word of `git <verb>` the redirection stands before.

    A number or a `{fd}` is a descriptor only as a word of its own, so those
    are spaced: glued, bash hands it to git inside the word before
    (`--2>&1` is the option `--2`), which is another verb."""
    words = ["git", *verb.split()]
    for op, target in _redirections():
        gluable = not op[0].isdigit() and not op.startswith("{")
        for at in range(len(words) + 1):
            for glued in (False, True) if at and gluable else (False,):
                for spaced_target in (False, True):
                    redirection = op + (" " if spaced_target else "") + target
                    head = " ".join(words[:at])
                    tail = " ".join(words[at:])
                    joint = "" if glued else " "
                    command = (head + joint + redirection).lstrip()
                    command = (command + " " + tail).rstrip()
                    if target == "EOF":
                        command += "\nEOF"
                    yield command, at, glued, op


def _shapes(verb):
    """The commands `_placed` builds, without where each redirection stands."""
    for command, _at, _glued, _op in _placed(verb):
        yield command


def test_no_restore_is_asked_whatever_the_redirection_and_wherever_it_stands(
    tmp_path,
):
    """#737, S4. For every operator `_REDIRECTION` names, at every position, glued
    to the word before it and spaced, its target glued and spaced, a verb that
    switches nothing is no kind to the wider reading. Red at `2b1dcb1f`."""
    asked = []
    for verb in RESTORES:
        for command in _shapes(verb):
            kinds = wg.wider_only_kinds(command, str(tmp_path))
            if kinds:
                asked.append((command, kinds))
    assert not asked, (len(asked), asked[:10])


def _policy_text():
    """`docs/worktree-guard-spec.md`, whitespace folded so a wrapped sentence
    reads as one line."""
    path = os.path.join(
        os.path.dirname(__file__), "..", "docs", "worktree-guard-spec.md"
    )
    with open(path, encoding="utf-8") as f:
        return " ".join(f.read().split())


# The rule §*Which tree* states for candidate C, in its own words (round 2 of
# #737): a list of positions was wrong in each of two rounds, so the sentence
# states the condition, and the case below checks the condition.
POLICY_RULE = (
    "the guard asks wherever a view's words hold a switch or a creation that "
    "none of the frozen segments the view was made from holds"
)

# Verbs whose words read as a switch or a creation, each a restore or a
# detach among them where the tree decides: the rule asks them whenever the
# frozen reading misses them.
ASKABLE = (
    "switch feature/x",
    "switch --detach feature/x",
    "checkout README.md",
    "checkout -b y",
    "worktree add ../wt b",
)


def test_every_shape_the_wider_reading_asks_is_one_the_policy_rule_covers(
    tmp_path,
):
    """Round 2 of #737. Over the generated shapes, every kind
    `wider_only_kinds` asks is the kind the verb's own words hold, read with
    no redirection, and one none of the frozen segments of the command as
    written holds. Checked by that condition, never by a list of shapes, so
    the policy's rule and the code cannot drift apart a position at a time.
    Red against the round-1 sentence, which listed positions. The frozen half
    is read from the wider splitter's segments with nothing subtracted first,
    so it fails where the per-view subtraction is dropped (round 3 of #737,
    white 10)."""
    assert POLICY_RULE in _policy_text()
    asked, outside = 0, []
    for verb in (*RESTORES, *ASKABLE):
        own = wg.switch_kind(wg.parse_git(["git", *verb.split()]))
        for command in _shapes(verb):
            # `judged=set()`: the function-level default subtracts what the
            # frozen walk's words hold, which is this case's own frozen half,
            # and would leave nothing for it to check.
            kinds = wg.wider_only_kinds(command, str(tmp_path), judged=set())
            if not kinds:
                continue
            asked += 1
            text = wg.wide.drop_heredoc_bodies(wg.wide.drop_comments(command))
            items, _clean = wg.wide.split_segments_with_separators(text)
            frozen = {wg.switch_kind(wg.parse_git(tokens)) for _sep, tokens in items}
            if kinds != {own} or own in frozen:
                outside.append((command, sorted(kinds), own))
    assert asked, "the generator reached no shape the wider reading asks"
    assert not outside, (len(outside), outside[:10])


HIDDEN_FILE_CHECKOUTS = (
    "2>/dev/null git checkout README.md",
    "git 2>/dev/null checkout README.md",
    "git checkout>/dev/null README.md",
    "git checkout &>/dev/null README.md",
)


@pytest.mark.parametrize("command", HIDDEN_FILE_CHECKOUTS)
def test_a_file_checkout_hidden_from_the_frozen_reader_is_asked_as_a_switch(
    tmp_path, command
):
    """`docs/worktree-guard-spec.md` §*Which tree*: C reads no tree, so a
    file's name reads as a branch's, and the rule asks it wherever the frozen
    reading misses it (warden round 1 of #737). Seen red against a
    `switch_kind` that skips a name holding a `.`."""
    assert wg.wider_only_kinds(command, str(tmp_path)) == {"switch"}, command


def test_the_guard_policy_says_a_hidden_file_checkout_is_asked():
    """§14 of the agent contract: the sentence a person reads to learn when
    the guard asks states the rule, says the reading looks up no tree, and
    labels its examples as examples. Red against the round-1 sentence, which
    listed positions and promised silence for a detach (round 2 of #737)."""
    text = _policy_text()
    assert POLICY_RULE in text
    assert "it asks whether or not the command moves the tree" in text
    assert "the two are examples, not the set" in text
    assert "`git checkout &>/dev/null README.md` is asked" in text
    assert (
        "Each side is read by its words alone, as git is handed them: a "
        "`switch` naming a word or `-` or carrying a creating option, a "
        "`checkout` carrying a creating option (`-b`, `-B` or `--orphan`, in any "
        "spelling git's option parser accepts), a `checkout` that names `-` or a "
        "word other than `.` before any `--` and has no word after one, or a "
        "`worktree add`; an option's value is not a name, and a redirection is "
        "no word."
    ) in text
    # Round 1 of work item 1791119071, red 1: a bare trailing `--` is no
    # restore, and the limit the `&` cut leaves says so.
    assert (
        "A cut after a `--` leaves the frozen reading a `--` with nothing after "
        "it, so `git checkout feature/x -- <&1 README.md`, a restore, is judged "
        "a switch to `feature/x` too"
    ) in text


def test_the_guard_policy_says_what_it_reads_past_the_base():
    """§14 of the agent contract, for #764 and #738 (work item 1791119071)
    and #790 (work item 1791163981): the paragraph that says the command is
    read as `86256492` read it names the two rules now read past it, on whose
    act and when, and what stays the base's. Red against the paragraph as it
    stood at `94d7b2e0`, and its #790 sentences against `a3aa139a`'s; the
    round 1 sentences of 1791163981 against `85e77dc8`'s, and round 2's
    against `f659c466`'s."""
    text = _policy_text()
    assert (
        "Two rules are read past the base. The first, since #764 and #738 on "
        "the owner's answer of 2026-10-04: a `checkout`'s and a `switch`'s own "
        "words are read as git's option parser sees them once bash has taken "
        "the redirections off"
    ) in text
    assert (
        "The second, since #790 on the owner's placement of it in the "
        "milestone of the release that ships it, on 2026-10-05: a `checkout`'s "
        "name is looked up the "
        "way `git checkout` resolves it. The name is a branch to switch to "
        "where it names a commit once resolved and peeled, as every "
        "single-revision form does, a message search (`git checkout ':/fix "
        "typo'`) included, and where `rev-parse` reads the word as a range "
        "git's object lookup reads it whole, as `git checkout` does; where it "
        "is `<a>...<b>` with exactly one merge base, a side left empty meaning "
        "`HEAD`; and where a remote-tracking branch of any remote ends in it, "
        "or a remote's fetch refspec maps `refs/heads/<name>` to a ref that "
        "exists, which is git's guess. The base's lookup is still asked first, "
        "so no name it read as a branch goes quiet. A `checkout` only these "
        "lookups read as a switch takes the place of no switch the base read "
        "in the same command, and it takes no question away from candidate C "
        "below: it is judged only where the base read no switch at all."
    ) in text
    assert (
        "a few names git refuses are still read as a branch, so the command is "
        "asked although it would not run"
    ) in text
    # Round 2 of 1791163981, ⬜ 2: the limit the placement leaves, in the
    # walk's paragraph and in §*Known limits*.
    assert (
        "Since #790 the first switch is the first the base's lookups read, and "
        "a `checkout` only #790's lookups read takes the place only where they "
        "read none"
    ) in text
    assert (
        "so one in a second, dirty tree, written before a switch the frozen "
        "reading reads in a clean tree, goes unasked, as it did at the base."
    ) in text
    # Round 1 of 1791163981, 🟡 2: the guess reads the fetch refspecs, so the
    # sentence that it never guesses less than git is true.
    assert (
        "The guard reads each remote's fetch refspec, as git's guess does, but "
        "no `checkout.guess`, `checkout.defaultRemote` or `--no-guess`, so it "
        "guesses where git would not, never the other way."
    ) in text
    assert (
        "Which segments are git, the `-C` values each names and where every "
        "`cd` lands stay the base's, and `hooks/cmdline_base.py` is unchanged."
    ) in text
    assert (
        "and the frozen segments it is compared with are read the same way (#738)"
    ) in text


def test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1 of 1790993140, yellow 3: the subtraction is per view, so a
    restore both readings parse alike adds no question, as at the base."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, _ = run(
        monkeypatch, capsys, "cd w && git checkout README.md", session
    )
    assert decision == "silent", (decision, reason)


def test_a_hidden_switch_behind_a_judged_one_adds_no_question(
    monkeypatch, capsys, repo
):
    """The kind the frozen loop judged keeps its verdict: a clean single
    stream lets the switch through, and a second switch only the wider
    reading finds is not asked about."""
    command = f"{SWITCH}; 2>/dev/null git switch main"
    decision, reason, top = run(monkeypatch, capsys, command, repo)
    assert decision == "silent", (decision, reason)
    assert top and os.path.samefile(top, repo), top


def test_a_hidden_creation_behind_a_judged_one_adds_no_question(
    monkeypatch, capsys, repo, tmp_path
):
    """The judged creation's own clone has consent, so its verdict is
    silence; a second creation only the wider reading finds is not asked
    about from a directory in no repository."""
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert wg.worktree_consent.record(str(repo), "me")
    command = (
        f"git -C {repo} worktree add ../wt-a -b a && "
        f"git -C {repo} 2>&1 worktree add ../wt-b -b b"
    )
    decision, reason, _ = run(monkeypatch, capsys, command, elsewhere)
    assert decision == "silent", (decision, reason)


def test_a_broken_wider_reader_costs_only_the_question(
    monkeypatch, capsys, repo, tmp_path
):
    """Where `hooks/cmdline.py` failed to load, the guard keeps its own rows
    and asks nothing it could not read, as at the base."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    monkeypatch.setattr(wg, "wide", None)
    decision, _, _ = run(monkeypatch, capsys, "git --config-env k=v switch x", session)
    assert decision == "silent"


KINDS = {
    "switch to a branch": (["git", "switch", "x"], "switch"),
    "switch -c": (["git", "switch", "-c", "x"], "switch"),
    "switch -": (["git", "switch", "-"], "switch"),
    "switch with no target": (["git", "switch", "--detach"], None),
    "checkout -b": (["git", "checkout", "-b", "x"], "switch"),
    # `classify`'s order: `-b` is a switch before `--` is a restore.
    "checkout -b before --": (["git", "checkout", "-b", "x", "--"], "switch"),
    "checkout a name": (["git", "checkout", "x"], "switch"),
    "checkout -": (["git", "checkout", "-"], "switch"),
    "checkout .": (["git", "checkout", "."], None),
    "checkout -- path": (["git", "checkout", "--", "f"], None),
    "checkout with no name": (["git", "checkout", "-q"], None),
    # §*Which tree*'s words: a `--` with a word after it takes every name out
    # of a checkout, and `-B` is a switch with or without one (round 3 of
    # #737).
    "checkout a name before --": (["git", "checkout", "x", "--", "f"], None),
    # Round 1 of 1791119071, 🔴 1: a `--` with nothing after it only says the
    # name before it is no file, and git switches to it.
    "checkout a name and a bare --": (["git", "checkout", "x", "--"], "switch"),
    "checkout -B with no name": (["git", "checkout", "-B"], "switch"),
    "switch -- a name": (["git", "switch", "--", "x"], "switch"),
    # #764 (work item 1791119071): a creating option counts in every spelling
    # git's option parser accepts, with or without its value, and an option's
    # value is no name.
    "checkout -b stuck": (["git", "checkout", "-by"], "switch"),
    "checkout -b aggregated": (["git", "checkout", "-qb", "y"], "switch"),
    "checkout -B aggregated and stuck": (["git", "checkout", "-qBy"], "switch"),
    "checkout --orphan": (["git", "checkout", "--orphan", "y"], "switch"),
    "checkout --orphan stuck": (["git", "checkout", "--orphan=y"], "switch"),
    "checkout --orphan abbreviated and stuck": (
        ["git", "checkout", "--orph=y"],
        "switch",
    ),
    "switch -c alone": (["git", "switch", "-c"], "switch"),
    "switch -c stuck": (["git", "switch", "-cy"], "switch"),
    "switch -c aggregated and stuck": (["git", "switch", "-qcy"], "switch"),
    "switch --create stuck": (["git", "switch", "--create=y"], "switch"),
    "switch --create abbreviated and stuck": (["git", "switch", "--cre=y"], "switch"),
    "switch --force-create stuck": (["git", "switch", "--force-create=y"], "switch"),
    "switch --orphan stuck": (["git", "switch", "--orphan=y"], "switch"),
    "checkout --conflict and its value": (
        ["git", "checkout", "--conflict", "merge"],
        None,
    ),
    "checkout --conflict, its value and a name": (
        ["git", "checkout", "--conflict", "merge", "x"],
        "switch",
    ),
    "switch --conflict and its value": (["git", "switch", "--conflict", "merge"], None),
    "checkout -U and its value": (["git", "checkout", "-U", "3"], None),
    "checkout -t taking the rest of its word": (["git", "checkout", "-tb"], None),
    "checkout -b after --": (["git", "checkout", "--", "-b", "y"], None),
    # A word git refuses, an ambiguous abbreviation here, takes nothing.
    "switch an ambiguous abbreviation": (["git", "switch", "--c", "x"], "switch"),
    # #738: a redirection is no word.
    "checkout only a redirection": (["git", "checkout", "2>/dev/null"], None),
    "checkout . with a redirection glued": (["git", "checkout", ".>/dev/null"], None),
    "switch only a redirection": (["git", "switch", ">", "/dev/null"], None),
    "worktree add": (["git", "worktree", "add", "../wt"], "creation"),
    "worktree list": (["git", "worktree", "list"], None),
    "status": (["git", "status"], None),
    "not git": (["echo", "git", "switch", "x"], None),
}


@pytest.mark.parametrize("name", sorted(KINDS))
def test_switch_kind_reads_the_words_alone(name):
    tokens, kind = KINDS[name]
    assert wg.switch_kind(wg.parse_git(tokens)) == kind, name


def test_candidate_c_reads_a_redirection_glued_to_git(tmp_path):
    assert wg.wider_only_kinds("git>/dev/null switch x", str(tmp_path)) == {"switch"}


def test_a_wider_reader_that_exits_at_load_costs_only_the_question(
    monkeypatch, tmp_path
):
    """Round 1 of 1790993140, white 5. A `hooks/cmdline.py` whose body raises
    `SystemExit` is a failure `hooks/dispatch.py` catches beside `Exception`,
    and the guard's import catches it too, so the guard still loads and keeps
    its own rows. Seen red with `except Exception:` alone."""
    hooks = tmp_path / "hooks"
    shutil.copytree(os.path.join(os.path.dirname(__file__), "..", "hooks"), hooks)
    (hooks / "cmdline.py").write_text("raise SystemExit(3)\n", encoding="utf-8")
    monkeypatch.delitem(sys.modules, "cmdline", raising=False)
    monkeypatch.syspath_prepend(str(hooks))
    spec = importlib.util.spec_from_file_location(
        "wg_exiting_reader", hooks / "worktree-guard.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.wide is None
    assert (
        module.wider_only_kinds("git --config-env k=v switch x", str(tmp_path)) == set()
    )


# --- #764 and #738: a checkout's and a switch's words, as git is handed them ---
#
# Work item 1791119071. `spec.md`'s three axes, constructed: Axis 1 is each
# creating option of each subcommand, Axis 2 each spelling git's option parser
# accepts for it (`git help cli`: short separate and stuck, aggregated behind
# `-q` separate and stuck, long separate and stuck, abbreviated separate and
# stuck), and Axis 3 is `_placed`. git 2.54.0 switches on every spelling below
# and on none of the twins (phase 1's M1, executed).
CREATING = {
    "checkout": ("-b", "-B", "--orphan"),
    "switch": ("-c", "-C", "--create", "--force-create", "--orphan"),
}
# A value-taking option that creates nothing, in its three spellings.
VALUED = ("--conflict merge", "--conflict=merge", "--confl merge")


def _spellings(option, value):
    """OPTION carrying VALUE in each spelling git's option parser accepts. An
    abbreviation is the long name one character short, which no other option
    of either subcommand begins with."""
    if option.startswith("--"):
        short_by_one = option[:-1]
        return (
            f"{option} {value}",
            f"{option}={value}",
            f"{short_by_one} {value}",
            f"{short_by_one}={value}",
        )
    letter = option[1]
    return (
        f"{option} {value}",
        f"{option}{value}",
        f"-q{letter} {value}",
        f"-q{letter}{value}",
    )


CREATIONS = tuple(
    f"{sub} {spelling}"
    for sub, options in CREATING.items()
    for option in options
    for spelling in _spellings(option, "y")
)
SWITCHES = (
    *(
        f"{sub} {words}"
        for sub in CREATING
        for words in ("feature/x", "-", *(f"{v} feature/x" for v in VALUED))
    ),
    "switch -- feature/x",
    # `-t` may take a value stuck only, so the next word is the name.
    *(f"{sub} -t feature/x" for sub in CREATING),
)
# What switches nothing: a file, `.`, a name after `--`, an option's value
# where a name would stand, a creating option after `--` or after
# `--end-of-options`, where it is a pathspec or a name, and one behind a
# letter git refuses, which refuses the word.
TWINS = (
    "checkout README.md",
    "checkout .",
    "checkout -- feature/x",
    "checkout feature/x -- README.md",
    "checkout --conflict feature/x",
    "checkout --end-of-options -b y",
    "checkout -xb y",
    *(f"checkout {v} README.md" for v in VALUED),
    *(f"{sub} {v}" for sub in CREATING for v in VALUED),
    *(f"checkout -- {spelling}" for spelling in _spellings("-b", "y")),
)


def _dashed(verb):
    """A fourth axis, where a `--` stands (round 1 of work item 1791119071,
    🔴 1): `(placement, verb)` for the verb as written, a bare `--` after it,
    a `--` and a path after it, its last word behind a `--`, and
    `--end-of-options` before its words with a bare `--` after them."""
    sub, *words = verb.split()
    yield "as written", verb
    yield "a bare -- after", f"{verb} --"
    yield "a -- and a path after", f"{verb} -- README.md"
    yield "the last word behind a --", " ".join([sub, *words[:-1], "--", words[-1]])
    yield (
        "--end-of-options and a bare -- after",
        " ".join([sub, "--end-of-options", *words, "--"]),
    )


def _git_switches(verb, placement):
    """Whether git 2.54.0 moves HEAD on `git <verb>` with its `--` at
    PLACEMENT, for a VERB of `CREATIONS` or `SWITCHES`. Measured by round 1's
    fix pass: all 225 such commands, each run under bash in a scratch
    repository, agree with this.

    As written, every one switches. A bare `--` after only says the name
    before it is no file, so the verb still switches, unless it already holds
    a `--`, which makes two. A path after a `--` is a restore on `checkout`
    and refused on `switch`. A last word behind a `--` is a pathspec to
    `checkout`, still the branch to a `switch` that creates nothing, and a
    creating option's lost value otherwise. `--end-of-options` makes every
    option word a name: a `checkout` of a bare name or `-` still switches,
    and `switch` takes the trailing `--` for a second reference and refuses."""
    sub, *words = verb.split()
    holds_dashes = "--" in words
    if placement == "as written":
        return True
    if placement == "a bare -- after":
        return not holds_dashes
    if placement == "a -- and a path after":
        return False
    if placement == "the last word behind a --":
        return sub == "switch" and verb not in CREATIONS and not holds_dashes
    return sub == "checkout" and all(w == "-" or not w.startswith("-") for w in words)


DASHED = [
    (verb, placement, dashed)
    for verb in (*CREATIONS, *SWITCHES)
    for placement, dashed in _dashed(verb)
]
DASHED_SWITCHES = tuple(d for v, p, d in DASHED if _git_switches(v, p))
# A `checkout` that creates nothing, where git switches nothing: a restore, or
# a command git refuses. A creation or a `switch` git refuses here is asked,
# the loud direction on a command that does nothing.
DASHED_TWINS = tuple(
    d
    for v, p, d in DASHED
    if not _git_switches(v, p) and v.startswith("checkout") and v not in CREATIONS
)


@pytest.fixture
def a_branch_and_a_file(monkeypatch, repo):
    """`repo` with `README.md` on disk beside its branch `feature/x`. `is_ref`
    is a lookup over the repository's refs, read once, so a sweep of the
    generated shapes spawns no git per shape."""
    (repo / "README.md").write_text("r\n", encoding="utf-8")
    listed = subprocess.run(
        ["git", "-C", str(repo), "for-each-ref", "--format=%(refname:short)"],
        capture_output=True,
        check=True,
        encoding="utf-8",
    ).stdout.split()
    monkeypatch.setattr(wg, "is_ref", lambda name, cwd: name in listed)
    return str(repo)


def _read_apart(command, cwd):
    """`(judged, wider)`: the kinds `classify` reads on COMMAND's frozen
    segments, as `main`'s loop reads them, and the kinds candidate C then adds
    to them."""
    judged = set()
    for tokens, _wheres in wg.walk_command(command, cwd):
        found = wg.classify(tokens, cwd)
        if found:
            judged.add("creation" if found == "worktree-add" else "switch")
    return judged, wg.wider_only_kinds(command, cwd, judged)


def _kinds_read(command, cwd):
    """The kinds the guard reads in COMMAND at function level."""
    judged, wider = _read_apart(command, cwd)
    return judged | wider


@pytest.mark.parametrize("verb", CREATIONS)
def test_classify_reads_a_creating_option_in_every_spelling(repo, verb):
    """`spec.md` A2. At `94d7b2e0` every spelling but the separate short one
    was read as no switch, or as a plain one, because the arms test a word
    against `-b`, `-B`, `-c` and `-C` alone."""
    (repo / "README.md").write_text("r\n", encoding="utf-8")
    assert wg.classify(["git", *verb.split()], str(repo)) == "create+switch", verb


@pytest.mark.parametrize("verb", SWITCHES)
def test_classify_reads_the_name_past_an_options_value(repo, verb):
    """`spec.md` A2. At `94d7b2e0` `checkout --conflict merge feature/x` looked
    up `merge` and found no ref."""
    assert wg.classify(["git", *verb.split()], str(repo)) == "switch", verb


@pytest.mark.parametrize(
    "verb", [d for d in DASHED_SWITCHES if d not in (*CREATIONS, *SWITCHES)]
)
def test_classify_reads_a_switch_wherever_its_dashes_stand(repo, verb):
    """Round 1's 🔴 1: `git checkout feature/x --` switches, and both readers
    took any `--` for a restore."""
    (repo / "README.md").write_text("r\n", encoding="utf-8")
    assert wg.classify(["git", *verb.split()], str(repo)) in (
        "switch",
        "create+switch",
    ), verb


def test_a_bare_dashdash_names_the_branch_where_a_file_has_its_name(repo):
    """With a branch and a file both called `README.md`, `git checkout
    README.md --` switches to the branch (executed, git 2.54.0): the bare
    `--` says the name is no file, so the path test is not asked of it."""
    (repo / "README.md").write_text("r\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(repo), "branch", "README.md"], check=True, capture_output=True
    )
    tokens = ["git", "checkout", "README.md", "--"]
    assert wg.classify(tokens, str(repo)) == "switch"


@pytest.mark.parametrize("verb", (*TWINS, *DASHED_TWINS))
def test_classify_reads_no_switch_in_a_twin(repo, verb):
    (repo / "README.md").write_text("r\n", encoding="utf-8")
    assert wg.classify(["git", *verb.split()], str(repo)) is None, verb


def test_no_constructed_switch_is_silent(a_branch_and_a_file):
    """`spec.md` A4. Every shape of the three axes git switches on is read,
    by the frozen loop's `classify` with its tree or, where an `&`- or
    `|`-led operator cut the segment, by candidate C. Red at `94d7b2e0`, where
    phase 1 counted 7,025 silent shapes of 20,729. Since round 1's fix pass
    the verbs carry the `--` axis too (`_dashed`), and the shapes with a bare
    `--` after a `checkout`'s name were silent at `a7ab2a4e`."""
    silent = [
        command
        for verb in DASHED_SWITCHES
        for command in _shapes(verb)
        if "switch" not in _kinds_read(command, a_branch_and_a_file)
    ]
    assert not silent, (len(silent), silent[:10])


def test_no_twin_is_asked_unless_an_operator_cuts_the_segment(a_branch_and_a_file):
    """`spec.md` A5. A twin is silent wherever its redirection stands after
    the subcommand and holds no `&` or `|`. Where it stands before the
    subcommand or holds one, only candidate C reads the whole switch, and C
    asks what §*Which tree*'s rule says: the kind the verb's own words hold.
    Red at `94d7b2e0`, which read `-b` after `--` as a creation.

    Where an `&`- or `|`-led operator cuts the segment, the frozen loop reads
    the words before the cut alone, so `git checkout feature/x <&1 --
    README.md` is judged a switch to `feature/x`, as at `94d7b2e0`
    (§*Known limits*); only C's half is held to the rule there."""
    wrong = []
    for verb in (*TWINS, *DASHED_TWINS):
        own = {wg.switch_kind(wg.parse_git(["git", *verb.split()]))} - {None}
        for command, at, glued, op in _placed(verb):
            judged, wider = _read_apart(command, a_branch_and_a_file)
            after_the_subcommand = at > 2 or (at == 2 and not glued)
            if after_the_subcommand and not any(c in op for c in "&|"):
                if judged | wider:
                    wrong.append((command, sorted(judged | wider)))
            elif not wider <= own:
                wrong.append((command, sorted(wider), sorted(own)))
    assert not wrong, (len(wrong), wrong[:10])


# One shape per position of Axis 3, through `main()`, over the dirty `w`.
PLACED_SWITCHES = {
    "R0, a stuck value": "git checkout -by",
    "R1, between checkout and its name": "git checkout 2>/dev/null feature/x",
    "R3, glued to the name": "git checkout feature/x>/dev/null",
    "R4, between -b and its value": "git checkout -b 2>/dev/null y",
    "R4, glued to -b": "git checkout -b>/dev/null y",
    "R5, after the name": "git switch feature/x 2>/dev/null",
}


@pytest.mark.parametrize("name", sorted(PLACED_SWITCHES))
def test_a_switch_wherever_its_redirection_stands_meets_the_dirty_tree_row(
    monkeypatch, capsys, repo, tmp_path, name
):
    """bash runs each as a switch (phase 1, executed). All but R5 were
    silent at `94d7b2e0`."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, top = run(
        monkeypatch, capsys, f"cd w && {PLACED_SWITCHES[name]}", session
    )
    assert decision == "ask", (name, decision, reason)
    assert "f.txt" in reason, (name, reason)
    assert top and os.path.samefile(top, session / "w"), (name, top)


@pytest.mark.parametrize(
    "command",
    [
        "git checkout f.txt>/dev/null",
        "git checkout 2>/dev/null f.txt",
        "git checkout --conflict 2>/dev/null merge f.txt",
    ],
)
def test_a_restore_wherever_its_redirection_stands_stays_silent(
    monkeypatch, capsys, repo, tmp_path, command
):
    """The tree tells the file from the branch, so the restore keeps the
    base's silence -- the trade a fence in C, which reads no tree, could not
    avoid (`plan.md` Alternatives A)."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, _ = run(monkeypatch, capsys, f"cd w && {command}", session)
    assert decision == "silent", (command, decision, reason)


def test_a_switch_behind_an_ampersand_led_operator_is_candidate_cs():
    """R&: the frozen splitter cuts at `&`, so only C's merged view holds the
    switch, and C asks without a tree (§*Known limits*)."""
    assert wg.wider_only_kinds("git checkout 2>&1 feature/x", "/") == {"switch"}


# A usage line of `git <sub> -h`: an optional short, an optional long with or
# without `[no-]`, then `[=…]` for a value given stuck only, or ` <…>` for one
# that must be given.
USAGE = re.compile(
    r"^ {2,}(?:-(?P<short>[^\s,-]))?(?:, )?(?:--(?:\[no-\])?(?P<long>[a-z][a-z0-9-]*))?"
    r"(?P<value> <[^>]*>)?"
)


def _usage(sub):
    r = subprocess.run(
        ["git", sub, "-h"], capture_output=True, encoding="utf-8", errors="replace"
    )
    return r.stdout + r.stderr


@pytest.mark.parametrize("sub", sorted(CREATING))
def test_the_option_table_binds_the_installed_git(sub):
    """`spec.md` A7. Every option `git <sub> -h` lists as taking a value it
    must be given is one the guard's table says takes a value, so the value is
    never read as a name. Fails on the first git that lists a new one, naming
    it; red with `--conflict` taken out of the table.

    And the other way (round 1's ⬜ 2): every option the table says takes a
    value it must be given, and that git lists at all, git lists with one. A
    git that made `--conflict <style>` optional would otherwise leave the
    table taking the next word, and `checkout --conflict feature/x` would read
    no name. An option git does not list is left alone, since an older git
    may simply not have it. Red with `--guess` doctored to take a value."""
    table = wg.SWITCH_OPTIONS[sub]
    missing, seen = [], 0
    listed = {}
    for line in _usage(sub).splitlines():
        m = USAGE.match(line)
        if not m or not (m.group("short") or m.group("long")):
            continue
        for key in (m.group("short"), m.group("long")):
            if key:
                listed[key] = bool(m.group("value"))
        if not m.group("value"):
            continue
        seen += 1
        if m.group("short") and table.short.get(m.group("short"), (None,))[0] != (
            wg.VALUE
        ):
            missing.append("-" + m.group("short"))
        if m.group("long") and table.long.get(m.group("long"), (None,))[0] != (
            wg.VALUE
        ):
            missing.append("--" + m.group("long"))
    assert seen, f"read no value-taking option out of `git {sub} -h`"
    assert not missing, (sub, missing)
    loose = [
        key
        for names in (table.short, table.long)
        for key, (takes, _creates) in names.items()
        if takes == wg.VALUE and listed.get(key) is False
    ]
    assert not loose, (sub, "listed without a value it must be given", loose)


def test_the_reduction_takes_out_every_redirection_the_reader_names():
    """`spec.md` A8. The guard's own reduction is bound to `hooks/cmdline.py`'s
    `_REDIRECTION` by this case, not by an import: `classify` keeps answering
    where that module fails to load. Red with `<>` taken out of the guard's
    copy; `&>` taken out is not red, because the `&` a glued word keeps is
    cut and dropped before the operator is read."""
    left = []
    for op, target in _redirections():
        gluable = not op[0].isdigit() and not op.startswith("{")
        shapes = [[op + target], [op, target]]
        if gluable:
            shapes += [["name" + op + target], ["name" + op, target]]
        for words in shapes:
            got = wg.handed_words(words)
            if got not in ([], ["name"]):
                left.append((words, got))
    assert not left, left


def test_a_process_substitution_target_goes_with_its_operator():
    """bash runs `git checkout 2> >(cat) feature/x` as a switch to
    `feature/x` (executed); the splitter hands the target over as two words."""
    words = ["2>", ">(tee", "log)", "feature/x"]
    assert wg.handed_words(words) == ["feature/x"]


def test_a_word_holding_whitespace_is_not_cut():
    """A word with whitespace in it was quoted, so a `>` in it is the
    argument's, as `hooks/cmdline.py#unglued` reads it."""
    assert wg.handed_words(["a b>c"]) == ["a b>c"]


def test_a_long_option_named_exactly_wins_over_the_ones_it_begins():
    """git resolves an exact long name before a prefix: `--force` is
    `switch`'s `--force` and not an ambiguous prefix of `--force-create`.
    No option of either table tells the two readings apart today, so the rule
    is pinned on a table built for it."""
    options = wg._Options(
        short={}, long={"x": (wg.VALUE, True), "xy": (wg.NONE, False)}
    )
    assert wg._long_option(options, "x") == (True, True)
    assert wg._long_option(options, "x=v") == (False, True)
    assert wg._long_option(options, "xy") == (False, False)


def test_an_ambiguous_long_prefix_takes_nothing():
    """git refuses a prefix two long names begin with (`git switch --c y`:
    "ambiguous option: c (could be --create or --conflict)"), and a word git
    refuses reads as an option that takes nothing and creates nothing."""
    options = wg._Options(
        short={}, long={"ab": (wg.VALUE, True), "ac": (wg.NONE, False)}
    )
    assert wg._long_option(options, "a") == (False, False)
    assert wg._long_option(options, "ab") == (True, True)


# --- #790: a checkout's name, looked up the way `git checkout` resolves it ---
#
# Work item 1791163981. `spec.md` §*The class* enumerates the three routes git
# takes from a `checkout`'s name to a commit: C1 a single-revision expression,
# C2 the merge-base shorthand, C3 the remote-tracking guess. Phase 1's M1 ran
# every form below under every carrier with git 2.54.0, and the verdicts in
# these tables are what it found (executed).


def _git(d, *args):
    return subprocess.run(
        ["git", "-C", str(d), *args],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def _commit(d, path, message):
    (d / path).write_text(path + "\n", encoding="utf-8")
    _git(d, "add", path)
    _git(d, "commit", "-qm", message)


@pytest.fixture(scope="module")
def a_history(tmp_path_factory):
    """A repository whose names reach every route of `spec.md` §*The class*:
    commit messages to search, two branches with one merge base and two with
    two (a criss-cross), an annotated tag, an upstream, a previous branch, and
    two remotes, `origin` and `upstream`, holding a branch only `origin` has,
    one only `upstream` has and one both have. Read-only for every case."""
    root = tmp_path_factory.mktemp("a-history")
    d = root / "r"
    for bare in ("o.git", "u.git"):
        subprocess.run(
            ["git", "init", "-q", "--bare", str(root / bare)],
            check=True,
            capture_output=True,
        )
    subprocess.run(["git", "init", "-q", str(d)], check=True, capture_output=True)
    _git(d, "symbolic-ref", "HEAD", "refs/heads/main")
    _git(d, "config", "user.email", "t@t")
    _git(d, "config", "user.name", "t")
    _commit(d, "README.md", "initial commit")
    for branch in ("side", "cx1", "cx2"):
        _git(d, "branch", branch)
    _commit(d, "alpha.txt", "add alpha feature")
    _git(d, "tag", "-a", "v1", "-m", "v1")
    _commit(d, "beta.txt", "add beta !bang")
    _git(d, "switch", "-q", "side")
    _commit(d, "side.txt", "side work")
    _git(d, "switch", "-q", "cx1")
    _commit(d, "x.txt", "cx one")
    _git(d, "switch", "-q", "cx2")
    _commit(d, "y.txt", "cx two")
    _git(d, "merge", "-q", "--no-edit", "cx1")
    _git(d, "switch", "-q", "cx1")
    _git(d, "merge", "-q", "--no-edit", "cx2~1")
    _git(d, "remote", "add", "origin", str(root / "o.git"))
    _git(d, "remote", "add", "upstream", str(root / "u.git"))
    for branch, remotes in (
        ("onorigin", ("origin",)),
        ("onupstream", ("upstream",)),
        ("inboth", ("origin", "upstream")),
    ):
        _git(d, "branch", branch, "main")
        for remote in remotes:
            _git(d, "push", "-q", remote, branch)
        _git(d, "branch", "-D", branch)
    _git(d, "push", "-q", "-u", "origin", "main")
    _git(d, "fetch", "-q", "--all")
    _git(d, "switch", "-q", "side")
    _git(d, "switch", "-q", "main")
    return str(d)


# The carriers, `spec.md` §*The class*: the words that make a segment read a
# name. `switch` reads any word as a switch already, so it carries no lookup.
CARRIERS = {
    "checkout N": lambda n: ["checkout", n],
    "checkout N --": lambda n: ["checkout", n, "--"],
    "checkout --detach N": lambda n: ["checkout", "--detach", n],
    "checkout --detach N --": lambda n: ["checkout", "--detach", n, "--"],
}

# Forms git switches or detaches on under every carrier above (M1), and which
# `a3aa139a`'s lookup read: False is a shape it was silent on.
MOVES = {
    "C1 a message search": (":/alpha", False),
    "C1 a message search for a leading !": (":/!!bang", False),
    "C1 a negative message search": (":/!-alpha", True),
    "C1 a branch": ("side", True),
    "C1 an annotated tag": ("v1", True),
    "C1 an ancestor": ("main~1", True),
    "C1 the previous branch": ("@{-1}", True),
    "C1 an upstream": ("main@{upstream}", True),
    "C1 a search from a revision": ("main^{/alpha}", True),
    "C1 another remote's branch, named": ("upstream/onupstream", True),
    "C2 a merge base": ("main...side", False),
    "C2 a merge base with HEAD on the left": ("...side", False),
    "C2 a merge base with HEAD on the right": ("side...", False),
}

# The guess: git creates the branch and switches under the two carriers with
# no `--detach`, and refuses under the other two (M1).
GUESSED = {
    "C3 a branch only origin holds": ("onorigin", True),
    "C3 a branch only another remote holds": ("onupstream", False),
}

# Forms git refuses under every carrier (M1). Each keeps the base's verdict,
# which is silence.
REFUSED = {
    "C1 a message search matching nothing": ":/nomatch-xyz",
    "C1 a blob": "HEAD:README.md",
    "C1 a tree": "main^{tree}",
    "C1 past the reflog": "main@{9999}",
    "C2 two merge bases": "cx1...cx2",
    "C2 a side naming nothing": "main...nosuch",
    "range two dots": "side..main",
    "range a commit alone": "main^!",
    "range every parent": "main^@",
    "C3 a name no remote holds": "nosuch",
}


def _moving_shapes():
    for form_name, (form, _base) in MOVES.items():
        for carrier, make in CARRIERS.items():
            yield f"{form_name}, {carrier}", ["git", *make(form)]
    for form_name, (form, _base) in GUESSED.items():
        for carrier in ("checkout N", "checkout N --"):
            yield f"{form_name}, {carrier}", ["git", *CARRIERS[carrier](form)]


MOVING_SHAPES = dict(_moving_shapes())


@pytest.mark.parametrize("name", sorted(MOVING_SHAPES))
def test_every_name_git_moves_the_tree_on_is_read_as_a_switch(a_history, name):
    """`spec.md` A2. Each of `classify` with its tree, `switch_kind` without
    one, and candidate C reads the shape, and C finds nothing the frozen
    reading missed. Red at `a3aa139a` for every message search but the
    negative one, every merge-base form and the guess from `upstream`: the
    lookup asked `<name>^{commit}`, which a `:/` search reads as its pattern
    and `rev-parse --verify` cannot read beside `...`, and it guessed from
    `origin` alone."""
    tokens = MOVING_SHAPES[name]
    assert wg.classify(tokens, a_history) == "switch", name
    assert wg.switch_kind(wg.parse_git(tokens)) == "switch", name
    assert wg.wider_only_kinds(shlex.join(tokens), a_history) == set(), name


@pytest.mark.parametrize("name", sorted(REFUSED))
def test_a_name_git_refuses_keeps_the_bases_silence(a_history, name):
    """`spec.md` A2's other half: a form git refuses under every carrier is
    not read as a switch, as at `a3aa139a` (M1)."""
    for carrier, make in CARRIERS.items():
        tokens = ["git", *make(REFUSED[name])]
        assert wg.classify(tokens, a_history) is None, (name, carrier)


@pytest.mark.parametrize(
    "command",
    [
        "(git checkout :/alpha)",
        "(git checkout main...side)",
        "(git checkout onupstream)",
    ],
)
def test_a_subshell_checkout_resolves_a_name_git_resolves(a_history, command):
    """The `)` peel reads through the same lookups: the parenthesis rides on
    the name, and the name without it is what git resolves. Red at
    `a3aa139a`."""
    segments, _ = wg.split_command(command)
    assert wg.classify(segments[0], a_history) == "switch", command


@pytest.mark.parametrize(
    "tokens",
    [
        ["git", "checkout", ":/alpha", "--", "README.md"],
        ["git", "checkout", "main...side", "--", "README.md"],
        ["git", "checkout", "onupstream", "--", "README.md"],
        ["git", "checkout", "--", "README.md"],
    ],
)
def test_a_restore_naming_a_resolvable_name_stays_a_restore(a_history, tokens):
    """`spec.md` A5. A word after `--` makes the segment a restore before any
    name is looked up, as at `a3aa139a`."""
    assert wg.classify(tokens, a_history) is None, tokens


def _the_bases_lookup(name, cwd):
    """`a3aa139a`'s `is_ref`, verbatim: one `<name>^{commit}`."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{name}^{{commit}}"],
            cwd=cwd or None,
            capture_output=True,
        )
        return r.returncode == 0
    except Exception:
        return False


def test_nothing_the_base_read_as_a_switch_goes_quiet(monkeypatch, a_history):
    """`spec.md` A4. Over every form of the three tables under every carrier,
    bare and inside a subshell, the build's `classify` reads a switch wherever
    `a3aa139a`'s did. The base is the build's `classify` with the base's
    lookup put back and the guess from other remotes taken out, which is all
    the change touched. It holds by the OR in `spec.md` §*Scope* In 1 and In
    2; red with resolve-then-peel in place of the base's lookup rather than
    beside it (`plan.md` C), which turns `checkout ^main` quiet."""
    forms = [
        *(form for form, _ in MOVES.values()),
        *(form for form, _ in GUESSED.values()),
        *REFUSED.values(),
        "inboth",
        "^main",
    ]
    shapes = []
    for form in forms:
        for make in CARRIERS.values():
            words = ["git", *make(form)]
            shapes.append(words)
            shapes.append(wg.split_command(f"({shlex.join(words)})")[0][0])
    with monkeypatch.context() as m:
        m.setattr(wg, "is_ref", _the_bases_lookup)
        m.setattr(wg, "tracked_in_any_remote", lambda name, cwd: False)
        base = [wg.classify(tokens, a_history) for tokens in shapes]
    asked = [tokens for tokens, verdict in zip(shapes, base, strict=True) if verdict]
    assert len(asked) > len(shapes) // 4, "the base read too few shapes to compare"
    quieter = [tokens for tokens in asked if not wg.classify(tokens, a_history)]
    assert not quieter, quieter
    for form, read in (*MOVES.values(), *GUESSED.values()):
        assert bool(base[shapes.index(["git", "checkout", form])]) is read, form


def test_a_message_search_over_a_dirty_tree_is_asked(
    monkeypatch, capsys, repo, tmp_path
):
    """`spec.md` A3, #790's own shape through `main()`: `git checkout
    ':/<message>'` detaches at the newest commit whose message matches, so it
    moves a dirty tree, and the dirty-tree row asks. The same search matching
    nothing is refused by git and stays silent. Red at `a3aa139a`, where both
    were silent."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, top = run(
        monkeypatch, capsys, "cd w && git checkout ':/base'", session
    )
    assert decision == "ask", (decision, reason)
    assert "f.txt" in reason, reason
    assert top and os.path.samefile(top, session / "w"), top
    decision, reason, _ = run(
        monkeypatch, capsys, "cd w && git checkout ':/nomatch-xyz'", session
    )
    assert decision == "silent", (decision, reason)


# --- #780: a consent token inside a here-document body is not read ---------
#
# Work item 1791163981. `has_token` reads a token only where the command as
# written AND the command with its here-document bodies taken out carry it,
# the rule `hooks/tokens.py#given` has kept for the commit gate since #773.
# Each body below is one a consent read must not take a token from: the one
# shape `hooks/one_heredoc.py` matches byte for byte, and a body behind an
# unquoted delimiter, which `hooks/cmdline.py` finds.

BODY_TOKENS = {
    "[shared-tree-ok] in the one shape's body": (
        "python3 - <<'EOF'\n# [shared-tree-ok]\nEOF\ngit switch feature/x",
        "[shared-tree-ok]",
    ),
    "[shared-tree-ok] behind an unquoted delimiter": (
        "cat <<EOF >/dev/null\n[shared-tree-ok]\nEOF\ngit switch feature/x",
        "[shared-tree-ok]",
    ),
    "[worktree-ok] in the one shape's body": (
        "python3 - <<'EOF'\n# [worktree-ok]\nEOF\ngit worktree add ../wt -b y",
        "[worktree-ok]",
    ),
    "[worktree-ok] behind an unquoted delimiter": (
        "cat <<EOF >/dev/null\n[worktree-ok]\nEOF\ngit worktree add ../wt -b y",
        "[worktree-ok]",
    ),
}

# The documented forms, each beside a here-document in the same command.
TYPED_BESIDE_A_BODY = {
    "a trailing comment before a body": (
        "git switch feature/x  # [shared-tree-ok]\ncat <<'EOF' >/dev/null\nb\nEOF",
        "[shared-tree-ok]",
    ),
    "a trailing comment after the one shape's terminator": (
        "python3 - <<'EOF'\nprint(1)\nEOF\ngit switch feature/x  # [shared-tree-ok]",
        "[shared-tree-ok]",
    ),
    "a bare word after the command": (
        "git switch feature/x [shared-tree-ok]\ncat <<EOF >/dev/null\nb\nEOF",
        "[shared-tree-ok]",
    ),
    "a bare word before the command": (
        "cat <<EOF >/dev/null\nb\nEOF\n: [shared-tree-ok]; git switch feature/x",
        "[shared-tree-ok]",
    ),
    "inside a subshell": (
        "(git worktree add ../wt f [worktree-ok])\ncat <<EOF >/dev/null\nb\nEOF",
        "[worktree-ok]",
    ),
    "a comment after a creation, a body behind it": (
        "git worktree add ../wt f  # [worktree-ok]\ncat <<'EOF' >/dev/null\nb\nEOF",
        "[worktree-ok]",
    ),
}


@pytest.mark.parametrize("name", sorted(BODY_TOKENS))
def test_a_token_only_a_body_carries_is_not_read(monkeypatch, capsys, repo, name):
    """`spec.md` A6. A `[shared-tree-ok]` only a body carries leaves the
    cannot-tell row's choice in place, and a `[worktree-ok]` only a body
    carries leaves the single-stream creation denied. Red at `a3aa139a`, where
    the first was silent and the second asked."""
    command, token = BODY_TOKENS[name]
    assert not wg.has_token(command, token), name
    if token == "[shared-tree-ok]":
        decision, reason, _ = run(
            monkeypatch, capsys, command, repo, sessions=([], [], False)
        )
        assert decision == "deny", (name, decision, reason)
        assert "[shared-tree-ok]" in reason, reason
    else:
        decision, reason, _ = run(monkeypatch, capsys, command, repo)
        assert decision == "deny", (name, decision, reason)
        assert "[worktree-ok]" in reason, reason


@pytest.mark.parametrize("name", sorted(TYPED_BESIDE_A_BODY))
def test_a_typed_token_beside_a_body_is_still_read(name):
    """`spec.md` A7. Every documented form still carries consent when a
    here-document stands in the same command."""
    command, token = TYPED_BESIDE_A_BODY[name]
    assert wg.has_token(command, token), name


def _raises(command):
    raise RuntimeError("the wider body reader is broken")


def _a_guard_whose_wider_reader_exits_at_load(monkeypatch, tmp_path):
    """The guard loaded from a copy of `hooks/` whose `cmdline.py` raises
    `SystemExit` at load, as
    `test_a_wider_reader_that_exits_at_load_costs_only_the_question` makes
    it, so `tokens.without_bodies` fails on its own import."""
    hooks = tmp_path / "hooks"
    shutil.copytree(os.path.join(os.path.dirname(__file__), "..", "hooks"), hooks)
    (hooks / "cmdline.py").write_text("raise SystemExit(3)\n", encoding="utf-8")
    monkeypatch.delitem(sys.modules, "cmdline", raising=False)
    monkeypatch.syspath_prepend(str(hooks))
    spec = importlib.util.spec_from_file_location(
        "wg_exiting_reader_780", hooks / "worktree-guard.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.wide is None
    return module


@pytest.mark.parametrize("break_it", ["cmdline exits at load", "without_bodies"])
def test_a_broken_wider_reader_reads_no_body_token_and_keeps_a_typed_one(
    monkeypatch, tmp_path, break_it
):
    """`spec.md` A8. Where `hooks/cmdline.py` does not load, or where
    `hooks/tokens.py#without_bodies` raises, the bodies are found by the
    frozen reader `_judgment_text` uses. A body token is still not read and a
    typed one still is (`plan.md` G and H). The body half is red at
    `a3aa139a`."""
    guard = wg
    if break_it == "without_bodies":
        monkeypatch.setattr(wg.tokens, "without_bodies", _raises)
    else:
        guard = _a_guard_whose_wider_reader_exits_at_load(monkeypatch, tmp_path)
    for name, (command, token) in BODY_TOKENS.items():
        assert not guard.has_token(command, token), name
    for name, (command, token) in TYPED_BESIDE_A_BODY.items():
        assert guard.has_token(command, token), name


def _the_bases_token_read(command, token):
    """`a3aa139a`'s `has_token`, verbatim: the command as written."""
    segments, _clean = wg._tokenize(command)
    return any(
        tok == token or tok.strip("()") == token for toks in segments for tok in toks
    )


# Commands whose raw text the frozen splitter cannot finish, while the same
# text with its body taken out splits: a token there is one the command as
# written never offered (`plan.md` F, #773's reason for its AND).
UNREADABLE_UNTIL_THE_BODY_GOES = (
    "cat <<'EOF' >/dev/null\nit's\nEOF\ngit switch feature/x  # [shared-tree-ok]",
    "cat <<EOF >/dev/null\ndon't\nEOF\ngit worktree add ../wt f  # [worktree-ok]",
)

TOKEN_COMMANDS = (
    *(command for command, _ in BODY_TOKENS.values()),
    *(command for command, _ in TYPED_BESIDE_A_BODY.values()),
    *UNREADABLE_UNTIL_THE_BODY_GOES,
    "git switch feature/x  # [shared-tree-ok]",
    "git switch feature/x && echo done  # [shared-tree-ok]",
    "git switch feature/x && echo 'we documented [shared-tree-ok] today'",
    "git switch x && echo the [shared-tree-ok] token is documented",
    "git worktree add ../wt f  # [worktree-ok]",
    'git worktree add ../wt -b b origin/main && echo "wip; go"  # [worktree-ok]',
    'git worktree add ../wt f && echo "we agreed on [worktree-ok] yesterday',
    "git worktree add ../wt f  # [worktree-ok] but don't",
    "(git worktree add ../wt f [worktree-ok])",
    "git switch x [shared-tree-ok])",
)


@pytest.mark.parametrize("token", ["[worktree-ok]", "[shared-tree-ok]"])
@pytest.mark.parametrize("break_it", [None, "without_bodies"])
def test_the_token_read_never_reads_more_than_the_base(monkeypatch, token, break_it):
    """`spec.md` A9. Over every command of A6-A8, the two the splitter cannot
    finish until the body goes, and the existing token cases, `has_token` is
    True only where `a3aa139a`'s was, with the wider body reader working
    and raising. It holds by the AND in `spec.md` §*Scope* In 5; red with the
    read over the body-free text alone (`plan.md` F)."""
    if break_it:
        monkeypatch.setattr(wg.tokens, "without_bodies", _raises)
    read = [command for command in TOKEN_COMMANDS if wg.has_token(command, token)]
    assert read, "no command carried the token where both reads find it"
    more = [command for command in read if not _the_bases_token_read(command, token)]
    assert not more, more


def test_the_guard_policy_and_readmes_say_a_body_token_is_not_read():
    """§14 of the agent contract, for #780: §*Choice sites* and the two token
    rows of both READMEs say a token inside a here-document body is not
    read. Red against `a3aa139a`'s texts."""
    assert (
        "**Where the token is read from.** The command, and only the command. "
        "Not from a here-document body, since #780: a token counts only where "
        "the command as written and the command with its here-document bodies "
        "taken out both carry it"
    ) in _policy_text()
    root = os.path.join(os.path.dirname(__file__), "..")
    with open(os.path.join(root, "README.md"), encoding="utf-8") as f:
        readme = f.read()
    with open(os.path.join(root, "README.ko.md"), encoding="utf-8") as f:
        readme_ko = f.read()
    assert (
        "Read as a bare word, so it does not count inside a quoted message, "
        "and not inside a here-document body either."
    ) in readme
    assert "Read as a bare word, and not inside a here-document body." in readme
    assert (
        "따옴표 안의 문장에 적힌 것은 세지 않고, here-document 본문에 적힌 "
        "것도 세지 않는다."
    ) in readme_ko
    assert (
        "명령의 낱말로 있을 때만 세고, here-document 본문에 적힌 것은 세지 않는다."
    ) in readme_ko


# --- round 1 of 1791163981: nothing the base asked goes quiet through `main()` ---
#
# `classify` reads more names as a switch since #790, and `main` judges only
# the first switch of a command and hands candidate C the kinds it judged. So
# a newly read `checkout` in front must neither take the slot of the switch
# the base judged nor take C's question away (🟡 3).


def _a_dirty_clone_beside(repo, tmp_path):
    other = tmp_path / "other"
    shutil.copytree(repo, other)
    (other / "f.txt").write_text("changed on purpose\n", encoding="utf-8")
    return other


@pytest.mark.parametrize(
    "behind",
    [
        "git -C {other} switch feature/x",
        "2>/dev/null git -C {other} switch feature/x",
    ],
    ids=["a switch the frozen reading reads", "a switch only candidate C reads"],
)
@pytest.mark.parametrize("front", ["git checkout ':/base'", "git checkout ':/nomatch'"])
def test_a_newly_read_checkout_in_front_takes_no_question_away(
    monkeypatch, capsys, repo, tmp_path, front, behind
):
    """Round 1 of 1791163981, 🟡 3. A `checkout` that is a switch only through
    #790's lookups, in a clean single-session tree, stands in front of a
    switch in a second, dirty tree. `a3aa139a` read no switch in front, so it
    judged the second tree's switch, or C asked about it; the guard still
    asks. The two `:/base` cases were red at `85e77dc8`, where the checkout
    took the slot and C's question and the command went through silently.
    The two `:/nomatch` cases are controls, a search git refuses, and pass
    at every version."""
    other = _a_dirty_clone_beside(repo, tmp_path)
    command = f"{front} && {behind.format(other=other)}"
    decision, reason, _ = run(monkeypatch, capsys, command, repo)
    assert decision == "ask", (command, decision, reason)


def _a_repository(d):
    subprocess.run(["git", "init", "-q", str(d)], check=True, capture_output=True)
    _git(d, "symbolic-ref", "HEAD", "refs/heads/main")
    _git(d, "config", "user.email", "t@t")
    _git(d, "config", "user.name", "t")


def _where_git_checkout_lands(d, name):
    """The commit `git checkout NAME` detaches or switches to in a copy of D,
    or None where git refuses it."""
    copy = d.parent / (d.name + "-copy")
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(d, copy)
    r = subprocess.run(
        ["git", "-C", str(copy), "checkout", "-q", name], capture_output=True
    )
    landed = (
        _git(copy, "rev-parse", "HEAD").stdout.strip() if not r.returncode else None
    )
    shutil.rmtree(copy)
    return landed


@pytest.mark.parametrize("search", [":/v1..v2", ":/notes.*v1..v2"])
def test_a_message_search_holding_two_dots_is_read_as_a_switch(tmp_path, search):
    """Round 1 of 1791163981, 🟡 1. `git rev-parse` reads `..` as a range
    before it reads a name, so a message search holding it, both halves
    resolving, was two revisions to both of `_commit_named`'s calls while
    `git checkout` detached on it. Red at `85e77dc8`."""
    d = tmp_path / "r"
    _a_repository(d)
    _commit(d, "a.txt", "notes for v1..v2")
    _git(d, "tag", "v1")
    _commit(d, "b.txt", "second")
    _git(d, "tag", "v2")
    assert _where_git_checkout_lands(d, search), search
    for carrier, make in CARRIERS.items():
        tokens = ["git", *make(search)]
        assert wg.classify(tokens, str(d)) == "switch", (search, carrier)


@pytest.mark.parametrize("name", [":/v1..v2", ":/minus|^!", ":/minus|^@", ":/bang|^-1"])
def test_the_object_lookup_reads_a_word_rev_parse_reads_as_a_range(tmp_path, name):
    """Round 1 of 1791163981, 🟡 1: `git rev-parse` reads `..` and, where the
    regex library accepts an empty alternative, the parent shorthands `^!`,
    `^@` and `^-<n>` before it reads a name. `_object_named` hands the word to
    git's object lookup as `git checkout` does, so it finds the commit git
    lands on whichever way `rev-parse` reads it."""
    d = tmp_path / "r"
    _a_repository(d)
    for path, message in (("a", "notes for v1..v2"), ("b", "-1 minus"), ("c", "!x")):
        _commit(d, path, message)
        _git(d, "tag", "v1" if path == "a" else f"t{path}")
    _git(d, "tag", "v2")
    landed = _where_git_checkout_lands(d, name)
    assert landed, name
    assert wg._object_named(name, str(d)) == landed, name


@pytest.mark.parametrize(
    "fetch",
    [
        "+refs/heads/*:refs/fork/*",
        "+refs/heads/*:refs/remotes/fork/x-*",
        "refs/heads/onfork:refs/pinned/onfork",
    ],
    ids=["outside refs/remotes", "a partial glob", "an exact source"],
)
def test_a_guess_through_any_fetch_refspec_is_read_as_a_switch(tmp_path, fetch):
    """Round 1 of 1791163981, 🟡 2. git's guess maps `refs/heads/<name>`
    through each remote's fetch refspec, so a remote whose branches land
    outside `refs/remotes/`, or under a renaming glob, is guessed from by git
    and was not by the guard. Red at `85e77dc8`."""
    subprocess.run(
        ["git", "init", "-q", "--bare", str(tmp_path / "f.git")],
        check=True,
        capture_output=True,
    )
    d = tmp_path / "r"
    _a_repository(d)
    _commit(d, "README.md", "initial commit")
    _git(d, "remote", "add", "fork", str(tmp_path / "f.git"))
    _git(d, "config", "--replace-all", "remote.fork.fetch", fetch)
    _git(d, "branch", "onfork")
    _git(d, "push", "-q", "fork", "onfork")
    _git(d, "branch", "-D", "onfork")
    _git(d, "fetch", "-q", "fork")
    assert _where_git_checkout_lands(d, "onfork"), fetch
    for carrier in ("checkout N", "checkout N --"):
        tokens = ["git", *CARRIERS[carrier]("onfork")]
        assert wg.classify(tokens, str(d)) == "switch", (fetch, carrier)


def test_the_first_newly_read_checkout_is_the_one_judged(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1 of 1791163981, 🟡 3's fix. Where the base read no switch, the
    first `checkout` only #790's lookups read takes the slot, as `main` takes
    the first switch of a command everywhere else (#630). Seen red with the
    last one taking it."""
    other = tmp_path / "other"
    shutil.copytree(repo, other)
    command = f"git checkout ':/base' && git -C {other} checkout ':/base'"
    decision, reason, top = run(monkeypatch, capsys, command, repo)
    assert top and os.path.samefile(top, repo), (top, decision, reason)


def test_a_guess_through_a_remote_whose_name_holds_a_space(tmp_path):
    """Round 2 of 1791163981, 🟡 1. `git remote add` refuses a name holding a
    space, but git fetches and guesses through one the config names, and `git
    config --get-regexp` prints that key with the space in it, so a map that
    split each line at its first space read no refspec. Red at `f659c466`."""
    bare = tmp_path / "f.git"
    subprocess.run(
        ["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True
    )
    d = tmp_path / "r"
    _a_repository(d)
    _commit(d, "README.md", "initial commit")
    _git(d, "branch", "onfork")
    _git(d, "push", "-q", str(bare), "onfork")
    _git(d, "branch", "-D", "onfork")
    _git(d, "config", "remote.a b.url", str(bare))
    _git(d, "config", "remote.a b.fetch", "+refs/heads/*:refs/spaced/*")
    _git(d, "fetch", "-q", "a b")
    assert _where_git_checkout_lands(d, "onfork")
    for carrier in ("checkout N", "checkout N --"):
        tokens = ["git", *CARRIERS[carrier]("onfork")]
        assert wg.classify(tokens, str(d)) == "switch", carrier


@pytest.mark.parametrize(
    "space",
    ["\u00a0", "\u3000", "\u0085", "\u2028"],
    ids=["nbsp", "ideographic", "nel", "line separator"],
)
def test_a_guess_through_a_destination_ending_in_unicode_whitespace(tmp_path, space):
    """#811, round 3 of 1791163981. git's config reader strips only ASCII
    whitespace, so a fetch refspec whose destination ends in another space
    character fetches into a ref that ends in it, and git guesses through
    that ref. A map that ran `str.strip()` over the value, or split the ref
    listing with `str.splitlines()`, read a ref that does not exist. Red at
    `a8c7ab74`."""
    bare = tmp_path / "f.git"
    subprocess.run(
        ["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True
    )
    d = tmp_path / "r"
    _a_repository(d)
    _commit(d, "README.md", "initial commit")
    _git(d, "branch", "onfork")
    _git(d, "push", "-q", str(bare), "onfork")
    _git(d, "branch", "-D", "onfork")
    _git(d, "config", "remote.fork.url", str(bare))
    _git(d, "config", "remote.fork.fetch", "+refs/heads/*:refs/ws/*" + space)
    _git(d, "fetch", "-q", "fork")
    assert _where_git_checkout_lands(d, "onfork")
    for carrier in ("checkout N", "checkout N --"):
        tokens = ["git", *CARRIERS[carrier]("onfork")]
        assert wg.classify(tokens, str(d)) == "switch", carrier
