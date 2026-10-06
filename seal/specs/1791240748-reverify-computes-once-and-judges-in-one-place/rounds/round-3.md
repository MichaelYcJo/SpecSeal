# 1791240748-reverify-computes-once-and-judges-in-one-place — review round 3

| Field | Value |
|---|---|
| Target SHA | c4c2578980f900d3a2e0a3876fd7c75d27d6cf88 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #829 |
| Broad gate | 308fc48f against 4b363e68; earlier run: d4cdf7f0 against e6d5a055 |
| Fixes checked by | no fixes to check |
| Fix range | `c4c2578980f900d3a2e0a3876fd7c75d27d6cf88..c4c2578980f900d3a2e0a3876fd7c75d27d6cf88`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round for round 2's fix range `96cc3e46..90fb07c4`, which ends the run: whether the restored `rewrites` guard in `through` keeps a loop through a row `--checked` leaves whole from being read as a cycle, and whether every other member the early leaving reads can only be one with a hash to write and a row it rewrites, while the fallback at the bound leaves only coordinates still moving; whether the citation memo now keys on everything `read_citation` and `judge` read, so `--strict` and `--reverify` name a row in its own verb; whether the unsettled branch's case pins it; and whether the docstring, comment, changelog and ledger E3, E4 and 0.4.0 rows say what the code does.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | E3 says the bound's arm reads the cycle through the hash-to-write and row-rewritten guard and leaves only cycle members; the bound calls on_a_cycle with no AMONG and falls back to every moving coordinate | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:23` | deferred #833 | #833; Read: evidence_check.py:3723 against the row; the code comment at :3698 says it right; a correction to the run's paperwork, answered by the orchestrator's post-run fix |
| 🟢 | round 2's finding 1 is closed — a loop through a row --checked leaves whole is no longer read as a cycle | `skills/evidence-check/scripts/evidence_check.py:3716` | confirmed | Executed: the case red with the guard replaced by True; six probe shapes, three loops through a four-cell row named nothing does not settle, three real cycles named one row each |
| 🟢 | round 2's finding 2 is closed — the static memo keys on the row's verb | `skills/evidence-check/scripts/evidence_check.py:3611` | confirmed | Read: the key covers every input of read_citation and judge; executed: the case red with the verb dropped |
| 🟢 | round 2's finding 3 is closed — a coordinate that does not settle records no pact change, and a case pins it | `tests/test_a_signatory_records_a_pact_change.py:2376` | confirmed | Executed: red at its record assertion with the arm restored, green at the target |
| 🟢 | round 2's finding 4's answer holds — the record-order case is red only with the sort removed | `tests/test_a_signatory_records_a_pact_change.py:2355` | confirmed | Executed: red with return sorted(out) replaced by return out |
| 🟢 | round 2's finding 5's answer holds — the docstring, comment, changelog and E3 say a coordinate is left at its first rewrite from the second round | `skills/evidence-check/scripts/evidence_check.py:3396` | confirmed | Read against step, rewrote and through; the pinning case passed in the module run |
| 🟢 | The early leaving reads only members with a hash to write on a row a re-stamp rewrites | `skills/evidence-check/scripts/evidence_check.py:3332` | confirmed | Read: live comes from AMONG, names only over live, a start outside names is skipped |
| 🟢 | The bound's fallback leaves only coordinates still moving | `skills/evidence-check/scripts/evidence_check.py:3723` | confirmed | Read: looping is empty at exhaustion, so what is left is a subset of MOVING or MOVING itself |
| 🟢 | E4 and the 0.4.0 Corrected row say what the code does | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:24` | confirmed | Read against plan_ledger's unsettled arm and the memo key; executed: evidence-check --strict over the fragment, 240 ok |
| 🟢 | round 1's findings 1 to 4 stay closed under round 2's fixes | `skills/evidence-check/scripts/evidence_check.py:3314` | confirmed | Carried from round 2's grounds; executed: their cases pass in the two modules, 597 passed |

## Paste-ready fixes

```text
a coordinate on a cycle of rows naming each other or itself is left at the hash its row recorded and named on a `LEFT` line saying it does not settle: from the second round of a pass, in the first round that rewrites its own row, where the cycle is read over every coordinate still judged that has a hash to write on a row a re-stamp rewrites, so that a loop through a row `--checked` leaves whole is no cycle; and otherwise once the pass has run as many rounds as there are coordinates naming a line of a ledger it writes and not yet left, plus two, where every coordinate still moving is left, those on a cycle read over every coordinate still judged where any is
```

## Executed probes

| What was run | Result |
|---|---|
| bin/test over the fragment module and the pact-change module at the target | 597 passed, exit 0 |
| mutation-check: `and rewrites(key)` replaced by `and True`, the left-whole case | red: K named does not settle |
| mutation-check: the verb dropped from the static memo key, the shared-citation case | red: --reverify named the Corrected row in the Re-read row's words |
| mutation-check: the unsettled arm hands MOVES a BROKEN part, the does-not-settle case | red at the record assertion: one pact change recorded |
| mutation-check: `return sorted(out)` replaced by `return out`, the record-order case | red |
| One probe file run once over six shapes at the target, then deleted: the round 2 shape without --checked; a real two-row cycle beside a four-cell row; loops of two, three and four rows through a four-cell row under --checked; the loop of four with five cells in every row | Real cycles: one row named does not settle in each. Loops through the four-cell row: nothing named does not settle, the four-cell row left whole, every other drifted row re-stamped. Exit 1 in all six, for the row left whole or the row that does not settle |
| bin/evidence-check --strict --ledger over the work item's ledger fragment at the target | 240 ok, 0 drifted, exit 0 |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet; the sealer's, and its spawn comes due with this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3293` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3554` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3509` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3182` | round 1's 🟡 4 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3599` | round 1's ⬜ 5 — answered |
| round-1 | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:21` | round 1's ⬜ 6 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1669` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3549` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1827` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3653` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-2.md:80` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-4.md:21` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:19` | round 1's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3688` | round 2's 🟡 1 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3602` | round 2's 🟡 2 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3174` | round 2's 🟡 3 — fixed |
| round-2 | `tests/test_a_signatory_records_a_pact_change.py:2358` | round 2's ⬜ 4 — answered |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3397` | round 2's ⬜ 5 — answered |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3314` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3666` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2271` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3132` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1401` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2290` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
