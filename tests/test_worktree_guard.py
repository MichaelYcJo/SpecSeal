"""worktree-guard: command classification, decision matrix, lease detection.

Decision tests stub session detection — CI runners have no claude processes,
which would otherwise push every branch switch into the conservative-deny
path and hide the logic under test.
"""

import json
import os

import pytest
from conftest import load_hook_module

wg = load_hook_module("worktree-guard.py", "wg")

ACTIVE = [(111, "/tree", 1.0, 0.5, "VS Code")]
IDLE = [(222, "/tree", 400.0, 90.0, "Terminal")]


def reason_for(cmd, cwd):
    """The verdict `main()` would reach for `cmd`, without the session half.

    `split_command` returns segments as TOKEN LISTS, so classification and the
    quoting decision come from one place — a quoted sentence is a single token
    and can never arrive here as a command word.
    """
    segments, _clean = wg.split_command(cmd)
    for tokens in segments:
        got = wg.classify(tokens, cwd)
        if got:
            return got
    return None


# --- classify: what counts as a branch switch / worktree creation ---------


@pytest.mark.parametrize(
    "cmd,expected",
    [
        ("git switch feature/x", "switch"),
        ("git switch -c feature/y", "create+switch"),
        ("git switch -", "switch"),  # previous branch IS a switch
        ("git checkout -b feature/y", "create+switch"),
        ("git checkout -", "switch"),
        ("git worktree add ../wt feature/x", "worktree-add"),
        ("git worktree list", None),
        ("git worktree remove ../wt", None),
        ("echo git switch feature/x", None),  # prose mention, not a command
        ("cat > g.md <<EOF\nrun: git switch feature/x\nEOF", None),
        ("VAR=1 git switch feature/x", "switch"),  # env assignment prefix
        ("command git switch feature/x", "switch"),
        ("git status", None),
        # An unclosed apostrophe used to make shlex refuse the segment, and a
        # refused segment carried no classification at all.
        ("git switch feature/x  # don't ask", "switch"),
        ("git worktree add ../wt f  # user's call", "worktree-add"),
        ("git checkout -b feature/y  # don't rebase", "create+switch"),
        # A quoted string arrives as one token, so its contents can never
        # present themselves as a command word.
        ("echo don't switch feature/x", None),
        ('git commit -m "don\'t ship"', None),
        ("git worktree list  # what's open", None),
        # `split_segments` cuts on `;` inside quotes as well, so a quoted
        # sentence leaves a piece whose command word is literally `git`.
        # Measured before the whole command was handed down: an ordinary
        # commit denied with "attempting to create a worktree".
        ('echo "step 1; git switch feature/x"', None),
        ('git commit -m "see README; git worktree add ../wt f"', None),
        ('gh pr create --body "then; git switch feature/x"', None),
        ('git -C "my repo" switch b', "switch"),
        # An apostrophe on the command word or inside a `-C` value used to
        # defeat classification outright; the quote-aware splitter reads them.
        ("git -C 'my repo' switch b  # don't", "switch"),
        ("'git' switch main  # don't", "switch"),
        ("FOO='a b' git switch main  # don't", "switch"),
        # A quoted sentence is one token, so its `;` no longer opens a segment.
        ('echo "a; git switch feature/x; b"', None),
    ],
)
def test_classify(repo, cmd, expected):
    assert reason_for(cmd, str(repo)) == expected


def test_classify_checkout_of_existing_file_is_restore(repo):
    assert reason_for("git checkout f.txt", str(repo)) is None


def test_classify_checkout_dwim_remote_branch(repo, tmp_path):
    import subprocess

    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(repo), str(clone)], check=True)
    # feature/x exists only as origin/feature/x in the clone
    subprocess.run(
        ["git", "-C", str(clone), "branch", "-Dq", "feature/x"], capture_output=True
    )
    assert reason_for("git checkout feature/x", str(clone)) == "switch"


# --- decision matrix (session detection stubbed) --------------------------


def decide(
    monkeypatch, capsys, repo, command, sessions=([], [], True), session_id="me"
):
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": sessions)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": session_id,
            "tool_input": {"command": command},
            "cwd": str(repo),
        },
    )
    try:
        wg.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out.strip()
    if not out:
        return "silent", ""
    d = json.loads(out)["hookSpecificOutput"]
    return d["permissionDecision"], d["permissionDecisionReason"]


def test_switch_clean_single_allows(monkeypatch, capsys, repo):
    assert decide(monkeypatch, capsys, repo, "git switch feature/x")[0] == "silent"


def test_switch_dirty_single_asks(monkeypatch, capsys, repo):
    (repo / "f.txt").write_text("changed\n", encoding="utf-8")
    assert decide(monkeypatch, capsys, repo, "git switch feature/x")[0] == "ask"


def test_switch_active_session_denies(monkeypatch, capsys, repo):
    decision, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=(ACTIVE, [], True)
    )
    assert decision == "deny"
    assert "VS Code" in reason  # host app attribution shown


def test_switch_idle_sessions_offer_both_ways_on(monkeypatch, capsys, repo):
    decision, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=([], IDLE, True)
    )
    assert decision == "deny"
    assert "terminal in/out" in reason  # disaggregated signals, English default
    assert "AskUserQuestion" in reason
    assert "[shared-tree-ok]" in reason and "worktree" in reason


def test_the_second_attempt_gets_the_plain_prompt(monkeypatch, capsys, repo):
    """The deny fires once per session per repo. Without that, a session whose
    answer the guard cannot read off the command would be stuck denying."""
    assert (
        decide(
            monkeypatch, capsys, repo, "git switch feature/x", sessions=([], IDLE, True)
        )[0]
        == "deny"
    )
    decision, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=([], IDLE, True)
    )
    assert decision == "ask"
    assert "Approve" in reason and "Deny" in reason


def test_a_second_session_is_offered_the_choice_too(monkeypatch, capsys, repo):
    for session in ("me", "other"):
        assert (
            decide(
                monkeypatch,
                capsys,
                repo,
                "git switch feature/x",
                sessions=([], IDLE, True),
                session_id=session,
            )[0]
            == "deny"
        ), session


def test_without_a_session_id_it_asks_instead_of_denying(monkeypatch, capsys, repo):
    """Nowhere to record the question means a deny that repeats forever."""
    assert (
        decide(
            monkeypatch,
            capsys,
            repo,
            "git switch feature/x",
            sessions=([], IDLE, True),
            session_id="",
        )[0]
        == "ask"
    )


# --- [shared-tree-ok]: the retry the shared-tree answer never had ---------


def test_the_token_carries_the_shared_tree_answer(monkeypatch, capsys, repo):
    """[worktree-ok] gave the worktree answer a way back through the guard.
    Without its mirror, a user who chose the shared tree met the same question
    one command later — the answer they had just given."""
    for sessions in (([], IDLE, True), ([], [], False)):
        assert (
            decide(
                monkeypatch,
                capsys,
                repo,
                "git switch feature/x  # [shared-tree-ok]",
                sessions=sessions,
            )[0]
            == "silent"
        ), sessions


def test_the_token_does_not_cross_an_active_session(monkeypatch, capsys, repo):
    """That deny protects a tree this session does not own, so a token from
    this session is not the other session's consent."""
    decision, reason = decide(
        monkeypatch,
        capsys,
        repo,
        "git switch feature/x  # [shared-tree-ok]",
        sessions=(ACTIVE, [], True),
    )
    assert decision == "deny"
    assert "AskUserQuestion" not in reason  # the block, not the choice


