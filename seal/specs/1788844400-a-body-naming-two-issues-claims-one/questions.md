# 1788844400-a-body-naming-two-issues-claims-one — questions

The routing batch was answered before this work item was spawned, for every
work item of 0.9.2 at once. Nothing below blocked the build; each is written
here rather than raised, per `skills/implement/SKILL.md` §1.

| # | Question | Who must answer |
|---|---|---|
| Q1 | Should the check ship to user repositories through `templates/hygiene.yml`? It rejects the same defect anywhere `Closes #N` is written, which is everywhere on GitHub — but the template's steps all call `skills/…` scripts from the plugin clone, and `.github/scripts/` is this repository's own automation by the convention `run_tests.py`'s docstring states and `tests/test_first_setup_asks_once.py#test_the_rows_that_read_this_repository_do_not_travel` already pins for `gather_changelog` and `fold_ledger`. Shipping it means first deciding it belongs under `skills/`. Assumed **no** and built that way; `plan.md` §*Alternatives considered* carries the reasoning, and a case pins the absence so it does not read as an oversight | the repository owner |
| Q2 | Should `pull_request: types:` gain `edited`, so a corrected body re-runs the check? Today a body fixed after the warning shows the stale warning until the next commit. Against it: `edited` fires on every title and body edit and re-runs every OTHER step of the job — the version check, the chain check, the mode check — which are gates, to refresh a warning. Assumed **no**: the warning is read once and correcting the body needs no green | the repository owner |
| Q3 | Should a closing keyword before a full issue URL (`https://github.com/o/r/issues/150`) count as a claim? GitHub reads one; this check reads `#N` only, so such a body is neither claimed nor mentioned here. This repository writes `#N`, and a second syntax is a second way to be wrong about it. Assumed **no**, and named in `plan.md` so the gap is on the record rather than discovered | the repository owner |
