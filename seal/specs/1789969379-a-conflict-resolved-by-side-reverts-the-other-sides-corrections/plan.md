# Implementation Plan: a conflict resolved by taking a side reverts the other side's corrections (#424)

<!-- seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-21 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

A new check reads every merge commit in a range and reports a correction
marker that one parent's ledger text carried, the merge result does not, and
whose row still stands. It watches `seal/ledger.md` and every
`seal/ledger/*.md` fragment, matches on the leading verb and date rather than
on the sentence, and stays silent where the whole row went — which is
`REMOVED` and correct. One CI leg runs it on pull requests into `release/*`.
The two documents that state the fragment rule's exception gain the sentence
about resolving per hunk.

It does not prevent the loss. Reading both sides of a hunk is a person's act
and stays one; what this buys is that losing a correction stops being silent.

## Technical context

**Why the conflict is routine rather than exceptional.** `CLAUDE.md`'s
fragment rule exists because two branches appending to one file cost a
conflict at the worst moment, and it has one exception: a branch that removes
or falsifies what an existing `seal/ledger.md` row claims must touch that file
to leave the ledger true. So corrections to the shared file are the design.
The work item merged immediately before this one, `1789956662`, re-read and
widened four of its rows.

**What the markers are, counted rather than recalled.** `Corrected <date>`
appears 10 times, all in `seal/ledger.md`, in at least three spellings.
`Re-read <date>` appears 185 times there and 4 in the one live fragment. Both
are prose conventions; nothing reads either today.

**CORRECTED at round 1, finding 1.** Those are ROW counts, and the three
spellings all vary after the date. `seal/ledger.md` carried 404 marker
occurrences when round 1 measured it — 401 of them on the 190 rows that
carried one, and 3 in the file's prose — and 39 of them put a qualifier
between the verb and the date in ten spellings. This paragraph's numbers were
the ones the build was written against, and they hid the axis the check turned
out to be blind on.

