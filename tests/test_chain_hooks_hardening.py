"""Hardening cases: prose-mention false positives, cycle edges, lease isolation."""

import json
import os
import subprocess

import pytest

from conftest import decision_of, run_hook


def payload(cmd, repo, session="s1"):
    return {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }


def opt_in(repo):
    (repo / "_ai").mkdir(exist_ok=True)


def git(repo, *a):
    return subprocess.run(
        ["git", "-C", str(repo), *a], capture_output=True, text=True, check=False
    )


# --- gate: prose mentions must not gate (regression for the fixed FP) -----


def test_gate_ignores_echoed_git_commit(repo):
    opt_in(repo)
    assert (
        decision_of(
            run_hook("commit-review-gate.py", payload("echo git commit -m x", repo))
        )
        == "silent"
    )


def test_gate_ignores_heredoc_mentions(repo):
    opt_in(repo)
    cmd = "cat > doc.md <<EOF\nrun: git commit -m x\nEOF"
    assert (
        decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "silent"
    )


def test_gate_catches_heredoc_message_commit(repo):
    # The commit form Claude Code itself is instructed to use: the message
    # arrives via $(cat <<'EOF' ...) inside double quotes. A quote-blind
    # splitter shredded this and the gate stayed silent.
    opt_in(repo)
    cmd = "git commit -m \"$(cat <<'EOF'\nfix: thing\n\nbody\nEOF\n)\""
    assert decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "ask"


def test_gate_catches_separators_inside_message(repo):
    opt_in(repo)
    for cmd in (
        'git commit -m "fix && update deps"',
        'git commit -m "a; b"',
        'git commit -m "line1\nline2"',
    ):
        assert (
            decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "ask"
        ), cmd


def test_gate_fails_closed_on_unparseable_commit(repo):
    # Unbalanced quotes defeat tokenization; if git+commit appear anyway,
    # asking beats exempting exactly the commands too gnarly to parse.
    opt_in(repo)
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload('git commit -m "unbalanced', repo)
            )
        )
        == "ask"
    )
    assert (
        decision_of(
            run_hook("commit-review-gate.py", payload('echo "unbalanced git', repo))
        )
        == "silent"
    )


def test_gate_catches_commit_after_cd_chain(repo):
    opt_in(repo)
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py", payload("cd sub && git commit -m x", repo)
            )
        )
        == "ask"
    )


def test_gate_catches_env_prefixed_commit(repo):
    opt_in(repo)
    cmd = "GIT_AUTHOR_DATE=2026-01-01T00:00:00 git commit -m x"
    assert decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "ask"


def test_gate_rearms_after_commit_moves_head(repo):
    opt_in(repo)
    gd = git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    with open(os.path.join(gd, "specseal-reviewed"), "w") as f:
        f.write(head)
    (repo / "f.txt").write_text("more\n")
    git(repo, "commit", "-qam", "next")  # cycle closes, mark goes stale
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "ask"
    )


def test_gate_ignores_non_bash_tools(repo):
    opt_in(repo)
    p = {
        "tool_name": "Write",
        "session_id": "s",
        "tool_input": {"file_path": str(repo / "x")},
        "cwd": str(repo),
    }
    assert decision_of(run_hook("commit-review-gate.py", p)) == "silent"


# --- history guard: prose mentions must not remind ------------------------


def test_history_guard_ignores_echoed_gh(repo):
    opt_in(repo)
    assert (
        run_hook(
            "review-history-guard.py", payload("echo gh pr comment 42", repo)
        ).strip()
        == ""
    )


def test_history_guard_catches_gh_after_chain(repo):
    opt_in(repo)
    out = run_hook(
        "review-history-guard.py", payload("cd x && gh pr comment 7 --body hi", repo)
    )
    assert "PR-7" in out


# --- session-lease: repo resolution and isolation -------------------------


def leases_of(repo):
    gd = git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()
    d = os.path.join(gd, "specseal-leases")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def test_edit_tool_leases_like_write(repo, tmp_path):
    p = {
        "tool_name": "Edit",
        "session_id": "sess-e",
        "tool_input": {"file_path": str(repo / "f.txt")},
        "cwd": str(tmp_path),
    }
    run_hook("session-lease.py", p)
    assert "sess-e" in leases_of(repo)


