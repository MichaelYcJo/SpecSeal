### Fixed

- The worktree guard reads a command exactly as the release base read it
  (#689). The guard and the record of worktree consent take one answer from a
  command: the first segment of each kind, and the first directory in it that
  names a tree. Since #674 they shared the commit gate's wider reading, which
  finds more segments and more directories, and some commands put one that
  bash never ran the switch in first. `cd w; 2>/dev/null cd <missing>; git
  switch x` is one: bash switches in `w`, and the guard judged the session's
  own tree and said nothing. So did `2>/dev/null git switch x; cd w && git
  switch x`, where the first segment took the place of the second. Consent
  for a worktree created behind either was filed under the wrong clone.

  Both now read through a copy of the release base's command reader, frozen
  byte for byte. Over the 43,544 generated commands measured, the
  guard's decision, the kinds it recognised, the tree it judged and the clone
  consent was filed under are the release base's for every one. The commit
  gate is unchanged: over 5,092 commands no decision and no reason text
  differs.

  The cost, for the guard only: what #674 taught the commit gate to read is
  not read here. A `cd` with a redirection among its words (`2>/dev/null cd
  W`, `cd W 2>/dev/null`) does not move the tree the guard judges, and a git
  behind a redirection or zsh's `noglob`, `nocorrect`, `repeat N`, `for i
  (…)` or `foreach i (…)` is not a git command to it, as on the release base.
  The commit gate still reads both. #692, the redesign of how the gates learn
  where a command acts, decides the guard's reading again.
