# a segment's own wall clock is in no column — questions for the planner

<!-- seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

The routing batch was answered before the first edit and is committed in
`routing.md`: review through the review chain, the pull request opens, the
framer plans and `smith` builds. None of it is re-asked here.

**One row reaches a person and it does not block.** The other two are settled
by a probe inside the work, at the top of the phase that needs them. Sorting
them this way is what keeps the batch short enough to answer in one sitting —
a person's time is the wrong instrument for a question a command answers in
three seconds.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Now that the join exists, should `delegated_s` in the existing `--spawns` cycle table become the agent's own joined span? | **a person** — the repository owner. It changes what an already-published column means, and #145's `questions.md` §Q4 already assigned it to them | **Leave it** — `delegated_s` stays the `Agent` call's own tool_use-to-tool_result interval, which on this harness is seconds, and the agent's wall clock is read from the new per-segment table instead. Costs nothing and is what this plan builds. **Change it** — one arm in `#measure_cycles` once the join is a function, and every `--spawns` cycle reading published so far means something different with nothing on the page saying so; #200's repair is the precedent for what that then owes. The third answer in Q4's own table, *charge the wait*, is a guess at where the agent finished and is not improved by this work | **Leave it.** The number this work item produces is additive, so the owner can answer this after seeing one | ⬜ |
| Q2 | What marks a resume inside a segment transcript, and does the first slice still open at the spawn's result stamp? | **a measurement** — a probe over the transcripts already on this machine, at the top of phase 3 | `skills/verify/SKILL.md` §*Measure the segment* prescribes the hand split *at the user lines where the coordinator sent it a new message*, so the marker is named in the tree but has never been asserted against a file in code. The probe reads a resumed segment's transcript and reports what those rows actually look like — the row shape, whether a tool_result row is distinguishable from a coordinator message, and whether the file's first slice still matches its spawn | Split at coordinator message rows. Where the probe finds no reliable marker, phase 3's floor applies: one row, with the idle gap above the 900-second ceiling named in the report | ⬜ |
| Q3 | Is one second still the right join tolerance, on the current harness and for `specseal:*` agents? | **a measurement** — a probe over this machine's transcripts, at the top of phase 1 | The tolerance in the tree comes from 61 of 67 spawns across three runs of the 0.9.x line. The probe recomputes the opening-stamp-to-result-stamp distance over current transcripts and reports the distribution. A tolerance too tight loses a segment to the unnamed count; too loose and a batch of two spawns matches the wrong one. Either way the report prints the tolerance it used and the count on each side that went unmatched | 1.0 second, matched to the nearest spawn result, each spawn claimed at most once | ⬜ |

## Decided here rather than asked, with what each was chosen over

Both are in `spec.md` and `plan.md` in full. They are listed here so a reader
of this file alone does not take silence for an open question.

- **#343's shape is a line in the per-segment report**, chosen over a check
  and over a field the handover carries. Two of the three options are
  eliminated by facts rather than preference: a CI check has no transcript to
  read, since the evidence never leaves the machine that produced it, and a
  handover field asks the agent that broke the rule silently to disclose it —
  which is the delivery #343 says already worked. `spec.md` §*What #343's
  shape is, and what it was chosen over* holds the whole argument, including
  what the choice gives up.
- **The mode exits 0 whether or not it finds a spawn.** A measurement command
  that fails on a finding is a gate wearing the shape of a report, nothing
  reads its exit code today, and the orchestrator's own posting step would
  break on the finding it is meant to post.

## Assumptions taken, because a different answer would not change the build

- The flag is spelled `--segments` and `--json` gains a `segments` key beside
  `spawns`. A flag name is not a decision about behaviour, and #145's
  `questions.md` took the same assumption for `--spawns`.
- Each segment row's tokens cover that segment's own file only, with the run
  total summing the tree as it does today. Any other split would have to
  re-derive a number `token_totals` already produces correctly.
- The README rows are in scope in both editions. `--spawns` shipped without
  one, so this is a choice rather than a rule; it is taken because the READMEs
  are where a person outside an agent learns the command exists, and because a
  framing that names one edition and forgets the Korean one is this
  repository's measured omission.

Answered rows feed back into `docs/` (policy clause or open-questions section)
before this directory's work merges.
