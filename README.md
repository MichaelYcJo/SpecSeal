# SpecSeal

[![tests](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml/badge.svg)](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml)

**English** · [한국어](./README.ko.md)

**Specs, sealed** — when code moves under the line a spec cites, CI says so.

![SpecSeal demo: evidence-check catches spec-code drift](./assets/demo.gif)

Coding agents make claims. SpecSeal makes each claim leave something you can
open: a **proof block** the smith prints at the end of its response, naming the
policy files it read and what it actually ran, a **review mark**
(`.git/specseal-reviewed`, holding the reviewed HEAD sha) that a commit hook
looks for, and an **evidence ledger** (`seal/ledger.md`) pairing each spec
clause with the code that grounds it.

Commit without a current review mark and the hook stops the commit and puts the
choice in front of you. Move the lines a ledger row cites and the check script
exits non-zero. Neither is a wall — both are a record you have to walk past
knowingly.

Distributed as a Claude Code **plugin**; the ledger, the drift checker, and
the handoff protocol work anywhere git does.

## Why the always-on context is 12 lines

A seal is small; that is the point. Based on
[arxiv 2602.11988](https://arxiv.org/abs/2602.11988), context files generally
do *not* improve task success while adding over 20% inference cost — the model
already knows SOLID, DRY, and "read before edit". SpecSeal ships only what
changes default behavior; everything else loads when summoned (skills) or
works outside the context entirely (hooks).

## What ships

| Who / what | Follows | What it concretely is |
|---|---|---|
| **smith** (Claude Code subagent) | `agent-contract` · `implement` · `writing-style` | Implements against the spec, then prints a three-line proof block: which policy files it opened, which ledger rows it touched, what it executed versus merely read. The block is a disclosure the skill requires, not something a hook verifies — but `none — <reason>` in a row is visible to you |
| **warden** (subagent) | `agent-contract` · `code-review` · `writing-style` | Reviews spec compliance first, then quality. Once its report is verified the orchestrator writes the reviewed HEAD sha to `.git/specseal-reviewed`, which is what the commit gate looks for — the reviewer never writes its own mark |
| **scribe** (subagent) | `agent-contract` · `legacy-parity` | Records what the original code does as `path#anchor` coordinates and returns facts, not verdicts. Appears only in repos that declare `seal/parity.md` |
| Skills | — | Twenty-three, in three groups. The five the agents follow are in the column to the left. Eleven more a session loads on its own when the work calls for them — `audit`, `build-fix`, `checkpoint`, `commit-pr-convention`, `confidence-check`, `debug`, `evidence-check`, `feature-planner`, `gap-analysis`, `learn`, `verify`. Seven you invoke by name; they are in the cheat sheet below |
| Hooks | — | The gates themselves — auto-registered by the plugin, no settings wiring |
| CLAUDE.md block | — | 12 always-on lines — four section headings (`Tooling`, `Safety`, `Session cost`, `Git`) over eight rules: one on tooling, three on safety, one on session cost, three on git. No response-language rule — that stays yours |

## The chain

```
smith forges → verify (scoped) → warden reviews → report to the user
      ↑                                                │
      └──── reforge ↔ re-review, rounds 1..n ──────────┘
                          │ rounds settle
                          ▼
             broad gate — full suite, lint, typecheck, ONCE
                          │
        new breakage → back to the loop (three returns, then stop)
        failing on base too → named as a follow-up, does not block
                          ▼
                        PR / commit
commit  → unless .git/specseal-reviewed matches HEAD, the hook puts the two
          ways on to you: review it, or commit with [no-review]
```

**The broad checks run once, after the review rounds settle.** Evidence binds
to a tree state, so a full suite taken before the rounds is spent by the first
fix they cause — measured on one work item: twenty broad runs, every one
followed by more edits, none surviving to the handoff, and together more than
half the session's tool time. The smith hands over with the suite
`unverified` and says so; narrowing the scope is honest only because the label
is not omitted. At the gate, the run is read against the base commit: a
failure that predates the work is named as a follow-up rather than chased, and
nothing edits between that seal and the PR.

`verify` is the smith's own gate before it hands anything over: run the
checks, read the full output, and label each claim as executed, read, or
unverified. The warden audits that record rather than re-running it — did the
command run, can the check fail, is the label honest — which is not the same as
taking its conclusions. The code is still read.

**The warden starts cold.** It runs as a subagent, so the implementation
conversation does not reach it — what carries over is what was written down:
the diff, the specs, and the work item's round records. The one way in is the prompt
that spawns it, so the warden treats implementation rationale found there as
the author's account rather than evidence, and says in its report that it set
it aside. For a review with no path in at all, open a fresh session and call
`@agent-specseal:warden` there: the round history is files, so it is inherited
either way.
The review run is bounded: three rounds, or five while something marked
🔴 *blocks merge* is still open and only to close it. Then it ends whether
or not everything was resolved. What is left is handed over rather than
carried — an unanswered finding to `seal/follow-up.md`, a decision only
you can make to `questions.md`, an original whose behavior is plainly wrong
recorded both ways — each named in the PR body. **The chain ends at a PR,
never at a merge.**
Stopping at a report leaves finished work where nobody will look for it;
merging decides something that was never the chain's to decide. Whether that
PR merges, gets another round, or gets closed is yours.

## The ledger

Cross-session memory lives in the repo, not the session:

| Root | Lifetime | Holds |
|---|---|---|
| `seal/` | permanent | everything this plugin maintains — the ledger, the follow-up list, the repository's own config (the two language rows and the mode live there), the migration config — and, beneath it, the work items. Its existence is also what opts the repository in, for the four hooks that read it — the commit gate, the review-skill gate, the review-history guard and the version check. worktree-guard and session-lease act in every git repo regardless, and lint-python follows ruff (see Where below) |
| `seal/specs/<id>/` | one work item | SDD set: spec, plan, questions, and a closing memo holding only what the diff cannot show. A human approves `plan.md`, which is why this is a repository document and not tool state |
| `docs/` | permanent | whatever policy documents the repository already keeps. **Never created here** — a project's documentation convention is its own |

```
seal/
├── README.md         the export rules — what leaves a work item before it closes
├── ledger.md         spec clause ↔ code coordinates, from before work items
│                     started writing fragments
├── ledger/
│   └── <work-item-id>.md   one work item's rows — no header, folded into ledger.md at release
├── config.md         what this repository says about itself — two languages
│                     and the mode. Optional, and an absent row is not an
│                     error
├── parity.md         migration config, only when declared
├── follow-up.md      schedulable items in a repository with no tracker
└── specs/<work-item-id>/
    ├── routing.md    which way this work item goes, written before the first edit
    ├── spec.md · plan.md · questions.md · overview.md
    ├── rounds/
    │   └── round-N.md    review rounds — committed, drained, then closed and kept
    └── tests-todo.md · evidence-todo.md
```

Judgment runs policy > SDD > code where a repository has policy documents, and
SDD > code where it does not. Most repositories are the second kind, and the
plugin does not manufacture the first.

Missing files bootstrap from `templates/`. The handoff convention is
specified tool-agnostically in
[docs/review-handoff-protocol.md](./docs/review-handoff-protocol.md) — any
agent that reads and writes files in a git repo can conform. It names the
records' home as *the directory that holds the work item*; `seal/specs/<id>/` is
this implementation's answer to that, not the protocol.

The ledger is *checked*, not merely kept. A coordinate names **content, not a
position** — `path#unit@hash`, where the unit is a function or class for code
and a heading for a document, and the hash covers the region under it. The
`evidence-check` skill ships a CI-ready script that
exits 2 when an anchor is gone or ambiguous and 1 when the content under it
changed; both fail a default CI step, and `--strict` makes drift exit 2 too.
What it proves is narrow and worth stating: that the citation still points at
what it claimed, not that the claim it supports is still true. Specs rot
silently everywhere else — here the rot shows up in CI.

**A row carries no line number and no commit.** A line number moves for edits
that have nothing to do with the claim, so inserting a line above a cited
function used to leave the row pointing at the wrong lines while still reading
OK. A unit does not move, so that edit is silent and a real change to the cited
code is not. An anchor also degrades to *re-read this*, never to *go fix the
ledger* — the second is the bookkeeping the design exists to remove. Nothing
is written into a row for a rebase or a squash to
orphan, and the check calls git for nothing — the one exception is
`--migrate`, a one-shot writer that consults the old stamp's commit before it
trusts a line number it is rewriting. Re-verifying a row is
re-reading it and running `evidence-check --reverify`, which recomputes the
hash and names what it changed.

## The gates

Hooks are scripts the plugin auto-registers; they run on your machine at
tool events. One process handles all the gates on an event rather than one per
gate — four interpreter startups per Bash call was most of the cost of having
them (measured: 220ms → 104ms before a Bash call, 323ms → 120ms after). Full
decision tables:
[docs/worktree-guard-spec.md](./docs/worktree-guard-spec.md) ·
[docs/review-chain-spec.md](./docs/review-chain-spec.md).

| Gate | Fires | Does | Where |
|---|---|---|---|
| commit-review-gate | before `git commit` | stops the commit when `.git/specseal-reviewed` does not hold the current HEAD sha, and puts the two ways on to you as options: run the review chain, or commit with `[no-review]` (which stays visible in the command). In a repo that declares `seal/parity.md` it also stops a code commit with no `.git/specseal-parity` for this HEAD — compare against the original, or `[no-parity]`. Both arms are put up together, in one question each. **Once per session per repository** — after that it is the plain confirmation, where approving is the waiver. The repository judged is the one the command commits **into** — `git -C <path> commit` is judged at `<path>`, not where the shell sits. A `-C` the gate cannot resolve to a repository (a shell variable, since the gate reads the command before the shell expands it) stops the commit rather than passing it: it was never looked at, and that used to be indistinguishable from having passed | `seal/` at the root, or under the common git dir in local mode — silent elsewhere. A migration config lives inside it, so declaring one opts into both arms; waive the review arm per command with `[no-review]`, typed in FRONT of the command — `: '[no-review]'; git commit …`, quotes included |
| review-history-guard | after posting/reading a PR review via `gh` | reminds to write / read `seal/specs/<work-item>/rounds/round-N.md` and the two todo files beside `rounds/`. It also names any record left at the old flat location, since nothing reads one there. It finds the work item the way the commit gate does — through the routing declaration that names this branch — so a branch that declared nothing is not reminded | same opt-in |
| implementer-mark | before an Agent/Task call whose `subagent_type` is `smith` (`specseal:smith`, or a project-local `smith`) | writes the checked-out branch name to `.git/specseal-implementer`. It prints nothing, so it can neither deny nor ask; it is the trace the notice below reads. Written before the group decides, so a spawn the worktree guard then stops still leaves one | `seal/` at the root, or under the common git dir in local mode — silent elsewhere, and writes nothing |
| implementer-notice | after a command that actually runs `git commit` | where this branch's `routing.md` answers `Implementation` with `smith` and no mark stands for this branch, prints one line naming the file. Nothing is said when the mark stands, when the row is absent or unreadable, or when it answers `the session`. **Once per session per repository**, and it never blocks — a declared `smith` nobody spawned is a session forgetting its own answer, and a reminder is what that costs | same opt-in |
| review-skill-gate | before the model opens a skill named `code-review` | puts the choice to you rather than making it: that name is Claude Code's built-in, not this plugin's. The built-in sweeps the diff for bugs and cleanup; `specseal:code-review` judges spec compliance first and inherits earlier rounds' verdicts. Fires **once per session per working tree**, so picking the built-in and retrying goes straight through. A skill you invoke yourself never routes through here | `seal/` at the root, or under the common git dir in local mode — silent elsewhere |
| worktree-guard | before `git checkout`/`switch`, `git worktree add`, and Agent calls with `isolation: "worktree"` | one rule in two directions: denies a switch while another session is actively working this tree, and denies creating a worktree when yours is the only live stream. Where the tree holds only idle sessions, or the environment cannot be read at all, it offers the two ways on as options instead — switch here, or split into a worktree — **once per session per repository per direction**, then the plain confirmation. The two directions are counted apart, so one session can legitimately meet the question twice. `[worktree-ok]` and `[shared-tree-ok]` carry your answer back through on the retry. The reason names the other session's host app, how long each signal has been quiet, and its last message | any git repo |
| session-lease | after repo-touching tool calls (Bash · file edits) | writes a timestamp, host, and owning session pid to `.git/specseal-leases/<session-id>`. The guard's process heuristics miss sessions not named `claude`; a lease says outright which session is working here. Nothing removes the file at session end, so the owner is recorded: a lease whose session has exited is retired rather than counted, and one that cannot be attributed becomes a question instead of a block | any git repo |
| version-check | at session start | asks this repository for its newest release tag and, when the running plugin is behind, shows one line naming `/specseal:update`. Once a day, and a lookup that fails retries about twenty minutes later. It never installs anything — telling you a release exists and installing it are different acts | `seal/` at the root, or under the common git dir in local mode — silent elsewhere |
| lint-python | after Write/Edit/NotebookEdit on a `.py` file | runs `ruff check --fix` then `ruff format` on that file — autofixes included, so code changes, not just layout (uv → uvx → global ruff; skips silently if none). `SPECSEAL_LINT=off` disables it | **a project that configures ruff** — `ruff.toml`, `.ruff.toml`, or `[tool.ruff]` in `pyproject.toml`, searched up to the repo root. Silent everywhere else |

The commit gate is not the only place the review chain is enforced any more,
and for work that declares its route it is no longer the place at all. A work
item writes `seal/specs/<id>/routing.md` before its first edit — which way it goes,
and whether it opens a pull request — and the gate reads that instead of
guessing from the absence of a mark. The check moved to the pull request: CI
reads the same file out of the diff and, for anything routed through the
chain, requires a committed round record whose `Pass` does not contradict its
own verdict table. A pull request that declared neither way is not failed; it
gets a notice saying nothing was checked.

Each round record also has to say **who opened the fixes** that closed what it
found. A round's findings are closed after it ends, by whoever writes the
fixes, and the round that follows is what reads them — except after the last
round, where nobody did and the box saying the review passed was ticked by the
session that had just written them. So a run ends with a **verifying round**:
spawned after those fixes are committed, pointed at their diff rather than at
the branch, and asking whether each closed finding is actually closed. A round
that opens nothing needing a fix does not spend one of the three.

The record's `Fixes checked by` row is where that lands. It names a later
round, or says there was nothing to check, or says `nobody` and why. The last
of those prints on every run, and on the run's last record beside a checked
`Pass` it fails the pull request — a review cannot have passed while the fixes
that closed its findings went unread. Work items begun before the rule landed
are excused and only print, so a run that already shipped that way says so in
the diff instead of in a session that has ended.

No gate transmits your code, your paths, or your prompts anywhere. Three side
effects are worth stating outright: session-lease writes a timestamp file under
`.git/specseal-leases/`, version-check writes one under
`~/.claude/specseal/`, and lint-python rewrites the `.py` file you just saved —
in ruff-configured projects only.

Two hooks reach the network. lint-python falls back to `uvx ruff`, and uv
fetches ruff from PyPI on first use. version-check runs one `git ls-remote
--tags` against this repository, once a day where `seal/` exists. A lookup
that fails retries about twenty minutes later rather than waiting out the day.
What that tells GitHub is that a machine somewhere runs SpecSeal. Both stay
silent when the network is unavailable.

One deliberate read to know about:
when the worktree-guard blocks a switch, it quotes the last user message
(80 chars) of the OTHER local session's transcript in its block reason, so
the human can recognize which conversation is being protected. That snippet
stays on your machine.

## Honoring the original (migrations)

A repo that declares `seal/parity.md` (original repo, baseline commit) gets
three-way judgment — policy ↔ original ↔ new, with *preserve the original*
as the fallback — and the scribe fetches the original's facts. Repos without
the config never see any of it.

You do not write that file by hand. The smith asks once, the first time it
sets up a repo's layout: *does this project port behavior from an existing
codebase?* Answer no and it never asks again. Answer yes and it proposes
candidates for the original — sibling checkouts, an upstream in `git remote
-v`, repos whose paths overlap — reads the baseline from whichever you
confirm, and writes the file. Deciding later is `/specseal:parity-setup`.

Your checkout path stays out of the committed file, in
`~/.claude/specseal/parity-paths.md` keyed by the origin remote, since it is
wrong for every other machine.

## Cheat sheet

**Runs by itself (the gates above — nothing to invoke).**

**Run it yourself:**

| Command | Does |
|---|---|
| `evidence-check . [--strict]` | ledger drift check (the demo GIF) — works without any agent. The plugin puts it on PATH; `/specseal:evidence-ci` wires the same check into CI |
| `deferral-check . [--kind all]` | resolve the answerer an `unverified` row names — does anything here actually run the check you are deferring? Separates *answers on pull requests* from *answers too late*, *local hook only*, and *nothing* |
| `unverified-check . [--baseline <ref>]` | read the rows those `unverified` labels left behind — what is still open, in which work item, and who was named to answer it. Fails on a section it cannot read, because a tolerant reader reports zero and zero reads as *all closed*. With `--baseline`, it compares counts: a table with fewer rows than at that revision fails, as does an `overview.md` that was there and is gone. Replacing one row with another keeps the count and passes |
| `session-cost --latest` | where a session's minutes went — command time, model time between calls, checks re-run for a result already produced, and how many tools went out per turn. Fills the seal's `cost` row, which nothing inside a session can measure |
| `/specseal:preset-setup` | approval-gated semantic merge of the CLAUDE.md block |
| `/specseal:evidence-ci` | wire the drift check into CI — vendors the checker and writes the workflow |
| `/specseal:parity-setup` | declare that this repo ports from another codebase — finds the original, records the baseline |
| `/specseal:security-audit` · `/specseal:testing` | prompt checklists the model walks — an OWASP-shaped security pass and a test-strategy pass |
| `/specseal:config` | show what this repository decided for itself — the two languages it writes in and where its records live — and change any of it. Routes a change to whatever owns that row rather than editing behind it |
| `/specseal:update` | take the newest release and see what is in it — runs both update commands in the right order, then names the changelog entries between your version and the new one. Restart to load it |
| `bash install.sh [--project]` / `bash uninstall.sh` | add / remove the CLAUDE.md marker block |

**Inline switches:**

| Switch | Effect |
|---|---|
| `[no-review]` in a commit command | skips the review gate for **that one command**, visibly. Type it in front of the command — `: '[no-review]'; git commit …`, quotes included. After `git commit` a bare word is a pathspec and git rejects the whole command; a trailing `# [no-review]` works everywhere except an interactive zsh, which reads it as an unmatched glob |
| `[no-parity]` in a commit command | skips the original-comparison gate for **that one command**, visibly. Same placement: `: '[no-parity]'; git commit …` |
| `[worktree-ok]` in a worktree command | softens the single-stream worktree deny to ask. Read as a bare word, so it does not count inside a quoted message. An Agent call with `isolation: "worktree"` has no command line and takes no token — it asks outright instead |
| `[shared-tree-ok]` in a switch command | you already chose the shared tree — the switch goes through where the guard could not tell (idle sessions, unreadable environment). Read as a bare word. Ignored while another session is active, and while the tree is dirty |
| `WORKTREE_GUARD_IDLE_MIN=n` | idle threshold in minutes (default 5) |
| `SPECSEAL_LINT=off` | turns the Python auto-format hook off, even where ruff is configured |
| `SPECSEAL_LANG=ko\|en` | worktree-guard's prompts (the other gates are English-only); default follows the system locale |

## Install

**Requirements**: `git`, and **Python 3.12 or newer** resolving as `python3`
on PATH — the gates are Python scripts, and `python3` is the command the
plugin invokes them with. Worth checking rather than assuming: macOS ships
3.9 as `/usr/bin/python3`, and a version manager (pyenv, asdf) resolves
`python3` to whatever it was last told. `python3 -V` is the whole test. On
Windows that name is the one the official installer does not create, so each
hook falls back to `py -3` when `python3` cannot start. Optional: `uv`/`uvx` or `ruff`
for the Python auto-format hook — without them it silently skips.

```bash
# 1. Plugin (agents + skills + gates)
claude
> /plugin marketplace add MichaelYcJo/SpecSeal
> /plugin install specseal@specseal

# 2. CLAUDE.md block — pick ONE scope
bash install.sh            # interactive: global (~/.claude) or project (./)
bash install.sh --project  # non-interactive project scope
```

### Updating

```
/specseal:update
```

It runs both commands below in the right order and then names the changelog
entries between your version and the new one, calling out anything that
changes behavior or needs you to do something. Restart to load it; the session
you are in keeps the version it started with, so nothing is half-applied.

By hand:

```bash
claude plugin marketplace update specseal
claude plugin update specseal@specseal   # then restart
```

Both lines, in that order. The first refreshes the marketplace clone; the
second installs from it. Running only the second reports *already at the
latest version* against whatever the clone last knew. Updates are keyed to the
version in `plugin.json`, not to commits — a change that ships without a
version bump reaches nobody.

`install.sh` backs up to `CLAUDE.md.bak`, merges only its marker block
(idempotent — rerun to update), and never edits your own content: overlaps
are warned about, not resolved. For a reviewed, deduplicating merge run
`/specseal:preset-setup` inside Claude Code instead — every deletion goes through an
approval diff.

### Coming up from 0.3.x

0.3.x kept the plugin's files in two directories (`.specseal/`, `specs/<id>/`);
this release keeps them in one, `seal/`, and that folder's presence is now what
opts a repository in. The old pair opts nothing in any more, so until it is
moved every gate is silent there.

The move happens once, at the first session start after updating. The hook
renames every file with a staged `git mv` (history follows), re-points the
ledger rows that cite a moved file with their hashes untouched, prints one
line saying what moved, and stops there: you review `git diff --cached` and
commit. That commit belongs to no work item, so inside a session the commit
gate asks; waive it for that one command with
`: '[no-review]'; git commit -m "specseal: the root move"`, and put `[no-parity]` in
the same position where `seal/parity.md` exists.

A tree with uncommitted changes under the old pair is refused with a line
saying to commit first, and the next clean session start moves it. A
repository carrying the throwaway marker `.specseal/scratch` is left alone;
its successor is the file `.git/specseal-scratch`, which cannot be committed.

To move by hand instead — in CI, or without waiting for a session:

```bash
mkdir -p seal/specs
git mv .specseal/map.md seal/ledger.md
git mv .specseal/map seal/ledger             # if it exists
git mv .specseal/README.md seal/README.md    # then overwrite it from templates/seal-README.md
git mv .specseal/follow-up.md seal/          # and parity.md, and anything else in there
git mv specs/<id> seal/specs/<id>            # each work item
rmdir .specseal specs                        # git mv leaves them empty on disk; one holding something else stays
evidence-check --reverify .                  # re-points each row citing a moved file
```

## First run

Four of the seven gates wake only under a condition: the commit gate, the
review-history reminder, the review-skill gate, and the version check act in a
repo that has a `seal/` directory at its root or under its git directory, and
stay silent everywhere else. You never create it by hand — the smith builds it
the first time it works in a repo, after asking one question (*Shared or
local*, below), and it is the only directory this plugin adds to your tree —
plus, in shared mode, one workflow file under `.github/workflows/`; in local
mode, nothing at all.

The other three carry their own conditions. worktree-guard and session-lease
act in every git repo. lint-python acts only where the project has configured
ruff — configuring ruff is a project saying it wants ruff, and nothing else is.
Read the Where column above before installing globally.

Agents run only when you name one:

```
> @agent-specseal:smith implement <your ticket>
```

`@agent-` opens a picker that completes the name for you. Spelling it out in
prose works the same way, if you prefer it:

```
> use the specseal:smith agent to implement <your ticket>
```

The smith reads the spec chain, implements, verifies, and hands off to the
warden for review — you decide what happens to the report. Anything the
layout needs and the repo lacks (`seal/ledger.md`, `seal/README.md` carrying
the export rules) the smith creates from `templates/` as it goes.

Two things work with no agent at all: the ledger drift check
(`evidence_check.py`, the demo above) and every gate in the table.

### Shared or local

The first time the smith works in a repository it asks one question, once,
and never again: where `seal/` lives. Whichever place holds the folder is the
mode; there is no config key, and a repository with `seal/` at either place
is not asked.

| | Shared (the default) | Local |
|---|---|---|
| Where `seal/` lives | `<repo>/seal/`, committed | `$(git rev-parse --git-common-dir)/seal/` — under the common git dir, which is `.git/` in a main tree |
| What setup installs | the pull-request checks, `.github/workflows/hygiene.yml` written from the plugin's `templates/hygiene.yml` only if no file is there | nothing; the tree is untouched |
| Fits | your own repository, or one where a committed `seal/` bothers nobody | a repository whose tree must not carry this plugin's files: a company repository, a contribution to someone else's project |
| Gives up | nothing | CI — the checks read committed files — and every other machine or re-clone, which starts empty |

Local mode sits under the git directory rather than behind a `.gitignore`
line because a linked worktree checks out committed files only, so an ignored
folder is simply absent there. The common git dir is shared by every worktree
of the clone, and nothing under it is ever a commit candidate.

**Switching is one command.** It stages; you commit.

```bash
seal mode            # where the root is, what the config says, whether they agree
seal mode local      # move it out of the tree
seal mode shared     # move it into the tree
```

The move itself is two shell lines, printed further down. What the command
adds is everything around them: it refuses when the other mode's root is
already there, refuses over a submodule under the root, refuses when the
index carries a change under `seal/` or at the workflow's own path — `git rm
-r --cached` takes a staged edit out of the index without a word about it —
carries `.github/workflows/hygiene.yml` in and out where it can and says so
where it cannot, and writes the mode into `seal/config.md` so the file and
the folder agree afterwards. The hooks
need no restart: the next command reads the folder where it is.

**The row says what you want; the folder says what you have.** Nothing at
runtime reads the row — every gate finds the root by looking for it, in the
two places above — so the two can disagree, and that is the input the command
consumes rather than an error:

```bash
# edit seal/config.md to say `| Mode | local |`, then
seal mode --apply    # move the folder to what the row says
seal mode --check    # writes nothing; exits non-zero if they disagree
```

`--check` is what the pull-request checks run, so a row that stops being true
is caught rather than left standing. A repository that has never declared one
is not lying about anything: the first `seal mode` writes the row from where
the folder actually is.

**The two directions do not cost the same.** Going to local takes the records
out of the tree, and every other clone loses them at the next pull — `seal
export` here and `seal import` there is how a teammate gets a copy. Going to
shared is the one to be sure about: once you commit, the records are in the
history, and taking them out of the tree later does not take them out of it.
Until that commit, `git reset -- :/seal :/.github/workflows/hygiene.yml` and
then
`seal mode local` walk the whole thing back — the switch stages, and the guard
refuses a switch over a staged change. The pathspec is there because a bare
`git reset` unstages the whole index, and the guard has never looked outside
those two paths.

By hand it is a move and a commit, from the repository root — both paths are
asked of git, so a subdirectory as the working directory lands them in the
same place:

```bash
# local → shared, then commit
mv "$(git rev-parse --git-common-dir)/seal" "$(git rev-parse --show-toplevel)/seal" && git add "$(git rev-parse --show-toplevel)/seal"
# shared → local, then commit the removal
git rm -r --cached "$(git rev-parse --show-toplevel)/seal" && mv "$(git rev-parse --show-toplevel)/seal" "$(git rev-parse --git-common-dir)/seal"
```

Doing it that way leaves the workflow file where it was, and that is the half
worth knowing about. Copy `$CLAUDE_PLUGIN_ROOT/templates/hygiene.yml` in with
`v<version>` replaced by the release you run, or delete
`.github/workflows/hygiene.yml`. Left behind after a move to local it runs
checks that read committed files in a repository that commits none: one of
them goes red on every pull request forever, and the other goes green having
examined nothing.

Between two machines the move is not available, because the other machine has
no folder to move. That is what `seal export` and `seal import` below are for,
and they are the second way to switch modes as well.

### Carrying local records to another machine

Local mode's trade-off is that the records never leave the clone. `seal
export` and `seal import` make that *take a copy* rather than *lose it*.
Both ship on the Bash tool's PATH while the plugin is enabled.

```bash
seal export                 # writes seal-<repo>-<date>.zip beside the clone
seal import <the zip>       # takes one in, overwriting nothing
```

The zip holds the root and nothing else. The smith mark, the worktree
choices, the review and parity marks and every lease sit *beside* the root
under the git directory, so none of them travels — the export walks the root,
which is why the root has to be its own directory. A symbolic link inside it
is skipped and named rather than followed. Alongside the files goes a
manifest naming the remote URL and the HEAD SHA at export.

**Import never overwrites and never asks.** A file that is not there is
added. One that is there with the same bytes is left alone, so re-importing
the same zip writes nothing. One that is there with different bytes gets the
incoming copy beside it — `ledger/<id>.incoming.md` next to
`ledger/<id>.md` — and the collision is listed. Which of a pair is right is a
reading, not a merge, and no answer the command could pick would avoid
sometimes throwing work away. `evidence-check .` afterwards says which ledger
rows drift against this tree.

It refuses, writing nothing, when the zip came from another repository
(`--allow-other-repo` if the two are one repository under two spellings),
when the manifest declares a format this build does not read,
when a member would land outside the root, when a member or the whole zip
declares more bytes or more members than a root of records holds, when a
member cannot be read — a bad checksum, encryption, a compression method this
build has no decompressor for — when a name has to be a directory for the zip
and is a file, and when both roots already exist.

Those all stop before the first byte. One failure cannot: if a directory in
the root cannot be written into, or the disk fills, the copy stops part-way
and says what the filesystem said. Fix that and run it again — nothing is
overwritten, so a second run finishes the copy and reports what was already
there byte for byte.

A symbolic link at a name a collision would fall back to is treated as taken:
the copy lands at the next free name rather than being written through it.
`seal export` does the same with the zip's own name. If anything is already
at the temporary name it writes through, it refuses and leaves that alone —
it removes a half-written archive of its own, never a file it found there.
`seal import --into shared` or `--into local` creates the named mode's root,
which is the other way to switch modes: export, import into the other place,
commit or remove.

In shared mode `seal export` writes no zip. The records are committed, so
every clone and CI already have them, and it prints the path and the `mv`
that switches to local mode instead. Once per release, `seal export --check`
prints one line — how many work items changed since the last export — and
uploads nothing anywhere. Where the copy goes is nobody's business but yours.

## Limits

What this does not do is as load-bearing as what it does.

- **The gates put the decision to you; they do not block.** The commit gate
  stops the call and hands you the ways on as options; retrying reaches an
  ordinary prompt where approving is the waiver, and `[no-review]` in the
  command skips it outright. It is a speed bump for an agent about to commit
  unreviewed work, not a security control — anyone who can answer a prompt can
  commit.
- **evidence-check proves a citation still resolves, not that it is true.**
  `DRIFTED` means someone must re-verify, not that the claim is wrong. A
  coordinate that still resolves while the code's meaning changed reports
  `OK`.
- **The proof block is a disclosure, not enforcement.** No hook reads it. Its
  value is that a `none — <reason>` row is visible to you in the transcript.
- **"Broad and once" is a rule the agents follow, not a gate.** Nothing stops
  a session from running the full suite mid-round; what exists is the
  instruction, the warden's audit of the seal, and the `round-N.md` field that
  makes a repeat visible. A hook could not tell the difference anyway —
  whether the rounds have settled is not a property of the command being run.
- **`Fixes checked by: nobody` prints everywhere and fails in one place.** On
  the run's last record, beside a checked `Pass`, it fails the pull request: a
  review cannot have passed while the fixes that closed its findings went
  unread. Anywhere else it only prints. Work items begun before this rule
  landed are excused entirely, because a check whose first act is red on merged
  history nobody can repair is a check people learn to skip. The way out costs
  no round — one verifying round at the diff of those fixes.
- **A parity mark says someone compared, not that they compared well.** The
  gate checks that a comparison was recorded for this HEAD; the quality of
  that comparison is the reviewer's, and writing the mark for work you did not
  compare turns "nobody checked" into "someone checked and it was fine".
- **Session detection is heuristic.** Extension-hosted sessions aren't named
  `claude`, and a session editing this tree from another cwd leaves no trace
  here. Leases close most of that gap, but only for sessions that have run a
  tool recently. Where detection is unusable the guard hands you the two ways
  on instead of deciding, and the attempt after that is an ordinary
  confirmation — no environment is locked out by it.
- **Windows was run on real hardware once, and one defect is still open
  there.** Until 2026-08-26 this section claimed the `windows-latest` suite
  passed; it did not — 72 cases failed, were filed as an issue, and were fixed since on
  a native Windows 11 tree. The entry point was measured on the same machine:
  the `hooks/hooks.json` command line, run through `cmd.exe` against an
  opted-in repository, returned a `deny` and then an `ask`. `python3`
  resolved, so the `py -3` fallback is still unrun on Windows — it was
  verified on POSIX by removing the first name from PATH. The console-encoding
  defect that stood beside it is closed: a plain `pytest tests/` on
  a Korean cp949 console passes whole, with no `PYTHONUTF8=1`.
- **The conformance evals have never run.** `evals/` is written against
  `claude plugin eval`, which is early access; the suite awaits enablement.
  CI checks their shape — required fields, a grader per case — which is what
  can be checked without the runner. Treat them as authored, not as passing.

## Contributing

Changes to a gate carry a higher bar than the rest of the tree, because a gate
decides whether someone's commit proceeds: a test seen failing before the fix,
a stated failure direction, and honesty about platforms you could not test.
See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Language policy

Functional files (skills, agents, hooks, commands) are English-only — they
load into model context, and a translated mirror would drift. Korean exists
for human-facing docs only (this README). One deliberate exception: the
writing-style skill carries per-language prose rules (Korean and English
sections) — independent norms, not mirrors, so the drift argument does not
apply. Response language follows the user's own CLAUDE.md settings — the
distributed block does not impose one.

## License

MIT
