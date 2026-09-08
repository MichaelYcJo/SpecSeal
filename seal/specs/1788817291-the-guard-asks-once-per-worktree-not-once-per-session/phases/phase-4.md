# 1788817291-the-guard-asks-once-per-worktree-not-once-per-session — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 275345f |
| Ran by | specseal:smith on Opus 5 (1M context) |

## What this phase was asked

Build phase 4 only: the `isolation: "worktree"` Agent/Task path shares the
record — it is the same decision arriving through a different tool, and the
guard already guards both. Both directions: the path writes a record, and it
reads one a Bash creation wrote.

## What this phase found

**Sharing the record is two wirings, and only one of them existed.** The
reading half was already there once phase 3 landed the parameter — the Agent
call site just had to name its value. The writing half needed a hook group that
did not exist: `hooks.json` had `PostToolUse` matchers for `Bash` and for
`Write|Edit|NotebookEdit` and none for `Agent|Task`, so nothing observed an
Agent worktree creation at all. `post-agent` is the first group in this tree
that exists for one gate.

**It cannot be folded into `pre-agent`.** That group already carries the guard,
and it fires before the call. What the record says is that the call **ran**,
which is the whole of why it is evidence a command text cannot forge.

**The Agent path is silent where the Bash path allows, and that is not an
inconsistency.** The Bash allow is bounded to a command that is worktree
creation and nothing else; an Agent call with `isolation: "worktree"` is never
that — it is a creation **plus** an agent with a prompt. Silence is the guard
withdrawing its objection, which is exactly what the record establishes, and it
leaves whatever the harness wants to ask about running the agent where it was.
The same principle produced both answers.

**The module's existing rider on this path is unaffected and still open.** It
says an Agent worktree may be concurrent work the guard cannot see, because a
subagent renews the parent's lease and creates no id of its own. The record
does not touch that: it answers *has this session been told yes*, never *how
many streams are live*.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
