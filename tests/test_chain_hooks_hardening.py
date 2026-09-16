"""Hardening cases: prose-mention false positives, cycle edges, lease isolation."""

import json
import os
import re
import subprocess
import sys

import pytest
from conftest import decision_of, declare_routing, fired, run_hook


def payload(cmd, repo, session="s1"):
    return {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }


def opt_in(repo):
    (repo / "seal").mkdir(exist_ok=True)


def git(repo, *a):
    return subprocess.run(
        ["git", "-C", str(repo), *a],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
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
    assert fired(run_hook("commit-review-gate.py", payload(cmd, repo)))


def test_gate_catches_separators_inside_message(repo):
    opt_in(repo)
    for cmd in (
        'git commit -m "fix && update deps"',
        'git commit -m "a; b"',
        'git commit -m "line1\nline2"',
    ):
        assert fired(run_hook("commit-review-gate.py", payload(cmd, repo))), cmd


def test_gate_fails_closed_on_unparseable_commit(repo):
    # Unbalanced quotes defeat tokenization; if git+commit appear anyway,
    # asking beats exempting exactly the commands too gnarly to parse.
    opt_in(repo)
    assert fired(
        run_hook("commit-review-gate.py", payload('git commit -m "unbalanced', repo))
    )
    assert (
        decision_of(
            run_hook("commit-review-gate.py", payload('echo "unbalanced git', repo))
        )
        == "silent"
    )


def test_gate_catches_commit_after_cd_chain(repo):
    opt_in(repo)
    assert fired(
        run_hook("commit-review-gate.py", payload("cd sub && git commit -m x", repo))
    )


def test_gate_catches_env_prefixed_commit(repo):
    opt_in(repo)
    cmd = "GIT_AUTHOR_DATE=2026-01-01T00:00:00 git commit -m x"
    assert fired(run_hook("commit-review-gate.py", payload(cmd, repo)))


def test_gate_rearms_after_commit_moves_head(repo):
    opt_in(repo)
    gd = git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    with open(os.path.join(gd, "specseal-reviewed"), "w", encoding="utf-8") as f:
        f.write(head)
    (repo / "f.txt").write_text("more\n")
    git(repo, "commit", "-qam", "next")  # cycle closes, mark goes stale
    assert fired(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))


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
    item = declare_routing(repo)
    out = run_hook(
        "review-history-guard.py", payload("cd x && gh pr comment 7 --body hi", repo)
    )
    assert item.name in out, out


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


