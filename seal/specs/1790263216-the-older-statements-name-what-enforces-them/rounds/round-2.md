# 1790263216-the-older-statements-name-what-enforces-them — review round 2

| Field | Value |
|---|---|
| Target SHA | da07ecbd2ff7f779d1bf0ad378b681191f1dabb3 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 594 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item 1790263216 is the verifying round: the diff of round 1's fixes, 7e9bf98f..c231af28, at da07ecbd, together with the merge of #587's final tip (f52abbe1) and the -s ours record of the release (da07ecbd). Its job is whether round 1's eight verdicts are closed, whether the four new targets go red, and whether the merge kept every note.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Four phase rows (D13, D14, D32, D33) still state the decision round 1's fixes replaced, and only D6's row carries a correction note | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/phase-1.md:51` | open | read; also `phase-1.md:52`, `phase-2.md:39`, `phase-3.md:22`; a correction to the run's paperwork, the overview's *Not done* already names the moves |
| 🟢 | round 1's finding 1 is closed — D6 names the pin on its instruction | `docs/the-evidence-ledger.md:153` | confirmed | executed: the target red with CONTRIBUTING.md's instruction reworded and red with CLAUDE.md's; read: no `continue-on-error` in any workflow; the owner's own opening reworded leaves it green, and nothing in `tests/` reads that sentence |
| 🟢 | round 1's finding 2 is closed — D13 names two pins | `docs/the-evidence-ledger.md:346` | confirmed | executed: the first target red with the settle skill's sentence reworded; the second red with the policy's own bold opening reworded |
| 🟢 | round 1's finding 3 is closed — D14 names the pin on settle's three answers | `docs/the-evidence-ledger.md:359` | confirmed | executed: red with *retire the case* reworded; the owner's opening reworded leaves it green |
| 🟢 | round 1's finding 4 is closed — D32 names the contract's §15 pin | `docs/round-record-spec.md:941` | confirmed | executed: red 1 of 16 with §15's phrase reworded; the statement names §15 as the rule's home; its own opening reworded leaves it green |
| 🟢 | round 1's finding 5 is closed — D33 says no case reads its opening | `docs/review-chain-spec.md:112` | confirmed | read: the one mention in `tests/` is the rule-13 comment saying the phrase is not pinned; executed: `fold-check` exit 0 |
| 🟢 | round 1's finding 6 is closed — the checklist names `Target SHA` alone | `docs/release-checklist.md:29` | confirmed | read: also line 260; the class sweep finds no sentence saying a stamp names a commit; executed: `survivor-check` over the PR range exit 0 |
| 🟢 | round 1's finding 7 stays answered | `docs/branch-and-release.md:146` | confirmed | read: the fix range does not touch D90, and the overview's *Not done* carries it |
| 🟢 | round 1's finding 8 is closed — both phase records corrected | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/phase-2.md:82` | confirmed | read at c231af28; phase 1's D6 row withdraws *allowed to fail* |
| 🟢 | f52abbe1 kept every note as a union, and every re-stamped row carries a dated note | `seal/releases/0.15.1.md` | verified | executed: the probe found 0 missing notes over 37 rows; `correction-check` 0 dropped over 3 merges; `evidence-check` 2115 ok, 0 drifted |
| 🟢 | da07ecbd's `-s ours` dropped nothing from the release branch | da07ecbd | verified | executed: its tree equals f52abbe1's; 58629718's tree equals 6e850fb1's, which f52abbe1 merged |
| 🟢 | the fix pass's four re-stamps (S9, C1, C3, E2) each carry a dated note | `seal/releases/0.13.1.md` | confirmed | read in 6826f53f; also `0.11.1.md` and `0.15.1.md`; executed: `evidence-check` 0 drifted |
| 🟢 | the counts moved with the fixes: 9 `nothing` lines, 4/0/2/3 | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/overview.md:28` | confirmed | executed: the grep returns 9, split as stated |
| ❓ | Whether the read decisions no round has opened catch their breaking edits, including owner statements whose only reader is a guide's or skill's copy (as D6, D14 and D32 are) | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/` | ❓ out of verified scope | carried from round 1; a verifying round stays in the fix range; the orchestrator decides whether a later work item takes it |

