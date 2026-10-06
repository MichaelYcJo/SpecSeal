### Changed

- **The worktree guard stops predicting a branch switch from a command's
  text, and stops on what it does not recognise instead (#826).** It reads
  each git command as one of three shapes. A subcommand on its list — the
  ones this repository's recorded runs hold that leave the branch where it
  is, each with its count, in `LEAVES_THE_TREE` in
  `hooks/worktree-guard.py` — is silent everywhere and spawns no git, and so
  is `git checkout -- <path>`. `git switch` meets the branch-switch rules as
  before. Everything else is unrecognised: a `git checkout` with no `--
  <path>`, a subcommand not on the list, and git in a shell's string, in a
  `$( … )` body, behind a redirection or a zsh word, or in a command that
  would not split. An unrecognised shape stops only in a tree where a
  switch would matter — another session there, detection unusable, or
  uncommitted tracked changes — and says nothing in a clean tree nobody
  else is in. The stop quotes each shape and its plain spelling (`git
  switch <branch>`, `git checkout -- <path>`, the command run on its own).
  Where the person pressed `automation` it is a `deny` to the model, which
  rewrites and retries, and nobody is asked; otherwise it is an `ask`,
  except in a tree another session is actively working in, where it is a
  `deny` either way.

  What a person meets: `git checkout <branch>` in a dirty tree now stops
  with *write `git switch <branch>`* instead of asking about the changes,
  and `git checkout README.md` stops the same way where it used to pass as
  a restore. A git subcommand this repository never ran — `git submodule
  update`, `git notes` — stops in such a tree until a release adds it to the
  list. On Windows, where the guard can never count the other sessions,
  every unrecognised shape stops in every tree. Over the 31,193 distinct
  command and directory pairs this repository recorded before 2026-10-03,
  the guard stops 315 by shape, tree-blind, 55 of them pairs it did not
  stop before, and it lets through none it stopped.

  The four readings the guard grew on the old question leave with it: the
  option table, the name lookups and guesses, and candidate C's question
  about a git only the commit gate's reading finds. This closes #732, a git
  command inside a string handed to a shell, which is now an unrecognised
  shape, and #734, a creation only a redirection hid, whose consent was
  read against the wrong clone: the stop reads no consent record at all.
