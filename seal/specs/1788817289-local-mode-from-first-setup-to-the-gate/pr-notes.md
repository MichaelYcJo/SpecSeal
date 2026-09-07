# What a change to a gate must carry

`CONTRIBUTING.md` §*What a change to a gate must carry* asks four things. They
are answered here so the pull-request body can lift them.

Two gates changed. `chain_check.py` is the pull-request check; `mode-gate.py`
is new, and `hooks/dispatch.py` puts it in the `pre-bash` group.

## A test seen red

Every case was written against the unfixed code and watched to fail. What was
seen, in order:

| Change | What was red, and against what |
|---|---|
| `round_record.py#where` | 4 of 11 cases, against `02ef9d7`'s parent. The refusal itself was reproduced first on a scratch local-mode repository — `round-record: --item …/.git/seal/specs/<id> is not a directory inside a git repository`, exit 2 |
| `chain_check.py#nothing_declared` | 1 case. The false sentence was reproduced first: a local-mode repository holding a declaration for the checked-out branch printed *Add seal/specs/<work-item>/routing.md to declare*, exit 0 |
| `mode-gate.py` and `hooks/config.py` | 6 failures and 8 collection errors, against a tree where neither file existed |
| the preset block and the bootstrap | 5 of 6 cases, against the documents as they stood at `589cf25`. The sixth reads the gate, which the previous phase had already landed; it was red before that phase |

Beyond §15, every unit added was mutation-tested one at a time with the
caches cleared: 5 mutations in phase 1, 5 in phase 2, 9 in phase 3. Three
survived the first pass and each one was a real gap rather than an equivalent
mutant — a shared work item in a linked worktree resolving to the main tree, a
message half nothing asserted, and the gate going silent for any session
sitting in a subdirectory. Three cases exist because those mutations survived.

## A stated failure direction

**`chain_check.py` — neither. It cannot move a verdict.** The change replaces
one sentence with another and returns the same `([], why)` in the same
branch; a defect in it is a confusing sentence, never a wrong pass or a wrong
fail. That is why this answer was taken over the one that would have made the
local run report *declared*: the cheaper mistake is the one that has no
verdict to get wrong. `spec.md` §*The sharp question* carries the argument.

**`mode-gate.py` — blocks more, and deliberately.** It stops a command that
would have gone through, in a repository that has `seal/` and no `Mode` row.
A wrong deny costs one prompt in a session and is recoverable by approving the
next attempt. The wrong allow it replaces is not recoverable in the same
sense: a monorepo's review records get committed, every clone carries them,
and the way back is a documented command sequence somebody has to know exists
— which is the state #151 was reported from. It also cannot become an outage:
after the first denial in a session the decision degrades to `ask`, after the
`ask` it degrades to silence, and a marker that cannot be written counts as
already asked, so no environment can be denied twice in a row and none is
prompted for a whole session. The middle clause is round 1's: the decision
degraded to `ask` and then stopped degrading, which on a per-command gate is a
prompt on every command and is the outage this paragraph claimed it could not
become.

## A prompt budget

**Two prompts per session per repository — one deny, then one `ask` — and
only while the `Mode` row is absent. Zero after `seal mode` has been run once,
and zero forever in a repository with no `seal/`.**

Counted by running the gate rather than by reading it, 2026-09-08, twenty
ordinary Bash calls per session and two sessions in each repository:

| The repository | Session 1 | Session 2 |
|---|---|---|
| `seal/`, no `Mode` row | 1 deny, 1 ask, 18 silent | 1 deny, 1 ask, 18 silent |
| `seal/` with a `Mode` row | 20 silent | 20 silent |
| no `seal/` at all | 20 silent | 20 silent |

**The first count was wrong, and the reason is worth keeping.** This section
read *one deny per session per repository* while the code produced one deny
and then an `ask` on every command for the rest of the session — nine of ten
ordinary calls, measured in round 1, where the sibling gate was silent on nine
of the same ten. The gate had moved from the commit to every Bash call and the
properties bounded by *how often does somebody commit* were not re-derived
against *how often does somebody run a command*. The sibling has an early
return for a command that is not a commit; this one has none by design, so the
budget has to be spent rather than bounded by what the command happens to be.

It matters more than an extra prompt because the way out, `seal mode`, is
itself a Bash call: a run that cannot answer an `ask` could not reach the
command that ends the asking, so every command it tried was stopped rather
than one. Both prompts are spent once now and the rest of the session is
silent.

