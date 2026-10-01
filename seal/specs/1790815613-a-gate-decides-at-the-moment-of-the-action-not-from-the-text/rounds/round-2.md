# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — review round 2

| Field | Value |
|---|---|
| Target SHA | bd588eb0e3ce3d1c4e5b21b9f05ca296c970d81f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 705 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `b6d5bdb2af90a44a6d48b579ad9ae5df94b2f6f8..75577dc083e99e193264b734542aa06bcb73cdf5`, 6 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (the session variable removed by `NAME=`, `env -u` or `unset`) and 🟡 2 (`core.hooksPath` through `include.path` or `HOME=`, and `chmod -x` missing from the written limit). |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round at `bd588eb0`. Its diff is round 1's fix range `12c09ec3..e9977509`, plus the post-merge fix `12b35e31` and the two release merges `c3f3fef5` and `bd588eb0`, which no round had read. It was asked, for each of round 1's thirteen `fixed` verdicts, whether the finding and its class are closed, by re-running round 1's probes through the clone's own stubs. It was also asked whether a written known limit is true where a fix was text. It was asked to treat every unit in round 1's `New units` row, and the rider sentence `12b35e31` changed, as a finding surface. Finally, it was asked whether either merge changed what this branch's hooks do or say.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | Removing the session variable by `NAME=`, `env -u` or `unset` leaves the stub no session where no lease stands, and the reading stands aside; 0.16.0 stopped each | `hooks/tokens.py:55-87` | **fixed** `db4bcaea` | fixed at db4bcaea; executed n01–n03: landed, target silent, 0.16.0 deny; patched, all three deny; class of round 1's finding 8 |
| 🟡 2 | `git -c include.path=<file>` and `HOME=<dir>` reach `core.hooksPath` through a config file, and `chmod -x` on the stubs is not in the written limit; each lands unjudged | `hooks/tokens.py:63-87`, `docs/commit-review-gate-spec.md:189-194` | **fixed** `191bd420` | fixed at 191bd420; executed n04–n06: landed, target silent, 0.16.0 deny; patched, n04 and n05 deny; class of round 1's finding 2 |
| ⬜ 3 | The old spelling's limit says "byte-for-byte"; the match drops all but letters and digits and is a substring | `docs/commit-review-gate-spec.md:216-217`, `hooks/answers.py:147-181` | **fixed** `26d1bf58` | fixed at 26d1bf58; executed: a command carrying no token was given another open call's answer |
| ⬜ 4 | A person's commit with a lease starts three interpreters; the limit says two | `docs/commit-review-gate-spec.md:218-226` | **fixed** `de257dff` | fixed at de257dff; read: the `post-commit` stub has no narrowing line; c18 timing consistent |
| ⬜ 5 | A conflicted merge's conclusion is judged, including `git merge --continue` which 0.16.0 let through, and the policy names no merge | `docs/commit-review-gate-spec.md:112-143` | **fixed** `4f99a0ef` | fixed at 4f99a0ef; executed n07, n08 refused; the hook's `git` is the shell's process |
| 🟢 | round 1's blocking finding 1 is closed — a refused `worktree add -B` moves nothing | `hooks/worktree-guard.py`, `docs/worktree-guard-spec.md:376-398` | confirmed | executed p02: deny before git, tip unchanged, no tree; the deny text names no take-back |
| 🟢 | round 1's finding 2 is closed for its instances — `-c core.hooksPath`, `GIT_CONFIG*`; a removed stub is a written limit | `hooks/tokens.py#steps_around_hooks`, `docs/commit-review-gate-spec.md:189-194` | confirmed | executed c02, c03 deny, c06 silent and stated; the class is this round's finding 2 |
| 🟢 | round 1's finding 3 is closed — a stub git cannot execute is rewritten and decides nothing | `hooks/hook-install.py#write_stubs`, `hooks/githooks.py#decides` | confirmed | executed c07 |
| 🟢 | round 1's finding 4 is closed — `--no-checkout` and `--orphan` are denied before git | `hooks/worktree-guard.py` | confirmed | executed c22, c23 |
| 🟢 | round 1's finding 5 is closed — a Bash creation under `.claude/worktrees/` is denied and writes no record | `hooks/worktree-guard.py`, `hooks/worktree_consent.py` | confirmed | executed c21 |
| 🟢 | round 1's finding 6 is closed — `--lock` is denied before git | `hooks/worktree-guard.py` | confirmed | executed c24 |
| 🟢 | round 1's finding 7 is closed — the sequencer's own commits land, a typed one at a pause is refused | `hooks/commitgate.py#_sequencer_commit` | confirmed | executed c09, c12, c13 landed; c14 typed refused, alias landed as the limit states |
| 🟢 | round 1's finding 8 is closed for `env -i` | `hooks/tokens.py#steps_around_hooks` | confirmed | executed p01 deny; the class is this round's finding 1 |
| 🟢 | round 1's finding 9 is closed — an answer reaches only the call that carried it | `hooks/answers.py#given`, `hooks/hooksession.py#call_args` | confirmed | executed c25, and c25b under the harness's own shell |
| 🟢 | round 1's finding 10 is closed — an aborted commit's mark passes nothing | `hooks/commitgate.py#_key` | confirmed | executed c16 refused |
| 🟢 | round 1's finding 11 is closed — an empty lease directory starts no Python | `hooks/githooks.py:117-126` | confirmed | executed c18: 548 ms against 525 ms with no lease and 2,478 ms with a lease file |
| 🟢 | round 1's finding 12 is closed — contract §9 and §17 name the policy's four places | `skills/agent-contract/SKILL.md:241-251`, `:349-357` | confirmed | read against the policy's state table |
| 🟢 | round 1's finding 13 is closed — the installer's cost is stated and measured | `docs/commit-review-gate-spec.md:228-233` | confirmed | executed c19: 107 ms in-process median |
| 🟢 | the two release merges changed no hook of this branch, and the rider `12b35e31` wrote is true | `hooks/cmdline_base.py:1-22` | confirmed | executed: release files byte-identical, comment lines only; read: both importers |
| 🟢 | the ledger holds unscoped, and no merge dropped a correction | `seal/` | confirmed | executed: `bin/evidence-check .` exit 0, 3,469 ok, 0 drifted, 0 broken; `bin/correction-check` exit 0 |
| 🟢 | the six modules the fixes touched pass at the target | `tests/` | confirmed | executed: 268 passed, 62 skipped, exit 0 |
| ❓ | Whether a `systemMessage` from the installer reaches the model or only the person | `hooks/hook-install.py#main` | ❓ out of verified scope | carried from round 1; nothing here ran the harness's renderer; the orchestrator answers it |
| ❓ | Whether a command the person types with `!` is "a person's own commit" under P2 — it carries `CLAUDECODE` and is judged | `hooks/githooks.py:117-126` | ❓ out of verified scope | carried from round 1; the owner answers it |
| ❓ | M4's version floor and M5 | `overview.md` §*Not verified* | ❓ out of verified scope | carried; this round ran the stubs under a real `claude` ancestor and shell (c25, c25b), not under the harness's own Bash calls; the orchestrator answers it |