def test_a_quoted_separator_does_not_hide_a_real_token(monkeypatch, capsys, repo):
    """`split_segments` is a regex: it cuts on `;` and `|` inside quotes too,
    so the pieces held half a quote each, shlex refused them, and a token the
    user really gave read as absent. That landed on the single-stream deny —
    the one site with no budget and no `ask` behind it — where it repeated on
    every retry until the command itself was rewritten."""
    cmd = 'git worktree add ../wt -b b origin/main && echo "wip; go"  # [worktree-ok]'
    assert decide(monkeypatch, capsys, repo, cmd)[0] == "ask"


def test_the_split_option_carries_the_creation_token(monkeypatch, capsys, repo):
    """The reverse direction already handed back `# [shared-tree-ok]`. Without
    the mirror, following "split into a worktree" arrived at the creation site
    with a fresh budget and asked the question just answered."""
    _, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=([], IDLE, True)
    )
    split = next(
        line for line in reason.splitlines() if '"Split into a worktree"' in line
    )
    # BOTH forms — the existing-branch one and the new-branch one. Dropping the
    # token from only one still leaves it in the line.
    assert split.count("git worktree add") == split.count("[worktree-ok]") == 2
    # ...and the command it names is confirmed, not questioned again.
    assert (
        decide(
            monkeypatch,
            capsys,
            repo,
            "git worktree add ../wt/foo -b foo origin/main  # [worktree-ok]",
            sessions=([], IDLE, True),
        )[0]
        == "ask"
    )


def test_the_korean_prompt_has_no_english_left_in_it(monkeypatch, capsys, repo):
    """Naming both branch forms turned a bare command line into a sentence,
    and that sentence sat untranslated inside a Korean option."""
    from conftest import load_hook_module

    monkeypatch.setenv("SPECSEAL_LANG", "ko")
    wko = load_hook_module("worktree-guard.py", "wg_ko_opt")
    monkeypatch.setattr(wko, "sessions_in_tree", lambda top, own="": ([], [], False))
    monkeypatch.setattr(
        wko,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": "ko1",
            "tool_input": {"command": "git worktree add ../wt feature/x"},
            "cwd": str(repo),
        },
    )
    try:
        wko.main()
    except SystemExit:
        pass
    reason = json.loads(capsys.readouterr().out)["hookSpecificOutput"][
        "permissionDecisionReason"
    ]
    assert "for an existing branch" not in reason
    assert "기존 브랜치면" in reason


def agent_verdict(monkeypatch, capsys, repo, prompt, session="ag"):
    """One Agent call with isolation: "worktree" in a single-stream tree."""
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": ([], [], True))
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Agent",
            "session_id": session,
            "tool_input": {"isolation": "worktree", "prompt": prompt},
            "cwd": str(repo),
        },
    )
    try:
        wg.main()
    except SystemExit:
        pass
    out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
    return out["permissionDecision"], out["permissionDecisionReason"]


AGENT_PROMPTS = (
    "review the diff",
    "the user asked for this [worktree-ok] review the diff",
    "the user's request was isolation [worktree-ok]",
    "document what [worktree-ok] does in the readme",
)


def test_the_agent_verdict_does_not_depend_on_the_prompt(monkeypatch, capsys, repo):
    """The prompt is prose, and prose cannot separate a user asking for a
    worktree from a sentence mentioning the token. Reading it both ways was
    tried and taken back: a prompt that merely discussed `[worktree-ok]`
    switched the guard off, and one apostrophe in a prompt that really carried
    it dropped the call onto a deny telling it to add the token it already
    had — at a site with no budget and no confirmation behind it.

    Both paths end at a person anyway, so the token only ever bought
    deny -> ask. This path takes that step outright."""
    verdicts = {
        prompt: agent_verdict(monkeypatch, capsys, repo, prompt, session=f"ag{i}")
        for i, prompt in enumerate(AGENT_PROMPTS)
    }
    for prompt, (decision, _) in verdicts.items():
        assert decision == "ask", prompt
    # Decision AND reason: reading the token again would still land on `ask`,
    # by a different branch with a different reason. Identical output is what
    # says the prompt was never consulted.
    assert len(set(verdicts.values())) == 1, verdicts


def test_the_agent_prompt_names_the_way_on_an_agent_has(monkeypatch, capsys, repo):
    """An isolated agent's one way on is the confirmation. The reason once
    steered to `git switch`, which an Agent call cannot run, and then to
    calling the Agent again without isolation, which puts the agent in this
    session's tree while this session works there (#8). It names neither."""
    _, reason = agent_verdict(monkeypatch, capsys, repo, "review the diff")
    assert "git switch" not in reason
    assert "without isolation" not in reason
    assert "runs beside this session" in reason
    assert "Declining cancels this spawn." in reason


def test_the_agent_prompt_does_not_point_at_a_token_it_cannot_use(
    monkeypatch, capsys, repo
):
    """Naming a token this path no longer reads sends the model knocking on a
    door that does not exist."""
    _, reason = agent_verdict(monkeypatch, capsys, repo, "review the diff")
    assert "[worktree-ok]" not in reason


def test_a_token_inside_quoted_prose_is_not_consent(monkeypatch, capsys, repo):
    """A substring test read `echo 'we documented [shared-tree-ok] today'` as
    an answer and turned the guard off — the defect the commit gate had fixed
    for `[no-review]`, recurring where it costs more."""
    prose = "git switch feature/x && echo 'we documented [shared-tree-ok] today'"
    assert (
        decide(monkeypatch, capsys, repo, prose, sessions=([], IDLE, True))[0] == "deny"
    )


def test_the_worktree_token_follows_the_same_bare_word_rule(monkeypatch, capsys, repo):
    """Same test, the other token: prose must not downgrade the deny."""
    prose = "git worktree add ../wt feature/x && echo 'see [worktree-ok] notes'"
    decision, reason = decide(monkeypatch, capsys, repo, prose)
    assert decision == "deny"
    assert "AskUserQuestion" not in reason  # the single-stream steer, not a choice


def test_a_token_in_a_neighbouring_segment_still_counts(monkeypatch, capsys, repo):
    """The documented retry form is a trailing `# [shared-tree-ok]`, and a
    comment attaches to the last segment rather than the git one."""
    cmd = "git switch feature/x && echo done  # [shared-tree-ok]"
    assert (
        decide(monkeypatch, capsys, repo, cmd, sessions=([], IDLE, True))[0] == "silent"
    )


def test_a_session_id_with_separators_stays_inside_the_git_dir(
    monkeypatch, capsys, repo
):
    """Measured: `../../escaped` put an empty file at the repository root."""
    decide(
        monkeypatch,
        capsys,
        repo,
        "git switch feature/x",
        sessions=([], IDLE, True),
        session_id="../../escaped",
    )
    assert not (repo / "escaped").exists()
    assert (repo / ".git" / "specseal-worktree-choice" / "switch" / "escaped").is_file()


