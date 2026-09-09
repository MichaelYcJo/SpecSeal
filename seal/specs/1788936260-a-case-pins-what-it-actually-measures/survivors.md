# 1788936260-a-case-pins-what-it-actually-measures — survivor exemptions

`survivor-check --range cea4c81..HEAD` reports one place still carrying
wording this range removed. It is not a stale copy: it states the same claim
in the same direction, and it is the case's rationale rather than a copy of
the assertion that changed.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_a_segment_feeds_the_flow_log.py` | measured over one machine's transcripts, 100% of the overlap above a second is calls batched into one assistant message and none of it crosses a turn. | **Same claim, same direction, and it is the rationale rather than a copy.** What the range removed was the four assertion MESSAGES — *"the measured claim is that none of the overlap crosses a turn; without it the paragraph asserts a cause it does not bound"* and its siblings. The check matched two phrases they share with this docstring, *"of the overlap"* and *"crosses a turn"*, scoring 2.00. The docstring says why the case exists: batching is the ordinary cause, and the measurement found none of the overlap crossing a turn. `skills/verify/SKILL.md` now reads *"every second of overlap above a second came from calls batched into one message and none of it from a call that crossed a turn"* — the same ranking and the same direction. Nothing survived a correction here; the assertions were replaced because a SUBSTRING cannot pin a rearrangement, not because the claim was wrong |

**What would make this exemption stop holding.** The quote is the anchor. If
that sentence changes — in particular if it comes to name a background command
as the ordinary cause, or to reverse the *from A and not from B* direction —
the exemption no longer covers it and the docstring is a genuine survivor.

## Round 1's fix pass

`survivor-check --range d07ccbb..5b55671` reports one place. It is a second
scope filter, not a stale copy of a corrected claim.

| Path | Quote | Grounds |
|---|---|---|
| `skills/verify/scripts/arm_check.py` | `if only:` / `found = [a for a in found if a.scope == only]` | **Two filters in two places, both correct, and only one of them was corrected.** Finding 8's fix rewrote the LISTING branch of `main` — `found = [a for a in every if a.scope == args.only] if args.only else every` — so that the unfiltered total is taken before `--only` narrows anything and the header can say `N of M arms (--only)`. What the check matched are two code phrases the two filters share, *"only found a"* and *"a in found if a"*, scoring 1.90; there is no claim in either. `run_arms`'s filter is the run's own scope narrowing, it returns verdicts rather than a total, and `main` computes `every` from `arms_of_file` before calling it — so nothing there states a denominator for the corrected line to have falsified. Enumerated: `git grep -n "scope == \|args.only\|if only"` over the module gives these two filter sites and no third |

**What would make this exemption stop holding.** If `run_arms` comes to print
or return a total of its own, its filter starts stating a denominator and the
correction above reaches it.

## Round 2's fix pass

`survivor-check --range 0c93614..970e2e0` reports five places, and they are
one group. Round 2's finding 15 relabelled a list that had come to hold **two**
outcomes — an arm `mutate` refused before anything was written, and an arm
whose command timed out or could not be spawned after the mutation was applied
and restored. The wording the range removed (*the truth is this was never
tried*, *an operator that could not be asked of an arm*) was true of the whole
list when it held only the first outcome, and it is **still true of every one
of these five places, because each one's subject is that first outcome**: a
match pattern, a bare `except:`, a `SyntaxError` from a mis-spliced mutation.
None of them is a stale copy of a corrected claim; correcting them would make
them vaguer than the thing they describe.

| Path | Quote | Grounds |
|---|---|---|
| `skills/verify/scripts/arm_check.py` | An unmutated arm reported as `survived` reads as *no case watches this* when the truth is *this was never tried*. | `mutate`'s docstring, about `mutate` raising rather than returning the source unchanged. On that path nothing has been written to disk, so *never tried* is exactly right — it is the outcome round 2 kept sayable by moving the distinction into the reason beside each arm |
| `tests/test_arm_check.py` | An arm the checker enumerates and cannot mutate must not come back as `survived` — that reads as *no case watches this* when the truth is *this was never tried*. | `test_an_arm_with_no_defined_mutation_is_refused_not_reported_unwatched`, whose arms are a match pattern and a bare `except:`. Both are refused by `mutate`, so nothing was tried and nothing was written. The case that pins the *other* door asserts the absence of *not mutated* instead |
| `seal/specs/1788936260-a-case-pins-what-it-actually-measures/phases/phase-3.md` | `survived` on either would read as *no case watches this* when the truth is *this was never tried*, so the report counts and names them separately. | The sentence's *either* is the match pattern and the bare `except:` named in the two clauses before it, so it is the same true statement about the same door. A phase record is a past-state account besides; the label round 2 changed is named in a dated addendum under this file's own §*What this phase found* rather than by rewriting what the phase measured |
| `seal/specs/1788936260-a-case-pins-what-it-actually-measures/phases/phase-3.md` | **An operator that could not be asked of an arm was invisible, and only the report's own arithmetic gave it away.** | The arm was `gh_segments:176`, whose `remove` mutation was a `SyntaxError` — an operator that genuinely could not be asked. What round 2 widened is the SECTION, which now also lists pairs that were asked and answered nothing; this passage is about the pair that could not be asked, and it stays that |
| `tests/test_arm_check.py` | def test_an_operator_that_could_not_be_asked_of_an_arm_is_named | The case's arm is a match-case pattern that has no mutation for either operator, so *could not be asked* is its subject and its name is accurate — `mutate` raises before anything is written, and the case asserts on `refused[0]`'s reason rather than on the report. **It never calls `_report`.** The section header, and the absence of *not asked* from it, are both asserted by a different case, `test_a_partly_skipped_operator_is_reported_without_refusing_the_arm`. The two together are what keep the wider list honest, and round 3's finding 25 is this cell having credited the first one with the second one's assertion |

**What would make these exemptions stop holding.** Each quote is the anchor. If
one of them comes to describe the timeout or spawn-failure door — an arm whose
mutation was written, run and restored — then *never tried* and *could not be
asked* are false of it and it is a genuine survivor.
