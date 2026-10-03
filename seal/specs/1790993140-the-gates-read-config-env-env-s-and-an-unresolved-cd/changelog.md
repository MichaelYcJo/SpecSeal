### Fixed

- The commit gate finds two commits it used to read as none (#716). A
  global option written with its value as a separate word,
  `git --config-env core.hooksPath=VAR commit`, read its value as the
  subcommand; `--config-env`, `--attr-source` and `--shallow-file` now take
  their value as git 2.54.0 does, beside `-C`, `-c`, `--git-dir`,
  `--work-tree` and `--namespace`. `env -S '-i git commit'` read the split
  string alone, as a command whose word is `-i`; `env` splits that string
  into its own arguments, so the string is now also read as
  `env -i git commit`, in every spelling of the option and for `genv`. Both
  readings only add, so the gate stops more and never less. Neither shape is
  plain, so the reading judges it even where git's own hooks run.

### Changed

- The worktree guard asks about a branch switch or a worktree creation that
  only the commit gate's reading finds, instead of passing it silently
  (#678). That covers a git behind a redirection (`2>/dev/null git switch
  x`, `git 2>&1 worktree add …`), behind zsh's `noglob`, `nocorrect`,
  `repeat N`, `for i (…)` or `foreach i (…)`, or after a spaced
  `--config-env`. It asks only where it was about to say nothing, so every
  deny, choice and ask it already gave still comes first, and a creation is
  silent under consent, as before, so an `automation` run is not asked.
  Counted before it was wired over the 27,351 distinct command and directory
  pairs recorded in this repository's transcripts: it would have stopped
  none.

- A switch whose tree the guard cannot place stays judged against the
  session's own tree, and is now a named limit in the guard's
  specification (#686). `builtin cd w`, `pushd w`, `noglob cd w`,
  `cd "$W"` with `W` unset and `2>&1 cd w` before a `git switch` are
  examples. Asking there was built and counted under the owner's rule of
  2026-10-03: it would have stopped 9 of the same 27,351 pairs, so it was
  removed. `git -C <dir> switch …` is the spelling the guard reads.
