# review chain — behavior spec

Authority for `hooks/commit-review-gate.py` and
`hooks/review-history-guard.py`, and for the cycle contract the `code-review`
and `legacy-parity` skills participate in. Update spec and code together.

**Two words, and they are not the same size.** A **cycle** is the mark's own
unit: one mark written, one commit, one mark gone stale. A **review run** is
the whole thing a work item goes through — up to five rounds, ending at a pull
request. A cycle is what the hook counts; a review run is what a person means
by "the review". Both were spelled "cycle", and a bound stated in one unit
read as a bound in the other.

## The cycle — the mark's unit

```
changes accumulate → review runs → reviewed-HEAD mark written → commit allowed
commit moves HEAD  → mark no longer matches → next cycle starts unreviewed
```

- **Marks**: `<git-dir>/specseal-reviewed` holds the reviewed HEAD SHA,
  written by the review orchestrator as the `code-review` skill's closing
  step. In a ported repo, `<git-dir>/specseal-parity` holds the HEAD an
  actual comparison against the original was made at, written by the
  `legacy-parity` skill. Living under `.git/` keeps both uncommitted and
  per-worktree (each worktree has its own git-dir — no cross-worktree false
  sharing).
- **One review per cycle**: fixes made after the review, before the commit,
  do not re-arm the gate. Re-review is the user's call. The parity mark
  follows the same cycle rule.

## The review run has a bound, and an end

Rounds are capped at **three**, and at **five while a 🔴 is open**.

Three is the rule. A fourth round is normally not another finding; it is the
loop failing to converge, and that is a different problem — the same reading
the 3+ Fix Rule gives a bug that keeps moving.

