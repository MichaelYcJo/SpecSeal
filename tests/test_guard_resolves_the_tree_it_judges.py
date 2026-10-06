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
    """Run the hook, returning (decision, reason, tree_it_judged): the last
    tree the sessions were read for. SESSIONS is the answer for every tree,
    or a function of the tree that gives it."""
    seen = {}

    def stub(top, own=""):
        seen["top"] = top
        return sessions(top) if callable(sessions) else sessions

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


def test_an_untokenizable_command_holding_git_is_a_finding_of_its_own():
    """The splitter reports what it managed to read and says it gave up.
    `git switch "unclosed` yields a `switch` segment, which the ladder reads,
    and the command as a whole is an untokenizable one holding `git`, which is
    unrecognised (#826, the owner's answer P4 (a)): what the splitter could
    not read is not taken to be nothing."""
    command = 'git switch "unclosed'
    segments, clean = wg.split_command(command)
    assert clean is False
    assert wg.shape_of(segments[0]) == "switch"
    found = wg._command_findings(wg._judgment_text(command), clean)
    assert [f.kind for f in found] == ["untokenizable"], found


def test_segment_cwd_leaves_a_non_git_segment_alone(tmp_path):
    assert wg.segment_cwd(["echo", "hello"], str(tmp_path)) == str(tmp_path)


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


def test_a_restore_inside_a_subshell_is_listed_by_its_dashes_alone():
    """A closing parenthesis rides on the last word, and since #826 no word is
    looked up, so nothing has to peel it: `(git checkout -- README.md)` holds
    a path after `--` and is listed, and the two without one are
    unrecognised, inside a subshell as outside it."""
    for command, shape in (
        ("(git checkout -- README.md)", "listed"),
        ("(git checkout README.md)", "unrecognised"),
        ("(git checkout .)", "unrecognised"),
        ("(git checkout feature/x)", "unrecognised"),
    ):
        segments, _ = wg.split_command(command)
        assert wg.shape_of(segments[0]) == shape, command


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