## Paste-ready fixes

```python
# hooks/tokens.py, steps_around_hooks: in the loop, after the hookspath test
        # The stub's P2 short-cut reads these two names, so a command that
        # empties, unsets or reassigns them leaves the stub no session where
        # no lease stands: `NAME= git commit`, `env -u NAME`, `unset NAME`
        # (round 2 of #692, executed). 0.16.0's reading stopped each.
        if "CLAUDECODE" in word or "CLAUDE_CODE_SESSION_ID" in word:
            return True
```
```python
# tests/test_the_commit_gate_decides_at_the_commit.py, STEPS_AROUND: add
    "an emptied session variable": (
        "CLAUDECODE= CLAUDE_CODE_SESSION_ID= git commit -m x"
    ),
    "env -u": "env -u CLAUDECODE -u CLAUDE_CODE_SESSION_ID git commit -m x",
    "unset": "unset CLAUDECODE CLAUDE_CODE_SESSION_ID; git commit -m x",
```
```markdown
[docs/commit-review-gate-spec.md, the stand-aside paragraph at :154-160 -- the list becomes]
`core.hooksPath` in any spelling (`-c`, `--config-env`, `git config`), a config
file that can carry it (`include.path`, `includeIf`, `HOME=`,
`XDG_CONFIG_HOME=`), any `GIT_CONFIG*` assignment, `env` emptying the
environment, a word naming `CLAUDECODE` or `CLAUDE_CODE_SESSION_ID`, and a
command that does not split.

[the same file, the state table's first row at :240]
| a clone carrying the stubs | `pre-commit`, then `reference-transaction` for one that skipped it; the PreToolUse reading as well for a command carrying one of the words `hooks/tokens.py#steps_around_hooks` reads |

