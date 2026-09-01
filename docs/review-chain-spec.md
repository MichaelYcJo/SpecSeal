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
`.specseal/follow-up.md` or the tracker with an answerer named, exactly as
they would at three.

🔴 is not a judgement layered on top of the cap. `code-review` already grades
by what a finding requires rather than by rank, and 🔴 means *blocks merge* —
so "a 🔴 is open" is a state the review already reports, readable from the
last round record's verdict table and its `Pass` checkbox.

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
| A finding neither fixed nor answered | `.specseal/follow-up.md`, and named in the PR body |
| A decision only a person can make | `specs/<item>/questions.md`, and named in the PR body |
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

| | `<git-dir>/specseal-reviewed` | `specs/<work-item-id>/rounds/round-N.md` |
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
(`specs/1788184145-…/rounds/round-3.md`): four findings, fixed by the
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
anyone noticing. The migration config lives at `.specseal/parity.md`, so
writing it creates `.specseal/` — the directory whose existence is the review
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

### Review arm — opt-in: `.specseal/` at the repo root

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

The gate reads `specs/<work-item-id>/routing.md` before it reads anything
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
| an empty cell | **fails** on any record — a row that says nothing answers nothing, and an empty cell is always the author's to fill |
| a `Contract changes` entry (`;`-separated) carrying `unit → call sites` (`→` or `->`) | passes |
| an entry with no arrow, or an empty half | **fails** on any record, naming the entry — a unit without its reach restates the diff and leaves the measured failure's unchecked half unchecked |

Only the ABSENT row is grandfathered. A merged record has no honest repair
for a missing row — writing reach rows for fixes nobody re-read fabricates a
review — where a malformed row's repair is formatting, which is always the
author's. The rows are filled when the fixes land, by the session that has
the fix diff open, so their prompt budget is zero. What `New units` buys sits
with the verifying round: what it names is a finding surface — *is this
correct* — rather than a verification surface, because a unit the fixes
created has been reviewed by nobody.

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

### Parity arm — opt-in: `.specseal/parity.md` at the repo root

Ported behavior follows the original where policy is silent, so a commit that
changes code should carry a record that the original was consulted. Mark:
`<git-dir>/specseal-parity`, written by the `legacy-parity` skill after an
actual comparison.

| Condition | Decision |
|---|---|
| `[no-parity]` in the command | silent (explicit skip, visible in history). Same placement as `[no-review]` |
| the change confined to `docs/`, `specs/`, `.specseal/` | silent — nothing there can be compared against an original, and a gate that fires where no comparison was possible teaches people to click through it |
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
| review posted (`gh pr review/comment`, `gh api -X POST …/pulls/N/(reviews\|comments)`) | the work item's `rounds/` holds **no** `round-*.md` | write `round-N.md` / `tests-todo.md` / `evidence-todo.md` now — the posting session is the only one that still holds its verdicts and probe results |
| review read (`gh pr view --json …comments`, `gh api …/pulls/N/(comments\|reviews)` without POST) | a round record **exists** | read it before acting on inline comments — the todo lists may not be in the comments at all |

Which work item: the one whose `specs/<id>/routing.md` names the checked-out
branch — the same key the commit gate reads. The records used to be keyed by
the pull request number, at `.specseal/handoff/PR-<n>/`, and that directory
was never once created in this repository: the number does not exist while the
rounds that would fill it are running. One key instead of two costs this
reminder the case where `gh pr merge` runs from a branch that declared
nothing. What replaced the deadline is the pull-request check in CI, not this.

Reminder-only (PostToolUse cannot block). Same `.specseal/` opt-in as the gate.

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
