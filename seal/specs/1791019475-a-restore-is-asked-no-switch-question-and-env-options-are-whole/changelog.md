### Fixed

- The worktree guard no longer asks "This command switches a branch" about a
  restore of `.` or of a path after `--`, or a detach, that carries a
  redirection, such as `git checkout . &>/dev/null`,
  `git checkout -q &>/dev/null` or `git switch --detach>/dev/null` (#737).
  The question added for #678 read the redirection's word as a branch name.
  It now reads each command as git is handed it, with every redirection
  taken off. It still reads no tree, so a checkout of a file whose
  `checkout` a redirection hides from the guard's own reading
  (`git checkout &>/dev/null README.md`) is still asked, as it was before
  this change. It now also asks about a
  worktree creation with a redirection between `worktree` and `add`
  (`git worktree 2>/dev/null add ../wt b`), which bash runs as a creation. As
  before, a creation is silent under consent. Counted over the 27,351
  distinct command and directory pairs recorded in this repository's
  transcripts, the question still stops none.

- The commit gate finds a commit behind `env` options it used to misread
  (#737). Examples are `env -i-S '…'`, `env --S '…'`,
  `env --unset -iS '…'` and `env --env0-from f -iS '…'`. macOS `env` reads
  `-` as a letter and a word starting `--` as a cluster of letters. GNU's
  `env` has `--env0-from` and, unreleased, `--quoting-style`, and each takes
  a value. `env`'s options are now read both ways, and every string either
  reading finds is judged, so the gate stops on every spelling either `env`
  runs. A prefix of `--env0-from` or `--quoting-style` now takes the next
  word as its value, as GNU reads it, so a string behind one is no longer
  read where no `env` runs it. `genv` is read as GNU's alone.
