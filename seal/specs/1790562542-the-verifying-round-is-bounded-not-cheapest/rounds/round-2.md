# 1790562542-the-verifying-round-is-bounded-not-cheapest — review round 2

| Field | Value |
|---|---|
| Target SHA | 08e6eeb450a2124110ab63720f1869c524f3d8b4 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #648 |
| Broad gate | 65ace7cc against 1fa25931 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790562542 (#639), the verifying round. Its target is the diff of round 1's fixes, e062e3a7..1200940f (14ddebd6 the fixes, 1200940f the record corrections and re-stamps), with the branch at 08e6eeb4 and draft PR #648. The job is the answers, not new findings: for each verdict round-1.md records as closed (🟡 1, 🟡 2 and ⬜ 3 fixed at 14ddebd6, ⬜ 4 answered as a correction at 1200940f), is it actually closed. The finding surface is what round 1's `New units` names (none) plus the changed constants `CARRIERS` (a fifth tuple) and `CHEAPEST_81_CARRIERS` (gone halves now tuples), since nobody has reviewed them. Answer `Needs a fix:` and `Loses a record or crashes:` in lines of their own.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed — the #82 comparison is gone from the skill, the template comment and the module docstring, and both carriers pin its absence | `skills/code-review/SKILL.md:230` | confirmed | Read at `08e6eeb4`; a tree-wide grep finds it only in gone halves and `seal/` quotations. Executed: re-adding it to the skill, and then to the template, turned the absent case red each time |
| 🟢 | round 1's finding 2 is closed — the warden's scoping paragraph is grounded on answering the finding, not on a first round's price | `agents/warden.md:111` | confirmed | Read; it now matches C4's ground. Executed: the `5a66666d` paragraph restored turned both cases red, and the old clause appended alone turned the gone case red. A price-word sweep found no further member |
| 🟢 | round 1's note 3 is closed — the chain spec's median names round 1's span | `docs/review-chain-spec.md:220` | confirmed | Read; the fragment, docstring, V1 and `overview.md` agree. Executed: deleting `the span of` turned the stands case red. RUF001 on the literal sign confirmed with ruff |
| 🟢 | round 1's correction 4 is closed — the changelog fragment, V2, phase 1 and the overview row follow the corrected wording with dated notes | `seal/ledger/1790562542-the-verifying-round-is-bounded-not-cheapest.md:4` | confirmed | Read each; `evidence_check.py .` exits 0 (executed). The six release re-stamps change only hash and note, each note true to its edit |
| 🟢 | the fifth `CARRIERS` tuple and the tuple-valued gones in `CHEAPEST_81_CARRIERS` are consumed correctly and each gone is live | `tests/test_the_verifying_round_is_bounded_not_cheapest.py:65` | confirmed | Read every consumer. Executed: each added gone seen red on its own, and both modules pass at `08e6eeb4` |
| ❓ | Whether #639's median 0.83, its range 0.26–1.27 and the five at or above round 1 reproduce | `docs/review-chain-spec.md:219` | ❓ out of verified scope | Carried from round 1 and not re-derived here. Answered by a measurement from #639's author (`questions.md` Q1) |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_verifying_round_is_bounded_not_cheapest.py` and `tests/test_a_segments_record_says_what_it_was_asked.py`, in the clone at `08e6eeb4` | exit 0, 15 passed, before the mutations and again after the bytes were restored |
| Mutation: the #82 comparison re-added to `skills/code-review/SKILL.md` beside the stands phrase | exit 1, 1 failed (`test_81s_round_one_is_not_called_the_cheapest_again`), 14 passed |
| Mutation: the #82 comparison re-added to the `templates/sdd-round.md` comment | exit 1, the same case failed, 14 passed |
| Mutation: the `agents/warden.md` scoping paragraph restored as at `5a66666d` | exit 1, 2 failed (the stands case and the gone case), 13 passed |
| Mutation: the new warden clause kept and "which is how a review loop costs more than the work it reviews" appended | exit 1, 1 failed (the gone case), 14 passed |
| Mutation: `the span of` deleted from `docs/review-chain-spec.md` | exit 1, 1 failed (the stands case), 14 passed |
| `evidence_check.py .` in the clone | exit 0, 0 drifted |
| `bin/survivor-check --range e062e3a7..1200940f` in the clone | exit 0, "no removed wording is still standing" over 454 files and 35 removed sentences |
| `ruff check` and `ruff format --check` on the two changed test modules | exit 0, and both already formatted |
| `ruff check` on a one-line scratch file holding a literal `×` in a string | RUF001 reported |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — not run by this round. It is the sealer's, and it is now due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/SKILL.md:231` | round 1's 🟡 1 — fixed |
| round-1 | `agents/warden.md:111` | round 1's 🟡 2 — fixed |
| round-1 | `docs/review-chain-spec.md:220` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/changelog.md:28` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/orchestration.md:132` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.4.0.md:114` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_segments_record_says_what_it_was_asked.py:8` | round 1's 🟢 — confirmed |
| round-1 | `docs/review-chain-spec.md:219` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