def _hook_commands():
    with open(os.path.join(ROOT, "hooks", "hooks.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    return [
        h["command"]
        for groups in cfg["hooks"].values()
        for group in groups
        for h in group["hooks"]
    ]


def test_hooks_json_points_at_existing_python_scripts():
    # Every hook runs through an explicit interpreter -- shebang and exec bit
    # do not exist on Windows -- and every script it names must be in the
    # plugin, on either side of the fallback.
    for cmd in _hook_commands():
        for alt in cmd.split(" || "):
            rel = alt.split('"')[1].replace("${CLAUDE_PLUGIN_ROOT}/", "")
            assert rel.endswith(".py"), f"non-python hook: {rel}"
            assert os.path.isfile(os.path.join(ROOT, rel)), rel


def test_every_hook_names_a_windows_interpreter_after_the_posix_one():
    # `python3` is the documented requirement and stays first, so a POSIX
    # machine never pays for a second attempt. It is also the one name the
    # official Windows installer does not create -- that installer ships the
    # `py` launcher instead -- so a command knowing only `python3` leaves
    # every gate silent there, which is the failure direction that allows.
    #
    # The fallback runs only when the first alternative could not start:
    # dispatch exits 0 for every decision it makes, deny included, so `||`
    # is never a second run of a gate that already decided.
    for cmd in _hook_commands():
        alts = cmd.split(" || ")
        assert len(alts) == 2, f"expected exactly one fallback: {cmd}"
        assert alts[0].startswith('python3 "${CLAUDE_PLUGIN_ROOT}/'), cmd
        assert alts[1].startswith('py -3 "${CLAUDE_PLUGIN_ROOT}/'), cmd


def test_the_fallback_runs_the_same_script_with_the_same_arguments():
    # A fallback naming another group is worse than no fallback: the gates
    # that fired would be the wrong ones, and only on the platform nobody
    # runs by hand.
    for cmd in _hook_commands():
        first, second = cmd.split(" || ")
        assert first.split('"')[1:] == second.split('"')[1:], cmd


def test_plugin_version_is_in_changelog():
    # The changelog starts at the first public release, so commits before it
    # legitimately have no file — the claim under test is "if a changelog
    # exists, it must mention the version being shipped".
    changelog = os.path.join(ROOT, "CHANGELOG.md")
    if not os.path.isfile(changelog):
        pytest.skip("no CHANGELOG.md in this tree")
    with open(
        os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"
    ) as f:
        version = json.load(f)["version"]
    with open(changelog, encoding="utf-8") as f:
        assert version in f.read(), f"CHANGELOG missing {version}"


def test_bin_wrapper_resolves_the_checker_from_any_cwd():
    # bin/ lands on the Bash tool's PATH while the plugin is enabled, so the
    # wrapper must resolve the script relative to itself, never the caller's
    # working directory. Windows can't run a POSIX shebang script directly,
    # so a .cmd sibling ships alongside it -- PATHEXT resolves a bare
    # `evidence-check` to whichever one the platform can execute.
    posix_wrapper = os.path.join(ROOT, "bin", "evidence-check")
    windows_wrapper = os.path.join(ROOT, "bin", "evidence-check.cmd")
    assert os.path.isfile(posix_wrapper), "bin/evidence-check missing"
    assert os.path.isfile(windows_wrapper), "bin/evidence-check.cmd missing"
    assert os.access(posix_wrapper, os.X_OK), "bin/evidence-check not executable"
    target = os.path.join(
        ROOT, "skills", "evidence-check", "scripts", "evidence_check.py"
    )
    assert os.path.isfile(target), "wrapper points at a missing script"
    wrapper = windows_wrapper if sys.platform == "win32" else posix_wrapper
    r = subprocess.run(
        [wrapper, "--help"],
        cwd="/",
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert r.returncode == 0, r.stderr
    assert "evidence_check" in r.stdout


def test_migrated_commands_stay_user_invoked():
    # These three shipped as commands/ (user-invoked). Moving them to skills/
    # must not silently turn them into auto-triggering skills.
    for name in ("preset-setup", "security-audit", "testing"):
        p = os.path.join(ROOT, "skills", name, "SKILL.md")
        assert os.path.isfile(p), f"{name} not migrated"
        head = open(p, encoding="utf-8").read().split("\n---\n", 1)[0]
        assert "disable-model-invocation: true" in head, name
    assert not os.path.isdir(os.path.join(ROOT, "commands")), (
        "commands/ should be gone — skills/ is the documented layout"
    )


def test_parity_declaration_is_bootstrappable_not_hand_written():
    # The migration config is the one declaration a user cannot derive, so the
    # blank-page problem is real: without a template and a place that asks,
    # migration mode is a feature nobody can reach.
    tpl = os.path.join(ROOT, "templates", "parity.md")
    assert os.path.isfile(tpl), "templates/parity.md missing"
    body = open(tpl, encoding="utf-8").read()
    for field in (
        "Original repo",
        "Baseline commit",
        "Policy root",
        "Coordinate-trust exceptions",
    ):
        assert field in body, f"template lost the {field!r} field"
    assert "parity-paths.md" in body, "template must say where the local path goes"

    # The bootstrap and the parity setup are the orchestrator's half of the
    # skill since #292, so the file that has to point at the template is
    # `orchestration.md`, not the `SKILL.md` every smith spawn preloads.
    implement = open(
        os.path.join(ROOT, "skills", "implement", "orchestration.md"),
        encoding="utf-8",
    ).read()
    assert "templates/parity.md" in implement, "bootstrap never points at the template"
    assert "seal/README.md" in implement

    setup = os.path.join(ROOT, "skills", "parity-setup", "SKILL.md")
    assert os.path.isfile(setup), "no command for declaring parity later"
    head = open(setup, encoding="utf-8").read().split("\n---\n", 1)[0]
    assert "disable-model-invocation: true" in head, (
        "parity-setup writes a declaration; it must not fire on its own"
    )


def test_ci_wiring_never_asks_for_the_plugin_path():
    # The CI setup used to say `cp <specseal plugin>/skills/...`, a path the
    # docs never gave — the same dead end bin/ fixed for the CLI. Whatever the
    # instructions say, they must not send a reader hunting for the install
    # location.
    setup = os.path.join(ROOT, "skills", "evidence-ci", "SKILL.md")
    assert os.path.isfile(setup), "no command wires the drift check into CI"
    head = open(setup, encoding="utf-8").read().split("\n---\n", 1)[0]
    assert "disable-model-invocation: true" in head, (
        "this writes files into a repo; it must not fire on its own"
    )

    tpl = open(
        os.path.join(ROOT, "templates", "evidence-check.yml"), encoding="utf-8"
    ).read()
    assert "<specseal plugin>" not in tpl, "template still names an unknown path"
    assert "/specseal:evidence-ci" in tpl, "template should point at the command"
    # The workflow must still do the thing it exists for.
    assert "evidence_check.py" in tpl and "fetch-depth: 0" in tpl

    skill = open(
        os.path.join(ROOT, "skills", "evidence-check", "SKILL.md"), encoding="utf-8"
    ).read()
    assert "/specseal:evidence-ci" in skill, "CI section never mentions the command"


def parity_repo(repo):
    """Declare the migration config — which now opts into the review arm too.

    It used to be possible to declare parity alone, through the pre-0.10
    `docs/parity.md`. That address is gone, and the current one lives INSIDE
    `seal/`, so writing it creates the directory whose existence is the
    review opt-in. The two arms are still evaluated independently — own
    marker, own waiver token, own silence rules — but they can no longer be
    declared independently, and `docs/review-chain-spec.md` says so.

    These cases are about the parity arm on its own, so they carry
    `[no-review]` to silence the other one. That is the per-command waiver
    doing exactly its job.
    """
    (repo / "seal").mkdir(exist_ok=True)
    (repo / "seal" / "parity.md").write_text("| Original repo | org/legacy |\n")


def parity_only(command):
    """`command` with the review arm waived, so the parity arm answers alone."""
    return f"{command} [no-review]"


def stage(repo, name, body="x\n"):
    (repo / name).write_text(body)
    git(repo, "add", name)


def test_parity_repo_asks_when_code_commits_without_a_comparison(repo):
    parity_repo(repo)
    stage(repo, "service.py")
    cmd = parity_only("git commit -m x")
    out = run_hook("commit-review-gate.py", payload(cmd, repo))
    assert decision_of(out) == "deny"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "[no-parity]" in reason
    assert "[no-review]" not in reason, (
        "the parity arm fired alone — naming the review marker sends the user "
        "to the one token that does not silence it"
    )


def test_the_parity_arms_plain_prompt_names_its_own_marker(repo):
    """The closing sentence used to be hardcoded to `[no-review]`, so a commit
    stopped by the parity arm alone was told to re-issue with a token that
    changes nothing here."""
    parity_repo(repo)
    stage(repo, "service.py")
    cmd = parity_only("git commit -m x")
    run_hook("commit-review-gate.py", payload(cmd, repo))  # spends it
    out = run_hook("commit-review-gate.py", payload(cmd, repo))
    assert decision_of(out) == "ask"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "[no-parity]" in reason and "[no-review]" not in reason


def test_parity_mark_matching_head_allows(repo):
    parity_repo(repo)
    stage(repo, "service.py")
    gd = git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    with open(os.path.join(gd, "specseal-parity"), "w", encoding="utf-8") as f:
        f.write(head)
    cmd = parity_only("git commit -m x")
    assert (
        decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "silent"
    )


def test_parity_gate_ignores_document_only_commits(repo):
    # Asking on a docs-only commit trains people to click through the prompt.
    parity_repo(repo)
    (repo / "docs" / "policies").mkdir(parents=True, exist_ok=True)
    stage(repo, "docs/policies/note.md", "text\n")
    cmd = parity_only("git commit -m x")
    assert (
        decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "silent"
    )


def test_parity_gate_silent_without_the_declaration(repo):
    stage(repo, "service.py")
    assert (
        decision_of(run_hook("commit-review-gate.py", payload("git commit -m x", repo)))
        == "silent"
    )


def test_no_parity_escape_is_visible_in_the_command(repo):
    parity_repo(repo)
    stage(repo, "service.py")
    assert (
        decision_of(
            run_hook(
                "commit-review-gate.py",
                payload(parity_only("git commit -m x [no-parity]"), repo),
            )
        )
        == "silent"
    )


def test_parity_gate_sees_commits_that_never_touched_the_index(repo):
    """`-a` and a trailing pathspec both skip staging.

    The gate read only `git diff --cached`, so these two forms — the ones
    people type by hand — reported an empty change and the gate went silent
    on them."""
    parity_repo(repo)
    (repo / "f.txt").write_text("one\ntwo\nfour\n")  # tracked, never staged
    for cmd in (
        "git commit -am x",
        "git commit -a -m x",
        "git commit -m x f.txt",
        "git commit -mfix f.txt",
        "git commit -m x -- f.txt",
    ):
        one = parity_only(cmd)
        assert fired(run_hook("commit-review-gate.py", payload(one, repo))), one


def test_an_unstaged_document_change_still_does_not_ask(repo):
    """The `-a` fix must not turn every docs commit into a prompt."""
    parity_repo(repo)
    (repo / "docs").mkdir(exist_ok=True)
    (repo / "docs" / "note.md").write_text("text\n")
    git(repo, "add", "docs/note.md")
    git(repo, "commit", "-qm", "docs")
    (repo / "docs" / "note.md").write_text("more text\n")
    cmd = parity_only("git commit -am x")
    assert (
        decision_of(run_hook("commit-review-gate.py", payload(cmd, repo))) == "silent"
    )


def test_user_invoked_skills_do_not_carry_trigger_scaffolding():
    """`Use when:` / `NOT for:` exist to route the model's own choice.

    A skill the model can never choose is picked by a person typing its name,
    and the routing paragraph does nothing there but take space."""
    import glob

    offenders = []
    for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        with open(path, encoding="utf-8") as f:
            head = f.read().split("\n---\n", 1)[0]
        if "disable-model-invocation: true" not in head:
            continue
        if "Use when:" in head or "NOT for:" in head:
            offenders.append(os.path.basename(os.path.dirname(path)))
    assert not offenders, (
        f"user-invoked skills carrying auto-trigger scaffolding: {offenders}"
    )


def test_declaring_the_migration_config_opts_into_the_review_arm_too(repo):
    """The two opt-ins stopped being independently declarable at 0.10.

    `docs/review-chain-spec.md` claimed a repo could have `.specseal/parity.md`
    and no `.specseal/`, which the path makes impossible. The claim survived
    because the pre-0.10 `docs/parity.md` could still produce that state, and
    the tests here used it. Removing that address is what made the claim
    visible; the document now says the arms are evaluated independently and
    declared together.
    """
    parity_repo(repo)
    stage(repo, "service.py")
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "specseal-reviewed" in reason and "specseal-parity" in reason


def test_both_opt_ins_report_together(repo):
    parity_repo(repo)
    opt_in(repo)
    stage(repo, "service.py")
    out = run_hook("commit-review-gate.py", payload("git commit -m x", repo))
    assert decision_of(out) == "deny"
    reason = json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]
    assert "specseal-reviewed" in reason and "specseal-parity" in reason, reason
    # Two axes waived independently, so two questions — but ONE call, because
    # a second call is a second interruption for a decision made at once.
    assert "BOTH questions in ONE call" in reason
    assert "[no-review]" in reason and "[no-parity]" in reason


NUMBER_WORDS = {
    20: ("Twenty", "스무"),
    21: ("Twenty-one", "스물한"),
    22: ("Twenty-two", "스물두"),
    23: ("Twenty-three", "스물세"),
}

# Where each edition states the count. Scoping to the row is not tidiness:
# `README.ko.md` says `스무 번` about something else entirely, and a
# whole-file search reads that as a stale skill count.
SKILL_ROW = {"README.md": "| Skills |", "README.ko.md": "| 스킬 |"}


def test_both_readmes_count_the_skills_that_are_actually_there():
    """The count is prose in two languages, and shipping a skill is a diff
    that never opens either file.

    Deriving it is the point. `CONTRIBUTING.md` requires the two editions to
    move together, so a check that read only the English one would license
    exactly half the drift.
    """
    import glob

    shipped = len(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md")))
    assert shipped in NUMBER_WORDS, (
        f"{shipped} skills ship and no spelling is recorded for that number "
        "-- add it to NUMBER_WORDS rather than loosening the check"
    )
    english, korean = NUMBER_WORDS[shipped]

    def says(text, word):
        # A bare `in` reads `Twenty` out of `Twenty-one`, which makes the
        # stale half fire on a correct document and the present half pass on
        # a wrong one. Both directions need the boundary.
        return re.search(re.escape(word) + r"(?![-\w])", text) is not None

    for edition, word in (("README.md", english), ("README.ko.md", korean)):
        with open(os.path.join(ROOT, edition), encoding="utf-8") as f:
            rows = [ln for ln in f if ln.startswith(SKILL_ROW[edition])]
        assert len(rows) == 1, (
            f"{edition} has {len(rows)} rows starting `{SKILL_ROW[edition]}`; "
            "the check reads exactly one"
        )
        row = rows[0]
        assert says(row, word), (
            f"{edition}'s skills row does not say `{word}`, and {shipped} "
            f"skills ship: {row.strip()[:120]}"
        )
        for other, (wrong_en, wrong_ko) in NUMBER_WORDS.items():
            if other == shipped:
                continue
            stale = wrong_en if edition == "README.md" else wrong_ko
            assert not says(row, stale), (
                f"{edition}'s skills row still says `{stale}` while "
                f"{shipped} skills ship"
            )


def test_every_shipped_skill_is_named_in_both_readmes():
    """A count that matches while a name is missing is the quieter half.

    Round 1 found the first version of this useless in both directions. It
    searched the WHOLE file for a BARE name, so `audit` was satisfied by
    `/specseal:security-audit` in the cheat sheet and `verify` by two
    sentences of prose -- removing either from both editions' lists stayed
    green. The name is looked for in backticks, and in the row that lists
    the group, which is the only place its absence means anything."""
    import glob

    listed = {
        name
        for path in glob.glob(os.path.join(ROOT, "agents", "*.md"))
        for name in re.findall(
            r"^  - (\S+)", open(path, encoding="utf-8").read().split("\n---\n")[0], re.M
        )
    }
    for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(path))
        head = open(path, encoding="utf-8").read().split("\n---\n", 1)[0]
        user_invoked = "disable-model-invocation: true" in head
        for edition in ("README.md", "README.ko.md"):
            with open(os.path.join(ROOT, edition), encoding="utf-8") as f:
                text = f.read()
            if name in listed:
                # Round 2: `\`code-review\` in text` was satisfied by the
                # hook table thirty rows below, so removing it from BOTH
                # editions' agents column stayed green -- which agent
                # preloads what is the whole content of that column.
                agent_rows = [ln for ln in text.splitlines() if ln.startswith("| **")]
                assert any(f"`{name}`" in ln for ln in agent_rows), (
                    f"{edition}'s agents table never names `{name}` as "
                    "preloaded by any agent"
                )
                continue
            if user_invoked:
                # A skill nobody can trigger is reachable only as a typed
                # command, so that is the form that has to be shown.
                assert f"/specseal:{name}" in text, (
                    f"{edition} never shows `{name}` in the form a person types"
                )
                continue
            rows = [ln for ln in text.splitlines() if ln.startswith(SKILL_ROW[edition])]
            assert f"`{name}`" in rows[0], (
                f"{edition}'s skills row does not list `{name}`, which no "
                "agent preloads and nobody can type"
            )


def test_the_readme_group_counts_are_derived_too():
    """21 = 4 + 11 + 6, and all four numbers were prose.

    Round 1: the total was pinned and the split was not, so a skill could
    move between groups, or the middle count could go stale against its own
    list, with nothing red. Each group has a machine-readable definition --
    preloaded by an agent, typed by a person, neither -- so each is spelled
    from that rather than from the sentence beside it."""
    import glob

    paths = glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))
    preloaded = {
        name
        for path in glob.glob(os.path.join(ROOT, "agents", "*.md"))
        for name in re.findall(
            r"^  - (\S+)", open(path, encoding="utf-8").read().split("\n---\n")[0], re.M
        )
    }
    user_invoked = {
        os.path.basename(os.path.dirname(p))
        for p in paths
        if "disable-model-invocation: true"
        in open(p, encoding="utf-8").read().split("\n---\n", 1)[0]
    }
    on_demand = {os.path.basename(os.path.dirname(p)) for p in paths}
    on_demand -= preloaded | user_invoked

    # Round 2: the counts were derived correctly and then looked for
    # ANYWHERE in the one row that holds all three, so swapping the three
    # words between the groups stayed green -- `four more a session loads`
    # above a list of eleven. The word is anchored to its own group's
    # sentence, which also settles `열` being a prefix of `열한`.
    groups = {
        "preloaded": (len(preloaded), ("The %s the agents follow", "따르는 %s 개는")),
        "on demand": (len(on_demand), ("%s more a session loads", "%s 개는 작업이")),
        "user invoked": (len(user_invoked), ("%s you invoke by name", "나머지 %s은")),
    }
    spellings = {
        4: ("four", "네"),
        5: ("five", "다섯"),
        6: ("Six", "여섯"),
        7: ("Seven", "일곱"),
        10: ("Ten", "열"),
        11: ("Eleven", "열한"),
        12: ("Twelve", "열두"),
    }
    for group, (count, phrases) in groups.items():
        assert count in spellings, (
            f"the `{group}` group holds {count} skills and no spelling is "
            "recorded -- add it rather than loosening the check"
        )
        english, korean = spellings[count]
        for edition, word, phrase in (
            ("README.md", english, phrases[0]),
            ("README.ko.md", korean, phrases[1]),
        ):
            with open(os.path.join(ROOT, edition), encoding="utf-8") as f:
                rows = [ln for ln in f if ln.startswith(SKILL_ROW[edition])]
            assert phrase % word in rows[0], (
                f"{edition}'s skills row does not say `{phrase % word}`, and "
                f"the `{group}` group holds {count}"
            )
    assert sum(c for c, _ in groups.values()) == len(paths), (
        "the three groups do not partition the shipped skills"
    )


