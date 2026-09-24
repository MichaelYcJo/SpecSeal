# 1790260565-a-ledger-row-carries-two-readings-in-one — review round 2

| Field | Value |
|---|---|
| Target SHA | 103b0974ad8f64f6d27cac8a900fe141b4320f2f |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 588 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item 1790260565 is the verifying round: the diff of round 1's fixes, db544d4f..938edc68, at 103b0974. Its job is whether round 1's ⬜ 1 and ⬜ 2 are closed and ⬜ 3 and ⬜ 4 stand as answered, and whether EDIT_OUTCOMES, the unit the fixes created, is correct.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `CONTRIBUTING.md`'s re-stamp needle in `EDIT_OUTCOMES` holds the bullet's premise, and the act (`evidence-check --reverify .`) can be deleted with every case green | `tests/test_a_merge_cannot_silently_drop_a_correction.py:754` | open | Executed: clause deleted from `CONTRIBUTING.md` in the clone, guides' case 1 passed |
| ⬜ 2 | Correction: E1's note cites `EDIT_OUTCOMES` as what holds the outcomes, and the row does not anchor it | `seal/releases/0.15.1.md` | open | Read. The owner's case anchor hashes the function, not the dictionary; `CONFLICT_SENTENCES` is anchored for this reason. Hash `f810196e` computed by `--reverify` on a scratch ledger (executed) |
| ⬜ 3 | Correction: E1's and E2's new notes cite `rounds/round-1.md` for red runs it does not record | `seal/releases/0.15.1.md` | open | Read. `round-1.md` carries no deletion run; the runs appear only in commit 950db9ef's message |
| 🟢 | round 1's ⬜ 1 is closed — the union clause, the edit rule's other two outcomes and the guides' two arguments are held by needles | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | confirmed | Executed: each of 13 needle-carrier pairs occurs once; each deletion red in the right case, needle named |
| 🟢 | round 1's ⬜ 2 is closed — the unit case's comment names what goes red and what does not | `tests/test_release_hygiene.py:1296` | confirmed | Executed: width dropped inside `ledger_overwide` → 1 failed; corpus calling `overwide_rows` bare → 3 passed |
| 🟢 | round 1's ⬜ 3 is answered — none of the four shapes is in a ledger file, and the two deferred shapes have homes | `tests/test_release_hygiene.py:1255` | confirmed | Carried: the fix range touches neither `overwide_rows` nor any ledger file's table shape, so round 1's executed count still stands |
| 🟢 | round 1's ⬜ 4 is answered — the plan's approval line stands alone | `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5` | confirmed | Read: the second sentence is on line 6 at the target |
| 🟢 | `CLAUDE.md` was not edited in place | `CLAUDE.md` | confirmed | Executed: no commit in f673e3b1..103b0974 touches it; empty fix-range diff |
| 🟢 | E1, E2 and L1 re-read and re-stamped, and every anchor resolves | `seal/releases/0.15.1.md`, `seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md` | confirmed | Executed: `evidence-check` 200 ok, 0 drifted, 0 broken over the two files; whole tree exit 0 |

## Paste-ready fixes

```python
    "CONTRIBUTING.md": (
        "the claim still holds and you have re-read it — run "
        "`evidence-check --reverify .`",
        "remove the row and write the new claim into your own fragment",
    ),
```
```
`docs/the-evidence-ledger.md#"## A row is a content anchor, and it names no commit"@c69d1fb2`, `CONTRIBUTING.md#"## House rules"@c1fd7d64`, `tests/test_a_merge_cannot_silently_drop_a_correction.py#CONFLICT_SENTENCES@4e5f6382`, `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_policy_document_owns_the_exception_and_the_halves@b5565675`, `tests/test_a_merge_cannot_silently_drop_a_correction.py#EDIT_OUTCOMES@f810196e`
```
```
the right case went red (commit 950db9ef's message; reproduced by round 2's reviewer, `rounds/round-2.md`)
```

## Executed probes

| What was run | Result |
|---|---|
| A probe named with the test_tmp prefix, run once in the clone and deleted: whitespace-collapsed counts of the 13 new needle-carrier pairs, then each deleted from its carrier in turn, running the guides' case and the owner's case | each count 1; each deletion 1 failed, 1 passed, with that needle named; the carrier restored each time |
| The same probe: the act `evidence-check --reverify .`, which recomputes the hash and names what it changed, deleted from `CONTRIBUTING.md` with the premise kept | 1 passed: this is ⬜ 1 |
| The same probe: the proposed ⬜ 1 needle searched in `CONTRIBUTING.md`, whitespace collapsed | found |
| The same probe: `ledger_overwide` returns `overwide_rows(text)` without the width | 1 failed, 2 passed |
| The same probe: the corpus case calls `overwide_rows` instead of `ledger_overwide` | 3 passed |
| Argument needle counts in `docs/the-evidence-ledger.md` | 0 and 0 |
| `git log f673e3b1..103b0974 -- CLAUDE.md` and `git diff db544d4f..103b0974 -- CLAUDE.md` | no commit, empty diff |
| `bin/evidence-check --ledger seal/releases/0.15.1.md --ledger` the fragment | 200 ok, 0 drifted, 0 broken, exit 0 |
| `bin/evidence-check .` | exit 0 |
| `bin/evidence-check --reverify` over a scratch ledger with one `EDIT_OUTCOMES` row, deleted after | `EDIT_OUTCOMES@f810196e` |
| `bin/correction-check --range db544d4f...103b0974` | exit 0 |
| `bin/test -q -p no:xdist tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_release_hygiene.py tests/test_no_real_identifiers.py` | 108 passed, exit 0 |
| The broad gate: full suite, lint and format over the finished branch | not yet: it has not been run, and it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | round 1's ⬜ 1 — fixed |
| round-1 | `tests/test_release_hygiene.py:1296` | round 1's ⬜ 2 — fixed |
| round-1 | `tests/test_release_hygiene.py:1255` | round 1's ⬜ 3 — answered |
| round-1 | `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5` | round 1's ⬜ 4 — answered |
| round-1 | `seal/releases/0.9.2.md:31`, `seal/releases/0.8.2.md:145`, `seal/releases/0.9.3.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.2.md:31` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_release_hygiene.py:1233` | round 1's 🟢 — confirmed |
| round-1 | `docs/round-record-spec.md:542` | round 1's 🟢 — confirmed |
| round-1 | `seal/` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
