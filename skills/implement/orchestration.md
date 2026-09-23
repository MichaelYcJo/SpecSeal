# implement — the orchestrator's half

The sections `skills/implement/SKILL.md` used to carry for the session that
spawns agents, under the `Orchestrator:` prefix `code-review` already used for
its own. They are the procedure for **starting** a work item: creating the
`seal/` root the first time a repository opts in, setting up parity mode where
a project ports an original, and asking the one routing question — two
questions, one call, one file — before the first edit.

The sequence those sections sit inside arrived later, from the shared
checklist that was deleted for being written by every branch (#351). It is
the first section below, because a session starting a work item needs the
order before it needs any step of it.

**Read this if you are orchestrating a work item.**
`skills/implement/SKILL.md` is the other half and holds the implementation
itself — the record language, the document layout, the spec-first procedure,
the evidence feedback, the SDD file set, the closing memo and the review
incorporation. An orchestrator reads both; a `smith` spawn preloads that one
and never this, because asking a person and writing `routing.md` are acts
`agents/smith.md` leaves to the session that spawned it.

Nothing changed in the three sections #292 moved out of
`skills/implement/SKILL.md`, except one sentence a `# RIDER:` had asked to
name its arm; their headings keep the `Orchestrator:` prefix they were marked
with, so a reference to one of those names the section it always named and
only the file it names changed (#292, the shape #265 gave `code-review`).
**The order below is the exception**: it gained the prefix when it moved, so
it is cited by its new name and not by the one the shared checklist gave it.
Every `seal/…` path here means what it means in the other
half: `<repo>/seal/` where that directory exists, and
`$(git rev-parse --git-common-dir)/seal/` otherwise (contract §16).

## Orchestrator: the order inside a ticket

1. Branch from the release branch; write `routing.md` before the first edit.
2. spec · plan (framer) → smith → the draft pull request opens
   (`skills/code-review/orchestration.md` §*Orchestrator: the pull request
   opens before round 1, and a phase is re-run* owns when) → warden rounds →
   sealer → the pull request is marked ready.
3. The pull request body carries `Closes #N`; the release workflow closes the
   ticket when the release reaches `main`.

## Orchestrator: Bootstrap — create what's missing

When a root or file this skill needs doesn't exist, create it from
`templates/` in this plugin and continue. In particular:

- `seal/ledger.md` — written from `templates/ledger.md`, which carries the
  coordinate notation and the feed-back rule a session needs before it adds
  a row. Its **clause tables arrive empty** and there is no baseline to
  stamp: a coordinate names content rather than a position, so there is
  nothing for a header to declare. A work item's own rows go in
  `seal/ledger/<work-item-id>.md`.
- `seal/README.md` — carries the export rules so sessions that never load
  this skill still see them.
- **Not** policy documents. If the repository has none, it has none; judge from
  the SDD set and the code. Creating `docs/policies/<domain>/` imposes one
  project's documentation habit — and one field's vocabulary — on every
  repository this plugin touches.
- Leave evidence rows empty. They fill through the feedback rule in
  `skills/implement/SKILL.md` §2 as work happens — do not pre-populate
  speculatively.

**When `seal/` exists at neither place — the once-per-repo moment — ask one
question before creating anything, then do two more things before
continuing.** Creating the root is what opts the repository in: from the
next command on, every gate here is awake. Nobody reads a README to discover
a question they did not know to ask, so this is the only place the mode and
the migration question get asked at all.

First, look for the 0.3.x layout. A repository still holding
`.specseal/` or a top-level `specs/` is on the 0.3.x layout and committed the
plugin's files, so it chose shared already: do not ask, say *"this repository
is on the 0.3.x layout; start a new session and the plugin moves it into
`<repo>/seal/`, or follow the README's by-hand sequence — and `seal mode
local` moves it out of the tree afterwards if that is what you wanted"*, and
stop the bootstrap there. The session-start hook moves it, and the root it
creates is the one this section would have asked about. Naming the command
is what keeps *not asked* from meaning *not offered*: nobody who lands in
shared mode without a question goes looking in a README for the way out.

1. Ask, once, with one `AskUserQuestion` carrying **two questions** — the
   mode, and the `Broad gate` row. One interruption or two is the whole of
   what is being decided by putting them together, and this is the only place
   either of them is asked at all. The mode's two options come first, in this
   order:

   - **shared** (the default, listed first) — creates `<repo>/seal/` in the
     tree; the routing commit you make before the first edit carries it. It
     installs the pull-request checks: `.github/workflows/hygiene.yml`,
     written from `templates/hygiene.yml` only when that path is absent — an
     existing file is never overwritten, and say so when you leave one alone.
     Before writing it, replace `v<version>` in the template with the version
     of the installed plugin, prefixed with `v`, so CI checks with the
     release that wrote the file. The session sits in the user's repository
     and the plugin sits in its cache, so the version is read from
     `$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json` and never from a file
     in the tree — a wrong read leaves `v<version>` in the workflow, and
     CI's `git clone --branch` fails on it. One line reads it:

     ```bash
     python3 -c 'import json, os; print("v" + json.load(open(os.path.join(os.environ["CLAUDE_PLUGIN_ROOT"], ".claude-plugin", "plugin.json")))["version"])'
     ```
   - **local** — creates `$(git rev-parse --git-common-dir)/seal/`, installs
     nothing, touches nothing in the tree. Spell the path through the common
     git directory rather than through `.git`, which is a file in a linked
     worktree; the root lands beside the smith mark, shared by every
     worktree of the clone, never a commit candidate, with no `.gitignore`
     line. Say what it gives up: the pull-request checks read committed
     files, so CI cannot run them, and a new machine or a re-clone starts
     empty.

   Whichever answer, the mode is the place: the hooks read `<repo>/seal/` and
   then the common git directory, and a repository with both is shared.

   **The answer is not a door that shuts.** `seal mode` reports where the
   root is and `seal mode local` / `seal mode shared` moves it, carrying the
   workflow file and writing the mode into `seal/config.md` on the way. Say
   so in one line when you create the root, because this question is asked
   once and the person answering it does not yet know what they will want.

   **The second question is the `Broad gate` row, and it is a proposal rather
   than a blank.** That row is the one value in this whole flow only a person
   can write — `templates/config.md` §*Broad gate* says why it has no default
   — and until #401 nothing ever asked for it, so it reached a person as the
   gate's refusal, after the review rounds had settled, at the one moment
   whoever is there has every reason to answer it themselves. A repository
   being opted in may not yet know its broad command, so a bare question gets
   answered badly to get past it. The parity setup below is the shape that
   answers that, and it is the shape here too: **what the machine can derive
   is offered, the person picks, and nothing is guessed.**

   Read candidates off the repository, in this order, and offer what you
   found with the file each came from:

   | Where to look | What to take |
   |---|---|
   | `.github/workflows/*.yml` | the `run:` steps of whatever job gates a pull request. What CI already refuses a merge for is the repository's own answer, written down before anybody asked |
   | a runner under `bin/` | `bin/test`, `bin/check`, or whatever the contribution guide names first |
   | a package manifest | `package.json`'s `scripts.test`, a `pyproject.toml` tool section, `Cargo.toml` |
   | a `Makefile` | a `test`, `check` or `lint` target |

   Offer each candidate as **one shell command line** composed the way
   `templates/config.md` §*Choosing a value — the criterion* says to compose
   one, and name the file it came from — a candidate whose source is named is
   one the person can correct. Where nothing is findable, say so rather than
   inventing one: a guessed row is what `templates/config.md` §*Broad gate*
   argues against by name, and offering it with a source that does not exist
   is worse than offering nothing.

   **A candidate carrying a `|` is written with the pipe escaped, `\|`**, and
   a CI `run:` step is where one is likeliest to come from. Offer it that way
   rather than dropping the pipe or moving to the next candidate: the cell is
   markdown's, and the reader reduces `\|` to a plain pipe before any shell
   sees it. Say why, because a bare one still parses as no row, the gate then
   quotes that line back instead of reporting the row as absent, and — where
   a row above it already parsed — every row written below it is lost with it.
   `templates/config.md` §*What is refused, and what stays allowed* carries
   the measurement.

   **Name the criterion; do not restate it.** `templates/config.md`
   §*Choosing a value — the criterion* owns the criterion, three rules with
   the reason for each, and the person answering reads it there.

   **Offer a decline, and say what it costs.** *Not yet* is a real answer:
   the repository may not have a broad command yet, and one written to get
   past a question is worse than none. The cost is one sentence — the first
   `broad-gate` run refuses with nothing run, and that refusal lands after
   the review rounds have settled, which is the last moment available.
   `/specseal:config` fills the row in at any point before then.

   **Then record the answer: run `seal mode`, with no argument.** It writes
   the row from where the folder is, which is where you just put it, and it
   moves nothing — `seal mode shared` on a root that is already shared works
   too and answers with the whole switch narrative, which is not what
   somebody who has just chosen needs to read. The row is not decoration and
   it is not a default being guessed at: it is the only trace
   that anybody was asked. Left unwritten, a root somebody chose and a root
   that appeared because a session followed the preset's routing rule are
   byte-identical — which is #151, reported from a repository whose review
   records were committed without the question ever reaching a person.
   `hooks/mode-gate.py` is what reads the absence, and it stops the next
   command to ask this same question; running the command here is what keeps
   the person who just answered from being asked twice.

   **Then the `Broad gate` row, where a command was chosen.** `seal mode` has
   just written a config file carrying `Mode` and nothing else, so add the
   row the way `/specseal:config` step 3 adds one — the row **and the prose
   under `## Broad gate` down to but not including `### What is refused, and
   what stays allowed`**, taken from
   `$CLAUDE_PLUGIN_ROOT/templates/config.md`. A bare row hands the person the
   value and none of the half they read; the two lists and the criterion are
   pointed at rather than copied down, because a frozen copy of them in
   somebody's `seal/config.md` says something false about the tool at the
   plugin's next release. No command does this and none is being added:
   `skills/implement/scripts/seal.py`'s writer is the `Mode` row's, and
   `skills/config/SKILL.md` §*What this does not do* refuses a generic setter
   for a file people edit by hand.

   **A decline writes nothing at all.** No row, no sentinel, no note. A
   repository that declined and one that was never asked meet the same
   refusal at the same moment and are told the same correct thing, so a trace
   would separate two states nothing treats differently — which is the
   opposite of the mode row, whose absence is what #151 measured the cost of.
2. Say in three lines what you created, that its presence at that place is
   the opt-in, and what each part of the root is for. The layout is invisible
   otherwise: it appears in a diff the user did not request — or, in local
   mode, in no diff at all.
3. Ask, once: *"Does this project port behavior from an existing codebase? If
   so, tell me which one and I will set up parity mode."*
   - **Yes** → run the parity setup below, then continue the work.
   - **No** → continue, and never raise it again. Bootstrap does not re-run,
     so the question does not either.

Nothing else is asked. **`/specseal:config` is how any of it is changed
later** — it shows every row with its value, and routes a change to
whatever owns that row. Say so once, here, because a person who answers a
question in a batch has no reason to expect a way back to it.

Ask only here. A repository that has `seal/` at either place — `<repo>/seal/`
or `$(git rev-parse --git-common-dir)/seal/` — has been through this: the
mode is read from where the folder is, and re-asking is the nagging this
plugin exists to avoid.

## Orchestrator: Parity setup — deriving what can be derived

Three of the four fields come from the machine; only one needs the user.
Never guess the original: a comparison against a guessed repo proves nothing.

1. **Propose candidates for the original.** Sibling directories that are git
   repos (a port usually sits beside its original), an upstream or fork
   relation in `git remote -v`, and repos whose paths overlap this one's.
   Present what you found and let the user pick or give a path.
2. **Baseline commit** — read `HEAD` of the confirmed original checkout.
3. **Policy root** — `docs/policies/` if it exists, else propose it.
4. **Coordinate-trust exceptions** — leave empty. Rows arrive from real work.

Write `seal/parity.md` from `templates/parity.md` with those values, and
record the machine-local checkout path in `~/.claude/specseal/parity-paths.md`
keyed by the origin remote URL. The path never goes in the committed file.

## Orchestrator: how the work is routed — two questions, one call, one file

**How this work is routed is one of them.** It is one decision about where the
work goes, and asking a later part of it on its own is itself the mid-round
prompt this exists to remove. Opening a pull request is an outward-facing act —
it is not a detail that can wait for the end.

**This is two questions in ONE `AskUserQuestion` call**, which is one wait. What
the batch rule asks for is one batch before the first edit, not one question
(`skills/implement/SKILL.md` §1). `AskUserQuestion` allows at most four options
per question, and two presets beside the boxes is five — so the shape below is
two questions rather than one, and that is what makes both fit.

### Question 1 — single-select

| Order | Label | Description |
|---|---|---|
| 1 | **automation** | Every party runs: the framer frames it, `smith` builds it, `warden` reviews it, the sealer takes the broad run, and the pull request opens. **This is the last question — nothing stops to ask again.** |
| 2 | **per axis** | The four boxes below are the answer. |
| 3 | **no work item** | No work item is opened: no frame, no review, no seal, no `routing.md`, and this session writes the change itself. Every commit needs `[no-review]` typed in front of it, and nothing checks this change at the pull request. |

**A label must name what it turns off, not where it ends.** The measured
instance is the reason the exit is labelled the way it is: the owner read
`straight to the PR` as *call no agents at all*, where in the tree that answer
turns off `warden` alone. The label named a destination and what it meant was
what does not run. So the exit names no destination, and its description names
the five things that do not happen.

**The exit is last, and that is a decision rather than an ordering.** This
document warns below that a preset makes the least-verified path the cheapest
to press. The exit is one click and it is that path, so it sits where a
reader's eye lands last, and its description states the cost. It stays cheap to
press and expensive to use by a mechanism that already exists: `[no-review]`
waives one command, typed in front of each, which is a per-command price none
of the other answers pays.

### Question 2 — `multiSelect`, meaningful only under *per axis*

**The order is the specification, not an incidental listing.** The first box is
a property of the run; the three below name parties, in the order they run. A
reader meeting four boxes of apparently the same kind reads the first as a
fourth party to switch on, and that separation is the cheapest defence against
it. If these are ever generated from a list, the list is what carries the order.

| Order | Box | Checked | Not checked |
|---|---|---|---|
| 1 | **run end to end without stopping to ask** | the run goes from here to its destination with nobody at the keyboard · `Automation` = `yes` | **this run may stop to ask** — somebody may be asked at minute thirty · `Automation` = `no` |
| 2 | **implement with `smith`** | spawn the subagent · `Implementation` = `smith` | **this session writes the code** · `Implementation` = `the session` |
| 3 | **review with `warden`** | the review rounds run · `Review` = `through the review chain` | **nothing reviews this code before the pull request** · `Review` = `straight to the PR` |
| 4 | **open the pull request** | push it and open one · `Destination` = `open the pull request` | **the branch is handed back, committed and unpushed** · `Destination` = `stop before the pull request` |

**What is checked is the answer, and each box is a row of the declaration** —
which is why each box's description carries its unchecked meaning too. That is
the half a label cannot say and the half the measured instance got wrong. Box 1's
unchecked half is the one most easily misread: `no` says this run may stop to
ask, never that a person did the work by hand.

**The ceiling, stated where the shape is defined.** `AskUserQuestion` allows at
most four options per question. Question 2 sits at exactly four, and the room
was made by taking the framer and the sealer out of the question. **It is fully
spent: a fifth box breaks this shape**, and whoever adds one is back on #88's
original wall — two questions in one call, or a preset that hides the axes.

### What the answer writes

Question 1's first two options and question 2's four boxes write the same rows;
what differs is how many clicks it took and which row says so.

| Row | Answers |
|---|---|
| Automation | yes · no — OPTIONAL; absent reads as never asked |
| Implementation | smith · the session — OPTIONAL; absent reads as unanswered |
| Review | through the review chain · straight to the PR |
| Destination | open the pull request · stop before the pull request |
| Answer pressed | automation · per axis — OPTIONAL; absent reads as unanswered |

**`automation` writes all four party rows at their checked values**, plus
`Automation` = `yes`, plus `Answer pressed` = `automation`. Ticking all four
boxes under `per axis` writes the same four rows and `Answer pressed` =
`per axis`.

**That last row is why the preset buys anything.** Without it a pressed preset
and four boxes somebody ticked by hand are the same bytes, so a chosen answer
goes back to being indistinguishable from a question nobody read — #151's shape
exactly, and the reason `seal mode` writes a row saying a person was asked.
Question 1's third option never reaches the row: it opens no work item, so
there is no file to write it in.

**`Automation` is an audit trail, not a gate.** Nothing at the pull request can
hold a run to it — a session that promised not to stop and then stopped leaves
no artifact to find. What it buys is that a run which stopped at minute thirty
has now broken something a reader can point at.

**The declaration has one more row, and nobody is asked about it.**

| Axis | Answers |
|---|---|
| Planning | framer · the session — OPTIONAL; absent reads as unanswered |

It is a record, not a checkbox. #88 holds the rule a box here would break
— the question grows only where a decision is genuinely a person's — and this
one is not a person's: `agents/framer.md`'s `## When you run` says the SDD
ladder decides, so the framer runs where §3 calls for a `spec.md` and nowhere
else.

So fill the row from what happened. `framer` where the frame was drawn by the
subagent, `the session` where this session drew it, and no row at all where
the ladder called for no frame. A wrong answer here is contradicted by
nothing, which is why `hooks/implementer-notice.py` says one line after a
commit when a declared agent left no mark — for this row and for
`Implementation` together, in one line rather than one each.

**Asking one part of this later is the failure, not a lesser version of it.**
Measured here: routing at the start, the reviewer in the middle, the pull
request at the end — three interruptions, in the session that had the
one-batch rule loaded. Nothing had said the three belonged to one question, so
obeying the rule for the first of them looked like obeying it.

**It is YOUR question, whether or not a framer runs**, and that is a property
of the harness rather than a preference. **A subagent here has no
`AskUserQuestion` and no equivalent** — measured from two agents independently,
each declaring no `tools:` key and inheriting the full set: the tool is not in
the list and `ToolSearch` for it returns *No matching deferred tools found*. A
document that handed this act to the framer would be telling an agent to call a
tool it does not have.

So the one moment of human contact is here, before the first edit, and the
order does not change when a framer runs:

```
you        : ask the two questions in one call        ← the tool is here
you        : write and commit routing.md
the framer : read, judge, write spec / plan / questions
you        : read plan.md and spawn the build         ← the approval
```

`agents/framer.md` §*You have no interactive phase* is the other half of this,
and it tells a framer that arrives to a missing `routing.md` to report it
rather than write one — a declaration written from a guess is a recorded answer
nobody gave.

**Write the answer down before the first edit**, in
`seal/specs/<work-item-id>/routing.md`, from `templates/sdd-routing.md`. Committed,
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
| direct | open the PR | the review arm stays silent | the sealer takes the broad run, then the PR opens | the sealer's `broad-gate.md` in the work item's directory — the one broad run, at a SHA, against the base — and no round record; the answer turns off the reviewer alone |
| direct | stop before the PR | the review arm stays silent | the branch is handed back | **nothing runs** — say so in the handback; the sealer's record is owed when a pull request opens |

That column is about the review arm. The gate has two arms, they are separate
opt-ins, and each has terms that **wake** it and terms that **quiet** it.
Prose has described this three times and lost a different term each time, so
it is a table:

| | Review arm | Parity arm |
|---|---|---|
| **Wakes when** | `seal/` exists in the repository the commit lands in, whatever the change touches — a commit confined to `docs/` and `seal/` wakes it too | `seal/parity.md` exists there, **and** the change touches something outside `docs/` and `seal/` |
| **Quiets when** | a `routing.md` declaration names this branch, for either answer · the review mark stands at HEAD, written by the review chain · `[no-review]` rides in front of one command | the parity mark stands at HEAD, written by a recorded comparison against the original · `[no-parity]` rides in front of one command |

Two things the sentences kept dropping. A declaration reaches the review arm
only, so a migration repository still meets the parity arm on a code-touching
commit. And a commit confined to those two directories never wakes the PARITY
arm at all — which is why the `routing.md` commit this section mandates costs
nothing even in a migration repository, and why asking would only teach a
reader to click through the prompt. (Both were once read the other way round
in one session, which put the question to the user twice; the table above is
unambiguous and the sentence is what gets read, so the sentence names the arm.)

The declaration is what the commit gate reads, for **either** review answer.
A work item routed to the chain used to carry "no marker at all", and that was
true only after the first review mark landed — false for every commit before
it, which is why every commit of every round was stopped on its way to the
reviewer the answer had already named.

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
request against the round record, the direct answer against the sealer's
`broad-gate.md` at the same place — and there is no third value meaning no
enforcement anywhere. The declaration silences the review arm for either
answer, so no token checks the direct answer at any commit; what the answer
turns off is the reviewer, and the broad run is owed just the same.
Deciding early does not weaken the question; it moves it to the minute where
answering it costs a reply rather than a stopped session.

## Orchestrator: which of these acts runs itself

Every act addressed to the orchestrator sits under a heading carrying the
`Orchestrator:` prefix, in this file or in
`skills/code-review/orchestration.md`, and until #330 there was no list of
them. This is the list.
`tests/test_every_orchestrator_act_names_its_delivery.py` holds it against
both files from both sides: an act with no row fails, and a row naming an act
no file carries fails. One-sided is the state `broad_gate.PARTITION` was
written to end one subject over, and that list went three releases at five
entries while the workflow it mirrored went to thirteen steps.

**The row set is mechanical.** Every `##` heading whose text begins
`Orchestrator:` in either file, plus every `###` heading directly beneath
one. This section is one of those headings, so it has a row of its own.

**`Delivered by` answers one question: when the orchestrator forgets this
act, what notices?** Four values and nothing else.

| Value | What it says |
|---|---|
| `command: <path>` | the act is one command somebody types, so there is nothing to reconstruct from prose. The path has to exist |
| `check: <path>` | something refuses, or says so, when the act did not happen. The path has to exist |
| `part of its parent's act` | a `###` describing its parent's act rather than naming one of its own. A `##` cannot take it |
| `still a sentence` | nothing notices. The `Grounds` cell says what was looked at and came back empty, and an empty cell there fails |

**A command does not make anybody run it, and a row naming one says so where
that is the case.** The miss #330 measured for the flow log is that the meter
sat unreferenced through a full day of measurements nobody took: the
measurement was not taken, not that the posting failed. So the grounds of a
row whose delivery reaches only part of its act name the part it does not
reach. A row that reads closed over a tree that is not is worse than no row
at all, because the next work item picks its subject from this table.

**What this does not catch**, stated rather than left to be found: an act
written for the orchestrator under a heading carrying no marker has no row
and nothing notices. The check reads the marker, not the meaning, which is
the limit
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` already
states for itself. The two read the headings through one parser, so they
cannot come to different answers about what a heading is.

**The one act outside this table is the one #330 measured, and it is named
here because the table cannot hold it.** Posting a segment's reading to the
flow log is structurally the orchestrator's — contract §6 withholds posting
from every agent whatever its definition says — and it lives in
`skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*, under
a heading carrying no marker, in a file the row rule above does not read. Its
delivery is `session-cost … --post`, which resolves the label, applies the
invariant and posts the reading with what a person says about it. **And
nothing makes it run.** The miss the ticket measured is that the meter sat
unreferenced through a full day of measurements nobody took: the measurement
was not taken, not that the posting failed. So this paragraph is the row that
act would have, written where the table's own blind spot put it, and it is
not a closed-looking one.

| Act | File | Delivered by | Grounds |
|---|---|---|---|
| Orchestrator: the order inside a ticket | `skills/implement/orchestration.md` | still a sentence | Nothing reads the order. Each step it sequences has a row of its own, and what the sequence itself asserts, which party runs when, is in no file a check opens. A run that opened the pull request after the rounds leaves the same tree as one that opened it before them |
| Orchestrator: Bootstrap — create what's missing | `skills/implement/orchestration.md` | check: `hooks/mode-gate.py` | A root with no `Mode` row in `config.md` is exactly nobody was asked, and this gate stops the next command until `seal mode` writes it. It reaches the mode question alone. Nothing reads the `Broad gate` proposal, so a repository that was never offered candidates meets `bin/broad-gate`'s own refusal after the rounds have settled, and nothing checks that the workflow file was written from the template with the version substituted |
| Orchestrator: Parity setup — deriving what can be derived | `skills/implement/orchestration.md` | still a sentence | The four fields are derived by hand and nothing reads the result. The commit gate's parity arm wakes on `seal/parity.md` existing, so a setup that never happened is silence rather than a refusal, and a guessed original produces a file that parses |
| Orchestrator: how the work is routed — two questions, one call, one file | `skills/implement/orchestration.md` | check: `hooks/commit-review-gate.py` | The review arm asks at every commit until a declaration naming the branch stands in the working tree, and `templates/claude-md-block.md` carries the question's exact shape into every session on the machine. What neither reaches is the shape of the asking: a declaration built from four separate questions parses exactly like one built from the single call this section mandates |
| Question 1 — single-select | `skills/implement/orchestration.md` | part of its parent's act | The three options of the one `AskUserQuestion` call its parent describes. It names no act of its own |
| Question 2 — `multiSelect`, meaningful only under *per axis* | `skills/implement/orchestration.md` | part of its parent's act | The four boxes of the same call, and the ceiling on how many there may be. It names no act of its own |
| What the answer writes | `skills/implement/orchestration.md` | check: `skills/code-review/scripts/chain_check.py` | It refuses a `Review` or `Destination` value outside the vocabulary at the pull request, and `hooks/routing.py` parses the same rows at every commit. The three optional rows are read by nothing that refuses: `hooks/implementer-notice.py` says one line after a commit where a declared agent left no mark, and blocks nothing |
| Orchestrator: which of these acts runs itself | `skills/implement/orchestration.md` | check: `tests/test_every_orchestrator_act_names_its_delivery.py` | The test holds this table against both files from both sides, which is the condition #330 set for enumerating the class at all: unless something reads it. It reads the marker and not the meaning, so an act written under a heading with no prefix is in neither the table nor the test |
| Orchestrator: a fix pass resumes the implementer | `skills/code-review/orchestration.md` | still a sentence | A resumed fix pass and a fresh spawn leave identical trees, so nothing at the pull request can tell them apart, and the measured difference between them is 282 calls against 30. The steps inside the section are commands, `bin/round-record` for the fix table and `bin/survivor-check` for the sweep that follows, and the choice of session is not one of them |
| Orchestrator: the run ends with a verifying round | `skills/code-review/orchestration.md` | check: `skills/code-review/scripts/chain_check.py` | It fails the pull request when the run's last record carries `nobody` beside a checked `Pass`, which is the run whose own last fixes nobody opened. Work items begun before its cutoff print instead of failing |
| The cap is a ceiling, and this is the floor it never had | `skills/code-review/orchestration.md` | check: `skills/code-review/scripts/chain_check.py` | It reads `Loses a record or crashes` on every record and refuses a run whose count of records passes the bound that row sets. What it cannot read is whether the reviewer's answer was true |
| A fix pass adds the unit that pins it, and that unit ships unreviewed | `skills/code-review/orchestration.md` | command: `bin/round-record` | `close` derives `New units` from the fix range with a depth per entry, and refuses depth 2 before any cell is written. It does not reach the level above: a fix pass that adds mechanism, a rule or a checker or a template section or a walk, leaves a unit at depth 1 and nothing refuses it |
| Then say who checked them, in the record | `skills/code-review/orchestration.md` | command: `bin/round-record` | `new` sets the previous record's cell when it writes the next round's, so the act is no longer a last step to remember, and it was forgotten five times on the branch before it existed. `skills/code-review/scripts/chain_check.py` refuses any value outside the three |
| And name the fix surface, in the same record | `skills/code-review/orchestration.md` | command: `bin/round-record` | `close` writes `Contract changes` and `New units` from the fix range, so the rows cost no question to anybody. Before it did, one record sat at its starting values for two rounds and the six units its fix pass created reached the next round only because a reviewer went and looked. What the derivation does not reach is a surface with no unit in it: `New units` reads top-level defs, classes and module constants, and for a file the AST cannot read the `+` lines for five keywords, so a fix pass that adds a template section, a skill rule or a walk names an empty surface and nothing refuses it |
| And say what ran the round | `skills/code-review/orchestration.md` | command: `bin/round-record` | `new` writes the row from the value the spawning session gives it, and `skills/code-review/scripts/chain_check.py` fails a record missing it after its cutoff and refuses a present row it cannot read. Neither reaches whether the value is true: the agent and the model are the orchestrator's own knowledge, and nothing else in the tree holds them |
| And commit the record before commissioning the fixes | `skills/code-review/orchestration.md` | check: `skills/code-review/scripts/chain_check.py` | It refuses a record whose adding commit descends from a commit its own verdicts name as the fix. `round_record.py new` lists the commits between and refuses nothing, because 40 records of 152 differ that way for a reason that is not this one. Nothing reads whether the reviewer's report rode in the same commit |
| The check a round runs reads everything, and only a write is narrowed | `skills/code-review/orchestration.md` | command: `bin/evidence-check` | A narrowed run names the ledgers it did not read and says how to read them, so the narrowing announces its own blind spot instead of waiting for the pull request to find it. It does not refuse: a round that reads only its own fragment still exits 0, and the unscoped read at the pull request is what found fifteen drifted rows and one broken claim over three rounds that had all reported clean |
| Orchestrator: the pull request opens before round 1, and a phase is re-run | `skills/code-review/orchestration.md` | still a sentence | A pull request opened after the rounds leaves the same tree as one opened before them, so nothing reads the timing, and nothing records that a closed phase's suite and lint were re-run before the next phase spawned. What is delivered is the step the section ends on: `skills/code-review/scripts/chain_check.py` fails a ready pull request whose last record's `Broad gate` cell still reads `not yet`, which is what makes the sealer's spawn happen |
| Orchestrator: verify before posting | `skills/code-review/orchestration.md` | still a sentence | The four checks are readings the orchestrator takes before posting, and nothing in the tree records that any of them happened. The one part a record carries is both SHAs in `Target SHA` where HEAD moved, and `round_record.py new` prints the commits between rather than refusing |
| Orchestrator: closing the cycle | `skills/code-review/orchestration.md` | check: `hooks/commit-review-gate.py` | The review arm quiets on a mark standing at HEAD, so a cycle left unclosed meets the gate at the next commit. On a branch with a routing declaration in force the declaration quiets that arm first, and that is every branch this workflow routes, so for those the missing mark is never noticed |