def test_a_git_only_the_reading_past_redirections_finds_stops_in_its_segments_tree(
    monkeypatch, capsys, repo, tmp_path
):
    """#689. `2>/dev/null nice -n 5 git switch` is git only to the reading
    past redirections (#674). The guard reads through `86256492`'s frozen
    reader, which finds no git there, while bash switches `w`.

    Changed by round 1 of 1790745049, by phase 4 of 1790993140 (#678's
    candidate C, which asked about it with no tree), and by phase 3 of
    1791270162 (#826): the segment is an unrecognised shape now, judged in the
    tree its segment names, which the frozen walk places in the dirty `w`, so
    the stop asks there. It asserted `top is None`, C's tree-less question."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, top = run(
        monkeypatch,
        capsys,
        "cd w && 2>/dev/null nice -n 5 git switch feature/x",
        session,
    )
    assert decision == "ask", (decision, reason)
    assert "`2>/dev/null nice -n 5 git switch feature/x`" in reason, reason
    assert top and os.path.samefile(top, session / "w"), top


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
    segment took the slot and the guard judged the session's own tree.

    Rewritten by phase 3 of 1791270162 (#826): the hidden segment in front
    is an unrecognised shape judged in its own tree, the clean session tree
    (`clean` for the last command) with nobody else in it, so it says
    nothing there, and the switch the frozen reading reads keeps the slot and
    is denied over the session active in `w`. The stub used to put an ACTIVE
    session in every tree, which now stops on the hidden shape first."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    w = session / "w"
    active = [(111, str(w), 1.0, 0.5, "VS Code")]
    decision, reason, top = run(
        monkeypatch,
        capsys,
        command,
        session,
        sessions=lambda t: (
            (active, [], True) if os.path.samefile(t, w) else ([], [], True)
        ),
    )
    assert decision == "deny", (command, decision, reason)
    assert "Blocking this branch switch" in reason, reason
    assert top and os.path.samefile(top, w), (command, top)


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
    `silent` over the ACTIVE session, then `ask`, candidate C's question with
    no tree. Changed again by phase 3 of 1791270162 (#826): the shape is
    unrecognised and judged in `w`, where a session is ACTIVE, so the stop is
    a `deny` whoever is at the keyboard (`questions.md` P5) and names the
    plain spelling. The writer's half is unchanged."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    active = [(111, str(session / "w"), 1.0, 0.5, "VS Code")]
    decision, reason, top = run(
        monkeypatch,
        capsys,
        shape.format(verb="switch feature/x"),
        session,
        sessions=(active, [], True),
    )
    assert decision == "deny", (shape, decision, reason)
    assert "Write `git` first" in reason, reason
    assert top and os.path.samefile(top, session / "w"), (shape, top)
    acted = wg.worktree_consent.creation_directory(
        shape.format(verb="worktree add ../wt"), str(session)
    )
    assert acted == "", (shape, acted)


# --- #686 and #678's guard half, decided by a count ------------------------
#
# Both were built in phase 2 of work item 1790993140 and counted in phase 3
# over the recorded runs; phase 4 wired or removed each by that count, under
# the owner's rule of 2026-10-03. #686's ask fired on 9 recorded pairs and was
# removed, so its fallback is a known limit. #678's question was wired, and
# #826 replaced it with the unrecognised-shape stop.

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
    # Run in `w` since #826: in the clean session tree an unrecognised shape
    # says nothing, which is §A row 5 and not the reading under test.
    "--config-env, a creation": (
        "cd w && git --config-env k=v worktree add ../wt b",
        "creation",
    ),
    "2>/dev/null nice -n 5 git switch": (
        f"cd w && 2>/dev/null nice -n 5 {SWITCH}",
        "switch",
    ),
    "--config-env, a switch": ("cd w && git --config-env k=v switch x", "switch"),
    # Round 2 of 1790993140: a redirection glued to the subcommand's end.
    # bash runs each (executed by the round); the frozen parser reads
    # `switch>/dev/null` as the subcommand, which is the redirection shape
    # since #826, and `worktree add>/dev/null` as a `worktree` whose `add` a
    # redirection hides (`_hidden_mover`).
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
    # #737. The splitter cuts `&>` at `&`; bash runs each as a switch
    # (executed). The frozen reading reads the `git switch` or `git checkout`
    # in front of the cut, so the first meets the ladder and the second is
    # unrecognised.
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
def test_a_git_only_the_wider_reading_finds_stops_where_its_tree_matters(
    monkeypatch, capsys, repo, tmp_path, name
):
    """#678's guard half asked each of these with no tree (candidate C, silent
    at `233f0455`). Since #826 each is an unrecognised shape, judged in the
    tree its segment names, the dirty `w`, and stopped there with its plain
    spelling. The two creations hidden behind a redirection after `worktree`
    were silent at `9c03ae85`, where `worktree` was listed whatever stood
    where git reads `add` (phase 3 of 1791270162)."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    command, _kind = WIDER_ONLY[name]
    decision, reason, top = run(monkeypatch, capsys, command, session)
    assert decision == "ask", (name, decision, reason)
    # The stop's text, or the ladder's where an `&` cut leaves the frozen
    # reading a plain `git switch` (`&>` between switch and its name).
    assert "uncommitted tracked changes" in reason, reason
    assert top and os.path.samefile(top, session / "w"), (name, top)


@pytest.mark.parametrize(
    "name", sorted(k for k, (_c, kind) in WIDER_ONLY.items() if kind == "creation")
)
def test_a_creation_only_the_wider_reading_finds_stops_whatever_the_consent_record(
    monkeypatch, capsys, repo, tmp_path, name
):
    """`questions.md` D10 of 1790993140 read consent first for these, as for
    every creation, and #734 found it read against the wrong clone. Since
    #826 the stop reads no consent record (`spec.md` In 3 of 1791270162): a
    creation having run says nothing about whether this one is plain, and
    the plain retry meets §B, which reads its own clone's consent."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    assert wg.worktree_consent.record(str(session), "me")
    assert wg.worktree_consent.record(str(session / "w"), "me")
    decision, reason, _ = run(monkeypatch, capsys, WIDER_ONLY[name][0], session)
    assert decision == "ask", (name, decision, reason)


@pytest.mark.parametrize(
    "first", ["git checkout README.md && ", "git checkout nosuch; "]
)
def test_a_shape_in_a_clean_tree_takes_no_stop_from_one_in_a_dirty_tree(
    monkeypatch, capsys, repo, tmp_path, first
):
    """Round 1 of 1790993140, yellow 3, in #826's terms. The `checkout` in
    front is unrecognised in the clean session tree, which matters to nobody,
    and the switch behind the redirection is unrecognised in the dirty `w`.
    Each shape is judged in its own tree, so the second still stops, and the
    stop lists both. Silent at `9c03ae85`, where only the first unrecognised
    shape's tree was read."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    command = f"{first}cd w && 2>/dev/null {SWITCH}"
    decision, reason, top = run(monkeypatch, capsys, command, session)
    assert decision == "ask", (decision, reason)
    assert f"`2>/dev/null {SWITCH}`" in reason, reason
    assert f"`{first.split(' &&')[0].rstrip('; ')}`" in reason, reason
    assert top and os.path.samefile(top, session / "w"), top