def test_an_unwritable_marker_counts_as_already_asked(monkeypatch, capsys, repo):
    """The rule both specs state: a marker that cannot be recorded means the
    question is treated as asked. Inverted, a deny repeats forever in exactly
    the environments that cannot write — and the session never gets through."""
    # A path that is unwritable on BOTH platforms, and inside the fixture.
    # `/proc/nonexistent-git-dir` was neither: on Windows it resolves under
    # the current drive and `os.makedirs` SUCCEEDS, so the marker was written,
    # the verdict came back `deny` instead of `ask`, and a real `C:\proc`
    # was left on the machine -- which then made `os.path.isdir("/proc")` true
    # in `test_worktree_guard_signals.py` and took two more cases down with
    # it. One test's choice of path, three failures.
    #
    # Occupying the marker directory's own name with a file is the same
    # `OSError` on every platform (`FileExistsError` here, and `makedirs`
    # re-raises it because the name is not a directory), and it says what it
    # is for.
    blocked = repo / ".git" / wg.CHOICE_DIR
    blocked.write_text("not a directory", encoding="utf-8")
    assert (
        decide(
            monkeypatch, capsys, repo, "git switch feature/x", sessions=([], IDLE, True)
        )[0]
        == "ask"
    )


def test_the_token_does_not_answer_the_dirty_tree_question(monkeypatch, capsys, repo):
    """Different question: the branch is the same either way, and what is
    being asked is whether the uncommitted changes ride along."""
    (repo / "f.txt").write_text("changed\n", encoding="utf-8")
    assert (
        decide(monkeypatch, capsys, repo, "git switch feature/x  # [shared-tree-ok]")[0]
        == "ask"
    )


def test_korean_locale_via_env(monkeypatch, capsys, repo):
    from conftest import load_hook_module

    monkeypatch.setenv("SPECSEAL_LANG", "ko")
    wko = load_hook_module("worktree-guard.py", "wg_ko")  # fresh load resolves LANG
    monkeypatch.setattr(wko, "sessions_in_tree", lambda top, own="": ([], IDLE, True))
    monkeypatch.setattr(
        wko,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": "me",
            "tool_input": {"command": "git switch feature/x"},
            "cwd": str(repo),
        },
    )
    try:
        wko.main()
    except SystemExit:
        pass
    reason = json.loads(capsys.readouterr().out)["hookSpecificOutput"][
        "permissionDecisionReason"
    ]
    assert "터미널 입력/출력" in reason


def test_locale_defaults_to_english_without_env(monkeypatch):
    from conftest import load_hook_module

    monkeypatch.delenv("SPECSEAL_LANG", raising=False)
    monkeypatch.setenv("LANG", "en_US.UTF-8")
    monkeypatch.delenv("LC_ALL", raising=False)
    weng = load_hook_module("worktree-guard.py", "wg_en")
    assert weng.LANG == "en"


def test_locale_follows_system_korean(monkeypatch):
    from conftest import load_hook_module

    monkeypatch.delenv("SPECSEAL_LANG", raising=False)
    monkeypatch.setenv("LC_ALL", "ko_KR.UTF-8")
    wko2 = load_hook_module("worktree-guard.py", "wg_ko2")
    assert wko2.LANG == "ko"


def test_switch_unreliable_detection_offers_both_ways_on(monkeypatch, capsys, repo):
    # A blanket deny once locked out every extension-hosted session (the
    # ancestor process isn't named `claude` there). It costs a choice now, and
    # the second attempt costs the plain confirmation it always did.
    decision, reason = decide(
        monkeypatch, capsys, repo, "git switch feature/x", sessions=([], [], False)
    )
    assert decision == "deny" and "AskUserQuestion" in reason
    assert (
        decide(
            monkeypatch, capsys, repo, "git switch feature/x", sessions=([], [], False)
        )[0]
        == "ask"
    )


def test_worktree_add_single_denies(monkeypatch, capsys, repo):
    assert (
        decide(monkeypatch, capsys, repo, "git worktree add ../wt feature/x")[0]
        == "deny"
    )


def test_worktree_add_user_tag_downgrades_to_ask_without_re_asking(
    monkeypatch, capsys, repo
):
    """`[worktree-ok]` is a completed confirmation coming back through the
    guard, so this site does NOT put the question again — declining the ask
    withdraws the token, which is the other way on. It was briefly a choice
    site, and that closed a ring: choosing "split into a worktree" at a switch
    site brings the model here carrying the token, to be asked whether it
    meant it."""
    cmd = "git worktree add ../wt feature/x  # [worktree-ok]"
    decision, reason = decide(monkeypatch, capsys, repo, cmd)
    assert decision == "ask"
    assert "AskUserQuestion" not in reason
    assert "[worktree-ok]" in reason  # declining withdraws it — say so


def test_the_token_site_does_not_spend_the_switch_questions_budget(
    monkeypatch, capsys, repo
):
    """Measured before the split: two round trips at the `[worktree-ok]` site
    left a later switch with the two-button prompt this work replaces."""
    decide(monkeypatch, capsys, repo, "git worktree add ../wt f  # [worktree-ok]")
    decide(monkeypatch, capsys, repo, "git worktree add ../wt f  # [worktree-ok]")
    assert (
        decide(
            monkeypatch, capsys, repo, "git switch feature/x", sessions=([], IDLE, True)
        )[0]
        == "deny"
    )


def test_each_direction_carries_its_own_question(monkeypatch, capsys, repo):
    """Answering in one direction must not answer for the other — for commands
    that carry NO token. A command that carries one is not a question at all
    (see the cross-direction test below), which is what keeps the two budgets
    from becoming two prompts for one decision."""
    for command in ("git worktree add ../wt feature/x", "git switch feature/x"):
        assert (
            decide(monkeypatch, capsys, repo, command, sessions=([], IDLE, True))[0]
            == "deny"
        ), command
    # ...and within a direction the budget is still spent exactly once.
    for command in ("git worktree add ../wt feature/x", "git switch feature/x"):
        assert (
            decide(monkeypatch, capsys, repo, command, sessions=([], IDLE, True))[0]
            == "ask"
        ), command


def test_worktree_add_active_session_asks(monkeypatch, capsys, repo):
    assert (
        decide(
            monkeypatch,
            capsys,
            repo,
            "git worktree add ../wt feature/x",
            sessions=(ACTIVE, [], True),
        )[0]
        == "ask"
    )


# --- leases: declared work streams ----------------------------------------


def lease_dir(repo):
    import subprocess

    gd = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    d = f"{gd}/specseal-leases"
    import os

    os.makedirs(d, exist_ok=True)
    return d


def test_fresh_foreign_lease_without_an_owner_is_unattributable(repo):
    """A bare-timestamp lease names no owner, so it is a question, not a deny.
    Owner-aware cases live in test_lease_liveness.py."""
    (lambda d: open(f"{d}/other-session", "w", encoding="utf-8").write("1"))(
        lease_dir(repo)
    )
    live, unattributable = wg.fresh_leases(str(repo), "me")
    assert live == []
    assert len(unattributable) == 1 and "[lease: other-se" in unattributable[0][1]


def test_own_lease_is_ignored(repo):
    (lambda d: open(f"{d}/me", "w", encoding="utf-8").write("1"))(lease_dir(repo))
    assert wg.fresh_leases(str(repo), "me") == ([], [])


def test_stale_lease_is_ignored(repo):
    import os
    import time

    d = lease_dir(repo)
    open(f"{d}/old-session", "w", encoding="utf-8").write("1")
    os.utime(f"{d}/old-session", (time.time() - 3600,) * 2)
    assert wg.fresh_leases(str(repo), "me") == ([], [])


# --- an apostrophe is not a waiver ----------------------------------------


