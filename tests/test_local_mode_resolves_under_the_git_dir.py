"""In local mode every gate finds what it reads under `<git-common-dir>/seal/`.

The read side of #80 shipped in 0.4.0: `optin.home_at` looks at `<repo>/seal/`
and then at the common git directory's `seal/`. What these cases pin is the
JOINERS — the hooks that spelled `seal/` under the repository root rather than
asking for the resolved root, and the one whose printed path a session would
type in the wrong place (spec S6, Q5). Each is run in a local-mode fixture:
the `repo` fixture with `local_home` and nothing at `<repo>/seal/`.

The fail direction of every path here is "not opted in" or "nothing written"
(S10), and the scratch marker under the common directory takes the opt-in
back in local mode the way it does in shared mode.
"""

import json
import os
import subprocess

import pytest
from conftest import (
    decision_of,
    declare_routing,
    fired,
    load_hook_module,
    local_home,
    run_hook,
)

ITEM = "1788000000-a-work-item"
SERVICE = "def handler(x):\n    return x + 1\n\n\ndef other():\n    return 0\n"
BROKEN_ROW = "# rows\n\n| A | `src/service.py#gone@00000000` |\n"
OLD_ROW = "# rows\n\n| A | `src/service.py:1-2` | 2026-08-31 |\n"


def bash(repo, command="git commit -m x", session="s1"):
    return {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": command},
        "cwd": str(repo),
    }


def reason_of(out):
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


def branch_of(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def declare_smith(repo, home, item=ITEM):
    """A declaration under `home` whose third axis says `smith`."""
    d = home / "specs" / item
    d.mkdir(parents=True, exist_ok=True)
    (d / "routing.md").write_text(
        f"# {item} -- routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        "| Review | through the review chain |\n"
        "| Destination | open the pull request |\n"
        "| Implementation | smith |\n"
        f"| Branch | {branch_of(repo)} |\n",
        encoding="utf-8",
    )
    return d


def linked_worktree(repo, tmp_path):
    other = tmp_path / "linked"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-q", str(other), "feature/x"],
        check=True,
        capture_output=True,
    )
    assert os.path.isfile(other / ".git"), "a linked worktree carries a .git FILE"
    return other


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def local(repo):
    """The `repo` fixture in local mode: `seal/` under `.git/` and nowhere
    else, with a source file for the ledger rows to cite."""
    home = local_home(repo)
    assert not (repo / "seal").exists()
    write(repo / "src" / "service.py", SERVICE)
    return repo, home


# --- the commit gate: reads the declaration, and names where to write it ------


def test_the_commit_gate_is_silent_with_a_declaration_under_the_local_root(local):
    repo, home = local
    declare_routing(repo, home=home)
    assert decision_of(run_hook("commit-review-gate.py", bash(repo))) == "silent"


def test_the_commit_gate_is_silent_from_a_linked_worktree_too(repo, tmp_path):
    """The declaration lives in the main tree's common directory; the
    worktree's branch is what it names."""
    home = local_home(repo)
    other = linked_worktree(repo, tmp_path)
    declare_routing(other, home=home)
    assert decision_of(run_hook("commit-review-gate.py", bash(other))) == "silent"


def test_the_commit_gate_fires_without_one_and_names_the_resolved_path(local):
    """Q5 (a). The stop text used to spell `seal/specs/<work-item-id>/routing.md`
    whatever the mode, and a session that typed it in local mode wrote a
    declaration the gate never reads. The path is under the resolved root,
    relative to the repository, spelled the way the platform spells it."""
    repo, _ = local
    out = run_hook("commit-review-gate.py", bash(repo))
    assert fired(out)
    reason = reason_of(out)
    resolved = os.path.join(".git", "seal", "specs", "<work-item-id>", "routing.md")
    assert resolved in reason, reason
    assert "`seal/specs/<work-item-id>/routing.md`" not in reason, (
        "the literal shared-mode spelling is still offered in local mode"
    )


def test_the_stop_text_from_a_linked_worktree_is_a_path_a_person_can_type(
    repo, tmp_path
):
    """From a linked worktree the resolved root is outside the tree, so the
    relative path climbs out of it — typeable, where `.git/seal/…` names a
    FILE's child there."""
    home = local_home(repo)
    other = linked_worktree(repo, tmp_path)
    out = run_hook("commit-review-gate.py", bash(other))
    assert fired(out)
    resolved = os.path.join(
        os.path.relpath(home, other), "specs", "<work-item-id>", "routing.md"
    )
    assert resolved in reason_of(out), reason_of(out)


def test_in_shared_mode_the_stop_text_still_names_the_tree_root(repo):
    """The other half of Q5: a shared repository is told `seal/specs/…`,
    the path it always was."""
    (repo / "seal").mkdir()
    out = run_hook("commit-review-gate.py", bash(repo))
    assert fired(out)
    resolved = os.path.join("seal", "specs", "<work-item-id>", "routing.md")
    assert resolved in reason_of(out), reason_of(out)


# --- the implementer notice: prints the path it resolved --------------------


def test_the_implementer_notice_names_the_local_path(local):
    repo, home = local
    declare_smith(repo, home)
    out = run_hook("implementer-notice.py", bash(repo))
    assert "answers `Implementation` with `smith`" in out, out
    assert os.path.join(".git", "seal", "specs", ITEM, "routing.md") in out, out