def test_the_writing_style_handoff_names_a_skill_that_ships():
    """Round 1, M6: reverting the handoff to its receiverless form was green.

    That line having no receiver IS the third strand of the work that added
    one, and every check on it compared the new text to itself. The pin is
    two facts: the frontmatter names a skill, and that skill is on disk --
    a name pointing at nothing is the same defect spelled differently."""
    head = (
        open(
            os.path.join(ROOT, "skills", "writing-style", "SKILL.md"), encoding="utf-8"
        )
        .read()
        .split("\n---\n", 1)[0]
    )
    assert "NOT for:" in head, "the boundary went, so the handoff has no sender"
    assert "commit-pr-convention" in head, (
        "the handoff lost its receiver again -- `NOT for: … branch/commit "
        "format` pointing at nobody is what shipped a PR with no prefix"
    )
    assert os.path.exists(
        os.path.join(ROOT, "skills", "commit-pr-convention", "SKILL.md")
    ), "the frontmatter names a skill that does not ship"


def test_auto_firing_skills_declare_when_not_to_fire():
    # Model-invoked skills load into context when their description matches.
    # Keyword-shaped triggers ("auto-triggers on implement/create/build") fire
    # on nearly every request, which is the redundant-context cost the README
    # cites a paper about. Each one states where it does NOT belong.
    import glob

    offenders = []
    for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
        head = open(path, encoding="utf-8").read().split("\n---\n", 1)[0]
        if "disable-model-invocation: true" in head:
            continue  # user-invoked; never fires on its own
        name = os.path.basename(os.path.dirname(path))
        if "NOT for" not in head:
            offenders.append(name)
    assert not offenders, (
        "model-invoked skills with no NOT-for boundary — each will fire on "
        f"matches it should leave to another skill: {offenders}"
    )


