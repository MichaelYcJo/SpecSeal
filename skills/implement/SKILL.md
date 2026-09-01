---
name: implement
description: |
  Spec-driven implementation methodology: document layout (specs/ + .specseal/), policy-first
  judgment, evidence feedback, and review incorporation.
  Use when: implementing a feature, starting a ticket — including deciding how to
  start one, incorporating review feedback, or when a repo needs its document
  layout bootstrapped.
  NOT for: reviewing someone else's code (use `code-review`), or explaining how
  something already works. The line is whether the question names a work item to
  be built: "how should I approach TICKET-4" is this skill, "how does the review
  chain work" is not.
---

# implement — spec-driven implementation

Methodology for implementing against written specs, leaving durable evidence,
and closing the loop with review. Loaded by the `smith` agent; usable directly.

## Document layout — three axes

Every artifact this skill produces goes to exactly one of three roots, split by
**lifetime**, not by who wrote it:

| Root | Lifetime | Test | Authority |
|---|---|---|---|
| `docs/` | Permanent, cumulative | Must still be true in 6 months | **Norms, ratified by humans.** Read when the repository has them; **never created here** — a project's documentation convention is its own |
| `specs/` | One work item | Its role ends when this work ships (SDD, overview) | The contract this work executes against. A human approves `plan.md`, which is why this is a repository document and not tool state |
| `.specseal/` | Permanent | Everything this plugin maintains | Written and read by machines: the map, the migration config, the follow-up list |

The axis is lifetime and authority, **not audience** — humans and AI read all
three. (Labeling policies "for humans" would push sessions away from reading
them, and policy outranks everything else when a repository has it.)

`.specseal/` is committed — gitignored files do not follow worktrees or other
machines — and its existence is what tells the gates this repository runs the
workflow. Everything in it is permanent:

```
.specseal/
├── map.md            spec clause ↔ code coordinates, as they stood before
│                     work items wrote fragments
├── map/
│   └── <work-item-id>.md   one work item's rows — never gathered, no header
├── parity.md         migration config, only when declared
└── follow-up.md      schedulable items in a repository with no tracker
```

The review round records are **not** here. They live beside the work item they
are about, in `specs/<work-item-id>/`, together with the routing declaration
and the rest of the SDD set:

```
specs/<work-item-id>/
├── routing.md        the routing answer, written before the first edit
├── spec.md · plan.md · questions.md · overview.md
├── rounds/
│   └── round-N.md    one review round — closed at merge and kept
└── tests-todo.md · evidence-todo.md
```

They used to sit under the plugin's own directory, keyed by a pull request
number that does not exist while the rounds that would fill it are running.
No correct session could create that directory, and none ever did
(`docs/review-handoff-protocol.md` carries the whole reasoning). A work
item's directory exists from its first commit, because routing is written
into it before the first edit.

**Nothing else follows them, because there is nothing else.** A round record
carries the SHA it reviewed, so it never asserts a present state and can live
beside the contract. Progress does the same thing one file up, in `plan.md`'s
Status column, where a closed phase carries the commit that closed it — the
same past-state trick, for the same reason.

**Judgment precedence is policy > SDD > code where policy exists, and
SDD > code where it does not.** Most repositories are the second kind. Do not
manufacture the first by writing policy documents nobody asked for: the SDD set
is the root of judgment, and a policy document is a thing a human decides to
keep.

### Bootstrap — create what's missing

When a root or file this skill needs doesn't exist, create it from
`templates/` in this plugin and continue. In particular:

- `.specseal/map.md` — stamp the baseline (current HEAD SHA, date) into its
  header at creation time. That header is the fallback for the rows `git blame`
  cannot answer for; a work item's own rows go in `.specseal/map/<work-item-id>.md`,
  which carries no header at all.
- `.specseal/README.md` — carries the export rules so sessions that never load
  this skill still see them.
- **Not** policy documents. If the repository has none, it has none; judge from
  the SDD set and the code. Creating `docs/policies/<domain>/` imposes one
  project's documentation habit — and one field's vocabulary — on every
  repository this plugin touches.
- Leave evidence rows empty. They fill through the feedback rule below as work
  happens — do not pre-populate speculatively.

