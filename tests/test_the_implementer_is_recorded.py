"""Who framed and who implemented is declared, marked when it happens, noticed.

The routing declaration answers four axes and only two of them decide anything.
`Implementation` says who writes the code — the `smith` subagent, or the
session itself — and a session can declare `smith` and then implement the whole
work item on its own with nobody the wiser. Issue #26 records that nothing
watched the axis, and why that was left so.

`Planning` is the same gap one storey up: a session can declare `framer` and
draw the frame itself. #84's `questions.md` Q1 put the two answers to the
repository owner with *no mark* as the frame's own default, and the answer on
2026-09-11 was **a mark**, on the grounds that the gap is the same gap. Both
marks live in one module and one hook reads both, because two files whose
`git_dir`, `write` and `stands` differ by a constant is the near-identical
copy contract §11 and §16 each record having already been paid for.

Three parts, and each is a different failure if it goes missing:

  the mark    spawning either agent leaves that axis's trace in the
              repository's git dir. Missing, the notice fires for work that was
              done correctly.

  the notice  a declaration naming an agent no mark answers for says so, once,
              after a commit — one line for both axes where both are
              unfulfilled. Missing, the axes are notes nobody reads.

  the silence nothing is said about an axis whose mark stands, whose row was
              not answered, or in a repository that never opted in. Missing,
              this is a fourth prompt in a plugin whose first goal is
              verification that runs unattended.

The notice never blocks. The commit gate's decision has to be byte-identical
with the row and without it, which is the case that would catch this axis
leaking into a decision it was never given. And a broken mark gate must leave
the worktree guard's verdict alone, which is the objection #26 raised against
putting a second gate in `pre-agent`.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from conftest import fired, load_hook_module, run_hook

HOOKS = os.path.join(os.path.dirname(__file__), "..", "hooks")

implementer = load_hook_module("implementer.py", "specseal_implementer")

CHAIN = "through the review chain"
NOTICE = "answers `Implementation` with `smith`"
PLANNING_NOTICE = "answers `Planning` with `framer`"
BOTH = "`Planning` with `framer` and `Implementation` with `smith`"
# The sentence every notice ends with, whichever axes it names. Counting it is
# how S14 tells one line naming two axes from two lines naming one each.
ONCE = "Nothing was blocked, and this is said once per session."
ITEM = "1788137177-a-work-item"


def run_dispatch(group, payload, hooks=HOOKS):
    r = subprocess.run(
        [sys.executable, os.path.join(hooks, "dispatch.py"), group],
        input=json.dumps(payload),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    return r.stdout


def opt_in(repo):
    (repo / "seal").mkdir(exist_ok=True)


def branch_of(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def git_dir(repo):
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def mark_path(repo, mark):
    """Where one axis's mark lives. The axis is named at every call site, so a
    case cannot assert about the implementation mark while meaning the other."""
    return os.path.join(git_dir(repo), mark)


def declare(repo, implementation="smith", item=ITEM, planning=None):
    """A declaration for this repo's branch; a `None` answer omits its row."""
    d = repo / "seal" / "specs" / item
    d.mkdir(parents=True, exist_ok=True)
    third = f"| Implementation | {implementation} |\n" if implementation else ""
    fourth = f"| Planning | {planning} |\n" if planning else ""
    (d / "routing.md").write_text(
        f"# {item} -- routing\n\n"
        "| Axis | Answer |\n|---|---|\n"
        f"| Review | {CHAIN} |\n"
        "| Destination | open the pull request |\n"
        f"{fourth}"
        f"{third}"
        f"| Branch | {branch_of(repo)} |\n",
        encoding="utf-8",
    )
    return d


def spawn(repo, agent="specseal:smith", session="s1", **extra):
    return {
        "tool_name": "Agent",
        "session_id": session,
        "tool_input": {"subagent_type": agent, "prompt": "build it", **extra},
        "cwd": str(repo),
    }


def bash(repo, cmd="git commit -m x", session="s1"):
    return {
        "tool_name": "Bash",
        "session_id": session,
        "tool_input": {"command": cmd},
        "cwd": str(repo),
    }


# --- the mark: spawning smith leaves one, spawning anything else does not ----