<!-- CORRECTED 2026-09-22 by work item 1789996780 (#470). What stood here:
"The file carries 404 marker occurrences on 190 rows". It is false because
404 is the file's total and only 401 of them stand on the 190 rows; the other
3 are in prose, which correction_check.py puts out of scope by construction,
so a reader taking the sentence at face value believes the survival test
watches three markers it cannot see. The corpus and the moment are named now
as well, because a8bf2a86 folded three ledger fragments into that file and
this branch wrote a marker into it. Corrected in place with the issue named,
never deleted silently: a record of a past state that quietly becomes true is
a record nobody can audit. -->


**What is NOT available to build on.** `grep -n "Checked"
skills/evidence-check/scripts/evidence_check.py` returns two lines, `1577` and
`1587`, both inside the `# RIDER:` at `reverify()`. The `Checked` column is
written by people and read by no code, so the ticket's second direction is new
mechanism rather than one more column — and it collides with an open question
the rider already owns. `questions.md` Q1 keeps it out.

**The nearest sibling, and why it is the model.** `survivor_check.py` answers
the same *here is what you lost and where it still stands* question over a
range, reports one entry per place with the standing text quoted, and exits 1
while one is unanswered. W1 follows its shape rather than inventing one.

**Constraints the build has to respect.**

- **A row is content, never a position.** No line numbers anywhere, and the
  check must keep working after `fold_ledger.py` moves a fragment into the
  shared file.
- **A feature branch squashes**, so the merge commits this reads exist only
  before that. The leg runs at the pull request or nowhere — M2 measures it.
- **`seal/ledger.md` runs to thousands of lines and about a megabyte**, with
  single rows running to thousands of characters. Anything that reads it whole per merge commit per
  file will be slow; read blobs with `git show` and compare marker sets rather
  than diffing text.
  <!-- CORRECTED 2026-09-22 by work item 1789996780 (#470). What stood here:
  "`seal/ledger.md` is 2364 lines and 1.07 MB". The file is 2408 lines and
  1.11 MB at the tip of the branch for #469, #470 and #471, and it grows at
  every release, so a measured size stated in the present tense with no
  moment is stale the moment it ships. The sentence's point is that the file
  is big enough that reading it whole per merge commit per file is slow, and
  that survives a release where the digits do not. Corrected in place with
  the issue named, never deleted silently: a record of a past state that
  quietly becomes true is a record nobody can audit. -->
- **`agent-contract` §8**: a probe that needs a repository drives git from
  Python, and a fixture here needs real merge commits with real conflicts.

**The failure scenario of the chosen approach, at six months.** Somebody
corrects a row and writes neither word, and the check watches nothing. The
mitigation is that the counts are written down in `spec.md` — 10 and 189 — so
a later reader can see what the check's reach actually was rather than
assuming it covered corrections as a class. The alternative that closes it is
a structured column, which is the ledger format changing, and that is a
different work item.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A marker present in either parent, absent in the result, whose row survives** | A correction carrying no marker is invisible; a marker legitimately reworded down to its date is not, but a marker whose verb changes is | **chosen.** It is the only candidate that separates a loss from a `REMOVED` row by construction, and row survival is `CLAUDE.md`'s own rule rather than a new judgment |
| Count the markers in the file and fail when the count falls | Fires on every legitimate row removal, which the repository's own rule requires. A check that refuses correct work is one people learn to skip | rejected. This is #424's first direction taken literally, and the row-survival test is what repairs it |
| `Checked` going backwards across a merge | Nothing reads the column, so this is new mechanism on a surface a standing `# RIDER:` already owns, and it would answer that rider's question as a side effect of a different work item | rejected as this work's mechanism; `questions.md` Q1 is where the owner can move it |
| The document sentence alone | It reaches the person at the moment of the act, which no check does — and it is a sentence nobody reads at the moment they are resolving a conflict. #386 is the same shape, open, and its subject is a step no document names being skipped three times running | rejected as the whole answer, **kept as part of it**: it is §Scope 5 |
| A merge driver for `seal/ledger.md` | It would have to understand what a row claims | rejected by the ticket |
| Forbid corrections to the shared file | Leaves the ledger stating what the tree contradicts | rejected by the ticket |
| Match markers on the whole sentence | Three spellings exist today; the fourth is somebody rewording one | rejected. Verb and date, nothing after |
| Watch `seal/ledger.md` only | `fold_ledger.py` moves fragments in at the release, so the check would go blind exactly when the rows become shared | rejected |
| Run it as a hook at merge time | An unattended merge has no hook, the resolution happens in whatever tool the person used, and a hook cannot see the pull request's range | rejected. The leg runs where the squash has not happened yet |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The marker reader: verb-and-date matching over ledger text, and the row-survival test. Plus M1's measurement over this repository's own merge history, recorded | A7 and the row-survival half, each red against the reader's absence. M1's count written into `overview.md` whatever it says | cba1b536 |
| 2 | The check proper: merge commits in a range, both parents, both markers, every lost marker named | A1, A2, A3, A6, each red first. A fixture builder that makes two branches, a real conflict and a taken side | 8311d7a2 |
| 3 | Fragments, and the empty case | A4 and A5. A5 asserts the cheap path says it looked at no merges, so the common case cannot silently pass by doing nothing | 99948792 |
| 4 | The wrapper in `bin/` and the CI leg, plus M2's measurement that the merges are reachable where the leg runs | A9, and M2 recorded. If M2 comes back negative the leg moves and `overview.md` carries the divergence | e5776914 |
| 5 | The documents: `CLAUDE.md`, `CONTRIBUTING.md`, `skills/evidence-check/SKILL.md`, the changelog fragment and the `seal/ledger/` fragment | A8, red when either document stops saying it. The ledger fragment's anchors resolve under `evidence-check --strict` | 7d404216 |

Phase 1 delivers no check, deliberately: the reader is the part with the most
cases and the least risk, and separating it is what lets phase 2's cases be
about merges rather than about matching.

## Operational impact

- **Failure direction: the check refuses more, and A3 is what bounds it.** A
  lost correction is silent today, so anything is stricter than nothing; the
  risk is a false refusal, which is exactly what the row-survival test exists
  to prevent and what A3 pins.
- **Prompt budget: zero.** No question is added to any session. The check
  prints and the CI leg goes red; nobody is asked anything.
- **One new CI leg on pull requests into `release/*`.** Q2 decides whether it
  blocks; the default is that it does, like every other arm of that workflow.
- **No new dependency, no new env var, no migration.** Git and the standard
  library.
- **Platform honesty.** `git show`, `git log --merges` and `git rev-list` are
  git behaviour rather than OS behaviour; the fixtures run on every matrix
  leg. Not run on Windows or Linux from this machine — CI is the answerer.
- **A repository with no `seal/ledger.md` and no fragments is unaffected**: A5
  is the case, and the check exits 0 having looked at nothing.