**When you create `.specseal/README.md` — the once-per-repo moment — do two more
things before continuing.** Nobody reads a README to discover a question they
did not know to ask, so this is the only place the migration question gets
asked at all.

1. Say in three lines what you created and what each root is for. The layout
   is invisible otherwise: it appears in a diff the user did not request.
2. Ask, once: *"Does this project port behavior from an existing codebase? If
   so, tell me which one and I will set up parity mode."*
   - **Yes** → run the parity setup below, then continue the work.
   - **No** → continue, and never raise it again. Bootstrap does not re-run,
     so the question does not either.

Ask only here. A repo that already has `.specseal/README.md` has been through this,
and re-asking is the nagging this plugin exists to avoid.

### Parity setup — deriving what can be derived

Three of the four fields come from the machine; only one needs the user.
Never guess the original: a comparison against a guessed repo proves nothing.

1. **Propose candidates for the original.** Sibling directories that are git
   repos (a port usually sits beside its original), an upstream or fork
   relation in `git remote -v`, and repos whose paths overlap this one's.
   Present what you found and let the user pick or give a path.
2. **Baseline commit** — read `HEAD` of the confirmed original checkout.
3. **Policy root** — `docs/policies/` if it exists, else propose it.
4. **Coordinate-trust exceptions** — leave empty. Rows arrive from real work.

Write `.specseal/parity.md` from `templates/parity.md` with those values, and
record the machine-local checkout path in `~/.claude/specseal/parity-paths.md`
keyed by the origin remote URL. The path never goes in the committed file.

## Procedure

### 1. Read the spec before the code

Judgment precedence: **policy (`docs/`) > SDD (`specs/`) > the ticket >
existing code** — and, where the repository declares a migration config, the
original sits between the ticket and the existing code, because policy being
silent is what makes the original decide (see `legacy-parity`).

A spec that contradicts policy gets fixed, not followed. **A ticket is a
request, not an authority**: it says what someone wants, which is why it ranks
above the code as it happens to be, and why it ranks below the documents that
were ratified. A ticket asking for something policy forbids is a question for a
person, not an instruction — write it into `questions.md` rather than building
it or dropping it.

- Policy documents delegate to each other. "This document doesn't answer it"
  is not a policy gap until sibling documents in the same domain are checked.
- Read `.specseal/follow-up.md` before starting. It holds items
  whose answer exists but which waited on prerequisite work — **this work may
  be that prerequisite.** If so, include the item in this change and delete its
  row; what remains in that file is the definition of remaining scope.
- Verify clause numbers a ticket cites. Tickets are written before (or drift
  from) the documents they cite; a missing clause means writing it is part of
  this work, with a freshly allocated number.
- A spawn prompt's facts arrive under `docs/review-handoff-protocol.md`'s
  handoff before round 1: coordinates rather than prose, each fact labelled
  executed, read, or unverified. A fact with no coordinate and no label is an
  assertion nobody has opened — open it before building on it, however
  confident the prompt that carried it. An aggregate (a count, a total) is
  not a coordinate: the number can be checked while the claim it stands for
  cannot, and one such fact reached five documents before a review round
  found it false.

**Collect what needs a person before the first edit, and ask it in one batch.**
Read the spec chain looking for the questions as well as the answers, and put
every one of them in front of the user at the start: a decision only they can
make, an approval, a credential, a permission the session does not have.

The cost of a question is not its difficulty, it is when it arrives. Asked
before the work starts, it costs a reply. Asked at minute thirty, it stops
everything until someone is at the keyboard — and the longer a session is
meant to run unattended, the more of it a late question wastes. Asking one at
a time is the same failure spread out: three interruptions cost three waits.

Two things sharpen the list:

- **A question you can answer is not a question.** Read the documents and the
  code first. What survives that is the batch.
- **Assume, in writing, whatever would not change what you build.** State the
  assumption in `questions.md` and continue. Only where different answers mean
  different code does the work actually have to wait.

Something a session cannot do for itself belongs on the same list — widening
its own permissions, for one, which the harness blocks by design. Better
found in the first minute than at the commit.

**A question in this batch names its answers, and every answer continues.**
"Should I release this?" and "should the warden review it?" both have a `no`
that leads nowhere — the session that answers it is holding finished work with
no destination, which is a gate wearing the shape of a question. A yes/no is
the tell. Ask which of two named paths instead, and say what each one does.

