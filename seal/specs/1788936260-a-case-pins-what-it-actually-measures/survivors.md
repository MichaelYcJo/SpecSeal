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
