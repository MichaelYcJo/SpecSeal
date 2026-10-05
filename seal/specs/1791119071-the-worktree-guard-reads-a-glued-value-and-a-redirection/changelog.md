### Fixed

- The worktree guard now asks about a branch switch however its options are
  spelled, and wherever a redirection stands among its words (#764, #738).
  Before, it recognised a creating option only as a separate short word
  (`-b NAME`, `-c NAME`), so `git checkout -bNAME`, `git checkout -qb NAME`,
  `git checkout --orphan=NAME` and `git switch --cre NAME` created a branch
  and switched to it over a dirty or shared tree without a word. It also
  read a redirection as part of the branch name, so `git checkout
  feature/x>/dev/null` and `git checkout 2>/dev/null feature/x` switched
  unasked. The guard now reads a `checkout`'s and a `switch`'s words the way
  git does once bash has taken the redirections off: a creating option counts
  in every spelling git accepts, an option's value is not read as a name, and
  a redirection is no word. A file restore keeps its silence, because the
  guard still checks the name against the tree (`git checkout
  README.md>/dev/null` restores and is not asked). The guard now goes quiet
  only where git switches nothing: a `-b` written after `--`, which git takes
  as a file name, and an option's value where a name would stand. A bare
  `--` after the name (`git checkout NAME --`) switches in git and is asked;
  a `--` with a path after it stays a restore.
  `docs/worktree-guard-spec.md` says which rule is now read past the frozen
  0.16.0 reading, on the owner's answer, and §*Known limits* names what is
  left: a static table of options a later git may outgrow, a quoted `>` in a
  name, and a switch behind `2>&1`, which is still asked without a tree.
