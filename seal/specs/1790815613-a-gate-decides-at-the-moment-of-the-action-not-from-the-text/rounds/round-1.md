# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — review round 1

| Field | Value |
|---|---|
| Target SHA | 9fce8f7f9dbfe3146c3803dd10fb510a12763131 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 705 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `12c09ec34795d78b9efdcd5148800fa1a7fd25a5..e9977509d1e593a16ddaea2adb640d725d1b2eab`, 6 commits |
| Contract changes | clear → main, pytest; write → claude_block.py, check, write, main, split, load_checker, load_blocks, write_block, _refuse, post_commit, write_stubs, stamp, rewrite_readme, repoint, due, round-1-report.md, round-1.md, round-2-report.md, round-2.md, plan.md, round_record.py, load, write_record, load_reader, write_atomic, refuse_without_hooks, write_zip, write_members, write_row, install_workflow, fold_check.py, run, settle.py, write_rule_kept, write_anchored, report, retire, restore, run_arms, broad_gate.py, gate, signal, payload_meter.py, _session_cost, _fence_rule, seal_stamp.py, post, pytest; given → main, waived, given, pytest; _key → _leave_mark, _take_mark, round-1-report.md, round-1.md, pytest |
| New units | COMMAND (depth 1); call_id (depth 1); _call_dir (depth 1); _prune (depth 1); _ESCAPE (depth 1); _OTHER (depth 1); _squash (depth 1); _git_process (depth 1); SEQUENCER (depth 1); _process (depth 1); _sequencer_commit (depth 1); _ps (depth 1); call_args (depth 1); _empties_the_environment (depth 1); steps_around_hooks (depth 1); HOOKS (depth 1); install_mod (depth 1); BASH (depth 1); pytestmark (depth 1); SESSION (depth 1); _installer_writes (depth 1); env (depth 1); Clone (depth 1); clone (depth 1); q (depth 1); test_a_refused_dash_capital_b_leaves_the_branch_where_it_was (depth 1); test_a_creation_git_runs_no_undo_for_is_refused_before_it (depth 1); test_a_bash_creation_under_the_harness_path_buys_no_consent (depth 1); test_an_answered_creation_runs_and_the_record_follows_it (depth 1); test_the_old_token_puts_the_creation_to_the_person_before_it_runs (depth 1); test_no_git_hook_judges_a_creation (depth 1); diverged (depth 1); resolve (depth 1); busy (depth 1); test_a_rebase_git_continues_is_not_judged (depth 1); test_an_interactive_rebases_reword_is_not_judged (depth 1); test_a_pick_git_continues_is_not_judged (depth 1); test_a_commit_typed_while_a_rebase_is_paused_is_still_met (depth 1); test_a_commit_an_alias_starts_is_still_judged (depth 1); test_a_mark_an_aborted_commit_left_passes_no_later_commit (depth 1); group (depth 1); as_a_call (depth 1); test_an_old_spelling_waives_no_other_agents_commit (depth 1); STEPS_AROUND (depth 1); test_a_command_that_can_step_around_the_hooks_keeps_the_text_reading (depth 1); test_only_those_words_make_the_reading_judge_a_git_decided_clone (depth 1); test_a_sequencer_that_stopped_on_a_conflict_commits_with_the_date (depth 1); test_what_a_take_back_cannot_undo (depth 1); test_an_emptied_lease_directory_starts_no_python (depth 1); test_a_stub_git_cannot_run_is_written_again_and_decides_nothing_till_then (depth 1); A (depth 1); B (depth 1); shell (depth 1); test_an_answer_is_given_to_the_call_that_carried_it_and_no_other (depth 1); test_another_call_neither_replaces_nor_clears_an_answer (depth 1); test_the_shells_own_spelling_of_the_command_still_matches (depth 1); test_the_argv_is_read_only_when_an_answer_is_there (depth 1); test_a_call_left_behind_is_pruned_by_the_next_write (depth 1); test_a_session_or_call_id_cannot_name_a_directory_outside (depth 1); test_the_tree_answers_are_not_carried (depth 1); test_two_calls_carrying_tokens_at_once_keep_their_own (depth 1); test_two_calls_are_kept_apart_by_id_and_by_command (depth 1); test_a_payload_with_no_tool_use_id_is_keyed_by_its_command (depth 1) |
| Needs a fix | yes — 🔴 1 (a refused `worktree add -B` leaves the branch reset) and 🟡 2–11 (five unjudged action shapes the text gate stands aside for, the `--lock` undo, the backstop's rebase refusals, the stale mark, the shared-session token, and the P2 short-cut's lease directory). |
| Loses a record or crashes | yes — 🔴 1: a refused `git worktree add -B <existing>` moves that branch off its tip, which survives only in the reflog. It is a git branch rather than a record under the seal root, so under a root-only reading this line is no. |

