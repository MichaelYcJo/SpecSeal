# One plugin-owned root, laid out by lifetime

*English · [한국어](./one-root-by-lifetime.ko.md)*

The design 0.4.0 starts from, gathered from issue #74 and the ten comments
under it (2026-09-02, after 0.3.0 shipped), plus the decisions the owner took
after the thread while this document was reviewed: the opt-in is the root's
presence, a work item's directory is removed only once a later `settle`
step has folded it into `docs/` and the ledger, and 0.4.0 itself deletes
nothing. Nothing here is for 0.3.x. Every name below is a placeholder until
the owner decides it; where the thread leaned one way, the text says
*recommended* and the reason. What is decided and what is still open are
both collected at the end.

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
lives. Where that root sits is a per-repository choice, shared (committed)
or local (under `.git/`, never committed), and its presence there is the
opt-in. `specs/` stops being SpecSeal's directory. A work item's directory
lives until `settle` folds it into `docs/` and the ledger; 0.4.0 has no
such step yet, so it moves everything and deletes nothing.

```
today                                      after
─────                                      ─────
specs/<id>/   spec plan questions overview  seal/specs/<id>/  the whole work item, until settle folds it
              routing rounds/ todos pr.ko  seal/ledger/<id>.md  its rows, until the release folds them
.specseal/    map.md map/<id>.md            seal/ledger.md    the gathered ledger
              follow-up.md parity.md        seal/follow-up.md seal/parity.md
(.specseal/ exists)  = opted in            seal/ exists at the mode's place = opted in
```

## The problem, as measured

| Observation | Measured at `5685029` | In the issue | What it says |
|---|---|---|---|
| `specs/` after one week | 13 work items · 101 files · 6,937 lines | 13 · 96 · 6,655 | after a merge nothing mechanical reads a round record, and people rarely do |
| `.specseal/map/` | 6 fragment files, 79 anchored rows across `map.md` and `map/` | 83 live rows | the rows are bounded by live claims; the files are one per work item forever, and almost every pull request touches the directory |

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

### Where the line between the SDD set and the process record runs

Comment 1 drew a line through the work item by asking whether a file would
exist without this tool. Under SpecSeal the AI writes every file in the
directory, so the line is not about who writes; it is about what the file
is and who reads it after the merge.

| The SDD set: what was decided and why | The process record: what SpecSeal's checkers read |
|---|---|
| `spec.md` · `plan.md` · `questions.md` · `overview.md` · `changelog.md` | `routing.md` (read by the commit gate, the hook that stops an unrouted commit) · `rounds/round-N.md` (read by `chain_check.py`, the pull-request check that a declared review chain has its record) · `tests-todo.md` · `evidence-todo.md` |
| exists under spec-driven development (SDD) with or without SpecSeal | exists because SpecSeal's gates read it |
| read by people after the merge, for "why" | read by nothing after the merge |

Separating the two kinds inside a work item is out of scope by the owner's
decision. Round records have to be in the tree while the pull request is
open, and pulling them apart from the spec is a larger change than this one.
The design below therefore does not assume `specs/` is tool-free. The line
is used for one thing: saying what `settle` folds (the SDD set) and what it
simply drops with the directory (the process record).

## The proposed tree

One root the plugin owns. "Plugin-owned" means the plugin creates, moves and
folds it and its checkers define the formats, the way `.github/` is
GitHub's. It is committed in the default mode, because the ledger and the
round records must reach CI and other clones.

```
<repo>/
├── seal/                          created, moved and folded by the plugin. Committed in shared mode.
│   ├── README.md                  this folder's rules: export rules, what moves when
│   ├── ledger.md                  the gathered ledger. Permanent
│   ├── ledger/<id>.md             rows of work items in development. Folded into ledger.md at release, then removed
│   ├── follow-up.md               permanent
│   ├── parity.md                  migration projects only. Permanent
│   └── specs/<epoch>-<slug>/      the whole work item. Lives until settle folds it; 0.4.0 keeps it
│       ├── spec.md plan.md questions.md overview.md      the SDD set: what was decided and why
│       ├── changelog.md                                  gathered into CHANGELOG.md at release
│       ├── routing.md rounds/round-N.md                  the process record: what the commit gate and CI read
│       ├── tests-todo.md evidence-todo.md                evidence-todo must be empty before anything folds
│       └── pr.ko.md
├── docs/                          policy, and where settle folds the SDD set. Read by people; written by people and by settle
├── CHANGELOG.md                   unchanged
└── .git/                          never committed
    ├── seal/                      local mode only: the whole root above lives here instead of <repo>/seal/
    ├── specseal-implementer       the smith mark (the file a spawned smith agent leaves behind). Session state, unchanged
    └── specseal-worktree-choice/  the worktree question's record. Session state, unchanged
```