**How this work is routed is one of them, and it has three axes.** Ask all
three in the same breath: they are one decision about where the work goes, and
asking a later one on its own is itself the mid-round prompt this exists to
remove. Opening a pull request is an outward-facing act — it is not a detail
that can wait for the end.

| Axis | Answers |
|---|---|
| Implementation | smith · the session — OPTIONAL; absent reads as unanswered |
| Review | through the review chain · straight to the PR |
| Destination | open the pull request · stop before the pull request |

**Ask them as one `multiSelect` question with three checkboxes.** The three
are independent, so single-select options spell out eight combinations and
cost three waits, where three boxes cost one question and one reply. What is
checked is the answer, and each box is a row of the declaration:

| Checkbox | Checked | Not checked |
|---|---|---|
| Implement with `smith` | spawn the subagent · `Implementation` = `smith` | this session builds it · `Implementation` = `the session` |
| Review with `warden` | run the rounds · `Review` = `through the review chain` | `Review` = `straight to the PR` |
| Open the pull request | push it and open one · `Destination` = `open the pull request` | `Destination` = `stop before the pull request` |

**Asking one of the three later is the failure, not a lesser version of it.**
Measured here: routing at the start, the reviewer in the middle, the pull
request at the end — three interruptions, in the session that had the
one-batch rule loaded. Nothing had said the three belonged to one question, so
obeying the rule for the first of them looked like obeying it.

**Write the answer down before the first edit**, in
`specs/<work-item-id>/routing.md`, from `templates/sdd-routing.md`. Committed,
because the check happens at the pull request and CI sees only what is in the
tree. Below the SDD ladder this may be the only file a work item ever gets,
and it is the first place such a change exists at all.

**Write the file in a command of its own, never batched with the commit.**
The declaration is read from the WORKING TREE — `hooks/routing.py`'s
`declarations()` opens the path rather than asking git — so a `routing.md`
that exists on disk silences the review arm for the very commit that adds it.
There is no first-commit exception to arrange and no `[no-review]` to spend.
That only holds if the file actually got written, and batching is what stops
it: the commit gate is a `PreToolUse` hook, so it denies the WHOLE tool call,
and `write routing.md && git add && git commit` in one call writes nothing.
The gate then reports no declaration, which is true, and the session reads a
chicken-and-egg the design does not have. Measured here: two questions put to
a user who had to explain the batch was the bug. This is the one place a
*batch independent commands* habit misleads — the commit is not independent
of the write, and a gate sits between them.

What the four combinations do:

| Review | Destination | During the work | At the end | What CI checks |
|---|---|---|---|---|
| chain | open the PR | the review arm stays silent | the PR opens | a round record is required |
| chain | stop before the PR | the review arm stays silent | the branch is handed back, committed and unpushed | **nothing runs** — say so in the handback |
| direct | open the PR | the review arm stays silent | the PR opens | nothing required |
| direct | stop before the PR | the review arm stays silent | the branch is handed back | nothing |

That column is about the review arm. The gate has two arms, they are separate
opt-ins, and each has terms that **wake** it and terms that **quiet** it.
Prose has described this three times and lost a different term each time, so
it is a table:

| | Review arm | Parity arm |
|---|---|---|
| **Wakes when** | `.specseal/` exists in the repository the commit lands in | `.specseal/parity.md` exists there, **and** the change touches something outside `docs/`, `specs/` and `.specseal/` |
| **Quiets when** | a `routing.md` declaration names this branch, for either answer · the review mark stands at HEAD, written by the review chain · `[no-review]` rides in front of one command | the parity mark stands at HEAD, written by a recorded comparison against the original · `[no-parity]` rides in front of one command |

Two things the sentences kept dropping. A declaration reaches the review arm
only, so a migration repository still meets the parity arm on a code-touching
commit. And a commit confined to those three directories never wakes that arm
at all — which is why the `routing.md` commit this section mandates costs
nothing even there, and why asking would only teach a reader to click through
the prompt.

<!-- # RIDER: "that arm" is the PARITY arm and "even there" is a migration
     repository. Both readings are correct and both were read the other way
     round in one session, which then treated the review arm's ordinary wake on
     a `specs/`-only commit as a chicken-and-egg the design does not have and
     put it to the user twice. The table above says it unambiguously; this
     paragraph is what gets read instead. Name the arm in the sentence when
     this section is next opened. Verified 2026-08-31 at 9829412. -->

