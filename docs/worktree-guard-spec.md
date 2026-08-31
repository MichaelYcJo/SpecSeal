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
| ACTIVE session present | deny — steer to a worktree. One destination, so no choice to offer |
| only IDLE sessions | **choice** — switch here, or split into a worktree; each session listed with its last-activity age, because forgotten tabs are the user's call |
| detection unusable (can't see even our own process) | **choice** — same two. A blanket deny locked out extension hosts entirely |
| single stream, tracked changes present | ask — the changes follow the switch. Genuinely yes/no: the destination branch is the same either way, and what is being asked is whether the uncommitted changes ride along |
| single stream, clean | allow silently |

`[shared-tree-ok]` in the command turns the two **choice** rows silent — see
§Choice sites.

### B. Worktree creation (`git worktree add`, or Agent/Task `isolation: "worktree"`)

| Tree state | Decision |
|---|---|
| ACTIVE session present | ask — separation justified, creation still needs a human. Declining leads to "use the worktree that session opened, or wait for it", neither of which is a command this session issues, so there is nothing to offer |
| only IDLE sessions | **choice** — create it, or switch in the shared tree; likely single-stream |
| detection unusable | **choice** — the same two |
| `[worktree-ok]` given (Bash only) | ask — the token IS a completed confirmation coming back through the guard, so putting the question again asks what the user already answered. Declining withdraws the token, which is the other way on |
| single stream, **Bash** | deny — steer to `git switch`; `[worktree-ok]` in a retry reaches the row above |
| single stream, **Agent/Task** | ask — see below |

#### Why the Agent path ends at `ask` and reads no token

The two entry points part company at exactly one row, and the reason is that
one of them has no command line.

`[worktree-ok]` is a bare word in a command: a shell command is tokens, so
"the user asked for this" and "a sentence about the token" are distinguishable
there. An Agent call carries prose instead, and reading the token out of a
prompt was tried and taken back after both halves failed:

- a prompt that merely *documented* `[worktree-ok]` switched the guard off,
  and the thing that writes those prompts is the model itself;
- a prompt that really carried it — `the user's request was isolation
  [worktree-ok]` — tokenized badly on one apostrophe and fell to the
  single-stream **deny**, whose text told it to put `[worktree-ok]` in the
  prompt. It already had.

What the token was buying was one step, `deny` to `ask`, because worktree
creation ends at a human confirmation on both paths regardless. Taking that
step outright costs nothing and removes the guessing. So the Agent verdict
does not depend on the prompt at all, and its reason names the only way on it
actually has: call the Agent again without `isolation: "worktree"`.

## Choice sites

A hook decision renders as approve/decline and the model never gets the turn,
so at a site where declining has TWO destinations the user sees neither and
has to retype the command they wanted. Those sites deny instead, and spend the
reason on an AskUserQuestion instruction naming both — the shape measured in
`hooks/review-skill-gate.py`.

The test for whether a site qualifies is one question: **after declining, is
there more than one command this session could issue?** Where there is not,
options would have to be invented, and the three rows above that stay `ask`
or `deny` are the ones that fail it.

A choice deny and the ACTIVE-session block are both `deny`; the reason is what
tells them apart.

**Once per session per direction**, not per site. The marker is
`<git-dir>/specseal-worktree-choice/{create,switch}/<session-id>`, and the
session id is reduced to its basename first — it names a file, and
`../../escaped` otherwise wrote one at the repository root (measured).

Direction is the right grain in both directions of error. One budget for the
whole guard let a creation question spend the answer a later switch needed,
and the switch then got the two-button prompt this design exists to replace
(measured). Splitting per site would buy nothing — within a direction the
sites are mutually exclusive on tree state — while costing a second question
whenever the model retries with a token and lands on a neighbouring site.

An unwritable marker counts as already asked: one missed question beats a deny
nothing can get past. Every attempt after the first gets the decision the site
made before this design, which is also the answer for an environment with
nobody to ask — one extra round trip, then the old behavior. No session id, no
marker, so the site's old decision stands from the start.

**Retry tokens, one per direction.** Both are matched as **bare words** of the
command, never as substrings: a substring test read
`echo 'we documented [shared-tree-ok] today'` as an answer and turned the
guard off (measured). Both stay visible in shell history.

The whole command is tokenized first, and only when that fails does the check
drop to per-segment scanning. Segments come from a regex that cuts on `;` and
`|` inside quotes as well, so `… && echo "wip; go"  # [worktree-ok]` left
pieces holding half a quote each; shlex refused them and a token the user
really had given read as absent (measured). That landed on the single-stream
deny — the one site with no budget and no `ask` behind it — and repeated on
every retry until the command itself was rewritten.

Tokenizing the whole command keeps **quoted** prose harmless, because a quoted
sentence becomes one token that no bare-word comparison matches. Unquoted
prose is a different matter and still passes — measured:
`git switch x && echo the [shared-tree-ok] token is documented` goes silent.
Shell prose is usually quoted, so the residual is narrow, but it is a
residual and not a property.

**Where the token is read from.** The command, and only the command. The
Agent/Task path has no command line and reads no token at all — see §B's
"Why the Agent path ends at `ask`".

| Token | Answer it carries | Effect |
|---|---|---|
| `[worktree-ok]` | create the worktree | the site asks — creating one always takes a confirmation, so this direction's floor is `ask` and no token lowers it |
| `[shared-tree-ok]` | switch in the shared tree | the two switch **choice** rows go silent — this direction's floor is `allow`, and the guard's own verdict there is *cannot tell*, so the token settles it |

**The token check runs before the choice sites**, immediately after the
ACTIVE-session row. Order matters: behind them, a user who answered "split
into a worktree" came back carrying `[worktree-ok]`, and in an unreadable
environment the choice site caught it first and asked the question they had
just answered.

**Each choice hands back the other direction's token.** The switch options
name `git worktree add … # [worktree-ok]` and the creation options name
`git switch … # [shared-tree-ok]`, so following either answer arrives
confirmed rather than questioned again. One half was missing at first, and the
measured cost was two AskUserQuestion prompts for one decision.

**What `[shared-tree-ok]` cannot reach.** The ACTIVE-session row is tested
before the token, so a token in this session's command never crosses the deny
that protects a tree this session does not own. What it can settle is only the
two rows where the guard itself says it cannot tell, and the dirty-tree row is
outside it too because that asks something else.

The token records the user's answer in the command; nothing verifies that a
user rather than the model put it there. That is the same standing
`[worktree-ok]` has always had, and the same one `[no-review]` has at the
commit gate: an inline switch is an audit trail, not an authorization.

`[shared-tree-ok]` is ignored where another session is ACTIVE (that deny
protects a tree this session does not own, and a token from this session is
not the other session's consent) and where the tree is dirty (a different
question). Without it, a user who chose the shared tree met the mirror
question one command later — the answer they had just given.

Never guarded: file restores (`checkout -- <path>`, `restore`), every
non-`add` worktree subcommand, sessions living in linked worktrees (already
isolated — switching the shared tree cannot affect them).

## Declared work streams — leases beat every heuristic

The signals below INFER liveness, and inference has a measured ceiling: a
session hosted outside a terminal (comm != `claude`) or working on this tree
from another cwd leaves no process, tty, or per-project transcript trace
here. So every repo-touching tool call (Bash, and file edits including
notebooks) also DECLARES: the `session-lease` hook stamps
`<git-dir>/specseal-leases/<session-id>` for the repo being touched
(file edits lease the edited file's repo; Bash leases its cwd's repo). A
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
above. Those rows are a **choice**, which is a deny that hands the decision
back rather than a block: the second attempt is the `ask` those rows used to
return, so no host is locked out. What must not return is a *plain* deny —
some hosts never satisfy the process heuristics, and a permanent deny there
disables `git switch` outright. Rationale: the
guard's failure modes are asymmetric — a wrong deny costs a prompt, a wrong
allow breaks another session's tree — but a deny that fires on EVERY switch
in an environment is no longer a cost, it is an outage.

### Which tree, when the command walks to it

The tree judged is the one the command acts on. `git -C <path>` names it
outright, and a `cd` earlier in the command moves the shell to it — this guard
is the reason a session is in that shape at all, since it refuses a switch and
tells the user to work in a separate worktree, so the session stays where it
was while the commands do not. Both are read the same way the commit gate
reads them (`review-chain-spec.md` §Which repository).

Two kinds of destination fall back to the session's own directory, which is
this guard's answer from before it could read a `cd` at all:

- one that cannot be computed — a variable, a glob, a subshell, `cd -` with
  nothing behind it;
- one that reads cleanly and holds **no repository**. `cd /no/such/dir ; git
  switch x` leaves the shell exactly where it started, because `;` runs what
  follows whether the `cd` worked or not — so the switch happens in the
  session's own tree, which is the tree another session may be sitting in.

A `git -C` naming no repository is not one of them and stays silent: git
refuses that command itself, so no tree is touched.

The commit gate stops on a target like this instead of falling back. The two
differ because what they protect differs: a commit nobody judged is a commit
nobody reviewed, while a guard that goes silent leaves a shared tree
unguarded, and §Unknowns resolve conservatively puts the cost of a wrong deny
at one prompt against a wrong allow breaking another session's tree.

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