The exception exists because the cap counts rounds and rounds are not all the
same thing (#51). A round that turns up a defect nobody had looked for is the
shape the cap was written for: stopping is right, because something structural
is being missed. A round that turns up a **regression the last fix made** —
coordinate named, patch already run — is not. Stopping there hands over a
branch with a known open blocker and no question for anyone to answer.

| Bound | When |
|---|---|
| three rounds | the ordinary case, and the only one for 🟡 and ❓ findings |
| up to five | **only while a 🔴 is open**, and only to close it |
| stop regardless | a round opens a new 🔴 at the same site as the one it was closing — that is the structure signal, whatever the count |

**Five is a ceiling, not a target.** The moment the last 🔴 closes, the run
ends; unused rounds are not spent on 🟡 findings. Those go to
`seal/follow-up.md` or the tracker with an answerer named, exactly as
they would at three.

🔴 is not a judgement layered on top of the cap. `code-review` already grades
by what a finding requires rather than by rank, and 🔴 means *blocks merge* —
so "a 🔴 is open" is a state the review already reports, readable from the
last round record's verdict table and its `Pass` checkbox.

### The bound has a floor, and a quiet round is where it stops

**Stop when a round finds nothing that leaves the root and nothing that
crashes.** Whatever else it found is deferred with a named answerer, or becomes
an issue — the same homes the table at the end of this section gives any other
leftover.

The numbers above are a ceiling and say nothing about when to stop under one,
so the cap was spent like a budget. #81 ran seven rounds: rounds 1 through 4
each found something that loses a record, and rounds 5, 6 and 7 found none of
either kind. That is roughly an hour of agent time on the flat part of the
curve, and the curve is not one chain's luck — the most expensive round in the
flow log (63 tool calls) was also the most productive (four 🔴), and cost per
finding rose in the late rounds, where the reviewer was searching a diff it had
already read three times.

Nothing new has to be measured for it. The evidence is the round's own verdict
table, which already separates what needs a fix from what does not, and the
answer goes into `round-N.md`'s `| Loses a record or crashes |` row — the
reviewer's own, given in a line of its own, exactly as `Needs a fix` is.

**A first round is never optional, and the floor does not make it one.** #104
looked small and cost four 🔴 in round 1, three of them losing a record or
sending a person down a path that does not work. What the floor makes optional
is the round after a quiet one.

**This is not the cap's arithmetic.** The next subsection carries a rule that
reads like this one said twice, and the two decide different things.

| Rule | What it decides |
|---|---|
| A round that opens nothing needing a fix does not consume the cap | whether a round that has already run counts toward three or five |
| Stop when a round finds nothing that leaves the root and nothing that crashes | whether the next round is spawned at all, with the cap nowhere near spent |

They also reach different rounds. A round that opened nothing needing a fix has
opened nothing that loses a record either, so it meets the floor as well. A
round that meets the floor may still have opened a 🔴 in a line a person reads,
and that round consumes the cap and ends the run in the same breath.

**The verifying round still runs.** The floor ends the finding rounds, not the
run's obligation to have somebody read its last set of fixes. A record that met
the floor is followed by at most one more round record: the verifying round
defined next, at the diff of the fixes that closed it. A second one is the run
carrying on past its own stopping rule.

### The last round verifies, and what it verifies is a diff

A run ends with a **verifying round**. It is spawned after the previous
round's fixes are committed, its target is the diff of those fixes, and its
job is the answers rather than new findings: for each verdict the last round
recorded as closed, is it actually closed.

That is what a round is already good at. `code-review` says an axis marked
clean in round 1 can be broken by the fixes made for round 2, and that
inheriting the verdict is how it goes unseen. The verifying round applies the
same sentence to the last set of fixes, which is the one set that rule never
reached — see *Two records* below for what it cost when nothing did.

| | A finding round | A verifying round |
|---|---|---|
| Target | the branch, or what the prompt narrows it to | the diff of the previous round's fixes |
| Asks | what is wrong here | is each closed finding actually closed |
| Ends the run | never on its own — its own fixes are unopened | when it opens nothing needing a fix |

**A round that opens nothing needing a fix does not consume the cap.** The cap
counts rounds that found something, because it exists to stop a loop that is
not converging, and a round that finds nothing is the loop having converged.
That is the distinction the numbers above could not make: a round that found
nothing and a round whose fixes nobody read looked identical to them, and the
run ended at both.

Nothing here can loop, and it is worth saying why rather than adding a second
bound. A verifying round that opens something IS a finding round and consumes
the cap like any other. A verifying round that opens nothing is by definition
the last one, because the run ends at it. There is no third case to run away.

What it costs is one extra spawn per work item, on a surface that is a diff
rather than a branch — the cheapest round of the run. What it does not cost is
a change to the numbers above.

**This is not the rule that a round has to find nothing.** A verifying round
that raises a 🟡 the smith answers with grounds has opened nothing needing a
fix, and the run ends there. The condition is *this round wrote no code
nobody read*, which is narrower than *this round was silent* and is what keeps
the bound a bound.

At the bound, or earlier when a round returns nothing blocking, the change
ends the same way whether or not everything was resolved. Nothing is dropped;
each kind of leftover has a home that outlives the session:

| What is left | Where it goes |
|---|---|
| A finding the smith fixed | the diff |
| A finding the smith answered with grounds | `round-N.md`, with the grounds |
| A finding neither fixed nor answered | `seal/follow-up.md`, and named in the PR body |
| A decision only a person can make | `seal/specs/<item>/questions.md`, and named in the PR body |
| An original whose behavior is plainly wrong | both texts side by side per `legacy-parity`, and named in the PR body |

Then the broad gate runs once, and the change opens as a pull request.

**The chain ends at a PR, never at a merge.** Those are two mistakes at the
same spot. A run that stops at a report leaves finished work where nobody
will find it — worst when nobody was watching, which is exactly when a run
goes long. A run that merges has decided something that was never its to
decide; the commit gate asks precisely because approving is a person's act.
Between them sits the PR: complete, reviewable, and waiting.

A PR opened with open items named is the correct end state, not a failure to
finish. What makes it correct is that the items are *named* — an unresolved
finding written into `follow-up.md` and quoted in the PR body has been handed
over. The same finding left only in a session's memory has not.

## Two records, and what each of them says

The mark and the round record are both "this was reviewed", and they are not
interchangeable. Reading one for the other is how three branches came to have
no readable review state at all.

| | `<git-dir>/specseal-reviewed` | `seal/specs/<work-item-id>/rounds/round-N.md` |
|---|---|---|
| Says | **this tree, right now** is reviewed at this HEAD | **that SHA, back then** was reviewed, and what came of it |
| Lives | under the git directory, per worktree | in the tree, committed |
| Travels | nowhere — not to CI, not to another worktree, not to another machine | with the branch, into the diff, into CI |
| Ages | goes stale the instant HEAD moves, by design | never — it names the SHA it is about |

**The mark cannot be committed.** It asserts something about the current HEAD,
and committing it moves HEAD, so the assertion is false the moment it lands.
That is not a limitation to work around; it is what makes the mark honest
about a moving tree.

The consequence is that the mark can answer *may this commit go through* and
nothing else. It cannot answer *did this branch pass review* — and that is the
question someone holding several unmerged branches actually has. Measured: three
branches on this repository had each run review rounds, each carried fix
commits, and none of them could be told apart from an unreviewed branch by
anything in git. The verdicts existed only in agent reports, which end with
the session.

So the durable half is the round record, and the passing half of it is the
`Pass` checkbox (`docs/review-handoff-protocol.md`). The last round's checkbox
speaks for the whole review: earlier verdicts are not archived, every one of
them needs an answer in the round that follows, so nothing can be open in
round 1 and absent from round 3.

**That closes the findings and says nothing about the answers**, and the two
are not the same claim. A finding is closed by a fix, the fix is written after
the round ends, and the round that follows is what opens it. Every round has
one — except the last, whose fixes are written by the session that then ticks
its box.

Measured on two consecutive work items here (#33). Round 2 of the first found
**seven** defects inside round 1's own fixes, which is the entire hit rate on
the one set of fixes anybody looked at, and round 2's fixes then went in
unread. The work item after it recorded the same ending in a comment
(`seal/specs/1788184145-…/rounds/round-3.md`): four findings, fixed by the
orchestrator, opened by nobody, `- [x] Pass`.

So the record carries a second field, `| Fixes checked by |`, and it names a
later round, `no fixes to check`, or `nobody — <why>`. A round cannot be its
own checker, because only a number above its own is accepted and that round's
own `Target SHA` has to be later than this one's, and the pull-request check
refuses every claim git can contradict.

`nobody` with its reason is refused nothing on any record but the last. That
is not a contradiction inside one file, and a check that fails for an honest
disclosure teaches people to write none — the reasoning `unverified_check.py`
already runs on. On the run's LAST record beside a checked `Pass` it does
fail, for a work item begun on or after the cutoff, because that pair is the
review claiming to have passed rather than disclosing anything. The refusal
table under §`Fixes checked by` holds both halves and what each costs.

The field records the state. What keeps `nobody` rare rather than routine is
the verifying round, which is the run's own shape and sits with the bound
above.

## Registration — gates run in groups, not one process each

`hooks/hooks.json` registers `hooks/dispatch.py <group>` per event, and the
dispatcher calls each gate in that group inside one interpreter. A gate is
still a standalone script — that is how it is tested and debugged — but on a
live tool call it does not pay for its own Python startup. Adding a gate means
adding it to `GROUPS` in `dispatch.py`.

When more than one gate in a group returns a decision, the strictest wins
(deny > ask > silence) and **every** reason is kept in the merged text: a gate
that was overruled still has something the user needs to read. A gate that
raises is skipped and the rest of the group still decides — a crashing gate
must not block a tool call.

## commit-review-gate (PreToolUse, Bash)

The hook carries **two opt-ins, evaluated independently**. Each has its own
mark, its own waiver token and its own silence rules, and neither is nested
behind the other: one arm being satisfied never suppresses the other's prompt.

They are no longer declared independently, and that changed at 0.10 without
anyone noticing. The migration config lives at `seal/parity.md`, so
writing it creates `seal/` — the directory whose existence is the review
opt-in. A repository with a migration config and no review opt-in cannot be
built through any address the plugin documents or writes.

This paragraph used to claim the opposite, and the claim stayed true only
through the pre-0.10 `docs/parity.md`, which no user-facing document has ever
named and which nothing in the plugin has ever written. That read was removed
rather than documented, on the grounds that the address had no
users; removing it is what made the collapse visible. A repository that wants
the parity arm and not the review arm waives the review arm per command with
`[no-review]`, which is what the tests here do.

| Condition | Decision |
|---|---|
| not a `git commit` command | silent |
| neither opt-in applies | silent — a globally installed plugin must not nag unrelated repos |
| the command names a `-C` the gate cannot resolve | **stopped** — see below |
| every applicable mark equals current HEAD | allow |
| no session id in the payload | **ask** — nowhere to record that the choice was put up, and a deny would then repeat forever |
| otherwise, first time this session meets it in this repo | **deny**, whose reason **instructs the model to put the choice up** with AskUserQuestion, naming both ways on for every arm that fired |
| otherwise | **ask**, which is the harness **putting two buttons to the user** — every missing mark named at once, and approving IS the waiver |

Those last two rows are different acts and the word "asks" covers both, so it
is not used for either on its own. A `deny` addresses the **model**: the hook
cannot render a dialog, so it spends its reason on instructions and hands the
turn back. An `ask` addresses the **user**: the harness renders two buttons
that the model never sees, and declining is a bare "No".

### Which repository, and what happens when it cannot be read

The repository judged is the one the command commits **into**, not the one the
shell sits in. `git -C <path> commit` moves git without moving the shell, so
the directory comes from the command and falls back to `cwd` only when the
command names none. Repeated `-C` compose. A command committing into two
repositories is judged for both.

The shell moves too, and reading only `-C` missed it. `cd <path> && git commit`
leaves the shell somewhere else before git runs, so the gate judged the
directory the session started in — measured wrong in both directions, and in
the one that matters a routing declaration found in the session's own
repository silenced a commit landing in a repository that had never given that
answer. There was no moment on that path at which anyone could
have typed a waiver or clicked a prompt. Every directory a command can commit
into is resolved from the command, `cd` included.

Which directories it reaches depends on the operator joining the segments.
`&&` and `||` are opposites: `&&` runs the commit where the `cd` arrived,
`||` runs it only if the `cd` failed, which is where the shell already was.
The pipe and background operators are a third case — they open a subshell, so
a `cd` on one side of them does not move the shell the commit runs in at all.

| The command | What is judged |
|---|---|
| `cd X && git commit` | the repository holding X |
| `cd X ; git commit` | both — `;` runs the commit whether the `cd` succeeded or not, so a failed `cd` leaves it in the session's own repository |
| `cd X \|\| git commit` | both — the session's own repository and X |
| `cd X \| git commit`, `cd X \|& git commit`, `cd X & git commit` | both, and for a different reason: the commit runs in a subshell that never left the session's own repository, and a shell told to run a pipeline's last stage in the current shell (`shopt -s lastpipe`) does land in X |
| `cd N \|\| cd B && git commit` | both N and B — the second `cd` is skipped whenever the first works |
| `cd X && git commit`, where X is inside the session's own repository | that one repository, with the verdict and the prompt unchanged |

A segment joined by one of those operators may never run, so the directories
in front of it stay candidates past it. Reading only the operator that
*follows* a segment loses that: `cd N \|\| cd B && git commit` kept B alone,
and where B carried a declaration the commit went unjudged.

**Where an operator is written does not change which operator it is.** An
operator at the end of a line — the ordinary way to write a long command — put
the line break directly behind itself, and a run of shell punctuation reads as
a single token, so `cd X \|\|` and a newline arrived as one operator that
matched none of these rules. The line break is read as its own separator, the
first operator after a segment is the one that binds it, and a backslash
before a line break is a continuation whose two characters both go.

**Only what the shell would EXECUTE is read as commands.** A heredoc body is
data the shell feeds to a command on stdin, so the gate drops it before
splitting, exactly as it drops a comment. Writing a script and then committing
it is ordinary, and every newline being a separator meant a `cd` on the second
line of `cat > run.sh <<'EOF'` moved the reader's shell — the commit after the
terminator was then judged against a repository the shell never entered, with
the session's own directory absent from the candidates altogether. A `<<`
inside a comment opens nothing, `<<<` is a herestring and opens no body, and a
body whose terminator never arrives runs to the end, which is what the shell
does with one. Neither does `$((…))` open one: the `<<` in `n=$((1<<2))` is an
arithmetic left shift, and reading it as a redirect took `2))` for a delimiter
and dropped every line after it looking for a match no line makes — so a
commit written below it did not arrive misjudged, it did not arrive at all. This is a JUDGMENT read; the scan for a waiver token still sees
the command as written.

**A failure branch waits for the operator that runs it.** `cd X && make \|\|
git commit` commits where the shell is when the `cd` fails, and that is the
directory the session started in. Reading only the operator immediately after
a segment lost it as soon as anything stood between the `cd` and the `\|\|`.
The directory a failed command leaves the shell in is carried until something
consumes it, and a failure branch nothing ever reaches is not reported — which
is what keeps `cd X && git commit` answering for X alone.

**Two operators consume one, not one.** `\|\|` runs its right side only from
the failure branch; `;` — and a newline, which is the same operator written
differently — runs it from both, which is why `cd X ; git commit` answers for
two repositories where `cd X && git commit` answers for one. Only `\|\|` was
treated as a consumer, so the session's own repository dropped out of the `;`
answer and a routing declaration in X silenced a commit that could land in
either. `bash -c 'cd /no/such/dir ; pwd'` prints the directory it started in.

**The reader enumerates what it understands, not what moves a shell.** Where
it met a construct it did not model it answered *the shell stayed where it
was*, and that is a confident answer rather than an absent one: a stop where
the session's own directory needs review, and a silence where that directory
carries a declaration and the commit lands elsewhere. Measured on seven
commands, five leaked — a `cd` inside a function body, a sourced script, an
`eval`, a `pushd`, and a loop, with `command cd X` a sixth found alongside
them. Filling the parser in is not the fix; the list of constructs that move a
shell is not one anybody finishes, and every one still missing resolves
confidently to the wrong directory.

So a segment the reader can read as a simple command — a literal command word
and its arguments — leaves the shell where the reader computed it, and every
other segment leaves it **unreadable**, which is the stop below. What is
enumerated is therefore the shell's reserved words, which are a closed and
documented part of its grammar, rather than the open list of things that
relocate a shell. The remaining error changes direction with it: a construct
nobody added to the understood set reads as not understood, and stops.

**Exclusive branches are not walked as one.** A directory reached by a branch
that succeeded is not somewhere the alternative branch then runs, so
`cd build \|\| cd dist` reaches build or dist and never `build/dist`. That
composed path is not merely extra: it exists nowhere, so it resolves to no
repository, and a target that resolves to nothing is reported as unreadable —
which returns before the real verdict is used and puts a directory the user
never typed in the prompt. Sixteen branches produced 65536 such candidates.
What is still bounded only by a bound is every shape whose reachable
directories genuinely multiply — a chain of pipe stages, one of `;`, and one
alternating `&&` and `\|\|`. Those directories are all real, so the bound limits how much
answering the reader will do rather than correcting anything; past it the
command reads as one whose directory could not be computed.

The last row is what keeps this cheap. Where every directory a command reaches
sits in one repository, the operator does not matter and neither does the `cd`:
the common `cd src && git commit` costs exactly what it cost before, compared
byte for byte against the parent commit. Prompt volume is the problem reading
the command was added to reduce.

The gate reads `tool_input.command` **before the shell expands it**. So a `-C`
whose value is a shell variable arrives as the literal characters `$WT`, names
a directory that does not exist, and resolves to no repository. A path that was
simply typed wrong looks identical from here — there is no reading of the
command that tells them apart.

That target is not a repository the gate checked and found clean. It is a
repository the gate never saw, and until the release that closed it, both
produced the same nothing. Every agent in that release session was instructed to
commit with `git -C "$VAR"`, and every one of those commits passed a gate that
had looked at nothing.

| What the gate has | What it does |
|---|---|
| a `-C` it resolved to a repository | judges that repository — its opt-in, its marks |
| a `-C` it could not resolve, in a session whose own repository opted in | **stops**: deny once per session per repository, then ask |
| a `-C` it could not resolve, anywhere else | silent — the plugin has no standing in a repository that never opted in |
| no `-C`, and `cwd` is no repository | silent — there is no repository and no command naming one |

The session's own repository decides *whether* the gate speaks, never *what is
true* of the target. Judging an unresolved target against the session's marks
would answer for a repository the commit may never touch, which is the defect
`-C` parsing was added to fix.

The two ways on are ordered deliberately. The first is to write the path out,
because that is what lets the gate reach a verdict at all; `[no-review]` is
second and works exactly as everywhere else.

#### A `cd` the gate cannot read

The rest of the shell is deliberately not implemented. A `cd` whose
destination cannot be computed is treated as one that cannot be computed,
rather than followed to a guess:

| The `cd` | Why it cannot be read |
|---|---|
| `cd "$WT"` | the command is read before the shell expands it — the same fact that leaves a `-C` variable unresolvable |
| `cd /tmp/x*`, `cd {a,b}` | names a set of paths rather than one |
| `(cd X && git commit)` | the closing parenthesis decides whether the commit runs inside the subshell or after it, and finding that reliably is a shell parser. The `git commit` itself IS read — a subshell opener is taken off the command word and a closing parenthesis off the subcommand, because `(git commit)` commits for real and used to be invisible to the gate entirely |
| `cd -` with nothing behind it | there is no previous directory to return to |

Each takes the treatment the table above gives an unresolvable `-C`: a stop
where the session's own repository opted in, silence anywhere else. It is that
same partition and not a second one. A hook that follows a construct it half
understands is back to being confidently wrong, which is the failure this
section exists to describe — and the same-root collapse is what limits what
the honesty costs, since a destination inside the right repository changes no
verdict.

`hooks/worktree-guard.py` reads a command the same way, because the parsing is
shared and a session that walks to another repository to switch a branch there
was judged against the tree it started in. Its answer for a destination it
cannot read is the opposite one: it keeps judging the session's own tree,
which is where today's answer already was. What that guard protects is a tree
two sessions would share, so stopping is not available to it and going silent
would be a fail-open.

### Why a deny, and why only once

A hook returns allow/deny/ask and nothing else, and the harness renders an
`ask` as two buttons the model never sees. Declining is then a bare "No", and
the user who wanted the *other* way on has to retype the command themselves —
the yes/no shape `implement` §1 rejects, still present after the reason string
was made to name both continuations. Denying gives the model the turn back and
spends the reason on the question, which is the shape measured in
`hooks/review-skill-gate.py`.

Firing once per session per repository is what keeps that from being a trap.
The marker is `<git-dir>/specseal-commit-choice/<session-id>`, with the session
id reduced to its basename first — it names a file, and a malformed id with
separators in it otherwise escapes the directory. An unwritable marker counts
as already asked, since one missed question beats a deny nothing can get
past. Every attempt after the first meets the plain `ask` — which is
also the answer for an environment with nobody to ask: one extra round trip,
then today's behavior.

**Both arms, one call.** When both arms fire, the reason asks for two
questions inside a single AskUserQuestion call rather than one question with
four combined options. The arms are waived independently, so combining them
makes every label carry two facts and multiplies the option count; one call
still costs one interruption.

### Review arm — opt-in: `seal/` at the repo root

| Condition | Decision |
|---|---|
| `[no-review]` in the command | silent (explicit skip, visible in history). Typed in front of it: `: '[no-review]'; git commit …` — see below |
| `specseal-reviewed` equals current HEAD | satisfied |
| otherwise | contributes an ask |

The marker is decided when the work starts, not discovered at the commit
(`implement` §1) — and until the release that added `routing.md`, nothing
recorded it, so the gate had to
re-derive the answer at every commit and could only ask. The branch that
submitted to review was interrupted at every step; the branch that skipped
review was silent. The incentive ran backwards, and it ran backwards for
exactly the work the chain exists to serve.

Approving is still per commit and the marker still per command. What changed
is that the routing answer now has somewhere to live, and the check it
silences now happens at the pull request instead. See below.

#### Where the marker goes, which is not where it is read

`has_marker` finds a bare word anywhere in the command. Where it can be *typed*
is a separate question, and the prompts answered it wrongly for three releases
After `git commit`, a bare word is a **pathspec**, so
`git commit -m x [no-review]` is rejected by git before the gate's advice can
help. The gate stopped the commit, the escape it named failed, and approving
the prompt was left as the only thing that worked — the outcome the wording
exists to offer an alternative to.

Measured in three shells:

| Form | bash | `zsh -c` | interactive zsh |
|---|---|---|---|
| `git commit -m x [no-review]` | rejected (pathspec) | rejected | rejected (unmatched glob) |
| `git commit -m x  # [no-review]` | commits | commits | **rejected** — `#` is not a comment there, so the marker globs |
| `: '[no-review]'; git commit -m x` | commits | commits | commits |

So the advised form puts the marker in front, inside a no-op `:` command. The
shell discards it, git never sees it, and the word stays in the command where
shell history keeps it — which is the whole point of a waiver that is supposed
to be visible.

`tests/test_the_waiver_can_be_typed.py` runs the advised form against real git
in every non-interactive shell present, and pins the rejected form too. The
interactive-zsh row is recorded rather than run: an interactive shell in CI
needs a tty and sources a user's rc.

#### The declaration, and where the check went instead

The gate reads `seal/specs/<work-item-id>/routing.md` before it reads anything
else. Where a declaration is in force the review arm stays silent — for
**either** answer, because the routing question was answered before the first
edit and asking for `[no-review]` as well is asking for the same answer twice.

| The declaration says | At the commit | At the pull request |
|---|---|---|
| through the review chain | silent | a committed `rounds/round-N.md` is required, every commit its `Target SHA` names being REACHABLE — an ancestor of HEAD, or of the branch `routing.md` declares — its last round's `Pass` **checked**, that claim consistent with its own verdict table, and its `Fixes checked by` naming a checker the repository can confirm. A record this pull request does not touch keeps every requirement except reachability: its commits are expected to be gone, and the review it records was enforced at the pull request that added it |
| straight to the PR | silent | nothing required; the declaration is printed |
| nothing readable, or no file | today's behavior — deny once, then ask | pass, with a notice saying nothing was checked |

##### `Pass` has to be checked, and a draft is the way to open one that is not

The chain runs **before** the pull request in this design — smith, then
warden, then the PR — so a checked `Pass` is the normal state of a work item
by the time one opens. An unchecked one means the chain was skipped or has not
finished, and neither is a state to ask for a merge in.

| The pull request | An unchecked `Pass` |
|---|---|
| ready | fails. The review did not finish, and the pull request says it did |
| draft | passes. A draft is not a request to merge, and a review still running has to have somewhere to be |
| not visible to the check at all | judged as **ready** |

That last row is the decision, and it is deliberately the strict one. The
draft state is read from the event payload the code host writes to disk, so a
run outside a pull-request event — a session running the check by hand — has
no pull request to read. Judged as a draft, "no pull-request context" would
become the quietest way past this check that exists, quieter than
`[no-review]`, which at least stays in the command where history keeps it. An
override flag was considered for the same case and rejected for the same
reason: an escape anyone can type is the same hole with a name.

What it must not do is pass in silence, so the check prints which state it
assumed and where it read that from, on every run.

**What it still cannot see** is whether the review was any good. A checked
`Pass` is a claim made by whoever wrote the round record. What is refused is
the claim that contradicts the table underneath it — the same limit the
commit gate has always carried.

##### `Fixes checked by` has to name a checker the repository can confirm

The draft excuse does not reach this row. `Pass` is excused in a draft because
a review still running has not reached its verdict; a record naming a checker
it does not have is wrong at every stage of a run.

| The cell says | The check |
|---|---|
| the row is absent | **fails.** Adding it is always available to the author, which is the line this check has always drawn |
| `round-N`, above this record's own number, that record is committed, and its own `Target SHA` is later than this record's | passes |
| `round-N`, at or below this record's own number | **fails** — the checker is this round, or one that ran before the fixes existed. That is the fixer certifying its own work, which is the state #33 measured |
| `round-N` above this record's number, whose `Target SHA` is the same commit this record's names or an ancestor of it | **fails** — the number is later and the review is not. Rounds are cheap to number and expensive to run, and a round that read what this round read opened none of the fixes that closed it. Where either row names two commits, the NEWEST on each side is what is compared |
| `round-N` naming a record git does not carry | **fails** — a claim git contradicts |
| `no fixes to check`, with no verdict cell closing on a fix | passes |
| `no fixes to check` beside a verdict cell reading a fix word | **fails** — a contradiction inside one file, the shape already refused for `Pass` beside an open 🔴 |
| `nobody — <why>` | prints on every run. **Fails** beside a checked `Pass` on the run's last record, for a work item begun on or after the cutoff below; passes everywhere else |
| `nobody` with nothing after it | **fails.** The reason is what makes the state readable; without it the cell records that something is missing and not what |
| anything else, `the session that wrote them` included | **fails**, naming the three values. Read loosely, a session's own name would pass as an answer, and that is precisely the state this field exists to refuse — the direction `CLOSED_WORDS` already takes for a verdict cell |

Two of those deserve their cost written down.

The first is `nobody — <why>`, and it is a disclosure rather than a claim. A
check that failed for an honest disclosure teaches people to write none, which
is the reasoning `unverified_check.py` already runs on, so the cell prints
wherever it appears and on any record but the last it is refused nothing.

What it may not do is stand beside a checked `Pass` on the run's last record.
That combination is the review saying it passed, and a run whose final fixes
nobody opened has not passed — #33 measured the one set anybody did open and
found seven defects inside it, which is every defect there was to find.

**The refusal reaches work items begun on or after the cutoff, and no others.**
The cutoff is a unix second, compared against the one in the work item's own
directory name, and its value is the id of the work item that added the rule
(`chain_check.py`'s `STRICT_FROM`). One number serves every repository: a fresh
install creates every work item after it, and a repository updating the plugin
has exactly its pre-existing items excused.

Why grandfather at all. A record written before the rule existed is usually
merged and has no honest repair — writing a `round-4.md` for a review nobody
ran fabricates one, and unticking `Pass` fails the ready-pull-request rule
instead. A check whose first production act is red on history nobody can fix
is a check people learn to skip, and skipping loses the records it could have
caught in exchange for the ones it never could.

What it costs is stated rather than left to be found: an old work item
reopened years from now still writes records under its original id and stays
excused. That is taken knowingly, rather than closed with a second rule about
how old is too old.

Nothing after the cutoff is stuck. One verifying round at the diff of those
fixes closes it, and a round that opens nothing needing a fix does not consume
the cap — so the way out costs no round, which is what the failure says.

The second cost is the scope. This is read on **every** record, where `Pass` is
read on the last one alone, and the two differ because the two facts do:
`Pass` is a verdict on the whole review and the last round's speaks for it,
while this is a fact about one round's own fixes and every round has one.
Reading only the last record makes `round-N` unreachable — a checker has to be
later, and the last record has none. What that costs is a repository updating
the plugin: every record in a work item whose declaration the pull request
touches needs the row, not just the newest.

##### The fix surface — `Contract changes` and `New units`

Two more rows, read on every record the same way `Fixes checked by` is, and
for the same reason: every round has its own fixes. Issue #57 measured ten
regressions each traced to the fix that opened it, and the largest class —
four of ten — was a fix that changed a unit's contract while not every place
that contract reaches was revisited. The diff names the changed signature and
`grep` names the reach, which is why this can be a gate rather than a
question.

| The row | The check |
|---|---|
| `Contract changes` or `New units` absent, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| either row absent, work item begun before the cutoff (or with no timestamp prefix) | prints — the same grandfathering as above, keyed to `chain_check.py`'s `SURFACE_FROM`, whose value is the id of the work item that added the rows |
| `none`, with or without a reason after it | passes — `none — the fixes are not yet written` is the honest value while a round runs |
| `none — the fixes are not yet written`, on a record whose `Fixes checked by` names a `round-N`, work item begun on or after `chain_check.py`'s `ORDER_FROM` | **fails**, naming the row and the checker two rows above it. A later round opened these fixes, so they exist, and the cell contradicts its own file — the shape `no fixes to check` beside a `fixed` verdict already takes. Before that cutoff it prints |
| the same cell while `Fixes checked by` still reads `nobody — <why>` | passes. That is the state the ordering rule REQUIRES, and refusing it would refuse every correctly written record at the moment it lands |
| the same cell while `Fixes checked by` reads `no fixes to check` | passes — the arm reads a `round-N` and nothing else. This is the value the TERMINAL record of every run carries, and it is the one place the pair is not merely unrefused but wrong: a round that commissioned no fixes will never have any, so *not yet written* is false the moment it is written and nothing here says so. Whether the arm should refuse it too is open — the refusal would land on merged records whose repair is honest, unlike the `nobody` case |
| `none` with a reason the checker does not recognise | passes — see the limit below |
| an empty cell | **fails** on any record — a row that says nothing answers nothing, and an empty cell is always the author's to fill |
| a `Contract changes` entry (`;`-separated) carrying `unit → call sites` (`→` or `->`) | passes |
| an entry with no arrow, or an empty half | **fails** on any record, naming the entry — a unit without its reach restates the diff and leaves the measured failure's unchecked half unchecked |

**The pending arm is this branch's own damage repaired**, and it is worth
saying which way round that went. Before `ORDER_FROM` a record could be
written after its fixes and both rows filled from the start; the ordering rule
made *not yet written* the value every record now begins with, and nothing
required the second step. `says_none` accepts a reason, so an abandoned cell
read exactly like a finished one — a check reporting clean while something is
missing, which is the title of the work item that produced it.

**Its direction is `allow` for a reason the checker does not recognise, and
that is a deliberate exception to this document's `blocks more` default.** The
alternative is refusing an honest custom reason for its wording, and a rule
about which English sentences mean *not yet* is the enumeration over an
unbounded domain the arrow's and the comma's limits already decline. What is
caught instead is the measured failure: the template's own words, copied into
a record and left standing. The phrase lives in `chain_check.py` as `NOT_YET`
and `templates/sdd-round.md` prints that constant, so the two cannot drift.

**What escapes is wider than a rewording, and three spellings carry the
template's words UNCHANGED.** This paragraph declared the escape as a
rewording for a round, and it was measured over 23 cells and found narrower
than the behaviour (round 3's 🟡 5). `says_none` tests the first character
after `none` while `says_not_yet` strips `SEPARATORS` from both ends, so each
of these passes the cell as `none` and silences the arm:

| The cell | Why it escapes |
|---|---|
| `none ― the fixes are not yet written`, with U+2015 rather than the em dash | the leading space is what satisfies `says_none`, and the bar is outside `SEPARATORS`, so it survives the strip and stands in front of the constant |
| `none — the  fixes are not yet written`, with a doubled space | the extra space is INSIDE the constant rather than before it, so no widening of `SEPARATORS` reaches it |
| `none — nothing yet; the fixes are not yet written` | only a substring match reaches a clause before the phrase, and the substring match is exactly the mutation the prefix rule exists to refuse |

Only the first of the three is punctuation, so widening `SEPARATORS` would
close one and leave this section false about the other two — and it would
widen a constant four other readers in the same file share. The limit is
written down instead. What *this record passed* means is *its cell does not
carry the template's own pending words*, never *its fix surface is complete*,
and a session that spelled the cell any of these ways is not the session that
forgot it.

**The arm keys on `Fixes checked by`, so a session that leaves THAT cell
behind too is reached by nothing here** (round 3's 🟡 1). The value a
forgetful session leaves is `nobody — <why>`, which is the honest mid-run
state and the row above says why it cannot be refused — so the arm reaches
the session that filled the checker cell and stopped, and not the one that
filled nothing. What covers the second is `Fixes checked by`'s own check: it
prints a notice for `nobody` on every record, and refuses it on the LAST
record beside a checked `Pass`. A non-terminal record carrying `nobody` is
false by construction — a later record exists, and round N+1 reviews round
N's fixes — and nothing refuses that today. Keying the arm on the sibling
records instead would give it a second source of truth, which is the property
that makes the narrow key defensible in the first place.

Only the ABSENT row is grandfathered by `SURFACE_FROM`, and the pending arm
above has a grandfathering of its own that reaches a row which is PRESENT:
before `ORDER_FROM` the same cell prints instead of failing. A merged record
has no honest repair
for a missing row — writing reach rows for fixes nobody re-read fabricates a
review — where a malformed row's repair is formatting, which is always the
author's. One limit is recorded rather than parsed away: the arrow is found
by substring, so an ASCII `->` inside a backticked unit name reads as the
reach separator, and such a unit passes without its reach. `→` is the
spelling that avoids it — parsing code spans to close the gap would be an
enumeration over an unbounded domain, the closing the review skill's own
rules refuse. The rows are filled when the fixes land, by the session that has
the fix diff open, so their prompt budget is zero. What `New units` buys sits
with the verifying round: what it names is a finding surface — *is this
correct* — rather than a verification surface, because a unit the fixes
created has been reviewed by nobody.

##### The floor — `Loses a record or crashes`, and what may follow it

The floor is stated at the top of this document, and this is what the check
makes of it. The row is read on every record, like the two above and for the
same reason: every round has its own answer, and the run's stopping point is a
fact about the round that met the floor rather than about the last one.

| The row | The check |
|---|---|
| absent, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| absent, work item begun before the cutoff (or with no timestamp prefix) | prints — the grandfathering above, keyed to `chain_check.py`'s `FLOOR_FROM`, whose value is the id of the work item that added the row |
| `no`, or `yes — <what>` | passes |
| an empty cell, or a word that is neither | **fails** on any record — a word the check cannot read is never the reassuring reading, and `nothing anybody can see` is a sentence rather than an answer |
| `yes` with nothing after it | **fails** on any record — the cell then records that something was found and not what |
| `no`, with two or more later round records, none of them saying the run reopened and none whose verdicts closed on a fix | **fails**, naming the exit. One later record is the verifying round; a second is the run carrying on past its own stopping rule. A record whose own verdicts say `fixed` stops the count exactly as a reopening does |
| the ABSENT row, or the run that went past it, work item with no timestamp prefix | prints — `item_began` has no second to compare, so the cutoff is below it and those two are excused permanently. **The three malformed states above are not**: `stopping_floor` appends their errors without consulting the work item's age at all |

Only the ABSENT row and the run that went past it are grandfathered, and they
are grandfathered for different reasons. The first is the reason the rows
above are: the round is over, and a record written before the rule has no
honest repair. The second is one this document has not needed before — the
repair for a run that ran three rounds too long is a round that was never
spawned, which nobody can write now. A malformed row is refused at any age,
because formatting is always the author's.

**What the count counts, and why it is not simply *the records after this
one*.** A verifying round that opens something is a finding round, so its own
fixes need a reader, and that reader is a third record — which a blind count
refuses, making the only legal end to such a run unwritable. It did: the first
record ever held to this rule was this repository's own, and the sequence its
documents required could not be written. So the count stops at the first later
record whose `Needs a fix` says the run reopened, that record included. Every
record after a reopening answers to THAT round rather than to the one that met
the floor.

**And it stops at the first later record whose own verdicts closed on a fix —
a `fixed` cell — whatever its `Needs a fix` says.** The two rows answer
different questions: `Needs a fix` is the reviewer's, *what did I open*; the
bound needs *were fixes written that owe a reader*. They come apart in one
sequence, and it happened: the reviewer answers `no`, judging a 🟡 answerable
with grounds, and the orchestrator fixes it anyway because it ships — a false
count in a ledger fragment that `fold_ledger.py` copies into the shared file.
The row still reads `no`, the fixes exist, and a walk reading only that row
has no terminal record it accepts: the verifying round that reads the fixes
is a second uncounted record after the floor, and ending without it is
refused both ways, `no fixes to check` beside `fixed` and `nobody` beside a
ticked `Pass`. Measured on this repository's own seventh round. The record
already carries the fact in its verdict column, and the walk reads it there.
The direction is ALLOW, one record wider in that one sequence, and it is the
cheaper mistake: the other way to satisfy the old walk was rewriting `fixed`
to `answered` over fixes that exist.

##### `Needs a fix` — the row the bound above rests on

It has been in the record since draft 0.5 of `docs/review-handoff-protocol.md`
and nothing read it until the bound above needed it. It is the reviewer's own
line, copied into the cell after the colon, and it takes the floor's
vocabulary.

| The row | The check |
|---|---|
| `no`, or `yes — <what>` | passes. A reason after `no` is an answer too, and 30 of this repository's own records are written that way |
| absent, empty, or a value that is neither, work item begun on or after `NEEDS_FROM` | **fails**, naming the row and the bound that rests on it |
| any of those, work item begun before `NEEDS_FROM` (or with no timestamp prefix) | prints |

**This row is grandfathered WHOLE, where the three above grandfather only an
absent row, and the difference is the row's history rather than an
inconsistency.** The floor and the fix surface arrived with their checks, so a
row present on a later record was written by an author who knew one would read
it and a malformed value is carelessness. This row carried free text for three
releases with nothing reading it, so a value written before the check was
never held to a vocabulary at all — refusing those would fail records for a
rule that did not exist when they were written, which is what every
grandfathering here exists to prevent.

`NEEDS_FROM` may never be later than `FLOOR_FROM`. Between the two, the bound
above would rest on a row no record was required to carry, which is a run
failed for a cell nobody asked its author for.

##### The depth in `New units`

`New units` carries a second thing beyond the names, and it has a cutoff of
its own — `chain_check.py`'s `DEPTH_FROM`, later than `SURFACE_FROM`. A work
item begun between the two owes the row and not the depth in it: its records
were written when the row named units alone, and deriving a depth now for
fixes nobody re-read fabricates the answer.

| The entry | The check |
|---|---|
| `unit (depth 1)`, entries separated by `;` | passes |
| `none`, with or without a reason | passes, unchanged — the depth did not take the value a round with no fixes yet has to be able to write |
| an entry with no depth, work item begun on or after `DEPTH_FROM` | **fails**, naming the entry and showing the shape |
| an entry at depth 2 or above | **fails**, naming the entry and where the unit goes instead: deferred with a named answerer, or an issue |
| an entry below depth 1 | **fails** — it names no level the rule defines, and read permissively it sits under the bound |
| an entry carrying more than one unit or more than one depth — a comma list under a single `(depth N)`, or two markers | **fails**, naming the entry. One declaration covering two names says nothing about the second, and the comma is the spelling this row used before the depth existed |
| any of those, work item begun before `DEPTH_FROM` (or with no timestamp prefix) | prints |

**The refusal names the exit because a refusal that does not is a wall.** The
rule and its exit shipped one phase before this check, in that order and on
purpose: a session meeting *this unit may not exist* with nowhere to put it
stops the chain, which costs more than the unreviewed unit did.

What no check can see is a depth declared wrong — `(depth 1)` on a unit that
is really second-level. The rule is a declaration, and the verifying round
reading the `New units` surface is what looks at it.

One limit is recorded rather than parsed away, the mirror of the arrow's above:
the comma that marks a crowded entry is found by substring, so a comma anywhere
in the entry outside the depth marker is read as separating two units.
`` `get(a, b)` (depth 1) `` is refused, and so is
`` `helper` (depth 1) — adds a, b ``, where the comma sits in the reason rather
than in the name. An entry that needs a comma is written without one.

**The separator has the same limit, and it runs before both of the others.**
`;` splits `Contract changes` and `New units` before anything looks at code
spans, so a literal semicolon inside a code span splits the entry carrying it,
and the tail is refused for having no reach. The record that first hit this was
the one describing a change to how the separator is read — the entry recording
the limit is the entry that met it. Spell the character as a word. Because the
hygiene workflow runs this check on every pull request, a record written the
other way opens the pull request red.

Parsing code spans to tell any of the three apart is the same enumeration over
an unbounded domain the arrow's limit declines.

##### What ran the round — `Ran by`

A record says what the round was asked, what it found, and which commit it
read. It said nothing about what executed it, and that fact survives nowhere
else: the model is a spawn-time argument, and once the session ends it exists
only in a transcript. Measured — every segment of two consecutive work items
was metered and posted to a measurement log, and not one of those readings can
be attributed to a runner afterwards.

The cell names **two** things joined by the word `on` — `agent on model`.
Either half alone answers neither question the numbers raise: an agent without
a model cannot be compared against another run of the same agent, and a model
without an agent cannot be told apart from the orchestrating session's own
turns. The joining word is a word rather than a punctuation mark, which is
what keeps this row out of the separator limit above.

Read on every record, like the three above and for the same reason: every
round was run by something, and a work item whose rounds ran under different
runners is the comparison the row exists to make. A check reading the last
record alone answers it for one round.

| The row | The check |
|---|---|
| `agent on model`, both halves non-empty | passes |
| `unknown — <why>` | passes at any age — a project may genuinely not know, since agent definitions pin no model and a session spawning through another harness has no name for one |
| absent, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| absent, work item begun before the cutoff | prints — the grandfathering above, keyed to `chain_check.py`'s `RUNNER_FROM`, whose value is the id of the work item that added the row |
| an empty cell | **fails** on any record — a row that says nothing answers nothing |
| a bare `unknown`, with nothing after it | **fails** on any record — the cell then records that something is missing and not what, which is the refusal `nobody` takes for the same reason |
| a cell naming one thing — no `on` with whitespace on both sides, or a half that is empty | **fails** on any record, naming what the two halves are for |
| the ABSENT row, work item with no timestamp prefix | prints — `item_began` has no second to compare, so the cutoff is below it and that row is excused permanently. **The three malformed states above are not**: they fail for a work item named any way at all |

Only the ABSENT row is grandfathered, and the reason is sharper here than for
the rows above: nobody can recover what ran a segment whose session is over,
and a value invented now is worse than the blank, because a reading nobody can
trust reads exactly like one nobody took. A malformed row is refused at any
age, because formatting is always the author's.

**The row is the spawning session's, and that is a rule about where the value
comes FROM rather than about whose keystrokes fill the cell.** An agent is
told what it is, so a value it writes about itself is the value it was told;
the orchestrator is the party that chose the model. For a round record the two
coincide, because the orchestrator writes that file. For a build phase's
record they do not — the segment writes it — so the value is handed over in
the spawn prompt and transcribed, or filled in afterwards. What is refused is
a segment sourcing the value from its own idea of what it is.

**What no check can see is which of those two happened.** `ran_by` reads the
shape of the cell and nothing about where the value came from, so a
transcribed `specseal:smith on Opus` and an invented one are the same eight
words. The rule is a declaration, like the depth's, and the reader who looks
at it is whoever holds the spawn prompt beside the record — the orchestrator
at the round that follows, or the person reading the pull request.

This branch's own four phase records are the worked case, and they are the
mixed one rather than the clean one: the agent half and the model came from
the spawn prompt, and the version detail after it did not. That is what the
declaration looks like when it is only partly sourced, and no check reports
it. A round record has the easier job — the orchestrator writes that file and
chose the model — which is why the rule's difficulty is entirely on the phase
side.

One limit is recorded rather than parsed away, the same shape the three above
take and outside their sequence — those three are `Contract changes` and
`New units` parsing, and this row is parsed by neither:
a cell beginning with the word `unknown` is read as the unknown answer whole,
so `unknown on Opus` is an unknown carrying a reason rather than a pair whose
agent is not known. Nothing is lost by it — the model is still written where a
reader sees it — and telling the two apart would mean a rule about whether an
English reason may begin with `on`.

##### When the record was written — before the fixes it commissioned

`templates/sdd-round.md` says a record is written *right after it posts*, and
until this check nothing observed it. Measured twice in one release, four
minutes and two minutes after the fix commits those records commissioned, and
both times the reviewer's drafted replacement text lived only in a report and
the next segment rebuilt it from scratch. That is the failure a build phase's
own record was built to close, arriving on the review side of the chain.

**A record written late leaves no trace.** By the time the orchestrator writes
it the fixes have landed, so its verdict cells read `fixed at <sha>` — which
is exactly what a correctly written record looks like after its own update
pass. The two are indistinguishable in the file, and distinguishable in git.

**So the check reads the ADDING commit, never the last one.** A correct record
is committed with `open` cells when the round posts and updated when the fixes
land, so its LAST commit legitimately descends from the fix; refusing on that
would fail every well-written record. The commit that ADDED the file is the
distinguishing one.

Read on every record, like the four above and for the same reason: when a
record was written is a fact about that round, and every round has one. The
last record is the one **least** likely to be late, because nothing follows it
to commission anything — so a check reading the last record alone would read
the one record the defect cannot reach.

| The state | The check |
|---|---|
| the adding commit descends from a commit this record's own verdict names as the fix, work item begun on or after the cutoff | **fails**, naming the adding commit, the fix, and the row — keyed to `chain_check.py`'s `ORDER_FROM`, whose value is the id of the work item that added the rule |
| the same, work item begun before the cutoff (or with no timestamp prefix) | prints — the grandfathering `Fixes checked by` already uses. A merged record has no honest repair: nobody can commit it earlier now |
| the record added with `open` cells and updated to `fixed at <sha>` afterwards | passes. This is the correct shape, and the whole reason the ADDING commit is what is read |
| a verdict closing with `answered`, `withdrawn` or `not a defect` | passes, whatever commit sits in the cell — those close a finding and produce no code, so there is no fix the record could have been written after |
| a fix commit that is an ancestor of this record's own `Target SHA` | passes — the round already reviewed that commit, so it is a fix this round did not commission. Round N+1's record is committed after round N's fixes by construction, and reading those as commissioned would fail the second round of every run |
| a fix commit this repository cannot resolve | passes — after a squash that is the ordinary state of a reviewed commit, the reading `resolves_to` gives every other consumer |
| **a `fixed` verdict that names no commit at all** | passes, and this is the commonest of the pass states rather than an edge — measured across this repository's own records, 235 cells close with a fix word, 215 name a commit and **20 do not**. `\| fixed \|` and `\| fixed — round-2 read it \|` are house style, not malformed |
| a record DELETED and re-added on the branch | judged on the **latest** add, which is the only shape producing more than one. A stub committed on time, removed, and the real record written after the fixes is what makes a late record look early, and the version anybody reads was authored at the last add. What it costs: a record accidentally deleted and restored after the fixes is refused, and the failure names the restoring commit |
| a record with no adding commit in `<baseline>..HEAD` | passes — it arrived before the base, and nothing is claimed about it. The same *no claim* the reachability requirement already makes for a record the pull request does not touch. This is also what a base moving under a long branch produces: the record's own adding commit leaves the range and the commit that UPDATED its verdicts stays inside it, so reading *any commit that touched the file* would refuse a record for doing exactly what a correct record does |

**So the refusal's reach is the commit a cell happens to carry, and that is a
limit rather than a choice about which column to read.** A record whose
`fixed` cells name no commit at all — the bolded row above — is invisible to
it however late it was committed. Two answers were weighed and the cheaper one is not a check:

- **Refuse a `fixed` cell that names no commit.** It would be a sixth refusal,
  owed its own cutoff and its own subsection, refusing a spelling 20 of this
  repository's own cells already use — and the value it would add is reach
  over records whose authors were never asked for the commit.
- **Ask for the commit where a person writes the cell.**
  `templates/sdd-round.md` does, beside the vocabulary, with the reason: a
  reader six months on has no other route to the change, and this refusal
  cannot see a cell without one. Records written afterwards carry it; the
  reach grows as they land, and nothing red is inherited.

The second is what shipped. What it costs, stated rather than buried: the
reach is a convention rather than a guarantee, so *this record passed* means
*no cell in it named a commit the record descends from* and never *this record
was written on time*.

**What a rebase does to this, stated rather than left to be found.** The
refusal reads a commit relationship and a rebase rewrites commits, so the
question is which direction it can move a verdict. The adding commit is read
in `<baseline>..HEAD` rather than in the repository's whole history, and a
rebase replays a branch's commits in order — so a record added before its fix
on the branch is still added before it afterwards, and a passing record cannot
be turned failing. What a rebase does change is the SHA the verdict cell
names: the rewritten fix has a new hash while the cell still holds the old
one, which resolves to nothing in a fresh clone and to an unreachable object
in a local one. Either way no claim is made, so a rebase can turn a **failing**
record passing.

That is the safe direction of the two, and it is taken knowingly. Closing it
would mean matching rewritten commits by patch id, which is a second mechanism
for a case nobody has met — where the cost of the other direction is an honest
record refused for a rebase its author did not connect to the failure.

What no check can see is a record committed on time that carries nothing: the
file exists before the fixes and says only what the round found. This refusal
is about ORDER alone, and issue #150's own comment asks the narrower question
beside it. The next subsection answers it.

##### What the record carries — a declaration, and why no check reads it

Writing the record first is necessary and not sufficient, and the measurement
that says so was taken on the round after the one above. `1788491830`'s round
2 was written **before** the fix pass it commissioned — the thing the refusal
asks for — and its executed-probes table reads:

> the round's proposed fixes for 🟡 6 and 🟡 7, unmutated then under three
> mutations each · green, then red in every case

**The record contains none of that code.** So it asserts a verification and
does not carry its artifact, and the implementer wrote its own replacement for
the second time running. It is the ticket's own opening observation arriving
one level in: a record that says it verified something it does not carry looks
complete.

**The rule.** An `Executed probes` row whose subject was a **proposed
replacement** rather than a command carries the replacement itself, in the
record, in a fenced block. A command is reproducible from its own text; a
patch is not. `templates/sdd-round.md` carries it beside the column.

**Whether it is checkable was asked before it was assumed, and the answer is
no.** Three readings were tried and each fails in a way this document already
refuses elsewhere:

| The check somebody would write | Why it is not written |
|---|---|
| a probe row naming a fix, with no fenced block anywhere in the file | *naming a fix* is a keyword match over free prose — an enumeration over an unbounded domain, the closing the arrow's and the comma's limits above already decline. The column is a sentence a reviewer writes, and a rule about which sentences mean *patch* is a rule about English |
| every record carries at least one fenced block | fails every record whose probes were all commands, which is most of them. A check that refuses the ordinary case teaches people to write a block that says nothing |
| the block's content appears in the diff | the record is written BEFORE the fixes by the rule above, so at that moment the replacement is in no diff at all. Requiring it later would require re-editing the record after the fixes land, for a claim that is already true |

So it stays a declaration, the shape `New units`' depth and `Ran by`'s
provenance already take: written by the party that knows, read by the party
that holds the artifact beside the record — here the fix pass, which is the
one that would otherwise retype it. That is the third declaration in this
document, and the count is worth stating: what a check cannot reach, a reader
does, and saying which is which is what keeps the checks honest.

Which declaration applies is settled by the branch it names, looked up from
the checked-out branch. Every way that lookup can fail — a renamed branch, a
detached HEAD, two declarations naming one branch, a file that will not parse
— resolves to *no declaration*, and therefore to **asking**. There is no path
from a missing or ambiguous declaration to silence: a fail-open here would be
a gate that a corrupt file switches off, and a failed read is not a decision
anyone made.

**This is a reversal, and of this document.** The paragraph below the review
arm's table used to say there is deliberately no standing waiver, because
"a gate that can be turned off for a session has nothing left to do but stay
quiet". That was correct while the commit was the only place a check could
live: with one enforcement site, recording the answer necessarily removes the
check.

A waiver removes a check; a routing record moves it. Both answers stay
enforced — the chain at the pull request against the round record, the direct
route by `[no-review]` in every commit command, unchanged. There is no third
value meaning "no enforcement anywhere". What makes the reversal possible is
the second site, which did not exist when that paragraph was written:
`gh pr create` passed no gate at all, so enforcement sat entirely on every
commit and was absent at the moment the work actually left.

What it costs, stated rather than buried:

- A commit on an unreviewed branch is no longer stopped as it is typed.
  Between the declaration and the pull request, nothing local blocks.
- A branch that declares the chain and never opens a pull request is checked
  by nothing. Today the gate would have stopped every commit. The
  destination axis is what turns that from an accident into a state someone
  declared and can be shown.
- A repository that adopts the declaration and not the workflow has traded a
  prompt for a convention, and the plugin cannot detect that state.
- Deleting the routing file restores today's behavior exactly, because the
  fallback for a missing declaration is today's decision table.

### Parity arm — opt-in: `seal/parity.md` at the repo root

Ported behavior follows the original where policy is silent, so a commit that
changes code should carry a record that the original was consulted. Mark:
`<git-dir>/specseal-parity`, written by the `legacy-parity` skill after an
actual comparison.

| Condition | Decision |
|---|---|
| `[no-parity]` in the command | silent (explicit skip, visible in history). Same placement as `[no-review]` |
| the change confined to `docs/`, `seal/` | silent — nothing there can be compared against an original, and a gate that fires where no comparison was possible teaches people to click through it |
| `specseal-parity` equals current HEAD | satisfied |
| otherwise | contributes an ask |

"The change" there is every path the commit would carry, not the index alone:
`changed_paths()` reads the staged diff, and also what `-a` and a trailing
pathspec pick up, because two of the three forms never touch the index. A
document-root row that said *staged* would describe a narrower silence than
the gate actually keeps, and a reader would expect a prompt where none comes.

The mark says a comparison was recorded, not that it was a good one. Writing
it for work nobody compared converts "nobody checked" into "someone checked
and it was fine" — the one claim the parity methodology exists to keep honest.

`ask` was chosen over `deny` here originally, on these grounds: the gate
cannot know whether the user already accepted the risk, and *a deny with no
override path forces workflow contortions* (measured on the worktree guard's
earlier design). That reasoning stands — it is the override path that changed,
so the premise no longer holds:

| The old worry | What answers it now |
|---|---|
| a deny repeats, and the user cannot get past it | the question fires once per session per repository; every attempt after it is the same `ask` as before |
| the gate cannot know the user already accepted the risk | it no longer has to guess — the deny's reason puts the choice to the user, and their answer comes back as `[no-parity]` (or the comparison itself) |
| nowhere to record the risk being accepted | the marker, and the token in the command, which stays visible in shell history |

What the deny buys is the half the `ask` could never deliver: the reason
string could *name* both ways on, but only the model can put them up as
options, and an `ask` never gives the model the turn.

## review-history-guard (PostToolUse, Bash)

Two branches with **opposite conditions** — the failure modes differ:

| Trigger | Condition | Reminder |
|---|---|---|
| review posted (`gh pr review/comment`, `gh api -X POST …/pulls/N/(reviews\|comments)`) | the work item's `rounds/` holds **no** `round-*.md` | write `rounds/round-N.md`, and `tests-todo.md` and `evidence-todo.md` beside `rounds/` rather than inside it, now — the posting session is the only one that still holds its verdicts and probe results |
| review read (`gh pr view --json …comments`, `gh api …/pulls/N/(comments\|reviews)` without POST) | a round record **exists** | read it before acting on inline comments — the todo lists may not be in the comments at all |

Which work item: the one whose `seal/specs/<id>/routing.md` names the checked-out
branch — the same key the commit gate reads. The records used to be keyed by
the pull request number, at `.specseal/handoff/PR-<n>/`, and that directory
was never once created in this repository: the number does not exist while the
rounds that would fill it are running. One key instead of two costs this
reminder the case where `gh pr merge` runs from a branch that declared
nothing. What replaced the deadline is the pull-request check in CI, not this.

Reminder-only (PostToolUse cannot block). Same `seal/` opt-in as the gate.

## implementer-mark · implementer-notice (PreToolUse Agent|Task · PostToolUse Bash)

The routing declaration's third axis, `Implementation`, names who builds the
work item — `smith` or `the session` — and until these two existed the answer
was written down and read by nothing. Two hooks, sharing one address module
(`hooks/implementer.py`), so the writer and the reader cannot spell the path
two ways:

| | Fires | Does | Prompt budget |
|---|---|---|---|
| `implementer-mark` (`pre-agent`) | an Agent/Task spawn whose `subagent_type` is `smith` | writes the checked-out branch name to `<git-dir>/specseal-implementer`. Prints nothing | zero — it cannot deny or ask |
| `implementer-notice` (`post-bash`) | a command that actually invokes `git commit` | where the declaration for this branch answers `smith` and no mark stands for this branch, prints one line naming the file; silent when the mark stands, when the row is absent or outside its vocabulary, or when it answers `the session` | zero — a reminder, once per session per repository, never a decision |

The mark is keyed on the **branch**, not on HEAD as `specseal-reviewed` is: a
work item commits many times and the implementer does not change when it does.
It lives in the git dir and CI never sees it, which is why nothing at the pull
request reads this axis — `smith` produces no committed artifact a session
could not also write. Everything fails toward "no mark", which is toward a
reminder: a mark gate that quietly stops running turns the notice on, not off,
so a dead gate produces a line somebody reads rather than a silence nobody
does. The commit gate's decision is byte-identical with the row and without it.

## Non-goals

- No Stop-hook turn blocking (v0.2): high false-positive cost in sessions
  that legitimately end without review; the commit gate is where an unreviewed
  commit is stopped and the choice put to a person. It is not a hard stop, and
  was never meant to be: the first attempt in a session denies and asks which
  way on, every attempt after that is a prompt where approving is the waiver,
  and `[no-review]` as a bare word silences it outright. Anyone who can answer
  a prompt can commit — the same limit `README.md` §Limits states.
- The gate does not verify review *quality* — only that the cycle carries a
  review mark. Quality lives in the `code-review` skill's procedure.