def test_each_tree_is_placed_once_however_many_shapes_it_holds(
    monkeypatch, capsys, repo
):
    """#826, phase 3. Each unrecognised shape is judged in its own tree, and
    a tree is looked up once, so three `checkout`s in one clean tree cost one
    `repo_paths` for the stop, not three. Survived a break dropping the
    dedupe until this case; red with it dropped."""
    asked = []
    real = wg.repo_paths

    def counting(cwd):
        asked.append(cwd)
        return real(cwd)

    monkeypatch.setattr(wg, "repo_paths", counting)
    command = "git checkout a; git checkout b; git checkout c"
    decision, reason, _ = run(monkeypatch, capsys, command, repo)
    assert decision == "silent", (decision, reason)
    assert asked == [str(repo)], asked


def _redirections():
    """Every redirection `hooks/cmdline.py`'s `_REDIRECTION` names, as (operator,
    target) pairs, each operator once bare and, where it is not `&`-led, with
    a number and with bash 4.1's `{fd}` in front. Derived from the pattern, so
    an operator the reader learns is a new case the day it is added.

    Each operator takes every kind of target it has: a duplicating one a
    descriptor, `-` to close it and `1-` to move it, and every other one but
    a here-document's a word and the word `-`. A target ending in `-` is
    what `<<-` looks like, and round 1 of work item 1791270162 found
    `git worktree 2>&- add …` and `git worktree >- add …` listed where bash
    creates the worktree, because the generator gave `>&` and `<&` the
    target `1` alone."""
    pattern = wg.wide._REDIRECTION.pattern
    assert pattern.endswith(")"), pattern
    operators = pattern[pattern.rindex("(?:") + 3 : -1]
    pairs = []
    for op in (o.replace("\\", "") for o in re.split(r"(?<!\\)\|", operators)):
        if op in ("<<", "<<-"):
            targets = ["EOF"]
        elif op.endswith("&"):
            targets = ["1", "-", "1-"]
        else:
            targets = ["word" if op == "<<<" else "/dev/null", "-"]
        fds = [""] if op.startswith("&") else ["", "2", "{fd}"]
        pairs += [(fd + op, target) for fd in fds for target in targets]
    return pairs


def test_the_redirections_are_read_from_the_reader():
    """The generator below is only as wide as this list, and as its targets:
    a closed and a moved descriptor, and a word ending in `-`, among them."""
    pairs = _redirections()
    ops = {op for op, _target in pairs}
    assert {"&>", "&>>", ">&", "<&", "2>", "{fd}>", "<<<", ">|", ">!"} <= ops, ops
    assert len(ops) == 2 + 12 * 3, sorted(ops)
    assert {("2>&", "-"), (">&", "1-"), ("<&", "-"), (">", "-"), ("&>", "-")} <= set(
        pairs
    ), pairs


# Since #826: a verb that can move a branch or add a worktree, and a listed
# verb whose listing rests on a word after the subcommand.
MOVING = (
    "switch feature/x",
    "checkout feature/x",
    "checkout -b y",
    "worktree add ../wt b",
    "stash branch x",
)
LISTED = (
    "status",
    "checkout -- README.md",
    "worktree list",
    "stash",
    "stash push -m wip",
)


