# 1788302682-the-release-check-never-watched-bin — review round 2

| Field | Value |
|---|---|
| Target SHA | 1c8bee4 — the fix diff `81d1022..1c8bee4`, one file, not the branch |
| PR | none yet |
| Broad gate | not yet — it follows this record |
| Fixes checked by | no fixes to check |
| Contract changes | none — the round opened nothing, so no fixes were written for it |
| New units | none |
| Needs a fix | no |

- [x] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 1's 🟡 2 — the document pin checked one direction | `tests/test_the_release_check_watches_what_ships.py:151-152` | answered — closed by 1c8bee4, which predates this round; this round reproduced the closure | `:151` collects every `` `x/` `` token of the paragraph and `:152` asserts the set equals `SHIPS`. Reviewer's mutation: a seventh `` `commands/` `` token in `docs/branch-and-release.md:36` reddened this test alone (1 failed · 28 passed), the message naming both sets. Orchestrator read the diff line by line and it matches the snippet round 1 supplied |
| 🟢 2 | Round 1's 🟡 3 — a renamed step failed with a bare `IndexError` | `tests/test_the_release_check_watches_what_ships.py:80-82` | answered — closed by 1c8bee4, which predates this round; this round reproduced the closure | `:81` asserts the step name is present, with a message, before the split. Reviewer's mutation: renaming the step at `hygiene.yml:24` failed the 26 cases that call `ships_pattern` at `:81` with the message, and no `IndexError` |
| 🟢 3 | The fix diff creates no unit and changes no contract | `git diff 81d1022..1c8bee4` | pass | `ships_pattern()` still returns a compiled regex and its four call sites (`:100`, `:111`, `:121`, `:122`) are untouched; `text` and `named` are locals. The only assertion whose direction changed is `:152`, which is the fix itself |

## Executed probes

| What was run | Result |
|---|---|
| pytest (3.12) `tests/test_the_release_check_watches_what_ships.py` at 1c8bee4 | 29 passed, 0 skipped |
| mutation A: `` `commands/` `` added to the doc paragraph | 1 failed · 28 passed — the doc pin only |
| mutation B: step renamed to `…must bump the version` | 26 failed · 3 passed, all at `:81` with the message; restored |
| `evidence_check.py --strict .` | 71 ok · 0 drifted · 0 broken — the two anchored units are outside this diff, so no `--reverify` |
| `git diff --quiet` after both mutations | exit 0 |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_release_check_watches_what_ships.py:147` (now `:151-152`) | the doc pin's assertion — the one line the fix diff changed in meaning |
| round-1 | `tests/test_the_release_check_watches_what_ships.py:80` | the split that had no guard |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain.