# The stems that mark a person answering, and the window the sweep below
# reads them in. AT MODULE LEVEL so a case can assert what they do: the
# pattern IS the behaviour this repair changes, and a pattern nothing opens is
# the shape this whole release keeps finding
# (`seal/specs/1789455558-…/overview.md` — pin the thing the production path
# calls, never a copy beside it).
#
# Matched at a WORD BOUNDARY, and the first draft of this guard was not. A
# bare `"ask" in window` fires on `task`, so the probe that was supposed to
# show the contract's own wording passing — `open every coordinate a task
# names in one batch` — went red on the word `task`. That is the same defect
# as the one being guarded against, one layer down: a substring standing in
# for a word.
#
# #422, half one: that repair anchored the FRONT of each stem and left the
# back open, so a stem matched inside a longer word and the same defect stood
# one layer down again. Measured: `agent-contract` §10's own wording — *open
# every coordinate a task names in one batch* — refused at exit 1 with
# `persona` one clause away, which `agents/smith.md` already writes. Both ends
# are anchored now, and the back anchor is what splits the stems into two
# groups.
#
# These carry their inflections, because an instruction is written in any of
# them: `asks`, `asked`, `asking`, `questions`, `answers`, `answered`.
ASKING_INFLECTED = ("question", "ask", "answer")
# These are anchored bare at both ends. The plural of each names a POPULATION
# rather than the party at the keyboard — `users` is whoever installs this
# plugin, `humans` is a category — where the singular is the party who
# answers, which is what this guard is looking for. `person's` still matches,
# because an apostrophe is a word boundary; `persona` does not, which is the
# half the issue measured.
#
# `user` stays, against the issue's own patch, which drops the stem to stop
# `users`. The back anchor added in the same breath already stops `users`, and
# dropping the stem would let *collect in one batch what the user answers*
# pass in silence — the user being precisely the party who answers
# (`questions.md` Q1, measured: no batch phrase in any definition is within
# the window of any occurrence of the word today, so keeping it refuses
# nothing that stands).
ASKING_BARE = ("person", "people", "human", "user")
ASKING = re.compile(
    r"\b(?:(?:{})(?:s|es|ed|ing|'s)?|(?:{}))\b".format(
        "|".join(ASKING_INFLECTED), "|".join(ASKING_BARE)
    ),
    re.IGNORECASE,
)
ASKING_WINDOW = 140

