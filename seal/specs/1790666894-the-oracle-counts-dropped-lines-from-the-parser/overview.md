# 1790666894-the-oracle-counts-dropped-lines-from-the-parser — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. Each part is written when it happens. -->

## Why this work exists

The suite's CommonMark oracle stops reading container markers by hand, so a
paragraph whose top line the parser's strip drops no longer makes the
property report a false disagreement with the hooks' walk (#677, #673 round
3's 🟡 1).

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The Python the S4 set is measured on | spec S4: "On Python 3.14 that is U+001F, U+00A0, …"; the virtualenv `bin/test` builds runs Python 3.13.9 | the case computes the set on whichever Python runs it, as the spec asks; phase 2 records 3.13's set | spec S4: "Computing the set is what keeps a new Unicode version from leaving a character out" |
| Which of H's P1-1 anchors is re-stamped | spec §*The ledger*: "Its `_inline_html_lines` and `test_the_oracle_names_each_kind_it_hides` anchors are re-stamped"; `--reverify` moved only `_inline_html_lines` | only the anchor that moved | the case's rows stay where they were (spec §*Scope*, Out), so its hash did not change |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck after this branch | the sealer, spawned by the orchestrator once the review rounds settle |
| The S4 case on a Python other than the 3.13.9 `bin/test` built: CI's matrix runs 3.12 (`.github/workflows/test.yml`), and the spec measured its set on 3.14 | phase 2 of this build, by running the S4 case under 3.12 and 3.14 |
| The `Ran by` row of each phase record | the orchestrator, which chose the model at the spawn |

## Not done

Nothing yet.

## Fed back into the spec

None.