def test_bash_in_subdir_leases_repo_root(repo):
    (repo / "sub").mkdir()
    p = {
        "tool_name": "Bash",
        "session_id": "sess-sub",
        "tool_input": {"command": "ls"},
        "cwd": str(repo / "sub"),
    }
    run_hook("session-lease.py", p)
    assert "sess-sub" in leases_of(repo)


def test_linked_worktree_lease_stays_isolated(repo, tmp_path):
    wt = tmp_path / "wt"
    git(repo, "worktree", "add", "-q", str(wt), "feature/x")
    p = {
        "tool_name": "Bash",
        "session_id": "sess-wt",
        "tool_input": {"command": "ls"},
        "cwd": str(wt),
    }
    run_hook("session-lease.py", p)
    # the worktree session's lease lands in the worktree's own git-dir,
    # so it does NOT count against the main tree (already-isolated rule)
    assert "sess-wt" not in leases_of(repo)


def test_missing_session_id_falls_back_to_pid(repo):
    p = {"tool_name": "Bash", "tool_input": {"command": "ls"}, "cwd": str(repo)}
    run_hook("session-lease.py", p)
    assert any(name.startswith("pid-") for name in leases_of(repo))


# --- packaging sanity ------------------------------------------------------

ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_hooks_json_points_at_existing_python_scripts():
    # Every hook must run through an explicit `python3` (shebang + exec bit
    # don't exist on Windows) and its script file must exist in the plugin.
    with open(os.path.join(ROOT, "hooks", "hooks.json")) as f:
        cfg = json.load(f)
    for groups in cfg["hooks"].values():
        for group in groups:
            for h in group["hooks"]:
                cmd = h["command"]
                assert cmd.startswith('python3 "${CLAUDE_PLUGIN_ROOT}/'), cmd
                rel = cmd.split('"')[1].replace("${CLAUDE_PLUGIN_ROOT}/", "")
                assert rel.endswith(".py"), f"non-python hook: {rel}"
                assert os.path.isfile(os.path.join(ROOT, rel)), rel


def test_plugin_version_is_in_changelog():
    # The changelog starts at the first public release, so commits before it
    # legitimately have no file — the claim under test is "if a changelog
    # exists, it must mention the version being shipped".
    changelog = os.path.join(ROOT, "CHANGELOG.md")
    if not os.path.isfile(changelog):
        pytest.skip("no CHANGELOG.md in this tree")
    with open(os.path.join(ROOT, ".claude-plugin", "plugin.json")) as f:
        version = json.load(f)["version"]
    with open(changelog) as f:
        assert version in f.read(), f"CHANGELOG missing {version}"


