# Round 1 report — a gate decides at the moment of the action (#692)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | `9fce8f7f9dbfe3146c3803dd10fb510a12763131` |
| Base | `cd24f516` (diff `cd24f516..9fce8f7f`, 70 files) |
| Reviewer | warden |
| Where | a `git clone --no-local` of the branch at the target, under the session scratchpad; real-git probes in scratch repositories under the round directory, every one removed at hand-over |

## How the work relates, in one picture

```
the convergence claim ── holds for any SHELL construct (S1, S2, c01, c04, c17 executed)
   │
   ├─ but a commit or creation git runs no hook for is judged by nobody,
   │  because the text gate asked before the command and stood aside
   │     → 🟡 2 (-c core.hooksPath, GIT_CONFIG_* env, stubs removed in the call)
   │     → 🟡 3 (a stub made non-executable: never repaired, decides() still yes)
   │     → 🟡 4 (worktree add --no-checkout / --orphan: no post-checkout at all)
   │     → 🟡 5 (.claude/worktrees/ from Bash: kept, and buys consent)
   │     → 🟡 8 (env -i into a clone with no lease of this session)
   │
   ├─ the undo of a refused creation is not an undo everywhere
   │     → 🔴 1 (worktree add -B resets an existing branch, and it stays reset)
   │     → 🟡 6 (worktree add --lock: the tree stays, the text says it went)
   │
   ├─ the backstop's criterion is wider than the policy says
   │     → 🟡 7 (rebase --continue and rebase -i reword are refused)
   │     → 🟡 10 (a mark from an aborted commit passes a later --no-verify one)
   │
   └─ the old-spelling translator and the P2 short-cut
         → 🟡 9 (a token in one agent's call waives another agent's commit)
         → 🟡 11 (a person's own commit starts Python in every clone a session ever used)
```

## Stage 1 — against `spec.md`, `plan.md`, `questions.md`

Read, every claim checked against the code at the target:

- **P1 (a)** is built as answered: a foreign slot (`core.hooksPath` at any level,
  or an unmarked hook file) installs nothing, takes this plugin's stubs out, and
  is said once per session (`hooks/hook-install.py:162-168`; their module
  executed green, below).
- **P2 (a)** is built: with no session the hooks exit 0. Executed: five commits
  with no Claude variables all landed (probe c18). The short-cut that is
  supposed to make this free is 🟡 11.
- **P4 option 1** is built: `hooks/cmdline_base.py` below its rider hashes to
  the same sha256 as `86256492:hooks/cmdline.py` less its shebang (executed),
  and `hooks/worktree-guard.py` gained only the import and the creation
  stand-aside at `:1629`; the switch path has no hunk.
- **P3 (a)** and **the backstop criterion** were decided by the build and
  recorded in `phases/phase-1.md` and `phase-3.md`. The criterion's measured
  list is incomplete (🟡 7).
- **P5** is open for the owner and the build kept the text paths as a
  stepping-aside fallback (`overview.md` §*diverged*). This report does not
  answer P5; findings 2, 3, 4, 5 and 8 are what the stand-aside costs where
  git runs no hook, and they are the measurement P5's owner may want.
- **Divergences** in `overview.md` are each stated with grounds. One is not
  true as written: phase 1's *"Every creation runs `post-checkout` on the four
  gits (M3, M14), which is the argument from construction"*
  (`phases/phase-1.md:211`). `worktree add --no-checkout` and `--orphan` run
  none on 2.50.1 (executed, 🟡 4).

What the implementer's account asserted and what I found:

- *Claimed* "no merge, reset, cherry-pick, rebase or pull" hands
  `GIT_AUTHOR_DATE` to `reference-transaction` (`hooks/githooks.py:37-42`,
  `docs/commit-review-gate-spec.md:111-114`, ledger G1 and G7). *Found*: a
  conflicted `git rebase --continue` and an interactive rebase's `reword` both
  reach the backstop and are refused (executed, 🟡 7).
- *Claimed* the installer answers "`core.hooksPath` pointing elsewhere, a stub
  deleted or made non-executable" (`spec.md` §*The convergence argument*).
  *Found*: it does not repair a mode (executed, 🟡 3) and cannot see a
  per-invocation `-c` (executed, 🟡 2).
