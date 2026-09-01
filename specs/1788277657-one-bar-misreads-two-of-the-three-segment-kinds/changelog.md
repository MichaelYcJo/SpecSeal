- **The per-segment acceptance bars are written rules, and one bar no longer
  misreads two of the three segment kinds.** The meter the handoff protocol
  points at (`session_cost.py`) had numbers and no rule about what they mean;
  the one figure that existed anywhere was a single acceptance bar on an
  issue, right for a reviewing segment and wrong for the other two. The
  protocol (draft 0.8, §After the run) now says it: a reviewing segment is
  judged on tools per turn **≥ 1.8** (measured range 1.29–1.89, the batched
  round at 1.89 the fastest); an implementing segment on **`repeats = 0`**
  and calls per deliverable, never on tools per turn — an edit-test loop is
  inherently serial (1.08–1.17 measured); a verifying segment is exempt. At
  very small rounds the ratio has few independent batches to rise on (a
  23-call round read 1.64 doing everything right), so the bar is a lens for
  rounds of ordinary size, never a refusal threshold — no gate fails a round
  on it. (#51)

- **A fix pass resumes the implementer instead of respawning it.** The
  code-review skill's orchestrator sections said when the verifying round
  runs and nothing about how the fixing session is obtained. Now they do:
  resume the session that built the branch — its context already holds the
  files, the tests, and the grounds — and spawn fresh only when that session
  no longer exists, with the handoff before round 1 as the price. Measured
  three times with no counterexample: fresh spawn 282 calls / 45 minutes
  (#33); resume 30 calls / 3.9 minutes (#29) and 26 calls / 5.2 minutes
  (the #57 chain). (#51)

- **Q1 of the meter work item is answered: the advisory stays at 1.2.** The
  script cannot tell a reviewer's transcript from an edit-test loop, so its
  threshold sits where it does not nag the serial case; the bars above are
  the orchestrator's instrument, applied knowing the segment kind.
  `session_cost.py` itself is unchanged. (#51)
