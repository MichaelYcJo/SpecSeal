# One plugin-owned root, laid out by lifetime

*English · [한국어](./one-root-by-lifetime.ko.md)*

The design 0.4.0 starts from, gathered from issue #74 and the ten comments
under it (2026-09-02, after 0.3.0 shipped). Nothing here is for 0.3.x. Every
name below is a placeholder until the owner decides it; where the thread
leaned one way, the text says *recommended* and the reason. The decisions
themselves are collected at the end, under "Decisions left open".

The numbers in this document were re-measured against `origin/main` at
`5685029` (the 0.3.0 merge) on 2026-09-02. Where the issue's own numbers
differ, both are given.

## The change in four lines

Today two committed roots hold files that live for three different lengths
of time, and neither root sorts by that. `specs/<id>/` holds a work item's
documents and its review records, which die at different times, and
`.specseal/` holds the ledger (the table pairing spec clauses with code
coordinates), whose rows outlive the work item that wrote them. After this
change one root the plugin owns holds everything, sorted by how long it
lives. The opt-in signal moves out of the tree into local git
state, and `specs/` becomes a directory SpecSeal reads and never writes.

```
today                                      after
─────                                      ─────
specs/<id>/   spec plan questions overview  seal/specs/<id>/  the whole work item
              routing rounds/ todos pr.ko  seal/ledger/<id>.md  its rows, until the release
.specseal/    map.md map/<id>.md            seal/ledger.md    the gathered ledger
              follow-up.md parity.md        seal/follow-up.md seal/parity.md
(.specseal/ exists)  = opted in            git config specseal.*  = opted in
```

## The problem, as measured

| Observation | Measured at `5685029` | In the issue | What it says |
|---|---|---|---|
| `specs/` after one week | 13 work items · 101 files · 6,937 lines | 13 · 96 · 6,655 | after a merge nothing mechanical reads a round record, and people rarely do |
| `.specseal/map/` | 6 fragment files, 79 anchored rows across `map.md` and `map/` | 83 live rows | the rows are bounded by live claims; the files are one per work item forever, and almost every pull request touches the directory |
| `specs/` is spec-kit's directory too (GitHub's spec-driven toolkit writes `specs/NNN-feature/`) | — | — | two tools would write one folder |

The issue's counts were taken before this document's; what was counted
differently was not traced.

Half of the `specs/` lines are `rounds/` and `overview.md`: 2,147 and 1,279
lines respectively. The rows are fine; the files and the churn accumulate.

These are one defect. **Things with different lifetimes share a folder, and
things with the same lifetime are split across two.**

| What | Real lifetime | Where it is today |
|---|---|---|
| spec · plan · questions · overview | until the release that carries it; git history and the CHANGELOG's work-item comment keep it after | `specs/<id>/` |
| routing · rounds · todos | while the pull request is open (the commit gate and `chain_check.py` read them) | `specs/<id>/` |
| ledger rows | as long as the code they cite lives, which is longer than the work item | `.specseal/map/<id>.md` |
| follow-up · parity | as long as the repository | `.specseal/` |

### Where the line between a person's files and the tool's actually runs

The criterion behind "keep `specs/`, hide `.specseal/`" was whether a person
would have written and read the file without this tool. That criterion does
not coincide with the `specs/` folder boundary.

| A person's, the shape spec-driven development (SDD) prescribes | The tool's, in SpecSeal's vocabulary |
|---|---|
| `spec.md` · `plan.md` · `questions.md` · `overview.md` · `changelog.md` | `routing.md` (read by the commit gate, the hook that stops an unrouted commit) · `rounds/round-N.md` (read by `chain_check.py`, the pull-request check that a declared review chain has its record) · `tests-todo.md` · `evidence-todo.md` |

Separating the two kinds inside a work item is out of scope by the owner's
decision. Round records have to be in the tree while the pull request is
open, and pulling them apart from the spec is a larger change than this one.
The design below therefore does not assume `specs/` is tool-free; it uses the
line only to decide what is worth keeping after a release.

## The proposed tree

One root the plugin owns. "Plugin-owned" means the plugin creates, moves and
empties it and its checkers define the formats, the way `.github/` is
GitHub's. It is committed in the default mode, because the ledger and the
round records must reach CI and other clones.