# #422, half two. The refusal became a claim in round 2 of #419; WHAT IT
# DECIDES ABOUT did not. The occurrence that opened a window was whatever
# contained the exact substring `in one batch`, so an instruction written any
# other way never reached the window that would have refused it. Three
# spellings were measured passing at exit 0:
#
#   *go in **one batch** before the first edit*  -- `CLAUDE.md:39` verbatim,
#       where the emphasis markers break the literal;
#   *in a single batch* and *as a single batch* -- ordinary synonyms.
#
# So the preposition and the article are read as a small set, and emphasis
# comes out before the search. Widening the SET OF WORDS the window refuses is
# a different thing and is not done here: that direction makes a legitimate
# definition unwritable, which is round 2's finding pointing the other way.
BATCH_PHRASE = re.compile(r"\b(?:in|as) (?:one|a single|a) batch\b", re.IGNORECASE)
# `*` only. `_` is the other emphasis marker in markdown and is load-bearing
# in every identifier these definitions name — `round_record.py`,
# `test_the_...` — so stripping it would mangle the window a person reads in
# the refusal. An instruction hidden behind `_one batch_` is residue, recorded
# with the rest below.
EMPHASIS = re.compile(r"\*+")


def test_the_asking_stems_are_anchored_at_both_ends():
    """#422 half one, pinned on the object the sweep below actually reads.

    The front anchor alone let a stem match inside a longer word, and the two
    words it reached are both ordinary in a definition: `persona`, which
    `agents/smith.md` writes, and `users`. Anchoring the back is not free —
    `\\bquestion\\b` would stop matching `questions` — so the stems are split,
    and this case is what says which group each is in.

    Red with the back anchor removed: `persona` and `users` start matching.
    Red with the inflection group removed: `questions` and `asked` stop.
    """
    for word in ("question", "questions", "ask", "asks", "asked", "asking"):
        assert ASKING.search(word), f"{word} no longer marks a person answering"
    for word in ("answer", "answers", "answered", "person", "person's"):
        assert ASKING.search(word), f"{word} no longer marks a person answering"
    for word in ("people", "human", "user", "user's"):
        assert ASKING.search(word), f"{word} no longer marks a person answering"
    # The back anchor. `persona` and `users` are what the issue measured; the
    # other three are the same shape and would have been the next report.
    for word in ("persona", "personas", "users", "humanity", "asker"):
        assert not ASKING.search(word), (
            f"{word} fires the guard, so a definition using an ordinary word "
            "has to be reworded for a question nobody is asking"
        )
    # The front anchor, which round 2 of #419 bought and this must not undo.
    for word in ("task", "multitasking", "flask"):
        assert not ASKING.search(word), f"{word} is a substring, not the word"