- *Claimed* "a person's own commit start[s] none" (`docs/commit-review-gate-spec.md:156-159`).
  *Found*: true only in a clone with no lease directory; a session's first Bash
  call creates one and nothing removes it (executed, 🟡 11).
- *Claimed* the answer "lives for one Bash call" (`hooks/answers.py:8-10`).
  *Found*: it is keyed by a session id the parent and every subagent share
  (executed: this subagent's `CLAUDE_CODE_SESSION_ID` is its parent's), so it
  lives for one call of whichever agent wrote it, and every agent's commit in
  that window reads it (🟡 9).

## Stage 2 — quality, the silent direction first

### 🔴 1 — A refused `git worktree add -B <existing>` leaves that branch reset

`hooks/creationgate.py:271-281` takes the worktree back after `-B` has already
reset the branch. `take_back` (`:118-126`) removes the tree and nothing moves
the branch back. Executed (probe p02): branch `feat` at `77e5a59` with its own
commit, `git worktree add -B feat ../wt main` → exit 1, the worktree gone, and
`feat` at main's tip `09b84f2`. Its reflog reads `feat@{0}: branch: Reset to
main`. The refusal text then says `` Its branch `feat` stays; `git branch -D
feat` removes it if `-b` just made it `` (`:161-169`), which is false and points
the model at deleting the branch.

Why it matters: 0.16.0's text guard refused this command before git ran, so
nothing moved. Now a refused creation discards a branch's tip, which survives
only in the reflog, and the text steers toward deleting the branch outright.
The policy's "the undo leaves the branch `-b` made" (`docs/worktree-guard-spec.md:687`)
does not name `-B`.

### 🟡 2 — A commit whose hooks git does not run is judged by nobody

In a clone carrying the stubs, `hooks/commit-review-gate.py:1344-1347` stands
aside before the command runs, and these commands then commit with no hook at
all. Executed (c02, c03, c06; text-gate verdicts from the target and from the
installed 0.16.0 gate on the same payload):

| Command | Target | 0.16.0 |
|---|---|---|
| `git -c core.hooksPath=/dev/null commit -m x` | landed, text gate silent | deny |
| GIT_CONFIG_COUNT=1, GIT_CONFIG_KEY_0=core.hooksPath, GIT_CONFIG_VALUE_0=/nonexistent, then `git commit` | landed | not measured |
| `rm -f .git/hooks/pre-commit .git/hooks/reference-transaction && git commit -m x` | landed, text gate silent | deny |

Each is a stop 0.16.0 made on a real commit that the target drops. The
spec's convergence list answers `core.hooksPath` with "the installer re-checks
at every session start and every Bash call", which cannot see a setting that
lives in one invocation. `docs/commit-review-gate-spec.md` §*Known limits of
the commit gate inside git* (`:144-161`) lists neither.

### 🟡 3 — A stub made non-executable is never repaired, and `decides` still says yes

`write_stubs` (`hooks/hook-install.py:116-122`) skips a stub whose bytes match
and never looks at its mode. `decides` (`hooks/githooks.py:237-241`) checks the
marker and the entry point, not that git can run the file. Executed (c07):
`chmod 644` on `pre-commit` and `reference-transaction`, the installer run
again → modes still `0o644`, `decides` → `True`, `git commit -m x` landed.
git skips a hook it cannot execute, and the text gate stands aside on
`decides`. So the clone stays unjudged on every later call, not only the one
that changed the mode. The spec names this case as one the installer answers.

### 🟡 4 — `worktree add --no-checkout` and `--orphan` are judged by nobody

git runs no `post-checkout` for either (2.50.1, executed: c22, c23 both
created, no record, no refusal), and `guard_worktree_creation` stands aside at
`hooks/worktree-guard.py:1629` because the clone carries stubs. Installed
0.16.0's guard answered `deny` to both (executed). The policy says "a creation
is judged whatever `cd`, redirection, loop variable or `eval` stood in front
of it" (`docs/worktree-guard-spec.md:386`) and its known limits do not name
these flags. The phase 1 claim at `phases/phase-1.md:211` is the same claim.

### 🟡 5 — A Bash creation under `.claude/worktrees/` is kept and buys the session's consent

`harness_made` (`hooks/creationgate.py:109-115`) matches any path with
`.claude/worktrees/` in it, and `post_checkout` (`:271-277`) then writes the
consent record. Executed (c21): `git worktree add .claude/worktrees/x -b n21`
from Bash in an attended session with no consent → kept, record written. The
next `git worktree add ../c21_second -b n21b` → kept too. 0.16.0's guard
denied the first (executed). The exemption exists for the Agent/Task spawn the
person already approved (M5 unmeasured), but nothing ties it to that spawn. A
model refused once can name the path and lift the ladder for the rest of the
session. That is the "consent nobody gave" the policy's own stand-aside
paragraph warns about.

### 🟡 6 — `worktree add --lock` is refused but its tree stays

`take_back` runs `git worktree remove --force` (`hooks/creationgate.py:125`),
and one `--force` refuses a locked worktree. Executed (c24): exit 1, the
worktree still listed, the directory still there. The text opens with
"SpecSeal took this worktree back: … was created and removed again"
(`:155-156`), which is false.

### 🟡 7 — The backstop refuses `rebase --continue` and an interactive rebase's `reword`

The sequencer commits through a child `git commit -n` that exports
`GIT_AUTHOR_DATE` and skips `pre-commit`, so `reference_transaction`
(`hooks/commitgate.py:179-199`) finds no mark and refuses. Executed in an
undeclared opted-in repository:

- c13: a conflicted `git rebase main`, resolved and staged, then `git rebase
  --continue` → refused, the rebase left in progress on a detached HEAD.
- c09: `git rebase -i main` with `reword` → refused after the first pick.
- c10, c11: `rebase --committer-date-is-author-date` and `merge --no-ff`
  landed unjudged, as the policy says.

0.16.0 judged neither command. The policy (`docs/commit-review-gate-spec.md:106-118`),
`hooks/githooks.py:37-42` and ledger rows G1 and G7 say no rebase is met. The
refusal text names `--no-verify` and advises `git -c specseal.waive=review
commit …`, which does not describe what the model ran. The fail direction is
a stop, but it is a stop the policy says does not exist. Whether a
cherry-pick or revert paused on a conflict behaves the same is read from the
same sequencer path and not executed (c12's setup hit an unrelated conflict).

### 🟡 8 — `env -i` into a clone with no lease of this session is silent

`hooksession.session` (`hooks/hooksession.py:102-111`) falls back to a lease
in the clone being committed into. A session holds leases only in clones its
payload `cwd` has been in. Executed (p01): `env -i PATH=… git commit -m x`
from under a real `claude` process, into a stubbed clone holding no lease →
landed. Where the clone has no lease directory at all, the stub leaves in
`sh` (`hooks/githooks.py:109-118`) before Python can look for the ancestor.
0.16.0's text gate stopped `env -i git commit` (M6's own rows). S9's case uses
a lease in the same clone, so it does not see this.

### 🟡 9 — A token in one agent's Bash call waives another agent's commit

`hooks/answer-write.py:28` writes under the payload's `session_id`, and
`answers.given` (`hooks/answers.py:97-109`) answers for any hook that carries
the same id. The parent and every subagent share one `CLAUDE_CODE_SESSION_ID`
(executed: this subagent's environment carries its parent's id and
`CLAUDE_CODE_CHILD_SESSION=1`). Executed (c25): with call A's `[no-review]`
written, a commit from another call with no token landed. So while agent A's
`: '[no-review]'; bin/test && git commit` runs, agent B's commit into any
undeclared repository is waived silently. The other order clobbers:
`answers.write` clears the session's files first (`:78`), so B's next call
removes A's token before A's commit reaches its hook.

### 🟡 10 — A mark from an aborted commit passes a later commit `pre-commit` never saw

`_key` (`hooks/commitgate.py:77-79`) is the old HEAD, the tree and the author
date. A commit that aborts after `pre-commit` leaves its mark for a day.
Executed (c16): `git -c specseal.waive=review commit -m ''` aborted on the
empty message and left one mark. Then `git commit --no-verify -m x` with the
same `GIT_AUTHOR_DATE` landed in the undeclared repository. The same holds
unpinned within one second of the abort. The policy and G7 say the mark lets
through only the commit `pre-commit` judged.

### 🟡 11 — A person's own commit starts Python in every clone a session has used

`_P2` (`hooks/githooks.py:109-118`) starts Python when any `specseal-leases`
*directory* exists. `hooks/session-lease.py` prunes lease files and never the
directory. Executed (c18, five commits each, medians): 50 ms with no stubs,
125 ms with stubs and no lease directory, 396 ms with an empty lease
directory. Every commit landed, so P2's decision holds. The policy's "a
person's own commit start[s] none" (`docs/commit-review-gate-spec.md:156-159`)
is false in every clone a session has run a Bash call in.

### ⬜ 12 — Contract §9 and §17 say the reading judges only a foreign clone

`skills/agent-contract/SKILL.md:241` and `:345` say that since #692 the
reading "judges only a clone whose hooks slot is somebody else's". The policy's
own state table also names an opted-in clone no session has reached, and its
second known limit names an unplaceable target. Behaviour and the policy are
right; the two sentences undercount.

### ⬜ 13 — The installer costs more than "one `stat` per call"

`spec.md` §*Scope* 2 says the installer runs in `pre-bash` "as one `stat` per
call". Executed (c19): `hooks/hook-install.py` with current stubs took 97 ms
median as its own process, interpreter start included. Inside the dispatcher
it pays two to three `git` processes and five file reads per Bash call. M10
measured commits only, and the policy's latency limit says nothing about
`pre-bash`. In-dispatcher cost is not measured here.

### Confirmed

- Executed: a plain commit (c01) and `--no-verify` (c04) are refused in an
  undeclared opted-in clone; a linked worktree's `rev-parse --git-path hooks`
  answers the main checkout's `.git/hooks` and its commit is refused (c17); a
  waived commit leaves no mark behind (c15); a plain attended creation is taken
  back with no tree left (c20).
- Executed: `bin/evidence-check .`, unscoped, exit 0 — 3,211 ok, 0 drifted,
  0 broken.
- Executed: the five new modules below pass at the target.
- Read: the dispatcher runs gates in-process and in order
  (`hooks/dispatch.py:123-165`), so the installer's write lands before the
  commit gate asks `decides`, and the first Bash call in a clone is judged by
  git.
- Read: the two readers can both judge one commit only where the session's
  own clone carries no stubs and the text cannot place a target that does. The
  text gate's deny then stops the command first, and where it allows, the hook
  judges with the same arms. That is not a silent case.

### Items the prompt asked about that are not findings

- `git commit-tree` with `update-ref` and `git am` land unjudged (c05, c08,
  executed), as under 0.16.0, whose reading never treated them as commits.
  `git stash` moves no branch. Neither is a stop lost. The policy's known
  limits do not name them, and 🟡 2's paragraph is where a sentence would go.
- `tokens.given` reads a token out of a heredoc body (c26, executed), and
  installed 0.16.0's `has_marker` does the same on the same command
  (executed). It is not a regression.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A refused `worktree add -B <existing>` leaves the branch reset, and the text says it stays and names `git branch -D` | `hooks/creationgate.py:118-126`, `:161-169`, `:271-281` | open | executed p02: `feat` 77e5a59 → 09b84f2, reflog `branch: Reset to main`; 0.16.0 refused before git ran |
| 🟡 2 | A commit whose hooks git does not run (`-c core.hooksPath`, GIT_CONFIG_* env, stubs removed in the call) is judged by nobody; the policy's known limits omit it | `hooks/commit-review-gate.py:1344-1347`, `docs/commit-review-gate-spec.md:144-161` | open | executed c02, c03, c06 landed; 0.16.0 denied c02 and c06 |
| 🟡 3 | A stub made non-executable is never repaired, and `decides` keeps answering yes | `hooks/hook-install.py:116-122`, `hooks/githooks.py:237-241` | open | executed c07: modes 0o644 after reinstall, decides True, commit landed |
| 🟡 4 | `worktree add --no-checkout` and `--orphan` run no `post-checkout`, and the guard stands aside | `hooks/worktree-guard.py:1629`, `docs/worktree-guard-spec.md:386` | open | executed c22, c23 created unjudged; 0.16.0 denied both |
| 🟡 5 | A Bash creation under `.claude/worktrees/` is kept and writes the session's consent | `hooks/creationgate.py:109-115`, `:271-277` | open | executed c21: kept, record written, the next creation kept; 0.16.0 denied |
| 🟡 6 | `worktree add --lock` is refused but the tree stays, and the text says it was removed | `hooks/creationgate.py:125`, `:155-156` | open | executed c24: exit 1, the directory and the worktree entry remain |
| 🟡 7 | The backstop refuses `rebase --continue` and `rebase -i` reword; policy, docstring, G1 and G7 say no rebase is met | `hooks/commitgate.py:179-199`, `hooks/githooks.py:37-42`, `docs/commit-review-gate-spec.md:106-118` | open | executed c13, c09 refused mid-rebase; c10, c11 landed |
| 🟡 8 | `env -i` into a clone holding no lease of this session is silent | `hooks/hooksession.py:102-111`, `hooks/githooks.py:109-118` | open | executed p01 landed under a real `claude` ancestor |
| 🟡 9 | An old-spelling token written for one agent's call waives every commit of the shared session id while that call runs, and clobbers the other way | `hooks/answers.py:76-109`, `hooks/answer-write.py:28` | open | executed c25 landed; parent and subagent share the id (executed, env) |
| 🟡 10 | A mark left by an aborted commit passes a later `--no-verify` commit with the same HEAD, tree and author date | `hooks/commitgate.py:77-79`, `:107-118` | open | executed c16 landed undeclared |
| 🟡 11 | A person's own commit starts Python wherever a lease directory exists, and the policy says it starts none | `hooks/githooks.py:109-118`, `docs/commit-review-gate-spec.md:156-159` | open | executed c18: 50 / 125 / 396 ms medians |
| ⬜ 12 | Contract §9 and §17 say the reading judges only a foreign clone; the policy names two more states | `skills/agent-contract/SKILL.md:241`, `:345` | open | read against the policy's state table and its second known limit |
| ⬜ 13 | The installer's `pre-bash` cost is not "one `stat` per call" and is in no measurement | `hooks/hook-install.py:145-181` | open | executed c19: 97 ms standalone median |
| 🟢 | the switch arm's reader is `86256492`'s byte for byte and gained no rule | `hooks/cmdline_base.py`, `hooks/worktree-guard.py:1629` | confirmed | sha256 equal (executed); the guard's diff is the import and the creation stand-aside alone (read) |
| 🟢 | the ledger holds unscoped | `seal/` | confirmed | `bin/evidence-check .` exit 0, 3,211 ok, 0 drifted, 0 broken (executed) |
| 🟢 | a commit in the declared or undeclared worktree is judged where it lands, `--no-verify` included | `hooks/commitgate.py:129-199` | confirmed | executed c01, c04, c17, c15 |
| 🟢 | P2: a commit with no session is not judged | `hooks/hooksession.py:102-111` | confirmed | executed c18, 15 of 15 landed |
| ❓ | Whether a `systemMessage` from the installer reaches the model or only the person | `hooks/hook-install.py:184-195` | ❓ out of verified scope | the harness renders it, and nothing here ran under the harness; the orchestrator answers it |
| ❓ | Whether a command the person types with `!` in a Claude Code session is "a person's own commit" under P2 — it carries `CLAUDECODE` and is judged | `hooks/githooks.py:109-118` | ❓ out of verified scope | the owner answers it; not executed |
| ❓ | The stubs under a real Claude Code session, M4's version floor, M5 | `overview.md` §*Not verified* | ❓ out of verified scope | carried from the build's own list; the orchestrator answers it |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🔴 1 — put back a branch `-B` reset (applies on top of 🟡 6's `take_back`)

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

The reflog subject `branch: Reset to <start>` was read on 2.50.1 (executed);
the smith confirms it on 2.34.1–2.43.0 before relying on it there.

### 🟡 2 — say it in the policy (and the owner may want the text gate not to stand aside)

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

Goes after the second bullet of `docs/commit-review-gate-spec.md` §*Known
limits of the commit gate inside git*. The spec's convergence paragraph, which
says the installer answers `core.hooksPath`, gets the same narrowing.

### 🟡 3 — a stub git cannot run is not a stub that decides

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

### 🟡 4 — the creations git runs no `post-checkout` for

```markdown
- `git worktree add --no-checkout` and `git worktree add --orphan` run no
  `post-checkout` (2.50.1, executed in round 1), so where this plugin's git
  hooks run they are judged by nobody: the Bash creation rows of §B stand
  aside for the clone, and git has no hook to run. 0.16.0's reading denied
  both.
