"""A worktree creation, judged and recorded where it ran (#692, phase 4).

`hooks/git/post-checkout.py` is the entry point. git runs it in the worktree
`git worktree add` just made, with the null object id as the previous HEAD --
the one sign, on every git measured, that this checkout is a creation and not
a switch (phase 1's M3, M14). No command text is read, so a creation is
judged whatever `cd`, redirection or wrapper stood in front of it, and a
creation the shell never ran is never recorded.

**What it decides is the guard's creation ladder** (`hooks/worktree-guard.py`
§B, `docs/worktree-guard-spec.md` §*Creation consent*), counted in the tree
the creation was run from. That tree is the working directory of
`post-checkout`'s parent, the `git worktree add` process, which git leaves at
the toplevel it ran in (M14). Where the process table cannot be read, the
ladder takes its cannot-tell row, as the guard always has.

  * **Consent first** -- a creation already ran in this clone this session
    (the record), or the person pressed `automation` (the transcript): the
    creation stands, and the record is written.
  * **The person's answer** -- `git -c specseal.answer=worktree-ok worktree
    add …`, or the old `# [worktree-ok]` carried by `hooks/answers.py` (P3):
    the creation stands, and the record is written. The guard used to answer
    the token with an `ask` the person clicked; a git hook has no `ask`, so
    the refusal below tells the model to ask the person and the token is how
    their answer comes back (W2).
  * **Otherwise the creation is taken back**: `git worktree remove --force`
    on a tree nothing has used yet, a non-zero exit so `worktree add` reports
    failure, and the ladder's reason. A branch `-b` made stays, as it does
    when `reference-transaction` refuses (M3); the text says how to drop it.
    This is spec S8's "post-hoc equivalent". `reference-transaction` cannot
    hold the decision because nothing at `prepared` tells a creation from a
    switch (M13).

**A worktree the harness makes for an isolated agent** lands under
`<repo>/.claude/worktrees/` and was already put to the person by the guard's
Agent/Task arm. Whether that path runs `git worktree add` at all is M5,
unmeasured, so such a worktree is recorded and never taken back: a refusal
there would fail a spawn the person had approved.
"""

import importlib.util
import os
import subprocess

import answers
import hooksession
import optin

HERE = os.path.dirname(os.path.abspath(__file__))

_GUARD = []


def guard():
    """`hooks/worktree-guard.py`, loaded once; its counting and its texts."""
    if not _GUARD:
        spec = importlib.util.spec_from_file_location(
            "specseal_worktree_guard_for_creation",
            os.path.join(HERE, "worktree-guard.py"),
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _GUARD.append(module)
    return _GUARD[0]


def _git(args, cwd):
    # git's own variables for the hook are dropped, so a command run from here
    # acts on the repository its `cwd` names -- except the `GIT_CONFIG*` family,
    # which is how git hands the hook a `-c` from the command line (M11).
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("GIT_") or k.startswith("GIT_CONFIG")
    }
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=cwd or None,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            env=env,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out


def answered(cwd, session):
    """True when the command carried the person's answer to create it."""
    out = _git(["config", "--get-all", "specseal.answer"], cwd)
    if out is not None and out.returncode == 0:
        if "worktree-ok" in out.stdout.replace(",", " ").split():
            return True
    return answers.given(session, "[worktree-ok]")


def origin_tree(new_top):
    """The toplevel the creation ran from, or "" when it cannot be read."""
    where = guard().proc_cwd(os.getppid())
    top = optin.repo_root(where) if where else ""
    if top and os.path.realpath(top) != os.path.realpath(new_top):
        return top
    return ""


def harness_made(new_top):
    """True for a worktree under some `<repo>/.claude/worktrees/`."""
    parts = os.path.realpath(new_top).split(os.sep)
    return any(
        parts[i] == ".claude" and parts[i + 1] == "worktrees"
        for i in range(len(parts) - 2)
    )


def take_back(new_top, where):
    """Remove the worktree just made, running git from `where` -- another
    worktree of the clone; the branch it was on, or ""."""
    branch = ""
    out = _git(["symbolic-ref", "-q", "--short", "HEAD"], new_top)
    if out is not None and out.returncode == 0:
        branch = out.stdout.strip()
    _git(["worktree", "remove", "--force", new_top], where)
    return branch


def _two(git, tr, top):
    return [
        tr(
            '  1. "Create the worktree" — re-issue it as `git -c '
            "specseal.answer=worktree-ok worktree add …`. The older spelling, "
            "`git worktree add …  # [worktree-ok]`, still works.",
            '  1. "worktree 를 만든다" — `git -c specseal.answer=worktree-ok '
            "worktree add …` 로 다시 실행하세요. 예전 표기인 `git worktree add …  "
            "# [worktree-ok]` 도 그대로 됩니다.",
        ),
        tr(
            '  2. "Switch in the shared tree" — run '
            f"{guard().steer_to_shared(git)} instead.",
            '  2. "공용 트리에서 브랜치만 전환한다" — 대신 '
            f"{guard().steer_to_shared(git)} 중 하나를 실행하세요.",
        ),
    ]


