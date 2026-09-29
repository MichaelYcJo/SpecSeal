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

### Added

- Contract §17: an agent commits with the repository's absolute path after
  `git -C`, in a command of its own, and joins a `cd` to the commit with `&&`
  alone. An agent's shell starts in the session's directory at every call, so
  a commit after a `;` or a new line also runs there whenever the `cd` fails,
  and the gate cannot read a path held in a loop variable. The orchestrator's
  routing commits follow the same rule.
