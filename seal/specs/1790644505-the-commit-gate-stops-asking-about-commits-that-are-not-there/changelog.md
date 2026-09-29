### Fixed

- The commit gate no longer puts a permission prompt in front of a person who
  pressed `automation` on the routing question (#662, #665). That preset
  promises the run will not stop to ask, and one measured run still stopped
  four times: the gate refuses once per session per repository and then asks,
  every agent in a run shares the session, and the first refusal had already
  been spent. In such a session every stop is now a refusal addressed to the
  model, in both arms and for a repository the gate could not read, and its
  text names the ways on that need nobody: re-issue the commit as `git -C
  <absolute path> commit` in a command of its own, or after a `cd` joined by
  `&&` alone; make file edits through the `Edit` and `Write` tools; the waiver
  only for a commit no work item owns; otherwise hand the commit back. The
  press changes nothing about what the gate stops, so no commit it used to
  judge now passes unjudged. The press is read from the session's transcript
  with the reader the worktree guard already uses, and every way of not
  reading it is the old behaviour. An attended session, and a `per axis` run,
  meet the same prompts as before.
- The commit gate judges a commit written after a reserved word on the same
  line (#669). `for d in a; do git commit -m x; done`, `while …; do git commit
  …; done` and `if true; then git commit …; fi` reached it as no commit at
  all, because the shell splits them at `;` and the commit arrived behind `do`
  or `then`; the same commands written across lines were always judged. After
  `do`, `then`, `else`, `elif`, `if`, `while`, `until` or `{` the next word is
  now the command word, and the commit is stopped as one whose repository
  cannot be read, as its multi-line spelling always was. Inside a `case` arm,
  a function body or a coprocess, the first `git` word stands in for the
  command word. The change only adds stops: nothing the gate used to read as a
  commit reads differently. The worktree guard shares the reading, so a
  branch switch or a worktree creation in a loop body is now read by it too.
- The commit gate judges a commit behind a program that runs its arguments,
  inside a string handed to a shell, or inside a command substitution (#670).
  `exec git commit`, `nice git commit`, `timeout 5 git commit`, `xargs git
  commit`, `sh -c 'git commit'` and `echo $(git commit)` reached it as no
  commit at all, while `env git commit` was judged. The reader now knows the
  programs that run their operands as a command — POSIX's, GNU coreutils' and
  their `g`-prefixed macOS names, util-linux's, `sudo`, `doas` and `pkexec`,
  the tracers, `find`, `parallel`, `watch` and `script` — and reads past
  them; behind their own options it stops rather than guess where they run.
  A string `sh -c`, `bash -c`, `su -c`, `script -c`, `env -S` or `watch`
  hands to a shell is read as `eval`'s argument already was, and the body of
  a `$( … )`, backticks, `<( … )` or `>( … )` is read as a heredoc body is. A
  commit found in either stops as one whose repository cannot be read. The
  change only adds stops. A program whose arguments are a script or a remote
  command — `bash run.sh`, `make`, `uv run`, `ssh` — is still not read. The
  worktree guard shares the wrapper reading, so `nice git worktree add` now
  meets it too.

### Added

- Contract §17: an agent commits with the repository's absolute path after
  `git -C`, in a command of its own, and joins a `cd` to the commit with `&&`
  alone. An agent's shell starts in the session's directory at every call, so
  a commit after a `;` or a new line also runs there whenever the `cd` fails,
  and the gate cannot read a path held in a loop variable. The orchestrator's
  routing commits follow the same rule.