The declaration is what the commit gate reads, for **either** review answer.
A work item routed to the chain used to carry "no marker at all", and that was
true only after the first review mark landed — false for every commit before
it, which is why every commit of every round was stopped on its way to the
reviewer the answer had already named.

`[no-review]` still works and is unchanged: it waives **one command**, where
the declaration routes **a work item**. Coupling them would ask for the same
answer twice and stop a session for not repeating itself. Where no declaration
is in force — no file, a branch it does not name, or a file that will not
parse — the gate behaves exactly as it did before, which is to ask.

For a change that belongs to no work item at all, the token is still the way
past, and it goes in FRONT of the command, quotes included:
`: '[no-review]'; git commit …` (and `[no-parity]` too where a migration
config is declared). After `git commit` a bare word is a pathspec and git
rejects the whole command.

Work that was never headed for a reviewer — a release chore, a documentation
pass — declares `straight to the PR`.

**Which branch the PR lands on is the other.** `main` is what the marketplace
serves, so a PR into `main` is a release and a PR into the release branch is
not (`CONTRIBUTING.md`), and the answer changes what the work writes rather
than whether it finishes.

| Answer | What it does |
|---|---|
| `release/vX.Y.Z` (the default) | the entry accumulates unreleased; `plugin.json` is left alone |
| `main` | the version moves, the accumulated entries are collected and dated, and the tag follows the merge |

Take `main` when the accumulated entries read as one thing, or when the change
is a gate or a hook firing where it should not — that one does not wait for
company.

**Where an entry accumulates is the repository's convention, so read it before
writing one.** Two shapes are common and they are not interchangeable: a
heading in the changelog that every branch appends to, or one fragment per
work item that a release gathers. Writing the first into a repository that
uses the second either invents a heading its checks refuse or appends to the
shared region the fragments exist to empty — which is the collision, arriving
from the document that was supposed to prevent it.

Where the repository gathers fragments, **basing on `main` means running the
gather**, because that is the branch where the entries are due. It is the one
moment a feature branch touches the changelog at all, and the repository's
contribution guide names the command.

What must not happen instead is a standing waiver. A session-level switch that
turns the gate off leaves it nothing to do but stay quiet, which is the state
the gate exists to end. The routing declaration is not that switch: it moves
the check rather than removing it — the chain answer is checked at the pull
request against the round record, the direct answer by the token in every
command — and there is no third value meaning no enforcement anywhere.
Deciding early does not weaken the question; it moves it to the minute where
answering it costs a reply rather than a stopped session.

**Once the batch is answered, the session runs to the pull request.** What
surfaces after it is written down rather than raised: a decision only a person
can make goes to `questions.md`, a finding you neither fixed nor answered to
`.specseal/follow-up.md` with an answerer named — a deferral to nobody is how
"someone will look at it" becomes nobody did (`verify` §The answerer has to
exist) — and what was deliberately left goes to the overview's Not done
section. Each is named in the PR body, because a leftover nobody can find was
not handed over.

The test for whether something is a question or a row: would a different
answer change what you build *now*? If it would not, raising it spends a
person's attention on something that was never blocking, and the session that
waits for the reply spends more.

### 2. Implement, and feed evidence back where you verified it

When you open code or run something to settle a judgment, record the outcome on
the row it belongs to (spec clause ↔ `file:line`) and put **the date you read
it** in the Checked column. Only rows in this work's scope — full-ledger audits
verify what is already correct and return nothing.

**Rows a work item adds go in its own fragment**, `.specseal/map/<work-item-id>.md`,
not appended to `.specseal/map.md`. Two branches cannot collide there, because
no two work items share an id, and the checker reads the whole
`.specseal/map/*.md` glob. A fragment needs no baseline header of its own.

The commit a row's drift is measured from is the commit that row first
appeared in, derived from its own line's history — not the commit that last
touched the line, which any bulk rewrite of the rows would pull forward to
itself. Re-verification drains row by row instead of ledger-wide, and nothing
has to be typed that a rewrite could orphan. A stamp written into the row still
wins, which is how rows stamped under the older rule go on working and how a
re-verified row clears drift the derivation cannot see.

