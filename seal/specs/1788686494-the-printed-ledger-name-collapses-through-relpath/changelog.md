- **The evidence check printed the name of a file it had not read.** Where a
  `--ledger` pattern crosses a symlink before a `..` — `--ledger
  'x/lnk/../ledger.md'`, with `x/lnk` pointing at `y` — the checker opened the
  file the pattern actually names and printed a header naming a different one.
  `os.path.relpath` folds `..` the way `normpath` does, by rewriting the
  string rather than by asking the filesystem, so it answered `x/ledger.md`:
  a real file, usually holding different rows. The exit code and the rows
  were right; the name a person reads and then goes and opens was wrong.

  A ledger path rendered for a person now goes through one helper that drops
  the root's own leading segments and touches nothing else about the
  spelling. Where a path is not under the root, it prints in full — longer
  than before, and naming the file that was read. That covers a local-mode
  root seen from a linked worktree, where the ledger genuinely sits outside
  the tree.

  **The issue named four places and there were five.** The fifth is the
  `--ledger narrowed this run` notice, which lists the ledgers a narrowed run
  did not read; it was missed because its variable is spelled differently
  from the other four. So the class was closed by following where a ledger
  path can reach rather than by searching for a name, and a test now
  recomputes that reach against the source on every run and refuses the old
  call anywhere in it. A sixth place added later is caught by that test as
  long as the ledger path gets there by one of the ordinary ways a value
  moves — assigned straight across, aliased, unpacked from a tuple, looped
  over, or handed to another function in this file.
  It is a guard against the edit somebody actually makes, not a proof that
  no such place can exist.

  What deliberately did not change: the suggestion list a broken row prints
  when its code looks to have moved. Those are scanned source files rather
  than ledgers, they are built downward from the repository root so they
  carry no `..` to fold, and they are normalised on purpose so they can be
  compared against the path a row spells. (#163)