def _placed(verb):
    """`git <verb>` with every redirection `_redirections` gives, at every
    position, glued to the word before it and spaced, its target glued and
    spaced -- as `(command, at, glued, operator, spaced_target)`, where `at`
    is the index of the word of `git <verb>` the redirection stands before.

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
                    yield command, at, glued, op, spaced_target


def _read_by_the_guard(command):
    """What `main` acts on in COMMAND before any tree is read: each switch
    and creation the frozen segments hold, and every unrecognised shape, from
    a segment, a group a `&` cut apart, a substitution body or an
    untokenizable command. Empty where every git in it is listed."""
    text = wg._judgment_text(command)
    items, clean = wg._tokenize_with_separators(text)
    found = []
    for _sep, tokens in items:
        shape, finding = wg._segment_finding(tokens)
        if shape in ("switch", "creation"):
            found.append(shape)
        elif finding is not None:
            found.append(finding)
    found += [finding for _index, finding in wg._merged_findings(items)]
    return found + wg._command_findings(text, clean)


def test_no_redirection_makes_a_moving_verb_listed_wherever_it_stands():
    """#826, phase 3. For every operator `_REDIRECTION` names, at every
    position, glued to the word before it and spaced, its target glued and
    spaced, a verb that can move a branch or add a worktree is never read as
    listed: it is a switch, a creation, or an unrecognised shape the stop
    names. Red at `9c03ae85` on 208 of the 2,356 shapes, 104 each of `worktree
    add` and `stash branch`, whose deciding word a redirection stood in front
    of, was glued to, or cut away with an `&`: `worktree` and `stash` were
    listed by their subcommand alone (a deleted probe, phase 3). With the
    targets widened to a closed and a moved descriptor and a word ending in
    `-` (round 1, red 2), red at `4de95fa7` on 110 of 4,712 shapes, every one
    a target ending in `-` that `_plain_words` read as taking the next word
    (`git worktree 2>&- add`, `>-`, `<<<-`, `<>-`)."""
    silent = [
        command
        for verb in MOVING
        for command, *_where in _placed(verb)
        if not _read_by_the_guard(command)
    ]
    assert not silent, (len(silent), silent[:10])


def test_a_redirection_after_a_listed_verbs_words_keeps_it_listed():
    """The other direction, so the rule above cannot be met by stopping
    everything: a listed verb with any redirection written after its own
    words, glued or spaced, is still listed and costs no stop. `git stash
    2>/dev/null` hides no word, while `git stash 2>/dev/null branch x` does.
    One placement is left out, a redirection glued to the subcommand itself
    (`git status>/dev/null`): the frozen reading takes that word for the
    subcommand, and phase 2 made it a shape of its own whose rewrite moves
    the redirection (`questions.md` W3). Red at `9c03ae85` on 24 shapes, a
    path glued to its redirection after `--` read as no path, and on 96
    against this phase's first draft, which read `git worktree list>/dev/null`
    as hiding a word (a deleted probe and a run, phase 3)."""
    stopped = [
        (command, _read_by_the_guard(command))
        for verb in LISTED
        for command, at, glued, *_rest in _placed(verb)
        if at == len(verb.split()) + 1
        and not (glued and at == 2)
        and _read_by_the_guard(command)
    ]
    assert not stopped, (len(stopped), stopped[:10])


def _policy_text():
    """`docs/worktree-guard-spec.md`, whitespace folded so a wrapped sentence
    reads as one line."""
    path = os.path.join(
        os.path.dirname(__file__), "..", "docs", "worktree-guard-spec.md"
    )
    with open(path, encoding="utf-8") as f:
        return " ".join(f.read().split())


def test_the_guard_policy_says_which_shapes_reach_the_rows_and_who_reads_the_stop():
    """S12 of work item 1791270162, §14 of the agent contract: §A names the
    three shapes, the stop's two readers and its failure direction, in the
    sentences a person reads to learn when the guard stops. Red against the
    policy as it stood at `9c03ae85`."""
    text = _policy_text()
    for sentence in (
        "The guard does not predict whether a command switches a branch.",
        "A listed shape is silent in every tree state and spawns no git.",
        "**a switch** — `git switch`, whatever its words.",
        "In a clean tree nobody else is in, row 5 says nothing of a switch, "
        "and nothing is said of a shape that might be one.",
        "it is a `deny` to the model, which rewrites in the plain spelling "
        "and meets the rows above on the retry, and no person is asked.",
        "so the stop is a `deny` whoever is at the keyboard.",
        "The consent record is never read for the stop",
        "**The failure direction.** The guard stops more than it did",
        # Round 1 of work item 1791270162: red 1 and red 3, absent at
        # `4de95fa7`.
        "A `git switch` on the same line makes the stop a `deny` whoever is "
        "at the keyboard",
        "Every tree on the line is read before the stop is taken",
        "A `rebase` is listed unless it has two words that are not options, "
        "or `--root` and one",
    ):
        assert sentence in text, sentence


def test_the_guard_policy_says_nothing_is_read_past_the_base():
    """S12 of work item 1791270162: §*Which tree* keeps the frozen reading's
    paragraphs, says nothing is read past the base's words and why the
    readings left, and §*Known limits* holds the new limits and none of the
    removed ones. Red against the policy as it stood at `9c03ae85`."""
    text = _policy_text()
    assert "Nothing is read past the base's words since #826" in text
    assert "left with #826" in text
    for limit in (
        "A git subcommand this repository never ran",
        "A creation only a hidden spelling holds",
        "A `rebase` is listed, and detaches HEAD while it runs",
        "every unrecognised shape stops there, in every tree",
        # Round 1 of work item 1791270162, yellow 5 and yellow 4, absent at
        # `4de95fa7`.
        "A string handed to a shell (`sh -c`, `bash -c`, `eval`) is judged in "
        "the tree its segment names",
        "or either side of an `&` the splitter cut is the finding",
    ):
        assert limit in text, limit
    for gone in (
        "Two rules are read past the base.",
        "options are read from a static table",
        "name is looked up as git resolves it (§*Which tree*)",
        "the guard asks wherever a view's words hold a switch",
    ):
        assert gone not in text, gone


def test_a_hidden_switch_behind_a_judged_one_adds_no_question(
    monkeypatch, capsys, repo
):
    """The kind the frozen loop judged keeps its verdict: a clean single
    stream lets the switch through, and a second switch only the wider
    reading finds is not asked about. Since #826 the second is an
    unrecognised shape, and its tree is the same clean single-stream one, so
    it says nothing there either."""
    command = f"{SWITCH}; 2>/dev/null git switch main"
    decision, reason, top = run(monkeypatch, capsys, command, repo)
    assert decision == "silent", (decision, reason)
    assert top and os.path.samefile(top, repo), top


def test_a_hidden_creation_behind_a_judged_one_adds_no_question(
    monkeypatch, capsys, repo, tmp_path
):
    """The judged creation's own clone has consent, so its verdict is
    silence; a second creation only the wider reading finds is not asked
    about. Since #826 the second is an unrecognised shape judged in the tree
    its `-C` names, which is clean with nobody else in it, so it says
    nothing there."""
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert wg.worktree_consent.record(str(repo), "me")
    command = (
        f"git -C {repo} worktree add ../wt-a -b a && "
        f"git -C {repo} 2>&1 worktree add ../wt-b -b b"
    )
    decision, reason, _ = run(monkeypatch, capsys, command, elsewhere)
    assert decision == "silent", (decision, reason)


def test_a_wider_reader_that_exits_at_load_leaves_the_guard_reading(
    monkeypatch, tmp_path
):
    """Round 1 of 1790993140, white 5. A `hooks/cmdline.py` whose body raises
    `SystemExit` is a failure `hooks/dispatch.py` catches beside `Exception`,
    and the guard's import catches it too, so the guard still loads and keeps
    its own rows. Seen red with `except Exception:` alone.

    Since #826 what it keeps is the frozen reading's shapes, and a git only
    the missing reader could have read is the bare word's finding, a stop
    where the tree matters (`test_a_broken_wider_reader_costs_a_stop_never_a_silence`
    holds the verdicts). It asserted candidate C's empty answer."""
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
    assert module.shape_of(["git", "switch", "x"]) == "switch"
    assert module.shape_of(["noglob", "git", "switch", "x"]) == "unrecognised"


