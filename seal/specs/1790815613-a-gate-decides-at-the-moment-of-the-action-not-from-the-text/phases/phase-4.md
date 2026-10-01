# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 99ecd923 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

Build creation consent and the creation ladder at git, against real git.
`post-checkout` writes the record in the clone the worktree belongs to,
keyed by session (S7). The creation is refused at `reference-transaction
prepared` where M3 says the new `HEAD` is a transaction, and otherwise by
the post-hoc path P4 settles (S8). The Agent/Task arm is kept or retired by
M5. The token translator for `[worktree-ok]` and `git -c
specseal.answer=worktree-ok` (P3, W6). `creation_directory` deleted.
`hooks/worktree-guard.py`'s creation arm reads the hook's tree.

## What this phase found

- **The ladder decides in `post-checkout`, after the fact.** M13 found
  nothing at `prepared` that tells a creation from a switch, and M14 found
  that `post-checkout` can take a fresh worktree back. A refusal therefore
  runs `git worktree remove --force` on the new tree and exits 1, and
  `worktree add` reports failure. The tree is gone, and a `-b` branch
  stays, which the text names along with `git branch -D <branch>`. It is
  S8's "post-hoc equivalent".
- **Counted in the tree the creation ran from.** `post-checkout`'s parent is
  `git worktree add`, whose working directory is the toplevel it ran in, so
  `proc_cwd(getppid())` names it. That reading uses `/proc` on Linux and
  `lsof` on macOS, the guard's own `proc_cwd`. Where it cannot be read, the
  clone's main tree stands in. Opt-in, consent and the session count are all
  read for that tree.
- **Consent is the guard's rows, with no `ask`.** The record or the press
  keeps the creation and writes the record. So does the person's answer, as
  `git -c specseal.answer=worktree-ok` or the old `# [worktree-ok]` carried
  by `hooks/answers.py`. Without one, the ladder's reason for its row
  (another active session, only idle ones, cannot tell, single-stream)
  tells the model to put the question with AskUserQuestion. The token that
  comes back is the answer.
  - **What changed:** the guard answered that token with an `ask` the person
    clicked. A git hook has none, so the person's confirmation now arrives
    through the model, the trade W2 states for the commit gate.
  - **What stayed:** `S8`'s sequence. Attended is refuse, then answer, then
    allow, allow, allow, allow; an automation run pays nothing.
- **`-c` reaches the hook through `GIT_CONFIG_PARAMETERS`,** so the helper
  that strips git's variables before running git from the hook keeps the
  `GIT_CONFIG*` family. A mutant that dropped it went red.
- **A worktree under `.claude/worktrees/` is never taken back.** Whether the
  Agent tool's isolation runs `git worktree add` is M5, which nobody here
  could measure. If it does, the person already answered the guard's Agent
  arm, and a refusal would fail an approved spawn. So M5 does not decide
  anything in this phase. The Agent/Task arm stays as it was, and so does
  `hooks/worktree_consent.py`'s PostToolUse Agent arm.
- **Both text paths stand aside where git decides,** and for the consent
  writer that is a correctness fix, not tidiness. In a git-decided clone a
  command that ran may have had its creation taken back by the hook, and a
  record written from the command would be consent nobody gave.
  `test_the_guard_and_the_consent_writer_stand_aside_where_git_decides`
  pins both. In a foreign clone both judge as 0.16.0 did (P5).
  `creation_directory` stays for that reason.
- **S7 against bash.** 14 shapes of a creation that ran each leave the
  record. They include a `cd` behind a redirection, `builtin cd`, `time cd`,
  `pushd`, a loop variable, `eval`, and #686's `eval true; … cd … ||` with
  a `cd` that fails. 4 shapes that never ran leave none: `false &&`, an
  `echo`, a heredoc body, and a function never called.
- **Mutation testing: 22 mutants, all red after three cases were added.**
  Two of the survivors were the stub's `sh` lines shadowing the Python
  checks, and they are now pinned in-process. The third was the origin
  tree, which only an attended refusal from a linked worktree shows.
- **Executed on four gits.** The phase 2, 3 and 4 modules, the S2 corpus
  included, pass on 2.34.1 and 2.39.5 (255 passed, 57 skipped, Linux, run
  as root) and on 2.50.1 (macOS). On 2.43.0 they pass with the corpus
  deselected (110 passed).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the guard's creation arm and `creation_directory` stay as the foreign clone's fallback (P5); each stands aside where git decides | none |
