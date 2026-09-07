# 1788761915-a-record-states-what-nothing-reads — review round 3

| Field | Value |
|---|---|
| Target SHA | e41352f |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 214 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no — the seven open findings are all issues rather than fixes to commission; the run is capped and this record ends it |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, **the closing round**, spawned against `e41352f` with round 2 closed —
eight fixed, one answered, one deferred — and the fix diff `9d04016..e41352f`
as the primary surface.

**The prompt stated the bound and what it changes about a finding's cost.**
Round 1 met the floor, round 2 was the verifying round and reopened, and round
2's fixes are the run's one reopening. `round_record.py new` had printed the
bound as it wrote round 2's record, so this round was told in as many words:
*the run ends with you, whatever you find; there is no fix pass after this and
no round 4; every finding you leave open becomes a filed issue.*

It was told just as plainly what that does **not** change: it does not lower
the bar. What it changes is what each finding owes — one that becomes an issue
has to stand for a reader six months out with no session context, so grounds
and coordinates matter more, not less. The prompt asked for **one line per open
finding saying `block` or `issue`**, and named that judgment as the most useful
thing the round would produce.

Round 1's finding 3 was handed over as decided by the owner rather than open —
the corpus hole stays, made durable as an issue — and round 2's finding 9 as
already deferred to one. Neither was the round's to reopen.

Eight facts were handed over with coordinates and §5 applied to each, including
the fix pass's `770 ok`, its narrow suite counts, its eleven new units at depth
1, and its two enumerations. **The prompt asked the round to assume a ninth
mutation survivor**, the assumption having been right on all three of this
run's passes. Two disclosures were carried rather than left to be rediscovered:
the fix pass declined a system directive to edit through `sed`, on contract §9,
and deferred one fail-open sibling as a rider.

Five axes: each claimed fix against its finding and its class, with finding 1's
monotonicity argument to be **tested rather than accepted**; what the three
widened signatures broke across five caller sets; the `held` region reader end
to end — nested fences, a fence in an aside, an aside in a fence, a marker on a
held line, a record ending mid-region; whether `2f2144c`'s dates are true,
sampled against the units they cite; and the branch as a whole, once, for
anything that loses a record, crashes, or fails open.