# One shape per position of Axis 3 of work item 1791119071, through `main()`,
# over the dirty `w`.
PLACED_SWITCHES = {
    "R0, a stuck value": "git checkout -by",
    "R1, between checkout and its name": "git checkout 2>/dev/null feature/x",
    "R3, glued to the name": "git checkout feature/x>/dev/null",
    "R4, between -b and its value": "git checkout -b 2>/dev/null y",
    "R4, glued to -b": "git checkout -b>/dev/null y",
    "R5, after the name": "git switch feature/x 2>/dev/null",
}


@pytest.mark.parametrize("name", sorted(PLACED_SWITCHES))
def test_a_switch_wherever_its_redirection_stands_is_stopped_in_a_dirty_tree(
    monkeypatch, capsys, repo, tmp_path, name
):
    """bash runs each as a switch (phase 1 of 1791119071, executed). All but
    R5 were silent at `94d7b2e0`. Since #826 R0-R4 are a `checkout` with no
    `-- <path>`, unrecognised and stopped in the dirty tree before the
    ladder, and R5 meets the ladder's dirty-tree row; both texts name the
    uncommitted changes, in the tree the segment names. It asserted the
    ladder's file list for all six."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, top = run(
        monkeypatch, capsys, f"cd w && {PLACED_SWITCHES[name]}", session
    )
    assert decision == "ask", (name, decision, reason)
    assert "uncommitted tracked changes" in reason, (name, reason)
    assert top and os.path.samefile(top, session / "w"), (name, top)


@pytest.mark.parametrize(
    "command",
    [
        "git checkout -- f.txt 2>/dev/null",
        "git checkout -- 2>/dev/null f.txt",
        "git checkout --conflict 2>/dev/null merge -- f.txt",
    ],
)
def test_a_restore_with_its_dashes_stays_silent_wherever_its_redirection_stands(
    monkeypatch, capsys, repo, tmp_path, command
):
    """The tree used to tell the file from the branch (`plan.md` Alternatives
    A of 1791119071); since #826 the `--` does, and a redirection among the
    words after it is no path, so a restore with a path after its `--` keeps
    its silence in the dirty `w`. It asserted the silence of the same three
    restores without their `--`, which are unrecognised now."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, _ = run(monkeypatch, capsys, f"cd w && {command}", session)
    assert decision == "silent", (command, decision, reason)


