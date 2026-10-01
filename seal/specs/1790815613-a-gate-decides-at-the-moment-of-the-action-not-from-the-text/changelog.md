- **A commit and a worktree creation are judged inside git, where they
  happen, and not from a reading of the command (#692).** The commit gate
  used to predict from the Bash command's text where a shell would run the
  commit, and milestone 49 found one more shell shape at every round. In the
  recorded run that cost 15 prompts and 102 minutes of waiting, 13 of them
  for commits into a declared worktree that the reading placed in the main
  checkout. Now `pre-commit` judges the commit in the worktree it lands in,
  with the same two arms, marks and routing declaration. `post-checkout`
  records a worktree creation git made in the clone it belongs to, and takes
  back the first creation of an attended session that nobody answered for,
  as the worktree guard's ladder says. No `cd`, redirection, loop variable
  or `eval` moves either one around the judgment. Over 413 commands of the
  milestone's corpora, every real commit the release base stopped is still
  stopped, 37–44 it missed now are, and the stops on commands that committed
  nothing are gone.

  **What a session meets.** A stop is git refusing the commit with the ways
  on in the command's output, the same text on every attempt. Attended, it
  tells the model to ask the person with AskUserQuestion. Under the
  `automation` press it asks nobody. `git -c specseal.waive=review commit …`
  is the waiver in git's own spelling, and the old `: '[no-review]'; git
  commit …` and `# [worktree-ok]` keep working. `--no-verify` is met where
  the branch moves, and nothing but a `git commit` is. A person's own commit
  at their own terminal, with no Claude session behind it, is not judged.

  **What stays a reading of the command.** A branch switch: no git refuses
  one before its tree has moved, so the guard keeps the 0.16.0 reading for
  it on every git, pinned so it cannot gain a rule. And every arm in a clone
  whose git hooks slot is somebody else's, which keeps 0.16.0's behaviour.

  **Operational.** SpecSeal now writes four small stub files —
  `pre-commit`, `reference-transaction`, `post-checkout`, `post-commit` —
  into the common `.git/hooks/` of every opted-in clone a session reaches,
  and says so once. Each carries the line `# specseal-git-hook <version>`
  and the installed plugin's path, and does nothing once the plugin is
  removed. A clone with `core.hooksPath` set, or a hook file without that
  line, gets nothing, and the session is told once. A judged commit pays
  one or two Python starts, about 200–400 ms on the machine measured, and a
  fetch, a merge and a person's own commit pay none.
