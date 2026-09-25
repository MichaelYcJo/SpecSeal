# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     this work item's spec.md, plan.md and questions.md
· evidence: seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md
· verified: each phase's record under phases/ says what was executed

## Why this work exists

The survivor sweep named the wrong file as a correction, hid a correction
behind text a fold carried verbatim, and reported a removed ledger row's
claim as a correction. After this work it names the correction, holds the
fold's text, and leaves the removed row out.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A fourth condition on the #603 exit | `plan.md` phase 3 names three: a live row, its line gone at `b`, and an anchor resolving at `a` and not at `b`. Q2 measured #589's squash, where a row corrected in place took the exit because the same commit renamed one of its tests | The three, plus: a row that a live row of the same file at `b` still cites by every anchor that resolves there stays measured | `spec.md` judgment 1: a row corrected in place "IS a correction, and dropping it is the silent direction". Its premise, that such a row keeps its anchors, did not hold on #589. The added condition only keeps rows measured. Measured: it names #589's R1 and none of #587's three rows |
| Two #603 cases beyond S7–S13 | The spec names no case for condition (b) or for the left-end half of (c), and a mutation of each stayed green | A duplicate-row case and a never-resolved-anchor case | `skills/agent-contract` and `agents/smith.md`: every unit is mutation-tested, and one that stays green while broken has nothing behind it |
| A fourth #592 case | `spec.md` names S1–S3 for #592. S1's moved file is gone at the tip, so a gone-at-`b`-only rule passes it | A split case where both files remain, added beside S1 | `plan.md` §*Alternatives considered*: gone-at-`b` as the primary rule "falls back to path order: #592 again" on a split. Only a split case can go red for it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |
| Windows and Linux: only macOS was run | the three-OS matrix in `test.yml` at the pull request |

## Not done

The order of entries tied on score in a report follows Python's hash seed,
because `score` iterates a `set` of strings. It was measured on #593's
squash and it predates this work. It changes no place, source or score, and
no issue names it, so it was left as found.

## Fed back into the spec

- *Inferred during implementation* (phase 3, from Q2's measurement): a
  ledger row that a live row of the same file still cites by every anchor
  that resolves at the tip still stands, re-pointed, and is not a removed
  row. `docs/review-chain-spec.md`'s first statement carries it as "a row
  corrected in place is still read", and the module docstring and
  `removed_ledger_rows` state it in full. A planner may overturn it; without
  it, #589's corrected row goes silent.
