"""worktree-guard: command classification, decision matrix, lease detection.

Decision tests stub session detection — CI runners have no claude processes,
which would otherwise push every branch switch into the conservative-deny
path and hide the logic under test.
"""

import json
import os

import pytest
from conftest import load_hook_module, shell_probe

wg = load_hook_module("worktree-guard.py", "wg")

ACTIVE = [(111, "/tree", 1.0, 0.5, "VS Code")]
IDLE = [(222, "/tree", 400.0, 90.0, "Terminal")]


def reason_for(cmd):
    """The first shape `main()` would act on in `cmd`, without the session
    half: a switch, a creation or an unrecognised shape, and None where every
    segment is listed or no git at all.

    `split_command` returns segments as TOKEN LISTS, so the shape and the
    quoting decision come from one place — a quoted sentence is a single token
    and can never arrive here as a command word. Since #826 the shape is read
    from the words alone, so no repository is needed.
    """
    segments, _clean = wg.split_command(cmd)
    for tokens in segments:
        got = wg.shape_of(tokens)
        if got not in (None, "listed"):
            return got
    return None


# --- shape_of: what counts as a branch switch / worktree creation ---------


@pytest.mark.parametrize(
    "cmd,expected",
    [
        ("git switch feature/x", "switch"),
        ("git switch -c feature/y", "switch"),
        ("git switch -", "switch"),  # previous branch IS a switch
        # A `checkout` with no `-- <path>` is unrecognised: its stop names
        # `git switch` and `git checkout -- <path>` (#826).
        ("git checkout -b feature/y", "unrecognised"),
        ("git checkout -", "unrecognised"),
        ("git worktree add ../wt feature/x", "creation"),
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
        ("git worktree add ../wt f  # user's call", "creation"),
        ("git checkout -b feature/y  # don't rebase", "unrecognised"),
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
def test_shape_of(cmd, expected):
    assert reason_for(cmd) == expected


def test_a_checkout_restores_by_its_dashes_and_not_by_the_tree(repo):
    """#826. `git checkout f.txt` used to be a restore because `f.txt` exists
    in the tree and no ref has its name. The tree is no longer read: the same
    words name a branch as easily as a file, so they are unrecognised, and
    the `--` is what makes a restore."""
    assert (repo / "f.txt").exists()
    assert reason_for("git checkout f.txt") == "unrecognised"
    assert reason_for("git checkout -- f.txt") is None


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
    """A token inside a quote that never closes is prose, and no consent
    read takes it: `hooks/tokens.py#given` reads nothing from where a split
    fails (#868). Read loosely, `[shared-tree-ok]` would turn this guard off
    with nobody asked — the regression two review rounds went into closing."""
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
    whose shape it read, from the same token list. Reading the two from
    separate tokenizations is how a switch aimed at another repository gets
    judged against THIS tree."""
    cmd = "git -C /x/y switch b  # don't"
    segments, _ = wg.split_command(cmd)
    assert wg.shape_of(segments[0]) == "switch"
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
        assert wg.shape_of(segments[0]) == "switch", cmd
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
    a branch-form `checkout` outright and nobody is asked to approve it, and
    on a line holding a `git switch` the frozen reading reads, where
    approving would run the switch past the ladder (round 1 of work item
    1791270162, red 1)."""
    for state in ("active", "idle", "unusable", "dirty"):
        in_state(monkeypatch, repo, state)
        for command, rewrite in UNRECOGNISED.items():
            decision, reason = verdict(monkeypatch, capsys, repo, command)
            switch_on_line = command.startswith("git switch")
            want = "deny" if state == "active" or switch_on_line else "ask"
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
    beside a switch leaves the switch to today's dirty-tree row alone. The
    stop is a `deny` there: approving an `ask` would run the switch past the
    ladder (round 1 of work item 1791270162, red 1; an `ask` at
    `4de95fa7`)."""
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(
        monkeypatch, capsys, repo, "git checkout README.md && git switch feature/x"
    )
    assert decision == "deny" and STOP in reason, reason
    assert reason.endswith(
        "Re-issue the command in a plain spelling. Run the `git switch` as a "
        "command of its own, so the branch-switch rules judge its tree."
    ), reason
    assert "They will follow you onto the target branch" not in reason, reason
    decision, reason = verdict(
        monkeypatch, capsys, repo, "git status && git switch feature/x"
    )
    assert decision == "ask", reason
    assert "They will follow you onto the target branch" in reason, reason
    assert STOP not in reason, reason


def test_no_approval_runs_a_line_past_an_active_tree(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 1 of work item 1791270162, red 1. Approving the stop's `ask`
    runs every segment of the line. So a `git switch` on it, or an
    unrecognised shape in a second tree another session is ACTIVE in, put
    §A row 1's deny one approval away: each of these was an `ask` about the
    session tree's changes at `4de95fa7`, and the base denied the switches.
    The other direction holds too: with the second tree IDLE or its
    detection unusable and no switch on the line, the stop is still the
    person's `ask`, and its reason names each tree that matters (round 2,
    yellow 4)."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    in_state(monkeypatch, repo, "dirty")
    # None is W with detection unusable.
    for held, sessions in (
        (ACTIVE, (ACTIVE, [], True)),
        (IDLE, ([], IDLE, True)),
        (None, ([], [], False)),
    ):
        monkeypatch.setattr(
            wg,
            "sessions_in_tree",
            lambda top, own="", s=sessions: s if top.endswith("W") else ([], [], True),
        )
        for command in (
            f"git checkout f.txt && git -C {w} switch feature/x",
            f"git checkout f.txt && cd {w} && git switch feature/x",
            f"git update-ref refs/x HEAD && git -C {w} switch feature/x",
        ):
            decision, reason = verdict(monkeypatch, capsys, repo, command)
            assert decision == "deny", (held, command, decision, reason)
            assert "Run the `git switch` as a command of its own" in reason, reason
        for command in (
            f"git checkout f.txt && git -C {w} checkout feature/x",
            f"git checkout f.txt && cd {w} && git checkout feature/x",
        ):
            decision, reason = verdict(monkeypatch, capsys, repo, command)
            if held is ACTIVE:
                assert decision == "deny", (command, decision, reason)
                assert "another Claude session is actively working here" in reason
                assert "uncommitted tracked changes" not in reason, reason
                continue
            # Round 2, yellow 4: the reason names both trees, the session's
            # for its changes and W for its sessions or its detection. At
            # `3c9a1161` it named the session tree's changes alone.
            assert decision == "ask", (command, decision, reason)
            assert "uncommitted tracked changes" in reason, reason
            assert f"`{repo}`" in reason and f"`{w}`" in reason, reason
            if held is IDLE:
                assert "none of them can be shown to be working" in reason, reason
                assert "pid 222" in reason, reason
            else:
                assert "cannot be told in this environment" in reason, reason


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


# Round 2 of work item 1791270162, yellow 4: where more than one tree on the
# line matters and none is ACTIVE, the reason names each, first one first.
TREES_EN = (
    "This command holds a git command this guard does not know to leave the "
    "branch where it is, and in each of these trees a branch switch would "
    "matter:\n"
    "  `{repo}`: it has 1 uncommitted tracked changes, which a switch would "
    "carry onto the other branch.\n"
    "  `{w}`: whether another session works here cannot be told in this "
    "environment (process inspection is unavailable).\n"
    "\n"
)
TREES_KO = (
    "이 명령에는 브랜치를 그대로 둔다고 이 guard 가 확인하지 못한 git 명령이 "
    "있고, 아래 트리마다 브랜치 전환이 문제가 됩니다.\n"
    "  `{repo}`: 커밋되지 않은 추적 파일 변경이 1건 있고, 전환하면 이 변경이 "
    "다른 브랜치로 따라갑니다.\n"
    "  `{w}`: 이 환경에서는 프로세스를 조회할 수 없어, 다른 세션이 이 트리에서 "
    "작업 중인지 확인할 수 없습니다.\n"
    "\n"
)


def test_the_stop_names_each_tree_that_matters_in_both_languages(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of work item 1791270162, yellow 4. Approving the `ask` runs
    the line in every tree it names, so the person is shown each tree that
    matters and why, not only the first: at `3c9a1161` this reason named the
    session tree's changes alone."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    monkeypatch.setenv("SPECSEAL_LANG", "ko")
    wko = load_hook_module("worktree-guard.py", "wg_ko_trees")
    command = f"git checkout f.txt && git -C {w} checkout feature/x"
    for lang, module, text in (("en", wg, TREES_EN), ("ko", wko, TREES_KO)):
        in_state(monkeypatch, repo, "dirty", module=module)
        monkeypatch.setattr(
            module,
            "sessions_in_tree",
            lambda top, own="": (
                ([], [], False) if top.endswith("W") else ([], [], True)
            ),
        )
        decision, reason = verdict(monkeypatch, capsys, repo, command, module=module)
        assert decision == "ask", (lang, decision, reason)
        assert reason.startswith(text.format(repo=repo, w=w)), (lang, reason)
    # Two directories of one tree are one tree, and its reason reads as it
    # always did.
    (repo / "sub").mkdir()
    one_tree = "git checkout f.txt && cd sub && git checkout feature/x"
    decision, reason = verdict(monkeypatch, capsys, repo, one_tree)
    assert decision == "ask", (decision, reason)
    assert reason.startswith(STOP_EN.split("\n")[0]), reason


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


@pytest.mark.parametrize(
    "command", ["git worktree &>/dev/null add ../wt b", "2>&1 git switch feature/x"]
)
@pytest.mark.parametrize("broken", ["missing", "raising"])
def test_a_broken_reader_leaves_no_cut_group_silent(
    monkeypatch, capsys, repo, command, broken
):
    """Round 1 of work item 1791270162, yellow 4. The reader that glues an
    `&` cut back is `hooks/cmdline.py#merged_view`; where it did not load or
    raises, the cut is the finding. Silent at `4de95fa7` for three of the
    four, where `_merged_findings` returned nothing."""
    in_state(monkeypatch, repo, "dirty")
    if broken == "missing":
        monkeypatch.setattr(wg, "wide", None)
    else:

        def boom(*_a, **_k):
            raise RuntimeError("broken reader")

        monkeypatch.setattr(wg.wide, "merged_view", boom)
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "ask" and "could not run" in reason, (command, reason)


# A git an `&` cut, with its `-C` before the cut, after it, or on both sides
# of a chain of cuts. `{w}` is the second tree.
CUT_GROUPS = (
    "2>&1 git -C {w} switch feature/x",
    "2>&1 git -C {w} checkout feature/x",
    "git -C {w} worktree &>/dev/null add ../wt b",
    "git -C {w} worktree 2>&1 add ../wt b",
    "git -C {w} worktree 2>&1 >&2 add ../wt b",
    "git -C {w} stash &>/dev/null branch y",
    "git -C {w} stash 2>&1 branch y",
    "cd {w} && 2>&1 git switch feature/x",
    "cd {w} && git worktree 2>&1 add ../wt b",
)


def test_a_cut_group_is_judged_in_the_tree_its_own_c_names(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of work item 1791270162, red 2. A git an `&` cut was placed
    by the tokens of the group's last part, which carry no `-C`, so it was
    judged in the tree it was typed from: each row carrying its `-C` inside
    the group was silent at `3c9a1161` with the session's tree clean and `W`
    dirty or ACTIVE, where the base asked about `2>&1 git -C W switch` and
    `git -C W worktree &>/dev/null add` (round 2's report). The group is one
    command, run where its first part runs, so it is judged in the tree its
    own `-C` names; the two rows reached through a `cd` watch that
    directory."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    for state, want in (("dirty", "ask"), ("active", "deny")):
        sessions = (ACTIVE, [], True) if state == "active" else ([], [], True)
        (w / "f.txt").write_text(
            "changed\n" if state == "dirty" else "one\ntwo\nthree\n", encoding="utf-8"
        )
        monkeypatch.setattr(
            wg,
            "sessions_in_tree",
            lambda top, own="", s=sessions: s if top.endswith("W") else ([], [], True),
        )
        for group in CUT_GROUPS:
            command = group.format(w=w)
            decision, reason = verdict(monkeypatch, capsys, repo, command)
            assert decision == want and STOP in reason, (state, command, reason)


@pytest.mark.parametrize("broken", ["missing", "raising"])
def test_a_broken_reader_judges_a_cut_in_the_tree_before_it(
    monkeypatch, capsys, repo, tmp_path, broken
):
    """Round 2 of work item 1791270162, yellow 3. Where the reader that glues
    an `&` cut back is missing or raises, the cut is placed by the part
    before it, where the frozen reading finds a `-C`: `git -C W worktree
    2>&1 add ../wt b` asks with `W` dirty and the session's tree clean,
    silent at `3c9a1161`, which placed it by the part after. A `-C` after
    the cut (`2>&1 git -C W switch x`) only the broken reader could read, so
    that group is judged in the tree it was typed from: the limit
    `docs/worktree-guard-spec.md` §*Known limits* names."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    (w / "f.txt").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": ([], [], True))
    if broken == "missing":
        monkeypatch.setattr(wg, "wide", None)
    else:

        def boom(*_a, **_k):
            raise RuntimeError("broken reader")

        monkeypatch.setattr(wg.wide, "merged_view", boom)
    for group in CUT_GROUPS:
        command = group.format(w=w)
        decision, reason = verdict(monkeypatch, capsys, repo, command)
        if group.startswith("2>&1 git -C"):
            assert decision == "silent", (command, decision, reason)
        else:
            assert decision == "ask" and "could not run" in reason, (command, reason)


# Phase 1 of work item 1791270162, `phases/phase-1.md` §M1: every git
# subcommand the frozen reading yields over the recorded runs, as pairs
# holding it in cut 1 / cut 2. Phase 3 re-read cut 1 on the same definition
# and found the same table.
RECORDED = {
    "log": (2858, 3064),
    "status": (2609, 2848),
    "commit": (2014, 2149),
    "diff": (2028, 2127),
    "add": (1842, 1947),
    "rev-parse": (893, 961),
    "show": (651, 756),
    "push": (573, 607),
    "checkout": (532, 576),
    "grep": (385, 454),
    "fetch": (252, 276),
    "clone": (223, 243),
    "branch": (223, 236),
    "worktree": (152, 164),
    "switch": (120, 126),
    "merge-base": (98, 104),
    "config": (84, 100),
    "stash": (95, 99),
    "ls-tree": (55, 73),
    "tag": (46, 60),
    "ls-files": (56, 58),
    "merge": (52, 55),
    "ls-remote": (44, 47),
    "archive": (43, 47),
    "pull": (43, 44),
    "cat-file": (38, 41),
    "for-each-ref": (26, 40),
    "describe": (26, 27),
    "rev-list": (23, 24),
    "reset": (23, 23),
    "remote": (17, 19),
    "init": (17, 17),
    "update-ref": (13, 13),
    "merge-tree": (7, 11),
    "apply": (8, 11),
    "check-ignore": (10, 10),
    "restore": (6, 7),
    "clean": (5, 6),
    "reflog": (6, 6),
    "revert": (6, 6),
    "blame": (3, 5),
    "rm": (5, 5),
    "cherry-pick": (4, 4),
    "mv": (1, 2),
    "show-ref": (2, 2),
    "rebase": (2, 2),
    "diff-tree": (1, 2),
    "gc": (1, 1),
    "format-patch": (0, 1),
    "count-objects": (0, 1),
    "update-index": (1, 1),
    "help": (1, 1),
    "symbolic-ref": (1, 1),
    "shortlog": (1, 1),
}
# What the frame judges does not leave the branch (`spec.md` In 5), and the
# words that are a shape of their own rather than a list entry.
MOVERS = {"switch", "checkout", "worktree", "update-ref", "symbolic-ref", "bisect"}


def test_the_list_carries_its_counts_and_nothing_unmeasured():
    """S10 of work item 1791270162. `LEAVES_THE_TREE` is exactly the recorded
    subcommands that leave the branch, each beside the count phase 1
    measured, and holds none of the movers. Red with one count changed in
    the module's comment, and with `rebase` taken off the list."""
    import inspect
    import re

    listed = re.findall(
        r'^\s+"([\w-]+)",\s+#\s+(\d+)/(\d+)',
        inspect.getsource(wg).split("LEAVES_THE_TREE = frozenset(")[1].split(")")[0],
        re.M,
    )
    counts = {sub: (int(a), int(b)) for sub, a, b in listed}
    assert set(counts) == set(wg.LEAVES_THE_TREE), sorted(
        set(counts) ^ set(wg.LEAVES_THE_TREE)
    )
    assert counts == {s: n for s, n in RECORDED.items() if s not in MOVERS}
    assert not (MOVERS & wg.LEAVES_THE_TREE)


@pytest.mark.parametrize(
    "command",
    [
        "git rebase main feature/x",
        "git rebase --onto main main feature/x",
        "git rebase --root feature/x",
        "git rebase main feature/x 2>/dev/null",
        # Round 2, red 1: revision spellings that are not options. git reads
        # a lone `-` as `@{-1}`, and every word after `--` as a revision, so
        # each of these switches (git 2.50.1); the first two and the last
        # were listed at `3c9a1161`.
        "git rebase - feature/x",
        "git rebase -i - feature/x",
        "git rebase --onto main - feature/x",
        "git rebase @{-1} feature/x",
        "git rebase main @{-1}",
        "git rebase -- main -x",
        # #854 (round 3 of work item 1791270162, yellow 1): git's other word
        # that ends the options, and a prefix of `--root`, which git takes as
        # `--root`. Each switches under git 2.50.1 and was listed at
        # `3d78c220`.
        "git rebase --ro feature/x",
        "git rebase --roo feature/x",
        "git rebase -i --ro feature/x",
        "git rebase --end-of-options main -x",
        # bash hands git `--root` once the redirection is off.
        "git rebase --root>/dev/null feature/x",
    ],
)
def test_a_rebase_naming_a_branch_is_unrecognised(monkeypatch, capsys, repo, command):
    """Round 1 of work item 1791270162, red 3. git switches to the named
    branch before it rebases, and HEAD stays there; listed and silent at
    `4de95fa7`. The stop names the plain spelling."""
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "ask" and STOP in reason, reason
    assert (
        "a `git rebase` naming a branch, which git switches to before it rebases. "
        "Write `git switch <branch>` first, then `git rebase <upstream>`." in reason
    ), reason


# #856: S11 of work item 1791384157. bash makes other words of each before git
# runs (`git rebase main feature/x`, `git rebase --ro --ro feature/x`, `git
# stash branch x`, `git worktree add ../wt f`), so the words the frozen
# reading read are not git's.
BRACE_SHAPES = (
    "git rebase {main,feature/x}",
    "git rebase --ro{,} feature/x",
    "git stash {branch,} x",
    "git worktree {add,} ../wt f",
)
BRACE_EN = (
    "a word holding a brace expansion (`{a,b}`, `{1..3}`), which the shell "
    "turns into other words before git reads them. Write the words out as the "
    "shell would make them, as in `git rebase main feature/x` for `git rebase "
    "{main,feature/x}`, or quote the braces where they are meant literally."
)
BRACE_KO = (
    "중괄호 확장(`{a,b}`, `{1..3}`)이 든 단어이며, 셸은 git 이 읽기 전에 이를 다른 "
    "단어들로 바꿉니다. 셸이 만들 단어를 직접 풀어 쓰세요. 예: `git rebase "
    "{main,feature/x}` 대신 `git rebase main feature/x`. 중괄호를 글자 그대로 쓰려면 "
    "따옴표로 감싸세요."
)


@pytest.mark.parametrize("command", BRACE_SHAPES)
def test_a_brace_expansion_in_a_git_word_is_unrecognised(
    monkeypatch, capsys, repo, tmp_path, command
):
    """S11 of work item 1791384157 (#856, the owner's answer (c) of
    2026-10-08). The shape stops where the tree matters, names the brace and
    its plain spelling, and is a `deny` in an ACTIVE tree and under the
    press; silent in a clean single-stream tree, like every unrecognised
    shape. Red at `5623d728`, where each was listed or a creation-free
    `worktree` and silent in every tree."""
    empty = tmp_path / "no-projects"
    empty.mkdir()
    monkeypatch.setattr(wg.worktree_consent, "PROJECTS_ROOT", str(empty))
    in_state(monkeypatch, repo, "active")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "deny" and STOP in reason, (command, decision, reason)
    assert f"`{command}` — {BRACE_EN}" in reason, reason
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "ask" and BRACE_EN in reason, (command, decision, reason)
    monkeypatch.setattr(
        wg.worktree_consent, "PROJECTS_ROOT", str(pressed_root(tmp_path, repo))
    )
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "deny" and BRACE_EN in reason, (command, decision, reason)
    in_state(monkeypatch, repo, "clean")
    assert verdict(monkeypatch, capsys, repo, command) == ("silent", "")


@pytest.mark.parametrize(
    "command",
    [
        "{git,} rebase main feature/x",
        "{,git} switch feature/x",
        # Round 2 of work item 1791384157, yellow 1: braces the guard does not
        # take apart, each run by bash as `git switch feature/x`. Red at
        # `e0c5a191`.
        "{{git,},} switch feature/x",
        "{,{git,}} switch feature/x",
        "{g..g}it switch feature/x",
        "${HOME}/bin/{git,} switch feature/x",
    ],
)
def test_a_brace_that_makes_the_command_word_is_unrecognised(
    monkeypatch, capsys, repo, tmp_path, command
):
    """#856's class, one instance further (round 1 of work item 1791384157,
    yellow 3): bash makes `git` itself of the brace, so the frozen reading
    reads no git and the guard said nothing in an ACTIVE tree. Red at
    `1680ea76`. Since round 2, a command word holding a brace the guard
    cannot take apart exactly is unrecognised whatever it makes, so the
    nested, sequence and `${…}`-adjacent spellings stop too, without the
    guard predicting what bash makes of them."""
    empty = tmp_path / "no-projects"
    empty.mkdir()
    monkeypatch.setattr(wg.worktree_consent, "PROJECTS_ROOT", str(empty))
    in_state(monkeypatch, repo, "active")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "deny" and STOP in reason and BRACE_EN in reason, reason
    in_state(monkeypatch, repo, "clean")
    assert verdict(monkeypatch, capsys, repo, command) == ("silent", "")


@pytest.mark.parametrize(
    "command",
    [
        "echo {a,b}",
        "ls {x,y}",
        "ls {x,y}.md && git status",
        "cat {.gitignore,README.md}",
        # Round 2: a command-word brace taken apart exactly that makes no git,
        # and braces in arguments, which make no command word whatever they
        # are.
        "{echo,printf} x",
        "echo {{a,b},c}",
        "echo {git,} x",
    ],
)
def test_a_brace_in_no_git_word_stays_silent(monkeypatch, capsys, repo, command):
    """The other side of yellow 3: a brace outside the command word stops
    nothing (`cat {.gitignore,README.md}`'s command word is `cat`), and a
    command-word brace the guard takes apart exactly stops only where one of
    its alternatives is `git`."""
    in_state(monkeypatch, repo, "dirty")
    assert verdict(monkeypatch, capsys, repo, command) == ("silent", "")


@pytest.mark.parametrize(
    "command",
    [
        "{{git,}} -C {w} switch feature/x",
        "{{git,}} -C {w} rebase main feature/x",
        "{{{{git,}},}} -C {w} switch feature/x",
    ],
)
def test_a_brace_command_word_is_judged_in_the_tree_its_c_names(
    monkeypatch, capsys, repo, tmp_path, command
):
    """Round 2 of work item 1791384157, yellow 2. The frozen reading reads
    no git in `{git,} -C W switch x`, so the brace finding was judged in the
    tree it was typed from and said nothing with `W` dirty and the session's
    tree clean. Its `-C` is read off the words after the brace word now, as
    git would read them. Red at `e0c5a191`."""
    import shutil

    w = tmp_path / "W"
    shutil.copytree(repo, w)
    (w / "f.txt").write_text("changed\n", encoding="utf-8")
    monkeypatch.setattr(wg, "sessions_in_tree", lambda top, own="": ([], [], True))
    decision, reason = verdict(monkeypatch, capsys, repo, command.format(w=w))
    assert decision == "ask" and STOP in reason, reason


@pytest.mark.parametrize(
    "command",
    [
        # A body is read with its own quoting.
        "echo $(git rebase {main,feature/x})",
        # A cut group is read whole, and the cut took the deciding word.
        "git worktree &>/dev/null {add,} ../wt f",
    ],
)
def test_a_brace_in_a_body_or_a_cut_group_is_unrecognised(
    monkeypatch, capsys, repo, command
):
    """S11 of work item 1791384157, the two places a git is read besides its
    own segment. Each stops in a dirty tree and names the brace. Both
    survived a break dropping the brace reading from their reader until
    these cases."""
    in_state(monkeypatch, repo, "dirty")
    decision, reason = verdict(monkeypatch, capsys, repo, command)
    assert decision == "ask" and BRACE_EN in reason, (command, decision, reason)


def test_a_broken_token_reader_reads_every_brace_as_unquoted(monkeypatch, capsys, repo):
    """S11 of work item 1791384157, its failure direction: where
    `hooks/tokens.py` did not load, the quoting cannot be read, so a quoted
    brace in a git word stops too, and an unquoted one still does. A broken
    reader costs a stop and never a silence. Survived a break answering no
    brace at all until this case."""
    monkeypatch.setattr(wg, "tokens", None)
    in_state(monkeypatch, repo, "dirty")
    for command in (BRACE_SHAPES[0], "git commit -m '{a,b}'"):
        decision, reason = verdict(monkeypatch, capsys, repo, command)
        assert decision == "ask" and BRACE_EN in reason, (command, decision, reason)


def test_the_brace_stop_reads_in_korean(monkeypatch, capsys, repo):
    """§14 for S11: the brace kind's own text in the second language."""
    monkeypatch.setenv("SPECSEAL_LANG", "ko")
    wko = load_hook_module("worktree-guard.py", "wg_ko_brace")
    in_state(monkeypatch, repo, "dirty", module=wko)
    decision, reason = verdict(monkeypatch, capsys, repo, BRACE_SHAPES[0], module=wko)
    assert decision == "ask" and BRACE_KO in reason, reason


@pytest.mark.parametrize(
    "command",
    [
        "git commit -m '{a,b}'",
        "git log --format='{%h}'",
        'git commit -m "{a, b}"',
        "git log --format=%h -- 'docs/{a,b}.md'",
        "git commit -m x && echo '{a,b}'",
        "git log ${x,}",
        # A brace GROUP holds whitespace and expands nothing, so a quoted
        # brace beside it stays quoted.
        "git commit -m '{a,b}' && { echo x,y; }",
    ],
)
def test_a_quoted_brace_in_a_git_word_stays_listed(monkeypatch, capsys, repo, command):
    """S12 of work item 1791384157: a brace the shell does not expand, because
    it is quoted, holds whitespace or is a parameter expansion, leaves the
    shape what it was, silent in every tree."""
    for state in STATES:
        in_state(monkeypatch, repo, state)
        got = verdict(monkeypatch, capsys, repo, command)
        assert got == ("silent", ""), (state, command, got)


@pytest.mark.parametrize(
    "command",
    [
        "git rebase main",
        "git rebase -i HEAD~3",
        "git rebase --continue",
        "git rebase --root",
        "git rebase main 2>/dev/null",
        "git rebase -",
        "git rebase -i -",
        "git rebase @{-1}",
        # #854: a long option starting `--r` that is no prefix of `--root`
        # stays an option, a prefix of `--root` alone names no branch, and
        # `--end-of-options` ends the options without being a word itself.
        "git rebase --rebase-merges main",
        "git rebase --reapply-cherry-picks main",
        "git rebase --ro",
        "git rebase --end-of-options main",
        # git refuses `--r` as ambiguous and `--roots` as unknown (exit 129,
        # git 2.50.1), and reads a `--ro` after the end of the options as a
        # revision, so none of them names a branch.
        "git rebase --r feature/x",
        "git rebase --roots feature/x",
        "git rebase --end-of-options --ro",
    ],
)
def test_a_rebase_of_the_current_branch_stays_listed(command):
    """The other direction: a `rebase` with one word that is not an option,
    or `--root` alone, rebases the branch HEAD is on and stays listed."""
    assert wg.shape_of(command.split()) == "listed"


# One form of each `LEAVES_THE_TREE` row, run against git by the case below:
# where the subcommand takes a branch, the form names one. `{start}` is the
# branch HEAD is on; `..` is the directory beside the repository.
FORMS = {
    "log": "log feature/x",
    "status": "status",
    "commit": "commit --allow-empty -qm x",
    "diff": "diff feature/x",
    "add": "add -A",
    "rev-parse": "rev-parse feature/x",
    "show": "show feature/x",
    "push": "push -q . feature/x:refs/heads/pushed",
    "grep": "grep one feature/x",
    "fetch": "fetch -q . feature/x:fetched",
    "clone": "clone -q . ../cloned{n}",
    "branch": "branch y feature/x",
    "merge-base": "merge-base {start} feature/x",
    "config": "config user.name x",
    "stash": "stash",
    "ls-tree": "ls-tree feature/x",
    "tag": "tag t feature/x",
    "ls-files": "ls-files",
    "merge": "merge -q --no-edit feature/x",
    "ls-remote": "ls-remote .",
    "archive": "archive -o ../a{n}.tar feature/x",
    "pull": "pull -q --no-rebase --no-edit . feature/x",
    "cat-file": "cat-file -t feature/x",
    "for-each-ref": "for-each-ref",
    "describe": "describe --always feature/x",
    "rev-list": "rev-list feature/x",
    "reset": "reset -q --hard feature/x",
    "remote": "remote add o .",
    "init": "init -q",
    "merge-tree": "merge-tree --write-tree {start} feature/x",
    "apply": "apply ../p.diff",
    "check-ignore": "check-ignore f.txt",
    "restore": "restore --source feature/x g.txt",
    "clean": "clean -fdq",
    "reflog": "reflog",
    "revert": "revert --no-edit HEAD",
    "blame": "blame f.txt",
    "rm": "rm -q --cached f.txt",
    "cherry-pick": "cherry-pick feature/x",
    "mv": "mv f.txt h.txt",
    "show-ref": "show-ref",
    "rebase": "rebase -q feature/x",
    "diff-tree": "diff-tree feature/x",
    "gc": "gc --auto",
    "format-patch": "format-patch -q -o ../p{n} {start}..feature/x",
    "count-objects": "count-objects",
    "update-index": "update-index --refresh",
    "help": "help -a",
    "shortlog": "shortlog -s feature/x",
}
# Forms git runs as a switch, each of which the guard must not list.
SWITCHING = (
    "rebase {start} feature/x",
    "rebase --onto {start} {start} feature/x",
    "rebase --root feature/x",
    "rebase - feature/x",
    # #854: a prefix of `--root`, and the two words that end git's options
    # before a branch named `-x`, which the template holds.
    "rebase --ro feature/x",
    "rebase --end-of-options {start} -x",
    "rebase -- {start} -x",
    "stash branch y",
    "checkout feature/x",
    "switch feature/x",
)
# #856: forms whose braces bash expands into other words before git runs,
# written for `str.format`. Each switches HEAD or adds a worktree under bash
# (S13 of work item 1791384157), and the guard reads none of them as listed.
BRACED = (
    "rebase {{{start},feature/x}}",
    "rebase --ro{{,}} feature/x",
    "stash {{branch,}} y",
    "worktree {{add,}} ../wt{n} feature/x",
)


def test_no_listed_form_moves_head_under_git(repo, tmp_path):
    """Binds `LEAVES_THE_TREE` to git (round 1 of work item 1791270162, red
    3): each row's form runs in a copy of a repository with a second commit
    on `feature/x` and a stash, and a form the guard reads as listed must
    leave HEAD naming the branch it named. Every row has a form, so a row
    added without one goes red, and each switching form must move HEAD
    under git, so the comparison cannot pass by measuring nothing. Red at
    `4de95fa7`, where `git rebase <start> feature/x` was listed.

    Every git the case runs must have run: a form git refused leaves HEAD
    where it was and would pass as listed unmeasured, on a runner whose git
    lacks an option (round 2 of work item 1791270162, white 5). `git
    check-ignore` exits 1 for a path it does not ignore, which is its form's
    answer."""
    import shutil
    import subprocess

    def git(d, *args, ok=0):
        done = subprocess.run(
            ["git", "-C", str(d), *args],
            capture_output=True,
            stdin=subprocess.DEVNULL,
            env={**os.environ, "GIT_EDITOR": "true", "GIT_PAGER": "cat"},
        )
        assert done.returncode == ok, (args, done.returncode, done.stderr)
        return done

    def head(d):
        return (d / ".git" / "HEAD").read_text(encoding="utf-8").strip()

    template = tmp_path / "template"
    shutil.copytree(repo, template)
    start = head(template).rsplit("/", 1)[-1]
    git(template, "switch", "-q", "feature/x")
    (template / "g.txt").write_text("g\n", encoding="utf-8")
    git(template, "add", "g.txt")
    git(template, "commit", "-qm", "g")
    git(template, "switch", "-q", start)
    # A branch whose name starts with `-`, which `git branch` refuses to
    # make; a word git reads as a revision only after `--` or
    # `--end-of-options` (#854).
    git(template, "update-ref", "refs/heads/-x", "HEAD")
    (template / "f.txt").write_text("changed\n", encoding="utf-8")
    (tmp_path / "p.diff").write_bytes(git(template, "diff").stdout)
    git(template, "stash", "-q")
    assert head(template) == f"ref: refs/heads/{start}"

    assert set(FORMS) == set(wg.LEAVES_THE_TREE), sorted(
        set(FORMS) ^ set(wg.LEAVES_THE_TREE)
    )
    listed, moved = [], []
    for n, form in enumerate([*FORMS.values(), *SWITCHING]):
        words = form.format(start=start, n=n).split()
        if wg.shape_of(["git", *words]) == "listed":
            listed.append(form)
        copy = tmp_path / f"r{n}"
        shutil.copytree(template, copy)
        git(copy, *words, ok=1 if words[0] == "check-ignore" else 0)
        if head(copy) != head(template):
            moved.append(form)
    # A listed form that moved HEAD is a wrong row.
    assert not set(listed) & set(moved), sorted(set(listed) & set(moved))
    assert sorted(listed) == sorted(FORMS.values()), sorted(
        set(FORMS.values()) ^ set(listed)
    )
    assert sorted(moved) == sorted(SWITCHING), moved

    # #856 (S13 of work item 1791384157): each braced form runs through bash,
    # which expands the braces before git reads the words, and each switches
    # HEAD or adds a worktree. The guard reads the frozen words with the
    # command's unquoted braces, and none of them is listed. Red at
    # `5623d728`, where all four were. The guard's half reads words and runs
    # everywhere; bash's half runs only where `bash` is a shell.
    import shlex

    braced = [
        (n, form.format(start=start, n=n))
        for n, form in enumerate(BRACED, start=len(FORMS) + len(SWITCHING))
    ]
    braced_listed = [
        text
        for _n, text in braced
        if wg.shape_of(["git", *shlex.split(text)], braced=wg._unquoted_brace(text))
        == "listed"
    ]
    assert not braced_listed, braced_listed
    # On a `windows-latest` runner `bash` resolves to the WSL launcher, which
    # exits 1 for every command it is handed (`conftest.shell_probe`; round 1
    # of work item 1791384157, red 1). The ubuntu and macOS legs run it.
    why = shell_probe("bash")
    if why is not None:
        pytest.skip(f"bash: {why}")
    acted = []
    for n, text in braced:
        copy = tmp_path / f"r{n}"
        shutil.copytree(template, copy)
        done = subprocess.run(
            ["bash", "-c", f"git -C {shlex.quote(str(copy))} {text}"],
            capture_output=True,
            stdin=subprocess.DEVNULL,
            env={**os.environ, "GIT_EDITOR": "true", "GIT_PAGER": "cat"},
        )
        assert done.returncode == 0, (text, done.returncode, done.stderr)
        if head(copy) != head(template) or (tmp_path / f"wt{n}").is_dir():
            acted.append(text)
    assert len(acted) == len(BRACED), acted


def test_the_readings_are_gone():
    """S11 of work item 1791270162. None of the symbols `spec.md` In 4
    removes is defined, and the switch arm runs no `rev-parse`: nothing
    looks a name up. Red at `9c03ae85`, where every one was still defined."""
    import inspect

    gone = (
        "wider_only_kinds",
        "_bare_words",
        "ask_what_only_the_wider_reading_finds",
        "switch_kind",
        "SWITCH_OPTIONS",
        "_Options",
        "_long_option",
        "read_switch_words",
        "handed_words",
        "_redirection_width",
        "_REDIRECTION",
        "is_ref",
        "_verified",
        "_commit_named",
        "_object_named",
        "_one_merge_base",
        "_OBJECT_NAME",
        "tracked_in_any_remote",
        "_refs",
        "_fetched_as",
        "_the_bases_lookup",
        "_no_guess",
        "classify",
    )
    assert [name for name in gone if hasattr(wg, name)] == []
    arm = (
        wg.main,
        wg.shape_of,
        wg._segment_finding,
        wg._git_finding,
        wg._merged_findings,
        wg._command_findings,
        wg._finding_tree,
    )
    assert [f.__name__ for f in arm if "rev-parse" in inspect.getsource(f)] == []