def reason(top, session, new_top, branch, cwd):
    """The ladder's text for a creation it took back."""
    g = guard()
    tr = g.tr
    git = g.git_at(top, cwd)
    lines = [
        tr(
            f"SpecSeal took this worktree back: {new_top} was created and "
            "removed again, and nothing in it was used.",
            f"SpecSeal 이 이 worktree 를 되돌렸습니다: {new_top} 를 만들었다가 "
            "다시 지웠고, 그 안에서 쓰인 것은 없습니다.",
        )
    ]
    if branch:
        lines.append(
            tr(
                f"Its branch `{branch}` stays; `git branch -D {branch}` removes "
                "it if `-b` just made it.",
                f"브랜치 `{branch}` 는 남아 있습니다. `-b` 로 방금 만든 것이면 "
                f"`git branch -D {branch}` 로 지우세요.",
            )
        )
    lines.append("")
    active, idle, reliable = g.sessions_in_tree(top, session)
    ask = tr(
        "Do not choose for the user. Ask with the AskUserQuestion tool, "
        "offering exactly these two options:",
        "사용자 대신 고르지 마세요. AskUserQuestion 툴로 아래 두 선택지를 그대로 "
        "물어보세요:",
    )
    if active:
        lines += [
            tr(
                f"Another Claude session is actively working in {top}, so a "
                "worktree split looks justified. Creating a worktree still "
                "takes the user's confirmation, once per session.",
                f"{top} 에서 다른 Claude 세션이 동시에 작업 중이라 worktree 분리가 "
                "타당해 보입니다. 다만 worktree 생성은 세션마다 한 번 사용자 확인을 "
                "거칩니다.",
            ),
            g.fmt_sessions(active),
            "",
            tr(
                "Do not choose for the user. Ask with the AskUserQuestion tool "
                "whether to create it. If they confirm, re-issue it as `git -c "
                "specseal.answer=worktree-ok worktree add …`; the older "
                "spelling, `git worktree add …  # [worktree-ok]`, still works. "
                "If they decline, use the worktree that session already has, "
                "or wait for it to finish.",
                "사용자 대신 고르지 마세요. AskUserQuestion 툴로 만들지 물어보세요. "
                "확인하면 `git -c specseal.answer=worktree-ok worktree add …` 로 "
                "다시 실행하세요. 예전 표기인 `git worktree add …  # "
                "[worktree-ok]` 도 됩니다. 거절하면 그 세션이 쓰는 worktree 를 "
                "쓰거나 끝날 때까지 기다리세요.",
            ),
        ]
    elif idle or not reliable:
        situation = (
            tr(
                f"The only other sessions in {top} have shown no activity for "
                f"{g.IDLE_MIN}+ minutes. If they are forgotten tabs this is "
                "single-stream work, and a plain `git switch` beats a worktree.",
                f"{top} 의 다른 세션은 {g.IDLE_MIN}분 이상 활동이 없는 것뿐입니다. "
                "잊힌 탭이면 사실상 단건 작업이라 worktree 없이 `git switch` 가 "
                "낫습니다.",
            )
            if idle
            else tr(
                f"Whether other sessions are working in {top} cannot be told "
                "here (process inspection is unavailable), so there is no "
                "automatic verdict.",
                f"{top} 에서 다른 세션이 작업 중인지 여기서는 알 수 없어(프로세스 "
                "조회 불가) 자동 판정을 하지 않습니다.",
            )
        )
        lines += [situation]
        if idle:
            lines.append(g.fmt_sessions(idle))
        lines += ["", ask, "", *_two(git, tr, top)]
    else:
        lines += [
            tr(
                f"No other session is working in {top} (= single-stream). "
                "Rule: for single-stream work, don't create a worktree, switch "
                "branches in the shared tree instead:",
                f"{top} 에서 동시에 작업 중인 다른 세션이 없습니다(= 단건 작업). "
                "룰: 단건이면 worktree 를 만들지 말고 공용 트리에서 브랜치만 "
                "갈아끼웁니다:",
            ),
            "",
            f"  {git} fetch origin",
            f"  {git} switch -c <branch> origin/main   # new branch",
            f"  {git} switch <branch>                  # existing branch",
            "",
            tr(
                "If the user asked for a worktree, re-issue it as `git -c "
                "specseal.answer=worktree-ok worktree add …`; the older "
                "spelling, `git worktree add …  # [worktree-ok]`, still works.",
                "사용자가 worktree 를 지시했다면 `git -c "
                "specseal.answer=worktree-ok worktree add …` 로 다시 실행하세요. "
                "예전 표기인 `git worktree add …  # [worktree-ok]` 도 됩니다.",
            ),
        ]
    return "\n".join(lines)


def post_checkout(cwd, environ, argv, stream):
    previous = argv[0] if argv else ""
    if not previous or set(previous) - {"0"}:
        return 0
    new_top = optin.repo_root(cwd)
    if not new_top:
        return 0
    common = optin.git_common_dir(new_top)
    top = origin_tree(new_top)
    counted = top or new_top
    if not optin.home_at(counted, common):
        return 0
    session, _route = hooksession.session(common, environ)
    if not session:
        return 0
    import worktree_consent

    if (
        harness_made(new_top)
        or worktree_consent.consent(counted, session)
        or answered(cwd, session)
    ):
        worktree_consent.record(counted, session)
        return 0
    where = top or os.path.dirname(common)
    text = reason(where, session, new_top, take_back(new_top, where), cwd)
    stream.write(text + "\n")
    return 1
