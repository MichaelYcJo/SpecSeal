# a subagent rediscovers what the session established — questions

<!-- specs/1788224363-a-subagent-rediscovers-what-the-session-established/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | The `batching` advisory prints below 1.2 tools per turn. The pre-fix meter could not read above ~1.00, so the threshold was never really exercised; the corrected meter reads 1.08–1.89 on real segments, and issue #29's acceptance bar for a review segment is ≥ 2.0. Where does the advisory threshold sit? | **Keep 1.2** — the line stays a nudge for near-serial runs, and the wording now distinguishes exactly-1.00 ("one at a time") from above-1 ("most turns send a single call"). Costs nothing to a serial edit-test loop, which the contracts say is not forced to fake batching. **Raise to 2.0** — the advisory matches the acceptance bar, but then an inherently serial loop at 1.1 is told to batch on every run, which is the demand the smith's contract caveat exists to remove | Keep 1.2. The acceptance bar on the issue is for reviewing segments, where reads are independent; the script cannot tell a reviewer's transcript from an edit-test loop, so its advisory stays at the value that does not nag the serial case. Answered by: repository owner | ⬜ |

**Who answers Q1**: the repository owner — the threshold is a value every
future run is measured against, and the issue's own comment says a target is
a decision nobody has made yet ("1.00 is the measurement; nobody has said
what good looks like").

**Asked and answered before this file existed**: routing (all three axes, in
`routing.md`), the PR's target branch (`release/v0.0.2`), and the five-piece
scope — all by the repository owner on issue #29 and in the spawn
instruction. The batch before the first edit found nothing else only a
person can answer.
