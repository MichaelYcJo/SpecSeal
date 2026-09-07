- **The worktree guard asks once per session instead of once per worktree
  (issue #237).** It answered creation with `ask` at every site that reached
  it, so no path through it cost zero prompts and the cost grew with the number
  of worktrees. Measured on the 0.9.1 release run: six work items on six
  branches needed six `git worktree add` calls, and the guard held the run at
  all six. An unattended run reaches the first and stops there.

  **`[worktree-ok]` could not fix that and `has_token`'s docstring says why.**
  The token is written into the command by whoever issues it, so the model can
  write it on the first attempt; reading it as consent turns the guard off with
  nobody asked. What separates the first creation from the sixth needs no
  token: the harness only runs a `git worktree add` that was permitted, so a
  `PostToolUse` observation of one that actually **ran** is written after the
  answer rather than before the question, which is the one thing a command text
  cannot forge.

  `hooks/worktree_consent.py` writes that record — an empty file at
  `<git-common-dir>/specseal-worktree-consent/<session-id>` — on both entry
  points, and the guard reads it above every row of its creation ladder,
  because each of them asks something a person has already answered. One
  invariant changes: *creating a worktree always takes one confirmation*
  becomes *the first creation of a session takes one*.

  **A third directory, not a value in the choice marker beside it.** That
  marker is written by `PreToolUse` before the answer and means *the question
  was put*, so one shared file would let the guard read its own question back
  as consent. They also fail in opposite directions — an unwritable choice
  marker counts as **already asked**, an unwritable consent record counts as
  **no consent** — and one file cannot fail two ways.

  **Keyed to the clone, with no expiry.** The record stands for *this session
  may split this clone into worktrees*, so it lives under the common git
  directory and a linked worktree of the same clone shares it. A session id is
  already scoped to a session, so a time bound on top of it could only produce
  one new outcome: a session outliving the bound is asked a second time, which
  is the failure being removed. A failed `git worktree add` records too — the
  record is about the approval, and the retry after a failure is the worst
  moment to put the question again.

  **The allow is bounded, and the bound is about each segment rather than only
  about the compound.** `permissionDecision: "allow"` covers the whole tool
  call, so the guard speaks only for a command that is worktree creation and
  nothing else; a compound gets `ask` about the rest of the command line, never
  a deny about the worktree, and a command the lexer gave up on gets `ask` too.
  So does a creation carrying an expansion or a redirection — `$( )`,
  backticks, `>`, `>>`, `<`, `2>`, `<(…)`, a subshell, a heredoc — and one
  behind a wrapper, `sudo git worktree add …` or `env VAR=… git worktree add
  …`, because a user's own `permissions.deny` must not be spoken over by a hook
  reasoning about worktrees.

  **A creation anywhere in the command is judged before it runs.** The guard
  classified the first segment it could read while the writer records for a
  creation anywhere, so a `git switch` written in front of a creation took the
  decision and the creation was never judged — it ran, and the session held
  consent from that point. The switch ladder keeps every verdict it had, and
  only its two silent exits now fall through to the creation.
  On the `Agent`/`isolation: "worktree"` path the guard goes silent rather than
  allowing, because that call is a creation *plus* an agent with a prompt and
  the record is about the first half.

  What does not change: a session with no record still asks at every site, the
  single-stream row still denies and steers to `git switch`, and the switch
  direction never reads the record. (#237)
