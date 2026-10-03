# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     this work item's spec.md (items 1-13, S1-S18, Data & interfaces), plan.md (phases 1-5, Technical context, the first wave's rules), questions.md (Q1-Q17); docs/the-pact.md; docs/the-evidence-ledger.md (the freeze, the citing rows); CLAUDE.md §the fragment rule, §no real identifiers, §whose; seal/config.md; #735's round-3 report; templates/sdd-phase.md, templates/sdd-overview.md, templates/pact.md
· evidence: seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md W1, W2, G1, G2, C1, D1, D2 added, and 32 Re-read rows for released rows; #735's P8 corrected in place and P3, P6, P9, P10, P11 re-stamped with notes; #736's L4 and seven citing rows and #718's R3 and W3 re-stamped with notes
· verified: executed — every new case seen red (against 2b1dcb1f, or with its arm broken through mutation-check), 87 distinct mutation breaks each red at the end (38, 13, 15, 17 and 4 by phase), each phase's modules naming its files green, the three hygiene modules, ruff on every touched Python file, evidence-check --strict and correction-check exit 0, fold-check exit 0, survivor-check over 2b1dcb1f...HEAD exit 0 with five places exempted; unverified — the full suite, the repository-wide lint and the typecheck (the sealer's)

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

- **The container nesting the walker cannot see.** A header taken lazily into
  a list item two blocks up (`- x`, a blank line, an indented paragraph, the
  header) is read as a table GitHub does not render. Telling it apart needs
  the container nesting no table reader here tracks; `gfm_table`'s docstring
  and the corpus module's docstring name it, and nothing in a pact, a record
  of pact changes or a record of pact reviews writes that shape.
- **A record a person edits by hand.** The record of pact changes is written
  by `--reverify` alone and said never to be edited by hand; a hand edit
  changes its content hash, which `pact-check` then reports as a record grown
  after its review. That is the loud direction, and nothing refuses the edit
  itself.
- **The two-repository end to end.** S7–S17 run the writer and the reader in
  temporary repositories side by side, the writer's output feeding the reader
  (`tests/test_a_pact_review_takes_a_pact_change.py#record`); nothing was run
  across two real checkouts on two machines, which is the local-mode limit
  `docs/the-pact.md` names.

## Fed back into the spec

none