```

Goes in `docs/worktree-guard-spec.md` §*Known limits*, and the sentence at
`:386` gains "unless the creation passes `--no-checkout` or `--orphan`". The
alternative that keeps the stop is in code and is the owner's call: the
guard's caller already parses the creation's arguments with the frozen
reader, so it can pass whether either flag is present, and the stand-aside
at `hooks/worktree-guard.py:1629` can skip only when neither is.

### 🟡 5 — the harness's path keeps the tree and buys no consent

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

The residue is that a Bash creation under `.claude/worktrees/` itself stays
unjudged. Add that sentence to the policy paragraph at
`docs/worktree-guard-spec.md:413`.

### 🟡 6 — remove a locked tree too, and say so only when it is gone

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

### 🟡 7 — the sequencer's own commits are not the backstop's

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

The trade is that a `git commit --no-verify` typed while a rebase or
cherry-pick is paused goes unbackstopped. A plain `git commit` there still
meets `pre-commit`. Correct the policy sentence at
`docs/commit-review-gate-spec.md:111-114`, `hooks/githooks.py:37-42`, and
ledger rows G1 and G7 in place to name that trade. Extend
`test_only_git_commit_hands_reference_transaction_an_author_date` with the
two shapes that DO hand it the date, so the pin says what git does.

### 🟡 8 — a `claude` above the hook is a session even with no lease here

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

The code half closes the case where the clone has some lease; the markdown
goes in the policy's known limits for the case where it has none.

### 🟡 9 — the window a token stands in, said, and the design question

```markdown
- **An old spelling stands for every agent of the session while the call that
  carried it runs.** The answer is kept per session id, and the parent and each
  subagent share one. A commit another agent makes in that window reads the
  token, and a Bash call another agent starts in that window clears it. The
  git-native `git -c specseal.waive=…` belongs to its own command and has
  neither problem.
