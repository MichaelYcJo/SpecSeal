# arm-check reads every supported `ast` — questions for the planner

<!-- seal/specs/1790690762-arm-check-reads-every-supported-ast/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row here blocks the build.** The ticket and the spawn left these
judgments open, and the tree answered each of them. They are listed so nobody
reopens them, each with where its grounds are, so a reviewer can overturn one
by opening the same place.

## Decided from the tree

| # | Judgment | Answer | Grounds |
|---|---|---|---|
| J1 | Does an `Interpolation` carry an arm, the way an f-string's replacement field might? | No. `TemplateStr` and `Interpolation` join `JoinedStr` and `FormattedValue` in the group "an expression that computes a value and forks on nothing" | spec M3: the `IfExp` inside an interpolation is found by the walk as one arm, the same as in the f-string, and the `BoolOp` value is not an arm, the same as `BoolOp` anywhere. `str` is a plain string and `conversion` an integer. plan.md §*Alternatives*, I |
| J2 | How the stale-name case judges a name the floor has and the running Python lacks, and the reverse | Each such name carries the first Python that has it and the first that no longer does. On any Python, a name placed there must be in `ast`, and a name placed elsewhere must not be | spec S4, plan.md §*Alternatives*, A against B and C. Both directions of the old case survive, and a wrong range is red on the Python it misdescribes |
| J3 | Where the ranges live | In `arm_check.py`, beside `CLASSIFIED` | plan.md §*Alternatives*, J |
| J4 | Should the cases run on more than one interpreter, and how | Yes, in CI: a job after `ledger` runs `tests/test_arm_check.py` at 3.13 and 3.14. S6 holds every range bound to a version some job runs the module at | plan.md §*Alternatives*, A against D. A check that skips on every CI runner is not unattended (`CLAUDE.md` §*The goal a design is chosen against*) |
| J5 | Is `run_tests.py` picking the newest interpreter part of the defect? | No, and it is not changed | spec §*Scope*, out: its docstrings, `CONTRIBUTING.md` and `build`'s `>=` all state the floor or newer as intent, and it is the only run that met this defect |
| J6 | The whole suite on 3.13 or 3.14 in CI | Out of this item | spec §*Scope*, out, and plan.md §*Alternatives*, F: the `pytest` job's floor rule is pinned by a case, and whether the suite is green on 3.14 is Q1 |
| J7 | Which versions the new job pins | `3.13` and `3.14`, not a floating `3.x` | plan.md §*Alternatives*, H. The owner may still want a non-blocking floating leg (Q3) |
| J8 | Where the new job goes in `test.yml` | After `ledger` | `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#test_ci_runs_the_suite_at_the_floor_the_runner_holds` reads from `  pytest:` to `  ledger:` and requires the floor alone there |
| J9 | The stale matrix comment about 3.13 (spec M7) | Rewritten in this item | This item is what gives CI a 3.13 run. The comment names a leg that never existed |
| J10 | `CONTRIBUTING.md`'s "CI runs four jobs" | Rewritten to name the new job, with no second mention of the floor number | the section's `FLOOR_TEXT` count case (plan.md §*Technical context*) |
| J11 | The 0.9.5 ledger row claiming totality over "this interpreter's" 122 constructors | `Corrected` in place, new claims in this item's fragment | plan.md §*Ledger*; `CLAUDE.md` §*Repo rule — a change writes fragments* |
| J12 | Where the changelog bullet goes | `### Fixed` | A plugin user's `arm-check` refused valid code on 3.14. Nothing refuses more afterwards (spec §*Failure direction*) |

## Rows still open

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Is the whole suite green on 3.14, apart from `tests/test_arm_check.py`? #684 reports one module, and nobody in the tree has recorded a whole run on 3.14. The tree cannot answer it: it is a broad run, which the framer and the builder do not take | a measurement | The sealer's broad gate in this worktree runs on the 3.14 `.venv` that `bin/test` builds here (spec M5), so it answers this. Green: plan.md §*Alternatives* F has its ground for a later item. Red elsewhere: a new issue for each module, not this item's | The build does not wait on it. A red outside `tests/test_arm_check.py` at the broad gate goes to the orchestrator as a new issue | ⬜ |
| Q2 | Should the new CI job be a required status check? The rulesets are GitHub settings and not in the tree, so nothing here can read or change them | a person — the repository owner | Required: a red leg blocks the merge like the `pytest` legs do. Not required: the job reports and a reviewer reads it. The code built is the same either way | Unchanged rulesets. The job runs on every pull request and its result is visible | ⬜ |
| Q3 | Should a floating newest-Python leg (`3.x`, perhaps with `allow-prereleases`) run beside the pinned ones, so 3.15's grammar is seen without anybody adding a leg? The tree cannot choose between a verdict that can move without a commit and a leg someone must remember to add | a person — the repository owner | Floating and blocking: a new Python can turn every open pull request red on its release day. Floating with `continue-on-error`: it warns without blocking, and a warning can be ignored. Pinned only (this item): nothing is red until someone adds 3.15, and S6 makes that addition complete | Pinned only. Adding a floating leg later is one matrix entry and does not touch S6 | ⬜ |
| Q4 | The range table's name and exact shape | the work | Any shape that gives, per name, the first Python having it and the first lacking it, either end open, with minor-version tuples | spec §*Data & interfaces*'s suggested shape. The phase record says what was chosen | ⬜ |
| Q5 | Which fixture S2 uses, and whether one module covers every interpolation feature at once | the work | One module holding an `IfExp`, a `BoolOp` value, a comprehension guard, a conversion and a nested format field, or one case per feature | One module, so the f-string twin is one text substitution | ⬜ |
