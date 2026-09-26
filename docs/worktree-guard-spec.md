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
| **consent: this session already created a worktree in this clone, or its person pressed `automation` on the routing question** | **allow** where the tool call is worktree creation and nothing else · **silent** where the command does more, and on the Agent/Task path. Read before every row below it — see §Creation consent |
| ACTIVE session present | ask — separation justified, creation still needs a human. Declining leads to "use the worktree that session opened, or wait for it", neither of which is a command this session issues, so there is nothing to offer |
| only IDLE sessions | **choice** — create it, or switch in the shared tree; likely single-stream |
| detection unusable | **choice** — the same two |
| `[worktree-ok]` given (Bash only) | ask — the token IS a completed confirmation coming back through the guard, so putting the question again asks what the user already answered. Declining withdraws the token, which is the other way on |
| single stream, **Bash** | deny — steer to `git switch`; `[worktree-ok]` in a retry reaches the row above |
| **Agent/Task**, no consent, any tree state | ask — the agent runs beside this session, so the call is concurrent by construction. No session is counted, no choice site is reached, and declining cancels the spawn. See below |

Every row between the consent row and the Agent/Task row is the Bash path's.

#### Why the Agent path counts nothing, asks once, and reads no token

**An isolated agent is concurrent work by construction, so the Agent path does
not count sessions (#8).** The agent runs beside the session that spawned it,
and that session's tree is not switched: two work streams, which is what the
Premise counts. The session count cannot see it. A subagent's tool call renews
its parent's lease and has no id of its own (measured), so an agent spawned in
a one-session tree read as single-stream work. The verdict that reading
produced told the model to call the Agent again without `isolation:
"worktree"`, which puts the agent in the parent's tree while the parent works
there — the mixing this guard exists to prevent.

So the path has two outcomes. Consent is silence, for the reason §Creation
consent gives: the call is a creation plus an agent with a prompt, and consent
answers the first half. Otherwise it asks, once per session, because the
first creation of a session is one confirmation and a spawn that ran writes the
record. What changed is what the path measures, not that floor: lowering it for
supervised sessions is not something #8 asked for.

The token is a separate matter, and the reason the path reads none is that it
has no command line.

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
creation ends at a human confirmation on both paths regardless. The path now
asks outright, so the verdict does not depend on the prompt at all.
Enforced by: tests/test_worktree_guard.py::test_an_isolated_agent_asks_without_counting_sessions, tests/test_worktree_guard.py::test_the_agent_verdict_does_not_depend_on_the_prompt

## Creation consent — the first creation is the question, not every one

<!-- specs/1788817291-the-guard-asks-once-per-worktree-not-once-per-session -->
**The first worktree creation in a session is the question, and a later one in
the same session is allowed — and where the person pressed `automation`, not
even the first is asked.**
The guard used to answer creation with `ask` at every site that reached it, so
no path through it cost zero prompts and the cost grew with the number of
worktrees. Measured on the release run that opened #237, on 2026-09-08: six work items on six branches
needed six `git worktree add` calls, and the guard held the run at all six. An
unattended run reaches the first and stops there, which is the one shape
`CONTRIBUTING.md`'s prompt-budget rule has no room for.

`[worktree-ok]` cannot fix that, and the reason is the same one `has_token`
gives: the token is written into the command by whoever issues it, so the model
can write it on the first attempt, and reading it as consent turns the guard
off with nobody asked.

**What separates the first creation from the sixth is available without
trusting any token.** The harness only runs a `git worktree add` that was
permitted, so a `PostToolUse` observation of one that actually ran is written
**after** the answer rather than before the question. That is the one thing a
command text cannot forge.

| | `[worktree-ok]` | the consent record |
|---|---|---|
| written by | whoever issues the command | the `PostToolUse` hook |
| written when | before the question | after the answer |
| forgeable by the model | yes | no |

`hooks/worktree_consent.py` writes it, on both entry points, and
`guard_worktree_creation` reads it. What changes is one invariant: *creating a
worktree always takes one confirmation* becomes *the first creation of a
session takes one*, and the routing answer below makes that zero for a session
whose person pressed `automation`.

**The routing answer is the second consent, and it covers the creation the
record cannot: the first.** An automation run creates its worktrees before any
of them has run, so no record exists at the first `git worktree add`, and the
guard stopped a run whose person had pressed `automation` one minute earlier
(#604). That answer is on disk when the first creation arrives, and the model
did not write it: the harness writes an `AskUserQuestion` result into the
session's transcript from the person's click. The model writes the question
and its options, never which one was pressed.

| | `[worktree-ok]` | a `routing.md` reading `Automation \| yes` | the consent record | the routing answer in the transcript |
|---|---|---|---|---|
| written by | whoever issues the command | the model, with `Write` | the `PostToolUse` hook | the harness, from the person's click |
| written when | before the question | after the answer, but the answer it records is the model's account of it | after a creation ran | when the person answers |
| present at the first creation of an automation run | yes | no — measured twice, the worktrees came first so each branch could carry its own | no | **yes** |
| forgeable by the model by habit | yes | yes | no | no |
| forgeable by editing a file on purpose | — | — | yes (`touch`) | yes (an appended line) — the record's standing |

A `routing.md` is not read, not even as a fallback: a fallback the model can
satisfy by writing a file is `[worktree-ok]`'s standing under another name.

**What exactly is read**, and every way of failing it is *no consent*, which is
the guard's behaviour before the answer was read:

1. **This session's own main transcript** — the payload's `transcript_path`
   where its basename is `<session-id>.jsonl`, otherwise the one file matching
   `~/.claude/projects/*/<session-id>.jsonl`. A subagent's call carries its
   parent's session id, so it reaches the parent's answer through the second
   form. No other session's file is read, and no `subagents/` file.
2. **A harness-written `AskUserQuestion` result**: a `user` entry whose
   `tool_result` names, by `tool_use_id`, an earlier `AskUserQuestion` call,
   read from its structured `toolUseResult.answers`. A Bash result echoing
   *The user answered: "automation"* has no such link.
3. **The routing question**: one single-select question whose options' leading
   phrases are exactly `automation`, `per axis` and `no work item`
   (`skills/implement/orchestration.md` §*Question 1 — single-select*),
   answered `automation`. A leading phrase is the label casefolded and cut at
   the first ` (`, ` —` or ` -`, so `automation (Recommended)` counts.
4. **The same clone**: the result entry's own `cwd` resolves to the same common
   git directory as the creation's repository.

A `per axis` answer is not read, even with its first box ticked: in every
measured instance the box label had been reworded or translated, so a rule
matching the prescribed label would never fire. The record is read first,
because it is one `stat`; the transcript is scanned only while there is no
record, and the first creation writes one.

**The record.** An empty file at
`<git-common-dir>/specseal-worktree-consent/<session-id>`; its existence is the
whole fact, the way the choice marker's is.

- **A third directory, not a value in `specseal-worktree-choice/create/`.**
  That marker is written by `PreToolUse` before the answer and means *the
  question was put*, so one shared file would let the guard read its own
  question back as consent. The two also fail in opposite directions — an
  unwritable choice marker counts as **already asked**, an unwritable consent
  record counts as **no consent** — and one file cannot fail two ways.
- **The common git directory, not the per-worktree one.** The record stands
  for *this session may split this clone into worktrees*, and a linked worktree
  is the same clone. A session that creates its first worktree from the main
  tree and its second from inside a linked one has made one decision, so it
  pays for one.
- **No expiry and no pruning.** A session id is already scoped to a session, so
  a time bound can only produce one new outcome: a session that outlives it is
  asked a second time, which is the failure this removes.
- **A failed `git worktree add` records too.** The record is about the
  approval, which happened; the retry after a failure — a path that already
  exists, a branch already checked out — is the worst moment to put the
  question again.
- **An unwritable record leaves none**, silently, and the next creation asks.
  A crash would be worse than the prompt it saves: a hook that raises dies with
  stdout empty, which is how a hook says *nothing to see here*.

**Why the allow is bounded.** `permissionDecision: "allow"` bypasses the user's
own permission settings for the **whole** tool call, and a creation is
routinely written as one segment of a compound. Consent is about worktree
creation, so the guard speaks for a command that is worktree creation and
nothing else. For anything more it stays **silent**: it withdraws its
objection, and the rest of the command line meets the harness's own permission
flow rather than a deny about the worktree. A command the lexer gave up on is not vouched
for either — what it could not read is what the allow would be covering.

**And a segment is more than its command word.** *Nothing else* used to be
asked of the compound only, which is what a `&&` or a `;` produces — and a
shell runs a great deal inside one segment. Review round 1 executed eleven
shapes that were vouched for with a record present: `$( )`, backticks, `>`,
`>>`, `<`, `2>`, `<(…)`, a subshell, a heredoc, `sudo`, `env VAR=…` and a bare
`VAR=…`. Two were run in a real shell and did what a shell does — the
substitution created its marker, the redirection truncated a file — under an
allow that had already covered the whole tool call.

Two tests are the bound now, and both are about one segment rather than the
command: **the segment's command word is the word `git`**, which
`cmdline.parse_git` deliberately does not require (it reads past `sudo`, `env`
and a leading `VAR=val`, because the question IT answers is *is this a git
invocation*); and **no token carries an expansion or a redirection** — `$`, a
backtick, `<` or `>`. A glob and a `~` in an ARGUMENT are left alone on
purpose: both expand and neither runs anything. A trailing `&` is left alone
too — it backgrounds the creation and runs nothing else, and `… & rm -rf
<path>` is two segments where the second one fails the first test.

**The first test is exact equality, because a basename is not an identity.**
It compared `os.path.basename(tokens[0])` for one release, and review round 2
executed the consequence with a record present: `./git`, `../git`, `bin/git`,
`/tmp/evil/git`, `~/git` and `*/git worktree add …` all answered `allow`. That
allow covers the whole tool call, so a session that had **one** creation
approved could then run any executable on the machine by giving it a filename
of `git` — and the reason this test exists, that a hook must not speak over a
user's own `permissions.deny`, does not stop at `sudo`.

The boundary the code implements is *a command word carrying no separator, so
the shell resolves it on `PATH`*. Anything with a `/` in it names a file this
hook cannot identify. Re-enumerated by construction over 32 command-word
shapes, exactly five are vouched for, and all five are the word `git` after
lexing: `git`, `\git`, `'git'`, `"git"` and `g"i"t`. Every path, every
expansion (`~/git`, `*/git`, `gi*`, `$GIT`, `` `which git` ``), a different
case, a trailing slash, every wrapper and every leading assignment falls to
`ask`. What that costs is one prompt on `/usr/bin/git worktree add …`, which is
the trade already made for `$` and `>`: a wrong deny spends a prompt, a wrong
allow signs for a binary nobody identified.

**A creation the guard never judged used to mint the record.** The guard's
`PreToolUse` walk classifies the **first** segment it can read, while
`hooks/worktree_consent.py` records for a creation **anywhere** in a command
that ran. Any first segment with a verdict of its own therefore took the
decision and the creation ladder never ran. Executed at round 1, clean
single-stream tree, no record: `git worktree add ../wt f` denied and
`git status && git worktree add ../wt f` denied — `git status` classifies to
nothing, so the walk moved on — but `git switch feature/x && git worktree add
../wt f` was **silent**, the shell created the worktree, and the session held
session-wide consent from that point. The model never had to forge the record;
it only had to choose which question got asked, and the first segment is where
that is chosen.

The switch ladder keeps every verdict it had. Making the creation outrank the
earlier verdict closes the same hole and costs a protection: a switch denied
because another session is working in the tree would become an `ask` about the
creation, and the branch would still be taken out from under that session one
approval later. **So the creation is judged between the ladder's two halves.**

| Switch-ladder row | Order | Why |
|---|---|---|
| ACTIVE session | above the creation | the one row that denies unconditionally. A `deny` stops the creation along with the rest of the command, and making a creation outrank this would turn it into an `ask` while the branch is still taken out from under the other session, one approval later |
| only IDLE · detection unusable | **both**, and the branch decides | these are [choice sites](#choice-sites): they deny **once** per session per direction and `ask` on every attempt after. The deny keeps its precedence, because it stops the whole command line. The `ask` does not — approving it runs every segment while its own text asks about the switch — so that branch hands the creation its verdict first, through `choose`'s `before_ask` |
| **the creation** | | |
| tracked changes present | below | its own text says *the switch is allowed* — it protects no tree, it asks whether uncommitted changes should ride along. Approving it created the worktree too, so whether the creation was questioned came down to whether the tree happened to be dirty. Executed: the same command denied on a clean tree and asked about the changes on a dirty one |
| single stream, clean | below | says nothing at all. This is where `git switch feature/x && git worktree add ../wt f` ran unjudged and minted session-wide consent |

**Reading *"the three rows above all deny"* off that first row is what put row
2 in this table twice.** It was written when the creation sat below all three,
and it was true of the first attempt in a session and false of every attempt
after. Executed at round 2, in both the idle and the detection-unusable state:
the same `git switch feature/x && git worktree add ../wt f` answered `deny`
then `ask`, the `ask` read *Approve — switch branches in this shared tree*, and
approving it created the worktree and minted session-wide consent with the
creation question never put.

The guard's other silent exit is earlier, at `if not top`, and it has the same
hole: it is reached when the shell is outside any repository while a `git -C
<repo> worktree add` in the same command is not. That one falls through too.

**The property, measured rather than the shapes.** Whatever the writer would
record for, the guard has either denied it — which stops the whole command
line — or put the creation question in the text of its `ask`. Re-derived after
the change over 21 command shapes × 5 tree states × 2 shell directories × 2
record states × 3 attempts, which is **1260 combinations**: 230 of them are
cells the writer records for, and **0** of those reach a verdict that lets the
command run without the creation question. With both round-2 fixes reverted the
same sweep finds **64**, all of them the second and third attempt at a
switch-then-create in the idle or detection-unusable state.

**Why the Agent/Task path is silent rather than an allow.** That call is a
worktree creation *plus* an agent with a prompt, and the record is about the
first half. Silence is the guard withdrawing its objection, which is the whole
of what the record establishes; whatever the harness asks about running the
agent is not the guard's to remove.

**What does not change.** A session with neither the record nor the routing
answer still asks at every site, and the single-stream row still denies and
steers to `git switch`. The switch direction reads neither: a creation the user
agreed to, or a run the user said should not stop, says nothing about taking
another session's branch out from under it.

**The prompt budget.** Zero for a session whose person pressed `automation`. One per session otherwise, from one per worktree unbounded — for a creation written on its own, which is the form the measured six took. Re-measured after round 2's fixes, six creations in one session on a clean single-stream tree: **deny, allow, allow, allow, allow, allow**.
Before consent, a creation written as one segment of a compound still costs one
prompt each time, and so does one carrying an expansion, a redirection, a wrapper or a **path-qualified command word**, because that is exactly what the bound above refuses to speak for. The last of those is what round 2's second fix added to the list, and it moves nothing in the budget: `git worktree add …`, the same backgrounded, and the `\git` spelling all still allow.
Enforced by: tests/test_the_guard_asks_once_per_session.py::test_the_first_creation_is_still_a_question, tests/test_the_guard_asks_once_per_session.py::test_a_second_creation_in_the_same_session_is_allowed, tests/test_the_guard_asks_once_per_session.py::test_the_measured_automation_run_is_not_stopped, tests/test_the_guard_asks_once_per_session.py::test_a_result_not_linked_to_an_ask_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_automation_on_another_question_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_an_answer_given_in_another_clone_is_not_consent, tests/test_the_guard_asks_once_per_session.py::test_the_labels_match_the_routing_question_the_orchestrator_asks

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

**The two branches have opposite standing for whatever else is on the command
line, and only one of them is a protection.** The deny stops the WHOLE command,
so anything written beside what the site is asking about is stopped too. The
fallback `ask` does not: approving it runs every segment, while its own text
asks about one of them. So a site reading a choice deny as *this row protects
the tree* is reading the first attempt only. `choose` takes a `before_ask`
for that reason — a judgment the fallback yields to, run on that branch alone,
which is how the switch ladder's two choice rows keep their deny and stop
deciding whether a creation on the same line is questioned at all.

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

**Not the same record as creation consent**, and the difference is what keeps
them apart in one directory listing: this marker is written by `PreToolUse`
before the answer and means *the question was put*; the consent record is
written by `PostToolUse` after it and means *a creation ran*. §Creation consent
holds the rest.

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
"Why the Agent path counts nothing, asks once, and reads no token".

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

<!-- specs/1788846800-an-exited-session-reads-as-live-for-five-minutes -->
**Active = ANY signal within `WORKTREE_GUARD_IDLE_MIN` minutes (default 5):**

| Signal | Detects | Measured grounds (2026-05-06, live sessions) |
|---|---|---|
| tty atime (keystrokes) | human at the keyboard | forgotten tabs: hours stale |
| tty mtime (screen writes) | session streaming its progress | an idle Claude prompt does NOT repaint; a working one repaints every second |
| transcript last ACTIVE event | autonomous turns and **background agents** (`~/.claude/projects/<slug>/<session-id>/subagents/*.jsonl`) | a session 52 min past its last keystroke was writing its transcript that second |

The 5-minute default is safe only because of the second and third signals —
keyboard input alone cannot distinguish "forgotten" from "autonomous turn in
progress", which is why the earlier input-only design needed 60 minutes.
Enforced by: tests/test_worktree_guard_signals.py::test_fresh_active_event_counts, tests/test_worktree_guard_signals.py::test_transcript_scan_reaches_background_agents

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
reads them (`commit-review-gate-spec.md` §Which repository).

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
