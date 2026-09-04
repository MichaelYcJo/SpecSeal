# 1788491830-a-segments-record-says-what-it-cost — review round 3

| Field | Value |
|---|---|
| Target SHA | 7386c07 |
| Ran by | specseal:warden on Opus — handed over in the spawn prompt |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no — four 🟡 opened, every one answerable with grounds and all four handed to issue #152 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round of round 2's fixes, at `git diff 6bd730c..HEAD` — one
commit — with round 2's four findings and its ❓ 10 as the agenda.

**The prompt said not to go looking for work.** This is the third round and
the ordinary cap, so the question was whether round 2's four are closed and
whether the fix pass's own work holds.

One surface was named as unusual: `round-2.md`'s `New units` reads `none`,
deliberately, because both 🟡 6 and 🟡 7 land inside cases the round-1 fix pass
created and a new top-level unit answering them would be depth 2, which this
repository's own rule forbids. The round was told that *no new units* is the
answer the depth rule rewards and therefore the answer to be suspicious of,
and to check the claim rather than accept it.

Six things to break, in order: the 🟡 6 replacement and whether building its
reference from the module's own constants moves both sides together; the class
at its sixth instance and whether `count == 1` is itself satisfiable by
something else; §12's reach on the false row; R1's rewritten grounds; the
sibling edit ❓ 10 carried; and whether the mutation loop mutated duplication
as well as deletion.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 2's 🟡 6, the arm-order case | `tests/test_a_record_says_what_ran_it.py` | answered | Executed. Arms reversed → green, which **is** the claim; the unknown arm's `.strip(SEPARATORS)` weakened → red naming the case; the arm deleted → red. The corpus is 756 cells, 72 reaching both arms, and its `reached_both` guard is live — deleting the one tail carrying ` on ` turns the case red on that guard |
| 🟢 2 | Round 2's 🟡 7, the one-record fixture | same file | answered | Executed three ways: `declared()` reverted to one record → red on the new assertion; `ran_by` narrowed to the last record → red; both → red |
| 🟢 3 | Round 2's 🟡 8, the false no-prefix row and §12's second place | `docs/review-chain-spec.md` | answered on the code question | Both rows now match the code — `stopping_floor` and `ran_by` gate only the absent row on `began is None`, and the empty and neither-answer branches append unconditionally. Its **pin** is 🟡 5 below |
| 🟢 4 | The third row, `:717` under `Needs a fix`, rightly left alone | `docs/review-chain-spec.md:717` | answered | `needs_excused` gates all three states there, so *any of those … prints* is true in that one place and nowhere else. `:651` and `:681` claim only about absent rows and are correct |
| 🟢 5 | Round 2's 🟡 9, the rule stated as enforced | `docs/review-chain-spec.md` | answered | Executed: rewriting the sentence → red; deleting the paragraph → red |
| 🟢 6 | Round 2's ❓ 10, the constant-name tautology and the sibling | two test files | answered | Executed all four directions — deleting the reason from either file → red; duplicating it into an unrelated docstring → red. The sibling kept everything it already held |
| 🟢 7 | `New units: none` | `tests/test_a_record_says_what_ran_it.py:701` | answered | `split_first` is nested, so the depth rule is not evaded. Read line by line against `runner_problem`: a faithful mirror with the arms swapped, its index guarded by the same short-circuit. What it is **built from** is 🟡 6 |
| 🟡 5 | The pin for round 2's 🟡 8 counts copies and never asks where they are, so the row it guards can be false again while the case stays green | `tests/test_a_record_says_what_ran_it.py:505` | answered — deferred to #152 | Executed: reword the row false in different words and add a second corrective to the floor's row — count stays 2, suite green, and the false row is back unseen. The seventh instance of this work item's class, and the sibling assertion one screen away uses `count == 1`, which is not satisfiable that way |
| 🟡 6 | R1's Verified cell names `6bd730c`, where the case it describes does not exist, and names a red the case does not produce | ledger `:18` | answered — deferred to #152 | The other three rows name the commit their content is in; this names the parent. And the reference is built from the module's constants, so adding `;/` to `SEPARATORS` and dropping `ON_RE`'s `IGNORECASE` each left the whole suite green — the red the cell claims comes from a different mutation |
| 🟡 7 | The fixture's `2 round record(s)` needle is a substring satisfied by `12 round record(s)` | same file, `:273` | answered — deferred to #152 | Executed: widen the fixture to twelve and the case stays green while its own message says two. The eighth instance, inside the guard written to close the seventh |
| 🟡 8 | R1's Notes assert a refusal-message difference that does not exist | ledger `:18` | answered — deferred to #152 | Executed: 393 of 756 cells refused by both orders, **zero divergences**, and true by construction. Inherited through the rewrite rather than introduced, but the row was the thing being fixed |
| ❓ 9 | The fragment is 9 ok where rounds 1 and 2 both recorded 10 — a coordinate was dropped unremarked | ledger | recorded | No coverage lost: the dropped case is verdict-only and green under the reversed order. The number two records assert has moved and nothing says so |

## Executed probes

| What was run | Result |
|---|---|
| control, both changed files | 85 passed |
| real arms reversed | green — the claim |
| `.strip(SEPARATORS)` → `.strip()` in the unknown arm | red, naming the arm-order case |
| `SEPARATORS` gains `;/`; `ON_RE` loses `IGNORECASE` | **green — whole suite**, which is 🟡 6 |
| the corpus's only both-arm tail removed | red on the `reached_both` guard |
| the two orders' refusal reasons over 756 cells | 393 both-refused, **0 divergences** |
| the false row reworded **and** the corrective duplicated into the floor's row | **green — 🟡 5** |
| a third true mention of the corrective added | red — 🟡 5's other direction |
| the fixture widened to twelve records | **green — 🟡 7** |
| the reason deleted and duplicated across both files | red, all seven |
| both proposed fixes, unmutated then under their mutations | green, then red |
| `evidence-check --ledger 'seal/ledger/1788491830-*.md' --strict .` | 9 ok, exit 0 |
| `uvx ruff check tests/ skills/` · `bin/unverified-check` | exit 0 · exit 0 |

Twenty-eight mutations plus a control, in a `git clone --no-local`.

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 2 | the class named in `phases/phase-4.md` | Six instances at round 2, seven and eight here, **both inside the fix for the sixth** |
| round 2 | `seal/ledger/1788491830-*.md` R1 | Round 2 found its grounds were a story; round 3 found the rewritten grounds name a commit the case is not in and a red it does not produce |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 5, 🟡 6, 🟡 7 and 🟡 8, with their paste-ready fixes and the mutations each was measured under | issue #152 | the repository owner |
| ❓ 9, the coordinate count two records assert | #152's context | the repository owner |
| The full suite, repository-wide lint and typecheck | `overview.md` §Not verified | the orchestrator's single broad run — now due |
| `seal/ledger.md` S8 | work item `1788472135`'s memo | the repository owner |

**The run ends here, at the cap rather than at the floor.** Three rounds, no
🔴 open, and `docs/review-chain-spec.md` gives three as *the ordinary case, and
the only one for 🟡 and ❓ findings*. All three rounds also answered
`Loses a record or crashes: no`, so the floor says the same thing from the
other direction.

This is the **second time in this release a bound has stopped a run with cheap
fixes on the table** — #146 was the first, at #136's verifying round. Both are
evidence for whether the bounds are set right, which is what makes recording
the cost worth more than taking an exception. Every fix in #152 is paste-ready
and already measured.
