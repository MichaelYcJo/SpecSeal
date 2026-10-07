### Fixed

- **The worktree guard reads two more spellings of a `git rebase` that
  switches branches (#854).** git stops reading a rebase's options at
  `--end-of-options` as well as at `--`, and it takes `--ro` and `--roo` as
  `--root`. So `git rebase --ro feature/x` and `git rebase --end-of-options
  main -x` each switch to the named branch before they rebase, and the
  guard used to let both through without a word, even in a tree another
  session was working in. Both now stop where a switch would matter, with
  the advice to run `git switch <branch>` first. So does `git rebase
  --root>/dev/null feature/x`, where the redirection used to hide `--root`.
  A rebase of the branch HEAD is on still passes, and so does one carrying
  `--rebase-merges` or another option that takes no value.

  The guard's policy now says two more things a person meets. A stop that
  describes one tree calls it "this tree", even when it is not the tree the
  session types from. And `cd w 2>&1 && git switch x`, or a git cut at an
  `&` inside an `if` body after `cd w`, is judged in the session's own
  tree rather than in `w`.
