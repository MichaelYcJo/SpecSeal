# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e5ed166 |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Read `gh issue view 237` first, then `hooks/worktree-guard.py`'s module
docstring and `has_token`'s, because that is where the current behaviour is
argued for and the change has to answer them rather than step around them.
Write the SDD ladder — `routing.md` and the `docs/flow.md` row were already
committed — and argue the suggested shape in `spec.md` rather than only
implementing it. Three questions were named as the implementer's to decide and
argue rather than bring back: whether the record expires, whether a failed
`git worktree add` records consent, and what happens when the record cannot be
written. A fourth was named as something to *say*: whether the record is a
third directory or a value in the existing one.

## What this phase found

**The docstring the change has to answer is right, and that is what made the
argument writable.** `has_token` refuses a loose read because *reading this
token loosely turns the guard off with nobody asked*, and the `[worktree-ok]`
site refuses to allow because the token is *what a completed confirmation looks
like coming back through the guard*. Neither is an argument against a
`PostToolUse` record, and the reason fits in one table: the token is written by
whoever issues the command **before** the question, the record by a hook
**after** the answer. `spec.md` carries that table, and every later phase
points at it rather than re-deriving it.

**The existing session-scoped state is not the place for this, and reading it
first is what settled Q4.** `<git-dir>/specseal-worktree-choice/create/` looks
like the same thing and is its opposite: `already_asked` writes it from
`PreToolUse`, before the answer, and *records it when it was not* — so it means
"the question was put". Sharing one file would let the guard read its own
question back as consent. The two also fail in opposite directions, which
`already_asked`'s docstring states outright for its half: an unwritable choice
marker counts as **already asked**. An unwritable consent record must count as
**no consent**, and one file cannot fail two ways.

**The scope is the clone, not the tree.** `already_asked` resolves through
`--absolute-git-dir`, which in a linked worktree is
`<main>/.git/worktrees/<name>`. A consent record there would be lost the moment
a session created its second worktree from inside its first.
`hooks/optin.py#git_common_dir` already resolves the clone's directory with the
`.git`-is-a-file case handled, so the resolution exists and is not rewritten.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
