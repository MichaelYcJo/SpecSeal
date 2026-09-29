### Fixed

- The commit gate reads the rest of what a shell runs (#674). A commit behind
  a redirection (`2>/dev/null git commit`, `git 2>/dev/null commit`, `2>&1 git
  commit`), a subshell with its host glued to the `(` (`(sh -c 'git
  commit')`), and a string a host runs past a redirection after its flag
  (`bash -c 2>/dev/null "$CMD"`) each reached the gate as no commit at all,
  and bash landed every one it was given. So did `watch` inside a `case` arm,
  a function body or a coprocess, and `2>/dev/null cd W && git commit`, whose
  commit the gate judged where the shell started.

  Each is now read where the shell reads it. A redirection in front of the
  program, glued or spaced, is read past. One the command splitter cuts at `&`
  or `|` (`2>&1`, `>&2`, `>|f`) is glued back and read beside the pieces.
  `watch` and a host string's command word are read by position inside a
  compound command's header. `flock -c` is read as a host, and `parallel`'s
  arguments are read for a commit. `sudo -s` and `sudo -i` are not hosts:
  sudo escapes their command into a single word before the shell sees it. A
  body nested inside another is read 32 levels deep and then counts as one
  that might commit. That shortens the answer for a pathological nesting from
  up to a minute to a few seconds, and it stays the same stop. A compound
  command's headers are read 32 deep in the same way.

  A redirection glued to the end of a word (`git>/dev/null commit`,
  `cd>/dev/null W`) is read as well, as are zsh's `noglob`, `nocorrect`,
  `repeat N` and `for i (…) cmd`, a `cd` behind a redirection the splitter
  cut (`2>&1 cd W`), and a shell's string past `--` or an option after a
  redirection (`bash -c 2>/dev/null -- "$CMD"`). bash or zsh committed for
  each. A `cd` with a redirection after its operand (`cd W 2>/dev/null && git
  commit`) now lands in W too. It was silent from a directory that is not
  opted in and under `[no-review]`, and the worktree guard judged the
  session's own tree for a switch made in W.

  The change only adds stops. Every reader asks what it asked before and adds
  to it. A long chain of `cd` segments, such as nine `2>/dev/null cd W;` in a
  row, reaches the walk's cap of 64 directories sooner than on the release
  base, so the walk keeps the release base's directories apart and the cap
  collapses only the new ones. Where a redirection hides a `cd`, the
  directory the shell may have reached is added as unreadable beside the one the release base judged, and
  never replaces it. A generated corpus of 11,393 commands found none that the
  release base stopped and this one lets through. Among the 6,033 commands
  recorded in the milestone's runs, none changes its verdict. A string's
  command word behind a runner's own options now counts when it expands
  (`sh -c 'timeout 5 wc -l "$1"'` stops), because the reader cannot tell an
  option's value from the program. The worktree guard shares the redirection
  reading, so `2>/dev/null git worktree add` now meets it too.
