- **The routing declaration's third axis has a reader now.** `Implementation`
  said whether `smith` or the session builds a work item, and nothing looked at
  the answer again — a session could declare `smith`, build the whole item
  itself, and leave a record saying otherwise. Two hooks close that. When
  `smith` is spawned, a gate in the `pre-agent` group writes the checked-out
  branch name to `.git/specseal-implementer` and prints nothing, so it can
  neither deny nor ask. After a command that actually runs `git commit`, a
  reminder in the `post-bash` group prints one line naming the declaration
  where it answers `smith` and no mark stands for this branch — once per
  session per repository, never a decision, and silent when the mark stands,
  when the row is absent or unreadable, or when it answers `the session`. The
  commit gate's verdict is byte-identical with the row and without it. Both
  fail toward "no mark", which is toward a reminder: a mark gate that quietly
  stops running turns the notice on rather than off. A mark gate broken on
  disk leaves the worktree guard's verdict in the same group untouched, which
  is the objection issue #26 recorded against putting a second gate there,
  measured. `hooks/routing.py`, `templates/sdd-routing.md`, the README's gate
  table and `docs/review-chain-spec.md` no longer say the axis is read by
  nothing.