[skills/agent-contract/SKILL.md §9 at :245-246 -- the parenthesis becomes]
words can keep the hooks from running (`core.hooksPath` or a config file that
can carry it, `GIT_CONFIG*`, `env -i`, the session variables).
```
```python
# hooks/tokens.py, steps_around_hooks: in the loop, beside the test above
        # A config file the command names can carry core.hooksPath where no
        # word does: `-c include.path=<file>`, an includeIf, and HOME or
        # XDG_CONFIG_HOME pointing git at another global config (round 2 of
        # #692, executed).
        low = word.lower()
        if "include.path" in low or "includeif." in low:
            return True
        name, eq, _ = word.lstrip("(").partition("=")
        if eq and name in ("HOME", "XDG_CONFIG_HOME"):
            return True
```
```python
# tests/test_the_commit_gate_decides_at_the_commit.py, STEPS_AROUND: add
    "include.path": "git -c include.path=/x/cfg commit -m x",
    "includeIf": "git -c includeIf.onbranch:main.path=/x/cfg commit -m x",
    "HOME": "HOME=/x/h git commit -m x",
    "XDG_CONFIG_HOME": "XDG_CONFIG_HOME=/x/c git commit -m x",
```
```markdown
[docs/commit-review-gate-spec.md, the known limit at :189-194, replaced]
- **A command that removes the stubs, or takes their execute bit, before it
  commits is judged by nobody.** `rm .git/hooks/pre-commit
  .git/hooks/reference-transaction && git commit`, and `chmod -x` on the same
  two files, step around both hooks, and the reading stood aside before the
  command ran, because nothing in its words names a hook setting. The
  installer puts the stubs and their mode back at the next Bash call. 0.16.0's
  reading stopped both (rounds 1 and 2 of #692, executed).
```
```markdown
[docs/commit-review-gate-spec.md :216-217, the last sentence replaced]
  belongs to its own command. The match drops everything but letters and
  digits and looks for the carried command inside the shell's argv, which is
  what lets the shell's own quoting through. So two agents running the same
  command are both waived, and so is a command that contains another open
  call's whole command that way.
```
```markdown
[docs/commit-review-gate-spec.md :225, the clause replaced]
  a person's commit pays three interpreter starts, `pre-commit`,
  `reference-transaction` at `prepared` and `post-commit`, so the stub can look
  for a `claude` ancestor:
```
```markdown
[docs/commit-review-gate-spec.md, the sequencer statement at :129-142, appended before its Enforced by: line at :143]
A conflicted merge is not one of them. `git merge --continue` runs its commit
in the process the shell started, so it is judged as a typed `git commit`
concluding the merge is, where 0.16.0's reading let `git merge --continue`
through (round 2 of #692, executed).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_creation_is_judged_before_git_runs.py`, `tests/test_the_commit_gate_decides_at_the_commit.py`, `tests/test_the_old_spellings_reach_the_hook.py`, `tests/test_the_hooks_are_installed_where_git_runs_them.py`, `tests/test_the_hook_surface_git_offers.py`, `tests/test_the_frozen_reading_never_grows.py`, in the round's clone | 268 passed, 62 skipped, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone | exit 0; 3,469 ok, 0 drifted, 0 broken |
| `bin/correction-check --range origin/release/v0.17.0...bd588eb0`, read-only against the worktree | exit 0; 2 merge commits examined, no marker dropped |
| `git diff 30ee491 bd588eb0` against the two release deltas, on `hooks`, `docs`, `skills/agent-contract` | release files byte-identical to `821e592d`; `hooks/cmdline_base.py` comment lines only |
| one temporary probe script driving real git 2.50.1 through the clone's stubs (installed by `hooks/hook-install.py` into scratch repositories), cases c01–c26, p01, p02, n01–n08; each command's payload through the target's and the installed 0.16.0's `commit-review-gate.py`, and creations through the target's `dispatch.py pre-bash` and 0.16.0's `worktree-guard.py` | as reported per finding; c05 and c08 (`commit-tree`, `am`) landed, as the written limit says; c26's heredoc token is read, as 0.16.0 read it |
| the proposed `steps_around_hooks` lines patched into the clone, n01–n06 re-run, and 52 selected cases of the two touched modules | n01–n05 deny, n06 silent; 52 passed; the patch reverted |
| a pre-commit hook printing its ancestry under `git merge --continue`, in a scratch repository | the hook's parent `git` has the starting process for its parent |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — none of the three was run here; it is the sealer's, and it comes due once 🟡 1 and 🟡 2 are answered |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/creationgate.py:118-126`, `:161-169`, `:271-281` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/commit-review-gate.py:1344-1347`, `docs/commit-review-gate-spec.md:144-161` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/hook-install.py:116-122`, `hooks/githooks.py:237-241` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/worktree-guard.py:1629`, `docs/worktree-guard-spec.md:386` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/creationgate.py:109-115`, `:271-277` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/creationgate.py:125`, `:155-156` | round 1's 🟡 6 — fixed |
| round-1 | `hooks/commitgate.py:179-199`, `hooks/githooks.py:37-42`, `docs/commit-review-gate-spec.md:106-118` | round 1's 🟡 7 — fixed |
| round-1 | `hooks/hooksession.py:102-111`, `hooks/githooks.py:109-118` | round 1's 🟡 8 — fixed |
| round-1 | `hooks/answers.py:76-109`, `hooks/answer-write.py:28` | round 1's 🟡 9 — fixed |
| round-1 | `hooks/commitgate.py:77-79`, `:107-118` | round 1's 🟡 10 — fixed |
| round-1 | `hooks/githooks.py:109-118`, `docs/commit-review-gate-spec.md:156-159` | round 1's 🟡 11 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:241`, `:345` | round 1's ⬜ 12 — fixed |
| round-1 | `hooks/hook-install.py:145-181` | round 1's ⬜ 13 — fixed |
| round-1 | `hooks/cmdline_base.py`, `hooks/worktree-guard.py:1629` | round 1's 🟢 — confirmed |
| round-1 | `seal/` | round 1's 🟢 — confirmed |
| round-1 | `hooks/commitgate.py:129-199` | round 1's 🟢 — confirmed |
| round-1 | `hooks/hooksession.py:102-111` | round 1's 🟢 — confirmed |
| round-1 | `hooks/hook-install.py:184-195` | round 1's ❓ — out of verified scope |
| round-1 | `hooks/githooks.py:109-118` | round 1's ❓ — out of verified scope |
| round-1 | `overview.md` §*Not verified* | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
