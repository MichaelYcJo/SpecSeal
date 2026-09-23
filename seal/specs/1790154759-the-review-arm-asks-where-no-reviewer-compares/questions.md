# 1790154759-the-review-arm-asks-where-no-reviewer-compares — questions for the planner

<!-- seal/specs/1790154759-the-review-arm-asks-where-no-reviewer-compares/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. -->

**Judgments the issue left open that the tree answered.** They are listed so
nobody reopens them as if they had not been met. `spec.md` holds the grounds
for each, and any of them can be overturned by opening what was opened.

- **Whether a lighter tier by paths is drawn at all** — no. The issue made this
  depend on one number: how many review rounds on docs/seal-only changes found
  a real defect. The number is not zero. The only such changes that reached a
  reviewer (#514's fold) produced seven fixed findings in `docs/`, one 🔴, and
  the docs/seal-only commits that never reached one were planning bookkeeping
  in `docs/flow.md`, retired on 2026-09-11. `spec.md` §*The measurement the
  issue asked for*, M1 to M4.
- **Which paths** (issue question 1) — none, by the answer above.
- **Where the list lives** (question 2) — there is no list.
- **Whether `DOC_ROOTS` becomes that list** (question 3) — no. It stays the
  parity arm's line.
- **What `chain_check` does with a pull request that has no declaration**
  (question 4) — it passes with a notice, read from `chain_check.py`'s module
  docstring. The lighter tier a person wants for a docs pass is the existing
  `straight to the PR` declaration.
- **Branch-name exemption** — refused by the issue, and nothing here reads a
  branch name.

**No row below blocks the build.** None needs a person.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should §*Review arm*'s decision table also gain the row it lacks for a `routing.md` declaration naming the branch? The quieter is in the code (`routed`) and in the wake/quiet table, and the section describes it in prose below the table, but the table itself lists three conditions | the work | **Add it** — phase 2 is editing that table anyway, and a table missing one of its quieters is what the wake/quiet table was built to end. **Leave it** — the prose below already covers it, and the phase stays narrower | Add it in phase 2, and say so in the phase record. Why the tree did not settle it: whether the prose below the table already serves as the row is a reading of that section that phase 2 makes while it edits the table | ⬜ |
| Q2 | Does A3 (a docs-only commit on a branch declared `straight to the PR` is silent) need a case of its own, or does an existing declaration case already cover it? | the work | **Cite an existing case** — a declaration silences the arm before any path is read, so the path adds nothing. **Plant a docs-only variant** — costs one case, and pins the absence of an interaction nobody has proposed | Cite the existing case. Why the tree did not settle it: the existing cases were located by name only, and which one fits is judged when phase 1 opens them | ✅ default taken 2026-09-23 by phase 1: cite `tests/test_routing_is_recorded.py#test_a_declared_direct_item_commits_without_a_prompt`. `routed` is decided in `hooks/commit-review-gate.py#judge` before anything reads a path, and the review arm's condition reads none, so a docs-only variant would pin nothing the existing case does not (`phases/phase-1.md`) |
| Q3 | Does M4's lower bound move the decision? The count skips findings whose Location cell cites no backticked path, and every verdict other than `fixed` | a measurement | A fuller count can only add findings, so it can only strengthen the refusal. No answer changes what gets built | Not taken. Why it is still a row: the spec states a lower bound, and this row says where the rest of the count went | ⬜ |
