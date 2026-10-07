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
import inspect
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAMP = os.path.join(ROOT, "skills", "verify", "scripts", "seal_stamp.py")
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")

# A panel in the shape `broad_gate.panel` returns since #832. Neutral values.
ROWS = [
    ("SEALED", ""),
    ("tree", "aaa1111"),
    ("", "feat/x"),
    ("base", "bbb2222  origin/base"),
    ("item", "#12 · 1799000000"),
    None,
    ("suite", "✓ 3 passed"),
    ("ledger", "✓ 4 ok · 0 drifted · 0 broken"),
    ("chain", "✓ exit 0"),
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
        "branch": "feat/x",
        "pr": "#12",
        "item": item,
        "session": "s-1",
        "scale": scale,
        "rows": rows,
    }


# The label a values file in `values()`'s shape draws under (#666): the
# `SEALED` line's own names, the pull request, the work item.
LABEL = (
    "SEALED feat/x @ aaa1111 against origin/base @ bbb2222 · #12 · 1799000000-an-item"
)


def test_a_values_file_from_an_older_gate_draws_the_label_it_always_drew():
    """A15's compatibility half. A file with no `branch` key was written by
    a gate older than #666, and may still be pending when a newer hook draws
    it, so it gets the label it always got. `branch` present and `null` is a
    detached HEAD, which is the new shape with the branch left out; no `pr`
    leaves the pull request out."""
    mod = stamp_module()
    old = {k: v for k, v in values().items() if k not in ("branch", "pr")}
    assert mod.label(old) == "SEALED aaa1111 against bbb2222 · 1799000000-an-item"
    assert mod.label({**values(), "branch": None, "pr": None}) == (
        "SEALED aaa1111 against origin/base @ bbb2222 · 1799000000-an-item"
    )


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


def test_the_drawn_refusal_names_the_file_the_values_are_in(tmp_path):
    """Round 1's 🟡 3. Naming the drawn file itself was refused — rightly —
    with a sentence saying the values stay in `X.drawn.drawn.json`, which does
    not exist, on the one path a person has to recover them from. The file
    the refusal says holds the values exists, whichever name was given."""
    mod = stamp_module()
    path = mod.write_values(str(tmp_path), "s-1", values())
    assert seal_stamp("--from", path).returncode == 0
    drawn = mod.drawn_path(path)
    for given in (path, drawn):
        out = seal_stamp("--from", given)
        assert out.returncode == 2, out.stdout + out.stderr
        assert f"the values stay in {drawn}." in out.stderr, out.stderr
        assert ".drawn.drawn.json" not in out.stderr, out.stderr


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
    open(os.path.join(directory, ".3-aaa1111.tmp"), "w", encoding="utf-8").close()
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


def drawn(mod, label, rows, scale):
    """One block of the hook's message as `fitted` draws it at `scale`: the
    label, then the block form. `scale` None is the rung with no disc."""
    return "\n".join([label, *mod.stamp(rows, scale, shape=False)])