## Paste-ready fixes

```
 **Corrected in round 1's fix pass:** the line now names `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row` and `test_the_skill_says_what_a_fold_does_to_the_ledger`, the pins on the rule's instruction and on the policy's own opening.
```
```
 **Corrected in round 1's fix pass:** the line now names `test_the_skill_names_the_floors_a_fold_has_to_answer`, the pin on settle's three answers.
```
```
 **Corrected in round 1's fix pass:** the line now names `test_each_section_holds_its_rule`, the pin on the contract's §15.
```
```
 **Corrected in round 1's fix pass:** rule 13 pins the statement's third bold sentence and not its opening, so the line now says `nothing — no case reads the opening yet`.
```

## Executed probes

| What was run | Result |
|---|---|
| clean run of the five node ids the four fixed lines name | exit 0, 20 passed |
| D6: CONTRIBUTING.md's, then CLAUDE.md's *resolve it hunk by hunk and read both sides* reworded | red each time (1 failed) |
| D6: the policy's bold opening reworded to *take the newer side* | green (1 passed): no case reads the owner's sentence |
| D13: the settle skill's *A fold opens no directory* reworded | 1 failed, 1 passed |
| D13: the policy's *A fold is not a work item, and it adds nothing to the ledger.* reworded | 1 failed, 1 passed |
| D14: the settle skill's *retire the case* reworded | 1 failed |
| D14: the policy's bold opening reworded to *lowered until the run passes* | green (1 passed) |
| D32: the contract's §15 *before it is committed as a case* reworded | 1 failed, 15 passed |
| D32: the statement's bold opening reworded | green (16 passed) |
| tree state after every restore | clean |
| notes-union probe over f52abbe1 (base e9dfe623, sides 1d0262d7 and 6e850fb1) | exit 0; 0 missing notes; 7 rows edited by both sides, each with one new merge note; no row changed only at the merge |
| `git merge-tree --write-tree 1d0262d7 6e850fb1` | 6 conflicted files, as the commit message says |
| `git diff f52abbe1 da07ecbd`, `git diff 6e850fb1 58629718` | both empty |
| `bin/correction-check --range 7e9bf98f..da07ecbd` | exit 0; 3 merges, no correction marker dropped |
| `bin/evidence-check .` at da07ecbd | exit 0; 2115 ok, 0 drifted, 0 broken |
| `bin/fold-check` at da07ecbd | exit 0; 136 statements read, cutoff 0 binds 136; 14 documents under 1000 lines |
| `bin/survivor-check --range 58629718...da07ecbd` | exit 0; 88 removed sentences, none standing |
| `bin/survivor-check --range 7e9bf98f..c231af28` | exit 1; 2 places, neither a rider sentence: the ownership statement's line and the spec's template example |
| `bin/test` over the folded-statement, room, editions, merge-correction and one-owner modules | exit 0, 184 passed |
| `bin/test tests/test_release_hygiene.py -k "ledger or row or reading or overwide"` | exit 0, 6 passed |
| `grep -rn 'Enforced by: nothing' docs/` | 9 lines |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/the-evidence-ledger.md:148` | round 1's 🟡 1 — fixed |
| round-1 | `docs/the-evidence-ledger.md:343` | round 1's 🟡 2 — fixed |
| round-1 | `docs/the-evidence-ledger.md:358` | round 1's 🟡 3 — fixed |
| round-1 | `docs/round-record-spec.md:941` | round 1's 🟡 4 — fixed |
| round-1 | `docs/review-chain-spec.md:112` | round 1's 🟡 5 — fixed |
| round-1 | `docs/release-checklist.md:30` | round 1's 🟡 6 — fixed |
| round-1 | `docs/branch-and-release.md:146` | round 1's ⬜ 7 — answered |
| round-1 | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/phase-2.md:82` | round 1's ⬜ 8 — answered |
| round-1 | `seal/config.md` | round 1's 🟢 — confirmed |
| round-1 | the 116 added `Enforced by:` lines | round 1's 🟢 — confirmed |
| round-1 | `docs/one-root-by-lifetime.ko.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
