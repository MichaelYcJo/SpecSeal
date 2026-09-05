# the run outlives its last finding — questions for the planner

<!-- seal/specs/1788472135-the-run-outlives-its-last-finding/questions.md — decisions only
a human can make, extracted so nothing ships on a silent assumption. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Are #110's floor and #117's depth read by `chain_check.py`, or recorded for a person to read? | **Enforced** — the check refuses, grandfathered by work-item id. Costs a check that can go red on a branch nobody is watching, and buys a rule that holds while nobody is watching. **Recorded only** — the template gains the rows and the skills state the rule, and nothing reads them. This is the shape `Needs a fix` already has, and that row says of itself that no check reads it | Enforced | ✅ answered 2026-09-04 — **enforced**, with three conditions: older work items are excused the way `STRICT_FROM` and `SURFACE_FROM` excuse them; the place a refused unit goes is written before the check that refuses; every refusal is seen red before it ships |

The answer was given in the batch collected before the first edit, and the
reason is the one `CLAUDE.md` states above the rules: **verification through
an automated workflow is this project's first goal.** The question was asked
against a run nobody would be watching, and a row no check reads is only true
while somebody is awake. `Needs a fix` is the measurement rather than the
counterexample — it is honest because a reviewer answers it in the same
breath it is written, where these two rows are claims about work already
finished.

Nothing else is open. #97's three remaining levers each change pins that
already exist and each needs its own batch, which is why #117 was split out of
it and this branch carries only the lever that already had an answer.