- [x] Pass

## What this round was asked

Round 1 targets `9fce8f7f` and the diff `cd24f516..9fce8f7f`, the whole build, 70 files. It was asked to check stage 1 against `spec.md`, `plan.md` and the owner's answers. It was then asked to attack the silent direction first: a commit or a creation that should be judged and is not. That covered the convergence claim's edges, the backstop's `GIT_AUTHOR_DATE` criterion and its mark, the fallback stepping aside, session identity under P2, the installer, the creation arm's undo, the switch arm's byte pin, the old-spellings translator, and the ledger and policy rewrites.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A refused `worktree add -B <existing>` leaves the branch reset, and the text says it stays and names `git branch -D` | `hooks/creationgate.py:118-126`, `:161-169`, `:271-281` | **fixed** `74b833ec` | fixed at 74b833ec; executed p02: `feat` 77e5a59 → 09b84f2, reflog `branch: Reset to main`; 0.16.0 refused before git ran |
| 🟡 2 | A commit whose hooks git does not run (`-c core.hooksPath`, GIT_CONFIG_* env, stubs removed in the call) is judged by nobody; the policy's known limits omit it | `hooks/commit-review-gate.py:1344-1347`, `docs/commit-review-gate-spec.md:144-161` | **fixed** `5458f376` | fixed at 5458f376; executed c02, c03, c06 landed; 0.16.0 denied c02 and c06 |
| 🟡 3 | A stub made non-executable is never repaired, and `decides` keeps answering yes | `hooks/hook-install.py:116-122`, `hooks/githooks.py:237-241` | **fixed** `b14f1edf` | fixed at b14f1edf; executed c07: modes 0o644 after reinstall, decides True, commit landed |
| 🟡 4 | `worktree add --no-checkout` and `--orphan` run no `post-checkout`, and the guard stands aside | `hooks/worktree-guard.py:1629`, `docs/worktree-guard-spec.md:386` | **fixed** `74b833ec` | fixed at 74b833ec; executed c22, c23 created unjudged; 0.16.0 denied both |
| 🟡 5 | A Bash creation under `.claude/worktrees/` is kept and writes the session's consent | `hooks/creationgate.py:109-115`, `:271-277` | **fixed** `74b833ec` | fixed at 74b833ec; executed c21: kept, record written, the next creation kept; 0.16.0 denied |
| 🟡 6 | `worktree add --lock` is refused but the tree stays, and the text says it was removed | `hooks/creationgate.py:125`, `:155-156` | **fixed** `74b833ec` | fixed at 74b833ec; executed c24: exit 1, the directory and the worktree entry remain |
| 🟡 7 | The backstop refuses `rebase --continue` and `rebase -i` reword; policy, docstring, G1 and G7 say no rebase is met | `hooks/commitgate.py:179-199`, `hooks/githooks.py:37-42`, `docs/commit-review-gate-spec.md:106-118` | **fixed** `65430596` | fixed at 65430596; executed c13, c09 refused mid-rebase; c10, c11 landed |
| 🟡 8 | `env -i` into a clone holding no lease of this session is silent | `hooks/hooksession.py:102-111`, `hooks/githooks.py:109-118` | **fixed** `5458f376` | fixed at 5458f376; executed p01 landed under a real `claude` ancestor |
| 🟡 9 | An old-spelling token written for one agent's call waives every commit of the shared session id while that call runs, and clobbers the other way | `hooks/answers.py:76-109`, `hooks/answer-write.py:28` | **fixed** `e3ecb7d7` | fixed at e3ecb7d7; executed c25 landed; parent and subagent share the id (executed, env) |
| 🟡 10 | A mark left by an aborted commit passes a later `--no-verify` commit with the same HEAD, tree and author date | `hooks/commitgate.py:77-79`, `:107-118` | **fixed** `65430596` | fixed at 65430596; executed c16 landed undeclared |
| 🟡 11 | A person's own commit starts Python wherever a lease directory exists, and the policy says it starts none | `hooks/githooks.py:109-118`, `docs/commit-review-gate-spec.md:156-159` | **fixed** `b14f1edf` | fixed at b14f1edf; executed c18: 50 / 125 / 396 ms medians |
| ⬜ 12 | Contract §9 and §17 say the reading judges only a foreign clone; the policy names two more states | `skills/agent-contract/SKILL.md:241`, `:345` | **fixed** `e3ecb7d7` | fixed at e3ecb7d7; read against the policy's state table and its second known limit |
| ⬜ 13 | The installer's `pre-bash` cost is not "one `stat` per call" and is in no measurement | `hooks/hook-install.py:145-181` | **fixed** `e3ecb7d7` | fixed at e3ecb7d7; executed c19: 97 ms standalone median |
| 🟢 | the switch arm's reader is `86256492`'s byte for byte and gained no rule | `hooks/cmdline_base.py`, `hooks/worktree-guard.py:1629` | confirmed | sha256 equal (executed); the guard's diff is the import and the creation stand-aside alone (read) |
| 🟢 | the ledger holds unscoped | `seal/` | confirmed | `bin/evidence-check .` exit 0, 3,211 ok, 0 drifted, 0 broken (executed) |
| 🟢 | a commit in the declared or undeclared worktree is judged where it lands, `--no-verify` included | `hooks/commitgate.py:129-199` | confirmed | executed c01, c04, c17, c15 |
| 🟢 | P2: a commit with no session is not judged | `hooks/hooksession.py:102-111` | confirmed | executed c18, 15 of 15 landed |
| ❓ | Whether a `systemMessage` from the installer reaches the model or only the person | `hooks/hook-install.py:184-195` | ❓ out of verified scope | the harness renders it, and nothing here ran under the harness; the orchestrator answers it |
| ❓ | Whether a command the person types with `!` in a Claude Code session is "a person's own commit" under P2 — it carries `CLAUDECODE` and is judged | `hooks/githooks.py:109-118` | ❓ out of verified scope | the owner answers it; not executed |
| ❓ | The stubs under a real Claude Code session, M4's version floor, M5 | `overview.md` §*Not verified* | ❓ out of verified scope | carried from the build's own list; the orchestrator answers it |