def test_a_message_search_over_a_dirty_tree_is_asked(
    monkeypatch, capsys, repo, tmp_path
):
    """`spec.md` A3 of 1791163981, #790's own shape through `main()`: `git
    checkout ':/<message>'` detaches at the newest commit whose message
    matches, so it moves a dirty tree. Red at `a3aa139a`, where it was
    silent. Since #826 nothing is looked up: a `checkout` with no `-- <path>`
    is unrecognised and stopped in the dirty tree, so the search matching
    nothing, which git refuses, is stopped too, where it used to be silent
    because the lookup found nothing. Its plain spelling is `git switch
    --detach ':/<message>'`, which the stop names."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    for search in ("':/base'", "':/nomatch-xyz'"):
        decision, reason, top = run(
            monkeypatch, capsys, f"cd w && git checkout {search}", session
        )
        assert decision == "ask", (search, decision, reason)
        assert "git switch --detach <rev>" in reason, reason
        assert top and os.path.samefile(top, session / "w"), (search, top)


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
# The property outlived the reading it was written against: a `checkout` in
# front, in a clean tree, takes no stop away from a switch behind it in a
# second, dirty tree (🟡 3). #790's lookups are gone since #826, and the
# `checkout` is an unrecognised shape judged in its own tree.


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
    """Round 1 of 1791163981, 🟡 3. A `checkout` in a clean single-session
    tree stands in front of a switch in a second, dirty tree. `a3aa139a`
    read no switch in front, so it judged the second tree's switch, or
    candidate C asked about it; the guard still asks. The two `:/base` cases
    were red at `85e77dc8`, where the checkout took the slot and C's question.

    Since #826 the `checkout` is unrecognised in the clean tree, which takes
    no stop, and the switch behind it is judged in `other`: by the ladder
    where the frozen reading reads it, and as an unrecognised shape in its
    own tree where only the wider reading does. The second pair was silent at
    `9c03ae85`, where only the first unrecognised shape's tree was read."""
    other = _a_dirty_clone_beside(repo, tmp_path)
    command = f"{front} && {behind.format(other=other)}"
    decision, reason, _ = run(monkeypatch, capsys, command, repo)
    assert decision == "ask", (command, decision, reason)