@pytest.mark.parametrize(
    "command,sessions,expected",
    [
        ("git switch feature/x", (ACTIVE, [], True), "deny"),
        ("git worktree add ../wt f", ([], [], True), "deny"),
    ],
)
def test_a_comment_with_an_apostrophe_reaches_the_same_verdict(
    monkeypatch, capsys, repo, command, sessions, expected
):
    """`classify` returned None for a segment shlex refused, and `main()` reads
    no classification as nothing to guard. One unclosed apostrophe anywhere was
    enough, and an English comment supplies one: the switch that takes another
    session's branch and the worktree creation the single-stream rule exists to
    stop both went through with no verdict at all."""
    bare = decide(monkeypatch, capsys, repo, command, sessions=sessions)[0]
    assert bare == expected
    for comment in ("# don't ask", "# user's call", "# it's fine"):
        assert (
            decide(
                monkeypatch, capsys, repo, f"{command}  {comment}", sessions=sessions
            )[0]
            == expected
        ), comment


@pytest.mark.parametrize(
    "prefix,command,sessions,expected",
    [
        (
            "git status  # don't forget",
            "git worktree add ../wt f",
            ([], [], True),
            "deny",
        ),
        ("ls -la  # who's there", "git switch feature/x", (ACTIVE, [], True), "deny"),
        ("npm t  # it's slow", "git switch feature/x", (ACTIVE, [], True), "deny"),
    ],
)
def test_an_apostrophe_on_an_earlier_line_reaches_the_same_verdict(
    monkeypatch, capsys, repo, prefix, command, sessions, expected
):
    """The same hole as the test above, one line up. A comment ends at the
    newline and bash runs the next line; the splitter clears `commenters` so a
    retry token stays readable, and with it cleared the apostrophe in `don't`
    opens a quote that never closes. Everything after it — every LATER LINE —
    is swallowed into that string, so the command on line two produced no
    verdict at all while bash ran it.

    Judging what a command DOES now drops comments the way a shell does."""
    assert decide(monkeypatch, capsys, repo, command, sessions=sessions)[0] == expected
    joined = f"{prefix}\n{command}"
    assert decide(monkeypatch, capsys, repo, joined, sessions=sessions)[0] == expected


def test_a_hash_inside_a_word_is_not_a_comment(repo):
    """A shell opens a comment at the start of a WORD. `git switch feat#1`
    names a branch, and `git -C repo#2` names a repository — dropping from
    that `#` would silently retarget the verdict at `repo`."""
    assert wg.split_command("git switch feat#1")[0] == [["git", "switch", "feat#1"]]
    segments, clean = wg.split_command("git -C repo#2 switch b")
    assert clean
    assert wg.parse_git(segments[0])[2] == ["repo#2"]
    # And the comment form still loses its comment.
    assert wg.split_command("git switch b  # note")[0] == [["git", "switch", "b"]]


def test_a_separator_inside_a_quote_survives_the_comment_drop(
    monkeypatch, capsys, repo
):
    """Dropping the comment must not reopen the defect two rounds closed. The
    `git worktree add` here is inside `-m`'s double quotes, and it is still
    inside them after ` # don't forget` is gone."""
    cmd = 'git commit -m "step 1; git worktree add ../wt f" # don\'t forget'
    assert decide(monkeypatch, capsys, repo, cmd)[0] == "silent"


def test_the_unbalanced_quote_note_is_read_from_the_command_as_written(
    monkeypatch, capsys, repo
):
    """Two reads of the same string, and they must not be confused. The
    judgment read drops comments, so this command classifies cleanly. The
    consent read does not, because a `[worktree-ok]` is written in a comment
    on purpose — and here the apostrophe really would have swallowed one.

    Taking the note's condition from the judgment read instead would suppress
    it exactly where it is true, and the single-stream deny would go back to
    telling the user to append a token it cannot read."""
    cmd = "git worktree add ../wt f  # don't forget"
    assert wg.split_command(cmd)[1] is True
    assert wg.parses_cleanly(cmd) is False
    decision, reason = decide(monkeypatch, capsys, repo, cmd)
    assert decision == "deny"
    assert "unbalanced" in reason


def test_consent_is_not_read_out_of_a_command_that_did_not_parse(
    monkeypatch, capsys, repo
):
    """The commit gate falls back to a SUBSTRING test when a command does not
    parse cleanly (`has_marker`), and this guard must not inherit it. Reading
    `[no-review]` loosely skips one check the user is being asked about
    anyway; reading `[shared-tree-ok]` loosely turns this guard off with
    nobody asked — the regression two review rounds went into closing."""
    cmd = 'git worktree add ../wt f && echo "we agreed on [worktree-ok] yesterday'
    assert "[worktree-ok]" in cmd  # a substring test would say yes
    assert not wg.has_token(cmd, "[worktree-ok]")
    # Judged, and judged as single-stream: the token is still prose.
    assert decide(monkeypatch, capsys, repo, cmd)[0] == "deny"


def test_a_hidden_token_is_named_in_the_single_stream_deny(monkeypatch, capsys, repo):
    """The single-stream deny is the one verdict with no budget behind it, and
    its way past is "append [worktree-ok]". When a quote opens BEFORE the
    token, the splitter stops there and the token is genuinely lost — so that
    instruction tells the user to add what is already in the command. The
    reason names the quote instead."""
    decision, reason = decide(
        monkeypatch,
        capsys,
        repo,
        "git worktree add ../wt f  # \"don't forget [worktree-ok]",
    )
    assert decision == "deny"
    assert "unbalanced" in reason

    # Not shown where the token WAS read. The last two are the ones the
    # quote-aware splitter recovered: an apostrophe AFTER the token no longer
    # hides it, and neither does one inside a quoted phrase.
    for cmd in (
        "git worktree add ../wt f",
        "git worktree add ../wt f  # [worktree-ok]",
        'git worktree add ../wt -b b origin/main && echo "wip; go"  # [worktree-ok]',
        "git worktree add ../wt f  # [worktree-ok] ; echo \"don't",
        "git worktree add ../wt f  # [worktree-ok] but don't",
        "git worktree add ../wt f  # it's a 'nested [worktree-ok]",
    ):
        assert "unbalanced" not in decide(monkeypatch, capsys, repo, cmd)[1], cmd


def test_an_apostrophe_after_the_token_no_longer_hides_it(monkeypatch, capsys, repo):
    """This was the trap the previous fix could only paper over: the user gave
    `[worktree-ok]`, an apostrophe later in the same comment made it
    unreadable, and the deny told them to append what they had already
    written. The quote-aware splitter reads the token, so the verdict is the
    `ask` that a given token has always meant."""
    for cmd in (
        "git worktree add ../wt f  # [worktree-ok] but don't",
        "git worktree add ../wt f  # [worktree-ok] — it's concurrent work",
    ):
        assert decide(monkeypatch, capsys, repo, cmd)[0] == "ask", cmd


def test_the_C_target_follows_the_segment_that_was_judged(repo):
    """`main()` asks `segment_cwd` for the `-C` target of the very segment
    `classify` judged, from the same token list. Reading the two from separate
    tokenizations is how a switch aimed at another repository gets judged
    against THIS tree."""
    cmd = "git -C /x/y switch b  # don't"
    segments, _ = wg.split_command(cmd)
    assert wg.classify(segments[0], str(repo)) == "switch"
    # `normpath`, because `apply_chdir` ends in one: the assertion is that
    # the target followed the segment, not that this platform spells a path
    # with `/`.
    assert wg.segment_cwd(segments[0], "/base") == os.path.normpath("/x/y")