## Paste-ready fixes

```python
# hooks/creationgate.py — beside take_back
def restore_reset(branch, where):
    """Put back a branch `worktree add -B` just reset; the tip restored, or "".

    `-B` moves an existing branch before `post-checkout` runs, and taking the
    worktree back does not move it again. git's reflog names that reset as the
    branch's newest entry, and the entry before it is the old tip.
    """
    if not branch:
        return ""
    ref = f"refs/heads/{branch}"
    last = _git(["reflog", "show", "-n", "1", "--format=%gs", ref], where)
    if last is None or last.returncode != 0:
        return ""
    if not last.stdout.startswith("branch: Reset to "):
        return ""
    prev = _git(["rev-parse", "--verify", "--quiet", f"{ref}@{{1}}"], where)
    if prev is None or prev.returncode != 0 or not prev.stdout.strip():
        return ""
    tip = prev.stdout.strip()
    done = _git(["update-ref", "-m", "specseal: undo worktree add -B", ref, tip], where)
    return tip if done is not None and done.returncode == 0 else ""


# post_checkout, the last three lines become
    where = top or os.path.dirname(common)
    branch, gone = take_back(new_top, where)
    restored = restore_reset(branch, where) if gone else ""
    text = reason(where, session, new_top, branch, cwd, gone=gone, restored=restored)
    stream.write(text + "\n")
    return 1


# reason(top, session, new_top, branch, cwd, gone=True, restored=""): the branch line
    if branch and restored:
        lines.append(
            tr(
                f"`-B` had reset its branch `{branch}`; it is back at {restored[:12]}.",
                f"`-B` 가 초기화한 브랜치 `{branch}` 를 {restored[:12]} 로 되돌렸습니다.",
            )
        )
    elif branch:
        lines.append(
            tr(
                f"Its branch `{branch}` stays; `git branch -D {branch}` removes "
                "it if `-b` just made it.",
                f"브랜치 `{branch}` 는 남아 있습니다. `-b` 로 방금 만든 것이면 "
                f"`git branch -D {branch}` 로 지우세요.",
            )
        )
```
```markdown
- **A commit whose hooks git does not run is judged by nobody in a clone that
  carries the stubs.** `git -c core.hooksPath=<elsewhere> commit`, the same
  setting through `GIT_CONFIG_PARAMETERS` or GIT_CONFIG_COUNT and its KEY and
  VALUE pairs, and a command that removes the stubs before it commits each
  step around `pre-commit` and `reference-transaction` at once. The PreToolUse
  reading has already stood aside for that clone, because it asked before the
  command ran, and 0.16.0's reading stopped each of these. The installer cannot
  answer them: the setting or the removal lives inside the one call.
```
```python
# hooks/hook-install.py, write_stubs: the skip
        found = githooks.read_stub(path)
        if found and found[0]:
            try:
                with open(path, encoding="utf-8") as f:
                    current = f.read() == text
            except OSError:
                current = False
            # git skips a hook it cannot execute, so a stub with the right
            # bytes and the wrong mode is a stub to write again.
            if current and os.access(path, os.X_OK):
                continue


# hooks/githooks.py, decides: the loop
    for hook in HOOKS:
        path = os.path.join(directory, hook)
        found = read_stub(path)
        if (
            not found
            or not found[0]
            or not found[2]
            or not os.path.isfile(found[2])
            or not os.access(path, os.X_OK)
        ):
            return False
    return True
```
```markdown
- `git worktree add --no-checkout` and `git worktree add --orphan` run no
  `post-checkout` (2.50.1, executed in round 1), so where this plugin's git
  hooks run they are judged by nobody: the Bash creation rows of §B stand
  aside for the clone, and git has no hook to run. 0.16.0's reading denied
  both.
```
```python
# hooks/creationgate.py, post_checkout: replaces the combined condition
    if harness_made(new_top):
        # The Agent/Task arm put this creation to the person before the spawn,
        # and its PostToolUse arm records it. A Bash command naming the same
        # path is not that answer: the tree is kept while M5 is unmeasured, and
        # it buys no consent for the creations after it.
        return 0
    if worktree_consent.consent(counted, session) or answered(cwd, session):
        worktree_consent.record(counted, session)
        return 0
```
```python
# hooks/creationgate.py
def take_back(new_top, where):
    """Remove the worktree just made, running git from `where` -- another
    worktree of the clone; (the branch it was on or "", whether it is gone)."""
    branch = ""
    out = _git(["symbolic-ref", "-q", "--short", "HEAD"], new_top)
    if out is not None and out.returncode == 0:
        branch = out.stdout.strip()
    # Twice: `worktree add --lock` leaves the new tree locked, and one
    # `--force` refuses a locked worktree.
    _git(["worktree", "remove", "--force", "--force", new_top], where)
    return branch, not os.path.isdir(new_top)


# reason(...): the opening line
    opening = (
        tr(
            f"SpecSeal took this worktree back: {new_top} was created and "
            "removed again, and nothing in it was used.",
            f"SpecSeal 이 이 worktree 를 되돌렸습니다: {new_top} 를 만들었다가 "
            "다시 지웠고, 그 안에서 쓰인 것은 없습니다.",
        )
        if gone
        else tr(
            f"SpecSeal refused this worktree, but {new_top} could not be "
            f"removed: run `git worktree remove --force --force {new_top}`.",
            f"SpecSeal 이 이 worktree 를 거절했지만 {new_top} 를 지우지 "
            f"못했습니다: `git worktree remove --force --force {new_top}` 를 "
            "실행하세요.",
        )
    )
    lines = [opening]
```
```python
# hooks/commitgate.py
# What a rebase, cherry-pick, revert or am leaves under the git directory
# while it runs. Their commits go through a child `git commit -n`, which hands
# the hook GIT_AUTHOR_DATE and skips pre-commit; without this the backstop
# refuses `rebase --continue` and an interactive rebase's reword.
SEQUENCER = ("rebase-merge", "rebase-apply", "sequencer", "CHERRY_PICK_HEAD", "REVERT_HEAD")


def _sequencer_running(cwd):
    git_dir = gate.git(["rev-parse", "--absolute-git-dir"], cwd)
    return bool(git_dir) and any(
        os.path.exists(os.path.join(git_dir, name)) for name in SEQUENCER
    )


# reference_transaction, after `if not pairs: return 0`
    if _sequencer_running(cwd):
        return 0
```
```python
# hooks/hooksession.py
def session(common, environ=None):
    """(session id, route) for the hook running now; ("", "") for none."""
    environ = os.environ if environ is None else environ
    sid = _clean(environ.get("CLAUDE_CODE_SESSION_ID"))
    if sid:
        return sid, "environment"
    pid = claude_ancestor()
    sid = from_lease(common, pid)
    if sid:
        return sid, "lease"
    # A `claude` above the hook is a Claude session even where it holds no
    # lease in this clone (`env -i git -C <other clone> commit`). P2 makes
    # only a commit with NO session a person's own; this one is judged, as a
    # session whose press and answers cannot be read.
    if pid is not None:
        return f"pid-{pid}", "ancestor"
    return "", ""
```
```markdown
- **An emptied environment, in a clone where no session holds a lease, is a
  person's commit to the stub.** `env -i git commit` loses the session
  variables, and the stub leaves before Python wherever the clone has no
  lease, because walking the process table for a `claude` ancestor on every
  person's commit is the cost P2's answer avoids. 0.16.0's reading stopped it.
```
```markdown
- **An old spelling stands for every agent of the session while the call that
  carried it runs.** The answer is kept per session id, and the parent and each
  subagent share one. A commit another agent makes in that window reads the
  token, and a Bash call another agent starts in that window clears it. The
  git-native `git -c specseal.waive=…` belongs to its own command and has
  neither problem.
```
```python
# hooks/commitgate.py
def _key(old, tree, date, process=None):
    # Both hooks of one commit are children of the one `git commit` process,
    # so naming it means a mark left by a commit that aborted after
    # `pre-commit` can never be taken by a later commit with the same HEAD,
    # tree and date.
    old = "" if not old or set(old) <= ZERO else old
    process = os.getppid() if process is None else process
    return hashlib.sha1(f"{old}\n{tree}\n{date}\n{process}".encode()).hexdigest()
```
```python
# hooks/githooks.py
_P2 = (
    'if [ -z "$CLAUDE_CODE_SESSION_ID$CLAUDECODE" ]; then\n'
    "  c=$(git rev-parse --git-common-dir 2>/dev/null)\n"
    "  l=\n"
    '  for d in "$c/specseal-leases" "$c"/worktrees/*/specseal-leases; do\n'
    '    for f in "$d"/*; do [ -e "$f" ] && l=1; break; done\n'
    "  done\n"
    '  [ -n "$l" ] || {{ {drain}exit 0; }}\n'
    "fi\n"
)
```
```markdown
  ref update that is not a commit, a fetch's among them, starts none, and a
  person's own commit starts none where no session holds a lease in the clone;
  while one does, it pays the two hooks' interpreter starts (396 ms against
  50 ms with no stubs, round 1 of #692).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_the_frozen_reading_never_grows.py`, `tests/test_the_hooks_are_installed_where_git_runs_them.py`, `tests/test_the_old_spellings_reach_the_hook.py`, `tests/test_a_creation_is_judged_where_git_made_it.py`, `tests/test_the_hook_surface_git_offers.py`, in the round's clone | 81 passed, exit 0 |
| `bin/evidence-check .`, unscoped | exit 0; 3,211 ok, 0 drifted, 0 broken |
| sha256 of `git show 86256492:hooks/cmdline.py` less line 1, and of `hooks/cmdline_base.py` below the rider's `Verified` line | equal |
| one `test_tmp_` script driving real git 2.50.1 through the clone's own stubs (installed by `hooks/hook-install.py` into scratch repositories only), cases c01–c26 | as reported per finding above |
| a second `test_tmp_` script: each command's payload through the target's and the installed 0.16.0's `commit-review-gate.py` and `worktree-guard.py` | target silent on all six; 0.16.0 `deny`/`ask` on all six |
| a third `test_tmp_` script: `env -i` commit (p01) and `worktree add -B` (p02) | p01 landed; p02 branch reset left |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — none of the three was run here, and it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
