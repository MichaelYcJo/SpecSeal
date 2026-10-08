### Changed

- **The hooks read the session, a waiver and a creation one way each, and
  a brace expansion in a git command is a shape the worktree guard does not
  recognise (#868, #856).** Four facts every gate depends on were read in
  more than one place, and the readings disagreed. Each now has one reader.

  1. Where a worktree creation lands. The consent writer files a creation
     under the clone the worktree guard judged, by the guard's own
     placement. It used to take the first directory it could compute, so
     `eval x ; cd A || git worktree add …` was filed under `A`, the branch
     bash skips, and `cd <missing> ; git worktree add …` filed nothing.
  2. Which process is the session. The lease writer, the commit gate's
     lease route and the guard's count of other sessions test a process by
     one rule, its basename is `claude`, and read `CLAUDE_PID` first where
     the harness exports it. The lease writer used to accept any name
     holding `claude`, so it could record a lease no reader matched. The
     git hook stubs test one session variable, `CLAUDE_CODE_SESSION_ID`;
     they also tested `CLAUDECODE`, which nothing behind them read.
  3. Whether a waiver token was typed. The commit gate, the worktree guard
     and the old spelling handed to the git hooks read `[no-review]`,
     `[no-parity]`, `[worktree-ok]` and `[shared-tree-ok]` through one
     reader, which reads the words before a quote that never closes and
     none inside it.
  4. What a failed git call means. The commit gate's two readings run git
     through one runner, which tells an empty answer from a failure.

  What a person meets:

  - A `[no-review]` inside a quote that never closes, or after an
    apostrophe in its comment (`# don't [no-review]`), waives nothing. The
    commit gate used to read it as a substring. The stop names the waiver
    typed in front, `: '[no-review]'; git commit …`. Over the 32,431
    recorded command and directory pairs, one pair's waiver moves.
  - A token written before an apostrophe in its comment (`# [shared-tree-ok]
    the release's own tree`) is still read, by every gate.
  - In a repository declaring `seal/parity.md`, a commit whose `git diff`
    fails meets the parity question, where it was let through as a change
    confined to `docs/` and `seal/`. That includes `git commit -a` or a
    pathspec on a branch with no commit yet.
  - `git rebase {main,feature/x}`, `git rebase --ro{,} feature/x`, `git
    stash {branch,} x` and `git worktree {add,} ../wt f` stop where the tree
    matters, like every unrecognised shape, with the words written out as
    the plain spelling. bash expands the braces before git reads them, and
    the two rebases and the stash switch the branch. So does a brace that
    makes the word `git` itself, `{git,} switch x`. A quoted brace (`git
    commit -m '{a,b}'`) changes nothing, and neither does a brace in a word
    that only contains the letters, `cat {.gitignore,README.md}`. No
    recorded pair holds a git word
    with an unquoted brace expansion, so the stop costs no recorded command.
  - The git hook stubs' bytes change by one variable name, so the installer
    rewrites every opted-in clone's three stubs at the next session, as it
    does when the plugin moves.
