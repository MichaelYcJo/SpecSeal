### Fixed

- The worktree guard no longer reads a redirection's word as a branch name
  (#737). The question added for #678 did, so a command whose words name
  nothing a switch could take, such as `git checkout . &>/dev/null`, was
  asked "This command switches a branch". It now reads each command as git
  is handed it, with every redirection taken off, and asks wherever those
  words hold a switch or a creation that the guard's own reading of the
  command as written misses. It reads no tree, so a restore or a detach
  whose words read as a switch is asked as one, such as
  `git checkout &>/dev/null README.md`. It now also asks about a
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
  word as its value, as GNU reads it, so an abbreviated split string behind
  one (`env --quoti --spl '…'`) is no longer read where no `env` runs it.
  `-S` and `--split-string` spelt in full are still read wherever they
  stand, as before, so `env --e -S '…'` is read although no `env` runs
  that string. `genv` is read as GNU's alone.