def test_the_main_sessions_stop_draws_each_undrawn_file_once(tmp_path):
    """S3 and S4. The main session's `Stop` — `session_id` X, no `agent_id` —
    prints one JSON object whose `systemMessage` opens with a label naming
    what was sealed and then draws the block form of the file's rows at the
    file's scale, colour sequences and all. The file is marked drawn, so the
    next `Stop` of the same session prints nothing.

    #717's A15: the bytes are compared with the message `fitted` holds under
    the budget, not with the file's scale drawn whatever its size — and at
    `ROWS`' size that message IS the file's 0.90 drawing, so the step-down
    is asserted not to have fired here rather than assumed."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    path = pending_for(repo, "s-1")
    lines = message(stop(repo))
    assert lines[0] == LABEL, lines[0]
    assert "\n".join(lines) == mod.fitted([(LABEL, ROWS, 0.9)]), "not the fitted form"
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


# The smallest panel a run could carry. Whether two of its stamps share one
# message is the disc's mark's to say, not this module's: under #717's lily
# they did; under phase 2's § of #832 they did not; under the owner's 14-cell
# disc they did again; under the S of 2026-10-07 they do not, and under the
# archived key they do (`phases/phase-6.md` of work item 1791270164 and round
# 1's report there have the sizes). A case that needs a pair over the budget
# grows this panel until it is.
SMALL_ROWS = [("SEALED", ""), ("tree", "aaa1111"), ("", "feat/x"), ("rounds", "2")]


def test_several_files_come_out_one_stop_each_oldest_first(tmp_path):
    """Several pending seals come out one `Stop` at a time, oldest first,
    each stamp whole under its own label and with its disc, and a file that
    is not a run's values is skipped and left where it is rather than taking
    the others down.

    Phase 2's name for #717's case. The pair has to be over the budget
    together for the newer to wait for the next `Stop` rather than share the
    message, and whether a small pair is depends on the disc's mark, which
    #857 replaces by changing `seal-mark.txt` alone. So the panel is grown
    by deferral homes, one at a time, until the pair does not fit — none
    under the S, some under the archived key — and the premise is asserted
    rather than assumed (round 1's 🟡 3)."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    other = LABEL.replace("aaa1111", "ccc3333")
    rung = mod.SCALE_LADDER[-1]
    rows = list(SMALL_ROWS)
    while sum(len(drawn(mod, who, rows, rung)) for who in (LABEL, other)) + 2 <= (
        mod.MESSAGE_BUDGET
    ):
        rows.append(("", f"home-{len(rows)}"))
    small = values(rows=rows)
    first = mod.write_values(str(repo / ".git"), "s-1", small, now=1)
    second = mod.write_values(
        str(repo / ".git"), "s-1", {**small, "tree": "ccc3333"}, now=2
    )
    broken = os.path.join(os.path.dirname(first), "3-ddd4444.json")
    with open(broken, "w", encoding="utf-8") as handle:
        handle.write("not json")
    older, newer = (drawn(mod, who, rows, rung) for who in (LABEL, other))
    assert len(older) + 2 + len(newer) > mod.MESSAGE_BUDGET, (
        "the grown pair shares one message; this case's premise moved"
    )
    assert len(older) <= mod.MESSAGE_BUDGET, "the grown stamp lost its disc alone"
    assert json.loads(stop(repo))["systemMessage"] == older
    assert not os.path.exists(first) and os.path.exists(second)
    assert json.loads(stop(repo))["systemMessage"] == newer
    assert all("\x1b[38;2;" in block for block in (older, newer)), "a disc was lost"
    assert not os.path.exists(second)
    assert mod.pending(os.path.dirname(first)) == [broken]
    assert stop(repo) == "", "the broken file was drawn"


def test_a_malformed_later_file_does_not_take_the_earlier_ones(tmp_path):
    """Round 1's 🟡 2. `drawings` claimed a file and only then built its
    label, and `label` raises `TypeError` on an `item` that is not a string —
    outside the guarded read, so the exception left the good file before it
    claimed and never printed, and `--from` then refused it as drawn. Every
    block is built whole before its file is claimed now: the good file is
    drawn, and the bad one stays pending under its own name."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    good = mod.write_values(str(repo / ".git"), "s-1", values(), now=1)
    bad = mod.write_values(str(repo / ".git"), "s-1", {**values(), "item": 5}, now=2)
    lines = message(stop(repo))
    assert lines[0] == LABEL, lines
    assert "\n".join(lines) == mod.fitted([(LABEL, ROWS, 0.9)])
    assert os.path.exists(mod.drawn_path(good)) and not os.path.exists(good)
    assert os.path.exists(bad), "the malformed file was claimed"
    assert not os.path.exists(mod.drawn_path(bad))


def test_a_file_at_a_scale_the_band_refuses_is_left_pending(tmp_path):
    """#717. `drawings` hands `fitted` the rows and the scale rather than a
    finished drawing, so it still draws each file once at its own scale
    before the claim: that is what proves the file draws at all. A file at
    0.5 passes `read_values` — the scale is a number — and is refused by the
    band, so it stays pending under its own name and the good file beside it
    is drawn, rather than both being claimed and nothing printed."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    good = mod.write_values(str(repo / ".git"), "s-1", values(), now=1)
    small = mod.write_values(str(repo / ".git"), "s-1", values(scale=0.5), now=2)
    lines = message(stop(repo))
    assert "\n".join(lines) == mod.fitted([(LABEL, ROWS, 0.9)])
    assert os.path.exists(mod.drawn_path(good)) and not os.path.exists(good)
    assert os.path.exists(small), "a file the band refuses was claimed"


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
    assert message(stop(repo))[0].startswith("SEALED feat/x @ aaa1111"), (
        "not from the checkout"
    )
    pending_for(repo, "s-1", item="/x/seal/specs/1799000001-another")
    assert message(stop(tree))[0].endswith("1799000001-another"), "not from the tree"


def test_a_turn_ending_in_a_subdirectory_still_draws(tmp_path):
    """The payload's `cwd` is wherever the session last stood, which need not
    be the repository's root. The hook walks up to the `.git` entry rather
    than asking git, so a turn ending in a subdirectory draws the same."""
    repo = opted_in(tmp_path)
    (repo / "docs" / "deep").mkdir(parents=True)
    pending_for(repo, "s-1")
    assert message(stop(repo / "docs" / "deep"))[0].startswith(
        "SEALED feat/x @ aaa1111"
    )


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


# --- #717: the hook's whole message is held under a budget --------------------

# What `broad_gate.panel` returns for a real run since #832 — `full_values()`'s
# run, with values as long as a real run's: its branch elided at
# `PANEL_VALUE_WIDTH`, the base's ref beside its commit, the result rows behind
# a `✓`. Neutral values.
FULL_ROWS = [
    ("SEALED", ""),
    ("tree", "aaa1111a"),
    ("", "feat/12-the-branch-names-the-work-item..."),
    ("base", "bbb2222b  origin/release/v1.2.3"),
    ("item", "#12 · 1799000000"),
    ("gate", "tree 1.2.3"),
    None,
    ("suite", "✓ 6621 passed · 11 skipped"),
    ("ledger", "✓ 3451 ok · 0 drifted · 0 broken"),
    ("chain", "✓ exit 0"),
    ("CI also", "· 4 more steps"),
    ("rounds", "2"),
]

# A panel in the shape the gate wrote from #666 to #717, with values as long as
# a real run's. Its 0.90 drawing under its label was over the harness's limit,
# which put every stamp drawn from #666 on behind a 2 KB preview of a file.
# Neutral values; a file in this shape may still be pending when a newer hook
# draws it, which is why a case keeps it rather than following `panel`.
OLD_ROWS = [
    ("SEALED", ""),
    None,
    ("tree", "aaa1111a"),
    ("", "feat/12-the-branch-n..."),
    ("base", "bbb2222b"),
    ("", "origin/release/v1.2.3"),
    ("item", "#12 . 1799000000"),
    ("gate", "tree 1.2.3"),
    None,
    ("suite", "6621 passed, 11 skipped"),
    ("", "exit 0"),
    ("ledger", "3451 ok"),
    ("", "0 drifted . 0 broken"),
    ("chain", "exit 0"),
    None,
    ("workflow", "4 of 9 not answered"),
    None,
    ("rounds", "2"),
]


def full_values(tree="aaa1111a"):
    """A values file as long as a real run's, label included: a branch and a
    work item named the way this repository names them."""
    name = "the-branch-names-the-work-item-it-carries"
    return {
        **values(item=f"/x/seal/specs/1799000000-{name}", rows=FULL_ROWS),
        "tree": tree,
        "base": "bbb2222b",
        "from": "origin/release/v1.2.3",
        "branch": f"feat/12-{name}",
    }


def test_the_budget_is_named_and_derived_from_the_measured_limit():
    """A2. The limit is the harness's, measured in characters, and the
    budget leaves room for the report `dispatch.py` prepends to the same
    message; every rung of the ladder is a scale the band accepts, so no
    rung can be refused when the hook steps down to it."""
    mod = stamp_module()
    assert mod.MESSAGE_LIMIT <= 10090, "above a size the harness has persisted"
    assert mod.MESSAGE_LIMIT == 10000, "not the number the probe measured"
    assert mod.MESSAGE_BUDGET <= mod.MESSAGE_LIMIT - 1000, mod.MESSAGE_BUDGET
    assert mod.SCALE_LADDER == (0.90,), "#832: one rung, then the text block alone"
    assert all(mod.check_scale(rung) is None for rung in mod.SCALE_LADDER)


def test_the_hooks_message_is_under_the_budget_for_one_file(tmp_path):
    """A3, one file. A run's values at a real run's size, drawn by the hook
    through `dispatch.py stop`: the printed `systemMessage` is no longer than
    `MESSAGE_BUDGET`, it still opens with the file's label, and it is the
    stamp WITH its disc at 0.90. Under the budget by itself is what
    `admitted` guarantees whatever the stamp's size, by dropping the disc
    from a block that does not fit with it, so without the last assertion a
    stamp grown past the budget passed here as the text block alone (round
    1's 🟡 4)."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    mod.write_values(str(repo / ".git"), "s-1", full_values())
    text = json.loads(stop(repo))["systemMessage"]
    assert len(text) <= mod.MESSAGE_BUDGET, len(text)
    assert text.split("\n", 1)[0] == mod.label(full_values())
    assert text == drawn(mod, mod.label(full_values()), FULL_ROWS, 0.9), (
        "a real run's stamp no longer fits the budget with its disc"
    )


# The rows the owner's chosen reference was drawn over: the orchestrating
# session's `frames.py`'s `ROWS`, behind the panel's title row, which
# `frames.py#design_open` drew from a constant. They are the panel's shape
# with one difference the real panel does not have — a `flow` row where the
# panel carries `CI also` (`questions.md` Q15 of work item 1791270164) — and
# they stay here as data, because the owner's picture was drawn over them.
REFERENCE_ROWS = [
    ("SEALED", ""),
    ("tree", "aaa1111a"),
    ("", "feat/12-the-branch-names-the-work-item"),
    ("base", "bbb2222b  origin/release/v1.2.3"),
    ("item", "#12 · 1799000000"),
    ("gate", "tree 1.2.3"),
    None,
    ("suite", "✓ 6621 passed · 11 skipped"),
    ("ledger", "✓ 3451 ok · 0 drifted · 0 broken"),
    ("chain", "✓ exit 0"),
    ("flow", "· 4 of 9 not answered"),
    ("rounds", "2"),
]
# The owner's reference for a real run's stamp, chosen on 2026-10-07: design 3
# of `frames.py`, `~/Desktop/specseal-frame-3-open.ans` on the owner's
# machine (`spec.md` decision 6 and S3 of work item 1791270164). Transcribed
# from that file's SGR stream and half-blocks by a script that read no line
# of `seal_stamp.py`: each disc cell its top half's letter (its bottom
# half's where the top is off the disc), the text as the twin writes it, and
# each line without the blank cells the reference carries past its end.
REFERENCE_TWIN = (
    "        mmmmmmmmmmmm           SEALED ------------------------------",
    "     mmmMMMMMMMMMMMMmmm",
    "   mmMMMMNNN....NNNnnnnmm      tree    aaa1111a",
    "  mmMMNN............NMnnmm             feat/12-the-branch-names-the-work-item",
    " mMMMN....YYxyyyXXYy..MnnNm    base    bbb2222b  origin/release/v1.2.3",
    "mmMMN....YXXy.....xy...MNNmm   item    #12 . 1799000000",
    "mMMN.....YXXXXYY...y....MNNm   gate    tree 1.2.3",
    "mMMN.......xxXXXXXX.....MNNm",
    "mMMNN....Y.....yXXXxy..MMNNm   suite   + 6621 passed . 11 skipped",
    " mMMN....YX......Yxxy..MNNm    ledger  + 3451 ok . 0 drifted . 0 broken",
    "  mnnNN..YyxxYYYYxyy.MMNNm     chain   + exit 0",
    "   mnnnMM..........MMNNNm      flow    . 4 of 9 not answered",
    "     mmnnNNMMMMMMNNNNmm        rounds  2",
    "        mmmNNNNNNmmm",
)
# The disc's twenty-eight half-rows in the reference, columns 0 to 27 of its
# fourteen lines, each half its colour's letter and a space off the disc.
REFERENCE_DISC = (
    "           mmmmmm           ",
    "        mmmMMMMMMmmm        ",
    "      mmMMMMMMMMMMMMmm      ",
    "     mmMMMMNNNNNNMMnnmm     ",
    "    mMMMMNNN....NNNnnnnm    ",
    "   mMMMNN..........NNnnnm   ",
    "  mmMMNN............NMnnmm  ",
    "  mMMNN....YYYYYY.Y..MMnnm  ",
    " mMMMN....YYxyyyXXYy..MnnNm ",
    " mMMN....YYxyy...Xxy...MNNm ",
    " mMMN....YXXy.....xy...MNNm ",
    "mMMNN....YXXX.....Yy...MMNNm",
    "mMMN.....YXXXXYY...y....MNNm",
    "mMMN......XXXXXXXY......MNNm",
    "mMMN.......xxXXXXXX.....MNNm",
    "mMMN........yyxXXXXx....MNNm",
    "mMMNN....Y.....yXXXxy..MMNNm",
    " mMMN....Yy......XXxy..MNNm ",
    " mMMN....YX......Yxxy..MNNm ",
    " mMnnN...YXX....YYxyy.MNNNm ",
    "  mnnNN..YyxxYYYYxyy.MMNNm  ",
    "  mmnnMM..y.yyyyyyy.MMNNmm  ",
    "   mnnnMM..........MMNNNm   ",
    "    mnnnnMMM....MMMNNNNm    ",
    "     mmnnNNMMMMMMNNNNmm     ",
    "      mmNNNNNNNNNNNNmm      ",
    "        mmmNNNNNNmmm        ",
    "           mmmmmm           ",
)
# The reference's colours by letter, the owner's `seal28.py`'s nine.
REFERENCE_COLOURS = {
    "m": (150, 24, 28),
    "M": (208, 68, 64),
    "n": (160, 30, 34),
    "N": (96, 10, 14),
    ".": (112, 16, 20),
    "X": (186, 38, 42),
    "Y": (222, 86, 78),
    "x": (90, 8, 12),
    "y": (84, 8, 12),
    " ": None,
}


def test_a_real_runs_stamp_is_the_owners_reference_cell_for_cell():
    """#832 S1-S4 against the picture the owner chose rather than against a
    rule: the stamp over the rows the reference was drawn over is the
    reference — 14 lines, the disc's grid at column 0 and half-row 0, each of
    its 784 half-cells the reference's colour or off the disc, the twin the
    reference's letters line for line, and the block form's text, codes
    stripped, the twin's with the owner's characters in place. The block
    form leads its `·` dim where the reference left it plain, which is the
    owner's decision 6's wording, and the reference is a picture of it.

    A real run's message is its label and its block and nothing else."""
    mod = stamp_module()
    letter = mod.compose(REFERENCE_ROWS, 0.9)
    assert (letter.height, letter.width, letter.disc) == (14, 77, (0, 0, 28, 28))
    assert mod.stamp(REFERENCE_ROWS, 0.9, shape=True) == list(REFERENCE_TWIN)
    for y, said in enumerate(REFERENCE_DISC):
        line = letter.cells[y // 2]
        for x, key in enumerate(said):
            # A line ends at its last visible cell, so past it is off the disc.
            char, fg, bg, _style = line[x] if x < len(line) else (None,) * 4
            top, bottom = (fg, bg) if char == "▀" else (bg, fg)
            half = top if y % 2 == 0 else bottom
            assert half == REFERENCE_COLOURS[key], (x, y, key, char, fg, bg)
    blocks = [mod.strip_ansi(line) for line in mod.stamp(REFERENCE_ROWS, 0.9)]
    ascii_ = str.maketrans({"·": ".", "✓": "+", "─": "-", "→": ">"})
    for line, twin in zip(blocks, REFERENCE_TWIN, strict=True):
        assert len(line) == len(twin), (line, twin)
        text = line.translate(ascii_)
        same = zip(text, twin, strict=True)
        assert all(a == b for a, b in same if a not in "▀▄"), (line, twin)
    label = mod.label(full_values())
    assert mod.fitted([(label, FULL_ROWS, 0.9)]) == "\n".join(
        [label, *mod.stamp(FULL_ROWS, 0.9, shape=False)]
    )


def test_two_files_in_one_turn_are_under_the_budget_together(tmp_path):
    """A3, two files, under the owner's rule of 2026-10-02 (`questions.md`
    Q6). Two stamps of a real run's size do not fit one message together
    even at the last rung, so the old rule drew both with no disc. The disc is kept
    now: the first is drawn whole at its own 0.90, the second stays pending
    under its own name, and the next `Stop` draws it whole — two turns,
    each message under the budget. The name is the case's from phase 1,
    kept because round 1's record cites it.

    Whether two real runs share a message is a fact about the drawing, and
    the emblem sets it (#832): under #717's lily two did not fit at 0.75, and
    under the interim ring of work item 1791270164 they did
    (`phases/phase-1.md` there has the sizes). The second run therefore
    carries deferral homes, one at a time, until the pair does not fit at
    the ladder's last rung — none under the lily or under phase 2's § at
    0.90, where this is the case as it stood, and some under the owner's
    14-cell disc, where two real runs share a message — and the premise is
    asserted rather than assumed."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    label = mod.label(full_values())
    budget, floor = mod.MESSAGE_BUDGET, mod.SCALE_LADDER[-1]
    alone = len(drawn(mod, label, FULL_ROWS, floor))
    homes = []
    while alone + 2 + len(drawn(mod, label, FULL_ROWS + homes, floor)) <= budget:
        homes.append(("", f"home-{len(homes)}"))
    rows = FULL_ROWS + homes
    late = {**full_values("ccc3333c"), "rows": rows}
    assert len(drawn(mod, mod.label(late), rows, 0.9)) <= budget, (
        "the second no longer fits at 0.90 alone",
        len(homes),
    )
    first = mod.write_values(str(repo / ".git"), "s-1", full_values(), now=1)
    second = mod.write_values(str(repo / ".git"), "s-1", late, now=2)
    text = json.loads(stop(repo))["systemMessage"]
    assert len(text) <= mod.MESSAGE_BUDGET, len(text)
    assert text == drawn(mod, label, FULL_ROWS, 0.9), "not the first, whole"
    assert os.path.exists(mod.drawn_path(first)) and not os.path.exists(first)
    assert os.path.exists(second), "the second was claimed with the first"
    later = json.loads(stop(repo))["systemMessage"]
    assert later == drawn(mod, mod.label(late), rows, 0.9)
    assert os.path.exists(mod.drawn_path(second)) and not os.path.exists(second)
    assert stop(repo) == "", "a drawn file was drawn a second time"


def test_seals_past_what_one_message_carries_wait_for_the_next_turn(tmp_path):
    """A3, any set — round 1's 🟡 1. Twelve files of a real run's size were
    all claimed and printed at once with no disc, 15,000 characters and more,
    which the harness persists. Now each `Stop` draws the oldest that fit
    with their disc, under `MESSAGE_BUDGET`, and leaves the rest pending in
    order; the next `Stop` takes the next, so twelve turns draw all twelve
    and none is drawn without its disc."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    # `now` of one width: the name sort is oldest first because a real time
    # in nanoseconds always has the same number of digits.
    paths = [
        mod.write_values(str(repo / ".git"), "s-1", full_values(f"{n:08x}"), now=n)
        for n in range(101, 113)
    ]
    before = 0
    for turn in range(1, 13):
        text = json.loads(stop(repo))["systemMessage"]
        assert len(text) <= mod.MESSAGE_BUDGET, (turn, len(text))
        blocks = text.split("\n\n")
        assert all("\x1b[38;2;" in b for b in blocks), f"turn {turn} lost a disc"
        drawn_now = [p for p in paths if os.path.exists(mod.drawn_path(p))]
        waiting = [p for p in paths if os.path.exists(p)]
        assert drawn_now == paths[: len(drawn_now)], "not oldest first"
        assert waiting == paths[len(drawn_now) :], "a file was lost"
        assert len(drawn_now) >= turn, f"turn {turn} drew nothing new"
        # A claim renames the file whether or not its stamp is printed, so
        # the drawn names alone cannot see a file claimed and dropped: the
        # message's labels are exactly the files this turn claimed.
        assert [b.split("\n", 1)[0] for b in blocks] == [
            mod.label(full_values(f"{n:08x}"))
            for n in range(101 + before, 101 + len(drawn_now))
        ], f"turn {turn} claimed a file its message does not carry"
        before = len(drawn_now)
        if not waiting:
            break
    assert stop(repo) == "", "something was left to draw"


def test_one_seal_too_large_for_the_disc_is_drawn_alone_without_it(tmp_path):
    """A4's last rung, under the owner's rule. A record whose stamp does not
    fit the budget with its disc at the ladder's last rung by itself — a
    long list of deferral homes — is the one case the text block is drawn
    with no disc, and it is drawn alone: the first pending file is always drawn, so
    the queue cannot stall, and the seal after it waits for the next `Stop`
    rather than losing its disc.

    The record carries deferral homes, one at a time, until its stamp does
    not fit with its disc: sixty did under phase 2's § of #832, and under
    the owner's 14-cell disc sixty fit, so the count is derived and the
    premise asserted rather than assumed."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    label = mod.label(full_values())
    rung = mod.SCALE_LADDER[-1]
    homes = []
    while len(drawn(mod, label, FULL_ROWS + homes, rung)) <= mod.MESSAGE_BUDGET:
        homes.append(("", f"home-{len(homes)}"))
    big = {**full_values(), "rows": FULL_ROWS + homes}
    oversized = mod.write_values(str(repo / ".git"), "s-1", big, now=1)
    after = mod.write_values(str(repo / ".git"), "s-1", full_values("ccc3333c"), now=2)
    assert mod.label(big) == label
    assert len(drawn(mod, label, big["rows"], rung)) > mod.MESSAGE_BUDGET
    text = json.loads(stop(repo))["systemMessage"]
    assert text == drawn(mod, label, big["rows"], None), "not the text block alone"
    assert "\x1b[38;2;" not in text, "the oversized seal drew a disc"
    assert os.path.exists(mod.drawn_path(oversized)) and os.path.exists(after)
    later = json.loads(stop(repo))["systemMessage"]
    assert later == drawn(mod, mod.label(full_values("ccc3333c")), FULL_ROWS, 0.9)


def test_a_character_outside_the_bmp_is_counted_as_two():
    """The round-1 question, measured in the fix pass: the harness counts a
    `systemMessage` in UTF-16 units, so 5,001 U+1D54F (10,002 units) were
    persisted where 4,999 were shown. Python's `len` counts each as one, so
    a label of them fitted a rung the harness would not. A budget between
    the two counts steps the block down — since #832 to the text block alone,
    the one step after 0.90."""
    mod = stamp_module()
    label = LABEL + " " + "\U0001d54f" * 50
    at = {s: drawn(mod, label, ROWS, s) for s in (0.9, None)}
    assert len(at[0.9].encode("utf-16-le")) // 2 == len(at[0.9]) + 50
    assert mod.fitted([(label, ROWS, 0.9)], len(at[0.9]) + 10) == at[None]
    assert mod.fitted([(label, ROWS, 0.9)], len(at[0.9]) + 50) == at[0.9]
    # A values file is JSON, which can carry a lone surrogate; counting it
    # must not raise, or every pending file would wait forever.
    lone = LABEL + "\ud800"
    assert mod.fitted([(lone, ROWS, 0.9)]) == drawn(mod, lone, ROWS, 0.9)


def test_a_values_file_from_an_older_gate_draws_every_row_in_the_new_layout(
    tmp_path,
):
    """A13. A file the gate wrote from #666 to #717 carries `null` blanks, a
    `chain` row, `exit 0` under the suite and `0 drifted . 0 broken` under
    the ledger, the base's ref on a row of its own and ` . ` between parts,
    and may still be pending when this hook draws it. Since #832 nothing
    converts it (`spec.md` §*Out* of work item 1791270164): every row it
    carries is drawn as text in the open layout, one line each and in order,
    its blanks as blank lines, under `label(values)`, at 0.90 with its disc.
    #717's name for this case said the blanks drew no line, which the sheet
    did; the open layout draws them, as `panel`'s own `None` is drawn."""
    mod = stamp_module()
    repo = opted_in(tmp_path)
    old = {**full_values(), "rows": OLD_ROWS}
    mod.write_values(str(repo / ".git"), "s-1", old)
    text = json.loads(stop(repo))["systemMessage"]
    label, *lines = text.split("\n")
    assert label == mod.label(old)
    assert lines == mod.stamp(OLD_ROWS, 0.9, shape=False), "not the 0.90 drawing"
    said = [mod.strip_ansi(line)[31:] for line in lines]
    rows = OLD_ROWS[1:]
    assert len(said) == max(14, 2 + len(rows)), len(said)
    top = (len(said) - 2 - len(rows)) // 2
    assert said[top].startswith("SEALED ─"), said[top]
    for k, row in enumerate(rows, top + 2):
        want = "" if row is None else f"{row[0]:<7} {row[1]}".rstrip()
        assert said[k] == want, (k, said[k], want)


def test_the_ladder_steps_down_in_order_and_ends_with_no_disc():
    """A4. Driven at small budgets: the file's own scale where it fits, then
    the ladder's one rung, 0.90 since #832, then the panel with no disc —
    which is returned whatever the budget, because nothing comes after it.
    Each block takes the highest rung the others leave room for, oldest
    first (`questions.md` Q6 of #717), and never a rung above the file's
    own scale; a newer block that does not fit beside the older waits rather
    than shrinking, because no smaller disc is drawn.

    Since the owner's 14-cell disc, every scale in the band draws the same
    bytes, so the drawing has two sizes — the disc and the text block alone —
    and a file at 1.0 that does not fit steps to the text block alone, as a file at
    0.90 does."""
    mod = stamp_module()
    at = {s: drawn(mod, LABEL, ROWS, s) for s in (1.0, *mod.SCALE_LADDER, None)}
    assert at[1.0] == at[0.9] == drawn(mod, LABEL, ROWS, 0.75), "the disc moved size"
    assert len(at[0.9]) > len(at[None]), (len(at[0.9]), len(at[None]))
    one = [(LABEL, ROWS, 0.9)]
    assert mod.fitted(one, len(at[0.9])) == at[0.9]
    assert mod.fitted(one, len(at[0.9]) - 1) == at[None]
    assert mod.fitted(one, 0) == at[None], "the last rung is the last"
    bare = mod.strip_ansi(at[None])
    assert "▀" not in bare and "▄" not in bare, "the last rung drew a disc"
    for row in ROWS[1:]:
        if row is not None:
            assert f"{row[0]:<7} {row[1]}".strip() in bare, row
    # A file at 1.0 keeps its disc where it fits, and is the text block alone
    # where it does not: there is no smaller disc between.
    big = [(LABEL, ROWS, 1.0)]
    assert mod.fitted(big, len(at[1.0])) == at[1.0]
    assert mod.fitted(big, len(at[1.0]) - 1) == at[None]
    # Two blocks that fit together at 0.90 are one message; where the newer
    # does not fit beside the older, it is left out rather than both losing
    # the disc or the newer shrinking.
    two = [(LABEL, ROWS, 0.9), (LABEL, ROWS, 0.9)]
    room = len(at[0.9]) * 2 + 2
    assert mod.fitted(two, room) == at[0.9] + "\n\n" + at[0.9]
    assert mod.admitted(two, room - 1) == [at[0.9]], "both drawn, or not at 0.90"
    # The older at 1.0 takes the rung the newer leaves room for.
    pair = [(LABEL, ROWS, 1.0), (LABEL, ROWS, 0.9)]
    assert mod.admitted(pair, room) == [at[0.9], at[0.9]]
    assert mod.admitted(pair, len(at[1.0]) + 2 + len(at[0.9])) == [at[1.0], at[0.9]]
    # Oldest first: a newer seal that would fit is not drawn ahead of an
    # older one that does not, which the hook would claim and not print.
    huge = (LABEL, ROWS + [("", f"home-{k}") for k in range(60)], 0.9)
    plain = (LABEL, ROWS, 0.9)
    assert mod.admitted([plain, huge, plain], room) == [at[0.9]], (
        "drawn past a seal that waits"
    )
    # A single seal exactly at the budget keeps its disc.
    assert mod.admitted([(LABEL, ROWS, 0.9)], len(at[0.9])) == [at[0.9]]
    # A file that asked for less is never drawn larger, and one that asked
    # for more than the first rung gets it where it fits.
    low = drawn(mod, LABEL, ROWS, 0.75)
    assert mod.fitted([(LABEL, ROWS, 0.75)], 10**6) == low
    assert mod.fitted([(LABEL, ROWS, 0.75)], len(low) - 1) == at[None]
    assert mod.fitted([(LABEL, ROWS, 1.0)], 10**6) == at[1.0]


def test_admitteds_docstring_fits_the_line_length():
    """S13 (#721). Round 3 of #717 reflowed one line of `admitted`'s
    docstring to 113 columns; the paragraph is round 3's paste-ready one,
    and no line of the docstring is wider than 79 as the source holds it —
    read from the source, because Python 3.13 strips a docstring's indent
    from `__doc__` and 3.12 keeps it. Seen red against the 113-column line."""
    source = inspect.getsource(stamp_module().admitted)
    doc = source.split('"""', 2)[1]
    wide = [line for line in source.splitlines() if line in doc and len(line) > 79]
    assert wide == [], wide


def test_the_policy_states_the_budget_and_names_its_case():
    """A18. `docs/the-broad-gate.md` §*Where the stamp is drawn* carries the
    budget rule under #717's marker, and its `Enforced by:` line names A3's
    case; the marker stands a second time over the paragraph nothing
    enforces. #832: the rule names the one rung with a disc and the text
    block alone after it, the owner's disc 28 cells across, and one real
    run to a message; the unchecked paragraph says nothing outside the disc
    is painted, so the stamp is read in the terminal's own theme, where it
    gave the parchment's contrast figures before decision 6 of work item
    1791270164 retired the sheet."""
    text = flat("docs", "the-broad-gate.md")
    marker = "<!-- specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner -->"
    assert text.count(marker) == 2, "the rule and the unchecked half, one marker each"
    unchecked = text.split(marker)[2]
    assert "**What the person's screen shows is not checked" in unchecked
    assert (
        "So is how the stamp reads on a light background as well as a dark one. "
        "Nothing outside the disc is painted, so its text is in the terminal's "
        "own colours and theme"
    ) in unchecked
    assert "1.02 and 1.48" not in unchecked and "parchment" not in unchecked
    rule = text.split(marker)[1].split("<!--", 1)[0]
    assert "**The hook holds its whole message under a budget named in the code" in rule
    assert "::test_the_hooks_message_is_under_the_budget_for_one_file" in rule
    # Round 1's 🟡 1, under the owner's rule of 2026-10-02 (`questions.md` Q6).
    assert "A seal past what one message can carry stays pending" in rule
    assert "::test_seals_past_what_one_message_carries_wait_for_the_next_turn" in rule
    assert "a character outside the BMP is two" in rule
    # #832: one rung with a disc, then the text block alone — and the reason
    # is the owner's 28-cell disc having one size, not a smaller disc refused.
    assert "then 0.90, the one rung with a disc since #832" in rule
    assert (
        "the owner's disc is drawn 28 cells across at every scale, so there is "
        "no smaller disc to step to"
    ) in rule
    assert "one real run's stamp goes out per message" in rule
    assert "does not fit with its disc by itself is the only one drawn" in rule
    assert "as the text block with no disc" in rule
    assert "0.80 and 0.75" not in rule and "at 0.75 by itself" not in rule
    assert "24 cells" not in rule and "§ fragment" not in rule
    assert "14 cells" not in rule and "sheet" not in rule
    section = text.split("## Where the stamp is drawn", 1)[1]
    assert marker in section.split("## What the runner owes", 1)[0]


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
        # Round 1's 🟡 1: the command is named on every line that points at a
        # values file now, and it stays the person's wherever it appears.
        "Wherever the `SEALED` line names `seal-stamp --from`, quote it as it "
        "stands: that command is the person's to type, and never yours.",
        # Round 1's ⬜ 7: the one route that writes the cell without the gate.
        "a cell written by `close --broad-gate` is sealed with no stamp",
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
    # Round 1's 🟡 1: the hook's silence where it cannot draw is stated where
    # a person looks for why no stamp appeared, with the way to draw it.
    assert "**Nor is the hook's silence where it cannot draw.**" in unchecked
    # Round 2's ⬜ 1: not EVERY sealed line — a run with no `--record` and
    # one whose values could not be written name no file and no command.
    assert (
        "every `SEALED` line that names a values file names `seal-stamp --from "
        "<path>` too"
    ) in unchecked
    assert "every sealed `SEALED` line" not in text
    # Round 1's ⬜ 6: a terminal draws only over a written cell, and the
    # `gate` row names the copy that measured, since in a sealer none draws.
    assert "the gate draws only on a terminal, and only over a written cell" in rule
    assert "the stamp says which copy drew it" not in text


def test_both_readmes_list_the_stamp_hook():
    """Round 1's 🟡 4. The hook inventory a user reads to learn what runs on
    their machine did not list the `Stop` hook, in either edition: the gate
    table, the opt-in list, the count of gates that wake on a condition, and
    the side effects. The editions move together, so both are read."""
    for edition, count, opt_in, effects, clause in (
        (
            "README.md",
            "Eight of the eleven gates",
            # The opt-in list's own words: the count sentence names the stamp
            # hook too, so the bare name would pass with the list unchanged.
            "the two implementer hooks, the stamp hook and the version check.",
            "Four side effects",
            # The clause's own words (round 2's ⬜ 2): the gate-table row
            # carries `specseal-stamp/` too, so the bare directory passed
            # with the side effect deleted.
            "`<git-common-dir>/specseal-stamp/`, which the stamp hook renames "
            "once drawn and nothing prunes",
        ),
        (
            "README.ko.md",
            "게이트 열하나 중 여덟",
            "구현자 훅 둘, 도장 훅, 버전 확인이다.",
            "네 가지 부수 효과",
            "도장 훅은 그린 뒤 그 파일의 이름을 바꿀 뿐 지우지 않습니다",
        ),
    ):
        text = flat(edition)
        table = [ln for ln in text.split("| ") if ln.startswith("sealer-stamp ")]
        assert table, f"{edition}'s gate table has no `sealer-stamp` row"
        assert count in text, (edition, count)
        assert opt_in in text, (edition, opt_in)
        assert effects in text and clause in text, (edition, effects, clause)
        assert "Seven of the ten" not in text and "게이트 열 중 일곱" not in text


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
    # Round 1's ⬜ 6: no gate draws in a sealer, so the `gate` row says which
    # copy measured the tree, not which drew the stamp.
    assert "which gate drew the stamp" not in text


# --- S13: the scale --------------------------------------------------------


def test_the_default_scale_is_ninety_percent_with_its_reason_beside_it():
    """S13. `DEFAULT_SCALE` is 0.90, and the comment above it says why and
    names 0.75 as the candidate passed over, so the next reader does not
    re-run #400's six-scale comparison to find out. Since #832's hand-drawn
    disc it also says the scale no longer sizes the disc, and nothing above
    it names the 24-cell disc or a floor the owner saw it fragment at."""
    mod = stamp_module()
    assert mod.DEFAULT_SCALE == 0.90
    with open(STAMP, encoding="utf-8") as handle:
        source = handle.read()
    above = source.split("DEFAULT_SCALE = 0.90", 1)[0].rsplit("\n\n", 1)[-1]
    assert "0.75 was the other candidate" in above, above
    assert "passed over" in above, above
    flat_above = " ".join(above.replace("#", " ").split())
    assert (
        "the disc is `DISC_CELLS` across at every scale in the band, so the "
        "scale sizes nothing"
    ) in flat_above, flat_above
    for gone in ("24 cells", "13 lines", "accepted nothing below 24", "fragment"):
        assert gone not in flat_above, gone


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