def test_bin_wrapper_resolves_the_checker_from_any_cwd():
    # bin/ lands on the Bash tool's PATH while the plugin is enabled, so the
    # wrapper must resolve the script relative to itself, never the caller's
    # working directory.
    wrapper = os.path.join(ROOT, "bin", "evidence-check")
    assert os.path.isfile(wrapper), "bin/evidence-check missing"
    assert os.access(wrapper, os.X_OK), "bin/evidence-check not executable"
    target = os.path.join(ROOT, "skills", "evidence-check", "scripts",
                          "evidence_check.py")
    assert os.path.isfile(target), "wrapper points at a missing script"
    r = subprocess.run([wrapper, "--help"], cwd="/", capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "evidence_check" in r.stdout


def test_migrated_commands_stay_user_invoked():
    # These three shipped as commands/ (user-invoked). Moving them to skills/
    # must not silently turn them into auto-triggering skills.
    for name in ("preset-setup", "security-audit", "testing"):
        p = os.path.join(ROOT, "skills", name, "SKILL.md")
        assert os.path.isfile(p), f"{name} not migrated"
        head = open(p).read().split("\n---\n", 1)[0]
        assert "disable-model-invocation: true" in head, name
    assert not os.path.isdir(os.path.join(ROOT, "commands")), \
        "commands/ should be gone — skills/ is the documented layout"


def test_parity_declaration_is_bootstrappable_not_hand_written():
    # docs/parity.md is the one declaration a user cannot derive, so the
    # blank-page problem is real: without a template and a place that asks,
    # migration mode is a feature nobody can reach.
    tpl = os.path.join(ROOT, "templates", "parity.md")
    assert os.path.isfile(tpl), "templates/parity.md missing"
    body = open(tpl).read()
    for field in ("Original repo", "Baseline commit", "Policy root",
                  "Coordinate-trust exceptions"):
        assert field in body, f"template lost the {field!r} field"
    assert "parity-paths.md" in body, "template must say where the local path goes"

    implement = open(os.path.join(ROOT, "skills", "implement", "SKILL.md")).read()
    assert "templates/parity.md" in implement, "bootstrap never points at the template"
    assert "_ai/README.md" in implement

    setup = os.path.join(ROOT, "skills", "parity-setup", "SKILL.md")
    assert os.path.isfile(setup), "no command for declaring parity later"
    head = open(setup).read().split("\n---\n", 1)[0]
    assert "disable-model-invocation: true" in head, \
        "parity-setup writes a declaration; it must not fire on its own"


def test_ci_wiring_never_asks_for_the_plugin_path():
    # The CI setup used to say `cp <specseal plugin>/skills/...`, a path the
    # docs never gave — the same dead end bin/ fixed for the CLI. Whatever the
    # instructions say, they must not send a reader hunting for the install
    # location.
    setup = os.path.join(ROOT, "skills", "evidence-ci", "SKILL.md")
    assert os.path.isfile(setup), "no command wires the drift check into CI"
    head = open(setup).read().split("\n---\n", 1)[0]
    assert "disable-model-invocation: true" in head, \
        "this writes files into a repo; it must not fire on its own"

    tpl = open(os.path.join(ROOT, "templates", "evidence-check.yml")).read()
    assert "<specseal plugin>" not in tpl, "template still names an unknown path"
    assert "/specseal:evidence-ci" in tpl, "template should point at the command"
    # The workflow must still do the thing it exists for.
    assert "evidence_check.py" in tpl and "fetch-depth: 0" in tpl

    skill = open(os.path.join(ROOT, "skills", "evidence-check", "SKILL.md")).read()
    assert "/specseal:evidence-ci" in skill, "CI section never mentions the command"


def parity_repo(repo):
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "parity.md").write_text("| Original repo | org/legacy |\n")


def stage(repo, name, body="x\n"):
    (repo / name).write_text(body)
    git(repo, "add", name)


def test_parity_repo_asks_when_code_commits_without_a_comparison(repo):
    parity_repo(repo)
    stage(repo, "service.py")
    d = decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
    assert d == "ask"


def test_parity_mark_matching_head_allows(repo):
    parity_repo(repo)
    stage(repo, "service.py")
    gd = git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    with open(os.path.join(gd, "specseal-parity"), "w") as f:
        f.write(head)
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git commit -m x", repo))) == "silent"


def test_parity_gate_ignores_document_only_commits(repo):
    # Asking on a docs-only commit trains people to click through the prompt.
    parity_repo(repo)
    (repo / "docs" / "policies").mkdir(parents=True, exist_ok=True)
    stage(repo, "docs/policies/note.md", "text\n")
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git commit -m x", repo))) == "silent"


def test_parity_gate_silent_without_the_declaration(repo):
    stage(repo, "service.py")
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git commit -m x", repo))) == "silent"


def test_no_parity_escape_is_visible_in_the_command(repo):
    parity_repo(repo)
    stage(repo, "service.py")
    assert decision_of(run_hook("commit-review-gate.py",
                                payload("git commit -m x [no-parity]", repo))) == "silent"


def test_both_opt_ins_report_together(repo):
    parity_repo(repo)
    opt_in(repo)
    stage(repo, "service.py")
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "ask"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "specseal-reviewed" in reason and "specseal-parity" in reason, reason
