# The record layout — where each kind of record lives

This repository keeps a dozen kinds of record, and every one of them has one
home. This document is the index: one table per place, each row naming a file
or a file shape and the one question it answers. A reader looking for a rule
or a record opens this index and then one file.

It is a policy document. A file that states a rule this index gives another
home links to that home and does not restate it, because two copies of one
rule are one rule today and two after the first edit to either. Where a copy
is found, the copy is the defect.

## Every kind of record, at a glance

| Kind | Home | Size target | Index |
|---|---|---|---|
| The evidence ledger | `seal/ledger/<work-item-id>.md` while a work item is open; `seal/releases/<X.Y.Z>.md` once its release folds it; `seal/ledger.md` for the rows from before the fragments. The rules: `docs/the-evidence-ledger.md` | a release file is over target, and its reading unit is one `### <work-item-id>` section | the file name, by version, and the `### <work-item-id>` heading inside it |
| The changelog | `seal/specs/<work-item-id>/changelog.md` while a work item is open; `CHANGELOG.md` once its release gathers it | `CHANGELOG.md` is over target; one release's section is the unit | the `## X.Y.Z` heading. One file per release is decided and not built (F2) |
| A work item's files | `seal/specs/<work-item-id>/` | each file under target | the table under *seal/specs/<work-item-id>/* below |
| The repository's rules | `CLAUDE.md` for the rules a session must hold, `CONTRIBUTING.md` for a contributor's procedure, and the `docs/` document each one links to | each file under target | this document, and the *docs/* table below |
| The configuration | `seal/config.md`, one row per item; `templates/config.md` documents every row | under target | the `Item` column |
| The follow-up list | `seal/follow-up.md`, one row per item that waits on a named party | under target | its rows, each naming who answers it |

## The size a reader takes whole

**A file a reader is meant to take whole stays at or under 1,000 lines and
64 KB.** The line half is the ceiling `seal/config.md`'s `Document line
ceiling` row already sets for `docs/`, and `fold-check` holds it. The byte
half is added because a ledger row is one long line: at 233f0455 the longest
was 8,831 characters, so a ledger file can reach megabytes under any line
cap.

Two kinds are over target today, and each is named here rather than
discovered:

- **A release ledger file.** 37 files at 233f0455, 2.42 MB together, the
  largest 225 KB. They are released, so they never change (see
  `docs/the-evidence-ledger.md`) and are not split. The reading unit is the
  section: all 148 `### <work-item-id>` sections measured then are at most
  58 KB, with a median of 14 KB.
- **`CHANGELOG.md`.** 549 KB at 233f0455, with sections at a median of 12 KB
  and at most 33 KB. F2 below moves it to one file per release.

No index file is added inside `seal/releases/`. The file name is the index
by version and the `### <work-item-id>` heading is the index inside a file;
a separate index would be one more file every release edits.

## A change writes fragments, never a shared file

Two files used to take an append from every branch, and both cost a conflict
at the worst moment — after the broad gate has run, which forces it to run
again. So a change writes a file of its own, named for its work item:

| Instead of | Write |
|---|---|
| an entry under `CHANGELOG.md`'s `## Unreleased` | `seal/specs/<work-item-id>/changelog.md` |
| rows appended to `seal/ledger.md` or a `seal/releases/<X.Y.Z>.md` | `seal/ledger/<work-item-id>.md` |
| a re-read or a correction of a row in `seal/ledger.md` or a `seal/releases/<X.Y.Z>.md` | a `Re-read ·` or `Corrected ·` row in `seal/ledger/<work-item-id>.md`, citing the row |

No two work items share an id, so no two branches share a file. A ledger
fragment needs no header of its own: every row carries its own anchor and
hash. A changelog fragment has no line starting `## `, because that line
ends the released section, and the gather refuses a fragment that has one. What a citing row is, and how the checker reads it, is
`docs/the-evidence-ledger.md` §*A released row is read again in the branch's
fragment*.

**Both kinds of fragment are gathered at the release, by two commands in one
commit**, and `docs/release-checklist.md` §*2. Gather, fold, bump* holds the
commands. The changelog fragments are concatenated into the released section
of `CHANGELOG.md`. The ledger fragments move into that release's own file,
`seal/releases/X.Y.Z.md`, and the fragments are removed. A fragment lives
from the work item's first row to the release that ships it.

A `settle` fold has no work item, so its fragment is named for the moment:
`seal/ledger/<unix-seconds>-fold.md` (`skills/settle/SKILL.md` §*What a fold
branch owes*). The release folds it like any other.

## docs/

The standing policy. A `docs/` document outranks the work items' specs, and
a work item that finds one wrong corrects it.

| File | The question it answers |
|---|---|
| `docs/branch-and-release.md` | where a branch is cut from, how it merges back, and what carries the version |
| `docs/commit-review-gate-spec.md` | how the gates are registered, what the PreToolUse reading of a commit decides where git cannot, and what the review-history guard and the implementer mark say |
| `docs/issues-and-milestones.md` | what the issue tracker's fields mean here, and which of them anything reads |
| `docs/measuring-a-run.md` | what a segment of a run measures, and where the reading goes |
| `docs/one-root-by-lifetime.md` and its `.ko.md` edition | the design 0.4.0 started from: one root, laid out by lifetime |
| `docs/release-checklist.md` | what to type on the day of a release, in order |
| `docs/review-chain-spec.md` | the cycle contract of the review skills, and the review run's bound and end |
| `docs/review-handoff-protocol.md` | the file convention for handing review work between sessions |
| `docs/round-record-spec.md` | the rows of a round record as the pull-request check reads them |
| `docs/the-agent-set.md` | how the rules are split between the agents a work item spawns |
| `docs/the-broad-gate.md` | who takes the one broad run, what it runs, and what it may say |
| `docs/the-commit-gate-inside-git.md` | what git decides inside a commit, what its hooks cannot see, and which reading judges each state of a repository |
| `docs/the-evidence-ledger.md` | what a ledger row is, how a coordinate names code, how a released row is read again, and what a merge can drop |
| `docs/the-record-layout.md` | this index: where each kind of record lives, and which file a change writes |
| `docs/the-review-and-parity-arms.md` | what each opt-in arm of the commit gate wants, and the routing declaration that moves the review arm's check to the pull request |
| `docs/worktree-guard-spec.md` | what the worktree guard refuses, and why |

`docs/experiments/` holds dated scratch documents and is no policy; a fold
never writes there.

## seal/

What the plugin maintains, read and written by machines. Every `seal/…` path
means `<repo>/seal/` where that directory exists, and the root under the git
common directory otherwise.

| File | The question it answers |
|---|---|
| `seal/README.md` | the export rules, for a session that never loads a skill |
| `seal/config.md` | what this repository says about itself, one row per item |
| `seal/follow-up.md` | which items wait on a named party, and who |
| `seal/ledger.md` | the rows from before the fragments existed, and the notation. Released: it never changes |
| `seal/ledger/<work-item-id>.md` | one open work item's ledger rows, re-reads and corrections, until its release folds them |
| `seal/ledger/<unix-seconds>-fold.md` | a `settle` fold's readings and corrections, until the release folds them |
| `seal/releases/<X.Y.Z>.md` | the rows one release gathered, one `### <work-item-id>` section each. Released once tagged: it never changes |
| `seal/specs/<work-item-id>/` | one work item's records, the table below |

## seal/specs/<work-item-id>/

One work item's records, from its first commit to the `settle` fold that
retires the directory. Which file each agent writes is
`skills/implement/SKILL.md` §3's table; this one says what each file answers.

| File | The question it answers |
|---|---|
| `routing.md` | who frames, builds and reviews this work, and where it ends — answered before the first edit |
| `spec.md` | what is built, its scenarios, and the decisions with their grounds |
| `plan.md` | in which phases it is built, how each is shown, and the approval line |
| `questions.md` | which decisions only a person could make, and how each was answered |
| `overview.md` | what the diff cannot show: purpose, divergences, what was not verified |
| `phases/phase-N.md` | what one build phase was asked, found and removed |
| `rounds/round-N.md` | what one review round read, found and closed |
| `changelog.md` | this work item's entry in the next release's notes |
| `survivors.md` | which standing copies of a removed sentence are deliberate, with the quote that anchors each |
| `tests-todo.md`, `evidence-todo.md` | which cases and which verified facts a review left for the implementer |
| `broad-gate.md` | the sealer's one broad run, where the work went straight to the pull request |

The files keep these paths and stop mattering at two different times (F3).
`routing.md` and the SDD set (`spec.md`, `plan.md`, `questions.md`,
`overview.md`, `changelog.md`) stay until the `settle` fold retires the
directory. The process record (`rounds/`, `phases/`, `survivors.md`, the two
todo files, `broad-gate.md`, and a `handoff.md` or `pr.*.md` where one was
written) is read by nothing after the release that ships the work item, and
`settle --retire-process` removes it at the next release, fold or no fold.

## The root records

| File | The question it answers |
|---|---|
| `CLAUDE.md` | the rules a session in this repository must hold, each linking to its home |
| `CONTRIBUTING.md` | how a contribution is made and checked, and what a change to a gate must carry |
| `CHANGELOG.md` | what each release changed, one `## X.Y.Z` section each |
| `README.md` and `README.ko.md` | what the plugin is and how to install it |

## What is decided and not built yet

Four parts of this layout were decided here, each to be built by its own
issue. F1 is built; the other three are not yet. Each says when, by the
release it lands in relative to #716's; the issue's milestone names the
version, so no number here goes stale when it ships.

**F1 — `docs/commit-review-gate-spec.md` is cut in three (#727, in the
release #716 ships in, after #716 lands). Built by #727.** The table below
records the cut as it was decided, with the lines it read at 233f0455.
#716 changes that document's reading of the commit gate
in the same release, and a split landing first would conflict with it at its
squash. The cut follows the document's own headings, as #526 cut
`docs/review-chain-spec.md`:

| File | Takes | Lines at 233f0455 |
|---|---|---|
| `docs/the-commit-gate-inside-git.md` | §*The commit gate inside git*, with *Known limits* and *Where each state of a repository stands* | 41–277 |
| `docs/the-review-and-parity-arms.md` | §*Review arm*, *Where the marker goes*, *The declaration, and where the check went instead*, §*Parity arm* | 760–994 |
| `docs/commit-review-gate-spec.md` | *Registration*, §*commit-review-gate (PreToolUse, Bash)* through *Why a deny*, review-history-guard, implementer-mark, and an index naming the other two | 1–40, 278–759, 995–1047 |

Each part answers one question — what git decides, what the text reading
decides, what each arm wants. Built, the parent is 586 lines, the commit gate
inside git 254 and the arms 250, each under the ceiling of 1,000. Fold markers
went across whole, and the `Over the ceiling` entry went with the cut in the
same change. The row stays and reads `none`, which says the listing is empty.
The ceiling itself is the `Document line ceiling` row, which `fold-check`
holds every unlisted document to (`docs/the-evidence-ledger.md` §*The fold,
and what tells it from a deletion*).

**F2 — `CHANGELOG.md` becomes one file per release (#728, in the release
after that one).** The
target is `changelog/<X.Y.Z>.md`, with all existing sections migrated and
`CHANGELOG.md` kept as a short index linking each one; the GitHub Release
reads the release's own file. Migrated rather than frozen, because no branch
writes the changelog in parallel, and a link at an old tag keeps resolving at
that tag.

**F3 — a work item's directory is laid out by lifetime (#729, in the release
after #716's). Built by #729.**
The principle: what outlives the merge stays, or folds into `docs/` and the
ledger; what a review run needs only while it runs leaves the tree, or
becomes one file per run. #729's frame read the readers and chose the first.

- **The paths do not change.** Ten readers and the test suite name them, and
  a regrouping under one subdirectory would show a reader nothing a listing
  of `rounds/` and `phases/` does not.
- **One file per run is rejected.** The round records of 41 of 53 runs
  measured would together exceed the 64 KB a reader takes whole.
- **The process record leaves after the release, without waiting for the
  fold.** Once its release has merged to `main`, nothing reads it: the
  release pull request and the release seal were its last readers. So
  `settle --retire-process` removes it from every released work item as the
  first act of `docs/release-checklist.md` §*2b*, on every release, and
  leaves `routing.md` and the SDD set for the fold. Its guards are
  `--retire`'s: an open todo row or an anchored ledger row keeps the item.
- **Released items are not exempt.** The ledger freeze rests on content
  anchors and parallel re-stamps, and no ledger row anchors inside a work
  item's directory. The first run, over every item released before it, is
  its own pull request at a release's step 2b.

**F4 — the other rules `CLAUDE.md` restates get one home each (#730, in the
release after #716's).** The merge-direction table, *no real identifiers*, the commit
cadence, and every restated rule outside `CLAUDE.md` and `CONTRIBUTING.md`.
#715 moved the ledger and fragment rules alone, because it rewrote them; the
rest change no meaning, and finding a restated rule repository-wide needs a
method of its own.