Three lifetimes, and each has one home.

| Lifetime | Lives in | Ends when |
|---|---|---|
| a session | `.git/` | the session ends |
| between releases | `seal/ledger/<id>.md` · `seal/specs/<id>/` | the release step folds it: ledger fragments from 0.4.0 on, work items once `settle` exists |
| permanent | `seal/ledger.md` · `follow-up.md` · `parity.md` · `docs/` · `CHANGELOG.md` | never |

A work item's directory has the middle lifetime, and 0.4.0 keeps it on disk
anyway, because the step that folds it does not exist yet and deleting
before folding is the half that cannot be undone. The dependency rule below
is what keeps that step possible.

Against today, the root itself changes in three ways: two roots become one,
the root may sit under `.git/` instead of in the tree, and the fragments and
work items gain a lifetime. The later comments added on top of that, and
the sections below carry them: the mode choice at first setup, and an
export/import pair.

**What the names say.** `seal/specs/<id>/` holds the spec and its process
record. `seal/ledger*` is the seal itself: the binding of spec to code that
breaks on drift.

## What happens at a release

Both accumulation problems end in the release-preparation step. The thread
names only "the release-preparation script"; this document reads that as
the step that already gathers `changelog.md` fragments by hand
(`.github/scripts/gather_changelog.py --version`, see
`docs/branch-and-release.md`).

1. **`seal/ledger/<id>.md` folds into `seal/ledger.md`**, and the fragment
   is removed. A work item still unmerged keeps its fragment. This is a
   move, not a deletion: every row survives, and it is the one part of the
   design that answers "almost every pull request touches the directory".
   From 0.4.0.
2. **`seal/specs/<id>/` folds into `docs/`, then the directory is
   removed.** This is `settle`, a later item and not in 0.4.0. It merges
   the SDD set of each released work item into `docs/<domain>` files,
   merging into a document that already exists and creating one only for a
   new area. The newest work item wins where two say different things.
   Each folded sentence carries the work item id as an HTML comment, the
   way a CHANGELOG entry does, so a reader can trace a rule back through git
   history after the directory is gone. The process record is dropped with
   the directory: nothing reads it after the merge. This rule replaces the
   retention setting comment 4 proposed; there is nothing left to choose
   to keep, because what is worth keeping has moved.
3. **The guard.** A sentence in a work item's `spec.md` that must outlive
   the release has to have moved into a `docs/` policy or a ledger row
   before the merge. `evidence-todo.md` half-enforces that today. The
   release step refuses to run while any released work item still has an
   open `evidence-todo.md` row (the issue says "any work item"; an unmerged
   one is not part of the release), and `settle` skips such an item:
   neither folded nor removed, named in its output. The guard is what makes
   removal safe: it is the proof that nothing permanent lives only in the
   work item.

Why the rows fold rather than stay is this document's reading, not the
thread's: the fragment layout exists to stop two branches queueing at one
file, and after the merge there is no branch left to queue.

## The dependency rule

**Anything that must outlive a release may not read `seal/specs/<id>/`
after the merge.** The directory will be removed by `settle`, so the design
treats it as already gone for every permanent purpose. Measured against the
code on `origin/main`, the reads of that directory fall into three groups.

- **Already safe.** A ledger row carries the clause text beside the code
  coordinate, so it never points into `spec.md`. A round record's
  `Target SHA` is read by `chain_check.py` only while the pull request is
  open. The HTML comment above a released CHANGELOG entry, and the one
  `settle` leaves in `docs/`, name the work item; a name is a pointer
  rather than a read, and it still resolves through git history when the
  folder is gone.
- **Would break on removal, so must change before `settle` lands.**
  `skills/verify/scripts/unverified_check.py --baseline` compares the
  work-item tree against the base revision and fails for "a file that was
  there and is gone"; it has to be scoped to work items the pull request
  touches, or to unmerged ones. `.github/scripts/gather_changelog.py --check`
  finds fragments that never reached `CHANGELOG.md` by reading the
  fragments; after a removal it can only judge by the comment in
  `CHANGELOG.md`. Both are named here so the `settle` item starts from
  this list rather than rediscovering it.
- **Kept on purpose.** The evidence-todo guard above; the export rules in
  `seal/README.md`, which say where each kind of content must have gone
  before the work item closes; and `settle` itself, the one sanctioned
  reader after the merge, in the same position as the ledger fold.