```

Goes in the policy's known limits. Closing it in code needs a key the
PreToolUse writer and the git hook both see, and no such key exists today. One
candidate is the writer prefixing the command with an exported variable
through PreToolUse's `updatedInput`, so the answer lives in that call's own
process tree. Whether the harness honours `updatedInput` without an `allow`
decision is unverified, and that design is the owner's (P3) call.

### 🟡 10 — a mark belongs to the git process that left it

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

### 🟡 11 — look for a lease, not for the directory that held one

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

The markdown replaces the last sentence of the *Latency* bullet at
`docs/commit-review-gate-spec.md:156-159`.

## Regression tests to plant

| Case | Destination |
|---|---|
| a refused `git worktree add -B feat` leaves `feat` at its old tip, and the text names the restore | `tests/test_a_creation_is_judged_where_git_made_it.py` |
| a refused `git worktree add --lock` leaves no directory and no worktree entry | `tests/test_a_creation_is_judged_where_git_made_it.py` |
| a Bash creation under `.claude/worktrees/` writes no consent record, and the next creation is refused | `tests/test_a_creation_is_judged_where_git_made_it.py` |
| a stub chmodded 644 is made executable again by the installer, and `decides` answers no until it is | `tests/test_the_hooks_are_installed_where_git_runs_them.py` |
| a conflicted `git rebase --continue` and a `rebase -i` reword land in an undeclared clone | `tests/test_the_commit_gate_decides_at_the_commit.py` |
| an aborted waived commit's mark does not pass a later `--no-verify` commit with a pinned author date | `tests/test_the_commit_gate_decides_at_the_commit.py` |
| a person's commit in a clone with an empty `specseal-leases` directory starts no interpreter (a `python3` shim on PATH that logs) | `tests/test_the_hooks_are_installed_where_git_runs_them.py` |
| `env -i` commit under a `claude` ancestor into a clone holding another session's lease is refused | `tests/test_the_commit_gate_decides_at_the_commit.py` |

Each is to be seen red against the target before it is planted (§15). Every
shape above was seen landing or failing at the target in this round's probes.

## Facts for the evidence ledger

- G1 and G7 (this item's fragment) are false as written: a conflicted
  `git rebase --continue` and a `rebase -i` reword hand `reference-transaction`
  `GIT_AUTHOR_DATE` on 2.50.1 (executed). Correct them in place with the fix
  of 🟡 7.
- G10's "keeps a worktree under `.claude/worktrees/`" is true of the code and
  silent on the consent record it writes there; rewrite it with 🟡 5's fix.
- New, executed on 2.50.1: `git worktree add --no-checkout` and `--orphan` run
  no `post-checkout`; `git -c core.hooksPath=/dev/null` and the GIT_CONFIG_COUNT
  form run no hook at all; `git worktree remove --force` once refuses a tree
  made with `--lock`; `worktree add -B` over an existing branch writes the
  reflog subject `branch: Reset to <start>`.

Needs a fix: yes — 🔴 1 (a refused `worktree add -B` leaves the branch reset) and 🟡 2–11 (five unjudged action shapes the text gate stands aside for, the `--lock` undo, the backstop's rebase refusals, the stale mark, the shared-session token, and the P2 short-cut's lease directory).
Loses a record or crashes: yes — 🔴 1: a refused `git worktree add -B <existing>` moves that branch off its tip, which survives only in the reflog. It is a git branch rather than a record under the seal root, so under a root-only reading this line is no.

## Proof block

Opened in this round, at the target, in the round's clone or read-only in the
branch's worktree:

- `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/`: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `survivors.md`, `phases/phase-1.md` (M6, M12–M14, §*Resumed*), `phases/phase-3.md`, `phases/phase-4.md`, `phases/phase-5.md`
- `hooks/githooks.py`, `hooks/hook-install.py`, `hooks/hooksession.py`, `hooks/commitgate.py`, `hooks/gate.py`, `hooks/creationgate.py`, `hooks/answers.py`, `hooks/tokens.py`, `hooks/answer-write.py`, `hooks/answer-clear.py`, `hooks/git/pre-commit.py`, `hooks/git/reference-transaction.py`, `hooks/git/post-checkout.py`, `hooks/git/post-commit.py`
- the diffs of `hooks/commit-review-gate.py`, `hooks/dispatch.py`, `hooks/worktree-guard.py`, `hooks/worktree_consent.py`, `hooks/cmdline_base.py`, `hooks/implementer-notice.py`; `hooks/dispatch.py:115-175`; `hooks/session-lease.py:57-97`; `hooks/optin.py` (`repo_root`, `git_common_dir`, `home_at`, `opted_in`); `hooks/worktree-guard.py:664-689`, `:1603-1643`; `hooks/cmdline_base.py:2248-2270`
- the added text of `docs/commit-review-gate-spec.md` and `docs/worktree-guard-spec.md`, and `docs/commit-review-gate-spec.md:144-175`, `docs/worktree-guard-spec.md:685-699`
- the diffs of `skills/agent-contract/SKILL.md`, `agents/smith.md`, `CLAUDE.md`, `README.md`, `skills/implement/SKILL.md`, `templates/claude-md-block.md`
- `seal/ledger/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text.md`; the added rows of `seal/releases/*.md`
- the installed 0.16.0 plugin's `hooks/commit-review-gate.py` and `hooks/worktree-guard.py`, run as the comparison and not edited