def test_a_quoted_sentence_does_not_become_a_git_invocation(monkeypatch, capsys, repo):
    """The recovery for a refused segment is reached only when the WHOLE
    command is refused. `split_segments` is a regex that cuts on `;` and `|`
    inside quotes too, so a quoted sentence leaves a piece whose command word
    is literally `git` — and `parse_git` cannot tell it from a real one.
    Measured: an ordinary commit was denied with "attempting to create a
    worktree", and its documented way past was to append `[worktree-ok]` to
    the commit. Writing an example command into a commit message is routine
    in this repository."""
    for cmd in (
        'echo "step 1; git switch feature/x"',
        'git commit -m "see README; git worktree add ../wt f"',
        'gh pr create --body "then; git switch feature/x"',
        'git commit -m "fix; git worktree add ../wt f" && echo ok',
        # The same four with an apostrophe added. A condition keyed on "does
        # the WHOLE command lex" answered these wrong, because both causes —
        # a separator inside quotes, and an unclosed quote — hold at once.
        'git commit -m "step 1; git worktree add ../wt f" # don\'t forget',
        'git commit -m "see README; git switch feature/x"  # user\'s call',
        'gh pr create --body "then; git switch feature/x"  # don\'t merge',
        'echo "step 1; git switch feature/x"  # it\'s fine',
    ):
        assert decide(monkeypatch, capsys, repo, cmd)[0] == "silent", cmd


def test_a_quoted_C_value_survives_an_apostrophe(repo):
    """A `-C` value with a space is what separates a quote-aware splitter from
    a whitespace one, and an apostrophe elsewhere in the command must not cost
    it. Both forms were unclassified before the guard borrowed the splitter."""
    for cmd, target in (
        ('git -C "my repo" switch b', "/base/my repo"),
        ("git -C 'my repo' switch b  # don't", "/base/my repo"),
    ):
        segments, _ = wg.split_command(cmd)
        assert wg.classify(segments[0], str(repo)) == "switch", cmd
        assert wg.segment_cwd(segments[0], "/base") == os.path.normpath(target), cmd


# --- #8: the Agent path is judged as concurrent, not counted ----------------

AGENT_STATES = {
    "single-stream": ([], [], True),
    "idle": ([], IDLE, True),
    "unreliable": ([], [], False),
    "active": (ACTIVE, [], True),
}


@pytest.mark.parametrize("state", sorted(AGENT_STATES))
def test_an_isolated_agent_asks_without_counting_sessions(
    monkeypatch, capsys, repo, state
):
    """S4. The agent runs beside this session, so the call is two work
    streams by construction, and a count of Claude sessions cannot see a
    subagent at all. At every tree state the answer is one confirmation with
    one reason: no choice-site deny, no *single-stream*, no instruction to
    drop `isolation`, and `sessions_in_tree` is never asked. `state` names the
    tree the count WOULD report, so a guard that still counted would answer
    differently across the four."""
    counted = []

    def count(top, own=""):
        counted.append(top)
        return AGENT_STATES[state]

    monkeypatch.setattr(wg, "sessions_in_tree", count)
    monkeypatch.setattr(
        wg,
        "load_input",
        lambda: {
            "tool_name": "Agent",
            "session_id": f"s4-{state}",
            "tool_input": {"isolation": "worktree", "prompt": "review the diff"},
            "cwd": str(repo),
        },
    )
    try:
        wg.main()
    except SystemExit:
        pass
    out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
    reason = out["permissionDecisionReason"]
    assert out["permissionDecision"] == "ask", state
    assert "runs beside this session" in reason
    assert "single-stream" not in reason
    assert "without isolation" not in reason
    assert "AskUserQuestion" not in reason
    assert counted == [], "the Agent path counted sessions"


AGENT_REASON_EN = (
    'The Agent tool was called with isolation: "worktree" (the harness creates a '
    "worktree at <repo>/.claude/worktrees/<name>). The agent runs beside this "
    "session, so it is concurrent work and a separate tree is the right shape "
    "for it. Creating a worktree still takes the user's confirmation once per "
    "session. Declining cancels this spawn."
)
AGENT_REASON_KO = (
    'Agent 툴을 isolation: "worktree" 로 호출했습니다(하네스가 '
    "<repo>/.claude/worktrees/<name> 에 worktree 를 만듭니다). 이 agent 는 이 "
    "세션과 나란히 돌기 때문에 동시 작업이고, 별도 트리가 맞는 모양입니다. 다만 "
    "worktree 생성은 세션마다 한 번 사용자 확인을 거칩니다. 거부하면 이번 호출이 "
    "취소됩니다."
)


def _reasons(monkeypatch, capsys, repo, module):
    """The Agent `ask` reason and the `[worktree-ok]` row's reason."""
    monkeypatch.setattr(module, "sessions_in_tree", lambda top, own="": ([], [], True))
    reasons = []
    for payload in (
        {
            "tool_name": "Agent",
            "session_id": "s10",
            "tool_input": {"isolation": "worktree", "prompt": "x"},
            "cwd": str(repo),
        },
        {
            "tool_name": "Bash",
            "session_id": "s10",
            "tool_input": {"command": "git worktree add ../wt f  # [worktree-ok]"},
            "cwd": str(repo),
        },
    ):
        monkeypatch.setattr(module, "load_input", lambda payload=payload: payload)
        try:
            module.main()
        except SystemExit:
            pass
        reasons.append(
            json.loads(capsys.readouterr().out)["hookSpecificOutput"][
                "permissionDecisionReason"
            ]
        )
    return reasons


def test_the_two_reworded_reasons_are_pinned_in_both_languages(
    monkeypatch, capsys, repo
):
    """S10, §14. The Agent reason is pinned whole. The `[worktree-ok]` row's
    first sentence starts from what was counted -- no Claude session shown to
    be working -- where a count was taken, instead of asserting *single-stream
    work*, which a worktree a subagent chain will use is not.

    #624.3: *No other Claude session is working in this tree* was false where
    the count found idle sessions, and that row is reached above the idle
    choice row. *Can be shown to be working* is true with nobody counted and
    with only idle sessions counted, so one sentence serves both."""
    agent, token = _reasons(monkeypatch, capsys, repo, wg)
    assert agent == AGENT_REASON_EN
    assert (
        "No other Claude session can be shown to be working in this tree, but "
        "[worktree-ok]" in token
    )
    assert "No other Claude session is working" not in token
    assert "Single-stream work" not in token

    monkeypatch.setenv("SPECSEAL_LANG", "ko")
    wko = load_hook_module("worktree-guard.py", "wg_s10_ko")
    agent, token = _reasons(monkeypatch, capsys, repo, wko)
    assert agent == AGENT_REASON_KO
    assert (
        "이 트리에서 작업 중임이 확인되는 다른 Claude 세션은 없지만 [worktree-ok]"
        in token
    )
    assert "작업 중인 다른 Claude 세션은 없지만" not in token
    assert "단건 작업이지만" not in token


