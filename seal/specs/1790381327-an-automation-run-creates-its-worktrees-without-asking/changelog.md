- **An automation run creates its worktrees without the worktree guard
  stopping it, and an isolated agent is no longer told to drop isolation
  (issues #604 and #8).** A session whose person pressed `automation` on the
  routing question used to meet a guard prompt at its first `git worktree
  add`, one call after the answer that says nothing stops to ask again. The
  guard now reads that answer as consent, beside the record a creation that
  already ran leaves. It reads the answer from this session's own
  transcript, where the harness wrote it from the click, and only when it is
  the real `AskUserQuestion` result for the routing question, the option
  labelled `automation` was pressed, and it was given from this clone. A
  message, a command's output or a `routing.md` saying `automation` does not
  count, because the model writes those, and neither does a typed answer
  such as "automation - but ask me first". A `per axis` answer still
  meets one prompt per session. An Agent call with `isolation: "worktree"`
  is now judged as concurrent work, because the agent runs beside the session
  that spawned it: without consent it asks once, and its reason no longer
  says the tree is single-stream or suggests calling the agent again without
  isolation, which would have put it in the parent's tree. The switch
  direction reads neither consent.