```
<repo>/
├── seal/                          created, moved and emptied by the plugin. Committed in shared mode.
│   ├── README.md                  this folder's rules: export rules, what disappears when
│   ├── ledger.md                  the gathered ledger. Permanent
│   ├── ledger/<id>.md             rows of work items in development — folded into ledger.md at release, then deleted
│   ├── follow-up.md               permanent
│   ├── parity.md                  migration projects only. Permanent
│   └── specs/<epoch>-<slug>/      the whole work item. See "Retention" for what survives the release
│       ├── spec.md plan.md questions.md overview.md      what a person reads
│       ├── changelog.md                                  gathered into CHANGELOG.md at release
│       ├── routing.md rounds/round-N.md                  what the commit gate and CI read
│       ├── tests-todo.md evidence-todo.md                evidence-todo must be empty before the release empties anything
│       └── pr.ko.md
├── docs/                          policy — where intent that outlives a release lives. Unchanged
├── specs/                         never written by SpecSeal; if present (spec-kit, a person) read as policy input
├── CHANGELOG.md                   unchanged
└── .git/                          session state, never committed. Unchanged
    ├── specseal-implementer       the smith mark (the file a spawned smith agent leaves behind)
    ├── specseal-worktree-choice/  the worktree question's record
    └── config                     specseal.mode / specseal.optin: the opt-in signal, per clone or --global
```

Three lifetimes, and each has one home.

| Lifetime | Lives in | Ends when |
|---|---|---|
| a session | `.git/` | the session ends |
| between releases | the tool's files in `seal/specs/<id>/` · `seal/ledger/<id>.md` | the release-preparation step runs |
| permanent | `seal/ledger.md` · `follow-up.md` · `parity.md` · `docs/` · `CHANGELOG.md` · the person's files in `seal/specs/<id>/`, under the proposed retention default | never |

With `retain = none` the person's files join the middle row; with `all`,
the tool's files join the last.

Against today, the root itself changes in three ways: two roots become one,
opt-in moves from a directory's existence to a local config key, and the
work-item directory and the ledger fragments gain a lifetime. The later
comments added on top of that, and the sections below carry them: two
choices at first setup, a retention rule, and an export/import pair.

