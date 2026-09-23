- **A commit confined to `docs/` and `seal/` still meets the commit gate's
  review question, and the documents now say that is deliberate (issue
  #518).** The parity arm stays silent on those two directories because
  nothing there can be compared against an original. The review arm asks a
  different question — whether anybody reads the change before it lands — and
  it has no such line. The issue asked for a measurement before any line was
  drawn, and the measurement refused one: every docs-only change that reached
  a reviewer produced real defects in `docs/`, one of them 🔴, while the
  docs-only commits that never reached a reviewer were planning notes in a
  file retired on 2026-09-11. What the gate decides is unchanged.
  `docs/review-chain-spec.md` §*Review arm* gains a row for a docs-only change
  and a paragraph with the measurement, plus the row for a `routing.md`
  declaration that the table had left to the prose. The wake/quiet table in
  `skills/implement/orchestration.md` says the review arm wakes whatever the
  change touches. Cases fail if the parity arm's path line ever reaches the
  review arm. A documentation pass that should reach no reviewer declares
  `straight to the PR` before the first edit, as before.
