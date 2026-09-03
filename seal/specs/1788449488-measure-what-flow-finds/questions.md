# measure-what-flow-finds — questions for the planner

<!-- seal/specs/1788449488-measure-what-flow-finds/questions.md — decisions
only a human can make, extracted so nothing ships on a silent assumption.
Before adding a row, check the inheritance rule: if policy is silent but
existing behavior answers it, inherit and record — only genuinely NEW rules
belong here. -->

Routing (implementation / review / destination / branch) was answered before
the first edit — `routing.md`. Nothing else in issue #109's text or the
branch task needed a person: every open point the task raised was either
pre-decided by the task itself or a judgment the framer was explicitly asked
to make and record. Both judgments are recorded in `plan.md`'s own
"Judgment recorded" section rather than repeated here, since neither would
change what a phase builds if answered differently later (the version-title
enforcement question has a stated structural answer; the version-arithmetic
default has a stated fallback cost). This file exists so the shape is
present for later work, not because either judgment is blocking.

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should `roll_flow_measurement_issue.py`'s title-carries-a-version rule be enforced by a runtime check rather than structurally (the opener script always writes one)? | A — structural only, no gate (chosen; see `plan.md` Alternatives) · B — add a `chain_check.py`-style refusal once real issues exist to measure a check against | A | ✅ answered in `plan.md`, not blocking |
| Q2 | What is "the next version" when a release ships a patch (`X.Y.Z+1`) rather than a minor, and the bump-minor default guesses wrong? | A — accept the wrong guess; a human retitles the issue by hand, since nothing depends on the title being correct (chosen) · B — read `docs/flow.md`'s own roadmap headings to pick the real next version · C — read the release PR's own base-branch name convention if one existed | A | ✅ answered in `plan.md`, not blocking — flagged as a known limitation of the default, not a defect |

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges. Neither row above changes a policy
clause — both are local to the new script's own behaviour and are recorded
in this work item's own `plan.md` instead.