# --- the evidence advisor: globs the ledger under the resolved root ---------


@pytest.mark.parametrize("at", ["ledger.md", os.path.join("ledger", "f.md")])
def test_the_evidence_advisor_reports_a_broken_row_from_the_local_ledger(local, at):
    """S6. The advisory globbed `seal/ledger.md` and `seal/ledger/*.md` under
    the repository root, so a local-mode ledger was never read and a commit
    that broke an anchor was told nothing."""
    repo, home = local
    write(home / at, BROKEN_ROW)
    out = run_hook("evidence-advisor.py", bash(repo))
    assert "BROKEN" in out, out
    assert "src/service.py#gone" in out, out


def test_the_evidence_advisor_reads_the_local_ledger_from_a_linked_worktree(
    repo, tmp_path
):
    home = local_home(repo)
    other = linked_worktree(repo, tmp_path)
    write(other / "src" / "service.py", SERVICE)
    write(home / "ledger.md", BROKEN_ROW)
    out = run_hook("evidence-advisor.py", bash(other))
    assert "BROKEN" in out and "src/service.py#gone" in out, out


def test_the_evidence_advisor_still_reads_the_pre_0_10_address_under_the_tree(
    local,
):
    """`docs/**/_evidence.md` stays under the repository root: it is a
    committed file at an old address, not part of the root that moved."""
    repo, _ = local
    write(repo / "docs" / "policies" / "demo" / "_evidence.md", BROKEN_ROW)
    out = run_hook("evidence-advisor.py", bash(repo))
    assert "BROKEN" in out and "src/service.py#gone" in out, out


# --- the ledger migration hook: same globs, same fix -------------------------


@pytest.fixture
def migrate(tmp_path):
    mod = load_hook_module("ledger-migrate.py", "ledger_migrate_local")
    mod.STATE_DIR = str(tmp_path / "state")
    mod.MARKER = os.path.join(mod.STATE_DIR, "ledger-migrated")
    return mod


def session_start(hook, cwd):
    import io
    import sys

    out = io.StringIO()
    stdin, stdout = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(json.dumps({"cwd": str(cwd)}))
    sys.stdout = out
    try:
        hook.main()
    finally:
        sys.stdin, sys.stdout = stdin, stdout
    return out.getvalue()


def test_the_ledger_migration_hook_migrates_a_pre_anchor_ledger_under_the_local_root(
    local, migrate
):
    repo, home = local
    ledger = home / "ledger" / "f.md"
    write(ledger, OLD_ROW)
    out = session_start(migrate, repo)
    assert "ledger migrated to anchor format" in out, out
    text = ledger.read_text(encoding="utf-8")
    assert "src/service.py#handler@" in text, text
    assert "src/service.py:1-2" not in text, text


def test_the_ledger_migration_hook_is_not_refused_from_a_linked_worktree(
    repo, tmp_path, migrate
):
    """`dirty()` asked `git status` about every ledger path. A path under the
    common directory of ANOTHER tree is outside this worktree's repository,
    git answers `fatal: … is outside repository`, and a non-zero exit read as
    work in progress — so the migration was refused at every session start,
    with the wrong reason printed. Nothing under the git directory can be
    uncommitted work; those paths are not asked about."""
    home = local_home(repo)
    other = linked_worktree(repo, tmp_path)
    write(other / "src" / "service.py", SERVICE)
    ledger = home / "ledger" / "f.md"
    write(ledger, OLD_ROW)
    out = session_start(migrate, other)
    assert "uncommitted" not in out, out
    assert "ledger migrated to anchor format" in out, out
    assert "src/service.py#handler@" in ledger.read_text(encoding="utf-8")


def test_a_dirty_ledger_under_the_tree_is_still_refused_in_local_mode(local, migrate):
    """The old address under the tree keeps its boundary: an uncommitted
    `docs/**/_evidence.md` is work in progress, whatever mode the root is in."""
    repo, _ = local
    write(repo / "docs" / "policies" / "demo" / "_evidence.md", OLD_ROW)
    out = session_start(migrate, repo)
    assert "uncommitted" in out, out


# --- S10: the scratch marker takes local mode back too -----------------------


def test_a_scratch_marker_under_the_common_directory_keeps_every_gate_silent(
    local, migrate
):
    repo, home = local
    (repo / ".git" / "specseal-scratch").write_text("")
    declare_smith(repo, home)
    write(home / "ledger.md", BROKEN_ROW)
    write(home / "ledger" / "f.md", OLD_ROW)

    assert decision_of(run_hook("commit-review-gate.py", bash(repo))) == "silent"
    assert (
        decision_of(
            run_hook(
                "review-skill-gate.py",
                {
                    "tool_name": "Skill",
                    "session_id": "s1",
                    "tool_input": {"skill": "code-review"},
                    "cwd": str(repo),
                },
            )
        )
        == "silent"
    )
    assert run_hook("implementer-notice.py", bash(repo)) == ""
    assert run_hook("evidence-advisor.py", bash(repo)) == ""
    assert session_start(migrate, repo) == ""