def test_the_token_rows_count_sentence_is_said_only_where_a_count_was_taken(
    monkeypatch, capsys, repo
):
    """Round 1, finding 4. The `[worktree-ok]` row is reached before the
    choice rows, so the detection-unusable state reaches it, and there nothing
    was counted. *No other Claude session can be shown to be working in this
    tree* is a measurement, and it is printed only where the measurement was
    made -- which includes a count that found only idle sessions (#624.3)."""
    cmd = "git worktree add ../wt f  # [worktree-ok]"
    for module, sentence in (
        (wg, "No other Claude session can be shown to be working in this tree"),
        (None, "이 트리에서 작업 중임이 확인되는 다른 Claude 세션은 없지만"),
    ):
        if module is None:
            monkeypatch.setenv("SPECSEAL_LANG", "ko")
            module = load_hook_module("worktree-guard.py", "wg_f4_ko")
        for sessions, said in (
            (([], [], True), True),
            (([], IDLE, True), True),
            (([], [], False), False),
        ):
            monkeypatch.setattr(
                module, "sessions_in_tree", lambda t, o="", s=sessions: s
            )
            monkeypatch.setattr(
                module,
                "load_input",
                lambda: {
                    "tool_name": "Bash",
                    "session_id": "f4",
                    "tool_input": {"command": cmd},
                    "cwd": str(repo),
                },
            )
            try:
                module.main()
            except SystemExit:
                pass
            out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
            assert out["permissionDecision"] == "ask", sessions
            assert (sentence in out["permissionDecisionReason"]) is said, sessions
            assert "[worktree-ok]" in out["permissionDecisionReason"]


def test_the_dirty_tree_row_names_what_was_measured(monkeypatch, capsys, repo):
    """#624.2. The switch ladder's tracked-changes row is reached in three
    states: single stream (nothing idle, detection reliable), and, under
    `[shared-tree-ok]`, only-idle and detection-unusable. It opened *Single-
    stream tree* in all three, which is a count the last two never took. There
    the lead says the token carried the user's answer; the list of changes and
    the verdict are unchanged. Both languages. Seen red at the base: the lead
    was *Single-stream tree* and no `[shared-tree-ok]` was named."""
    (repo / "f.txt").write_text("changed on purpose\n", encoding="utf-8")
    for module, single in (
        (wg, "Single-stream tree, so the switch is allowed"),
        (None, "이 트리는 단건 작업이라 브랜치 전환을 허용할 수 있지만"),
    ):
        if module is None:
            monkeypatch.setenv("SPECSEAL_LANG", "ko")
            module = load_hook_module("worktree-guard.py", "wg_624_2_ko")
        for n, (sessions, command, counted) in enumerate(
            (
                (([], [], True), "git switch other", True),
                (([], IDLE, True), "git switch other  # [shared-tree-ok]", False),
                (([], [], False), "git switch other  # [shared-tree-ok]", False),
            )
        ):
            monkeypatch.setattr(
                module, "sessions_in_tree", lambda t, o="", s=sessions: s
            )
            monkeypatch.setattr(
                module,
                "load_input",
                lambda command=command, n=n: {
                    "tool_name": "Bash",
                    "session_id": f"d{n}",
                    "tool_input": {"command": command},
                    "cwd": str(repo),
                },
            )
            try:
                module.main()
            except SystemExit:
                pass
            out = json.loads(capsys.readouterr().out)["hookSpecificOutput"]
            reason = out["permissionDecisionReason"]
            assert out["permissionDecision"] == "ask", (sessions, reason)
            assert reason.startswith(single) is counted, (sessions, reason)
            assert "f.txt" in reason, reason
            if not counted:
                first = reason.splitlines()[0]
                assert first.startswith("[shared-tree-ok]"), first


def test_a_git_command_inside_a_heredoc_body_is_not_judged(monkeypatch, capsys, repo):
    """#243's phase 3 measured `docs/worktree-guard-spec.md` §*Known limits*'s
    old first line -- *a heredoc line that IS exactly a git command still
    matches* -- and found it closed: `_judgment_text` drops heredoc bodies, so
    a body line is data. The line was deleted and this is what holds it, in a
    tree where a real switch would be denied."""
    monkeypatch.setattr(wg, "sessions_in_tree", lambda t, o="": (ACTIVE, [], True))
    for command, want in (
        ("cat > notes.txt <<'EOF'\ngit switch feature/x\nEOF", None),
        ("cat > notes.txt <<EOF\ngit worktree add ../wt f\nEOF", None),
        ("git switch feature/x", "deny"),
    ):
        monkeypatch.setattr(
            wg,
            "load_input",
            lambda command=command: {
                "tool_name": "Bash",
                "session_id": "hd",
                "tool_input": {"command": command},
                "cwd": str(repo),
            },
        )
        try:
            wg.main()
        except SystemExit:
            pass
        out = capsys.readouterr().out.strip()
        got = (
            json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else None
        )
        assert got == want, (command, out)


# --- #826: a listed shape is silent, and the rest stop where the tree matters --
#
# `spec.md` S1, S3, S4, S8 and S9 of work item 1791270162. The guard no longer
# predicts a switch from a command's words: it lets through a git command it
# knows leaves the branch where it is, sends a `git switch` to the ladder, and
# stops every other git shape, but only in a tree where a switch would matter.

STOP = "does not know to leave the branch where it is"

# The five tree states of `docs/worktree-guard-spec.md` §A, as the stub of
# `sessions_in_tree` and whether `f.txt` carries an uncommitted change.
STATES = {
    "active": ((ACTIVE, [], True), False),
    "idle": (([], IDLE, True), False),
    "unusable": (([], [], False), False),
    "dirty": (([], [], True), True),
    "clean": (([], [], True), False),
}


def in_state(monkeypatch, repo, state, module=None):
    """Put `repo` and the session stub into STATE, and return the stub."""
    sessions, dirty = STATES[state]
    (repo / "f.txt").write_text(
        "changed\n" if dirty else "one\ntwo\nthree\n", encoding="utf-8"
    )
    monkeypatch.setattr(module or wg, "sessions_in_tree", lambda top, own="": sessions)
    return sessions


def verdict(monkeypatch, capsys, cwd, command, session_id="me", module=None):
    """`main()`'s decision and reason for COMMAND run from CWD."""
    module = module or wg
    monkeypatch.setattr(
        module,
        "load_input",
        lambda: {
            "tool_name": "Bash",
            "session_id": session_id,
            "tool_input": {"command": command},
            "cwd": str(cwd),
        },
    )
    try:
        module.main()
    except SystemExit:
        pass
    out = capsys.readouterr().out.strip()
    if not out:
        return "silent", ""
    d = json.loads(out)["hookSpecificOutput"]
    return d["permissionDecision"], d["permissionDecisionReason"]


def pressed_root(tmp_path, repo):
    """A projects root holding session `me`'s `automation` answer for REPO,
    in the shape the harness writes it."""
    from test_the_guard_asks_once_per_session import ask_entries, write_transcript

    root = tmp_path / "pressed-projects"
    write_transcript(root, "me", ask_entries(repo))
    return root


# S1's shapes. Each is a git command that leaves HEAD's branch where it was,
# or a substitution whose body holds only such commands (P2 (a)).
LISTED = (
    "git status",
    "git diff",
    "git add -A",
    "git commit -m x",
    "git log",
    "git rev-parse HEAD",
    "git fetch",
    "git checkout -- README.md",
    "git checkout feature/x -- README.md",
    "git restore README.md",
    "git -C W status",
    "git worktree list",
    "git stash",
    "F=$(git diff --name-only)",
    "echo `git rev-parse HEAD`",
    "diff <(git show HEAD:f.txt) f.txt",
    "git log $(git rev-parse HEAD)",
)

# Where a redirection goes, glued or spaced, sampled rather than crossed.
REDIRECTED = (
    lambda c: c,
    lambda c: c + " 2>/dev/null",
    lambda c: c + " 2> /dev/null",
    lambda c: c + " >/dev/null 2>&1",
)


