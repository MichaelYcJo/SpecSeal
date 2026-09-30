### Fixed

- Past the walk's cap, the worktree guard judges the tree the release base
  judged again, and the consent writer files a creation where it did (#689).
  A command long enough to collapse the walk, followed by `cd <dir> || git
  switch`, gave the walk a readable directory only on the branch the `||`
  skips. That directory led, so the guard read the collapsed walk's
  unreadable directory as the session's own clean tree and was silent on a
  switch into a dirty one, and the consent writer filed the creation under
  the skipped `cd` target. The walk now leads only where the first directory
  it gives, the shell the segment runs in, is one it can name and a directory
  that exists. The second half closes `cd w; 2>/dev/null cd <missing>; git
  switch`, where the `cd` behind the redirection fails, bash switches in the
  dirty `w`, and the guard had judged the missing path and fallen back to the
  session's own clean tree, with or without a long command. The same cause
  had filed `cd w; 2>/dev/null cd nosuch || (cd O) && git worktree add` under
  `w/nosuch` with no cap reached, and that is closed too. A `cd` read past its
  redirections into a directory that exists still leads past the cap. The
  commit gate's verdicts do not
  move. Where the walk's first directory is unreadable, the gate's deny now
  lists the base's directories ahead of the walk's.
