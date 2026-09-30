### Fixed

- The worktree guard judges the tree the release base judged, whatever order
  the commit gate's wider reading puts a command's directories in (#689). The
  guard and the record of worktree consent take one directory per command
  segment, the first that names a tree. Since #674 that directory came from a
  list holding both the release base's reading and the new one, and some
  chains put a directory bash never ran the command in at the front of it.
  `cd w; 2>/dev/null cd <missing>; git switch x` is one: bash switches in
  `w`, and the guard judged the session's own tree and said nothing. So did a
  long chain of failing `cd`s ending in `cd <missing> || git switch x`, and
  consent for a worktree created behind either was filed under the wrong
  clone.

  Both now read the release base's directories alone. Over 32,893 generated
  commands their answer equals the release base's for every one they both
  read as git. The commit gate is unchanged: over 5,092 commands no decision
  and no reason text differs.

  What this gives back: a `cd` with a redirection among its words
  (`2>/dev/null cd W`, `cd W 2>/dev/null`) no longer moves the tree the guard
  judges, as on the release base. The commit gate still judges W.
