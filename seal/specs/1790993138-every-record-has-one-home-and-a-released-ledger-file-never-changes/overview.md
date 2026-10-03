# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show, each part written when it happened. -->

📋 implement applied
· spec:     spec.md D1–D8, S1–S15 and §*The classes, enumerated*; plan.md's phases; questions.md Q1–Q6, M1–M3, W1–W3
· evidence: seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md
· verified: each phase record carries its runs, labelled executed or read

## Why this work exists

A re-read of a released ledger row used to edit the released file in place, so two branches re-reading one row conflicted at their squash; from this work on, the re-read is a citing row in the branch's own fragment, a released file never changes, and every kind of record has one home that the rest link to.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The literal a citation carries (W1) | D2: "The literal is a prefix of the row's first cell, long enough to be unique in its section." / `citation_for` takes the shortest unique word-prefix of the first run of the cell free of `\`, `"` and a backtick; where every prefix is on another line too, the cell's last run with its closing pipe; and the heading tried nearest first, then the enclosing path, then each enclosing heading outward | the code | M2, phase 1: a plain prefix left 68 of 1,083 coordinate-bearing released rows with no citation, every one a cell opening with a code span. Cutting at the quoting characters left 22, all under a heading holding a backtick, which cannot sit inside the citation's code span. With both rules, 0 of 1,083 fail. The closing-pipe fallback was found by the phase-1 case for a row whose whole first cell starts a longer row's. D2's semantics (a content coordinate naming one row) are unchanged |

## Not verified

| Item | Who must answer |
|---|---|
| Whether the family union's failure direction (a coordinate whose content returns to a hash an earlier reading recorded reads OK again, spec D3) is acceptable in practice | the warden, reading D3 against the cases; the repository owner if it is contested |

## Not done

Nothing yet.

## Fed back into the spec

None yet.
