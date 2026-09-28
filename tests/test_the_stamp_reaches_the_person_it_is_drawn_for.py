"""The sealer's stamp reaches the person it is drawn for (#400).

Work item 1790562543. A sealer's stdout is a pipe into a report that arrives
folded behind `ctrl+o`, so a stamp drawn there was never seen. The gate now
draws only on a terminal; a recorded seal on a pipe writes its panel to a
values file under the git common dir, and a `Stop` hook in the session that
spawned the sealer draws each undrawn file once, after that turn's text.

This module holds the stamp's half — the values file, `seal-stamp --from`,
the default scale. The gate's half is in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside the fixtures
that drive a real gate over a settled work item.
"""

import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAMP = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")

# A panel in the shape `broad_gate.panel` returns. Neutral values.
ROWS = [
    ("SEALED", ""),
    None,
    ("tree", "aaa1111"),
    ("base", "bbb2222"),
    ("from", "origin/base"),
    ("gate", "plugin 0.0.0"),
    None,
    ("suite", "3 passed"),
    ("row", "exit 0"),
    ("ledger", "4 ok . 0 broken"),
    ("chain", "exit 0"),
    None,
    ("rounds", "2"),
]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def stamp_module():
    return _load("specseal_seal_stamp_for_its_values", STAMP)


def values(scale=0.9, item="/x/seal/specs/1799000000-an-item", rows=ROWS):
    return {
        "tree": "aaa1111",
        "base": "bbb2222",
        "from": "origin/base",
        "item": item,
        "session": "s-1",
        "scale": scale,
        "rows": rows,
    }


def seal_stamp(*args):
    """`seal_stamp.py` as a person types it, stdout a pipe."""
    return subprocess.run(
        [sys.executable, STAMP, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )


# --- S11: a values file drawn by hand, once --------------------------------


def test_a_values_file_is_drawn_by_hand_once_and_then_refused(tmp_path):
    """S11. `seal-stamp --from <file>` draws that run's rows — not the
    sample — at the file's own scale, and marks the file drawn. The same
    command again refuses with one sentence and exit 2, because a sealed
    run's values are drawn once whoever draws them."""
    mod = stamp_module()
    path = mod.write_values(str(tmp_path), "s-1", values())
    out = seal_stamp("--from", path)
    assert out.returncode == 0, out.stderr
    assert out.stdout == "\n" + "\n".join(mod.stamp(ROWS, 0.9, shape=True)) + "\n\n"
    assert "aaa1111" in out.stdout and "c46fd2d" not in out.stdout, (
        "the drawing is the sample's, not the run's"
    )
    assert not os.path.exists(path), "the file was drawn and not marked drawn"
    assert os.path.exists(mod.drawn_path(path)), "the drawn file's values are gone"

    again = seal_stamp("--from", path)
    assert again.returncode == 2, again.stdout + again.stderr
    assert again.stdout == "", f"something was drawn a second time:\n{again.stdout}"
    refusal = again.stderr.strip()
    assert "was drawn already" in refusal and "\n" not in refusal, refusal
    assert seal_stamp("--from", mod.drawn_path(path)).returncode == 2, (
        "the drawn file itself can be drawn again by naming it"
    )


def test_a_file_that_is_not_a_run_is_refused_and_left_for_a_repair(tmp_path):
    """A values file that is not in the gate's shape is refused before it is
    claimed, so it is still there to be drawn once somebody repairs it — and
    one refused for a scale under the floor is refused by the function that
    draws, which checks the band itself."""
    for broken, said in (
        ("not json", "it is not JSON"),
        (json.dumps({**values(), "rows": "SEALED"}), "`rows` is not a list"),
        (json.dumps(values(scale=0.5)), "under the floor"),
    ):
        path = tmp_path / "1-aaa1111.json"
        path.write_text(broken, encoding="utf-8")
        out = seal_stamp("--from", str(path))
        assert out.returncode == 2, (broken, out.stdout, out.stderr)
        assert said in out.stderr, out.stderr
        assert out.stdout == "", out.stdout
        assert path.exists(), f"a refused file was claimed: {broken!r}"


def test_pending_lists_the_undrawn_oldest_first_and_claim_takes_one_once(tmp_path):
    """The reader the hook uses. `pending` lists undrawn files oldest first
    and skips drawn ones and the writer's hidden temporary; `claim` renames a
    file to its drawn name and answers None to the second caller, which is
    what keeps two drawers racing for one file to one drawing."""
    mod = stamp_module()
    older = mod.write_values(str(tmp_path), "s-1", values(), now=1)
    newer = mod.write_values(str(tmp_path), "s-1", values(), now=2)
    directory = mod.values_dir(str(tmp_path), "s-1")
    open(os.path.join(directory, ".3-aaa1111.tmp"), "w").close()
    assert mod.pending(directory) == [older, newer]
    assert mod.claim(older) == mod.drawn_path(older)
    assert mod.claim(older) is None, "a claimed file was claimed a second time"
    assert mod.pending(directory) == [newer]
    assert mod.pending(str(tmp_path / "nowhere")) == []


def test_a_session_id_cannot_name_a_directory_outside_the_values_dir(tmp_path):
    """The session id names a directory, so a separator in a malformed one
    must not become a path escape, and an absent one lands under `none/`."""
    mod = stamp_module()
    assert mod.session_key("../../elsewhere") == "elsewhere"
    for absent in (None, "", "  ", ".", ".."):
        assert mod.session_key(absent) == mod.NO_SESSION, absent
    path = mod.write_values(str(tmp_path), "../../elsewhere", values())
    assert os.path.dirname(path) == os.path.join(
        str(tmp_path), mod.VALUES_DIR, "elsewhere"
    ), path


# --- S3-S6: the hook draws at the main session's `Stop`, once ---------------

DISPATCH = os.path.join(ROOT, "hooks", "dispatch.py")


def git(repo, *args):
    """git driven from Python, so no Bash line carries a commit (§8)."""
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )


def opted_in(tmp_path, name="repo"):
    """A repository with `seal/` at its root and one commit, so a linked
    worktree can be added to it."""
    repo = tmp_path / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    (repo / "seal").mkdir()
    (repo / "seal" / "config.md").write_text("# config\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.name=e",
        "-c",
        "user.email=e@example.com",
        "commit",
        "-qm",
        "x",
    )
    return repo


def pending_for(repo, session, **kw):
    """One values file for `session` in `repo`'s common dir; its path."""
    return stamp_module().write_values(str(repo / ".git"), session, values(**kw))


def stop(cwd, session="s-1", **payload):
    """`dispatch.py stop` as the harness runs it: the payload on stdin, and
    what it printed."""
    body = {"hook_event_name": "Stop", "session_id": session, "cwd": str(cwd)}
    body.update(payload)
    r = subprocess.run(
        [sys.executable, DISPATCH, "stop"],
        input=json.dumps(body),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    assert r.returncode == 0, r.stderr
    return r.stdout


def message(stdout):
    """The `systemMessage` the hook printed, as lines."""
    return json.loads(stdout)["systemMessage"].split("\n")


def test_the_main_sessions_stop_draws_each_undrawn_file_once(tmp_path):
    """S3 and S4. The main session's `Stop` — `session_id` X, no `agent_id` —
    prints one JSON object whose `systemMessage` opens with a label naming
    what was sealed and then draws the block form of the file's rows at the
    file's scale, colour sequences and all. The file is marked drawn, so the
    next `Stop` of the same session prints nothing."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    path = pending_for(repo, "s-1")
    lines = message(stop(repo))
    assert lines[0] == "SEALED aaa1111 against bbb2222 · 1799000000-an-item", lines[0]
    assert lines[1:] == mod.stamp(ROWS, 0.9, shape=False), "not the file's block form"
    assert any("\x1b[38;2;" in line for line in lines[1:]), "the drawing lost colour"
    assert not os.path.exists(path) and os.path.exists(mod.drawn_path(path))
    assert stop(repo) == "", "a drawn file was drawn a second time"


def test_a_subagents_end_draws_nothing_and_leaves_the_file(tmp_path):
    """S5. `SubagentStop` carries the parent's `session_id` and differs by
    `agent_id` alone (`questions.md` Q2), so a payload naming an agent is the
    sealer's own end — or any subagent's — and draws nothing; so does any
    event that is not `Stop`. The file stays for the main session."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    path = pending_for(repo, "s-1")
    assert stop(repo, agent_id="a-1", agent_type="specseal:sealer") == ""
    assert stop(repo, hook_event_name="SubagentStop", agent_id="a-1") == ""
    assert stop(repo, hook_event_name="SubagentStop") == ""
    assert mod.pending(os.path.dirname(path)) == [path], "the file was taken"


def test_another_sessions_stop_leaves_its_file_alone(tmp_path):
    """S6. A concurrent session of the same clone ends its turn: its own
    directory is empty, so it prints nothing and takes nothing, and session
    Y's file is still there for Y."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    path = pending_for(repo, "s-y")
    assert stop(repo, session="s-x") == ""
    assert mod.pending(os.path.dirname(path)) == [path]


def test_several_files_come_out_as_one_message_oldest_first(tmp_path):
    """Two seals in one turn are one message, oldest first, each stamp whole
    under its own label; a file that is not a run's values is skipped and
    left where it is rather than taking the others down."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    first = mod.write_values(str(repo / ".git"), "s-1", values(), now=1)
    second = mod.write_values(
        str(repo / ".git"), "s-1", {**values(), "tree": "ccc3333"}, now=2
    )
    broken = os.path.join(os.path.dirname(first), "3-ddd4444.json")
    with open(broken, "w", encoding="utf-8") as handle:
        handle.write("not json")
    text = json.loads(stop(repo))["systemMessage"]
    blocks = text.split("\n\n")
    assert [b.split("\n", 1)[0] for b in blocks] == [
        "SEALED aaa1111 against bbb2222 · 1799000000-an-item",
        "SEALED ccc3333 against bbb2222 · 1799000000-an-item",
    ], text
    for block in blocks:
        assert block.split("\n")[1:] == mod.stamp(ROWS, 0.9, shape=False)
    assert mod.pending(os.path.dirname(first)) == [broken]
    assert not os.path.exists(first) and not os.path.exists(second)


def test_the_sealers_worktree_and_the_main_checkout_share_the_file(tmp_path):
    """The sealer's root is a linked worktree while the main session's `cwd`
    is the checkout (Q2's reading: the `Stop` payload's `cwd` was the main
    checkout). The file lives under the COMMON dir, so a `Stop` from either
    tree finds it — a file written through the worktree is drawn from the
    main checkout, and one written there is drawn from inside the worktree."""
    repo = opted_in(tmp_path)
    tree = tmp_path / "tree"
    git(repo, "worktree", "add", "-q", str(tree))
    common = git(tree, "rev-parse", "--git-common-dir").stdout.strip()
    common = os.path.normpath(os.path.join(str(tree), common))
    assert common == os.path.normpath(str(repo / ".git")), common
    stamp_module().write_values(common, "s-1", values())
    assert message(stop(repo))[0].startswith("SEALED aaa1111"), "not from the checkout"
    pending_for(repo, "s-1", item="/x/seal/specs/1799000001-another")
    assert message(stop(tree))[0].endswith("1799000001-another"), "not from the tree"


def test_a_repository_that_never_opted_in_is_not_drawn_for(tmp_path):
    """No `seal/` at either place, and the hook stays silent and takes
    nothing — even over a file that is there."""
    repo = opted_in(tmp_path)
    for name in os.listdir(repo / "seal"):
        os.remove(repo / "seal" / name)
    os.rmdir(repo / "seal")
    path = pending_for(repo, "s-1")
    assert stop(repo) == ""
    assert os.path.exists(path), "a file was taken in a repository not opted in"


def test_the_stop_group_reports_the_stop_event(monkeypatch, capsys):
    """`dispatch.main` names the event on its decision path, and named every
    group that is not `pre-` as `PostToolUse`. The `stop` group answers
    `Stop`, so a decision coming out of it, should one ever do, says so."""
    dispatch = _load("specseal_dispatch_for_the_stop_group", DISPATCH)
    decision = json.dumps(
        {
            "hookSpecificOutput": {
                "permissionDecision": "ask",
                "permissionDecisionReason": "r",
            }
        }
    )
    monkeypatch.setattr(dispatch, "run_gate", lambda _gate, _payload: decision)
    monkeypatch.setattr(sys, "argv", ["dispatch.py", "stop"])
    monkeypatch.setattr(sys, "stdin", __import__("io").StringIO("{}"))
    dispatch.main()
    said = json.loads(capsys.readouterr().out)
    assert said["hookSpecificOutput"]["hookEventName"] == "Stop", said


def test_the_hook_is_registered_for_stop_and_nothing_else():
    """`hooks.json` runs the `stop` group at `Stop`, and `dispatch.GROUPS`
    holds the hook there. Registered at `SubagentStop` it would draw inside
    the sealer, where the whole work item began."""
    with open(os.path.join(ROOT, "hooks", "hooks.json"), encoding="utf-8") as handle:
        events = json.load(handle)["hooks"]
    commands = [h["command"] for group in events["Stop"] for h in group["hooks"]]
    assert commands and all(c.split()[-1] == "stop" for c in commands), commands
    assert "SubagentStop" not in events
    dispatch = _load("specseal_dispatch_for_its_groups", DISPATCH)
    assert dispatch.GROUPS["stop"] == ("sealer-stamp.py",)


# --- S16: the rules are where they are read ----------------------------------


def test_the_orchestrator_is_told_the_stamp_is_drawn_for_it():
    """S16, the orchestrator's half (contract §14). The rule sits in the
    section that spawns the sealer: the stamp is drawn at the end of the
    turn, the result text comes first, the orchestrator draws none — by
    `seal-stamp` or by relaying the sealer's log, which 0.15.6 did — and a
    red run relays `NOT SEALED` with nothing drawn."""
    text = flat("skills", "code-review", "orchestration.md")
    section = text.split("## Orchestrator: the pull request opens before round 1", 1)[1]
    section = section.split("## Orchestrator: verify before posting", 1)[0]
    for said in (
        "**The stamp is drawn for you at the end of your turn, and you never draw one (#400).**",
        "So put the result text first",
        "Draw none yourself, neither with `seal-stamp` nor by relaying the sealer's log.",
        "On a red run relay the `NOT SEALED` lines, and nothing is drawn.",
    ):
        assert said in section, said


def test_the_form_bullet_says_what_draws_the_final_seal():
    """S16, `verify`'s half. The **Form** bullet said `broad-gate` prints the
    disc on success alone, which stopped being true of a sealer's run: it now
    says the gate draws on a terminal and the `Stop` hook draws elsewhere,
    both only over a written cell."""
    text = flat("skills", "verify", "SKILL.md")
    assert "`broad-gate` prints the disc on success alone" not in text
    for said in (
        "when every check passed and the cell was written, and on no other path",
        "the `Stop` hook draws those values at the end of the turn",
    ):
        assert said in text, said


def test_the_policy_names_what_enforces_the_drawing_and_what_nothing_does():
    """S16, the policy's half. `docs/the-broad-gate.md` carries the rule
    under this work item's marker with an `Enforced by:` line naming the
    hook's cases, and a second statement saying what the screen shows is
    enforced by nothing."""
    text = flat("docs", "the-broad-gate.md")
    marker = "<!-- specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for -->"
    assert text.count(marker) == 2, "the rule and the unchecked half, one marker each"
    rule, unchecked = text.split(marker)[1:3]
    assert "**The stamp is drawn once, where a person sees it" in rule
    assert "::test_the_main_sessions_stop_draws_each_undrawn_file_once" in rule
    assert "**What the person's screen shows is not checked" in unchecked
    assert "Enforced by: nothing — no case, hook or workflow can observe a screen" in (
        unchecked
    )


# --- S16: the sealer is told it draws nothing --------------------------------


def flat(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as handle:
        return " ".join(handle.read().split())


def test_the_sealer_is_told_the_gate_draws_nothing_and_neither_does_it():
    """S16, the sealer's half (contract §14). `agents/sealer.md` said the
    drawing arrives as letters and to pass it through, which the 0.15.6 run
    did — every seal behind `ctrl+o`. It now says the gate draws nothing in a
    sealer, that the session which spawned it has the stamp drawn, that the
    sealer draws none by either route, and that the exit-0 outcome is the
    `SEALED` line; and the old instruction is gone."""
    text = flat("agents", "sealer.md")
    for said in (
        "**The gate draws nothing in a sealer, and neither do you**",
        "A hook in the session that spawned you draws that file once",
        "Do not draw it yourself, neither with `seal-stamp` nor from the file",
        "The gate printed one line beginning `SEALED`",
    ):
        assert said in text, said
    assert "the drawing arrives as letters" not in text
    assert "pass it through as it came" not in text


# --- S13: the scale --------------------------------------------------------


def test_the_default_scale_is_ninety_percent_with_its_reason_beside_it():
    """S13. `DEFAULT_SCALE` is 0.90, and the comment above it says why and
    names 0.75 as the candidate passed over, so the next reader does not
    re-run #400's six-scale comparison to find out."""
    mod = stamp_module()
    assert mod.DEFAULT_SCALE == 0.90
    with open(STAMP, encoding="utf-8") as handle:
        source = handle.read()
    above = source.split("DEFAULT_SCALE = 0.90", 1)[0].rsplit("\n\n", 1)[-1]
    assert "0.75 was the other candidate" in above, above
    assert "passed over" in above, above


def test_both_commands_draw_at_the_default_scale_when_given_none():
    """S13's other half: `seal-stamp` with no `--scale` draws the sample at
    `DEFAULT_SCALE`, and `broad-gate`'s own default is the same constant —
    the gate's values file carries it, which the gate module's cases read."""
    mod = stamp_module()
    out = seal_stamp("--shape")
    assert out.returncode == 0, out.stderr
    assert out.stdout == (
        "\n" + "\n".join(mod.stamp(mod.SAMPLE_ROWS, mod.DEFAULT_SCALE, True)) + "\n\n"
    )
    help_text = subprocess.run(
        [sys.executable, GATE, "--help"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    ).stdout
    assert f"default {mod.DEFAULT_SCALE}" in help_text, help_text