def test_a_listed_shape_is_silent_in_every_tree_and_spawns_nothing(
    monkeypatch, capsys, repo, tmp_path
):
    """S1. A listed shape says nothing in all five tree states, with and
    without the person's `automation` press, and runs no program at all: the
    tree is never read for it. A sampled product: every shape meets every
    state and both readers, with one redirection spelling each, rotated."""
    import subprocess

    calls = []
    real_run = subprocess.run

    def counting(*args, **kwargs):
        calls.append(args[0] if args else kwargs.get("args"))
        return real_run(*args, **kwargs)

    empty = tmp_path / "no-projects"
    empty.mkdir()
    pressed = pressed_root(tmp_path, repo)
    n = 0
    for press in (False, True):
        monkeypatch.setattr(
            wg.worktree_consent, "PROJECTS_ROOT", str(pressed if press else empty)
        )
        for state in STATES:
            in_state(monkeypatch, repo, state)
            for shape in LISTED:
                command = REDIRECTED[n % len(REDIRECTED)](shape)
                n += 1
                monkeypatch.setattr(subprocess, "run", counting)
                got = verdict(monkeypatch, capsys, repo, command)
                monkeypatch.setattr(subprocess, "run", real_run)
                assert got == ("silent", ""), (state, press, command, got)
                assert not calls, (state, press, command, calls)


# S3's shapes, each with a phrase of the plain spelling its stop must name.
UNRECOGNISED = {
    "git checkout feature/x": "`git switch <branch>`",
    "git checkout README.md": "`git restore <path>`",
    "git checkout -b y": "`git switch <branch>`",
    "git checkout --detach HEAD~1": "`git switch --detach <rev>`",
    "git checkout ':/fix'": "`git checkout -- <path>`",
    "git bisect start": "`git -C <scratch clone>`",
    "git update-ref refs/heads/y HEAD": "`git -C <scratch clone>`",
    "sh -c 'git switch x'": "rather than as a string",
    'bash -c "git checkout x"': "rather than as a string",
    'eval "git switch x"': "rather than as a string",
    "echo $(git switch x)": "outside the substitution",
    "2>/dev/null git switch x": "Write `git` first",
    "noglob git switch x": "Write `git` first",
    "git 2>&1 worktree add ../wt b": "after the command's own words",
    'git switch x && echo "unclosed': "`git commit -F <file>`",
    # W3: a redirection written after `git` is no subcommand.
    "git 2>/dev/null status": "after the command's own words",
    # P2 (a): a body is read through the same shapes, nested ones too.
    "echo $(echo $(git checkout x))": "`git switch <branch>`",
    "X=$(git symbolic-ref HEAD refs/heads/y)": "`git -C <scratch clone>`",
    "echo $(2>&1 git switch x)": "Write `git` first",
    # A `--` names a restore only with a path after it, and a redirection is
    # no path: git reads each of these as `feature/x --` and switches.
    "git checkout feature/x --": "`git switch <branch>`",
    "git checkout feature/x -- >/dev/null": "`git switch <branch>`",
    "git checkout feature/x -- > out.txt": "`git switch <branch>`",
    "git stash branch y": "`git -C <scratch clone>`",
    "git>/dev/null switch x": "Write `git` first",
    "2>&1 git switch x": "Write `git` first",
}


def test_an_unrecognised_shape_stops_where_the_tree_matters(monkeypatch, capsys, repo):
    """S3. Without the press, in each state where a switch would matter, the
    guard stops before the ladder and names the shape it read and the plain
    spelling it reads. An `ask` for the person, except in a tree another
    session is ACTIVE in, where `docs/worktree-guard-spec.md` §A row 1 denies
    a branch-form `checkout` outright and nobody is asked to approve it."""
    for state in ("active", "idle", "unusable", "dirty"):
        in_state(monkeypatch, repo, state)
        for command, rewrite in UNRECOGNISED.items():
            decision, reason = verdict(monkeypatch, capsys, repo, command)
            want = "deny" if state == "active" else "ask"
            assert decision == want, (state, command, decision, reason)
            assert STOP in reason, (state, command, reason)
            assert rewrite in reason, (state, command, reason)
            assert "LEAVES_THE_TREE" in reason, (state, command, reason)


def test_the_stop_names_the_shape_it_read(monkeypatch, capsys, repo):
    """S3: the shape as it was read, quoted, so the person and the model see
    which command on the line stopped it."""
    in_state(monkeypatch, repo, "dirty")
    for command, quoted in (
        ("git status && git checkout feature/x", "`git checkout feature/x`"),
        ("git update-ref refs/heads/y HEAD", "`git update-ref refs/heads/y HEAD`"),
        ("echo $(git switch x)", "`git switch x`"),
        ('sh -c "git switch x"', "`sh -c 'git switch x'`"),
    ):
        decision, reason = verdict(monkeypatch, capsys, repo, command)
        assert decision == "ask" and quoted in reason, (command, reason)
    # Each shape once, however often it is written, and the rest counted
    # past the fifth.
    decision, reason = verdict(
        monkeypatch, capsys, repo, "git checkout x; git checkout x; git status"
    )
    assert reason.count("`git checkout x`") == 1, reason
    six = "; ".join(f"git checkout b{n}" for n in range(6))
    decision, reason = verdict(monkeypatch, capsys, repo, six)
    assert "`git checkout b4`" in reason and "`git checkout b5`" not in reason
    assert "  · and 1 more" in reason, reason


def test_a_body_nested_past_the_bound_is_read_as_one_it_could_not_finish(
    monkeypatch, capsys, repo
):
    """P2 (a) reads a body inside a body, to the commit gate's depth; a body
    deeper than that stops rather than passing unread."""
    in_state(monkeypatch, repo, "dirty")
    command = "echo $(echo $(git status))"
    assert verdict(monkeypatch, capsys, repo, command) == ("silent", "")
    monkeypatch.setattr(wg, "BODY_DEPTH", 1)
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "ask" and "could not run" in reason, reason


def test_a_switch_carrying_a_cut_redirection_still_meets_the_ladder(
    monkeypatch, capsys, repo
):
    """`2>&1` cuts a segment at its `&`, and the glued-back view of a switch
    the frozen reading already read is that switch's, not a hidden one."""
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(monkeypatch, capsys, repo, "git switch feature/x 2>&1")
    assert decision == "ask" and STOP not in reason, reason
    assert "They will follow you onto the target branch" in reason, reason


def test_the_same_shapes_are_silent_in_a_clean_single_stream_tree(
    monkeypatch, capsys, repo
):
    """S4. §A row 5: nothing to protect, so nothing is asked, whatever the
    shape. The base asked about a hidden switch here (candidate C)."""
    in_state(monkeypatch, repo, "clean")
    for command in UNRECOGNISED:
        assert verdict(monkeypatch, capsys, repo, command) == ("silent", ""), command