**Draft as you go, write in one pass.** The recording is cheap and the round
trip is not: one session made twenty-six separate edits to its ledger and
policy documents, seventy-eight seconds of command time that cost about three
and a half minutes of waiting. Keep the rows as you settle them and write
them to the file when the work item closes, or at a phase boundary — not one
edit per row.

This record is the input for the reviewer and the next ticket. Unrecorded
verification gets redone by every session that follows — the single largest
avoidable cost in multi-session work.

**Commit at the smallest step that stands on its own.** What an intermediate
commit costs is a property of the repository rather than a fact about
committing, and two things can drive that cost to nothing:

- feature branches **squash** into their base, so every commit the branch
  wrote stops existing at the merge and none is left for anyone to read;
- a `routing.md` declaration is in force, which silences the review arm of the
  commit gate for either answer (§1).

Read both off the repository before leaning on them. One that merges without
squashing keeps every commit in its history, and one with no declaration meets
the review question at each commit. **A declaration does not silence the
parity arm**: the two opt-ins are independent, so where a migration config is
declared a code-touching commit still meets that one. §1's table says what
wakes and quiets each arm, and it is the only place that says it.

What committing *buys* is a separate matter, and that one holds everywhere. A
review round records the commit it read, so work still sitting in the working
tree is not visible to the reviewer at all — there is no spelling for *and
also the four files that were not committed yet*.

*Commit as you go* alone does not settle the cadence. One session was told
exactly that and did it, eight commits across two rounds, and still had five
modified files in the working tree when an unrelated command reached the
worktree guard. That window has a price wherever this plugin is installed: the
guard asks whether the changes should ride along to the other branch, and
*commit them here first* — the answer that is usually right — is not one of
the two buttons. Nothing had said how early early is.

The two cadences in this section govern different acts. *Draft as you go*
batches the **write** into the ledger file, so rows land in one edit at a
phase boundary instead of one edit each; this rule is about the **commit**. A
phase boundary is where they meet: write the rows you have been keeping, and
let that write ride the commit that closes the phase. Pairing each row with
the one slice it describes is not on offer, because those slices are already
several commits behind and buying the pairing costs one write per row, which
the rule above refuses. What must not happen is a run of commits reaching the
reviewer with the ledger still empty, because by the paragraph above the
reviewer sees only what was committed.

**Commit freely; a ledger row names no commit for a merge to orphan.** This
used to be the one place the cadence had to be steered around. A row's drift
baseline was a SHA somebody typed, and no commit a feature branch could type
was both reachable after the squash and current with its coordinates: name the
base and the row read DRIFTED at birth, name the branch and the squash left it
pointing at nothing. Blame of the row's own line has no such choice to make —
it is computed on the tree as it stands, so after a squash it answers with the
squash commit.

**An edit must be able to fail.** Prefer the `Edit` tool: a pattern that does
not match is an error you see immediately. When the environment routes edits
through the shell instead — `sed -i`, a heredoc, a short script — a
substitution whose pattern misses does nothing, says nothing, and exits zero.
The miss surfaces at the next check, and the cost is another edit and another
run of whatever you had already run. Measured on one work item here: no `Edit`
calls, 128 shell edits across 47 files, 2.7 edits per file, and a column
insertion that silently did not happen because the indentation did not match.

So assert the landing. Every shell substitution states what it expected to
match and fails loudly when it did not:

```python
assert old in text, f"pattern did not match: {old[:60]}"
```

This is `verify`'s second condition — *a check that cannot fail is a
counterfeit seal* — applied one step earlier. An edit that cannot fail is an
unverified edit, and reporting it as made is the same claim as reporting a
`read` as passing.

### 3. The SDD file set

**When a work item is required** — the same threshold the Design Gate uses,
because they are the same judgment. Drawing no line is how the set quietly
stops being written; this repo's own history has two features that shipped
without one and nothing noticed.

| Work | What to write |
|---|---|
| It **alters observable behaviour** — a gate's verdict, a hook's output, a skill's or agent's instructions, a public API, text a person reads and acts on. Or it changes a value someone waits on or is limited by — a timeout, a retry count, a rate, a size cap — and NAMING that value is what puts it on this rung | `spec.md` and `plan.md` **before** implementing — approval of `plan.md` IS the gate — then the closing memo |
| It alters none of that and is more than one line — a refactor, a performance pass, a formatting sweep, a test that pins what already holds. These four are DEFAULTS, not a closed list: a performance pass that moves a timeout a person waits on belongs on the rung above, and the value's name is what moves it | the closing memo. A one-line scope confirmation replaces the plan |
| A typo, a config value, a one-line fix | nothing |