def test_spawning_smith_leaves_a_mark(repo):
    """S1, through the group the harness actually runs, not the gate alone."""
    opt_in(repo)
    assert not os.path.exists(mark_path(repo, implementer.IMPLEMENTATION_MARK))
    assert run_dispatch("pre-agent", spawn(repo)).strip() == "", (
        "the mark gate must decide nothing; output here would be a fourth prompt"
    )
    assert os.path.isfile(mark_path(repo, implementer.IMPLEMENTATION_MARK))
    assert implementer.stands(
        str(repo), branch_of(repo), implementer.IMPLEMENTATION_MARK
    )


def test_spawning_the_framer_leaves_the_planning_mark(repo):
    """S13. The second axis arrives on the first's mechanism: same gate, same
    group, same silence, a different file under the git dir."""
    opt_in(repo)
    assert run_dispatch("pre-agent", spawn(repo, agent="specseal:framer")).strip() == ""
    assert os.path.isfile(mark_path(repo, implementer.PLANNING_MARK))
    assert implementer.stands(str(repo), branch_of(repo), implementer.PLANNING_MARK)


def test_a_mark_for_one_axis_does_not_answer_for_the_other(repo):
    """S13's other half, and the shape `stands`'s branch scoping already has.

    Two axes share one directory, so the axis is part of the address exactly as
    the branch is. A `smith` spawned on this branch answering for a `framer`
    that never ran is the false silence the module refuses — and it is the
    likelier direction, because `smith` is spawned on nearly every work item.
    """
    opt_in(repo)
    run_dispatch("pre-agent", spawn(repo))
    branch = branch_of(repo)
    assert implementer.stands(str(repo), branch, implementer.IMPLEMENTATION_MARK)
    assert not implementer.stands(str(repo), branch, implementer.PLANNING_MARK)
    assert not os.path.exists(mark_path(repo, implementer.PLANNING_MARK))


def test_spawning_any_other_agent_leaves_none(repo):
    """S2. `smith-helper` and `framer-helper` are in the list because a
    substring test would read either as the agent itself."""
    opt_in(repo)
    for agent in (
        "specseal:warden",
        "specseal:scribe",
        "specseal:sealer",
        "general-purpose",
        "smith-helper",
        "framer-helper",
    ):
        run_dispatch("pre-agent", spawn(repo, agent=agent))
        for mark in (implementer.IMPLEMENTATION_MARK, implementer.PLANNING_MARK):
            assert not os.path.exists(mark_path(repo, mark)), f"{agent} -> {mark}"


def test_the_project_local_spelling_of_the_agent_counts_too(repo):
    """S3. The harness spells a plugin's agent `specseal:smith` and a
    project-local one `smith`. Reading only the first would leave the notice
    firing forever in a repository that defines its own."""
    opt_in(repo)
    run_dispatch("pre-agent", spawn(repo, agent="smith"))
    assert os.path.isfile(mark_path(repo, implementer.IMPLEMENTATION_MARK))
    run_dispatch("pre-agent", spawn(repo, agent="framer"))
    assert os.path.isfile(mark_path(repo, implementer.PLANNING_MARK))


def test_a_repository_that_never_opted_in_gets_no_files_written(repo):
    """S4. A globally installed plugin must not write into repositories that
    never asked for the workflow."""
    for agent in ("specseal:smith", "specseal:framer"):
        run_dispatch("pre-agent", spawn(repo, agent=agent))
    for mark in (implementer.IMPLEMENTATION_MARK, implementer.PLANNING_MARK):
        assert not os.path.exists(mark_path(repo, mark)), mark


def test_the_mark_does_not_answer_for_another_branch(repo):
    """S5. One `smith` spawned once would otherwise silence the notice for
    every work item in that repository, forever."""
    opt_in(repo)
    run_dispatch("pre-agent", spawn(repo))
    run_dispatch("pre-agent", spawn(repo, agent="specseal:framer"))
    for mark in (implementer.IMPLEMENTATION_MARK, implementer.PLANNING_MARK):
        assert implementer.stands(str(repo), branch_of(repo), mark), mark
        assert not implementer.stands(str(repo), "feature/somewhere-else", mark), mark