A new reader of `seal/specs/<id>/` after 0.4.0 lands in the second group by
definition, and a review should say so.

**The wider rule behind it: nothing may need to be found and updated when
something else moves.** The ledger already went through this once. A row
cited `path:line`, a line moves for edits that have nothing to do with the
claim, so rows were re-anchored, stamped, and orphaned by a squash. 0.2.0
replaced the position with a content anchor (`path#unit@hash`), and a row
now changes state only when the code it is about changes. `settle` rewrites
`docs/` and removes directories on every release, so anything coupled to a
path or a position inside a work item would break the same way. What still
carries such a coupling is short: the `Verified at <sha>` stamp on a
`# RIDER:` comment (held together by the merge-method rulesets, and untouched
by `settle`), and a round record's `Target SHA` (resolved through
`refs/pull/<N>/head`, and gone with the record).

**What keeps `settle` light**, since it is the heaviest step this design
adds:

- It moves and does not verify. Whether a coordinate still holds is
  `evidence-check`'s job; folding it in would re-read the whole ledger on
  every release.
- It runs incrementally. Only work items released since the last fold are
  read, and the folded ids are recorded so a second run folds nothing twice
  and an interrupted run resumes.
- The `docs/` merge replaces by provenance id. A sentence carrying a work
  item's comment is swapped for the newer one; judgment is needed only when
  an area gets its first document.
- An item with an open `evidence-todo.md` row is skipped and named, never
  folded or removed.
- Its cost is measured with `session-cost`, so the release where it turns
  heavy is visible.

## What "spec" means after this

Nothing changes here. `spec.md` was always the spec of one change. What must
outlive the change already has two homes: the `docs/` policy (judgment order
is policy > SDD > code) and the ledger row, which carries the clause text
beside the code coordinate. `settle` is the step that moves it there for
every released work item. A person checking the AI's work does it while the
pull request is open, when `spec.md` is there. A person asking "why does
this behave so" after the release reads `docs/` and the ledger, and `docs/`
now holds the folded record of every change, not only the norms people
wrote by hand.

`docs/` is defined by who reads it, people, and not by who writes it. The
`implement` skill's layout table says `docs/` is "never created here", and
that sentence overclaims once `settle` writes there; it is one of the
places the `settle` item corrects.

## The opt-in signal is the root itself, wherever the mode put it

**A repository is opted in when `seal/` exists at its mode's location**:
`<repo>/seal/` in shared mode, `.git/seal/` in local mode. The hooks look at
the two places in that order; whichever exists says both "on" and which
mode. Nothing else is read, and there is no config key. This is the owner's
decision after the thread; the thread itself leaned another way, described
below.

| | Today | After |
|---|---|---|
| What opts a repository in | `.specseal/` exists at the root (`hooks/optin.py`) | `seal/` exists at the mode's location |
| Who decides | whoever committed the directory, for every clone | shared: whoever committed it, for every clone that installed the plugin. Local: the developer of that clone |
| A collaborator who did not set anything up | gated anyway, if the plugin is installed | shared: the same. Local: nothing runs, because their clone has no `.git/seal/` |
| The `.specseal/scratch` opt-out | an empty file that turns the gates off in a throwaway fixture | no longer needed as such: a fixture simply creates no `seal/` (see "Decisions left open") |

**What the thread proposed instead, and why it is not needed.** Comment 2
argued that only what the checkers read must be committed, so the opt-in
could be a local signal separate from the folder: a git config key
(`specseal.optin`, later `specseal.mode`), a marker under `.git/`, or a
fetched ref. The point was that a committed root should not impose the
gates on every collaborator; a local key would make it each developer's
choice per clone. Two things make the key redundant once local mode lives
under `.git/`:

- In local mode the folder's presence already is a per-clone signal.
  `.git/seal/` exists only in the clone that set it up, so a key beside it
  would say the same thing twice.
- In shared mode the imposition is smaller than it reads. The hooks belong
  to the plugin, so a collaborator who never installed SpecSeal runs
  nothing, key or no key. The only person a committed `seal/` reaches is one
  who installed the plugin and cloned this repository, and that person is in
  the same position under today's `.specseal/`.

The fail direction is unchanged: no folder at either place means not opted
in, and a hook that cannot tell does nothing.

## What first setup asks

The one moment this project allows a question is first setup. The thread
proposed two questions there, the mode and the retention; retention went
away with the `settle` rule, so one remains.

Today the `implement` skill has one once-per-repo moment, when it creates
`.specseal/README.md`; that moment becomes the question. One
`AskUserQuestion` with two options, shared first as the default, each
option saying what it does:

- **shared** creates `<repo>/seal/` and commits it, and installs the hygiene
  workflow.