def test_the_segments_tree_is_the_one_that_matters(monkeypatch, capsys, repo, tmp_path):
    """S8. The stop is judged in the tree the segment names: a `git -C` or a
    `cd` to a second clone is judged there, and a `cd` the walk cannot
    resolve falls back to the session's own tree (#686)."""
    import subprocess

    other = tmp_path / "w"
    subprocess.run(
        ["git", "clone", "-q", str(repo), str(other)], check=True, capture_output=True
    )
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": ([], [], True))
    named = (f"git -C {other} checkout x", f"cd {other} && git checkout x")
    unresolved = 'cd "$W" && git checkout x'

    (other / "f.txt").write_text("changed\n", encoding="utf-8")
    for command in named:
        decision, reason = verdict(monkeypatch, capsys, repo, command)
        assert decision == "ask" and STOP in reason, (command, reason)
    assert verdict(monkeypatch, capsys, repo, unresolved) == ("silent", "")

    (other / "f.txt").write_text("one\ntwo\nthree\n", encoding="utf-8")
    (repo / "f.txt").write_text("changed\n", encoding="utf-8")
    for command in named:
        assert verdict(monkeypatch, capsys, repo, command) == ("silent", ""), command
    decision, reason = verdict(monkeypatch, capsys, repo, unresolved)
    assert decision == "ask" and STOP in reason, reason

    # A `git -C` naming no repository touches no tree, and git refuses it:
    # silent even where every tree asked about holds an ACTIVE session.
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": (ACTIVE, [], True))
    nowhere = f"git -C {tmp_path / 'none'} checkout x"
    assert verdict(monkeypatch, capsys, repo, nowhere) == ("silent", "")


def test_an_unrecognised_shape_stops_before_a_switch_on_the_same_line(
    monkeypatch, capsys, repo
):
    """S9. The stop stops the whole line, so it comes first; a listed shape
    beside a switch leaves the switch to today's dirty-tree row alone."""
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(
        monkeypatch, capsys, repo, "git checkout README.md && git switch feature/x"
    )
    assert decision == "ask" and STOP in reason, reason
    assert "They will follow you onto the target branch" not in reason, reason
    decision, reason = verdict(
        monkeypatch, capsys, repo, "git status && git switch feature/x"
    )
    assert decision == "ask", reason
    assert "They will follow you onto the target branch" in reason, reason
    assert STOP not in reason, reason


def test_the_tree_is_read_once_for_both_kinds(monkeypatch, capsys, repo):
    """W2. A command holding an unrecognised shape and a switch in one tree
    reads that tree's sessions and its changes once each, and the ladder
    takes what the stop's question already read."""
    seen = {"sessions": 0, "changes": 0}
    real_changes = wg.tracked_changes

    def sessions(top, own=""):
        seen["sessions"] += 1
        return ([], [], True)

    def changes(cwd):
        seen["changes"] += 1
        return real_changes(cwd)

    monkeypatch.setattr(wg, "sessions_in_tree", sessions)
    monkeypatch.setattr(wg, "tracked_changes", changes)
    got = verdict(
        monkeypatch, capsys, repo, "git checkout README.md && git switch feature/x"
    )
    assert got == ("silent", "")
    assert seen == {"sessions": 1, "changes": 1}, seen


# W1: the stop's one text, both readers' endings, in both languages.
STOP_EN = (
    "This command holds a git command this guard does not know to leave the "
    "branch where it is, and in this tree a branch switch would matter: it has "
    "1 uncommitted tracked changes, which a switch would carry onto the other "
    "branch.\n"
    "\n"
    "  · `git checkout feature/x` — a `git checkout` with no `-- <path>`, which "
    "can switch a branch as well as restore a file. For a switch, write `git "
    "switch <branch>` or `git switch --detach <rev>`; for a restore, `git "
    "checkout -- <path>` or `git restore <path>`.\n"
    "\n"
    "The plain spellings are what this guard reads: a `git switch` then meets "
    "the branch-switch rules, and a git subcommand on the list passes. Name "
    "another tree with `git -C <dir>`. The list is `LEAVES_THE_TREE` in "
    "hooks/worktree-guard.py. "
)
STOP_KO = (
    "이 명령에는 브랜치를 그대로 둔다고 이 guard 가 확인하지 못한 git 명령이 "
    "있고, 이 트리에서는 브랜치 전환이 문제가 됩니다. 커밋되지 않은 추적 파일 "
    "변경이 1건 있고, 전환하면 이 변경이 다른 브랜치로 따라갑니다.\n"
    "\n"
    "  · `git checkout feature/x` — `-- <path>` 가 없는 `git checkout` 이라, "
    "파일을 되돌릴 수도 있지만 브랜치를 전환할 수도 있습니다. 전환이라면 `git "
    "switch <branch>` 나 `git switch --detach <rev>` 로, 파일 되돌리기라면 `git "
    "checkout -- <path>` 나 `git restore <path>` 로 쓰세요.\n"
    "\n"
    "이 guard 는 위의 평범한 표기를 읽습니다. `git switch` 는 브랜치 전환 "
    "규칙으로 판단하고, 목록에 있는 git 하위 명령은 그대로 통과합니다. 다른 "
    "트리는 `git -C <dir>` 로 지정하세요. 목록은 hooks/worktree-guard.py 의 "
    "`LEAVES_THE_TREE` 입니다. "
)
ENDINGS = {
    ("en", "ask"): "Approve to run it as written, or decline and re-issue it in "
    "a plain spelling.",
    ("en", "deny"): "Re-issue the command in a plain spelling.",
    ("ko", "ask"): "그대로 실행하려면 승인하고, 아니면 거부한 뒤 평범한 표기로 "
    "다시 실행하세요.",
    ("ko", "deny"): "평범한 표기로 다시 실행하세요.",
}


def test_the_stop_says_one_text_with_two_endings_in_both_languages(
    monkeypatch, capsys, repo, tmp_path
):
    """W1. The person's `ask` and the model's `deny` carry one text, and only
    the last sentence says which of them is reading it."""
    pressed = pressed_root(tmp_path, repo)
    empty = tmp_path / "no-projects"
    empty.mkdir()
    monkeypatch.setenv("SPECSEAL_LANG", "ko")
    wko = load_hook_module("worktree-guard.py", "wg_ko_stop")
    for lang, module, text in (("en", wg, STOP_EN), ("ko", wko, STOP_KO)):
        in_state(monkeypatch, repo, "dirty", module=module)
        for decision, root in (("ask", empty), ("deny", pressed)):
            monkeypatch.setattr(module.worktree_consent, "PROJECTS_ROOT", str(root))
            got = verdict(
                monkeypatch, capsys, repo, "git checkout feature/x", module=module
            )
            assert got == (decision, text + ENDINGS[lang, decision]), (lang, got)


def test_a_broken_wider_reader_costs_a_stop_never_a_silence(monkeypatch, capsys, repo):
    """W3. Where `hooks/cmdline.py` does not load, or one of its readers
    raises, the bare word `git` in a string, a substitution or a hidden
    position is the finding: a stop where the tree matters, never a silence.
    A plain git command is read by the frozen reading and is unaffected."""
    in_state(monkeypatch, repo, "dirty")
    hidden = (
        "sh -c 'git switch x'",
        'eval "git switch x"',
        "echo $(git switch x)",
        "git log $(git switch x)",
        "2>/dev/null git switch x",
    )
    monkeypatch.setattr(wg, "wide", None)
    for command in hidden:
        decision, reason = verdict(monkeypatch, capsys, repo, command)
        assert decision == "ask" and "could not run" in reason, (command, reason)
    assert verdict(monkeypatch, capsys, repo, "git status") == ("silent", "")
    monkeypatch.undo()

    in_state(monkeypatch, repo, "dirty")
    assert wg.wide is not None

    def boom(*args, **kwargs):
        raise RuntimeError("a shape nobody measured")

    for reader in ("reparsed_texts", "substitution_bodies", "parse_git"):
        monkeypatch.setattr(wg.wide, reader, boom)
    for command in hidden:
        decision, reason = verdict(monkeypatch, capsys, repo, command)
        assert decision == "ask" and "could not run" in reason, (command, reason)
