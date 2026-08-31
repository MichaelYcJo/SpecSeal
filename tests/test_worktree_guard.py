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
    (repo / "f.txt").write_text("changed\n")
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
    """The verdict here steered to `git switch`, which an Agent call cannot
    run, while the reason's own first line already named the right way on."""
    _, reason = agent_verdict(monkeypatch, capsys, repo, "review the diff")
    assert "git switch -c" not in reason
    assert "isolation" in reason


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
    (repo / "f.txt").write_text("changed\n")
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
    (lambda d: open(f"{d}/other-session", "w").write("1"))(lease_dir(repo))
    live, unattributable = wg.fresh_leases(str(repo), "me")
    assert live == []
    assert len(unattributable) == 1 and "[lease: other-se" in unattributable[0][1]


def test_own_lease_is_ignored(repo):
    (lambda d: open(f"{d}/me", "w").write("1"))(lease_dir(repo))
    assert wg.fresh_leases(str(repo), "me") == ([], [])


def test_stale_lease_is_ignored(repo):
    import os
    import time

    d = lease_dir(repo)
    open(f"{d}/old-session", "w").write("1")
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