- **local** creates `.git/seal/` and installs no workflow. Nothing touches
  the tree.

A repository that already has `seal/` at either place has been through this
and is never asked again; the mode is read from where the folder is.

### Shared or local

The question is not "commit the folder or not" but "do CI and collaborators
see this workflow". Which answer fits is mostly decided by whose repository
it is.

| | Local mode | Shared mode |
|---|---|---|
| Fits | a repository with its own conventions where this plugin's files must not appear in the tree: a company repository, a contribution to someone else's project. Also a solo repository that wants nothing extra committed | your own repository, or any repository where a committed `seal/` bothers nobody |
| Where `seal/` lives | `.git/seal/`, inside the common git dir | `<repo>/seal/`, in the tree |
| Committed | never; nothing to gitignore either | yes |
| Linked worktrees and parallel sessions | read each other's records, because the git dir is common to every worktree of the clone | read each other's records, because the files are committed |
| Other machines and a re-clone | start empty; `seal export` / `seal import` carry a copy by hand | have everything |
| CI (`ledger` and chain checks) | cannot run; the hygiene workflow is not installed | runs |
| Switching later | move `.git/seal/` to `<repo>/seal/` and commit | move `<repo>/seal/` to `.git/seal/` and remove from the tree |

The mode needs no key of its own: the hooks find `<repo>/seal/` or
`.git/seal/` and that is the mode. Setup also decides whether the hygiene
workflow (the pull-request checks in `.github/workflows/hygiene.yml`) is
installed; in local mode it is not, because it would refuse a pull request
with no round records.

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

### Retention: measured, and answered by `settle`

The contents of `seal/specs/<id>/` split by who reads them after the merge.
Measured on this repository's 13 work items at `5685029`:

| | Files | Lines | Share | Value after release |
|---|---|---|---|---|
| the SDD set | spec · plan · questions · overview · changelog | 3,737 | 54% | yes. Like architecture decision records, "why" is browsable without git archaeology |
| the process record | rounds · routing · todos · pr.ko | 3,143 | 45% | none. Read only while the pull request is open |
| neither | `ab-comparison.md` (one work item) | 57 | 1% | — |

The issue measured 3,736 (56%) against 2,975 (44%). What was counted
differently was not traced; the split is the same.

Comment 4 proposed keeping the SDD set and deleting the process record at
release, with `retain = people | all | none` as a setup option. The owner's
decision after the thread makes the setting unnecessary: the SDD set is
folded into `docs/` by `settle` and the whole directory is then removed,
so what the measurement says is worth keeping is kept, in `docs/`, and
nothing is left in the directory to choose about. Until `settle` exists
nothing is deleted.

## Naming

**Product name, recommended: keep SpecSeal; use bare `seal` as the vocabulary
inside it.** The root `seal/`, the `seal export` / `seal import` commands,
"the seal" for the record.

| Name | Its one sentence | Why not |
|---|---|---|
| SpecSeal | seals a spec to the code that implements it | — names what and how; says "spec borrowed, seal ours" |
| Seal | seals | circular without its object; heavy collisions (Microsoft SEAL, kubeseal); unfindable as a marketplace name |
| AiSeal | seals what AI made | names the maker, not the thing sealed; the prefix dates; collisions |

A compound product name with a one-word command inside is an ordinary
arrangement (Sealed Secrets / `kubeseal`). Renaming costs the repository URL,
the marketplace entry, `plugin.json`, hook-file prefixes, install docs and
three tags' worth of history. If the plugin is ever renamed, 0.4.0 is the one
cheap moment, because this change renames the root anyway. Revisit only if
the scope really outgrows "spec", and then among seal compounds, not AI ones.

**Root name, recommended: `seal/`, visible, rather than `.seal/`.** A dot is
a declaration about the folder's nature, not a mechanism. The hooks look for
the folder by name at two places and do not care whether it is dotted.
Comment 9 tied the choice to what stays after release: visible if people
read what is in the folder, dotted if it is emptied entirely. With
`settle`, a released item leaves the folder, but the items in flight are
exactly what people read while the pull request is open, so the visible
name still fits. Either way, switching later means renaming one directory.

**Sub-directory name, recommended: `seal/specs/<id>/`, not `work/`.** A
directory has to say what is in it to whoever opens it first. `work` says
nothing, and a metaphor (`forge/`) hides the contents. smith and warden stay
as agent personas, where a name may describe character, and are not used
for directories. `specs/` names the primary artifact and is the first half
of the product's name.

**English stays for every shipped artifact**, since this is a plugin for
others and every token costs. Korean is the owner's per-user setting: the
response language and `pr.ko.md`.