**Behaviour, not file count, and the difference runs both ways.** The top rung
used to read *6+ files, a new module, or an architectural choice*, and two of
those three conditions measured size.

- **One file, and it qualifies.** A change to an agent's persona is two files
  of wording, and wording is what a session reads and acts on. Measured here:
  `warden-persona-accuracy` opened as exactly that, wrote no `spec.md`, and
  finished at eight files with five of them arriving in review rounds 2 and 3.
  Under the behaviour test it needed a plan at file one.
- **Many files, and it does not.** Copying test repositories instead of
  running `git init` for each touched more files than that and altered nothing
  anyone can observe — no verdict, no output, no instruction. The suite runs
  faster and says the same things.

The count also never said **when** it was taken (issue #35). The gate it
guards — plan approval — exists only before the first edit, so the number had
to be the estimate; nothing said so, and nothing said what to do when the
estimate was passed. Seven branches were measured for that issue and two
missed the rung by growing past it after the gate had already gone by. A test
with no number has no moment at which the number is taken, so the question
stops being answerable and stops needing an answer.

What it costs: *does this alter observable behaviour* is a judgment where
*six files* was a count, and two people can disagree about a borderline case.
That is the trade — a judgment that is about the right thing beats a
measurement of the wrong one, and the list in the rung is what keeps the
judgment from being free-form. The way out of a default is to NAME the value a
person waits on or is limited by, which a reader can open and check. *I judged
it observable* is not something anyone can check, and it is not a way out.

`questions.md` is not on that ladder: it starts with the batch collected
before the first edit (step 1) and gains a row whenever a decision only a
human can make appears later, at any size. A late one still gets written — the
batch is what keeps it from being the only way they arrive.

A work item's directory is `specs/<unix-epoch-seconds>-<slug>/` (e.g.
`specs/1784780439-center-list-sort/`), bootstrapped from `templates/`. The
timestamp prefix keeps directories in creation order and collision-free
without a registry — take it from `date +%s` when creating the directory.

| File | Holds | When |
|---|---|---|
| `spec.md` | WHAT — scope, mandatory user scenarios & acceptance, grounding clauses | before implementing |
| `plan.md` | HOW — phases as vertical slices, alternatives with failure scenarios; this is the Design Gate's artifact | before implementing (gated work) |
| `questions.md` | decisions only a human can make — extracted so nothing ships on a silent assumption | one batch before the first edit, then as they arise |
| `overview.md` | the closing memo — one line of purpose, then what the diff cannot show (below) | opened at the first divergence, unverified item, or fed-back clause; closed when implementation ends |

**`plan.md`'s Phases table is the task list, and there is no other.** Each
phase carries a **Verified by** column, so it cannot be called done the way a
checkbox can be ticked, and a **Status** column that is empty or holds the
commit that closed the phase.

The objection that sent task lists elsewhere is real and it is about form
rather than location: mutable progress inside the contract asserts a state
that is not true, which is the failure this plugin's ledger exists to prevent.
A commit is not mutable progress. It asserts a **past** state that someone can
open — the same trick that lets a round record sit beside the contract — so a
tick and the word `done` are refused where a hash is not. Both of those can be
typed without anything having happened.

What this gives up, stated rather than left to be found: the finer structure
`feature-planner` produces — per-task dependencies, what can run in parallel —
does not fit in a phase row and is not kept anywhere between sessions. Phases
are already ordered and already vertical slices, so what is lost is the
parallel marker, and the judgment is that a list nobody ever wrote had no
structure to lose. It had a home in `.specseal/` for three releases, no code
ever read it, and it was never once created.

### 4. The closing memo — only what the diff cannot show

`specs/<work-item>/overview.md` is not a summary of the work. `git diff --stat`
already holds the file list and the diff holds the detail; re-deriving them at
the end costs a re-read of your own change and lands further from the truth
than the command would.

