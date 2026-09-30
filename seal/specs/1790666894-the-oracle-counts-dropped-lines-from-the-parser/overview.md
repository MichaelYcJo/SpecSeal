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
| The Python the S4 set is measured on | spec S4: "On Python 3.14 that is U+001F, U+00A0, …"; the virtualenv `bin/test` builds runs Python 3.13.9 | the case computes the set on whichever Python runs it, as the spec asks; phase 2 records 3.13's set, the same 17 characters as the spec's 3.14 list, and 3.12 and 3.14 give 17 too | spec S4: "Computing the set is what keeps a new Unicode version from leaving a character out" |
| Which of H's P1-1 anchors is re-stamped | spec §*The ledger*: "Its `_inline_html_lines` and `test_the_oracle_names_each_kind_it_hides` anchors are re-stamped"; `--reverify` moved only `_inline_html_lines` | only the anchor that moved | the case's rows stay where they were (spec §*Scope*, Out), so its hash did not change |
| A third new case, the guard over S4's set | spec §*Scope*, In: "one new parametrized case holding the class's rows (S1 to S3), one case over every character the strip drops (S4), and one `FOUND` document (S5)"; the code adds `test_the_strips_set_is_the_one_measured` beside them | the guard stays | pytest skips a parametrized case whose list is empty rather than failing it (executed in phase 2: exit 0, 1 skipped), so a set condition that empties the list, or yields only a space and a tab, would leave S4 silent. The guard pins five characters the set must hold and excludes the two CommonMark reads as indentation; it is red alone with the set emptied and with a space and a tab in place of the set (`phases/phase-2.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck after this branch | the sealer, spawned by the orchestrator once the review rounds settle |
| ✅ The S4 case on a Python other than the 3.13.9 `bin/test` built: CI's matrix runs 3.12 (`.github/workflows/test.yml`), and the spec measured its set on 3.14 | executed in phase 2 at `128dda72`: 17 passed on 3.12.12 and 3.14.4 (the first spawn), and 18 passed, the 17 and the guard, on 3.12.11 and 3.14.3 (the second), each through `uv run --isolated` with `markdown-it-py==4.2.0` |
| ✅ The `Ran by` row of each phase record | the orchestrator named `specseal:smith on claude-opus-5-5` in phase 2's second spawn prompt, and both phase records carry it as given |

## Not done

Nothing yet.

## Fed back into the spec

None.