def test_the_batch_phrase_is_found_by_its_claim_not_by_one_spelling():
    """#422 half two, pinned on the objects the sweep below actually reads.

    The refusal decided by the claim and the FINDER still decided by one exact
    substring, so an instruction written any other way never reached the
    window. All three spellings below were measured passing at exit 0 before
    this repair — the first is `CLAUDE.md:39` verbatim.

    Red with the emphasis strip removed: the first assertion fails.
    Red with the preposition or the article back to a literal: the synonyms
    stop being found.
    """
    for spelling in (
        "questions go in **one batch** before the first edit",
        "collect them in a single batch",
        "collect them as a single batch",
        "collect them in one batch",
        "collect them in a batch",
        "collect them as one batch",
    ):
        assert BATCH_PHRASE.search(EMPHASIS.sub("", spelling)), (
            f"an instruction written {spelling!r} never reaches the window "
            "that would refuse it, so the guard says nothing about it"
        )
    # Not every sentence with the word in it. The finder opens a window; the
    # window is what refuses. Widening the finder past the phrase would put
    # ordinary prose in front of the stem set for no gain.
    for innocent in (
        "batch independent reads and runs",
        "a batch of questions",
        "batching is what the contract asks for",
    ):
        assert not BATCH_PHRASE.search(innocent), (
            f"{innocent!r} is not a batching instruction and opens a window"
        )


def test_the_questions_are_collected_before_the_work_not_during_it():
    """A question's cost is when it arrives, not how hard it is.

    Asked before the first edit it costs a reply; asked at minute thirty it
    stops a session that may have nobody at the keyboard."""
    with open(
        os.path.join(ROOT, "skills", "implement", "SKILL.md"), encoding="utf-8"
    ) as f:
        implement = f.read()
    assert "in one batch" in implement, "implement lost the batching rule"
    assert "would not change what you build" in implement, (
        "without the assume-in-writing half, the batch becomes a list of "
        "everything and the work waits on all of it"
    )
    # The batch belongs to the SESSION that spawns the work, and that is a
    # property of the harness rather than a preference: no agent this plugin
    # spawns has `AskUserQuestion`, measured from two of them independently
    # (#419, round 1). It was pinned in `agents/smith.md` while the design
    # gate lived there, then briefly in `agents/framer.md` — and a definition
    # that carries the words of an act its agent has no tool for is an
    # instruction nothing can carry out. So the presence is asserted where the
    # tool is, and the absence over EVERY agent definition, by glob, so a
    # fourth one added tomorrow is checked on the day it lands.
    import glob

    with open(
        os.path.join(ROOT, "skills", "implement", "orchestration.md"),
        encoding="utf-8",
    ) as f:
        orchestration = f.read()
    assert "in one call" in orchestration, (
        "the orchestrator's routing section no longer says the questions go "
        "in one call, which is what makes the batch one wait"
    )
    # WHAT IS REFUSED IS A CLAIM, NOT A SPELLING, and the first version of
    # this assertion refused the spelling. It read `"in one batch" not in
    # body` over every definition — and `agent-contract` §10, which every
    # agent receives at startup, gives that phrase a second and entirely
    # legitimate meaning: *Batch independent reads and runs*. A definition
    # writing `open every coordinate in one batch` would have been following
    # the contract and gone red under a message about a question nobody
    # asked. Round 2 found it; a check that refuses a phrase by spelling
    # rather than by what it claims is the shape this release keeps finding,
    # so it is repaired here rather than narrowed by one word.
    #
    # The claim is *this agent collects what a person must answer*. What marks
    # it is a question word beside the phrase, so the window around each
    # occurrence is what decides — flattened first, because these files wrap
    # prose at about 75 columns and a per-line test would miss every sentence
    # that spans two.
    #
    # WHAT IT STILL CANNOT TELL APART, written down rather than left to be
    # found: *you collect the batch* from *your caller collects the batch*.
    # The second is true and a definition may need to say it — `agents/
    # framer.md` does, and says it with `in one call`, which is the spelling
    # that stays clear of this. A definition that needs the other wording will
    # meet this assertion and should reword rather than widen it, because one
    # word is all that separates the true sentence from the instruction.
    #
    # THE REST OF THE RESIDUE, for the same reason — these are what the window
    # cannot see, and each has a direction rather than a fix:
    #
    #   · It CROSSES HEADINGS. 140 characters over the flattened file is a
    #     span with no structural boundary in it, and #422 measured 42 % of
    #     `agents/framer.md` and 60 % of `agents/smith.md` as positions where
    #     a new occurrence would fire. Bounding it at a heading is a change
    #     with its own failure direction — an instruction whose sentence
    #     straddles a heading would pass — and it is ruled out with grounds in
    #     `seal/specs/1789540097-…/spec.md` §*Out*.
    #   · It reads `*` and not `_`. See `EMPHASIS` above for why.
    #   · It refuses by the WORDS in the window, so a definition that names a
    #     person answering for some other reason within 140 characters of a
    #     legitimate batch phrase is refused and has to be reworded. That is
    #     the direction this guard is deliberately wrong in: a false refusal
    #     costs one sentence in a file somebody is already editing.
    #
    # The stems, the window, the phrase and the emphasis pattern are all
    # module-level, above, so `test_the_asking_stems_are_anchored_at_both_ends`
    # and `test_the_batch_phrase_is_found_by_its_claim_not_by_one_spelling`
    # read the same objects this sweep reads rather than copies of them.
    definitions = sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))
    assert len(definitions) >= 3, f"agents/*.md matched {len(definitions)} files"
    for path in definitions:
        with open(path, encoding="utf-8") as f:
            # Emphasis out before the search, so `in **one batch**` is the
            # occurrence it reads as. The window printed in the refusal is
            # this text, which is why it carries no `*`.
            flat_body = EMPHASIS.sub("", " ".join(f.read().split()))
        relative = os.path.relpath(path, ROOT)
        for found in BATCH_PHRASE.finditer(flat_body):
            at = found.start()
            window = flat_body[max(0, at - ASKING_WINDOW) : at + ASKING_WINDOW]
            named = sorted({m.group(0).lower() for m in ASKING.finditer(window)})
            assert not named, (
                f"{relative} tells an agent to collect {found.group(0)} "
                f"something a person answers — the window names {named}. No "
                "agent this plugin spawns has `AskUserQuestion`, so "
                "collecting a batch of questions is an instruction nothing "
                "can carry out; the act belongs to the session that spawns "
                "the work. Batching READS is a different thing and is what "
                "`agent-contract` §10 asks for — that wording is not refused "
                f"here.\n  …{window}…"
            )


