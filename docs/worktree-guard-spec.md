# worktree-guard — behavior spec

Authority for `hooks/worktree-guard.py`. A change to the hook that diverges
from this document changes one of them knowingly — update both.

## Premise

Worktrees exist to keep CONCURRENT work from mixing in one folder. Single-
stream work uses plain `git switch` on the shared tree. The guard enforces
both directions of that rule from one signal: how many work streams are
actually live on the tree.

## Decision matrix

### A. Branch switch (`git switch` / branch-form `checkout`)

| Tree state | Decision |
|---|---|
| ACTIVE session present | deny — steer to a worktree |
| only IDLE sessions | ask — list each with its last-activity age; forgotten tabs are the user's call |
| detection unusable (can't see even our own process) | deny (conservative) |
| single stream, tracked changes present | ask — changes follow the switch |
| single stream, clean | allow silently |

### B. Worktree creation (`git worktree add`, or Agent/Task `isolation: "worktree"`)

| Tree state | Decision |
|---|---|
| ACTIVE session present | ask — separation justified, creation still needs a human |
| only IDLE sessions | ask — likely single-stream; `git switch` may suffice |
| detection unusable | ask |
| single stream | deny — steer to `git switch`; `[worktree-ok]` in the command downgrades to ask (explicit user intent) |

Never guarded: file restores (`checkout -- <path>`, `restore`), every
non-`add` worktree subcommand, sessions living in linked worktrees (already
isolated — switching the shared tree cannot affect them).

## Declared work streams — leases beat every heuristic

The signals below INFER liveness, and inference has a measured ceiling: a
session hosted outside a terminal (comm != `claude`) or working on this tree
from another cwd leaves no process, tty, or per-project transcript trace
here. So every tool call also DECLARES: the `session-lease` hook stamps
`<git-dir>/claude-preset-leases/<session-id>` for the repo being touched
(Write/Edit lease the edited file's repo; Bash leases its cwd's repo). A
lease fresher than the idle threshold is an active work stream, no inference
involved. Leases older than a day are pruned; failures are silent — a lease
is a safety net, never a blocker.

## Activity: what makes a session ACTIVE (heuristics, for sessions without a lease)

Active = ANY signal within `WORKTREE_GUARD_IDLE_MIN` minutes (default 5):

| Signal | Detects | Measured grounds (2026-05-06, live sessions) |
|---|---|---|
| tty atime (keystrokes) | human at the keyboard | forgotten tabs: hours stale |
| tty mtime (screen writes) | session streaming its progress | an idle Claude prompt does NOT repaint; a working one repaints every second |
| transcript last ACTIVE event | autonomous turns and **background agents** (`~/.claude/projects/<slug>/<session-id>/subagents/*.jsonl`) | a session 52 min past its last keystroke was writing its transcript that second |

The 5-minute default is safe only because of the second and third signals —
keyboard input alone cannot distinguish "forgotten" from "autonomous turn in
progress", which is why the earlier input-only design needed 60 minutes.

### Passive-event filtering

Transcript file mtime over-reports: idle sessions keep receiving passive
appends (type `attachment` — e.g. file-changed notices fired by *other*
sessions editing shared files; observed live turning three forgotten tabs
"active"). Therefore a fresh mtime must be confirmed against the tail (last
64KB): only `user` / `assistant` / `tool_use` / `tool_result` / `progress`
events count, and their own timestamps are used. A stale mtime is trusted
as-is — passive appends only ever make a file look fresher, never staler.

### What a blocking prompt must show (identification)

"Another session is active" is undiagnosable without identity — measured in
practice: a session was misattributed to Cursor by guessing from a sibling
MCP process's flags, and "last activity 1 min ago" could not be told apart
from a heartbeat. So every listed session shows:

- **host app**, attributed by walking the ANCESTOR process chain (never
  sibling processes) — e.g. "(VS Code 터미널)";
- **disaggregated signals** — terminal input/output age and transcript
  active-event age separately;
- the project's newest OTHER transcript's **last user message snippet**, so
  the human can recognize which conversation is being protected.

### Unknowns resolve conservatively

No readable tty AND no readable transcript → active (deny-side). Detection
that cannot even find our own process → `reliable=False` → the matrix rows
above. Rationale: the guard's failure modes are asymmetric — a wrong deny
costs a prompt, a wrong allow breaks another session's tree.

## Known limits

- A heredoc line that IS exactly a git command still matches (segment
  splitting cannot tell heredoc bodies from commands). Mentions inside
  quoted strings or after other command words do not.
- Transcript activity is per-project, not per-pid: one working session marks
  every session of that project active. Conservative by design.
- tty atime also refreshes on in-turn stdin reads (a session listening for
  interrupts), not only human keystrokes — which is why the prompt labels it
  "terminal input/output", not "keystroke". Either cause means the session is
  live, so treating it as active errs conservative.
