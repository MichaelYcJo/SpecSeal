### Fixed

- A waiver token inside a here-document body no longer waives the commit
  gate (#773). A waiver is typed in front of a command, and a body is text the
  command only carries: a file's contents, or a Python program read from
  stdin. Both places that read the token used to read the bodies too. One is
  the gate's own reading, and the other passes the token to the git hook. So
  a token that a command only carried as data could let an unreviewed commit
  into a repository that declares no work item. Both now read the command
  with its bodies taken out and its comments kept. The bodies are the ones
  the gate already finds, so no new parsing was added. A token counts only
  where the command as written carries it as well, so the change can refuse
  a waiver and never grant one.
- One stop is new. A token typed inside a body that a shell runs, in front of
  a commit the body runs, no longer waives that commit, which now gets the
  verdict it would get with no token. Type the token in front of the Bash
  call's own command instead, outside the body, where it waives as before.
  The documented forms are unchanged: the no-op in front of the command, and
  the token in a comment.