def test_the_cycle_is_bounded_and_ends_at_a_pull_request():
    """An unattended run needs a terminus, and two are wrong at that spot.

    Stopping at a report leaves finished work nobody will find; merging
    decides something the chain was never given."""
    with open(
        os.path.join(ROOT, "docs", "review-chain-spec.md"), encoding="utf-8"
    ) as f:
        spec = f.read()
    assert "capped at **three**" in spec, "the review loop lost its bound"
    assert "ends at a PR, never at a merge" in spec
    for home in ("follow-up.md", "questions.md", "legacy-parity"):
        assert home in spec, f"no home recorded for what is left: {home}"
    with open(os.path.join(ROOT, "agents", "smith.md"), encoding="utf-8") as f:
        smith = f.read()
    assert "three rounds" in smith and "never at a merge" in smith


def test_the_five_round_exception_is_pinned_where_it_is_stated():
    """Nothing held the exception. The two assertions above read `capped at
    **three**` and `three rounds`, both of which survive deleting the
    exception paragraph whole — so the entire substance of the answer to #51
    was green against a document that no longer contained it.

    Four things have to be true together, because each alone is the wrong
    rule: five rounds, only for 🔴, only to close it, and a ceiling rather
    than a target."""

    def flat(*parts):
        """The file with its line wrapping collapsed — these sentences are
        wrapped at 80 columns and a phrase test must not depend on where."""
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
            return re.sub(r"\s+", " ", f.read())

    spec = flat("docs", "review-chain-spec.md")
    assert "at **five while a 🔴 is open**" in spec, "the exception is gone"
    assert "only while a 🔴 is open" in spec, "the exception lost its condition"
    assert "and only to close it" in spec, (
        "without this, five rounds becomes the budget rather than the reprieve"
    )
    assert "Five is a ceiling, not a target" in spec
    assert "a round opens a new 🔴 at the same site" in spec, (
        "the stop-regardless row is what keeps the exception from looping"
    )

    assert "five while a 🔴 is open, and only to close it" in flat(
        "agents", "smith.md"
    ), (
        "the agent that runs the loop has to carry the exception, not just "
        "the cap it is an exception to"
    )

    assert "five while a 🔴 is" in flat("skills", "verify", "SKILL.md"), (
        "the broad gate declines this exception on purpose (#51), and a "
        "decline that does not name what it declines cannot be read"
    )


# The two skills a definition calls rather than preloads. Neither is in any
# `skills:` list: a preloaded body is paid for on every spawn (#292), and a
# skill two frames in ten want is cheaper called than carried.
UTILITY_SKILLS = ("confidence-check", "feature-planner")


def definitions_naming(skill):
    """The `agents/*.md` files that name `skill`, read out of the glob.

    Which definition calls these is a fact about the tree, and a case that
    types the answer instead of reading it asserts an owner rather than
    checking one. That is what made the pair below go stale together when the
    gate moved: the name `smith` was in the case, so the tree could change
    under it and only the half that pinned a literal noticed.
    """
    import glob

    return [
        os.path.basename(path)
        for path in sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))
        if skill in open(path, encoding="utf-8").read()
    ]


def test_each_utility_skill_is_callable_from_exactly_one_definition():
    """S4 of #84. `confidence-check` and `feature-planner` were named in
    `agents/smith.md`'s design gate; 0.11.0 moves the judgment they serve to
    `agents/framer.md`, and a skill named in two definitions is two agents
    each believing the call is theirs.

    Counted from the glob rather than from a pair of filenames, so a sixth
    definition picking one of them up is red here on the day it lands."""
    for skill in UTILITY_SKILLS:
        homes = definitions_naming(skill)
        assert homes == ["framer.md"], (
            f"`{skill}` is named in {homes}. It belongs to exactly one "
            "definition -- the one whose phase decides what it answers -- and "
            "a second home is where the two agents start calling it over each "
            "other. If the home moved, `agents/framer.md`, the losing "
            "definition and the skill's own stand-down clause move together"
        )


