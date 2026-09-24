# commit-review-gate — behavior spec

Authority for `hooks/commit-review-gate.py`, `hooks/review-history-guard.py`
and the implementer mark: how the hooks are registered, which repository a
commit is judged against, the two opt-in arms, and the routing declaration
that moves the review arm's check to the pull request. The review run those
hooks serve is `docs/review-chain-spec.md`'s, and what the pull-request check
reads of a round record is `docs/round-record-spec.md`'s. Update spec and code
together.

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

<!-- specs/1788305134-the-reader-stops-where-it-need-not -->
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
commit written below it did not arrive misjudged, it did not arrive at all.
This is a JUDGMENT read; the scan for a waiver token still sees the command as
written.

<!-- specs/1788184145-the-gate-stops-the-session-editing-its-tests -->
**A file edit goes through the `Edit` tool, because a shell command that only
edits a file is still a command line this gate reads.** Dropping a heredoc
body from the walk decides where a commit lands; whether the command commits
at all is asked of every body separately, as shell, on purpose, because a
commit hidden in a body used to walk straight past (legacy #75). Two kinds of
segment count there. One is a segment whose command word is `git` with the
`commit` subcommand, so what counts is the position and never the presence of
the word: a whole fixture file of shell commands held in Python strings is
clean, while an eight-line patch of that file trips (#34). The other has no
commit in it at all — an `eval` whose argument the reader cannot expand
stops the session, since nothing can tell what it reduces to without running
the shell. So a session that searched its patch for a commit and found none
has not cleared it, and an edit the `Edit` tool makes leaves no command line
to read. Skipping a body that is only being written to a file would reopen
#75, and that trade is the repository owner's to make.

<!-- specs/1788305134-the-reader-stops-where-it-need-not -->

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
alternating `&&` and `\|\|`. Those directories are all real, so the bound
limits how much answering the reader will do rather than correcting anything;
past it the command reads as one whose directory could not be computed.

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
| a `routing.md` declaration names this branch, for either answer | silent — the routing question was answered before the first edit, and CI checks the answer at the pull request. See *The declaration* below |
| `specseal-reviewed` equals current HEAD | satisfied |
| the change confined to `docs/`, `seal/` | no different from any other change — this arm reads no paths. The parity arm's silence on the same roots is that arm's alone, and the paragraph below says why |
| otherwise | contributes an ask |

<!-- specs/1790154759-the-review-arm-asks-where-no-reviewer-compares -->
**The review arm reads no paths: a change confined to `docs/` and `seal/`
meets it as any other change does, and a lighter tier is declared, never
inferred.**

**Why this arm has no document-root line.** The two arms ask different
questions. The parity arm asks whether the original was consulted, and a
`docs/` file has no original, so its silence there is right. This arm asks
whether anybody reads the change before it lands, and here `docs/` is the
policy the code conforms to and `seal/ledger.md` is the verified evidence.
#518 measured whether review finds defects there before drawing any line,
and it does. Across every round record, at least 25 fixed findings sit in
`docs/` alone and 26 in the ledger alone. #514's fold, which changed `docs/`,
`seal/` and four test files, opened seven findings a later round verified as
fixed, all in `docs/`, one of them 🔴. No reviewed work item was ever confined
to the two roots, and the seventeen docs/seal-only commits on the release
branch never reached a reviewer, so nothing measured them either way. The
parity arm's line would stop asking exactly where the reviewed findings sit,
on the strength of a population nobody measured. A documentation pass that
should reach nobody is routed that way before the first edit, by declaring
`straight to the PR`; it is never inferred from the paths it touches.

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

<!-- specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer -->
The gate reads `seal/specs/<work-item-id>/routing.md` before it reads anything
else. Where a declaration is in force the review arm stays silent — for
**either** answer, because the routing question was answered before the first
edit and asking for `[no-review]` as well is asking for the same answer twice.

| The declaration says | At the commit | At the pull request |
|---|---|---|
| through the review chain | silent | a committed `rounds/round-N.md` is required, every commit its `Target SHA` names being REACHABLE — an ancestor of HEAD, or of the branch `routing.md` declares — its last round's `Pass` **checked**, that claim consistent with its own verdict table, and its `Fixes checked by` naming a checker the repository can confirm. A record this pull request does not touch keeps every requirement except reachability: its commits are expected to be gone, and the review it records was enforced at the pull request that added it |
| straight to the PR | silent | the sealer's `broad-gate.md` in the work item's directory, for a work item begun at or after `chain_check.py`'s `DIRECT_GATE_FROM` — the one broad run, at a SHA the tree can see, against the base — and nothing else: the answer turns off the reviewer alone. A draft pull request is excused the file, an earlier work item is excused and prints, and the declaration is printed either way, because a decision nobody sees is not a record |
| nothing readable, or no file | today's behavior — deny once, then ask | pass, with a notice saying nothing was checked |

What the check reads of each round record under the first answer, and what
each refusal costs, is `docs/round-record-spec.md` for the record's rows, and
`docs/review-chain-spec.md` for the floor, `Needs a fix`, the reopening and
when the record was written.

<!-- specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row -->
**`straight to the PR` owes the sealer's `broad-gate.md` and turns off the
reviewer alone, and `Review` has two answers, not three.**

**Two answers, and not three.** A session that wrote a change and then checked
it itself has asked for a third — *reviewed by the session* — with a record of
its own (#241). There is none, and the reason is what the chain's record is
worth: something, only because somebody other than the author wrote it.
`Fixes checked by` refuses *the session that wrote them*
(`docs/review-chain-spec.md` §*Two records, and what each of them says*),
`Ran by` is the spawning
session's row and never the agent's own, and the contract names a review that
certifies itself as what the commit gate exists to catch. What the author's own
check leaves that CI can read is what it RAN — the broad gate at a SHA against
a base — and that is the sealer's stamp, which `straight to the PR` already
owes in the row above. The reading half, *here is what I checked*, is prose,
and prose is not evidence. So a change its author checked declares `straight
to the PR` and takes the broad run; what that answer turns off is the reviewer,
and nothing else. A change belonging to no work item at all is the routing
question's third answer, `no work item`, whose recorded form is `[no-review]`
in front of each commit — there is no value meaning no enforcement anywhere.
Enforced by: skills/code-review/scripts/chain_check.py::direct_seal

<!-- specs/1789518345-who-asks-the-routing-question-and-what-checks-the-answer -->
**A declaration the pull request RETIRED is not one it made**, and neither is
one it only renamed. Both are ways a `routing.md` leaves a diff without
anybody declaring anything, and both are excluded: the rename because the
root move renames every declaration in the repository at once, the
retirement because `settle --retire` removes a released work item's directory
after a `docs/` policy has absorbed its spec, and that work item was reviewed
at its own pull request. The first fold put 88 retired declarations in one
diff, and this check failed all 88.

**The marker is what tells a retirement from a deletion**, because both leave
the file absent at `HEAD` and nothing else can. Where `docs/` carries the
work item's `<!-- specs/<work-item-id> -->` comment on a live line, the check
prints `retired: …` and reads no further; where it does not, the refusal stands —
that is a directory removed with nothing absorbing it, which is what the
refusal was written for. It is the same distinction
`unverified_check.folded_items` draws for a removed `overview.md`, and this
reader had not grown it.

**The rule is the other way a declaration is retired, and it carries no
marker.** `settle --retire` also removes a released directory that held no
`spec.md` and nothing open in its record, because a record of a moment states
no rule to fold (#517). So a declaration absent at `HEAD` whose directory is
gone is asked one more question of the merge base: did the directory hold no
`spec.md` there, and nothing open in its `overview.md` or `evidence-todo.md`?
Where it did not, the check prints `retired: by the rule — …`; where the merge
base held a spec or an open row, the refusal stands. The question is
`unverified_check.retired_by_rule`, the one predicate `settle`,
`unverified_check.py --baseline` and the survivor sweep ask too, so the four
cannot disagree about the same tree the way the marker arm once did. Asked of
the merge base rather than of the tree the branch left, and asked whether the
directory's history ever held a `spec.md`, a spec deleted in one commit — or
in an earlier pull request — and the directory in the next is still a
deletion.

Every record is read as git carries it at `HEAD`, never as the working tree
holds it: a tree that differs from `HEAD` is what CI never sees, and a local
run reading it would be the more permissive of the two. `--worktree` reads the
working tree instead, for the check `round_record.py` runs on a record before
its commit. The flag is local only, and CI keeps the default.

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

<!-- specs/1788844300-the-guards-cases-cannot-observe-what-they-guard -->
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

<!-- specs/1788310269-the-implementer-leaves-a-mark -->
The routing declaration has two axes that name an agent — `Planning`, who
draws the frame, and `Implementation`, who builds the work item — each
answered by that agent's name or by `the session`, and until these two hooks
existed the answers were written down and read by nothing. Two hooks, sharing
one address module (`hooks/implementer.py`), so the writer and the reader
cannot spell the path two ways — and one module for both axes, because a
second one beside it would differ by a constant:

| | Fires | Does | Prompt budget |
|---|---|---|---|
| `implementer-mark` (`pre-agent`) | an Agent/Task spawn whose `subagent_type` is `framer` or `smith` | writes the checked-out branch name to `<git-dir>/specseal-planner` or `<git-dir>/specseal-implementer`, one per axis. Prints nothing | zero — it cannot deny or ask |
| `implementer-notice` (`post-bash`) | a command that actually invokes `git commit` | where the declaration for this branch names an agent on either axis and no mark of that axis stands for this branch, prints one line naming the file — one line naming both axes where both are unfulfilled, never one line each; silent for an axis whose mark stands, whose row is absent or outside its vocabulary, or which answers `the session` | zero — a reminder, once per session per repository, never a decision |

A mark is keyed on the **branch**, not on HEAD as `specseal-reviewed` is: a
work item commits many times and neither the framer nor the implementer
changes when it does. It is keyed on the **axis** too, because the two marks
share a directory and `smith` is spawned on nearly every work item — one mark
answering for both would go silent in exactly the state the notice reports.
It lives in the git dir and CI never sees it, which is why nothing at the pull
request reads either axis — neither agent produces a committed artifact a
session could not also write. Everything fails toward "no mark", which is toward a
reminder: a mark gate that quietly stops running turns the notice on, not off,
so a dead gate produces a line somebody reads rather than a silence nobody
does. The commit gate's decision is byte-identical with the row and without it.
