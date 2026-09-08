<!-- specs/1788846800-an-exited-session-reads-as-live-for-five-minutes -->

### Fixed

- **Ending a session made the tree look busy for the next five minutes.** The
  worktree guard has one last check for a session it cannot see as a process —
  a VS Code extension panel, say, which writes this project's files without
  running anything called `claude`. It looked for a recently written session
  file and, finding one, reported someone at work. A session that has just
  *closed* leaves exactly the same trace, and nothing told the two apart, so
  for five minutes after every session in the project ended the guard refused
  branch switches and pushed the work into a worktree nobody needed. The guard
  already knew better one step earlier: sessions leave a note recording which
  process owns them, and that note had already been checked and correctly
  thrown away as belonging to a session that was gone. The recently written
  file then put it straight back. Those notes are now believed on both paths.
  The extension-panel case is unaffected — a live one still owns its note —
  and a session that cannot be checked at all still counts as working, so
  nothing new is ever waved through.

- **Batching commands into one call cost a confirmation the previous release
  had removed.** Since 0.9.1 the first worktree a session creates takes one
  confirmation and the rest take none — but only for a command that creates a
  worktree and does nothing else. Adding a pipe, or a `cd` in front, brought
  the confirmation back, which meant the repository's own instruction to batch
  independent commands into one call was what triggered it. On the 0.9.2
  release run that cost two stops out of five worktrees created. The guard now
  stays quiet for these instead of asking again: it has already had its answer
  about the worktree, and the rest of the command line is judged by your own
  permission settings, exactly as it would be if the guard were not installed.
  Nothing new is permitted — a `sudo` in the command is still judged by the
  rule you wrote for `sudo` — and the first worktree of a session is still a
  question.

### Changed

- The argument for why the guard stays quiet rather than asking again now sits
  with the code that acts on it, instead of only beside one of the two places
  that call it — the one a reader following the other path would never open.
