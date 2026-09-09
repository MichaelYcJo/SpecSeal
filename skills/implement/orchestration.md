# implement — the orchestrator's half

The three sections `skills/implement/SKILL.md` used to carry for the session
that spawns agents, under the `Orchestrator:` prefix `code-review` already
used for its own. They are the procedure for **starting** a work item:
creating the `seal/` root the first time a repository opts in, setting up
parity mode where a project ports an original, and asking the one routing
question — three axes, one question, one file — before the first edit.

**Read this if you are orchestrating a work item.**
`skills/implement/SKILL.md` is the other half and holds the implementation
itself — the record language, the document layout, the spec-first procedure,
the evidence feedback, the SDD file set, the closing memo and the review
incorporation. An orchestrator reads both; a `smith` spawn preloads that one
and never this, because asking a person and writing `routing.md` are acts
`agents/smith.md` leaves to the session that spawned it.

Nothing here changed when it moved, except one sentence a `# RIDER:` had
asked to name its arm. The headings keep the `Orchestrator:` prefix they were
marked with, so a reference to one of these sections names the section it
always named and only the file it names changed (#292, the shape #265 gave
`code-review`). Every `seal/…` path here means what it means in the other
half: `<repo>/seal/` where that directory exists, and
`$(git rev-parse --git-common-dir)/seal/` otherwise (contract §16).

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

1. Ask, once, with one `AskUserQuestion` carrying two options, in this order:

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

## Orchestrator: how the work is routed — three axes, one question, one file

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
| direct | open the PR | the review arm stays silent | the PR opens | nothing required |
| direct | stop before the PR | the review arm stays silent | the branch is handed back | nothing |

That column is about the review arm. The gate has two arms, they are separate
opt-ins, and each has terms that **wake** it and terms that **quiet** it.
Prose has described this three times and lost a different term each time, so
it is a table:

| | Review arm | Parity arm |
|---|---|---|
| **Wakes when** | `seal/` exists in the repository the commit lands in | `seal/parity.md` exists there, **and** the change touches something outside `docs/` and `seal/` |
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
request against the round record, the direct answer by the token in every
command — and there is no third value meaning no enforcement anywhere.
Deciding early does not weaken the question; it moves it to the minute where
answering it costs a reply rather than a stopped session.