**The relationship the names spell out.** The top-level `specs/` (spec-kit's,
a person's) is what gets sealed. `seal/specs/<id>/` is the sealed copy with
its process record. `seal/ledger*` is the seal itself: the binding of spec to
code that breaks on drift.

## What happens at a release

Both accumulation problems end with one rule in the release-preparation
step. The thread names only "the release-preparation script"; this document
reads that as the step that already gathers `changelog.md` fragments by hand
(`.github/scripts/gather_changelog.py --version`, see
`docs/branch-and-release.md`).

1. `seal/ledger/<id>.md` of every released work item folds into
   `seal/ledger.md`, and the fragment is deleted. A work item still unmerged
   keeps its fragment.
2. `seal/specs/<id>/` of every released work item is emptied according to
   the retention setting below.
3. **Guard before emptying.** A sentence in a work item's `spec.md` that must
   outlive the release has to have moved into a `docs/` policy or a ledger
   row before the merge. `evidence-todo.md` half-enforces that today; once
   the step deletes files, it must refuse to run while any work item still
   has an open `evidence-todo.md` row. The issue says "any work item"; an
   unmerged one is not emptied, so this document reads it as any released
   one.

Why the rows fold rather than stay is this document's reading, not the
thread's: the fragment layout exists to stop two branches queueing at one
file, and after the merge there is no branch left to queue.

## What "spec" means after this

Nothing changes here. `spec.md` was always the spec of one change. What must outlive the
change already has two homes: the `docs/` policy (judgment order is policy >
SDD > code) and the ledger row, which carries the clause text beside the code
coordinate. A person checking the AI's work does it while the pull request is
open, when `spec.md` is there. A person asking "why does this behave so" after
the release reads `docs/` and the ledger.

## The opt-in signal leaves the tree

Only what the checkers read must be committed: the ledger (CI's `ledger` job,
other clones) and `routing.md` / `rounds/` (the commit gate and
`chain_check.py` while the pull request is open). The signal itself is read
locally by the hooks, so it can live in any of three places.

- a git config key (`git config specseal.optin true`, per clone, or
  `--global` per machine; linked worktrees share it). Nothing in the tree.
- a marker under `.git/`, where the smith mark and the worktree choice
  already live. Per clone.
- the presence of a fetched ref, if the ledger ever moves to an orphan
  branch. Follows a clone automatically.

All three keep today's fail direction: absent means not opted in.

**What changes is the meaning.** Today the committed root is the repository's
declaration. Clone it and every collaborator's gates are on. A local signal
makes it the developer's choice for that clone.

A collaborator who does not opt in then commits without gates, and the
repository-level guarantee becomes CI's, since the ledger and chain checks
run from the workflow regardless of opt-in. For a plugin distributed to
others that is the right split: the tool's user turns it on, the repository
does not impose it. If chosen, the root loses its role as marker and the
tree carries only what the checkers read.

| | Today | After |
|---|---|---|
| What opts a repository in | `.specseal/` exists at the root (`hooks/optin.py`) | a local config key or `.git/` marker |
| Who decides | whoever committed the directory, for every clone | each developer, for their clone |
| A collaborator who did not opt in | gated anyway | commits without gates; CI still checks the pull request |
| The `.specseal/scratch` opt-out | an empty file that turns the gates off in a throwaway fixture | no longer needed as such: a fixture simply never sets the key (see "Decisions left open") |

## Two choices at first setup

The one moment this project allows a question is first setup, so both
choices are asked there and never again.

### Shared or local

The question is not "commit the folder or not" but "do CI and collaborators
see this workflow".

| Mode | `seal/` lives at | Gains | Loses |
|---|---|---|---|
| shared (default) | `<repo>/seal/`, committed | CI's ledger and chain checks; the same state in every clone and worktree; records survive a re-clone | one folder in the tree |
| local | `.git/seal/`, never committed | nothing in the tree; gates and the review chain still run in this clone | every CI check; other machines; the records on re-clone |

Local fits a solo repository or a contribution to someone else's tree. The
implementation is a config key written at setup (`specseal.mode = shared |
local`). The same flag decides that the hygiene workflow (the pull-request
checks in `.github/workflows/hygiene.yml`) is not installed, because it
would refuse a pull request with no round records.

**Why local mode is under `.git/` and not gitignored.** A linked worktree
checks out committed files only, so an ignored `<repo>/seal/` in the main
tree is simply absent in every worktree. The owner hit exactly this when
`.specseal/` was ignored and parallel sessions could not read each other's
records. It was git's behaviour, not a configuration mistake. So local mode
keeps `seal/` inside the common git dir (`git rev-parse --git-common-dir`,
i.e. `.git/seal/`), beside the smith mark and the worktree-choice records:
shared by every worktree of that clone, never a commit candidate, no
`.gitignore` line needed.

The owner's summary of the two modes, corrected for that:

1. At first setup, choose whether `seal/` is in the commit range. Shared mode
   puts it at `<repo>/seal/` and commits it; local mode puts it at
   `.git/seal/`, which is never committed.
2. In both modes, worktrees and parallel sessions read each other's records.
   In shared mode because the files are committed, in local mode because
   the git dir is common. Local mode has no per-branch isolation of
   uncommitted state; the per-work-item fragment layout is what keeps
   parallel items apart.
3. Local mode never leaves that clone on that machine. A new machine or a
   re-clone starts with no ledger and no work-item records (coordinates are
   re-derived), and CI's ledger and chain checks cannot run. That is the
   whole trade-off.

**Local records can be copied to another clone by hand.** The ledger's rows
are content anchors (`path#unit@hash`, no line, no SHA), so a copied ledger
degrades to DRIFTED (the checker's "content changed, re-read the claim"
state) where the other tree differs, and never breaks. Round records name
pushed commits. `.git/seal/` must be its own folder so that it alone is
copied; the smith mark, worktree choices and session leases beside it are
that machine's session state.

**A copy is not a sync, and the modes convert into each other.** Last copy
wins, and the person tracks which rows went, so needing a copy twice is the
signal to switch to shared mode. Either switch moves `.git/seal/` to
`<repo>/seal/` or back, then commits or removes. The setup choice is "where
does it live now", not a one-way door.

**Local mode gets an export/import pair**, so its trade-off becomes "take a
copy" rather than "lose it".

- `seal export` zips `.git/seal/` alone, never the session state beside it,
  into `seal-<repo>-<date>.zip` with a manifest naming the remote URL and the
  HEAD SHA at export.
- `seal import <zip>` never overwrites. Files are keyed by work-item id, so
  missing ones are added; an id already present lands as
  `<id>.incoming.md` beside the existing file, reported and not asked
  about. `evidence-check` afterwards says which rows drift against this
  tree.
- The same pair is the mode switch: export, unzip into `<repo>/seal/`,
  commit. Or the reverse.
- One reminder only. In local mode the release-preparation step prints
  "N work items changed since the last export". Nothing is uploaded
  anywhere; where the copy goes is the user's business and not a question
  the plugin asks.

### Retention of the work item after release

The contents of `seal/specs/<id>/` split by who reads them after the merge.
Measured on this repository's 13 work items at `5685029`:

| | Files | Lines | Share | Value after release |
|---|---|---|---|---|
| a person's record | spec · plan · questions · overview · changelog | 3,737 | 54% | yes. Like architecture decision records, "why" is browsable without git archaeology |
| the tool's record | rounds · routing · todos · pr.ko | 3,143 | 45% | none. Read only while the pull request is open |
| neither | `ab-comparison.md` (one work item) | 57 | 1% | — |

The issue measured 3,736 (56%) against 2,975 (44%). What was counted
differently was not traced; the split is the same.

Default proposed: keep the person's record, delete the tool's at release.
Growth halves and everything left is worth reading. Keeping all is a valid
choice too, at the cost of size only, so `retain = people | all | none` can
be the second setup option. The default matters more than the number of
options.

This choice and the root's name are linked: see the naming section.

## Naming

**Product name, recommended: keep SpecSeal; use bare `seal` as the vocabulary
inside it.** The
root `seal/`, the `seal export` / `seal import` commands, "the seal" for the
record.

| Name | Its one sentence | Why not |
|---|---|---|
| SpecSeal | seals a spec to the code that implements it | — names what and how; says "spec borrowed, seal ours"; reads the spec-kit relationship (they write, we seal) |
| Seal | seals | circular without its object; heavy collisions (Microsoft SEAL, kubeseal); unfindable as a marketplace name |
| AiSeal | seals what AI made | names the maker, not the thing sealed; the prefix dates; collisions |

A compound product name with a one-word command inside is an ordinary
arrangement (Sealed Secrets / `kubeseal`). Renaming costs the repository URL,
the marketplace entry, `plugin.json`, hook-file prefixes, install docs and
three tags' worth of history. If the plugin is ever renamed, 0.4.0 is the one
cheap moment, because this change renames the root anyway. Revisit only if
the scope really outgrows "spec", and then among seal compounds, not AI ones.

**Root name, recommended: `seal/`, visible, rather than `.seal/`.** A dot is a declaration
about the folder's nature, not a mechanism. With opt-in in local config the
hooks do not care either way. `specs/` in spec-kit is visible because people
write and read what is in it. If the person's record is kept after release,
as the retention default proposes, it is a document set and belongs in the
visible row beside `docs/`. Choose `.seal/` only if the work item is emptied
entirely at release and footprint is the priority. Either way, switching later
means renaming one directory.

**Sub-directory name, recommended: `seal/specs/<id>/`, not `work/`.** A directory has to say
what is in it to whoever opens it first. `work` says nothing, and a metaphor
(`forge/`) hides the contents. smith and warden stay as agent personas,
where a name may describe character, and are not used for directories.
`specs/` names the primary artifact and is the first half of the product's
name, so the tree reads as the relationship it is.

**English stays for every shipped artifact**, since this is a plugin for
others and every token costs. Korean is the owner's per-user setting: the
response language and `pr.ko.md`.

## What happens to the existing directories at the switch

- **Released work items in `specs/`.** Every folder there at 0.3.0 belongs to
  a released work item. The issue body says they are deleted rather than
  moved, because history and the CHANGELOG comments keep them and every
  `Target SHA` in a round record is a commit that still exists. With the
  retention default of "keep the person's record", the consistent answer is
  to apply that same rule at the switch: move the person's files under
  `seal/specs/<id>/` and delete the tool's. Which of the two applies is a
  decision (see below).
- **A work item unmerged at the switch** is moved whole by the session-start
  hook. `hooks/ledger-migrate.py` already owns that moment: it migrates once
  per repository, never over uncommitted files, and prints one line. The
  existing once-per-repo marker (`~/.claude/specseal/ledger-migrated`) is
  keyed to the anchor-format migration, so the path move needs a marker of
  its own.
- **`.specseal/map.md` and `.specseal/map/`** become `seal/ledger.md` and
  `seal/ledger/`. `follow-up.md` and `parity.md` move as they are.
- In this repository `specs/` then ends up empty and goes away.

## What it touches in this repository

Files on `origin/main` that mention `.specseal/` or `specs/`, counted per
area (a rough grep, not a list of edits):

| Area | Files | The load-bearing ones |
|---|---|---|
| `hooks/` | 11 | `optin.py` (`HOME = ".specseal"` is the whole signal today), `ledger-migrate.py`, the commit gate's `routing.md` path |
| `skills/` | 13 | `implement` (the three-axis layout table, fragment paths), `code-review`, `verify`, `evidence-check` and their scripts |
| `tests/` | 20 | fixtures that build `.specseal/` and `specs/<id>/` by hand |
| `templates/` | 8 | five SDD templates (spec, plan, questions, round, routing) name their `specs/<epoch>-<slug>/` path in a header comment; `sdd-overview.md` and `map.md` name `.specseal/map` |
| `.github/` | 2 | `hygiene.yml` passes `specs/` to `unverified_check.py`; `gather_changelog.py` globs the fragments. `test.yml`'s `ledger` job names no path (`evidence_check.py .`) and is outside the count, but the checker it runs must learn the new root |
| `agents/` | 3 | the smith, warden and scribe agent prompts |
| `docs/` | 3 | `branch-and-release.md`, `review-chain-spec.md`, `review-handoff-protocol.md` |
| root | 4 | `README.md`, `README.ko.md`, `CONTRIBUTING.md`, `CLAUDE.md` |

The CI paths change in step 3 of the order below, together with the root.

## What does not change

- Every gate's fail direction: cannot tell means not opted in.
- Fragments per work item during development, gathered only at release.
  That is what removed the merge conflicts, and three parallel branches
  benefited from it on 2026-09-01.
- `.git/` session state (the smith mark, the worktree choice, session
  leases) stays where it is, never committed.
- `docs/` and `CHANGELOG.md`, and the judgment order policy > SDD > code.

## Order

1. **Name decisions**: plugin name kept or not, root name, sub-directory
   name. The only human decision here.
2. **The release-automation item** takes "fold `ledger/`, empty the work
   item by the retention rule, refuse on open evidence-todo rows". Doable on
   today's paths, before the root merges.
3. **0.4.0: the root merge.** The session-start hook migrates once; CI paths
   change; `docs/` and the skills' path references follow.
4. **Later and separate**: taking state out of the working tree entirely,
   with an orphan branch as the ledger's home, opt-in by ref. That was the
   first version of this issue.

## Out of scope

- Separating the person's files from the tool's inside a work item while it
  is in development. They move together. The issue body put this out of
  scope outright; the retention rule from a later comment does split them,
  but only at release and only by deleting. That is the one place the split
  exists, and decision 4 is where it is decided.
- Anything in 0.3.x.

## Decisions left open

Each item names the options and what decides between them. The first four
are the ones the thread names as the owner's. Items 5 to 7 surfaced while
writing this document: 6 sets two positions the thread took at different
times against each other, and 5 and 7 are not in the thread at all.

| # | Decision | Options | What decides it | Where the thread leaned |
|---|---|---|---|---|
| 1 | Plugin name | keep SpecSeal · rename | rename costs the URL, marketplace entry, `plugin.json`, hook prefixes, install docs, three tags of history; 0.4.0 is the one cheap moment | keep SpecSeal |
| 2 | Root name | `seal/` · `.seal/` | visible if the person's record is kept after release (it is then a document set); dotted only if the work item is emptied entirely and footprint wins | `seal/` |
| 3 | Sub-directory name | `specs/` · `work/` · a metaphor | it must say what it holds to a first-time reader | `specs/` |
| 4 | Retention default | `people` · `all` · `none` | `people` halves growth and keeps what is readable; `all` costs size only; `.seal/` fits only under `none` | `people` |
| 5 | The opt-in key's shape | `specseal.optin = true` (comment 2) · `specseal.mode = shared \| local` (comment 4) · both | one key is enough if `mode` set means opted in; two keys let a clone be opted in without having chosen a mode, which is a state nothing needs | not discussed as one question |
| 6 | The existing `specs/` at the switch | delete all (issue body) · apply the retention rule (comment 4's default) | consistency with decision 4: if people's records are kept from 0.4.0 on, deleting the 13 that exist is the one exception | the body predates the retention comment |
| 7 | The `scratch` opt-out | drop it · keep it as a `.git/` marker | with a local key, a throwaway fixture opts in by never setting the key, so the file has nothing left to do; the tests that use it need the new shape | not in the thread |

Decisions 2, 4 and 6 are one choice seen from three sides. Take them together.
