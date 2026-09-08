# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 1000a0b |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build phase 3 only: the `PreToolUse` read in `guard_worktree_creation`, so a
later creation in a session with a consent record gets through. What must not
change was named: a session with no record still asks, and the single-stream
site still denies and steers to `git switch`. If the design lets a session with
no prior approval create a worktree silently, it is wrong.

## What this phase found

**The read goes above every row, including the ACTIVE one.** Each row of §B
asks something the record has already answered — the ACTIVE row asks for a
confirmation, the two choice rows ask which way to go, the `[worktree-ok]` row
asks whether the token was meant. Moving the read below any of them turns four
cases red, which is what mutation 12 in phase 5 measures.

**Silence would not have reached the budget, and that decided the `allow`.**
A hook that stays quiet has no opinion, so the harness's own permission
question stands. Measured on this machine: `~/.claude/settings.json` allowlists
`Bash(git worktree list:*)` and not `git worktree add`, so every creation would
still have held the run. A fix that needs a settings change is not a fix in
this repository's source.

**So the allow had to be bounded, and the bound is not a heuristic.**
`permissionDecision: "allow"` covers the **whole** tool call, and a creation is
routinely one segment of a compound; the record is about worktree creation, so
that is the whole of what the guard may speak for. Everything else answers
`ask` — explicitly, as a floor rather than a fallthrough, because landing back
on the ladder would put the single-stream **deny** in front of a session that
has already been told yes.

**A command the lexer gave up on is not vouched for, which is the opposite call
from `has_token`.** That function widens on an unreadable command, deliberately:
it is a consent read, and widening one costs a prompt. This is a permission
decision, and widening one costs whatever else was on the line.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
