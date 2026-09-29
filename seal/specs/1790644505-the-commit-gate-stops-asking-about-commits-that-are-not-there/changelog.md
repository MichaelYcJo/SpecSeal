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
  only for a commit no work item owns; otherwise hand the commit back. What
  the gate stops has not changed, so no commit it used to judge now passes
  unjudged. The press is read from the session's transcript with the reader
  the worktree guard already uses, and every way of not reading it is the old
  behaviour. An attended session, and a `per axis` run, meet the same prompts
  as before.

### Added

- Contract §17: an agent commits with the repository's absolute path after
  `git -C`, in a command of its own, and joins a `cd` to the commit with `&&`
  alone. An agent's shell starts in the session's directory at every call, so
  a commit after a `;` or a new line also runs there whenever the `cd` fails,
  and the gate cannot read a path held in a loop variable. The orchestrator's
  routing commits follow the same rule.