def test_a_broken_mark_gate_leaves_the_worktree_guards_verdict_alone(repo, tmp_path):
    """S13. Issue #26's second objection to building this: a second gate in
    `pre-agent` whose import fails could take the worktree guard's answer
    with it. `dispatch.py#run_gate` catches per gate, so it does not — and
    this is the measurement, with the mark gate unparseable and then absent.

    The intact run also pins `questions.md` Q2: the mark is written even when
    the guard stops the same spawn, because the gates do not see each other.
    """
    opt_in(repo)
    hooks = tmp_path / "hooks"
    shutil.copytree(Path(HOOKS).resolve(), hooks)
    # A fresh session id per call. The guard remembers which sessions it has
    # already put the two-option question to (`already_asked`) and answers a
    # repeat from the same session with the shorter fallback, so three calls
    # under one id would differ on the guard's own state and say nothing
    # about the mark gate. Measured on CI, where ps/lsof are absent and the
    # guard reaches that site; macOS reached another and never showed it.
    isolated = spawn(repo, isolation="worktree", session="s-intact")

    intact = run_dispatch("pre-agent", isolated, hooks=str(hooks))
    assert fired(intact), "the guard did not fire, so there is nothing to protect"
    assert os.path.isfile(mark_path(repo, implementer.IMPLEMENTATION_MARK)), (
        "Q2: written before the group decides"
    )

    for n, broken in enumerate(("def broken(:\n", None)):
        if broken is None:
            (hooks / "implementer-mark.py").unlink()
        else:
            (hooks / "implementer-mark.py").write_text(broken, encoding="utf-8")
        again = spawn(repo, isolation="worktree", session=f"s-broken-{n}")
        after = run_dispatch("pre-agent", again, hooks=str(hooks))
        assert after == intact, (
            f"a broken mark gate changed the worktree guard's verdict:\n{after}"
        )


# --- the notice: said once, and only where the answer went unhonoured --------


def test_a_declared_smith_with_no_mark_is_noticed_after_a_commit(repo):
    """S6. Emitted from `post-bash`, whose output is read — a PreToolUse
    gate that allows produces no output at all."""
    opt_in(repo)
    declare(repo, implementation="smith")
    out = run_dispatch("post-bash", bash(repo))
    assert NOTICE in out, out
    assert ITEM in out, "the notice does not say which file"


def test_the_notice_names_the_file_the_way_the_platform_spells_it(repo):
    """S14. `review-history-guard.py` was changed for this: a path joined with
    a literal `/` arrived on Windows as half of one command in each dialect.
    The file named is the one a person has to open."""
    opt_in(repo)
    declare(repo, implementation="smith")
    out = run_dispatch("post-bash", bash(repo))
    assert os.path.join("seal", "specs", ITEM, "routing.md") in out, out


def test_with_the_mark_present_nothing_is_said(repo):
    """S7."""
    opt_in(repo)
    declare(repo, implementation="smith")
    run_dispatch("pre-agent", spawn(repo))
    assert NOTICE not in run_dispatch("post-bash", bash(repo))


def test_the_notice_is_said_once_per_repository_per_session(repo):
    """S8. The grain is stated because `once` has meant four things here."""
    opt_in(repo)
    declare(repo, implementation="smith")
    assert NOTICE in run_dispatch("post-bash", bash(repo))
    assert NOTICE not in run_dispatch("post-bash", bash(repo))
    assert NOTICE in run_dispatch("post-bash", bash(repo, session="s2"))


def test_the_other_answer_is_not_a_defect(repo):
    """S9. `the session` implemented it, which is what the declaration said."""
    opt_in(repo)
    declare(repo, implementation="the session")
    assert NOTICE not in run_dispatch("post-bash", bash(repo))


def test_a_declaration_without_the_row_says_nothing(repo):
    """S9. Every declaration written before this axis existed looks like this."""
    opt_in(repo)
    declare(repo, implementation=None)
    assert NOTICE not in run_dispatch("post-bash", bash(repo))


def test_an_unreadable_answer_says_nothing_either(repo):
    """S9. `parse()` reads it as unanswered, and unanswered is not a finding."""
    opt_in(repo)
    declare(repo, implementation="whoever gets to it")
    assert NOTICE not in run_dispatch("post-bash", bash(repo))