Four things go in it, and after the session closes three of them are nowhere
else. Write each **when it happens** — a call made at minute ten is invisible
by minute ninety, and reconstruction is the expensive way to get a worse
answer.

1. Why this work exists and what the result changes — **one line**, not a walk
   through the diff. Where the change alters nothing observable no `spec.md`
is written, so this is
   the only place the purpose stays in the repository.
2. Where spec and implementation diverged — both sides quoted, which side won,
   and the grounds, at the moment you decide it. "The document probably said
   so" is not grounds; quote it.
3. What was not verified — with **who has to answer it**, at the moment you
   decide not to run something.
4. What was fed back into the spec — clauses this work added, marked as
   *inferred during implementation* so planners know they may overturn them.

A memo whose last three sections are empty is correct and four lines long.

**`## Not verified` is read by a machine, so it has one shape** — a
`| Item | Who must answer |` table, or the line `none — <why>`. Any other
spelling of the heading or the header row fails the check rather than reporting
zero, because zero reads as "everything has been closed".

An item is closed by marking it, never by deleting it:

```
| ✅ how the gates render in a TUI | seen on screen, session of 2026-08-25 |
```

An unmarked row counts open, so the silent direction is always "still open",
and a bare check mark with nothing after it is refused the same way a ticked
checkbox is. Deleting the row — or the whole file — fails the next pull
request (`unverified-check --baseline origin/<base>`), which is what keeps "I
verified it" and "I tidied it away" from being the same edit.

What that check reads is the **number** of rows, not their text. So the second
cell saying what closed the item is a convention it cannot enforce: swapping
one row for another keeps the count and passes. Leaving the original answerer
in place beside a check mark is how a closing goes out unproven, and only a
reader catches it.

Never record something as passing that you did not run. Findings from reading
and findings from execution are labeled separately.

### 5. Incorporate review — read the round records first

A session fixing review feedback starts at `specs/<work-item-id>/`,
**not** at the inline comments. Two of its files are owned by the implementer:

| File | Written by | Acted on by |
|---|---|---|
| `round-N.md` | review orchestrator | next review round |
| `tests-todo.md` | review orchestrator | **implementer** — plant each test in the file the row names |
| `evidence-todo.md` | review orchestrator | **implementer** — merge each fact into `.specseal/map/<work-item-id>.md` |

Inline comments may not contain these lists at all. Fixing only the comments
ships the code change and silently drops the tests and the evidence.

A finding is a claim too, and it arrives from someone who did not write the
code. Open the coordinate and judge it yourself: fix what holds, and where it
does not, answer it in `round-N.md` with the grounds — the policy clause, the
original's behavior, the constraint that makes the state unreachable. What is
not allowed is the third path, changing the code to quiet a finding you do not
believe. A review the implementer cannot argue with is not a review, it is a
handoff of judgment.
Probes already run by a previous round (listed in `round-N.md`) are not
rebuilt — only re-checked for whether the finding is now fixed.

### 6. Close before merge — drain the rows, keep the records

Before the PR merges, every unresolved (⬜) row must move out:

| Remaining item | Destination |
|---|---|
| Doable within this PR | Do it now — merging is the last moment anyone is looking |
| Waiting on prerequisite work | `.specseal/follow-up.md` |
| Needs a decision | The policy document's open-questions section |

Then say so in the round record: what went where, or `nothing to drain`. The
records themselves stay. It used to be deleted here, and deletion was buying
one thing worth keeping — a deadline that forced the draining — while costing
more than it bought: rows left for durable homes because the directory was
about to disappear, and those homes are outside what the next reviewer reads.
A deferral that leaves the round records leaves the inheritance range with
it, and comes back as a finding next round.

A finding deferred mid-change is a row in `round-N.md`'s Deferred field as
well, naming where it went. That field is the one-line version of this table,
in the file the next round already opens.

## Proof block

End the response with this block whenever the skill was applied. Its values
cannot be filled without actually opening the documents — that is the point.
Never invent them; write `none — <reason>` for anything not actually read.

```
📋 implement applied
· spec:     <policy/SDD files and clauses actually read>
· evidence: <ledger rows added or updated, with the file they went in>
· verified: <what was executed vs. what was only read>
```

When the skill matched but did not apply, say so explicitly with the reason —
silence is indistinguishable from failure to trigger.
