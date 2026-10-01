- **A commit is judged inside git, where it happens, and not from a reading
  of the command (#692).** The commit gate used to predict from the Bash
  command's text where a shell would run the commit, and milestone 49 found
  one more shell shape at every round. In the recorded run that cost 15
  prompts and 102 minutes of waiting, 13 of them for commits into a declared
  worktree that the reading placed in the main checkout. Now `pre-commit`
  judges the commit in the worktree it lands in, with the same two arms,
  marks and routing declaration. No `cd`, redirection, loop variable or
  `eval` moves a commit around the judgment. Over 413 commands of the
  milestone's corpora, every real commit the release base stopped is still
  stopped, 37–44 it missed now are, and the stops on commands that committed
  nothing are gone. That convergence is claimed for commits alone.

  **What a session meets.** A stop is git refusing the commit with the ways
  on in the command's output, the same text on every attempt. Attended, it
  tells the model to ask the person with AskUserQuestion. Under the
  `automation` press it asks nobody. `git -c specseal.waive=review commit …`
  is the waiver in git's own spelling, and the old `: '[no-review]'; git
  commit …` keeps working for the one Bash call that carries it, and for no
  other agent's call in the same session. A command that sets `core.hooksPath` or a
  `GIT_CONFIG*` variable, or empties its environment with `env -i`, is
  still judged before it runs, because those can keep git's hooks from
  judging it. `--no-verify` is met where the branch moves, and nothing but a
  `git commit` is. The commit git makes itself to finish a rebase,
  cherry-pick or revert that stopped on a conflict, or a reword, is not
  judged, as 0.16.0 did not judge `git rebase --continue`; a commit typed
  while one is paused is. A person's own commit at their own terminal, with
  no Claude session behind it, is not judged.

  **What stays a reading of the command.** A branch switch and a worktree
  creation. No git refuses a switch before its tree has moved, and a hook
  that runs after a creation can only take it back, which cannot undo what
  `worktree add -B`, `--no-checkout`, `--orphan` or `--lock` already did. So
  the worktree guard keeps the 0.16.0 reading for both on every git, pinned
  so it cannot gain a rule, and `# [worktree-ok]` works as it did. And the
  commit gate in a clone whose git hooks slot is somebody else's, which
  keeps 0.16.0's behaviour.

  **Operational.** SpecSeal now writes three small stub files —
  `pre-commit`, `reference-transaction`, `post-commit` — into the common
  `.git/hooks/` of every opted-in clone a session reaches,
  and says so once. Each carries the line `# specseal-git-hook <version>`
  and the installed plugin's path, and does nothing once the plugin is
  removed. A clone with `core.hooksPath` set, or a hook file without that
  line, gets nothing, and the session is told once. A judged commit pays
  one or two Python starts, about 200–400 ms on the machine measured, and a
  fetch and a merge pay none. A person's own commit pays none in a clone
  where no session has worked in the last day; in one where a session has,
  it pays the two starts and is still not judged.