def test_a_command_that_does_not_commit_says_nothing(repo):
    """S10. Including one that merely mentions a commit in prose."""
    opt_in(repo)
    declare(repo, implementation="smith")
    for cmd in ("ls -la", "echo 'remember to git commit'", "git status"):
        assert NOTICE not in run_dispatch("post-bash", bash(repo, cmd=cmd)), cmd


def test_a_declared_framer_with_no_mark_is_noticed_after_a_commit(repo):
    """S13. The fourth axis earns the same one line the third does."""
    opt_in(repo)
    declare(repo, implementation=None, planning="framer")
    out = run_dispatch("post-bash", bash(repo))
    assert PLANNING_NOTICE in out, out
    assert ITEM in out, "the notice does not say which file"
    assert NOTICE not in out, "the notice named an axis the declaration did not answer"


def test_with_the_planning_mark_present_nothing_is_said(repo):
    """S13. Spawning the framer is the whole of what the row asked for."""
    opt_in(repo)
    declare(repo, implementation=None, planning="framer")
    run_dispatch("pre-agent", spawn(repo, agent="specseal:framer"))
    assert PLANNING_NOTICE not in run_dispatch("post-bash", bash(repo))


def test_a_mark_for_one_axis_does_not_silence_the_other_at_the_notice(repo):
    """S13. The cross-axis case at the reader rather than at `stands`.

    Both rows answered and only `smith` spawned: the framer never ran, and the
    line has to say so. A notice that read one mark for both axes would go
    quiet here, which is the state this whole mechanism exists to report.
    """
    opt_in(repo)
    declare(repo, implementation="smith", planning="framer")
    run_dispatch("pre-agent", spawn(repo))
    out = run_dispatch("post-bash", bash(repo))
    assert PLANNING_NOTICE in out, out
    assert NOTICE not in out, "the fulfilled axis was named as unfulfilled"


def test_two_unfulfilled_axes_produce_one_line_not_two(repo):
    """S14. The grain is once per repository per session, and two lines in one
    session is that grain broken in the commonest state of all — a declaration
    copied from the template and answered on both optional rows, by a session
    that then framed and built the work itself."""
    opt_in(repo)
    declare(repo, implementation="smith", planning="framer")
    out = run_dispatch("post-bash", bash(repo))
    assert out.count(ONCE) == 1, (
        f"two unfulfilled axes produced {out.count(ONCE)} notices:\n{out}"
    )
    assert BOTH in out, (
        f"one line was printed and it names only one of the two axes:\n{out}"
    )
    assert "neither was spawned" in out, (
        "the line names two axes and then says `no smith was spawned`, which "
        "reads as one of them"
    )


def test_the_fourth_axis_other_answers_are_not_a_defect(repo):
    """S13's silences. `the session` framed it, which is what the row said; an
    absent row is every declaration written before the axis existed; and an
    unreadable one is unanswered, which is not a finding."""
    opt_in(repo)
    for answer in ("the session", None, "whoever gets to it", "`framer`"):
        declare(repo, implementation=None, planning=answer)
        out = run_dispatch("post-bash", bash(repo, session=f"s-{answer}"))
        assert PLANNING_NOTICE not in out, answer
        assert ONCE not in out, answer


def test_an_unrelated_repository_is_not_reminded(repo):
    opt_in(repo)
    declare(repo, implementation="smith")
    shutil.rmtree(repo / "seal")
    assert NOTICE not in run_dispatch("post-bash", bash(repo))


# --- and it changes no decision ---------------------------------------------


def test_the_commit_gate_decides_identically_with_the_row_and_without(repo):
    """S11, the load-bearing half: notice, never denial. Byte-identical,
    because the reason text is what a session acts on."""
    opt_in(repo)
    declare(repo, implementation=None)
    without = run_hook("commit-review-gate.py", bash(repo))
    declare(repo, implementation="smith")
    with_row = run_hook("commit-review-gate.py", bash(repo, session="s2"))
    assert without == with_row == "", (without, with_row)


def test_the_notice_never_carries_a_permission_decision(repo):
    """S12. A PostToolUse hook cannot block, and a decision emitted from one
    would be merged by `dispatch.py` into a group that CAN."""
    opt_in(repo)
    declare(repo, implementation="smith")
    out = run_hook("implementer-notice.py", bash(repo))
    assert NOTICE in out
    assert "permissionDecision" not in out
