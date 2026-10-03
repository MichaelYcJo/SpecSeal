# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     filled at the close
· evidence: filled at the close
· verified: filled at the close

## Why this work exists

A signatory that changes code a pact clause binds now leaves a record of it,
and `pact-check` at the pact's repository reports that record until a pact
review there takes it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A row of another width than the header | `spec.md` item 1: the walker "reads what cmark-gfm reads and refuses, with the true cause, only what it cannot read". cmark-gfm pads a short row with empty cells and drops a long row's extra ones; the walker refuses both | refused | A padded cell is a value nobody wrote, and a dropped one is a value somebody wrote and nobody reads. #735's walk already refused a long row in the `Signatory` table (`TABLE_ENDS`' *too many cells*), and its sentence is pinned; a short row in a four-column record is the same silence one cell over. Refusing keeps S1's property, which allows a refusal on any shape |
| A table GFM does not render, under a block that absorbs its header | spec silent; the corpus's *before the header* position found the walk at `2b1dcb1f` reading a table under `- a note` that cmark-gfm renders as part of the list item (656 of the 5,454 `Signatory` shapes wrong at the base; most of them this position) | refused, saying which line absorbed it | S1: "No shape yields cells cmark-gfm does not" |
| A tab before a row | `plan.md` §*Technical context*: each kind is tried "with a tab where the kind permits"; round 3 of #735 (⬜ 22) said GFM reads "a leading tab, on a row" | cmark-gfm ends the table at a tab-indented row (an indented code block), so the walker ends it there and refuses the row as unread | measured with `cmarkgfm` 2025.10.22 (`questions.md` Q13); round 3's sentence does not reproduce at this version |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once the review rounds settle |
| `cmarkgfm==2025.10.22` installing from a wheel on CI's Windows and Linux legs | the first push's three-platform CI run |

## Not done

Filled at the close.

## Fed back into the spec

none