def test_the_skills_stand_down_for_whichever_definition_calls_them():
    """Both skills used to fire on their own keywords while a design gate was
    deciding the same thing, so one request could open three scope
    conversations. The `NOT for` clause is what stopped that, and it names the
    agent it stands down for.

    This case used to read that name as the literal `smith`, which is why the
    clause and the gate could come apart: 0.11.0 moved the gate to the framer
    and the two SKILL.md files went on naming an agent that no longer calls
    them, with nothing red. The name is read out of the glob now, so the
    clause has to follow whichever definition actually holds the skill."""
    for skill in UTILITY_SKILLS:
        homes = definitions_naming(skill)
        assert len(homes) == 1, (
            f"`{skill}` is named in {homes}, so there is no single agent for "
            "its stand-down clause to name"
        )
        owner = os.path.splitext(homes[0])[0]
        head = (
            open(os.path.join(ROOT, "skills", skill, "SKILL.md"), encoding="utf-8")
            .read()
            .split("\n---\n", 1)[0]
        )
        assert f"{owner} is driving" in head, (
            f"`{skill}` stands down for somebody other than `{owner}`, which "
            f"is the definition that names it. The clause is what keeps it "
            "from firing on its own beside the phase that already calls it"
        )


def test_the_smith_says_whether_the_frame_holds_before_building_to_it():
    """S5 of #84. A `spec.md` and a `plan.md` are a drawing another party
    made, and a drawing can be wrong about the tree it describes. #107's
    phase 1 established that its own stated path could not work before a line
    was written; phase 1 of #84 did it again on a `skills:` list it was
    handed. Twice in two work items, unprompted, and written into no
    document -- which makes it a habit, and a habit is what the next spawn
    does not inherit.

    The home is pinned as well as the sentence, and it is the Requirements
    phase. There the check runs on what was just read and a `no` costs the
    reading; below the design gate it arrives after the question batch has
    already been spent on a frame that does not hold.

    A `no` needs a destination or it becomes a second interruption. The one
    the sentence names is the phase record and the hand-back -- never a route
    back to the framer, which has no interactive phase to route back TO: the
    one moment of human contact belongs to the session that spawns the work,
    before the framer is spawned at all."""
    smith = " ".join(
        open(os.path.join(ROOT, "agents", "smith.md"), encoding="utf-8").read().split()
    )
    holds = "say whether the frame holds before you build to it"
    assert holds in smith, (
        "`agents/smith.md` no longer tells the builder to judge the frame "
        "before building to it. It happened twice unprompted and was recorded "
        "nowhere, which is exactly what a written instruction is for"
    )
    start = smith.index("1. **Requirements**")
    # Bounded by the NEXT phase, found by its number rather than by its
    # title. Phase 2 stopped being the design gate when the act moved
    # (#419), and a slice keyed on the old title raises rather than
    # reporting — which is the one failure shape a reader cannot read.
    requirements = smith[start : smith.index("2. **")]
    assert holds in requirements, (
        "the drawing-holds check moved out of the Requirements phase. Below "
        "the design gate it fires after the question batch, so a frame that "
        "does not hold has already cost the one interruption"
    )
    for named in ("phases/phase-N.md", "## What this phase found", "the hand-back"):
        assert named in requirements, (
            f"the sentence no longer names `{named}` as where a `no` goes. A "
            "`no` with no destination is a finding that reaches nobody"
        )
    assert "never back to the framer" in requirements, (
        "the sentence stopped ruling out the route back to the framer, which "
        "is the second interruption that phase exists to spend once"
    )


def test_spec_directories_carry_the_timestamp_prefix():
    # implement/SKILL.md: "A work item's directory is
    # seal/specs/<unix-epoch-seconds>-<slug>/ ... keeps directories in
    # creation order and collision-free without a registry". Two were written
    # without
    # it and nothing noticed — the drift this plugin exists to catch, in its
    # own tree. The four that predate the convention were backfilled from the
    # commit that introduced each, so a plain listing now reads in order.
    import re

    specs = os.path.join(ROOT, "seal", "specs")
    offenders = [
        name
        for name in sorted(os.listdir(specs))
        if os.path.isdir(os.path.join(specs, name))
        and not re.match(r"^\d{10}-[a-z0-9][a-z0-9-]*$", name)
    ]
    assert not offenders, (
        "spec directories missing the <unix-epoch-seconds>-<slug> prefix "
        f"the implement skill specifies: {offenders}"
    )


def test_every_spec_directory_that_reached_the_ladder_has_an_overview():
    """A work item that wrote a spec or a plan owes a closing memo.

    Not every directory does. Below the SDD ladder nothing is written but the
    routing declaration, and a routing-only directory is the whole record of a
    typo fix -- demanding a memo there would either fabricate one or push those
    changes back to leaving no trace at all, which is what giving them a
    directory was for.

    The exemption is narrow on purpose: the moment a directory holds a
    `spec.md` or a `plan.md`, someone decided the work was worth describing,
    and the memo is the other half of that.
    """
    specs = os.path.join(ROOT, "seal", "specs")
    missing = []
    for n in sorted(os.listdir(specs)):
        d = os.path.join(specs, n)
        if not os.path.isdir(d):
            continue
        on_the_ladder = any(
            os.path.isfile(os.path.join(d, f)) for f in ("spec.md", "plan.md")
        )
        if on_the_ladder and not os.path.isfile(os.path.join(d, "overview.md")):
            missing.append(n)
    assert not missing, f"work items with no closing overview: {missing}"


def test_installer_prints_commands_a_user_can_actually_type():
    # Plugin commands are namespaced. The installer printed /preset-setup,
    # which resolves to nothing — found by running the installer against a
    # real machine rather than by reading it.
    import re

    text = open(os.path.join(ROOT, "install.sh"), encoding="utf-8").read()
    bare = [
        m
        for m in re.findall(r"(?<!:)/([a-z][a-z-]+)\b", text)
        if m
        in {"preset-setup", "security-audit", "testing", "parity-setup", "evidence-ci"}
    ]
    assert not bare, f"un-namespaced plugin commands in install.sh: {bare}"