It arrives on the session's first Bash call. That placement is the budget
argument rather than an accident: the count is identical at the commit,
because the budget is per session and not per command, but at the commit the
question lands beside the review arm's, at minute thirty, on a session that
may have nobody at the keyboard. On the first Bash call it lands in the batch
`skills/implement/SKILL.md` §1 says a session collects before it starts, which
is where this project wants questions.

**Per session per REPOSITORY, and in local mode that is the clone.** One root
under the common git directory serves every work tree, so the two markers are
keyed to the folder the question is about rather than to the tree the command
came from. Keyed to the tree, one session was denied once per worktree about
one folder. Shared roots stay keyed per tree, because each work tree carries
its own `<repo>/seal/` and each is a separate root nobody chose a mode for.

**What each one costs when nobody is at the keyboard.** The first is a deny,
which returns the turn to the model with three named options; an unattended
run cannot answer it and stalls until the next attempt, where the decision is
`ask` and approving proceeds. So the worst case for an unattended run is one
stalled command and one approval, not a halt.

**And a cost that is not a prompt: one `git` process per Bash call, in every
repository on the machine.** Measured the same day with a logging `git` on
`PATH`, one `ls` payload: this gate makes one `git rev-parse --show-toplevel`
in a repository with no `seal/` at all, where `commit-review-gate.py` makes
none — it returns before resolving anything for a command that is not a
commit. In a repository that has a root and no row it is two, and it stays two
on the calls after the budget is spent, because the root is resolved before
there is anything to say. Wall time for the gate alone, median of twelve:
36.4 ms against the sibling's 26.7 ms on this machine.

That cost is the price of the placement argued for above, and it is stated
rather than removed. Removing it means resolving the root once per Bash call
for all three gates instead of once each — `hooks/optin.py#repo_root` carries
a RIDER counting exactly this class, and this adds a caller to it. That is a
change to three gates at once and it is not this branch's.

**Why nothing cheaper reaches the same guarantee.** Three cheaper things were
tried and each is in the tree, doing the part it can do. The bootstrap now
records the answer, so a repository that went through it is never asked here
— that removes the prompt for every correct path. The preset block names the
condition before it instructs the write, so a session reading carefully never
reaches the state. Neither of those observes anything: both are instructions,
and #151 is a report of instructions being correct and unread. A `SessionStart`
notice was weighed and costs zero prompts, and it cannot meet the first Done-
when at all — in a fresh repository the root does not exist at session start,
so the notice fires only in the session AFTER the one that opted in and
committed. The question this gate asks is the one that must not be answered
by a default: `templates/config.md` states that the `Mode` row has no default,
because a fixed `shared` writes a lie into every local-mode repository.

**There is no waiver token, and that is a budget decision too.** The two arms
of the commit gate each carry one because a change can honestly be exempt from
a check. Setup cannot, the way on is a single command, and a token would build
the standing exemption `docs/review-chain-spec.md` refuses.

## Platform honesty

**Executed on macOS 15.5 (darwin 25.5.0), Python 3.12, git 2.x.** Everything
below is what could not be tried here.

- **Windows.** Nothing on this branch was run on it. Three places are where a
  difference would show: `git worktree list --porcelain`'s paths, which
  `round_record.py#repo_of` compares through `os.path.realpath` rather than
  by string; the marker path in `mode-gate.py#already_asked`, which is built
  the way its sibling gate builds one and is covered by the same
  session-id-escape case; and the em dashes in both prompts, which reach the
  console through `hooks/console.py#to_utf8` for the reason that module owns.
  The repository's own CI has a Windows leg and will run all of it.
- **Linux.** Not run here either; CI covers it.
- **A repository whose git directory is elsewhere** (`--separate-git-dir`, a
  submodule) **was built in round 1, and this bullet used to say the opposite
  of what it found.** It read: the root resolution asks `git worktree list`
  instead of taking `dirname` of the common directory, so the untested case is
  the one the design avoids relying on. Executed, it is the case the design
  got wrong. `git worktree list --porcelain` prints the GIT DIRECTORY as the
  worktree path when the tree was separated from it, with no `bare` line to
  tell it by, so the caller's real tree was not in the list it belongs to and
  a path every later `git -C` refuses was named as the root. A bare clone took
  the same path. Both now compare the clone by common git directory, and a
  root that is not a work tree is refused rather than named. Not being able to
  try a case is not the same as the case being avoided, which is what this
  bullet had quietly turned into.
- **A console that is not UTF-8** was not exercised for the new gate's text.
  It goes through the same `console.to_utf8()` line every other gate uses.