## What happens to the existing directories at the switch

- **Every work item in `specs/`** moves whole to `seal/specs/<id>/`, released
  or not. The issue body said released ones are deleted, because history
  and the CHANGELOG comments keep them; under the `settle` rule they wait
  there for the first fold instead, which is what "delete nothing before
  folding" means at the switch.
- **The move is done by the session-start hook, once.** `hooks/ledger-migrate.py`
  already owns that moment: it migrates once per repository, never over
  uncommitted files, and prints one line. The existing once-per-repo marker
  (`~/.claude/specseal/ledger-migrated`) is keyed to the anchor-format
  migration, so the path move needs a marker of its own.
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
- `CHANGELOG.md`, and the judgment order policy > SDD > code. `docs/` keeps
  its role as what people read; it gains `settle` as a writer.
- Every file a work item writes today. 0.4.0 changes where they live, not
  whether they exist.

## Order

The tickets are grouped into releases on GitHub milestones, and
`docs/flow.md` is the checklist that tracks them until the last one merges.
0.4.0 carries #78, #30 and #79 only; everything a person can live without
for one release moved to 0.5.0, because even that set is large.


1. **Name decisions**: plugin name kept or not, root name, sub-directory
   name. The only human decision here.
1. **The sealer (#30)**, first of the tickets, because its rule applies to
   every work item from here on, the root merge included.
2. **The release-automation item (#78)** takes "fold `ledger/`, refuse on open
   evidence-todo rows". Doable on today's paths, before the root merges.
3. **0.4.0: the root merge (#79).** The session-start hook moves
   everything once; CI paths change; `docs/` and the skills' path
   references follow. Shared mode only.
3. **0.5.0**: local mode and the first-setup question (#80),
   `seal/config.md` for per-repository settings such as the pull request
   language (#82), and `seal export` / `seal import` (#81).
4. **Later: the `settle` item (#83)**, and the framer (#84), the agent
   that writes the frame the smith fills. For `settle`, first the two checks in "The dependency
   rule" stop reading released work items; then `settle` folds released
   work items into `docs/` and removes their directories, and the
   `implement` skill's description of `docs/` is corrected to match.
5. **Later and separate (#85)**: taking state out of the working tree
   entirely, with an orphan branch as the ledger's home, opt-in by ref. That
   was the first version of this issue.

## Out of scope

- Deleting anything from `seal/specs/<id>/` in 0.4.0. Removal arrives with
  `settle`, and only after a fold.
- Separating the SDD set from the process record inside a work item while
  it is in development. They move together; the line between them is used
  only to say what `settle` folds and what it drops.
- Anything in 0.3.x.

## Decided after the thread

Taken by the owner on 2026-09-02, while this document was being reviewed.

| Decision | Answer | What it closes |
|---|---|---|
| The opt-in signal | `seal/` existing at the mode's location; no config key | comment 2's key, marker and ref candidates; the question of the key's shape |
| What happens to a work item's directory | it lives until `settle` has folded its SDD set into `docs/` and its rows into the ledger, then it is removed; 0.4.0 has no `settle` and deletes nothing | comment 4's `retain` setting and its default; the second setup question; the existing `specs/` moves whole |
| Design stance toward the directory meanwhile | nothing permanent may depend on `seal/specs/<id>/` after the merge, and nothing may need finding and updating when a path or position moves | the dependency rule; the two checks that must change before `settle` |
| Where the folded record lives | `docs/`, defined by who reads it (people), written by people and by `settle` | the `implement` skill's "never created here" sentence, to be corrected |

## Decisions left open

Each item names the options and what decides between them. The first three
are the ones the thread names as the owner's. Item 4 surfaced while writing
this document and is not in the thread.

| # | Decision | Options | What decides it | Where the thread leaned |
|---|---|---|---|---|
| 1 | Plugin name | keep SpecSeal · rename | rename costs the URL, marketplace entry, `plugin.json`, hook prefixes, install docs, three tags of history; 0.4.0 is the one cheap moment | keep SpecSeal |
| 2 | Root name | `seal/` · `.seal/` | the items in flight are what people read while a pull request is open, which argues for the visible row beside `docs/`; a dot only if footprint wins | `seal/` |
| 3 | Sub-directory name | `specs/` · `work/` · a metaphor | it must say what it holds to a first-time reader | `specs/` |
| 4 | The `scratch` opt-out | drop it · keep it as a `.git/` marker | a throwaway fixture opts in by creating no `seal/`, so the file has nothing left to do; the tests that use it need the new shape | not in the thread |
