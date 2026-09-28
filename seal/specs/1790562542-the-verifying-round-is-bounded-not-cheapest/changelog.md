- **No document calls the verifying round the cheapest round of the run any
  more (issue #639).** Three documents said so because its target is a diff,
  and `agents/warden.md` said its surface was the whole reason it was
  affordable. The measurements do not hold that. #456 measured nine rounds
  over three work items at 13.8–17.8 minutes whatever their target, and over
  0.14.0–0.15.5, 29 verifying rounds ran at a median of 0.83 × their own
  round 1, with five of the 29 at or above it. What a round spends is the
  frame, the earlier records and the probes, and none of those shrink with
  the diff. The four places now say that the diff target bounds the round
  and does not make it cheap. `docs/review-chain-spec.md` is the one place
  the figure and its sources are printed, and the orchestrator's table points
  there. The warden is told to stay inside the diff because of the round's
  job, which is answering whether each closed verdict is closed. It is not
  told the diff makes the round cheap. The per-segment bars keep the verifying
  segment `exempt`. Its grounds now name that job and #51 observation 1,
  where the exemption was recorded, and no longer claim cost or size: #456's
  verifying rounds took 46–58 calls, which is not "a segment that small". The
  durable baseline log, #51, was corrected in step. A new test module holds
  each of the four places to its corrected wording and to the absence of the
  old wording, and fails if the phrase comes back anywhere under `agents/`,
  `skills/`, `docs/`, `templates/` or either README. The rule itself is
  unchanged: when the round runs, what it targets, what it does and when it
  ends the run.
- **#81's round 1 is no longer called the cheapest round on record.** It was
  not the cheapest when the sentence was written. #89, the log that measured
  it, already held #79's verifying round at 5.6 minutes and 28 calls, and
  #51's baseline held #29's at 4.2 minutes and 10. What #89 measured for it,
  five defects in 29 tool calls where #82's six rounds averaged three times
  the calls for fewer, is what `skills/code-review/SKILL.md` and the
  `templates/sdd-round.md` comment now say. Both carriers are pinned. The
  released 0.7.0 entry still says it, and is left as written.
