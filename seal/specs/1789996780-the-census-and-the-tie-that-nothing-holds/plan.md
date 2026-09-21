# Implementation Plan: the census and the tie that nothing holds

<!-- seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/plan.md —
HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

Three tickets, four phases, and the order is load-bearing. The tie case
(#471) touches nothing else and goes first. The census case (#469) is built
next, because the instrument it establishes is what phase 4's figures are
taken with. The corrections (#470) come third, and they include a correction
to `seal/ledger.md` row C1 — which adds a marker to the very file the figures
are counted over. So the figures are written **last**, measured at the branch
tip after that edit.

Writing them earlier is precisely the failure #470 reports: a census
invalidated by a commit inside the range that wrote it.

## Technical context

- `skills/evidence-check/scripts/correction_check.py:175-176` — `LEDGER =
  "seal/ledger.md"` and `FRAGMENTS = "seal/ledger"`, the two addresses the
  check watches. The census case reads the corpus through these, never a
  hard-coded list, because the glob is exactly what goes empty at a release.
- `correction_check.py`'s census note — the comment block opening *The two
  verbs, and the date shape* and ending at the `VERBS` assignment (lines 183 to
  231 at this SHA), the comment #470 finding 1 is about. Its figures are over *the three
  ledger files*, a corpus that no longer exists.
- `correction_check.py#examine` — the comment opening *The parent named is the
  one that lost the most occurrences of it*, and the `max(by_parent.items(),
  key=lambda kv: len(kv[1]))` that acts on it, whose tie behaviour is *the first key in insertion
  order*, i.e. the first parent. That is what A8 pins.
- `tests/test_a_merge_cannot_silently_drop_a_correction.py` — 48 cases, none
  of which opens a real ledger file. `test_the_longest_qualifier_the_tree_
  carries_is_seen` states a tree fact in its docstring and asserts it
  synthetically, so A7 is the module's first case that reads the tree.
- `a8bf2a86`, the 0.12.2 release: `seal/ledger.md` +44 rows, all three
  `seal/ledger/*.md` fragments deleted. Row C1 stands in `seal/ledger.md` and did not exist in
  that file before this commit.
- `git show fix/the-gate-states-what-its-own-fixes-disproved:seal/specs/
  1789996775-…/spec.md` §*The correction marker* — the marker A5 adopts, and
  its reasoning for the uppercase verb.

**What breaks in six months.** The census note's digits go stale again, the
next time a release folds fragments in or a branch corrects a row. That is
accepted and it is why the note carries the date and names both movements:
the digits are a snapshot and the **case** is what holds the property. If the
case is ever weakened into asserting a count, the design is gone and the
third circular census is one commit away.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Keep stating the figures over the three ledger files, corrected to 412/413 | The corpus does not exist: `a8bf2a86` deleted all three fragments. The corrected number would be false on the day it was written, for a fourth reason | Rejected |
| State the figures over `seal/ledger.md` because *a branch cannot move it*, as #470 prescribes | False twice over. A release moved it by folding 44 rows in, and this branch moves it by correcting C1. Shipping that sentence would hand the next reader a guarantee the same commit breaks | Corpus kept, **grounds replaced**: it is chosen as what a release folds fragments INTO and what survives one, and the note says it moves |
| Drop the numbers and state the property alone | #469 and #470 both say *not this*, and the bound's justification is a census. A bound with no stated census is how the first two went wrong | Rejected |
| Leave the figures spread over the module docstring and the census comment, correcting each | That is the six-site shape the defect already has. Correcting six copies leaves six copies to drift | Rejected — **one census site**, everything else points at it |
| Have the census case assert a NUMBER over the corpus | Identical in kind to the comment: a number over a corpus that moves is stale the next time anybody records a correction, and the case would go red for a legitimate edit | Rejected — the case asserts the **property** (judgment 2) |
| Have the census case walk a hard-coded list of ledger paths | It goes blind exactly when the fragments are folded away — which has already happened once, at 0.12.2 | Rejected — read `LEDGER` and `FRAGMENTS` from the module |
| Have the case warn, or skip, when the corpus grows a longer run | A green that means nothing, which is the hole #469 exists to close | Rejected — **red, naming the file, the row, the run length and the spelling**, so the bound is raised deliberately with the case re-driven |
| Correct the six sites round 3 listed | The class moved under the list: the ledger fragment was folded into `seal/ledger.md` and the changelog fragment was gathered into `CHANGELOG.md` §0.12.2. Fixing the list ships the class one site short, for the fourth time in this lineage | Rejected — enumerate by construction (§12) |
| One marker convention for records and ledger rows alike | A hand-grep for the ledger's `Corrected <date>` would return SDD records, and that grep is the only way the #424 incident was ever caught | Rejected — uppercase `CORRECTED` in records, sentence case in the ledger, per work item 1789996775 |
| Write the census figures in phase 2 or 3, beside the code they describe | The C1 correction in phase 3 changes the count. The figure would be true in the clone and false when it landed — #470's finding 9, verbatim | Rejected — figures are phase 4, measured at the tip |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The tie (#471).** `test_a_tie_falls_to_the_first_parent` planted from round 3's paste-ready text, beside `test_the_parent_named_is_the_one_that_lost_the_most` | Green on shipped code; **red** with the parent walk reversed, the mutation that leaves 48 of 48 green today. Both runs recorded (§15) | ecca19b9 |
| 2 | **The census case (#469).** An unbounded walk over the corpus read through `LEDGER` and `FRAGMENTS`, asserting every candidate site is one `MARKER` sees; no count asserted; empty corpus refused; failure message names file, row, run length and spelling; docstring states how its number was taken and why the instrument is not `MARKER` | Green as shipped. Red with the bound narrowed to four. **Green** with the bound narrowed to four AND the census taken with `MARKER` — the circularity demonstrated, which is the pair that proves the instrument load-bearing (A7) | a0606e94 |
| 3 | **The corrections (#470).** The class enumerated by construction over the tracked tree; every present-state site corrected; `seal/ledger.md` C1 corrected with a sentence-case marker; SDD records corrected under `<!-- CORRECTED … -->`; positional coordinates replaced by content ones (A9); `CHANGELOG.md` §0.12.2 left under Q1's default with the divergence disclosed | A grep for the figure returns only corrected sentences and past-state records. `correction-check --range origin/release/v0.12.3...HEAD` and `bin/evidence-check` both read directly (`cmd >/dev/null 2>&1; echo $?`). Q5: `survivor-check` answered with grounds, never a reword chosen to quiet it | 02ec71ee |
| 4 | **The census note (#470 finding 1).** One site, rewritten: corpus, instrument, moment, and the conclusion the figures support. Figures **measured at the tip, after phase 3's ledger edit**, with phase 2's instrument. Then the ledger fragment's new rows and the anchor question | The note's digits reproduce from the walk it describes, re-run at the tip. Rows citing a drifted coordinate read by hand, then `evidence-check --reverify`, then `bin/evidence-check` exit 0 (A10) | 57c31e70 |

## Operational impact

No migration, no environment variable, no dependency, no compatibility break.
`correction-check`'s exit codes and printed lines are unchanged: this work
adds two cases and corrects prose.

Two things a deployer and the next release must not miss:

- **`seal/ledger.md` is touched by this branch**, which the fragment rule
  permits only for the reason stated — row C1's claim is false and leaving the
  ledger true means correcting it there. A sibling branch,
  `fix/the-gate-states-what-its-own-fixes-disproved`, corrects rows of the
  same file in the same release. That is the exact configuration #424 was
  about: resolve the conflict **hunk by hunk, reading both sides**, never
  `--ours` and never `--theirs`, and let `correction-check` read the range at
  the pull request.
- **The census note's digits are a snapshot with a date on them.** The next
  release that folds fragments into `seal/ledger.md` makes them stale by
  construction. Nothing is wrong when that happens; the case is what holds the
  property, and the note says so.

Approved 2026-09-22 by the repository owner, when `smith` was spawned.
The `automation` preset was pressed once for the whole 0.12.3 run, and the
spawn carried this plan as the build's contract (`routing.md`).