The assumption was right a fourth time. Seven findings, none needing a fix, and
the ninth survivor turned out to be the vestige of the design decision behind
one of them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 an HTML comment the record never closes silences every claim under it, and the arm says nothing — round 2's 🟡 3 one region kind over | `skills/evidence-check/scripts/evidence_check.py:1999` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/217 | https://github.com/MichaelYcJo/SpecSeal/issues/217 |
| 2 | 🟡 `bound_line` prints `one reopening remains` over a run the gate already refuses, and the sentence is not monotone — round 1's 🔴 2 and round 2's 🟡 1 a third time | `skills/code-review/scripts/round_record.py:1135` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/218 | https://github.com/MichaelYcJo/SpecSeal/issues/218 |
| 3 | 🟡 five `seal/ledger.md` rows carry a `Checked` date from before the unit they cite existed | `seal/ledger.md:121, :123, :161, :169, :296` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/219 | https://github.com/MichaelYcJo/SpecSeal/issues/219 |
| 4 | ⬜ a closer ends the LINE rather than a position in it: a claim after one is dropped, and a comment reopened on a closing line is read as claims | `skills/evidence-check/scripts/evidence_check.py:1999, :1993` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/220 | https://github.com/MichaelYcJo/SpecSeal/issues/220 |
| 5 | ⬜ the rider deferring `unread_items` gives a cost that belongs to `unshipped`, and names the cheap repair in its next sentence | `skills/evidence-check/scripts/evidence_check.py:1790` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/221 | https://github.com/MichaelYcJo/SpecSeal/issues/221 |
| 6 | ⬜ the count walk's inner `break` is unobservable — the ninth mutation survivor | `skills/code-review/scripts/round_record.py:1133` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/218 | https://github.com/MichaelYcJo/SpecSeal/issues/218 |
| 7 | ⬜ `depth_two` scopes by file, which is what keeps §15 satisfiable, and no docstring says so | `skills/code-review/scripts/round_record.py:1909` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/222 | https://github.com/MichaelYcJo/SpecSeal/issues/222 |
| 8 | round 2's findings 1 to 8 — each fix opened against the finding and against its class | `seal/specs/1788761915-a-record-states-what-nothing-reads/rounds/round-2.md` | answered | all eight close the finding. 1's class is open one walk-state over (finding 2); 3's is open one region kind over (finding 1); 7's is open on five rows (finding 3). 2's enumeration over the three kinds of line is right and complete for what it asks; 4's six sites and three fail-open verified by construction, not by its count; 5, 6 and 8 close whole — the duplicated comment is gone, the plural branch is pinned, and the two overstating rows now say what the code does |
| 9 | round 2's finding 9 — `N unread` mixes shipped history with the live case | `skills/evidence-check/scripts/evidence_check.py:1751` | deferred https://github.com/MichaelYcJo/SpecSeal/issues/216 | https://github.com/MichaelYcJo/SpecSeal/issues/216 |
| 10 | round 1's finding 3 — the corpus is a walk, not the tree | `skills/evidence-check/scripts/evidence_check.py:1885` | answered | inherited. The owner has decided it: the hole stays, made durable as an issue. `test_the_checker_asks_git_for_nothing` is green in this round's run, so the revert at `7dac665` still holds |
| 11 | §15 — the five `claim_lines` cases seen red | `tests/test_a_record_states_what_the_tree_has.py` | answered | executed: with `claim_lines` reverted to its `9d04016` body, 4 of the 5 fail and 1 passes — a pair-case, not a defect case. Four targeted mutations of the new body each turn exactly one of the five red |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test` on the three modules the diff touches, in the clone | `159 passed` |
| `./bin/evidence-check --strict .` in the clone at `e41352f` | exit 0 · `770 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records `3 work items read · 38 unread · 236 names read · 0 stamps read · 0 refused` |
| `claim_lines` over 15 constructed region shapes — nested fences, a fence in an aside, an aside in a fence (closed and unclosed), the marker on a held line, a record ending mid-region | 12 correct; three gaps — an unclosed aside takes everything (finding 1), a claim after a mid-line closer is dropped, a comment reopened on a closing line is read as claims (finding 4) |
| the checker end to end on six fixtures: bare claim, closed fence, unclosed fence, closed comment, unclosed comment, unclosed comment with the claim four lines down | unclosed fence exit 2 as designed; **unclosed comment exit 0, `0 names read`, both shapes** — finding 1 |
| every `.md` under the three unshipped work items, walked for a record ending inside a fence or an aside | none — finding 1 is latent, not live |
| differential run of `bound_line` against `chain_check.stopping_floor`, 584 record sequences of length ≤ 3 over floor × `Needs a fix` × verdict, `chain.WORKTREE` on both sides | one disagreeing class, 16 sequences, all permissive: the gate already errors and the line does not end the run. No sequence trips the gate unannounced — finding 2 |
| the reachable shape run through `round_record.py`: floor `no`, quiet, reopened, writing round 4 | round 3 → `this record ends the run … reaches 2`; round 4 → `one reopening remains`; `stopping_floor` at `round-1.md` → error — finding 2 |
| twelve mutations of `floor_and_fixes`, `bound_line`, `unshipped`, `record_files` and `check_records`, one at a time, files restored and byte-compared after each | eleven killed; the inner `break` survives at `94 passed` — finding 6 |
| `claim_lines` reverted to its `9d04016` body, plus four targeted mutations of the new body, against the five new cases | old body: `4 failed, 1 passed`. Each mutation turns exactly one case red. Unmutated control `5 passed` — §15 satisfied |
| every ledger row's anchor set and `Checked` cell compared at `8740da3` and `e41352f` (319 rows both sides) | 7 rows hash-and-date moved; 8 rows hash moved alone, 5 of them re-pointed onto a unit created on 2026-09-07 with dates of 2026-09-01/02 — finding 3 |
| the base tree and the reverse history of `check_text` | absent at base; created at `1b1a1c8`, 2026-09-07 — finding 3 |
| every directory read in `evidence_check.py`, by construction | six sites at `:635`, `:977`, `:1739`, `:1799`, `:1850`, `:2094` — finding 4's enumeration verified, not accepted |
| every caller of the three widened signatures, by grep over `*.py` | `floor_and_fixes` 2 · `record_files` 2 · `unshipped` 4 · `unread_items` 2 · `claim_lines` 3. All converted; nothing unpacks the old arity |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2115` | round 1's 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1056` | round 1's 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1885` | round 1's 3 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:97` | round 1's 4 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2126` | round 1's 5 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1699` | round 1's 6 — fixed |
| round-1 | `tests/test_a_record_states_what_the_tree_has.py` | round 1's 7 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1017` | round 1's 8 — fixed |
| round-1 | `skills/evidence-check/SKILL.md:230` | round 1's 9 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1735` | round 1's 10 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1822` | round 1's 11 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1041` | round 1's 12 — fixed |
| round-1 | PR #214 body | round 1's 13 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:95` | round 1's 14 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:1103` | round 2's 1 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1797` | round 2's 4 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2213` | round 2's 5 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:1147` | round 2's 6 — fixed |
| round-2 | `seal/ledger.md` | round 2's 7 — fixed |
| round-2 | `seal/specs/1788761915-a-record-states-what-nothing-reads/rounds/round-1.md` | round 2's 8 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:1751` | round 2's 9 — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 2's 🟡 9 — `N unread` mixes shipped history with the live case | an issue, filed by the orchestrator | the orchestrator |
| round 1's finding 3 — the corpus is a walk, not the tree | an issue, filed by the orchestrator | the owner, decided — leave the hole |
| findings 1 to 7 above | issues, filed by the orchestrator | the orchestrator; `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* is why they are issues rather than fixes to commission |
